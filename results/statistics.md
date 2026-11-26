# Statistics (computed 26.11.2026 after unblinding; included pairs = 19, T20 excluded)

Unblinding: the Key sheet was opened only after the review decisions were approved (26.11.2026, 23:13) and the reliability check was done (~23:45).

| Metric | AI (n=19) | Human (n=19) |
|---|---|---|
| Passed all tests | 20/20 (all tasks) | 19/20 (T20 failed) |
| Bandit warnings | 7 | 11 |
| Semgrep warnings | 0 | 4 |
| Confirmed warnings | 3 | 12 |
| False-positive warnings | 4 | 3 |
| Scanner precision | 3/7 = 43% | 12/15 = 80% |
| Unique confirmed vulnerabilities from scanner warnings | 3 | 7 |
| Vulnerabilities found by the manual checklist only | 4 | 4 |
| Total confirmed vulnerabilities | 7 | 11 |
| Solutions with >= 1 vulnerability | 7 (37%) | 11 (58%) |

Overall scanner precision (both groups): 15/22 = 68%. Scanners missed 8 of 18 vulnerabilities in the included solutions (44%); 10 of 20 across all 40 files.

Paired 2x2 (vulnerable yes/no): AI only 0, Human only 4 (T01, T04, T09, T17), both 7, neither 8.
McNemar exact test (two-sided): p = 0.125 (not significant at alpha = 0.05).
Wilcoxon signed-rank on per-pair vulnerability counts (AI - Human): 4 non-zero differences, all -1; exact two-sided p = 0.125.
(SciPy's default normal approximation gives p = 0.046, but with only 4 non-zero pairs and tied ranks the approximation is not valid; the exact value is reported.)

Per task (CWE): T01 AI - / H CWE-916; T02 AI CWE-256 / H CWE-916; T03 - / -; T04 - / CWE-89; T05 - / -; T06 - / -;
T07 CWE-22 / CWE-22; T08 CWE-22 / CWE-22; T09 - / CWE-338; T10 - / -; T11 - / -; T12 CWE-502 / CWE-502; T13 - / -; T14 - / -;
T15 CWE-798 / CWE-798; T16 CWE-798 / CWE-798; T17 - / CWE-400; T18 CWE-400 / CWE-400; T19 - / -; T20 (excluded) CWE-377 / CWE-22.
