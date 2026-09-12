#!/usr/bin/env python3
"""folio2 design-intent の床（day-1 の暫定 script・M0 で folio の検査に置換する）。使い方: python3 scripts/check_draft.py（repo root で・design-intent/*.yaml を読む）。

検査（すべて決定的・fail-closed: 読めない／parse できないは rc 2）:
  schema  : 憲法 schema 節の top_level / meta / precedence / article / statement / mechanism の欄集合（未知の欄は落とす = N-3）
            enums / tier_mechanism_allowed / live / stage・polarity（reject・build-check に必須）/ 1 文 1 極性（R-11）/ plain 必須（R-10）
  refs    : 参照 id の未解決 0（R-4・母集団 = 正本 4 file の全欄・内部 3 空間 = 要件書 id・条 id〔枝番含む〕・rules 行 id）
            どの条からも参照されない rules 行 0（R-4 双方向）/ rules 行の article ⇔ 条の relations.rules
  rules   : rules schema（top_level / 行の欄 / enums / 凍結行の裁定 id）/ kind_map（R 行だけ）
  vocab   : 本文（憲法の見出し・規範文・平易文・前文 / rules の what / 要件書の見出し・規範文・平易文・制約）の英字の語のうち
            語彙（terms・field_terms の term / en・identifiers）に無いもの（R-9・R-12 の機械側）/ 語彙の定義の閉包（定義文の英字語も同じ母集団）
  inject  : 注入の母集団（前文 + 規範文）の本数が inject_check.derive と一致
  polarity: 極性一覧（P-18.3）を mechanism の stage / polarity と rules 行の stage から生成し、in-loop の本数を出す
            （P-18.4「in-loop 0 なら落とす」は live: delivery-0 ゆえ発効時点では「まだ分からない」として出す）
  adr     : 判断の記録（adr/ADR-n.yaml・schema は adr/schema.yaml・ADR-1）の欄・値域・退けた案（採用 1）・撤退条件の非空（P-8.1）・承認欄（N-4）
            amends ⇔ amended_by の双方向（A-2）。判断の記録の本文は refs（R-4）と vocab（R-9）の母集団にも入る（id 空間は 3 つのまま）
  anchor  : 凍結 anchor（anchors/constitution-<版>.yaml・ADR-2）と現行の射影（schema 節・前文・条の 5 欄）の一致（N-4）・版の一致（A-2）
            anchor の欄集合 ≡ adr/schema.yaml の射影 ⊇ A-2.2 の 5 欄・digest（sha256）の一致・previous の鎖（根 = first_version・切れは rc 2）
            直前 anchor との差分が各条の amended_by と「その版の amends（前の文と今の文の対・完全一致）」で説明されること。anchor 0 本は「まだ分からない」（rc 2）
            --freeze-anchor: 全検査が 0 違反のときだけ現行の射影を anchor として凍結する（検査と同じ射影関数・同じ版は上書きしない・版は最新 anchor より新しい）
  counts  : meta.counts と実数の一致
rc: 0 = 全部通った / 1 = 違反あり / 2 = 読めない・測れない（anchor 0 本）
"""
import re, sys, pathlib, collections, argparse, hashlib
try:
    import yaml
except ImportError:
    print('check_draft: pyyaml が無い', file=sys.stderr); sys.exit(2)

ap = argparse.ArgumentParser(); ap.add_argument('--dir', default='design-intent'); ap.add_argument('--names', default='placed', choices=['draft', 'placed']); ap.add_argument('--freeze-anchor', action='store_true')
args = ap.parse_args()
HERE = pathlib.Path(args.dir).resolve()
SUF = '.draft.yaml' if args.names == 'draft' else '.yaml'
def load(name):
    p = HERE / (name + SUF)
    if not p.exists():
        print(f'check_draft: 正本が無い: {p}', file=sys.stderr); sys.exit(2)
    try:
        return yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as ex:
        print(f'check_draft: parse できない: {p}: {ex}', file=sys.stderr); sys.exit(2)

