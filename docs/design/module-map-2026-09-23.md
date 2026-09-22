# 設計ノート: 実装の区切りの図（2026-09-23）— 責務の 6 層・依存の向き・割り直しの便 106〜110

- 状態: **起草**（反対側からの確認〔grill〕の前）。判断の記録 **ADR-15**（提案中）の材料であり、判断そのものは ADR-15 が持つ。この文書は実測と割り方の案だけを持つ。
- 出所: 総点検の設計ノート `docs/design/audit-2026-09-23.md` の §3-c・§3-d と §4 の 🔴 3（持ち主の承認 2026-09-23 08:13 JST・対話面 R-8・逐語「問いは全部推奨で」）。
- 基準点: `origin/main` = **aff1b32**。実装の側 `crates/folio/src/` 44 file・正規化 26,160 行。
- 数え方: 正規化行 = 全行 + 各行の `ceil(字数 ÷ 120) − 1`（器 scribe2 の規則 `R-C4.line-width` = 120 と同じ式）。余地 = 1,500 − 正規化行。依存の辺 = その file の本文に現れた `crate::<区切り名>` の相異なる名（`use crate::{a, b}` の括り書きも解く・自分自身は数えない）。
- 置き場: folio2 の設計ノート。規則を置かない（P-5.4・N-2.1）。ここで決まったことは ADR-15 と便の契約表へ写す。

## 1. 責務の 6 層

| 層 | 責務 | 何を知っているか |
| --- | --- | --- |
| 0 土台 | 文書を何も知らない共通の型と計算 | 何も知らない |
| 1 読む | 正本の byte を型に直す。閉じた一覧・値域・床の木の型を持つ | 正本の形 |
| 2 検査する | 型に直したものを決まりに照らして数える | 正本の形 + 決まり |
| 3 導出する | 正本から別の型付きの出力を作る（生成区間・索引・束・印・anchor・支度表） | 上記 + 出力の形 |
| 4 面に出す | 人が読むページ（HTML）と図の本体（SVG）を書く | 上記 + 見た目 |
| 5 配る | 生成物を置き、見せ、知らせる | 全部 |

**向きの決まり**: file は自分より下の層だけを名指す。同じ層どうしの名指しは許す。

総点検の設計ノート §3-d は 5 層（読む → 検査する → 導出する → 面に出す → 配る）を挙げた。土台を 1 つ足したのは、`verdict.rs`（判定の 3 値と終了コード）と `sha256.rs`（要約値の計算）が正本を 1 字も読まず、文書の形を何も知らないためである。読む層に入れると、その層の責務を「正本を型に直す」と言えなくなる。

## 2. 区切りの図（層 × file × 責務 × 正規化行 × 余地）

太字の余地は 300 未満（size M の便が受付で断られる）。

