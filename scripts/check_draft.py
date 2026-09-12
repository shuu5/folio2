#!/usr/bin/env python3
"""folio2 design-intent の床（day-1 の暫定 script・M0 で folio の検査に置換する）。使い方: python3 scripts/check_draft.py（repo root で・design-intent/*.yaml を読む）。

検査（すべて決定的・fail-closed: 読めない／parse できないは rc 2）:
  schema  : 憲法 schema 節の top_level / meta / precedence / article / statement / mechanism の欄集合（未知の欄は落とす = N-3）
            enums / tier_mechanism_allowed / live / stage・polarity（reject・build-check に必須）/ 1 文 1 極性（R-11）/ plain 必須（R-10）
  refs    : 参照 id の未解決 0（R-4・母集団 = 正本 4 file + 判断の記録の全欄・内部 3 空間 = 要件書 id・条 id〔枝番含む・anchor の鎖に在った過去の id も知っている〕・rules 行 id）
            どの条からも参照されない rules 行 0（R-4 双方向）/ rules 行の article ⇔ 条の relations.rules
  rules   : rules schema（top_level / 行の欄 / enums / 凍結行の裁定 id）/ kind_map（R 行だけ）
  vocab   : 本文（憲法の見出し・規範文・平易文・前文 / rules の what / 要件書の見出し・規範文・平易文・制約）の英字の語のうち
            語彙（terms・field_terms の term / en・identifiers）に無いもの（R-9・R-12 の機械側）/ 語彙の定義の閉包（定義文の英字語も同じ母集団）
  inject  : 注入の母集団（前文 + 規範文）の本数が inject_check.derive と一致
  polarity: 極性一覧（P-18.3）を mechanism の stage / polarity と rules 行の stage から生成し、in-loop の本数を出す
            （P-18.4「in-loop 0 なら落とす」は live: delivery-0 ゆえ発効時点では「まだ分からない」として出す）
  adr     : 判断の記録（adr/ADR-n.yaml・schema は adr/schema.yaml・ADR-1）の欄・値域・非空・退けた案（採用 1）・撤退条件（P-8.1）・承認欄（N-4・承認者・裁定 id の形・対話面 R-8）
            発効した判断（accepted / retired + 承認欄）だけが条文の改訂を説明できる。amends ⇔ amended_by（A-2）。ADR-n の参照解決は A-2 の機構（R-4 の 3 空間は変えない）
            判断の記録の本文の英字語は rules 行 R-14 が在るときだけ数える（行が無ければ「まだ分からない」・N-2）
  anchor  : 凍結 anchor の鎖（anchors/index.yaml + anchors/constitution-<版>.yaml・ADR-2）。現行の射影 ≡ 最新 anchor（N-4）・版の一致（A-2）
            anchor 全欄の digest（json 正規化・sha256）・索引との 1:1・previous の鎖（根 = first_version・切れは rc 2）・meta.approval の写しの一致・symlink 拒否
            直前 anchor との差分は欄単位（見出し・段・縛る相手・規範文ごとの本文/型/強度・並び・schema 節と前文の各欄）で全件を amends と 1:1 に消し込む（余りも不足も落とす）
            --freeze-anchor: 全検査が 0 違反かつ「まだ分からない」が無いときだけ凍結し索引へ追記（版は最新より新しい・差分と発効した判断が要る）
            --emit-amends: 最新 anchor と現行の欄単位の差分を amends の形で印字する（判断の記録を書く補助・read-only）
  counts  : meta.counts と実数の一致
rc: 0 = 全部通った / 1 = 違反あり / 2 = 読めない・測れない（parse 不能・型違い・anchor 0 本・鎖切れ・R-14 行なし）
"""
import re, sys, os, json, pathlib, collections, argparse, hashlib
try:
    import yaml
except ImportError:
    print('check_draft: pyyaml が無い', file=sys.stderr); sys.exit(2)

ap = argparse.ArgumentParser(); ap.add_argument('--dir', default='design-intent'); ap.add_argument('--names', default='placed', choices=['draft', 'placed'])
ap.add_argument('--freeze-anchor', action='store_true'); ap.add_argument('--emit-amends', action='store_true')
args = ap.parse_args()
def _hook(t, v, tb):   # 想定外の例外（型違い・欠落）は「違反あり」でなく「読めない」（rc 2）
    sys.stderr.write(f'check_draft: 読めない・型が違う（想定外の例外）: {t.__name__}: {v}\n'); sys.stderr.flush(); os._exit(2)
sys.excepthook = _hook
class StrictLoader(yaml.SafeLoader):   # 同じ表に同じキーを 2 度書いた file を拒む（人と機械の読みの分裂を防ぐ）
    pass
def _strict_mapping(loader, node, deep=False):
    seen = set()
    for kn, _ in node.value:
        k = loader.construct_object(kn, deep=deep)
        if k in seen: raise yaml.constructor.ConstructorError(None, None, f'重複キー {k!r}', kn.start_mark)
        seen.add(k)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)
StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, lambda l, n: _strict_mapping(l, n))
HERE = pathlib.Path(args.dir).resolve()
SUF = '.draft.yaml' if args.names == 'draft' else '.yaml'
def load(name):
    p = HERE / (name + SUF)
    if not p.exists():
        print(f'check_draft: 正本が無い: {p}', file=sys.stderr); sys.exit(2)
    try:
        return yaml.load(p.read_text(encoding='utf-8'), Loader=StrictLoader)
    except Exception as ex:
        print(f'check_draft: parse できない: {p}: {ex}', file=sys.stderr); sys.exit(2)

c = load('constitution'); r = load('rules'); v = load('vocabulary'); s = load('srs')
errs = []
def err(kind, msg): errs.append((kind, msg))
def keys_ok(kind, where, obj, spec):
    if not isinstance(obj, dict): err(kind, f"{where}: 型が違う（欄の表でない）: {type(obj).__name__}"); return
    ks = set(obj.keys()); req = set(spec.get('required', [])); opt = set(spec.get('optional', []))
    if not req <= ks: err(kind, f"{where}: 必須欄が無い: {sorted(req - ks)}")
    if ks - req - opt: err(kind, f"{where}: 未知の欄（N-3）: {sorted(ks - req - opt)}")

