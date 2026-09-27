# 設計: 便 162 — 床の定数の写しの借りを返し、承認欄の対話面を承認者との組で縛り、種別 deny の意味を行 D-17 に揃える（台帳 f2-648.239 + f2-648.230・M）

- 要件: FR19（欄の決まりの生成区間は床の定数から決定的に導出する）・FR5（構造の床）。規範文・確かめ方・受入基準は変えない。
- 条: P-5.6（実装の定数の写しを設計文書へ導出する）/ P-6.3（値域を 1 つの定数に）/ P-12.1・P-12.2（承認の通り道と記帳）。
- 根拠: 行 D-11 と行 D-17（ADR-26 決定 (4)・f2-648 notes 2026-09-27 00:40 JST）。出所は便 158・159・161 の検証（台帳 **f2-648.239**）と天井の 49・51 周目（台帳 **f2-648.230**）。
- 承認: 行 D-17 の注により、実装の定数を変えて生成区間の規則を変える本便は「規則の表の行の変更」に入る。**持ち主の承認（一括 30 と同じ 1 回）の後に受け付ける。**承認が要る変更の一覧は §1 (i) の 1。
- 改訂 b: 検証の blocking 2 つ（④ の字・承認者と対話面の組）と非 blocking を当てた。組の判定で落ちる今の承認欄は ADR-27 だけで、同じ便で対話面を D-17 に直す（席の裁定 (A)）。改訂 b の 3 で 52 周目の整合の所見 F-3（enums_note の retreat_kind の比べ方）を足した。
- 置き場: 契約表は末尾。審査の材料は行 `fi` が指す §1 だけ。write-set 41 本・新しい file も dir も無い。
- 門: **まだ分からない（2・印が古い〔引き金の要約値が違う〕）**。design-intent の 4 file を書く便なので、区切りの周 52 の印の後に受け付ける（想定どおり）。
- 前の便: **base = main 8472b5c（便 161 の着地の後）。数は base の写しの実測（参考値・行 D-13）。**一括 30 の着地の後に席が載せ替えて受け付ける（§1 (g)）。手順は控え `.local/share/folio2/handoff-2026-09-27/d162-draft.md`。

## 1. 設計

### (a) いま起きていること（参考値・base 8472b5c）

1. **写しの無い判定（.239・行 D-11 の借り）。** 便 158・159・161 が実装の定数に足した判定の写しが、欄の決まりの生成区間に無い。
   - 雛形の印 未記入（adr.rs の UNFILLED）と、それを空と見る欄（承認欄の逐語・anchor の承認一覧の承認者と逐語）。
   - anchor の承認一覧の日付の形と確かめの順（空 → 台帳 id の形 → 印 → 日付）。
   - inject --check の区間の外の規範語の数え（normative_outside）と、folio2 の置き場の判じ方（置き場の憲法の名が列の根の表の最初の行の名と違えば数えない）。
   - schema.rs の頭の注は inject と同じ型と書くが、印の無い file に区間を作るのは inject --write だけ（便 159）。
   - enums_note は retreat_kind の比べ方を「部分集合の比較・便 122」と書くが、便 157 の後の実装（check.rs の place_range）と FR25 は同じ集合か（列の値を外した一覧も まだ分からない・52 周目の整合 F-3）。
2. **行 D-17 に揃っていない字（.230）。**
   - 対話面の値域は floor_adr.rs の SURFACE と floor_note.rs の SURFACE_ENUM の 2 つの定数で、どちらも [R-8]。席の裁定の ADR-27 も承認者 orchestrator 席・対話面 R-8 で記帳されている。
   - 床は承認者と対話面の組を見ない。値域に D-17 を足すだけだと持ち主 × D-17 も通り、条 P-12.1 を値域で縛る部分が外れる（検証の B-2）。
   - 設計ノートの注は、発効に持ち主の逐語が要り、承認欄は R-8 を通った記録にだけ置く、と書く。
   - 種別 deny の意味（kind_meaning.deny）は機械が測って落とすだけで、席が数える上限の行 R-7・R-21・R-22 と合わない（行 R-21・R-22 の注が本件を名指す）。
