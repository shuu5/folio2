# 設計: 便 159 — 生成区間の置き場が無い CLAUDE.md へ inject --write が区間を作る（群 A・台帳 f2-648.238）

- 要件: FR6（憲法を AI の手元に届ける）。規範文と受入基準 AC4 は変えない（§1 (i) の 1）。
- 条: P-14.1・P-14.2・P-14.3（注入の書き込み・検査・上限）/ N-1.1（消さない）/ P-4.1（書けなかったことを合格にしない）/ P-10.1（歯の期待は手書きの fixture）。
- 出所: 席の外の置き場の通し（2026-09-27・main a6a868d）と台帳 **f2-648.238**。形は席の見込みのまま。
- 置き場: 審査の材料は行 `ff` が指す §1 だけ。write-set は 4 本で、新しい file も dir も無い。
- 門: 対象外。作業ツリーの一番上で base・本便・本流の binary に write-set 4 本を渡すと、どれも **0（通す・設計文書の正本を書き換えない便）**。
- 前の便: **base = main a6a868d（便 157 の着地の後）。数は base の写しの実測（参考値・行 D-13）**で、受付の時点の main が違えば数え直す。

## 1. 設計

### (a) いま起きていること（base a6a868d の実測・参考値）

1. **外の置き場での答え。** 一時 dir で git の init → `folio init --dir design-intent` → commit の後、根で inject を撃った。右の欄は本便を当てた写し。

| CLAUDE.md の形 | base | 本便の後 |
| --- | --- | --- |
| 無い・--write | 2（読めない） | 0（marker の対と区間だけの file）・続く --check 0・2 回目は「差が無い」 |
| marker の無い file（末尾に改行あり・なし・空）・--write | 2（marker が 1 対でない）・byte 不変 | 0（利用者の字の後に足す）・続く --check 0 |
| begin だけ・2 対・--write | 2・byte 不変 | 同じ |
| 無い・--check | 2（読めない） | 同じ（作らない） |

2. **止まる所。** `crates/folio/src/inject.rs` の関数 run は、CLAUDE.md を読めなければ（無いときを含む）「読めない」、marker が 1 対でなければ（0 本を含む）「marker が 1 対でない」の まだ分からない（2）で終える。init は CLAUDE.md を書かない（init.rs の頭の注・`crates/folio/tests/init.rs` 436 行・FR22 の規範文と AC19 の書く file 11 本の閉じた一覧）ので、外の置き場は marker の 2 行を人が手で書くまで注入が回らない。群 A の通しの歯 f152_the_skeleton_runs_every_command_without_hand_edits も marker の対を手で書いてから撃つ（tests/init.rs 801〜806 行）。
3. **通しで見つけたほかの手の要る所（本便では運ばない・席が決める）。**
   1. **新しく見つけたもの。** 利用者の CLAUDE.md に「…する。」「…ない。」で終わる行が在ると、区間を足した後の `inject --check` が 1（区間の外の規範語）で、利用者がその行を言い換えるまで通らない。出所の条 N-2 の機構の注は「検査対象は folio2 が所有する文書に限る」と書く＝外の置き場に掛けてよいかは席の判断。
   2. **既知のもの（台帳か 2026-09-24 の外の置き場の控え）。** 始まりの凍結の前は床と `build --write` が 2（`--freeze-start` は承認欄の裁定と列の根の表の行が要る・台帳 .233）。`derive --check` は導出物の dir が無いと 2（`--write` が作る空の dir は版管理に載らない）。`ceiling --write` は設計ノートの面が無いと 2、`ceiling --gate` は印が無いと 2。
4. **folio2 自身は変わらない。** folio2 の CLAUDE.md は marker の対を持つので今の道を通る。
5. **base の歯。** workspace の nextest 974 / 974・clippy 0 警告・床 4 本 rc 0・`folio build --write` の出力 34 file。`--test inject` は 14 本・`--test init` は 21 本。`f159_` と行 id `ff` は 0 件。

### (b) 直す先 — `crates/folio/src/inject.rs` の関数 run

