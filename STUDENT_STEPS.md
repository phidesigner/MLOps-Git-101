# Git hands-on: one story, step by step

**The story:** a small team owns one business rule: *customers who use the app less than 10 hours a week may leave (churn)*. You will save versions, share work with a teammate, combine ideas, settle a disagreement, undo mistakes and fix an urgent typo

**How to use this file:** copy and paste one block at a time into the VS Code terminal (PowerShell), then compare your screen with the **Check** line. Slide numbers point to the matching slides. Your commit ids will differ from the slides; that is normal

| Part | Slides | The one idea |
| --- | --- | --- |
| 0 Get ready | 59 | Git is the tool on your laptop; GitHub hosts shared copies |
| 1 Save versions | 62 to 65 | Edit, select, save: three areas and what a commit really is |
| 2 Share work | 66 to 67 | Push sends, fetch looks, pull brings in |
| 3 Combine work | 68 to 69 | Five ways to bring changes together |
| 4 Conflict | 70, 73 | When two people change the same line, a person decides |
| 5 Ask the history | 71 | Precise questions get instant answers |
| 6 Undo | 72 | Local mistakes: rewind. Shared mistakes: add a correction |
| 7 Urgent fix | 74, 76 | A second folder for an urgent task, unfinished work untouched |
| 8 Hygiene | 75 | Ignore secrets, delete what is done, look before deleting |

