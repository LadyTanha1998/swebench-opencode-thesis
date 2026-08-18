#!/usr/bin/env python3
"""
Automation script: runs OpenCode on a batch of SWE-bench Lite tasks.

For each task:
  1. Reset astropy repo to clean state
  2. Checkout the task's base_commit (buggy version)
  3. Run OpenCode (non-interactive) with the bug report, no internet access
  4. Capture the resulting git diff as the agent's patch
  5. Save patch into a SWE-bench-compatible predictions.jsonl file

After this script finishes, run Docker evaluation separately with:
  python -m swebench.harness.run_evaluation \
    --predictions_path predictions_batch.jsonl \
    --max_workers 4 \
    --run_id batch_run_1

Usage:
  # Single repo (legacy-style, still works):
  python3 run_swebench_batch.py --n 6 --repos astropy

  # Multiple repos, ~30 tasks total split evenly:
  python3 run_swebench_batch.py --n 30 --repos astropy,django,sympy,scikit-learn

  # Explicit count per repo (recommended for control):
  python3 run_swebench_batch.py --repos astropy,django,sympy,scikit-learn --per_repo 6

  # With repetitions for variance testing:
  python3 run_swebench_batch.py --repos astropy --per_repo 6 --runs 5

Requires each repo to be cloned locally first:
  git clone https://github.com/astropy/astropy.git ~/astropy
  git clone https://github.com/django/django.git ~/django
  git clone https://github.com/sympy/sympy.git ~/sympy
  git clone https://github.com/scikit-learn/scikit-learn.git ~/scikit-learn
  git clone https://github.com/matplotlib/matplotlib.git ~/matplotlib
  git clone https://github.com/pytest-dev/pytest.git ~/pytest
  git clone https://github.com/sphinx-doc/sphinx.git ~/sphinx
  git clone https://github.com/psf/requests.git ~/requests
  git clone https://github.com/pylint-dev/pylint.git ~/pylint
  git clone https://github.com/pydata/xarray.git ~/xarray
  git clone https://github.com/mwaskom/seaborn.git ~/seaborn
  git clone https://github.com/pallets/flask.git ~/flask
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ASTROPY_DIR = Path.home() / "astropy"
DJANGO_DIR = Path.home() / "django"
SYMPY_DIR = Path.home() / "sympy"
SKLEARN_DIR = Path.home() / "scikit-learn"
MATPLOTLIB_DIR = Path.home() / "matplotlib"
PYTEST_DIR = Path.home() / "pytest"
SPHINX_DIR = Path.home() / "sphinx"
REQUESTS_DIR = Path.home() / "requests"
PYLINT_DIR = Path.home() / "pylint"
XARRAY_DIR = Path.home() / "xarray"
SEABORN_DIR = Path.home() / "seaborn"
FLASK_DIR = Path.home() / "flask"

REPO_DIRS = {
    "astropy": ASTROPY_DIR,
    "django": DJANGO_DIR,
    "sympy": SYMPY_DIR,
    "scikit-learn": SKLEARN_DIR,
    "matplotlib": MATPLOTLIB_DIR,
    "pytest": PYTEST_DIR,
    "sphinx": SPHINX_DIR,
    "requests": REQUESTS_DIR,
    "pylint": PYLINT_DIR,
    "xarray": XARRAY_DIR,
    "seaborn": SEABORN_DIR,
    "flask": FLASK_DIR,
}

MODEL = "opencode/deepseek-v4-flash-free"
MODEL_NAME = "opencode-deepseek-v4-flash-free"


def get_repo_dir(repo_full_name):
    """Map a SWE-bench 'repo' field (e.g. 'django/django') to local clone path."""
    for key, path in REPO_DIRS.items():
        if key in repo_full_name:
            return path
    return None


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
    # Write prompt to a temp file to avoid shell-escaping issues
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=30, help="number of tasks to run")
    parser.add_argument("--runs", type=int, default=1, help="repetitions per task")
    parser.add_argument("--repos", type=str, default="astropy,django,sympy,scikit-learn",
                         help="comma-separated list of repo keywords to include")
    parser.add_argument("--per_repo", type=int, default=None,
                         help="max tasks to take from each repo (overrides even split if set)")
    parser.add_argument("--output", type=str, default="predictions_batch.jsonl")
    parser.add_argument("--start", type=int, default=0, help="start index within each repo's task list")
    args = parser.parse_args()

    print("Loading SWE-bench Lite dataset...")
    from datasets import load_dataset
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")

    repo_keywords = [r.strip() for r in args.repos.split(",")]

    # Group dataset tasks by repo keyword
    tasks = []
    for repo_kw in repo_keywords:
        repo_tasks = [t for t in dataset if repo_kw in t["repo"]]
        repo_dir = get_repo_dir(repo_kw)
        if repo_dir is None or not repo_dir.exists():
            print(f"  WARNING: no local clone found for '{repo_kw}' (expected at {repo_dir}) -- skipping")
            continue
        limit = args.per_repo if args.per_repo is not None else max(1, args.n // len(repo_keywords))
        selected = repo_tasks[args.start: args.start + limit]
        print(f"  {repo_kw}: {len(repo_tasks)} available in dataset, selected {len(selected)}")
        for t in selected:
            tasks.append((t, repo_dir))

    print(f"\nTotal tasks selected across all repos: {len(tasks)}")

    results_log = []
    predictions = []

    # Open output files immediately for incremental writing
    output_path = args.output
    log_path = output_path.replace(".jsonl", "_runlog.json")

    # Load existing progress if resuming (skip already-completed runs)
    completed_keys = set()
    if Path(output_path).exists():
        with open(output_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    key = (entry["instance_id"], entry["model_name_or_path"])
                    completed_keys.add(key)
                    predictions.append(entry)
                except:
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
            }
            predictions.append(entry)

            # INCREMENTAL SAVE after every single run
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

            # Save run log incrementally too
            with open(log_path, "w") as f:
                json.dump(results_log, f, indent=2)

            # Reset for next run/task
            reset_repo(repo_dir)


if __name__ == "__main__":
    main()
