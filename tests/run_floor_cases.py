#!/usr/bin/env python3
"""床（scripts/check_draft.py）が RED になる fixture を回す runner（f2-648.2 の受入）。fixture の正本は tests/floor_cases.yaml（凍結・P-10.1）。
使い方: python3 tests/run_floor_cases.py（repo root で）。各 case: design-intent/ を一時 dir へ写し、mutate を順に当て、床を回して
終了コード・違反の種別・出力の語・file の有無を照合する。正本は触らない。
mutate の 1 段: {file, path, value} = 欄を置き換える / {file, delete: true} = file を消す / {file, create: <文書>} = file を新しく置く /
{freeze_anchor: true} = 写しの現行を anchor に凍結する（--freeze-anchor・全検査の後に 0 違反なら書く）。
凍結が最後の段なら、その実行が case の結果（rc・kind・stderr）。凍結が rc 0 なら続けて素の床も回し rc 0 を要る。
rc: 0 = 全 case が期待どおり / 1 = 期待と違う case あり / 2 = 読めない"""
import re, sys, shutil, subprocess, tempfile, pathlib
try:
    import yaml
except ImportError:
    print('run_floor_cases: pyyaml が無い', file=sys.stderr); sys.exit(2)
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'design-intent'; CHECK = ROOT / 'scripts' / 'check_draft.py'
try:
    _fx = yaml.safe_load((ROOT / 'tests' / 'floor_cases.yaml').read_text(encoding='utf-8'))
    cases = [c for k, v in _fx.items() if k.startswith('cases') for c in v]
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
def run(work, *flags): return subprocess.run([sys.executable, str(CHECK), '--dir', str(work), *flags], capture_output=True, text=True)
def judge(cs, pr):
    ok = pr.returncode == cs['expect_rc']
    if cs.get('expect_kind') and f"[{cs['expect_kind']}]" not in pr.stdout: ok = False
    if cs.get('expect_msg') and cs['expect_msg'] not in pr.stdout + pr.stderr: ok = False
    if cs.get('expect_stderr') and cs['expect_stderr'] not in pr.stderr: ok = False
    return ok
bad = 0
for cs in cases:
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / 'design-intent'; shutil.copytree(SRC, work)
        last = None; note = ''
        for mu in cs.get('mutate') or []:
            if mu.get('freeze_anchor'): last = run(work, '--freeze-anchor'); continue
            last = None
            f = work / mu['file']
            if mu.get('delete'): f.unlink(); continue
            if 'create' in mu: f.parent.mkdir(parents=True, exist_ok=True); f.write_text(yaml.safe_dump(mu['create'], allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8'); continue
            doc = yaml.safe_load(f.read_text(encoding='utf-8')); mutate(doc, mu['path'], mu['value'])
            f.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=10**6), encoding='utf-8')
        if last is not None:   # 凍結が最後の段
            pr = last
            if pr.returncode == 0:
                pr2 = run(work)
                if pr2.returncode != 0: note = f' ／ 凍結後の素の床が rc {pr2.returncode}'; pr = pr2
        else: pr = run(work)
        ok = judge(cs, pr) and not note
        for rel in cs.get('expect_no_file') or []:
            if (work / rel).exists(): ok = False; note += f' ／ {rel} が書かれている'
        for rel in cs.get('expect_file') or []:
            if not (work / rel).exists(): ok = False; note += f' ／ {rel} が無い'
    print(f"{'PASS' if ok else 'FAIL'} {cs['id']}: rc={pr.returncode}（期待 {cs['expect_rc']}）" + (f" kind={cs.get('expect_kind')}" if cs.get('expect_kind') else '') + f" — {cs['why']}{note}")
    if not ok:
        bad += 1
        for ln in (pr.stdout + pr.stderr).strip().splitlines()[:10]: print('    ' + ln)
print(f"# {len(cases) - bad} / {len(cases)} case が期待どおり", file=sys.stderr)
sys.exit(1 if bad else 0)
