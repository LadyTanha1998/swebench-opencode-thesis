# Case file - instance_flipt-io__flipt-9d25c18b79bc7829a6fb08ec9e8793d5d17e2868

**Repo:** flipt-io  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_flipt-io__flipt-9d25c18b79bc7829a6fb08ec9e8793d5d17e2868 @2026-08-25 15:42; corrected_prompt_pilot_5_20260918 @2026-09-18 10:46
- Final attempt: batch `corrected_prompt_pilot_5_20260918` (09-18 10:46)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 212937 bytes; files touched (1): go.work.sum
- Copy: `patches/flipt-io-9d25c18b.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_baseline/instance_flipt-io__flipt-9d25c18b79bc7829a6fb08ec9e8793d5d17e2868
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
- NOTE: evaluator evidence may predate the final attempt - verify or re-run.
### Trace
- 317218 bytes at `/Users/zt/swebench-thesis/outputs/corrected_prompt_pilot_5_20260918/instance_flipt-io__flipt-9d25c18b79bc7829a6fb08ec9e8793d5d17e2868/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)