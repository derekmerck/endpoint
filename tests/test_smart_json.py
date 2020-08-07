import logging, json
from hashlib import md5
import pathlib
from datetime import datetime
from service.utils import SmartJSONEncoder


def test_encoder():

    data = {
        "time": datetime(year=2000, month=1, day=1, hour=12),
        "path": pathlib.Path("/path/to/object"),
        "hash": md5("hello".encode("UTF-8"))
    }

    data_str = json.dumps(data, cls=SmartJSONEncoder)

    logging.debug(data_str)

    expected = """{"time": "2000-01-01T12:00:00", "path": "/path/to/object", "hash": "5d41402abc4b2a76b9719d911017c592"}"""

    assert( data_str == expected )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_encoder()
