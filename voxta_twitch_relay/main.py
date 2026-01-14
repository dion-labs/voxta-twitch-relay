import asyncio
import contextlib
import logging
import os

import uvicorn
from dotenv import load_dotenv
from voxta_gateway.client import GatewayClient

from .bot import TwitchVoxtaRelay
from .webapp import create_debug_app


def main():
    load_dotenv()

    # --- CONFIGURATION ---
    twitch_token = os.getenv("TWITCH_TOKEN")
    twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
    twitch_client_secret = os.getenv("TWITCH_CLIENT_SECRET")
    twitch_channel = os.getenv("TWITCH_CHANNEL")
    twitch_prefix = os.getenv("TWITCH_PREFIX", "!")

    ignored_users_raw = os.getenv("IGNORED_USERS", "Nightbot,StreamElements").split(",")
    ignored_users = [u.strip().lower() for u in ignored_users_raw if u.strip()]

    gateway_url = os.getenv("GATEWAY_URL", "http://localhost:8081")
    immediate_reply = os.getenv("IMMEDIATE_REPLY", "true").lower() == "true"

    debug_host = os.getenv("DEBUG_HOST", "0.0.0.0")
    debug_port = int(os.getenv("DEBUG_PORT", "8082"))
    # ---------------------

    if not twitch_token or not twitch_channel or not twitch_client_id:
        print("\n[!] CONFIGURATION REQUIRED:")
        print("Set TWITCH_TOKEN, TWITCH_CLIENT_ID and TWITCH_CHANNEL in your .env or environment")
        return

    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # Reduce noise
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("twitchio").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger("Main")

    async def run_services():
        # Initialize Gateway Client
        gateway_client = GatewayClient(
            gateway_url=gateway_url,
            client_id="twitch-relay",
            events=["chat_started", "chat_closed", "ai_state_changed"],
            reconnect_delay=30.0,
        )

        # Initialize Twitch Bot
        bot = TwitchVoxtaRelay(
            gateway_client=gateway_client,
            token=twitch_token,
            client_id=twitch_client_id,
            client_secret=twitch_client_secret,
            prefix=twitch_prefix,
            initial_channels=[twitch_channel],
            ignored_users=ignored_users,
            immediate_reply=immediate_reply,
        )

        # Gateway event handlers
        @gateway_client.on("chat_started")
        async def on_chat_started(_data):
            logger.info("Voxta Chat Started! Flushing queue...")
            await bot.process_queue()

        @gateway_client.on("connected")
        async def on_connected(_data):
            logger.info("Connected to Voxta Gateway")
            if gateway_client.chat_active:
                await bot.process_queue()

        # Start Gateway client in background
        gateway_task = asyncio.create_task(gateway_client.start())

        # Start Debug Webapp
        debug_app = create_debug_app(bot)
        config = uvicorn.Config(debug_app, host=debug_host, port=debug_port, log_level="warning")
        server = uvicorn.Server(config)
        web_task = asyncio.create_task(server.serve())
        logger.info(f"Debug webapp started on http://{debug_host}:{debug_port}")

        # Start Twitch Bot
        try:
            await bot.start()
        except KeyboardInterrupt:
            logger.info("Exiting...")
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            await gateway_client.stop()
            gateway_task.cancel()
            web_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.gather(gateway_task, web_task, return_exceptions=True)

    asyncio.run(run_services())


if __name__ == "__main__":
    main()