# ── schema（憲法）──
sc = c['schema']; en = sc['enums']
if set(c.keys()) - set(sc['top_level']): err('schema', f"憲法の未知の節（N-3）: {sorted(set(c.keys()) - set(sc['top_level']))}")
keys_ok('schema', 'meta', c['meta'], sc['meta'])
pr = c.get('precedence') or {}
keys_ok('schema', '前文', pr, sc['precedence'])
def mech_ok(where, m, tier=None):
    keys_ok('schema', f'{where}.mechanism', m, sc['mechanism'])
    if m.get('kind') not in en['mechanism_kind']: err('schema', f"{where}: mechanism.kind が値域外: {m.get('kind')}")
    if m.get('live') not in en['mechanism_live']: err('schema', f"{where}: mechanism.live が値域外: {m.get('live')}")
    if m.get('kind') == 'none' and not m.get('note'): err('schema', f"{where}: mechanism none に理由が無い")
    if m.get('kind') in sc['mechanism']['stage_polarity_required_for']:
        if m.get('stage') not in en['stage']: err('schema', f"{where}: mechanism.stage が無いか値域外（極性一覧の元・P-18.3）: {m.get('stage')}")
        if m.get('polarity') not in en['polarity']: err('schema', f"{where}: mechanism.polarity が無いか値域外: {m.get('polarity')}")
    if tier and m.get('kind') not in sc['tier_mechanism_allowed'][tier]: err('schema', f"{where}: 段 {tier} に機構 {m.get('kind')} は座れない（G3）")
mech_ok('前文', pr.get('mechanism') or {})
ids = [a['id'] for a in c['articles']]; st_ids = set()
if len(ids) != len(set(ids)): err('schema', f'条 id が重複: {[i for i, n in collections.Counter(ids).items() if n > 1]}')
for a in c['articles']:
    keys_ok('schema', a.get('id', '?'), a, sc['article'])
    if a.get('tier') not in en['tier']: err('schema', f"{a['id']}: tier が値域外: {a.get('tier')}")
    if a.get('binds') not in en['binds']: err('schema', f"{a['id']}: binds が値域外: {a.get('binds')}")
    mech_ok(a['id'], a.get('mechanism') or {}, a['tier'])
    if not str(a.get('plain') or '').strip(): err('R-10', f"{a['id']}: plain が無い")
    for x in a.get('rationale') or []:
        if set(x.keys()) != {'kind', 'ref'}: err('schema', f"{a['id']}: rationale の欄が壊れている（flow mapping の「,」）: {sorted(x.keys())}")
        elif x['kind'] not in en['rationale_kind']: err('schema', f"{a['id']}: rationale.kind が値域外: {x['kind']}")
    if a.get('retreat'):
        if set(a['retreat'].keys()) != {'kind', 'condition'}: err('schema', f"{a['id']}: retreat の欄が {sorted(a['retreat'].keys())}")
        elif a['retreat'].get('kind') not in en['retreat_kind']: err('schema', f"{a['id']}: retreat.kind が値域外")
    if not a.get('statements'): err('schema', f"{a['id']}: 規範文が 0 本")
    for st in a.get('statements') or []:
        if set(st.keys()) != set(sc['statement']['required']): err('schema', f"{st.get('id')}: 規範文の欄が {sorted(st.keys())}")
        if st.get('pattern') not in en['pattern']: err('schema', f"{st['id']}: pattern が値域外: {st.get('pattern')}")
        if st.get('strength') not in en['strength']: err('schema', f"{st['id']}: strength が値域外: {st.get('strength')}")
        t = str(st.get('text', '')).strip()
        if not t.endswith('。'): err('schema', f"{st['id']}: 「。」で終わらない")
        if t.count('。') != 1: err('schema', f"{st['id']}: 1 文でない（「。」が {t.count('。')}）")
        neg = t.rstrip('。').endswith('ない')
        if (st.get('strength') == 'must-not') != neg: err('R-11', f"{st['id']}: strength={st.get('strength')} と文末「…{t[-8:]}」が不一致")
        if not st['id'].startswith(a['id'] + '.'): err('schema', f"{st['id']}: 条 id {a['id']} の枝番でない")
        st_ids.add(st['id'])
cnt = collections.Counter(a['tier'] for a in c['articles'])
for k, n in c['meta']['counts'].items():
    if cnt.get(k, 0) != n: err('counts', f"meta.counts.{k}={n} だが実数 {cnt.get(k, 0)}")

# ── rules ──
rs = r['schema']; ren = rs['enums']
if set(r.keys()) - set(rs['top_level']): err('rules', f"rules の未知の節（N-3）: {sorted(set(r.keys()) - set(rs['top_level']))}")
rule_ids = []; rows = {}
for sect, spec in (('thresholds', rs['threshold_row']), ('discipline', rs['discipline_row'])):
    for row in r.get(sect) or []:
        rid = row.get('id'); rule_ids.append(rid); rows[rid] = (sect, row)
        keys_ok('rules', rid, row, spec)
        if row.get('kind') not in ren['kind']: err('rules', f"{rid}: kind が値域外: {row.get('kind')}")
        if row.get('status') not in ren['status']: err('rules', f"{rid}: status が値域外: {row.get('status')}")
        if 'stage' in row and row.get('stage') not in ren['stage']: err('rules', f"{rid}: stage が値域外: {row.get('stage')}")
        if row.get('article') not in ids: err('refs', f"{rid}: article {row.get('article')} が条に無い")
        if row.get('status') == '凍結' and not row.get('ruling'): err('rules', f"{rid}: 凍結なのに裁定 id が無い（P-17）")
if len(rule_ids) != len(set(rule_ids)): err('rules', '行 id が重複')
art_mech = {a['id']: a['mechanism']['kind'] for a in c['articles']}
for rid, (sect, row) in rows.items():
    if sect != 'thresholds': continue
    allowed = rs['kind_map_to_constitution'].get(row['kind'], [])
    if art_mech.get(row['article']) not in allowed: err('rules', f"{rid}: kind {row['kind']} と条 {row['article']} の機構 {art_mech.get(row['article'])} が写像表に合わない")

# ── adr（判断の記録の正本・P-8 / A-2 / N-4 の live: adr・ADR-1）──
ADR_DIR = HERE / 'adr'; ANCH_DIR = HERE / 'anchors'
A22_MIN = {'id', 'title', 'tier', 'binds', 'statements'}   # A-2.2「条文（id・見出し・規範文・段・縛る相手）」の機械形。adr/schema.yaml はこれと一致を要る（下限を data 側で動かせない）
ST_FIELDS = ('text', 'pattern', 'strength')               # 規範文の中身（本文・型・強度）。id は欄の道に使う
SCOPE_MIN = {'schema', 'precedence', 'articles'}          # A-2.2「schema 節・前文」+ 条文。憲法 schema.amendment_scope はこれを含む
NEW_MARK, DEL_MARK = '（新設）', '（削除）'
def real_under_here(p, what):   # symlink と design-intent の外の実体を拒む
    ok = True
    if p.is_symlink(): err('adr', f"{what}: symlink は認めない（{p}）"); ok = False
    try: p.resolve().relative_to(HERE)
    except ValueError: err('adr', f"{what}: design-intent の外を指している（{p}）"); ok = False
    return ok
