# Setup for 02: a shared remote and three branches waiting to join main
#   feature/docs       one commit ahead of main, main has not moved: fast-forward
#   feature/threshold  one commit from the same start: once docs is merged, main has
#                      moved on, so it needs a three-way merge or a rebase
# Run it again at any time to start this demo from zero
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gitdemo import churn_rule, commit, fresh_sandbox, git, new_repo, write  # noqa: E402

sandbox = fresh_sandbox(HERE)
origin = sandbox / "origin.git"  # plays the role of GitHub: a bare repository, no working files
git("init", "-q", "--bare", "-b", "main", str(origin), cwd=sandbox)

repo = new_repo(sandbox / "repo")
write(repo, "README.md", "# Churn rule\n")
write(repo, "churn.py", churn_rule(10.0))
commit(repo, "Add churn rule", "README.md", "churn.py")
git("remote", "add", "origin", str(origin), cwd=repo)
git("push", "-q", "-u", "origin", "main", cwd=repo)

git("switch", "-q", "-c", "feature/docs", cwd=repo)
write(repo, "README.md", "# Churn rule\n\nPredict churn from weekly usage hours\n")
commit(repo, "Explain the rule in README", "README.md")

git("switch", "-q", "-c", "feature/threshold", "main", cwd=repo)
write(repo, "churn.py", churn_rule(10.0) + "\n\ndef is_valid(hours):\n    return hours >= 0\n")
commit(repo, "Reject negative hours", "churn.py")

git("switch", "-q", "main", cwd=repo)
print("ready: sandbox/repo on main, remote sandbox/origin.git")
print("next: cd sandbox/repo")
