from datetime import datetime
from pytz import timezone



def parse_datetime(dt_str, max=False, min=False):
    moscow_tz = timezone('Europe/Moscow')

    if max:
        date_obj = datetime.strptime(dt_str, '%Y-%m-%d').date()
        dt_str = datetime.combine(date_obj, datetime.max.time())
        return moscow_tz.localize(dt_str)
    if min:
        date_obj = datetime.strptime(dt_str, '%Y-%m-%d').date()
        dt_str = datetime.combine(date_obj, datetime.min.time())
        return moscow_tz.localize(dt_str)

    """Преобразует строку даты в datetime"""
    if not dt_str:
        return None
    try:
        naive_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        aware_dt = moscow_tz.localize(naive_dt)

        return aware_dt
    except ValueError:
        return None