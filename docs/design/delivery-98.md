# 設計: 便 98 — 天井の材料の束を、観点が読むと宣言した最上位の節まで絞る（FR17）

- 要件: FR17（天井の材料の束を観点ごとに組む・第 1.28 版の規範文は「その観点が読むと宣言した節まで絞った正本の写し（基準）」と書く）
- 条: P-3.1（機械で決定的に検査できる項目は床に置く）/ P-4.1（検査・生成が実行できなかった結果を異常なしとして扱わない）/ P-4.2（判定できないものは まだ分からない として表に出す）/ P-5.1（規則・閾値・型の一覧は型付きデータに置く）/ P-6.2（生成物を手で直さない）/ P-10.1（独立した凍結 anchor を 1 本以上持つ）/ P-10.2（生成物どうしの突き合わせを唯一の合格判定にしない）/ P-10.3（anchor が維持できなくなった検査の結果は まだ分からない に落とす）/ N-3.1（規則の例外機構を足さない）
- 出所: 判断の記録 ADR-13 決定 (5)（天井の束を影響集合で切らない。束は観点が宣言する読む欄まで絞ったうえで丸ごと渡す）・決定 (10)（絞るとき、束の凍結 anchor を folio の実装に依らずに作り直す）・決定 (16) の 4 本目。設計ノート docs/design/delivery-97.md §1 (d)(e)(f)(g)(h)(i)（便 98 の設計は便 97 の契約に同梱されていた・本便はそれを起こしたもの）。持ち主の裁定 2026-09-22 20:52 JST（一括 12 の問 5・逐語「全部承認する」）= 束は最上位の章まで絞る（行の中の欄まで降りない）。
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 cy が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は手書き（新しい file は 1 本も無い・縮む file も無い・新しい dir は作らない）。
- 門: 本便は design-intent の下の正本を 1 file も書き換えない（読むだけ）ので、天井の門の対象外である。**起草役が本便の write-set 15 本をそのまま渡して folio ceiling --gate を実測し、0（通す・断りの字は 設計文書の正本を書き換えない便）を確かめた**（2026-09-22・base main 278ba59）。
- 前の便: 便 97（行 ct）は着地済み（main 420d910）で、独立の script `tests/fixtures/ceiling/bundle-anchor.py` と凍結 anchor `tests/fixtures/ceiling/bundle-anchor.txt` は既に main に在る。本便の base は **main 278ba59**（一括 12 = 天井の正本 v0.11 と要件書 v1.28 の発効）で、便 97 が挙げた 2 つの前提（🔴 1 = 読む欄の宣言を 8 対広げる・🔴 2 = FR17 の改訂）は **どちらも着地済み**である。
- 並行の便との重なり: **便 102（天井の正本の版上げ・読む文書に graph.yaml を足す便）と `crates/folio/src/bundle.rs` が重なる**（便 102 は同じ file の面の名の閉じた一覧 FACE_NAMES 9 を 10 にする見込み）。**器が順に運ぶ**。どちらが先でも、後の便が凍結 anchor `tests/fixtures/ceiling/bundle-anchor.txt` と所見 fixture 10 本の要約値を組み直す（束の中身が変わるため）。本便は FACE_NAMES にも床の定数 DOCUMENT_IDS（`crates/folio/src/ceiling.rs`）にも触らない。

## 1. 目的と中身

天井の束はいま、観点が読む文書の正本を **byte のまま丸ごと**写す。本便は、その写しを **観点が読むと宣言した最上位の節（と骨格）まで絞る**。落とした節は黙らずに束の中で名指す。凍結 anchor は便 97 の独立の script を絞った束に当てて組み直す。design-intent の下は 1 file も書き換えない。

### (a) 実測（2026-09-22・base main 278ba59・天井の正本 v0.11）

**数えは 2 つの実装で出して突き合わせた。** 1 つ目は節の範囲を先に作る向き、2 つ目は各行の持ち主の節を決める向きで、別々に書いた。当てた先は 実の正本（4 観点 × 宣言の doc）・凍結の土台・過去の全 25 周の束の sources で、**突き合わせ 2,144 対・食い違い 0 件**。食い違いが出た 2 点は (b) の規則 3・規則 4 として設計に入れた（下記）。数えの script は `~/.local/share/folio2/handoff-2026-09-22/d98/` に置いた（再実行できる）。

**src と歯の余地**（幅 120 で正規化＝全行 + 各行の ceil(len/120) − 1・上限 1,500・base main 278ba59）。

