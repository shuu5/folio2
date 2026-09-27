# 設計: 便 171 — 天井の束に判断の記録の面を写さない（判断の記録 ADR-30 決定 (4)(7)・行 fr・S）

- 要件: FR17（天井の材料の束を観点ごとに組む）。規範文・受入基準の字は変えない（束は今も「生成した面の写し」を持ち、判断の記録の面がその写しから外れるだけ）。
- 判断: ADR-30 決定 (4)（天井は判断の記録の題と状態だけを読む・面はそのまま生成する）と決定 (7) の末文（面を束から外す口は後続の便）。
- 条: P-5.1（面の名の形は床の定数の表で持つ）・P-10.1 / P-10.2（束の凍結 anchor は独立の script と歯の定数が持つ＝両方を同じ規則へ直す）。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `fr` が指す §1 だけ。
- 門: **対象外・0**。作業ツリー planner-d171 の一番上で base と本便の写しの binary に write-set を渡すと、どちらも「通す（設計文書の正本を書き換えない便）」。生成区間に面の名の形の写しは無い（天井の正本の schema.bundle は contents の 5 語だけ）ので、`folio schema --write` の出力は write-set に入らない。
- 前の便: **base = main a8866a1（ADR-30・天井の正本 第 0.18 版の着地の後）。数は base の写しの実測（参考値・行 D-13）**で、受付の時点の main が違えば数え直す。受付の順は便 169 → 170 → 171（(g)）。

## 1. 設計

### (a) いま起きていること（参考値・base a8866a1）

1. **束は面を丸ごと写す。** 束を組む口（`folio ceiling --write`・ceiling_src.rs の build_counted）は、観点が読む文書ごとに、正本の写しを読む節まで絞って sources/ に置き、面（人が読むページ）を床の定数 FACE_NAMES の名の形で faces/ へ byte のまま写す（copy_faces）。判断の記録の形は adr-〈数〉.html。
2. **読む欄と写す面が食い違う。** 天井の正本 第 0.18 版は 4 観点とも判断の記録を `[title, status]` で読み、sources/adr/ の写しは題と状態と骨格だけになった。一方 faces/ には判断の記録の面 28 本（決定・前提・退けた案・来歴が全部載る）が観点ごとに残る。
3. **束の大きさ（size-171.sh・digest.txt を除く byte）。** 4 観点の合計 10,212,350。うち判断の記録の面は観点ごとに 1,318,735（28 本）＝合計の 51.7%。表は (h)。
4. **読み手の全数（git grep）。**
   - FACE_NAMES を読むのは copy_faces と単体の歯 2 本（ceiling_src.rs の bundle_face_name_forms_follow_the_site_outputs・bundle.rs の f102_）だけ。
   - 束の faces/ を読むのは `--check` の測り直し（findings.rs の measure・規則 3「束が古い」）と印の欄 faces の要約値（stamp.rs の faces_digest）の 2 つ。門と面の名札は faces/ を読まない。`--refute` の束は faces を持たない（sources.txt = 親の digest.txt の字）。
   - 束の要約値の写しは凍結 anchor に在る（(b) の 2 の 3 か所）。
5. **base の歯。** workspace の nextest 1003 / 1003・clippy 0 警告・床 4 本 rc 0・`folio build --write` 35 file・2,162,994 byte。`f171_` と行 id `fr` は 0 件。

### (b) 直す先

1. **ceiling_src.rs の FACE_NAMES の adr の行を `None` にする。**
   - 注の `None` の意味を「束に写す面は無い（面を持たない文書と、面を束に写さない判断の記録・ADR-30 決定 (4)(7)）」にする。FaceName::Affix の注の例から adr を外す。
   - 単体の歯 bundle_face_name_forms_follow_the_site_outputs は adr を `None` の一覧へ移し、Affix の負の例を note-.html にする。
   - copy_faces と build_counted の本体は変えない（`None` の文書は今も面を写さずに通る）。
2. **凍結 anchor の追随。** 束の中身が変わるので、要約値は必ず変わる。
   - bundle-anchor.py の FACES から adr を外し、bundle-anchor.txt をその出力で書き直す。4 観点とも file 2 本・244 byte 減る。落とした節の数・正本に無い節の数は同じ。
   - tests/bundle.rs の期待 4 対（FIDELITY_FILES 13 → 11・REALITY_FILES 11 → 9・連結の byte 数と要約値）を同じ値にする。実の正本の歯 bundle_on_the_real_source_builds_four_bundles の「adr の面の数 = 判断の記録の数」を「0」にする。
   - 所見 file の fixture 10 本の record.bundle と tests/findings.rs の REALITY_FAIL を新しい要約値へ置き換える（4 対）。反証の束の REFUTE_SOURCES を新しい fidelity の要約値へ、REFUTE_DIGEST を f4374dcb… へ直す（歯の 5 つの定数の連結の sha256 を folio を呼ばずに測った・同じ測り方で base の ec8643e3… を再現）。連結の byte 数 2,338 は同じ。