c = load('constitution'); r = load('rules'); v = load('vocabulary'); s = load('srs')
errs = []
def err(kind, msg): errs.append((kind, msg))
def keys_ok(kind, where, obj, spec):
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
def load_path(p):
    if not p.exists(): print(f'check_draft: 正本が無い: {p}', file=sys.stderr); sys.exit(2)
    try: return yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception as ex: print(f'check_draft: parse できない: {p}: {ex}', file=sys.stderr); sys.exit(2)
asd = load_path(ADR_DIR / 'schema.yaml')
if set(asd.keys()) - {'meta', 'schema', 'plain'}: err('adr', f"adr/schema.yaml の未知の節（N-3）: {sorted(set(asd.keys()) - {'meta', 'schema', 'plain'})}")
asc = asd['schema']; aen = asc['enums']
if aen['retreat_kind'] != en['retreat_kind']: err('adr', f"adr/schema.yaml の retreat_kind {aen['retreat_kind']} が憲法の値域 {en['retreat_kind']} と食い違う")
r8 = next((row for row in r.get('thresholds') or [] if row.get('id') == asc['approval_rule']['surface_rules_row']), None)
if not r8 or not str(r8.get('value', '')).startswith(asc['approval_rule']['surface_prefix']): err('adr', f"rules 行 {asc['approval_rule']['surface_rules_row']} の value が adr/schema.yaml の surface_prefix「{asc['approval_rule']['surface_prefix']}」で始まらない")
ADR_ID = re.compile(asc['id_pattern']); DATE_RE = re.compile(asc['date_format']); adrs = {}
for p in sorted(ADR_DIR.glob('*.yaml')):
    if p.name == 'schema.yaml': continue
    d = load_path(p); aid = str(d.get('id'))
    keys_ok('adr', aid, d, {'required': asc['required'], 'optional': asc['optional']})
    if not ADR_ID.match(aid): err('adr', f"{p.name}: id「{aid}」が形 {asc['id_pattern']} でない（ゼロ詰めしない・4 桁は外部の記録）")
    if p.stem != aid: err('adr', f"{p.name}: file 名が id {aid} と違う（1 判断 = 1 file・file 名 = id）")
    if aid in adrs: err('adr', f"{aid}: id が重複（P-7）")
    adrs[aid] = d
    if d.get('status') not in aen['status']: err('adr', f"{aid}: status が値域外: {d.get('status')}")
    if not DATE_RE.match(str(d.get('date'))): err('adr', f"{aid}: date「{d.get('date')}」が年-月-日でない")
    for k in asc['non_empty']:
        if not str(d.get(k) or '').strip(): err('adr', f"{aid}: {k} が空")
    opts = d.get('options') or []
    if len(opts) < asc['options_rule']['min']: err('adr', f"{aid}: 案が {len(opts)} 件（退けた案を含めて {asc['options_rule']['min']} 件以上）")
    for o in opts:
        keys_ok('adr', f"{aid}.options[{o.get('id')}]", o, asc['option'])
        if o.get('verdict') not in aen['verdict']: err('adr', f"{aid}.options[{o.get('id')}]: verdict が値域外: {o.get('verdict')}")
    n_ad = sum(1 for o in opts if o.get('verdict') == 'adopted')
    if n_ad != asc['options_rule']['adopted']: err('adr', f"{aid}: 採用の案が {n_ad} 件（{asc['options_rule']['adopted']} 件）")
    rt = d.get('retreat') if isinstance(d.get('retreat'), dict) else {}
    keys_ok('P-8', f'{aid}.retreat', rt, asc['retreat'])
    if rt.get('kind') not in aen['retreat_kind']: err('P-8', f"{aid}: retreat.kind が値域外: {rt.get('kind')}")
    if asc['retreat']['condition_non_empty'] and not str(rt.get('condition') or '').strip(): err('P-8', f"{aid}: 撤退条件が空（P-8.1）")
    if asc['basis']['non_empty'] and not d.get('basis'): err('adr', f"{aid}: basis（根拠の id）が空")
    amends = d.get('amends') or []
    for e in amends:
        keys_ok('A-2', f"{aid}.amends[{e.get('target')}]", e, asc['amends_entry'])
        if e.get('target') not in ids and e.get('target') not in asc['amends_entry']['targets_extra']: err('A-2', f"{aid}: amends の対象 {e.get('target')} が条 id でも {asc['amends_entry']['targets_extra']} でもない")
        for k in ('version', 'previous_text', 'new_text'):
            if not str(e.get(k) or '').strip(): err('A-2', f"{aid}: amends[{e.get('target')}].{k} が空")
    ap_ = d.get('approval')
    if d.get('status') == 'accepted' and asc['approval_rule']['accepted_requires_approval'] and not ap_: err('N-4', f"{aid}: accepted なのに approval（逐語・日付・裁定 id）が無い")
    if ap_:
        keys_ok('N-4', f'{aid}.approval', ap_, asc['approval'])
        for k in ('date', 'ruling', 'verbatim'):
            if not str(ap_.get(k) or '').strip(): err('N-4', f"{aid}: approval.{k} が空")
        if not DATE_RE.match(str(ap_.get('date'))): err('N-4', f"{aid}: approval.date「{ap_.get('date')}」が年-月-日でない")
        if ap_.get('who') not in aen['approver']: err('N-4', f"{aid}: approval.who が値域外: {ap_.get('who')}")
        if not str(ap_.get('surface') or '').startswith(asc['approval_rule']['surface_prefix']): err('N-4', f"{aid}: approval.surface が rules 行 {asc['approval_rule']['surface_rules_row']} の対話面で始まらない")
    if amends:
        if d.get('status') == 'accepted' and asc['approval_rule']['amends_requires_owner'] and (not ap_ or ap_.get('who') != '持ち主'): err('N-4', f"{aid}: 条文を改訂する判断の承認者が持ち主でない")
        if asc['approval_rule']['amends_requires_grill'] and not d.get('grill'): err('A-2', f"{aid}: 条文を改訂する判断に grill の記録が無い（A-2.3）")
    if d.get('grill'):
        keys_ok('A-2', f'{aid}.grill', d['grill'], asc['grill'])
        if not DATE_RE.match(str(d['grill'].get('when'))): err('A-2', f"{aid}: grill.when「{d['grill'].get('when')}」が年-月-日でない")
