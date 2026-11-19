# Learn Git by changing a small project

Tiny sandboxes for agenda item 0, Git and GitHub. Each folder builds its own throwaway repository in `sandbox/`, so you can break things and start again in one command

Every folder uses the same example: `churn.py` predicts churn below **10.0 hours** of weekly usage. The setup fixes the author and the clock, so the commit ids of the setup match the slides on every laptop; ids you create during the demo contain your own clock and will differ

| Run before | Folder | The example grows from |
| --- | --- | --- |
| Save a change | `01_inside_a_commit` | Change a prediction, review the edit, select it and save a commit; inspect Git's internal records optionally |
| Combine separate work | `02_branches_and_merges` | Switch branches and see different files, then combine two improvements; compare rebase optionally |
| Resolve a disagreement | `03_conflicts_and_recovery` | Decide between incompatible edits and test the result; practise recovery and undo optionally |
| Use a second working folder | `04_worktrees_and_hygiene` | Fix an urgent typo while leaving unfinished work in its original folder; practise file cleanup optionally |

Each folder has a `setup.py` to build the example and a `STEPS.md` explaining what to run, what to look for and why it matters. Follow the four guides in the order above, one command at a time

The setup scripts prepare saved history for you; they do not install Python packages. Re-running any of these four scripts deletes and rebuilds that topic's sandbox, including your practice work

Use PowerShell in VS Code. Press **q** if Git opens a text viewer. Optional comparisons in `02_branches_and_merges/cheatsheet_examples` and `fetch_variants` can wait until the four main guides make sense
