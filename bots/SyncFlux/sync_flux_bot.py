import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!sync_", intents=intents)

video_queue = {}


@bot.event
async def on_ready():
    print("SyncFlux Online:", bot.user)


@bot.command(name="video")
async def video(ctx, *, url: str):
    """Queue a video for sync"""
    if ctx.guild.id not in video_queue:
        video_queue[ctx.guild.id] = []
    video_queue[ctx.guild.id].append(url)
    await ctx.send(f"📺 Video queued: {url}")


@bot.command(name="status")
async def status(ctx):
    """Check pipeline status"""
    q = video_queue.get(ctx.guild.id, [])
    await ctx.send(f"📊 Pipeline Status: {len(q)} videos in queue")


@bot.command(name="queue")
async def queue(ctx):
    """View video queue"""
    q = video_queue.get(ctx.guild.id, [])
    if q:
        await ctx.send("📺 Queue:\n" + "\n".join(q[:5]))
    else:
        await ctx.send("📭 Queue empty")


@bot.command(name="clear")
async def clear(ctx):
    """Clear video queue"""
    video_queue[ctx.guild.id] = []
    await ctx.send("🗑️ Queue cleared")


@bot.command(name="h")
async def h(ctx):
    embed = discord.Embed(title="🎥 SyncFlux Commands", color=discord.Color.blue())
    embed.add_field(name="!sync_video [url]", value="Queue video", inline=False)
    embed.add_field(name="!sync_queue", value="View queue", inline=False)
    embed.add_field(name="!sync_status", value="Pipeline status", inline=False)
    embed.add_field(name="!sync_clear", value="Clear queue", inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    token = os.getenv("SYNC_FLUX_TOKEN")
    if token:
        bot.run(token)
    else:
        print("SyncFlux: No SYNC_FLUX_TOKEN found")
