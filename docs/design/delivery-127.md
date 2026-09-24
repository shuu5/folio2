# 設計: 便 127 — 面の天井の名札に「印の後に変わった所はまだ読まれていない」を添える（ADR-18 決定 (6) の便イ）

- 要件: FR18（観点ごとの 3 値と日付を、生成する面に天井の名札として床の名札と別の欄で出す）/ FR20（印の中身の列の正本の要約値・引き金の要約値は印と門が同じ関数で測る）。どちらも要件書 第 1.37 版（main 4eb2d2d）の id。**本便の振る舞い（名札の添え書き）は、どちらの要件の規範文にもまだ字として無い。** 出所は判断の記録 ADR-18 決定 (6) で、同じ判断の決定 (7) が要件書へ運ぶ字は FR20 と AC18 の改訂だけだった。本便は規範文を変えない。要件 FR18 の注と語彙の「天井の名札」の定義に添え書きを書き足すのは、着地の後の席の起草と持ち主の承認である（§5）。
- 条: P-3.3（床の合格を、完成や天井の合格として扱わない）/ P-4.2（判定できないものは「まだ分からない」として表に出す＝読まれていない字を表に出す）/ P-4.1（測れない結果を「異常なし」として扱わない）/ P-15.2（名札と門と印は、正本の要約値を同じ 1 つの関数で測る）/ P-6.3（名札の字は 1 つの関数で組み、5 面で同じ）/ P-10.1・P-10.2（独立した物差しを持ち、生成物どうしの突き合わせを唯一の合格判定にしない）
- 出所: 判断の記録 **ADR-18**（案 a・発効 2026-09-24 11:51 JST・持ち主の承認・対話面 R-8・逐語「全部推奨で」・裁定 id = 台帳 f2-648 notes 2026-09-24 11:51 JST）の決定 (6)「面の天井の名札は、印の正本の要約値が今の正本と違えば、観点ごとの 3 値と日付に「印の後に変わった所はまだ読まれていない」を添える（条 P-3.3・P-4.2）」と、決定 (7) の実装の便の 2 本目、判断の記録の承認要求 docs/design/adr-18.md §5 の便の見積の **便イ**（面の天井の名札に「印の後に変わった所はまだ読まれていない」を添える・`crates/folio/src/face.rs`・歯 `crates/folio/tests/badge.rs`・size S）。規則の表の開発規律行 D-11 は、この行と契約表の行の title が ADR-18 と裁定 id を名指すことで満たす。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `ea` が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は手書きで 3 本。**新しい file は無い**（`+` は当たらない）。縮む file も消す file も無く（`-` は当たらない）、新しい dir も作らない。`~` は使わない。
- 門: 本便は設計文書の正本（`design-intent/` の下）を 1 本も書き換えないので、天井の門の対象外である。起草役が本体の作業ツリー（main 4eb2d2d・同じ木で build した binary）で write-set 3 本を `folio ceiling --gate --dir design-intent --write-set …` に渡した実測は **0（通す・断りの字 = 設計文書の正本を書き換えない便）**（2026-09-24）。規則の表の開発規律行 D-12 は当たらない。
- 前の便: **受付は便ア（便 126・契約 docs/design/delivery-126.md の行 `dy`・台帳 f2-648.178）の着地の後。受付の時点の main で数え直す（規則の表の行 D-13）。** 判断の記録の承認要求 §5 の順（便ア → 便イ → 次の周で印を付け直す）に従う。**base = main 4eb2d2d（便アの契約の着地の後・便アの実装の着地の前）。この契約の数はすべて base 4eb2d2d の参考値である。** 本便の code が呼ぶのは base に既に在る関数（`crates/folio/src/gate.rs` の sources_digest と `crates/folio/src/ceiling_src.rs` の load）だけで、便アの新しい関数・欄（引き金の要約値の関数・印の欄 trigger・門の判定の 8 段）は呼ばない。便アの契約の §1 (c) は、印の欄 sources と関数 sources_digest の形を変えず（門の判定の 7 段目「今の正本の要約値〔sources_digest〕が測れない → 2〔今と同じ理由の字〕」）、名札が読む口（`crates/folio/src/stamp.rs` の marks）も変えないと定める（便アの §1 (c) の 4）。この前提が便アの着地で崩れていたら、§1 (h) の撤退条件 (3) のとおり測り直す。
- 並行の便との重なり: 便アの write-set 37 本と本便の write-set 3 本は、`crates/folio/src/stamp.rs` の 1 本で重なる。便アが書き換えるのは印を導出する derive と頭の注で、本便が書き換えるのは名札のために印を読む marks（base で 268〜308 行）とその注である。受付を便アの着地の後に置くので、2 つを並べて運ばない。

