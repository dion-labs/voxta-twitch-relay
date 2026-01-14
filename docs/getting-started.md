# Getting Started

## Prerequisites

- Python 3.10 or higher.
- A Twitch account and an OAuth token (get one at [twitchapps.com/tmi](https://twitchapps.com/tmi/)).
- A Twitch Client ID (register an app at [dev.twitch.tv](https://dev.twitch.tv/console)).
- [Voxta Gateway](https://github.com/dion-labs/voxta-gateway) running and accessible.

## Installation

Install the package via pip:

```bash
pip install voxta-twitch-relay
```

## Basic Configuration

Create a `.env` file in your project directory:

```env
# Twitch Credentials
TWITCH_TOKEN=oauth:xxxxxxxxxxxxxxxxxxxxxx
TWITCH_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxx
TWITCH_CHANNEL=your_channel_name

# Gateway Settings
GATEWAY_URL=http://localhost:8081
IMMEDIATE_REPLY=true
```

## Running the Relay

Simply run the command:

```bash
voxta-twitch-relay
```

The relay will log into Twitch and start listening for messages. You can monitor the status at `http://localhost:8082`.
