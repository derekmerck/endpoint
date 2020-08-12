from datetime import datetime
from pprint import pprint
from cryptography.fernet import Fernet
from libsvc.utils import pack_data, unpack_data


def pack_data_test():

    fkey = Fernet.generate_key()

    data = {"today": datetime.today(),
            "dog": "cat",
            "red": "blue"}

    p = pack_data(data, fkey, fields=["today", "dog"])
    print(p.decode("utf8"))

    u = unpack_data(p, fkey)
    pprint(u)

    assert u["dog"] == "cat"
    today = datetime.fromisoformat(u["today"]).date()
    assert today == datetime.today().date()
    assert "red" not in u


if __name__ == "__main__":
    pack_data_test()