## 1. 設計

### (a) いま起きていること（実測・base main 4eb2d2d）

1. **名札は印の値をそのまま出し、古さを見ない。** 名札の字は `crates/folio/src/face.rs` の ceiling_stamp の 1 つで組み、5 面（入口・憲法・要件書・判断の記録・設計ノート）の生成器が同じ字を site-bar の床の名札（部品 freshness-stamp）の直後に置く（便 40・便 83）。出所は天井の印 `<dir>/preview/ceiling-stamp.yaml` と天井の正本の観点の名だけで、印が在れば「天井 <b>名 3 値</b> · …（<印の at>・束 <8 字>/…）」、無ければ「…（未実施）」。印の読み手は `crates/folio/src/stamp.rs` の marks で、返すのは（印の at・観点の行〔id・3 値・at・束〕）だけである。**印の欄 sources（正本の要約値）は読まない。** だから印を付けた後に設計文書が変わっても、名札は同じ字のまま「合格」を出し続ける。
2. **正本の要約値を測る関数は 1 つ在る。** `crates/folio/src/gate.rs` の sources_digest（crate の中だけで見える）は、天井の正本の観点の reads が指す文書の file（file 形はその file・dir 形は直下の .yaml）の全文を、`<dir>` からの相対 path の byte 順に連結した sha256 を「sha256 <16 進 64 字>」で返す。門（同じ file の run）と印（`crates/folio/src/stamp.rs` の derive・便 104）がこの関数を共有している。
3. **実の印は今古い。** 実の印（design-intent/preview/ceiling-stamp.yaml・天井の 28 周目・4 観点とも合格）の sources は `sha256 41524070…`。起草役が関数の式を写した独立の script（§1 (i)・PyYAML と hashlib）で今の design-intent を測ると `sha256 6bcd7e44…` で違う。今の名札は、印の後の判断の記録 ADR-17〜19 の発効と一括 16 を読んでいない周の「合格」を、断りなしで出している。
4. **独立の式は folio の式と一致する（実測）。** 同じ script の値を、写しの印の sources に書いて base の binary で門を撃つと、実の design-intent の写しでも面の凍結 fixture の写し（歯の face_copy と同じ 9 file）でも「通す（印が 4 観点とも合格・正本の要約値が同じ）」になる。面の凍結 fixture の写しで、どの観点も読まない rules.yaml の末尾にコメントの 1 行を足しても同じ「通す」、観点が読む srs.yaml の末尾に足すと「まだ分からない（印が古い）」になる。
5. **固定点の問題は起きない。** 便 40 §1 (b) は、名札を載せた面が次の束の入力になるので、名札が面の要約値を測ると固定点が無いと述べた。本便が比べるのは正本の要約値（設計文書の YAML の全文）で、生成物の棚 preview/ の file（印・面）は入らない（天井の正本の documents の file は preview/ を指さない）。名札の字が変わっても比べる値は変わらない。
6. **名札の字を固定している歯は `crates/folio/tests/badge.rs` だけ。** `git grep -n '天井 <b>' -- crates tests` は badge.rs の定数 2 つ（STAMP_PASS・STAMP_NONE）だけに当たる。名札を持つ凍結 fixture は `git grep -l 'data-component="ceiling-stamp"' -- tests` で 7 本（`tests/fixtures/face/` の expected-*.html）で、7 本とも印なしの「未実施」の形である。歯の印は helper の mark_text が書き、欄 sources は仮の値 `sha256 00` で、今の名札はこの欄を読まないので歯は緑である。
7. base の badge.rs の歯は 12 本（`#[test]` の数）。

### (b) 直す先 — 名札が印の正本の要約値と今の正本を比べる

