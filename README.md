# Git and GitHub, from the inside

A guided terminal exercise for MLOps Engineering, agenda item 0, Git and GitHub. Look inside commits, combine branches five ways, resolve a conflict, recover lost work and fix a bug in a second worktree

Everything runs locally. No GitHub account, network or credentials are needed: a bare repository in `sandbox/origin.git` plays the role of GitHub

## Start here

Install VS Code, Git 2.28 or newer, and Python 3.10 or newer (the `base` environment of Miniconda is enough: the scripts use only the standard library)

1. Open this whole folder in VS Code
2. Check your tools in a terminal:

```text
git --version
python --version
```

3. Right-click a folder inside `101` in Explorer > **Open in Integrated Terminal**
4. Build its sandbox and step into it:

```text
python setup.py
cd sandbox/repo
```

5. Follow the instructor, one command at a time

## Use the folders

| Folder or file | Purpose |
| --- | --- |
| `101/gitdemo.py` | Shared helper: fixed author, clock and line endings, so commit ids match the slides |
| `101/<topic>/setup.py` | Deletes and rebuilds `sandbox/` for that topic |
| `101/<topic>/sandbox/` | Your throwaway repository; ignored by Git |
| `101/<topic>/*.py` (other) | Small edit helpers, the same edit you could type in VS Code |

## Five branch-combination examples

Open [101/02_branches_and_merges/cheatsheet_examples/STEPS.md](101/02_branches_and_merges/cheatsheet_examples/STEPS.md) for rebase, merge, squash merge, fast-forward and cherry-pick
Each case has its own small practice repository, matching the Git cheat sheet

## If stuck

Read the last line Git printed: it usually names the next command. Then:

- In the middle of a merge or rebase you do not understand: `git merge --abort` or `git rebase --abort`
- Lost a commit: `git reflog`, pin it with `git branch rescue "HEAD@{n}"`, check `git status` is clean, then `git reset --hard "HEAD@{n}"`
- Anything else: go back to the topic folder (`cd ../..`) and run `python setup.py` to start again

On Windows, use the VS Code terminal with PowerShell or Git Bash; every command in the guides works in both. Quote `"HEAD@{1}"` and `"HEAD^{tree}"` as shown, because PowerShell treats braces as code
