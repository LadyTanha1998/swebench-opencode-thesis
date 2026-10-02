# Case file - instance_protonmail__webclients-cfd7571485186049c10c822f214d474f1edde8d1

**Repo:** protonmail  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_protonmail__webclients-cfd7571485186049c10c822f214d474f1edde8d1 @2026-08-26 12:32; protonmail_4_rerun_gcompat_timerfix @2026-09-14 13:09
- Final attempt: batch `protonmail_4_rerun_gcompat_timerfix` (09-14 13:09)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 74220 bytes; files touched (4): packages/components/components/addressesAutomplete/AddressesAutocomplete.tsx; packages/components/components/v2/addressesAutomplete/AddressesAutocomplete.tsx; packages/shared/lib/mail/recipient.ts; yarn.lock
- Copy: `patches/protonmail-cfd75714.diff`
### Evaluator
- Evidence dir: outputs/protonmail_944_ae36_cfd_eval/instance_protonmail__webclients-cfd7571485186049c10c822f214d474f1edde8d1
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 336221 bytes at `/Users/zt/swebench-thesis/outputs/protonmail_4_rerun_gcompat_timerfix/instance_protonmail__webclients-cfd7571485186049c10c822f214d474f1edde8d1/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: Judged the AddressesAutocomplete files + recipient.ts (yarn.lock stripped); incomplete; time exhausted. Not IG-C: no build failure.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)