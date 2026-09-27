# 設計: 便 164 — 列の根を二段で照らす（表に無い名の置き場は版管理に最初に記録した anchor が根・判断の記録 ADR-29・台帳 f2-648.233）

- 要件: FR23（列の根の照らし）と FR5（照らせないものを合格にしない）。FR23 の題・規範文・確かめ方・注は一括 31（枝 docs/batch31・ADR-29 と同じ承認）で二段の根に置き換わる。本便はその実装で、**一括 31 の着地（ADR-29 の発効）の後に受け付ける**。
- 条: P-4.2（照らせないは まだ分からない）/ P-10.2（表に無い名の根は版管理の記録と突き合わせる・生成物どうしではない）/ N-3.1（例外の口を足さない＝旗も置き場の欄も足さない）/ P-6.3（逆引きは同じ表 ROOT_DIGESTS を引く・2 つ目の表を作らない）。
- 出所: 台帳 **f2-648.233** の論点 1〜4 への持ち主の裁定（2026-09-27 10:47 JST・逐語「論点は推奨で良い」）と ADR-29 決定 (1)(2)(7)。材料は `.local/share/folio2/handoff-2026-09-27/rootdigests-options.md` §3 の (c)。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `fk` が指す §1 だけ。write-set は 7 本で、新しい file も dir も無い。
- 門: 本契約の write-set（書かない形・7 本）で **0（通す・設計文書の正本を書き換えない便）**。
- 前の便: **base = main 8472b5c に便 162 の模擬（`.local/share/folio2/handoff-2026-09-27/d162-scripts/c162b.patch`）を当てた写し。数は参考値（行 D-13）**。本便の差分は main にも便 162 の後にも当たる（(g) の 3）。
- 改訂 a（席の裁定 2026-09-27）: 書かない形を採った（(g) の 1）。名が無いか 未記入 のままの `--freeze-start` を承認欄の 未記入（便 155）と同じ形で断る 1 か所と歯 1 本を足した（(b) の 4・(c) の 7）。受付の順を (g) の 2 に書いた。

## 1. 設計

### (a) いま起きていること（参考値）

1. **列の根の表は許可の一覧になっている。** 表 ROOT_DIGESTS（`crates/folio/src/floor_adr.rs`・2 行）に名が無い置き場では、始まりの凍結（`freeze.rs` の check_root）が「表に無い（行を足すのは folio2 の便）」で断り、凍結済みの列の素の床（`anchor.rs` の check_root）も違反 1 で落とす。外の置き場は、folio2 の便で表に行を足して組み直すまで合格に届かない（次の世代の置き場では便 133・134 と 2 時間 42 分）。
2. **観測（base の binary・受け入れの物差しの手順）。** 版管理の中の一時の置き場（次の世代の置き場とは別）で、init → 憲法の名（kumo-constitution）と承認欄を埋めて commit → `--freeze-start` を撃つと rc 1（表に無い名の 1 行・組んだ木の digest の全桁）で、anchors/ は書かれず、素の床は まだ分からない 2 のまま（`root233-scripts/accept-base.log`）。
3. **表が上乗せしている守りは 1 つだけ。** 新しい版管理で別の中身の第 1.0 版から列を始め直す手を止めること。同じ repo の中の作り直し（anchor を消して凍結し直す・根の無い枝）は、版管理の照合（`gitcheck.rs`）と始め直しの拒否が表に依らず止める（ADR-29 の文脈 (2)）。
4. **版管理の照合の今の形。** `gitcheck.rs` の check_git は anchors/ の各 file を全ての参照の履歴の各記録と比べるが、形式の違う記録（固定の欄 digest_algo を欠く）は移行の痕跡として見ない。浅い写しは anchor が 1 本も無いときだけ まだ分からない にする。
5. **base の歯。** workspace の nextest 989 本（`--test freeze_root` 14・`--test anchor` 14・`--test gitcheck` 4・`--bin folio` 147）・clippy 0 警告・床 4 本 rc 0・`folio build --write` の出力 34 file。`f164_` と行 id `fk` は 0 件。

### (b) 直す先

