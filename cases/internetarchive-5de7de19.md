# Case file - instance_internetarchive__openlibrary-5de7de19211e71b29b2f2ba3b1dff2fe065d660f-v08d8e8889ec945ab821fb156c04c7d2e2810debb

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-5de7de19211e71b29b2f2ba3b1dff2fe065d660f-v08d8e8889ec945ab821fb156c04c7d2e2810debb @2026-08-26 05:24
- Final attempt: batch `(original)` (08-26 05:24)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 1971 bytes; files touched (2): openlibrary/core/models.py; vendor/infogami
- Copy: `patches/internetarchive-5de7de19.diff`
### Evaluator
- Evidence dir: outputs/openlibrary_four_reuse_eval_12/instance_internetarchive__openlibrary-5de7de19211e71b29b2f2ba3b1dff2fe065d660f-v08d8e8889ec945ab821fb156c04c7d2e2810debb
- Failed tests / errors: {"tests": [{"name": "openlibrary/tests/core/test_models.py::TestEdition::test_url", "status": "PASSED"}, {"name": "openlibrary/tests/core/test_models.py::TestEd

### Trace
- 90711 bytes at `/Users/zt/swebench-thesis/outputs/instance_internetarchive__openlibrary-5de7de19211e71b29b2f2ba3b1dff2fe065d660f-v08d8e8889ec945ab821fb156c04c7d2e2810debb/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: core/models.py edited (vendor pointer ignored); required model behaviour incomplete. Not IG-C: module loads, no integration break.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)