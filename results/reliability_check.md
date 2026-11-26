# Reliability check (26.11.2026, ~23:45)

Second rater: an independent AI instance (Claude subagent, general-purpose) that had not seen the study conversation.
It received only protocol.txt (rules 1-5, C1-C5, checklist), warnings.csv (22 scanner warnings without verdicts) and the 40 anonymised files S01-S40, and was instructed not to open any other path (the Key and the first rater's decisions).

Results versus the first-rater decisions (approved by the author on 26.11.2026, 23:13):
- Scanner warnings (confirmed vs false positive): 22/22 agree, Cohen's kappa = 1.00.
- File vulnerable yes/no (40 files): 40/40 agree, Cohen's kappa = 1.00 (20 vulnerable files in both).
- Exact CWE set per file: 39/40 agree. Disagreement: S15 - second rater added CWE-798 for the module-level example
  that registers a demo user with a literal password; first rater counted CWE-256 only. Resolution: see the research log.

Note: the first-rater decisions were themselves drafted by an AI assistant (Claude) under the same protocol and reviewed by the author,
so this check shows that the protocol yields the same decisions when applied independently; it is not a check of two human raters.
Raw output: rater2.json, rater2_protocol.txt.

Resolution of the S15 disagreement (author, 26.11.2026, 23:42): keep the first decision (CWE-256 only). The literal password belongs to a module-level usage example that registers a demo user in its own local dictionary, which the functions' callers do not use; it is not a credential the code uses to grant or obtain access.
