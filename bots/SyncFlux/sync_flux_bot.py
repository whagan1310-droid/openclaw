import discord
from discord.ext import commands

# SyncFlux: Academy Media Integration
# (Template for Future Expansion)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!sync_", intents=intents)

import os
from dotenv import load_dotenv
load_dotenv()

@bot.event
async def on_ready():
    print(f"SyncFlux Online: {bot.user}")

if __name__ == "__main__":
    token = os.getenv("SYNC_FLUX_TOKEN")
    if token:
        bot.run(token)
    else:
        print("SyncFlux: No SYNC_FLUX_TOKEN found. Standing by.")
        import time
        while True: time.sleep(3600)
