#!/usr/bin/env python3
"""床（scripts/check_draft.py）が RED になる fixture を回す runner（f2-648.2 の受入）。fixture の正本は tests/floor_cases.yaml（凍結・P-10.1）。
使い方: python3 tests/run_floor_cases.py（repo root で）。各 case: design-intent/ を一時 dir へ写し、mutate を順に当て、床を回して
終了コード・出力の語（expect_msg・rc が非 0 なら必須）・出て**いけない**語（expect_not_msg）・stderr の語・file の有無・違反件数（expect_n）を照合する。正本は触らない。
mutate の 1 段: {file, path, value[, add: true]} = 欄を置き換える（欄が無ければ落とす・add で新設）/ {file, delete: true} = file を消す /
{dir, delete_dir: true} = dir を消す / {file, create: <文書>} = file を新しく置く / {file, write_text: <生の文字列>} = 生で書く /
{symlink_dir: <dir>} = dir を design-intent の外へ動かして symlink に置き換える / {git_snapshot: true} = 写しを git の 1 commit にする /
{freeze_anchor: true} = 写しの現行を anchor に凍結する（--freeze-anchor）。途中の凍結は rc 0 を要る（freeze_rc で上書き）/
{emit_amends_into: <adr file>} = --emit-amends の出力（# 行を除く）をそのまま YAML として読み、その判断の記録の amends に置く（貼れる形の検査）。
凍結が最後の段なら、その実行が case の結果。凍結が rc 0 なら続けて素の床も回し rc 0 を要る。expected_cases（件数）を pin する。
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
if _fx.get('expected_cases') != len(cases): print(f"run_floor_cases: case 件数 {len(cases)} が expected_cases {_fx.get('expected_cases')} と違う（fixture が欠けたか増えた）", file=sys.stderr); sys.exit(2)
for cs in cases:
    if cs['expect_rc'] != 0 and not (cs.get('expect_msg') or cs.get('expect_stderr')): print(f"run_floor_cases: {cs['id']}: rc 非 0 の case には expect_msg か expect_stderr が要る", file=sys.stderr); sys.exit(2)
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
def mutate(doc, path, value, add):
    st = steps(path); cur = doc
    for x in st[:-1]: cur = get(cur, x)
    last = st[-1]
    if isinstance(last, tuple): raise ValueError(f'末尾の段は欄名か添字: {path}')
    if isinstance(cur, dict) and last not in cur and not add: raise KeyError(f'欄 {path} が無い（新設なら add: true）')
    if isinstance(cur, list) and isinstance(last, int) and last == len(cur):
        if not add: raise IndexError(f'{path} は一覧の末尾の次（新設なら add: true）')
        cur.append(value); return
    cur[last] = value
def dump(doc): return yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=10**6)
def run(work, *flags): return subprocess.run([sys.executable, str(CHECK), '--dir', str(work), *flags], capture_output=True, text=True)
def judge(cs, pr):
    ok = pr.returncode == cs['expect_rc']
    if cs.get('expect_msg') and cs['expect_msg'] not in pr.stdout + pr.stderr: ok = False
    if cs.get('expect_stderr') and cs['expect_stderr'] not in pr.stderr: ok = False
    if cs.get('expect_not_msg') and cs['expect_not_msg'] in pr.stdout + pr.stderr: ok = False
    if 'expect_n' in cs and len([l for l in pr.stdout.splitlines() if l.startswith('[')]) != cs['expect_n']: ok = False
    return ok
bad = 0
for cs in cases:
    with tempfile.TemporaryDirectory() as td:
        work = pathlib.Path(td) / 'design-intent'; shutil.copytree(SRC, work)
        last = None; note = ''
        muts = [x for m in (cs.get('mutate') or []) for x in (m if isinstance(m, list) else [m])]   # 共通の段（alias の一覧）を 1 段ずつに開く
        try:
            for mu in muts:
                if mu.get('freeze_anchor'):
                    last = run(work, '--freeze-anchor')
                    if mu is not muts[-1] and last.returncode != mu.get('freeze_rc', 0): note += f' ／ 途中の凍結が rc {last.returncode}'
                    continue
                last = None
                if mu.get('emit_amends_into'):
                    em = run(work, '--emit-amends')
                    if em.returncode != 0: note += f' ／ emit が rc {em.returncode}'; continue
                    lst = yaml.safe_load('\n'.join(l for l in em.stdout.splitlines() if not l.startswith('#'))) or []
                    f = work / mu['emit_amends_into']; doc = yaml.safe_load(f.read_text(encoding='utf-8')); doc['amends'] = lst; f.write_text(dump(doc), encoding='utf-8'); continue
                if mu.get('git_snapshot'):
                    for cmd in (['git', 'init', '-q'], ['git', 'add', '-A'], ['git', '-c', 'user.email=fx@example', '-c', 'user.name=fx', 'commit', '-q', '-m', 'fixture']): subprocess.run(cmd, cwd=td, capture_output=True, check=True)
                    continue
                if mu.get('symlink_dir'):
                    src_ = work / mu['symlink_dir']; outside = pathlib.Path(td) / 'outside'; outside.mkdir(exist_ok=True); dst = outside / src_.name
                    shutil.move(str(src_), str(dst)); src_.symlink_to(dst); continue
                if mu.get('delete_dir'): shutil.rmtree(work / mu['dir']); continue
                f = work / mu['file']
                if mu.get('delete'): f.unlink(); continue
                if 'create' in mu: f.parent.mkdir(parents=True, exist_ok=True); f.write_text(dump(mu['create']), encoding='utf-8'); continue
                if 'write_text' in mu: f.parent.mkdir(parents=True, exist_ok=True); f.write_text(mu['write_text'], encoding='utf-8'); continue
                doc = yaml.safe_load(f.read_text(encoding='utf-8'))
                if 'swap' in mu:   # 一覧の 2 要素を入れ替える（並びの差分の再現）
                    cur = doc
                    for x in steps(mu['path']): cur = get(cur, x)
                    i_, j_ = mu['swap']; cur[i_], cur[j_] = cur[j_], cur[i_]
                else: mutate(doc, mu['path'], mu['value'], mu.get('add', False))
                f.write_text(dump(doc), encoding='utf-8')
        except Exception as ex:
            print(f"FAIL {cs['id']}: fixture の適用で例外 {type(ex).__name__}: {ex}"); bad += 1; continue
        if last is not None:
            pr = last
            if pr.returncode == 0:
                pr2 = run(work)
                if pr2.returncode != 0: note += f' ／ 凍結後の素の床が rc {pr2.returncode}'; pr = pr2
        else: pr = run(work)
        ok = judge(cs, pr) and not note
        for rel in cs.get('expect_no_file') or []:
            if (work / rel).exists(): ok = False; note += f' ／ {rel} が書かれている'
        for rel in cs.get('expect_file') or []:
            if not (work / rel).exists(): ok = False; note += f' ／ {rel} が無い'
    print(f"{'PASS' if ok else 'FAIL'} {cs['id']}: rc={pr.returncode}（期待 {cs['expect_rc']}） — {cs['why']}{note}")
    if not ok:
        bad += 1
        for ln in (pr.stdout + pr.stderr).strip().splitlines()[:10]: print('    ' + ln)
print(f"# {len(cases) - bad} / {len(cases)} case が期待どおり", file=sys.stderr)
sys.exit(1 if bad else 0)
