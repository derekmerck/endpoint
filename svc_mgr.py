import typing as typ
import os
import pathlib
import yaml
import attr
from .attrs_serializable import AttrsSerializable as Serializable
from .data_item import UID


PathLike = typ.Union[str, pathlib.Path]


@attr.s(auto_attribs=True)
class ServiceManager(object):

    service_registry: typ.Dict[str, Serializable] = attr.ib(factory=dict)

    # Pass in a function to convert strings/names to appropriate service objects
    # ie, file:/foo -> FileEndpoint(root="/foo") or orthanc:/foo -> Orthanc(url=http:/foo)
    name_shortcuts: typ.Callable = None

    def get(self, name: UID) -> typ.Union[Serializable, None]:
        if self.name_shortcuts and self.name_shortcuts(name):
            return self.name_shortcuts(name)
        return self.service_registry.get(name)

    def status(self):
        res = {}
        for name, service in self.service_registry.items():
            try:
                res[name] = service.status() is not None  # Working if it returns a value
            except:
                res[name] = False  # Not a service or raised any error
        return res

    def add_service(self, name, **desc):
        if "ctype" not in desc:
            raise TypeError("Desc not appear to be a serialized object")
        service = Serializable.Factory.make(**desc)
        self.service_registry[name] = service

    @classmethod
    def from_descs(cls, data: PathLike, shortcuts: typ.Callable = None):
        mgr = cls(name_shortcuts=shortcuts)

        if os.path.isfile(data):
            with open(data) as f:
                descs = yaml.safe_load(f)
        else:
            descs = yaml.safe_load(data)

        for name, desc in descs.items():
            mgr.add_service(name, **desc)

        return mgr
