import os
import sys
import json
import requests
import websockets
import asyncio
from colorama import init, Fore
from keep_alive import keep_alive

init(autoreset=True)

status = "online"  # online/dnd/idle
custom_status = "youtube.com/@SealedSaucer"  # Custom status

usertoken = os.getenv("TOKEN")
if not usertoken:
    print(Fore.LIGHTRED_EX + "[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print(Fore.LIGHTRED_EX + "[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

async def onliner(token, status):
    async with websockets.connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
        start = json.loads(await ws.recv())
        heartbeat = start["d"]["heartbeat_interval"]

        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "Windows 10",
                    "$browser": "Google Chrome",
                    "$device": "Windows",
                },
                "presence": {"status": status, "afk": False},
            },
        }
        await ws.send(json.dumps(auth))

        cstatus = {
            "op": 3,
            "d": {
                "since": 0,
                "activities": [
                    {
                        "type": 4,
                        "state": custom_status,
                        "name": "Custom Status",
                        "id": "custom",
                    }
                ],
                "status": status,
                "afk": False,
            },
        }
        await ws.send(json.dumps(cstatus))

        online = {"op": 1, "d": "None"}
        await asyncio.sleep(heartbeat / 1000)
        await ws.send(json.dumps(online))

async def run_onliner():
    os.system("cls")
    print(Fore.LIGHTGREEN_EX + f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        await onliner(usertoken, status)
        await asyncio.sleep(50)

keep_alive()
asyncio.run(run_onliner())