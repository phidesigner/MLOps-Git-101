# Git and GitHub, from the inside

A guided exercise for learning Git through visible changes to a small Python project. Save a change, develop work on separate branches, resolve a disagreement and fix something urgent in a second folder

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

5. Open that folder's `STEPS.md`. Run one command at a time and read what its output means before continuing

Start with [Save a change](101/01_inside_a_commit/STEPS.md), then [Combine separate work](101/02_branches_and_merges/STEPS.md), [Resolve a disagreement](101/03_conflicts_and_recovery/STEPS.md) and [Use a second folder](101/04_worktrees_and_hygiene/STEPS.md)

Each guide explains the task, each command and the result you should look for. Sections marked **Optional** can wait until the basic workflow makes sense

Use PowerShell in VS Code. If Git opens a text viewer showing `(END)`, press **q** to return to the terminal

**The four main setup scripts delete and rebuild their own topic's `sandbox/` folder when run again**. The two optional example sets instead refuse to overwrite an existing folder

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

Run `git status` to see the current branch and whether Git is waiting for you to finish an operation

- To cancel an unfinished merge, run `git merge --abort`
- To cancel an unfinished rebase, run `git rebase --abort`
- For a lost saved commit, follow the recovery example in `101/03_conflicts_and_recovery/STEPS.md`
- To restart one of the four main exercises from `sandbox/repo`, run `cd ../..`, then `python setup.py`, then `cd sandbox/repo`; this discards that topic's practice work

On Windows, use the VS Code terminal with PowerShell or Git Bash; every command in the guides works in both. Quote `"HEAD@{1}"` and `"HEAD^{tree}"` as shown, because PowerShell treats braces as code
