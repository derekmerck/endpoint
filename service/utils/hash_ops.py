
import numpy as np


def hex_xor(h1: str, h2: str) -> str:
    "Hex string xor: F0 ^ 0F = FF"
    b1 = bytearray.fromhex(h1)
    b2 = bytearray.fromhex(h2)
    n1 = np.frombuffer(b1, dtype='uint8')
    n2 = np.frombuffer(b2, dtype='uint8')
    res = (n1 ^ n2).tobytes()
    return res.hex()