def load_path(p):
    if p.is_symlink(): print(f'check_draft: symlink は認めない: {p}', file=sys.stderr); sys.exit(2)
    if not p.exists(): print(f'check_draft: 正本が無い: {p}', file=sys.stderr); sys.exit(2)
    if not p.is_file(): print(f'check_draft: file でない: {p}', file=sys.stderr); sys.exit(2)
    try: return yaml.load(p.read_text(encoding='utf-8'), Loader=StrictLoader)
    except Exception as ex: print(f'check_draft: parse できない: {p}: {ex}', file=sys.stderr); sys.exit(2)
if ADR_DIR.is_symlink() or not ADR_DIR.is_dir(): print(f'check_draft: adr/ が dir でない（symlink・file・不在）: {ADR_DIR}', file=sys.stderr); sys.exit(2)
asd = load_path(ADR_DIR / 'schema.yaml')
if not isinstance(asd, dict) or set(asd.keys()) - {'meta', 'schema', 'plain'}: print(f"check_draft: adr/schema.yaml の形が違う（節は meta / schema / plain）", file=sys.stderr); sys.exit(2)
asc = asd['schema']; aen = asc['enums']; an = asc['anchor']
if set(an['article_fields_minimum']) != A22_MIN: err('adr', f"adr/schema.yaml anchor.article_fields_minimum {an['article_fields_minimum']} が A-2.2 の機械形 {sorted(A22_MIN)} と違う")
PROJ = list(an['projection_article_fields'])
if list(an.get('statement_fields') or []) != ['id', *ST_FIELDS]: err('adr', f"adr/schema.yaml anchor.statement_fields {an.get('statement_fields')} が床の規範文の射影 {['id', *ST_FIELDS]} と違う")
if not A22_MIN <= set(PROJ): err('anchor', f"adr/schema.yaml の射影の欄集合 {PROJ} が A-2.2 の条文の定義 {sorted(A22_MIN)} を含まない（射影を狭めることはできない）")
SCOPE = list(sc.get('amendment_scope') or [])
if not SCOPE_MIN <= set(SCOPE): err('anchor', f"憲法 schema.amendment_scope {SCOPE} が A-2.2 の母集合 {sorted(SCOPE_MIN)} を含まない")
if aen['retreat_kind'] != en['retreat_kind']: err('adr', f"adr/schema.yaml の retreat_kind {aen['retreat_kind']} が憲法の値域 {en['retreat_kind']} と食い違う")
for sid in aen['surface']:
    if sid not in rows: err('adr', f"adr/schema.yaml enums.surface の {sid} が rules 行に無い（対話面は rules 行の id で指す・R-8）")
ADR_ID = re.compile(asc['id_pattern']); DATE_RE = re.compile(asc['date_format']); RULING_RE = re.compile(asc['ruling_pattern']); adrs = {}
def nonempty(x): return bool(str(x if x is not None else '').strip())
def date_ok(kind, where, x):
    if not DATE_RE.match(str(x)): err(kind, f"{where}「{x}」が年-月-日でない")
def approval_ok(kind, where, ap_):
    keys_ok(kind, where, ap_, asc['approval'])
    if not isinstance(ap_, dict): return
    for k in ('ruling', 'verbatim'):
        if not nonempty(ap_.get(k)): err(kind, f"{where}.{k} が空")
    date_ok(kind, f'{where}.date', ap_.get('date'))
    if ap_.get('who') not in aen['approver']: err(kind, f"{where}.who が値域外: {ap_.get('who')}")
    if not RULING_RE.search(str(ap_.get('ruling') or '')): err(kind, f"{where}.ruling「{ap_.get('ruling')}」に台帳 id（{asc['ruling_pattern']}）が無い")
    if ap_.get('surface') not in aen['surface']: err(kind, f"{where}.surface が値域外（rules 行の id で指す）: {ap_.get('surface')}")
for p in sorted(ADR_DIR.glob('*.yaml')):
    if p.name == 'schema.yaml': continue
    if not real_under_here(p, p.name): continue
    d = load_path(p)
    if not isinstance(d, dict): err('adr', f"{p.name}: 判断の記録が欄の表でない"); continue
    aid = str(d.get('id'))
    keys_ok('adr', aid, d, {'required': asc['required'], 'optional': asc['optional']})
    if not ADR_ID.match(aid): err('adr', f"{p.name}: id「{aid}」が形 {asc['id_pattern']} でない（ゼロ詰めしない・4 桁は外部の記録）")
    if p.stem != aid: err('adr', f"{p.name}: file 名が id {aid} と違う（1 判断 = 1 file・file 名 = id）")
    if aid in adrs: err('adr', f"{aid}: id が重複（P-7）"); continue
    adrs[aid] = d
    if d.get('status') not in aen['status']: err('adr', f"{aid}: status が値域外: {d.get('status')}")
    date_ok('adr', f'{aid}.date', d.get('date'))
    for k in asc['non_empty']:
        if not nonempty(d.get(k)): err('adr', f"{aid}: {k} が空")
    opts = d.get('options') if isinstance(d.get('options'), list) else []
    if not isinstance(d.get('options'), list): err('adr', f"{aid}: options が一覧でない")
    if len(opts) < asc['options_rule']['min']: err('adr', f"{aid}: 案が {len(opts)} 件（退けた案を含めて {asc['options_rule']['min']} 件以上）")
    for o in opts:
        keys_ok('adr', f"{aid}.options[{o.get('id') if isinstance(o, dict) else '?'}]", o, asc['option'])
        if not isinstance(o, dict): continue
        if o.get('verdict') not in aen['verdict']: err('adr', f"{aid}.options[{o.get('id')}]: verdict が値域外: {o.get('verdict')}")
        for k in ('name', 'text', 'reason'):
            if not nonempty(o.get(k)): err('adr', f"{aid}.options[{o.get('id')}].{k} が空")
    n_ad = sum(1 for o in opts if isinstance(o, dict) and o.get('verdict') == 'adopted')
    if n_ad != asc['options_rule']['adopted']: err('adr', f"{aid}: 採用の案が {n_ad} 件（{asc['options_rule']['adopted']} 件）")
    rt = d.get('retreat')
    keys_ok('P-8', f'{aid}.retreat', rt, asc['retreat'])
    if isinstance(rt, dict):
        if rt.get('kind') not in aen['retreat_kind']: err('P-8', f"{aid}: retreat.kind が値域外: {rt.get('kind')}")
        if not nonempty(rt.get('condition')): err('P-8', f"{aid}: 撤退条件が空（P-8.1）")
    if not (isinstance(d.get('basis'), list) and d['basis']): err('adr', f"{aid}: basis（根拠の id）が空")
    amends = d.get('amends') if isinstance(d.get('amends'), list) else []
    if d.get('amends') is not None and not isinstance(d.get('amends'), list): err('A-2', f"{aid}: amends が一覧でない")
    for e in amends:
        keys_ok('A-2', f"{aid}.amends[{e.get('target') if isinstance(e, dict) else '?'}]", e, asc['amends_entry'])
        if not isinstance(e, dict): continue
        if e.get('target') not in ids and e.get('target') not in asc['amends_entry']['targets_extra']: err('A-2', f"{aid}: amends の対象 {e.get('target')} が条 id でも {asc['amends_entry']['targets_extra']} でもない")
        for k in ('field', 'version', 'previous_text', 'new_text'):
            if not nonempty(e.get(k)): err('A-2', f"{aid}: amends[{e.get('target')}].{k} が空")
    ap_ = d.get('approval')
    if d.get('status') in asc['effective_status'] and not ap_: err('N-4', f"{aid}: {d.get('status')} なのに approval（逐語・日付・裁定 id・対話面）が無い")
    if ap_ is not None: approval_ok('N-4', f'{aid}.approval', ap_)
    if d.get('grill') is not None:
        keys_ok('A-2', f'{aid}.grill', d['grill'], asc['grill'])
        if isinstance(d['grill'], dict):
            date_ok('A-2', f'{aid}.grill.when', d['grill'].get('when'))
            for k in ('who', 'where', 'summary'):
                if not nonempty(d['grill'].get(k)): err('A-2', f"{aid}.grill.{k} が空")