3. **変えないもの。** 面の生成（`folio build` / `folio face` の出力は base と byte 一致）・ほかの文書の面の写し・sources/ の絞り・束の要約値の規則・`--check` / `--stamp` / `--gate` / `--refute` の code・凍結の土台の faces/（adr-1.html・adr-2.html は残す＝写さないことを歯が見る）・設計文書の正本と生成区間。

### (c) 歯（関数名 f171_・`crates/folio/tests/bundle.rs`）

1. **f171_the_fixture_bundle_leaves_out_the_adr_faces。** 凍結の土台（配信先に adr-1.html・adr-2.html が在る）から `--write` で組む。4 観点とも:
   - faces/ に adr- で始まる file が無い。
   - faces/ の一覧が「配信先の面のうち、その観点の reads.yaml が読むと宣言した文書の面（index・constitution・srs・note-〈id〉）」と一致し、byte も配信先と同じ。
   - sources/adr/ の ADR-1.yaml は状態の行 1 つ、ADR-2.yaml は題と状態の行 2 つを、正本の byte のまま持つ。
   - 配信先の adr-*.html は消えない。
2. **f171_the_real_bundle_reads_the_adr_title_and_status_without_its_faces。** design-intent の写しを `folio build` してから `--write` で組む。
   - 配信先の adr-*.html の数が、正本の ADR-*.yaml の数と同じ（面は今のまま生成する・決定 (4)）。
   - 4 観点とも reads.yaml に `- {doc: adr, fields: [title, status]}` の行が在り、faces/ は 1 と同じ規則で、sources/adr/ の ADR-*.yaml はどれも題と状態の行 2 つを正本の byte のまま持つ。
3. 歯の側の面の名の規則（copied_face）は床の定数を読まず、字で書く（P-10.2）。fixture は足さない。
4. **RED。** 歯だけを base に当てると、2 本とも「束に判断の記録の面が在る」で落ちる（red.log）。ほかの 19 本は緑。

### (d) 採らなかった形

1. **天井の正本の documents か reads に「面を写すか」の欄を足す。** 設計文書の正本と生成区間（schema の節）が変わり、L になる。決定 (4) が決めたのは判断の記録だけで、床の定数の 1 行で足りる。
2. **題と状態だけに刈った判断の記録の面を束に写す。** 面の生成器を 2 つ持つことになる（P-2.1）。
3. **copy_faces の中で adr を名指しして飛ばす。** 規則を表の外の code に置く（P-5.1）。表の `None` なら単体の歯 f102_（表と文書の id の集合が同じ）も変わらず通る。

### (e) 既存の歯のうち落ちるもの・突然変異

1. **実装だけ（FACE_NAMES の 1 行だけ）を base に当てると、既存の歯 37 本が落ちる**（1003 本のうち・impl-only-nextest.log）。どれも (b) の 1・2 の追随の先。
   - 単体の歯 1 本: adr の形を unwrap する。
   - tests/bundle.rs の 4 本: 凍結 anchor の file の一覧と要約値（bundle_write_matches_the_frozen_anchor・f98_the_cut_bundle_matches_the_rebuilt_anchor・bundle_reads_the_lists_from_the_floor_not_the_source_file）と、実の正本の adr の面の数（bundle_on_the_real_source_builds_four_bundles）。
   - tests/findings.rs の 32 本: fixture の record.bundle が束の要約値と合わず「要約値が束と合わない」で まだ分からない になるか、反証の束の要約値が anchor と違う。
2. **本便を当てた写し。** workspace の nextest 1005 / 1005（1003 + 2）・clippy 0 警告・床 4 本 rc 0・`folio build` の出力は base と byte 一致・`--test bundle` 21 / 21・`--test findings` 39 / 39。rustfmt --check の差の塊は base と同じ数（tests/bundle.rs 7・tests/findings.rs 0・ceiling_src.rs 1・新しい塊は 0）。
3. **突然変異。** 写しの ceiling_src.rs を 1 通りずつ変えて `--test bundle` と単体の歯を撃った（mut-171.py・本文は mut-bodies.log）。5 通りとも f171_ の 2 本が落ちる。

