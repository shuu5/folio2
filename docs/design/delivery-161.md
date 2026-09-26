# 設計: 便 161 — 設計ノートの承認欄を判断の記録の承認欄と同じ形で確かめる（雛形の印「未記入」を含む・群 A・台帳 f2-648.240）

- 要件: FR9（設計ノートを 1 つの型で生成する・正本の形〔欄の非空〕は構造の床で数える）。規範文・確かめ方・受入基準 AC7 は変えない。
- 条: P-5.6（実装を設計文書の写しの字へ揃える向き）/ P-6.3（同じ内容を 2 つの面に持たない＝値域・形・印の定数は adr.rs と floor_adr.rs の 1 つを使う）/ P-12.2（承認は逐語と日付を添えて記帳する）。
- 出所: 便 158 の独立の検証（`.local/share/folio2/handoff-2026-09-27/d158-verify.md` の非 blocking 5・note.log）と台帳 **f2-648.240**。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `fh` が指す §1 だけ。write-set は 2 本で、新しい file も dir も無い。
- 門: 対象外。作業ツリー planner-d161 の一番上で base の binary に write-set 2 本を渡すと **0（通す・設計文書の正本を書き換えない便）**。base と本便の写しでも 0。
- 前の便: **base = main 346f825（便 158 の着地の後）。数は base の写しの実測（参考値・行 D-13）**で、受付の時点の main が違えば数え直す。
- 改訂 b: 席の依頼（注 approval_note と実装の食い違いを実装で揃える）を採った。承認者の値域と裁定 id の形を課し、印を空と見る欄は逐語だけにした（(b)）。歯を 3 本に組み直し、(a)(c)〜(f)(h)(i)・title・done を直した。write-set・verify・size は変えない。

## 1. 設計

### (a) いま起きていること（参考値・base 346f825）

1. **設計ノートの承認欄は、欄の決まりの注が言う形を確かめていない。** `crates/folio/src/note.rs` の check_meta は承認欄の各項の 5 欄（承認者・日付・裁定 id・逐語・対話面）に非空を課し、形は日付（年-月-日）と対話面（値域 R-8）だけを見る。
   - 設計ノートの欄の決まり（design-note/schema.yaml の生成区間）の注 approval_note は「承認者の値域・裁定 id の形は判断の記録の欄の決まり（adr/schema.yaml）と同じ定数を床が持つ」と書く。実装はこの 2 つを課さない＝設計文書と実装の食い違い。
   - init の雛形の印「未記入」は空でない字として通る。
2. **観測（base の binary）。** `folio init` の骨格の置き場に発効の設計ノートを 1 本足し、承認欄の 1 項を形ごとに変えて素の check を撃った。
   - 逐語だけ・承認者だけ・裁定 id だけ・3 欄とも 未記入、前後に空白の付いた逐語の印は、どれも**違反 0**（骨格のままと同じ rc 2）。
   - 日付と対話面の印はそれぞれの形の行 1 本で落ち、空の字（引用符 2 つ）の逐語は「verbatim が空」の 1 行。
3. **承認欄の全数。** 便 158 は「非空を課す欄のうち、形の決まりを持たない欄だけが印を空と見る」を下の表の上 2 行に入れた。床が承認欄を読む所を全部挙げた。

| 承認欄 | 床が課すもの | 印 |
| --- | --- | --- |
| 判断の記録の承認欄（adr.rs の check_approval） | 5 欄の非空と、承認者・対話面の値域・日付・裁定 id の形 | 逐語を空と見る（便 158） |
| 憲法の anchor の承認一覧と、--freeze-start が書く写し（anchor.rs の check_approvals） | 承認者・裁定 id・逐語の非空・裁定 id の形・日付 | 承認者と逐語を空と見る（便 158） |
| 憲法の meta.approval（素の check） | 読まない（凍結の前は上の行の写しが読む） | 上の行のとおり |
| **設計ノートの承認欄（note.rs の check_meta）** | 5 欄の非空・日付・対話面 | **見ない＝本便で 1 行目と揃える** |
| 要件書・入口・相談窓口・天井の正本・索引の欄の決まりの meta.approval（役と日付の行・逐語の欄を持たない形） | 何も課さない（床は欄を読まない） | 原理の外（非空を課さない） |

   最後の行は、骨格の 5 file に「5 欄とも印の行」か「5 欄とも空の字の行」を足しても素の check が骨格のままと 1 byte も違わない（10 形）。**揃える先は設計ノートの 1 か所だけ**で、S に収まる。
4. **base の歯。** workspace の nextest 977 / 977・clippy 0 警告・床 4 本 rc 0・`folio build --write` の出力 34 file。`--test note` は 36 本。`f161_` と行 id `fh` は 0 件。

