# Case file - instance_internetarchive__openlibrary-111347e9583372e8ef91c82e0612ea437ae3a9c9-v2d9a6c849c60ed19fd0858ce9e40b7cc8e097e59

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-111347e9583372e8ef91c82e0612ea437ae3a9c9-v2d9a6c849c60ed19fd0858ce9e40b7cc8e097e59 @2026-08-26 07:29; main_rerun_3task_02 @2026-09-09 14:51
- Final attempt: batch `main_rerun_3task_02` (09-09 14:51)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 2174 bytes; files touched (3): openlibrary/catalog/marc/marc_binary.py; openlibrary/catalog/marc/marc_xml.py; openlibrary/catalog/marc/parse.py
- Copy: `patches/internetarchive-111347e9.diff`
### Evaluator
- Evidence dir: outputs/eval_fixed_2tasks/instance_internetarchive__openlibrary-111347e9583372e8ef91c82e0612ea437ae3a9c9-v2d9a6c849c60ed19fd0858ce9e40b7cc8e097e59
- Failed tests / errors: {"tests": [{"name": "openlibrary/catalog/marc/tests/test_parse.py::TestParseMARCXML::test_xml[39002054008678.yale.edu]", "status": "PASSED"}, {"name": "openlibr

### Trace
- 332390 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_3task_02/instance_internetarchive__openlibrary-111347e9583372e8ef91c82e0612ea437ae3a9c9-v2d9a6c849c60ed19fd0858ce9e40b7cc8e097e59/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Agent edited the MARC parsing modules (marc_binary, marc_xml, parse) yet the run failed; visible tests pass while required parsing behaviour is absent. Not IG-C: modules import and tests execute (no build failure).
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)