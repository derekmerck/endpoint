import attr
from .persistence import PersistenceBackend


# Add a "shelf" attribute to any object, distinguish application vars
# by putting them into different shelf namespaces
@attr.s(auto_attribs=True)
class ShelfMixin(object):
    shelf_ns: str = "pbe"
    shelf_type: str = "pickle"  # 'pickle' or 'redis'
    shelf: PersistenceBackend = attr.ib(init=False, repr=False, default=None)

    def setup_shelf(self) -> PersistenceBackend:
        if self.shelf_type.lower() == "pickle":
            return PersistenceBackend(namespace=self.shelf_ns)
        elif self.shelf_type.lower() == "redis":
            # Lazy import for redis
            from .redis_persistence import RedisPersistenceBackend
            return RedisPersistenceBackend(namespace=self.shelf_ns)
        else:
            raise ValueError(f"Unknown shelf type {self.shelf_type} requested")

    # Cannot setup as a default b/c derived class namespaces will not be respected
    def __attrs_post_init__(self):
        self.shelf = self.setup_shelf()
