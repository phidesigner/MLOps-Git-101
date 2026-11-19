# resolve.py: the team agreed on 10.0 h; write the resolved churn.py without markers
# Usage, from sandbox/repo: python ../../resolve.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gitdemo import churn_rule, write  # noqa: E402

write(".", "churn.py", churn_rule(10.0))
print("churn.py: markers removed, THRESHOLD = 10.0")