1. **`crates/folio/src/adr.rs`。** 表の逆引き root_owner（要約値が表のどれかの行の根と同じなら、その行の名）を足す。引くのは root_digest と同じ ROOT_DIGESTS。root_digest の注を二段の形に直す。
2. **`crates/folio/src/anchor.rs` の check_root（素の床）。** 表に在る名は今のまま（値の違いは違反・一致は何もしない・字も同じ）。表に無い名は次の順。
   1. 索引の根の digest が表のどれかの行と同じなら違反（種別 anchor）「index.yaml: 列の根 v1.0 の憲法の名〈名〉は列の根の表に無いが、索引の digest〈digest〉は表の〈行の名〉の行の根と同じ（表に在る列は名を変えても表で照らす・名を戻す）」。
   2. そうでなく、根 anchors/constitution-v1.0.yaml を版管理で照らせなければ まだ分からない 1 行「index.yaml: 列の根 v1.0 の憲法の名〈名〉は列の根の表に無い＝根は版管理に最初に記録した anchors/constitution-v1.0.yaml で照らすが、〈理由〉（まだ分からない・P-4.2）」。理由は 3 つ: 版管理と照合できない（版管理の外）・浅い写し・HEAD に記録されていない。
   3. 照らせれば何も足さない（記録との中身の比べは 3）。
3. **`crates/folio/src/gitcheck.rs`。** check_git が根の file 名（表に無い名のときだけ）を受け取る。Tracked が浅い写しの印を持ち、root_unseen が 2 の 2 の理由を返す。履歴の照合で、根の file だけは形式の違う記録も免除せず、中身が違えば違反「anchors/constitution-v1.0.yaml は表に無い名の列の根で、版管理の履歴の記録と中身が違う（〈commit〉・根は最初の記録の anchor・形式を問わず差し替えない）」。表に在る名の置き場と、根でない file は今のまま。
4. **`crates/folio/src/freeze.rs` の check_root（`--freeze-start` と `--freeze-anchor`）。** 表に無い名は次の 2 つのときだけ断る（どちらも違反・種別 anchor・両方なら 2 行）。
   1. 名が無いか init の雛形の印（adr.rs の unfilled＝前後の空白を落として 未記入）: 「列の根の凍結だが憲法の名〈名〉は置き場の名でない（無いか 未記入＝init の雛形の印・空と同じ）＝〈旗〉は凍結しない（meta.id に置き場の名を書く）」。名が無いときの〈名〉は「（meta.id が無い）」。承認欄の 未記入 を断る便 155 と同じ原理（印を空と見る）で、表の断りが消えた後も名を書かずに列を始めない（改訂 a・席の裁定）。
   2. 組んだ木の digest が表のどれかの行と同じ: 「列の根の凍結だが憲法の名〈名〉は列の根の表に無いのに、組んだ木の digest〈digest〉は表の〈行の名〉の行の根と同じ＝〈旗〉は凍結しない（表に在る列の根を別の名で始め直さない・名を戻す）」。

   始まりの凍結の告げの末尾に「・列の根は表に無い名＝commit した最初の記録が根（digest〈全桁〉）」を足す（表へ任意に登録するときの値）。
5. **変えないもの。** 表 ROOT_DIGESTS とその 2 行・表に在る名の照らしとその字・床の定数（FLOOR）の注と、その写しの生成区間（書かない形・(g)）・init の雛形・承認欄の確かめ（便 155・158）・始め直しの拒否・設計文書の正本・fixture。旗も置き場の欄も足さない（N-3.1）。

### (c) 歯（関数名 f164_）

`crates/folio/tests/freeze_root.rs` に定数 1 つ（表に無い名 KUMO）と口 4 つ（列の根の行を拾う root_lines・骨格に名と承認欄を埋める kumo・根の固定の欄を外す drop_algo・まだ分からない の手書きの 1 行 unseen）と歯 5 本を足し、1 本の期待を反転する。fixture は足さない。頭の注の 3 と 11 を直す。