3. **値域に足すだけでは壊れる。** link.rs の surface は値域の全部の id に規則の表の行を求める。D-17 を足すだけだと行 D-17 の無い置き場（tsuzuri の表は D-1〜D-4・骨格は R-2・R-8・R-16）が全部落ち、骨格の答え（FR22）も変わる（M4）。承認欄が使う対話面の id は、今も id の参照の網（references）が「id が実在しない」で数える。
4. **今の承認欄の全数。** folio2 は判断の記録 27 本（持ち主 × R-8 が 26・orchestrator 席 × R-8 が ADR-27 の 1）で、設計ノートの承認欄は無い。tsuzuri は判断の記録 7 本と設計ノート 1 本で、8 本とも持ち主 × R-8。
5. **base の歯。** workspace の nextest 985 / 985・clippy 0 警告・床 4 本 rc 0・`folio build` 34 file。`f162_` と行 id `fi` は 0 件。

### (b) 直す先

1. **`crates/folio/src/floor_adr.rs`。**
   - 定数 SURFACE_OWNER（R-8）と SURFACE_SEAT（D-17 = 席の裁定の記帳先・台帳の notes）を足し、SURFACE をその 2 つにする。席の承認者 SEAT_APPROVERS（planner 席・orchestrator 席）を足し、APPROVER はこれを引く。
   - 床の木の enums に組の表 surface_approvers（R-8 → [持ち主]・D-17 → [planner 席, orchestrator 席]）を足す。組の定数はこれ 1 つ。
   - adr.rs の UNFILLED をここへ降ろし（adr.rs は `pub(crate) use`）、床の木の approval を表に替えて欄 unfilled_marker を足す（先例 amends_entry.empty_marker）。
   - 注 5 か所: date_format_note（anchor の承認一覧の date）・non_empty_note（印を空と見る欄）・enums_note（retreat_kind は同じ集合の比較〔列に無い値も、列の値を外した一覧も まだ分からない・便 157〕・D-17 と組と行の求め方）・approval_note（組）・anchor_note（承認一覧の確かめの順と、末尾の 1 項 = 列の根の表の最初の行は folio2 の行・inject --check の判じ方・区間の外の数えの式・1 行でも在れば不合格にして最初の行を出す・数えないときは知らせの 1 行）。
