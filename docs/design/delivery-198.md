# 設計: 便 198 — 編集時の口 folio check --proposed（書こうとしている中身を床と同じ関数で数える・判断の記録 ADR-33 の便 1）

- 要件: FR28（編集時の口・要件書 第 1.55 版の下書き）と受入基準 AC31。条 P-18.1（編集の時点で止める）の口の側と、P-15.2（編集時の判定の式を事後の検査が同じ関数で確かめる）の歯。
- 条: P-18.1・P-18.2（事後の床は今までどおり数える）・P-15.1（hook は保証でない・止める仕掛けは器が持つ）・P-15.2・P-4.1（読めない中身と置き場の外の字を「異常なし」にしない）・P-6.3（床の関数を 2 つにしない）・N-3.1（抜け道の旗を持たない）。
- 出所: 判断の記録 ADR-33（proposed・持ち主の承認待ち・台帳 f2-648.275.2）の決定 (1)(2)(4)(7)。**受付は ADR-33 と要件書 第 1.55 版の発効の後**（FR28 が本流の要件書に在ってから）。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `gs` が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は 7 本（src 4〔新 1〕・歯の file 3〔新 1・本文を変える 1・本文不変 1〕）。縮む file・消す file・新しい dir は無い。
- 門: 対象外。write-set に設計文書の正本（`design-intent/` の下）が無い。本流 6467915 の組み立てに write-set 7 本を渡した `folio ceiling --gate --dir design-intent --write-set …` は **0（通す・設計文書の正本を書き換えない便）**。
- 前提: **base = 本流 6467915**（便 185 の着地の後）。この契約の数はすべて 6467915 の写しの実測（参考値・規則の表の行 D-13）。
- 実装の見本: origin の枝 `impl/d198`（commit **d99e5f8**・親 6467915）。`git diff 6467915 d99e5f8` が便の全体の差分（6 file・+557 −3・30,693 byte）。**作業者は write-set の file をこの枝の中身にしてよい**（`git checkout impl/d198 -- <write-set の file>`）。
- 並行の便との重なり: §1 (g) の表。床の穴・検査の信頼・小さな直し・写しの負債のレーンの便が本便の write-set の file を書き換えて先に着地したら、本便は余地と歯の数を数え直してから受け付ける（着地の順は lanes-common の順）。

## 1. 設計

### (a) いま起きていること（base 6467915 の実測・参考値）

1. **設計文書を書く時点では何も止まらない。** 強制は事後の床（`folio check`・`inject --check`・`schema --check`・`derive --check`）と器の受付の床と天井だけ。器（scribe2）の道具の前の hook（PreToolUse）の門は書き込み範囲・命令・起票・権能・走っている便の行の 5 つで、設計文書の床を撃つ門は無い。憲法の条 P-18 と P-15 の機構は live が M1 のまま。
2. **床の形。** `folio check` は `crates/folio/src/main.rs` で `check::check_dir(&dir, flag)` を撃ち、続けて `graph::check_index(&dir, &mut report)` を撃つ（2 本を順に撃つ所は main.rs の 1 か所だけ）。違反は `verdict::Report.violations`（種類と字の組の列）で、どの検査の族かを持たない。
3. **網の関数。** `check_dir` の中の 5 つの関数は 2 か所以上を突き合わせる: `refs::check_refs`（参照 id の解決・逆参照・件数）・`vocab::check_vocab`（英字の語と語彙）・`link::check_link`（判断の記録と正本 4 file の突き合わせ）・`anchor::check_anchor`（凍結 anchor の列と改訂の記録）・`mentions::check_mentions`（散文の言及）。双方向の決まり（行と条の逆参照・後継と前任・改訂の記録と条の amended_by・発効と封・条の件数）は、2 つの file か同じ file の離れた 2 か所を順に書く途中で必ず一度食い違う。
4. **速さ（参考値・負荷 20〜110 の周）。** 素の床は最適化した組み立て（release）で folio2 0.19〜0.60 秒・tsuzuri の写し（bbc8126）0.15〜0.30 秒、最適化しない組み立て（debug）で 0.9〜3.2 秒・0.66〜0.99 秒。器の hook の予算は 2000 ミリ秒（器の規則の行 hook.budget_ms）。
5. **base の歯（参考値）。** workspace の nextest は §1 (e) の表・clippy 0 警告・床 4 本 rc 0・`folio build --write` の file 数は §1 (e)。`git grep -n f198_ -- crates` は 0 件・行 id `gs` は 0 件。`folio check --proposed` は base の binary で clap が断る（`error: unexpected argument '--proposed'`・終了 2）。

