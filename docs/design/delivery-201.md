# 設計: 便 201 — 索引の節点ごとの 1 行（`folio graph --print --summary`）に節点の裁定 id の一覧を足し、設計ノートの行はノートの承認欄を継ぐ（判断の記録 ADR-35・S）

- 要件: FR14（索引の口・要件書 第 1.56 版で --summary の行に節点の裁定 id の一覧を足す）。受入基準は足さない（確かめ方の 1 文だけ・AC30 は変えない）。切り出しは FR26（裁定 id の書き出し）と同じ関数。
- 条: P-6.3（同じ内容を 2 つの面が持つときは一方を正本にして他方は導出する＝切り出しの読み手を 1 つに保つ）・P-3.3（索引は床の合否を写さない）・P-4.1 / P-4.2（索引が組めないときは今のとおり まだ分からない）・P-10.1 / P-10.2（期待の字は歯の手書きで、書き出しとの突き合わせは唯一の合格判定にしない）。
- 出所: 台帳 **f2-648.275.3**（t3 の道の子）。外の利用者 tsuzuri の席の求め（2026-09-28 20:3x JST）: 導出の地図の行 c-g3g7 が、設計の節点から承認した裁定への辺（ruled_by）を張るために、--summary の各節点に裁定 id の欄が要る。今の書き出し（`folio check --emit-rulings`）は、設計ノートの承認欄の行の node が空（null）で、一覧が全数なのは床の終了コードが 0 のときだけ。
- 承認: 判断の記録 ADR-35（下書き・ADR-32 決定 (5) を置き換える）と要件書 第 1.56 版（FR14 の規範文の意味が変わる＝行 D-17 の「要件の追加と削除」）の持ち主の承認が前提。席が判断の記録 ADR-33・ADR-34 と 1 回に束ねて持ち主へ出す。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `gv` が指す §1 だけ。write-set は 5 本（src 3・歯の file 2）で、新しい file・縮む file・消す file・新しい dir は無い。
- 門: **対象外・0**。本流の binary（44c14ac の組み立て）で、下書きの枝 docs/rulings の置き場に write-set 5 本を渡した `folio ceiling --gate --dir design-intent --write-set …` の答えは「通す（設計文書の正本を書き換えない便）」。
- 前の便: **base = 本流 44c14ac** + 判断の記録 ADR-35 と要件書 第 1.56 版の発効。数は base の写しの実測（参考値・規則の表の行 D-13）。組み直す手順は §1 (h)。
- 見本: origin の枝 `impl/d201`（**8dbdd4d**・本流 44c14ac の上の 2 commit）。`git diff 44c14ac 8dbdd4d` が便の全体の差分。**作業者は write-set の file をこの commit の中身にしてよい**（`git checkout 8dbdd4d -- <write-set の file>`）。write-set の外は変えない。
- 並行の便との重なり: `graph.rs` は便 195（行 gp・見本 impl/d195 80aec6c）も書く。着地の順は 187 → 190 → 195 → 196 → 197 → 201 を既定とする。見本どうしの merge-tree は便 187・190・195・196・197・198 のどれとも衝突 0（§1 (g)）。

## 1. 設計

### (a) いま起きていること（参考値・base 44c14ac）

1. **--summary の行は 7 欄。** `folio graph --print --summary` は節点ごとに id・kind・file・line・title・plain・eng の 7 欄の 1 行を出す（`graph.rs` の Index の jsonl）。裁定 id の欄は無い。folio2 の置き場で 243 行、tsuzuri の写し（51c4045）で 404 行。
2. **裁定 id は書き出しだけが出す。** `folio check --emit-rulings` は決定の欄から切り出した裁定 id を 1 件 1 行（ruling・form・bead・node・file・line・field）で出す（`ruling.rs` の sites と rulings と emit）。folio2 で 204 行（node を持つ行 119）、tsuzuri で 192 行（node を持つ行 55・設計ノートの承認欄の行 65〔node は null〕・判断の表の行 67・憲法の発効 1）。設計ノートの行へ結ぶには file の字で結ぶ（判断の記録 ADR-32 決定 (5)）。
3. **索引が読む木。** `graph.rs` の build は憲法・規則の表・要件書・判断の記録（関数 adr）・設計ノート（関数 notes・`note.rs` の load_notes）を読み、節点と辺を組んだら木を捨てる。
4. **base の歯（参考値）。** workspace の nextest 1070 / 1070・clippy 0 警告・床 4 本 rc 0（check 合格 違反 0・まだ分からない 0）・`folio build --write` 37 file。`git grep -n f201_ -- crates` は 0 件・行 id `gv` は 0 件。

