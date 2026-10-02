# Case file - instance_gravitational__teleport-db89206db6c2969266e664c7c0fb51b70e958b64

**Repo:** gravitational  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_gravitational__teleport-db89206db6c2969266e664c7c0fb51b70e958b64 @2026-08-26 03:37; rerun_23 @2026-08-28 13:40
- Final attempt: batch `rerun_23` (08-28 13:40)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 53088 bytes; files touched (5): lib/client/api.go; lib/service/service.go; tool/tsh/db.go; tool/tsh/tsh.go; tool/tsh/tsh_test.go
- Copy: `patches/gravitational-db89206d.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_rerun/instance_gravitational__teleport-db89206db6c2969266e664c7c0fb51b70e958b64
- Failed tests / errors: {"tests": [{"name": "TestFetchDatabaseCreds", "status": "PASSED"}, {"name": "TestOIDCLogin", "status": "FAILED"}, {"name": "TestMakeClient", "status": "FAILED"}

### Trace
- 940956 bytes at `/Users/zt/swebench-thesis/outputs/rerun_23/instance_gravitational__teleport-db89206db6c2969266e664c7c0fb51b70e958b64/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Tests ran: TestOIDCLogin and TestMakeClient FAILED; 5-file 53KB patch left behavioural gaps (time exhausted, 600s era). Not IG-C: tests executed.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)