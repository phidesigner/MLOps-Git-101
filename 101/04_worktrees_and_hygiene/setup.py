# Setup for 04: you are halfway through a feature when an urgent fix arrives
#   feature/model  checked out, with an unsaved edit in churn.py you do not want to commit yet
#   main           has a typo in README.md that must be fixed now
# Run it again at any time to start this demo from zero
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gitdemo import churn_rule, commit, fresh_sandbox, git, new_repo, write  # noqa: E402

repo = new_repo(fresh_sandbox(HERE) / "repo")
write(repo, ".gitignore", "__pycache__/\n*.log\n")
write(repo, "README.md", "# Churn rule\n\nPredict chrun from weekly usage hours\n")
write(repo, "churn.py", churn_rule(10.0))
commit(repo, "Add churn rule", ".gitignore", "README.md", "churn.py")

git("switch", "-q", "-c", "feature/model", cwd=repo)
write(repo, "churn.py", churn_rule(10.0) + "\n\n# TODO: replace the rule with a trained model\n")
write(repo, "debug.log", "scratch output\n")
write(repo, "notes_tmp.txt", "half-finished ideas\n")
print("ready: sandbox/repo on feature/model with work in progress")
print("next: cd sandbox/repo")