1. **印の読み手が sources も返す。** `crates/folio/src/stamp.rs` の marks の返りを（印の at・**印の sources**・観点の行）にする。sources は今の欄 at と同じ読み（字で・空白だけでない）で、読めなければ Err「preview/ceiling-stamp.yaml: sources が読めない」（P-4.1・今の欄の Err と同じ形）。観点の行の型 Mark と他の欄の読みは変えない。呼び手は face.rs の ceiling_stamp の 1 か所だけ（base で `git grep -n 'stamp::marks' -- crates` は 1 件）。
2. **名札が今の正本の要約値を測って比べる。** face.rs の ceiling_stamp の、印が在る枝で、観点の id の列の突き合わせ（今の Err）の後に、天井の正本を `crates/folio/src/ceiling_src.rs` の load で読み、`crates/folio/src/gate.rs` の sources_digest で今の正本の要約値を測る。**印と門と名札が同じ 1 つの関数で測る**（P-15.2・便 104 と同じ形で、名札の側に式を書き写さない）。face.rs は責務の層 4、gate.rs は層 2、ceiling_src.rs は層 1 なので下向きの辺で、層の歯（`crates/folio/tests/modules.rs`）の割り当てと上がる辺の一覧は変わらない。
3. **字（3 形）。** 値は escape 済み。定数 1 つ（字は判断の記録 ADR-18 決定 (6) の逐語「印の後に変わった所はまだ読まれていない」）を face.rs に置く。
   - 印が無い: 今と同じ「天井 <b>名 まだ分からない</b> · …（未実施）」。要約値は測らない（天井の正本の documents の file が無くても面は出る＝今と同じ）。
   - 印の sources が今の正本の要約値と同じ: 今と同じ「天井 <b>名 3 値</b> · …（<at>・束 …）」。
   - 違う: 同じ字の閉じ括弧の直後に `<b>印の後に変わった所はまだ読まれていない</b>` を置く。観点ごとの 3 値（合格・不合格・まだ分からない）のどれでも同じに添える。小窓（hint）はその後ろで、中身は 1 字も変えない。
   - 例（違う・4 観点とも合格）: `<span data-component="ceiling-stamp">天井 <b>忠実さ 合格</b> · <b>読みやすさ 合格</b> · <b>文書どうしの整合 合格</b> · <b>実態との整合 合格</b>（2026-09-19T05:00:00Z・束 2bd67637/ded1548e/91ca924d/24ce1b87）<b>印の後に変わった所はまだ読まれていない</b><span class="hint">…`
4. **測れないときは面を導出しない。** 天井の正本が load で読めない、または sources_digest が Err（読む文書の file が無い・読めない・symlink）なら、ceiling_stamp は Err「天井の名札: 正本の要約値が測れない: <理由>」を返し、面は 2（まだ分からない）で 1 byte も書かない（P-4.1・今の「印が読めない」「印の観点が正本と違う」と同じ扱い）。測れないのに添え書きなしで出すと古い「合格」を断りなしで出すことになり、測れないのに添え書きを付けて出すと「変わった」と言えないことを言うことになる。どちらも採らない。
5. **5 面で同じ字。** 名札の字は ceiling_stamp の 1 つで組むので、添え書きも 5 面で同じになる（便 40 (d)・P-6.3）。`folio face` の --write と --check、`folio build` の --write と --check は同じ関数を通るので、添え書きも byte 一致の対象になる。
6. **並べる場所。** 添え書きは括弧の外に、`<b>` で置く。部品 ceiling-stamp の様式は inline-flex で子の間に隙間を取る（design-intent/preview/folio.css の 95 行）ので、`<b>` にすると添え書きは括弧の字と分かれた 1 つの塊として並ぶ。括弧の中に置かないのは、小窓の本体の字「括弧の中は、最後に数えた日付と、観点ごとの材料の束の要約値の先頭 8 字です。」を正しいまま保つためである（(d) の 2）。

### (c) 門と名札の違い（便アの後）

便アの着地の後、門は印の引き金の要約値で古さを判定し、引き金は同じで正本の要約値だけが違えば、通すときに理由の行へ「印の後に引き金の外の変更が在る（節点 k 個・次の引き金の周が読む）」を添える（便アの契約の §1 (c) の 2）。名札の添え書きは決定 (6) の字のとおり正本の要約値の比較だけで決め、次の 2 点で門と違う。

