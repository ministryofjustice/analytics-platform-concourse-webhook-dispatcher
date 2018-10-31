from schema import Schema


def release(payload) -> bool:
    data = Schema({
        'action': str,
        'release': {
            'prerelease': bool,
            str: object
        },
        'repository': {
            'name': str,
            str: object
        },
        str: object
    }).validate(payload)
    return data['action'] == 'published' and data['release']['prerelease'] == False
