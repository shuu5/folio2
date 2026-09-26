# 設計: 便 153 — 置き場に様式と部品目録が無いときだけ、組み立て時に焼いた 1 つの正本で build と parts を回す（群 A の 2 本目・台帳 f2-648.189 の残り）

- 要件: FR7（全面を配信先へ生成する）・NFR2（全生成面の design token は単一の定義に由来する）・FR4（1 組の design token）。規範文・確かめ方・受入基準は変えない。どの要件の規範文も「build は置き場の preview/ を読む」とは定めていない（§1 (i) の 1）。
- 条: P-2.3（design token は 1 か所＝焼く元は folio2 の design-intent/preview/ の file 1 つずつ）/ P-6.3（写しを手で持たない・置き場に写しを置かない）/ P-4.1（在るのに読めない様式は今までどおり まだ分からない）/ N-3.1（旗を足さない）。
- 出所: 台帳 **f2-648.189** の残り（便 152 が割った様式の file）。形は席の裁定（2026-09-27）で、判断の記録は起こさない。席の読みは、ADR-16 決定 (2)(エ) の「様式の写し」は置き場の repo に写しを置くことを指し、binary に焼いて出すのはそれに当たらない、というもので、席が台帳 f2-648 notes に記帳する。
- 置き場: 審査の材料は行 `ez` が指す §1 だけ。write-set は 5 本（src 2・歯の file 3）で、新しい file も dir も無い。
- 門: 対象外。作業ツリー planner-d153 の一番上で、base の binary・本便の binary・本流の target/debug/folio に write-set 5 本を渡すと、どれも **0（通す・設計文書の正本を書き換えない便）**。
- 前の便: **便 152（行 ey）の着地が前提**（通しの歯 f152_ を延ばす）。**base = main 6093b8d に便 152 の模擬の差分を当てた写し。数はすべてその実測（参考値・行 D-13）**で、便 152 の着地の後の main で数え直す。

## 1. 設計

### (a) いま起きていること（base の実測・参考値）

1. **骨格のままの命令の答え。** 一時 dir で git の init → `folio init --dir design-intent` → commit の後、手直しなしで撃った。右の欄は本便を当てた写しの binary。配信先の 4 面は build が書いた index・constitution・srs・adr-1。

| 命令 | base（便 152 の後） | 本便の後 |
| --- | --- | --- |
| build --write | **2（preview/folio.css が読めない・配信先に書かない）** | 2（6 file を書いた・床の まだ分からない 2 だけ） |
| build --check | **2** | 0（6 file が一致） |
| parts --check --page（配信先の 4 面） | **2（parts.json が読めない）** | 0（違反 0・まだ分からない 0） |
| parts --check（--page 無し） | 2（preview/ に面が無い） | 同じ（folio2 自身も同じ 2・範囲外） |
| ceiling --write | 2（設計ノートの面が無い） | 同じ（範囲外） |
| init・check・inject・schema・face 4 面 | 便 152 の答え | 同じ |

   build --write は、床が凍結の基準の不在で まだ分からない なので、書けても 2 のまま（FR5 の決まり）。0 に届くのは始まりの凍結の後で、それは列の根の表の便（台帳 f2-648.233）の範囲である。本便の後も置き場には preview/ を作らない。
2. **読む場所。** `crates/folio/src/site.rs` の関数 build_all は、様式 2 本（folio.css・folio-ui.js）を置き場の preview/ から byte のまま写す。`crates/folio/src/parts.rs` の関数 check は、置き場の preview/parts.json を組み立て時の目録と突き合わせ、既定の様式を置き場の preview/folio.css から読む。組み立ての script `crates/folio/build.rs` は、部品目録の型を folio2 の design-intent/preview/parts.json から導出して既に焼いている。
3. **folio2 自身。** design-intent/preview/ に folio.css・folio-ui.js・parts.json が 1 本ずつ在り、これが唯一の正本である。folio2 の parts --check は、--page 無しでは 2（preview/ に面が無い）、配信先の 3 面を --page で渡すと 0。
4. **base の歯。** workspace の nextest 956 / 956・clippy 0 警告・床 4 本 rc 0・`folio build --write` の出力 33 file。`--test site` 14 本・`--test parts` 25 本・`--test init` 20 本。`f153_` と行 id `ez` は 0 件。

### (b) 直す先 — 「無いときだけ焼いた正本」の 2 か所