### (b) 直す先

1. **`crates/folio/src/note.rs` の check_meta（承認欄の各項）。** 非空の確かめ（今のまま）の後に、欄の決まりの欄の順で次を見る。どれも値が空でないときだけ見て（空は今の「が空」の 1 行だけ）、違反は種別 note で 1 欄 1 行。
   1. 承認者: 判断の記録と同じ値域（floor_adr.rs の APPROVER）に無ければ「meta の approval[n]: who「<値>」が一覧に無い（判断の記録の承認者の値域）」。判定は adr.rs の in_enum（前後の空白を落とさずに比べる）。
   2. 日付: 今のまま。
   3. 裁定 id: 台帳 id の形（adr.rs の has_ledger_id）を持たなければ「meta の approval[n]: ruling「<値>」に台帳 id（<floor_adr.rs の RULING_PATTERN>）が無い」。
   4. 逐語: 雛形の印（adr.rs の UNFILLED と unfilled・前後の空白を落として印そのものか）なら「meta の approval[n] の verbatim が 未記入（init の雛形の印・空と同じ）」。状態（発効・草案・廃止）を問わない。
   5. 対話面: 今のまま。
2. **原理は便 158 と同じ 1 つ。** 判断の記録の承認欄と同じく、形を持たないのは逐語だけになるので、印を空と見るのは逐語だけ。承認者・裁定 id・日付・対話面の印は、それぞれの形の行が 1 本で落とす（2 重に積まない）。印を含むだけの字は印でない。
3. **定数と判定は 2 つ目を作らない（P-6.3）。** note.rs の use に adr.rs の UNFILLED・unfilled・in_enum・has_ledger_id と floor_adr.rs の APPROVER・RULING_PATTERN を足す。
4. **変えないもの。** note.rs のほかの確かめ・床の定数（floor_note.rs の FLOOR と、その写しの生成区間）・init の雛形・adr.rs・floor_adr.rs・anchor.rs・(a) の 3 の表のほかの承認欄・folio2 自身の床と面。

### (c) 歯（関数名 f161_・`crates/folio/tests/note.rs`・binary 経由）

口を 2 つ足す: approve（見本 example.yaml の status を替えて承認欄の 1 項を置く）と row_with（良い 1 項から 1 欄か 5 欄を替えた字）。fixture は足さない。頭の注に 1 行足す。

1. **f161_the_verbatim_mark_is_empty。** 発効の見本で逐語を 未記入 と「　未記入 」（全角と半角の空白付き）、草案の見本で逐語を 未記入 → どれも rc 1 で違反ちょうど 1 件（種別 note・逐語の印の行）。逐語が「未記入の欄は無いので承認する」なら合格。**base では rc 0＝RED。**
2. **f161_who_and_ruling_take_the_adr_shape。** 承認者だけ 未記入 → 承認者の値域の行 1 本だけ、裁定 id だけ 未記入 → 台帳 id の行 1 本だけ（印の行を 2 重に積まない）。承認者が空の字 → [欄の非空] の 1 行だけ。5 欄とも 未記入 → rc 1 で違反はちょうど 5 行（承認者・日付・裁定 id・逐語・対話面の順）。**base では 5 欄の形が 2 行＝RED。**
3. **f161_who_and_ruling_agree_with_the_adr_approval。** 同じ承認者と裁定 id を ADR-2 の承認欄と見本の承認欄に置いて 1 回撃ち、判断の記録の N-4 の行と設計ノートの行が、どちらも出るかどちらも出ないかを見る。
   - 承認者は判断の記録の欄の決まりの生成区間の approver の 3 つ（通る）と値域外の 4 つ、裁定 id は台帳 id を持つ 3 つと持たない 4 つ（値は done）。
   - あわせて、note.rs の字に approver の値の引用符付きの字が無い（値域を自分で持たない）ことを見る。
   - **base では 持ち主（shuu5）などで判断の記録だけが落ちる＝RED。**

「当たらない」ことの主張（(h)）は既存の歯が持つ: note_canonical_copy_passes（folio2 の実の設計ノートの写しが合格）と、tests/init.rs の f125_init_writes_the_skeleton_and_the_floor_passes（骨格の床）。どちらも workspace の nextest で本便の後も緑。

### (d) 採らなかった形

