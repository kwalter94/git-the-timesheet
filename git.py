from functools import reduce

import os
import re


class GitLog:
    '''Open git log for a given repository as a file.
    
    Example:
        >>> GitLog(repository=os.getcwd(), authors=['walterkaunda@live.co.uk'], start_date='2019-05-15', end_date='2019-05-16')\
                .open()\
                .readlines()[0]
        'commit 8c13c3d2d86aaff65211ee2c9c29ee4b7582784a\\n'
    '''

    def __init__(self, repository=None, authors=[], start_date=None, end_date=None):
        self.repository = repository
        self.authors = authors[:]
        self.start_date = start_date
        self.end_date = end_date

    def open(self):
        '''Returns a file like object from which the git log can be read.'''
        command = self.build_command()

        return os.popen(command)

    def build_command(self):
        authors = reduce(lambda s, i: f'{s} --author {i}', self.authors, '')
        start_date = self.start_date and f'--since {self.start_date}' or ''
        end_date = self.end_date and f'--until {self.end_date}' or ''
        repository = self.repository and f'-C {self.repository}' or ''

        return f'git {repository} log {authors} {start_date} {end_date} --date iso --date-order --branches'


class GitLogFileParser:
    '''Parses git commits from a file object.

    Example:
        >>> log = GitLog(repository=os.getcwd(), authors=['walterkaunda@live.co.uk'], end_date='2019-05-16')
        >>> commit = GitLogFileParser(log.open()).parse()[0]
        >>> commit['id']
        '8c13c3d2d86aaff65211ee2c9c29ee4b7582784a'
        >>> commit['date']
        '2019-05-15 21:20:54 +0200'
        >>> commit['author']
        'Walter Kaunda <walterkaunda@live.co.uk>'
    '''

    def __init__(self, log_file):
        self.log_file = log_file

    def parse(self, commit_transformer=lambda commit: commit):
        commits = []

        current_commit = {}

        for line in self.log_file:
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