| file | 正規化の行 | 余地 | 本便での役 |
| --- | --- | --- | --- |
| crates/folio/src/bundle.rs | 539 | **961** | 絞る口・骨格の閉じた一覧・落とした節の知らせ |
| crates/folio/tests/bundle.rs | 718 | 782 | 歯 7 本と、既に在る凍結の期待の組み直し |
| crates/folio/tests/findings.rs | 1,264 | **236** | 歯 1 本・反証の束の凍結 anchor の組み直し・注釈の行を読み飛ばす枝 2 か所 |

**触る src は bundle.rs 1 本で、余地 961 は M の見積 300 を上回る。** crates/folio/tests/findings.rs の余地は 236 しか無いので、そこへ置くのは 30 行以内に収める（見積は (f) の 25 行）。

**束の byte**（25 周目の束を土台に、v0.11 の宣言で絞ったときの大きさを測った）。

| 観点 | 束 前 | 束 後 | 割合 | うち sources 前 | sources 後 |
| --- | --- | --- | --- | --- | --- |
| 忠実さ | 1,689,669 | 1,569,021 | 92.9% | 609,617 | 488,969（80.2%） |
| 読みやすさ | 1,716,830 | 1,572,529 | 91.6% | 620,451 | 476,150（76.7%） |
| 整合 | 1,739,492 | 1,659,035 | 95.4% | 643,058 | 562,601（87.5%） |
| 実態 | 1,653,680 | 1,478,368 | 89.4% | 573,987 | 398,675（69.5%） |
| 合計 | 6,799,671 | 6,278,953 | **92.3%** | 2,447,113 | 1,926,395（78.7%） |

**字数は目的ではない**（持ち主の裁定・ADR-13 決定 (0)）。束の全体では 7.7% しか減らない（束は面の HTML が大半を占めるため）。本便の効き目は雑音を落とすこと（精度）にある。設計ノート docs/design/graph-and-incremental-ceiling.md §0.1 の表が書く「100% → 39.6%」は、束ではなく sources だけを行の中の欄まで降りて測った数で、束の数ではない（便 97 の 🔴 4・一括 12 で直した）。

**精度の実測（いちばん重い数）。** 過去の周の所見の根拠（evidence）は、床（`crates/folio/src/findings.rs` の verbatim）が **束の sources/ の下の 1 行の中に byte 列として在ること**を照合する。絞ると、落とした節に在った根拠は照合に落ちる＝観点が正しい所見を立てても床が 根拠が正本に無い と言う。過去の周の所見 file を全部読み、**v0.11 の宣言で絞ったとき**に根拠が束の外に出る件数を数えた。

| 窓 | 所見の根拠 | 絞った束の外 |
| --- | --- | --- |
| 直近 10 周（16〜25 周） | 171 | **0** |
| 便 97 が測った窓（14〜23 周） | 183 | **0** |
| 全 25 周 | 627 | 17 |

**全 25 周の 17 件は 1〜13 周に全部ある**（1 周 1・2 周 3・3 周 1・5 周 2・6 周 1・7 周 1・9 周 2・10 周 2・11 周 2・12 周 1・13 周 1）。その時期の読む欄の宣言は今より狭く、一括 12 が広げた 8 対がまだ無かった。**14 周目以降は 1 件も落ちない**（14〜25 周の 12 周・根拠 210 件で 0 件）。便 97 が測った 17 件（9.3%）は一括 12 の宣言の是正で消えており、本便は **前提がそろった状態で着地する**。

**宣言に在るが正本に無い節**（その doc のどの file にも無い節）は、**実の正本では 0 件**（4 観点・宣言の対 29・欄の名 80 を全部当てた）。凍結の土台では 2 件（読みやすさ の index.yaml の sections・整合 の rules.yaml の rows）出る。

### (b) 絞る規則（採る案）

**最上位の節（欄）の単位で切る。行の中の欄には降りない。** 切る単位は行で、残す行は正本の byte のまま・正本の順のまま写す。規則は 4 つ。

| # | 規則 |
| --- | --- |
| 1 | **残すのは ① その観点の reads が挙げた節（`articles.plain` なら `articles` の節ぜんぶ）② 骨格の 6 語（meta・id・title・status・date・schema）③ file の頭（最初の節より前の行）** |
| 2 | **最上位の節の始まりは 列 0 の `<名>:` の行だけ。列 0 の `- ` で始まる行は直前の節の値の続きであって、新しい節ではない** |
| 3 | **注釈と空行の連なりは、直後に最上位の節が来るならその節へ寄せる。来ないなら（＝ file の末尾）直前の節へ寄せる** |
| 4 | **生成区間（`# folio:schema:begin` から `# folio:schema:end` まで）は 1 つの塊として、その中の節と一緒に残す** |

