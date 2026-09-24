# 設計: 便 122 — 置き場の憲法の値域が、道具を組み立てた値域の部分集合かを床で数え、条の値を置き場の値域で引く（FR25・ADR-16 決定 (2)(ウ) と (7) の ③）

- 要件: FR25（置き場の憲法の値域が、道具を組み立てた値域の部分集合かを数える・要件書 第 1.34 版＝版 B・起草・承認待ち）/ AC22（組み立てた値域の外の値を持つ置き場の憲法は「まだ分からない」になり、部分集合なら床が続く・同じ版）。どちらも main（c33ee44・第 1.33 版）の要件書にはまだ無い id である。**受付は版 B の着地の後。** それまでは契約表の req が main の要件書に解けず、器の表の検査が req-unresolved を返す（既知・版 B の着地で消える）。規範文はどれも変えない。
- 条: P-4.2（判定できないものは「まだ分からない」として表に出す）/ P-4.1（実行できなかった結果を異常なしとして扱わない）/ N-3.1（規則の例外機構を足さない＝値域を置き場ごとに広げる口を持たない）/ P-5.1（値域は型付きデータに置く）/ P-10.1（独立した凍結 anchor を 1 本以上持つ）/ P-10.2（生成物どうしの突き合わせを唯一の合格判定にしない）/ P-6.2（生成物を手で直さない＝組み立て時の導出は変えない）
- 出所: 判断の記録 **ADR-16**（発効 2026-09-23 17:39 JST・持ち主の承認・対話面 R-8・逐語「裁定は両方承認する」・裁定 id = 台帳 f2-648 notes 2026-09-23 17:39 JST）の決定 (2)(ウ)「憲法の値域は、組み立て時の導出のまま道具の側に残す（判断の記録 ADR-11 決定 (4)② を変えない）」「床に置き場の憲法の値域の節の各鍵が、組み立てた版の同じ鍵の部分集合かを数える口を足す」「部分集合でない鍵が 1 つでも在れば組み立て時の値域に無い値があるの「まだ分からない」にする（条 P-4.2）」と、決定 (7) の便の列の **③「値域の部分集合を床で数える（小・1 便）」**。文脈 (3)(ウ) の実測（床は条の値を組み立てた型で引くので、利用者の憲法が別の値を宣言して使うと「憲法の値域に無い」の違反になる・照合先は利用者の憲法ではなく道具を組み立てた folio2 の憲法）が、この便の直す先である。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `du` が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は手書きで 4 本。**新しい file は 2 本で、先頭に `+` を付けて宣言する**（歯の file 1・手書きの凍結 anchor 1）。どちらも既に在る dir（`crates/folio/tests/` と `tests/fixtures/check/`）に置き、**新しい dir は作らない**。**縮む file も消す file も無い**（床の凍結の場合の file は行数が変わらない）。`~` は使わない。
- 門: 本便は設計文書の正本（`design-intent/` の下）を 1 本も書き換えないので、天井の門の対象外である。起草役が write-set 4 本をそのまま `folio ceiling --gate --write-set …` に渡した実測は **0（通す・断りの字 = 設計文書の正本を書き換えない便）**（2026-09-24・本便の後の binary）。規則の表の開発規律行 D-12 は当たらない。
- 前の便: ADR-16 決定 (7) の順は ① → 版 B → ② → ③ → ④。① は便 117（行 `dp`・着地）、⑤ は便 119（行 `dr`・着地 main c33ee44）。② は便 121（起草中・別の起草役）。**base = main c33ee44。この契約の数はすべて base c33ee44 の実測（参考値）である**（規則の表の行 D-13）。
- 並行の便との重なり: `crates/folio/src/check.rs` は便 ④（delivery-123〜・起草中）の実測 patch も触る。④ が書き換えるのは要件書と語彙の最上位の節の床の定数の注 2 か所（生成区間の注から条 N-3 の id を外す）だけで、本便の書き換える箇所（頭の注・use の 1 行・check_dir の憲法の段・check_constitution・check_article_enums）とは 1 hunk も重ならない。便 ②（delivery-121）の write-set は起草中で、check.rs を含むかは起草役が確かめている。**write-set が check.rs で重なる便とは並べて運ばず、ADR-16 決定 (7) の順（② → ③ → ④）で 1 本ずつ運ぶ。受付の時点で ② が先に着地していたら、base を着地の sha に取り直す改訂を先に入れる**（§1 (i) の撤退条件 (3)）。本便は ②（列の根の表・始まりの凍結・`crates/folio/src/freeze.rs`・`crates/folio/src/lineage.rs`・判断の記録の欄の決まりの写し）と ④（骨格の命令・案内の 1 行・`crates/folio/src/note.rs`・`crates/folio/src/face_note.rs`）の file には踏み込まない。

