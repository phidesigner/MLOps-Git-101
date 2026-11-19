# gitdemo.py: shared helper that builds the classroom sandboxes
# Every setup.py in 101 imports it. It writes files with LF endings, fixes the
# author, email and clock, and turns off line-ending conversion, so every laptop
# gets the same commit ids as the slides
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

AUTHOR = "Demo Student"
EMAIL = "student@example.com"
START = 1794816000  # 2026-11-16 09:00:00 UTC, the fixed clock for every commit
_tick = 0


def _env():
    """Fixed author and dates, so commit ids never depend on who runs the demo or when."""
    stamp = f"{START + _tick * 60} +0100"
    env = dict(os.environ)
    env.update(
        GIT_AUTHOR_NAME=AUTHOR,
        GIT_AUTHOR_EMAIL=EMAIL,
        GIT_COMMITTER_NAME=AUTHOR,
        GIT_COMMITTER_EMAIL=EMAIL,
        GIT_AUTHOR_DATE=stamp,
        GIT_COMMITTER_DATE=stamp,
    )
    return env


def git(*args, cwd):
    """Run one Git command and stop with its message if it fails."""
    result = subprocess.run(
        ["git", *args], cwd=cwd, env=_env(), capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout.strip()


def write(repo, name, text):
    """Write a file with LF endings on every operating system."""
    path = Path(repo) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def commit(repo, message, *files):
    """Stage the named files and commit them one clock minute after the last commit."""
    global _tick
    _tick += 1
    git("add", *files, cwd=repo)
    git("commit", "-q", "-m", message, cwd=repo)


def _make_writable(func, path, _):
    os.chmod(path, stat.S_IWRITE)  # Git marks its object files read-only on Windows
    func(path)


def fresh_sandbox(here):
    """Delete and recreate <folder>/sandbox, so a demo can always restart from zero."""
    sandbox = Path(here) / "sandbox"
    if sandbox.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(sandbox, onexc=_make_writable)
        else:
            shutil.rmtree(sandbox, onerror=_make_writable)
    sandbox.mkdir()
    return sandbox


def new_repo(path):
    """git init with main as the first branch and no line-ending conversion."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    git("init", "-q", "-b", "main", cwd=path)
    git("config", "user.name", AUTHOR, cwd=path)
    git("config", "user.email", EMAIL, cwd=path)
    git("config", "core.autocrlf", "false", cwd=path)
    git("config", "commit.gpgsign", "false", cwd=path)
    git("config", "pull.rebase", "false", cwd=path)
    return path


def churn_rule(threshold):
    """The one file every demo edits: below the threshold we predict churn."""
    return (
        "# churn.py: predict churn from weekly usage hours\n"
        f"THRESHOLD = {threshold}  # hours\n"
        "\n"
        "\n"
        "def predict(hours):\n"
        '    return "churn" if hours < THRESHOLD else "stay"\n'
    )