1. **承認者と裁定 id にも印の行を積む（改訂の前の形）。** 形を課した後は、同じ印を形の行と印の行で 2 重に数える（(e) の M5）。
2. **値域と形を note.rs が自分の定数と判定で持つ。** 今は同じ値でも、判断の記録の値域が変わると設計ノートだけ古くなる（P-6.3・M8〜M11）。
3. **adr.rs の check_approval をそのまま呼ぶ。** 種別（N-4）と場所の字が設計ノートの字面と違い、既存の日付と対話面の行の字が変わる。
4. **印を check.rs の non_empty（全ての正本が使う空の確かめ）に入れる。** 骨格の憲法・要件書の 未記入 の欄が全部違反になり、骨格の答え（FR22・rc 2・違反 0）が変わる。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **落ちる既存の歯は 0 本。** 本便を当てた写しで workspace の nextest 980 / 980・clippy 0 警告・床 4 本 rc 0・`--test note` 39 / 39。rustfmt --check の差の塊は 2 本とも 0（base も 0）。
2. **RED。** 歯だけを base に当てると f161_ の 3 本だけが落ち、ほかの 36 本は緑。
3. **突然変異。** 写しの note.rs だけを 1 通りずつ変え、`--test note` を撃った。**生き残る変異は無い。**

| 変異 | 落ちる歯 |
| --- | --- |
| M1 逐語の印を見ない / M14 逐語の印を「が空」の字で積む | 1・2 |
| M2 印の前後の空白を落とさない / M3 印を含む字も印と見る / M4 発効の文書でだけ印を見る | 1 |
| M5 承認者と裁定 id にも印の行を積む / M12 空の承認者にも値域の行を積む / M13 承認者の行を日付の行の後に積む | 2 |
| M6 承認者の値域を見ない / M7 裁定 id の形を見ない | 2・3 |
| M8 値域を別の定数で持つ（orchestrator 席を欠く）/ M9 値域を別の定数で持つ（今は同じ値の写し）/ M10 裁定 id を別の判定で見る（「-」を含むか）/ M11 承認者を前後の空白を落として比べる | 3 |

   表の 1・2・3 は (c) の 1・2・3。

### (f) 大きさ・verify と done の対応