2. **`crates/folio/src/adr.rs`。** 判定 surface_unpaired（承認者と対話面がどちらも値域に在り、その対話面の組に承認者が無いときだけ真）を足し、check_approval が値域の確かめの後に呼ぶ。違反の字は「surface と承認者が組でない（enums.surface_approvers・P-12.1・行 D-17）」。
3. **`crates/folio/src/note.rs`。** 承認欄の確かめが同じ surface_unpaired を呼ぶ（判断の記録と同じ 1 つの定数・1 つの判定）。
4. **`crates/folio/src/floor_note.rs`。** SURFACE_ENUM は floor_adr.rs の SURFACE を引く。注 status_note.effective を「持ち主の承認か席の裁定〔行 D-17〕の行」に、approval_note を「組・印・値域も判断の記録と同じ定数・承認欄は持ち主の承認（R-8）か席の裁定（行 D-17）を通った記録に置く」に直す。
5. **`crates/folio/src/rules.rs`。** kind_meaning.deny の末尾に「機械が数える面を持たず、行の注が数える者を席と定める上限の行は、席が数えて値域の外なら止める」を足す（検証の B-1 の字）。R-1・R-6 と、tsuzuri の歯や CI が測る行は当たらない。種別は足さない。
6. **`crates/folio/src/link.rs` の surface。** 置き場の規則の表に行を求めるのは SURFACE_OWNER（R-8）だけにする。D-17 の行は、判断の記録の承認欄が使うときだけ既存の id の参照の網が求める（同じ欠けを 2 行に積まない）。頭の注に「持ち主の対話面の id だけは floor_adr.rs の定数を引く」を足し、単体の歯の値域の針を [R-8, D-17] に。
7. **`crates/folio/src/schema.rs` の頭の注。** 印が 1 対でない file は --write でも書かない（inject --write と違う）と直す。
8. **design-intent。** 3 file（adr/schema.yaml・design-note/schema.yaml・rules.yaml）の生成区間は便の binary の `folio schema --dir design-intent --write` で書き直す（区間の外は 1 byte も変えない）。adr/ADR-27.yaml は承認欄の対話面を D-17 に、注【承認】を着地の後の字に直す（ほかの字は変えない）。
9. **歯の data。** 判断の記録の欄の決まりの写し 17 本は注でない欄 3 行（値域・組・印）を、土台の設計ノートの写しは値域の 1 行を字面の置き換えで直す。凍結 anchor 3 本（adr・note・rules の region）も導出を使わずに字面の置き換えで直し、tests/schema.rs と tests/schema_docs.rs の行数・byte 数・要約値を写す。便 99 の anchor は独立の script（node-digest.py）で組み直し、tests/graph.rs に写す。case surface-knob の値は [R-8, D-17, R-9]。
10. **変えないもの。** 判定のうち印・日付・承認者の値域・裁定 id の確かめと inject の数え・既存の違反の字・anchor.rs・inject.rs・init の雛形の書き手・写しの注（床は読まない）・規則の表の行。

### (c) 歯（関数名 f162_・binary 経由・fixture は足さない）

1. **f162_the_regions_copy_the_mark_the_seat_surface_and_the_seat_limit**（tests/note.rs）。実の 3 file の生成区間で、approval の行が印の欄を、組の行が R-8 → 持ち主・D-17 → 席を、設計ノートの approval の行が値域 [R-8, D-17] を持ち、注 9 行に (b) の字が在り、発効の注に 持ち主の逐語 が無い。src の `#[cfg(test)]` より前で引用符付きの印の字を持つのは floor_adr.rs だけ（init.rs を除く・検証の V11・V13）。**base では印の欄が無い＝RED。**
2. **f162_the_seat_surface_is_one_domain_for_both_records**（tests/note.rs）。値域がちょうど [R-8, D-17] で、note.rs と floor_note.rs が値の引用符付きの字を持たない。承認者 × 対話面の 9 通り（通る = 持ち主 × R-8・orchestrator 席 × D-17・planner 席 × D-17、落ちる = 持ち主 × D-17・orchestrator 席 × R-8・R-7・D-18・前に空白の付いた D-17・d-17）を ADR-27 と見本（発効）の承認欄に置くと、判断の記録と設計ノートの違反の数が等しく、落ちる側だけ 1、通る側は合格。**base では値域が [R-8]＝RED。**
3. **f162_the_seat_row_is_needed_only_when_used**（tests/link.rs）。fixture link/retreat-kind-drift（表は R-1・R-3・R-8・D-1）の一時の写しで、そのままなら違反 0、ADR-1 に承認者 orchestrator 席・対話面 D-17 の承認欄を足すと違反はちょうど 1 件（id D-17 が実在しない）、行 R-8 を消すと 対話面 R-8 が rules 行に無い が出る。**base では値域外と実在しないの 2 件＝RED。**
4. **f162_the_outside_count_follows_the_copied_formula**（tests/inject.rs・検証役の案）。anchor_note の末項が写す数えの式を 6 通り（「ない。」・字下げ・後ろの空白・注釈の印で始まる行・字下げした注釈の行・中ほどの「する。」）で縛る。式は変えないので base に当てても緑で、式を変える変異（(e) の M16〜M18）で落ちる。
5. **既存の歯 2 本の直し。** f161_who_and_ruling_agree_with_the_adr_approval（tests/note.rs）は席の承認者の通る case を対話面 D-17 で置く（組の判定の後も同じことを縛る）。f130_the_adr_region_notes_carry_no_stale_milestone_text（tests/schema.rs）は新しい字を enums_note の今の字に替え、古い括弧（部分集合の比較・便 122）を古い字の一覧に足す。

