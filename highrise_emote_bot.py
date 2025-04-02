import asyncio
import websockets
import json
import os

# Fetch bot token and room ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ROOM_ID = os.getenv("ROOM_ID")

# WebSocket URL for Highrise
HIGHRISE_WS_URL = "wss://highrise.game/ws"

async def send_emote(websocket, emote_name):
    """Send an emote command to Highrise."""
    command = {
        "action": "perform_emote",
        "emote": emote_name
    }
    await websocket.send(json.dumps(command))
    print(f"Performed emote: {emote_name}")

async def bot_logic():
    """Main bot logic to connect and send emotes periodically."""
    async with websockets.connect(HIGHRISE_WS_URL) as websocket:
        # Authenticate the bot
        auth_payload = {
            "action": "authenticate",
            "token": BOT_TOKEN,
            "room": ROOM_ID
        }
        await websocket.send(json.dumps(auth_payload))
        print("✅ Bot Authenticated Successfully!")

        emotes = ["wave", "dance", "clap", "laugh"]  # Add more emotes if needed

        while True:
            for emote in emotes:
                await send_emote(websocket, emote)
                await asyncio.sleep(10)  # Wait 10 seconds before the next emote

async def main():
    """Keep the bot running 24/7, reconnect if disconnected."""
    while True:
        try:
            await bot_logic()
        except Exception as e:
            print(f"❌ Error: {e}, reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # Wait before reconnecting

# Run the bot
asyncio.run(main())
