"""
Simple persistent dictionary using a redis instance.
"""

from urllib.parse import urlparse
import pickle
import attr
from redis import Redis
from .endpoint import UID, Data
from .persistence import PersistenceBackend


SERIALIZER = "pickle"


# Redis wrapper that behaves like a persistent k,v store
@attr.s(auto_attribs=True)
class RedisPersistenceBackend(PersistenceBackend):

    url: str = "redis://localhost:6379"
    password: str = None
    db: int = 0
    namespace: str = "pbe"

    gateway: Redis = attr.ib(init=False, repr=False)
    @gateway.default
    def make_gateway(self):
        p = urlparse(self.url)
        host = p.netloc.split(":")[0]
        if len( p.netloc.split(":") ) > 1:
            port = int( p.netloc.split(":")[1] )
        else:
            port = 6379
        _gateway = Redis(host=host, port=port, password=self.password, db=self.db)
        return _gateway

    def t(self, key: UID) -> Data:
        return f"{self.namespace}/{key}"

    def __getitem__(self, key: UID):
        ser = self.gateway.get(self.t(key))
        if ser:
            obj = pickle.loads(ser)
            return obj

    def __setitem__(self, key: UID, value: Data):
        ser = pickle.dumps(value)
        self.gateway.set(self.t(key), ser)

    def __delitem__(self, key: UID):
        return self.gateway.delete(self.t(key))

    def __contains__(self, key: UID):
        keys = self.gateway.keys()
        return keys.__contains__(self.t(key))

    def clear(self):
        """Clears all namespaces in this shelf"""
        self.gateway.flushdb()
