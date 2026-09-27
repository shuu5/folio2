# 設計: 便 162 — 床の定数の写しの借りを返し、承認欄の対話面と種別 deny の意味を行 D-17 に揃える（台帳 f2-648.239 + f2-648.230・M）

- 要件: FR19（欄の決まりの生成区間は床の定数から決定的に導出する）・FR5（構造の床）。規範文・確かめ方・受入基準は変えない。
- 条: P-5.6（実装の定数の写しを設計文書へ導出する）/ P-6.3（値域を 1 つの定数に）/ P-12.1・P-12.2（承認の通り道と記帳）。
- 根拠: 行 D-11 と行 D-17（ADR-26 決定 (4)・f2-648 notes 2026-09-27 00:40 JST）。出所は便 158・159・161 の検証（台帳 **f2-648.239**）と天井の 49・51 周目（台帳 **f2-648.230**）。
- 承認: 行 D-17 の注により、実装の定数を変えて生成区間の規則を変える本便は「規則の表の行の変更」に入る。**持ち主の承認（一括 30 と同じ 1 回）の後に受け付ける。**承認が要る変更の一覧は §1 (i) の 1。
- 置き場: 契約表は末尾。審査の材料は行 `fi` が指す §1 だけ。write-set 39 本・新しい file も dir も無い。
- 門: **まだ分からない（2・印が古い〔引き金の要約値が違う〕）**。design-intent の 3 file の生成区間を書く便なので、区切りの周 52 の印の後に受け付ける（想定どおり）。
- 前の便: **base = main 8472b5c（便 161 の着地の後）。数は base の写しの実測（参考値・行 D-13）**で、受付の時点の main が違えば数え直す（手順は控え `.local/share/folio2/handoff-2026-09-27/d162-draft.md`）。

## 1. 設計

### (a) いま起きていること（参考値・base 8472b5c）

1. **写しの無い判定（.239・行 D-11 の借り）。** 便 158・159・161 が実装の定数に足した次の判定は、欄の決まりの生成区間に写しが無い。
   - 雛形の印 未記入（adr.rs の UNFILLED）の値と、それを空と見る欄（判断の記録と設計ノートの承認欄の逐語・anchor の承認一覧の承認者と逐語）。
   - anchor の承認一覧の日付の形（年-月-日）と確かめの順（空 → 台帳 id の形 → 印 → 日付）。
   - inject --check の区間の外の規範語の数え（inject.rs の normative_outside）と、folio2 の置き場の判じ方（置き場の憲法の名が列の根の表の最初の行の名と違えば数えない）。
   - schema.rs の頭の注は inject と同じ型と書くが、印の無い file に区間を作るのは inject --write だけ（便 159）。
2. **行 D-17 に揃っていない字（.230）。**
   - 対話面の値域は判断の記録（floor_adr.rs の SURFACE）と設計ノート（floor_note.rs の SURFACE_ENUM）の 2 つの定数で、どちらも [R-8]。席の裁定の ADR-27 も対話面 R-8 で記帳されている。
   - 設計ノートの欄の決まりの注は、発効に持ち主の逐語が要り、承認欄は持ち主との対話面（R-8）を通った記録にだけ置く、と書く。
   - 種別 deny の意味（rules.rs の kind_meaning.deny）は機械が測って落とすだけで、席が数える上限の行 R-7・R-21・R-22 と合わない（行 R-21・R-22 の注が本件を名指す）。
3. **値域に足すだけでは壊れる（本便の実測）。** link.rs の surface は値域の全部の id に置き場の規則の表の行を求める。D-17 を足すだけだと行 D-17 の無い置き場が全部落ちる（tsuzuri の表は D-1〜D-4・init の骨格は R-2・R-8・R-16 だけ＝骨格の答え〔FR22〕が変わる・(e) の M4）。一方、承認欄が使う対話面の id は、今も id の参照の網（link.rs の references）が「id が実在しない」で数える。
4. **base の歯。** workspace の nextest 985 / 985・clippy 0 警告・床 4 本 rc 0・`folio build` 34 file。`f162_` と行 id `fi` は 0 件。

### (b) 直す先