1. **f164_unlisted_skeleton_passes_after_the_start_and_the_commit（受け入れの物差し）。** 表に無い名の骨格で `--freeze-start` が rc 0 で 3 file（constitution-v1.0.yaml・ids-v0.1.yaml・index.yaml）を書き、告げに根の digest の全桁（書いた根の file の digest と同じ 64 桁）が在る。commit の前の素の床は rc 1 で列の根の行はちょうど 1 行（HEAD に記録されていない の まだ分からない）。commit の後は rc 0・合格（違反 0・まだ分からない 0）・列の根の行 0。**base では凍結が rc 1＝RED。**
2. **f164_unlisted_root_is_unknown_on_a_shallow_or_bare_copy。** 凍結して commit した 1 の置き場を、深さ 1 の写しと版管理の外の複製で撃つと、どちらも rc 2・違反 0・列の根の行はちょうど 1 行（浅い写し／版管理と照合できない の まだ分からない）。**base では凍結が断られ置き場が作れない＝RED。**
3. **f164_unlisted_root_is_checked_against_every_record。** 表に無い名の根を、固定の欄を外した形で最初に commit し、正しい形に戻して commit すると rc 1・違反ちょうど 1 件（根の履歴の違反の頭の字）。表に在る名（folio2 の床の土台）の同じ操作は今までどおり rc 0・違反 0（形式の違う移行の記録を見ない）。**base では凍結が断られる＝RED。**
4. **f164_a_listed_root_under_another_name_names_its_row。** folio2 の床の土台の名を表に無い名に書き換えると、素の床の anchor の違反はちょうど 1 行（(b) の 2 の 1 の字・行の名 folio2-constitution）。anchors/ を外し表を空にして名を書き換えた置き場の `--freeze-start` は rc 1・違反ちょうど 1 行（(b) の 4 の字）で anchors/ を作らない。**base では表に無いの字＝RED。**
5. **f164_foreign_root_rests_on_the_record_and_fails_by_row（f121_foreign_root_fails_by_name_and_by_row の改名と前半の反転）。** 自分自身と一致する別の中身の根（tests/fixtures/anchor/root-digest-drift）を表に無い名のまま撃つと rc 2・違反 0・列の根の行 0（根は版管理の記録と同じ）。folio2 の名に書き換えると今までどおり表の行と違うで落ちる（後半は変えない）。**base では前半が rc 1＝RED。**
6. **`crates/folio/src/adr.rs` の単体の歯 f164_root_owner_finds_the_row_by_digest。** 表の各行の digest はその行の名を引き、次の世代の置き場の digest は tsuzuri-constitution を引き、64 桁の 0・空の字・名の字は何も引かない。
7. **f164_unfilled_name_is_refused_like_the_approval（改訂 a）。** 承認欄を埋めた骨格で、名が 未記入・前に全角の空白の付いた 未記入・meta.id の行が無い の 3 通りとも、`--freeze-start` は rc 1・違反ちょうど 1 行（(b) の 4 の 1 の字）で anchors/ を作らない。名を表に無い名に書けば同じ置き場で rc 0。**base では表に無いの字＝RED。**

受け入れの物差しの 3 つの止まり方は歯が縛る: 改名で逃げる列 = 4（と既存の f121_renamed_constitution_fails_the_floor_twice）・浅い写し = 2・根を作り直した列 = 表に在る名は 5 の後半と既存の f121_ / f134_ の歯（今と同じ）、表に無い名の同じ repo の中の差し替えは 3。表に無い名の置き場で新しい版管理から作り直す手は床の外（ADR-29 決定 (3)・(i) の 2）。

歯は環境に依らない。CI の既定の浅い取り出しでは、folio2 の repo の中の fixture root-digest-drift に浅い写しの まだ分からない が標準エラーに 1 行増えるが、anchor.rs の歯は違反・rc・標準出力だけを見る。

### (d) 採らなかった形

