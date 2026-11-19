"""Create five independent practice repositories for the Git cheat-sheet examples."""
import argparse
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, default=Path(__file__).resolve().parent / 'sandbox')
    root = parser.parse_args().sandbox.resolve()
    if root.exists():
        raise SystemExit('This sandbox already exists. Choose a new folder with --sandbox sandbox-2')
    root.mkdir(parents=True)
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
               GIT_AUTHOR_NAME='Demo Student', GIT_AUTHOR_EMAIL='student@example.com',
               GIT_COMMITTER_NAME='Demo Student', GIT_COMMITTER_EMAIL='student@example.com')

    def git(repo, *args):
        return subprocess.run(['git', *args], cwd=repo, env=env, check=True,
                              capture_output=True, text=True).stdout.strip()

    def save(repo, letter, filename, contents):
        env['GIT_AUTHOR_DATE'] = env['GIT_COMMITTER_DATE'] = f'2026-11-16T09:0{ord(letter)-65}:00+01:00'
        (repo / filename).write_text(contents, encoding='utf-8')
        git(repo, 'add', filename)
        git(repo, 'commit', '-q', '-m', letter)

    for name in ('rebase', 'merge', 'squash', 'fast-forward', 'cherry-pick'):
        repo = root / name
        repo.mkdir()
        git(repo, 'init', '-q', '-b', 'main')
        git(repo, 'config', 'user.name', 'Demo Student')
        git(repo, 'config', 'user.email', 'student@example.com')
        git(repo, 'config', 'core.autocrlf', 'false')
        git(repo, 'config', 'commit.gpgsign', 'false')
        save(repo, 'A', 'README.md', '# Practice project\n')
        save(repo, 'B', 'README.md', '# Practice project\n\nShared starting point\n')
        shared = git(repo, 'rev-parse', 'HEAD')
        save(repo, 'C', 'main.txt', 'Work added on main\n')
        git(repo, 'switch', '-q', '-c', 'banana', 'main' if name == 'fast-forward' else shared)
        save(repo, 'D', 'feature.txt', 'First feature change\n')
        save(repo, 'E', 'feature.txt', 'First feature change\nSecond feature change\n')
        git(repo, 'switch', '-q', 'main')
    print('Ready: five practice folders inside sandbox')
    print('Open STEPS.md and choose one example')


if __name__ == '__main__':
    main()