| 層 | file | 責務（file の頭の注釈から） | 正規化行 | 余地 |
| --- | --- | --- | ---: | ---: |
| 0 土台 | `sha256.rs` | 要約値（sha256）の手書き。外部 crate を足さない | 123 | 1377 |
| 0 土台 | `verdict.rs` | 判定（3 値と終了コード）。実行できなかった検査は合格にしない | 94 | 1406 |
| 1 読む | `yaml.rs` | 正本の読み手。低水準の event から木を組み、重複キーを拾う | 975 | 525 |
| 1 読む | `constitution_enums.rs` | 憲法の値域の置き場（正本から組み立て時に導出した型） | 86 | 1414 |
| 2 検査する | `adr.rs` | 判断の記録（adr/）の欄の決まりの検査 + その床の定数 | 1390 | **110** |
| 2 検査する | `note.rs` | 設計ノートの正本の形の検査 + その床の定数 | 1362 | **138** |
| 2 検査する | `findings.rs` | 天井の所見 file と起動の記録の検査（--check） | 1096 | 404 |
| 2 検査する | `anchor.rs` | 凍結 anchor の列（anchors/）の検査 | 1004 | 496 |
| 2 検査する | `check.rs` | 正本 7 file の形の床と、床の共通の道具（重複 id・非空・行 id・未知の節） | 879 | 621 |
| 2 検査する | `lineage.rs` | 凍結 anchor の列の区間の消し込み | 863 | 637 |
| 2 検査する | `parts.rs` | 部品目録の閉じた一覧（catalog）と、面が使った部品の検査 | 672 | 828 |
| 2 検査する | `link.rs` | 判断の記録と正本 4 file・凍結 anchor の列の突き合わせ | 657 | 843 |
| 2 検査する | `ceiling.rs` | 天井の正本（ceiling.yaml）の形の検査 + 天井の床の定数 | 576 | 924 |
| 2 検査する | `refs.rs` | 参照 id の解決（R-4）と規則の表の行の逆参照・憲法の件数 | 431 | 1069 |
| 2 検査する | `gitcheck.rs` | 凍結 anchor の列の版管理（git）との照合 | 395 | 1105 |
| 2 検査する | `entrance.rs` | 入口の正本（index.yaml）の形の検査 | 378 | 1122 |
| 2 検査する | `mentions.rs` | 規則の表の行 R-17 の床（散文の言及と型付きの欄の対） | 341 | 1159 |
| 2 検査する | `prose.rs` | 設計ノートの散文の門（R-16） | 327 | 1173 |
| 2 検査する | `ids.rs` | 要件・判断・受入基準の id の消失と改番 | 316 | 1184 |
| 2 検査する | `vocab.rs` | 語彙の検査（規則の表の行 R-9・本文の英字の語） | 297 | 1203 |
| 2 検査する | `rules.rs` | 規則の表の欄の決まりの床 + その床の定数 | 295 | 1205 |
| 2 検査する | `gate.rs` | 天井の門（--gate）。印と今の正本から 3 値を返す | 252 | 1248 |
| 2 検査する | `intake.rs` | 相談窓口の正本（intake.yaml）の形の検査 | 252 | 1248 |
| 3 導出する | `graph.rs` | 設計文書の索引（節点と辺）を正本から組み直す | 738 | 762 |
| 3 導出する | `bundle.rs` | 天井の材料の束を組む（--write）+ 天井の正本の読み手 | 730 | 770 |
| 3 導出する | `sheet.rs` | 相談窓口の支度表を書く（folio intake） | 571 | 929 |
| 3 導出する | `schema.rs` | 欄の決まりの生成区間の導出（folio schema）+ 床の木の型 Floor | 476 | 1024 |
| 3 導出する | `freeze.rs` | 凍結 anchor と id の凍結を書く（--freeze-anchor / --emit-amends）+ 実行の様態の型 | 357 | 1143 |
| 3 導出する | `stamp.rs` | 天井の判定の印を書く（--stamp） | 343 | 1157 |
| 3 導出する | `inject.rs` | 憲法の前文と規範文を CLAUDE.md の生成区間へ書く | 263 | 1237 |
| 4 面に出す | `face_index.rs` | 入口の面の生成器（棚・支度表の節） | 1378 | **122** |
| 4 面に出す | `face_constitution.rs` | 憲法の面の生成器 | 1294 | **206** |
| 4 面に出す | `face.rs` | 面の生成の入口と共通の部品（表紙・章帯・カード・図の枠）+ 正本の cursor | 1138 | 362 |
| 4 面に出す | `face_note.rs` | 設計ノートの面の生成器 | 1023 | 477 |
| 4 面に出す | `face_srs.rs` | 要件書の面の生成器（章 01・02・09 と骨格） | 1023 | 477 |
| 4 面に出す | `face_adr.rs` | 判断の記録の面の生成器 | 855 | 645 |
| 4 面に出す | `figure.rs` | 型付き記述から図の本体（SVG）を描く（folio figure） | 699 | 801 |
| 4 面に出す | `face_srs_items.rs` | 要件書の面の章 03〜06 | 389 | 1111 |
| 4 面に出す | `face_labels.rs` | 面の共有の名札（憲法の値域の型への網掛け） | 326 | 1174 |
| 4 面に出す | `face_srs_rtm.rs` | 要件書の面の章 07・08 | 114 | 1386 |
| 5 配る | `main.rs` | 命令の入口（副命令 12 本） | 574 | 926 |
| 5 配る | `serve.rs` | 配信（folio serve）。接続先を loopback か tailnet に限る | 419 | 1081 |
| 5 配る | `site.rs` | 配信先の組み立て（folio build） | 261 | 1239 |
| 5 配る | `hello.rs` | 気づかせる 1 行（folio hello） | 128 | 1372 |