規則 1 の骨格の理由: `meta` は版、判断の記録は `id`・`title`・`status`・`date` が最上位の欄なので落とすとどの判断か分からない。`schema`（生成区間・欄の決まり）は過去に 止める を 4 件生んだ場所。**骨格の一覧は実装の型付きの定数に置く**（`crates/folio/src/bundle.rs` の 6 語の閉じた一覧・P-5.1）。その写しを設計文書の置き場へ導出するか（P-5.6）は便 97 の 🔴 3 のまま本便では決めない（決めるなら天井の正本の版上げを伴うので、便 102 と同じ承認に載る）。

規則 2 の理由: 束が写す正本でこの形（列 0 の `- `）を持つのは 4 本（`srs.yaml` の figures と `adr/ADR-4.yaml`・`ADR-5.yaml`・`ADR-7.yaml` の figures・起草役が design-intent の下を全数走査して確かめた。`anchors/constitution-v1.0.yaml` も同じ形だが束の読む文書の一覧に無い）。この 1 文が無いと、列 0 の連なりの先頭の欄の名（`id`）を節の名と読み、`id` が骨格に在るために figures の節が丸ごと残る。**凍結の土台 `tests/fixtures/ceiling/bundle/source/` の 8 本には列 0 の `- ` が 1 行も無いので、土台だけを見る歯ではこの誤りを捕まえられない**（歯 6 は実の正本に当てる）。

規則 3 と規則 4 は、**起草役の 2 つの実装が食い違った 2 点**である。どちらも便 97 の設計には書かれていなかった。

- 規則 3 が無いと、file の末尾の注釈の連なりがどの節にも寄らずに落ちる。実の正本では `# folio:schema:end` がこれに当たり、**写しに開きの印だけが残る**（ceiling.yaml・index.yaml・intake.yaml・srs.yaml・vocabulary.yaml の 5 本が末尾に閉じの印を持つ）。
- 規則 4 が無いと、閉じの印が **次の節に寄ってしまい**、その節が宣言に無い観点では印だけが落ちる。実の正本で生成区間を持つ写しは 4 観点で 25 対あり、規則 4 が無いと **6 対で閉じの印だけが落ちる**（`adr/schema.yaml` が 整合 と 実態 の 2 対・`design-note/schema.yaml` が 4 観点の 4 対）。規則 4 を入れると **25 対とも開きと閉じが 1 つずつ残る**（起草役が実測）。生成区間に入る最上位の節は **9 file とも `schema` の 1 つだけ**なので、規則 4 がほかの節を巻き込むことは無い（全数で確かめた）。

**退けた案 1: 行の中の欄まで降りる。** sources はさらに縮むが、便 97 の実測で根拠の落ちが増える（当時の宣言で 17 件 → 25 件）。加えて、行の中の欄の多くは 1 行の flow の表（`- {id: P-1.1, pattern: ubiquitous, strength: must, text: …}`）で、その一部だけを落とすには行を組み直すしかない。組み直すと byte が変わり、床の根拠の逐語の照合（1 行の中の byte 列）が総崩れになる。**逐語の照合を守る限り、切る単位は行より細かくできない。** 持ち主の裁定（2026-09-22・一括 12 の問 5）も最上位の章までとした。

**退けた案 2: どの観点も宣言していない節だけを落とす（4 観点で同じ束）。** 観点ごとに雑音を落とすという ADR-13 決定 (5) の形にならない。

**退けた案 3: 束を切らない（今のまま）。** ADR-13 決定 (5) と要件 FR17 の第 1.28 版が既に決めている。

### (c) 落とした欄の知らせ方（P-4.1 / P-4.2）

落としたことを黙らない。置き場は **reads.yaml の末尾の注釈の行**にする。凍結の土台の 忠実さ で組んだときの形（起草役が独立の実装で出した）。

```
- {doc: constitution, fields: [articles.plain, articles.statements.text]}
- {doc: srs, fields: [requirements.plain, requirements.shall, acceptance.plain, acceptance.title]}
- {doc: adr, fields: [plain, decision, options.text, figures.refs]}
- {doc: design-note, fields: [sections, figures.refs]}
# 落とした節 constitution.yaml: north_star, precedence, rules_pointer, amendment, glossary_pointer, sources
# 落とした節 srs.yaml: goals, scope, scope_m1, actors, outputs, rail, verdicts, nonfunctional, not_frozen, constraints, glossary_pointer, figures
# 落とした節 adr/ADR-2.yaml: context, basis, retreat, amends, consequences
# 落とした節 design-note/full.yaml: sources
# 常に残す節: meta, id, title, status, date, schema
```

