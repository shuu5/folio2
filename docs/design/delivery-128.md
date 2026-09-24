# 設計: 便 128 — 憲法の meta・前文・条・規範文・mechanism と規則の表の行の未知の欄を床で落とす（天井の 29 周目 実態 F-1・台帳 f2-648.176・憲法 N-3 の機構の注）

- 要件: FR5（構造の床を実行し 3 値で返す・要件書 第 1.37 版）。FR9 の注が「正本の形（重複キー・未知の欄・欄の非空）は構造の床（FR5）で数える」と書く床がこの要件である。規範文はどれも変えない。FR19（生成区間への写し）は req に入れない。本便は生成区間を 1 byte も変えないからである（(b) の最後の段）。
- 条: N-3.1（規則の例外機構〔無効化の旗・「今回だけ」の口〕を足す変更を拒む＝行や条へ旗の欄を足す口を塞ぐ）/ P-4.1（実行できなかった検査を異常なしとして扱わない＝未知の欄を黙って読み捨てない）/ P-5.1・P-6.3・P-6.4（閉じた一覧は型付きデータに 1 つだけ置き、手書きの写しを持たない）/ P-5.6（実装の型付きの定数が正本なら写しを生成区間へ導出する）。
- 出所: 天井の 29 周目の実態の所見 **F-1**（重さ 止める・反証で支持・所見は持ち主の home の下の `.local/share/folio2/ceiling/2026-09-24-round29/` の実態の findings.yaml、反証の理由は同じ dir の refute-notes の reality-F-1.md）。憲法 N-3 の機構の注（kind build-check・live now・polarity fail-closed）は「正本と rules の全節（top_level・meta・前文・条・規範文・mechanism・rules 行）で未知の欄を schema 検査が落とす（床は folio check）」と約束するが、床は最上位の節しか数えない。台帳 **f2-648.176**（memo・2026-09-24）の観測「規則の表の開発規律行に stage を書いても床は黙って落とす」も同じ根である。判断の記録 ADR-11 の注 (ア)（2026-09-21）も、規則の表の行の欄の定数を床が読んでいないことを記録している。規則の表の開発規律行 D-11 は、この行と契約表の行の title が出所（29 周目の実態 F-1・台帳 f2-648.176・判断の記録 ADR-11 決定 (3)）を名指すことで満たす。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `dz` が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は手書きで 7 本。**新しい file は 1 本で、先頭に `+` を付けて宣言する**（歯の file 1・既に在る dir `crates/folio/tests/` に置く）。書き換える 6 本は印なし。**縮む file も消す file も無く、新しい dir も作らない。** 歯の runner `crates/folio/tests/floor_cases.rs` は本文を変えないが、verify が `--test floor_cases` で名指すので write-set に入れる。
- 門: 本便は設計文書の正本（`design-intent/` の下）を 1 本も書き換えないので、天井の門の対象外である。起草役が write-set 7 本をそのまま門に渡した実測は **0（通す・断りの字 = 設計文書の正本を書き換えない便）**（2026-09-24・本体の作業ツリーの binary・§1 (h) の 7）。印は 29 周目の不合格のものだが、対象外の便なので門の判定は印に依らない（規則の表の開発規律行 D-12 と、2026-09-22 の席の前例を当てる場面は無い）。
- 前の便: 前提の便は無い。**base = main ee714d7（便 125 の着地・骨格の命令 folio init）。この契約の数はすべて base ee714d7 の実測（参考値）である**（規則の表の行 D-13）。起草は 3b770a1 で始め、改訂 b で base を ee714d7 に取り直して数え直した（(a) の base の実測・模擬の数え・余地・門・受付の先撃ち）。数はどれも変わらなかった。3b770a1 から ee714d7 までの差分 8 file（`crates/folio/src/init.rs`・`crates/folio/src/hello.rs`・`crates/folio/src/main.rs`・歯の file 4 本・凍結 anchor 1 本）は本便の write-set 7 本と 1 本も重ならない。
- 改訂: 改訂 b（2026-09-24・席の連絡）= base を 3b770a1 から ee714d7 に取り直した。直したのは base の名指し 3 か所だけで、数値・write-set・歯の本数・`done`・`verify` は変えていない。
- 並行の便との重なり: 起草の時点で契約が main に在り未着地の便のうち、`crates/folio/src/check.rs`・`crates/folio/build.rs`・`tests/floor_cases.yaml` を触るものは無い（受付の先撃ちが write-set の重なりを見る・§0 の 門の次の段）。便 125 の骨格（folio init）が書く憲法と規則の表は、本便の閉じた一覧の内に収まる（(a) の 5）。