| 層 | file 数 | 正規化行 |
| --- | ---: | ---: |
| 0 土台 | 2 | 217 |
| 1 読む | 2 | 1061 |
| 2 検査する | 19 | 11783 |
| 3 導出する | 7 | 3478 |
| 4 面に出す | 10 | 8239 |
| 5 配る | 4 | 1382 |
| **計** | **44** | **26160** |

歯の側（`crates/folio/tests/`）は 38 file・22,134 行で、上限を超えているものが 2 本ある（`tests/face.rs` 1,785・余地 **−285**／`tests/face_index.rs` 1,528・余地 **−28**）。この 2 本の割り直しは総点検の設計ノート §3-c の便 105 で、本ノートの便 106 以降の前提である。

## 3. 依存の辺の実測

`crates/folio/src/` の 44 file が互いを名指す辺を全数取り、§1 の層に照らして数えた。

| 向き | 本数 |
| --- | ---: |
| 下向き（自分より下の層を名指す） | 115 |
| 同じ層 | 72 |
| **上向き（決まりに反する）** | **20** |

### 3-a. 上向きの辺 20 本（全数）

| use する側 | 層 | use される側 | 層 | 名指しているもの |
| --- | --- | --- | --- | --- |
| `adr.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor`・`floor_diff`・`keys_floor`・`strip_notes`・`derive` |
| `note.rs` | 2 検査 | `schema.rs` | 3 導出 | 同上 |
| `ceiling.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor`・`floor_diff`・`strip_notes`・`derive` |
| `entrance.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor`・`derive` |
| `rules.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor`・`derive` |
| `check.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor` |
| `intake.rs` | 2 検査 | `schema.rs` | 3 導出 | `Floor` |
| `bundle.rs` | 3 導出 | `face.rs` | 4 面 | `R`（正本の cursor の結果の型） |
| `findings.rs` | 2 検査 | `face.rs` | 4 面 | `R` |
| `gate.rs` | 2 検査 | `face.rs` | 4 面 | `R` |
| `stamp.rs` | 3 導出 | `face.rs` | 4 面 | `R` |
| `sheet.rs` | 3 導出 | `face.rs` | 4 面 | `R`・`X`・`load` |
| `entrance.rs` | 2 検査 | `face.rs` | 4 面 | `SHELF_DOCS`・`SHELF_RELATIONS`・`ANNEXES`・`SHELF_LEGEND`（入口の棚の閉じた一覧） |
| `parts.rs` | 2 検査 | `face.rs` | 4 面 | `FIGURE_LABELS`・`MAX_PER_BAND`・`MAX_RAIL_NODES`・`MAX_STATE_NODES` |
| `anchor.rs` | 2 検査 | `freeze.rs` | 3 導出 | `Flag`・`State` |
| `check.rs` | 2 検査 | `freeze.rs` | 3 導出 | `Flag`・`After`・`after` |
| `ids.rs` | 2 検査 | `freeze.rs` | 3 導出 | `Flag`・`After`・`not_frozen_by` |
| `findings.rs` | 2 検査 | `bundle.rs` | 3 導出 | `Ceiling`・`Rules`・`Viewpoint`・`Files`・`load`・`read_dir_names`・`digest_text`・`build_one` |
| `gate.rs` | 2 検査 | `bundle.rs` | 3 導出 | `Ceiling`・`load`・`read_dir_names` |
| `gate.rs` | 2 検査 | `stamp.rs` | 3 導出 | `STAMP_FILE`（印の file 名の定数） |

### 3-b. 20 本の出どころは 5 つの file の「同居」

| 出どころの file | 同居しているもの（層をまたいで使われる側） | 同居しているもの（その file 固有の口） | 辺 |
| --- | --- | --- | ---: |
| `schema.rs` | 床の木の型 `Floor`・その比較 `floor_diff`・`strip_notes`・`keys_floor`・型から字を書く `derive` | `folio schema` の口（`TARGETS`・`run`・`run_one`・`region_of`） | 7 |
| `face.rs` | 正本の cursor（`R`・`X`・`load`）・入口の棚と部品の閉じた一覧の定数 | 面の生成の入口と共通の部品（`Frame`・`card`・`figure_panel`・`esc` ほか） | 7 |
| `freeze.rs` | 凍結の実行の様態の型（`Flag`・`State`・`After`）とその言い換え | `--freeze-anchor` / `--emit-amends` の本体（`freeze`・`emit_lines`） | 3 |
| `bundle.rs` | 天井の正本の読み手と型（`Ceiling`・`Rules`・`Viewpoint`・`Files`・`load`）・置き場の走査（`read_dir_names`）・束の組み直し（`build_one`・`digest_text`） | `folio ceiling --write` の本体（`run`・`write_all`） | 2 |
| `stamp.rs` | 印の file 名の定数 `STAMP_FILE` | `--stamp` の本体 | 1 |

