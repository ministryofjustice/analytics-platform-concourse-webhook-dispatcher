from schema import Schema


def release(payload) -> bool:
    data = Schema(
        {
            "action": str,
            "release": {"prerelease": bool, str: object},
            "repository": {"name": str, str: object},
            str: object,
        }
    ).validate(payload)
    return data["action"] == "published" and data["release"]["prerelease"] == False


def push(payload) -> bool:
    data = Schema(
        {
            "ref": str,
            "repository": {"name": str, str: object},
            str: object,
        }
    ).validate(payload)
    return data["ref"] != "refs/heads/master"