effective = {k: d for k, d in adrs.items() if d.get('status') in asc['effective_status'] and isinstance(d.get('approval'), dict)}   # 発効した判断（承認欄あり・retired も含む）
for aid, d in adrs.items():
    amends = d.get('amends') if isinstance(d.get('amends'), list) else []
    if amends and aid in effective:
        if d['approval'].get('who') != asc['owner']: err('N-4', f"{aid}: 条文を改訂する発効した判断の承認者が {asc['owner']} でない（{d['approval'].get('who')}）")
        if not isinstance(d.get('grill'), dict): err('A-2', f"{aid}: 条文を改訂する発効した判断に grill の記録が無い（A-2.3）")
    for k in ('supersedes', 'superseded_by'):
        if d.get(k) is not None and str(d[k]) not in adrs: err('adr', f"{aid}: {k} {d[k]} の判断の記録が実在しない")
    if d.get('status') == 'retired' and d.get('superseded_by') is None: err('adr', f"{aid}: retired なのに superseded_by（後継）が無い（P-7.2・消すのでなく置き換える）")
    if d.get('superseded_by') is not None:
        if d.get('status') != 'retired': err('adr', f"{aid}: superseded_by を持つのに status が retired でない（P-7.2）")
        nx = adrs.get(str(d['superseded_by']))
        if nx and str(nx.get('supersedes')) != aid: err('adr', f"{aid}: 後継 {d['superseded_by']} の supersedes に {aid} が無い（双方向）")
    if d.get('supersedes') is not None:
        pv_ = adrs.get(str(d['supersedes']))
        if pv_ and str(pv_.get('superseded_by')) != aid: err('adr', f"{aid}: 置き換えた {d['supersedes']} の superseded_by が {aid} でない（双方向）")
for x in (asd.get('meta') or {}).get('decided_by') or []:
    if str(x) not in adrs: err('adr', f"adr/schema.yaml meta.decided_by の {x} が実在しない（欄の決まりの出所の判断が消えている）")
if (asd.get('meta') or {}).get('decided_by') is None or not (asd.get('meta') or {}).get('decided_by'): err('adr', "adr/schema.yaml meta.decided_by が空（欄の決まりの出所の判断が無い）")

# ── refs（R-4・母集団 = 4 file + 判断の記録の全欄）──
req_ids = set()
for sect in ('goals', 'requirements', 'nonfunctional', 'acceptance', 'constraints', 'actors', 'outputs'):
    for x in s.get(sect) or []: req_ids.add(x['id'])
hist_ids = set()   # 凍結 anchor の鎖に一度でも在った条・規範文の id（廃止は番号を空けたままにする＝P-7.2・記録はその番号を名指してよい）
for _p in (sorted((HERE / 'anchors').glob('constitution-*.yaml')) if (HERE / 'anchors').is_dir() else []):
    try:
        _d = yaml.load(_p.read_text(encoding='utf-8'), Loader=StrictLoader)
        for _a in ((_d.get('articles') or []) if isinstance(_d, dict) else []):
            if isinstance(_a, dict): hist_ids.add(str(_a.get('id'))); hist_ids |= {str(_st.get('id')) for _st in (_a.get('statements') or []) if isinstance(_st, dict)}
    except Exception: pass
known_ids = set(ids) | st_ids | req_ids | set(rule_ids) | hist_ids   # R-4 の内部 3 空間（過去の版の id を含む）。判断の記録の id は A-2 の機構で別に解決する
sections = {'§5', '§6', '§7', '§8'}
ID_RE = re.compile(r'(?<![A-Za-z0-9-])((?:P|A|N)-\d+(?:\.\d+)?|(?:FR|NFR|AC|CON|GOAL)\d+|(?:R|D)-\d+)(?![A-Za-z0-9])')
ADR_RE = re.compile(r'(?<![A-Za-z0-9-])(ADR-[1-9][0-9]*)(?![A-Za-z0-9])')   # 内部の判断の記録の id（4 桁 ADR-0047 は外部の参照で数えない）
def walk(obj, where):
    if isinstance(obj, dict):
        for k, vv in obj.items(): walk(vv, f'{where}.{k}')
    elif isinstance(obj, list):
        for i, vv in enumerate(obj): walk(vv, f'{where}[{i}]')
    elif isinstance(obj, str):
        for m in ID_RE.findall(obj):
            if m not in known_ids: err('refs', f"{where}: id {m} が実在しない")
        for m in ADR_RE.findall(obj):
            if m not in adrs: err('A-2', f"{where}: 判断の記録 {m} が実在しない")
for name, obj in (('憲法', {k: (vv if k != 'meta' else {kk: x for kk, x in vv.items() if not kk.startswith('changes_from')}) for k, vv in c.items() if k != 'schema'}), ('rules', {k: vv for k, vv in r.items() if k != 'schema'}), ('語彙', v), ('要件書', s)):
    walk(obj, name)
for aid, d in adrs.items(): walk(d, aid)
referenced_rules = set()
for a in c['articles']:
    rel = a.get('relations') or {}
    if not isinstance(rel, dict): err('refs', f"{a['id']}: relations が型付き map でない"); continue
    for k in rel:
        if k not in ('reqs', 'rules', 'articles', 'sections'): err('refs', f"{a['id']}: relations の未知の名前空間 {k}")
    for x in rel.get('sections', []):
        if x not in sections: err('refs', f"{a['id']}: 節 {x} が無い")
    referenced_rules |= set(rel.get('rules', []))
    for st in a['statements']:
        referenced_rules |= set(re.findall(r'\b([RD]-\d+)\b', st['text']))
for rid in rule_ids:
    if rid not in referenced_rules: err('R-4', f"rules 行 {rid} はどの条からも参照されていない（双方向）")
