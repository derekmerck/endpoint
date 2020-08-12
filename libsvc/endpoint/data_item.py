"""
DataItem's implement a range of validation and provenancing attributes
and methods.

Each data item encompasses three domains:
- metadata
- data
- the preferred binary representation (as it would be saved to disk, for example)

Information in each of these domains is should be hashable by implementing the
'mk_*hash' functions.  These functions all get called during __attrs_post_init__
so derived classes will have access to all their attributes by then.

This is distinct from the "Hashable" ABC, which provides a uuid for pythonic-hashing
of instances into sets or maps without freezing the instance.

Changing the classes __cmp__ function to look at different hashes (uuid, mhash, dhash,
or bhash) allows various comparisons.

1. Using 'uuid' is traditional pythonic "same instance"
2. Using 'mhash' can compare headers even if the data is not present in either or
   both instaces
3. Using 'dhash' will identifies duplicate data even when the metadata has changed,
   for example, when one dataset has been anonymized
4. Using 'bhash' is equivalent to comparing the hashes of the source data files

It's a bit clunky, but the user can set the comparison type on demand by manipulating
the class "comparator" attribute.

>> a = DataItem(meta="a", data=1)
>> b = DataItem(meta="b", data=1)
>> a == b
False
>> DataItem.comparator = ComparatorType.DATA
>> a == b
True

Comparison by Uuid-hashing ("strict-hashing") is always available by implementation.
Meta-hashing is assumed to be available bc there is not a good reason to use this
class without  some minimal amount of metadata.  Data-hashing and Binary-hashing may
not be available, if those hashes don't exist for either member, __cmp__ raises
ValueError.
"""

import typing as typ
from enum import Enum, auto
from datetime import datetime
import hashlib
import attr
from .hashable import Hashable

# Maybe the object uuid, or a source specific key
UID = typ.TypeVar('UID')


class ComparatorType(Enum):
    STRICT = auto()  # Value is irrelevant, as it's never serialized
    METADATA = auto()
    DATA = auto()
    BINARY = auto()


@attr.s(auto_attribs=True, eq=False, hash=False)
class DataItem(Hashable):
    meta: typ.Dict = attr.Factory(dict)
    data: typ.Any = None
    binary: bytes = attr.ib(repr=False, default=None)

    timestamp: datetime = None
    # Overload to set non-now timestamp
    def mk_timestamp(self):
        return datetime.now()

    mhash: str = None
    def mk_mhash(self):
        return hashlib.sha3_224(str(self.meta).encode("utf8")).hexdigest()

    dhash: str = None
    def mk_dhash(self):
        if self.data is None:
            return None
        return hashlib.sha3_224(self.data).hexdigest()

    bhash: str = None
    def mk_bhash(self):
        if self.binary is None:
            return None
        return hashlib.sha3_224(self.binary).hexdigest()

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

    comparator: typ.ClassVar[ComparatorType] = ComparatorType.STRICT

    def __eq__(self, other: "DataItem"):
        if self.__class__.comparator == ComparatorType.STRICT:
            return self._uuid == other._uuid
        elif self.__class__.comparator == ComparatorType.METADATA:
            return self.mhash == other.mhash
        elif self.__class__.comparator == ComparatorType.DATA:
            if self.dhash is None or other.dhash is None:
                raise ValueError("Incomparable -- missing data hash")
            return self.dhash == other.dhash
        elif self.__class__.comparator == ComparatorType.BINARY:
            if self.bhash is None or other.bhash is None:
                raise ValueError("Incomparable -- missing binary hash")
            return self.bhash == other.bhash
        raise TypeError(f"Unknown comparator type {self.__class__.comparator}")

    __hash__ = Hashable.__hash__  # Attrs thinks fancy eq means unhashable
