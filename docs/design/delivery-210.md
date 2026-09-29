# 設計: 便 210 — 床の版管理の照合は、別の repo から取り込んだ別の根の列の履歴を数えない（判断の記録 ADR-36）

- 要件: FR5（構造の床は結果を 3 値で返し、実行できなかった検査を合格と表示しない）。本流の要件書に在る id で、字は変えない。外の利用者の持ち込みで出る偽の違反（本物でない「不合格」）を消し、本物の違反は今までどおり落とす。
- 条: P-3.1（決まった答えの出る検査は床に置く）・P-4.1 と P-4.2（読めない版管理と見分けられない形は「まだ分からない」か今までどおり数える側）・P-10.1（期待の字は歯の側の手書き・凍結 anchor を測り直す）。
- 出所: 判断の記録 ADR-36（proposed・持ち主の承認の前・枝 docs/f1）。tsuzuri の席の求め（2026-09-29・持ち込みの予行で床が違反 9）。**本便は ADR-36 の発効の後に受け付ける。**
- 置き場: この文書は folio2 の設計ノート。契約表は末尾の区間。審査の材料は行 `he` が指す §1 だけなので、判定に要る材料は §1 に全部置く。write-set は 7 本（src 2・設計文書の正本の生成区間 1・凍結 anchor 1・歯の file 3〔本文不変 1〕）。新しい file・縮む file・消す file・新しい dir は無い。
- 門: `folio ceiling --gate --dir design-intent --write-set …`（本流 0c910db の binary・write-set 7 本・枝 docs/f1 の ADR-36 を置いた木）は **0（通す・印の周 2026-09-27-round51〔判定 合格〕に書き換える file を場所とする反証で支持された 止める は無い・印の後の変更は審査していない）**。
- 前提: **base = 本流 0c910db（便 209 の着地の後）**。この契約の数はすべてその写しの実測（参考値・規則の表の行 D-13）。
- 実装の見本: origin の枝 `impl/d210`（commit **21a64cf**・親 0c910db）。`git diff 0c910db 21a64cf` が便の全体の差分（6 file・+321 −19・47,519 byte）。**作業者は write-set の file をこの commit の中身にしてよい**（`git checkout 21a64cf -- <write-set の file>`）。write-set の外は変えない。
- 並行の便との重なり: (f) の 5。

## 1. 設計

### (a) いま起きていること（base の実測・参考値）