for aid, d in adrs.items():
    for k in ('supersedes', 'superseded_by'):
        if d.get(k) and str(d[k]) not in adrs: err('adr', f"{aid}: {k} {d[k]} の判断の記録が実在しない")
    if d.get('superseded_by'):
        if d.get('status') != 'retired': err('adr', f"{aid}: superseded_by を持つのに status が retired でない（P-7.2）")
        nx = adrs.get(str(d['superseded_by']))
        if nx and str(nx.get('supersedes')) != aid: err('adr', f"{aid}: 後継 {d['superseded_by']} の supersedes に {aid} が無い（双方向）")
effective = {k: d for k, d in adrs.items() if d.get('status') in asc['effective_status'] and d.get('approval')}   # 発効した判断（承認欄あり・retired も含む）

# ── refs（R-4・母集団 = 4 file + 判断の記録の全欄）──
req_ids = set()
for sect in ('goals', 'requirements', 'nonfunctional', 'acceptance', 'constraints', 'actors', 'outputs'):
    for x in s.get(sect) or []: req_ids.add(x['id'])
known_ids = set(ids) | st_ids | req_ids | set(rule_ids) | set(adrs)
sections = {'§5', '§6', '§7', '§8'}
ID_RE = re.compile(r'(?<![A-Za-z0-9-])((?:P|A|N)-\d+(?:\.\d+)?|(?:FR|NFR|AC|CON|GOAL)\d+|(?:R|D)-\d+|ADR-[1-9][0-9]*)(?![A-Za-z0-9])')   # ADR-[1-9]… は内部の判断の記録・4 桁（ADR-0047）は外部の参照で数えない
def walk(obj, where):
    if isinstance(obj, dict):
        for k, vv in obj.items(): walk(vv, f'{where}.{k}')
    elif isinstance(obj, list):
        for i, vv in enumerate(obj): walk(vv, f'{where}[{i}]')
    elif isinstance(obj, str):
        for m in ID_RE.findall(obj):
            if m not in known_ids: err('refs', f"{where}: id {m} が実在しない")
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
for a in c['articles']:
    for am in a.get('amended_by') or []:
        keys_ok('A-2', f"{a['id']}.amended_by", am, ab_spec)
        for k in ('approved_by', 'ruling', 'previous_text'):
            if not str(am.get(k) or '').strip(): err('N-4', f"{a['id']}: amended_by.{k} が空")
        if not DATE_RE.match(str(am.get('date'))): err('N-4', f"{a['id']}: amended_by.date「{am.get('date')}」が年-月-日でない")
        ref = adrs.get(str(am.get('adr')))
        if not ref: err('N-4', f"{a['id']}: amended_by.adr {am.get('adr')} の判断の記録が実在しない"); continue
        if str(am.get('adr')) not in effective: err('N-4', f"{a['id']}: amended_by.adr {am['adr']} が発効していない（status {ref.get('status')}・承認欄 {'有' if ref.get('approval') else '無'}）")
        hit = [e for e in (ref.get('amends') or []) if e.get('target') == a['id']]
        if not hit: err('A-2', f"{a['id']}: {am['adr']} の amends に {a['id']} が無い（双方向）")
        elif hit[0].get('previous_text') != am.get('previous_text'): err('A-2', f"{a['id']}: previous_text が {am['adr']}.amends と食い違う")