art_rules = {a['id']: set((a.get('relations') or {}).get('rules', [])) for a in c['articles']}
for rid, (sect, row) in rows.items():
    if rid not in art_rules.get(row['article'], set()): err('R-4', f"{rid}: article={row['article']} だが {row['article']} の relations.rules に無い")

# ── amended_by ⇔ amends（A-2 / N-4 の双方向・ADR-1）──
ab_spec = asc['amended_by_entry']; art_by_id = {a['id']: a for a in c['articles']}
def amends_of(aid, target): return [e for e in (adrs[aid].get('amends') if isinstance(adrs[aid].get('amends'), list) else []) if isinstance(e, dict) and e.get('target') == target]
for a in c['articles']:
    ams = a.get('amended_by')
    if ams is not None and not isinstance(ams, list): err('A-2', f"{a['id']}: amended_by が一覧でない"); continue
    for am in ams or []:
        keys_ok('A-2', f"{a['id']}.amended_by", am, ab_spec)
        if not isinstance(am, dict): continue
        for k in ('approved_by', 'ruling', 'previous_text', 'rationale'):
            if not nonempty(am.get(k)): err('N-4', f"{a['id']}: amended_by.{k} が空")
        date_ok('N-4', f"{a['id']}.amended_by.date", am.get('date'))
        if not RULING_RE.search(str(am.get('ruling') or '')): err('N-4', f"{a['id']}: amended_by.ruling「{am.get('ruling')}」に台帳 id が無い")
        ref = adrs.get(str(am.get('adr')))
        if not ref: err('N-4', f"{a['id']}: amended_by.adr {am.get('adr')} の判断の記録が実在しない"); continue
        if str(am.get('adr')) not in effective: err('N-4', f"{a['id']}: amended_by.adr {am['adr']} が発効していない（status {ref.get('status')}・承認欄 {'有' if isinstance(ref.get('approval'), dict) else '無'}）"); continue
        if am.get('approved_by') != ref['approval'].get('who'): err('N-4', f"{a['id']}: amended_by.approved_by「{am.get('approved_by')}」が {am['adr']} の承認者「{ref['approval'].get('who')}」と違う")
        if str(am.get('previous_text')) not in {str(e.get('previous_text')) for e in amends_of(str(am['adr']), a['id'])}: err('A-2', f"{a['id']}: amended_by.previous_text が {am['adr']} の amends（対象 {a['id']}）のどれとも一致しない")
for aid in effective:
    for t in {e.get('target') for e in amends_of(aid, None) or []} if False else {e.get('target') for e in (adrs[aid].get('amends') if isinstance(adrs[aid].get('amends'), list) else []) if isinstance(e, dict)}:
        if t in art_by_id and not any(isinstance(am, dict) and str(am.get('adr')) == aid for am in art_by_id[t].get('amended_by') or []): err('A-2', f"{aid}: {t} の amended_by に {aid} が無い（双方向）")

# ── anchor（凍結 anchor の鎖・A-2 / N-4 の差分検査の比較元・P-10.2 の限界を自認・ADR-2）──
INDEX = ANCH_DIR / an['index_file']; DIGEST_ALGO = an['digest_algo']; first_ver = str(an['first_version'])
def project(doc):
    out = {k: doc.get(k) for k in SCOPE if k != 'articles'}
    out['articles'] = [{k: ([{f: st.get(f) for f in ('id',) + ST_FIELDS} for st in (a.get('statements') or [])] if k == 'statements' else a.get(k)) for k in PROJ} for a in doc.get('articles') or []]
    return out
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=str)
def digest_of(anchor_doc): return hashlib.sha256(canon({k: vv for k, vv in anchor_doc.items() if k != 'digest'}).encode('utf-8')).hexdigest()
def flow(x): return yaml.safe_dump(x, allow_unicode=True, sort_keys=False, default_flow_style=True, width=10**6).strip()
def flatten(obj, prefix, out):   # 節を「欄の道 → 値」に平らにする。一覧は flow 形式の 1 値（一覧の中身の一覧・表は道を伸ばす）
    if isinstance(obj, dict):
        for k, vv in obj.items(): flatten(vv, f'{prefix}.{k}' if prefix else str(k), out)
    elif isinstance(obj, list):
        if all(not isinstance(x, (dict, list)) for x in obj): out[prefix] = flow(obj)
        else:
            for n, x in enumerate(obj): flatten(x, f'{prefix}[{n}]', out)
    else: out[prefix] = str(obj)
    return out
def flat_article(a):
    out = {k: str(a.get(k)) for k in PROJ if k not in ('id', 'statements')}
    sts = a.get('statements') or []
    for st in sts:
        for f in ST_FIELDS: out[f"statements.{st.get('id')}.{f}"] = str(st.get(f))
    return out
def flat_targets(proj):   # 対象 → 欄の道 → 値。対象 = 各条 id・schema・precedence・articles（条の並び）
    out = {t: flatten(proj.get(t), '', {}) for t in SCOPE if t != 'articles'}
    for a in proj['articles']: out[str(a.get('id'))] = flat_article(a)
    return out
def order_diff(prev_ids, cur_ids):   # 並びの差分は両側に在る id だけで見る（足した・消した id は欄の差分の側で数える）
    common = set(prev_ids) & set(cur_ids)
    a = '・'.join(x for x in prev_ids if x in common); b = '・'.join(x for x in cur_ids if x in common)
    return None if a == b else (a, b)
