import hmac


def make_digest(secret: bytes, data: bytes):
    digest = hmac.new(secret, msg=data, digestmod="sha1")
    return f"sha1={digest.hexdigest()}"
