from functools import reduce

import os

class GitLog:
    '''Open git log for a given repository as a file.
    
    Example:
        >>> GitLog().set_repository(os.getcwd())\
                    .add_author('walterkaunda@live.co.uk')\
                    .set_start_date('2019-05-15')\
                    .set_end_date('2019-05-16')\
                    .open()\
                    .readlines()[0]
        'commit 8c13c3d2d86aaff65211ee2c9c29ee4b7582784a\\n'
    '''

    def __init__(self):
        self.repository = None
        self.authors = []
        self.start_date = None
        self.end_date = None

    def add_author(self, author):
        self.authors.append(author)

        return self

    def set_start_date(self, date):
        self.start_date = date

        return self

    def set_end_date(self, date):
        self.end_date = date
        
        return self

    def set_repository(self, repository):
        self.repository = repository

        return self

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

if __name__ == '__main__':
    import doctest

    doctest.testmod()
