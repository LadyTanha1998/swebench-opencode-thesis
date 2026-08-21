# SWE-bench OpenCode Thesis

Master's thesis project — University of Luxembourg  
**Research question:** How well does an AI coding agent (OpenCode) automatically fix real GitHub bugs from the SWE-bench Pro benchmark?

---

## Overview

This repository contains the automation script used to run [OpenCode](https://opencode.ai) on [SWE-bench Pro](https://github.com/scaleapi/SWE-bench_Pro-os) — a benchmark of ~700 real GitHub bug-fixing tasks across multiple repositories.

**Pipeline:**
1. For each task, pulls the official SWE-bench Docker image with the repo at the buggy commit and all dependencies pre-installed
2. Runs OpenCode inside the container with the bug report — network restricted to LLM API only via Squid proxy
3. Extracts the patch (code fix) from the container via `git diff`
4. Saves results to a `.jsonl` file for evaluation
5. Cleans up the container and Docker image

**Evaluation:** Patches are verified using the official SWE-bench Docker harness (`swebench.harness.run_evaluation`).

---

## Requirements

- **OpenCode** binary at `~/.opencode/bin/opencode` (v1.18.20+)
- **Python** 3.11+
- **Docker** running
- Sufficient disk space (~2-5GB per task image, images are removed after use)

### Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv test-env
   source test-env/bin/activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure OpenCode (`opencode.json`):
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "permission": {
       "webfetch": "deny",
       "websearch": "deny"
     },
     "agent": {
       "build": {
         "temperature": 0.8
       }
     }
   }
   ```

> Web fetch and web search are explicitly disabled — the agent can only use local repository files.

---

## Network Isolation

A Squid proxy container restricts network access during agent execution:

- **Allowed:** `*.opencode.ai`, `opencode.ai`, `models.opencode.ai` (LLM API only)
- **Blocked:** Everything else (pip, npm, github.com, etc.)

This prevents the agent from:
- Fetching solutions from the internet
- Installing packages that might contain the fix
- Accessing GitHub to pull the merged PR

The proxy is automatically started and stopped by the batch script.

---

## Usage

```bash
source test-env/bin/activate

# Run 253 tasks with stratified sampling (default)
python3 run_swebench_batch.py --sample-size 253 --seed 42

# Quick test — 1 task from NodeBB
python3 run_swebench_batch.py --repos NodeBB --n 1

# With a different model
python3 run_swebench_batch.py --repos NodeBB --n 1 --model opencode/mimo-v2.5-free
```

### Arguments

| Argument | Description |
|----------|-------------|
| `--n` | Number of tasks to run (default: all) |
| `--runs` | Number of repetitions per task |
| `--repos` | Comma-separated list of repo keywords |
| `--start` | Start index within each repo's task list (for resuming) |
| `--sample-size` | Number of tasks to sample using stratified sampling (default: 253) |
| `--seed` | Random seed for stratified sampling (default: 42) |
| `--model` | OpenCode model to use (default: `opencode/mimo-v2.5-free`) |

---

## Output Format

### Per-Task Output

Each task run produces the following directory structure:

```
outputs/
  <instance_id>/
    run1/
      _docker_output/    # Raw output from the Docker container
        opencode-logs/   # OpenCode log files
        trace.json       # Full JSON event stream from opencode
        session.json     # OpenCode session export
        prompt.txt       # The prompt sent to the agent
      patch.diff         # The git diff produced by the agent
      summary.json       # Structured summary (status, tokens, tool calls, etc.)
      predictions.jsonl  # Single-entry prediction file for this run
      stderr.log         # Docker stderr (only if present)
      proxy_access.log   # Squid proxy access log for this run
    run2/                # Additional runs (if --runs > 1)
      ...
  runlog.json            # Overall run log across all tasks
  predictions_all.jsonl  # Aggregated predictions for SWE-bench evaluation
```

### Aggregated Predictions

Each line of `predictions_all.jsonl` is one run:

```json
{
  "instance_id": "instance_NodeBB__NodeBB-f083cd559d69c16481376868c8da65172729c0ca-vnan",
  "model_name_or_path": "opencode-mimo-v2.5-free-run1",
  "model_patch": "diff --git a/src/database/mongo/sorted.js ..."
}
```

The `runlog.json` contains status, elapsed time, and patch length for each run.

---

## Evaluation

SWE-bench Pro uses a different evaluation approach. First, convert the predictions to the expected format:

```bash
source test-env/bin/activate

python convert_predictions.py outputs/predictions_all.jsonl outputs/predictions_swebench_pro.json
```

Then run the evaluation:

```bash
python -m swebench.harness.run_evaluation \
  --dataset_name ScaleAI/SWE-bench_Pro \
  --predictions_path outputs/predictions_swebench_pro.json \
  --max_workers 4 \
  --run_id full_experiment
```

Results are written to `logs/run_evaluation/<run_id>/`.

---

## Repository Structure

```
run_swebench_batch.py     # Main automation script
convert_predictions.py    # Convert predictions to SWE-bench Pro format
requirements.txt          # Python dependencies
opencode.json             # OpenCode configuration
proxy/                    # Squid proxy configuration
  Dockerfile.proxy        # Proxy container definition
  squid.conf              # Whitelist rules
outputs/                  # Run outputs (gitignored)
test-env/                 # Python virtual environment
```

---

## References

- SWE-bench: [princeton-nlp/SWE-bench](https://github.com/princeton-nlp/SWE-bench)
- OpenCode: [opencode.ai](https://opencode.ai)
- Bug taxonomy: Tambon et al. (2024), arXiv:2403.08937
