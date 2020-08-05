from abc import ABC
import uuid
import attr


@attr.s(hash=False)
class Hashable(ABC):
    # Unique id for session, not persistent for endpoint across sessions
    _uuid: uuid = attr.ib(factory=uuid.uuid4, init=False)

    def __hash__(self):
        return self._uuid.int
