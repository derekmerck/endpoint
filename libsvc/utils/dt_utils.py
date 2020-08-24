import typing as typ
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

    def intervals(self, interval_delta=timedelta(hours=1)):
        """Usage:
        >>> for interval in TimeInterval().intervals(timedelta(hours=1)):
        ...    print(interval)
        """

        @attr.s(auto_attribs=True)
        class IntervalIterator(object):
            start: datetime = datetime.now()
            end: datetime = datetime.now() + timedelta(hours=1)
            interval_delta: timedelta = timedelta(minutes=5)

            interval_start: datetime = attr.ib(init=False)
            @interval_start.default
            def mk_interval_start(self):
                print(f"Range start: {self.start}")
                print(f"Range end:   {self.end}")
                return self.start

            def __iter__(self) -> "IntervalIterator":
                return self

            def __next__(self) -> typ.Tuple[datetime, datetime]:
                this_start = self.interval_start
                this_end = self.interval_start + self.interval_delta
                if this_start > self.end:
                    raise StopIteration
                self.interval_start += self.interval_delta
                return this_start, this_end

        return IntervalIterator(start=self.start, end=self.end, interval_delta=interval_delta)


def small_rand_td(second_range = 60*60*24*5, _seed: str = None) -> timedelta:
    if _seed:
        random.seed(_seed)
    second_offset = random.randint(-second_range, second_range)
    return timedelta(seconds=second_offset)
