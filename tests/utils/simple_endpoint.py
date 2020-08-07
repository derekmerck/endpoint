import typing as typ
import attr
from libsvc.endpoint import Endpoint, Serializable


@attr.s
class SimpleEP(Endpoint, Serializable):

    cache = attr.ib(factory=dict, init=False)
    dummy1 = attr.ib(default=42)
    dummy2 = attr.ib(default=43)

    def status(self):
        return True

    def get(self, id: str, **kwargs):
        return self.cache.get(id)

    def exists(self, id: str, **kwargs):
        return id in self.cache

    def find(self, query: typ.Mapping, **kwargs):
        val = query.get('q')
        for k, v in self.cache.items():
            if v == val:
                return k

    def put(self, item, **kwargs):
        id = hash(item)
        self.cache[id] = item
        return id

    def update(self, id, new_data, **kwargs):
        self.cache[id] = new_data


Serializable.Factory.register(SimpleEP)
