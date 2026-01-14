# Voxta Twitch Relay 🌉 By DionLabs (Creators of D_Precated)

[![Build Status](https://github.com/dion-labs/voxta-twitch-relay/actions/workflows/ci.yml/badge.svg)](https://github.com/dion-labs/voxta-twitch-relay/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dion-labs/voxta-twitch-relay/branch/main/graph/badge.svg)](https://codecov.io/gh/dion-labs/voxta-twitch-relay)
[![PyPI version](https://badge.fury.io/py/voxta-twitch-relay.svg)](https://badge.fury.io/py/voxta-twitch-relay)
[![Python versions](https://img.shields.io/pypi/pyversions/voxta-twitch-relay.svg)](https://pypi.org/project/voxta-twitch-relay/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A lightweight, zero-latency bridge that connects Twitch Chat directly to your Voxta AI Server. This is the exact code powering the interactive AI characters on [Twitch.tv/D_Precated](https://twitch.tv/D_Precated).

> **Note**: This app is designed to work exclusively with the [Voxta Gateway](https://github.com/dion-labs/voxta-gateway), which provides the necessary semantic orchestration for high-performance streaming applications.

## Features

🚀 **Event-Driven**: No polling. Chat is sent to your AI server instantly via high-speed WebSockets.

🛡️ **Bot Filtering**: Automatically ignores Nightbot, StreamElements, and your own bot account to keep your AI focused on the real conversation.

🔌 **Plug & Play**: Works with any standard Voxta installation when combined with the Voxta Gateway.

🧠 **Smart Queueing**: Automatically buffers and queues messages when your AI isn't in an active chat session, ensuring no viewer interaction is lost.

📊 **Debug Dashboard**: Real-time web interface at `localhost:8082` to monitor relay health, stream status, and message history.

## Installation

```bash
pip install voxta-twitch-relay
```

## Quick Start

1. Create a `.env` file with your credentials:

```env
# Twitch Credentials
TWITCH_TOKEN=oauth:your_token_here
TWITCH_CLIENT_ID=your_client_id
TWITCH_CHANNEL=your_channel_name

# Gateway Settings
GATEWAY_URL=http://localhost:8081
```

2. Run the relay:

```bash
voxta-twitch-relay
```

3. Access the debug dashboard at `http://localhost:8082`.

## Documentation

For full documentation including advanced configuration and API reference, visit [twitch.voxta.dionlabs.ai](https://twitch.voxta.dionlabs.ai).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
