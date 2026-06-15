import asyncio
import json
import os
import requests
import websockets

TOKEN = os.getenv("DISCORD_TOKEN")
STATUS = os.getenv("STATUS", "dnd")  # online / dnd / idle
CUSTOM_STATUS = os.getenv("CUSTOM_STATUS", "✅ 1.5$ Rust, cheatvault.net")  # Leave empty if you don't want a custom status
USE_EMOJI = os.getenv("USE_EMOJI", "false").lower() == "true"

if not TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable is not set!")
    print("Please set your Discord token as an environment variable.")
    exit()

headers = {"Authorization": TOKEN}

r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
if r.status_code != 200:
    print("Invalid token!")
    exit()

user = r.json()
print(f"Logged in as {user['username']} ({user['id']})!")

activity = {
    "name": "Custom Status",
    "type": 4,
    "state": CUSTOM_STATUS,
    "id": "custom"
}

if USE_EMOJI:
    activity["emoji"] = {
        "name": "🔥",   # Unicode emoji or emoji name
        "id": None,     # Required only for custom emojis
        "animated": False
    }

async def discord_gateway():
    uri = "wss://gateway.discord.gg/?v=10&encoding=json"

    async with websockets.connect(uri, max_size=10 * 1024 * 1024) as ws:  # 10MB limit
        hello = json.loads(await ws.recv())
        heartbeat_interval = hello["d"]["heartbeat_interval"]

        async def heartbeat():
            while True:
                await asyncio.sleep(heartbeat_interval / 1000)
                await ws.send(json.dumps({"op": 1, "d": None}))

        asyncio.create_task(heartbeat())

        identify = {
            "op": 2,
            "d": {
                "token": TOKEN,
                "properties": {
                    "$os": "windows",
                    "$browser": "chrome",
                    "$device": "pc"
                },
                "presence": {
                    "status": STATUS,
                    "afk": False,
                    "activities": [activity]
                }
            }
        }
        await ws.send(json.dumps(identify))

        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)

                if data.get("op") == 11:
                    pass

            except Exception as e:
                print("Connection lost, reconnecting...", e)
                break

async def main():
    while True:
        await discord_gateway()
        await asyncio.sleep(5)

asyncio.run(main())