## 1. 設計

### (a) いま起きていること（実測・base main c33ee44）

1. **憲法の値域は組み立て時に導出される。** 組み立ての script（`crates/folio/build.rs`）が folio2 の憲法の正本の値域の節（schema.enums・10 鍵）から閉じた一覧の型と、鍵の名と値の列の対の定数（ENUMS）を導出し、`crates/folio/src/constitution_enums.rs` が取り込む（便 49・ADR-11 決定 (4)②）。本便はこの導出を 1 字も変えない。
2. **床は置き場の値域の節を読まない。** `crates/folio/src/check.rs` の check_article_enums（便 55）は、条の値域を持つ欄 10 か所（条の tier と binds・規範文の pattern と strength・rationale の各行の kind・mechanism の kind と live と stage と polarity・retreat の kind）の値を、組み立てた型の from_name で引く。引けなければ種別 schema の違反 1 件（字 = 条 X の欄の値「v」が憲法の値域 schema.enums.鍵 に無い）。置き場の憲法の値域の節は、この検査では 1 度も読まれない。
3. **だから利用者の憲法の値域は効かない。** 起草役が design-intent の写しの値域 mechanism_live から M0 を外し（組み立てた版には在る値）、条 P-1 の機構の live を M0 にした写しに base の binary を撃つと、値域の違反は出ない（改憲の違反 N-4 の 1 件だけ）。逆に strength に may を足し、条 P-1.2 の strength を may にした写しでは、置き場の値域に在る値なのに値域の違反 1 件になる。どちらも、照合先が置き場ではなく組み立てた版であることの実例である（ADR-16 文脈 (3)(ウ)）。
4. **床のほかの箇所の値域の読み。** 条の値のほかに、組み立てた値域か置き場の値域を読む床の箇所は 3 つ在る。判断の記録の撤退条件の種類（`crates/folio/src/floor_adr.rs`・組み立てた型）・規則の表の行の stage（`crates/folio/src/rules.rs`・組み立てた型）・判断の記録と正本の突き合わせの retreat_kind（`crates/folio/src/link.rs`・置き場の値域の retreat_kind が判断の記録の欄の決まりの床の定数と長さ・字・並びまで一致するか）。面の生成器（`crates/folio/src/face_constitution_read.rs`）は置き場の値域が組み立てた版と集合で一致しなければ「組み立て直す」で断る。要件 FR25 の規範文は条の値だけを言うので、本便はこの 4 つを変えない（(i) の 2）。
5. **床の凍結の場合の 1 件が、組み立てた版の外の値を足している。** 凍結の場合の file（`tests/floor_cases.yaml`）の schema-amendment-complete は、土台の写しの値域 tier に値 maybe を足し、判断の記録で改訂を説明して凍結し、終了コード 0 を期待する。同じ値（共有の anchor の tier_new と tier_new_json）を、落ちることを期待する場合 4 件（schema-amendment-text-mismatch・schema-changed-without-record・schema-piggyback-other-field・schema-version-mismatch）も使う。
6. base の workspace の nextest は全部緑（参考値 792 本・base c33ee44・`cargo nextest run --workspace --no-tests=fail --no-fail-fast`）。folio2 自身の置き場への `folio check --dir design-intent` は 合格（違反 0・まだ分からない 0）。

### (b) 直す先 — 部分集合の数えと、置き場の値域で引くこと

**どの段で数えるか。** `crates/folio/src/check.rs` の check_dir が正本 7 file を読めた直後、憲法の検査（check_constitution）の直前に、新しい非公開の関数 place_range（同じ file）を 1 度呼ぶ。place_range は置き場の憲法の値域の節を読んで、鍵の名から値の列への表（同じ file の新しい型の別名 PlaceRange・値の列は file の順・同じ値は 1 つに）を返し、「まだ分からない」を報告に足す。**違反は出さず、ほかの検査を 1 つも止めない**（返った表を check_constitution に渡すだけで、判断の記録・凍結 anchor・参照 id ほかの段はこれまでどおり全部回る）。

**部分集合の式（鍵ごと・値の集合の比較・順は問わない）。** 置き場の値域の節の各鍵 k について、置き場の値の集合 S(k) と、組み立てた版の同じ鍵の値の集合 B(k)（定数 ENUMS の k の行・k が無ければ空集合）を比べ、S(k) ⊆ B(k) なら部分集合とする。値の並びと重複は数えない。組み立てた版の鍵が置き場に無いこと自体は部分集合を崩さないが、その鍵の条の値を引けないので次の表の 4 行目で扱う。