1. **無い file。** 読むときの誤りが「無い」（NotFound）で、かつ --write のときだけ、空の file と見て先へ進む。ほかの読めなさ（UTF-8 でない・dir など）は今のまま「読めない」の 2 で、上書きしない。
2. **marker が 1 本も無い --write。** begin も end も無ければ、利用者の字をそのまま頭に置き、空行 1 つを挟んで末尾に「begin の marker・改行・本文・改行・end の marker・改行」を足す（末尾が改行でなければ改行を 1 つ補う・空の file と無い file は marker から始める）。字は「〈path〉: 無いので区間だけの file を作った（n 行 / m byte）」か「〈path〉: marker が無いので末尾に区間を足した（…）」で 0。本文は今の導出で、R-2 の上限は今のまま読む前に検査する。
3. **書く口を 1 つに。** 関数 write_md（書けなければ「書けない」の 2）を足し、今の置き換えの道もそれを使う（字と終了コードは同じ）。頭の注に 1 行足す。
4. **`crates/folio/src/main.rs` の --write の説明 1 行**の括弧に「CLAUDE.md が無ければ区間だけの file を作り、marker が 1 本も無ければ末尾に区間を足す」を足す。
5. **変えないもの。** marker が在って 1 対でない形（begin だけ・end だけ・逆順・2 対以上）は今のまま 2 で byte 不変（書く場所を決められない）。--check と --print（作らない・--check は区間が無ければ非 0）・導出・R-2 の読み・区間の外の規範語の検査・init・folio2 自身の CLAUDE.md の出力。

### (c) 歯（関数名 f159_・`crates/folio/tests/inject.rs`・binary 経由）

期待は手書きの `tests/fixtures/inject/ok/CLAUDE.md`（「# fixture」の 1 行・空行・marker の対と区間）から取る。fixture は足さない。

1. **f159_write_puts_the_region_where_there_is_none。** fixture ok の正本で ① CLAUDE.md が無い ② 空 ③「# fixture」と改行 ④ 改行の無い「# fixture」の 4 形に --write が 0 で、①② は ok/CLAUDE.md から頭の「# fixture」と空行を除いた byte、③④ は ok/CLAUDE.md と等しい。字は ① が「作った」・②〜④ が「足した」。続く --check は 0、2 回目の --write は「差が無い」で byte 不変。folio2 自身の正本と CLAUDE.md の写しへの --write で CLAUDE.md は 1 byte も変わらない。**base では ① が 2＝RED。**
2. **f159_write_still_refuses_markers_that_are_not_one_pair。** begin だけ・end だけ・逆順・2 対で --write が 2（marker が 1 対でない）・byte 不変。base でも緑（今の断りを縛る・(e) の M6・M7）。
3. **f159_write_makes_nothing_it_must_not。** UTF-8 でない CLAUDE.md への --write は「読めない」の 2 で byte 不変。無い CLAUDE.md に --check は 2・--print は 0 で作らない。上限を超える fixture over-limit の --write は 1 で作らない。無い dir の下への --write は「書けない」の 2。**base では最後の形が「読めない」＝RED。**
4. **置き換える既存の歯 1 本（`crates/folio/tests/init.rs`・名は変えない）。** f152_the_skeleton_runs_every_command_without_hand_edits から marker の対を手で書く 5 行を外す。根に CLAUDE.md を置かずに --write と --check が 0 で、書いた file は begin の marker で始まり end の marker と改行で終わり、P-1.1 と R-2 を持つ。頭の注に 1 行足す。**base では --write が 2＝RED。**

### (d) 採らなかった形

1. **init が CLAUDE.md を書く。** FR22 の規範文・AC19 の書く file 11 本の閉じた一覧・init の「置き場の外には何も書かない」と食い違い、要件の直しが先に要る。区間は注入の持ち物（条 P-14）で、inject が作れば 1 つの口で閉じる。
2. **--claude-md の既定を版管理の根に替える。** 今の既定は呼んだ場所（条 P-13 の機構の注の書き込み先）で、変えると注の字が動く。作った path は字に出すので、場所の取り違えは黙らない。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **落ちる既存の歯は (c) の 4 で置き換える 1 本だけ。** 本便を当てた写しで workspace の nextest **977 / 977**・clippy 0 警告・床 4 本 rc 0・`folio build --write` は 34 file で base と diff -r 一致・folio2 自身の `inject --write` は「差が無い」で CLAUDE.md の差 0。`--test inject` 17 / 17・`--test init` 21 / 21。
2. **RED。** 歯だけを base に当てると、歯 1・歯 3・置き換えた f152 が落ち、歯 2 とほかは緑。
3. **突然変異（写しの inject.rs を 1 通りずつ変え、`--test inject` と `--test init` を撃つ）。** 11 通りとも 1 本以上が落ちる。