1. **名札は引き金の要約値を読まない。** 引き金の要約値が違う（門は まだ分からない〔印が古い〕）ときも、名札は印の 3 値に同じ添え書きを付けて出す。folio2 の天井の正本では観点 coherence の reads が読む文書 10 本を全部指す（design-intent/ceiling.yaml の viewpoints）ので、引き金の文書 5 つ（憲法・判断の記録・要件書・規則の表・天井の正本）のどれかの規範の欄が変われば、必ず正本の要約値も変わって添え書きが付く。
2. **名札は節点の数 k を出さない。** k は印の節点の表と今の表の突き合わせで、門だけが数える（(d) の 1）。

### (d) 採らなかった形

1. **名札に節点の数 k と引き金の比較を足す。** 決定 (6) の字は正本の要約値の比較と 1 つの添え書きで、k も引き金も求めていない。k を数えるには、面の生成のたびに節点の表（`crates/folio/src/graph.rs` の stamp_table）を 5 面ぶん組み、印の節点の表を読む口を marks に足すことになる。歯の印（helper の mark_text）は節点の表を持たないので、歯の土台も組み替えになる。引き金の比較は便アの関数に依って、本便を便アの実装と同じ木に縛る。読まれていない字が在ることは添え書きで表に出る（P-4.2）ので、この 2 つは採らない。持ち主が名札にも数を求めるなら、別の便で問う。
2. **添え書きを括弧の中に入れる（`（<at>・束 …・印の後に…）`）。** 小窓の本体の「括弧の中は、最後に数えた日付と、観点ごとの材料の束の要約値の先頭 8 字です。」が不正確になる。小窓を直すと、小窓の本体を逐語で持つ面の凍結 fixture 7 本（印なしの形でも小窓は在る）が全部動く。採らない。
3. **測れないときに添え書きを付けて面を出す。** 「変わった」と言えないことを言う。P-4.1 に従い、面は まだ分からない にする（(b) の 4）。
4. **名札の側に要約値の式を書き写す。** 印・門・名札の 3 面に同じ式を持つことになり、P-15.2 と P-6.3 に反する。採らない。
5. **印に「読まれていない」欄を足す。** 印は周の結果の生成物で、周の後に変わる字の量を印は知らない。名札が面の生成の時点で比べる（印の欄は 1 つも足さない）。

### (e) 歯（新しく 3 本・関数名は f127_ で始める・置き場は `crates/folio/tests/badge.rs`）

verify の絞り込みの語は f127_（base で `git grep -n 'f127_' -- crates` は 0 件）。

**独立の物差し（P-10.1・P-10.2）。** 歯の file に helper を 1 つ足す（仮の名 fresh_sources）。写しの天井の正本を yaml-rust2（folio が既に依存している crate・`crates/folio/tests/face_index.rs` ほかが歯の file から使っている）で読み、viewpoints の順に reads の doc（重複は 1 度）を documents の file に解き、file 形はその file、dir 形（末尾 `/`）は直下の通常 file で名が `.yaml` のものを、`<dir>` からの相対 path の byte 順に全文を連結して、外の命令 sha256sum（子の処理・`crates/folio/tests/bundle.rs` と同じ形）で測り、「sha256 <16 進>」を返す。folio の code を 1 行も呼ばない。この式は (a) の 4 で、base の binary の門と実の design-intent・面の凍結 fixture の写しの両方で一致することを実測した。

**helper の直し（既存の歯の本文は変えない）。** helper の put_mark（印を `<dir>/preview/ceiling-stamp.yaml` に書く）が、印の字の中の行 `sources: sha256 00` を fresh_sources の値に置き換えてから書く。既存の歯 12 本はどれも put_mark か real_copy（中で put_mark を呼ぶ）で印を置くので、印は今の写しに対して新しく、名札の字は今と同じになる＝既存の歯の期待の字（STAMP_PASS・STAMP_NONE ほか）は 1 字も変えずに緑のまま。仮の値のまま印を置きたい歯（歯 2）は、置き換えない書き方（fs::write で直に書く）を使う。