1. **`crates/folio/src/floor_adr.rs`。**
   - 定数 SURFACE_OWNER（R-8）を足し、SURFACE を [SURFACE_OWNER, D-17] にする（D-17 = 席の裁定の記帳先・台帳の notes）。
   - adr.rs の UNFILLED をここへ降ろす（adr.rs は `pub(crate) use` で引き直し、note.rs と anchor.rs の字は変えない）。
   - 床の木の approval を keys_floor の形から表に替え、欄 unfilled_marker（値は UNFILLED）を足す（先例 amends_entry.empty_marker と同じ形）。
   - 注 5 か所: date_format_note に anchor の承認一覧の date・non_empty_note に印を空と見る欄・enums_note に D-17 と行の求め方・anchor_note の承認一覧の項に確かめの順・anchor_note の末尾に 1 項（列の根の表の最初の行は folio2 の行で、inject --check の区間の外の数えの式と判じ方）。
2. **`crates/folio/src/floor_note.rs`。** SURFACE_ENUM を floor_adr.rs の SURFACE を引く形にする。注 status_note.effective を「持ち主の承認か席の裁定〔行 D-17〕の行」に、approval_note を「印と対話面の値域も判断の記録と同じ定数・承認欄は持ち主の承認（R-8）か席の裁定（行 D-17）を通った記録に置く」に直す。
3. **`crates/folio/src/rules.rs`。** kind_meaning.deny の末尾に「folio が数える面を持たない上限の行は、席が数えて値域の外なら止める」を足す。種別は足さない。
4. **`crates/folio/src/link.rs` の surface。** 置き場の規則の表に行を求めるのは SURFACE_OWNER（R-8）だけにする。D-17 の行は、判断の記録の承認欄が使うときだけ既存の id の参照の網が求める（同じ欠けを 2 行に積まない）。単体の歯の値域の針を [R-8, D-17] に。
5. **`crates/folio/src/schema.rs` の頭の注。** 印が 1 対でない file は --write でも書かない（inject --write と違う）と直す。
6. **design-intent の 3 file**（adr/schema.yaml・design-note/schema.yaml・rules.yaml）の生成区間は、便の binary の `folio schema --dir design-intent --write` で書き直す（手で書かない・区間の外は 1 byte も変えない）。
7. **歯の data。** 判断の記録の欄の決まりの写し 17 本と土台の設計ノートの写しは、注でない欄 2 行（値域・印の欄）を字面の置き換えで直す。凍結 anchor 3 本（adr・note・rules の region）は導出を使わずに字面の置き換えで直し、tests/schema.rs と tests/schema_docs.rs の行数・byte 数・要約値を写す。便 99 の anchor は独立の script（node-digest.py）で組み直し（残差の 2 行だけ）、tests/graph.rs の要約値を写す。case surface-knob の値は [R-8, D-17, R-9]（新しい値域を data 側で広げる形）。
8. **変えないもの。** 判定の振る舞い（印・日付・承認者・裁定 id の確かめと inject の数え）・違反の字・note.rs・anchor.rs・inject.rs・init の雛形の書き手・写しの注（床は読まない）・規則の表の行・ADR-27 の承認欄。

### (c) 歯（関数名 f162_・binary 経由・fixture は足さない）

1. **f162_the_regions_copy_the_mark_the_seat_surface_and_the_seat_limit**（tests/note.rs）。実の 3 file の生成区間で、判断の記録の approval の行が印の欄 未記入 を、設計ノートの approval の行が値域 [R-8, D-17] を持ち、注 8 行に (b) の字が在り、発効の注に 持ち主の逐語 が無い。**base では印の欄が無い＝RED。**
2. **f162_the_seat_surface_is_one_domain_for_both_records**（tests/note.rs）。生成区間の対話面の値域がちょうど [R-8, D-17] で、note.rs と floor_note.rs が値の引用符付きの字を持たない。値域の 2 つと値域外の 4 つ（R-7・D-18・前に空白の付いた D-17・d-17）を ADR-27 と見本（発効・承認者 orchestrator 席）の承認欄に置くと、N-4 の行と設計ノートの行がどちらも出るかどちらも出ず、値域の値なら合格。**base では値域が [R-8]＝RED。**
3. **f162_the_seat_row_is_needed_only_when_used**（tests/link.rs）。fixture link/retreat-kind-drift（表は R-1・R-3・R-8・D-1）の一時の写しで、そのままなら違反 0、ADR-1 に対話面 D-17 の承認欄を足すと違反はちょうど 1 件（id D-17 が実在しない）、行 R-8 を消すと 対話面 R-8 が rules 行に無い が出る。**base では値域外と実在しないの 2 件＝RED。**

口は region_line（tests/note.rs）と copy_tree・f162_violations（tests/link.rs）。

### (d) 採らなかった形