| 置き場の値域の節の形 | 報告に足すもの（字は `constitution.yaml: ` で始まる） | 返す表 | その鍵の条の値 |
| --- | --- | --- | --- |
| 鍵 k の値が文字列の一覧で、S(k) ⊆ B(k) | なし | k の値の列を入れる | 置き場の値域で引く |
| 鍵 k の値が文字列の一覧で、B(k) に無い値が在る（部分集合でない） | まだ分からない 1 件 = schema.enums.k: 組み立て時の値域に無い値がある（外の値を「」で括り・で繋いだ列・値域を置き場ごとに広げる口は無い・FR25） | k の値の列を入れる | 置き場の値域で引く |
| 鍵 k が組み立てた版に無い（部分集合でない） | まだ分からない 1 件 = schema.enums.k: 組み立て時の値域に無い値がある（組み立てた版に無い鍵・値域を置き場ごとに広げる口は無い・FR25） | 入れる（条の欄は k を引かないので効かない） | 当たらない |
| 組み立てた版の鍵 k が節に無い | まだ分からない 1 件 = schema.enums に鍵 k が無い＝条の k の値を置き場の値域で引けない（FR25） | 入れない | 数えない（黙る） |
| 鍵 k の値が文字列の一覧でない | まだ分からない 1 件 = schema.enums.k が文字列の一覧でない＝条の値を置き場の値域で引けない（FR25） | 入れない | 数えない（黙る） |
| 値域の節（schema.enums）が無いか表でない | まだ分からない 1 件 = schema.enums（置き場の憲法の値域の節）が表でない＝条の値を置き場の値域で引けない（FR25） | 空 | 10 か所とも数えない（黙る） |

- 「まだ分からない」は報告の測れない（pending）で出す＝読めたうえで比較元（組み立てた版の値域）が立たない。判定は `crates/folio/src/verdict.rs` の今の並びのまま（違反が在れば 不合格・無ければ まだ分からない・どちらも 合格 にしない）。読めない（unknown）で出さない理由は、読めない は違反より先に立つ判定で、置き場の中身を数えたうえでの違反（改憲の違反や置き場の値域に無い値）を隠してしまうからである。
- 部分集合でない鍵が在っても、その鍵の条の値は置き場の値域で引き続ける＝置き場の値域にも無い値は違反のままにする（部分集合でない鍵を丸ごと黙らせない）。組み立てた版の外で置き場の値域に在る値を条が使うと、値域の違反は出ず、その値の意味を式が持つ検査（規範文の strength と文末の一致 R-11）は組み立てた型で引けないので黙る。この 2 つを黙らせる代わりに、その鍵の「まだ分からない」が必ず立つ。
- 引けない鍵（表の 4〜6 行目）の条の値を数えないのは、置き場が宣言していない値域で合否を言えないからで（条 P-4.2）、その鍵の「まだ分からない」が必ず立つ。空の値域として全部を違反にする形は採らない（(d) の 3）。
- 値域を置き場ごとに広げる口（旗・設定・既定に倒れる枝）は持たない（条 N-3.1）。字「値域を置き場ごとに広げる口は無い」はその断りである。

**条の値を「置き場の値域で引く」とは何が変わるか。** check_article_enums の引き方だけが変わる。今は欄ごとに組み立てた型の from_name を呼ぶ判定の関数を渡しているが、本便の後は place_range が返した表を 1 つ受け取り（引数を 1 つ足す・check_constitution も同じ表を受けて渡す）、欄の値が表の同じ鍵の値の列に在るかで判定する。鍵が表に無ければ黙る。違反の字（条 X の欄の値「v」が憲法の値域 schema.enums.鍵 に無い）と種別 schema は 1 字も変えない＝便 55 の歯 6 本（`crates/folio/tests/check.rs` の check_constitution_enum_ で始まる歯）はそのまま緑。組み立てた型はそのまま残り、規範文の strength と文末の一致（check_statement_polarity）・判断の記録・規則の表・注入・面の生成器は今までどおり組み立てた型を使う。folio2 自身の置き場では S(k) = B(k) なので、どの条の値も同じ判定になる。

### (c) 歯（新しく 4 本・置き場は新しい file `crates/folio/tests/` の下の constitution_range.rs）

関数名は f122_ で始める（verify の絞り込みの語・base で `git grep -n 'fn f122_'` は 0 件）。**凍結 anchor（P-10.1）** は新しい file `tests/fixtures/check/` の下の enum-range-anchor.yaml の 1 本で、手で書いた、この版の folio を組み立てた憲法の値域 10 鍵（block の形・1 行 1 値・鍵は file の順）である。組み立ての script からも床からも独立で、歯はこの file の各行を 4 字下げて写しの値域の節の中身と差し替える。