### (b) 直す先

1. **`crates/folio/src/graph.rs` の Index。** 欄を 1 つ足す（節点の id → 裁定 id の組〔切り出した字・形の種類・台帳の id〕の一覧）。関連 fn を 1 つ足す（名は ruled・渡すのは `ruling.rs` の Tree）: `ruling.rs` の sites が拾った決定の欄ごとに、値が字なら `ruling.rs` の rulings で切り出し、(ア) 欄が節点を持てば（条の改訂来歴・規則の表の行・判断の記録の承認欄）その節点へ、(イ) 欄が設計ノートの承認欄の行なら同じ file の設計ノートの行（種類 設計ノートの行）の全部へ、欄の順・切り出した順で足す。(ウ) ほかの欄（憲法の発効の承認・5 正本の承認欄の stamp・判断の表の行）は足さない。値が字でない欄は切り出さない。
2. **`graph.rs` の build と読み手 2 つ。** 関数 adr は id を持つ記録の id と木を、関数 notes は meta の id を持つ設計ノートの file（`design-note/<file 名>`）と木を返す（節点と辺の組み方は変えない）。build は憲法・規則の表・要件書の木を残し、節点を組んだ後に `ruling.rs` の Tree（索引が読まない入口・天井の正本・相談窓口は空の木・索引の欄の決まりは無し）を組んで 1 の関連 fn に渡す。`ruling` は use せず `crate::ruling::` で名指す（便 195 が足す use の行と重ねない）。
3. **`graph.rs` の jsonl。** 各行の eng の後に欄 rulings（JSON の一覧）を足す。一覧の項は欄 ruling・form・bead をこの順に持つ JSON の表で、空白を挟まず、字は `yaml.rs` の json_str で書く（書き出しと同じ escape）。無ければ `[]`。ほかの 7 欄の字と順は変えない。
4. **`crates/folio/src/ruling.rs`。** 設計ノートの承認欄の行の欄の名 NOTE を crate の中へ公開する（`pub(crate)`・doc の 1 行）。値も文法も変えない。
5. **`crates/folio/src/main.rs`。** graph の旗 --summary の説明の字に「裁定 id の一覧」を足す（1 行）。
6. **既存の歯の字の期待（中身は変えない）。** `crates/folio/tests/graph_summary.rs` の手書きの行 7 本（土台の N-3・P-6.2・R-5・FR8・AC12・AC11・folio-v2 と、escape の歯の FR8・folio-v2・N-3・R-5・AC12）と `crates/folio/tests/graph_notes.rs` の手書きの行 4 本（example#a・wave#p・wave#q・wave#r）の末尾に欄 rulings を足す（R-5 は土台の裁定の欄から切った 2 つ・ほかは空の一覧 `[]`）。
7. **変えないもの。** --print の表と要約の 1 行・--digest・folio hello・床（folio check と check_index）・書き出し（--emit-rulings の 7 欄と行）・裁定 id の文法と決定の欄の一覧・索引の欄の決まり（graph.yaml の生成区間）・節点の種類 12 と辺の型 19・`folio build` の出力・憲法と要件書と判断の記録の字。

### (c) 歯（f201_・base で 0 件・`crates/folio/tests/graph_summary.rs`）

