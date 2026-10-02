# Case file - instance_protonmail__webclients-6dcf0d0b0f7965ad94be3f84971afeb437f25b02

**Repo:** protonmail  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_protonmail__webclients-6dcf0d0b0f7965ad94be3f84971afeb437f25b02 @2026-08-26 14:42
- Final attempt: batch `(original)` (08-26 14:42)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 791466 bytes; files touched (3): applications/drive/public/assets/sandbox.js; applications/mail/public/assets/sandbox.js; yarn.lock
- Copy: `patches/protonmail-6dcf0d0b.diff`
### Evaluator
- Evidence dir: outputs/protonmail_6dc_6e_815_8afd_eval/instance_protonmail__webclients-6dcf0d0b0f7965ad94be3f84971afeb437f25b02
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 178922 bytes at `/Users/zt/swebench-thesis/outputs/instance_protonmail__webclients-6dcf0d0b0f7965ad94be3f84971afeb437f25b02/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-D (artifact-only diff)**
- Rationale: Final patch touches only auto-generated dependency/build files (lockfiles, checksum caches, vendor pointers, bundled assets) - no task-relevant source change; the diff is non-empty but generation of solution code never started. Coded as its own category IG-D per TA guidance (2026-09-30): categories may be created where phenomena differ sufficiently. Distinct from IG-A (truly empty patch) and IG-B (genuine partial implementation).
- Note: Reclassified from IG-A (tie-breaker T2b) to IG-D following TA email (2026-09-30).
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)