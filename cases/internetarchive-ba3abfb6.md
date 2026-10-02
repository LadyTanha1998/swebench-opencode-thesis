# Case file - instance_internetarchive__openlibrary-ba3abfb6af6e722185d3715929ab0f3e5a134eed-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-ba3abfb6af6e722185d3715929ab0f3e5a134eed-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c @2026-08-26 06:13; main_rerun_task_ba3abfb @2026-09-10 11:06
- Final attempt: batch `main_rerun_task_ba3abfb` (09-10 11:06)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 4096 bytes; files touched (4): openlibrary/catalog/add_book/__init__.py; openlibrary/plugins/importapi/code.py; package-lock.json; vendor/infogami
- Copy: `patches/internetarchive-ba3abfb6.diff`
### Evaluator
- Evidence dir: outputs/eval_batch_current_3tasks/instance_internetarchive__openlibrary-ba3abfb6af6e722185d3715929ab0f3e5a134eed-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c
- Failed tests / errors: {"tests": [{"name": "openlibrary/catalog/add_book/tests/test_add_book.py::test_isbns_from_record", "status": "PASSED"}, {"name": "openlibrary/catalog/add_book/t

### Trace
- 272554 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_task_ba3abfb/instance_internetarchive__openlibrary-ba3abfb6af6e722185d3715929ab0f3e5a134eed-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: add_book/importapi source changed (package-lock + vendor churn ignored); required behaviour incomplete. Not IG-C: tests executed, no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)