土台（`tests/fixtures/floor_base/design-intent`）か、その写しの一時 dir で命令を撃つ。写しは、規則の表の行 R-5 の裁定の欄を 3 つの形の字（`t3-hub.56:20260927T2259Z-1・f2-648 notes 2026-09-28 07:18 JST（t3-hub.1）`）に、行 R-6 の裁定の欄を一覧 `[f2-648.1]` に、判断の記録 ADR-10 の承認欄の裁定を 未記入 に替え、条 N-3 に改訂来歴 1 項（裁定 `f2-648 notes 2026-09-20 00:09 JST・t3-hub.2`）を足し、最小の手書きの設計ノート ruled.yaml（承認欄 2 行〔`t3-hub.1（裁定 id = t3-hub.58:20260927T2357Z-1・board）` と `f2-648.270 notes 2026-09-28 16:13 JST`〕・契約表の行 x と y・判断の表の行 d〔裁定 s2-07l.999〕）を置いたもの。期待の字は歯の側の手書き（凍結 anchor・P-10.1）。

1. **f201_rulings_are_cut_from_the_decision_fields_of_the_node**: 土台で R-5 は 2 つ（f2-648・f2-648.6 の bead）・ADR-9 は notes-time 1 つ。写しで R-5 は 3 つの形の組を出てくる順に、N-3 は改訂来歴の 2 つ（notes-time・bead）。字でない欄（R-6）・未記入（ADR-10）・改訂来歴を持つ条の規範文（N-3.1）・憲法の発効の承認しか持たない条（P-1）・規範文・要件・受入基準・登場人物は `[]`。
2. **f201_note_rows_inherit_the_approval_of_their_note**: ruled#x と ruled#y は承認欄の 2 行から切った 3 つ（bead・question・notes-time）を行の順に持つ。判断の表の行の裁定（s2-07l.999）はどの行にも出ず、承認欄の無いノートの行 example#a は `[]`。承認欄の 2 行目を消すと、その 1 つだけが消える。
3. **f201_rulings_agree_with_the_emitted_rulings**（条 P-6.3）: 実の正本（`design-intent/`）と 1 の写しの両方で、全部の節点の rulings が、同じ置き場の `folio check --emit-rulings` の行から組んだ期待（node を持つ行はその節点へ・設計ノートの承認欄の行は同じ file の設計ノートの行の全部へ・行の順）と一致し、節点でない node の行が残らない。書き出しの行は欄 node・file・line・field の頭の区切りの字で割る（JSON の字の中の引用符は逃がされるので、区切りの字は字の中に出ない）。
4. **RED の実測。** base に歯の file 2 本だけを当てると、f201_ の 3 本と、字の期待を直した既存の 4 本（f180_the_frozen_base_lines_are_the_hand_written_ones・f180_text_fields_are_escaped_into_one_json_line・f185_the_frozen_base_row_is_a_node_with_its_req_edge・f185_block_rows_keep_the_meta_id_the_section_title_and_depends）が落ちる（15 本のうち 7 本・起草の記録の red-201.log）。

### (d) 採らなかった形

1. **1 つの字の欄（最初の 1 つ・無ければ null）。** 1 つの欄の中のほかの裁定 id を捨てる（tsuzuri の写しで 1 節点に最大 5）。どれを残すかは置き場の約束の形で、器の持ち分（判断の記録 ADR-31 決定 (4)）。
2. **書き出しの行を設計ノートの行の数だけ複製して node を埋める。** 書き出しの行と決定の欄の 1 対 1（file・line・field）が崩れ、全数の条件（終了コード 0）も残る。
3. **索引が裁定 id の字を自分で切る。** 切り出しの読み手が 2 つになる（条 P-6.3）。

### (e) 既存の歯・突然変異・外の置き場

