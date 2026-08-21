#!/usr/bin/env python3
"""
Automation script: runs OpenCode on a batch of SWE-bench Lite tasks.

For each task:
  1. Pull the official SWE-bench Docker image (swebench/sweb.eval.x86_64.{instance_id})
     which has the repo at base_commit with all dependencies pre-installed
  2. Run OpenCode inside the container with the bug report, network restricted to LLM API only
  3. Extract the resulting git diff from the container as the agent's patch
  4. Save patch + agent reasoning trace into a SWE-bench-compatible predictions.jsonl file
  5. Clean up the container and Docker image

After this script finishes, run Docker evaluation separately with:
  python -m swebench.harness.run_evaluation \
    --predictions_path predictions_batch.jsonl \
    --max_workers 4 \
    --run_id batch_run_1

Usage:
  # Full 300-task experiment (1 run each):
  python3 run_swebench_batch.py \
    --repos astropy,django,sympy,scikit-learn,matplotlib,pytest,sphinx,requests,pylint,xarray,seaborn,flask \
    --per_repo 120 --runs 1

  # Quick test — 1 task from astropy:
  python3 run_swebench_batch.py --repos astropy --per_repo 1 --runs 1

  # Multiple repos, explicit count per repo:
  python3 run_swebench_batch.py --repos astropy,django,sympy,scikit-learn --per_repo 6

  # With repetitions for variance testing:
  python3 run_swebench_batch.py --repos astropy --per_repo 6 --runs 5

  # With a different model:
  python3 run_swebench_batch.py --repos astropy --per_repo 1 --model opencode/gpt-4o

Docker images are pulled from Docker Hub and cached locally.
Images are removed after each task to save disk space.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from subprocess import Popen, PIPE
from tqdm import tqdm

# ── Supported repositories ───────────────────────────────────────────────────

VALID_REPOS = {
    "astropy", "django", "sympy", "scikit-learn", "matplotlib", "pytest",
    "sphinx", "requests", "pylint", "xarray", "seaborn", "flask",
}

DEFAULT_MODEL = "opencode/deepseek-v4-flash-free"

OPENCODE_BIN = OPENCODE_BIN = Path(__file__).resolve().parent / "bin" / "opencode-linux-x64"
OPENCODE_CONFIG = Path("opencode.json").resolve()
OPENCODE_AUTH = Path.home() / ".local" / "share" / "opencode" / "auth.json"

PROXY_IMAGE = "swebench-proxy"
PROXY_CONTAINER = "swebench-proxy"
PROXY_NETWORK = "swebench-net"
PROXY_LOG_VOLUME = "squid-logs"


# ── Helper functions ──────────────────────────────────────────────────────────

def get_repo_key(repo_full_name):
    """Map a SWE-bench 'repo' field (e.g. 'django/django') to a repo keyword."""
    for key in VALID_REPOS:
        if key in repo_full_name:
            return key
    return None


def check_docker_image_exists(image_name):
    """Check if a Docker image exists locally."""
    result = subprocess.run(
        ["docker", "image", "inspect", image_name],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def ensure_task_image(instance_id):
    """Pull the SWE-bench image for a specific task if not cached."""
    # Transform instance_id (e.g., "astropy__astropy-12907") to image name
    # Pattern: swebench/sweb.eval.x86_64.{repo}_1776_{issue}
    parts = instance_id.split("__")
    repo_name = parts[0]  # "astropy"
    issue_id = parts[1]   # "astropy-12907"
    image_name = f"swebench/sweb.eval.x86_64.{repo_name}_1776_{issue_id}"
    
    if check_docker_image_exists(image_name):
        print(f"  Using cached image: {image_name}")
        return True, image_name
    
    print(f"  Pulling image: {image_name}")
    result = subprocess.run(
        ["docker", "pull", image_name],
        capture_output=False,
        text=True,
    )
    
    if result.returncode != 0:
        print(f"  ERROR: Failed to pull image {image_name}")
        return False, image_name
    
    print(f"  Image pulled successfully")
    return True, image_name


def remove_task_image(image_name):
    """Remove the Docker image after task completion."""
    result = subprocess.run(
        ["docker", "rmi", image_name],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  Removed image: {image_name}")
    else:
        print(
            f"  WARNING: Failed to remove image {image_name}"
            + (f": {result.stderr.strip()}" if result.stderr.strip() else "")
        )


def check_docker_network_exists(network_name):
    """Check if a Docker network exists locally."""
    result = subprocess.run(
        ["docker", "network", "inspect", network_name],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def check_container_running(container_name):
    """Check if a Docker container is running."""
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={container_name}"],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def setup_proxy_network():
    """Create the internal Docker network for proxy isolation."""
    if check_docker_network_exists(PROXY_NETWORK):
        print("Proxy network already exists.")
        return True

    print(f"Creating proxy network {PROXY_NETWORK}...")
    result = subprocess.run(
        ["docker", "network", "create", "--internal", PROXY_NETWORK],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Failed to create network: {result.stderr}")
        return False

    print("Proxy network created.")
    return True


def start_proxy():
    """Start the whitelist proxy container."""
    if check_container_running(PROXY_CONTAINER):
        print("Proxy container already running.")
        return True

    if not check_docker_image_exists(PROXY_IMAGE):
        print("Building proxy image...")
        proxy_dir = Path("proxy")
        if not (proxy_dir / "Dockerfile.proxy").exists():
            print("ERROR: proxy/Dockerfile.proxy not found")
            return False
        if not (proxy_dir / "squid.conf").exists():
            print("ERROR: proxy/squid.conf not found")
            return False

        result = subprocess.run(
            ["docker", "build", "-f", "proxy/Dockerfile.proxy", "-t", PROXY_IMAGE, "proxy"],
            capture_output=False,
            text=True,
        )
        if result.returncode != 0:
            print("ERROR: Proxy image build failed")
            return False

    print("Starting proxy container...")
    result = subprocess.run(
        [
            "docker", "run", "-d",
            "--name", PROXY_CONTAINER,
            "-v", f"{PROXY_LOG_VOLUME}:/var/log/squid",
            PROXY_IMAGE,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Failed to start proxy: {result.stderr}")
        return False

    print("Connecting proxy to internal network...")
    result = subprocess.run(
        ["docker", "network", "connect", PROXY_NETWORK, PROXY_CONTAINER],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: Failed to connect proxy to network: {result.stderr}")
        return False

    print("Waiting for proxy to be ready...")
    time.sleep(1)
    for attempt in range(30):
        # Check if container is still running
        ps_result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"name={PROXY_CONTAINER}"],
            capture_output=True,
            text=True,
        )
        if not ps_result.stdout.strip():
            # Get container logs to see what went wrong
            logs_result = subprocess.run(
                ["docker", "logs", PROXY_CONTAINER],
                capture_output=True,
                text=True,
            )
            print(f"ERROR: Container stopped. Logs:\n{logs_result.stdout}\n{logs_result.stderr}")
            return False
        
        result = subprocess.run(
            ["docker", "exec", PROXY_CONTAINER, "sh", "-c", "netstat -tln 2>/dev/null | grep -q :3128 || exit 1"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("Proxy is ready.")
            return True
        time.sleep(0.5)

    print("ERROR: Proxy did not become ready in time")
    return False


def stop_proxy():
    """Stop and remove the proxy container and network."""
    if check_container_running(PROXY_CONTAINER):
        print("Stopping proxy container...")
        subprocess.run(["docker", "stop", PROXY_CONTAINER], capture_output=True, text=True)

    result = subprocess.run(
        ["docker", "rm", PROXY_CONTAINER],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("Proxy container removed.")

    if check_docker_network_exists(PROXY_NETWORK):
        print("Removing proxy network...")
        result = subprocess.run(
            ["docker", "network", "rm", PROXY_NETWORK],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("Proxy network removed.")

    result = subprocess.run(
        ["docker", "volume", "rm", PROXY_LOG_VOLUME],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("Squid logs volume removed.")


def collect_proxy_logs(task_dir, since_offset=0):
    """Collect proxy access logs for a task run."""
    result = subprocess.run(
        ["docker", "exec", PROXY_CONTAINER, "cat", "/var/log/squid/access.log"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return since_offset

    lines = result.stdout.splitlines()
    new_lines = lines[since_offset:]

    if new_lines:
        with open(task_dir / "proxy_access.log", "w") as f:
            f.write("\n".join(new_lines) + "\n")

    return len(lines)


def build_prompt(problem_statement):
    return (
        "You are a software engineer tasked with fixing a bug in the codebase.\n\n"
        "## Issue\n"
        f"{problem_statement}\n\n"
        "## Goal\n"
        "The codebase is located at /testbed. "
        "Fix the issue by editing the source files. "
        "Verify your fix works by running tests or a reproduction script.\n\n"
        "## Environment\n"
        "All dependencies are pre-installed. Do not attempt to install packages."
    )


def format_progress(event, elapsed_sec):
    """Format a single JSON event as a human-readable progress line."""
    event_type = event.get("type")
    part = event.get("part", {})

    if event_type == "reasoning":
        text = part.get("text", "")
        preview = text[:120].replace("\n", " ") if text else ""
        return f"  [{elapsed_sec:05.1f}s] 💭 reasoning: {preview}"

    elif event_type == "tool_use":
        tool = part.get("tool", "unknown")
        state = part.get("state", {})
        inp = state.get("input", {})
        status = state.get("status", "")

        if tool == "bash":
            cmd = inp.get("command", "")
            return f"  [{elapsed_sec:05.1f}s] 🔧 bash: {cmd[:80]}"
        elif tool == "read":
            path = inp.get("filePath", "")
            return f"  [{elapsed_sec:05.1f}s] 📖 read: {path}"
        elif tool == "edit":
            path = inp.get("filePath", "")
            return f"  [{elapsed_sec:05.1f}s] ✏️ edit: {path}"
        elif tool in ("grep", "glob", "search"):
            pattern = inp.get("pattern", inp.get("query", ""))
            return f"  [{elapsed_sec:05.1f}s] 🔍 {tool}: {pattern[:60]}"
        else:
            title = state.get("title", str(inp)[:60])
            return f"  [{elapsed_sec:05.1f}s] 🔧 {tool}: {title}"

    elif event_type == "text":
        text = part.get("text", "")
        preview = text[:120].replace("\n", " ") if text else ""
        return f"  [{elapsed_sec:05.1f}s] 💬 text: {preview}"

    return None


def parse_summary(events):
    """Parse JSON events into a structured summary."""
    session_id = None
    tool_calls = []
    reasoning = []
    text_messages = []
    total_tokens = {"input": 0, "output": 0, "reasoning": 0, "total": 0}

    for event in events:
        event_type = event.get("type")
        part = event.get("part", {})

        if event_type == "step_start" and not session_id:
            session_id = event.get("sessionID")

        elif event_type == "tool_use":
            tool = part.get("tool", "unknown")
            state = part.get("state", {})
            inp = state.get("input", {})
            output = state.get("output", "")
            status = state.get("status", "")
            metadata = state.get("metadata", {})
            time_info = part.get("time", state.get("time", {}))

            call = {
                "tool": tool,
                "input": inp,
                "output": output[:2000] if len(output) > 2000 else output,
                "status": status,
            }

            if tool == "bash":
                call["exit_code"] = metadata.get("exit")
            if time_info:
                start = time_info.get("start", 0)
                end = time_info.get("end", 0)
                if start and end:
                    call["duration_ms"] = end - start

            tool_calls.append(call)

        elif event_type == "reasoning":
            text = part.get("text", "")
            if text:
                reasoning.append(text)

        elif event_type == "text":
            text = part.get("text", "")
            if text:
                text_messages.append(text)

        elif event_type == "step_finish":
            tokens = part.get("tokens", {})
            if tokens:
                total_tokens["input"] += tokens.get("input", 0)
                total_tokens["output"] += tokens.get("output", 0)
                total_tokens["reasoning"] += tokens.get("reasoning", 0)
                total_tokens["total"] += tokens.get("total", 0)

    return {
        "session_id": session_id,
        "tool_calls": tool_calls,
        "reasoning": reasoning,
        "text_messages": text_messages,
        "tokens": total_tokens,
    }


def save_run_artifacts(task_dir, docker_output_dir, instance_id, run_num, events, patch, status, elapsed, summary, model_name, stderr=None):
    """Save all run artifacts to the task directory."""
    task_dir.mkdir(parents=True, exist_ok=True)

    trace_src = docker_output_dir / "trace.json"
    if trace_src.exists():
        shutil.copy(trace_src, task_dir / "trace.json")
    else:
        with open(task_dir / "trace.json", "w") as f:
            for event in events:
                f.write(json.dumps(event) + "\n")

    session_src = docker_output_dir / "session.json"
    if session_src.exists():
        shutil.copy(session_src, task_dir / "session.json")

    if stderr:
        with open(task_dir / "stderr.log", "w") as f:
            f.write(stderr)

    with open(task_dir / "patch.diff", "w") as f:
        f.write(patch)

    with open(task_dir / "summary.json", "w") as f:
        json.dump({
            "instance_id": instance_id,
            "run": run_num,
            "status": status,
            "elapsed_seconds": round(elapsed, 1),
            "patch_length": len(patch),
            **summary,
        }, f, indent=2)

    with open(task_dir / "predictions.jsonl", "w") as f:
        entry = {
            "instance_id": instance_id,
            "model_name_or_path": f"{model_name}-run{run_num}",
            "model_patch": patch,
        }
        f.write(json.dumps(entry) + "\n")


def run_opencode_docker(image_name, model, prompt, docker_output_dir, timeout=480):
    """Run OpenCode in a per-task SWE-bench Docker container with network isolation."""

    if not OPENCODE_BIN.exists():
        print(f"  ERROR: OpenCode binary not found at {OPENCODE_BIN}")
        return 1, [], f"OpenCode binary not found at {OPENCODE_BIN}", {}, None

    if not OPENCODE_CONFIG.exists():
        print(f"  ERROR: OpenCode config not found at {OPENCODE_CONFIG}")
        return 1, [], f"OpenCode config not found at {OPENCODE_CONFIG}", {}, None

    if not OPENCODE_AUTH.exists():
        print(f"  ERROR: OpenCode auth file not found at {OPENCODE_AUTH}")
        return 1, [], f"OpenCode auth file not found at {OPENCODE_AUTH}", {}, None

    docker_output_dir.mkdir(parents=True, exist_ok=True)
    trace_file = docker_output_dir / "trace.json"
    patch_file = docker_output_dir / "patch_from_container.diff"

    container_name = f"swebench-agent-{int(time.time())}"

    # Pass the prompt directly as an environment variable.
    # This avoids Docker Desktop bind-mount issues with individual files.
    prompt_env = prompt

    docker_cmd = [
        "docker", "run",
        "--name", container_name,
        "--network", PROXY_NETWORK,
        "--memory", "4g",
        "--cpus", "2",
        "-e", "HTTP_PROXY=http://swebench-proxy:3128",
        "-e", "HTTPS_PROXY=http://swebench-proxy:3128",
        "-e", "NO_PROXY=localhost,127.0.0.1",
        "-e", f"OPENCODE_PROMPT={prompt_env}",
        "-v", f"{OPENCODE_BIN}:/usr/local/bin/opencode:ro",
        "-v", f"{docker_output_dir.resolve()}:/output",
        "-v", f"{OPENCODE_CONFIG}:/mnt/config/opencode.jsonc:ro",
        "-v", f"{OPENCODE_AUTH}:/mnt/auth/auth.json:ro",
        image_name,
        "/bin/bash", "-c",
        "mkdir -p /tmp/opencode-config "
        "/tmp/opencode-home/.local/share/opencode && "
        "cp /mnt/config/opencode.jsonc "
        "/tmp/opencode-config/opencode.jsonc && "
        "cp /mnt/auth/auth.json "
        "/tmp/opencode-home/.local/share/opencode/auth.json && "
        "export OPENCODE_CONFIG_DIR=/tmp/opencode-config && "
        "export HOME=/tmp/opencode-home && "
        "cd /testbed && "
        "opencode run \"$OPENCODE_PROMPT\" "
        f"--model {model} "
        "--dangerously-skip-permissions "
        "--format json --thinking"
    ]

    events = []
    start_time = time.time()
    tool_call_count = 0
    returncode = None
    stderr = ""

    def extract_live_patch():
        """Extract git diff while the task container is still running."""
        try:
            diff_result = subprocess.run(
                [
                    "docker", "exec",
                    "-w", "/testbed",
                    container_name,
                    "git", "diff",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            patch_text = (
                diff_result.stdout
                if diff_result.returncode == 0
                else ""
            )
            patch_file.write_text(patch_text)
            print(
                f"  [DEBUG] Patch extracted: {len(patch_text)} chars"
            )
            return patch_text
        except Exception as exc:
            print(f"  [DEBUG] Could not extract patch: {exc}")
            patch_file.write_text("")
            return ""

    try:
        proc = Popen(
            docker_cmd,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,
        )

        print(f"  [DEBUG] Docker process started, PID={proc.pid}")
        print("  [DEBUG] Starting to read stdout...")

        # Use select so the timeout is effective even if OpenCode stops
        # producing output without exiting.
        import selectors

        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)

        with open(trace_file, "w") as trace_out:
            finished = False

            while True:
                remaining = timeout - (time.time() - start_time)
                if remaining <= 0:
                    print(
                        f"  [DEBUG] Timeout after {timeout}s. "
                        "Saving partial patch before killing Docker process..."
                    )
                    extract_live_patch()
                    proc.kill()
                    returncode = -1
                    stderr = "[TIMEOUT EXPIRED]"
                    break

                if proc.poll() is not None:
                    returncode = proc.returncode
                    break

                ready = selector.select(timeout=min(1.0, remaining))
                if not ready:
                    continue

                line = proc.stdout.readline()
                if not line:
                    if proc.poll() is not None:
                        returncode = proc.returncode
                        break
                    continue

                line = line.rstrip("\r\n")
                if not line:
                    continue

                trace_out.write(line + "\n")
                trace_out.flush()

                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                events.append(event)

                elapsed = time.time() - start_time
                progress = format_progress(event, elapsed)
                if progress:
                    print(progress)

                if event.get("type") == "tool_use":
                    tool_call_count += 1

                if (
                    event.get("type") == "step_finish"
                    and event.get("part", {}).get("reason") == "stop"
                ):
                    print("  [DEBUG] OpenCode reported reason=stop")
                    print("  [DEBUG] Agent finished. Extracting patch...")
                    extract_live_patch()

                    print("  [DEBUG] Stopping Docker container...")
                    subprocess.run(
                        ["docker", "stop", "-t", "2", container_name],
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                    finished = True
                    returncode = 0
                    break

        selector.close()

        if proc.poll() is None:
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print(
                    "  [DEBUG] Docker process did not exit after stop; "
                    "killing it."
                )
                proc.kill()
                proc.wait(timeout=10)

        if returncode is None:
            returncode = proc.returncode

        if proc.stderr:
            stderr_output = proc.stderr.read()
            if stderr_output:
                stderr = stderr_output

    except subprocess.TimeoutExpired:
        print("  [DEBUG] Timeout expired. Killing Docker process...")
        try:
            proc.kill()
            proc.wait(timeout=10)
        except Exception:
            pass
        returncode = -1
        stderr = "[TIMEOUT EXPIRED]"

    except Exception as exc:
        print(f"  [DEBUG] Unexpected error: {exc}")
        try:
            proc.kill()
            proc.wait(timeout=10)
        except Exception:
            pass
        returncode = 1
        stderr = str(exc)

    elapsed = time.time() - start_time
    summary = parse_summary(events)

    final_msg = (
        f"  [{elapsed:05.1f}s] ✓ done — "
        f"{tool_call_count} tool calls, "
        f"{summary['tokens']['total']} tokens"
    )
    print(final_msg)

    return returncode, events, stderr, summary, container_name

def extract_patch_from_container(container_name, docker_output_dir=None):
    """Read a patch saved while the container was still running, with a live fallback."""

    if docker_output_dir is not None:
        saved_patch = Path(docker_output_dir) / "patch_from_container.diff"
        if saved_patch.exists():
            patch_text = saved_patch.read_text()
            if patch_text.strip():
                return patch_text

    result = subprocess.run(
        [
            "docker", "exec",
            "-w", "/testbed",
            container_name,
            "git", "diff",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout if result.returncode == 0 else ""

def cleanup_container(container_name):
    """Remove the Docker container after extracting the patch."""
    result = subprocess.run(
        ["docker", "rm", "-f", container_name],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"  Removed container: {container_name}")
    else:
        print(f"  WARNING: Failed to remove container {container_name}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=30, help="number of tasks to run")
    parser.add_argument("--runs", type=int, default=1, help="repetitions per task")
    parser.add_argument("--repos", type=str, default="astropy,django,sympy,scikit-learn",
                        help="comma-separated list of repo keywords to include")
    parser.add_argument("--per_repo", type=int, default=None,
                        help="max tasks to take from each repo (overrides even split if set)")
    parser.add_argument("--start", type=int, default=0,
                        help="start index within each repo's task list (for resuming)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL,
                        help="OpenCode model to use (e.g. opencode/deepseek-v4-flash-free)")
    args = parser.parse_args()

    model = args.model
    model_name = model.replace("/", "-")

    print(f"Using model: {model}")

    print("Loading SWE-bench Lite dataset...")
    from datasets import load_dataset
    dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")

    repo_keywords = [r.strip() for r in args.repos.split(",")]

    # Group dataset tasks by repo keyword
    tasks = []
    for repo_kw in repo_keywords:
        repo_tasks = [t for t in dataset if repo_kw in t["repo"]]
        repo_key = get_repo_key(repo_kw)

        if repo_key is None:
            print(f"  WARNING: '{repo_kw}' not in known repo list — skipping")
            continue

        limit = args.per_repo if args.per_repo is not None else max(1, args.n // len(repo_keywords))
        selected = repo_tasks[args.start: args.start + limit]
        print(f"  {repo_kw}: {len(repo_tasks)} available in dataset, selected {len(selected)}")
        for t in selected:
            tasks.append((t, repo_key))

    print(f"\nTotal tasks selected across all repos: {len(tasks)}")

    print("\nSetting up proxy...")
    if not setup_proxy_network():
        print("ERROR: Failed to setup proxy network. Exiting.")
        sys.exit(1)
    if not start_proxy():
        print("ERROR: Failed to start proxy. Exiting.")
        stop_proxy()
        sys.exit(1)

    results_log = []
    predictions = []
    proxy_log_offset = 0

    output_dir = Path("outputs")
    log_path = output_dir / "runlog.json"
    predictions_path = output_dir / "predictions_all.jsonl"
    output_dir.mkdir(exist_ok=True)

    completed_keys = set()
    if predictions_path.exists():
        with open(predictions_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    key = (entry["instance_id"], entry["model_name_or_path"])
                    if entry.get("model_patch", "").strip():
                        completed_keys.add(key)
                    predictions.append(entry)
                except Exception:
                    pass
        print(f"Resuming: found {len(completed_keys)} already-completed runs in {predictions_path}")

    # Calculate total runs for progress bar
    total_runs = len(tasks) * args.runs
    
    try:
        with tqdm(total=total_runs, desc="Starting", unit="run", dynamic_ncols=True) as pbar:
            for i, (task, repo_key) in enumerate(tasks):
                instance_id = task["instance_id"]
                commit = task["base_commit"]
                problem = task["problem_statement"]
                repo_name = repo_key

                image_ok, image_name = ensure_task_image(instance_id)
                if not image_ok:
                    print(f"\nFAILED to get image for {instance_id}, skipping")
                    results_log.append({"instance_id": instance_id, "status": "image_pull_failed"})
                    with open(log_path, "w") as f:
                        json.dump(results_log, f, indent=2)
                    # Update progress bar for skipped runs
                    for _ in range(args.runs):
                        pbar.update(1)
                    continue

                for run_num in range(1, args.runs + 1):
                    run_model_name = f"{model_name}-run{run_num}"

                    # Update progress bar description
                    pbar.set_description(f"[{i+1}/{len(tasks)}] {instance_id} (run {run_num}/{args.runs})")

                    if (instance_id, run_model_name) in completed_keys:
                        pbar.update(1)
                        continue

                    t0 = time.time()

                    prompt = build_prompt(problem)
                    task_dir = output_dir / instance_id / f"run{run_num}"
                    docker_output_dir = task_dir / "_docker_output"
                    docker_output_dir.mkdir(parents=True, exist_ok=True)
                    
                    code, events, stderr, summary, container_name = run_opencode_docker(image_name, model, prompt, docker_output_dir)
                    
                    if stderr:
                        print(f"\nSTDERR: {stderr}")

                    trace_file = docker_output_dir / "trace.json"

                    if not trace_file.exists() or trace_file.stat().st_size == 0:
                        print("\nERROR: No output from opencode (trace.json missing or empty)")

                    patch = extract_patch_from_container(
                        container_name,
                        docker_output_dir,
                    )

                    if not patch.strip():
                        print("\nWARNING: Patch is empty after extraction.")
                    else:
                        print(f"\n[DEBUG] Final patch size: {len(patch)} chars")

                    cleanup_container(container_name)
                    elapsed = time.time() - t0

                    status = "ok" if patch.strip() else "empty_patch"
                    if code == -1:
                        status = "timeout"
                    elif code != 0 or stderr:
                        status = "opencode_error"
                        print(f"\nOpenCode failed with code {code}")

                    save_run_artifacts(task_dir, docker_output_dir, instance_id, run_num, events, patch, status, elapsed, summary, model_name, stderr)

                    proxy_log_offset = collect_proxy_logs(task_dir, proxy_log_offset)

                    entry = {
                        "instance_id": instance_id,
                        "model_name_or_path": run_model_name,
                        "model_patch": patch,
                    }
                    predictions.append(entry)

                    with open(predictions_path, "a") as f:
                        f.write(json.dumps(entry) + "\n")

                    results_log.append({
                        "instance_id": instance_id,
                        "repo": repo_name,
                        "run": run_num,
                        "status": status,
                        "elapsed_seconds": round(elapsed, 1),
                        "patch_length": len(patch),
                        "tool_calls": len(summary.get("tool_calls", [])),
                        "tokens_used": summary.get("tokens", {}).get("total", 0),
                        "session_id": summary.get("session_id", ""),
                        "output_dir": str(task_dir),
                    })

                    with open(log_path, "w") as f:
                        json.dump(results_log, f, indent=2)

                    pbar.update(1)

                remove_task_image(image_name)
    finally:
        print("\nCleaning up proxy...")
        stop_proxy()


if __name__ == "__main__":
    main()
