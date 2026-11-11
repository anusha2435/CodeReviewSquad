import ast
import os
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from config import DOCKER_IMAGE, SANDBOX_TIMEOUT


def _docker_run(workdir, args, timeout):
    name = f"squad-{uuid.uuid4().hex[:8]}"
    cmd = [
        "docker", "run", "--rm", "--name", name,
        "--network", "none",                 # no internet
        "--memory", "256m", "--cpus", "0.5", "--pids-limit", "64",
        "--read-only", "--tmpfs", "/tmp",    # read-only filesystem
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "-e", "PYTHONDONTWRITEBYTECODE=1",
        "--mount", f"type=bind,source={workdir},target=/work,readonly",
        "-w", "/work",
        DOCKER_IMAGE, "python", *args,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           stdin=subprocess.DEVNULL, timeout=timeout + 5)
        return {"ok": p.returncode == 0, "output": (p.stdout + p.stderr)[-3000:]}
    except subprocess.TimeoutExpired:
        # stopping the docker client does NOT stop the container, so kill it
        subprocess.run(["docker", "kill", name], capture_output=True)
        return {"ok": False, "output": f"TIMEOUT after {timeout}s (container killed)"}
    except FileNotFoundError:
        return {"ok": False, "output": "Docker not found. Install Docker Desktop."}


def _sandbox(files: dict, args: list, timeout: int) -> dict:
    """Write files to a temp folder and run `python <args>` inside the container."""
    with tempfile.TemporaryDirectory() as d:
        os.chmod(d, 0o755)      # container user must be able to read it
        for name, text in files.items():
            Path(d, name).write_text(text, encoding="utf-8")
        return _docker_run(d, args, timeout)




def sandbox_status() -> str:
    try:
        r = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except FileNotFoundError:
        return "docker (not installed)"
    except subprocess.TimeoutExpired:
        return "docker (not responding)"

    if r.returncode != 0:
        return "docker (not running, start Docker Desktop)"

    image = subprocess.run(
        ["docker", "image", "inspect", DOCKER_IMAGE],
        capture_output=True,
        text=True,
        timeout=5
    )

    if image.returncode == 0:
        return "docker (ready)"

    return "docker (image missing)"




def static_report(code: str) -> str:
    """Syntax check + flake8. Does not execute the code."""
    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"SyntaxError at line {e.lineno}: {e.msg}"
    with tempfile.TemporaryDirectory() as d:
        Path(d, "snippet.py").write_text(code, encoding="utf-8")
        p = subprocess.run(
            [sys.executable, "-m", "flake8", "--max-line-length=100", "snippet.py"],
            cwd=d, capture_output=True, text=True, timeout=30)
    return (p.stdout + p.stderr).strip() or "No flake8 issues."


def run_code(code: str) -> dict:
    """Run the snippet as-is in Docker to catch runtime errors."""
    return _sandbox({"main.py": code}, ["-I", "main.py"], SANDBOX_TIMEOUT)


def run_tests(solution: str, tests: str) -> dict:
    """Run pytest in Docker. Tests must start with `from solution import *`."""
    return _sandbox(
        {"solution.py": solution, "test_solution.py": tests},
        ["-m", "pytest", "-q", "-x", "--disable-warnings",
         "-p", "no:cacheprovider", "test_solution.py"],
        SANDBOX_TIMEOUT,
    )