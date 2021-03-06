import logging
from abc import ABC
from pprint import pformat
import yaml
import attr


@attr.s
class AttrsSerializable(ABC):

    # exclude_from_attrs serialization
    attr_exclude = ["_logger"]

    def as_dict(self, filters=None):

        def clean_entries(k, v):
            if k.name not in _filters and \
                    v is not None and \
                    k.repr and \
                    v != k.default and \
                    k.init:
                return True
            return False

        _filters = filters or []
        for cls in self.__class__.mro():
            if hasattr(cls, "attr_exclude"):
                _filters += cls.attr_exclude
        _dict = attr.asdict(self, filter=clean_entries)
        # Get rid of leading underscores for private vars (silly attrs convention)
        _dict = {k.lstrip("_"): v for k, v in _dict.items()}
        _dict["ctype"] = self.__class__.__name__
        return _dict

    @property
    def logger(self):
        _logger = logging.getLogger(self.__class__.__name__)
        return _logger

    def prepr(self, logger_level=logging.DEBUG, filters=None):
        # "Pretty repr"
        self.logger.log( logger_level, pformat(self.as_dict(filters=filters)) )

    @classmethod
    def loads(cls, ser: str, format="yaml"):
        if format == "yaml":
            _dict = yaml.load(ser, Loader=yaml.Loader)
        else:
            raise ValueError("Unknown formatter")
        return _dict

    def dumps(self, format="yaml"):
        _dict = self.as_dict()
        if format == "yaml":
            txt = yaml.dump(_dict)
        else:
            raise ValueError("Unknown formatter")
        return txt

    class Factory(object):
        registry = {}

        @classmethod
        def create(cls, **kwargs) -> "AttrsSerializable":
            if not "ctype" in kwargs.keys():
                raise ValueError("No ctype in description")
            ctype = kwargs.get("ctype")
            del kwargs["ctype"]
            if ctype not in cls.registry.keys():
                raise KeyError(f"No ctype={ctype} registered!")
            _cls = cls.registry[ctype]
            return _cls(**kwargs)

        make = create

        @classmethod
        def register(cls, _cls="AttrsSerializable"):
            # print(f"Registering {_cls.__name__}")
            cls.registry[_cls.__name__] = _cls

    def __attrs_post_init__(self):
        # self.logger.debug(f"Initting {self.__class__} as serializable")
        AttrsSerializable.Factory.register(self.__class__)
