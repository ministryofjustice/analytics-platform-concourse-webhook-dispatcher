
def webhook_url(base, team, pipeline, resource, token):
    return f'{base}/api/v1/teams/{team}/pipelines/{pipeline}/resources/{resource}/check/webhook?webhook_token={token}'