1. **既存の歯。** 本便の差分を base に当てた写しで workspace の nextest **1073 / 1073**（1070 + f201_ の 3 本）・clippy 0 警告・床 4 本 rc 0（合格 違反 0・まだ分からない 0）・`folio build --write` 37 file が base と byte で同じ。(b) の 6 の既存の 4 本は本便の src と字の期待が揃って通る。
2. **rulings を外した行は base と byte で同じ。** folio2 の置き場の 243 行と tsuzuri の写しの 404 行の全部で、見本の行は base の行の末尾の閉じ括弧の前に欄 rulings を足しただけの字（起草の記録の tally.py）。
3. **突然変異（見本の graph.rs だけを 1 通りずつ変え、graph_summary と graph_notes の歯を撃つ・mut-201.log）。** 12 通りとも落ち、どれも f201_ が 1 本以上落ちる（生き残り 0）。

| 変異 | 落ちる f201_ の歯 |
| --- | --- |
| M1 rulings の欄を出さない | 1・2・3 |
| M2 設計ノートの行が承認欄を継がない | 2・3 |
| M3 継ぐ先を同じ file に絞らない | 2・3 |
| M4 判断の表の行の裁定も継ぐ | 2・3 |
| M5 憲法の発効の承認を全部の条に付ける | 1・3 |
| M6 欄ごとに最初の 1 つだけ | 1・2・3 |
| M7 形の種類をいつも bead にする | 1・2・3 |
| M8 bead に切り出した字の全部を入れる | 1・2・3 |
| M9 切り出した順を逆にする | 1・2・3 |
| M10 一覧の値の字も切り出す | 1・3 |
| M11 条の改訂来歴を規範文にも付ける | 1・3 |
| M12 要件書の承認欄の stamp を要件に付ける | 1・3 |

4. **外の置き場（tsuzuri の写し 51c4045・参考値）。** 節点 404 のうち rulings が付くのは 206（設計ノートの行 162 / 162・規則の表の行 28 / 28・判断の記録 15 / 16〔残る 1 は承認欄の無い proposed〕・条 1 / 38）・裁定 id 291（bead 212・question 79）。全部の節点で書き出しから組んだ期待と一致。生成区間が変わらないので、tsuzuri は `folio schema --write` を撃たなくてよい。

### (f) 大きさ・余地・verify と done の対応

1. **write-set の印。** 5 本とも在る file（印なし）。差分は +275 −35・33,871 byte（`git diff 44c14ac 8dbdd4d`・参考値）。
2. **余地（CapHeadroom）。** 測るのは write-set の src の 3 本（各行 ceil(字数 / 120) の和・python と awk の 2 実装で一致・lines.py と lines.awk）。

