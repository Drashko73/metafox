import datetime

def get_current_date() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None).isoformat() + " UTC"