1. **焼く元。** `crates/folio/src/parts.rs` に型付きの定数 3 つを置く。BAKED_CATALOG・BAKED_CSS・BAKED_UI_JS は、folio2 の design-intent/preview/ の parts.json・folio.css・folio-ui.js を組み立て時に include した字である。写しの file は持たない。
2. **部品の検査（parts.rs）。** catalog_matches は、置き場の部品目録が無ければ BAKED_CATALOG で数える（突き合わせの式はそのまま）。check は、--css が無く置き場の preview/folio.css も無ければ BAKED_CSS を様式の定義とする。
3. **配信の組み立て（site.rs）。** build_all の様式の枝を関数 style に移す。置き場の preview/<名> が無ければ焼いた字の byte（folio.css は BAKED_CSS・folio-ui.js は BAKED_UI_JS・それ以外の名は Err）を返し、在れば今までどおり byte を読む。site（層 5）から parts（層 2）への下向きの辺が 1 本増える。
4. **無いの判定。** file の情報が取れないとき（symlink も含めて何も無い）だけを「無い」とする。壊れた symlink と dir は「在るのに読めない」で、今までどおり まだ分からない（build は配信先を作らない）。init の関数 present と同じ読み方。
5. **変えないもの。** 配信先へ出す file の一覧 OUTPUTS と全部か無しか・床を先に回すこと・--css に渡した path が読めなければ まだ分からない・--page 無しの既定の面・部品目録が組み立て時と違えば「組み立て直す」で断ること・init（preview/ を書かない）・folio2 自身の出力・命令の旗と help の字。

### (c) 歯（binary 経由）

1. **通しの歯 f152_the_skeleton_runs_every_command_without_hand_edits を延ばす（`crates/folio/tests/init.rs`）。** build の段の期待を次の答えに替える。build --write は 2 で、標準出力に床の行と「書いた（6 file・」を持ち、配信先の folio.css と folio-ui.js が repo の design-intent/preview/ の file と byte で同じ。置き場に preview/ が無く、build --check は 0。face の段の後に、配信先の 4 面を --page で渡した parts --check が 0 で「違反 0」を持つ。**base では build が 2 で何も書かない＝RED。**
2. **f153_build_falls_back_to_the_baked_style_only_when_the_place_has_none（`crates/folio/tests/site.rs`）。** 既存の口 fixture_copy の写しで 4 通りを撃つ。
   1. 置き場の様式（凍結 fixture の最小の様式・repo の正本と違う字）が在れば、配信先の folio.css はその字（終了コード 2）。
   2. 2 本を消すと 7 file を書き、2 本とも repo の正本と byte で同じ。--check は 0。
   3. folio.css が dir なら 2 で「folio.css: 読めない」を出し、配信先を作らない。
   4. 壊れた symlink でも 3 と同じ答え。

   **base では 2 の番が 2 で何も書かない＝RED。**
3. **f153_parts_check_uses_the_baked_catalog_and_style_when_the_place_has_none（`crates/folio/tests/parts.rs`）。** 空の置き場に、実の正本から生成した入口の面を --page で渡すと 0 で「違反 0」。置き場の preview/parts.json が dir なら 2 で「parts.json: 読めない」。**base では 1 つ目が 2（parts.json が読めない）＝RED。**

fixture は足さない。歯は既存の口（Work・folio・fixture_copy・folio_build・parts_check・generated_index・assert_unknown）だけを使う。

### (d) 採らなかった形

1. **init が preview/ の 3 file を書く。** 書く file が 14 本になり、受入基準 AC19 の 11 本の閉じた一覧と食い違う。置き場ごとに部品目録と様式の写しを持たせる形でもある（便 152 §1 (i) の 4）。
2. **置き場の様式が在っても、いつも焼いた字を出す。** folio2 自身と既存の歯の置き場（凍結 fixture の最小の様式）の出力が変わる（(e) の 3 の M2 で凍結 fixture との一致の歯が落ちる）。置き場を先に読むので、folio2 の出力は 1 byte も変わらない。
3. **読めないときも焼いた字で埋める。** 壊れた様式を黙って別の字に替えることになり、P-4.1 に反する（M3・M8）。
4. **parts --check の --page 無しの既定を配信先の面へ替える。** folio2 自身も同じ 2 で、既定の意味を変える便になる。範囲外。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **落ちる既存の歯は 0 本（起草役の実測）。** 本便を当てた写しで workspace の nextest **958 / 958**（base 956 + 2）・clippy 0 警告・床 4 本 rc 0。`folio build --write` の出力は 33 file で、base と diff -r で全 file が一致した。
2. **RED。** 歯だけを base に当てると、延ばした f152_ の通しの歯と f153_ の 2 本が落ち、ほかの 58 本（init・site・parts）は緑。
3. **突然変異（写しの src を 1 通りずつ変え、init・site・parts の歯を撃つ）。** 8 通りとも 1 本以上が落ちる。表の 通し は f152_ の通しの歯、site・parts は (c) の 2・3。