**上向きの辺はすべて左の列（層をまたいで使われる型・読み手・閉じた一覧の定数）を名指している。右の列（命令の口の本体）を名指す辺は 1 本も無い。** したがって左の列を 1 つ下の層へ降ろせば 20 本は 0 本になる。降ろしても呼ぶ側の式は 1 つも変わらないので、振る舞いは変わらない。

### 3-c. 同じ層どうしの絡み（本判断は禁じないが、記録しておく）

要件書の面の 3 file は互いを名指す（`face_srs` → `face_srs_items` / `face_srs_rtm`、`face_srs_items` → `face_srs`、`face_srs_rtm` → `face_srs`）。この 3 file は行数の上限だけを理由に割られた（便 35・便 100）。同じ層どうしなので向きの決まりには反しないが、責務の線ではないので、面の側にも「正本を読んで面の文脈を組む」と「HTML を書く」の線を引く便 108・便 109 の形をあとから当てるのが筋である（本判断の外・後続）。

`face_adr.rs` と `face_note.rs` が `face_index.rs` を名指すのも同じ性質で、名指しているのは入口の面の読み手（`Record`・`Note`・`records`・`notes`）である。便 108 でその読み手が読む層へ降りると、この 2 本の辺は上向きでも同層でもなく下向きになる。

## 4. 割り直しの便（106〜110 と後続 3 本）

原則: **1 便 = 既存の src 1 本 + 新設の src 1 本**。振る舞いを変えず、既存の歯は 1 本も動かさない。歯は便 106 で境界の歯 2 本を足すだけで、以後は増えない。

順は「塞がっている file を先に開ける 4 本 → 層をまたぐ型を降ろす 1 本 → 残りを 0 にする 3 本」である。逆順にできない理由は §4-f を見よ。

### 4-a. 便 106 — 判断の記録の床の定数を読む層へ

| | |
| --- | --- |
| 何 | `adr.rs` の床の定数（`FLOOR` と欄の決まりの `const` 群・行 23〜458）を新設 `floor_adr.rs`（層 1 読む）へ移す |
| 書き込み範囲 | `crates/folio/src/adr.rs`・`+ crates/folio/src/floor_adr.rs`・`crates/folio/src/main.rs`（区切りの宣言 1 行）・`+ crates/folio/tests/modules.rs`（境界の歯）・`crates/folio/tests/adr.rs`（名指しの行） |
| 実測 | `adr.rs` 1,390 → **896**（余地 110 → **604**）／`floor_adr.rs` 494（余地 1,006） |
| 振る舞い | 不変。移した定数は `pub(crate)` のまま、名前も値も 1 字も変えない |
| 歯 | 既存 20 本は全部緑。境界の歯 2 本を新設（§5） |
| 上向きの辺 | 20 → 20（`floor_adr.rs` が `schema::Floor` を名指すので 1 本増え、`adr.rs` の 1 本が減る） |

### 4-b. 便 107 — 設計ノートの床の定数を読む層へ

| | |
| --- | --- |
| 何 | `note.rs` の床の定数（`FLOOR` と欄の決まりの `const` 群・行 28〜467）を新設 `floor_note.rs`（層 1）へ |
| 書き込み範囲 | `note.rs`・`+ floor_note.rs`・`main.rs`・`tests/modules.rs`・`tests/note.rs` |
| 実測 | `note.rs` 1,362 → **884**（余地 138 → **616**）／`floor_note.rs` 478（余地 1,022） |
| 上向きの辺 | 20 → 20（同じ入れ替わり） |

### 4-c. 便 108 — 入口の面の読み手を読む層へ