| 変異 | f171_ | ほかに落ちる歯 |
| --- | --- | --- |
| M1 判断の記録の面を写す（base の形） | 2 / 2 | 5（凍結 anchor 3・実の正本・単体） |
| M2 設計ノートの面も写さない | 2 / 2 | 5 |
| M3 入口の面を写さない | 2 / 2 | 5 |
| M4 面を写さない文書は正本の写しも写さない | 2 / 2 | 7 |
| M5 名の形を緩める（.html は全部写す） | 2 / 2 | 6 |

### (f) 大きさ・verify と done の対応

1. **write-set 15 本・印なし（書き換えるだけ）。** src 1 本（ceiling_src.rs）・tests 2 本（bundle.rs・findings.rs）・独立の anchor 2 本（bundle-anchor.py・bundle-anchor.txt）・所見 file の fixture 10 本（tests/fixtures/ceiling/findings/ の fabricated-evidence・fail-no-findings・missing-field・pass-coherence・pass-fidelity・pass-readability・pass-reality・stop-refuted・stop-unrefuted・stop-upheld）。新しい file と dir は無い。
2. **余地（CapHeadroom）。** ceiling_src.rs 660 → 660（余地 840・各行 ceil(字数 / 120)・空行は 1・python と awk の 2 実装で一致）。src の外の参考値は tests/bundle.rs 979 → 1081 行。
3. **size は S。** src の変更は表の 1 行と注と単体の歯だけ。
4. **verify は 5 行**で、done の 5 つの塊と 1 対 1。
   1. `--test bundle f171_` = (c) の 1・2。
   2. `--test bundle` = 凍結 anchor の歯（期待 4 対・独立の script との byte 一致）と実の正本の歯を含む全部。
   3. `--test findings` = 所見 file の fixture と反証の束の凍結 anchor の歯の全部。
   4. `--bin folio ceiling_src_tests` = 単体の歯 2 本（面の名の形・束の要約値の順）。
   5. clippy。

   base では 1 が 0 件で終了コード 4、2〜4 は緑、5 は 0 警告。

### (g) 門・受付・並行の便

1. 門は対象外で 0（冒頭・gate.log）。受付の先撃ち（precheck）で契約に起因する断りは 0。
2. **便 169（行 fp）と tests/findings.rs が重なる**（169 は本文不変の verify の scope）。169 → 171 の順で運び、169 の着地で本文が変われば置き換えの当て先を数え直す。169 が書き換える stamp-*.yaml は束の要約値を持たない（0 の字）。
3. **便 170（行 fq）とは file が重ならない。** 170 が変える判断の記録の面は、本便の後は束に入らない。170 が縮める adr/schema.yaml は本便の歯が数えない（ADR-*.yaml だけ）。

### (h) 束の大きさの変化（参考値・行 D-13・実の正本 a8866a1・digest.txt を除く byte）

| 観点 | base 合計 | 本便 合計 | 差 | うち faces（base → 本便） | faces の本数 |
| --- | --- | --- | --- | --- | --- |
| 忠実さ | 2,540,605 | 1,221,870 | −1,318,735 | 2,066,137 → 747,402 | 32 → 4 |
| 読みやすさ | 2,577,654 | 1,258,919 | −1,318,735 | 2,091,468 → 772,733 | 33 → 5 |
| 文書どうしの整合 | 2,609,889 | 1,291,154 | −1,318,735 | 2,091,468 → 772,733 | 33 → 5 |
| 実態との整合 | 2,484,202 | 1,165,467 | −1,318,735 | 2,066,137 → 747,402 | 32 → 4 |
| 計 | 10,212,350 | 4,937,410 | −5,274,940（−51.7%） | | file 296 → 184 |

sources/ は 4 観点とも byte 一致。束の差は判断の記録の面 112 本（28 本 × 4）と digest.txt 4 本だけ（diff -r）。

### (i) 運ばないもの・撤退条件

1. **着地の前に組んだ束は `--check` で規則 3（束が古い）に当たる。** 本便の binary で base の束を `--check` すると、4 観点とも「束が古い（現在の正本から組んだ要約値と違う）」が出た（本便の binary で組んだ束には出ない）。次の周は `--write` から組み直すので手順は変わらない。印の欄 faces の要約値も次の印から値が変わる（門は読まない）。
2. **天井の正本の問いの文は直さない。** 「判断の記録の本文は、面に載っていても所見に挙げない」は、束から判断の記録の面が消えた後も偽ではない。刈るかは天井の正本の次の版で席が決める。
3. **撤退条件。**
   - (1) (b) の 2 に挙げた以外の既存の歯が 1 本でも落ちたら、歯も fixture も直さずに止めて席へ返す。
   - (2) 着地の後の main で、folio2 自身の床 4 本の結果か `folio build` の出力が着地の直前と 1 byte でも違ったら止めて席へ返す。
   - (3) 受付の時点の main で、束の要約値の写しの所（(a) の 4 の 3 つ目）が base と違えば、下の手順で測り直してから運ぶ。