1. **添え書きは、観点が読む文書が変わった後にだけ付き、5 面で同じ。** 面の凍結 fixture の写し（face_copy）に put_mark で 4 観点とも合格の印を置く → 5 面（five_faces）の名札がどれも STAMP_PASS で始まり、字「印の後に変わった所はまだ読まれていない」を持たない。続けて、どの観点も読まない rules.yaml の末尾に行 `# f127` を足す → 5 面とも同じく添え書きなし。続けて、観点が読む srs.yaml の末尾に同じ行を足す → 5 面の名札がどれも「STAMP_PASS の閉じ括弧と小窓の開きの間に `<b>印の後に変わった所はまだ読まれていない</b>` を挟んだ字」で始まり、5 面の名札が全部 index.html と同じ。**base では最後の段で添え書きが無く落ちる＝RED**（(a) の 4 の実測で、base の面は印の sources を読まず、仮の値の印でも名札の byte が変わらない）。
2. **添え書きは観点の 3 値のどれにも同じに付く。** 写しに、観点の 3 値を 不合格・合格・まだ分からない・合格 にした印を、sources を仮の値 `sha256 00` のまま fs::write で置く → 入口の面の名札に「天井 <b>忠実さ 不合格</b> · <b>読みやすさ 合格</b> · <b>文書どうしの整合 まだ分からない</b> · <b>実態との整合 合格</b>（2026-09-19T05:00:00Z・束 2bd67637/ded1548e/91ca924d/24ce1b87）<b>印の後に変わった所はまだ読まれていない</b><span class="hint">」が逐語で 1 度在る（helper の assert_once）。**base では添え書きが無く落ちる＝RED。**
3. **正本の要約値が測れなければ面は まだ分からない。** 写しに put_mark で 4 観点とも合格の印を置いてから、写しの天井の正本の観点 fidelity の reads に `{doc: graph, fields: [nodes]}` を足す（documents の行 graph の file graph.yaml は写しに無い・fixture の天井の正本で置き換える字 `reads: [{doc: srs, fields: [requirements.plain]}]}` は 1 度だけ在る）→ `folio face --face index --write` が終了コード 2・出力の file を書かない・標準エラーに字「正本の要約値が測れない」と「graph.yaml」が在る。**base では同じ写しで 5 面とも終了コード 0 で書く（起草役の実測）＝RED。** base の門は同じ写しで「まだ分からない（graph.yaml: 読めない: …）」を返すので、名札と門の Err の出所が同じ関数であることもこの歯が縛る。

**base で RED は 3 本とも。** 起草役は実装を組んでいないので、RED の根拠は上の base の実測（仮の値の印で名札の byte が変わらない・graph の reads を足しても面が 0）から読んだ見込みである。歯の効きの見込み（検証役が実装の後に変異を当てて確かめる）:

| 当てた形 | 落ちる歯（見込み） |
| --- | --- |
| 名札が添え書きを出さない（base の形） | 1・2・3 |
| 印の sources を比べず、印が在ればいつも添える | 1（1 段目と 2 段目）と、既存の歯 badge_stamp_is_verbatim_for_pass_fail_unknown・f83_stamp_comes_from_the_mark |
| 観点の reads でなく置き場の YAML を全部測る | 1（2 段目） |
| 測れないときに添え書きなしで出す／添え書きを付けて出す | 3 |
| 合格の観点だけに添える・3 値のどれかで添えない | 2 |
| 添え書きを括弧の中に入れる・字を変える | 1・2 |
| 面ごとに名札を組み直して字が割れる | 1 |

### (f) 既存の歯のうち落ちるもの・凍結 anchor が動くか