| | |
| --- | --- |
| 何 | `face_index.rs` のうち「正本を読んで面の文脈を組む」部分（`Record`・`Note`・`Readable`・`Doc`・`Annex`・`Rel`・`Ctx`・`adr_number`・`records`・`notes`・`exact`・`constitution_card`・`srs_card`・`updated`・`context`・行 118〜263 と 302〜592）を新設 `face_index_read.rs`（層 1）へ。残るのは HTML を書く側だけ |
| 書き込み範囲 | `face_index.rs`・`+ face_index_read.rs`・`main.rs`・`face_adr.rs`・`face_note.rs`（名指しの行のみ）・`tests/modules.rs`・`tests/face_index.rs` |
| 実測 | `face_index.rs` 1,378 → **941**（余地 122 → **559**）／`face_index_read.rs` 437（余地 1,063） |
| 前提 | 便 105（`tests/face_index.rs` の余地を正に戻す） |
| 上向きの辺 | 20 → 20 |

### 4-d. 便 109 — 憲法の面の読み手を読む層へ

| | |
| --- | --- |
| 何 | `face_constitution.rs` のうち文脈を組む部分（`Art`・`Ctx`・`context`・`enum_skew`・`check_counts`・`tier_names`・`tier_count`・`chapter_name`・`missing_numbers`・`relations`・`step`）を新設 `face_constitution_read.rs`（層 1）へ |
| 書き込み範囲 | `face_constitution.rs`・`+ face_constitution_read.rs`・`main.rs`・`tests/modules.rs`・`tests/face_constitution.rs` |
| 実測 | `face_constitution.rs` 1,294 → **1,000**（余地 206 → **500**）／`face_constitution_read.rs` 294（余地 1,206） |
| 上向きの辺 | 20 → 20 |

### 4-e. 便 110 — 床の木の型を読む層へ（上向きの辺が初めて減る）

| | |
| --- | --- |
| 何 | `schema.rs` の床の木の型（`Floor`・`strip_notes`・`floor_diff`・`derive` とその書き出しの補助・行 50〜289）を新設 `floor.rs`（層 1）へ。`schema.rs` に残るのは `folio schema` の口だけ |
| 書き込み範囲 | `schema.rs`・`+ floor.rs`・`main.rs`・名指しの行だけを書き換える 9 file（`adr.rs`・`note.rs`・`ceiling.rs`・`entrance.rs`・`rules.rs`・`check.rs`・`intake.rs`・`floor_adr.rs`・`floor_note.rs`）・`tests/modules.rs`・`tests/schema.rs` |
| 実測 | `schema.rs` 476 → **236**（余地 1,264）／`floor.rs` 240（余地 1,260）。名指しだけ変わる 9 file はどれも 2 行 |
| 上向きの辺 | **20 → 13** |

この便だけ src が 2 本を超える。実質の移動は 2 本で、残る 9 file は名指しの行が 2 行ずつ変わるだけである。便の大きさの見積は S（100 行）で、9 file の余地はどれも 500 以上（便 106〜109 が開けた後）なので受付を通る。

### 4-f. 順を逆にできない理由

便 110 を先に運ぶと、名指しの行を書き換える 7 file のうち `adr.rs`（余地 110）と `note.rs`（余地 138）の余地が size S の見積 100 に対して 10 行と 38 行しか残らない。逆に便 106〜109 を先に運ぶと、降ろし先の新しい file（`floor_adr.rs`・`floor_note.rs`）が `schema::Floor` を名指すので上向きの辺が入れ替わるだけで減らない。**塞がりを開けるのが先、型を降ろすのが後**で確定した。総点検の設計ノート §3-c は 4 本と見積もったが、この 1 本が要るので 5 本になる。

### 4-g. 後続 3 本（上向きの辺を 0 にする）

| 便 | 何 | 実測 | 上向きの辺 |
| --- | --- | --- | ---: |
| 後続 1 | `face.rs` の正本の cursor（`R`・`X`・`load`・行 28〜29 と 137〜300）を新設 `cursor.rs`（層 1）へ。あわせて入口の棚と部品の閉じた一覧の定数を `parts.rs` の目録の側へ戻す | `face.rs` 1,138 → 972（余地 528）／`cursor.rs` 166 | 13 → 6 |
| 後続 2 | `freeze.rs` の実行の様態の型（`Flag`・`State`・`After`・行 19〜63）を層 1 へ | `freeze.rs` 357 → 312／新設 45 | 6 → 3 |
| 後続 3 | `bundle.rs` の天井の正本の読み手と束の組み直し（`Ceiling`・`Rules`・`Viewpoint`・`Files`・`load`・`read_dir_names`・`build_one`・`digest_text` ほか）を層 1 へ。あわせて `stamp::STAMP_FILE` を層 1 へ | `bundle.rs` 730 → 319／新設 411 | 3 → **0** |

