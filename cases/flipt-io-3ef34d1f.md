# Case file - instance_flipt-io__flipt-3ef34d1fff012140ba86ab3cafec8f9934b492be

**Repo:** flipt-io  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_flipt-io__flipt-3ef34d1fff012140ba86ab3cafec8f9934b492be @2026-08-25 17:35; final_3task_check @2026-09-07 18:21; final_3task_check_v3 @2026-09-07 20:47
- Final attempt: batch `final_3task_check_v3` (09-07 20:47)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 147643 bytes; files touched (3): go.work.sum; internal/cmd/grpc.go; internal/server/middleware/grpc/middleware.go
- Copy: `patches/flipt-io-3ef34d1f.diff`
### Evaluator
- Evidence dir: outputs/eval_calibration/rerun_3task/instance_flipt-io__flipt-3ef34d1fff012140ba86ab3cafec8f9934b492be
- Failed tests / errors: TODO

### Trace
- 350104 bytes at `/Users/zt/swebench-thesis/outputs/final_3task_check_v3/instance_flipt-io__flipt-3ef34d1fff012140ba86ab3cafec8f9934b492be/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Ran the full 1,800s and still timed out (time exhausted); ~148KB patch largely churn - implementation incomplete. Not IG-C: no build signature in the patched package.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)