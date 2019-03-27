from . import checks


def should_trigger(event, payload):
    try:
        return getattr(checks, event)(payload)
    except AttributeError:
        return False


def resource_for_event(app, event):
    return {
        'release': 'release',
        'push': 'pull-request'
    }.get(event, app.config.CONCOURSE_DEFAULT_RESOURCE)


def get(app, event, payload):
    if should_trigger(event, payload):
        return {
            'team': app.config.CONCOURSE_TEAM,
            'pipeline': payload['repository']['name'],
            'resource': resource_for_event(app, event)
        }