## 1. 設計

### (a) いま起きていること（実測・base main ee714d7）

1. **床が未知の欄を数えるのは最上位の節だけである。** `crates/folio/src/check.rs` の check_constitution は、最上位の節を置き場の憲法の schema.top_level で閉じ（unknown_sections・種別 未知の節）、前文・条・規範文の必須の欄の非空と、条の値域の欄の値を数える。meta・前文・条・規範文・mechanism の中の欄の名は数えない。check_rules は最上位の節を床の定数 RULES_TOP_LEVEL で閉じ、行の id・article・what の非空と refs だけを数える。行の欄の閉じた一覧の定数（`crates/folio/src/rules.rs` の閾値行と開発規律行の required と optional の 4 本）を読むのは床の木（`folio schema` の導出）と歯だけで、床は読まない。
2. **だから未知の欄は黙って通る。** 起草役が design-intent の写し（器の導出 file の写しを親の contracts/ に置き、git の 1 commit にした形）に欄を 1 つずつ足して `folio check` を撃った（script は (h) の 1）。

| 足した欄 | 終了コード | 床の出力 |
| --- | --- | --- |
| なし（元の写し） | 0 | 合格（違反 0・まだ分からない 0） |
| meta に bogus_meta | 0 | 合格（元の写しと同じ） |
| 条 N-3 に bogus_a | 0 | 合格 |
| 条 N-3 の mechanism に bogus_m | 0 | 合格 |
| 規範文 N-3.1 に bogus_s | 0 | 合格 |
| 規則の表の行 R-2 に bogus_r | 0 | 合格 |
| 開発規律行 D-5 に disabled: true（例外の旗の形） | 0 | 合格 |
| 開発規律行 D-14 に stage: post（台帳 f2-648.176 の形） | 0 | 合格 |
| 前文に bogus_p | 1 | 改憲の違反（種別 N-4）1 件だけ。未知の欄は数えない |
| 前文の mechanism に bogus_pm | 1 | 改憲の違反 1 件だけ |
| 憲法の schema.meta.optional に bogus_meta を足す | 1 | 改憲の違反 1 件だけ |

   前文は改訂の差分の範囲（amendment_scope の precedence）が節ごと比べるので、欄を足すと改憲の違反が立つ。条・規範文・mechanism は、差分が比べる条の欄（id・title・statements・tier・binds）に足した欄が入らないので、欄を足しても立たない（規範文の行に足した欄も入らない・実測）。
3. **閉じた一覧はもう在る。** 憲法の正本の schema 節は、meta・precedence・article・mechanism・statement の 5 つの部位ごとに required と optional の一覧を宣言している（statement は required だけで optional の欄を持たない）。判断の記録 ADR-11 の決定 (3) の最後の文は「(ア) と (イ) の両方が当たる憲法自身の欄の決まりの節は、A-2 の門が在るので (ア)（file が正本）とする」と決めた。(ア) は、実装は実行時に読むか組み立て時に導出し、手書きの写しを持たないとする。規則の表の行の一覧は、決定 (3)(イ) と (4)② のとおり実装の型付きの定数が正本で、写しは既に規則の表の生成区間に在る（生成区間の threshold_row と discipline_row の required と optional・便 53 から）。
4. **実のデータは宣言した一覧の内に収まっている。** 起草役が実の design-intent を数えた（script は (h) の 2）。宣言した欄はどの部位でも 1 回以上使われていて、宣言の外の欄は 0 である。

| 部位 | 行の数（参考値） | 使われている欄 |
| --- | --- | --- |
| meta | 1 | required の 10 と optional の 2（changes_from_v0_1・changes_from_v0_2） |
| 前文と前文の mechanism | 1 | required の 5・mechanism は kind・live・note |
| 条 | 27 | required の 8・optional の relations・retreat・amended_by・supersedes_v1・note |
| 条の mechanism | 27 | kind・live・note・stage・polarity |
| 規範文 | 67 | id・pattern・strength・text |
| 閾値行 | 17 | required の 9・optional の basis・projection・same_failure・population・note・refs |
| 開発規律行 | 14 | required の 7・optional の note・refs |

