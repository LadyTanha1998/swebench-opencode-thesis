#!/usr/bin/env python3
"""
Automation script: runs OpenCode on a batch of SWE-bench Lite tasks.

For each task:
  1. Auto-clone the repo from GitHub if not already present locally
  2. Reset repo to clean state
  3. Checkout the task's base_commit (buggy version)
  4. Run OpenCode (non-interactive) with the bug report, no internet access
  5. Capture the resulting git diff as the agent's patch
  6. Save patch + agent reasoning trace into a SWE-bench-compatible predictions.jsonl file

After this script finishes, run Docker evaluation separately with:
  python -m swebench.harness.run_evaluation \
    --predictions_path predictions_batch.jsonl \
    --max_workers 4 \
    --run_id batch_run_1

Usage:
  # Full 300-task experiment (1 run each):
  python3 run_swebench_batch.py \
    --repos astropy,django,sympy,scikit-learn,matplotlib,pytest,sphinx,requests,pylint,xarray,seaborn,flask \
    --per_repo 120 --runs 1 --output predictions_300tasks.jsonl

  # Quick test — 1 task from astropy:
  python3 run_swebench_batch.py --repos astropy --per_repo 1 --runs 1 --output test_run.jsonl

  # Multiple repos, explicit count per repo:
  python3 run_swebench_batch.py --repos astropy,django,sympy,scikit-learn --per_repo 6

  # With repetitions for variance testing:
  python3 run_swebench_batch.py --repos astropy --per_repo 6 --runs 5

Repos are cloned automatically from GitHub if not already present locally.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

# ── Repo locations on this machine ───────────────────────────────────────────

REPO_DIRS = {
    "astropy":      Path.home() / "astropy",
    "django":       Path.home() / "django",
    "sympy":        Path.home() / "sympy",
    "scikit-learn": Path.home() / "scikit-learn",
    "matplotlib":   Path.home() / "matplotlib",
    "pytest":       Path.home() / "pytest",
    "sphinx":       Path.home() / "sphinx",
    "requests":     Path.home() / "requests",
    "pylint":       Path.home() / "pylint",
    "xarray":       Path.home() / "xarray",
    "seaborn":      Path.home() / "seaborn",
    "flask":        Path.home() / "flask",
}

# ── GitHub URLs for auto-cloning ─────────────────────────────────────────────

REPO_URLS = {
    "astropy":      "https://github.com/astropy/astropy.git",
    "django":       "https://github.com/django/django.git",
    "sympy":        "https://github.com/sympy/sympy.git",
    "scikit-learn": "https://github.com/scikit-learn/scikit-learn.git",
    "matplotlib":   "https://github.com/matplotlib/matplotlib.git",
    "pytest":       "https://github.com/pytest-dev/pytest.git",
    "sphinx":       "https://github.com/sphinx-doc/sphinx.git",
    "requests":     "https://github.com/psf/requests.git",
    "pylint":       "https://github.com/pylint-dev/pylint.git",
    "xarray":       "https://github.com/pydata/xarray.git",
    "seaborn":      "https://github.com/mwaskom/seaborn.git",
    "flask":        "https://github.com/pallets/flask.git",
}

MODEL = "opencode/deepseek-v4-flash-free"
MODEL_NAME = "opencode-deepseek-v4-flash-free"


# ── Helper functions ──────────────────────────────────────────────────────────

def get_repo_dir(repo_full_name):
    """Map a SWE-bench 'repo' field (e.g. 'django/django') to local clone path."""
    for key, path in REPO_DIRS.items():
        if key in repo_full_name:
            return key, path
    return None, None


def ensure_repo_cloned(repo_key, repo_dir):
    """Clone the repo from GitHub if it doesn't exist locally yet."""
    if repo_dir.exists():
        return True  # already cloned, nothing to do

    url = REPO_URLS.get(repo_key)
    if not url:
        print(f"  ERROR: No GitHub URL configured for '{repo_key}'")
        return False

    print(f"  Repo not found locally — cloning from {url} ...")
    print(f"  (This only happens once. It may take a few minutes for large repos.)")
    result = subprocess.run(
        ["git", "clone", url, str(repo_dir)],
        capture_output=False,  # show progress to user
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: Failed to clone {url}")
        return False

    print(f"  Cloned successfully to {repo_dir}")
    return True


def run_cmd(cmd, cwd=None, timeout=600):
    """Run a shell command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        return -1, out, err + "\n[TIMEOUT EXPIRED]"


def reset_repo(repo_dir):
    """Discard all changes and untracked files in the given repo."""
    run_cmd("git checkout -- .", cwd=repo_dir)
    run_cmd("git clean -fd", cwd=repo_dir)


def checkout_commit(repo_dir, commit):
    reset_repo(repo_dir)
    code, out, err = run_cmd(f"git checkout {commit}", cwd=repo_dir)
    return code == 0


def build_prompt(problem_statement):
    return (
        "Important: Do NOT search the internet, do NOT fetch any URLs, "
        "do NOT look up GitHub PRs. Only use the code in this repository.\n\n"
        "Bug report:\n"
        f"{problem_statement}\n\n"
        "Find the relevant file(s), identify the bug, and apply a fix directly "
        "to the code. Do not just describe the fix -- actually edit the files."
    )


def run_opencode(repo_dir, prompt, timeout=480):
    """Run OpenCode non-interactively with the given prompt."""
    prompt_file = Path("/tmp/opencode_prompt.txt")
    prompt_file.write_text(prompt)

    cmd = (
        f'opencode run "$(cat {prompt_file})" '
        f"--model {MODEL} "
        f"--dangerously-skip-permissions"
    )
    code, out, err = run_cmd(cmd, cwd=repo_dir, timeout=timeout)
    return code, out, err


def capture_patch(repo_dir):
    code, out, err = run_cmd("git diff", cwd=repo_dir)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=30, help="number of tasks to run")
    parser.add_argument("--runs", type=int, default=1, help="repetitions per task")
    parser.add_argument("--repos", type=str, default="astropy,django,sympy,scikit-learn",
                        help="comma-separated list of repo keywords to include")
    parser.add_argument("--per_repo", type=int, default=None,
                        help="max tasks to take from each repo (overrides even split if set)")
    parser.add_argument("--output", type=str, default="predictions_batch.jsonl")
    parser.add_argument("--start", type=int, default=0,
                        help="start index within each repo's task list (for resuming)")
    args = parser.parse_args()

    print("Loading SWE-bench Lite dataset...")
    from datasets import load_dataset
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")

    repo_keywords = [r.strip() for r in args.repos.split(",")]

    # Group dataset tasks by repo keyword
    tasks = []
    for repo_kw in repo_keywords:
        repo_tasks = [t for t in dataset if repo_kw in t["repo"]]
        repo_key, repo_dir = get_repo_dir(repo_kw)

        if repo_dir is None:
            print(f"  WARNING: '{repo_kw}' not in known repo list — skipping")
            continue

        # Auto-clone if not present
        if not ensure_repo_cloned(repo_key, repo_dir):
            print(f"  Skipping '{repo_kw}' — could not clone repo")
            continue

        limit = args.per_repo if args.per_repo is not None else max(1, args.n // len(repo_keywords))
        selected = repo_tasks[args.start: args.start + limit]
        print(f"  {repo_kw}: {len(repo_tasks)} available in dataset, selected {len(selected)}")
        for t in selected:
            tasks.append((t, repo_dir))

    print(f"\nTotal tasks selected across all repos: {len(tasks)}")

    results_log = []
    predictions = []
    output_path = args.output
    log_path = output_path.replace(".jsonl", "_runlog.json")

    # Load existing progress if resuming
    completed_keys = set()
    if Path(output_path).exists():
        with open(output_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    key = (entry["instance_id"], entry["model_name_or_path"])
                    completed_keys.add(key)
                    predictions.append(entry)
                except Exception:
                    pass
        print(f"Resuming: found {len(completed_keys)} already-completed runs in {output_path}")

    for i, (task, repo_dir) in enumerate(tasks):
        instance_id = task["instance_id"]
        commit = task["base_commit"]
        problem = task["problem_statement"]

        print(f"\n[{i+1}/{len(tasks)}] {instance_id} (repo: {repo_dir.name}, commit {commit[:10]})")

        for run_num in range(1, args.runs + 1):
            model_name = f"{MODEL_NAME}-run{run_num}"

            # Skip if already completed (resume support)
            if (instance_id, model_name) in completed_keys:
                print(f"  Run {run_num}/{args.runs}... SKIPPED (already completed)")
                continue

            print(f"  Run {run_num}/{args.runs}...")
            t0 = time.time()

            ok = checkout_commit(repo_dir, commit)
            if not ok:
                print(f"  FAILED to checkout commit for {instance_id}")
                results_log.append({"instance_id": instance_id, "run": run_num,
                                    "status": "checkout_failed"})
                continue

            prompt = build_prompt(problem)
            code, out, err = run_opencode(repo_dir, prompt)
            patch = capture_patch(repo_dir)
            elapsed = time.time() - t0

            status = "ok" if patch.strip() else "empty_patch"
            if code == -1:
                status = "timeout"
            elif code != 0:
                status = "opencode_error"

            print(f"  Status: {status} | elapsed: {elapsed:.0f}s | patch length: {len(patch)} chars")

            entry = {
                "instance_id": instance_id,
                "model_name_or_path": model_name,
                "model_patch": patch,
                "agent_trace": out,    # full reasoning trace: files opened, decisions made, etc.
            }
            predictions.append(entry)

            # Incremental save after every run
            with open(output_path, "a") as f:
                f.write(json.dumps(entry) + "\n")

            results_log.append({
                "instance_id": instance_id,
                "repo": repo_dir.name,
                "run": run_num,
                "status": status,
                "elapsed_seconds": round(elapsed, 1),
                "patch_length": len(patch),
                "opencode_returncode": code,
            })

            with open(log_path, "w") as f:
                json.dump(results_log, f, indent=2)

            reset_repo(repo_dir)


if __name__ == "__main__":
    main()
