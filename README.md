# SWE-bench OpenCode Thesis

Master's thesis project — University of Luxembourg  
**Research question:** How well does an AI coding agent (OpenCode) automatically fix real GitHub bugs from the SWE-bench Lite benchmark?

---

## Overview

This repository contains the automation script used to run [OpenCode](https://opencode.ai) on [SWE-bench Lite](https://github.com/princeton-nlp/SWE-bench) — a benchmark of 300 real GitHub bug-fixing tasks across 12 Python repositories.

**Pipeline:**
1. For each task, pulls the official SWE-bench Docker image with the repo at the buggy commit and all dependencies pre-installed
2. Runs OpenCode inside the container with the bug report — network restricted to LLM API only via Squid proxy
3. Extracts the patch (code fix) from the container via `git diff`
4. Saves results to a `.jsonl` file for evaluation
5. Cleans up the container and Docker image

**Evaluation:** Patches are verified using the official SWE-bench Docker harness (`swebench.harness.run_evaluation`).

---

## Requirements

- **OpenCode** v1.17.7 installed globally (`npm install -g opencode-ai`)
- **Python** 3.11+
- **Docker Desktop** running
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

# Run all 300 tasks, 1 run each (full experiment)
python3 run_swebench_batch.py \
  --repos astropy,django,sympy,scikit-learn,matplotlib,pytest,sphinx,requests,pylint,xarray,seaborn,flask \
  --per_repo 120 \
  --runs 1

# Quick test — 1 task from astropy
python3 run_swebench_batch.py --repos astropy --per_repo 1 --runs 1

# With a different model
python3 run_swebench_batch.py --repos astropy --per_repo 1 --model opencode/gpt-4o
```

### Arguments

| Argument | Description |
|----------|-------------|
| `--repos` | Comma-separated list of repo keywords |
| `--per_repo` | Max tasks per repository |
| `--runs` | Number of repetitions per task |
| `--start` | Start index within each repo's task list (for resuming) |
| `--model` | OpenCode model to use (default: `opencode/deepseek-v4-flash-free`) |

---

## Output Format

### Per-Task Output

Each task run produces the following directory structure:

```
outputs/
  <instance_id>/
    run1/
      _docker_output/    # Raw output from the Docker container
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
  "instance_id": "astropy__astropy-6938",
  "model_name_or_path": "opencode-deepseek-v4-flash-free-run1",
  "model_patch": "diff --git a/..."
}
```

The `runlog.json` contains status, elapsed time, and patch length for each run.

---

## Evaluation

```bash
source test-env/bin/activate

python -m swebench.harness.run_evaluation \
  --predictions_path outputs/predictions_all.jsonl \
  --max_workers 4 \
  --run_id full_experiment
```

Results are written to `logs/run_evaluation/<run_id>/`.

---

## Results So Far

| Experiment | Tasks | Runs | Resolved | Rate |
|-----------|-------|------|----------|------|
| 30-task batch (single run) | 30 | 1 | 17 | 56.7% |
| Variance test | 18 | 5 | avg 56.3% | — |

Model used: `opencode/deepseek-v4-flash-free` via Zen provider.

---

## Repository Structure

```
run_swebench_batch.py     # Main automation script
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
