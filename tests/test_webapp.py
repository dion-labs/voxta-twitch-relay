from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from voxta_twitch_relay.webapp import create_debug_app


@pytest.fixture
def mock_bot():
    bot = MagicMock()
    bot.gateway.is_connected = True
    bot.gateway.chat_active = True
    bot.stream_live = True
    bot.immediate_reply = True
    bot.relayed_history = [{"author": "user1", "text": "hello", "status": "relayed"}]
    bot.message_queue = [{"author": "user2", "text": "queued"}]
    return bot


@pytest.fixture
def client(mock_bot):
    app = create_debug_app(mock_bot)
    return TestClient(app)


def test_debug_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Twitch Relay Debug" in response.text
    assert "Gateway: Connected" in response.text
    assert "user1" in response.text
    assert "user2" in response.text


def test_api_status(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["gateway_connected"] is True
    assert data["queue_size"] == 1
    assert data["history"][0]["author"] == "user1"
