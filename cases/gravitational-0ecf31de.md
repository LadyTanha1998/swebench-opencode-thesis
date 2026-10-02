# Case file - instance_gravitational__teleport-0ecf31de0e98b272a6a2610abe1bbedd379a38a3-vce94f93ad1030e3136852817f2423c1b3ac37bc4

**Repo:** gravitational  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_gravitational__teleport-0ecf31de0e98b272a6a2610abe1bbedd379a38a3-vce94f93ad1030e3136852817f2423c1b3ac37bc4 @2026-08-26 03:26; rerun_23 @2026-08-28 12:03; rerun_0ecf_infra_repaired @2026-09-16 15:25
- Final attempt: batch `rerun_0ecf_infra_repaired` (09-16 15:25)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 1617 bytes; files touched (1): lib/utils/prompt/context_reader.go
- Copy: `patches/gravitational-0ecf31de.diff`
### Evaluator
- Evidence dir: outputs/0ecf_infra_repaired_eval/instance_gravitational__teleport-0ecf31de0e98b272a6a2610abe1bbedd379a38a3-vce94f93ad1030e3136852817f2423c1b3ac37bc4
- Failed tests / errors: TODO

### Trace
- 351170 bytes at `/Users/zt/swebench-thesis/outputs/rerun_0ecf_infra_repaired/instance_gravitational__teleport-0ecf31de0e98b272a6a2610abe1bbedd379a38a3-vce94f93ad1030e3136852817f2423c1b3ac37bc4/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Tiny single-file patch (context_reader.go) after an infra-repaired timeout; no failures captured - coded IG-B by default rule (no build signature in eval folder). Not IG-C: no build failure.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)