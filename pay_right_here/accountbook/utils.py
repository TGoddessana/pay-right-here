import base64
import secrets


def generate_short_code():
    random_bytes = secrets.token_bytes(3)
    short_code = base64.urlsafe_b64encode(random_bytes).rstrip(b"=").decode("utf-8")
    return short_code