### (b) 直す先

1. **`crates/folio/src/verdict.rs`。** `Report` に欄 `links: Vec<usize>`（つながりの違反の `violations` の添字）と、関数 mark（違反の数を印にする）と関数 links_from（印の後に積んだ違反をつながりに数える）を足す（どちらも新しい名）。`violation`・`verdict`・字・数は変えない。
2. **`crates/folio/src/check.rs`。** `check_dir` の中で、`refs::check_refs` と `vocab::check_vocab` の 2 本、`link::check_link` と `anchor::check_anchor` の 2 本、`mentions::check_mentions` の 1 本を、それぞれ `mark` と `links_from` で包む（3 か所・注 2 行）。撃つ順・引数・違反の字と数は変えない。
3. **`crates/folio/src/proposed.rs`（新）。**
   - 関数 floor（新しい名・引数は置き場と旗）: `check_dir` と `check_index` を順に撃つ床の 1 本の関数。`folio check` と口の両方がこれを撃つ（条 P-15.2）。
   - 関数 judge（新しい名・引数は置き場と相対の字と中身）: 相対の字が置き場からの相対の字（成分が全部ふつうの名・絶対 path と `..` と `.` と空は断る）であることを確かめ、置き場を一時の作業場所（`std::env::temp_dir()` の下の `folio-proposed-<pid>-<nanos>/<置き場の dir 名>`）へ丸ごと写す（symlink は symlink のまま）。器の導出 file は `note::external_path(dir)` で解き、在れば写しの根の `contracts/schema.toml`（`floor_note::EXTERNAL_PATH`）へ写す（版管理の外の写しは置き場の親の下を読む）。写しのまま `floor` を撃ち（前）、`rel` に `content` を書いて `floor` を撃つ（後）。後の違反のうち前に無いもの（種類と字の組を重複ごと数える差）を、後の `links` に在れば `links` へ、無ければ `stop` へ分け、後の「まだ分からない」（unknowns と pendings）のうち前に無いものを `unknowns` へ入れる。字の中の写しの path は置き場の path に戻して返す。一時の作業場所は `Drop` で消す。
   - 型 Judged（新しい名・止める行・つながりの行・まだ分からない の 3 つの列）の関数 verdict: 新しい「まだ分からない」が在れば まだ分からない、`stop` が在れば 不合格、どちらも無ければ 合格（つながりは数えない）。
4. **`crates/folio/src/main.rs`。** `folio check` に旗 `--proposed <PATH>` を足す（ほかの 6 つの旗と同時に撃てない＝`conflicts_with_all`）。旗があれば標準入力を全部読み（UTF-8 でなければ まだ分からない 2）、proposed.rs の関数 judge を撃ち、止める行を標準出力に `[種類] 字`、つながりを標準エラーに `# つながり（編集は止めない・事後の床が数える）: [種類] 字`、新しい まだ分からない を標準エラーに `# まだ分からない: 字`、要約を標準出力に `folio check --proposed: <判定>（新しい違反 N・つながり K・まだ分からない M）` で出し、判定の終了コード（0・1・2）で終える。`judge` が断れば標準エラーに `folio check --proposed: まだ分からない（<理由>）` の 1 行で 2。旗が無いときは今までの `check_dir` と `check_index` の 2 行を proposed.rs の関数 floor の 1 行にする（出力と終了は変えない）。`mod proposed;` と `use crate::verdict::Verdict;` を足す。
5. **`crates/folio/tests/modules.rs`。** 層の割り当ての表に区切り proposed を層 3 として 1 行足す（読む相手は check〔2〕・note〔2〕・graph〔3〕・floor_note と phase〔1〕・verdict〔0〕、名指す側は main〔5〕）。
6. **変えないもの。** 素の `folio check` の出力・判定・終了コード・凍結の旗と `--emit-amends` と `--emit-rulings`・網の関数の中身・違反の字・設計文書の正本と生成区間・憲法と要件書と判断の記録の字・`folio build` の出力。網の外の関数の中の突き合わせの字（設計ノート・計画・判断の記録どうし・封の欠け・入口と相談窓口と天井の英字の語）の族は便 199 が運ぶ（本便ではまだ止める側に数える）。

