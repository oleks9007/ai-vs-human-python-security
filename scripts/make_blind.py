"""Copies the 40 solutions into blind/S01.py ... S40.py according to the Key sheet.
Run from the research folder:  py -V:3.13 make_blind.py
It prints only counts, never which S-file belongs to which task or group."""
import pathlib, shutil, sys
from collections import Counter

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is missing. Run:  py -V:3.13 -m pip install openpyxl  and start again.")

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLIND = ROOT / "blind"
BLIND.mkdir(exist_ok=True)
if any(BLIND.glob("S*.py")):
    sys.exit("blind folder already contains S*.py files. Nothing was changed.")

ws = openpyxl.load_workbook(ROOT / "research_log_20.xlsx", read_only=True)["Key"]
rows = []
for sid, task, group in ws.iter_rows(min_row=2, max_row=41, min_col=1, max_col=3, values_only=True):
    sid, task, group = str(sid).strip(), str(task).strip(), str(group).strip().lower()
    if group not in ("ai", "human"):
        sys.exit("Unexpected group value in the Key sheet. Nothing was copied.")
    rows.append((sid, task, group))

problems = []
if len(rows) != 40 or len({r[0] for r in rows}) != 40:
    problems.append("Key must have 40 unique solution IDs")
per_task = Counter((r[1], r[2]) for r in rows)
if len(per_task) != 40 or any(n != 1 for n in per_task.values()):
    problems.append("each task must have exactly one AI and one Human row")
for sid, task, group in rows:
    src = ROOT / "solutions" / group / f"task{task[1:]}.py"
    if not src.exists():
        problems.append(f"missing source file for one Key row ({sid})")
if problems:
    sys.exit("Stopped, nothing was copied: " + "; ".join(problems))

for sid, task, group in rows:
    shutil.copyfile(ROOT / "solutions" / group / f"task{task[1:]}.py", BLIND / f"{sid}.py")

print(f"Done: {len(list(BLIND.glob('S*.py')))} files copied to blind\\. Do not open the Key sheet until the manual review is finished.")