1. **床の中で版管理を読むのは `crates/folio/src/gitcheck.rs` の `check_git` だけ。** 履歴の一覧の命令 `log --exclude=refs/stash --all --full-history --format=%H --name-status -- <anchor の置き場>` の行から、履歴に在った anchor の名（`ever`・消えたら違反「版管理の履歴に在ったが作業ツリーに無い」）・同じ形式の anchor の中身（`hist`・違えば違反「版管理の履歴の同じ形式の anchor と中身が違う」）・列の始め直しの判定（`Tracked::seen`）の 3 つを組む。数える範囲は ADR-34 決定 (1)（先頭から辿れる commit と根の無い枝・取り込んでいない枝は関数 `aside` で外す）。
2. **外の利用者の予行（tsuzuri の写し）。** 写しで tsuzuri の本流 821ed79（参照 261 本・commit 960・根 1）に folio2 の 0c910db を `folio2/` の下へ別の根として取り込む（`merge -s ours --no-commit --allow-unrelated-histories` と `read-tree --prefix=folio2/ -u`・commit の番号を保つ・取り込みの後の先頭 d87f07a の根 2・先頭の祖先 1,305）。base の binary の tsuzuri の置き場の床は **違反 9**（「履歴に在ったが作業ツリーに無い」5 = constitution-v1.4・ids-v1.24・v1.55・v1.56・v1.57、「中身が違う」4 = constitution-v1.0〜v1.3〔folio2 の e7fa42d・4929978・dcf76c7・dc16faf〕）。`folio2/design-intent` の床は合格。tsuzuri の席の報告と同じ数。
3. **最小の手書きの写し（`tests/fixtures/anchor/root-digest-drift` を列 T とし、その v1.0 の題と digest の欄の先頭の字を変えて v1.1 を足した別の列 F を根の無い枝に置く・base の binary）。** 列 T は土台の違反「列の根の表に無い」1 を持つ。
   - (i) F を sub-dir `f/` へ取り込む → 違反 3（土台 1・「中身が違う」1・「履歴に在ったが」1）＝偽の違反 2。
   - (i') F の側で先に `git mv design-intent f/design-intent` を commit してから、同じ path のまま取り込む → 同じく偽の違反 2。
   - (v) 別の列 2 つを `f1/` と `f2/` へ取り込む → 偽の違反 2。
   - 書き換えの細工 3 形（列 T と同じ digest の欄のまま v1.0 の題を変えた根の無い枝 x）は base で「中身が違う」1 で落ちる: (ii) x を最初の親にして本流を `-s ours` で取り込み、本流を x へ早送り・(iii) x を 2 本目の親として同じ path のまま `-X theirs` で取り込む・(vi) x の上で本流を sub-dir `junk/` へ取り込み（本流の元の列を移す）、本流を x へ早送り。
4. **判断の記録。** ADR-34 決定 (1) の字では、別の根から取り込みの commit で入った履歴は (a) 先頭から辿れる commit に入る＝偽の違反は字どおりの帰結。ADR-36（proposed）が (a) を狭める（ADR-34 の本文は変えない・ADR-30 決定 (1)）。今の規範の字は `design-intent/adr/schema.yaml` の生成区間の注 anchor_note（版管理の項）と limits_note が持つ（床の定数 `crates/folio/src/floor_adr.rs` の写し）。
5. **base の歯（参考値）。** workspace の nextest 〔TBD-base〕・clippy 0 警告・床 4 本 rc 0（check 合格 違反 0・まだ分からない 0）・`folio build --out <dir> --write` 〔TBD-build〕 file。`git grep -n f210_ -- crates` は 0 件・行 id `he` は 0 件。

### (b) 直す先

1. **`crates/folio/src/gitcheck.rs` の `check_git`。** 命令を 1 本足す: `rev-list --parents HEAD`（先頭の祖先と親）。`ls-tree`・`log`・`rev-list --all --not HEAD` と同じく、起動できない・待ち上限を超えたは「版管理（git）が無いか読めない」、失敗（rc が 0 でない）は「版管理を読めない（ls-tree / log / rev-list が失敗）」の「まだ分からない」で終える（字は変えない）。`log` の行はいったん行の列（commit・状態・anchor 名・追加か変更の constitution- の本文）に集め、次の 2 と 3 の後で `ever` と `hist` に入れる（`hist` の本文を出す `show` の撃ち方と待ち上限の扱いは今と同じ）。
2. **根の commit。** 今の作業ツリーの anchor の置き場の最初の版の anchor（床の定数 `anchor.file_name` の `<version>` を `anchor.first_version` に替えた名＝constitution-v1.0.yaml）を型付きで読み（`read_blob`・重複キーと読めない本文は None）、digest の欄の字を「今の根の digest」とする。行の列のうち、その名の追加か変更の行で、本文の digest の欄が今の根の digest と同じ行の commit を「根の commit」とする（取り込んでいない枝の commit は行の列に入らない）。今の根の anchor が無い・読めない・digest の欄が無いときは根の commit を空にする。
3. **関数 `apart`（新・同じ file）。** `rev-list --parents HEAD` の出力と根の commit から、根の commit のどれとも共通の祖先を持たない先頭の祖先（別の根の列）の集合を返す。組み方: 出力の中の根の commit から親へ辿った祖先（自分を含む）を「近い」とし、残りの行を関数 `aside` に渡して、近い commit から子へ辿れる commit を「共通の祖先を持つ」とする。どちらにも入らない commit が別の根の列。根の commit が出力に 1 つも無ければ空（狭めない＝ADR-36 決定 (2)）。行の列のうち、commit がこの集合に在る行は `ever` にも `hist` にも入れない（`seen` は同じ範囲の `ever` から組む）。
4. **`crates/folio/src/floor_adr.rs` の注 2 つ。** anchor_note の版管理の項の「…判断の記録 ADR-34）。」の後に 1 文「先頭の祖先のうち、今の列の根の anchor（first_version の anchor と digest の欄が同じ anchor）を足した commit のどれとも共通の祖先を持たない commit（別の repo から取り込んだ別の根の列）の履歴は数えない（今の置き場に根の anchor が無い・読めない・先頭の祖先の履歴に足した commit が無いときは狭めない・判断の記録 ADR-36）。」を足す。limits_note の「版管理の見え方…」の項の後に 1 項「別の根の列を見分けるのは今の列の根の anchor の digest の欄で、根の digest を固定するのは列の根の表である（根の anchor を別の digest のものへ差し替えると元の列を数えなくなるが、列の根の表と索引の照らしが落とす）。sub-dir へ取り込んだ置き場の床は、取り込む前の履歴を移す前の path では数えず、取り込みの commit が足した anchor も履歴に数えない（取り込む前の履歴の照合は元の repo か、履歴を sub-dir へ書き換えて取り込む形が受け持つ・判断の記録 ADR-36）。」を足す。どちらも判断の記録の番号は括弧の中の最後の項に置く（便 194 の外の置き場へ写す字〔`floor.rs` の `text_for`〕がその項だけを落とし、ほかの句は外の置き場にも残る）。注なので床（folio check）は数えない。
5. **`design-intent/adr/schema.yaml`。** `folio schema --dir design-intent --write` で生成区間を書き直す（上の 2 行だけが変わる・28,979 → 30,048 byte）。手では書かない。
6. **凍結 anchor。** `tests/fixtures/schema/adr-region.txt` を新しい生成区間（begin と end の行を除く）に測り直し、`crates/folio/tests/schema.rs` の定数 3 つ（REGION_LINES 151 → 152・REGION_BYTES 28979 → 30048・REGION_SHA256 → 56c6335b…c087）を直す。値は folio と独立の数え（python の hashlib・起草の記録の f1-scripts が使う anchors-190.py）。`tests/schema.rs` は器の式（幅 120 正規化・歯 f89）で **700 行＝上限 700 ちょうど**（base と同じ）。本便は定数 3 行の値を書き換えるだけで、どの行も 120 字の内＝器の式の行数は 700 のまま（見本 21a64cf で python の実装が 700）。**作業者は `tests/schema.rs` に行を足さない**（足すと f89 が落ちる）。
7. **変えないもの。** 違反と「まだ分からない」の字・ADR-34 の範囲（全ての参照を読む・`--full-history`・refs/stash を数えない・取り込んでいない枝を数えない・根の無い枝を数える）・先頭の木との照合・除外・未追跡・版管理の根・浅い写し・環境変数の遮断・列の根の digest の照らし・凍結の命令の振る舞い・`toplevel`・憲法と要件書と判断の記録の字・生成区間の注 2 つの外・床の fixture（`tests/floor_cases.yaml`）の字・`folio build` の出力・folio2 自身の床 4 本の結果（folio2 の先頭の祖先は根が 1 つ＝別の根の列が無い）。

### (c) 歯（f210_・base で 0 件）

binary 経由の歯は `crates/folio/tests/gitcheck.rs`（既存の file の末尾・助けの関数 4 つ = 根の無い枝に列を置く `orphan_column`・共通の祖先を持たない履歴を取り込む `merge_unrelated`・sub-dir へ取り込む `subtree`・今の枝の名 `current`、と土台の違反 1 行だけを見る `only_the_base`）。今の歯と同じく `tests/fixtures/anchor/` の組を一時 dir の `design-intent/` に写し、根で git init と 1 commit にする。別の列は根の無い枝で、組 root-digest-drift を写して v1.0 の題と digest の欄の先頭の字を変えた最初の commit（と v1.1 を足す commit）で作る。期待の数と字は歯の側の手書き。

1. **f210_imported_root_under_a_subdir_is_not_counted（(a) 3 の (i)）。** 別の列 f を `f/` へ取り込む。違反は土台の 1 行だけで、「履歴に在ったが」と「中身が違う」は 0。
2. **f210_premoved_import_is_not_counted（(i')）。** f の側で先に `f/design-intent` へ移す commit を置き、同じ path のまま取り込む。土台の 1 行だけ。
3. **f210_two_imports_are_not_counted（(v)）。** 別の列 2 つ（digest の欄の先頭の字が違う）を `f1/` と `f2/` へ取り込む。土台の 1 行だけ。
4. **f210_rootless_rewrite_made_first_parent_still_fails（(ii)・席の案 A の穴）。** 同じ digest の欄のまま v1.0 の題を変えた根の無い枝 x を最初の親にして本流を取り込み、本流を x へ早送り。「中身が違う」がちょうど 1。
5. **f210_rootless_rewrite_merged_at_the_same_path_still_fails（(iii)）。** x を 2 本目の親として同じ path のまま `-X theirs` で取り込む。「中身が違う」がちょうど 1。
6. **f210_relocated_original_line_still_fails（(vi)・席の案 C の穴）。** x の上で本流を `junk/` へ取り込み（本流の元の列を移す）、本流を x へ早送り。「中身が違う」がちょうど 1。
7. **f210_deletion_after_import_still_fails。** f を `f/` へ取り込んだ後、本流の v1.0 の削除を commit。終了コード 1・constitution-v1.0.yaml の「履歴に在ったが」の行が在る。
8. **f210_head_without_root_anchor_keeps_counting（ADR-36 決定 (2)）。** 組 no-anchor（根の anchor が無い置き場）に f を `f/` へ取り込む。狭めないので終了コード 1・「履歴に在ったが」がちょうど 3（f の v1.0・v1.1・索引）。
9. **f210_head_list_failure_is_unknown（条 P-4.1）。** 引数に rev-list を持ち `--all` を持たないとき（先頭の祖先の一覧）だけ終了コード 128 で終え、ほかは本物の git へ渡す shell の git を、folio の子の処理の PATH の先頭に置く。標準エラーに「# まだ分からない: 」で始まり「版管理を読めない（ls-tree / log / rev-list が失敗）」を含む行が在り、「履歴に在ったが」と「中身が違う」は 0。
10. **f210_schema_notes_name_the_other_root。** 実の `design-intent/adr/schema.yaml` に、(b) 4 の新しい字の 3 句（anchor_note の範囲の文の括弧まで・limits_note の最初の文の頭・「sub-dir へ取り込んだ置き場の床は…履歴に数えない」）がちょうど 1 回ずつ在る。
11. **単体の歯 f210_apart_takes_only_lines_without_a_common_ancestor（`crates/folio/src/gitcheck.rs` の tests の区間）。** 手書きの親の表 13 行（本流 t0〜t2 と根の commit k・t0 から切って取り込んだ枝 s1・別の根の列 f0〜f1 と g0〜g1 を取り込む m と m3・本流の続き x と m2）で、`apart` がちょうど f0・f1・g0・g1 を返す。根の commit が空・表に無い commit だけなら空。別の根の列の f1 も根の commit なら、残りは g0・g1 の 2 つ。
12. **RED の実測。** 〔TBD-red〕

### (d) 採らなかった形（ADR-36 の案 b〜f）

1. **床を変えず、取り込む側が履歴を sub-dir へ書き換える（案 b）。** 写し（folio2 0c910db を `filter-branch --index-filter` で `folio2/` の下へ書き換えた 3d553ac を取り込む）では base の binary のまま tsuzuri の置き場も `folio2/` の置き場も違反 0。commit の番号が変わる（tsuzuri の予行の決めに反する）ので床の決まりにはせず、取り込む側の選択肢に残す（ADR-36 決定 (6)）。
2. **最初の親の列の根を祖先に持つ commit だけ（席の案 A）。** 見本をこの形に変えると歯 4 と 6 が落ちる（変異 M9・席の案 A の見本の binary でも (ii)・(vi) の「中身が違う」が 0）。根の anchor が無い置き場（歯 8）でも狭めるので歯 8 も落ちる。
3. **sub-dir へ移された別の根の列だけを外す（席の案 C）。** 案 C の見本の binary（取り込みの commit ごとに `merge-base`・`rev-parse <親>:<置き場>`・`ls-tree -r -d` を撃つ形）で、歯 2・6・8 が落ちる（(i') の偽の違反 2 が残り、(vi) の「中身が違う」が 0）。
4. **tsuzuri の案 (a)（先頭と同じ根）・案 (b)（1 本目の親の列だけ）。** (a) は字のままでは本流自身の過去が落ちるか何も変わらない（ADR-36 の案 e）。(b) は ADR-34 決定 (2) の全ての参照と `--full-history` を捨てる（ADR-34 の案 b の変異 M2 で床の fixture git-orphan-branch-refreeze が落ちた・便 190 の実測）。

### (e) 既存の歯・突然変異・外の置き場

1. **既存の歯。** 〔TBD-nextest〕
2. **突然変異（見本 21a64cf の写しの src だけを 1 通りずつ変え、f210_ の 11 本を撃つ・M11 は tests/floor_cases と tests/schema も撃つ）。** 〔TBD-mut〕
3. **外の置き場（tsuzuri の写し・参考値）。** (a) 2 の写しで、base の binary の違反 9 が見本の binary で **0（合格・まだ分からない 0）**。`folio2/design-intent` の床は両方とも合格。案 A と案 C の見本の binary も 0。着地の後に tsuzuri の置き場で `folio schema --write` を 1 回（判断の記録の欄の決まりの注 2 つ）撃つまで `folio schema --check` が落ちる（床は注を数えないので落ちない）。
4. **列の根の表に頼る所（ADR-36 決定 (4)・`tests/fixtures/floor_base` の写し・iiib-real.sh）。** 根の無い枝 x が digest の違う v1.0（と索引の最初の項）を持ち、本流が `-X theirs` で取り込む形は、見本では本流の元の列を数えない（「中身が違う」0）が、列の根の表の違反「列の根 v1.0 の digest が床の定数（列の根の表の folio2-constitution の行）と違う」で落ちる（base・案 A・案 C・見本とも終了コード 0 でない）。
5. **取り込んだ置き場の床（変えない所・ADR-36 決定 (6)）。** tsuzuri の写しで `folio2/design-intent/anchors/constitution-v1.4.yaml` の削除を commit すると、base も見本も `folio2/design-intent` の床は終了コード 2（索引の照らしの「まだ分からない」）・版管理の違反 0。案 b の写しでは両方とも違反 1（「履歴に在ったが」）。本便はこの形を変えない。
6. **命令の時間。** 増える `rev-list --parents HEAD` は tsuzuri の写し（先頭の祖先 1,305）で 0.01 秒。両方の binary が合格する案 b の写しで床の全体の時間は同じ程度（3.5〜4.4 秒・負荷の高い host・参考値）。

### (f) 大きさ・余地・verify と done の対応

1. **write-set の印。** 新しい file は無い。`crates/folio/tests/floor_cases.rs` は本文を変えない（verify の `--test` の scope）。差分 47,519 byte（`git diff 0c910db 21a64cf | wc -c`・6 file・+321 −19）。
2. **余地（CapHeadroom）。** 測るのは write-set の src の 2 本（python と awk の 2 実装で一致・cap-210.log）。

| file | base の正規化行数（参考値） | base の余地 | 本便の後 | 本便の後の余地 |
| --- | ---: | ---: | ---: | ---: |
| `crates/folio/src/gitcheck.rs` | 477 | 1023 | 550（+73） | 950 |
| `crates/folio/src/floor_adr.rs` | 514 | 986 | 519（+5） | 981 |

3. **size は S。** src の増分は +78 で S の見積 100 の内。余地の最小（floor_adr.rs の base 986）は S の 100 を超える。
4. **verify は 6 行**で、done の 6 つの塊と 1 対 1 に揃える。〔TBD-verify〕
   1. `cargo nextest run -p folio --test gitcheck f210_` = (c) の 1〜10（10 本）。
   2. `cargo nextest run -p folio --bin folio f210_` = (c) の 11（1 本）。
   3. `cargo nextest run -p folio --test gitcheck` = 便 8 の 4 本・便 190 の 14 本と (c) の 10 本（今の違反の字と数が同じ）。
   4. `cargo nextest run -p folio --test schema` = 生成区間と凍結 anchor の一致（(b) 5・6）。
   5. `cargo nextest run -p folio --test floor_cases` = 床の fixture（根の無い枝の場合 git-orphan-branch-refreeze を今の字のまま・環境変数・浅い写しの場合を含む）。
   6. `cargo clippy --workspace --all-targets -- -D warnings` = 0 警告。
5. **verify の歯の file と write-set。** `--test` で名指す歯の file（gitcheck・schema・floor_cases）は全部 write-set に在る。`--bin folio` の歯の在り処（gitcheck.rs）も write-set に在る。
6. **並行の便との重なり（2026-09-29 19:5x の時点・origin の impl/* と docs/* の枝の 0c910db との差分の file を読んだ）。** write-set の file に触れる枝は、着地済みの便（190・196・198・209 ほか）と止めた便の控え（impl/d172〜d185・impl/f2-648.254-run1）だけで、走っている便の枝（impl/d201・impl/d211）は write-set に触れない。着地の順は F1（本便）と F2（便 211）の後に tsuzuri が持ち込む（tsuzuri の決め）。

| 並行の便 | 重なりうる file | 扱い |
| --- | --- | --- |
| 便 211（F2・impl/d211・tailnet の住所の字） | 無し（serve.rs と新しい歯） | 順は問わない |
| 便 201（impl/d201・地図の節点の裁定 id） | 無し | 順は問わない |
| 今後の便で `tests/schema.rs` の定数か判断の記録の生成区間を書く便 | `tests/schema.rs`（700 行＝上限ちょうど）・`adr/schema.yaml`・`adr-region.txt` | 後の便が本便の着地の後に数え直す |

### (g) 門と受付

1. **門。** 冒頭のとおり 0（通す）。
2. **受付。** ADR-36 の発効（持ち主の承認・枝 docs/f1 の取り込み）の後。受付の先撃ち（precheck）は 〔TBD-precheck〕。
3. **着地の後。** 席は tsuzuri へ「床の版管理の照合は別の repo から取り込んだ別の根の列の履歴を数えない（ADR-36）・`folio schema --write` を 1 回（判断の記録の欄の決まりの注 2 つ）・持ち込む commit は本便と便 211 の着地の後の先頭」を返す。

### (h) 数え直す手順（誰でも撃ち直せる形・規則の表の行 D-13）

起草の記録は持ち主の home の下の `.local/share/folio2/handoff-2026-09-28/f1-draft.md`、script と log は同じ dir の f1-scripts。

1. 模擬: 見本 21a64cf（c210.patch = `git diff 0c910db 21a64cf`・歯だけ = r210-teeth.patch）。chain-210.sh（組み立て・workspace の nextest〔`--test-threads 2`・folio2 の全レーンで同時 1 本を待つ〕・clippy・床 4 本と build の差・RED・変異・余地）。floor4.sh（床 4 本と build）。
2. 最小の写し: repro-210.sh（(i)・(i')・(v)・(ii)・(iii)・(vi)・取り込んでいない枝・根の anchor の無い置き場・取り込みの後の削除・取り込んだ置き場の削除・digest の違う根の差し替えを、base と案 A・案 C・見本の binary で撃つ）。iiib-real.sh（列の根の表に行を持つ土台で digest の違う根の差し替え）。
3. 外の置き場: tz-210.sh（tsuzuri の .git だけを写し、その写しの中では git を撃たず、clone --no-checkout の後に core.hooksPath が無く hook が sample だけなことを確かめてから checkout し、枝を局所の枝にしてから remote を外す。MODE=B で案 b の写し）。
4. RED: red-210.sh。突然変異: mut-210.py。余地: cap-210.sh（lines.py と lines.awk）。

### (i) 本便が運ばないもの・言えないこと・撤退条件

1. **運ばないもの。** ADR-36 の本文（枝 docs/f1・席が持ち主へ出す）・ADR-34 と ADR-2 の本文・要件書と憲法と規則の表の字・床の fixture の字・床の土台と fixture の中の判断の記録の欄の決まりの写し（注は床が数えない）・tsuzuri の写しの書き直し（tsuzuri の手番）・台帳への記帳（席）・外部 crate・新しい dir。
2. **言えないこと。** (1) 今の置き場に根の anchor が無い（凍結の前の）置き場が anchor を持つ repo を取り込むと、狭めないので偽の違反が残る（歯 8・黙らない側）。本流の根の anchor の削除を commit した場合も狭めないので、取り込んだ列の anchor の偽の違反が本物の違反と並んで出る。(2) 別の根の列の見分けは根の anchor の digest の欄に頼り、根を違う digest の anchor へ差し替えると本流の元の列を数えなくなる（落とすのは列の根の表・(e) 4）。(3) 取り込んだ置き場（sub-dir）の床は取り込む前の履歴を照らさない（本便の前から同じ・(e) 5）。(4) 浅い写しは ADR-34 のまま変えない（切り口の commit は根の anchor を足した形に見えるので、根の anchor を持つ切り口の列は数える）。
3. **撤退条件。** (1) 本便が要件書 FR5 か ADR-36 か憲法の字を変えないと書けないと分かったら、止めて席へ返す。(2) 受付の時点で本流の `gitcheck.rs` の `check_git`、`floor_adr.rs` の注 2 つ、`adr/schema.yaml` の生成区間、`tests/schema.rs` の REGION_ の 3 行のどれかが base と違えば、止めて席へ返す（数え直してから運ぶ）。(3) 本便の後に (b) 6 の定数の外の既存の歯が落ちたら、その歯の本文も fixture も直さずに止めて席へ返す。(4) 本便の後に folio2 自身の床 4 本の結果が変わるか、`folio build` の出力が 1 byte でも変われば、止めて席へ返す。

## 2. 範囲

- 入れる: `gitcheck.rs` の `check_git` の命令 1 本（`rev-list --parents HEAD`）と行の列・根の commit・関数 `apart`・単体の歯 1 本、`floor_adr.rs` の注 2 つ、`adr/schema.yaml` の生成区間の書き直し、凍結 anchor `adr-region.txt` と `tests/schema.rs` の定数 3 つ、`tests/gitcheck.rs` の f210_ の 10 本と助け 5 つ。
- 入れない: 違反の字・ADR-34 の範囲・先頭の木との照合・除外・未追跡・浅い写し・環境変数・列の根・凍結の命令・`toplevel`・憲法と要件書と判断の記録の字・床の fixture の字・取り込んだ置き場の床・外の置き場・台帳への記帳・外部 crate・新しい dir。

## 3. 部品

| id | 名 | 役 |
| --- | --- | --- |
| rows | 履歴の行の列 | `check_git` の `log` の行（commit・状態・anchor 名・constitution- の本文）を集める |
| root | 根の commit | 今の根の anchor の digest の欄と同じ digest の最初の版の anchor を足すか変えた commit |
| apart | 別の根の列 | `gitcheck.rs` の `apart`・命令 `rev-list --parents HEAD`・`aside` と同じ組み方 |
| note | 今の規範の字 | `floor_adr.rs` の注 2 つ → `adr/schema.yaml` の生成区間 |
| anchor | 凍結 anchor | `adr-region.txt`・`tests/schema.rs` の定数 |
| teeth | 歯 | `tests/gitcheck.rs` の f210_ の 10 本と `gitcheck.rs` の単体の 1 本 |

## 4. 検査（歯）

§1 (c)(e)(f) のとおり。共通の検証は `.vessel.toml` の common-verify（workspace 全体の nextest と clippy）。

## 5. 依存

- 外部 crate も外部ライブラリも増やさない。新しい dir は無い。
- 前提の着地: 便 209（本流 0c910db）と ADR-36 の発効（枝 docs/f1）。
- 本便の着地の後に席が見ること: 本流の `target/debug/folio` を組み直す。tsuzuri へ `folio schema --write` の 1 回と持ち込む commit を返す。

<!-- contracts:begin -->
schema = 1

[[contract]]
id = "he"
title = "床の版管理の照合は、別の repo から取り込んだ別の根の列の履歴を数えない（判断の記録 ADR-36・tsuzuri の持ち込みの予行の違反 9）: crates/folio/src/gitcheck.rs の check_git に命令 rev-list --parents HEAD を足し（起動できない・失敗は今と同じまだ分からない）、log の行をいったん行の列に集め、今の作業ツリーの最初の版の anchor の digest の欄と同じ digest の欄の最初の版の anchor を足すか変えた commit（根の commit）を組み、新しい関数 apart で根の commit のどれとも共通の祖先を持たない先頭の祖先（別の根の列）の集合を組んで、その commit の行を ever にも hist にも入れない（根の anchor が無い・読めない・根の commit が先頭の祖先に無いときは狭めない・ADR-34 の範囲と違反の字は変えない）。crates/folio/src/floor_adr.rs の注 anchor_note に 1 文と limits_note に 1 項を足し、folio schema --write で design-intent/adr/schema.yaml の生成区間を書き直し、凍結 anchor tests/fixtures/schema/adr-region.txt と crates/folio/tests/schema.rs の定数 REGION_LINES と REGION_BYTES と REGION_SHA256 を測り直す。歯は crates/folio/tests/gitcheck.rs の f210_ の 10 本（別の列を sub-dir へ取り込む・先に移してから取り込む・2 つ取り込むの 3 形で偽の違反が出ない・根の無い枝の書き換えを最初の親にして早送りする・同じ path のまま取り込む・本流の元の列を sub-dir へ移すの 3 形と取り込みの後の削除は今までどおり落ちる・根の anchor の無い置き場は狭めない・先頭の祖先の一覧の失敗はまだ分からない・注の字）と gitcheck.rs の単体の 1 本（apart の親の表）"
req = ["FR5"]
section = "1"
write-set = ["crates/folio/src/gitcheck.rs", "crates/folio/src/floor_adr.rs", "design-intent/adr/schema.yaml", "tests/fixtures/schema/adr-region.txt", "crates/folio/tests/gitcheck.rs", "crates/folio/tests/schema.rs", "crates/folio/tests/floor_cases.rs"]
verify = ["cargo nextest run -p folio --test gitcheck f210_", "cargo nextest run -p folio --bin folio f210_", "cargo nextest run -p folio --test gitcheck", "cargo nextest run -p folio --test schema", "cargo nextest run -p folio --test floor_cases", "cargo clippy --workspace --all-targets -- -D warnings"]
size = "S"
done = "crates/folio/tests/gitcheck.rs の f210_ の 10 本（別の列を sub-dir へ取り込む・先に sub-dir へ移してから取り込む・別の根を 2 つ取り込むの 3 形で先頭の床に版管理の違反が出ない・根の無い枝で v1.0 を書き換えて最初の親にし本流を早送りする・2 本目の親として同じ path のまま取り込む・本流の元の列を sub-dir へ移して書き換えを元の path に置くの 3 形は中身が違うで落ちる・取り込みの後の本流の削除は落ちる・根の anchor の無い置き場は狭めず取り込んだ列の anchor を数える・先頭の祖先の一覧だけが失敗するとまだ分からない・判断の記録の欄の決まりの注が ADR-36 の範囲の字）が緑、binary の単体の f210_ の 1 本（apart の親の表）が緑、tests/gitcheck.rs の歯の全部（便 8 の 4 本と便 190 の 14 本を含む）が緑、tests/schema.rs の歯の全部（生成区間と凍結 anchor の一致）が緑、tests/floor_cases.rs の歯の全部（根の無い枝の場合 git-orphan-branch-refreeze を今の字のまま・環境変数・浅い写しの場合を含む床の fixture）が緑、clippy が 0 警告で、workspace の nextest が全部緑で CI が通り、着地の後の main で folio check --dir design-intent が合格（違反 0・まだ分からない 0）・folio schema --dir design-intent --check が一致・folio inject --check が 0・folio derive --dir design-intent --out ../contracts --check が一致"
<!-- contracts:end -->
