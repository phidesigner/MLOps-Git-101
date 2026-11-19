# Setup for 01: a repository with two commits and nothing else
# Run it again at any time to start this demo from zero
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from gitdemo import churn_rule, commit, fresh_sandbox, new_repo, write  # noqa: E402

repo = new_repo(fresh_sandbox(HERE) / "repo")
write(repo, "README.md", "# Churn rule\n\nPredict churn from weekly usage hours\n")
write(repo, "churn.py", churn_rule(10.0))
commit(repo, "Add churn rule", "README.md", "churn.py")
RUN_LINE = 'Run: python -c "import churn; print(churn.predict(8.0))"\n'
write(repo, "README.md", "# Churn rule\n\nPredict churn from weekly usage hours\n\n" + RUN_LINE)
commit(repo, "Document how to run", "README.md")
print("ready: sandbox/repo, 2 commits on main")
print("next: cd sandbox/repo")
