# 101: Git from the inside, one small repository at a time

Tiny sandboxes for agenda item 0, Git and GitHub. Each folder builds its own throwaway repository in `sandbox/`, so you can break things and start again in one command

Every folder uses the same example: `churn.py` predicts churn below **10.0 hours** of weekly usage. The setup fixes the author and the clock, so the commit ids of the setup match the slides on every laptop; ids you create during the demo contain your own clock and will differ

| Run before | Folder | The example grows from |
| --- | --- | --- |
| Demo: inside a commit | `01_inside_a_commit` | `git log` > the raw commit > tree and blob > `HEAD` and `main` > working directory, staging, history |
| Demo: three ways to join a branch | `02_branches_and_merges` | A remote and two branches > fast-forward > three-way merge > rebase |
| Demo: conflict, then recover | `03_conflicts_and_recovery` | Two edits to one line > resolve > `blame` and `log -S` > `reset` and `reflog` > `revert` |
| Demo: hotfix in a second worktree | `04_worktrees_and_hygiene` | Work in progress > `worktree add` > fix and merge > `worktree remove` > `clean` |

Each folder has a `setup.py` (build or rebuild the sandbox) and a `STEPS.md` (what to run, what to expect, what to say)