**歯の土台。** 一時 dir に実の `design-intent/` の写しと、その親の contracts/ に器の導出 file の写し schema.toml を置き、git の 1 commit にしてから、写しの `constitution.yaml` の字面に変異を当てて `folio check` を撃つ（`crates/folio/tests/check.rs` の Work と同じ形・一時 dir は消す）。値域の節は憲法の改訂の差分の範囲（schema）に入るので、値域を変える変異では改憲の違反（種別 N-4）がちょうど 1 件出る。歯は N-4 がちょうど 1 件であることを確かめてから、それを除いた違反の行と、標準エラーの「まだ分からない」の行を全部数える。

1. **部分集合なら床が続き、条の値は置き場の値域で引かれる。** 値域 mechanism_live を M0 を外して並びも逆にした一覧にする → N-4 のほかに違反 0・まだ分からない 0・判定の行は 不合格（違反 1・まだ分からない 0）。続けて条 P-1 の機構の live を M0 にする → N-4 のほかの違反はちょうど 1 行で、字が [schema] constitution.yaml: 条 P-1 の mechanism.live の値「M0」が憲法の値域 schema.enums.mechanism_live に無い と一致・まだ分からない 0・終了コード 1。**base では 2 つ目で値域の違反が出ず落ちる＝RED。**
2. **組み立てた値域の外の値は「まだ分からない」で合格にならない。** 値域 strength に may を足す → N-4 のほかに違反 0・まだ分からない はちょうど 1 行で、字が constitution.yaml: schema.enums.strength: 組み立て時の値域に無い値がある（「may」・値域を置き場ごとに広げる口は無い・FR25）と一致・判定の行は 不合格（違反 1・まだ分からない 1）・終了コード 0 でない。続けて条 P-1.2 の strength を may にする → 値域の違反は出ず、まだ分からない は同じ 1 行のまま。続けて条 P-2.1 の strength を never-heard にする → N-4 のほかの違反はちょうど 1 行（条 P-2 の statements の P-2.1 の strength の値「never-heard」が憲法の値域 schema.enums.strength に無い）・まだ分からない は同じ 1 行・判定の行は 不合格（違反 2・まだ分からない 1）。**base では まだ分からない が出ず、may が値域の違反になって落ちる＝RED。**
3. **引けない鍵は「まだ分からない」で、その鍵の条の値は数えない。** 別々の写し 4 つ = 組み立てた版に無い鍵 colour を足す・鍵 polarity の行を消す・polarity の値を一覧でなく字 fail-closed にする・値域の節を丸ごと消す。それぞれ (b) の表の字の「まだ分からない」の行が在り、違反の行に字 が憲法の値域 schema.enums. を含むものが 1 つも無く（条は fail-closed を使い続けている）、終了コードが 0 でない。**base では まだ分からない の行が無く落ちる＝RED。**
4. **凍結 anchor と組み立てた値域が一致し、外の値は鍵ごとに「まだ分からない」になる。** 写しの値域の節の中身を凍結 anchor に差し替える → 判定の行は 合格（違反 0・まだ分からない 0）・終了コード 0（中身は実の値域と同じなので改憲の違反も出ない）。anchor の全部の鍵の末尾に値 zz-outside を 1 つずつ足して差し替える → まだ分からない の行の列が、anchor の鍵の順に 1 鍵 1 行の schema.enums.鍵: 組み立て時の値域に無い値がある（「zz-outside」・…）と一致（鍵の数は anchor から数える）・値域の違反の行は無い・終了コード 0 でない。**base では 2 つ目で落ちる＝RED。** 組み立てた値域から値を外すか名を変える改訂は、この歯の 1 つ目を落とす（ADR-16 の帰結「値を外すか名を変えると全利用者の床が まだ分からない に落ちる」を folio2 の側で見える形にする）。値を足す改訂はこの歯を落とさない。

歯の効き（起草役が `crates/folio/src/check.rs` に変異を 1 つずつ当てて、f122_ の 4 本を撃って測った・base c33ee44 に本便の patch・script は d122-draft-mut.py・逐語の記録は d122-draft-mut.out）:

