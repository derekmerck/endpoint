"""
Simple persistent dictionary using a pickle file.
Could easily extend it to use Redis or any other cache.
"""

import os
import typing as typ
import pickle
import attr

UID = str
Data = typ.Any


# Pickle wrapper that behaves like a persistent k,v store
@attr.s(auto_attribs=True)
class PersistenceBackend(object):

    file: str = "/tmp/pbe.pkl"
    namespace: str = "pbe"
    registry: typ.Dict = attr.ib(init=False)

    @registry.default
    def load_registry(self) -> typ.Dict:
        if os.path.isfile(self.file):
            with open(self.file, "rb") as f:
                return pickle.load(f)
        return {}

    def t(self, key: UID) -> Data:
        return f"{self.namespace}/{key}"

    def __getitem__(self, key: UID):
        return self.registry.__getitem__(self.t(key))

    def __setitem__(self, key: UID, value: Data):
        ret = self.registry.__setitem__(self.t(key), value)
        with open(self.file, "wb") as f:
            pickle.dump(self.registry, f)
        return ret

    def __delitem__(self, key: UID):
        return self.registry.__delitem__(self.t(key))

    def __contains__(self, key: UID):
        return self.registry.__contains__(self.t(key))


# Add a "shelf" attribute to any object, distinguish variables
# by putting them into different namespaces
@attr.s(auto_attribs=True)
class ShelfMixin(object):
    shelf_ns: str = "pbe"
    shelf: PersistenceBackend = attr.ib(init=False, repr=False, default=None)

    def setup_shelf(self):
        return PersistenceBackend(namespace=self.shelf_ns)

    # Cannot setup as a default b/c derived class namespaces will not be respected
    def __attrs_post_init__(self):
        self.shelf = self.setup_shelf()
