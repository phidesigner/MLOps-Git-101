# fix_typo.py: correct "chrun" in README.md, as if you typed it in VS Code
# Usage, from sandbox/hotfix: python ../../fix_typo.py
from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8").replace("chrun", "churn")
with open(path, "w", encoding="utf-8", newline="\n") as handle:
    handle.write(text)
print("README.md: chrun -> churn")
