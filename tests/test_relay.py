from unittest.mock import AsyncMock, MagicMock

import pytest

from voxta_twitch_relay.bot import TwitchVoxtaRelay


@pytest.fixture
def mock_gateway_client():
    client = MagicMock()
    client.is_connected = True
    client.chat_active = True
    client.ai_state = "idle"
    client.health_check = AsyncMock(return_value={"status": "ok"})
    client.send_dialogue = AsyncMock()
    return client


@pytest.fixture
def bot(mock_gateway_client):
    return TwitchVoxtaRelay(
        gateway_client=mock_gateway_client,
        token="oauth:fake_token",
        client_id="fake_id",
        client_secret=None,
        prefix="!",
        initial_channels=["test_channel"],
        ignored_users=["Nightbot"],
        immediate_reply=True,
    )


@pytest.mark.asyncio
async def test_relay_message_active(bot, mock_gateway_client):
    msg_data = {"text": "Hello AI", "author": "user123"}
    await bot.relay_message(msg_data)

    mock_gateway_client.send_dialogue.assert_called_once_with(
        text="Hello AI", source="twitch", author="user123", immediate_reply=True
    )
    assert len(bot.relayed_history) == 1
    assert bot.relayed_history[0]["status"] == "relayed"


@pytest.mark.asyncio
async def test_process_queue(bot, mock_gateway_client):
    bot.message_queue = [{"text": "Queued msg", "author": "user1"}]
    await bot.process_queue()

    mock_gateway_client.send_dialogue.assert_called_once()
    assert len(bot.message_queue) == 0
    assert len(bot.relayed_history) == 1


def test_ignored_users(bot):
    assert "nightbot" in bot.ignored_users
    assert "Nightbot".lower() in bot.ignored_users