| 変異 | 落ちる歯 |
| --- | --- |
| M1 作らない・足さない（base と同じ） | 歯 1・歯 3・f152 |
| M2 読めなさを全部「無い」と見る（UTF-8 でない file を上書き） | 歯 3 |
| M3 --check でも作る・足す | 歯 3 |
| M4 末尾に改行が無くても空行を補わない | 歯 1 |
| M5 末尾が改行でも空行を 2 つ挟む | 歯 1 |
| M6 begin が無ければ足す（end だけの file にも） | 歯 2 |
| M7 1 対でなければ足す | 歯 2 |
| M8 利用者の字の頭に足す | 歯 1 |
| M9 「作った」と「足した」を分けない | 歯 1 |
| M10 書けなくても合格 | 歯 3 |
| M11 end の marker の後の改行を落とす | 歯 1・f152 |

### (f) 大きさ・verify と done の対応

1. **write-set。** 4 本とも印なし（書き換えるだけ）: `crates/folio/src/inject.rs`・`crates/folio/src/main.rs`・`crates/folio/tests/inject.rs`・`crates/folio/tests/init.rs`。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file | base の正規化行数（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/inject.rs` | 263 | 1237 | 290（+27） | 1210 |
| `crates/folio/src/main.rs` | 668 | 832 | 668（±0） | 832 |

   src の外は `tests/inject.rs` 249 → 410・`tests/init.rs` 942 → 941。rustfmt --check（edition 2024）の差の塊は 3 本とも base と同じ（0・0・31）。
3. **size は S。** src は inject.rs +27 と main.rs の 1 行の書き換え。
4. **verify は 4 行**で、done の 4 つの塊と 1 対 1。
   1. `cargo nextest run -p folio --test inject f159_` = (c) の 1〜3。
   2. `cargo nextest run -p folio --test inject` = 注入の歯の全部（AC4 の歯を含む・参考値 17 本）。
   3. `cargo nextest run -p folio --test init` = (c) の 4 と init の歯の全部（参考値 21 本）。
   4. `cargo clippy --workspace --all-targets -- -D warnings`。

   base では 1 が 0 件で終了コード 4、2 は 14 本・3 は 21 本で緑、4 は 0 警告。`--test` の歯の file は 2 本とも write-set に在り、単体の歯は足さない。

### (g) 門・受付・並行の便

門は対象外で 0（冒頭）。受付の先撃ち（precheck）で契約に起因する断りは 0（(h) の 3）。並行の便 158（行 fe・anchor.rs・adr.rs・tests/freeze_root.rs）とは write-set が重ならない。

### (h) 数え直す手順（行 D-13）

記録は `.local/share/folio2/handoff-2026-09-27/d159-draft.md`、script は同じ dir の d159-scripts（repo の外）。

1. 再現: repro-159.sh（(a) の 1 と 3）。模擬: build-sim-159.sh（apply-159.py・apply-159-teeth.py・c159.patch）・suite-159.sh・floor-159.sh・verify-159.sh。
2. RED: red-159.sh。突然変異・余地・fmt・門: mut-159.py・lines-159.sh・fmt-159.sh・gate-159.sh。
3. 受付の先撃ち: `~/.cache/folio2-orchestrator/r86/precheck.sh <worktree> docs/design/delivery-159.md#ff`。

### (i) 要件との関係・運ばないもの・撤退条件

