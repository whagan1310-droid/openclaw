import discord
from discord.ext import commands

# SonicForge: Academy Audio Engine
# (Template for Future Expansion)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!sonic_", intents=intents)

import os
from dotenv import load_dotenv
load_dotenv()

@bot.event
async def on_ready():
    print(f"SonicForge Online: {bot.user}")

if __name__ == "__main__":
    token = os.getenv("SONIC_FORGE_TOKEN")
    if token:
        bot.run(token)
    else:
        print("SonicForge: No SONIC_FORGE_TOKEN found. Standing by.")
        import time
        while True: time.sleep(3600)