数え直しの手順（行 D-13）: 記録は `.local/share/folio2/handoff-2026-09-27/d171-draft.md`、script は同じ dir の d171-scripts（repo の外）。写し = apply-171.py（`--teeth-only` で歯だけ）・teeth-171.rs → c171.patch・r171-teeth.patch、検査 = base・run・red・impl-only・mut・gate・size（各 -171）・refute-anchor-171.py・lines-171.py / .awk。

## 2. 範囲・依存

- 入れる: §1 (b) の表の 1 行と注と単体の歯、凍結 anchor と要約値の写しの追随、(c) の歯 2 本と tests/bundle.rs の頭の注。検査は §1 (c)(e)(f) と `.vessel.toml` の common-verify。
- 入れない: 面の生成・天井の正本と生成区間・`--check` / `--stamp` / `--gate` / `--refute` の code・ほかの文書の面・台帳への記帳。
- 外部 crate と新しい dir は無い。前提の着地（ADR-30・天井の正本 第 0.18 版）は base に在る。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "fr"
title = "判断の記録 ADR-30 決定 (4)(7): 天井の束（folio ceiling --write）は、読む欄が判断の記録の題と状態だけになった後も、判断の記録の面 adr-*.html を観点ごとに丸ごと写す（実の正本で観点ごとに 28 本・1,318,735 byte・束の約半分・参考値）。ceiling_src.rs の面の名の形の表 FACE_NAMES の adr の行を None にして、束に判断の記録の面を写さない。面の生成・ほかの文書の面の写し・sources の絞り・束の要約値の規則・check / stamp / gate / refute の code は変えない。束の中身が変わるので、凍結 anchor（独立の script bundle-anchor.py とその出力・tests/bundle.rs の期待 4 対と実の正本の歯・所見 file の fixture 10 本の record.bundle・tests/findings.rs の REALITY_FAIL と反証の束の REFUTE_SOURCES / REFUTE_DIGEST）を同じ規則へ直す。歯 f171_ 2 本は凍結の土台と実の正本の写しで、束の faces/ に adr-*.html が無く、ほかの面は読む文書のとおり byte のまま在り、判断の記録の題と状態は sources/ に正本の byte のまま在ることを縛る。門の対象外。base = main a8866a1・受付は便 169 と 170 の後で、受付の時点の main で数え直す"
req = ["FR17"]
section = "1"
write-set = ["crates/folio/src/ceiling_src.rs", "crates/folio/tests/bundle.rs", "crates/folio/tests/findings.rs", "tests/fixtures/ceiling/bundle-anchor.py", "tests/fixtures/ceiling/bundle-anchor.txt", "tests/fixtures/ceiling/findings/fabricated-evidence.yaml", "tests/fixtures/ceiling/findings/fail-no-findings.yaml", "tests/fixtures/ceiling/findings/missing-field.yaml", "tests/fixtures/ceiling/findings/pass-coherence.yaml", "tests/fixtures/ceiling/findings/pass-fidelity.yaml", "tests/fixtures/ceiling/findings/pass-readability.yaml", "tests/fixtures/ceiling/findings/pass-reality.yaml", "tests/fixtures/ceiling/findings/stop-refuted.yaml", "tests/fixtures/ceiling/findings/stop-unrefuted.yaml", "tests/fixtures/ceiling/findings/stop-upheld.yaml"]
verify = ["cargo nextest run -p folio --test bundle f171_", "cargo nextest run -p folio --test bundle", "cargo nextest run -p folio --test findings", "cargo nextest run -p folio --bin folio ceiling_src_tests", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "tests/bundle.rs の f171_ の 2 本（凍結の土台と design-intent の写しから組んだ束の 4 観点とも、faces/ に adr- で始まる file が無く、faces/ の一覧が配信先の面のうち観点の reads.yaml が読む文書の面〔index・constitution・srs・note-〈id〉〕と名も byte も同じで、sources/adr/ の判断の記録は題と状態の行を正本の byte のまま持ち、配信先の adr-*.html は消えず正本の判断の記録と同じ数）が緑、tests/bundle.rs の歯の全部（凍結 anchor の期待 4 対と独立の script bundle-anchor.py の出力との byte 一致・実の正本の歯を含む）が緑、tests/findings.rs の歯の全部（所見 file の fixture と反証の束の凍結 anchor を含む）が緑、単体の歯 ceiling_src_tests の 2 本が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check と folio derive --dir design-intent --out ../contracts --check が 0 を返し、folio build の出力は着地の直前の main と file 数も byte も変わらない"
<!-- contracts:end -->
