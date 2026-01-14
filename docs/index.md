# Voxta Twitch Relay

Welcome to the Voxta Twitch Relay documentation.

Voxta Twitch Relay is a specialized bridge designed to connect Twitch chat with the Voxta conversational AI platform via the [Voxta Gateway](https://github.com/dion-labs/voxta-gateway).

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