cur_proj = project(c); cur_ver = str(c['meta']['version']); meta_approval = c['meta'].get('approval')
def ver_key(vs): return tuple(int(x) for x in re.findall(r'\d+', str(vs)))
pending = []; anchors = {}; index = None
if ANCH_DIR.exists() or ANCH_DIR.is_symlink():
    if ANCH_DIR.is_symlink() or not ANCH_DIR.is_dir(): print(f'check_draft: anchors/ が dir でない（symlink か file）: {ANCH_DIR}', file=sys.stderr); sys.exit(2)
    if INDEX.exists():
        if real_under_here(INDEX, INDEX.name):
            index = load_path(INDEX)
            if not (isinstance(index, dict) and index.get('kind') == 'constitution-anchor-index' and isinstance(index.get('entries'), list)): err('anchor', f"{INDEX.name}: 索引の形が違う"); index = None
    for p in sorted(ANCH_DIR.glob('constitution-*.yaml')):
        if not real_under_here(p, p.name): continue
        d = load_path(p)
        if not isinstance(d, dict) or set(d.keys()) != set(an['file_keys']) or d.get('kind') != 'constitution-anchor': err('anchor', f"{p.name}: anchor の欄が壊れている: {sorted(d.keys()) if isinstance(d, dict) else type(d).__name__}"); continue
        vs = str(d['version'])
        if p.name != an['file_name'].replace('<version>', vs): err('anchor', f"{p.name}: file 名が版 {vs} と違う")
        if vs in anchors: err('anchor', f"{p.name}: 版 {vs} の anchor が重複"); continue
        if d.get('digest_algo') != DIGEST_ALGO: pending.append(f"{p.name}: digest の方式 {d.get('digest_algo')} が床の {DIGEST_ALGO} と違う＝照合できない（まだ分からない）"); continue
        if digest_of(d) != str(d.get('digest')): err('anchor', f"{p.name}: digest が中身と一致しない（anchor のどこかが手で変えられた）")
        if list(d.get('projection_article_fields') or []) != PROJ: err('anchor', f"{p.name}: anchor の射影の欄集合 {d.get('projection_article_fields')} と adr/schema.yaml の {PROJ} が食い違う（射影を変えた）")
        if d.get('meta_approval') != meta_approval: err('N-4', f"{p.name}: anchor の meta_approval（発効の承認の写し）が憲法 meta.approval と一致しない（承認の記録が書き換えられた・P-12.2）")
        aps = d.get('approvals')
        if not (isinstance(aps, list) and aps): err('anchor', f"{p.name}: 承認の一覧（approvals）が空")
        else:
            for n, ap_ in enumerate(aps):
                if not isinstance(ap_, dict) or not nonempty(ap_.get('ruling')) or not nonempty(ap_.get('verbatim')) or not nonempty(ap_.get('who')): err('anchor', f"{p.name}: approvals[{n}] に who / ruling / verbatim が無い")
                elif not RULING_RE.search(str(ap_.get('ruling'))): err('anchor', f"{p.name}: approvals[{n}].ruling に台帳 id が無い")
        anchors[vs] = (d, p)
