# Online-Forever
Make your Discord Account 24/7 Online!

----

A code written in Python that helps you to keep your account 24/7 online.

The [main.py](https://github.com/SealedSaucer/Online-Forever/blob/main/main.py) is the main file. [keep_alive.py](https://github.com/SealedSaucer/Online-Forever/blob/main/keep_alive.py) prevents your repl from going to sleep. (If you have a replit hacker plan, then you can delete [this file](https://github.com/SealedSaucer/Online-Forever/blob/main/keep_alive.py) and paste this code inside the [main.py](https://github.com/SealedSaucer/Online-Forever/blob/main/main.py) file: 

</br>

```py
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=':', self_bot=True, help_command=None)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online)
  os.system('clear')
  print(f'Logged in as {client.user} (ID: {client.user.id})')

client.run(os.getenv("TOKEN"))
```

This code is from [this tutorial](https://youtu.be/yfgEbZAXMAQ). If you have any issues or doubts regarding this, feel free to [contact me](https://dsc.gg/phantom).

---

### DO NOT GIVE YOUR TOKEN TO OTHERS!

#### Giving your token to someone else will give them the ability to log into your account without the password or 2FA.

---

> ⭐ Feel free to Star the Repository if this helped you! ;)

----

> Online Forever by SealedSaucer is licensed under Attribution 4.0 International 
