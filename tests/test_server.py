#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `analytics_platform_concourse_webhook_dispatcher` package."""
import os
import json
import re
from typing import MutableMapping

from aioresponses import aioresponses
import pytest


from analytics_platform_concourse_webhook_dispatcher.signature import make_digest

DIR = os.path.dirname(__file__)
CONCOURSE_BASE_URL_PATTERN = re.compile(r'https://httpbin\.org/.*$')


def sign(app, data):
    if data is None:
        data = b''
    if isinstance(data, MutableMapping):
        data = bytes(json.dumps(data), encoding='utf8')

    return make_digest(bytes(app.config.SECRET, encoding='utf8'), data)


@pytest.fixture
def app():
    from analytics_platform_concourse_webhook_dispatcher.server import app
    return app


@pytest.fixture
def mock_aioresponse():
    with aioresponses(passthrough=['http://127.0.0.1']) as m:
        yield m


def test_home(app):
    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.json == {}


def test_ping_unsigned(app):
    """
    test ping without signature, should fail
    """
    request, response = app.test_client.post(
        '/', headers={'X-Github-Event': 'ping'})
    assert response.status == 400


def test_ping(app):
    digest = sign(app, None)

    request, response = app.test_client.post(
        '/',
        headers={
            'X-Github-Event': 'ping',
            'X-Hub-Signature': digest
        }
    )
    assert response.status == 200
    assert response.json == {'msg': 'pong'}


def test_implicit_ping(app):
    digest = sign(app, None)

    request, response = app.test_client.post(
        '/',
        headers={
            'X-Github-Event': 'ping',
            'X-Hub-Signature': digest
        }
    )
    assert response.status == 200
    assert response.json == {'msg': 'pong'}


def test_release_event(app, mock_aioresponse):
    mock_aioresponse.post(CONCOURSE_BASE_URL_PATTERN, status=200)
    with open(f'{DIR}/data/release.json', 'r') as f:
        data = json.load(f)
    digest = sign(app, data)
    request, response = app.test_client.post(
        '/',
        json=data,
        headers={
            'X-Github-Event': 'release',
            'X-Hub-Signature': digest
        }
    )
    assert response.status == 204
    reqs = {k: v for k, v in mock_aioresponse.requests}
    assert len(reqs) == 1
    repo_name = data['repository']['name']
    req = reqs['POST']
    expected_path = f'/api/v1/teams/' \
                    f'{app.config.CONCOURSE_TEAM}' \
                    f'/pipelines/' \
                    f'{repo_name}' \
                    f'/resources/' \
                    f'{app.config.CONCOURSE_DEFAULT_RESOURCE}' \
                    f'/check/webhook?webhook_token=' \
                    f'{app.config.CONCOURSE_WEBHOOK_TOKEN}'
    assert expected_path == req.path_qs
    assert app.config.CONCOURSE_BASE_URL == f'{req.scheme}://{req.host}'
