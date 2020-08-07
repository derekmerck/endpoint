import typing as typ
import os
import pathlib
import io
import yaml


def smart_yaml_loader(data: typ.Union[pathlib.Path, str, io.StringIO])\
        -> typ.Union[typ.List, typ.Dict]:

    # If this is an open-able file, open it
    try:
        if os.path.isfile(data):
            data = open(data)
    except:
        pass
    res = yaml.safe_load(data)
    return res