1. **helper を直さないと落ちる既存の歯は 2 本（見込み）。** badge_stamp_is_verbatim_for_pass_fail_unknown と f83_stamp_comes_from_the_mark は、名札の字を閉じ括弧の直後の小窓の開きまで逐語で見る。仮の値 `sha256 00` の印のままだと添え書きが挟まって落ちる。(e) の helper の直しで、本文を変えずに緑に戻る。ほかの既存の歯 10 本は、名札の中の束の字・小窓の数と中身・部品の名札・終了コードを見る形で、添え書きの有無に依らない（helper の直しの後はどれも添え書きの無い字を見る）。
2. **凍結 anchor と凍結 fixture は 1 byte も動かない。** 面の凍結 fixture 7 本はどれも印なしで組む（未実施の形・(a) の 6）ので、要約値を測らず字も変わらない。小窓の本体・部品目録（design-intent/preview/parts.json と `tests/fixtures/floor/parts-catalog.json`）・様式（folio.css）・印の凍結 fixture（`tests/fixtures/ceiling/findings/stamp-*.yaml`）・印の凍結 anchor（stamp-expected.yaml）は触らない。部品は増えない（添え書きは部品 ceiling-stamp の中の `<b>`・名札の 3 値の `<b>` と同じ要素）。
3. **実の design-intent から組む面の歯。** `crates/folio/tests/face.rs`・`face_index.rs`・`face_srs_body.rs` ほかの「実の正本」の歯は、実の印（今古い）の写しから面を組むので、本便の後は名札に添え書きが付く。これらの歯は名札の字を見ず、部品の名札の閉じた一覧・逐語・件数を見る（(a) の 6 の grep）ので、緑のままの見込み。
4. 本便の後の木で workspace の nextest は全部緑（見込み・base の歯の数 + 新しい歯 3）・clippy 0 警告・`folio check --dir design-intent` 合格・`folio schema --dir design-intent --check`・`folio inject --check` 0。

### (g) 大きさ・verify と done の対応

1. **write-set の印。** 3 本とも印なし（新しい file・消す file・縮む file は無い）。書き換える src 2 本（`crates/folio/src/face.rs`・`crates/folio/src/stamp.rs`）と歯の file 1 本（`crates/folio/tests/badge.rs`）。新しい dir は作らない。
2. **余地（CapHeadroom）。** 測るのは `crates/folio/src/` の下の印なしの .rs の 2 本。測り方は各行の字数を 120 で割って切り上げ（空行は 1）、全行で足す（`wc -l` ではない・script は §1 (i)）。size S の見積は 1 file あたり 100。

   | file | base の正規化行数（参考値・base 4eb2d2d） | 余地 = 1500 − 正規化行数 | 本便の後の見込み |
   | --- | --- | --- | --- |
   | `crates/folio/src/face.rs` | 988 | 512 | 約 1,005（定数 1・比べる数行・Err の字・注） |
   | `crates/folio/src/stamp.rs` | 341 | 1,159 | 約 347（sources の読み・返りの型・注） |

   2 本とも余地は S の 100 を超える。便アの着地で stamp.rs は約 345 になる見込み（便アの契約の §1 (g) の 2）で、余地は 1,100 を超えたまま。face.rs は便アの write-set に無い。歯の file は src の外なので余地を測らない（badge.rs は base 749 行・helper と歯 3 本で約 170 行増える見込み）。
3. **size は S。** 変える src は 2 本で、増える行は合わせて約 25 の見込み。
4. **verify は 3 行**で、done の 3 つの塊と 1 対 1 に揃える。
   1. `cargo nextest run -p folio --test badge f127_` = (e) の新しい歯 3 本。
   2. `cargo nextest run -p folio --test badge` = 名札の歯の全部（今の 12 本と新しい 3 本・helper の直しの後も既存の 12 本が本文不変で緑）。
   3. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** verify が `--test` で名指す歯の file は badge の 1 本で、write-set に在る。絞り込みの語 f127_ を関数名に持つ file は、その 1 本だけである（src の unit test には置かない）。`crates/folio/tests/face.rs` ほかの面の歯は本文を変えないので write-set に入れず、verify でも名指さない（共通の検証の workspace の nextest が回す）。

### (h) 本便が運ばないもの・言えないこと・まだ分からない点・撤退条件