行の並びは決定的にする。**落とした節の行は sources/ からの相対 path の byte 順（＝束の file の並びと同じ）で 1 file に 1 行**、節の名は正本に出る順。次に **宣言に在るが正本に無い節の行**（doc の一覧の順・doc の file を名指す）、最後に **常に残す節の 1 行**。落とす節が 1 つも無い file は行を出さない。実の正本では落とした節の行が観点あたり 20〜24 行、凍結の土台では 3〜5 行になる（起草役の実測）。

置き場を reads.yaml にする理由。

- **束の中身の閉じた一覧を動かさない。** 束の中身は床の定数 BUNDLE_CONTENTS の 5 つ（sources・faces・question・finding・reads）で、天井の正本 ceiling.yaml の生成区間にその写しが在る。file を 1 本足すと、床の定数・生成区間・凍結 anchor `tests/fixtures/schema/ceiling-region.txt`・`crates/folio/src/findings.rs` の読み直し・歯が同時に動き、**design-intent を書き換える便**（＝門の対象・承認が要る）になる。reads.yaml に入れれば 1 つも動かない。
- **sources/ の中へ書かない。** 床の根拠の照合は sources/ の下の行だけを見る。折り込みの注釈を写しに足すと、**folio が書いた字が根拠として通る穴**が開く。reads.yaml は照合の母集団の外なので、この穴が開かない。
- **YAML として今までどおり読める。** 束の reads.yaml を読むのは `crates/folio/src/findings.rs` の 1 か所で、そこは YAML の parser（`yaml::parse`）に渡すので注釈の行は無視される（起草役が読んで確かめた・src の直しは要らない）。行の字面を見る読み手は歯の側に 2 か所あり（`crates/folio/tests/findings.rs`）、そこへ `#` で始まる行を読み飛ばす枝を足す（2 行）。

**宣言に在るが正本に無い節は別立てで出す。** その doc の**どの file にも無い**節だけを数える（file ごとの欠け＝ある判断の記録にだけ figures の節が無い等は普通のことなので数えない）。**束を組むのは止めない**（P-4.2 の 表に出す であって、P-4.1 の 実行できなかった ではない。宣言の古さは正本の側の問題で、束は完全に組めている）。終了コードは 0 のまま。標準出力の 1 行にも、落とした節の数と 正本に無い節 の数を足す。

### (d) 凍結 anchor の組み直し（P-10.1 / P-10.2 / P-10.3）

便 97 が置いた独立の script `tests/fixtures/ceiling/bundle-anchor.py`（python3 の標準 library だけ・folio の code を 1 行も呼ばない）に、**(b) の 4 つの規則を写した絞りの口**を足し、その出力で凍結 anchor `tests/fixtures/ceiling/bundle-anchor.txt` を組み直す。

- anchor の種別は今の 4 つ（観点・file数・byte・要約値）に **2 つ足して 6 つ**にする（落とした節の数・正本に無い節の数）。1 行 = 種別 + タブ区切りの形は変えない。
- **file の一覧は 1 本も増減しない**（落とすのは行であって file ではない）。凍結の土台の絞りの実測（起草役の独立の実装）= 忠実さ 13,041 → 9,274 byte（71.1%）・読みやすさ 15,333 → 9,284（60.5%）・整合 13,880 → 9,076（65.4%）・実態 9,690 → 5,521（57.0%）。**確定の値は anchor file が持ち、歯はそれと突き合わせる**（設計ノートに byte も要約値も凍結しない）。
- python3 を起動できない環境では、便 97 と同じ形（標準エラーへ `# まだ分からない: ` の 1 行・歯は落とさない）を保つ。**新しい例外の口は足さない**（N-3.1）。
- 正本が UTF-8 として読めないときは、絞りに入る前に まだ分からない（終了コード 2）で止め、何も書かない（P-4.1・今の 全部か無しか と同じ形）。