| 変異 | 落ちる歯 |
| --- | --- |
| M1 build の焼いた様式を外す | 通し・site |
| M2 置き場の様式が在っても焼いた字を出す | site・凍結 fixture との一致（site_write_matches_the_frozen_fixture） |
| M3 build が読めない様式（dir）も焼いた字で埋める | site |
| M4 壊れた symlink を無いと数える | site |
| M5 焼いた様式 2 本を取り違える | 通し・site |
| M6 parts の焼いた部品目録を外す | 通し・parts |
| M7 parts の焼いた様式を外す | 通し・parts |
| M8 読めない部品目録（dir）も焼いた目録で数える | parts |

### (f) 大きさ・verify と done の対応

1. **write-set。** 5 本とも印なし（書き換えるだけ）: `crates/folio/src/parts.rs`・`crates/folio/src/site.rs`・`crates/folio/tests/init.rs`・`crates/folio/tests/parts.rs`・`crates/folio/tests/site.rs`。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file | base の正規化行数（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/parts.rs` | 633 | 867 | 651（+18） | 849 |
| `crates/folio/src/site.rs` | 263 | 1237 | 275（+12） | 1225 |

   src の外は tests/init.rs 918 → 940・tests/site.rs 802 → 883・tests/parts.rs 516 → 535。rustfmt --check の差の数は 5 file とも base と同じ（0・1・25・2・2）。焼いた字（約 82 KB）は binary に入るが、行数には数えない。
3. **size は S。** src 2 本で +30。
4. **verify は 7 行**で、done の 7 の塊と 1 対 1。
   1. `cargo nextest run -p folio --test site f153_` = (c) の 2。
   2. `cargo nextest run -p folio --test parts f153_` = (c) の 3。
   3. `cargo nextest run -p folio --test init f152_` = (c) の 1（延ばした通しの歯と便 152 の憲法の雛形の歯）。
   4. `cargo nextest run -p folio --test site` = 配信の組み立ての歯の全部（参考値 15 本）。
   5. `cargo nextest run -p folio --test parts` = 部品の検査の歯の全部（参考値 26 本）。
   6. `cargo nextest run -p folio --test init` = 骨格の歯の全部（参考値 20 本）。
   7. `cargo clippy --workspace --all-targets -- -D warnings`。

   base では 1・2 が 0 件で終了コード 4、3〜6 は緑（2・14・25・20 本）、7 は 0 警告。`--test` の 3 file は write-set に在り、`--bin` の行は無い。

### (g) 門と受付

門は対象外で 0（冒頭）。受付の先撃ち（precheck）で契約に起因する断りは 0（起草役の実測・(h) の 5）。

### (h) 数え直す手順（行 D-13）

記録は `.local/share/folio2/handoff-2026-09-27/d153-draft.md`、script は同じ dir の d153-scripts（repo の外）。

1. base: d152-scripts/build-sim-152.sh で main に便 152 を当てた写しを作り、commit する（便 152 の着地の後は main の clone でよい）。
2. 模擬: build-sim-153.sh が base の clone に apply-153.py（実装）と apply-153-teeth.py（歯）を当てて組む（c153.patch）。nextest・clippy・floor-153.sh（床 4 本と build の diff -r）・verify-153.sh・repro-153.sh（(a) の 1）を撃つ。
3. RED: apply-153-teeth.py だけを base に当てる（r153-teeth.patch）。
4. 突然変異と余地: mut-153.py（撃った後は元に戻して組み直す）・lines-153.py と lines-153.awk。
5. 受付の先撃ち: `~/.cache/folio2-orchestrator/r86/precheck.sh <worktree> docs/design/delivery-153.md#ez`。

### (i) 要件との関係・運ばないもの・撤退条件

