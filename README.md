<div id="SealedSaucer" align="center">
    <h1>Online Forever</h1>
    <p>Make Your Discord Account 24/7 Online!</p>
    <a href="https://github.com/SealedSaucer/Online-Forever/blob/main/LICENSE"><img src="https://img.shields.io/github/license/SealedSaucer/Online-Forever?style=for-the-badge"></a>
    <a href="https://sealedsaucer.sell.app"><img src="https://img.shields.io/badge/SHOP-CLICK HERE-5e40e4?style=for-the-badge"></a>
    <a href="https://phantom.fr.to/verify"><img src="https://img.shields.io/badge/contact-click me-05babf?style=for-the-badge"></a>
    <br>
    <img src="https://i.imgur.com/N61T21L.png" height="210">
</div>

---

<p align="center">
If you want to online tokens in bulk, consider checking out my store: <b><a href="https://sealedsaucer.sell.app">click here</a></b>! ☄️
<br>
⭐ Feel free to star the repository if this helped you!
</p>

## Disclaimer
By using this code, you are automating your Discord Account. This is against Discord's Terms of Service and Community Guidelines. If not used properly, your account(s) might get suspended or terminated by Discord. I, the developer, am not responsible for any consequences that may arise from the use of this code. Use this software at your own risk and responsibility. Learn more about <a href="https://discord.com/terms">Discord's Terms of Service</a> and <a href="https://discord.com/guidelines">Community Guidelines</a>.
#### This repository is in no way affiliated with, authorized, maintained, sponsored, or endorsed by Discord Inc. (discord.com) or any of its affiliates or subsidiaries.

## Warning
**DO <ins>NOT</ins> GIVE YOUR DISCORD TOKENS TO ANYONE.**
#### Giving your token to someone else will give them the ability to log into your account without the password or 2FA.

## Features
- Secure [🔒]
- Supports Custom Status
- Account will stay 24/7 online (if you set it up correctly)
- Supports all three status modes (Online, Idle, Do Not Disturb)
- Can be used almost on any platform that supports [Python](https://python.org)

## Obtaining Your Token ([Video Guide](https://www.youtube.com/watch?v=sYGdDLLu8cU))
You will need an user token inorder to use this code. You can obtain it by doing the following:
1. Logging in to your discord account
2. Pressing `Ctrl+Shift+I` to open Chrome Developer Tools
3. Go to the `Network` Tab
4. Keep it open and refresh the page
5. Type `/api` in the filter search box
6. Click the entry that has `science` as the `Name`
7. On the sub-menu, go to `Headers`
8. Scroll down till you see an entry named `Authorization`. Copy the line next to it.
9. This is your token, <ins>**DO NOT GIVE IT TO ANYONE**</ins>.

<p align="center">
  <img height="10px" width="10000px" src="https://i.imgur.com/w6MUcN8.png"/>
</p>

## 🛠️ Installation
### · Replit
#### The code inside the repository was originally made to be hostable on [Replit](https://replit.com), but due to a recent ban on all repositories that are against Discord's ToS, you won't be able to import this repository directly to Replit anymore.
#### Here's a workaround to solve that issue:
1. Click [here](https://github.com/SealedSaucer/Online-Forever/archive/refs/heads/main.zip) to download the latest version of this code.
2. Unzip the file
3. Create a new Python repl on [Replit](https://replit.com)
4. Upload the files into the repl (Just drag and drop it into the files sidebar)
5. Overwrite the files if a prompt pops-up
6. Add your token inside Secrets ([Guide](https://docs.replit.com/programming-ide/workspace-features/storing-sensitive-information-environment-variables)) with `TOKEN` as the key and your token as the value ([Video](https://youtu.be/sYGdDLLu8cU))
7. Modify both the status mode and custom status, if you want to make any adjustments
8. Run the repl
9. Add your repl url to an uptime monitor ([Video](https://youtu.be/dVIjpCqnZXE))

### · Docker

This repository includes a `Dockerfile` and a `docker-compose.yml` file. Since pre-built images are not available, you'll need to build them yourself.

### · Local Installation
1. Install [Python](https://python.org/downloads) on your machine (Make sure you add it to [PATH](https://i.imgur.com/Ukl6HdQ.png))
2. Copy the code below
<details>
<summary> Click here to view the code, and click again to close it</summary>
<br>

```py
import sys
import json
import time
import requests
import websocket

status = "online"

custom_status = "youtube.com/@SealedSaucer" #If you don't need a custom status on your profile, just put "" instead of "youtube.com/@SealedSaucer"

usertoken = "Add your token here"

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
  print("[ERROR] Your token might be invalid. Please check it again.")
  sys.exit()

userinfo = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
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
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
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
                    #Uncomment the below lines if you want an emoji in the status
                    #"emoji": {
                        #"name": "emoji name",
                        #"id": "emoji id",
                        #"animated": False,
                    #},
                }
            ],
            "status": status,
            "afk": False,
        },
    }
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": "None"}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))

def run_onliner():
  print(f"Logged in as {username}#{discriminator} ({userid}).")
  while True:
    onliner(usertoken, status)
    time.sleep(50)

run_onliner()

```
</details>

3. Create a new Python file and paste the code into it
4. Modify both the status mode and custom status, if you want to make any adjustments
5. Save the file
6. Create a `requirements.txt` file and copy and paste the file contents inside [requirements.txt](https://github.com/SealedSaucer/Online-Forever/blob/main/requirements.txt) without the `Flask` module
7. Save the file
8. Open command prompt where both the files are present and run `pip install -r requirements.txt`
9. Once the packages are downloaded, either double-click the python file in order to run it or open command prompt where the python file is present and run `python filename.py`

<p align="center">
  <img height="10px" width="10000px" src="https://i.imgur.com/w6MUcN8.png"/>
</p>

## 🔧 Known Errors And Fixes
### [Discord] Status is not changing

> Just wait for a few minutes. It takes some time for Discord to refresh your status.

### [Replit] This repository could not be accessed, try again later/This repository possibly violates our Terms of Service. Contact support if you believe this is a mistake.

> As I mentioned before, due to a recent ban on all repositories that are against Discord's ToS, you won't be able to import this repository directly to Replit anymore. Follow <a href="https://github.com/SealedSaucer/Online-Forever#heres-a-workaround-to-solve-that-issue">this</a> workaround to host the code on Replit.

### [Replit] sh: line 1: python3: command not found

> You cloned it into a bash repl. Make sure you select "Python" from the languages list when you create the repl.

### [Replit] Cloudflare Error/Temporarily banned from accessing Discord's API

> This happens because repls have Shared Public IP Addresses, and some Replit Users abuse the platform to spam (through self bots or nukers). Whenever Discord sees lots of invalid requests coming from a single IP address, it will use Cloudflare to temporarily block any incoming requests.

> Fix:
> - Go to shell
> - Enter <code>kill 1</code>
> - Wait for the repl to reload
> - Run the repl again

<p align="center">
  <img height="10px" width="10000px" src="https://i.imgur.com/w6MUcN8.png"/>
</p>

## 🛟 Help and Support
If you have any issues or doubts regarding this, feel free to [contact me](https://phantom.fr.to/verify).

---

<p align="center">Online Forever is licensed under GNU General Public License ❤️</p>
