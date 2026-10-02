# Case file - instance_protonmail__webclients-d8ff92b414775565f496b830c9eb6cc5fa9620e6

**Repo:** protonmail  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_protonmail__webclients-d8ff92b414775565f496b830c9eb6cc5fa9620e6 @2026-08-26 13:55
- Final attempt: batch `(original)` (08-26 13:55)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 164774 bytes; files touched (9): applications/drive/src/app/store/_views/useShareMemberViewZustand.tsx; applications/drive/src/app/zustand/share/invitations.store.ts; applications/drive/src/app/zustand/share/members.store.ts; applications/drive/src/app/zustand/share/types.ts; packages/drive-store/store/_views/useShareMemberViewZustand.tsx; packages/drive-store/zustand/share/invitations.store.ts; packages/drive-store/zustand/share/members.store.ts; packages/drive-store/zustand/share/types.ts; yarn.lock
- Copy: `patches/protonmail-d8ff92b4.diff`
### Evaluator
- Evidence dir: outputs/protonmail_d8ff92_eval_21/instance_protonmail__webclients-d8ff92b414775565f496b830c9eb6cc5fa9620e6
- Failed tests / errors: TODO
- NOTE: the evaluated patch differs from the final agent patch - verify which artefact the evaluator consumed.
### Trace
- 659911 bytes at `/Users/zt/swebench-thesis/outputs/instance_protonmail__webclients-d8ff92b414775565f496b830c9eb6cc5fa9620e6/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: 9-file zustand refactor (eval stripped to 36KB); judged source only - incomplete. Not IG-C: no build failure.
- Associated factors: time exhausted = Yes (final attempt timed out) | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)