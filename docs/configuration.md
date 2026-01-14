# Configuration

Voxta Twitch Relay is configured primarily through environment variables.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TWITCH_TOKEN` | Twitch OAuth token (starts with `oauth:`) | **Required** |
| `TWITCH_CLIENT_ID` | Twitch Application Client ID | **Required** |
| `TWITCH_CLIENT_SECRET` | Twitch Application Client Secret | Optional |
| `TWITCH_CHANNEL` | The Twitch channel to monitor | **Required** |
| `TWITCH_PREFIX` | Command prefix for the bot | `!` |
| `IGNORED_USERS` | Comma-separated list of users to ignore | `Nightbot,StreamElements` |
| `GATEWAY_URL` | URL of the Voxta Gateway | `http://localhost:8081` |
| `IMMEDIATE_REPLY` | Whether to request an immediate AI reply | `true` |
| `DEBUG_HOST` | Host for the debug web interface | `0.0.0.0` |
| `DEBUG_PORT` | Port for the debug web interface | `8082` |

## Twitch Commands

The bot supports the following commands in Twitch chat (for moderators):

- `!voxta`: Displays the current status of the Gateway, AI, and Stream.
- `!setreply <true|false>`: Dynamically toggles the `immediate_reply` flag.