5. **道具の fixture と骨格も収まっている。** folio2 の憲法の一覧を当てて、`tests/fixtures/` の下の憲法か規則の表を持つ置き場 25 本（schema 節に 5 部位の一覧を持たない 23 本〔4 file 形の fixture と天井の束の材料〕・凍結の土台・規則の表だけを持つ check/missing-file）と、便 125 の骨格（ee714d7 の binary の `folio init` が書いた置き場）を数えた。宣言の外の欄はどれも 0 である（script は (h) の 2）。その 23 本の憲法の schema 節は最上位の節と値域だけを持ち、5 部位の一覧を持たない。床の凍結の場合（`tests/floor_cases.yaml`）が憲法と規則の表へ足す欄（add の変異）は amended_by・statements の行・条 P-20 の欄で、どれも一覧の内である。

### (b) 直す先 — 閉じた一覧で未知の欄を落とす

**憲法の 5 部位の一覧は、組み立て時に憲法の正本から導出する。** `crates/folio/build.rs` に新しい純粋な関数 constitution_fields を足す。憲法の正本の字を受け、schema の meta・precedence・article・mechanism・statement の 5 部位（この 5 つの名だけは導出の側が書く）について、required と optional を file の順に繋いだ列を返す。出力は、部位の名とその列の対を 5 つ持つ定数 1 つの Rust の source で、main が値域の導出（constitution_enums）の source の後ろに繋いで、同じ OUT_DIR の file に書く。`crates/folio/src/constitution_enums.rs` はその file を今のまま取り込むので、取り込みの行は変わらない。optional が無い部位（statement）は空の列とする。一覧を狭める側に倒れるので黙る口にはならない。次のどれかなら Err にして、組み立てを失敗させる（値域の導出と同じ形・黙って空の一覧にしない）。

- 部位が表でない。
- required が字の一覧でない。
- optional が在って字の一覧でない。
- 同じ部位の中に同じ名が 2 度在る。

Err の理由の文には部位の名を入れる。憲法の字は変えない。憲法の一覧を変える改訂（部位に欄を足す・外す）は改憲の手続き（A-2・N-4）を通り、組み立て直せば床の一覧も同じ字で動く。手書きの写しは置かない（P-6.4）。

**規則の表の行の一覧は、今の型付きの定数を床が読む。** 閾値行は `crates/folio/src/rules.rs` の閾値行の required と optional を繋いだ列、開発規律行は開発規律行の required と optional を繋いだ列で閉じる。file の生成区間の threshold_row と discipline_row は床の定数の写しとして読まない。file の側で一覧に欄を足して通す口を塞ぐためである（N-3.1・最上位の節を RULES_TOP_LEVEL で閉じた便 51 と同じ向き）。

**数える段。** `crates/folio/src/check.rs` に新しい非公開の関数 unknown_fields を 1 つ足す（file 名・場所の字・欄の表・閉じた一覧を受け、表の鍵のうち一覧に無いものを 1 つにつき違反 1 件）。種別は要件書の項の床（check_srs_item）と同じ 未知の欄 で、字も同じ形「file: 場所 の未知の欄「鍵」」にする。呼ぶ所は次のとおりである。表でない holder は数えない。その形の誤りは読めない・非空の検査が別に拾う。

| holder | 閉じた一覧 | 場所の字（違反の行は `[未知の欄] ` の後にこの行の字が続く） |
| --- | --- | --- |
| 憲法の meta | 導出した meta の列 | constitution.yaml: meta の未知の欄「鍵」 |
| 憲法の前文 | 導出した precedence の列 | constitution.yaml: 前文（precedence） の未知の欄「鍵」（非空の検査の場所の字と同じ） |
| 前文の mechanism | 導出した mechanism の列 | constitution.yaml: 前文（precedence）の mechanism の未知の欄「鍵」 |
| 条 X | 導出した article の列 | constitution.yaml: 条 X の未知の欄「鍵」 |
| 条 X の mechanism | 導出した mechanism の列 | constitution.yaml: 条 X の mechanism の未知の欄「鍵」 |
| 条 X の規範文 Y | 導出した statement の列 | constitution.yaml: 条 X の規範文 Y の未知の欄「鍵」 |
| 閾値行 R-n | 閾値行の列 | rules.yaml: 行 R-n の未知の欄「鍵」 |
| 開発規律行 D-n | 開発規律行の列 | rules.yaml: 行 D-n の未知の欄「鍵」 |

