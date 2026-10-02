# Case file - instance_internetarchive__openlibrary-bdba0af0f6cbaca8b5fc3be2a3080f38156d9c92-ve8c8d62a2b60610a3c4631f5f23ed866bada9818

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-bdba0af0f6cbaca8b5fc3be2a3080f38156d9c92-ve8c8d62a2b60610a3c4631f5f23ed866bada9818 @2026-08-26 06:26
- Final attempt: batch `(original)` (08-26 06:26)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 2403 bytes; files touched (3): openlibrary/templates/account/books.html; openlibrary/templates/account/mybooks.html; openlibrary/utils/dateutil.py
- Copy: `patches/internetarchive-bdba0af0.diff`
### Evaluator
- Evidence dir: outputs/eval_batch_current_3tasks/instance_internetarchive__openlibrary-bdba0af0f6cbaca8b5fc3be2a3080f38156d9c92-ve8c8d62a2b60610a3c4631f5f23ed866bada9818
- Failed tests / errors: {"tests": [{"name": "openlibrary/utils/tests/test_dateutil.py::test_parse_date", "status": "PASSED"}, {"name": "openlibrary/utils/tests/test_dateutil.py::test_n

### Trace
- 128101 bytes at `/Users/zt/swebench-thesis/outputs/instance_internetarchive__openlibrary-bdba0af0f6cbaca8b5fc3be2a3080f38156d9c92-ve8c8d62a2b60610a3c4631f5f23ed866bada9818/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Templates + dateutil.py edited (templates are app code); required behaviour incomplete. Not IG-C: no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)