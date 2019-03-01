#!/usr/bin/env python

"""Tests for `analytics_platform_concourse_webhook_dispatcher` package."""
import os
import json
import re
from typing import MutableMapping
from unittest.mock import patch, Mock

import pytest


from analytics_platform_concourse_webhook_dispatcher.signature import make_digest

DIR = os.path.dirname(__file__)
CONCOURSE_BASE_URL_PATTERN = re.compile(r"https://httpbin\.org/.*$")


def sign(app, data):
    if data is None:
        data = b""
    if isinstance(data, MutableMapping):
        data = bytes(json.dumps(data), encoding="utf8")

    return make_digest(bytes(app.config.SECRET, encoding="utf8"), data)


@pytest.fixture
def app():
    from analytics_platform_concourse_webhook_dispatcher.server import app

    return app


def test_home(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.json == {}


def test_ping_unsigned(app):
    """
    test ping without signature, should fail
    """
    request, response = app.test_client.post(
        "/", headers={"X-Github-Event": "ping"})
    assert response.status == 400


def test_ping(app):
    digest = sign(app, None)

    request, response = app.test_client.post(
        "/", headers={"X-Github-Event": "ping", "X-Hub-Signature": digest}
    )
    assert response.status == 200
    assert response.json == {"msg": "pong"}


def test_implicit_ping(app):
    digest = sign(app, None)

    request, response = app.test_client.post(
        "/", headers={"X-Github-Event": "ping", "X-Hub-Signature": digest}
    )
    assert response.status == 200
    assert response.json == {"msg": "pong"}


mock_get_fly = Mock()
mock_login = Mock()
mock_run = Mock()


@patch("fly.Fly.get_fly", mock_get_fly)
@patch("fly.Fly.login", mock_login)
@patch("fly.Fly.run", mock_run)
def test_release_event(app):
    with open(f"{DIR}/data/release.json", "r") as f:
        data = json.load(f)
    digest = sign(app, data)
    request, response = app.test_client.post(
        "/", json=data, headers={"X-Github-Event": "release", "X-Hub-Signature": digest}
    )
    assert response.status == 204
    mock_get_fly.assert_called_once_with()
    mock_login.assert_called_once_with("", "", "main")
    mock_run.assert_called_once_with(
        "check-resource", 
        "--resource", 
        "Hello-World/release"
    )