### (c) 歯（f198_・base で 0 件）

binary 経由の歯は `crates/folio/tests/proposed.rs`（新）。どれも床の土台（`tests/fixtures/floor_base/design-intent/`）を一時 dir の `repo/design-intent/` に、器の導出 file を `repo/contracts/` に作って `repo/` を git の 1 commit にし（素の床は合格 0）、口の一時の作業場所を版管理の外の `tmp/` に作らせて（子の環境の `TMPDIR`）撃つ。期待の字は歯の側の手書き。

1. **f198_stop_line_is_a_line_of_the_floor（AC31 の前半・P-15.2）。** 規則の表の行 R-2 に未知の欄 `bogus: 1` を足した中身を `--proposed rules.yaml` に渡すと、終了 1・標準出力はちょうど `[未知の欄] rules.yaml: 行 R-2 の未知の欄「bogus」` と `folio check --proposed: 不合格（新しい違反 1・つながり 0・まだ分からない 0）` の 2 行・置き場の全 file の字が撃つ前と同じ。同じ中身を書いた置き場の素の `folio check` は終了 1 で、標準出力にその 1 行が同じ字で在る（編集時の判定 ⊆ 事後の判定）。
2. **f198_link_is_not_stopped_but_the_floor_counts_it（AC31・P-18.2）。** 要件 FR1 の basis に `P-99` を足した中身を `--proposed srs.yaml` に渡すと、終了 0・標準出力は要約の 1 行だけ（`合格（新しい違反 0・つながり 1・まだ分からない 0）`）・標準エラーに `# つながり（編集は止めない・事後の床が数える）: [参照 id] srs.yaml: requirements[0].basis[1]: id P-99 が実在しない`。同じ中身を書いた置き場の素の床は終了 1 で、標準出力にその違反の行が在る。
3. **f198_old_violations_do_not_stop（AC31）。** 置き場の規則の表に未知の欄を先に書いた（素の床 1）うえで、要件書の今の中身をそのまま渡す提案も、規則の表を元へ戻す提案も終了 0（後者の要約は `合格（新しい違反 0・つながり 0・まだ分からない 0）`）。
4. **f198_unreadable_proposal_is_unknown（P-4.1）。** `a: [` の 1 行を `--proposed rules.yaml` に渡すと終了 2 で、標準エラーに `# まだ分からない: rules.yaml: ` で始まる行が在る。
5. **f198_outside_the_place_is_unknown。** `../contracts/schema.toml`・`/etc/hosts`・`./rules.yaml` の 3 つとも終了 2・標準出力は空・標準エラーはちょうど `folio check --proposed: まだ分からない（<字> は置き場からの相対の file の字でない（絶対 path・.. ・空は数えない））` の 1 行。
6. **f198_new_file_is_counted_by_the_same_floor。** 判断の記録 ADR-10 の字の id を ADR-11 に、status を bogus にした中身を `--proposed adr/ADR-11.yaml`（新しい file）に渡すと終了 1 で、`[adr] ADR-11: status が値域外` で始まる行が在る。止めた行はどれも、同じ中身を書いた置き場の素の床の標準出力に在る。
7. **f198_scratch_is_removed。** 止めた周（歯 1 の中身）と通した周（歯 2 の中身）の後で、口の一時の作業場所の置き場（写しの根の `tmp/`）が空。
8. **f198_index_floor_is_in_the_same_function。** 要件 FR1 の id を単引用符で囲んだ中身を `--proposed srs.yaml` に渡すと終了 1 で、標準出力の 1 行目が `[索引の節点] srs.yaml: 索引の節点 FR1 の行を行の逐語で切れない（id か節の見出しの key が引用符つきか裸の形でない＝folio graph --print が組めない）`（索引の床も床の 1 本の関数に入る）。同じ中身を書いた置き場の素の床にその行が在る。
9. **f198_contract_rows_are_counted_with_the_vessel_file。** 設計ノートの見本 example.yaml の契約表の行 a に未知の欄 `bogus: x` を足した中身を `--proposed design-note/example.yaml` に渡すと終了 1 で、標準出力の 1 行目が `[note] design-note/example.yaml: §6 の行 a: 契約表の欄「bogus」が器の導出 file に無い`（器の導出 file を写しへ写して契約表の欄を数えた）。同じ中身を書いた置き場の素の床にその行が在る。
10. **単体の歯（`crates/folio/src/proposed.rs` の tests の区間）。** f198_inside_refuses_paths_out_of_the_place（`rules.yaml` と `adr/ADR-1.yaml` は受け、空・絶対 path・`..`・`./` を断る）と f198_judged_verdict_counts_stop_and_unknowns_only（つながりだけなら 合格・止める行が在れば 不合格・新しい まだ分からない が在れば まだ分からない）。
11. **RED の実測。** 歯の file だけ（`r198-teeth.patch`＝`tests/proposed.rs` と `tests/modules.rs` の差分）を base に当てると、binary の歯 9 本とも落ちる（旗が無く clap が `error: unexpected argument '--proposed' found` で断る）・`--bin folio f198_` は 0 本（nextest の rc 4）・`--test modules` の 2 本（`p106_layers_cover_every_module`・`p106_edges_point_down`）が落ちる（表に区切り proposed の行が在るのに src に file が無い）。log は起草の記録の `red-198.log`。

