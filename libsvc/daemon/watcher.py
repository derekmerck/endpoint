"""
Creating a Watcher framework
------------------------------
1. Derive an EventType class to distinguish relevant event types
2. Derive an Observable class for each source that implements a
   "changes" method
3. Changes should returns a list of new events (event_type, data)
   since last check
4. Create callable handlers with functools.partial that operate on
   the data attached to each change, it is often convenient to create
   these as methods on the source, but it is not required
5. Create a list of triggers (source instance, event_type, action)
6. Pass triggers to the generic watcher and call handle_all, run,
   or daemonize to fork a separate process
"""

import typing as typ
import time
import attr
from ..endpoint.hashable import Hashable

EventType = typ.TypeVar("EventType")


@attr.s(auto_attribs=True)
class Event(object):
    event_type: EventType
    data: typ.Any


@attr.s(auto_attribs=True, hash=False)
class ObservableMixin(Hashable):

    def changes(self) -> typ.List[Event]:
        raise NotImplemented


@attr.s(auto_attribs=True)
class Trigger(object):

    source: ObservableMixin = None
    event_type: EventType = None
    handler: typ.Callable = None


@attr.s(auto_attribs=True)
class Watcher(object):

    triggers: typ.List[Trigger] = attr.ib(factory=list)
    monitor_interval: float = 1.0

    def handle_all(self):
        observations = {}
        # Same source can trigger many events to cache
        # the observations for reuse
        for trigger in self.triggers:
            if observations.get(trigger.source) is None:
                observations[trigger.source] = trigger.source.changes()
        for trigger in self.triggers:
            for event in observations[trigger.source]:
                if event.event_type == trigger.event_type:
                    trigger.handler(event.data)

    def run(self):
        while True:
            self.handle_all()
            time.sleep(self.monitor_interval)
