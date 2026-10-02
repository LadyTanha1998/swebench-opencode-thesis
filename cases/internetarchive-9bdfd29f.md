# Case file - instance_internetarchive__openlibrary-9bdfd29fac883e77dcbc4208cab28c06fd963ab2-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-9bdfd29fac883e77dcbc4208cab28c06fd963ab2-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c @2026-08-26 07:42
- Final attempt: batch `(original)` (08-26 07:42)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 229 bytes; files touched (1): vendor/infogami
- Copy: `patches/internetarchive-9bdfd29f.diff`
### Evaluator
- Evidence dir: outputs/openlibrary_9bdfd29fac883e77dcbc4208cab28c06fd963ab2-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c_eval/instance_internetarchive__openlibrary-9bdfd29fac883e77dcbc4208cab28c06fd963ab2-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c
- Failed tests / errors: {"tests": [{"name": "openlibrary/plugins/worksearch/tests/test_worksearch.py::test_escape_bracket", "status": "PASSED"}, {"name": "openlibrary/plugins/worksearc

### Trace
- 68414 bytes at `/Users/zt/swebench-thesis/outputs/instance_internetarchive__openlibrary-9bdfd29fac883e77dcbc4208cab28c06fd963ab2-v76304ecdb3a5954fcf13feb710e8c40fcf24b73c/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)