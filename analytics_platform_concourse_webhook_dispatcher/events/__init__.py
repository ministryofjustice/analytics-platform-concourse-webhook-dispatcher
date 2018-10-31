from . import checks

def should_trigger(event, payload):
    try:
       return getattr(checks, event)(payload)
    except AttributeError:
        return False

def get(app, event, payload):
    if should_trigger(event, payload):
        return {
            'team': app.config.CONCOURSE_TEAM,
            'pipeline': payload['repository']['name'],
            'resource': app.config.CONCOURSE_DEFAULT_RESOURCE
        }