1. **名が 未記入 のままの凍結を通す（改訂 a の前の形）。** 承認欄の 未記入 を断る便 155 と揃わず、名を書かずに列を始められる（席の裁定）。
2. **凍結の前の置き場を合格として返す。** 実行できなかった検査を合格と表示しない（FR5・P-4.1）に当たる（ADR-29 案 e）。
3. **根の digest を置き場の欄（索引など）に書いて照らす。** 置き場が自分で書いた値との突き合わせで、生成物どうしの比べ（P-10.2）。ADR-29 案 f のうち「根を置き場の欄で選ぶ形」。
4. **表に無い名の根にも形式の免除を残す。** 形式を変えた記録を先に入れて根を差し替える道が残る（(e) の M6）。
5. **逆引きを床だけか凍結だけに置く。** 改名して凍結するか、改名して床を撃つかで逃げられる（M2・M3）。
6. **浅い写しと版管理の外で根を違反にする。** CI の既定の取り出しで落ち、照らせないを違反にする（P-4.2・M11）。
7. **表に在る名にも形式を問わない照合を掛ける。** folio2 の床の土台（形式の違う移行の記録を持つ）が落ち、表に在る名の答えが変わる（M10）。
8. **注の字（FLOOR の注とその写し）を本便で書く（書く形）。** 門が 2 になり、便 162 と write-set が重なる（(g) の 1・席は書かない形を採った）。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **src だけを当てると落ちる既存の歯は 5 本**で、どれも ADR-29 が変える答えを縛っていた。write-set の歯の file 3 本で期待を直す。
   - freeze_root.rs: f121_foreign_root_fails_by_name_and_by_row（前半を反転し f164_ へ改名＝(c) の 5）・f155_skeleton_freeze_start_refuses_the_empty_approval と f158_skeleton_freeze_start_reads_the_mark_and_the_date（骨格の凍結の違反は 2 件のまま、名の行の字が「表に無い」から「置き場の名でない」に変わる＝数える字を 名でない に直す）。
   - tests/anchor.rs: anchor_root_digest_drift_fails → anchor_root_digest_drift_is_not_a_root_violation（rc 2・違反 0・標準出力に列の根の行が無い）。
   - tests/gitcheck.rs: gitcheck_anchor_removed_from_worktree_fails（違反 2 件以上と列の根 → 消した anchor の違反ちょうど 1 件）。
2. **RED。** 歯だけを base に当てると 37 本のうち 10 本が落ちる（(c) の 1〜5・7 の 6 本と、1 で期待を直した f155_・f158_・tests/anchor.rs・tests/gitcheck.rs の 4 本）。
3. **本便の写し。** workspace の nextest 995 / 995（改訂 a の差分を main だけの上に当てた数は未測・改訂 a の前は 990 / 990）・clippy 0 警告・床 4 本 rc 0・rustfmt --check の差の塊は 7 file とも base と同じ数（adr 1・anchor 2・freeze 2・gitcheck 0・tests/anchor 3・tests/freeze_root 24・tests/gitcheck 0）。
4. **突然変異。** 写しの src だけを 1 通りずつ変え、verify の歯を撃った。**M1〜M16 は全部落ちる**（M13〜M16 は改訂 a）。

| 変異 | 落ちる歯 |
| --- | --- |
| M1 表に無い名でも根の履歴を形式で見逃す / M6 根の履歴の形式の免除を残す / M10 表に在る名にも形式を問わない照合を掛ける | (c) の 3 |
| M2 床の逆引きを外す | (c) の 4・f121_renamed_constitution_fails_the_floor_twice |
| M3 凍結の逆引きを外す | (c) の 4・f121_freeze_start_writes_nothing_on_any_finding |
| M4 浅い写しを照らせることにする / M7 版管理が無いときに根の行を出さない | (c) の 2 |
| M5 記録の前を照らせることにする / M8 始まりの凍結の根の告げを外す | (c) の 1 |
| M9 逆引きが行の名を取り違える | (c) の 6 |
| M11 照らせないを違反にする | (c) の 1・2 |
| M12 表に在る名の値の違いを見逃す | (c) の 5・f134_tsuzuri_name_picks_its_row |
| M13 名の印を見ない | (c) の 7・f155_・f158_ |
| M14 名の印の前後の空白を落とさない / M15 名が無いときを通す | (c) の 7 |
| M16 表に無い名を全部断る | (c) の 1〜4・7・f121_freeze_start_writes_nothing_on_any_finding |

### (f) 大きさ・verify と done の対応

1. **write-set 7 本**（どれも書き換えだけ）: src 4 本（adr.rs・anchor.rs・freeze.rs・gitcheck.rs）と歯の file 3 本（tests/freeze_root.rs・tests/anchor.rs・tests/gitcheck.rs）。
2. **余地（CapHeadroom）。** 各行 ceil(字数 / 120)・空行は 1。python と awk の 2 実装で一致。

| file（crates/folio/src/） | base の正規化行数（参考値） | 余地 | 模擬の後 | 便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| adr.rs | 1065 | 435 | 1090（+25） | 410 |
| anchor.rs | 1071 | 429 | 1096（+25） | 404 |
| freeze.rs | 514 | 986 | 538（+24） | 962 |
| gitcheck.rs | 403 | 1097 | 431（+28） | 1069 |

   main（便 162 の前）では adr.rs が 1049（余地 451）で、ほかは同じ。
