# Case file - instance_internetarchive__openlibrary-123e6e5e1c85b9c07d1e98f70bfc480bc8016890-v2733ff199fb72f0d033a30dc62cb0a4742e3a7f4

**Repo:** internetarchive  |  **Layer 1 (Tambon, frozen):** Incomplete Generation  |  **Label status:** CONFIRMED

## 1. Task requirements
- TODO: paste 2-5 bullets from the problem_statement (dataset JSONL).

## 2. Processing history
- Attempts (oldest to newest): instance_internetarchive__openlibrary-123e6e5e1c85b9c07d1e98f70bfc480bc8016890-v2733ff199fb72f0d033a30dc62cb0a4742e3a7f4 @2026-08-26 07:31
- Final attempt: batch `(original)` (08-26 07:31)
- Mechanical repair involved: TODO (check audit sheet)

## 3. Evidence
### Final patch
- Size: 4463 bytes; files touched (3): scripts/affiliate_server.py; scripts/tests/test_affiliate_server.py; vendor/infogami
- Copy: `patches/internetarchive-123e6e5e.diff`
### Evaluator
- Evidence dir: outputs/openlibrary_three_reuse_eval_11/instance_internetarchive__openlibrary-123e6e5e1c85b9c07d1e98f70bfc480bc8016890-v2733ff199fb72f0d033a30dc62cb0a4742e3a7f4
- Failed tests / errors: TODO

### Trace
- 70324 bytes at `/Users/zt/swebench-thesis/outputs/instance_internetarchive__openlibrary-123e6e5e1c85b9c07d1e98f70bfc480bc8016890-v2733ff199fb72f0d033a30dc62cb0a4742e3a7f4/run1/trace.json` (not copied into package)

## 4. Classification (Layer 2 - this study)
- Label: **IG-B (partial implementation)**
- Rationale: affiliate_server.py + test edited; implementation incomplete. Not IG-C: no build failure.
- Associated factors: time exhausted = No | context exhausted = TODO
- Ambiguous: TODO

## 5. Reviewer notes
- (second-coder notes)