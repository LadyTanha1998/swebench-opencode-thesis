# Case file - instance_internetarchive__openlibrary-6fdbbeee4c0a7e976ff3e46fb1d36f4eb110c428-v08d8e8889ec945ab821fb156c04c7d2e2810debb

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-6fdbbeee4c0a7e976ff3e46fb1d36f4eb110c428-v08d8e8889ec945ab821fb156c04c7d2e2810debb @2026-08-26 06:40; openlibrary_6fdbbeee_sanitized_rerun_v3 @2026-09-13 14:43
- Final attempt: batch `openlibrary_6fdbbeee_sanitized_rerun_v3` (09-13 14:43)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 228 bytes; files touched (1): vendor/infogami
- Copy: `patches/internetarchive-6fdbbeee.diff`
### Evaluator
- Evidence dir: outputs/openlibrary_five_reuse_eval_15/instance_internetarchive__openlibrary-6fdbbeee4c0a7e976ff3e46fb1d36f4eb110c428-v08d8e8889ec945ab821fb156c04c7d2e2810debb
- Failed tests / errors: {"tests": [{"name": "openlibrary/plugins/openlibrary/tests/test_lists.py::TestListRecord::test_from_input_no_data", "status": "PASSED"}, {"name": "openlibrary/p
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
- NOTE: evaluator evidence may predate the final attempt - verify or re-run.
### Trace
- 13467 bytes at `/Users/zt/swebench-thesis/outputs/openlibrary_6fdbbeee_sanitized_rerun_v3/instance_internetarchive__openlibrary-6fdbbeee4c0a7e976ff3e46fb1d36f4eb110c428-v08d8e8889ec945ab821fb156c04c7d2e2810debb/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)