3. **size は M。** src 4 本で +102（単体の歯を含む）。最小の余地は adr.rs の 410（M の 300 以上）。
4. **verify は 6 行**で、done の 6 つの塊と 1 対 1。
   1. `cargo nextest run -p folio --test freeze_root f164_` = (c) の 1〜5・7（6 本）。
   2. `cargo nextest run -p folio --bin folio f164_` = (c) の 6（1 本）。
   3. `cargo nextest run -p folio --test freeze_root` = 列の根の歯の全部（19 本）。
   4. `cargo nextest run -p folio --test anchor`（14 本）。
   5. `cargo nextest run -p folio --test gitcheck`（4 本）。
   6. `cargo clippy --workspace --all-targets -- -D warnings`。

   base では 1・2 が 0 件で終了コード 4、3〜5 は緑（14・14・4 本）、6 は 0 警告。本便の写しで 6 行とも 0（`root233-scripts/verify.log`）。

### (g) 門・受付・並行の便

1. **門は 0（書かない形・席の裁定で採った）。** 作業ツリー planner-d164 の一番上で、base の binary に write-set 7 本を渡すと 0（通す）。
   - **古くなる注の 5 か所。** 床の定数 FLOOR の注（floor_adr.rs の anchor_note と limits_note）の列の根の字と、その写し（design-intent/adr/schema.yaml の生成区間・凍結 anchor tests/fixtures/schema/adr-region.txt・tests/schema.rs の byte 数と要約値）が、便の後に実装より古い字で残る（ADR-29 の帰結の 4 が予告済み）。① 根の digest は表の行と一致する（表に無い名の列は落とす）② 浅い写しの項（表に無い名の根は照らせない が無い）③ 列の真偽は索引と digest と根の定数が受け持つ ④ 表に無い名の列の根は digest の全桁を出して凍結しない ⑤ 床が応じるのは列の根の digest の固定まで・床の実装は表の各行の憲法に結び付く。
   - **その後続の台帳 id は席が振る**（便 162 の着地の後の S の便）。字の当て方（`root233-scripts/apply-164-notes.py`・6 置き換え）と写しの組み直し（`notes-data-164.py`）は模擬済みで、生成区間は 27124 → 28081 byte、workspace の nextest 994 / 994・clippy 0（改訂 a の前の写し）。生成区間を書くので、印が古いあいだその便の門は 2。
2. **受付の順（前提）。** 一括 31（ADR-29・要件書 第 1.50 版の FR23）の発効と取り込みが先で、本便の受付はその後。FR23 の今の規範文（表に無い名は落とす）と実装が食い違う時間を作らない（P-18.1）。一括 31 は一括 30 の後に載せ替える（一括 31 の字の当て方は main と一括 30 の両方に当たる）。便 162 との前後は問わない（3）。
3. **write-set の重なり。**
   - 便 162（行 fi）: adr.rs が重なるが箇所は別（162 は check_approval と non_empty の近く、本便は root_digest の近くと単体の歯の末尾）。162 は本便の歯が読む fixture root-digest-drift の adr/schema.yaml も書き換える。本便の差分は main にも 162 の後にも当たり、どちらの上でも workspace の nextest が緑（162 の後 + 本便 995 / 995。main + 本便は改訂 a の前の差分で 990 / 990、改訂 a の差分では未測）。
   - 便 163（fj）・便 165（fl）・便 166（fm）・便 168（fo）・一括 30・一括 31: 重ならない（一括 30 の歯の直しは tests/check.rs・face_constitution.rs・face_srs.rs）。
4. **受付の先撃ち（precheck）。** 契約に起因する断りは 0（起草役の実測）。

### (h) 今の置き場の答えが変わらないこと（撤退条件 (2) の実測）

改訂 a の後の binary での 1〜3 の撃ち直しは未測（改訂 a の断りは表に無い名で名が無いか 未記入 のときだけで、1・2 の表に在る名と 3 の名を書いた置き場には当たらない見込み・(c) の 7 と既存の歯が縛る）。数は改訂 a の前の写しの実測。

