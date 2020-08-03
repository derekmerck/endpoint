"""Generic endpoint and rest ep with shelf ABC"""

from abc import ABC
import typing as typ

UID = typ.TypeVar('UID')
Data = typ.TypeVar('Data')


# Basic ABC that translates UIDs and Data to and from
# endpoint APIs
class Endpoint(ABC):

    def status(self) -> bool:
        raise NotImplemented

    def get(self, uid: UID, *args, **kwargs) -> Data:
        """Send a single uid, return a data object"""
        raise NotImplemented

    def find(self, query: typ.Dict, *args, **kwargs) -> typ.List[UID]:
        """Send a query dict, return a list of uid's or []"""
        raise NotImplemented

    def put(self, data: Data, *args, **kwargs) -> UID:
        """Send a data object, return its uid or None"""
        raise NotImplemented

    def delete(self, uid: UID, *args, **kwargs) -> bool:
        """Send a single uid, return a boolean"""
        raise NotImplemented
