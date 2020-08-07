"""Generic endpoint ABCs"""

from abc import ABC
import typing as typ
import attr
from .data_item import DataItem, UID


# Basic ABC that translates UIDs and Data to and from endpoint APIs
@attr.s(hash=False)
class Endpoint(ABC):

    def status(self) -> bool:
        """Check enpoint health or raise EndpointHealthException"""
        raise NotImplemented

    def get(self, uid: UID, *args, **kwargs) -> DataItem:
        """Send a single uid, return a data object"""
        raise NotImplemented

    def find(self, query: typ.Dict, *args, **kwargs) -> typ.List[UID]:
        """Send a query dict, return a list of uid's or []"""
        raise NotImplemented

    def exists(self, uid: UID, *args, **kwargs) -> bool:
        raise NotImplementedError

    def put(self, data: DataItem, *args, **kwargs) -> UID:
        """Send a data object, return its uid or None"""
        raise NotImplemented

    def delete(self, uid: UID, *args, **kwargs) -> bool:
        """Send a single uid, return a boolean"""
        raise NotImplemented

    # Alias 'remove' to the 'delete' method for convenience
    remove = delete

    def inventory(self, *args, **kwargs) -> typ.Union[UID, DataItem]:
        """Return all items or keys for all items"""
        raise NotImplementedError

    def clear(self, *args, **kwargs):
        """Remove all items, reset endpoint data"""
        raise NotImplementedError