for aid, d in effective.items():
    for e in d.get('amends') or []:
        t = e.get('target')
        if t in art_by_id and not any(str(am.get('adr')) == aid for am in art_by_id[t].get('amended_by') or []): err('A-2', f"{aid}: {t} の amended_by に {aid} が無い（双方向）")

# ── anchor（凍結 anchor の鎖・A-2 / N-4 の差分検査の比較元・P-10・ADR-2）──
an = asc['anchor']; PROJ = list(an['projection_article_fields']); A22_MIN = set(an['article_fields_minimum']); SECTS = ('schema', 'precedence', 'articles')
if not A22_MIN <= set(PROJ): err('anchor', f"adr/schema.yaml の射影の欄集合 {PROJ} が A-2.2 の条文の定義 {sorted(A22_MIN)} を含まない（射影を狭めることはできない）")
def project(doc): return {'schema': doc.get('schema'), 'precedence': doc.get('precedence'), 'articles': [{k: a.get(k) for k in PROJ} for a in doc.get('articles') or []]}
def canon(x): return yaml.safe_dump(x, allow_unicode=True, sort_keys=True, width=10**6)
def flow(x): return yaml.safe_dump(x, allow_unicode=True, sort_keys=False, default_flow_style=True, width=10**6)
def digest(proj): return hashlib.sha256(canon({k: proj.get(k) for k in SECTS}).encode('utf-8')).hexdigest()
def art_values(a):   # 条の欄の値の集合（見出し・段・縛る相手・各規範文）＝ previous_text / new_text の完全一致の相手
    if a is None: return set()
    vals = {str(a.get(k)) for k in PROJ if k not in ('id', 'statements')}
    return vals | {str(st.get('text')) for st in a.get('statements') or []}
cur_proj = project(c); cur_ver = str(c['meta']['version'])
def ver_key(vs): return tuple(int(x) for x in re.findall(r'\d+', str(vs)))
ANCH_KEYS = set(an['file_keys']); anchors = {}
for p in (sorted(ANCH_DIR.glob('constitution-*.yaml')) if ANCH_DIR.exists() else []):
    d = load_path(p)
    if not isinstance(d, dict) or set(d.keys()) != ANCH_KEYS or d.get('kind') != 'constitution-anchor': err('anchor', f"{p.name}: anchor の欄が壊れている: {sorted(d.keys()) if isinstance(d, dict) else type(d)}"); continue
    vs = str(d['version'])
    if p.name != an['file_name'].replace('<version>', vs): err('anchor', f"{p.name}: file 名が版 {vs} と違う")
    if vs in anchors: err('anchor', f"{p.name}: 版 {vs} の anchor が重複"); continue
    if list(d.get('projection_article_fields') or []) != PROJ: err('anchor', f"{p.name}: anchor の射影の欄集合 {d.get('projection_article_fields')} と adr/schema.yaml の {PROJ} が食い違う（射影を変えた）")
    if digest(d) != str(d.get('digest')): err('anchor', f"{p.name}: digest が中身と一致しない（anchor が手で変えられた）")
    if not (isinstance(d.get('approval'), dict) and str(d['approval'].get('ruling') or '').strip()): err('anchor', f"{p.name}: 承認欄（ruling）が無い")
    anchors[vs] = (d, p)
