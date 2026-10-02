# Case file - instance_internetarchive__openlibrary-e1e502986a3b003899a8347ac8a7ff7b08cbfc39-v08d8e8889ec945ab821fb156c04c7d2e2810debb

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-e1e502986a3b003899a8347ac8a7ff7b08cbfc39-v08d8e8889ec945ab821fb156c04c7d2e2810debb @2026-08-26 07:21; main_rerun_task_e1e50298 @2026-09-10 11:31
- Final attempt: batch `main_rerun_task_e1e50298` (09-10 11:31)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 228 bytes; files touched (1): vendor/infogami
- Copy: `patches/internetarchive-e1e50298.diff`
### Evaluator
- Evidence dir: outputs/instance_internetarchive__openlibrary-e1e502986a3b003899a8347ac8a7ff7b08cbfc39-v08d8e8889ec945ab821fb156c04c7d2e2810debb_eval_current/instance_internetarchive__openlibrary-e1e502986a3b003899a8347ac8a7ff7b08cbfc39-v08d8e8889ec945ab821fb156c04c7d2e2810debb
- Failed tests / errors: {"tests": [{"name": "openlibrary/plugins/upstream/tests/test_table_of_contents.py::TestTableOfContents::test_from_db_well_formatted", "status": "PASSED"}, {"nam
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 195834 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_task_e1e50298/instance_internetarchive__openlibrary-e1e502986a3b003899a8347ac8a7ff7b08cbfc39-v08d8e8889ec945ab821fb156c04c7d2e2810debb/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)