口は region_line（tests/note.rs）と copy_tree・f162_violations（tests/link.rs）。

### (d) 採らなかった形

1. **D-17 を値域に足し link.rs の式をそのままにする。** 行 D-17 を持たない置き場（tsuzuri・骨格）が全部落ちる（(a) の 3・M4）。
2. **骨格と利用者の表に行 D-17 を足させる。** folio2 の作法の行を利用者に課し、骨格（FR22）も変わる。
3. **席が数える上限の種別を足す。** 値域 kind と憲法の機構の対応を決める要があり、依頼の断り（席へ返す形）に当たる。deny の意味の字を広げた。
4. **組を字で断るだけにする（検証の B-2 の a）か、持ち主の側だけを縛る（席は R-8 も通す・M13）。** どちらも縛りを緩める側で、席の裁定 (A) で退けた。
5. **印の欄を設計ノートの欄の決まりにも写す。** 同じ値の写しが 2 つになる（P-6.3）。注で判断の記録の欄の決まりを指す。
6. **inject の数えのために新しい生成区間を作る。** CLAUDE.md の欄の決まりの正本が無く、M を超える。判じ方の表（root_digests）の注の 1 項にした。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **落ちる既存の歯は、組の判定が答えを変える f161_ と、enums_note の字を縛る f130_ の 2 本だけ**で、(c) の 5 で直す。本便の全部を当てた写しで workspace の nextest 989 / 989・clippy 0 警告・床 4 本 rc 0。rustfmt --check の差の塊は、変えた 13 本とも base と同じ数。src だけを当てると 249 本、生成区間 3 本を schema --write で書き直しても 233 本（写しの欄と ADR-27 の組）が落ちる＝data は write-set に要る。
2. **RED。** 歯だけを base に当てると f162_ の 3 本（(c) の 1〜3）と直した f161_・f130_ の 2 本だけが落ち、tests/note.rs・link.rs・inject.rs・schema.rs のほかの 80 本は緑。
3. **突然変異。** 写しの src だけを 1 通りずつ変え、歯の束（--test note・link・schema・schema_docs・inject・graph・floor_cases と --bin folio の floor_）を撃った。**M1〜M19 は全部落ちる。**

| 変異 | 落ちる歯 |
| --- | --- |
| M1 値域から D-17 を外す / M7 印の欄を写さない / M10 印の値を別の字で持つ / M14 組の表の持ち主と席を入れ替える | 2・3・写しの床と anchor |
| M3 設計ノートが [R-8] を持つ | 2・写しの床と anchor |
| M2 設計ノートが値域を自分で持つ（同じ値） | 2 |
| M4 値域の全部の行を求める（base の式）/ M6 R-8 の代わりに D-17 の行を求める | 3・link の fixture 3 本・floor_cases |
| M5 R-8 の行を求めない | 3 |
| M8 deny の字を改訂 a の字に戻す / M9 発効の注を戻す | anchor と要約値 |
| M11 判断の記録の側で組を見ない / M12 設計ノートの側で組を見ない / M13 組を持ち主の側だけにする | 2 |
| M15 判定の側が印の字を別に持つ | 1 |
| M16 注釈の行も数える / M17 「ない。」を数えない / M18 行の頭の空白を落とさない | 4 |
| M19 enums_note の比べ方を base の字（部分集合）に戻す | anchor と要約値 |

   表の数字は (c) の歯の番号。

### (f) 大きさ・余地・verify と done