**巻き添えの確認（起草役が repo 全体で実測した）。** 束の要約値 4 本を repo 全体で grep すると、当たるのは `crates/folio/tests/bundle.rs`・`crates/folio/tests/findings.rs`・`tests/fixtures/ceiling/bundle-anchor.txt`・`tests/fixtures/ceiling/findings/` の 10 本（fabricated-evidence・fail-no-findings・missing-field・pass-coherence・pass-fidelity・pass-readability・pass-reality・stop-refuted・stop-unrefuted・stop-upheld）と、着地済みの設計ノート 5 本（散文）だけで、**14 本とも write-set に入れた**。

write-set の外の凍結 anchor は全部列挙して当たらないことを確かめた。

| 凍結 anchor | 当たるか | 理由 |
| --- | --- | --- |
| `tests/fixtures/ceiling/findings/digest-mismatch.yaml` | **当たらない** | わざと食い違わせる 0 だけの値（絞っても 0 のまま食い違う） |
| `tests/fixtures/ceiling/findings/stamp-pass / stamp-fail / stamp-unknown.yaml` | **当たらない** | 束の要約値の欄は 0 だけの値で、`crates/folio/tests/stamp.rs` が実行のたびに測った値へ差し替える |
| `tests/fixtures/ceiling/findings/stamp-expected.yaml`（印の anchor） | **当たらない** | 印の中の要約値は歯が落として突き合わせる。節点の要約値 23 行は正本の本文から出る値で、束を絞っても動かない（便 99 が置いた・本便は正本を 1 字も変えない） |
| `tests/fixtures/schema/node-digest-anchor.txt` と `node-digest.py`（節点の要約値の残差） | **当たらない** | 母集団は `tests/fixtures/floor_base/design-intent/` で、束の fixture も design-intent も見ない（起草役が歯の入力を読んで確かめた） |
| `tests/fixtures/schema/graph-anchor.txt`・`graph-digest-anchor.txt` | **当たらない** | 同じく floor_base が母集団 |
| `tests/fixtures/schema/*-region.txt` 13 本（生成区間の写し） | **当たらない** | 実装の型付きの定数からの導出物。本便は生成区間に関わる定数を 1 つも変えない |
| `tests/fixtures/face/expected*.html` 7 本・`tests/fixtures/intake/expected-sheet*.yaml`・`tests/fixtures/figure/anchor` | **当たらない** | 面・支度表・図の生成物で、束を通らない |
| `tests/floor_cases.yaml`・id の一覧の凍結 anchor | **当たらない** | 床の判定は 1 つも変わらない |

**全数を固定した歯**も当たらないことを確かめた。`crates/folio/src/bundle.rs` の面の名の閉じた一覧 FACE_NAMES 9（本便は 1 行も変えない・便 102 が 10 にする見込み）・`crates/folio/src/ceiling.rs` の DOCUMENT_IDS 9（触らない）・`crates/folio/tests/check.rs` の p1_commands_closed_list 12（本便は命令も旗も足さない）。

**反証の束の凍結 anchor は当たる。** `crates/folio/tests/findings.rs` の反証の束（file の一覧 5 本・連結の byte 数・要約値・reads.yaml の逐語）は、**親の観点の reads.yaml をそのまま写す**ので注釈の行のぶんだけ動く。file の一覧 5 本は変わらない。この 4 つの凍結の値も write-set の中（同じ file）で組み直す。

### (e) 歯（8 本）

歯は実行 file 経由で測る（`env!(CARGO_BIN_EXE_folio)` を起動する形）。器の受付は verify の旗 --bin の次の語を filter 語と読むので、**verify の行に --bin は書かない**。

**`crates/folio/tests/bundle.rs`（7 本）**

