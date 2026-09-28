//! `folio graph --print --summary`（便 180・docs/design/delivery-180.md §1 (c)・要件 FR14 第 1.52 版）の歯。folio は
//! 実行 file の crate なので命令を撃つ。
//! 1. 実の正本で、節点の表の各行に 1 行ずつ同じ順・同じ id・種類・file・題で出て、line の行にその id が書かれている。
//! 2. 凍結した土台の写しの 8 節点の行が、歯の側に手で書いた字（凍結 anchor・P-10.1）と一致する（受入基準の技術の要約は
//!    題の全文）。
//! 3. タブ・改行・引用符・逆斜線・制御の字と `|` の塊（複数行・末尾の改行）を持つ欄が JSON の escape で 1 行に収まり、
//!    技術の要約の欄の順（shall・text・what・decision・空の値は飛ばす）と条の「最初の規範文」と受入基準の題の全文
//!    （畳まず切らない）が守られる。期待の字はどれも歯の側の手書き（凍結 anchor・P-10.1 / P-10.2）。
//! 4. 組めない置き場では 1 行も出さずに まだ分からない（終了コード 2）。--summary は --print と一緒のときだけ。
//! 5. --summary の口が在っても、--summary の無い --print と --digest の出力は凍結 anchor のまま（土台の写し）。
//! 6. 行の末尾の rulings（便 201・判断の記録 ADR-35・要件 FR14 第 1.56 版）は、節点が持つ決定の欄の裁定 id を書き出しと同じ組
//!    （ruling・form・bead）で欄の順・切り出した順に並べ、節点を持たない欄と字でない欄は何も付けない。
//! 7. 設計ノートの行はノートの承認欄の全部の行を継ぎ、判断の表の行は継がない。
//! 8. 全部の節点の rulings が、同じ置き場の folio check --emit-rulings の行から組んだ期待と一致する。

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::{Command, Output, Stdio};

const EDGES_HEAD: &str = "# 辺（1 行 = 端 / 端 / 型・タブ区切り）";
const FLOOR_BASE: &str = "tests/fixtures/floor_base/design-intent";

fn repo_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
}

fn copy_tree(src: &Path, dst: &Path) {
    fs::create_dir_all(dst).unwrap();
    for entry in fs::read_dir(src).unwrap() {
        let entry = entry.unwrap();
        let to = dst.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_tree(&entry.path(), &to);
        } else {
            fs::copy(entry.path(), &to).unwrap();
        }
    }
}

/// 凍結した土台 tests/fixtures/floor_base/design-intent の写しの一時 dir（歯の終わりに消す）。
struct Work {
    root: PathBuf,
}

impl Work {
    fn base(case: &str) -> Work {
        let root = std::env::temp_dir().join(format!("folio-graph-summary-{case}-{}", std::process::id()));
        let _ = fs::remove_dir_all(&root);
        copy_tree(&repo_root().join(FLOOR_BASE), &root.join("design-intent"));
        Work { root }
    }

    /// 写しの file の中の `from`（ちょうど 1 か所）を `to` に替える。
    fn replace(&self, file: &str, from: &str, to: &str) {
        let path = self.dir().join(file);
        let text = fs::read_to_string(&path).unwrap();
        assert_eq!(text.matches(from).count(), 1, "{file}: 「{from}」が 1 か所でない");
        fs::write(&path, text.replacen(from, to, 1)).unwrap();
    }

    fn dir(&self) -> PathBuf {
        self.root.join("design-intent")
    }
}

impl Drop for Work {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}

fn graph(dir: &Path, flags: &[&str]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_folio"))
        .arg("graph")
        .args(flags)
        .arg("--dir")
        .arg(dir)
        .output()
        .expect("folio を起動できない")
}

fn passed(out: Output) -> String {
    assert_eq!(out.status.code(), Some(0), "{}", String::from_utf8_lossy(&out.stderr));
    String::from_utf8(out.stdout).expect("出力が UTF-8 でない")
}

fn summary(dir: &Path) -> String {
    passed(graph(dir, &["--print", "--summary"]))
}

