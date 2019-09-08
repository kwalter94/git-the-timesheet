from collections import namedtuple
from datetime import date, timedelta
from typing import Dict, List

from utils import start_of_week, date_range

DAYS_IN_MONTH = 28  # Timesheets are done for 28 day periods
DAYS_IN_WEEK = 7

def create_timesheet(tasks:List[Dict[str, str]], start_date:date, end_date:date) -> Dict[int, Dict[str, List[str]]]:
    '''Creates a timesheet from the given list of tasks.

    A tasks is just a dictionary with a 'date' and 'body' field.
    Timesheets on the other hand have a slightly complex structure.
    It's a tree-like object with weeks mapping to days that map to
    task bodies (ie week -> day -> task body). This structure is
    constructed as a dictionary of integers that map to dictionaries
    of dates that map to lists of task bodies
    (ie: Dict[int, Dict[str, List[str]]]).

    Example:
        >>> tasks = [{'date': '2019-09-08', 'body': 'foobar'}]
        >>> timesheet = create_timesheet(tasks, date(2019, 9, 8), date(2019, 9, 10))
        >>> timesheet[1]['2019-09-08'][0]
        'foobar'
    '''
    start_date = start_of_week(start_date)  # Timesheet weeks start on Sunday

    def find_week(day):
        '''Returns the week the day belongs to.'''
        for week in [1, 2, 3, 4, 5]:
            # Extending to week 5 to account for timesheets where th 15th falls
            # after sunday.
            if day < start_date + timedelta(days=DAYS_IN_WEEK * week):
                return week

    def init_timesheet():
        '''Creates an empty timesheet.'''
        timesheet = {}

        for day in date_range(start_date, end_date + timedelta(days=1)):
            week = find_week(day)
            if week not in timesheet:
                timesheet[week] = {}
            
            timesheet[week][str(day)] = []

        return timesheet

    def load_tasks_into_timesheet(timesheet):
        '''Loads tasks into timesheet.'''
        for task in tasks:
            task_date = date.fromisoformat(task['date']) # Strip off time part
            task_week = find_week(task_date)

            week_days = timesheet.get(task_week)
            if week_days is None:
                continue

            week_days[str(task_date)].append(task['body'])

    timesheet = init_timesheet()
    load_tasks_into_timesheet(timesheet)

    return timesheet


if __name__ == '__main__':
    import doctest

    doctest.testmod()