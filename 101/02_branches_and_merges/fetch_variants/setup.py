"""Build local practice remotes. Run once, then follow STEPS.md in sandbox/repo."""
import argparse
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, default=Path(__file__).resolve().parent / 'sandbox')
    args = parser.parse_args()
    root = args.sandbox.resolve()
    if root.exists():
        raise SystemExit('Sandbox already exists; use --sandbox with a new practice folder')
    root.mkdir(parents=True)
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
               GIT_AUTHOR_NAME='Demo Student', GIT_AUTHOR_EMAIL='student@example.com',
               GIT_COMMITTER_NAME='Demo Student', GIT_COMMITTER_EMAIL='student@example.com',
               GIT_AUTHOR_DATE='2026-11-16T09:00:00+01:00', GIT_COMMITTER_DATE='2026-11-16T09:00:00+01:00')

    def git(*cmd, cwd=root):
        return subprocess.run(['git', *cmd], cwd=cwd, env=env, check=True,
                              text=True, capture_output=True).stdout.strip()

    for name in ('origin.git', 'upstream.git'):
        git('init', '-q', '--bare', '-b', 'main', name)
    repo = root / 'repo'
    git('init', '-q', '-b', 'main', str(repo))
    git('config', 'core.autocrlf', 'false', cwd=repo)
    git('config', 'commit.gpgsign', 'false', cwd=repo)
    (repo / 'README.md').write_text('# Shared project\n', encoding='utf-8')
    git('add', 'README.md', cwd=repo)
    git('commit', '-q', '-m', 'Start project', cwd=repo)
    git('remote', 'add', 'origin', str(root / 'origin.git'), cwd=repo)
    git('push', '-q', '-u', 'origin', 'main', cwd=repo)
    # A private local branch lets pull --rebase replay work after the teammate's change
    git('switch', '-q', '-c', 'feature/demo', cwd=repo)
    (repo / 'notes.txt').write_text('A local experiment\n', encoding='utf-8')
    git('add', 'notes.txt', cwd=repo)
    git('commit', '-q', '-m', 'Add private note', cwd=repo)
    git('switch', '-q', 'main', cwd=repo)
    git('branch', 'feature/retired', cwd=repo)
    git('push', '-q', 'origin', 'feature/retired', cwd=repo)
    # A second repository advertises a branch not yet known by the learner's copy
    git('push', '-q', str(root / 'upstream.git'), 'main', 'main:refs/heads/reference', cwd=repo)
    git('remote', 'add', 'upstream', str(root / 'upstream.git'), cwd=repo)
    # Another person's local copy advances origin and deletes the retired remote branch
    peer = root / 'peer'
    git('clone', '-q', str(root / 'origin.git'), str(peer))
    git('config', 'core.autocrlf', 'false', cwd=peer)
    git('config', 'commit.gpgsign', 'false', cwd=peer)
    (peer / 'README.md').write_text('# Shared project\n\nUpdate from a teammate\n', encoding='utf-8')
    git('add', 'README.md', cwd=peer)
    git('commit', '-q', '-m', 'Update instructions', cwd=peer)
    git('push', '-q', 'origin', 'main', cwd=peer)
    git('push', '-q', 'origin', '--delete', 'feature/retired', cwd=peer)
    print('Ready: sandbox/repo has origin and upstream; its remote-tracking names are out of date')
    print('Next: cd sandbox/repo')


if __name__ == '__main__':
    main()