pending = []; prev_anchor = None; freeze_plan = None; first_ver = str(an['first_version'])
newest = max(anchors, key=ver_key) if anchors else None
if args.freeze_anchor:
    if cur_ver in anchors: print(f'check_draft: anchor {cur_ver} は既に凍結されている（上書きしない・版を上げてから）', file=sys.stderr); sys.exit(2)
    if newest is None and cur_ver != first_ver: err('anchor', f"最初の anchor は版 {first_ver}（adr/schema.yaml anchor.first_version）でなければならない＝{cur_ver} で鎖を始め直すことはできない")
    if newest is not None and ver_key(newest) >= ver_key(cur_ver): err('anchor', f"凍結する版 {cur_ver} は最新 anchor の版 {newest} より新しくなければならない")
    prev_anchor = anchors[newest][0] if newest else None
else:
    if not anchors: pending.append(f"凍結 anchor が 0 本（{ANCH_DIR}）＝A-2 / N-4 の差分検査は「まだ分からない」（P-10.3）。発効版で --freeze-anchor を実行する")
    else:
        nd, np_ = anchors[newest]
        if newest != cur_ver: err('A-2', f"憲法の版 {cur_ver} と最新 anchor の版 {newest} が違う＝版を上げたのに凍結していない（--freeze-anchor）か、版を上げずに直した")
        elif {k: nd.get(k) for k in SECTS} != cur_proj: err('N-4', f"現行の条文（schema 節・前文・条の {len(PROJ)} 欄）が凍結 anchor {np_.name} と一致しない＝判断の記録と承認を伴わない改憲（N-4.1）")
        chain = []; link = newest   # 鎖: newest → previous → … → first_version（変数名は語彙の v と衝突させない）
        while link is not None and link not in chain:
            chain.append(link)
            if link not in anchors: pending.append(f"anchor の鎖が切れている: 版 {link} の anchor が無い（消された）＝差分検査は「まだ分からない」（P-10.3）。anchors/ は消さない"); break
            link = anchors[link][0].get('previous')
        else:
            if link is not None: err('anchor', f"anchor の鎖が輪になっている: {link}")
            elif chain[-1] != first_ver: err('anchor', f"anchor の鎖の根 {chain[-1]} が最初の版 {first_ver}（adr/schema.yaml anchor.first_version）でない")
        for extra in sorted(set(anchors) - set(chain)): err('anchor', f"anchor {extra} が鎖に無い（previous で辿れない）")
        pv0 = nd.get('previous')
        if pv0 is not None and pv0 in anchors: prev_anchor = anchors[pv0][0]
def amends_for(t): return [e for d in effective.values() for e in d.get('amends') or [] if e.get('target') == t and str(e.get('version')) == cur_ver]
def pair_ok(e, prev_pool, cur_pool, member):
    pt, nt = str(e.get('previous_text')), str(e.get('new_text'))
    return member(pt, prev_pool) and not member(pt, cur_pool) and member(nt, cur_pool) and not member(nt, prev_pool)