1. **write-set 41 本**（どれも印なし＝書き換えるだけ）: src 7・tests 7（tests/floor_cases.rs は verify の scope で本文不変）・design-intent 4・fixture 23。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file | base（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| floor_adr.rs | 520 | 980 | 552（+32） | 948 |
| floor_note.rs | 509 | 991 | 511（+2） | 989 |
| rules.rs | 316 | 1184 | 317（+1） | 1183 |
| adr.rs | 1049 | 451 | 1065（+16） | 435 |
| link.rs | 669 | 831 | 670（+1） | 830 |
| schema.rs | 182 | 1318 | 183（+1） | 1317 |
| note.rs | 940 | 560 | 950（+10） | 550 |

3. **size は M。** src は小さいが、file 41 本と生成区間 3 本と凍結 anchor 4 本を同時に動かす。最小の余地は adr.rs の 435（≥ 300）。
4. **verify は 11 行**で、done の塊と 1 対 1: f162_ の 3 行（(c) の 1・2 と 3 と 4）・--test note・--test link・--test schema・--test schema_docs・--bin folio の単体の歯 4 本（床の木の導出と anchor 3 本の byte 一致・値域の針）・--test graph の f99_・--test floor_cases・clippy。base では f162_ の 3 行が 0 件で終了コード 4、ほかは緑。

### (g) 受付・並行の便

受付の先撃ち（precheck）で契約に起因する断りは 0。**受付は一括 30 の着地の後で、その時点の main へ席が載せ替えて衝突を解く前提。**一括 30（枝 docs/batch29 dd63fbe）と重なる file は design-intent/rules.yaml（一括 30 は区間の外・本便は区間の中＝そのまま当たる）と adr/ADR-27.yaml（一括 30 の改訂 d が帰結の 3 つ目の今の読みを注へ移す塊が、本便の承認欄と注【承認】の塊と隣り合い、3-way では衝突する）。解き方は一括 30 の行を残して【承認】の行だけを本便の字にすることで、dd63fbe の上で nextest 989 / 989・clippy 0・床 4 本 rc 0。

### (h) 今の置き場の床が変わらないこと（撤退条件 (2) の実測）

1. **folio2 自身。** 床 4 本と凍結の 4 つの旗の出力は、schema --check の byte 数の 3 行（参考値 25693 → 27124・16789 → 17023・2263 → 2404）のほかは同じ。build は 34 file のままで、違うのは constitution.html の種別 deny の説明（+141 byte）と adr-27.html の注【承認】の 1 か所だけ。
2. **tsuzuri**（写しへ cp・repo では何も書かず git も撃たない）。base の schema --write で揃えた土台に本便の binary を当てると、書き直す前は 4 件で落ち、schema --write で 3 file を書き直すと、素の check・4 つの旗・schema --check・derive --check が base と同じ（byte 数の 3 行だけ違う）。承認欄 8 本は組の判定でも落ちず、行 D-17 は要らない。
3. **骨格。** init の骨格は base と本便で素の check が同じ（rc 2・違反 0）で、骨格の file の差は 3 file の生成区間だけ。

### (i) 承認・連絡・運ばないもの・撤退条件

1. **持ち主の承認が要る変更（行 D-17・一括 30 と同じ 1 回に載せる）。**
   - ① 対話面の値域に D-17（席の裁定の記帳先）を足し、判断の記録 enums.surface と設計ノート approval.surface_enum を 1 つの定数にする。あわせて承認者と対話面の組 enums.surface_approvers と組の判定を足し、承認者が持ち主なら対話面は R-8、承認者が席（orchestrator 席・planner 席）なら D-17 の組だけを通す（判断の記録と設計ノートが同じ判定を呼ぶ・条 P-12.1 の値域の縛りは外さない）。D-17 は folio2 の規則の表の行の id で、外の置き場が承認欄に D-17 を書くには番号 D-17 の行が要る。今の承認欄で組の判定に落ちるのは席の裁定の ADR-27 だけで、同じ便で ADR-27 の承認欄の対話面を D-17 に直す（注【承認】の古い 1 文も）。
   - ② 置き場の規則の表に対話面の行を求める式を、R-8 は常に・D-17 は承認欄が使うときだけ、にする。
   - ③ 承認欄の印の欄 approval.unfilled_marker（値 未記入）を足す（判定は便 158 のまま）。
   - ④ 種別 deny の意味に、機械が数える面を持たず行の注が数える者を席と定める上限の行は席が数えて止める、を足す（値は緩めない・R-1・R-6 と機械が測る行は当たらない）。
   - 注の直し（非空・日付・値域・retreat_kind の比べ方・承認一覧・inject の数え・発効・承認欄）は判定の説明で、規則を変えない。
