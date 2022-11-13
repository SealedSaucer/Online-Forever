# Online-Forever
Make Your Discord Account 24/7 Online!

----

A code written in Python that helps you to keep your account 24/7 online.

#### Please check out this if you want to add multiple tokens with just one file: [sealedsaucer.sellix.io/product/635d5774050c1](https://sealedsaucer.sellix.io/product/635d5774050c1)

---

The [main.py](https://github.com/SealedSaucer/Online-Forever/blob/main/main.py) is the main file. [keep_alive.py](https://github.com/SealedSaucer/Online-Forever/blob/main/keep_alive.py) prevents your repl from going to sleep. (If you have a replit hacker plan or want to run the script locally, then you can delete [this file](https://github.com/SealedSaucer/Online-Forever/blob/main/keep_alive.py) and paste this code inside the [main.py](https://github.com/SealedSaucer/Online-Forever/blob/main/main.py) file: 

</br>

```py
import json
import time
import websocket
import requests
import os

status = "online"

headers = {"Authorization": os.getenv("TOKEN"), "Content-Type": "application/json"}
userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {"op": 2,"d": {"token": token,"properties": {"$os": "Windows 10","$browser": "Google Chrome","$device": "Windows"},"presence": {"status": status,"afk": False}},"s": None,"t": None}
    ws.send(json.dumps(auth))
    online = {"op":1,"d":"None"}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))

def run_onliner():
  print(f"Logged in as {username}#{discriminator} ({userid}).")
  while True:
    onliner(os.getenv("TOKEN"), status)
    time.sleep(30)

run_onliner()
```

This code is from [this tutorial](https://www.youtube.com/watch?v=-soq0pOqP_4). If you have any issues or doubts regarding this, feel free to [contact me](https://dsc.gg/phantom).

---

### DO NOT GIVE YOUR TOKEN TO OTHERS!

#### Giving your token to someone else will give them the ability to log into your account without the password or 2FA.

---

> ⭐ Feel free to Star the Repository if this helped you! ;)

----

> Online Forever by SealedSaucer is licensed under Attribution 4.0 International 
