import datetime


def convert_date_to_int(date: str) -> int:
    date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return int(date.timestamp())