1. **D-17 を値域に足し link.rs の式をそのままにする。** 行 D-17 を持たない置き場（tsuzuri・骨格）が全部落ちる（(a) の 3・M4）。
2. **骨格と利用者の表に行 D-17 を足させる。** folio2 の作法の行を利用者に課し、骨格（FR22）も変わる。
3. **席が数える上限の種別を足す。** 値域 kind と憲法の機構の対応を決める要があり、依頼の断り（席へ返す形）に当たる。deny の意味の字を広げた。
4. **印の欄を設計ノートの欄の決まりにも写す。** 同じ値の写しが 2 つになる（P-6.3）。承認者の値域と同じく注で判断の記録の欄の決まりを指す。
5. **inject の数えのために新しい生成区間を作る。** CLAUDE.md の欄の決まりの正本が無く、M を超える。判じ方の表（root_digests）の注の 1 項にした。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **落ちる既存の歯は 0 本**（本便の全部を当てた写し）。workspace の nextest 988 / 988・clippy 0 警告・床 4 本 rc 0。rustfmt --check の差の塊は、変えた 11 本とも base と同じ数。src だけを変えて data を当てないと 49 本が落ちる＝data は write-set に要る。
2. **RED。** 歯だけを base に当てると f162_ の 3 本だけが落ち、tests/note.rs と tests/link.rs のほかの 42 本は緑。
3. **突然変異。** 写しの src だけを 1 通りずつ変え、verify の歯の束（--test note・link・schema・schema_docs と --bin folio の floor_ を含む単体の歯）を撃った。**M1〜M10 は全部落ちる。**

| 変異 | 落ちる歯 |
| --- | --- |
| M1 値域から D-17 を外す | 2・3・写しの床と anchor |
| M2 設計ノートが値域を自分で持つ（同じ値）/ M3 設計ノートが [R-8] を持つ | 2（M3 は写しの床も） |
| M4 値域の全部の行を求める（base の式）/ M6 R-8 の代わりに D-17 の行を求める | 3・link の fixture 3 本 |
| M5 R-8 の行を求めない | 3 |
| M7 印の欄を写さない / M10 印の値を別の字で持つ | 写しの床と anchor |
| M8 deny の字を戻す / M9 発効の注を戻す | anchor と要約値 |

   表の 2・3 は (c) の 2・3。印の欄の値を UNFILLED でなく同じ字の文字列で持つ形は振る舞いが変わらず、歯で拾えない＝審査で見る。

### (f) 大きさ・余地・verify と done

1. **write-set 39 本**（どれも印なし＝書き換えるだけ）: src 7・tests 6（src の note.rs は verify の単体の歯の名で、tests/floor_cases.rs は verify の scope で、どちらも本文不変）・design-intent 3・fixture 23。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file | base（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| floor_adr.rs | 520 | 980 | 540（+20） | 960 |
| floor_note.rs | 509 | 991 | 511（+2） | 989 |
| rules.rs | 316 | 1184 | 317（+1） | 1183 |
| adr.rs | 1049 | 451 | 1049（±0） | 451 |
| link.rs | 669 | 831 | 669（±0） | 831 |
| schema.rs | 182 | 1318 | 183（+1） | 1317 |
| note.rs | 940 | 560 | 940（本文不変） | 560 |

3. **size は M。** src は小さいが、file 39 本と生成区間 3 本と凍結 anchor 4 本を同時に動かす。最小の余地は adr.rs の 451（≥ 300）。
4. **verify は 10 行**で、done の 10 の塊と 1 対 1: f162_ の 2 行（(c) の 1・2 と 3）・--test note・--test link・--test schema・--test schema_docs・--bin folio の単体の歯 4 本（床の木の導出と anchor 3 本の byte 一致・値域の針）・--test graph の f99_・--test floor_cases・clippy。base では f162_ の 2 行が 0 件で終了コード 4、ほかは緑。

### (g) 受付・並行の便

受付の先撃ち（precheck）で契約に起因する断りは 0。一括 30（枝 docs/batch29）とは design-intent/rules.yaml が重なるが、一括 30 は生成区間の外の行だけ、本便は区間の中だけで塊は重ならない。一括 30 の後に載せて数える。

### (h) 今の置き場の床が変わらないこと（撤退条件 (2) の実測）

