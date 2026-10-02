# Case file - instance_element-hq__element-web-4c6b0d35add7ae8d58f71ea1711587e31081444b-vnan

**Repo:** element-hq  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_element-hq__element-web-4c6b0d35add7ae8d58f71ea1711587e31081444b-vnan @2026-08-25 11:14; final_3task_check @2026-09-07 17:58; final_3task_check_v3 @2026-09-07 19:53
- Final attempt: batch `final_3task_check_v3` (09-07 19:53)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 5005 bytes; files touched (1): src/PosthogAnalytics.ts
- Copy: `patches/element-hq-4c6b0d35.diff`
### Evaluator
- Evidence dir: outputs/eval_calibration/rerun_3task/instance_element-hq__element-web-4c6b0d35add7ae8d58f71ea1711587e31081444b-vnan
- Failed tests / errors: TODO

### Trace
- 257082 bytes at `/Users/zt/swebench-thesis/outputs/final_3task_check_v3/instance_element-hq__element-web-4c6b0d35add7ae8d58f71ea1711587e31081444b-vnan/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Single PosthogAnalytics.ts change; failures not captured - coded IG-B by default rule (no build signature). Not IG-C: no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)