| 当てた形 | 落ちる歯 |
| --- | --- |
| 本便の形 | なし（4 本とも緑） |
| M1 条の値を組み立てた型で引く（base の引き方） | 1・2 |
| M2 外の値を まだ分からない にしない | 2・4 |
| M3 組み立てた版に無い鍵を黙る | 3 |
| M4 節に無い鍵を黙る | 3 |
| M5 文字列の一覧でない鍵を空の値域として引く | 3 |
| M6 値域の節が無いのを黙る | 3 |
| M7 部分集合でなく一致を求める | 1 |
| M8 まだ分からない を読めない（unknown）で出す | 2 |
| M9 外の値を違反にする | 2・4 |
| M10 並びまで見る（組み立てた版と同じ位置の値だけを認める） | 1 |
| M11 外の値を持つ鍵を返す表に入れない（その鍵の条の値を数えない） | 2 |

### (d) 採らなかった形

1. **値域を実行時に置き場の憲法から読み、組み立てた型を外す。** ADR-16 案（値域を実行時に利用者の憲法から読む）で退けた形で、面の名札の網羅と、値の意味を持つ式（R-11）の確かさを失う。本便は組み立てた型を残し、引き方だけを置き場の表にする。
2. **部分集合でない鍵を違反にする。** 条 P-4.2 と FR25 の規範文は「まだ分からない」を求める。違反にすると、利用者の中身の誤りと道具の値域の不足が同じ字で区別できなくなる。
3. **引けない鍵を空の値域として、その鍵の条の値を全部違反にする。** 置き場が値域を宣言し損ねた 1 か所が、条の数だけの違反に化ける。合否を言えないものは「まだ分からない」1 件にまとめる（M5 がこの形で、歯 3 が拾う）。
4. **床の凍結の場合 schema-amendment-complete の期待を終了コード 2 に替え、緑の場合を 1 件足す。** 場合の数（expected_cases）が変わり、改訂の記録の緑の経路という場合の意味が別の話（値域の外の値）に替わる。本便は共有の値を組み立てた値域の中の変更（並びの入れ替え）にして、5 件の意味と期待を保つ（(f)）。

### (e) 大きさ・verify と done の対応

1. **write-set の印。** 新しい file 2 本に `+`（`crates/folio/tests/` の下の constitution_range.rs・`tests/fixtures/check/` の下の enum-range-anchor.yaml）。書き換える 2 本（`crates/folio/src/check.rs`・`tests/floor_cases.yaml`）は印なし。`-`（行が減る file）・`~`（着地で消える file）は当たらない。新しい dir は作らない。
2. **余地（CapHeadroom）。** 測るのは `crates/folio/src/` の下の印なしの .rs の 1 本だけ（新しい .rs は src に無い）。測り方は各行の字数を 120 で割って切り上げ（空行は 1）、全行で足す（`wc -l` ではない・script は (h)）。size S の見積は 1 file あたり 100。

| file | base の正規化行数（参考値） | 余地 = 1500 − 正規化行数 | 本便の後（参考値） |
| --- | --- | --- | --- |
| `crates/folio/src/check.rs` | 889 | 611 | 950 |

   歯の file は src の外なので余地を測らない（参考に、新しい歯の file は同じ式で 398 行・参考値）。
3. **size は S。** 変える src は 1 本（増える行は参考値 61）。
4. **verify は 2 行**で、done の 2 つの塊と 1 対 1 に揃える。
   1. `cargo nextest run -p folio --test constitution_range f122_` = (c) の新しい歯 4 本。
   2. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** verify が `--test` で名指す歯の file は constitution_range の 1 本で、write-set に在る。絞り込みの語 f122_ を関数名に持つ file は、その 1 本だけである（src には置かない）。床の凍結の場合（`crates/folio/tests/floor_cases.rs`）と便 55 の歯（`crates/folio/tests/check.rs`）は本文を変えないので write-set に入れず、verify でも名指さない＝共通の検証（`.vessel.toml` の common-verify の workspace の nextest）が走らせる。

### (f) 既存の歯のうち落ちるもの・凍結 anchor が動くか・直し方

起草役が、本便の src（`crates/folio/src/check.rs`）だけを当てて workspace の nextest を撃つと、**落ちる既存の歯は 1 本**（参考値・base c33ee44 の 792 本のうち）で、`crates/folio/tests/floor_cases.rs` の floor_cases_all_pass_with_folio の中の場合 schema-amendment-complete（期待 0・実 2・字 = 凍結しない — 違反 0 件・まだ分からない 1 件を直してから）である。土台の写しに足した値 maybe が組み立てた版の外なので、(b) のとおり「まだ分からない」が立って凍結を断る。これは FR25 が求める振る舞いそのもので、場合の前提（値域に新しい値を足す改訂を記録で説明すれば緑）が、組み立てた版の外の値を足す限り成り立たなくなった。

