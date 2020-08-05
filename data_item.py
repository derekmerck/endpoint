import typing as typ
import attr
from .hashable import Hashable

# Maybe the object uuid, or a source specific key
UID = typ.TypeVar('UID')


@attr.s(auto_attribs=True)
class DataItem(Hashable):
    meta: typ.Dict = attr.Factory(dict)
    data: typ.Any = None
    binary: bytes = None

    mhash: str = None
    def mk_mhash(self):
        raise NotImplementedError

    dhash: str = None
    def mk_dhash(self):
        raise NotImplementedError

    bhash: str = None
    def mk_bhash(self):
        raise NotImplementedError

    # Don't want to do this until everything is settled
    def __attrs_post_init__(self):
        if not self.mhash:
            self.mhash = self.mk_mhash()
        if not self.dhash:
            self.dhash = self.mk_dhash()
        if not self.bhash:
            self.bhash = self.mk_bhash()
