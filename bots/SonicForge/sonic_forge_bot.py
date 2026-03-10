import discord
from discord.ext import commands

# SonicForge: Academy Audio Engine
# (Template for Future Expansion)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!sonic_", intents=intents)

@bot.event
async def on_ready():
    print(f"SonicForge Online: {bot.user}")

if __name__ == "__main__":
    # bot.run("TOKEN")
    pass