- **直し方（`tests/floor_cases.yaml` の 4 行・行数は変わらない）。** 共有の anchor の tier_new を並びを入れ替えた [never, ask-first, always] に、tier_new_json を同じ並びの json の字に替え、判断の記録の fixture adr5_schema の title と decision の字を「段の値域の値の並びを替える」に替える（値 maybe の字は file から消える）。並びの入れ替えも schema 節の改訂なので、改訂の記録の照合（欄単位の対・一覧は json の 1 値）は同じ式を通り、5 件とも期待（終了コード・期待の字）を変えずに通る（本便の後の木で 142 件が期待どおり・参考値）。場合の数 expected_cases は 142 のまま。
- この file は床の凍結の場合の置き場（凍結 fixture）で、本便が動かす凍結の材料はこの 4 行だけである。凍結の土台（`tests/fixtures/floor_base/`）と、節点の要約値の anchor・生成区間の写し・判断の記録の欄の決まりの写しは 1 byte も動かない（本便は `design-intent/` も `tests/fixtures/` の既存の file も書き換えない）。
- 便 55 の歯 6 本（`crates/folio/tests/check.rs` の check_constitution_enum_ で始まる歯）は、どの変異の値も組み立てた版にも置き場の値域にも無いので、違反の字と件数が変わらず緑のまま。folio2 自身の置き場の合格は同じ file の check_canonical_design_intent_passes が見る。
- **folio2 自身の結果は変わらない**（ADR-16 撤退条件 (2) の当て先）。本便の後の木で、`folio check --dir design-intent` は 合格（違反 0・まだ分からない 0）のまま・`folio schema --dir design-intent --check` は全 file 一致・`folio derive --dir design-intent --out ../contracts --check` は 0・`folio build --write` の出力は本便の前後の binary で `diff -r` が差 0（参考値 23 file）。組み立てた値域（`crates/folio/build.rs` と `crates/folio/src/constitution_enums.rs`）・列の根の表・folio2 の行 R-16 の値は触らない。歯 4 の 1 つ目が、組み立てた値域と手書きの anchor の一致を見る。
- 本便の後の木で workspace の nextest は全部緑（参考値 796 本 = base c33ee44 の 792 + 新しい歯 4）・clippy 0 警告。

### (g) 門（規則の表の開発規律行 D-12）

本便は `design-intent/` の下を 1 本も書き換えないので天井の門の対象外で、実測は 0（通す）（§0 の 門）。

### (h) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草役の実測 patch は `~/.local/share/folio2/handoff-2026-09-24/d122-measured.patch`（base c33ee44 に `git apply --check` が通る・repo には入れない）。起草の記録は同じ dir の d122-draft.md、変異の script は d122-draft-mut.py（使い方: `python3 d122-draft-mut.py <写しの repo> <CARGO_TARGET_DIR>`）、その出力は d122-draft-mut.out、行数の script は便 119 の d119-draft-lines.py（同じ式）。

1. base の写し: `git worktree add --detach <写し> c33ee44`。
2. RED: 歯の file と凍結 anchor の 2 本だけを当てて `cargo nextest run -p folio --test constitution_range f122_ --no-fail-fast` → 4 本とも落ちる。
3. 落ちる既存の歯: patch のうち `crates/folio/src/check.rs` だけを当てて workspace の nextest → (f) の 1 本だけが落ちる。
4. 全部: patch の全部を当てて `cargo nextest run --workspace --no-tests=fail --no-fail-fast`（全部緑）・`cargo clippy --workspace --all-targets -- -D warnings`（0 警告）・`folio check --dir design-intent`（合格）・`folio schema --dir design-intent --check`・`folio derive --dir design-intent --out ../contracts --check`（0）。
5. 出力の差: base と後の binary で `folio build --dir design-intent --out <別々の置き場> --write` を撃ち、`diff -r` が差 0。
6. 変異: (c) の表。
7. 門: `folio ceiling --gate --write-set <write-set の 4 本（接頭辞を剥がす）>`。
8. 余地: `python3 d119-draft-lines.py crates/folio/src/check.rs`。

### (i) 本便が運ばないもの・言えないこと・まだ分からない点・撤退条件

