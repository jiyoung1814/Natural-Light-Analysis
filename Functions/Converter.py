from datetime import datetime, timedelta

def TimestampToDatetime(ts):
    dt = datetime.fromtimestamp(ts / 1000)
    return dt

def DatetimeToTimestamp(dt):
    if type(dt) == str:
        dt = StrToDatetime(dt)

    float_ts = datetime.timestamp(dt)
    long_ts = int(float_ts * 1000)

    return long_ts

def StrToDatetime(str, type='%Y-%m-%d %H:%M:%S'):
    dt = datetime.strptime(str, type)
    return dt

def StrToDate(str, type='%Y-%m-%d'):
    d = datetime.strptime(str, type).date()
    return d

def DatetimeToStr(dt, type='%Y-%m-%d %H:%M:%S'):
    dt = dt.strftime(type)
    return dt


def TimestampToStrDatetime(ts, type='%Y-%m-%d %H:%M:%S'):
    dt = TimestampToDatetime(ts)
    return DatetimeToStr(dt, type)


def TimestampToDatetime_v1(ts):  # timestapm -> datetime
    # 서버와 현재 시간과 맞추기 위해 9시간 뺀다
    dt = datetime.fromtimestamp(ts / 1000) - timedelta(hours=9)
    return dt


def TimestampToStrDatetime_v1(ts, type='%Y-%m-%d %H:%M:%S'):
    dt = TimestampToDatetime_v1(ts)
    return DatetimeToStr(dt, type)


def class_to_dict(obj):
    if hasattr(obj, '__dict__'):
        data = {}
        for key, value in obj.__dict__.items():
            if isinstance(value, list):
                data[key] = [class_to_dict(item) for item in value]
            elif hasattr(value, '__dict__'):
                data[key] = class_to_dict(value)
            else:
                data[key] = value
        return data
    else:
        return obj