- 一覧は holder ごとで、部位の和集合にしない。条には在ってよい note は規範文では未知の欄、閾値行の value・stage は開発規律行では未知の欄である（開発規律行の stage が台帳 f2-648.176 の形）。
- 置き場の憲法の schema 節の一覧は読まない。道具を組み立てた folio2 の憲法の一覧で閉じる。置き場の schema 節に欄を足しても床の一覧は広がらない（歯 3）。値域を組み立てた版で持つ判断の記録 ADR-16 決定 (2)(ウ) と同じ向きで、置き場ごとに一覧を広げる口は持たない（N-3.1）。
- 例外の旗・既定に倒れる枝・一覧を切り替える設定は持たない。
- rationale の各行・retreat・relations・amended_by の各行・meta の counts と approval の中の欄は、憲法の注が名指さず、schema 節も一覧を宣言していないので数えない（(i) の 2）。
- 未知の欄のほかの検査は 1 つも止めない。必須の欄の有無も数えない。今の床の非空（id・title・statements ほか・規則の表は id・article・what）は変えない（(i) の 2）。

**生成区間は動かない。** 規則の表の行の一覧は、定数の値も床の木（rules.rs の FLOOR）も変えないので、生成区間の写しと凍結 anchor `tests/fixtures/schema/rules-region.txt` は 1 byte も動かない。憲法の一覧は憲法の正本そのものが正本なので、写しを置く生成区間を持たない（P-5.6 が掛かるのは実装の定数が正本のときだけ・値域の導出と同じ扱い）。`rules.rs` の書き換えは頭の注の 1 文だけである（「それまで FLOOR と行の欄の定数の読み手は歯だけ」を「行の欄の定数は床〔check.rs の check_rules〕も読む〔便 128〕」に直す）。

**folio2 自身の結果は変わらない。** (a) の 4 のとおり実のデータは一覧の内なので、`folio check --dir design-intent` は合格（違反 0・まだ分からない 0）のまま、`folio schema --dir design-intent --check` は全 file 一致のままである。憲法 N-3 の機構の注の約束は、本便の着地で実態と合う。注の字は変えない。

### (c) 歯（新しく 4 本・置き場は新しい file `crates/folio/tests/` の下の unknown_fields.rs）

関数名は f128_ で始める（verify の絞り込みの語・base で `git grep -n 'fn f128_'` は 0 件）。**歯の土台**は `crates/folio/tests/constitution_range.rs` の Work と同じ形とする。一時 dir に実の `design-intent/` の写しと親の contracts/ に器の導出 file の写し schema.toml を置き、git の 1 commit にしてから、写しの字面に変異を当てて `folio check` を撃つ。当て先はちょうど 1 か所で、一時 dir は消す。歯は標準出力の違反の行（`[` で始まる行）を全部数える。

1. **f128_constitution_unknown_fields_are_violations（憲法の 5 部位）。** 元の写し → 合格（違反 0・まだ分からない 0）・終了コード 0。続けて別々の写し 4 つ = meta に bogus_meta・条 N-3 に bogus_a・条 N-3 の mechanism に bogus_m・規範文 N-3.1 に bogus_s を足す。それぞれ違反の行はちょうど 1 行で、(b) の表の字（例 `[未知の欄] constitution.yaml: 条 N-3 の mechanism の未知の欄「bogus_m」`）と一致し、終了コード 1。さらに別々の写し 2 つ = 前文に bogus_p・前文の mechanism に bogus_pm を足す。それぞれ違反の行はちょうど 2 行で、改憲の違反（種別 N-4）の行と (b) の表の字の行である。**base では 4 つが合格・2 つが改憲の違反だけで落ちる＝RED。**
2. **f128_rule_row_unknown_fields_are_violations（規則の表の行）。** 別々の写し 3 つ = 行 R-2 に bogus_r・行 D-5 に disabled: true・行 D-14 に stage: post を足す。それぞれ違反の行はちょうど 1 行（`[未知の欄] rules.yaml: 行 D-14 の未知の欄「stage」` ほか）・終了コード 1。**base では 3 つとも合格で落ちる＝RED。**
3. **f128_place_schema_cannot_widen_the_lists（置き場の側で一覧を広げても通らない）。** 写し 1 つ目 = 憲法の schema.meta.optional に bogus_meta を足し、meta にも bogus_meta を足す → 違反の行はちょうど 2 行（改憲の違反と `[未知の欄] constitution.yaml: meta の未知の欄「bogus_meta」`）。写し 2 つ目 = 規則の表の生成区間の threshold_row.optional に bogus_r を足し、行 R-2 にも bogus_r を足す → 違反の行はちょうど 1 行（`[未知の欄] rules.yaml: 行 R-2 の未知の欄「bogus_r」`・床は生成区間の印を見ない）。**base では 1 つ目が改憲の違反だけ・2 つ目が合格で落ちる＝RED。** 置き場の schema 節か生成区間から一覧を読む形は、この歯が落とす。
4. **f128_lists_are_per_holder（部位ごとの一覧で、和集合でない）。** 1 つの写しに 5 か所の変異を同時に当てる = 規範文 N-3.1 に note（条では在ってよい欄）・条 N-3 の mechanism に relations（条では在ってよい欄）・開発規律行 D-5 に value（閾値行では在ってよい欄）・条 N-3 に bogus_a1 と bogus_a2。違反の行はちょうど 5 行で、(b) の表の字が 5 つ揃い（同じ holder の 2 つの欄は 1 つずつ数える）、終了コード 1。**base では合格で落ちる＝RED。**

