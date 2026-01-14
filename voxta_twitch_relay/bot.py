import asyncio
import logging

from twitchio.ext import commands
from voxta_gateway.client import GatewayClient


class TwitchVoxtaRelay(commands.Bot):
    def __init__(
        self,
        gateway_client: GatewayClient,
        token: str,
        client_id: str,
        client_secret: str | None,
        prefix: str,
        initial_channels: list[str],
        ignored_users: list[str],
        immediate_reply: bool = True,
    ):
        super().__init__(
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            prefix=prefix,
            initial_channels=initial_channels,
        )
        self.gateway = gateway_client
        self.logger = logging.getLogger("TwitchRelay")
        self.message_queue: list[dict] = []
        self.relayed_history: list[dict] = []
        self.stream_live = False
        self.immediate_reply = immediate_reply
        self.ignored_users = [u.lower() for u in ignored_users]
        self.channel_name = initial_channels[0] if initial_channels else ""

    async def event_ready(self):
        self.logger.info(f"Logged in as | {self.nick}")
        print(f"\n--- Twitch Relay Logged In as {self.nick} ---")
        print(f"Relaying messages from channel: {self.channel_name}\n")

        # Start health and stream check loops
        asyncio.create_task(self.gateway_health_loop())
        asyncio.create_task(self.stream_check_loop())

    async def gateway_health_loop(self):
        """Check if the gateway is up, retry every 30s."""
        while True:
            try:
                if not self.gateway.is_connected:
                    self.logger.info("Attempting to connect to Voxta Gateway...")
                    health = await self.gateway.health_check()
                    self.logger.info(f"Gateway Health: {health}")
            except Exception as e:
                self.logger.warning(f"Gateway health check failed: {e}. Retrying in 30s...")

            await asyncio.sleep(30)

    async def stream_check_loop(self):
        """Check if the stream is live, retry every 1 minute."""
        while True:
            try:
                if self.channel_name:
                    streams = await self.fetch_streams(user_logins=[self.channel_name])
                    was_live = self.stream_live
                    self.stream_live = len(streams) > 0

                    if self.stream_live and not was_live:
                        self.logger.info(f"Stream is now LIVE on {self.channel_name}")
                    elif not self.stream_live and was_live:
                        self.logger.info(f"Stream went OFFLINE on {self.channel_name}")

            except Exception as e:
                self.logger.warning(f"Stream check failed: {e}")

            await asyncio.sleep(60)

    async def event_message(self, message):
        if message.echo:
            return

        if message.content.startswith(self._prefix):
            await self.handle_commands(message)
            return

        author_name = message.author.name.lower()
        if author_name in self.ignored_users:
            return

        self.logger.info(f"Twitch > {message.author.name}: {message.content}")

        msg_data = {
            "text": message.content,
            "author": message.author.name,
            "ts": asyncio.get_event_loop().time(),
        }

        if self.gateway.chat_active:
            await self.relay_message(msg_data)
        else:
            self.logger.info(f"Queueing message (chat not active): {message.content[:30]}...")
            self.message_queue.append(msg_data)

    async def relay_message(self, msg_data: dict):
        """Relay a message to the Voxta Gateway."""
        try:
            await self.gateway.send_dialogue(
                text=msg_data["text"],
                source="twitch",
                author=msg_data["author"],
                immediate_reply=self.immediate_reply,
            )
            self.logger.info(f"Relayed to Voxta: {msg_data['author']}: {msg_data['text'][:30]}...")

            # Track in history
            self.relayed_history.append(
                {**msg_data, "status": "relayed", "relayed_at": asyncio.get_event_loop().time()}
            )
            if len(self.relayed_history) > 100:
                self.relayed_history.pop(0)

        except Exception as e:
            self.logger.error(f"Failed to relay message: {e}")
            msg_data["error"] = str(e)
            self.message_queue.append(msg_data)

    async def process_queue(self):
        """Process queued messages when chat becomes active."""
        if not self.message_queue:
            return

        self.logger.info(f"Processing {len(self.message_queue)} queued messages...")
        queue_to_process = self.message_queue[:]
        self.message_queue.clear()

        for msg in queue_to_process:
            await self.relay_message(msg)

    @commands.command(name="voxta")
    async def voxta_status(self, ctx):
        """Check Voxta and Gateway status."""
        gw_status = "Connected" if self.gateway.is_connected else "Disconnected"
        chat_status = "Active" if self.gateway.chat_active else "Inactive"
        ai_state = self.gateway.ai_state
        status_msg = (
            f"Gateway: {gw_status} | Chat: {chat_status} | "
            f"AI State: {ai_state} | Stream Live: {self.stream_live}"
        )
        await ctx.send(status_msg)

    @commands.command(name="setreply")
    async def set_reply(self, ctx, value: str):
        """Set immediate_reply flag (true/false)."""
        if value.lower() in ["true", "on", "1"]:
            self.immediate_reply = True
            await ctx.send("Voxta immediate_reply set to True")
        else:
            self.immediate_reply = False
            await ctx.send("Voxta immediate_reply set to False")
