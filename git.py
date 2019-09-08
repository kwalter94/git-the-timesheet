from functools import reduce

import os
import re


def open_git_log(repository, authors, start_date=None, end_date=None):
    '''Open git log for a given repository as a file.
    
    Example:
        >>> open_git_log(repository=os.getcwd(), authors=['walterkaunda@live.co.uk'], start_date='2019-05-15', end_date='2019-05-16')\
                .readlines()[0]
        'commit 8c13c3d2d86aaff65211ee2c9c29ee4b7582784a\\n'
    '''
    def build_command():
        authors_opt = reduce(lambda s, i: f'{s} --author {i}', authors, '')
        start_date_opt = start_date and f'--since {start_date}' or ''
        end_date_opt = end_date and f'--until {end_date}' or ''
        repository_opt = repository and f'-C {repository}' or ''

        return f'git {repository_opt} log {authors_opt} {start_date_opt} {end_date_opt} --date iso --date-order --branches'

    return os.popen(build_command())

def parse_git_log(log_file, commit_transformer=lambda commit: commit):
    '''Parses git commits from a file object.

    Example:
        >>> log = open_git_log(repository=os.getcwd(), authors=['walterkaunda@live.co.uk'], end_date='2019-05-16')
        >>> commit = parse_git_log(log)[0]
        >>> commit['id']
        '8c13c3d2d86aaff65211ee2c9c29ee4b7582784a'
        >>> commit['date']
        '2019-05-15 21:20:54 +0200'
        >>> commit['author']
        'Walter Kaunda <walterkaunda@live.co.uk>'
    '''
    commits = []

    current_commit = {}

    for line in log_file:
        if line.isspace():
            continue
        elif line.startswith('commit'):
            if current_commit:
                commits.append(current_commit)
                current_commit = {'body': ''}

            _, commit_id = line.split(' ', 1)
            current_commit['id'] = commit_id.strip()
        elif line.startswith('Author') or line.startswith('Date'):
            field, value = re.split(r'\s+', line, 1)
            current_commit[field.lower()[:-1]] = value.strip()
        else:
            body = current_commit.get('body', '')
            line = line.lstrip()
            current_commit['body'] = f'{body}{line}'

    if current_commit:
        commits.append(current_commit)

    return commits


if __name__ == '__main__':
    import doctest

    doctest.testmod()