tracked_anchor_files = None   # 版管理（HEAD）にある anchor file 名。git が無ければ None（分からない）
try:
    import subprocess
    _top = subprocess.run(['git', '-C', str(HERE), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, timeout=20)
    if _top.returncode == 0:
        _rel = HERE.resolve().relative_to(pathlib.Path(_top.stdout.strip()).resolve()) / an['dir']
        _ls = subprocess.run(['git', '-C', _top.stdout.strip(), 'ls-tree', '-r', '--name-only', 'HEAD', '--', str(_rel)], capture_output=True, text=True, timeout=20)
        if _ls.returncode == 0: tracked_anchor_files = {pathlib.Path(x).name for x in _ls.stdout.split()}
except Exception: tracked_anchor_files = None
present_anchor_files = {p.name for p in ANCH_DIR.glob('*.yaml')} if ANCH_DIR.is_dir() else set()
for _missing in sorted((tracked_anchor_files or set()) - present_anchor_files): err('anchor', f"anchors/{_missing} は版管理（HEAD）にあるが作業ツリーに無い（anchor と索引は消さない）")
records_exist = any(isinstance(a.get('amended_by'), list) and a['amended_by'] for a in c['articles']) or any(isinstance(d.get('amends'), list) and d['amends'] for d in effective.values())
prev_anchor = None; newest = None; freeze_plan = None
if index is not None:
    ents = index['entries']
    for n, e in enumerate(ents):
        if not isinstance(e, dict) or not {'version', 'previous', 'digest'} <= set(e.keys()): err('anchor', f"{INDEX.name}: entries[{n}] の欄が壊れている"); continue
        vs = str(e['version']); expect_prev = None if n == 0 else str(ents[n - 1].get('version'))
        if n == 0 and vs != first_ver: err('anchor', f"{INDEX.name}: 鎖の根 {vs} が最初の版 {first_ver}（adr/schema.yaml anchor.first_version）でない")
        if (None if e.get('previous') is None else str(e['previous'])) != expect_prev: err('anchor', f"{INDEX.name}: entries[{n}]（{vs}）の previous {e.get('previous')} が直前の版 {expect_prev} でない（鎖の付け替え）")
        if vs not in anchors: pending.append(f"anchor の鎖が切れている: 索引にある版 {vs} の anchor file が無い（消された）＝差分検査は「まだ分からない」（P-10.3）。anchors/ は消さない"); continue
        d = anchors[vs][0]
        if str(d.get('digest')) != str(e['digest']): err('anchor', f"{vs}: anchor の digest が索引の記載と違う（差し替えられた）")
        if (None if d.get('previous') is None else str(d['previous'])) != expect_prev: err('anchor', f"{vs}: anchor の previous {d.get('previous')} が索引の鎖 {expect_prev} と違う")
    listed = {str(e.get('version')) for e in ents if isinstance(e, dict)}
    for extra in sorted(set(anchors) - listed): err('anchor', f"anchor {extra} が索引に無い（鎖の外の anchor）")
    if ents and isinstance(ents[-1], dict): newest = str(ents[-1].get('version'))
elif anchors: err('anchor', f"anchor file はあるが索引（{INDEX.name}）が無い（消された）")
elif records_exist: err('N-4', "改訂の記録（amended_by か発効した判断の amends）があるのに anchor が 1 本も無い＝anchor が消された（鎖の始め直しは認めない）")
if args.freeze_anchor:
    if newest is not None and newest in anchors and ver_key(newest) >= ver_key(cur_ver): print(f'check_draft: 版 {cur_ver} は最新 anchor {newest} より新しくない（同じ版は上書きしない・版を上げてから）', file=sys.stderr); sys.exit(1)
    if newest is None and cur_ver != first_ver: err('anchor', f"最初の anchor は版 {first_ver}（adr/schema.yaml anchor.first_version）でなければならない＝{cur_ver} で鎖を始め直すことはできない")
    if newest is None and (tracked_anchor_files or records_exist): err('anchor', "anchor が版管理か記録の上では存在した（消された）ので、鎖を始め直す凍結は認めない")
    if newest is not None and newest in anchors: prev_anchor = anchors[newest][0]
else:
    if index is None and not anchors and not records_exist: pending.append(f"凍結 anchor が 0 本（{ANCH_DIR}）＝A-2 / N-4 の差分検査は「まだ分からない」（P-10.3）。発効版で --freeze-anchor を実行する")
    elif newest is not None and newest in anchors:
        nd, np_ = anchors[newest]
        if newest != cur_ver: err('A-2', f"憲法の版 {cur_ver} と最新 anchor の版 {newest} が違う＝版を上げたのに凍結していない（--freeze-anchor）か、版を上げずに直した")
        elif {k: nd.get(k) for k in SCOPE} != cur_proj: err('N-4', f"現行の条文（{'・'.join(SCOPE)} の射影）が凍結 anchor {np_.name} と一致しない＝判断の記録と承認を伴わない改憲（N-4.1）")
        pv0 = nd.get('previous')
        if pv0 is not None and str(pv0) in anchors: prev_anchor = anchors[str(pv0)][0]
this_ver_adrs = {k: d for k, d in effective.items() if any(isinstance(e, dict) and str(e.get('version')) == cur_ver for e in (d.get('amends') if isinstance(d.get('amends'), list) else []))}
def diff_targets(prev_proj, cur_p):   # 対象 → 欄の道 → (前, 今)。無い側は印
    pf, cf = flat_targets(prev_proj), flat_targets(cur_p); out = {}
    for t in set(pf) | set(cf):
        pt_, ct_ = pf.get(t, {}), cf.get(t, {}); ch = {}
        for k in set(pt_) | set(ct_):
            if pt_.get(k) != ct_.get(k): ch[k] = (pt_.get(k, NEW_MARK), ct_.get(k, DEL_MARK))
        if ch: out[t] = ch
    od = order_diff([str(a.get('id')) for a in prev_proj['articles']], [str(a.get('id')) for a in cur_p['articles']])
    if od: out.setdefault('articles', {})['order'] = od
    pa_ = {str(a.get('id')): a for a in prev_proj['articles']}; ca_ = {str(a.get('id')): a for a in cur_p['articles']}
    for i_ in set(pa_) & set(ca_):
        od = order_diff([str(st.get('id')) for st in pa_[i_].get('statements') or []], [str(st.get('id')) for st in ca_[i_].get('statements') or []])
        if od: out.setdefault(i_, {})['statements.order'] = od
    return out
if prev_anchor is not None:
    prev = {k: prev_anchor.get(k) for k in SCOPE}; pv = str(prev_anchor['version'])
    changed = diff_targets(prev, cur_proj)
    if args.emit_amends:
        print(f'# 最新 anchor {pv} → 現行（版 {cur_ver}）の欄単位の差分。amends に写す（version は上げる版に直す）')
        for t, ch in sorted(changed.items()):
            for k, (pv_, cv_) in sorted(ch.items()): print(yaml.safe_dump([{'target': t, 'field': k, 'version': cur_ver, 'previous_text': pv_, 'new_text': cv_}], allow_unicode=True, sort_keys=False, default_flow_style=True, width=10**6).strip())
        sys.exit(0)
    prev_ids = {str(a.get('id')) for a in prev['articles']}; cur_ids = {str(a.get('id')) for a in cur_proj['articles']}
    for i_ in sorted(prev_ids - cur_ids): err('P-7', f"条 {i_} が anchor {pv} に在って現行に無い（番号は消さない・廃止は状態で）")
    recorded = {}   # (対象, 欄の道) → (adr, entry)
    for aid, d in this_ver_adrs.items():
        for e in d['amends']:
            if not isinstance(e, dict) or str(e.get('version')) != cur_ver: continue
            key = (str(e.get('target')), str(e.get('field')))
            if key in recorded: err('A-2', f"{aid}: {key[0]}.{key[1]} の改訂が {recorded[key][0]} と重複して記録されている")
            recorded[key] = (aid, e)
    for t, ch in changed.items():
        if t in prev_ids - cur_ids: continue
        for k, (pv_, cv_) in ch.items():
            rec = recorded.pop((t, k), None)
            if rec is None: err('N-4', f"{t}.{k} が anchor {pv} から変わったが、それを amends（version {cur_ver}・field）に持つ発効した判断の記録が無い（前「{pv_[:40]}」→ 今「{cv_[:40]}」）"); continue
            aid, e = rec
            if str(e.get('previous_text')) != pv_ or str(e.get('new_text')) != cv_: err('A-2', f"{aid}: {t}.{k} の previous_text / new_text が anchor {pv} と現行の値に完全一致しない（前「{pv_[:40]}」今「{cv_[:40]}」）")
        if t in art_by_id and t in ch:
            pass
    for (t, k), (aid, e) in recorded.items(): err('A-2', f"{aid}: amends が {t}.{k} の改訂を記録しているが、anchor {pv} と現行に差分が無い（記録と差分が食い違う）")
    for t in changed:
        if t in art_by_id and not any(isinstance(am, dict) and str(am.get('adr')) in this_ver_adrs for am in art_by_id[t].get('amended_by') or []): err('N-4', f"{t} が anchor {pv} から変わったが、その版の判断の記録を指す amended_by が無い")
    if args.freeze_anchor and not changed: err('A-2', f"版を {pv} → {cur_ver} に上げたが条文（{'・'.join(SCOPE)}）に差分が無い（意味の無い版上げは凍結しない）")
    if args.freeze_anchor and not this_ver_adrs: err('N-4', f"版 {cur_ver} を凍結するには、その版を amends に持つ発効した判断の記録（持ち主の承認）が要る")
elif args.emit_amends: print('# 比較元の anchor が無い（最初の版か、鎖が切れている）'); sys.exit(2 if pending else 0)
if args.freeze_anchor:
    aps = [{'adr': k, **{f: d['approval'].get(f) for f in ('who', 'date', 'ruling', 'verbatim')}} for k, d in this_ver_adrs.items()] if prev_anchor is not None else [{'adr': None, **{f: (meta_approval or {}).get(f) for f in ('who', 'date', 'ruling', 'verbatim')}}]
    fz = {'kind': 'constitution-anchor', 'digest_algo': DIGEST_ALGO, 'version': cur_ver, 'previous': newest if prev_anchor is not None else None, 'projection_article_fields': PROJ, 'meta_approval': meta_approval, 'approvals': aps, **cur_proj}
    fz['digest'] = digest_of(fz); freeze_plan = (ANCH_DIR / an['file_name'].replace('<version>', cur_ver), fz)

# ── vocab（R-9 / R-12 の機械側）──
known = set()
for t in (v.get('terms') or []) + (v.get('field_terms') or []):
    for w in re.findall(r'[A-Za-z][A-Za-z0-9\-\.]*[A-Za-z0-9]|[A-Za-z]', (t.get('term') or '') + ' ' + (t.get('en') or '')): known.add(w.lower())
for g in v.get('identifiers') or []:
    for w in g.get('words') or []: known.add(str(w).lower())
IDENT = re.compile(r'^(P|A|N|FR|NFR|AC|CON|GOAL|R|D)-?\d|^ADR-[1-9][0-9]*$|^ADR-n$|^[RD]-n$|^[a-z]\d-[0-9a-z]+(\.\d+)?$')   # 4 桁の ADR-0047 は免除しない（外部の参照は「日本語（原語）」の形で書く）   # 条・要件・rules 行の id / R-n・D-n / 台帳 id（f2-648・s2-07l.149）
GLOSS = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff][^（）]*?（([^（）]*)）')   # 「日本語（原語）」の形＝グロス済み（R-12 の免除）
def words(text): return re.findall(r'[A-Za-z][A-Za-z0-9\-\.]*[A-Za-z0-9]|[A-Za-z]', text)
body = []
for a in c['articles']:
    body.append((a['id'] + ' title', a['title'])); body.append((a['id'] + ' plain', a['plain']))
    for st in a['statements']: body.append((st['id'], st['text']))
