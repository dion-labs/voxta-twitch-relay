from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .bot import TwitchVoxtaRelay

def create_debug_app(bot: TwitchVoxtaRelay):
    app = FastAPI(title="Twitch Relay Debug")

    @app.get("/", response_class=HTMLResponse)
    async def index():
        status_color = "green" if bot.gateway.is_connected else "red"
        chat_color = "green" if bot.gateway.chat_active else "orange"
        stream_color = "green" if bot.stream_live else "gray"
        
        history_html = "".join([
            f"<li><b>{msg['author']}:</b> {msg['text']} <small>({msg['status']})</small></li>"
            for msg in reversed(bot.relayed_history)
        ])
        
        queue_html = "".join([
            f"<li><b>{msg['author']}:</b> {msg['text']}</li>"
            for msg in bot.message_queue
        ])

        html = f"""
        <html>
            <head>
                <title>Twitch Relay Debug</title>
                <style>
                    body {{ font-family: sans-serif; margin: 20px; line-height: 1.6; background: #121212; color: #e0e0e0; }}
                    .card {{ background: #1e1e1e; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); margin-bottom: 20px; border: 1px solid #333; }}
                    .status {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 5px; }}
                    .green {{ background: #4caf50; box-shadow: 0 0 8px #4caf50; }}
                    .red {{ background: #f44336; box-shadow: 0 0 8px #f44336; }}
                    .orange {{ background: #ff9800; box-shadow: 0 0 8px #ff9800; }}
                    .gray {{ background: #9e9e9e; box-shadow: 0 0 8px #9e9e9e; }}
                    h1 {{ color: #ffffff; }}
                    h2 {{ margin-top: 0; color: #bb86fc; border-bottom: 1px solid #333; padding-bottom: 10px; }}
                    ul {{ list-style: none; padding: 0; }}
                    li {{ padding: 10px; border-bottom: 1px solid #333; }}
                    li:last-child {{ border-bottom: none; }}
                    b {{ color: #03dac6; }}
                    small {{ color: #999; margin-left: 10px; }}
                </style>
                <meta http-equiv="refresh" content="5">
            </head>
            <body>
                <h1>Twitch Relay Debug</h1>
                <div class="card">
                    <h2>System Status</h2>
                    <p><span class="status {status_color}"></span> Gateway: {"Connected" if bot.gateway.is_connected else "Disconnected"}</p>
                    <p><span class="status {chat_color}"></span> Active Chat: {"Yes" if bot.gateway.chat_active else "No"}</p>
                    <p><span class="status {stream_color}"></span> Stream Live: {"Yes" if bot.stream_live else "No"}</p>
                    <p>Immediate Reply: {bot.immediate_reply}</p>
                </div>
                
                <div class="card">
                    <h2>Message Queue ({len(bot.message_queue)})</h2>
                    <ul>{queue_html or "<li>Queue is empty</li>"}</ul>
                </div>

                <div class="card">
                    <h2>Relayed History (Last 100)</h2>
                    <ul>{history_html or "<li>No history yet</li>"}</ul>
                </div>
            </body>
        </html>
        """
        return html

    @app.get("/api/status")
    async def get_status():
        return {
            "gateway_connected": bot.gateway.is_connected,
            "chat_active": bot.gateway.chat_active,
            "stream_live": bot.stream_live,
            "immediate_reply": bot.immediate_reply,
            "queue_size": len(bot.message_queue),
            "queue": bot.message_queue,
            "history": bot.relayed_history
        }
        
    return app