/// 歯の側の JSON の字の書き方（引用符・逆斜線・制御の字だけを逃がす・非 ASCII はそのまま）。
fn quoted(s: &str) -> String {
    let mut out = String::from("\"");
    for c in s.chars() {
        match c {
            '"' | '\\' => {
                out.push('\\');
                out.push(c);
            }
            '\n' => out.push_str("\\n"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

/// 出力の中の id の行（ちょうど 1 行）。
fn line_of<'a>(text: &'a str, id: &str) -> &'a str {
    let head = format!("{{\"id\":{},", quoted(id));
    let found: Vec<&str> = text.lines().filter(|l| l.starts_with(&head)).collect();
    assert_eq!(found.len(), 1, "{id} の行の数");
    found[0]
}

/// 要約値（sha256）は命令 `sha256sum` を子の処理で撃って測る（歯は crate の中を読めない・tests/graph.rs と同じ形）。
fn sha256_hex(bytes: &[u8]) -> String {
    let mut child = Command::new("sha256sum")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .expect("sha256sum を起動できない");
    child.stdin.take().unwrap().write_all(bytes).unwrap();
    let out = child.wait_with_output().unwrap();
    String::from_utf8_lossy(&out.stdout)
        .split_whitespace()
        .next()
        .unwrap_or_default()
        .to_string()
}

#[test]
fn f180_each_node_of_the_print_has_one_line() {
    let dir = repo_root().join("design-intent");
    let print = passed(graph(&dir, &["--print"]));
    let text = summary(&dir);
    assert!(text.ends_with('\n') && !text.contains(['\t', '\r']), "JSON Lines でない");
    let rows: Vec<&str> = print.lines().skip(1).take_while(|l| *l != EDGES_HEAD).collect();
    let lines: Vec<&str> = text.lines().collect();
    assert!(!rows.is_empty());
    assert_eq!(lines.len(), rows.len(), "節点の表の行の数と 1 行ずつでない");
    for (row, line) in rows.iter().zip(&lines) {
        let cols: Vec<&str> = row.split('\t').collect();
        let (id, kind, file, title) = (cols[0], cols[1], cols[2], cols[4]);
        let head = format!("{{\"id\":{},\"kind\":{},\"file\":{},\"line\":", quoted(id), quoted(kind), quoted(file));
        let rest = line.strip_prefix(&head).unwrap_or_else(|| panic!("表の {row} と頭が違う: {line}"));
        let digits: String = rest.chars().take_while(char::is_ascii_digit).collect();
        let n: usize = digits.parse().unwrap_or_else(|_| panic!("line が数でない: {line}"));
        let next = format!(",\"title\":{},\"plain\":", quoted(title));
        assert!(rest[digits.len()..].starts_with(&next), "題が表と違う: {line}");
        assert!(line.contains(",\"eng\":") && line.ends_with('}'), "{line}");
        let source = fs::read_to_string(dir.join(file)).unwrap();
        let at = source.lines().nth(n.checked_sub(1).expect("line が 0")).expect("line が file の外");
        // 設計ノートの行（便 185）の id は「文書 id#行 id」で、書かれているのは行 id
        let key = format!("id: {}", id.rsplit('#').next().unwrap_or(id));
        let written = at.match_indices(&key).any(|(i, _)| {
            matches!(at[i + key.len()..].chars().next(), None | Some(',' | '}' | ' '))
        });
        assert!(written, "{file} の {n} 行目に {key} が無い: {at}");
    }
}

#[test]
fn f180_the_frozen_base_lines_are_the_hand_written_ones() {
    let text = summary(&repo_root().join(FLOOR_BASE));
    for want in [
        r#"{"id":"N-3","kind":"条","file":"constitution.yaml","line":463,"title":"例外の仕組みを作らない","plain":"「今回だけ特別」のスイッチを足す変更は、機械が止めます。変えたいときは正式に改訂します。","eng":"変更が規則の例外機構（無効化の旗・「今回だけ」の口）を足すなら、それを拒む。","rulings":[]}"#,
        r#"{"id":"P-6.2","kind":"規範文","file":"constitution.yaml","line":201,"title":"生成物を手で直さない。","plain":null,"eng":"生成物を手で直さない。","rulings":[]}"#,
        r#"{"id":"R-5","kind":"規則行","file":"rules.yaml","line":33,"title":"密度 profile と図の型の数","plain":null,"eng":"密度 profile と図の型の数","rulings":[{"ruling":"f2-648","form":"bead","bead":"f2-648"},{"ruling":"f2-648.6","form":"bead","bead":"f2-648.6"}]}"#,
        r#"{"id":"FR8","kind":"要件","file":"srs.yaml","line":195,"title":"途中で足す窓口","plain":"あとから「やっぱりこの文書も」となっても、最初からやり直さず、差分だけ相談します。","eng":"folio は差分だけを対象に intake を再実行し、支度表を更新する。","rulings":[]}"#,
        r#"{"id":"AC12","kind":"受入基準","file":"srs.yaml","line":409,"title":"検査を通らない図は生成されず、前の生成物が残る","plain":"わざと崩れた図の記述を入れて走らせ、図が作られず前の図がそのまま残ることを見せる。","eng":"検査を通らない図は生成されず、前の生成物が残る","rulings":[]}"#,
        r#"{"id":"AC11","kind":"受入基準","file":"srs.yaml","line":406,"title":"印の無い commit の契約は「まだ分からない」と出て「未着地」と出な","plain":"便が入ったかを示す印が無いとき、「まだ分からない」と表示され「入っていない」とは表示されないことを見せる。","eng":"印の無い commit の契約は「まだ分からない」と出て「未着地」と出ない","rulings":[]}"#,
        r#"{"id":"folio-v2","kind":"登場人物","file":"srs.yaml","line":92,"title":"folio v2","plain":null,"eng":null,"rulings":[]}"#,
    ] {
        let id = want.split('"').nth(3).unwrap();
        assert_eq!(line_of(&text, id), want);
    }
    // 判断の記録は file の頭の注の後の id の行・技術の要約は決定の欄
    let adr = line_of(&text, "ADR-9");
    let head = r#"{"id":"ADR-9","kind":"判断の記録","file":"adr/ADR-9.yaml","line":5,"title":"欄の決まりの file（判断の記録・設計ノート）の schema 節は床","plain":"「判断の記録の書き方」と"#;
    assert!(adr.starts_with(head), "{adr}");
    assert!(adr.contains(r#","eng":"欄の決まりの file 2 本（adr/schema.yaml・design-note/schema.yaml）のうち schema 節"#), "{adr}");
}

#[test]
fn f180_text_fields_are_escaped_into_one_json_line() {
    let work = Work::base("escape");
    work.replace(
        "srs.yaml",
        "    shall: folio は差分だけを対象に intake を再実行し、支度表を更新する。\n    plain: あとから「やっぱりこの文書も」となっても、最初からやり直さず、差分だけ相談します。\n",
        "    shall: folio は差分だけを対象に intake を再実行し、支度表を更新する。\n    text: 本文の欄（規範文の欄が先）\n    plain: \"タブ\\tと改行\\nと \\\"引用符\\\" と \\\\ 逆斜線と \\u0001 制御の字\"\n",
    );
    work.replace(
        "srs.yaml",
        "  - {id: folio-v2, name: folio v2, role: 道具}\n",
        "  - {id: folio-v2, name: folio v2, role: 道具, shall: ~, decision: 決定の欄, what: \"what の欄 \\\"x\\\"\", plain: ~}\n",
    );
    work.replace(
        "constitution.yaml",
        "      - {id: N-3.1, ",
        "      - {pattern: unwanted, text: id の無い行は規範文でない}\n      - {id: N-3.1, ",
    );
    work.replace(
        "srs.yaml",
        "  - {id: AC12, title: 検査を通らない図は生成されず、前の生成物が残る, ",
        "  - {id: AC12, title: \"検査を通らない図は  生成されず、\\n前の生成物が残る（題を 36 字で切らず、空白も畳まない全文）\", ",
    );
    work.replace(
        "constitution.yaml",
        "    plain: 「今回だけ特別」のスイッチを足す変更は、機械が止めます。変えたいときは正式に改訂します。\n",
        "    plain: |\n      「今回だけ特別」のスイッチを足す変更は、\n      機械が止めます。\n",
    );
    work.replace("rules.yaml", "  - {id: R-5, article: P-2, what: ", "  - {id: R-5, article: P-2, text: 本文が what より先, what: ");
    let text = summary(&work.dir());
    let print = passed(graph(&work.dir(), &["--print"]));
    let rows = print.lines().skip(1).take_while(|l| *l != EDGES_HEAD).count();
    assert_eq!(text.lines().count(), rows, "字の中の改行で行が割れた");
    assert!(!text.contains('\t'), "字の中のタブが逃がされていない");
    assert_eq!(
        line_of(&text, "FR8"),
        r#"{"id":"FR8","kind":"要件","file":"srs.yaml","line":195,"title":"途中で足す窓口","plain":"タブ\tと改行\nと \"引用符\" と \\ 逆斜線と \u0001 制御の字","eng":"folio は差分だけを対象に intake を再実行し、支度表を更新する。","rulings":[]}"#
    );
    assert_eq!(
        line_of(&text, "folio-v2"),
        r#"{"id":"folio-v2","kind":"登場人物","file":"srs.yaml","line":92,"title":"folio v2","plain":null,"eng":"what の欄 \"x\"","rulings":[]}"#
    );
    // `|` の塊の平易文は複数行と末尾の改行ごと・条の技術の要約は id を持つ最初の規範文の字
    assert_eq!(
        line_of(&text, "N-3"),
        r#"{"id":"N-3","kind":"条","file":"constitution.yaml","line":463,"title":"例外の仕組みを作らない","plain":"「今回だけ特別」のスイッチを足す変更は、\n機械が止めます。\n","eng":"変更が規則の例外機構（無効化の旗・「今回だけ」の口）を足すなら、それを拒む。","rulings":[]}"#
    );
    // 本文の欄 text は what より先
    assert_eq!(
        line_of(&text, "R-5"),
        r#"{"id":"R-5","kind":"規則行","file":"rules.yaml","line":33,"title":"密度 profile と図の型の数","plain":null,"eng":"本文が what より先","rulings":[{"ruling":"f2-648","form":"bead","bead":"f2-648"},{"ruling":"f2-648.6","form":"bead","bead":"f2-648.6"}]}"#
    );
    assert!(
        line_of(&text, "AC12").ends_with(r#","title":"検査を通らない図は 生成されず、 前の生成物が残る（題を 36 字で切ら","plain":"わざと崩れた図の記述を入れて走らせ、図が作られず前の図がそのまま残ることを見せる。","eng":"検査を通らない図は  生成されず、\n前の生成物が残る（題を 36 字で切らず、空白も畳まない全文）","rulings":[]}"#),
        "受入基準の技術の要約が題の全文でない"
    );
}

#[test]
fn f180_an_unbuildable_index_prints_no_line() {
    let gone = Work::base("gone");
    fs::remove_file(gone.dir().join("srs.yaml")).unwrap();
    let broken = Work::base("disagree");
    broken.replace("constitution.yaml", "      - {id: P-1.1, ", "      -  {id: P-1.1, ");
    for (dir, why) in [(gone.dir(), "srs.yaml を読めない"), (broken.dir(), "食い違う")] {
        let out = graph(&dir, &["--print", "--summary"]);
        let err = String::from_utf8_lossy(&out.stderr);
        assert_eq!(out.status.code(), Some(2), "{err}");
        assert!(out.stdout.is_empty(), "行が出た: {}", String::from_utf8_lossy(&out.stdout));
        assert!(err.contains("まだ分からない") && err.contains(why), "{err}");
    }
    let dir = repo_root().join(FLOOR_BASE);
    for flags in [&["--summary"][..], &["--digest", "--summary"]] {
        let out = graph(&dir, flags);
        assert_eq!(out.status.code(), Some(2), "{flags:?}");
        assert!(out.stdout.is_empty(), "{flags:?}");
    }
    assert_eq!(passed(graph(&dir, &["--summary", "--print"])), summary(&dir), "旗の順で出力が変わった");
}

#[test]
fn f180_the_summary_leaves_the_print_and_the_digest_on_their_anchors() {
    let dir = repo_root().join(FLOOR_BASE);
    assert!(summary(&dir).starts_with("{\"id\":"), "--summary が節点ごとの行を出さない");
    let anchor = fs::read_to_string(repo_root().join("tests/fixtures/schema/graph-anchor.txt")).unwrap();
    let whole = anchor
        .lines()
        .find_map(|l| l.strip_prefix("出力全体 sha256 = "))
        .expect("anchor に出力全体の行が無い");
    let print = passed(graph(&dir, &["--print"]));
    assert_eq!(sha256_hex(print.as_bytes()), whole[..64], "--print の出力が anchor と違う");
    let digest = fs::read(repo_root().join("tests/fixtures/schema/graph-digest-anchor.txt")).unwrap();
    assert!(passed(graph(&dir, &["--digest"])).as_bytes() == digest.as_slice(), "--digest の出力が anchor と違う");
}

// ── 便 201（docs/design/delivery-201.md §1・判断の記録 ADR-35・要件 FR14 第 1.56 版）: 節点の裁定 id の一覧 rulings ──

/// 3 つの形の裁定 id を 1 つの欄に持つ字と、その rulings の字（歯の側の手書き・便 181 の歯と同じ形）。
const THREE: &str = "t3-hub.56:20260927T2259Z-1・f2-648 notes 2026-09-28 07:18 JST（t3-hub.1）";
const THREE_JSON: &str = r#"[{"ruling":"t3-hub.56:20260927T2259Z-1","form":"question","bead":"t3-hub.56"},{"ruling":"f2-648 notes 2026-09-28 07:18 JST","form":"notes-time","bead":"f2-648"},{"ruling":"t3-hub.1","form":"bead","bead":"t3-hub.1"}]"#;

/// 承認欄の 2 行と判断の表の行を持つ設計ノート（契約表の行 x・y は承認欄を継ぎ、判断の表の行 d の裁定は継がない）。
const RULED_NOTE: &str = "meta:
  id: ruled
  title: 承認欄を持つノート
  version: v1.0
  status: effective
  generated: 2026-09-28
  profile: design-note
  approval:
    - {who: 持ち主, date: 2026-09-28, ruling: \"t3-hub.1（裁定 id = t3-hub.58:20260927T2357Z-1・board）\", verbatim: 承認する, surface: R-8}
    - {who: 持ち主, date: 2026-09-28, ruling: f2-648.270 notes 2026-09-28 16:13 JST, verbatim: 承認する, surface: R-8}
sections:
  - n: 1
    type: prose
    title: 行 x
    body: |
      x。
  - n: 2
    type: contract-table
    title: 契約表
    rows:
      - {id: x, title: 行 x の題, req: [FR1], section: \"1\"}
      - {id: y, title: 行 y の題, req: [FR2], section: \"1\"}
  - n: 3
    type: decision-table
    title: 判断の表
    rows:
      - {id: d, text: 判断, ruling: s2-07l.999}
";

/// 行の rulings の字（行の末尾の `,"rulings":` の後から閉じの `}` の前まで）。
fn rulings_of<'a>(text: &'a str, id: &str) -> &'a str {
    let line = line_of(text, id);
    let at = line.rfind(",\"rulings\":[").unwrap_or_else(|| panic!("{id} の行に rulings が無い: {line}"));
    line[at + ",\"rulings\":".len()..].strip_suffix('}').expect("行の終わりが } でない")
}

/// 裁定の欄を書き換えた土台の写し（歯 1・歯 3 が使う）。
fn ruled_work(case: &str) -> Work {
    let work = Work::base(case);
    work.replace(
        "rules.yaml",
        "ruling: \"申告 B（初版 2026-09-12）・ADR-4 発効承認 2026-09-16 22:5x JST（f2-648 notes・f2-648.6 notes・逐語「いずれも承認する」）\"",
        &format!("ruling: \"{THREE}\""),
    );
    work.replace(
        "rules.yaml",
        "（直接／間接の本数・ライセンスの許可一覧）, value: 未定, kind: deny, status: 未定, ruling: 発効承認 2026-09-12（f2-648.1 notes・P-17.3）",
        "（直接／間接の本数・ライセンスの許可一覧）, value: 未定, kind: deny, status: 未定, ruling: [f2-648.1]",
    );
    work.replace(
        "constitution.yaml",
        "    plain: 「今回だけ特別」のスイッチを足す変更は、機械が止めます。変えたいときは正式に改訂します。\n",
        "    plain: 「今回だけ特別」のスイッチを足す変更は、機械が止めます。変えたいときは正式に改訂します。\n    amended_by:\n      - {adr: ADR-9, ruling: \"f2-648 notes 2026-09-20 00:09 JST・t3-hub.2\"}\n",
    );
    work.replace(
        "adr/ADR-10.yaml",
        "ruling: f2-648 notes 2026-09-19 20:1x JST（発効の承認・判断の記録 ADR-9・ADR-10 と天井の正本 第 2 版（v0.2）を 1 つの承認で発効する承認要求への回答）",
        "ruling: 未記入",
    );
    fs::write(work.dir().join("design-note/ruled.yaml"), RULED_NOTE).unwrap();
    work
}

/// 歯 1（便 201）: 節点の rulings は、その節点が持つ決定の欄（規則の表の行・判断の記録の承認欄・条の改訂来歴）から、書き出しと
/// 同じ形の組（ruling・form・bead）で欄の順・切り出した順に並ぶ。値が字でない欄と未記入の欄と、節点を持たない欄（憲法の発効の
/// 承認・要件書の承認欄の stamp）は何も付けず、条の改訂来歴はその条の規範文に付けない。期待の字は歯の側の手書き。
#[test]
fn f201_rulings_are_cut_from_the_decision_fields_of_the_node() {
    let base = summary(&repo_root().join(FLOOR_BASE));
    assert_eq!(
        rulings_of(&base, "R-5"),
        r#"[{"ruling":"f2-648","form":"bead","bead":"f2-648"},{"ruling":"f2-648.6","form":"bead","bead":"f2-648.6"}]"#
    );
    assert_eq!(rulings_of(&base, "ADR-9"), r#"[{"ruling":"f2-648 notes 2026-09-19 20:1x JST","form":"notes-time","bead":"f2-648"}]"#);
    let work = ruled_work("cut");
    let text = summary(&work.dir());
    assert_eq!(rulings_of(&text, "R-5"), THREE_JSON);
    assert_eq!(
        rulings_of(&text, "N-3"),
        r#"[{"ruling":"f2-648 notes 2026-09-20 00:09 JST","form":"notes-time","bead":"f2-648"},{"ruling":"t3-hub.2","form":"bead","bead":"t3-hub.2"}]"#
    );
    assert_eq!(rulings_of(&text, "ADR-9"), rulings_of(&base, "ADR-9"));
    for none in ["R-6", "ADR-10", "N-3.1", "P-1", "P-6.2", "FR8", "AC12", "folio-v2"] {
        assert_eq!(rulings_of(&text, none), "[]", "{none}");
    }
}

/// 歯 2（便 201）: 設計ノートの契約表の行は、そのノートの承認欄の全部の行の裁定 id を継ぐ（行の順・切り出した順）。判断の表の
/// 行の裁定と、承認欄の無いノートの行（土台の example#a）は継がない。承認欄の行を消すとその裁定 id だけが消える。
#[test]
fn f201_note_rows_inherit_the_approval_of_their_note() {
    let work = ruled_work("note");
    let text = summary(&work.dir());
    let want = r#"[{"ruling":"t3-hub.1","form":"bead","bead":"t3-hub.1"},{"ruling":"t3-hub.58:20260927T2357Z-1","form":"question","bead":"t3-hub.58"},{"ruling":"f2-648.270 notes 2026-09-28 16:13 JST","form":"notes-time","bead":"f2-648.270"}]"#;
    assert_eq!(rulings_of(&text, "ruled#x"), want);
    assert_eq!(rulings_of(&text, "ruled#y"), want);
    assert_eq!(rulings_of(&text, "example#a"), "[]");
    assert!(!text.contains("s2-07l.999"), "判断の表の行の裁定を継いだ");
    work.replace(
        "design-note/ruled.yaml",
        "    - {who: 持ち主, date: 2026-09-28, ruling: f2-648.270 notes 2026-09-28 16:13 JST, verbatim: 承認する, surface: R-8}\n",
        "",
    );
    let fewer = summary(&work.dir());
    assert_eq!(rulings_of(&fewer, "ruled#x"), want.replace(r#",{"ruling":"f2-648.270 notes 2026-09-28 16:13 JST","form":"notes-time","bead":"f2-648.270"}"#, ""));
}

/// 書き出しの 1 行（`{"ruling":…,"form":…,"bead":…,"node":…,"file":…,"line":…,"field":…}`）を、組の字と node と file と
/// field に分ける（JSON の字の中の引用符は逃がされているので、区切りの字は字の中に出ない）。
fn split_emit(line: &str) -> (String, Option<&str>, &str, &str) {
    let (pair, rest) = line.split_once(",\"node\":").expect("node の欄が無い");
    let (node, rest) = rest.split_once(",\"file\":\"").expect("file の欄が無い");
    let (file, rest) = rest.split_once("\",\"line\":").expect("line の欄が無い");
    let field = rest.split_once(",\"field\":\"").and_then(|(_, f)| f.strip_suffix("\"}")).expect("field の欄が無い");
    let node = node.strip_prefix('"').and_then(|n| n.strip_suffix('"'));
    (format!("{pair}}}"), node, file, field)
}

/// 歯 3（便 201・条 P-6.3）: 実の正本と裁定の欄を書き換えた写しの両方で、全部の節点の rulings が、同じ置き場の
/// folio check --emit-rulings の行から組んだ期待（node を持つ行はその節点へ・設計ノートの承認欄の行は同じ file の設計ノートの
/// 行の全部へ・行の順）と一致する（切り出しの読み手が 1 つ）。
#[test]
fn f201_rulings_agree_with_the_emitted_rulings() {
    let work = ruled_work("agree");
    for dir in [repo_root().join("design-intent"), work.dir()] {
        let text = summary(&dir);
        let out = Command::new(env!("CARGO_BIN_EXE_folio"))
            .args(["check", "--emit-rulings", "--dir"])
            .arg(&dir)
            .output()
            .unwrap();
        let emitted = String::from_utf8(out.stdout).unwrap();
        let rows = |file: &str| -> Vec<String> {
            text.lines()
                .filter(|l| l.contains(&format!(",\"kind\":\"設計ノートの行\",\"file\":{},", quoted(file))))
                .map(|l| l.split('"').nth(3).unwrap().to_string())
                .collect()
        };
        let mut want: std::collections::BTreeMap<String, Vec<String>> = std::collections::BTreeMap::new();
        for line in emitted.lines() {
            let (pair, node, file, field) = split_emit(line);
            let approval = field.strip_prefix("meta.approval[").is_some_and(|f| f.ends_with("].ruling"));
            let heirs = match node {
                Some(id) => vec![id.to_string()],
                None if file.starts_with("design-note/") && approval => rows(file),
                None => Vec::new(),
            };
            for id in heirs {
                want.entry(id).or_default().push(pair.clone());
            }
        }
        assert!(want.values().map(Vec::len).sum::<usize>() > 0, "{}", dir.display());
        for line in text.lines() {
            let id = line.split('"').nth(3).unwrap();
            let expect = format!("[{}]", want.remove(id).unwrap_or_default().join(","));
            assert_eq!(rulings_of(&text, id), expect, "{}: {id}", dir.display());
        }
        assert!(want.is_empty(), "節点でない node: {want:?}");
    }
}
