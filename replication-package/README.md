# Replication Package

Data and evidence for the thesis *Bugs in AI-Generated Code: An Empirical Study on
SWE-bench Pro* (University of Luxembourg). The method is described in Chapter 3 of
the thesis; the defect categories are defined in its Appendix A.

## Contents

| Path | Content |
|------|---------|
| `master_dataset.csv` | One row per task (253 rows): final outcome, main defect label, second-layer form for Incomplete Generation, number of attempt folders, final run status, patch sizes, files touched, failing tests. |
| `patches/` | The final patch of the final attempt for each task. 32 files are empty, because the final attempt produced no code change. |
| `evaluator/` | Benchmark evaluation output for each task (test logs and result files). 249 of the 253 tasks have evaluator output. For four failed tasks (`gravitational-cb712e3f`, `internetarchive-53e02a22`, `internetarchive-8a5a63af`, `tutao-40e94dee`), no evaluation output could be located; all four have an empty final patch. |
| `traces/` | The execution trace of the final attempt for each task: model messages, tool calls, file reads and edits, shell commands, and test runs. Local file paths were replaced with neutral paths. |

File names use the pattern `<repository>-<first 8 characters of the commit hash>`,
for example `internetarchive-4a5d2a7d`. The same name links a row in
`master_dataset.csv` with its patch, evaluation output, and trace.

## Summary of the results

- 71 of 253 tasks passed (28.1%); 182 failed.
- Main defect labels of the failures: Incomplete Generation 93, Misinterpretation 67,
  Silly Mistake 12, Missing Corner Case 8, Wrong Attribute 2.
- Second-layer forms of the 93 Incomplete Generation cases: IG-A empty patch 21,
  IG-B partial implementation 55, IG-C integration failure 1, IG-D artefact-only diff 16.
