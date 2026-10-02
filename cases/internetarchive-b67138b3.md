# Case file - instance_internetarchive__openlibrary-b67138b316b1e9c11df8a4a8391fe5cc8e75ff9f-ve8c8d62a2b60610a3c4631f5f23ed866bada9818

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-b67138b316b1e9c11df8a4a8391fe5cc8e75ff9f-ve8c8d62a2b60610a3c4631f5f23ed866bada9818 @2026-08-26 08:13; main_rerun_task03 @2026-09-10 10:50
- Final attempt: batch `main_rerun_task03` (09-10 10:50)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 26846 bytes; files touched (5): openlibrary/catalog/marc/get_subjects.py; openlibrary/catalog/marc/marc_base.py; openlibrary/catalog/marc/marc_binary.py; openlibrary/catalog/marc/marc_xml.py; openlibrary/catalog/marc/parse.py
- Copy: `patches/internetarchive-b67138b3.diff`
### Evaluator
- Evidence dir: outputs/openlibrary_b67138b316b1e9c11df8a4a8391fe5cc8e75ff9f-ve8c8d62a2b60610a3c4631f5f23ed866bada9818_eval/instance_internetarchive__openlibrary-b67138b316b1e9c11df8a4a8391fe5cc8e75ff9f-ve8c8d62a2b60610a3c4631f5f23ed866bada9818
- Failed tests / errors: {"tests": [{"name": "openlibrary/catalog/marc/tests/test_marc_binary.py::test_wrapped_lines", "status": "PASSED"}, {"name": "openlibrary/catalog/marc/tests/test

### Trace
- 664554 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_task03/instance_internetarchive__openlibrary-b67138b316b1e9c11df8a4a8391fe5cc8e75ff9f-ve8c8d62a2b60610a3c4631f5f23ed866bada9818/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: 5-file MARC refactor cut off by the 600s timeout - work left unfinished mid-refactor (time exhausted). Not IG-C: coherent Python, no build failure observed.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)