1. **運ばないもの。** 完成の判定（決定 (6) の前半・機械の口は無く、判断の記録 ADR-8 決定 (4) の今の字のまま）。門・印・引き金の要約値（便ア）。名札の節点の数と引き金の比較（(d) の 1）。小窓の本体の字。実の印の付け直し（生成物・次の周で席が --stamp で書く）。要件 FR18 の注・語彙の「天井の名札」の定義への添え書きの書き足し（人が書く字・着地の後の席の起草）。外部 crate。
2. **言えないこと — 名札は「どこが」変わったかを言わない。** 添え書きは、印の後に観点が読む文書のどれかが 1 byte でも変わったことだけを言う。変わった所が規範の欄か注か、何か所かは、門の理由の行（便アの後）と次の周の束が言う。
3. **言えないこと — 読む文書の外の変更。** 観点がどれも読まない文書の変更は正本の要約値に入らないので、添え書きは付かない（歯 1 の 2 段目の形）。folio2 の天井の正本では観点 coherence が文書 10 本を全部読むので当たらないが、利用者の置き場の天井の正本が観点の読む文書を絞れば当たる。
4. **まだ分からない — 狭い幅の見え方。** 名札は site-bar の中で折り返さない（white-space: nowrap）。中幅と狭い幅では床と天井の名札を隠す（folio.css の 510 行と 544 行）ので、添え書きが見えるのは広い幅だけである。広い幅で site-bar に収まるかは、歯では言えない（次の天井の周の読みやすさの観点が読む）。
5. **撤退条件。** (1) 本便の後に (f) の 1 の 2 本（helper の直しで戻るもの）のほかに既存の歯が 1 本でも落ちたら、その歯の本文を直さずに止めて席へ返す。(2) 実の design-intent で正本の要約値が測れない（sources_digest が Err）なら、実の面が全部 まだ分からない になるので止めて席へ返す。(3) 受付の時点の main で、`crates/folio/src/gate.rs` の sources_digest の名・引数・返りの形、`crates/folio/src/stamp.rs` の marks の返りの形、`crates/folio/src/face.rs` の ceiling_stamp の字の組み方、印の欄 sources の名のどれかが base 4eb2d2d と違っていたら（便アの着地で変わった場合を含む）、(b) の 1〜4 を測り直して契約を改訂してから運ぶ。(4) 判断の記録 ADR-18 決定 (6) の字が改訂されていたら、(b) の 3 の字を改訂してから運ぶ。

### (i) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草の記録は持ち主の home の `.local/share/folio2/handoff-2026-09-24/d127-draft.md`、正本の要約値の独立の script は同じ dir の d127-draft-sources.py（PyYAML と hashlib・repo には入れない）、行数の script は d119-draft-lines.py（便 119 と同じ式）。

1. base の写し: `git worktree add --detach <写し> <受付の時点の main>`（起草の base は 4eb2d2d）。
2. 独立の式の一致: 実の design-intent の写しの印の sources を `python3 d127-draft-sources.py <写しの design-intent>` の値に書き換え、`folio ceiling --gate --dir design-intent --write-set design-intent/srs.yaml` が「通す（…正本の要約値が同じ）」になる。面の凍結 fixture の face_copy の 9 file の写しでも同じ。
3. RED: 歯の file（`crates/folio/tests/badge.rs`）だけを当てて `cargo nextest run -p folio --test badge f127_`（3 本とも落ちる）と `cargo nextest run -p folio --test badge`（既存の 12 本は緑）。
4. 落ちる既存の歯: src の 2 本だけを当てて `cargo nextest run -p folio --test badge` → (f) の 1 の 2 本だけが落ちる。
5. 門: `folio ceiling --gate --dir design-intent --write-set crates/folio/src/face.rs crates/folio/src/stamp.rs crates/folio/tests/badge.rs`（0）。
6. 余地: `python3 d119-draft-lines.py crates/folio/src/face.rs crates/folio/src/stamp.rs`。
7. 字を固定する歯と凍結 fixture の全数: `git grep -n '天井 <b>' -- crates tests` と `git grep -l 'data-component="ceiling-stamp"' -- tests`（(a) の 6）。

## 2. 範囲

