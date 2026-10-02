# Case file - instance_protonmail__webclients-e7f3f20c8ad86089967498632ace73c1157a9d51

**Repo:** protonmail  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_protonmail__webclients-e7f3f20c8ad86089967498632ace73c1157a9d51 @2026-08-26 15:29; protonmail_e7f3f20c_rerun_v3 @2026-09-13 21:27
- Final attempt: batch `protonmail_e7f3f20c_rerun_v3` (09-13 21:27)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 71006 bytes; files touched (1): yarn.lock
- Copy: `patches/protonmail-e7f3f20c.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_recovery_04/instance_protonmail__webclients-e7f3f20c8ad86089967498632ace73c1157a9d51
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
- NOTE: evaluator evidence may predate the final attempt - verify or re-run.
### Trace
- 0 bytes at `/Users/zt/swebench-thesis/outputs/protonmail_e7f3f20c_rerun_v3/instance_protonmail__webclients-e7f3f20c8ad86089967498632ace73c1157a9d51/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)