**床の凍結の場合に 2 件足す（`tests/floor_cases.yaml`・新しい組 cases_unknown_fields・凍結の土台は実の design-intent から独立＝P-10.1）。**

- unknown-field-article: 変異 = 憲法の articles[id=P-8] に欄 bogus_a を add で足す。期待 = 終了コード 1・字 条 P-8 の未知の欄「bogus_a」・違反 1 件。
- unknown-field-discipline-stage: 変異 = 規則の表の discipline[id=D-1] に欄 stage（値 post）を add で足す。期待 = 終了コード 1・字 行 D-1 の未知の欄「stage」・違反 1 件。

場合の数 expected_cases は 143 から 145 になる（参考値）。起草役が凍結の土台の写しに同じ 2 つの変異を当てて base の binary を撃つと、どちらも合格（終了コード 0）である＝**base で RED**（(h) の 3）。

**導出の歯（common-verify が走らせる・f128_ の名を持たない）。** `crates/folio/src/constitution_enums.rs` の tests に 1 本足す。導出した 5 部位の列が、実の憲法の正本の schema の同じ部位の required と optional を file の順に繋いだ列と、長さ・字・並びまで一致することを見る（正本の側は歯が file から読む・定数を書かない）。base では導出の定数が無いので組み立てに失敗する。名に f128_ を持たないので、verify の絞り込みには入らない（src の unit test に絞り込みの語を置かない）。

### (d) 採らなかった形

1. **置き場の憲法の schema 節から実行時に一覧を読む（最上位の節の読みと同じ形）。** (a) の 5 の 23 本の憲法は 5 部位の一覧を持たないので、読めない一覧を「まだ分からない」にすれば fixture を使う既存の歯が一斉に終了コード 2 に落ちる。黙って通せば N-3 の穴が残る。どちらを選んでも 23 本の書き換え（write-set の外の大きな便）になる。置き場の schema 節で一覧を広げられる形にもなる（歯 3 の 1 つ目）。
2. **5 部位の一覧を check.rs に手で書く。** 憲法の schema 節と同じ一覧を 2 か所に人が書き、一致を歯で強制する形で、P-6.4 と判断の記録 ADR-11 決定 (3)(ア) の「手書きの写しを持たない」に反する。
3. **憲法に生成区間を足して一覧を写す。** 憲法の字を変える（schema 節は改訂の差分の範囲）ので改憲の手続きが要り、正本の向き（憲法が正・ADR-11 決定 (3)）も逆になる。
4. **憲法 N-3 の機構の注を実態に合わせて弱める（所見 F-1 の note のもう 1 つの直し方）。** 条文の改訂ではないが、fail-closed を約束した機構の注を「まだ分からない」へ下げる形で、N-3.1 の機構の中身（行や条へ旗の欄を足しても床が拒む）を失う。
5. **未知の欄を「まだ分からない」にする。** 閉じた一覧が組み立てた版で必ず立っているので、比較元が立たない場面は無い。N-3.1 は拒むことを求めるので違反にする。

### (e) 大きさ・verify と done の対応

1. **write-set の印。** 新しい file 1 本に `+`（`crates/folio/tests/` の下の unknown_fields.rs）。書き換える 6 本（`crates/folio/build.rs`・`crates/folio/src/check.rs`・`crates/folio/src/constitution_enums.rs`・`crates/folio/src/rules.rs`・`crates/folio/tests/floor_cases.rs`〔本文不変・verify の scope〕・`tests/floor_cases.yaml`）は印なし。`-`（行が減る file）と、着地で消える file の印は当たらない。新しい dir は作らない。
2. **余地（CapHeadroom）。** 測るのは `crates/folio/src/` の下の印なしの .rs の 3 本（新しい .rs は src に無い）。測り方は各行の字数を 120 で割って切り上げ（空行は 1）、全行で足す（`wc -l` ではない・script は (h) の 4）。size S の見積は 1 file あたり 100。

