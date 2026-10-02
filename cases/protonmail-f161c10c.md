# Case file - instance_protonmail__webclients-f161c10cf7d31abf82e8d64d7a99c9fac5acfa18

**Repo:** protonmail  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_protonmail__webclients-f161c10cf7d31abf82e8d64d7a99c9fac5acfa18 @2026-08-26 12:55; protonmail_remaining_rerun_v5_gcompat_timerfix @2026-09-14 10:12
- Final attempt: batch `protonmail_remaining_rerun_v5_gcompat_timerfix` (09-14 10:12)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 72209 bytes; files touched (3): packages/shared/lib/contacts/helpers/csvFormat.ts; packages/shared/lib/contacts/property.ts; yarn.lock
- Copy: `patches/protonmail-f161c10c.diff`
### Evaluator
- Evidence dir: outputs/protonmail_f161_eval_gcompat_v3/instance_protonmail__webclients-f161c10cf7d31abf82e8d64d7a99c9fac5acfa18
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 400575 bytes at `/Users/zt/swebench-thesis/outputs/protonmail_remaining_rerun_v5_gcompat_timerfix/instance_protonmail__webclients-f161c10cf7d31abf82e8d64d7a99c9fac5acfa18/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Judged csvFormat.ts + property.ts (yarn.lock stripped); incomplete; time exhausted. Not IG-C: no build failure.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)