1. **write-set。** 2 本とも印なし（書き換えるだけ）: `crates/folio/src/note.rs`・`crates/folio/tests/note.rs`。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file | base の正規化行数（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/note.rs` | 916 | 584 | 941（+25） | 559 |

   src の外は `tests/note.rs` 721 → 871。
3. **size は S。** src は 1 本で +25。
4. **verify は 3 行**で、done の 3 の塊と 1 対 1: `--test note f161_`（(c) の 1〜3）・`--test note`（全部・参考値 39 本）・clippy。base では 1 が 0 件で終了コード 4、2 は 36 本で緑、3 は 0 警告。`--bin` の行は無い。

### (g) 門・受付・並行の便

門は対象外で 0（冒頭）。受付の先撃ち（precheck）で契約に起因する断りは 0。並行の便 159（inject.rs・main.rs・tests/inject.rs・tests/init.rs）と便 160（tests/sheet.rs だけ・席が確かめ済み）とは write-set が重ならない。

### (h) 今の置き場の床が変わらないこと（撤退条件 (2) の実測）

1. **folio2 自身。** 設計ノート 2 本は見本（status example）で承認欄を持たない。床 4 本・build（34 file）・凍結の 4 つの旗の出力（標準出力・標準エラー・rc・書いた file）が base と本便で 1 byte も違わない。
2. **tsuzuri。** design-intent と contracts を写しへ cp して撃った（tsuzuri の repo では何も書かず git も撃たない）。承認欄を持つ設計ノートは surface.yaml だけで、承認者は値域に在り、裁定 id は台帳 id を持つ。素の check・schema --check・derive --check・4 つの旗の出力が base と本便で一致した（1 は両方とも ceiling.yaml の生成区間の古さ）。逐語を 未記入 にした写しでだけ、本便が 1 行を足す。
3. **骨格。** init の骨格のままの素の check は base と本便で同じ rc 2・違反 0（骨格は設計ノートを書かない）。(a) の 3 の 10 形も同じ。

### (i) 要件との関係・運ばないもの・撤退条件

1. **要件との関係（正本は書き換えない）。** FR9 の規範文と確かめ方は変えない。本便は、欄の決まりの注が既に言う形を実装に揃え、「欄の非空」の中身を締めるだけで意味は同じ。骨格の答え（FR22）も変わらない。生成区間を変えないので、行 D-17 の持ち主の承認は要らない。
2. **運ばないもの（借り・行 D-11）。** 承認者の値域と裁定 id の形は、判断の記録の欄の決まりの生成区間（approver・ruling_pattern）に写しが在り、設計ノートの注 approval_note がそれを指す。新しく借りになるのは、設計ノートの逐語で印を空と見る判定だけで、便 158 の借り（判断の記録の逐語の印）と同じ台帳 **f2-648.239** の一括に束ねる。
   - 残る穴: 対話面の値域は R-8 だけ（席の裁定の記帳先は台帳 f2-648.230）。持ち主の承認そのもの（P-12.1・P-12.3）は機械では締まらない。
3. **撤退条件。**
   - (1) 既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。
   - (2) 着地の後の main で、次のどれかが着地の直前と 1 byte でも違ったら止めて席へ返す: folio2 自身の床 4 本の結果・`folio build` の出力・tsuzuri の写しの素の check。
   - (3) 受付の時点の main で、note.rs の check_meta の承認欄の箇所、adr.rs の UNFILLED・unfilled・in_enum・has_ledger_id、floor_adr.rs の APPROVER・RULING_PATTERN、ADR-2 の承認欄、tests/note.rs の口 Work のどれかが base と違えば、下の手順で数え直してから運ぶ。

数え直しの手順（行 D-13）: 記録は `.local/share/folio2/handoff-2026-09-27/d161-draft.md`、script は同じ dir の d161-scripts（repo の外）。写し = setup、観測 = repro・survey、模擬 = apply-161b.py・apply-161b-teeth.py（差分は c161b.patch・r161b-teeth.patch）、検査 = suite・verify・red-161b・mut-161b.py・lines・fmt、置き場 = floor・tsuzuri、門 = gate（各 -161）。

## 2. 範囲

- 入れる: §1 (b) の 1、(c) の歯 3 本と口 2 つ。
- 入れない: adr.rs・floor_adr.rs・anchor.rs・check.rs・床の定数とその写し・init の雛形・ほかの承認欄・命令の旗・設計文書の正本・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| shape | 設計ノートの承認欄の形 | note.rs の check_meta で承認者の値域・裁定 id の形・逐語の印を欄の順に 1 欄 1 行で積む（adr.rs と floor_adr.rs の定数と判定を使う） |
| teeth | 歯 | tests/note.rs の f161_ 3 本・approve・row_with |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地は便 158（UNFILLED と unfilled・base に入る）。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。台帳 .240 を閉じ、.239 の一括に (i) の 2 の写しを 1 行足す。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "fh"
title = "群 A（台帳 f2-648.240）: 設計ノートの承認欄（crates/folio/src/note.rs の check_meta）は、欄の決まりの注 approval_note が言う判断の記録と同じ承認者の値域と裁定 id の形を課さず、init の雛形の印 未記入 も空と見ないので、承認者・裁定 id・逐語が 未記入 でも違反 0 で通る。承認欄の各項で非空の確かめの後に、欄の順で、承認者を floor_adr.rs の APPROVER と adr.rs の in_enum で、裁定 id を adr.rs の has_ledger_id で確かめ、形を持たない逐語だけが adr.rs の UNFILLED と unfilled で印を空と見る（便 158 の原理・1 欄 1 行・種別 note・2 つ目の定数を作らない）。ほかの承認欄は便 158 で揃ったか床が読まない。床の定数とその写し・init の雛形・adr.rs と floor_adr.rs と anchor.rs・設計文書の正本は変えず、folio2 と tsuzuri の写しの床も変わらない。歯は tests/note.rs の f161_ 3 本。門の対象外。base = main 346f825・受付の時点の main で数え直す"
req = ["FR9"]
section = "1"
write-set = ["crates/folio/src/note.rs", "crates/folio/tests/note.rs"]
verify = ["cargo nextest run -p folio --test note f161_", "cargo nextest run -p folio --test note", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "tests/note.rs の f161_ の 3 本（見本を発効にして逐語を 未記入 か全角と半角の空白を付けた印にするか、草案にして逐語を 未記入 にすると素の check が rc 1 で違反はちょうど 1 件〔種別 note・meta の approval[0] の verbatim が 未記入（init の雛形の印・空と同じ）〕・未記入の欄は無いので承認する なら合格 / 承認者だけ 未記入 なら who の値域の行 1 本だけ・裁定 id だけ 未記入 なら ruling の台帳 id の行 1 本だけ・承認者が空の字なら 欄の非空 の 1 行だけ・5 欄とも 未記入 なら rc 1 で違反はちょうど 5 行〔承認者・日付・裁定 id・逐語・対話面の順〕 / 同じ承認者と裁定 id を ADR-2 と見本の承認欄に置くと、判断の記録の欄の決まりの生成区間の approver の 3 つと f2-648.37 notes・t3-hub.1（裁定）・x9-a はどちらも通り、持ち主（shuu5）・未記入・席・前後に空白の付いた 持ち主 と 口頭・未記入・F2-648・f2- はどちらも落ち、note.rs の字に approver の値の引用符付きの字が無い）が緑、tests/note.rs の歯の全部が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と file 数も byte も変わらない"
<!-- contracts:end -->