| file | base の正規化行数（参考値） | 余地 = 1500 − 正規化行数 | 本便で増える見積（参考値） |
| --- | --- | --- | --- |
| `crates/folio/src/check.rs` | 951 | 549 | 40 |
| `crates/folio/src/constitution_enums.rs` | 86 | 1414 | 30 |
| `crates/folio/src/rules.rs` | 295 | 1205 | 0（注の 1 文の書き直し） |

   3 本とも余地は S の 100 を超える（check.rs は M の 300 も超える）。src の外の `crates/folio/build.rs` は参考に 442（余地 1058）で、増える見積は 50 である。歯の file は src の外なので余地を測らない。
3. **size は S。** 変える src は 3 本と組み立ての script 1 本で、どれも 1 file あたり 100 行を超えない見積である。
4. **verify は 3 行**で、done の 3 つの塊と 1 対 1 に揃える。
   1. `cargo nextest run -p folio --test unknown_fields f128_` = (c) の新しい歯 4 本。
   2. `cargo nextest run -p folio --test floor_cases` = 床の凍結の場合（expected_cases の件数どおり・新しい 2 件を含む）。
   3. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** verify が `--test` で名指す歯の file は unknown_fields と floor_cases の 2 本で、どちらも write-set に在る（floor_cases は本文不変）。絞り込みの語 f128_ を関数名に持つ file は unknown_fields の 1 本だけで、src には置かない。導出の歯（constitution_enums.rs の tests）は共通の検証（`.vessel.toml` の common-verify の workspace の nextest）が走らせる。

### (f) 既存の歯のうち落ちるもの・凍結 anchor が動くか

1. **落ちる既存の歯は 0 本の見積である。** (a) の 4・5 のとおり、実の design-intent・fixture 25 本・床の凍結の場合の add の変異・骨格の置き場は、どれも閉じた一覧の内に収まる。値域の歯（`crates/folio/tests/check.rs` の check_constitution_enum_ で始まる歯）の変異は値だけを変え、欄の名を足さない。起草役は実装を組んでいないので、この 0 本は模擬の数え（(h) の 2）による見積で、workspace の nextest の実測ではない（(i) の 3 の撤退条件 (1)）。
2. **凍結 anchor は動かない。** 凍結の土台（`tests/fixtures/floor_base/`）・生成区間の写し（`tests/fixtures/schema/` の下の *-region.txt の 9 本と要約値の anchor）・判断の記録の欄の決まりの写しは 1 byte も動かない。本便は `design-intent/` を書き換えず、`tests/fixtures/` の file を 1 本も書き換えないからである。値域の凍結 anchor（`tests/fixtures/check/enum-range-anchor.yaml`）も値域を変えないので動かない。床の凍結の場合の file は場合が 2 件増えるだけで、既存の 143 件の変異と期待は変えない。
3. **folio2 自身の結果**（`folio check --dir design-intent` の合格・`folio schema --dir design-intent --check`・`folio inject --check`・`folio build --write` の出力）は変わらない。歯 1 の最初の段が、元の写しの合格を見る。

### (g) 門（規則の表の開発規律行 D-12）

本便は `design-intent/` の下を 1 本も書き換えないので天井の門の対象外で、実測は 0（通す）（§0 の 門）。

### (h) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草の記録は持ち主の home の下の `.local/share/folio2/handoff-2026-09-24/d128-draft.md`、script は同じ dir の d128_base_measure.sh と d128_sim.py（repo には入れない）。

1. base の実測（(a) の 2）: `d128_base_measure.sh <repo> <folio の binary>`。写しを git の 1 commit にしてから欄を 1 つずつ足し、`folio check` の終了コードと末尾の行を印字する。
2. 模擬の数え（(a) の 4・5）: `BUILT=design-intent/constitution.yaml python3 d128_sim.py design-intent <fixture の置き場>...`（folio2 の憲法の 5 部位の一覧と規則の表の行の一覧で、宣言の外の欄を数える）。骨格は `folio init --dir <一時 dir>/design-intent` の出力に同じ script を当てる。
3. 床の凍結の場合の RED: 凍結の土台の写しに (c) の 2 件の変異を当てて base の binary の `folio check` → どちらも合格。
4. 余地: `python3 d119-draft-lines.py crates/folio/src/check.rs crates/folio/src/constitution_enums.rs crates/folio/src/rules.rs crates/folio/build.rs`（便 119 の script・同じ式）。
5. 着地の後: `cargo nextest run --workspace --no-tests=fail --no-fail-fast`（全部緑）・`cargo clippy --workspace --all-targets -- -D warnings`・`folio check --dir design-intent`（合格）・`folio schema --dir design-intent --check`・`folio inject --check`。
6. 出力の差: base と後の binary で `folio build --dir design-intent --out <別々の置き場> --write` を撃ち、`diff -r` が差 0。
7. 門: 本体の作業ツリーで `folio ceiling --gate --dir design-intent --write-set <write-set の 7 本（接頭辞を剥がす）>`。

