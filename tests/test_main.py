import os
from unittest.mock import patch, MagicMock
from voxta_twitch_relay.main import main

@patch("voxta_twitch_relay.main.os.getenv")
@patch("voxta_twitch_relay.main.TwitchVoxtaRelay")
@patch("voxta_twitch_relay.main.GatewayClient")
@patch("voxta_twitch_relay.main.uvicorn.Server.serve")
@patch("voxta_twitch_relay.main.asyncio.run")
def test_main_startup(mock_run, mock_serve, mock_gateway, mock_bot, mock_getenv):
    # Setup mock env vars
    mock_getenv.side_effect = lambda k, default=None: {
        "TWITCH_TOKEN": "fake_token",
        "TWITCH_CLIENT_ID": "fake_id",
        "TWITCH_CHANNEL": "fake_channel",
    }.get(k, default)
    
    # Run main
    main()
    
    # Verify asyncio.run was called
    mock_run.assert_called_once()

@patch("voxta_twitch_relay.main.os.getenv")
def test_main_missing_config(mock_getenv):
    mock_getenv.return_value = None
    
    with patch("builtins.print") as mock_print:
        main()
        mock_print.assert_any_call("\n[!] CONFIGURATION REQUIRED:")
