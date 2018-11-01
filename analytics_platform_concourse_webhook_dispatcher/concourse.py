# Concourse specific functionality


def webhook_url(base, team, pipeline, resource, token):
    """
    Given a base url, a team, pipeline name, resource and webhook token
    :return: the correct url to POST to to trigger a check
    """
    return f"{base}/api/v1/teams/{team}/pipelines/{pipeline}/resources/{resource}/check/webhook?webhook_token={token}"
