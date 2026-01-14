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
    # We mock fetch_streams on the bot instance later
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
async def test_relay_message_error(bot, mock_gateway_client):
    mock_gateway_client.send_dialogue.side_effect = Exception("Gateway error")
    msg_data = {"text": "Hello AI", "author": "user123"}
    await bot.relay_message(msg_data)

    assert len(bot.message_queue) == 1
    assert bot.message_queue[0]["error"] == "Gateway error"


@pytest.mark.asyncio
async def test_process_queue(bot, mock_gateway_client):
    bot.message_queue = [{"text": "Queued msg", "author": "user1"}]
    await bot.process_queue()

    mock_gateway_client.send_dialogue.assert_called_once()
    assert len(bot.message_queue) == 0
    assert len(bot.relayed_history) == 1


@pytest.mark.asyncio
async def test_event_message_ignored(bot, mock_gateway_client):
    message = MagicMock()
    message.echo = False
    message.content = "Hello"
    message.author.name = "Nightbot"

    await bot.event_message(message)
    mock_gateway_client.send_dialogue.assert_not_called()


@pytest.mark.asyncio
async def test_event_message_relay(bot, mock_gateway_client):
    message = MagicMock()
    message.echo = False
    message.content = "Hello AI"
    message.author.name = "user123"

    await bot.event_message(message)
    mock_gateway_client.send_dialogue.assert_called_once()


@pytest.mark.asyncio
async def test_event_message_queue(bot, mock_gateway_client):
    mock_gateway_client.chat_active = False
    message = MagicMock()
    message.echo = False
    message.content = "Hello AI"
    message.author.name = "user123"

    await bot.event_message(message)
    mock_gateway_client.send_dialogue.assert_not_called()
    assert len(bot.message_queue) == 1


def test_ignored_users(bot):
    assert "nightbot" in bot.ignored_users
    assert "Nightbot".lower() in bot.ignored_users


@pytest.mark.asyncio
async def test_voxta_status_command(bot):
    ctx = MagicMock()
    ctx.send = AsyncMock()
    # Call the underlying callback instead of the Command object
    await bot.voxta_status._callback(bot, ctx)
    ctx.send.assert_called_once()
    assert "Gateway: Connected" in ctx.send.call_args[0][0]


@pytest.mark.asyncio
async def test_set_reply_command(bot):
    ctx = MagicMock()
    ctx.send = AsyncMock()

    # Call the underlying callback
    await bot.set_reply._callback(bot, ctx, "false")
    assert bot.immediate_reply is False
    ctx.send.assert_called_with("Voxta immediate_reply set to False")

    await bot.set_reply._callback(bot, ctx, "true")
    assert bot.immediate_reply is True
    ctx.send.assert_called_with("Voxta immediate_reply set to True")
