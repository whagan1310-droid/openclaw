import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!sonic_", intents=intents)

music_queues = {}


@bot.event
async def on_ready():
    print("SonicForge Online:", bot.user)


@bot.command(name="play")
async def play(ctx, *, query: str):
    """Play music from YouTube"""
    if not ctx.author.voice:
        await ctx.send("❌ Join a voice channel first!")
        return
    
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.author.voice.channel.connect()
        voice_client = ctx.guild.voice_client
    
    await ctx.send(f"🎵 Search: {query} - Use YouTube link for best results!")


@bot.command(name="queue")
async def queue(ctx):
    """View music queue"""
    if ctx.guild.id not in music_queues or not music_queues[ctx.guild.id]:
        await ctx.send("📭 Queue is empty!")
    else:
        await ctx.send(f"📋 Queue: {len(music_queues[ctx.guild.id])} songs")


@bot.command(name="skip")
async def skip(ctx):
    """Skip song"""
    if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.stop()
        await ctx.send("⏭️ Skipped!")
    else:
        await ctx.send("❌ Nothing playing!")


@bot.command(name="stop")
async def stop(ctx):
    """Stop and disconnect"""
    if ctx.guild.voice_client:
        ctx.guild.voice_client.stop()
        await ctx.guild.voice_client.disconnect()
        if ctx.guild.id in music_queues:
            music_queues[ctx.guild.id] = []
        await ctx.send("⏹️ Stopped!")
    else:
        await ctx.send("❌ Not connected!")


@bot.command(name="pause")
async def pause(ctx):
    """Pause playback"""
    if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.pause()
        await ctx.send("⏸️ Paused!")
    else:
        await ctx.send("❌ Nothing playing!")


@bot.command(name="resume")
async def resume(ctx):
    """Resume playback"""
    if ctx.guild.voice_client and ctx.guild.voice_client.is_paused():
        ctx.guild.voice_client.resume()
        await ctx.send("▶️ Resumed!")
    else:
        await ctx.send("❌ Nothing paused!")


@bot.command(name="volume")
async def volume(ctx, vol: int):
    """Set volume 0-100"""
    if ctx.guild.voice_client:
        ctx.guild.voice_client.source.volume = vol / 100
        await ctx.send(f"🔊 Volume: {vol}%")
    else:
        await ctx.send("❌ Not playing!")


@bot.command(name="nowplaying")
async def nowplaying(ctx):
    """Current song"""
    await ctx.send("🎵 Use !sonic_play with YouTube URL")


@bot.command(name="h")
async def h(ctx):
    embed = discord.Embed(title="🎵 SonicForge Commands", color=discord.Color.blue())
    embed.add_field(name="!sonic_play [song]", value="Search/play music", inline=False)
    embed.add_field(name="!sonic_queue", value="View queue", inline=False)
    embed.add_field(name="!sonic_skip", value="Skip song", inline=False)
    embed.add_field(name="!sonic_stop", value="Stop & disconnect", inline=False)
    embed.add_field(name="!sonic_pause", value="Pause", inline=False)
    embed.add_field(name="!sonic_resume", value="Resume", inline=False)
    embed.add_field(name="!sonic_volume [0-100]", value="Set volume", inline=False)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    token = os.getenv("SONIC_FORGE_TOKEN")
    if token:
        bot.run(token)
    else:
        print("❌ SONIC_FORGE_TOKEN not found")
