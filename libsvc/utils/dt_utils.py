from datetime import datetime, timedelta
import random
from dateutil import parser as dtparser
import attr


def parse_time(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return dtparser.parse(value)
        except dtparser._parser.ParserError:
            return None


def pathsafe_dt(dt: datetime) -> str:
    s = dt.strftime('%y-%m-%dT%H-%M')
    return s


@attr.s(auto_attribs=True)
class TimeInterval(object):
    start: datetime = attr.ib(converter=parse_time)

    @start.default
    def default_start(self):
        return datetime.now() - timedelta(minutes=5)
    end: datetime = attr.ib(factory=datetime.now, converter=parse_time)

    def duration(self) -> timedelta:
        return self.end - self.start

    def as_dict(self):
        return {'startTime': self.start.isoformat(),
                'endTime': self.end.isoformat()}


def small_rand_td(second_range = 60*60*24*5, _seed: str = None) -> timedelta:
    if _seed:
        random.seed(_seed)
    second_offset = random.randint(-second_range, second_range)
    return timedelta(seconds=second_offset)
