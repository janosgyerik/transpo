from datetime import time


def times_gte(times, t):
    """
    Return the times greater than or equal to specified time

    >>> times_gte([], None)
    []

    >>> times_gte([time.min], time.min)
    [datetime.time(0, 0)]

    >>> times_gte([time.min], time.max)
    []

    >>> times_gte([time.max], time.max)
    [datetime.time(23, 59, 59, 999999)]

    >>> times_gte([time(1, 1), time(2, 2), time(3, 3)], time(2, 2))
    [datetime.time(2, 2), datetime.time(3, 3)]

    >>> times_gte([time(1, 1), time(2, 2), time(3, 3)], time(1, 9))
    [datetime.time(2, 2), datetime.time(3, 3)]

    :param times: time objects to filter
    :param t: target time to compare to
    :return: times greater than or equal to t
    """
    return list(filter(lambda x: t <= x, times))
