import pytz
from datetime import datetime


def now_datetime() -> str:
    local_tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(local_tz)
    return today.strftime("%Y-%m-%d %H:%M:%S")