1. **folio2 自身。** 床 4 本と凍結の 4 つの旗の出力は、schema --check の byte 数の 3 行（参考値 25693 → 26719・16789 → 16964・2263 → 2362）のほかは同じ。build は 34 file のままで、違うのは constitution.html の種別 deny の説明の 1 か所（面が規則の表の欄の決まりを写す・+99 byte）だけ。
2. **tsuzuri**（design-intent と contracts を写しへ cp・repo では何も書かず git も撃たない）。base の schema --write で揃えた土台に本便の binary を当てると、書き直す前は 3 件（判断の記録の印の欄の欠落と値域・設計ノートの値域）で落ち、schema --write で 3 file を書き直すと、素の check・4 つの旗・schema --check・derive --check が base と同じ（byte 数の 3 行だけ違う）。承認欄 8 本は全部 R-8 で、行 D-17 は要らない。参考: tsuzuri は今も天井の正本の生成区間が便 151 より古い（base の binary で違反 2）。
3. **骨格。** init の骨格は base と本便で素の check が同じ（rc 2・違反 0）で、骨格の file の差は 3 file の生成区間だけ。

### (i) 承認・連絡・運ばないもの・撤退条件

1. **持ち主の承認が要る変更（行 D-17・一括 30 と同じ 1 回に載せる）。**
   - ① 対話面の値域に D-17（席の裁定の記帳先）を足し、判断の記録 enums.surface と設計ノート approval.surface_enum を 1 つの定数にする。
   - ② 置き場の規則の表に対話面の行を求める式を、R-8 は常に・D-17 は承認欄が使うときだけ、にする。
   - ③ 承認欄の印の欄 approval.unfilled_marker（値 未記入）を足す（判定は便 158 のまま）。
   - ④ 種別 deny の意味に、folio が数える面を持たない上限の行は席が数えて止める、を足す（値は緩めない）。
   - 注の直し（非空・日付・値域・承認一覧・inject の数え・発効・承認欄）は判定の説明で、規則を変えない。
2. **利用者への連絡（着地の後に席が送る字）。** folio を便 162 の後の版にしたら、置き場の根で folio schema --dir design-intent --write を 1 回撃ち、書き直った 3 file（adr/schema.yaml・design-note/schema.yaml・rules.yaml）を commit してください。撃つまでは素の check と schema --check が落ちます（生成区間が床の定数と違う）。規則の表に行 D-17 を足す必要はありません（承認欄の対話面に D-17 を書くときだけ要ります）。
3. **要件との関係。** FR19・FR5 の規範文と確かめ方は変えない。
4. **運ばないもの（席の手番）。** 行 R-21・R-22・D-17 の注の本件を名指す字は着地の後に古くなる（規則の表の行の直し）。ADR-27 の対話面を D-17 に直すかは席の裁定。残る穴: 設計ノートの承認欄の D-17 は表の行を求めない（note.rs は id の参照を解かない）・承認者と対話面の組（持ち主 と D-17 など）は床が見ない・違反の字の「・R-8」は変えない。
5. **撤退条件。**
   - (1) 既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。
   - (2) 着地の後の main で、folio2 自身の床 4 本の結果か `folio build` の出力が、(h) の 1 の差のほかで着地の直前と違えば止めて席へ返す。
   - (3) 受付の時点の main で、(b) の箇所・写し 17 本・土台の 2 file・anchor 4 本・case surface-knob が base と違えば、数え直してから運ぶ（手順は控え d162-draft.md）。

## 2. 範囲

