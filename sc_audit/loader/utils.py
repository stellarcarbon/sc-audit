import datetime

def parse_iso_date(iso_date: str) -> datetime.date:
    return datetime.datetime.fromisoformat(iso_date).date()

def parse_iso_datetime(iso_datetime: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(iso_datetime)
