# Case file - instance_gravitational__teleport-288c5519ce0dec9622361a5e5d6cd36aa2d9e348

**Repo:** gravitational  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_gravitational__teleport-288c5519ce0dec9622361a5e5d6cd36aa2d9e348 @2026-08-26 04:45; main_rerun_batch_01 @2026-09-08 14:28
- Final attempt: batch `main_rerun_batch_01` (09-08 14:28)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 6523 bytes; files touched (4): api/client/proto/authservice.pb.go; api/client/proto/authservice.proto; lib/auth/db.go; tool/tctl/common/auth_command.go
- Copy: `patches/gravitational-288c5519.diff`
### Evaluator
- Evidence dir: outputs/vuls_teleport_three_reuse_eval_17/instance_gravitational__teleport-288c5519ce0dec9622361a5e5d6cd36aa2d9e348
- Failed tests / errors: {"tests": [{"name": "TestCheckKubeCluster", "status": "PASSED"}, {"name": "TestCheckKubeCluster/non-k8s_output_format", "status": "PASSED"}, {"name": "TestCheck
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 371206 bytes at `/Users/zt/swebench-thesis/outputs/main_rerun_batch_01/instance_gravitational__teleport-288c5519ce0dec9622361a5e5d6cd36aa2d9e348/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Named tests ran (TestCheckKubeCluster et al.) so the build succeeded; behavioural gaps remain in the auth/db changes including generated protobuf edits. Not IG-C: compilation succeeded.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)