### (d) 採らなかった形

1. **書いた後の置き場の違反を全部止める（族を分けない）。** 双方向の決まりを持つ 2 つの file の編集が互いに止め合う。書く前から在る違反でどの編集も止まる。抜け道の旗は条 N-3.1 で持てない（ADR-33 案 b）。
2. **1 file の形だけを別の関数で数える（写さない）。** 床と別の式になり（条 P-15.2・P-6.4）、封と番号の消失のような凍結を見ない（ADR-33 案 c）。
3. **置き場を写さず、読む所ごとに差し替えの字を渡す（上書きの層）。** 床の 10 余りの読み手の全部に口を通す改修になり、write-set が床の全部の file に広がる。写しなら同じ関数をそのまま撃てる（違いは版管理との照合が写しで測れないことだけで、前と後の 2 回とも同じ「まだ分からない」になり差に出ない）。
4. **口が道具の外の枠の hook の入力（JSON）を読む。** folio がその形に縛られる（条 P-1.1 の外・ADR-33 案 f）。書いた後の本文の組み立ては器が持つ。

### (e) 既存の歯・突然変異・外の置き場

1. **既存の歯。** 本便の差分を base に当てた写し（見本 impl/d198）の数は次の表（参考値・起草の記録の `verify-198-summary.txt`）。字の期待を直した既存の歯は無い（`tests/modules.rs` は表に 1 行を足すだけ）。

| 数え | base 6467915 | 見本 d99e5f8 |
| --- | ---: | ---: |
| workspace の nextest（`cargo nextest list --workspace --message-format oneline` の行数・全部合格） | 1050 | 1061（+9 の歯・+2 の単体） |
| clippy の警告 | 0 | 0 |
| 床 4 本（check・inject --check・schema --check・derive --check） | 4 本とも rc 0 | 4 本とも rc 0 |
| `folio build --write` の file 数 | 37 | 37（base と全 file が byte で同じ） |

2. **突然変異（見本の写しの src だけを 1 通りずつ変え、f198_ の歯を撃つ・`mut-198.py`）。**

