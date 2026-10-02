# Case file - instance_flipt-io__flipt-2ce8a0331e8a8f63f2c1b555db8277ffe5aa2e63

**Repo:** flipt-io  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_flipt-io__flipt-2ce8a0331e8a8f63f2c1b555db8277ffe5aa2e63 @2026-08-25 16:16; final_3task_check @2026-09-07 18:10; final_3task_check_v3 @2026-09-07 20:15
- Final attempt: batch `final_3task_check_v3` (09-07 20:15)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 7009 bytes; files touched (3): go.work.sum; internal/cmd/grpc.go; internal/server/middleware/grpc/middleware.go
- Copy: `patches/flipt-io-2ce8a033.diff`
### Evaluator
- Evidence dir: outputs/eval_calibration/rerun_3task/instance_flipt-io__flipt-2ce8a0331e8a8f63f2c1b555db8277ffe5aa2e63
- Failed tests / errors: TODO

### Trace
- 342910 bytes at `/Users/zt/swebench-thesis/outputs/final_3task_check_v3/instance_flipt-io__flipt-2ce8a0331e8a8f63f2c1b555db8277ffe5aa2e63/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: gRPC middleware wiring edited; eval identical; failures beyond excerpt - coded IG-B by default rule (no build signature). Not IG-C: no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)