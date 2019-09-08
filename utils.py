from datetime import date, timedelta
from typing import List

def start_of_week(date:date) -> date:
    '''Returns the date which marks the start of the week containing given date.
    
    Example:
        >>> start_of_week(date(2019, 9, 13))
        datetime.date(2019, 9, 8)
        >>> start_of_week(date(2019, 9, 8))
        datetime.date(2019, 9, 8)
    '''
    if date.weekday() == 6: return date

    return date - timedelta(days=date.weekday() + 1)

def date_range(start_date:date, end_date:date) -> List[date]:
    '''Returns a list of dates in range [start_date, end_date).
    
    Example:
        >>> date_range(date(2019, 9, 8), date(2019, 9, 10))
        [datetime.date(2019, 9, 8), datetime.date(2019, 9, 9)]
        >>> date_range(date(2019, 9, 8), date(2019, 9, 8))
        []
    '''
    return [start_date + timedelta(days=days) for days in range((end_date - start_date).days)]


if __name__ == '__main__':
    import doctest

    doctest.testmod()