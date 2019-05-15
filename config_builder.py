from configparser import ConfigParser
from typing import List
import os
import os.path


HOME_DIR_PATH = os.path.expanduser('~')
GIT_CONFIG_FILE_PATH = os.path.join(HOME_DIR_PATH, '.gitconfig')
TIMESHEET_CONFIG_FILE_PATH = os.path.join(HOME_DIR_PATH, '.timesheet')

def find_git_repos(root_dir: str) -> List[str]:
    repos = []

    for path, dirs, _files in os.walk(root_dir):
        if '.git' in dirs:
            path = os.path.abspath(path)

            response = prompt_stdin_yes_no(f'Do you wish to track {path}?', 'No')
            if response.lower() == 'no':
                print(f'Not tracking {path}')
                continue

            print(f'Tracking {path}...')
            repos.append(os.path.abspath(path))

    return repos

def configure_repos(repos: List[str], default_donor: str, default_username: str,
                    default_email: str) -> List[dict]:
    def configure_repo(repo: str) -> List[dict]:
        print(f'\n\nConfiguring repo: {repo}........')
        return (repo, {
            'donor': get_repo_donor(repo, default_donor),
            'username': get_repo_git_username(repo, default_username),
            'email': get_repo_git_email(repo, default_email)
        })

    return map(configure_repo, repos)

def get_repo_dir() -> str:
    repo_dir = prompt_stdin('Where are your git repositories?', HOME_DIR_PATH)
    
    return os.path.abspath(os.path.expanduser(repo_dir))

def get_primary_donor() -> str:
    return prompt_stdin('Who is your primary donor?')

def get_repo_donor(repo: str, default_donor: str) -> str:
    return prompt_stdin(f'Donor?', default_donor)

def get_repo_git_email(repo: str, default_email: str) -> str:
    repo_config = read_config(os.path.join(repo, '.git', 'config'))
    default_email = repo_config.get('user', 'dummy', fallback={}).get('email') or default_email

    return prompt_stdin(f'Email?', default_email)

def get_git_username() -> str:
    config = read_config(GIT_CONFIG_FILE_PATH)
    default_username = config.get('user', 'dummy', fallback={}).get('name') or os.environ['USERNAME']

    return prompt_stdin('What username do you *frequently* use for git?', default_username)

def get_repo_git_username(repo: str, default_username: str) -> str:
    repo_config = read_config(os.path.join(repo, '.git', 'config'))
    default_username = repo_config.get('user', 'dummy', fallback={}).get('name') or default_username

    return prompt_stdin(f'Username?', default_username)

def get_git_email() -> str:
    if os.path.exists(GIT_CONFIG_FILE_PATH):
        config = read_config(GIT_CONFIG_FILE_PATH)
        default_email = config['user'].get('email', None)
    else:
        default_email = None

    return prompt_stdin('What email address do you *frequently* use for git?', default_email)

def prompt_stdin(prompt_text: str, default_value: str = None):
    if default_value:
        prompt_text = f'{prompt_text} [default: {default_value}]'

    while True:
        value = input(f'{prompt_text}> ').strip()

        if not (value or default_value):
            print('Please enter a valid value...')
            continue

        return value or default_value

def prompt_stdin_yes_no(prompt_text: str, default_value: str = 'No') -> str:
    while True:
        response = prompt_stdin(prompt_text, default_value).lower()

        if response in 'no' or response in ['y', 'yes']:
            return response


def read_config(path: str) -> ConfigParser:
    config = ConfigParser()
    config.read(path)

    return config

def build_config(repos_root_dir: str):
    config = ConfigParser()

    print('1. Setting up base configuration..........')
    config['DEFAULT'] = { 'username': get_git_username(),
                          'email': get_git_email(),
                          'donor': get_primary_donor() }   

    print(f'\n\n2. Scanning `{repos_root_dir}` for repos........')
    repos = find_git_repos(repos_root_dir)

    print(f'\n\n3. Configuring repos.............')
    repo_configs = configure_repos(repos, config['DEFAULT']['donor'], config['DEFAULT']['username'],
                                   config['DEFAULT']['email'])

    for repo, repo_config in repo_configs:
        config[repo] = repo_config

    return config

def main():
    import sys

    repo_dir = get_repo_dir()
    config = build_config(repo_dir)
    config.write(sys.stdout)
    config.write(TIMESHEET_CONFIG_FILE_PATH)

if __name__ == '__main__':
    main()
