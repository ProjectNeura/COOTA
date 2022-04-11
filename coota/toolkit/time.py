from typing import Sequence
import datetime as _dt
import re as _re


UNITS = ("year", "month", "day", "hour", "minute", "second", "microsecond")

UNITS_FEATURES = (
    ("year", lambda t: 3 < t <= 4, lambda t: True),
    ("month", lambda t: 0 < t <= 2, lambda t: 0 < t < 13),
    ("day", lambda t: 0 < t <= 2, lambda t: 0 < t < 32),
    ("hour", lambda t: 0 < t <= 2, lambda t: -1 < t < 25),
    ("minute", lambda t: 0 < t <= 2, lambda t: -1 < t < 61),
    ("second", lambda t: 0 < t <= 2, lambda t: -1 < t < 61),
    ("microsecond", lambda t: 0 < t <= 6, lambda t: -1 < t < 1000000)
)


def parse_time_type(t: str, exclude: Sequence) -> [str, int]:
    length = len(t)
    t = int(t)
    for unit in UNITS_FEATURES:
        if unit[1](length) and unit[0] not in exclude and unit[2](t):
            return unit[0], t
    return "unknown", t


def parse_time(time: str) -> _dt.datetime:
    cases = _re.findall(r"\d+", time)
    exclude = []
    now = _dt.datetime.now()
    matched = [now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond]
    for t in cases:
        time_type, t = parse_time_type(t, exclude)
        if time_type == "unknown":
            continue
        exclude.append(time_type)
        matched[UNITS.index(time_type)] = t
    return _dt.datetime(year=matched[0], month=matched[1], day=matched[2], hour=matched[3], minute=matched[4],
                        second=matched[5], microsecond=matched[6])
