# Voxta Twitch Relay 🌉 By DionLabs

A lightweight, zero-latency bridge that connects Twitch Chat directly to your Voxta AI Server. This is the exact code powering the interactive AI characters on [Twitch.tv/D_Precated](https://twitch.tv/D_Precated).

Voxta Twitch Relay is a specialized bridge designed to connect Twitch chat with the Voxta conversational AI platform via the [Voxta Gateway](https://github.com/dion-labs/voxta-gateway).

## Features

🚀 **Event-Driven**: No polling. Chat is sent to your AI server instantly via high-speed WebSockets.

🛡️ **Bot Filtering**: Automatically ignores Nightbot, StreamElements, and your own bot account to keep your AI focused on the real conversation.

🔌 **Plug & Play**: Works with any standard Voxta installation when combined with the Voxta Gateway.

🧠 **Smart Queueing**: Automatically buffers and queues messages when your AI isn't in an active chat session, ensuring no viewer interaction is lost.

📊 **Debug Dashboard**: Real-time web interface at `localhost:8082` to monitor relay health, stream status, and message history.

## How it works

1.  **Listen**: The relay connects to your Twitch channel as a bot.
2.  **Filter**: It ignores messages from bots or users you specify.
3.  **Relay**: When a user sends a message, it's sent to the Voxta Gateway.
4.  **Queue**: If the AI isn't currently in a chat session, messages are queued and flushed once the chat starts.
5.  **Respond**: Voxta processes the message and can respond through your configured TTS or back to Twitch (if configured).

## Key Links

- [GitHub Repository](https://github.com/dion-labs/voxta-twitch-relay)
- [PyPI Package](https://pypi.org/project/voxta-twitch-relay/)
- [Voxta Client](https://voxta.dionlabs.ai)
- [Voxta Gateway](https://gateway.voxta.dionlabs.ai)