2. **利用者への連絡（着地の後に席が送る字）。** folio を便 162 の後の版にしたら、置き場の根で folio schema --dir design-intent --write を 1 回撃ち、書き直った file を全部 commit してください（本便の分は adr/schema.yaml・design-note/schema.yaml・rules.yaml の 3 file。便 151 の天井の正本の書き直しがまだの置き場では ceiling.yaml も入り、tsuzuri の今の写しでは 4 file）。撃つまでは素の check と schema --check が落ちます（生成区間が床の定数と違う）。承認欄は承認者が持ち主なら対話面 R-8 だけが通ります。規則の表に行 D-17 を足す必要はありません（承認欄の対話面に D-17 を書くときだけ要ります）。
3. **要件との関係。** FR19・FR5 の規範文と確かめ方は変えない。
4. **運ばないもの（席の手番）。** 着地の後に古くなる字 7 つ: 行 R-21・R-22・D-17 の注（本件を名指す）・行 R-8 の注（承認欄の schema がこの値を要求する）・語彙の「対話面」（行 R-8 が指す場所）・ADR-16 の文脈 (オ)（対話面は行 R-8 に固定）・見本 example.yaml の meta.note（発効なら持ち主の逐語）。FR6 か条 P-14 の注から anchor_note の末項への指し先も席の一括。残る穴: 設計ノートの承認欄の D-17 は表の行を求めない（行 D-17 の無い置き場で判断の記録と答えが割れる）。
5. **撤退条件。**
   - (1) (e) の 1 の f161_・f130_ のほかに既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。
   - (2) 着地の後の main で、folio2 自身の床 4 本の結果か `folio build` の出力が、(h) の 1 の差のほかで着地の直前と違えば止めて席へ返す。
   - (3) 受付の時点の main で、(b) の箇所・写し 17 本・土台の 2 file・anchor 4 本・case surface-knob・ADR-27 の承認欄が base と違えば、数え直してから運ぶ（手順は控え d162-draft.md）。

## 2. 範囲

- 入れる: §1 (b) の 1〜9 と (c) の歯 4 本と直し 2 本。
- 入れない: §1 (b) の 10・(i) の 4・命令の旗・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

