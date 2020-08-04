"""Generic endpoint ABCs"""

from abc import ABC
import typing as typ
import uuid
import attr


@attr.s(hash=False)
class Hashable(ABC):
    # Unique id for session, not persistent for endpoint across sessions
    _uuid: uuid = attr.ib(factory=uuid.uuid4, init=False)

    def __hash__(self):
        return self._uuid.int


@attr.s(auto_attribs=True)
class Data(Hashable):
    meta: typ.Dict = attr.Factory(dict)
    data: typ.Any = None


# Maybe the object uuid, or a source specific key
UID = typ.TypeVar('UID')


# Basic ABC that translates UIDs and Data to and from endpoint APIs
@attr.s(hash=False)
class Endpoint(ABC):

    def status(self) -> bool:
        """Check enpoint health or raise EndpointHealthException"""
        raise NotImplemented

    def get(self, uid: UID, *args, **kwargs) -> Data:
        """Send a single uid, return a data object"""
        raise NotImplemented

    def find(self, query: typ.Dict, *args, **kwargs) -> typ.List[UID]:
        """Send a query dict, return a list of uid's or []"""
        raise NotImplemented

    def exists(self, uid: UID, *args, **kwargs) -> bool:
        raise NotImplementedError

    def put(self, data: Data, *args, **kwargs) -> UID:
        """Send a data object, return its uid or None"""
        raise NotImplemented

    def delete(self, uid: UID, *args, **kwargs) -> bool:
        """Send a single uid, return a boolean"""
        raise NotImplemented

    # Alias 'remove' to the 'delete' method for convenience
    remove = delete

    def inventory(self, *args, **kwargs) -> typ.Union[UID, Data]:
        """Return all items or keys for all items"""
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        """Remove all items, reset endpoint data"""
        raise NotImplementedError