body.append(('前文', pr.get('text', ''))); body.append(('前文 plain', pr.get('plain', '')))
for sect in ('thresholds', 'discipline'):
    for row in r.get(sect) or []: body.append((row['id'] + ' what', str(row['what'])))
for sect in ('requirements', 'nonfunctional'):
    for x in s.get(sect) or []:
        for k in ('title', 'when', 'shall', 'plain'): body.append((f"要件書 {x['id']} {k}", str(x.get(k, ''))))
for x in s.get('acceptance') or []:
    for k in ('title', 'plain'): body.append((f"要件書 {x['id']} {k}", str(x.get(k, ''))))
for x in s.get('constraints') or []:
    for k in ('title', 'text'): body.append((f"要件書 {x['id']} {k}", str(x.get(k, ''))))
for x in s.get('goals') or []: body.append((f"要件書 {x['id']}", x.get('title', '') + ' ' + x.get('text', '')))
for t in v.get('terms') or []: body.append((f"語彙 {t['id']} def", str(t.get('short', '')) + ' ' + str(t.get('def', ''))))
ADR_ROW = asc['plain_language_rules_row']   # 判断の記録の本文の英字語を数える rules 行（無ければ規則は無い＝数えない・N-2）
adr_body = []
for aid, d in adrs.items():
    for k in ('title', 'context', 'decision', 'plain'): adr_body.append((f'{aid} {k}', str(d.get(k) or '')))
    adr_body.append((f'{aid} retreat', str((d.get('retreat') if isinstance(d.get('retreat'), dict) else {}).get('condition') or '')))
    for o in (d.get('options') if isinstance(d.get('options'), list) else []): adr_body.append((f"{aid} option {o.get('id') if isinstance(o, dict) else '?'}", ' '.join(str(o.get(k) or '') for k in ('name', 'text', 'reason')) if isinstance(o, dict) else ''))
    for x in d.get('consequences') or []: adr_body.append((f'{aid} consequences', str(x)))
adr_body.append(('adr schema plain', str(asd.get('plain') or '')))
body += adr_body
if ADR_ROW not in rows: err('rules', f"adr/schema.yaml plain_language_rules_row の {ADR_ROW} が rules 行に無い")
elif '判断の記録' not in str(rows[ADR_ROW][1].get('population', '')): print(f"# 注: rules 行 {ADR_ROW} の population が判断の記録を名指していない（実装は数えている＝行の更新に裁定 id が要る・P-17.1）", file=sys.stderr)
unknown = collections.Counter()
for where, text in body:
    glossed = {x.lower() for g in GLOSS.findall(text) for x in words(g)}
    for w in words(text):
        lw = w.lower()
        if IDENT.match(w) or lw in known or lw in glossed or re.fullmatch(r'[a-z]', lw) or ('--' + w) in text: continue
        unknown[(lw, where)] += 1
for (lw, where), n in sorted(unknown.items()):
    err('R-9', f"{where}: 語彙に無い英字の語「{lw}」")

# ── inject（母集団の本数が導出器と一致）──
try:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import inject_check
    _, n_inj = inject_check.derive(HERE / ('constitution' + SUF))
    n_expect = sum(len(a['statements']) for a in c['articles']) + (1 if pr.get('text') else 0)
    if n_inj != n_expect: err('inject', f"注入の本数 {n_inj} ≠ 前文 + 規範文 {n_expect}")
except Exception as ex:
    err('inject', f"inject_check.derive を呼べない: {ex}")

# ── polarity（極性一覧・P-18.3）──
pol = []
for a in c['articles']:
    m = a['mechanism']
    if m.get('kind') in sc['mechanism']['stage_polarity_required_for']: pol.append((a['id'], m['kind'], m.get('stage'), m.get('polarity'), m.get('live')))
for rid, (sect, row) in rows.items():
    if sect == 'thresholds' and row.get('kind') in ('deny', 'build-check'): pol.append((rid, row['kind'], row.get('stage'), 'fail-closed', 'row'))
inloop = [x for x in pol if x[2] == 'in-loop']

# ── 出力 ──
by = collections.Counter(k for k, _ in errs)
for k, m in errs: print(f'[{k}] {m}')
n_st = sum(len(a['statements']) for a in c['articles'])
print(f"# 極性一覧: {len(pol)} 件（in-loop {len(inloop)} / post {len(pol) - len(inloop)}）。P-18.4（in-loop 0 なら落とす）= " + ('合格' if inloop else 'まだ分からない（live delivery-0・便 0 で編集時 guard が入るまで）'), file=sys.stderr)
print(f"# 条 {len(ids)}（{dict(cnt)}）/ 規範文 {n_st} / rules 行 {len(rule_ids)} / 語彙 {len(v.get('terms') or [])} 語 + 欄 {len(v.get('field_terms') or [])} + 識別子 {sum(len(g.get('words') or []) for g in (v.get('identifiers') or []))} / 判断の記録 {len(adrs)} / anchor {len(anchors)} / 違反 {len(errs)} {dict(by)}", file=sys.stderr)
if args.freeze_anchor:   # 凍結は全検査の後・0 違反かつ「まだ分からない」が無いときだけ（床が落ちる憲法・鎖の切れた木を anchor にしない）
    if errs or pending: print(f'check_draft: 凍結しない — 違反 {len(errs)} 件・まだ分からない {len(pending)} 件を直してから --freeze-anchor', file=sys.stderr)
    elif freeze_plan is None: print('check_draft: 凍結しない — 凍結の計画が立たなかった', file=sys.stderr); errs.append(('anchor', '凍結できない'))
    else:
        fp, fz = freeze_plan; ANCH_DIR.mkdir(exist_ok=True)
        ents = (index or {'entries': []})['entries'] + [{'version': fz['version'], 'previous': fz['previous'], 'digest': fz['digest']}]
        fp.write_text(f"# folio2 憲法 {cur_ver} の凍結 anchor（ADR-2）。条文の射影（{'・'.join(SCOPE)}・条は {'・'.join(PROJ)}・規範文は id・{'・'.join(ST_FIELDS)}）+ 発効の承認の写し + この版の承認 + digest。手で直さない・消さない・同じ版は上書きしない（check_draft.py --freeze-anchor が全検査 0 違反のときだけ作る）。\n" + yaml.safe_dump(fz, allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8')
        INDEX.write_text("# folio2 凍結 anchor の索引（追記のみ・ADR-2）。鎖 = entries の順。手で直さない・消さない。\n" + yaml.safe_dump({'kind': 'constitution-anchor-index', 'entries': ents}, allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8')
        print(f'check_draft: 凍結した: {fp}（条 {len(cur_proj["articles"])}・previous {fz["previous"]}・承認 {len(fz["approvals"])} 件）・索引 {INDEX.name} に追記', file=sys.stderr)
for u in pending: print(f'# まだ分からない: {u}', file=sys.stderr)
sys.exit(1 if errs else (2 if pending else 0))