1. **f98_the_cut_bundle_matches_the_rebuilt_anchor** — 独立の script `tests/fixtures/ceiling/bundle-anchor.py` の出力が組み直した anchor file と **byte 一致**し、凍結の土台から `folio ceiling --write` で組んだ 4 観点の束の file の数・連結の byte 数・要約値が anchor file の 6 種別の値と一致すること（要約値は sha256sum でも測り直す）。python3 が無いときは まだ分からない の 1 行を出して落とさない（P-10.3）。**赤い歯**。
2. **f98_the_dropped_sections_are_named_in_reads** — 凍結の土台の 忠実さ の reads.yaml に、constitution.yaml の落とした 6 節（north_star・precedence・rules_pointer・amendment・glossary_pointer・sources）と srs.yaml の落とした 12 節（goals・scope・scope_m1・actors・outputs・rail・verdicts・nonfunctional・not_frozen・constraints・glossary_pointer・figures）と adr/ADR-2.yaml の 5 節と design-note/full.yaml の 1 節が **sources/ の path の byte 順**に出て、常に残す 6 語の行が末尾に来ること。**数を固定してよいのは凍結の土台だからである**（実の正本には当てない）。**赤い歯**。
3. **f98_a_section_absent_from_every_source_is_named** — 凍結の土台の 読みやすさ の reads.yaml に index.yaml の sections が、整合 の reads.yaml に rules.yaml の rows が 宣言に在るが正本に無い節 として出ること。どちらの場合も束は組めて終了コードは 0 であること。**赤い歯**。
4. **f98_the_skeleton_and_the_head_survive_every_cut** — 凍結の土台と**実の正本**の両方で、4 観点の sources/ の下の全 file について、骨格の 6 つの節の見出しの行と file の頭の行が 1 行も落ちていないこと。**不変条件で書き、節の数も byte も固定しない**（実の正本は便のたびに動くため）。**赤い歯**。
5. **f98_every_kept_line_is_verbatim_and_in_order** — 凍結の土台と実の正本の両方で、絞った写しの各行が正本の同じ file の行として byte のまま在り、写しの中の順序が正本の中の順序と同じであること（＝折り返しも組み直しもしていない＝床の逐語の照合が成り立つ）。**不変条件**。**赤い歯**。
6. **f98_a_column_zero_sequence_is_not_a_new_section** — 実の正本の `srs.yaml` と `adr/ADR-4.yaml`・`ADR-5.yaml`・`ADR-7.yaml` について、`figures` を宣言に持たない観点の写しに figures の節の行が 1 行も残らず、`figures` を宣言に持つ観点の写しには残ること（規則 2）。**不変条件で書き、節の byte も行数も固定しない。凍結の土台にはこの形が無いので、この歯だけが列 0 の連なりの読み違いを捕まえる。** **赤い歯**。
7. **f98_the_generated_region_stays_whole** — 実の正本の 4 観点の写しのうち生成区間を持つものについて、開きの印（`# folio:schema:begin`）と閉じの印（`# folio:schema:end`）が **どちらも 1 つずつ残る**こと（規則 3・規則 4）。**不変条件で書き、file の名も対の数も固定しない**（起草役の実測では 25 対で、規則が無いと 6 対で閉じだけが落ちる）。**赤い歯**。

**`crates/folio/tests/findings.rs`（1 本）**

8. **f98_the_frozen_findings_still_pass_the_check** — 絞った束に凍結の所見 fixture を当て、3 値が今と同じであること（pass-fidelity / pass-readability / pass-coherence / pass-reality が 合格・stop-upheld と stop-refuted と stop-unrefuted と fail-no-findings と missing-field と digest-mismatch と fabricated-evidence が今と同じ結果）。**起草役が根拠を絞った束に当てて確かめた**（要約値を持つ fixture 11 本のうち根拠を持つのは 7 本で、絞った束に残らないのは fabricated-evidence の作り話の根拠 1 件だけ＝絞る前も後も束の外）。**赤い歯**（凍結の要約値が動くため）。

