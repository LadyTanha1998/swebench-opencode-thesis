# Case file - instance_gravitational__teleport-bb69574e02bd62e5ccd3cebb25e1c992641afb2a

**Repo:** gravitational  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_gravitational__teleport-bb69574e02bd62e5ccd3cebb25e1c992641afb2a @2026-08-26 04:05; main_rerun_batch_01 @2026-09-08 18:46
- Final attempt: batch `main_rerun_batch_01` (09-08 18:46)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 3728 bytes; files touched (2): lib/services/user.go; lib/utils/parse/parse.go
- Copy: `patches/gravitational-bb69574e.diff`
### Evaluator
- Evidence dir: outputs/teleport_three_reuse_eval_20/instance_gravitational__teleport-bb69574e02bd62e5ccd3cebb25e1c992641afb2a
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 298632 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_batch_01/instance_gravitational__teleport-bb69574e02bd62e5ccd3cebb25e1c992641afb2a/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: user.go + parse.go edited; required behaviour incomplete. Not IG-C: no build failure in the patched package.
- Note: PROVENANCE FOOTNOTE: eval patch 1,466B smaller than final with no lockfile explanation - verify which attempt was evaluated.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)