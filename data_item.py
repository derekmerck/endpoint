import typing as typ
from datetime import datetime
import attr
from .hashable import Hashable

# Maybe the object uuid, or a source specific key
UID = typ.TypeVar('UID')


@attr.s(auto_attribs=True, hash=False)
class DataItem(Hashable):
    meta: typ.Dict = attr.Factory(dict)
    data: typ.Any = None
    binary: bytes = None

    timestamp: datetime = None
    # Overload to set non-now timestamp
    def mk_timestamp(self):
        return datetime.now()

    mhash: str = None
    def mk_mhash(self):
        raise NotImplementedError

    dhash: str = None
    def mk_dhash(self):
        raise NotImplementedError

    bhash: str = None
    def mk_bhash(self):
        raise NotImplementedError

    # Don't want to do these ops until everything is settled
    def __attrs_post_init__(self):
        if not self.timestamp:
            self.timestamp = self.mk_timestamp()
        if not self.mhash:
            self.mhash = self.mk_mhash()
        if not self.dhash:
            self.dhash = self.mk_dhash()
        if not self.bhash:
            self.bhash = self.mk_bhash()
