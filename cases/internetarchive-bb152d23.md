# Case file - instance_internetarchive__openlibrary-bb152d23c004f3d68986877143bb0f83531fe401-ve8c8d62a2b60610a3c4631f5f23ed866bada9818

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-bb152d23c004f3d68986877143bb0f83531fe401-ve8c8d62a2b60610a3c4631f5f23ed866bada9818 @2026-08-26 06:57
- Final attempt: batch `(original)` (08-26 06:57)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 17095 bytes; files touched (3): openlibrary/coverstore/archive.py; openlibrary/coverstore/code.py; openlibrary/coverstore/tests/test_code.py
- Copy: `patches/internetarchive-bb152d23.diff`
### Evaluator
- Evidence dir: outputs/eval_batch_current_3tasks/instance_internetarchive__openlibrary-bb152d23c004f3d68986877143bb0f83531fe401-ve8c8d62a2b60610a3c4631f5f23ed866bada9818
- Failed tests / errors: {"tests": [{"name": "openlibrary/coverstore/tests/test_archive.py::test_get_filename", "status": "FAILED"}, {"name": "openlibrary/coverstore/tests/test_archive.

### Trace
- 360599 bytes at `/Users/zt/swebench-thesis/outputs/instance_internetarchive__openlibrary-bb152d23c004f3d68986877143bb0f83531fe401-ve8c8d62a2b60610a3c4631f5f23ed866bada9818/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Evaluator shows test_get_filename FAILED; agent edited archive.py/code.py but filename handling remains wrong - missing behaviour. Not IG-C: tests executed.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)