### (i) 本便が運ばないもの・言えないこと・撤退条件

1. **運ばないもの。** 憲法・規則の表・要件書・判断の記録・語彙・天井の字（憲法 N-3 の機構の注と判断の記録 ADR-11 の注 (ア) の字を含む）。値域の導出と値域の部分集合の数え（便 49・便 122）。面の生成器。規則の表の生成区間と床の木の値。台帳への記帳（台帳 f2-648.176 の昇格と close は席）。外部 crate。
2. **言えないこと — 数えない欄。** (b) の最後の箇条の holder（rationale の各行・retreat・relations・amended_by の各行・meta の counts と approval）の中の未知の欄は、本便の後も数えない。憲法の注はこれらを名指さず、schema 節も一覧を宣言していないので、閉じる一覧が無い。必須の欄の有無（閾値行の value・kind・status・ruling・ruled_at・stage ほか・判断の記録 ADR-11 の注 (ア) が「床に足すのは後続の便」と書いた部分）も数えない。この部分は ADR-11 の注のとおり「まだ分からない」のままである。
3. **撤退条件。** (1) 本便の後に既存の歯が 1 本でも落ちたら、その歯の本文も fixture も直さずに止めて席へ返す（(f) の 1 は模擬の見積なので、落ちたら見積の外の欄が在ったことになる）。(2) 本便の後に folio2 自身の置き場の床の結果（合否・違反と「まだ分からない」の件数）か `folio build` の出力が 1 byte でも変わったら、止めて席へ返す。(3) 受付の時点の main で `crates/folio/src/check.rs` の check_constitution か check_rules の周り、`crates/folio/build.rs` の main の憲法の段、または憲法の正本の schema の 5 部位の一覧が base と違っていたら、base を取り直して (a) の 4・5 と余地を測り直してから運ぶ。

## 2. 範囲

- 入れる: `crates/folio/build.rs` の新しい純粋な関数 constitution_fields（憲法の 5 部位の閉じた一覧の導出・Err の 4 つの形）と、main で値域の source の後ろに繋ぐ 1 行。`crates/folio/src/constitution_enums.rs` の導出の歯 1 本と頭の注の 1 文。`crates/folio/src/check.rs` の新しい関数 unknown_fields と、check_constitution・check_rules からの呼び出し（(b) の表の 8 か所）と頭の注の 1 文。`crates/folio/src/rules.rs` の頭の注の 1 文。新しい歯の file（f128_ の 4 本）。`tests/floor_cases.yaml` の組 cases_unknown_fields の 2 件と expected_cases（145）。
- 入れない: 憲法と規則の表ほか設計文書の字・生成区間と床の木の値・凍結の土台と生成区間の写しと値域の anchor・値域の導出と部分集合の数え・必須の欄の有無の検査・rationale ほか (i) の 2 の holder の欄・面の生成器・`crates/folio/tests/floor_cases.rs` の本文・新しい dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| derive | 憲法の 5 部位の一覧の導出 | `crates/folio/build.rs` の新しい関数 constitution_fields（組み立て時・導出できなければ組み立てを失敗させる） |
| derivetest | 導出の歯 | `crates/folio/src/constitution_enums.rs` の tests（導出した列と正本の一致） |
| count | 未知の欄の数え | `crates/folio/src/check.rs` の新しい関数 unknown_fields と check_constitution・check_rules からの呼び出し |
| rows | 規則の表の行の一覧 | `crates/folio/src/rules.rs` の閾値行と開発規律行の required と optional（値は不変・頭の注の 1 文） |
| cases | 床の凍結の場合 | `tests/floor_cases.yaml` の組 cases_unknown_fields の 2 件 |
| teeth | 歯 | 新しい歯の file の f128_ の 4 本 |

## 4. 検査（歯）