8 本とも期待値を起草役が独立に出した（1・2・3 は (c)(d) の独立の実装の出力と凍結の土台の実測、4・5・6・7 は不変条件、8 は根拠の実測）。回帰は verify の 2 行目（`crates/folio/tests/bundle.rs` と `crates/folio/tests/findings.rs` の全部）と `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）が見る。

### (f) 大きさ

| 何 | 行 |
| --- | --- |
| crates/folio/src/bundle.rs（節の範囲を取る読み口・規則 2〜4・骨格の閉じた一覧・落とした節と 正本に無い節 の一覧・reads.yaml の注釈・標準出力の 1 行・余地 961） | 150 |
| crates/folio/tests/bundle.rs（歯 7 本と、凍結の期待・reads.yaml の逐語・byte のままの写しの歯の組み直し・余地 782） | 80 |
| crates/folio/tests/findings.rs（歯 1 本・反証の束の凍結の 4 つの値・注釈を読み飛ばす枝 2 か所・**余地 236**） | 25 |
| tests/fixtures/ceiling/bundle-anchor.py（絞る規則を写す・種別を 2 つ足す） | 45 |
| tests/fixtures/ceiling/bundle-anchor.txt（script が組み直す・4 観点 × 6 種別） | 25 |
| tests/fixtures/ceiling/findings/ の 10 本（束の要約値を 1 行ずつ） | 10 |
| 合計 | **335** |

**M（見積 300）を 35 行上回る。それでも割らない**のは、束の要約値が 1 度に動くためである。絞る口・anchor・所見 fixture の 3 つはどれか 1 つだけ先に着地させると歯が赤いままになり、赤い歯を跨いで 2 便を運ぶことになる（P-3.1 に反する）。**触る src は bundle.rs 1 本で、その余地 961 は M の見積 300 を大きく上回る。** 新しい file は 1 本も無い。新しい dir は作らない。縮む file は無い。外部 crate は増やさない。

### (g) 運ばないもの・撤退条件

- 天井の正本 ceiling.yaml の読む欄の宣言（一括 12 で着地済み）・要件 FR17 の字（同）・骨格 6 語の写しを生成区間へ導出するか（便 97 の 🔴 3・天井の正本の版上げを伴うので便 102 と同じ承認に載る）。
- 束の中身の閉じた一覧（BUNDLE_CONTENTS）を動かすこと・反証の束の中身を動かすこと・所見の欄の決まりを動かすこと・観点の問いの文・注意の先の一覧・周の引き金・門の単位・新しい命令と旗・新しい dir・外部 crate・台帳への記帳。
- `crates/folio/src/` の bundle.rs 以外（ceiling.rs・findings.rs・stamp.rs・gate.rs・graph.rs・check.rs ほか）。**床の判定も天井の印も門も 1 つも変わらない。**
- `crates/folio/tests/check.rs`（p1_commands_closed_list）・`tests/floor_cases.yaml`・`tests/fixtures/schema/` の下・面と支度表と図の凍結 anchor。
- 撤退条件: 絞った束で観点の所見が落ちるようになったとき（次の周で 根拠が正本に無い が 1 件でも出たとき）は、`crates/folio/src/bundle.rs` の切る口を外して丸ごと写す今の形へ戻し、anchor の値を script で組み直す。**便 1 本で戻せる**（ほかの src を 1 字も触らないため）。戻したときも便 97 の script と anchor は残る＝2 つは別々に捨てられる。

## 2. 範囲

- 入れる: `crates/folio/src/bundle.rs` の絞る口（最上位の節の範囲を取る読み口・規則 2〜4・骨格の閉じた一覧 6 語・落とした節と 正本に無い節 の一覧・reads.yaml の末尾の注釈・標準出力の 1 行）・独立の script と凍結 anchor file の組み直し（種別を 6 つに）・`crates/folio/tests/bundle.rs` の f98_ 7 本と既に在る凍結の期待の組み直し・`crates/folio/tests/findings.rs` の f98_ 1 本と反証の束の凍結の値と注釈の読み飛ばし・凍結の所見 fixture 10 本の束の要約値。
- 入れない: design-intent の下の file の書き換え（読むだけ）・天井の正本の読む欄・要件 FR17 の字・束の中身の閉じた一覧・面の名の閉じた一覧 FACE_NAMES・床の定数 DOCUMENT_IDS・観点の問いの文・新しい命令と旗・新しい dir・新しい file・外部 crate・台帳への記帳。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| cut | 切る口 | `crates/folio/src/bundle.rs`（最上位の節の範囲・骨格の閉じた一覧 6 語・規則 2〜4・行の byte と順を変えない） |
| notice | 落とした節の知らせ | `crates/folio/src/bundle.rs`（reads.yaml の末尾の注釈と標準出力の 1 行） |
| script | 独立の実装 | `tests/fixtures/ceiling/bundle-anchor.py`（便 97 が置いた script に絞りの口を足す・python3 の標準 library だけ・folio の code を 1 行も呼ばない） |
| anchor | 凍結 anchor | `tests/fixtures/ceiling/bundle-anchor.txt`（観点ごとの file数・byte・要約値・落とした節の数・正本に無い節の数） |
| teeth | 歯 | `crates/folio/tests/bundle.rs` の f98_ 7 本と `crates/folio/tests/findings.rs` の f98_ 1 本 |

## 4. 検査（歯）

§1 (e) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate は増やさない。便 97（行 ct）は着地済み（main 420d910）で、その script と anchor file が本便の前提である。
- 一括 12（天井の正本 v0.11 の読む欄の宣言と要件書 v1.28 の FR17）は **base main 278ba59 に着地済み**で、便 97 が挙げた 2 つの前提はそろっている。
- **便 102 と `crates/folio/src/bundle.rs` が重なる。器が順に運ぶ。** 後に運ぶ便が anchor と所見 fixture の要約値を組み直す。
- python3 は host（/usr/bin/python3）に在る。CI の runner には支度の段が無いので、歯は python3 が無くても落ちない形にする（便 97 と同じ）。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "cy"
title = "天井の材料の束が写す正本を、観点が読むと宣言した最上位の節まで絞る。残すのは ① その観点の reads が挙げた節 ② 骨格の 6 語（meta・id・title・status・date・schema）③ file の頭で、切る単位は行とし、残した行は正本の byte のまま・正本の順のまま写す（行の中の欄には降りない）。最上位の節の始まりは 列 0 の 名: の行だけで、列 0 の - で始まる行は直前の節の続きである。注釈と空行の連なりは直後の節へ寄せ、直後に節が無ければ直前の節へ寄せる。生成区間（folio:schema:begin から folio:schema:end まで）は 1 つの塊として中の節と一緒に残す。落とした節は黙らず、束の reads.yaml の末尾に注釈の行として出す（落とした節は sources からの相対 path の byte 順に 1 file 1 行・次に その doc のどの file にも無い宣言の節・最後に常に残す 6 語）。束の中身の閉じた一覧は動かさず、注釈を sources の写しへは書かない。標準出力の 1 行に落とした節の数と 正本に無い節 の数を足す。凍結 anchor は便 97 の独立の script tests/fixtures/ceiling/bundle-anchor.py に同じ絞りの規則を写して組み直し、種別を 6 つ（観点・file数・byte・要約値・落とした節の数・正本に無い節の数）にする。file の一覧は 1 本も増減しない。python3 を起動できない環境では まだ分からない の 1 行を標準エラーへ出して歯を落とさない。design-intent の下は 1 file も書き換えない"
req = ["FR17"]
section = "1"
write-set = ["crates/folio/src/bundle.rs", "crates/folio/tests/bundle.rs", "crates/folio/tests/findings.rs", "tests/fixtures/ceiling/bundle-anchor.py", "tests/fixtures/ceiling/bundle-anchor.txt", "tests/fixtures/ceiling/findings/fabricated-evidence.yaml", "tests/fixtures/ceiling/findings/fail-no-findings.yaml", "tests/fixtures/ceiling/findings/missing-field.yaml", "tests/fixtures/ceiling/findings/pass-coherence.yaml", "tests/fixtures/ceiling/findings/pass-fidelity.yaml", "tests/fixtures/ceiling/findings/pass-readability.yaml", "tests/fixtures/ceiling/findings/pass-reality.yaml", "tests/fixtures/ceiling/findings/stop-refuted.yaml", "tests/fixtures/ceiling/findings/stop-unrefuted.yaml", "tests/fixtures/ceiling/findings/stop-upheld.yaml"]
verify = ["cargo nextest run -p folio --test bundle --test findings f98_", "cargo nextest run -p folio --test bundle --test findings", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "M"
done = "f98_ の歯 8 本（独立の script の出力が組み直した凍結 anchor tests/fixtures/ceiling/bundle-anchor.txt と byte 一致し、凍結の土台から組んだ 4 観点の束の file の数と連結の byte 数と要約値が anchor の 6 種別の値と一致し sha256sum で測り直しても同じで、python3 が無い環境では まだ分からない の 1 行で落ちない／凍結の土台の 忠実さ の reads.yaml に constitution.yaml の落とした 6 節と srs.yaml の落とした 12 節と adr/ADR-2.yaml の 5 節と design-note/full.yaml の 1 節が sources からの相対 path の byte 順に出て常に残す 6 語の行が末尾に来る／読みやすさ の reads.yaml に index.yaml の sections が 整合 の reads.yaml に rules.yaml の rows が 宣言に在るが正本に無い節 として出て終了コードは 0／凍結の土台と実の正本の両方で 4 観点の sources の全 file の骨格 6 節の見出しの行と file の頭の行が 1 行も落ちない／凍結の土台と実の正本の両方で絞った写しの各行が正本の同じ file の行として byte のまま在り順序も同じ／実の正本の srs.yaml と adr/ADR-4.yaml と ADR-5.yaml と ADR-7.yaml で figures を宣言に持たない観点の写しに figures の節の行が 1 行も残らず持つ観点の写しには残る／実の正本の生成区間を持つ写しで開きの印と閉じの印がどちらも 1 つずつ残る／絞った束に凍結の所見 fixture を当てて 3 値が今と同じ）が全部緑、crates/folio/tests/bundle.rs と crates/folio/tests/findings.rs の歯が全部緑、clippy が 0 警告で CI が通る"

<!-- contracts:end -->