§1 (b) の 1〜9 がそのまま部品（印の写し・対話面の値域と組・席の裁定の字・写しと anchor・歯）。

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地は便 158・159・161（base に入る）と、一括 30 と、持ち主の承認（§1 (i) の 1）と区切りの周 52 の印。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。§1 (i) の 2 の連絡を利用者（tsuzuri）へ送る。台帳 .239 と .230 を閉じ、(i) の 4 の字の直しを次の一括に積む。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "fi"
title = "台帳 f2-648.239 と f2-648.230: 便 158・159・161 が実装の定数に足した判定（雛形の印と空と見る欄・anchor の承認一覧の日付と確かめの順・inject --check の区間の外の数えと判じ方）を欄の決まりの生成区間へ写し（行 D-11）、対話面の値域・承認者と対話面の組・設計ノートの発効の注・種別 deny の意味を行 D-17 に揃える。floor_adr.rs に D-17・組の表 surface_approvers・印の欄 unfilled_marker、adr.rs と note.rs に同じ組の判定、link.rs は R-8 の行だけを求め、3 file の生成区間は folio schema --write で書き、ADR-27 の対話面を D-17 に直す。持ち主の承認（行 D-17）と一括 30 と周 52 の印の後に受け付ける。enums_note の retreat_kind の比べ方を同じ集合に直す（整合 F-3）。歯は f162_ 4 本と f161_・f130_ の直し 2 本。base = main 8472b5c"
req = ["FR19", "FR5"]
section = "1"
write-set = ["crates/folio/src/floor_adr.rs", "crates/folio/src/floor_note.rs", "crates/folio/src/rules.rs", "crates/folio/src/adr.rs", "crates/folio/src/link.rs", "crates/folio/src/schema.rs", "crates/folio/src/note.rs", "crates/folio/tests/note.rs", "crates/folio/tests/link.rs", "crates/folio/tests/inject.rs", "crates/folio/tests/schema.rs", "crates/folio/tests/schema_docs.rs", "crates/folio/tests/graph.rs", "crates/folio/tests/floor_cases.rs", "design-intent/adr/schema.yaml", "design-intent/design-note/schema.yaml", "design-intent/rules.yaml", "design-intent/adr/ADR-27.yaml", "tests/fixtures/schema/adr-region.txt", "tests/fixtures/schema/note-region.txt", "tests/fixtures/schema/rules-region.txt", "tests/fixtures/schema/node-digest-anchor.txt", "tests/fixtures/floor_base/design-intent/adr/schema.yaml", "tests/fixtures/floor_base/design-intent/design-note/schema.yaml", "tests/floor_cases.yaml", "tests/fixtures/adr/effective-no-approval/adr/schema.yaml", "tests/fixtures/adr/schema-drift/adr/schema.yaml", "tests/fixtures/adr/two-adopted/adr/schema.yaml", "tests/fixtures/anchor/no-anchor/adr/schema.yaml", "tests/fixtures/anchor/root-digest-drift/adr/schema.yaml", "tests/fixtures/check/dup-key/adr/schema.yaml", "tests/fixtures/check/empty-field/adr/schema.yaml", "tests/fixtures/check/unknown-section/adr/schema.yaml", "tests/fixtures/link/adr-id-missing/adr/schema.yaml", "tests/fixtures/link/amended-by-orphan/adr/schema.yaml", "tests/fixtures/link/retreat-kind-drift/adr/schema.yaml", "tests/fixtures/refs/bad-counts/adr/schema.yaml", "tests/fixtures/refs/dangling-id/adr/schema.yaml", "tests/fixtures/refs/orphan-rule/adr/schema.yaml", "tests/fixtures/vocab/exemptions/adr/schema.yaml", "tests/fixtures/vocab/unknown-word/adr/schema.yaml"]
verify = ["cargo nextest run -p folio --test note f162_", "cargo nextest run -p folio --test link f162_", "cargo nextest run -p folio --test inject f162_", "cargo nextest run -p folio --test note", "cargo nextest run -p folio --test link", "cargo nextest run -p folio --test schema", "cargo nextest run -p folio --test schema_docs", "cargo nextest run -p folio --bin folio adr_floor_derives_the_frozen_anchor_byte_for_byte note_floor_derives_the_frozen_anchor_byte_for_byte rules_floor_derives_the_frozen_anchor_byte_for_byte floor_constants_are_read_through_the_floor", "cargo nextest run -p folio --test graph f99_", "cargo nextest run -p folio --test floor_cases", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "M"
done = "f162_ の 4 本（§1 (c) の 1〜4・tests/note.rs・link.rs・inject.rs）が緑、tests/note.rs（直した f161_ を含む）・tests/link.rs・tests/schema.rs（直した f130_ を含む）・tests/schema_docs.rs の歯の全部（生成区間の行数・byte 数・要約値と凍結 anchor の byte 一致を含む）が緑、--bin folio の単体の歯 4 本が緑、tests/graph.rs の f99_ の歯と tests/floor_cases.rs の歯の全部が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が 9 file とも一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と比べて constitution.html の種別 deny の説明と adr-27.html の注【承認】のほかは変わらない"
<!-- contracts:end -->
