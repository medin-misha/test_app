import base64
import random


def base_encode(user_id: str) -> str:
    string: str = f"{random.randint}:{user_id}"
    str_bytes: bytes = string.encode("ascii")
    str_base64: str = base64.b64encode(str_bytes).decode("ascii")
    return str_base64