1. **運ばないもの。** 要件書・判断の記録・憲法・規則の表・語彙の字（版 B の AC22 の固定の材料の字〔まだ置いていない・置き場は便で決める〕を、本便の歯の file と凍結 anchor の名に揃えるのは、着地の後の要件書の版・席の起草・持ち主の承認）。組み立ての script と組み立てた値域。面の生成器（置き場の値域が組み立てた版と集合で一致しなければ「組み立て直す」で断る形を含む・M3 の外）。列の根の表と始まりの凍結（便 ②）。骨格の命令と案内の 1 行（便 ④）。外部 crate。
2. **言えないこと — 条の値のほかの値域の読み。** (a) の 4 の 3 か所は本便の後も組み立てた型か床の定数との一致で数える。判断の記録の撤退条件の種類と規則の表の行の stage は、置き場の値域が部分集合でも組み立てた版の値で引く。判断の記録と正本の突き合わせは、置き場の値域の retreat_kind が組み立てた版と長さ・字・並びまで一致しなければ種別 adr の違反を出す（歯 4 の 2 つ目で起草役が観測・本便の歯はその行を数えない）。したがって「部分集合なら床が続く」は条の 10 欄について言え、retreat_kind を狭めたか並べ替えた置き場はこの別の違反で落ちる。M3 の骨格は組み立てた版の値域をそのまま書く（ADR-16 撤退条件 (1) の「骨格が組み立てた版の値域で書かれている間は値域のずれは起きない」）ので M3 の判定点には効かないが、利用者が retreat_kind を狭めたときにどちらへ揃えるかは本便では言えない（席への申し送り）。
3. **言えないこと — 意味を持つ式の黙り。** 組み立てた版の外で置き場の値域に在る値を条が使うと、規範文の strength と文末の一致（R-11）はその規範文を数えない。その鍵の「まだ分からない」が同時に立つので合格にはならないが、R-11 の違反が隠れているかどうかは言えない。
4. **まだ分からない — 版 B の着地。** 本便の req の FR25 は版 B（承認待ち）の id で、main の要件書に解けない。版 B の文面（FR25 の規範文と AC22）が承認の過程で変わったら、(b) の表の字と歯 2・歯 4 の期待を直してから受付に出す。
5. **撤退条件。** (1) 本便の後に (f) の 1 本のほかに既存の歯が 1 本でも落ちたら、その歯の本文を直さずに止めて席へ返す。(2) 本便の後に folio2 自身の置き場の床の結果（合否・違反と「まだ分からない」の件数）か `folio build` の出力が 1 byte でも変わったら、止めて席へ返す（ADR-16 撤退条件 (2)）。(3) 受付の時点の main で `crates/folio/src/check.rs` の check_dir の憲法の段・check_constitution・check_article_enums の周りが書き換わっていたら（便 ② の着地を含む）、base を取り直して余地と歯の効きを測り直してから運ぶ。(4) 受付の時点の main で `tests/floor_cases.yaml` の共有の anchor の tier_new か tier_new_json の字が base と違っていたら、(f) の直し方を測り直してから運ぶ。(5) 版 B が FR25 を持たずに着地したら受付に出さずに park する。

## 2. 範囲

- 入れる: `crates/folio/src/check.rs` の頭の注の 1 行の書き直し（2 行に）・use の 1 行（HashMap）・check_dir の憲法の段の 1 行を 2 行に（place_range を呼び、表を渡す）・新しい型の別名 PlaceRange と新しい関数 place_range・check_constitution と check_article_enums の引数に表を 1 つ足し、check_article_enums の引き方を表に替える（違反の字と種別は不変）。新しい歯の file（f122_ の 4 本）と手書きの凍結 anchor 1 本。`tests/floor_cases.yaml` の共有の anchor 2 つと判断の記録の fixture の字 2 つ。
- 入れない: 組み立ての script と `crates/folio/src/constitution_enums.rs`・規範文の strength と文末の一致・判断の記録の床（`crates/folio/src/floor_adr.rs`・`crates/folio/src/adr.rs`・`crates/folio/src/link.rs`）・規則の表の床（`crates/folio/src/rules.rs`）・面の生成器（`crates/folio/src/face_constitution_read.rs` ほか）・凍結の土台と生成区間と写し・要件書と判断の記録と憲法と規則の表と語彙・天井・列の根と凍結（便 ②）・骨格（便 ④）・新しい dir・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| range | 置き場の値域の読みと部分集合の数え | `crates/folio/src/check.rs` の新しい関数 place_range と型の別名 PlaceRange（check_dir の憲法の段から 1 度呼ぶ） |
| lookup | 条の値の引き方 | `crates/folio/src/check.rs` の check_article_enums（引数に表を 1 つ・判定を表の値の列に） |
| anchor | 凍結 anchor | `tests/fixtures/check/` の下の enum-range-anchor.yaml（手書き・組み立てた値域 10 鍵） |
| cases | 床の凍結の場合 | `tests/floor_cases.yaml` の共有の anchor tier_new・tier_new_json と fixture adr5_schema の字 |
| teeth | 歯 | 新しい歯の file の f122_ の 4 本 |

## 4. 検査（歯）