| 変異 | 落ちる歯（歯の番号は (c)） |
| --- | --- |
| M1 書く前の床を比べない（後の違反を全部新しいとする） | 3 |
| M2 つながりも止める | 2・7 |
| M3 新しい まだ分からない を数えない | 4 |
| M4 差し替えを写しの根に書く（file を取り違える） | 1・2・4・6・7・8・9 |
| M5 一時の作業場所を消さない | 7 |
| M6 置き場の外の字を断らない | 5・10 |
| M7 止めても 0 で終える | 1・6・7・8・9・10 |
| M8 参照 id と語彙の網をつながりに数えない | 2・7 |
| M9 床の 1 本の関数から索引の床を外す | 8 |
| M10 止める行を標準エラーへ出す | 1・6・8・9 |
| M11 つながりの行を出さない | 2 |
| M12 器の導出 file を写さない | 9 |
| M13 つながりの印を積まない（`links_from` が何もしない） | 2・7 |

   13 通りとも落ちる（生き残り 0・`mut-198.log`）。M12 は、口の一時の作業場所を置き場と同じ版管理の中に作らせた歯の初めの形では生き残った（写しが版管理の根の下の器の導出 file を読めた）。一時の作業場所を版管理の外へ移し、歯 9 を足して落ちるようにした。

3. **外の置き場（tsuzuri の写し bbc8126・参考値）。** 見本の binary で、設計ノート surface-wave9.yaml の契約表の行 e-hold に未知の欄を足した中身は終了 1（`[note] design-note/surface-wave9.yaml: §2 の行 e-hold: 契約表の欄「bogus」が器の導出 file に無い`＝器の導出 file を写しへ写して契約表の欄を数えた）。req に FR999 を足した中身も終了 1（設計ノートの参照 id の解決は網の外の関数の中の字＝便 199 がつながりへ移す）。同じ中身をそのまま渡すと終了 0。口の速さは release で 0.16〜0.27 秒、folio2 の要件書で 0.30〜0.46 秒（debug では 1.1〜1.9 秒・2.1〜3.1 秒・負荷 20〜110 の周・`time-198.log`）。

### (f) 大きさ・余地・verify と done の対応

1. **write-set の印。** 新しい file は `+crates/folio/src/proposed.rs` と `+crates/folio/tests/proposed.rs`。`crates/folio/tests/check.rs` は本文を変えない（verify の `--test` の scope）。差分 30,693 byte（`git diff 6467915 d99e5f8 | wc -c`・6 file・+557 −3）。
2. **余地（CapHeadroom）。** 測るのは write-set の src の 4 本（python と awk の 2 実装で一致・`cap-198.sh`）。