- 入れる: `crates/folio/src/stamp.rs` の marks が印の sources も返す（返りの型と注）。`crates/folio/src/face.rs` の ceiling_stamp が天井の正本を読み、gate.rs の sources_digest で今の正本の要約値を測って印の sources と比べ、違えば閉じ括弧の直後に添え書きの `<b>` を置く・測れなければ Err（定数 1 つ・use の 1 行・頭の注と関数の注）。`crates/folio/tests/badge.rs` の helper fresh_sources と put_mark の置き換え・f127_ の歯 3 本・頭の注。
- 入れない: 門・印の導出・引き金の要約値（便ア）。完成の判定。名札の節点の数と引き金の比較。小窓の本体・部品目録・様式・面の凍結 fixture。要件書・判断の記録・憲法・規則の表・語彙の字。実の印の付け直し。新しい file と dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| read | 印の読み手 | `crates/folio/src/stamp.rs` の marks（sources も返す） |
| badge | 名札の字 | `crates/folio/src/face.rs` の ceiling_stamp（今の正本の要約値を gate.rs の sources_digest で測って比べ、違えば添え書き） |
| teeth | 歯 | `crates/folio/tests/badge.rs` の f127_ の 3 本と、独立の物差し fresh_sources・put_mark の置き換え |

## 4. 検査（歯）

§1 (e)(f) と (g) の 4 のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate は増やさない（独立の物差しは folio が既に依存する yaml-rust2 と外の命令 sha256sum を使う）。新しい dir は無い。
- 前提の着地: 判断の記録 ADR-18 の発効（main 16ed6a2）。**便ア（便 126・行 `dy`・台帳 f2-648.178）の着地**（§0 の 前の便）。
- 並行の便: 便アとは `crates/folio/src/stamp.rs` で write-set が重なるので、便アの着地の後に 1 本で運ぶ（§0）。
- 本便の着地の後に席が見ること: 実の印は今古い（(a) の 3）ので、本便の着地の後に組む実の面の名札には添え書きが付く。次の周で --stamp を撃ち直して印を付け直すと消える（ADR-18 決定 (7) の順）。要件 FR18 の注と語彙の「天井の名札」の定義に添え書きの字を書き足す起草（次の要件書の版・持ち主の承認）。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "ea"
title = "判断の記録 ADR-18 決定 (6) の便イ（裁定 id = 台帳 f2-648 notes 2026-09-24 11:51 JST・案 a）: 面の天井の名札に、印の正本の要約値が今の正本と違えば「印の後に変わった所はまだ読まれていない」を添える。crates/folio/src/stamp.rs の marks が印の欄 sources も返し、crates/folio/src/face.rs の ceiling_stamp が天井の正本を読んで、門と印と同じ関数（crates/folio/src/gate.rs の sources_digest）で今の正本の要約値を測り、印の sources と違えば閉じ括弧の直後に添え書きを b 要素で置く（観点の 3 値のどれにも同じ・5 面で同じ字・小窓の本体は変えない）。印が無ければ今の未実施の形のまま測らない。測れなければ面は まだ分からない で書かない。名札は引き金の要約値と節点の数を読まない。歯は f127_ の 3 本（crates/folio/tests/badge.rs・正本の要約値の独立の物差しを yaml-rust2 と sha256sum で持つ）で、既存の歯 12 本は helper の put_mark が印の仮の sources を独立の物差しの値に置き換えることで本文不変のまま緑。面の凍結 fixture 7 本と部品目録は動かない。受付は便ア（行 dy・台帳 f2-648.178）の着地の後で、受付の時点の main で数え直す"
req = ["FR18", "FR20"]
section = "1"
write-set = ["crates/folio/src/face.rs", "crates/folio/src/stamp.rs", "crates/folio/tests/badge.rs"]
verify = ["cargo nextest run -p folio --test badge f127_", "cargo nextest run -p folio --test badge", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "f127_ の歯 3 本（4 観点とも合格の新しい印では添え書きが無く、観点が読まない rules.yaml を変えても無く、観点が読む srs.yaml を変えると 5 面の名札がどれも閉じ括弧の直後に「印の後に変わった所はまだ読まれていない」を持ち 5 面で同じ字／仮の sources の印で 3 値が 不合格・合格・まだ分からない・合格 の名札が添え書きつきの逐語で 1 度在る／観点の reads に写しに無い文書 graph を足すと folio face が まだ分からない で書かず、字「正本の要約値が測れない」と graph.yaml を出す）が緑、名札の歯の全部（今の 12 本を本文不変で含む 15 本）が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、folio check と folio schema --check と folio inject --check が着地の後の main で 0 を返す"
<!-- contracts:end -->
