"""Recomputes the numbers reported in the paper from research_log_20.xlsx.
Run from the repository root:  python scripts/compute_stats.py
Requires: openpyxl. Uses exact tests (no SciPy needed)."""
import pathlib, itertools
from math import comb
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
wb = openpyxl.load_workbook(ROOT / "research_log_20.xlsx")
res, key = wb["Results"], wb["Key"]
group = {r[0]: (r[1], r[2]) for r in key.iter_rows(min_row=2, max_row=41, values_only=True)}

rows = {}
for r in range(2, 42):
    sid = res[f"A{r}"].value
    task, g = group[sid]
    rows[(task, g)] = dict(sid=sid, passed=res[f"B{r}"].value == "Yes",
                           bandit=res[f"C{r}"].value, semgrep=res[f"D{r}"].value,
                           confirmed=res[f"F{r}"].value, fp=res[f"G{r}"].value,
                           vulns=res[f"I{r}"].value + res[f"J{r}"].value, manual=res[f"J{r}"].value)

tasks = sorted({t for t, _ in rows})
included = [t for t in tasks if rows[(t, "AI")]["passed"] and rows[(t, "Human")]["passed"]]
print(f"Included pairs: {len(included)} (excluded: {[t for t in tasks if t not in included]})")
for g in ("AI", "Human"):
    L = [rows[(t, g)] for t in included]
    warn = sum(x["bandit"] + x["semgrep"] for x in L); conf = sum(x["confirmed"] for x in L)
    print(f"{g:6} warnings={warn} confirmed={conf} fp={sum(x['fp'] for x in L)} "
          f"manual_only={sum(x['manual'] for x in L)} vulns={sum(x['vulns'] for x in L)} "
          f"vulnerable={sum(x['vulns'] > 0 for x in L)}/{len(L)}")

b = sum(rows[(t, "AI")]["vulns"] > 0 and rows[(t, "Human")]["vulns"] == 0 for t in included)
c = sum(rows[(t, "AI")]["vulns"] == 0 and rows[(t, "Human")]["vulns"] > 0 for t in included)
n = b + c
p_mcnemar = min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n) if n else 1.0
print(f"McNemar exact: AI-only={b}, Human-only={c}, p={p_mcnemar:.3f}")

d = [rows[(t, "AI")]["vulns"] - rows[(t, "Human")]["vulns"] for t in included]
nz = [x for x in d if x != 0]
ab = sorted(abs(x) for x in nz)
ranks = {}
for v in set(ab):
    idx = [i + 1 for i, a in enumerate(ab) if a == v]; ranks[v] = sum(idx) / len(idx)
w_obs = sum(ranks[abs(x)] for x in nz if x > 0)
dist = [sum(ranks[abs(x)] for x, s in zip(nz, signs) if s > 0) for signs in itertools.product((1, -1), repeat=len(nz))]
p_low = sum(w <= w_obs for w in dist) / len(dist); p_high = sum(w >= w_obs for w in dist) / len(dist)
print(f"Wilcoxon exact: non-zero differences={len(nz)}, W+={w_obs}, p={min(1.0, 2 * min(p_low, p_high)):.3f}")