1. **要件との関係（正本は書き換えない）。** FR7 の規範文（全面を配信先へ生成する）は様式の出どころを定めず、どの要件の規範文にも「置き場の preview/ を読む」の字は無い（起草役が要件書の規範文・契機・確かめ方・受入基準の字を検めた）。したがって席の止める条件（規範文の意味を変える）には当たらない。NFR2 と FR4 の単一の design token は、利用者の置き場でも folio2 の 1 つの定義から出ることで保たれる。着地の後に古くなるのは記述の字で、ADR-16 文脈 (エ) の「様式の 2 file は検査される置き場の下から写す」と、同 帰結の「利用者の repo は様式の file を持たない…面は描かれない」である。直しは次の節目の材料（行 D-16）で、席が台帳 f2-648.189 に控える。
2. **運ばないもの。** ceiling --write（設計ノートの面が要る）・parts --check の既定の面・焼かれた名 folio2（.191）・規則の表の引用符と索引（.190）・凍結の罠（.193）・行 R-17 の黙り（.194）・列の根の表（.233）・図の道具の置き場（archify の vendor）・main.rs の --css の help の字・設計文書の正本・台帳への記帳・外部 crate。
3. **撤退条件。** (1) 本便の後に既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。(2) 着地の後の main で folio2 自身の床 4 本の結果か `folio build` の出力が着地の直前と 1 byte でも違ったら、止めて席へ返す。(3) 受付の時点の main で、便 152 が未着地か、site.rs の build_all か parts.rs の check と catalog_matches か、tests/init.rs の通しの歯が base と違えば、(h) で数え直してから運ぶ。

## 2. 範囲

- 入れる: §1 (b) の 1〜4、(c) の通しの歯の延長と歯 2 本。
- 入れない: init・面の生成器・床・命令の旗と help・parts の既定の面・設計文書の正本・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| baked | 焼いた正本 | parts.rs の BAKED_CATALOG・BAKED_CSS・BAKED_UI_JS |
| parts | 部品の検査の読み | parts.rs の catalog_matches と check の様式 |
| site | 配信の組み立ての読み | site.rs の style |
| teeth | 歯 | tests/init.rs の通しの歯・tests/site.rs と tests/parts.rs の f153_ |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地 = 便 152（行 ey・枝 docs/d152）。並行の便は無い（parts.rs・site.rs と歯の 3 file を書き換える契約は、便 152 の tests/init.rs のほかに無い）。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。台帳 f2-648.189 を閉じるか（骨格のままで落ちる命令のうち、この便の範囲は閉じる）を決め、§1 (i) の 1 の字の直しを控える。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "ez"
title = "群 A の 2 本目（台帳 f2-648.189 の残り・席の裁定 2026-09-27）: 骨格の置き場には preview/ の様式と部品目録が無いので、folio build が preview/folio.css の読めなさで何も書けず、folio parts --check が parts.json の読めなさで数えられない。crates/folio/src/parts.rs に folio2 の design-intent/preview/ の parts.json・folio.css・folio-ui.js を組み立て時に include した型付きの定数を置き、置き場にその file が無いときだけ（壊れた symlink と dir は在ると数えて今までどおり まだ分からない）、parts --check は焼いた部品目録と様式で数え、crates/folio/src/site.rs の build は焼いた様式を配信先へ出す。置き場の様式が在ればそれを読むので folio2 自身の出力は変わらない。置き場に写しを置かない。歯は tests/init.rs の通しの歯 f152_ の延長（build が 6 file を書いて床の まだ分からない だけで rc 2・--check 0・配信先の 4 面の parts --check 0）と tests/site.rs・tests/parts.rs の f153_ 1 本ずつ。便 152 の着地が前提。門の対象外。base = main 6093b8d + 便 152・着地の後の main で数え直す"
req = ["FR7", "NFR2", "FR4"]
section = "1"
write-set = ["crates/folio/src/parts.rs", "crates/folio/src/site.rs", "crates/folio/tests/init.rs", "crates/folio/tests/parts.rs", "crates/folio/tests/site.rs"]
verify = ["cargo nextest run -p folio --test site f153_", "cargo nextest run -p folio --test parts f153_", "cargo nextest run -p folio --test init f152_", "cargo nextest run -p folio --test site", "cargo nextest run -p folio --test parts", "cargo nextest run -p folio --test init", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "tests/site.rs の f153_（置き場の様式が在ればその字を出し、無ければ 7 file を書いて folio.css と folio-ui.js が repo の design-intent/preview/ と byte で同じで --check が rc 0、folio.css が dir か壊れた symlink なら rc 2 で folio.css: 読めない を出して配信先を作らない）が緑、tests/parts.rs の f153_（空の置き場で実の正本の入口の面が rc 0 で 違反 0、parts.json が dir なら rc 2 で parts.json: 読めない）が緑、tests/init.rs の f152_（通しの歯で build --write が rc 2 で 書いた（6 file・ と床の まだ分からない 2 だけを出し、配信先の様式 2 本が repo の正本と byte で同じで置き場に preview/ が無く、build --check が rc 0、配信先の 4 面の parts --check が rc 0）が緑、tests/site.rs・tests/parts.rs・tests/init.rs の歯の全部が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と file 数も byte も変わらない"
<!-- contracts:end -->