**Before you start:** install VS Code, Git 2.28 or newer and Python. Open a terminal in VS Code with **Ctrl + `** (PowerShell). Nothing else is needed: every file is created by the commands below. To start again, see the last table

---

## Part 0. Get ready (slide 59)

```powershell
git --version
cd ~
mkdir git-demo
cd git-demo
git init -b main
$env:GIT_PAGER = "cat"
ls -Force
```

**Check:** "Initialized empty Git repository" and the hidden **.git** folder: that is the memory

The `GIT_PAGER` line makes Git print results straight into the terminal instead of a scrolling viewer

---

## Part 1. Save versions (slides 62 to 65)

### 1.1 The first save

Two files: the rule and a README. The README title has a typo (Chrun); leave it, you will fix it as an urgent task in Part 7

```powershell
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 10", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
Set-Content README.md "# Chrun predictor", "Predicts which customers may leave"
code .
git status
```

**Check:** both files in red, "Untracked": Git sees them but is not saving them yet. In VS Code, the Source Control icon shows 2 changes

```powershell
git add churn.py README.md
git status
git commit -m "Add churn rule at 10 hours"
```

### 1.2 A change with business impact

A customer uses the app 11 hours a week. Watch what one number does to the prediction

```powershell
python -B -c "import churn; print(churn.predict(11))"
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 12", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
python -B -c "import churn; print(churn.predict(11))"
```

**Check:** **stay** becomes **churn**. One number changed a business decision. That is why every change should be recorded

```powershell
git status -s
git diff
```

**Check:** ` M churn.py`: the **M** in the right column means edited, not yet selected. The diff shows red `-THRESHOLD = 10` and green `+THRESHOLD = 12`

```powershell
git add churn.py
git status -s
git diff --staged
git commit -m "Raise churn threshold to 12 hours"
git log --oneline
```

**Check:** `M  churn.py` moved to the left column: selected. `diff --staged` previews exactly what the commit will save. The log lists both saves, newest first

### 1.3 Walk backwards through the three areas (slide 63)

Break the file on purpose, select the broken version, then undo step by step

```powershell
Set-Content churn.py "oops"
git add churn.py
git status -s
git restore --staged churn.py
git status -s
git restore churn.py
git status -s
```

**Check:** left **M** (selected) → right **M** (unselected but still broken) → nothing: the file is back. Watch the editor

```powershell
git reset --soft HEAD~1
git status -s
git log --oneline
git commit -m "Raise churn threshold to 12 hours"
```

**Check:** the 12-hour commit disappears from the log, `M  churn.py` is still selected, and you save it again

### 1.4 What a commit really is (slides 62, 65)

```powershell
git cat-file -p HEAD
git cat-file -p "HEAD^{tree}"
cat .git/HEAD
cat .git/refs/heads/main
```

**Check:**
- **tree**: the folder snapshot; **parent**: the previous commit; then author and message
- the tree lists each file (a **blob**, the stored content) with its id
- **HEAD** says "you are on main"; **main** is just a file holding the id of the latest commit

---

## Part 2. Share work (slides 66 to 67)

### 2.1 Put the project on "GitHub"

To work offline, the folder `pretend-github.git` plays GitHub and a second folder, `teammate`, plays a colleague's laptop. The commands are the same as with the real GitHub

```powershell
cd ~
git init --bare -b main pretend-github.git
cd git-demo
git remote add origin ../pretend-github.git
git push -u origin main
git branch -vv
```

**Check:** `[origin/main]`: your main is now linked to the shared copy, called **origin**

### 2.2 Your teammate joins

```powershell
cd ~
git clone pretend-github.git teammate
cd teammate
Set-Content README.md "# Chrun predictor", "Predicts which customers may leave", "Owner: data team"
git commit -am "Add owner to README"
git push
```

### 2.3 Look before you bring it in

```powershell
cd ~/git-demo
git fetch
git branch -vv
git diff main origin/main
```

**Check:** `[origin/main: behind 1]` and the teammate's green line. Your README in the editor has **not** changed

```powershell
git pull --ff-only
```

**Check:** the Owner line appears in the editor

### 2.4 Publish a branch and name a version

```powershell
git switch -c feature/docs
Set-Content CHANGELOG.md "- Threshold raised to 12 hours"
git add CHANGELOG.md
git commit -m "Add changelog"
git push -u origin feature/docs
git tag v1.0 main
git push origin --tags
git branch -a
```

**Check:** your local branches plus `remotes/origin/...`: what the shared copy has

### 2.5 Tidy names of deleted branches

After review, your teammate deletes your branch on the shared copy. Your laptop remembers its name until you prune

```powershell
cd ~/teammate
git push origin --delete feature/docs
cd ~/git-demo
git branch -r
git fetch --prune
git branch -r
```

**Check:** `origin/feature/docs` disappears. Your local `feature/docs` stays: prune only cleans the remote names

---

## Part 3. Combine work: five ways (slides 68 to 69)

### 3.1 Fast-forward: main simply moves ahead

```powershell
git switch main
git merge feature/docs
git log --oneline --graph -3
```

**Check:** "Fast-forward": nobody else changed main, so main just moves to the newer commit. No extra commit

### 3.2 Merge: both sides changed

```powershell
git switch -c feature/validation
Set-Content validate.py "# Reject impossible usage values", "def valid(hours): return hours >= 0"
git add validate.py
git commit -m "Add input check"
git switch main
Set-Content CHANGELOG.md "- Threshold raised to 12 hours", "- Input check planned"
git commit -am "Update changelog"
git merge --no-edit feature/validation
git log --oneline --graph -4
```

**Check:** the graph splits and joins, with one extra commit that ties both lines together

### 3.3 Rebase: replay your work on top of the latest

```powershell
git switch -c feature/report
Set-Content report.md "Weekly churn report: draft"
git add report.md
git commit -m "Draft weekly report"
git switch main
Set-Content team.md "Team: data science and marketing"
git add team.md
git commit -m "List the team"
git switch feature/report
git log --oneline -1
git rebase main
git log --oneline --graph -3
git switch main
git merge feature/report
```

**Check:** the report commit gets a **new id** and now sits after "List the team" in one straight line; main then fast-forwards

### 3.4 Squash merge: many small saves become one

```powershell
git switch -c feature/tidy
Set-Content report.md "Weekly churn report: v1"
git commit -am "wip"
Set-Content report.md "Weekly churn report: v1 with charts"
git commit -am "wip again"
Set-Content report.md "Weekly churn report: final"
git commit -am "fix typo"
git switch main
git merge --squash feature/tidy
git commit -m "Finish weekly report"
git log --oneline -3
```

**Check:** three messy commits arrive on main as **one** clear commit

### 3.5 Cherry-pick: take only the fix

```powershell
git switch -c experiment
Set-Content model_v2.py "# Unfinished new model: do not ship"
git add model_v2.py
git commit -m "Start new model (unfinished)"
Set-Content validate.py "# Reject impossible usage values", "def valid(hours): return 0 <= hours <= 168"
git commit -am "Fix: a week has at most 168 hours"
git switch main
git cherry-pick experiment
ls
```

**Check:** the 168-hour fix is on main, but **model_v2.py is not**

---

## Part 4. The conflict (slides 70, 73)

Two colleagues disagree: one branch lowers the threshold to 8 while main raises it to 15. Git cannot choose a business rule, so it will stop and ask you

```powershell
git switch -c feature/threshold
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 8", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
git commit -am "Lower threshold to 8 hours"
git switch main
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 15", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
git commit -am "Raise threshold to 15 hours"
git merge feature/threshold
git status -s
```

**Check:** `CONFLICT (content): Merge conflict in churn.py` and `UU churn.py` (unmerged). Open churn.py in VS Code:

```text
<<<<<<< HEAD
THRESHOLD = 15            <- main: what is already here
=======
THRESHOLD = 8             <- feature/threshold: what is coming in
>>>>>>> feature/threshold
```

```powershell
git merge --abort
git status -s
git merge feature/threshold
```

The team agrees on **10**. Resolve in VS Code (write `THRESHOLD = 10`, delete the three marker lines, **Ctrl + S**) or paste:

```powershell
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 10", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
python -B -c "import churn; print(churn.predict(8), churn.predict(11))"
git add churn.py
git commit -m "Agree on 10 hours after review"
git log --oneline --graph -5
git push
```

**Check:** `churn stay`: 8 h triggers an alert and 11 h does not, so the agreed rule works before you save it. Then the graph joins the two opinions into one decision

---

## Part 5. Ask the history (slide 71)

```powershell
git log --oneline --graph --all
git show v1.0
git diff v1.0 main -- churn.py
git blame churn.py
git log -S "THRESHOLD = 8" --oneline
git reflog -8
```

**What each command answers:**
- `log --graph --all`: the whole story, every branch
- `show`: what one version changed, who and when
- `diff`: how two versions differ, here v1.0 against today
- `blame`: which commit last changed each line (who to ask, not who to blame)
- `log -S`: when the value 8 appeared and disappeared
- `reflog`: your laptop's private diary of everywhere you have been

---

## Part 6. Undo (slide 72)

Gentle to drastic: amend and reset only for work nobody else has; revert for work you already shared

### 6.1 Fix the last message

```powershell
Set-Content CHANGELOG.md "- Threshold raised to 12 hours", "- Input check planned", "- Threshold agreed at 10 hours"
git commit -am "chnagelog"
git commit --amend -m "Record the agreed threshold in the changelog"
git log --oneline -2
```

### 6.2 Rewind hard, then rescue

```powershell
git reset --hard HEAD~1
git log --oneline -2
git reflog -3
git branch rescue "HEAD@{1}"
git reset --hard rescue
git log --oneline -2
git branch -d rescue
```

**Check:** the changelog commit vanishes from the log, `reflog` still lists it as `HEAD@{1}`; you name it **rescue** and jump back

### 6.3 A shared mistake: add a correction

You push a wrong threshold (100 h). The team already has it, so you add a correction instead of erasing history

```powershell
git push
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 100", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'"
git commit -am "Raise threshold to 100 hours"
git push
git revert HEAD --no-edit
git push
git log --oneline -3
```

**Check:** churn.py is back to **10**; the log shows the mistake **and** `Revert "Raise threshold to 100 hours"`

---

## Part 7. Urgent fix in a second folder (slides 74, 76)

You are in the middle of new work when the README typo becomes urgent. Fix it in a second folder so the two tasks never mix

```powershell
Set-Content churn.py "# Churn rule: customers using the app less than THRESHOLD hours a week may leave", "THRESHOLD = 10", "def predict(hours): return 'churn' if hours < THRESHOLD else 'stay'", "# TODO: try one threshold per country"
Set-Content notes_tmp.txt "Ideas for next week"
git status -s
```

**Check:** unfinished edit in churn.py and a scratch file

```powershell
git worktree add ../hotfix -b hotfix/readme-typo main
git worktree list
cd ../hotfix
git status -s
Set-Content README.md "# Churn predictor", "Predicts which customers may leave", "Owner: data team"
git commit -am "Fix typo in README title"
cd ../git-demo
git merge --ff-only hotfix/readme-typo
git worktree remove ../hotfix
git branch -d hotfix/readme-typo
git status -s
git push
```

**Check:** the hotfix folder is clean, the fix lands on main, and back in git-demo your unfinished churn.py and notes are exactly where you left them

---

## Part 8. Hygiene (slide 75)

### 8.1 Never commit secrets

```powershell
Set-Content .env "API_KEY=do-not-share"
git status -s
Set-Content .gitignore ".env", "__pycache__/"
git status -s
git add .gitignore
git commit -m "Ignore local secrets and caches"
```

**Check:** `.env` disappears from the list once it is in `.gitignore`

### 8.2 Small, focused commits

```powershell
git commit -am "Note idea: one threshold per country"
```

### 8.3 Look before deleting

```powershell
git clean -n
git clean -f
```

**Check:** `-n` only previews ("Would remove notes_tmp.txt"); `-f` actually deletes

### 8.4 Delete branches that are done

```powershell
git branch
git branch -d feature/docs feature/validation feature/report feature/threshold
git branch -d feature/tidy experiment
git branch -D feature/tidy experiment
git branch
```

**Check:** `-d` refuses for feature/tidy and experiment ("not fully merged"): Git protects work that is not on main yet. `-D` forces it, because you decided you do not need them

### Finale

```powershell
git push
git log --oneline --graph --all
git status
```

**Check:** "Your branch is up to date with 'origin/main'" and "working tree clean"

---

## The ideas to remember

- **Memory:** edit, select, save; every commit is a snapshot with a note
- **Teamwork:** push sends, fetch looks, pull brings in
- **Combining:** fast-forward, merge, rebase, squash, cherry-pick, each for a situation
- **Decisions:** a conflict means people decide, then test
- **Safety:** restore and reset for local work, revert for shared work, reflog to rescue
- **Hygiene:** no secrets, one task per branch and folder, delete what is done

---

## If something goes wrong

| You see | Do this |
| --- | --- |
| `(END)` at the bottom of the terminal | Press **q**; run `$env:GIT_PAGER = "cat"` again (it lasts until the terminal closes) |
| "Please tell me who you are" | `git config --global user.name "Your Name"` and `git config --global user.email "you@ie.edu"` |
| "nothing to commit" | The file was not saved in VS Code (**Ctrl + S**) |
| An editor full of text opens after a Git command | Type `:wq` and press **Enter** (that editor is Vim) |
| "Your local changes would be overwritten" | `git status -s` to see what is unsaved, then commit it or `git restore` it |
| Lost in the middle of a merge or rebase | `git merge --abort` or `git rebase --abort` |
| Start again from scratch | `cd ~` then `Remove-Item -Recurse -Force git-demo, pretend-github.git, teammate, hotfix -ErrorAction SilentlyContinue`, then Part 0 |
