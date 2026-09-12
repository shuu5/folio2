#!/usr/bin/env python3
"""床（scripts/check_draft.py）が RED になる fixture を回す runner（f2-648.2 の受入）。fixture の正本は tests/floor_cases.yaml（凍結・P-10.1）。
使い方: python3 tests/run_floor_cases.py（repo root で）。各 case: design-intent/ を一時 dir へ写し、mutate を当て、
check_draft.py --dir <写し> を回して終了コードと違反の種別を照合する。正本は触らない。
rc: 0 = 全 case が期待どおり / 1 = 期待と違う case あり / 2 = 読めない"""
import re, sys, shutil, subprocess, tempfile, pathlib
try:
    import yaml
except ImportError:
    print('run_floor_cases: pyyaml が無い', file=sys.stderr); sys.exit(2)
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'design-intent'; CHECK = ROOT / 'scripts' / 'check_draft.py'
try:
    _fx = yaml.safe_load((ROOT / 'tests' / 'floor_cases.yaml').read_text(encoding='utf-8')); cases = list(_fx['cases']) + list(_fx.get('cases_amendment') or [])
except Exception as ex:
    print(f'run_floor_cases: fixture が読めない: {ex}', file=sys.stderr); sys.exit(2)
SEG = re.compile(r'([^\[\].]+)|\[([^\]]+)\]')
def steps(path):
    out = []
    for m in SEG.finditer(path):
        if m.group(1): out.append(m.group(1))
        else:
            t = m.group(2)
            out.append(('find',) + tuple(t.split('=', 1)) if '=' in t else int(t))
    return out
def get(obj, st):
    if isinstance(st, tuple): return next(x for x in obj if str(x.get(st[1])) == st[2])
    return obj[st]
def mutate(doc, path, value):
    st = steps(path); cur = doc
    for x in st[:-1]: cur = get(cur, x)
    if isinstance(st[-1], tuple): raise ValueError(f'末尾の段は欄名か添字: {path}')
    cur[st[-1]] = value
bad = 0
for cs in cases:
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / 'design-intent'; shutil.copytree(SRC, work)
        for mu in cs.get('mutate') or []:
            if mu.get('freeze_anchor'):   # 写しの現行の射影を anchor として凍結する（正の経路の再現・check_draft と同じ関数）
                subprocess.run([sys.executable, str(CHECK), '--dir', str(work), '--freeze-anchor'], capture_output=True, text=True); continue
            f = work / mu['file']
            if mu.get('delete'): f.unlink(); continue
            if 'create' in mu: f.write_text(yaml.safe_dump(mu['create'], allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8'); continue
            doc = yaml.safe_load(f.read_text(encoding='utf-8')); mutate(doc, mu['path'], mu['value'])
            f.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8')
        pr = subprocess.run([sys.executable, str(CHECK), '--dir', str(work)], capture_output=True, text=True)
    ok = pr.returncode == cs['expect_rc']
    if cs.get('expect_kind') and f"[{cs['expect_kind']}]" not in pr.stdout: ok = False
    if cs.get('expect_stderr') and cs['expect_stderr'] not in pr.stderr: ok = False
    print(f"{'PASS' if ok else 'FAIL'} {cs['id']}: rc={pr.returncode}（期待 {cs['expect_rc']}）" + (f" kind={cs.get('expect_kind')}" if cs.get('expect_kind') else '') + f" — {cs['why']}")
    if not ok:
        bad += 1
        for ln in (pr.stdout + pr.stderr).strip().splitlines()[:8]: print('    ' + ln)
print(f"# {len(cases) - bad} / {len(cases)} case が期待どおり", file=sys.stderr)
sys.exit(1 if bad else 0)