1. **folio2 自身（表に在る名）。** 床 4 本・`folio build` の出力（34 file・diff -r）・凍結の 4 つの旗（--freeze-start・--freeze-anchor・--freeze-ids・--emit-amends）の標準出力と標準エラーと rc が、base と本便で 1 byte も違わない（`root233-scripts/floor.log`）。
2. **次の世代の置き場（表に在る名）。** design-intent と contracts を写しへ cp して撃った（その repo では何も書かず git も撃たない）。素の check・4 つの旗・schema --check・derive --check の出力が base と本便で一致した（`tsuzuri.log`）。
3. **受け入れの物差し（表に無い名・本便で変わる答え）。** 版管理の中の一時の置き場で init → 憲法の名と承認欄 → `--freeze-start` rc 0 → commit → 素の床 rc 0（合格）。続けて schema --check・inject --write / --check・derive --write / --check・build（6 file）も rc 0 で、その後の床も合格。深さ 1 の写しでは まだ分からない 2（`accept-sim.log`・手順は `accept-164.sh`）。folio2 の便も組み直しも無い。名を 未記入 のまま承認欄だけ埋めた置き場の `--freeze-start` は、base（表に無い の字）と本便（置き場の名でない の字）のどちらも rc 1 で断る（`probe-unfilled.log`）。

### (i) 要件との関係・運ばないもの・撤退条件

1. **要件との関係（正本は書き換えない）。** FR23 の規範文と確かめ方、FR24 の注 ⑦、受入基準 AC20 は一括 31 が二段の根に置き換える（持ち主の承認・行 D-17）。本便はその実装で、FR5 の まだ分からない の口（浅い写し・版管理の外・記録の前）を足す。
2. **運ばないもの・残る穴。**
   - 表に無い名の置き場で、新しい版管理から根を作り直して持ち帰る手は床が止めない（ADR-29 決定 (3)・共有の版管理の保護と取り込みの審査へ移した）。取り込まれたと分かったら ADR-29 撤退条件 (3)。
   - 表に無い名の置き場の床は全履歴を要る（浅い写しは まだ分からない）。
   - 注の字（(g) の 1 の 5 か所）は借り（P-5.6）として残り、席が振る後続の便が運ぶ。
   - 名は凍結の木に入らないので、凍結の後に表に無い名どうしで名を変えても床は落とさない（表に在る名へ変えれば表で照らし、表に在る根を別の名で持てば逆引きで落ちる）。
3. **撤退条件。**
   - (1) (e) の 1 の 5 本のほかに既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。
   - (2) 着地の後の main で、folio2 自身の床 4 本の結果・`folio build` の出力・次の世代の置き場の写しの床の結果のどれかが着地の直前と 1 byte でも違ったら、止めて席へ返す（ADR-29 撤退条件 (4)）。
   - (3) 受付の時点の main で、(b) が使う check_root（anchor.rs と freeze.rs）・check_git・ROOT_DIGESTS・adr.rs の unfilled・歯の口（Work・rename・edit・skeleton_approval）が base と違えば、数え直してから運ぶ（手順は行 D-13 のとおり控え `.local/share/folio2/handoff-2026-09-27/root233-draft.md` の便 164 の節）。

## 2. 範囲

