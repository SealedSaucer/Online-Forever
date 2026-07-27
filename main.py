# ==============================
#            Imports
# ==============================
import asyncio
import json
import requests
import websockets

# ==============================
#            Configs
# ==============================

# Key:
#    * = Default
#    ! = Required

TOKEN = "Add your token here"        # Your discord token. (! string)
STATUS = "online"                    # Set status type. (! "online", "dnd", "idle") (* "online")
CUSTOM_STATUS = "Hey!"               # Custom Status? To dissable leave blank. (* "Hey!")
USE_EMOJI = False                    # Use a emoji? (! True or False) (* False)

# ==============================
#            Headers
# ==============================

headers = {"Authorization": TOKEN}

# ==============================
#        Requests & Setup
# ==============================

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


# ==============================
#           Functions
# ==============================

async def discord_gateway():
    uri = "wss://gateway.discord.gg/?v=10&encoding=json"

    async with websockets.connect(uri) as ws:
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

while True:
    asyncio.run(discord_gateway())
    asyncio.sleep(5)