1. **要件との関係（正本は書き換えない）。** FR6 の規範文（前文と規範文を持つ条を CLAUDE.md の生成区間へ書き込む）は区間が無いときの扱いを定めない。本便は、書けなかった形のうち書く場所が 1 つに決まる 2 形（file が無い・marker が 1 本も無い）で書けるようにするだけで、中身・決定性（2 回目は差が無い）・R-2 の上限は変えない（条 P-14.1・P-14.3 の字どおり）。--check は変えない（条 P-14.2・AC4 の歯は緑）。規範文の意味は変わらない（行 D-17 に当たらない）。init は今も CLAUDE.md を書かない（tests/init.rs 436 行は緑）。**古くなる字**: 便 2 の設計ノート（delivery-2.md §1 の「CLAUDE.md が無い場合は まだ分からない」）は --write に当たらなくなる（過去の記録で書き換えない）。ADR-16 決定 (3) と FR22 の注の「骨格は注入の対象にしない」は便 152 の §1 (i) の ④ が控え済みで、新しく古くなる設計文書の字は無い。
2. **運ばないもの。** (a) の 3 の手の要る所（区間の外の規範語・凍結の前の床・derive の置き場・ceiling の面と印）・--claude-md の既定・設計文書の正本・台帳への記帳・外部 crate。
3. **撤退条件。** (1) (c) の 4 のほかの既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。(2) 着地の後の main で folio2 自身の床 4 本・`folio build` の出力・`inject --write` の後の CLAUDE.md が着地の直前と 1 byte でも違ったら止めて席へ返す。(3) 受付の時点の main で inject.rs の run・tests/inject.rs の口（folio_inject・temp_dir・pinned）・tests/init.rs の f152 が base と違えば、(h) で数え直してから運ぶ。

## 2. 範囲

- 入れる: §1 (b) の 1〜4、(c) の歯 3 本と置き換え 1 本。
- 入れない: 区間の外の規範語の検査の範囲・init・--check と --print・--claude-md の既定・設計文書の正本・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| place | 区間の置き場 | inject.rs の run が無い file と marker の無い file に区間を作る |
| teeth | 歯 | tests/inject.rs の f159_ 3 本と tests/init.rs の f152 の置き換え |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地は無い（base = main a6a868d）。並行の便は §1 (g)。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。.238 を閉じる。§1 (a) の 3 の 1（区間の外の規範語）を起票するか決める。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "ff"
title = "群 A（台帳 f2-648.238）: 外の置き場は CLAUDE.md か生成区間の marker が無いと folio inject --write が まだ分からない で止まり、marker を手で書くまで注入が回らない。crates/folio/src/inject.rs の run を、--write のときだけ、CLAUDE.md が無ければ marker の対と区間だけの file を作り、marker が 1 本も無ければ利用者の字を変えずに空行 1 つを挟んで末尾に足す形にし（末尾の改行を補う・字は 作った と 足した を分ける）、書く口を write_md 1 つにまとめる。marker が在って 1 対でない形・無い以外の読めなさ・--check と --print・導出と R-2 の上限・init・folio2 自身の出力は変えない。main.rs の --write の説明 1 行を直す。歯は tests/inject.rs の f159_ 3 本と、tests/init.rs の群 A の通しの歯 f152 から手書きの CLAUDE.md を外す置き換え。門の対象外。base = main a6a868d・受付の時点の main で数え直す"
req = ["FR6"]
section = "1"
write-set = ["crates/folio/src/inject.rs", "crates/folio/src/main.rs", "crates/folio/tests/inject.rs", "crates/folio/tests/init.rs"]
verify = ["cargo nextest run -p folio --test inject f159_", "cargo nextest run -p folio --test inject", "cargo nextest run -p folio --test init", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "tests/inject.rs の f159_ の 3 本（fixture ok の正本で CLAUDE.md が無い・空・# fixture と改行・改行の無い # fixture の 4 形に --write が 0 で、書いた byte が手書きの ok/CLAUDE.md（前の 2 形は頭の # fixture と空行を除く）と等しく、字は 作った か 足した、続く --check が 0、2 回目の --write は 差が無い、folio2 自身の CLAUDE.md の写しは --write で変わらない / begin だけ・end だけ・逆順・2 対に --write が 2 で byte 不変 / UTF-8 でない file への --write が 読めない の 2 で byte 不変、無い file に --check が 2・--print が 0 でどちらも作らず、R-2 の上限を超える --write が 1 で作らず、無い dir の下への --write が 書けない の 2）が緑、tests/inject.rs の歯の全部（AC4 の歯を含む）が緑、tests/init.rs の歯の全部（根に CLAUDE.md を置かずに inject の --write と --check が 0 で、書いた file が marker の対と区間だけ、という f152 の置き換えを含む）が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio inject --write で CLAUDE.md が変わらず、folio build の出力は着地の直前の main と file 数も byte も変わらない"
<!-- contracts:end -->
