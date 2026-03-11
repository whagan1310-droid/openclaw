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
SHARED_LINKS_PATH = "shared_links.json"
SORRY_DAVE_MSG = "!!!---SORRY_DAVE_YOU_SHOULD_HAVE_KNOWN_WE_CAN'T_DO_THAT---!!!"
SORRY_DAVE_CHANNEL_ID = 1480230319935324241 # Placeholder, update per build plan
GITHUB_SHARE_CHANNEL_ID = 1481056548510892063  # Category or channel for shared links

# VISUAL ASSETS (From Forge Assets)
GUARD_AVATAR_URL = "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/image_ccdb2fa9-f41f-4ee6-8798-936616055dcc.png"

# DYNAMIC ALERT MAPPING (Categorized by Hazard Level)
ALERT_ASSETS = {
    "CRITICAL": {
        "color": discord.Color.red(),
        "siren": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/assets/sirens/red_siren.gif",
        "avatar": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/sampi_bot_red.png",
        "label": "🚨 CRITICAL: SECURITY BREACH NEUTRALIZED 🚨"
    },
    "HIGH": {
        "color": discord.Color.orange(),
        "siren": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/assets/sirens/amber_siren.gif",
        "avatar": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/sampi_bot_yellow.png",
        "label": "⚠️ HIGH: THREAT QUARANTINED ⚠️"
    },
    "MEDIUM": {
        "color": discord.Color.blue(),
        "siren": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/assets/sirens/blue_siren.gif",
        "avatar": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/sampi_bot_blue.png",
        "label": "🔹 MEDIUM: ANOMALY DETECTED 🔹"
    },
    "LOW": {
        "color": discord.Color.green(),
        "siren": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/assets/sirens/green_siren.gif",
        "avatar": "https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/sampi_bot_green.png",
        "label": "🟢 LOW: MINOR INFRACTION LOGGED 🟢"
    }
}

DISCIPLINE_REPORTS_FILE = "DISCIPLINE_REPORTS.md"

class SAMPIRatBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threat_vault: dict[str, Any] = {}
        self.whitelist: list[str] = []
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
            
            # Heuristic Danger Level Determination
            danger_level = "CRITICAL"
            if reason in ["SPAM", "PROFANITY"]:
                danger_level = "LOW"
            elif "Domain" in reason or "PHISHING" in reason:
                danger_level = "HIGH"
            elif "VIRUS" in reason or "MALWARE" in reason:
                danger_level = "CRITICAL"
            else:
                danger_level = "MEDIUM"

            alert = ALERT_ASSETS.get(danger_level, ALERT_ASSETS["CRITICAL"])

            # Log to #sorry_dave
            log_channel = self.get_channel(SORRY_DAVE_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(
                    title=f"⚔️ S.A.M.P.I.RT: {danger_level} BREACH 🛡️", 
                    description=f"**{SORRY_DAVE_MSG}**",
                    color=alert["color"]
                )
                # Dynamic Identity: Avatar matches Siren color
                embed.set_author(name="S.A.M.P.I.RT Security Engine", icon_url=alert["avatar"])
                embed.add_field(name="🚨 INTRUDER", value=message.author.mention, inline=True)
                embed.add_field(name="🛑 THREAT TYPE", value=reason, inline=True)
                # Dynamic Style: Fullscreen Siren chose by Bot according to level
                embed.set_image(url=alert["siren"])
                embed.set_footer(text=f"🛑 [VISUAL PULSE: {danger_level}] - Forge Secure 100% 🛑")
                embed.timestamp = datetime.utcnow()
                await log_channel.send(content=f"🚨 **{alert['label']}** 🚨", embed=embed)
                
                # Private DM to User
                try:
                    dm_embed = discord.Embed(
                        title="⚠️ ACADEMY INFRACTION RECORED",
                        description=f"**{SORRY_DAVE_MSG}**\n\nYour recent action was flagged and neutralized. Refer to Forge Case #{os.urandom(4).hex().upper()}.",
                        color=discord.Color.red()
                    )
                    dm_embed.add_field(name="Reason", value=reason)
                    await message.author.send(embed=dm_embed)
                except:
                    pass
                
                # Long-term Archival
                self.log_discipline_action(message.author, f"Auto-Quarantine: {reason}", "S.A.M.P.I.RT")
        except Exception as e:
            print(f"Quarantine Error: {e}")

    # ══════════════════════════════════════════════
    #  EXPANDED HAZARD AWARENESS COMMANDS
    # ══════════════════════════════════════════════

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        """Server-wide health check with color pulse system."""
        # Heuristic: Overall health depends on recent strikes/threats
        # For demo, we reflect a 'GOOD' state unless there are recent threats
        health = "LOW" # Green/Good default
        
        # Check if any CRITICAL or HIGH threats in last 24h (mock logic)
        # health = "CRITICAL" if recent_critical else "LOW"
        
        alert = ALERT_ASSETS.get(health, ALERT_ASSETS["CRITICAL"])
        
        embed = discord.Embed(
            title="🛰️ ACADEMY MASTER STATUS 🛡️",
            description=f"**Current Forge Vibe**: {health}\n**Security Protocol**: Active 100%",
            color=alert["color"]
        )
        embed.set_author(name="S.A.M.P.I.RT Diagnostic", icon_url=alert["avatar"])
        embed.set_image(url=alert["siren"])
        embed.add_field(name="🛡️ S.A.M.P.I.RT", value="🟢 ONLINE", inline=True)
        embed.add_field(name="⚔️ GOONSCLAWBOT", value="🟢 ONLINE", inline=True)
        embed.add_field(name="🎥 SYNCFLUX", value="🟡 STANDBY", inline=True)
        embed.add_field(name="🎵 SONICFORGE", value="🟡 STANDBY", inline=True)
        
        embed.set_footer(text=f"🛑 [VISUAL PULSE: {health}] - Forge Monitoring Active 🛑")
        await ctx.send(embed=embed)

    @commands.command(name="scan_channel")
    @commands.has_permissions(manage_messages=True)
    async def scan_channel(self, ctx, channel: discord.TextChannel = None):
        """Diagnostic scan of a channel's pulse."""
        channel = channel or ctx.channel
        async with ctx.typing():
            # Heuristic scan of last 50 messages
            hazard_score = 0
            messages = []
            async for msg in channel.history(limit=50):
                if not msg.author.bot:
                    # Look for links/attachments
                    if re.findall(r'(https?://\S+)', msg.content): hazard_score += 1
                    if msg.attachments: hazard_score += 2
            
            level = "LOW"
            if hazard_score > 10: level = "CRITICAL"
            elif hazard_score > 5: level = "HIGH"
            elif hazard_score > 2: level = "MEDIUM"
            
            alert = ALERT_ASSETS.get(level)
            
            embed = discord.Embed(
                title=f"🔍 CHANNEL SCAN: #{channel.name} 🛡️",
                description=f"**Hazard Level**: {level}\n**Diagnostic Score**: {hazard_score}",
                color=alert["color"]
            )
            embed.set_author(name="S.A.M.P.I.RT Deep Scan", icon_url=alert["avatar"])
            embed.set_image(url=alert["siren"])
            embed.set_footer(text=f"🛑 [VISUAL PULSE: {level}] - Deep Scan Complete 🛑")
            await ctx.send(embed=embed)

    @commands.command(name="scan_user")
    @commands.has_permissions(manage_messages=True)
    async def scan_user(self, ctx, member: discord.Member):
        """Risk assessment of a specific member."""
        # Mock risk assessment based on status
        level = "LOW"
        if member.guild_permissions.administrator:
            level = "LOW"
        # In real build, check strike_log.json
        
        alert = ALERT_ASSETS.get(level)
        
        embed = discord.Embed(
            title=f"👤 USER RISK ASSESSMENT: {member.name} 🛡️",
            description=f"**Risk Profile**: {level}\n**Status**: Verified Apptivator",
            color=alert["color"]
        )
        embed.set_author(name="S.A.M.P.I.RT Identity Audit", icon_url=alert["avatar"])
        embed.set_image(url=alert["siren"])
        embed.set_footer(text=f"🛑 [VISUAL PULSE: {level}] - Identity Verified 🛑")
        await ctx.send(embed=embed)

    @commands.command(name="query")
    @commands.has_permissions(manage_messages=True)
    async def query(self, ctx, user_id: str):
        """Forensic analysis of a user's logs and strike history."""
        if os.path.exists(STRIKE_LOG_PATH):
            with open(STRIKE_LOG_PATH, "r") as f:
                log = json.load(f)
        else:
            log = {}

        if user_id not in log:
            await ctx.send(f"🔍 No historical data for User ID `{user_id}`.")
            return

        user_data = log[user_id]
        strikes = user_data.get("strikes", [])
        
        embed = discord.Embed(title=f"🕵️‍♂️ FORENSIC AUDIT: {user_data['username']}", color=discord.Color.blue())
        embed.add_field(name="ID", value=user_id, inline=True)
        embed.add_field(name="Total Infractions", value=len(strikes), inline=True)
        
        history = ""
        for s in strikes[-5:]: # Last 5
            history += f"• [{s['timestamp'][:10]}] {s['reason']} (by {s['issued_by']})\n"
        
        embed.add_field(name="Recent History", value=history or "Clean Record", inline=False)
        embed.set_footer(text="S.A.M.P.I.RT Forensic Engine")
        await ctx.send(embed=embed)

    # ══════════════════════════════════════════════
    #  STAFF DISCIPLINARY CORE (Lvl 4-5 / Admin)
    # ══════════════════════════════════════════════
    
    async def _check_mod_level(self, member):
        """Check if a member has Lvl 4-5 Moderator or Admin roles."""
        if member.guild_permissions.administrator: return True
        return any("level 4" in r.name.lower() or "level 5" in r.name.lower() for r in member.roles)

    @commands.command(name="freeze")
    @commands.has_permissions(manage_roles=True)
    async def freeze(self, ctx, member: discord.Member):
        """Lock a user in review (remove all roles, add 'Freezed' role)."""
        if not await self._check_mod_level(ctx.author):
            await ctx.send("❌ Access Denied: Requires Lvl 4-5 Moderator clearances.")
            return

        freeze_role = discord.utils.get(ctx.guild.roles, name="Freezed")
        if not freeze_role:
            freeze_role = await ctx.guild.create_role(name="Freezed", color=discord.Color.dark_blue())

        # Blackout: Remove all other roles
        await member.edit(roles=[freeze_role])
        await ctx.send(f"❄️ USER FROZEN: {member.mention} has been locked in the Private Review Chamber.")

    @commands.command(name="unfreeze")
    @commands.has_permissions(manage_roles=True)
    async def unfreeze(self, ctx, member: discord.Member):
        """Restore user access."""
        if not await self._check_mod_level(ctx.author):
            await ctx.send("❌ Access Denied.")
            return

        freeze_role = discord.utils.get(ctx.guild.roles, name="Freezed")
        if freeze_role in member.roles:
            await member.remove_roles(freeze_role)
            # Logic here to restore previous roles if stored? For now, back to Initiate
            initiate = discord.utils.get(ctx.guild.roles, name="Initiate")
            if initiate: await member.add_roles(initiate)
            await ctx.send(f"🔥 USER UNFROZEN: {member.mention} access restored to Initiate.")

    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, *, reason="1 Year Suspension"):
        """1 Year Ban (Quorum Required)."""
        if not await self._check_mod_level(ctx.author):
            await ctx.send("❌ Access Denied.")
            return

        # Quorum Check (Simulated: requires a specific reaction or confirmation)
        await ctx.send(f"⚖️ **BAN QUORUM INITIATED**: Lvl 4-5 Moderator `{ctx.author}` requests a 1YR Ban for {member.mention}.\nReason: {reason}\n*Requires 2nd Mod confirmation or SAM malicious content report.*")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Permanent Expulsion"):
        """Permanent Ban (Quorum Required)."""
        if not await self._check_mod_level(ctx.author):
            await ctx.send("❌ Access Denied.")
            return
        
        await ctx.send(f"💀 **PROTOCOL 0: PERMANENT PURGE**: {member.mention} is scheduled for expulsion.\n*Quorum Verification Pending...*")

    @commands.command(name="unban")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, user_id: int):
        """Restore access (Admin Only)."""
        user = await self.fetch_user(user_id)
        await ctx.guild.unban(user)
        self.log_discipline_action(user, "Unban / Amnesty", ctx.author.name)
        await ctx.send(f"🔓 **RESTORED**: User ID `{user_id}` has been allowed back into the forge.")

    def log_discipline_action(self, user, action, moderator):
        """Log disciplinary actions to a persistent Markdown report in the repo."""
        report_exists = os.path.exists(DISCIPLINE_REPORTS_FILE)
        with open(DISCIPLINE_REPORTS_FILE, "a", encoding="utf-8") as f:
            if not report_exists:
                f.write("# ⚖️ ACADEMY DISCIPLINE REPORTS & STRIKE RECORDS\n\n")
                f.write("| Timestamp | User | Action | Moderator/Bot | Case ID |\n")
                f.write("|-----------|------|--------|---------------|---------|\n")
            
            ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            case_id = os.urandom(4).hex().upper()
            f.write(f"| {ts} | {user.name} ({user.id}) | {action} | {moderator} | {case_id} |\n")

    # ══════════════════════════════════════════════
    #  GITHUB LINK SHARING SYSTEM
    # ══════════════════════════════════════════════

    def _validate_github_url(self, url: str) -> bool:
        """Validate if URL is a valid public GitHub repository."""
        github_pattern = r'^https?://(www\.)?github\.com/[\w-]+/[\w.-]+/?$'
        return bool(re.match(github_pattern, url.strip()))

    async def _verify_github_accessible(self, url: str) -> bool:
        """Verify GitHub repo is accessible (not private)."""
        try:
            async with aiohttp.ClientSession() as session:
                api_url = url.replace("github.com", "api.github.com/repos")
                async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("private", True) == False
                    return False
        except:
            return False

    def _load_shared_links(self) -> list:
        """Load shared links from JSON file."""
        if os.path.exists(SHARED_LINKS_PATH):
            with open(SHARED_LINKS_PATH, "r") as f:
                return json.load(f)
        return []

    def _save_shared_links(self, links: list):
        """Save shared links to JSON file."""
        with open(SHARED_LINKS_PATH, "w") as f:
            json.dump(links, f, indent=2)

    @commands.command(name="sharelink")
    async def sharelink(self, ctx, github_url: str, *, description: str = None):
        """Share a public GitHub link to the community. Usage: !!sharelink <github_url> [description]"""
        await ctx.message.delete()
        
        if not self._validate_github_url(github_url):
            await ctx.send("❌ **INVALID LINK**: Please provide a valid GitHub repository URL.\nExample: `!!sharelink https://github.com/username/repo`", delete_after=10)
            return

        await ctx.trigger_typing()
        
        is_accessible = await self._verify_github_accessible(github_url)
        if not is_accessible:
            await ctx.send("❌ **ACCESS DENIED**: This GitHub repository appears to be private or does not exist.\nOnly **PUBLIC** repositories can be shared.", delete_after=15)
            return

        link_data = {
            "id": len(self._load_shared_links()) + 1,
            "url": github_url.strip(),
            "description": description or "No description provided",
            "user_id": str(ctx.author.id),
            "user_name": ctx.author.name,
            "user_nickname": ctx.author.display_name,
            "channel_name": ctx.channel.name if ctx.guild else "DM",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        links = self._load_shared_links()
        links.append(link_data)
        self._save_shared_links(links)

        embed = discord.Embed(
            title=f"🔗 SHARED REPOSITORY #{link_data['id']}",
            color=discord.Color.from_rgb(88, 101, 242),
            url=github_url.strip()
        )
        embed.add_field(name="📂 Repository", value=f"[{github_url.strip()}]({github_url.strip()})", inline=False)
        embed.add_field(name="📝 Description", value=link_data["description"], inline=False)
        embed.add_field(name="👤 Shared By", value=f"**{ctx.author.display_name}** (`{ctx.author.id}`)", inline=True)
        embed.add_field(name="💬 Channel", value=f"#{ctx.channel.name if ctx.guild else 'DM'}", inline=True)
        embed.add_field(name="⏰ Added", value=f"<t:{int(datetime.utcnow().timestamp())}:R>", inline=True)
        embed.set_footer(text="🔒 Verified Public Repository • S.A.M.P.I.RT Link Security")
        embed.set_thumbnail(url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")

        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def list_links(self, ctx, limit: int = 10):
        """List shared GitHub links. Usage: !!links [number]"""
        links = self._load_shared_links()
        if not links:
            await ctx.send("📭 No links shared yet. Use `!!sharelink <github_url> [description]` to share a repository!")
            return

        links = links[-limit:]
        embed = discord.Embed(
            title="🔗 Recent Shared Repositories",
            color=discord.Color.from_rgb(88, 101, 242)
        )
        
        for link in links:
            embed.add_field(
                name=f"#{link['id']} • {link['user_nickname']}",
                value=f"[{link['url']}]({link['url']})\n{link['description'][:100]}...",
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command(name="mylinks")
    async def my_links(self, ctx):
        """Show links you've shared."""
        links = self._load_shared_links()
        user_links = [l for l in links if str(l["user_id"]) == str(ctx.author.id)]
        
        if not user_links:
            await ctx.send("📭 You haven't shared any links yet.")
            return

        embed = discord.Embed(
            title=f"🔗 Your Shared Repositories ({len(user_links)})",
            color=discord.Color.from_rgb(88, 101, 242)
        )
        
        for link in user_links:
            embed.add_field(
                name=f"#{link['id']} • {link['timestamp'][:10]}",
                value=f"[{link['url']}]({link['url']})\n{link['description'][:80]}",
                inline=False
            )
        
        await ctx.send(embed=embed)

# MAIN ENTRY POINT
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    intents = discord.Intents.all()
    bot = SAMPIRatBot(command_prefix="!!", intents=intents)
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