後続 3 の根拠: 束を組む関数（`build_one`）は `Files`（byte の表）を返すだけで何も書かない。書くのは `write_all` で、それは `folio ceiling --write` の口に残る。読み手と組み手を読む層へ、書き手を導出する層へ分ければ、天井の所見の検査（`findings.rs`）が束を組み直して要約値を照らす辺は下向きになる。

番号は起票のときに決める。総点検の設計ノート §3-c の便 110 以降（歯の pin を性質へ）の番号は、本ノートの 5 本ぶん後ろへ動く。

## 5. 境界の歯（`crates/folio/tests/modules.rs`・便 106 で新設）

層の割り当てと、まだ降ろしていない上向きの辺の一覧は、**歯の側**が型付きデータで持つ。実装の側に置いて歯がそれを読む形にすると、実装が自分で自分を採点することになり、生成物どうしの突き合わせだけが合格判定になる（P-10.2）。

```rust
/// 層の割り当て（責務・ADR-15 決定 (2)）。新しい区切りは必ずここに 1 行を持つ。
const LAYERS: &[(&str, u8)] = &[
    ("verdict", 0), ("sha256", 0),
    ("yaml", 1), ("constitution_enums", 1), ("floor_adr", 1),
    // ... 44 行 ...
];

/// まだ降ろしていない上向きの辺（ADR-15 決定 (4)）。実測の写しであって許可ではない。
/// 行を足す書き換えは認めない（足すなら ADR-15 を改訂する）。
const REMAINING_UPWARD: &[(&str, &str)] = &[
    ("adr", "schema"), ("note", "schema"), /* ... 20 対 ... */
];
```

歯は 2 本。

| 歯 | 何を数えるか | 落ちるとき |
| --- | --- | --- |
| `p106_layers_cover_every_module` | `LAYERS` の file 名の集合が、`src/main.rs` の区切りの宣言（`mod <名>;`）の集合と一致する | 新しい file が層を持たない／消えた file が表に残っている |
| `p106_edges_point_down` | `src/*.rs` を走査して `crate::<区切り名>` を集め、層が上がる対の集合が `REMAINING_UPWARD` と**一致**する | 上向きの辺が 1 本でも増えた／減ったのに一覧を直していない |

2 本目は集合の一致を見るので、辺を足しても減らしても落ちる。無効化の旗も「今回だけ」の口も持たない（N-3.1）。各便は `REMAINING_UPWARD` を実測どおりに書き直し、便 110 で 20 対 → 13 対、後続 3 本で 0 対になる。0 対に達したあとは、上向きの辺を 1 本でも足す変更がこの歯で落ちる。

層の割り当ての表は設計文書へ写しを導出しない。規則の表の行 **D-11** が「file と置き場の名」を P-5.6 の対象外として名指しているからである。

## 6. 数の一覧（この便の列で動く値）

| 何 | いま | 便 110 の後 | 後続 3 本の後 |
| --- | ---: | ---: | ---: |
| 実装の側の file 数 | 44 | 49 | 52 |
| 余地 300 未満の src | 4 | 0 | 0 |
| 上向きの辺 | 20 | 13 | 0 |
| 歯の file | 38 | 39 | 39 |
| 歯の本数（境界の歯ぶん） | ±0 | +2 | +2 |

## 7. 未決（ADR-15 の発効までに答えが要るもの）

1. 反対側からの確認（grill）は未実施。総点検の設計ノート §3-d が先に行うと書いている。A-2.3 は条文を改訂する判断に掛かるので ADR-15 には掛からないが、独立の審査役に当てるのが筋である。
2. 便 105（歯の file 2 本の割り直し）は本ノートの外で、便 108 の前提。割り方（面ごと）は総点検の設計ノート §3-c が持つ。
3. §3-c の同じ層どうしの絡み（要件書の面の 3 file）を解く便は本判断の外に置いた。解くなら便 108・便 109 と同じ形（読み手と書き手の線）を当てる。