| file | base の正規化行数（参考値） | base の余地 | 本便の後 | 本便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/graph.rs` | 1036 | 464 | 1103（+67） | 397 |
| `crates/folio/src/ruling.rs` | 515 | 985 | 516（+1） | 984 |
| `crates/folio/src/main.rs` | 703 | 797 | 703（±0） | 797 |

便 195 が先に着地すると `graph.rs` は 1135（余地 365）で、本便の後は 1201（余地 299）になる（見本どうしの merge-tree の結果・参考値）。

3. **size は S。** src の増分の最大は graph.rs の 67（S の 100 の内）で、余地の最小（base 464・便 195 の後 365）は S の 100 を超える。
4. **verify は 4 行**で、done の 4 の塊と 1 対 1 に揃える。便の後の写しで 4 行とも rc 0。
   1. `cargo nextest run -p folio --test graph_summary f201_` = (c) の 1〜3。
   2. `cargo nextest run -p folio --test graph_summary` = 節点ごとの 1 行の既存の歯（手書きの行・escape・--print と --digest が凍結 anchor のまま）。
   3. `cargo nextest run -p folio --test graph_notes` = 設計ノートの行の既存の歯（手書きの行・設計ノートの外の行が動かない）。
   4. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** `--test` で名指す歯の file（graph_summary・graph_notes）は 2 本とも write-set に在る。絞り込みの語 f201_ を名に持つ歯は `crates/folio/tests/graph_summary.rs` の中だけで、src の中には無い。

### (g) 門と受付と重なり

1. **門。** 冒頭のとおり対象外・0。
2. **受付。** 受付の先撃ち（precheck）は下書きの枝 docs/rulings で契約に起因する断り 0（起草の記録の precheck-201.log）。
3. **重なり（見本の枝どうしの `git merge-tree --write-tree`・2026-09-28 の origin の先頭）。**

| 便（見本） | 重なる file | merge-tree |
| --- | --- | --- |
| 187（impl/d187 430c9c7） | `main.rs`（便 187 は検査の命令の説明と面の床の呼び出し・本便は graph の旗の説明） | 衝突 0 |
| 190（impl/d190 83f049d） | 無し | 衝突 0 |
| 195（impl/d195 80aec6c） | `graph.rs`（便 195 は床の定数 FLOOR と use の行と関数 rules と単体の歯・本便は Index と build と adr と notes と jsonl） | 衝突 0（見本の最初の形は use の行で 1 か所衝突した＝`crate::ruling::` で名指す形に直した） |
| 196（impl/d196 1a7c4c7） | 無し | 衝突 0 |
| 197（impl/d197 8a0abe9） | 無し | 衝突 0 |
| 198（impl/d198 f19045d） | `main.rs`（便 198 は検査の旗 --proposed） | 衝突 0 |

### (h) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草の記録は持ち主の home の下の `.local/share/folio2/handoff-2026-09-28/rulings-draft.md`、script と log は同じ dir の rulings-scripts。

1. 模擬: 見本 8dbdd4d（`c201.patch` が便の全体・`r201-teeth.patch` が歯だけ）。
2. RED: base に `r201-teeth.patch` を当てて `cargo nextest run -p folio --test graph_summary --test graph_notes`。突然変異: `mut-201.py <見本の写し>`（12 通り）。余地: lines.py と lines.awk。
3. 外の置き場: tsuzuri の `.git` だけを写して clone し（写しの設定に hook の path が無いこと・`.git/hooks` が sample だけなことを確かめる）、base と見本の binary で `folio graph --print --summary` と base の `folio check --emit-rulings` を撃って `tally.py <base の出力> <見本の出力> <書き出し>`。

### (i) 本便が運ばないもの・言えないこと・撤退条件

1. **運ばないもの。** 判断の記録 ADR-35 と要件書 第 1.56 版の字（下書きの枝 docs/rulings が運び、持ち主の承認で発効）・書き出しの形・裁定 id の文法・床・tsuzuri への知らせ（席）・台帳への記帳（席）・外部 crate・新しい dir。
2. **言えないこと。** (1) 裁定 id が台帳に在るか、置き場の約束の形か（器の持ち分）。(2) 設計ノートの承認欄はノートの版ごとの承認で、行を後から足したノートでは前の版の承認もその行に付く（承認欄が行を名指さない）。(3) 欄に台帳の id が書かれていない決定の欄は `[]` になり、その欄は床が違反か まだ分からない に数える（索引は床の判定を写さない）。
3. **撤退条件。** (1) 本便が要件書 FR14 の第 1.56 版の字か、憲法の条文か、判断の記録の字を変えないと書けないと分かったら、止めて席へ返す。(2) 受付の時点で本流の `graph.rs`・`ruling.rs`・`main.rs` が base（または便 195 などの着地の後の数え直し）と違えば、止めて席へ返す。(3) 本便の後に書き出し（`folio check --emit-rulings`）の出力か、--print か --digest の出力が 1 byte でも変われば、止めて席へ返す。(4) 本便の後に folio2 自身の床 4 本の結果か `folio build` の出力が変われば、止めて席へ返す。

## 2. 範囲

- 入れる: (b) の 1〜6。
- 入れない: 判断の記録と要件書の字・書き出し・床・裁定 id の文法・索引の欄の決まり・外の置き場・新しい dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| field | 裁定 id の欄 | `graph.rs` の Index に足す欄と、jsonl の末尾の rulings |
| heirs | 付ける先 | `graph.rs` の Index に足す関連 fn（節点を持つ欄はその節点・設計ノートの承認欄は同じ file の行の全部） |
| tree | 読んだ木 | `graph.rs` の build・adr・notes が `ruling.rs` の Tree を組む |
| name | 欄の名 | `ruling.rs` の NOTE の公開 |
| teeth | 歯 | f201_ の 3 本と既存の歯の手書きの行 11 本 |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate も外部ライブラリも増やさない。新しい dir は無い。
- 前提: 判断の記録 ADR-35 と要件書 第 1.56 版の発効（持ち主の承認・判断の記録 ADR-33・ADR-34 と 1 回に束ねる）。
- 書き換える file が重なる並行の便: 便 195（`graph.rs`）・便 187 と便 198（`main.rs`）。§1 (g) の 3 のとおり衝突 0 で、既定の順は 195 の後。
- 本便の着地の後に席が見ること: 台帳の本便の件を閉じる。本流の `target/debug/folio` を組み直す。tsuzuri へ ADR-35 決定 (8) の知らせ（欄の形・継ぐ規則・付かない欄・種類と型は増えない・切り出しの文法）を返す。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "gv"
title = "索引の節点ごとの 1 行（folio graph --print --summary）の末尾に節点の裁定 id の一覧 rulings を足す（判断の記録 ADR-35 決定 (1)〜(7)・要件書 第 1.56 版の FR14・台帳 f2-648.275.3）: crates/folio/src/graph.rs の Index に節点の id から裁定 id の組（切り出した字・形の種類・台帳の id）の一覧への欄と、それを組む関連 fn を 1 つ足す。関連 fn は ruling.rs の sites が拾った決定の欄ごとに、値が字なら ruling.rs の rulings で切り出し（裁定 id の書き出しと同じ歩き手と関数）、欄が節点を持てば（条の改訂来歴・規則の表の行・判断の記録の承認欄）その節点へ、設計ノートの承認欄の行なら同じ file の設計ノートの行の全部へ、欄の順・切り出した順で足し、ほかの欄（憲法の発効の承認・承認欄の stamp・判断の表の行）は足さない。build は関数 adr と notes が返す木と憲法・規則の表・要件書の木から ruling.rs の Tree を組んで渡す（ruling は use せず crate::ruling:: で名指す）。jsonl は各行の eng の後に rulings（組は ruling・form・bead の順・無ければ空の一覧）を足し、ほかの 7 欄の字は変えない。crates/folio/src/ruling.rs は設計ノートの承認欄の欄の名 NOTE を crate の中へ公開し、crates/folio/src/main.rs は --summary の説明の字を直す。歯は crates/folio/tests/graph_summary.rs の f201_ の 3 本で、graph_summary.rs と graph_notes.rs の手書きの行 11 本の末尾に rulings を足す。実装の見本は origin の枝 impl/d201 の commit 8dbdd4d で、作業者は write-set の file をその中身にしてよく、write-set の外は変えない。base = 本流 44c14ac + ADR-35 と要件書 第 1.56 版の発効"
req = ["FR14"]
section = "1"
write-set = ["crates/folio/src/graph.rs", "crates/folio/src/main.rs", "crates/folio/src/ruling.rs", "crates/folio/tests/graph_summary.rs", "crates/folio/tests/graph_notes.rs"]
verify = ["cargo nextest run -p folio --test graph_summary f201_", "cargo nextest run -p folio --test graph_summary", "cargo nextest run -p folio --test graph_notes", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "crates/folio/tests/graph_summary.rs の f201_ の 3 本（節点の rulings は自身の決定の欄から書き出しと同じ組で欄の順・切り出した順に並び、字でない欄・未記入・規範文・憲法の発効だけの条・要件は空の一覧・設計ノートの行はノートの承認欄の全部の行を継ぎ、判断の表の行と承認欄の無いノートは継がない・実の正本と写しの全部の節点で同じ置き場の folio check --emit-rulings から組んだ期待と一致する）が緑、tests/graph_summary.rs の歯の全部（手書きの行・escape・--print と --digest の凍結 anchor を含む）が緑、tests/graph_notes.rs の歯の全部（手書きの行・設計ノートの外の行が動かないことを含む）が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 で、folio build の出力は着地の直前の main と byte で同じである"
<!-- contracts:end -->
