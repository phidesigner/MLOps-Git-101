# Setup for 03: two branches change the same line, so merging them conflicts
#   main               THRESHOLD = 12.0 (marketing wants more churn alerts)
#   feature/threshold  THRESHOLD = 8.0  (data science found fewer false alarms)
# Run it again at any time to start this demo from zero
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gitdemo import churn_rule, commit, fresh_sandbox, git, new_repo, write  # noqa: E402

repo = new_repo(fresh_sandbox(HERE) / "repo")
write(repo, "README.md", "# Churn rule\n")
write(repo, "churn.py", churn_rule(10.0))
commit(repo, "Add churn rule", "README.md", "churn.py")

git("switch", "-q", "-c", "feature/threshold", cwd=repo)
write(repo, "churn.py", churn_rule(8.0))
commit(repo, "Lower threshold to 8 h", "churn.py")

git("switch", "-q", "main", cwd=repo)
write(repo, "churn.py", churn_rule(12.0))
commit(repo, "Raise threshold to 12 h", "churn.py")
print("ready: sandbox/repo on main, feature/threshold changes the same line")
print("next: cd sandbox/repo")
