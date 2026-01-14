# Voxta Twitch Relay

[![Build Status](https://github.com/dion-labs/voxta-twitch-relay/actions/workflows/ci.yml/badge.svg)](https://github.com/dion-labs/voxta-twitch-relay/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/voxta-twitch-relay.svg)](https://badge.fury.io/py/voxta-twitch-relay)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A bridge between Twitch chat and the Voxta conversational AI platform. This relay captures Twitch messages and sends them to the [Voxta Gateway](https://github.com/dion-labs/voxta-gateway), allowing your AI to interact with your live audience in real-time.

## Features

- **Seamless Integration**: Relays messages to Voxta Gateway with minimal latency.
- **Smart Queueing**: Automatically queues messages when the AI is not in an active chat session.
- **Bot Filtering**: Easily ignore common bots like Nightbot and StreamElements.
- **Debug Interface**: Built-in web dashboard to monitor relay status and message history.
- **Custom Commands**: Built-in `!voxta` and `!setreply` commands for channel moderators.

## Installation

```bash
pip install voxta-twitch-relay
```

## Quick Start

1. Create a `.env` file with your credentials:

```env
TWITCH_TOKEN=oauth:your_token_here
TWITCH_CLIENT_ID=your_client_id
TWITCH_CHANNEL=your_channel_name
GATEWAY_URL=http://localhost:8081
```

2. Run the relay:

```bash
voxta-twitch-relay
```

3. Access the debug dashboard at `http://localhost:8082`.

## Documentation

For full documentation, visit [twitch.voxta.dionlabs.ai](https://twitch.voxta.dionlabs.ai).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
