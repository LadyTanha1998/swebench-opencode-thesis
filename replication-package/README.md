# Replication Package - Layer-2 Failure Taxonomy Study

Per-task evidence files for the 93 Incomplete Generation (IG) failures
(SWE-bench Pro, OpenCode + DeepSeek agent). Generated from the experiment audit
(`digest2_summary.csv`) and the raw `outputs/` tree.

## Final Layer-2 distribution (93 tasks)
| Category | Definition | n | % |
|---|---|---|---|
| IG-A (empty patch) | Final attempt produced a 0-byte patch | 21 | 23% |
| IG-D (artifact-only diff) | Final patch contains only auto-generated dependency/build artefacts (lockfiles, checksum caches, vendor pointers, bundled assets); no task-relevant source change | 16 | 17% |
| IG-B (partial implementation) | Real code written; a required piece is missing | 55 | 59% |
| IG-C (integration failure) | Patch present but the patched package fails to compile | 1 | 1% |

IG-D was created as its own category (rather than folding these tasks into
IG-A) following supervisor guidance (2026-09-30): the phenomenon - non-empty
diffs of up to ~213KB containing zero task-relevant change - is qualitatively
distinct from both empty patches and partial implementations. IG-C is retained
despite n=1: it is defined by an objective criterion (the patched package fails
to build; verified in the evaluator log of gravitational-3fa69043), and merging
it into IG-B would misrepresent the mechanism. Its rarity is a finding: 55/56
real-patch failures (98%) are partial implementations.

## Coding protocol
Layer-2 labels were proposed from per-task evidence briefs (`coding/`) by an
LLM assistant and reviewed and adjudicated by the author; the category
structure was discussed with the supervisor before finalisation (email trail,
2026-09-30). Cross-cutting factors (e.g. time exhaustion) are recorded per task
in `data/final_labels.csv` rather than as subcategories.

## Layout
- `cases/` - 93 case files: processing history, final patch, evaluator output, classification + rationale.
- `patches/` - the final patch of each task's final attempt.
- `evaluator/` - evaluator artefacts where located.
- `coding/` - evidence briefs + decision rules used during coding.
- `data/final_labels.csv` - master sheet (labels, rationales, provenance notes).
- `data/master_dataset.csv` - all 253 processed tasks: outcome, main Layer-1 label, second-layer form for IG, processing history and evidence pointers.
- `SECRET_SCAN.txt` - auto secrets scan (review before making the repo public).

## Method notes
- Final attempt = latest attempt by file modification time (thesis rule 3.5).
- Layer-1 labels are frozen from the published study; only Layer-2 is coded here.
- Where evaluator output was truncated, tasks were coded IG-B by default after a
  systematic build-failure scan of all eval folders found no build errors (the
  only scan hits were the harness's own parser source - false positives).
- Teleport eval caveat: some eval runs show environment-level build failures in
  packages untouched by the agent; labels use the patched package's own result.
- Traces are referenced by path but not copied (size + secrets scrub pending).