- 入れる: §1 (b) の 1〜4、(c) の歯 6 本と単体の歯 1 本と定数 1 つと口 4 つ、(e) の 1 の期待の直し。
- 入れない: floor_adr.rs（表と FLOOR の注）・床の定数の写しの生成区間・init の雛形・承認欄の確かめ・命令の旗・設計文書の正本・新しい fixture と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| owner | 表の逆引き | adr.rs の root_owner（ROOT_DIGESTS を要約値で引く） |
| floor | 床の二段目 | anchor.rs の check_root（表に無い名は逆引きと版管理で照らせるか）と gitcheck.rs（浅い写しの印・根が記録済みか・根の履歴は形式を問わず比べる） |
| start | 凍結の二段目 | freeze.rs の check_root（表に無い名は、名が無いか 未記入 のときと逆引きで当たるときだけ断る）と始まりの凍結の告げ |
| teeth | 歯 | tests/freeze_root.rs の f164_ 6 本と口・tests/anchor.rs と tests/gitcheck.rs の期待の直し・adr.rs の単体の歯 |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate と新しい dir は無い。前提の着地は一括 31（ADR-29 の発効と FR23 の規範文）。
- 起草の記録: `.local/share/folio2/handoff-2026-09-27/root233-draft.md` と root233-scripts/（c164.patch = 差分の全部・r164-teeth.patch = 歯だけ・apply-164*.py = 当て方・accept-164.sh = 受け入れの物差し・mut-164.py = 変異）。
- 着地の後に席が見ること: 本流の target/debug/folio を組み直す。台帳 f2-648.233 を閉じ、(g) の 1 の注の字の後続の便を起こす（台帳 id は席が振る）。次の世代の置き場の表の行は ADR-29 決定 (4) のとおり ADR-21 の合流の後に外す（本便の外）。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "fk"
title = "台帳 f2-648.233（ADR-29）: 列の根の表に名の無い置き場は、始まりの凍結が断り床が落とすので、folio2 の便で表に行を足して組み直すまで合格に届かない。列の根を二段で照らす: 表に在る名は今のまま表の行と比べ、表に無い名は、根の digest が表のどれかの行と同じなら床も凍結も違反（adr.rs の root_owner で逆引き・改名の逃げ道）、違えば凍結を断らずに書いて根の digest を告げ（名が無いか 未記入 のままなら承認欄の 未記入 と同じく印を空と見て断る）、床は根 anchors/constitution-v1.0.yaml を版管理の記録で照らす（gitcheck.rs が根だけは形式の違う記録も免除せず比べ、違えば違反。浅い写し・版管理の外・HEAD に記録の無いときは まだ分からない）。表・表に在る名の答え・床の定数の注とその写しは変えず、folio2 と次の世代の置き場の写しの床も変わらない。歯は tests/freeze_root.rs の f164_ 6 本と adr.rs の単体の歯 1 本・既存の歯 5 本の期待を ADR-29 に合わせる。書かない形で門は 0。base = main 8472b5c + 便 162 の模擬・一括 31（ADR-29・FR23 第 1.50 版）の発効と取り込みの後に受け付け、受付の時点の main で数え直す"
req = ["FR23", "FR5"]
section = "1"
write-set = ["crates/folio/src/adr.rs", "crates/folio/src/anchor.rs", "crates/folio/src/freeze.rs", "crates/folio/src/gitcheck.rs", "crates/folio/tests/freeze_root.rs", "crates/folio/tests/anchor.rs", "crates/folio/tests/gitcheck.rs"]
verify = ["cargo nextest run -p folio --test freeze_root f164_", "cargo nextest run -p folio --bin folio f164_", "cargo nextest run -p folio --test freeze_root", "cargo nextest run -p folio --test anchor", "cargo nextest run -p folio --test gitcheck", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "M"
done = "tests/freeze_root.rs の f164_ の 6 本（表に無い名の骨格は名と承認欄を埋めると --freeze-start が 0 で 3 file を書き告げに根の digest の全桁が在り、commit の前の床は rc 1 で列の根の行は HEAD に記録されていない の まだ分からない ちょうど 1 行、commit の後は合格〔違反 0・まだ分からない 0〕/ 凍結して commit した置き場の深さ 1 の写しと版管理の外の複製は rc 2・違反 0・列の根の行ちょうど 1 行 / 表に無い名の根を固定の欄を外した形で最初に commit し戻すと違反ちょうど 1 件〔表に無い名の列の根で、版管理の履歴の記録と中身が違う〕、folio2 の床の土台の同じ操作は rc 0 / folio2 の床の土台を表に無い名にすると床の anchor の違反は表の folio2-constitution の行を名指す 1 行、anchors/ の無い置き場の --freeze-start は同じく 1 行で rc 1 で anchors/ を作らない / fixture root-digest-drift の表に無い名のままは rc 2・違反 0・列の根の行 0、folio2 の名に書き換えると表の行と違うで落ちる / 承認欄を埋めた骨格で名が 未記入・前に全角の空白の付いた 未記入・meta.id の行が無い の 3 通りとも --freeze-start は rc 1 で違反は置き場の名でない の 1 行だけで anchors/ を作らず、名を書けば rc 0）が緑、adr.rs の単体の歯 f164_root_owner_finds_the_row_by_digest（表の各行の digest がその名を引き、64 桁の 0・空の字・名の字は何も引かない）が緑、tests/freeze_root.rs・tests/anchor.rs・tests/gitcheck.rs の歯の全部が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と file 数も byte も変わらない"
<!-- contracts:end -->
