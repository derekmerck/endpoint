import tempfile
import yaml
from libsvc.endpoint import ServiceManager
import pytest

service_text = \
"""
simple1:
  ctype: SimpleEP

simple2:
  ctype: SimpleEP
  dummy1: foo
"""


def test_mgr_from_descs():
    M = ServiceManager.from_descs(data=service_text)
    assert len( M.status() ) == 2

    print(M.status())

    with tempfile.TemporaryFile("w+") as tmp:
        tmp.write(service_text)
        tmp.seek(0)
        MM = ServiceManager.from_descs(data=tmp)
        assert( len(MM.status() ) == 2)

    MMM = ServiceManager.from_descs(data="{simple1:{ctype: SimpleEP}}")
    assert len( MMM.status() ) == 1

    with pytest.raises(yaml.parser.ParserError):
        ServiceManager.from_descs(data="{simple1:{ctype: SimpleEP}")

    with pytest.raises(KeyError):
        ServiceManager.from_descs(data="{simple1:{ctype: SimpleEP1111}}")


if __name__ == "__main__":
    test_mgr_from_descs()