§1 (c)(f) と (e) の 4 のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate は増やさない。新しい dir は無い。host に要る命令は無い。
- 前提の着地: 要件書の版 B（第 1.34 版・FR25 / AC22）。ADR-16 決定 (7) の順で便 ②（delivery-121）の後。
- 並行の便: 便 ②（delivery-121・起草中）と便 ④（delivery-123〜・起草中）は `crates/folio/src/check.rs` を触りうる・触る。hunk は重ならないが write-set が重なるので、ADR-16 決定 (7) の順に 1 本ずつ運ぶ（§0 の 並行の便との重なり）。
- 本便の着地の後に席が見ること: 版 B の次の要件書の版で AC22 の固定の材料の字を本便の歯の file と凍結 anchor の名に（(i) の 1）。retreat_kind の並びの一致を部分集合に揃えるかどうか（(i) の 2）。
- 後の便への申し送り: folio2 の憲法の値域から値を外すか名を変える改訂（判断の記録と持ち主の承認が要る）は、凍結 anchor `tests/fixtures/check/enum-range-anchor.yaml` と、`crates/folio/tests/constitution_range.rs` の変異の当て先の行（値域の 3 行・条 P-1 の機構・条 P-1.2 と P-2.1 の規範文の頭）を同じ便で直す。値を足す改訂は anchor の 1 つ目の比較を落とす（anchor が実の値域と一致しなくなる）ので、同じく anchor に値を足す。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "du"
title = "判断の記録 ADR-16 決定 (2)(ウ) と (7) の ③（裁定 id = 台帳 f2-648 notes 2026-09-23 17:39 JST）の 1 便: 置き場の憲法の値域の節の各鍵が、道具を組み立てた版の同じ鍵の値の部分集合かを床で数え、条の値を置き場の値域で引く。crates/folio/src/check.rs の check_dir が正本を読めた直後・憲法の検査の直前に新しい関数 place_range を 1 度呼び、鍵ごとに値の集合を比べる（順と重複は問わない）。部分集合でない鍵（組み立てた版に無い値・組み立てた版に無い鍵）は鍵ごとに字 組み立て時の値域に無い値がある の まだ分からない 1 件、組み立てた版の鍵が節に無い・値が文字列の一覧でない・値域の節が表でない も まだ分からない 1 件（測れない＝違反が在れば不合格・無ければ まだ分からない・合格にしない）で、違反は出さずほかの検査を止めない。check_article_enums は組み立てた型の代わりに place_range が返した表で条の値域の欄 10 か所を引き、置き場の値域に無い値を今と同じ字と種別 schema の違反にし、引けない鍵の欄は黙る。値域を置き場ごとに広げる口は持たない。組み立て時の導出（build.rs・constitution_enums.rs）と、規範文の strength と文末の一致・判断の記録と規則の表の床・面の生成器は変えない。folio2 自身の床の結果と配信の組み立ての出力は変わらない。歯は新しい crates/folio/tests/constitution_range.rs の f122_ の 4 本と手書きの凍結 anchor tests/fixtures/check/enum-range-anchor.yaml（組み立てた値域 10 鍵）。落ちる既存の歯 1 本（床の凍結の場合 schema-amendment-complete が組み立てた版の外の値 maybe を足していた）は tests/floor_cases.yaml の共有の値を並びの入れ替えに替えて直す（場合の数と期待は不変）。受付は要件書の版 B（FR25）の着地と便 ② の後"
req = ["FR25"]
section = "1"
write-set = ["crates/folio/src/check.rs", "+crates/folio/tests/constitution_range.rs", "+tests/fixtures/check/enum-range-anchor.yaml", "tests/floor_cases.yaml"]
verify = ["cargo nextest run -p folio --test constitution_range f122_", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "f122_ の歯 4 本（値を 1 つ外して並びを逆にした値域で まだ分からない も値域の違反も出ず、外した値を条が使うとその条の値が値域の違反ちょうど 1 件／組み立てた値域の外の値 may を足すと鍵 strength の まだ分からない ちょうど 1 件で合格にならず、may を条が使っても値域の違反にならず、置き場の値域にも無い値の条は違反のまま／組み立てた版に無い鍵・節に無い鍵・一覧でない鍵・値域の節の不在の 4 通りでそれぞれ まだ分からない が出てその鍵の条の値を数えない／手書きの凍結 anchor に差し替えた写しが 合格 で、anchor の全部の鍵に外の値を足すと鍵ごとに まだ分からない 1 件）が緑、clippy が 0 警告で、workspace の nextest が全部緑（床の凍結の場合 142 件・便 55 の値域の歯・folio2 自身の置き場の合格の歯を含む）で CI が通り、着地の後の main で folio check --dir design-intent が 合格（違反 0・まだ分からない 0）を返す"
<!-- contracts:end -->
