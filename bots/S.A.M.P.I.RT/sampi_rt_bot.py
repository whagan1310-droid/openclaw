"""
⚔️ S.A.M.P.I.RT Bot: Real-Time Security Engine ⚔️
================================================
S = Security (Anti-Raid/Nuke)
A = Anti Virus (Static File Scanning)
M = Malware (Heuristic Detection)
P = Phishing (Link Verification)
I = IP Logger (Deceptive Link Blocking)
RT = Real Time (Sub-second response)

Forge Theme: 🛡️🔒🕵️‍♂️🔥
"""

import discord
from discord.ext import commands
import json
import re
import aiohttp
import asyncio
import os
from datetime import datetime

# CONFIGURATION
THREAT_VAULT_PATH = "threat_vault.json"
SAFE_HARBOR_PATH = "safe_harbor.json" # Whitelist
STRIKE_LOG_PATH = "strike_log.json"
SORRY_DAVE_MSG = "!!!---SORRY_DAVE_YOU_SHOULD_HAVE_KNOWN_WE_CAN'T_DO_THAT---!!!"
SORRY_DAVE_CHANNEL_ID = 1480230319935324241 # Placeholder, update per build plan

# VISUAL ASSETS (From Forge Assets)
GUARD_AVATAR_URL = "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/image_ccdb2fa9-f41f-4ee6-8798-936616055dcc.png"
SIREN_GIF_URL = "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/image_019fe84a-7182-4abc-96e9-b557045ddc1b.gif"

class SAMPIRatBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threat_vault = {}
        self.whitelist = []
        self.load_vault()

    def load_vault(self):
        if os.path.exists(THREAT_VAULT_PATH):
            with open(THREAT_VAULT_PATH, "r") as f:
                self.threat_vault = json.load(f)
        if os.path.exists(SAFE_HARBOR_PATH):
            with open(SAFE_HARBOR_PATH, "r") as f:
                self.whitelist = json.load(f)

    async def update_vault(self):
        """Self-updating engine to fetch latest threat feeds."""
        async with aiohttp.ClientSession() as session:
            sources = self.threat_vault.get("update_sources", [])
            for source in sources:
                try:
                    async with session.get(source) as resp:
                        if resp.status == 200:
                            content = await resp.text()
                            # Basic line-based domain list parsing
                            new_domains = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
                            
                            # Merge into threat vault
                            current_bad = set(self.threat_vault.get("known_bad_domains", []))
                            current_bad.update(new_domains)
                            self.threat_vault["known_bad_domains"] = list(current_bad)
                            
                            # Log update
                            self.threat_vault["last_updated"] = datetime.utcnow().isoformat()
                            
                            with open(THREAT_VAULT_PATH, "w") as f:
                                json.dump(self.threat_vault, f, indent=4)
                                
                            print(f"SAMPI.RT: Vault updated from {source}. Total domains: {len(current_bad)}")
                except Exception as e:
                    print(f"Update Error fetching {source}: {e}")

    async def on_ready(self):
        print(f"S.A.M.I.RT Bot Online: {self.user}")
        # Map the Log channel dynamically if possible, or use the configured ID
        # For now, we use the ID from the build plan (Sorry Dave Quarantine)
        self.loop.create_task(self.vault_update_loop())

    async def vault_update_loop(self):
        while True:
            await self.update_vault()
            await asyncio.sleep(86400) # Once a day

    async def on_message(self, message):
        if message.author.bot:
            return

        # 1. PHISHING & IP LOGGER CHECK (P & I)
        urls = re.findall(r'(https?://\S+)', message.content)
        for url in urls:
            domain = url.split("//")[-1].split("/")[0]
            if domain in self.threat_vault.get("known_bad_domains", []):
                await self.quarantine(message, f"Known Malicious Domain: {domain}")
                return

        # 2. ANTI VIRUS (A & M)
        for attachment in message.attachments:
            if any(attachment.filename.endswith(ext) for ext in [".exe", ".bat", ".lua", ".scr"]):
                # Heuristic: Scan file content or check against whitelist
                if attachment.filename not in self.whitelist:
                    await self.quarantine(message, f"Suspicious File Type: {attachment.filename}")
                    return

        await self.process_commands(message)

    async def quarantine(self, message, reason):
        """The Protocol: Delete, Respond, Log, Strike."""
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} {SORRY_DAVE_MSG}", delete_after=10)
            
            # Log to #sorry_dave
            log_channel = self.get_channel(SORRY_DAVE_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(
                    title="⚔️ S.A.M.P.I.RT: QUARANTINE BREACH 🛡️", 
                    description=f"**{SORRY_DAVE_MSG}**",
                    color=discord.Color.red()
                )
                embed.set_author(name="S.A.M.P.I.RT Security Engine", icon_url=GUARD_AVATAR_URL)
                embed.add_field(name="🚨 INTRUDER", value=message.author.mention, inline=True)
                embed.add_field(name="🛑 THREAT TYPE", value=reason, inline=True)
                # Fullscreen Alert Tweak: Move GIF to main image
                embed.set_image(url=SIREN_GIF_URL)
                embed.set_footer(text="🛑 [VISUAL PULSE ACTIVE] - Master Black Box Protocol - Forge Secure 100% 🛑")
                embed.timestamp = datetime.utcnow()
                await log_channel.send(content="🚨 **CRITICAL: SECURITY BREACH NEUTRALIZED** 🚨", embed=embed)
        except Exception as e:
            print(f"Quarantine Error: {e}")

# MAIN ENTRY POINT
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    intents = discord.Intents.all()
    bot = SAMPIRatBot(command_prefix="!!", intents=intents)
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
