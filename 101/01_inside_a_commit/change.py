# change.py: edit the threshold in sandbox/repo/churn.py, as if you typed it in VS Code
# Usage, from sandbox/repo: python ../../change.py 12.0
import sys
from pathlib import Path

new_value = sys.argv[1] if len(sys.argv) > 1 else "12.0"
path = Path("churn.py")
text = path.read_text(encoding="utf-8")
lines = [f"THRESHOLD = {new_value}  # hours" if line.startswith("THRESHOLD") else line
         for line in text.splitlines()]
with open(path, "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(lines) + "\n")
print(f"churn.py: THRESHOLD = {new_value}")
