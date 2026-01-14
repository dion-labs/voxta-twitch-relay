import logging
import asyncio
import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from voxta_gateway.client import GatewayClient
from .bot import TwitchVoxtaRelay
from .webapp import create_debug_app

def main():
    load_dotenv()

    # --- CONFIGURATION ---
    TWITCH_TOKEN = os.getenv('TWITCH_TOKEN')
    TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
    TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
    TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')
    TWITCH_PREFIX = os.getenv('TWITCH_PREFIX', '!')
    
    IGNORED_USERS = os.getenv('IGNORED_USERS', 'Nightbot,StreamElements').split(',')
    IGNORED_USERS = [u.strip().lower() for u in IGNORED_USERS if u.strip()]

    GATEWAY_URL = os.getenv('GATEWAY_URL', "http://localhost:8081")
    IMMEDIATE_REPLY = os.getenv('IMMEDIATE_REPLY', 'true').lower() == 'true'
    
    DEBUG_HOST = os.getenv('DEBUG_HOST', "0.0.0.0")
    DEBUG_PORT = int(os.getenv('DEBUG_PORT', "8082"))
    # ---------------------

    if not TWITCH_TOKEN or not TWITCH_CHANNEL or not TWITCH_CLIENT_ID:
        print("\n[!] CONFIGURATION REQUIRED:")
        print("Set TWITCH_TOKEN, TWITCH_CLIENT_ID and TWITCH_CHANNEL in your .env or environment")
        return

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Reduce noise
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("twitchio").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger("Main")

    async def run_services():
        # Initialize Gateway Client
        gateway_client = GatewayClient(
            gateway_url=GATEWAY_URL,
            client_id="twitch-relay",
            events=["chat_started", "chat_closed", "ai_state_changed"],
            reconnect_delay=30.0
        )

        # Initialize Twitch Bot
        bot = TwitchVoxtaRelay(
            gateway_client=gateway_client,
            token=TWITCH_TOKEN,
            client_id=TWITCH_CLIENT_ID,
            client_secret=TWITCH_CLIENT_SECRET,
            prefix=TWITCH_PREFIX,
            initial_channels=[TWITCH_CHANNEL],
            ignored_users=IGNORED_USERS,
            immediate_reply=IMMEDIATE_REPLY
        )

        # Gateway event handlers
        @gateway_client.on("chat_started")
        async def on_chat_started(data):
            logger.info("Voxta Chat Started! Flushing queue...")
            await bot.process_queue()

        @gateway_client.on("connected")
        async def on_connected(data):
            logger.info("Connected to Voxta Gateway")
            if gateway_client.chat_active:
                await bot.process_queue()

        # Start Gateway client in background
        gateway_task = asyncio.create_task(gateway_client.start())

        # Start Debug Webapp
        debug_app = create_debug_app(bot)
        config = uvicorn.Config(debug_app, host=DEBUG_HOST, port=DEBUG_PORT, log_level="warning")
        server = uvicorn.Server(config)
        web_task = asyncio.create_task(server.serve())
        logger.info(f"Debug webapp started on http://{DEBUG_HOST}:{DEBUG_PORT}")

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
            try:
                await asyncio.gather(gateway_task, web_task, return_exceptions=True)
            except asyncio.CancelledError:
                pass

    asyncio.run(run_services())

if __name__ == "__main__":
    main()