| file | base の正規化行数（参考値） | base の余地 | 本便の後 | 本便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/check.rs` | 1113 | 387 | 1121（+8） | 379 |
| `crates/folio/src/main.rs` | 698 | 802 | 743（+45） | 757 |
| `crates/folio/src/verdict.rs` | 94 | 1406 | 107（+13） | 1393 |
| `crates/folio/src/proposed.rs` | 0（新） | 1500 | 181（+181） | 1319 |

3. **size は M。** src の増分は +247 で S の見積 100 を超え、M の見積 300 の内。余地の最小（check.rs の base 387）は M の 300 を超える。
4. **verify は 5 行**で、done の 5 つの塊と 1 対 1 に揃える。見本の写しで 5 行とも rc 0。
   1. `cargo nextest run -p folio --test proposed f198_` = (c) の 1〜9（9 本）。
   2. `cargo nextest run -p folio --bin folio f198_` = (c) の 10（2 本）。
   3. `cargo nextest run -p folio --test modules` = 層の割り当ての表と層が上がる辺（便 106 の歯）。
   4. `cargo nextest run -p folio --test check` = 素の `folio check` の歯（床の 1 本の関数へ移しても出力と終了が同じ）。
   5. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** `--test` で名指す歯の file（proposed・modules・check）は全部 write-set に在る。`--bin folio` の歯の在り処（proposed.rs）も write-set に在る。

### (g) 門・受付・ほかのレーンとの重なり

1. **門。** 冒頭のとおり対象外・0（通す）。
2. **受付。** 受付の先撃ち（precheck）は、枝 docs/guard の本契約で 契約に起因する断り 0（起草の記録の `precheck-198.log`）。**受付は ADR-33 と要件書 第 1.55 版の発効の後**（req の FR28 が本流に在ること）。
3. **重なり（2026-09-28 の起草の時点・origin の impl/* と各レーンの依頼の見込み）。** 本便の write-set の src は `check.rs`・`main.rs`・`verdict.rs`。

| レーン（便） | 重なる見込みの file | 扱い |
| --- | --- | --- |
| 床の穴（187〜189） | `check.rs`（床の関数の呼び方） | 先に着地したら `check_dir` の網の 3 か所の包みを数え直す |
| 検査の信頼（190・191） | `check.rs`（版管理の照合）・`anchor.rs` は本便の外 | 同上 |
| 小さな直し（192〜194） | `main.rs`（命令の説明の字・.185） | 先に着地したら `--proposed` の旗の行と `Command::Check` の match を数え直す |
| 写しの負債（195〜197） | 本便の write-set とは重ならない見込み（`floor_*.rs`・生成区間） | 無し |

   origin の impl/* に上のレーンの枝は起草の時点で無い（`git ls-remote origin 'refs/heads/impl/*'` の最後は impl/d186）。着地の順は 185 → 床の穴 → 検査の信頼 → 小さな直し → 写しの負債 → 本便。
4. **着地の後。** 席は器の席へ、口の形（`folio check --dir <置き場> --proposed <相対の file>`・標準入力・終了 0/1/2・標準出力と標準エラーの分け方）と、便 199 の着地までは口がつながりの一部（設計ノートの参照 id など）を止めることを返す（器の行は便 199 の後）。

### (h) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草の記録は持ち主の home の下の `.local/share/folio2/handoff-2026-09-28/guard-draft.md`、script と log は同じ dir の `guard-scripts/`。

1. 模擬: 見本 impl/d198 の d99e5f8（`git diff 6467915 d99e5f8` = `c198.patch`・歯だけ = `r198-teeth.patch`）。`verify-198.sh`（組み立て・nextest・clippy・床 4 本・build の出力を base と byte で比べる）。
2. RED: `red-198.sh`。突然変異: `mut-198.py`。余地: `cap-198.sh`（`lines.py` と `lines.awk`）。
3. 速さ: `time-198.sh`（素の床と口を release と debug で 5 回ずつ・folio2 と tsuzuri の写し）。
4. 外の置き場: tsuzuri の `.git` だけを写して clone・remote を外した写しで、見本の binary の口を撃つ（`tz-198.sh`）。

### (i) 本便が運ばないもの・言えないこと・撤退条件

1. **運ばないもの。** 網の外の関数の中の突き合わせの字の族（便 199）・極性一覧の口と下限の数え・欄 key の値域・規則の表の行・床の定数の guards・憲法の機構の live と注（便 200）・器の hook の行（器の判断の記録と便）・生成区間の欄の決まりとの一致（`schema --check`）を口に入れること（ADR-33 決定 (6)）。
2. **言えないこと。** (1) 口の 通す は、その編集で増える違反が止める族に無いことだけを言い、置き場の床の 合格 ではない（条 P-3.3・置き場全体は素の床が数える）。(2) 写しは版管理の外なので、版管理との照合（凍結 anchor の削除・未追跡）は口が数えない。(3) 違反の字に行の番号を持つ種類（重複キー）は、前から在る違反でも行がずれると新しい違反に見える。(4) debug の binary では folio2 の置き場で器の予算（2000 ミリ秒）を超えうる（§1 (a) の 4）。
3. **撤退条件。** (1) 本便が要件書 FR28 か ADR-33 の字か憲法の条文を変えないと書けないと分かったら、止めて席へ返す。(2) 受付の時点で本流の `check_dir` の網の 5 つの関数の撃ち方か `main.rs` の `check_dir` と `check_index` の 2 行が base（6467915）と違えば、止めて席へ返す（数え直してから運ぶ）。(3) 見本の口が止めた行が、同じ中身を書いた置き場の素の床に無い周が 1 つでも見つかったら、止めて席へ返す（ADR-33 撤退条件 (2)）。

## 2. 範囲

- 入れる: `folio check --proposed`（旗・標準入力・判定・出力の分け方）・`proposed.rs` の関数 floor と judge と写し・`verdict.rs` の欄 links と関数 mark と links_from・`check.rs` の網の 5 つの関数の包み・`main.rs` の素の床の proposed.rs の関数 floor への置き換え・層の表の 1 行・歯の file の f198_ の 9 本と単体の 2 本。
- 入れない: 網の外の関数の中の字の族・極性一覧・規則の表と憲法と要件書と判断の記録の字・設計文書の正本と生成区間・器の hook・外部 crate・新しい dir。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| mouth | 口 | `main.rs` の `--proposed`・`proposed.rs` の `judge` と `Judged`（前後の差・族の分け・写し） |
| floor | 床の 1 本の関数 | `proposed.rs` の `floor`（`check_dir` と `check_index`・素の床と口が撃つ） |
| mark | 族の印 | `verdict.rs` の `links`・`mark`・`links_from`・`check.rs` の網の 3 か所の包み |
| teeth | 歯 | `tests/proposed.rs` の f198_ の 9 本と `proposed.rs` の単体の 2 本・`tests/modules.rs` の表の 1 行 |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate も外部ライブラリも増やさない（一時の作業場所と写しは std）。新しい dir は無い。
- 前提の着地: 便 185（本流 6467915）。ADR-33 と要件書 第 1.55 版の発効。
- 本便の着地の後に席が見ること: 台帳の本便の件を閉じる。本流の `target/debug/folio` を組み直す。便 199 の契約を書く（余地を数え直す）。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "gs"
title = "folio check --proposed を足す（判断の記録 ADR-33 の便 1・決定 (1)(2)(4)・要件書 第 1.55 版の FR28 と AC31）: crates/folio/src/proposed.rs（新）に床の 1 本の関数 floor（check_dir と check_index を順に撃つ・素の folio check もこれを撃つ）と judge（置き場と器の導出 file を一時の作業場所へ写し、写しのまま 1 回とその file を標準入力の中身に差し替えて 1 回 floor を撃ち、後にだけ在る違反を止める行とつながりの行に分け、後にだけ在る まだ分からない を返す・置き場の外の字は断る・一時の作業場所は消す）を置き、crates/folio/src/verdict.rs の Report に links・mark・links_from を足し、crates/folio/src/check.rs の check_dir の網の関数 5 つ（refs・vocab・link・anchor・mentions）の違反をつながりに数え、crates/folio/src/main.rs の folio check に旗 --proposed（ほかの 6 つの旗と同時に撃てない・止める行と要約は標準出力・つながりと まだ分からない は標準エラー・終了 0 通す 1 止める 2 まだ分からない）を足す。素の folio check の出力と終了・違反の字・設計文書の正本は変えない"
req = ["FR28"]
section = "1"
write-set = ["crates/folio/src/verdict.rs", "crates/folio/src/check.rs", "crates/folio/src/main.rs", "+crates/folio/src/proposed.rs", "+crates/folio/tests/proposed.rs", "crates/folio/tests/modules.rs", "crates/folio/tests/check.rs"]
verify = ["cargo nextest run -p folio --test proposed f198_", "cargo nextest run -p folio --bin folio f198_", "cargo nextest run -p folio --test modules", "cargo nextest run -p folio --test check", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "M"
done = "crates/folio/tests/proposed.rs の f198_ の 9 本（形の違反を止めた行が同じ中身を書いた置き場の素の床の行に同じ字で在る・つながりの違反は止めずに標準エラーに名指して素の床が落とす・書く前から在った違反は数えない・読めない中身は まだ分からない・置き場の外の字は まだ分からない・新しい file も同じ床で数える・一時の作業場所が残らない・索引の床も同じ関数に入る・器の導出 file を写して契約表の行の欄も数える）が緑、crates/folio/src/proposed.rs の単体の f198_ の 2 本（置き場の外の字の断り・判定の 3 値）が緑、crates/folio/tests/modules.rs（層の表に proposed の行）が緑、crates/folio/tests/check.rs（素の folio check が同じ出力と終了）が緑、cargo clippy --workspace --all-targets -- -D warnings が 0 警告。着地の後の本流で folio check --dir design-intent が合格 0 違反 0・folio schema --dir design-intent --check が一致・folio inject --check が一致・folio derive --dir design-intent --out ../contracts --check が一致"
<!-- contracts:end -->