if prev_anchor is not None:
    prev = {k: prev_anchor.get(k) for k in SECTS}; pv = str(prev_anchor['version'])
    for t in ('schema', 'precedence'):
        if prev[t] == cur_proj[t]: continue
        cands = amends_for(t)
        if not cands: err('N-4', f"{t} が anchor {pv} から変わったが、それを amends（version {cur_ver}）に持つ発効した判断の記録が無い"); continue
        if not any(pair_ok(e, flow(prev[t]), flow(cur_proj[t]), lambda x, pool: x in pool) for e in cands): err('A-2', f"{t}: 判断の記録の previous_text / new_text が anchor {pv} と現行の差分に一致しない（flow 形式の写しに「前に在って今に無い」「今に在って前に無い」）")
    prev_arts = {a['id']: a for a in prev['articles']}; cur_arts = {a['id']: a for a in cur_proj['articles']}
    for i in sorted(prev_arts.keys() - cur_arts.keys()): err('P-7', f"条 {i} が anchor {pv} に在って現行に無い（番号は消さない・廃止は状態で）")
    for i, ca in cur_arts.items():
        pa = prev_arts.get(i)
        if pa == ca: continue
        prev_vals = art_values(pa) if pa is not None else {str(asc['amends_entry']['new_article_marker'])}; cur_vals = art_values(ca)
        cands = [e for am in (art_by_id[i].get('amended_by') or []) if str(am.get('adr')) in effective
                 for e in (effective[str(am['adr'])].get('amends') or []) if e.get('target') == i and str(e.get('version')) == cur_ver and str(e.get('previous_text')) == str(am.get('previous_text'))]
        if not cands: err('N-4', f"{i} が anchor {pv} から変わったが、amended_by と対になる発効した判断の記録の amends（version {cur_ver}・裁定 id・承認）が無い"); continue
        if not any(pair_ok(e, prev_vals, cur_vals, lambda x, pool: x in pool) for e in cands): err('A-2', f"{i}: amends の previous_text / new_text が anchor {pv} と現行の欄の値に完全一致しない（前の値そのまま・今の値そのまま・両方が変わっていること）")

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
for aid, d in adrs.items():
    for k in ('title', 'context', 'decision', 'plain'): body.append((f'{aid} {k}', str(d.get(k) or '')))
    body.append((f'{aid} retreat', str((d.get('retreat') or {}).get('condition') or '')))
    for o in d.get('options') or []: body.append((f"{aid} option {o.get('id')}", ' '.join(str(o.get(k) or '') for k in ('name', 'text', 'reason'))))
    for x in d.get('consequences') or []: body.append((f'{aid} consequences', str(x)))
body.append(('adr schema plain', str(asd.get('plain') or '')))
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
if args.freeze_anchor:   # 凍結は全検査の後・0 違反のときだけ（床が落ちる憲法を anchor にしない）
    if errs: print(f'check_draft: 凍結しない — 違反 {len(errs)} 件を直してから --freeze-anchor', file=sys.stderr)
    else:
        src = next((d for d in effective.values() if any(str(e.get('version')) == cur_ver for e in d.get('amends') or [])), None)
        ap_src = (src or {}).get('approval') or c['meta']['approval']
        fz = {'kind': 'constitution-anchor', 'version': cur_ver, 'previous': newest, 'projection_article_fields': PROJ, 'digest': digest(cur_proj),
              'approval': {**{k: ap_src.get(k) for k in ('who', 'date', 'ruling', 'verbatim')}, 'adr': (src or {}).get('id')}, **cur_proj}
        fp = ANCH_DIR / an['file_name'].replace('<version>', cur_ver); ANCH_DIR.mkdir(exist_ok=True)
        fp.write_text(f"# folio2 憲法 {cur_ver} の凍結 anchor（P-10.1・ADR-2）。発効版の条文の射影（schema 節・前文・各条の {'・'.join(PROJ)}）+ digest + 承認欄。手で直さない・消さない・同じ版は上書きしない（check_draft.py --freeze-anchor が全検査 0 違反のときだけ作る）。\n" + yaml.safe_dump(fz, allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8')
        print(f'check_draft: 凍結した: {fp}（条 {len(cur_proj["articles"])}・previous {newest}）', file=sys.stderr)
for u in pending: print(f'# まだ分からない: {u}', file=sys.stderr)
sys.exit(1 if errs else (2 if pending else 0))