§1 (c)(f) と (e) の 4 のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate は増やさない（組み立ての script は今の yaml_rust2 を使う）。新しい dir は無い。host に要る命令は無い。
- 前提の着地: 無い。base は main ee714d7（便 125 の着地の後・§0 の 前の便）。
- 並行の便: `crates/folio/src/check.rs`・`crates/folio/build.rs`・`tests/floor_cases.yaml` を書き換える未着地の便は、起草の時点で契約表に無い。受付の時点で重なりが在れば、席が 1 本ずつ運ぶ。
- 本便の着地の後に席が見ること: 台帳 f2-648.176 を本便の行で閉じる。天井の次の周の実態の観点で、29 周目の F-1 の場所（憲法 N-3 の機構の注）が支持されないこと。判断の記録 ADR-11 の注 (ア) の必須の欄の集合の床は、別の便で起こす（(i) の 2）。
- 後の便への申し送り: 憲法の 5 部位の一覧を変える改訂（改憲の手続き）は、組み立て直すと床の一覧も動く。実の design-intent のどこかの holder が新しい欄を使い始めたら、同じ改訂で一覧に足さないと床が落とす。規則の表の行の一覧を変える便は `crates/folio/src/rules.rs` の定数を変え、生成区間を `folio schema --write` で導出し直し、凍結 anchor `tests/fixtures/schema/rules-region.txt` を同じ便で直す（行 D-11 の作法）。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "dz"
title = "天井の 29 周目の実態の所見 F-1（止める・反証で支持）と台帳 f2-648.176（規則の表の開発規律行に stage を書いても床が黙って落とす）と憲法 N-3 の機構の注（正本と rules の全節で未知の欄を schema 検査が落とす・床は folio check）の 1 便: 憲法の meta・前文・前文の mechanism・条・条の mechanism・規範文と、規則の表の閾値行・開発規律行の欄を、holder ごとの閉じた一覧で数え、一覧に無い欄を 1 つにつき種別 未知の欄 の違反 1 件にする（fail-closed・例外の口なし）。憲法の 5 部位（meta・precedence・article・mechanism・statement）の一覧は判断の記録 ADR-11 決定 (3) のとおり憲法の正本が正で、crates/folio/build.rs の新しい関数 constitution_fields が組み立て時に schema の required と optional から導出する（導出できなければ組み立てを失敗させる・手書きの写しは持たない・置き場の schema 節は読まない）。規則の表の行の一覧は crates/folio/src/rules.rs の今の型付きの定数（写しは生成区間に在る）を床が読み、file の生成区間は読まない。crates/folio/src/check.rs に新しい関数 unknown_fields を足し、check_constitution と check_rules から呼ぶ。憲法と設計文書の字・生成区間・凍結 anchor は変えず、folio2 自身の床の結果は変わらない。歯は新しい crates/folio/tests/unknown_fields.rs の f128_ の 4 本と、tests/floor_cases.yaml の新しい組の 2 件（凍結の土台の条 P-8 と開発規律行 D-1 に欄を足す）と、導出の歯 1 本"
req = ["FR5"]
section = "1"
write-set = ["crates/folio/build.rs", "crates/folio/src/check.rs", "crates/folio/src/constitution_enums.rs", "crates/folio/src/rules.rs", "+crates/folio/tests/unknown_fields.rs", "crates/folio/tests/floor_cases.rs", "tests/floor_cases.yaml"]
verify = ["cargo nextest run -p folio --test unknown_fields f128_", "cargo nextest run -p folio --test floor_cases", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "f128_ の歯 4 本（元の写しは合格で、憲法の meta・条・条の mechanism・規範文に足した未知の欄はそれぞれ違反ちょうど 1 行、前文と前文の mechanism に足した欄は改憲の違反と未知の欄の 2 行／規則の表の行 R-2 の bogus_r・行 D-5 の disabled・行 D-14 の stage はそれぞれ未知の欄の違反ちょうど 1 行／置き場の憲法の schema.meta.optional と規則の表の生成区間の threshold_row.optional を広げても未知の欄の違反は消えない／規範文の note・条の mechanism の relations・開発規律行の value・条の 2 つの欄を同時に足すと違反ちょうど 5 行で、一覧は holder ごと）が緑、床の凍結の場合が tests/floor_cases.yaml の expected_cases（145）どおりで新しい 2 件（条 P-8 の未知の欄・開発規律行 D-1 の stage）が終了コード 1、clippy が 0 警告で、workspace の nextest が全部緑（導出の歯・値域の歯・folio2 自身の置き場の合格の歯を含む）で CI が通り、着地の後の main で folio check --dir design-intent が 合格（違反 0・まだ分からない 0）を返す"
<!-- contracts:end -->
