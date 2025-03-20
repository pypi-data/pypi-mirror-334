import time


def get_today(ts, fmt='%Y-%m-%d'):
    return time.strftime(fmt, time.localtime(ts))