- 入れる: §1 (b) の 1〜7 と (c) の歯 3 本。
- 入れない: §1 (b) の 8・命令の旗・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| mark | 印の写し | UNFILLED・approval.unfilled_marker・注 3 つ（floor_adr.rs） |
| surface | 対話面の値域 | SURFACE_OWNER と SURFACE（floor_adr.rs）・floor_note.rs が引く・link.rs は R-8 の行だけを求める |
| seat | 席の裁定の字 | 設計ノートの注 2 つ・kind_meaning.deny |
| data | 写しと anchor | 写し 18 本・anchor 4 本・定数・case・生成区間 3 本 |
| teeth | 歯 | f162_ 3 本 |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地は便 158・159・161（base に入る）と、持ち主の承認（§1 (i) の 1）と区切りの周 52 の印。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。§1 (i) の 2 の連絡を利用者（tsuzuri）へ送る。台帳 .239 と .230 を閉じ、(i) の 4 の字の直しを次の一括に積む。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "fi"
title = "台帳 f2-648.239 と f2-648.230: 便 158・159・161 が実装の定数に足した判定（雛形の印 未記入 と空と見る欄・anchor の承認一覧の日付の形と確かめの順・inject --check の区間の外の数えと folio2 の置き場の判じ方）を欄の決まりの生成区間へ写し（行 D-11・P-5.6）、対話面の値域・設計ノートの発効の注・種別 deny の意味を行 D-17 に揃える。floor_adr.rs は SURFACE を R-8 と D-17 に、UNFILLED を adr.rs から降ろして承認欄の欄 unfilled_marker に写し、注 5 か所を直す。floor_note.rs は SURFACE を引き注 2 つを直す。rules.rs の deny に席が数える上限を足す。link.rs は規則の表に R-8 の行だけを求める（D-17 は承認欄が使うときだけ既存の id の参照の網が求める）。schema.rs の頭の注を直す。3 file の生成区間は folio schema --write で書き、写し 18 本・凍結 anchor 4 本・定数・case を合わせる。判定の振る舞いは変えない。持ち主の承認（行 D-17）と区切りの周 52 の印の後に受け付ける。歯は f162_ 3 本。base = main 8472b5c"
req = ["FR19", "FR5"]
section = "1"
write-set = ["crates/folio/src/floor_adr.rs", "crates/folio/src/floor_note.rs", "crates/folio/src/rules.rs", "crates/folio/src/adr.rs", "crates/folio/src/link.rs", "crates/folio/src/schema.rs", "crates/folio/src/note.rs", "crates/folio/tests/note.rs", "crates/folio/tests/link.rs", "crates/folio/tests/schema.rs", "crates/folio/tests/schema_docs.rs", "crates/folio/tests/graph.rs", "crates/folio/tests/floor_cases.rs", "design-intent/adr/schema.yaml", "design-intent/design-note/schema.yaml", "design-intent/rules.yaml", "tests/fixtures/schema/adr-region.txt", "tests/fixtures/schema/note-region.txt", "tests/fixtures/schema/rules-region.txt", "tests/fixtures/schema/node-digest-anchor.txt", "tests/fixtures/floor_base/design-intent/adr/schema.yaml", "tests/fixtures/floor_base/design-intent/design-note/schema.yaml", "tests/floor_cases.yaml", "tests/fixtures/adr/effective-no-approval/adr/schema.yaml", "tests/fixtures/adr/schema-drift/adr/schema.yaml", "tests/fixtures/adr/two-adopted/adr/schema.yaml", "tests/fixtures/anchor/no-anchor/adr/schema.yaml", "tests/fixtures/anchor/root-digest-drift/adr/schema.yaml", "tests/fixtures/check/dup-key/adr/schema.yaml", "tests/fixtures/check/empty-field/adr/schema.yaml", "tests/fixtures/check/unknown-section/adr/schema.yaml", "tests/fixtures/link/adr-id-missing/adr/schema.yaml", "tests/fixtures/link/amended-by-orphan/adr/schema.yaml", "tests/fixtures/link/retreat-kind-drift/adr/schema.yaml", "tests/fixtures/refs/bad-counts/adr/schema.yaml", "tests/fixtures/refs/dangling-id/adr/schema.yaml", "tests/fixtures/refs/orphan-rule/adr/schema.yaml", "tests/fixtures/vocab/exemptions/adr/schema.yaml", "tests/fixtures/vocab/unknown-word/adr/schema.yaml"]
verify = ["cargo nextest run -p folio --test note f162_", "cargo nextest run -p folio --test link f162_", "cargo nextest run -p folio --test note", "cargo nextest run -p folio --test link", "cargo nextest run -p folio --test schema", "cargo nextest run -p folio --test schema_docs", "cargo nextest run -p folio --bin folio adr_floor_derives_the_frozen_anchor_byte_for_byte note_floor_derives_the_frozen_anchor_byte_for_byte rules_floor_derives_the_frozen_anchor_byte_for_byte floor_constants_are_read_through_the_floor", "cargo nextest run -p folio --test graph f99_", "cargo nextest run -p folio --test floor_cases", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "M"
done = "tests/note.rs の f162_ の 2 本（§1 (c) の 1・2）と tests/link.rs の f162_ の 1 本（§1 (c) の 3）が緑、tests/note.rs・tests/link.rs・tests/schema.rs・tests/schema_docs.rs の歯の全部（生成区間の行数・byte 数・要約値と凍結 anchor の byte 一致・tests/schema.rs の上限を含む）が緑、--bin folio の単体の歯 4 本（床の木の導出と凍結 anchor 3 本の byte 一致・値域の針）が緑、tests/graph.rs の f99_ の歯と tests/floor_cases.rs の歯の全部が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が 9 file とも一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と比べて constitution.html の種別 deny の説明のほかは変わらない"
<!-- contracts:end -->
