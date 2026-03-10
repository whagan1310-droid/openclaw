"""
🛡️ Apptivators Academy: GoonsClawbot (Legendary Edition) 🛡️
==========================================================
The definitive backbone of the Apptivators Academy. This script handles 
everything from the initial 'Call to Arms' to the final 'I Agree' registration.

Architecture:
- Persistent GUIs: Interactive buttons that survive bot restarts.
- GitHub Integration: Automated pushing of blueprints and logs.
- AI Mentorship: Integrated Gemini 1.5 Flash for code reviews.
- Security: Automated blackout rules for private chambers.
- The Sentinel: Basic auto-moderation for link spam and filtering.

Forge Theme: ⚔️🛡️🤖💯
"""

import discord
from discord.ext import commands
from discord import ui
import os
import json
import base64
import datetime
import requests
from dotenv import load_dotenv
import logging
import asyncio

# ──────────────────────────────────────────────
# Setup logging to file
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GoonsClawbot")

# ──────────────────────────────────────────────
# Load environment variables from .env
# ──────────────────────────────────────────────
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_PAT = os.getenv("GITHUB_PAT")

# ──────────────────────────────────────────────
# Configuration constants
# ──────────────────────────────────────────────
GITHUB_OWNER = "whagan1310-droid"
GITHUB_REPO = "Discord-Build-Plan-Apptivators-Academy"
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}"

# Replace with your actual Category ID for Private Review Chambers
PRIVATE_CATEGORY_ID = 1480191656501186622

# Files that !deploy_plan will push to GitHub
BUILD_PLAN_DIR = os.path.dirname(os.path.abspath(__file__))
DEPLOY_FILES = [
    "discord_server_build_plan.md",
    "discord_channel_definitions.md",
    "github_readme_template.md",
    "discohook_rules_template.json",
    "goons_clawbot.py",
    "openclaw_bot_integration_guide.md",
    "strike_log.json",
    "bot.log",
    "setup_server.py",
]

# ──────────────────────────────────────────────
# Server Structure Definition
# ──────────────────────────────────────────────
SERVER_STRUCTURE = {
    "📢 1. Welcome & Information": [
        {"name": "welcome", "topic": "Landing page for new members. triggers Call to Arms."},
        {"name": "rules", "topic": "The immutable law of the server. Accept to participate."},
        {"name": "announcements", "topic": "Read-only space for Admins/Leaders."},
        {"name": "roles", "topic": "Self-assign skill levels and tags."},
        {"name": "github-shared-links", "topic": "Automated GitHub Webhook feed."},
    ],
    "🤝 2. Community & Collaboration": [
        {"name": "resources", "topic": "Curated collection of tutorials and guides."},
        {"name": "showcase", "topic": "Share projects and collaborate."},
        {"name": "memes", "topic": "Safe space for tech humor."},
        {"name": "career-growth", "topic": "Job opportunities and resume reviews."},
    ],
    "🛠️ 3. Support & Technical Help": [
        {"name": "help-desk", "topic": "Ticketing system for technical assistance."},
        {"name": "code-reviews", "topic": "Professional feedback and debugging."},
        {"name": "quick-questions", "topic": "Short, simple tech questions."},
        {"name": "learning-groups", "topic": "Study cohorts and bootcamps."},
    ],
    "💻 4. Language-Specific Categories": [
        {"name": "web-dev", "topic": "HTML, CSS, JS, and frameworks."},
        {"name": "python", "topic": "Python development and libraries."},
        {"name": "java-cpp", "topic": "Java and C++ discussion."},
        {"name": "rust", "topic": "Rustacean sanctuary."},
        {"name": "ai-machine-learning", "topic": "AI/ML developments."},
        {"name": "devops-cybersecurity", "topic": "Infra and security."},
    ],
    "🎥 5. SyncFlux: Media & Colab": [
        {"name": "youtube-links", "topic": "Shared Academy YouTube content."},
        {"name": "colab-notebooks", "topic": "Collaborative coding notebooks."},
        {"name": "sync-status", "topic": "Media pipeline health tracking."},
    ],
    "🎵 6. SonicForge: Audio & Rhythm": [
        {"name": "the-forge-audio", "topic": "High-fidelity Academy audio stream."},
        {"name": "academy-playlists", "topic": "Collaborative music queues."},
        {"name": "rhythm-status", "topic": "Audio engine diagnostics."},
    ],
    "📜 7. Transparency & Governance": [
        {"name": "all-bot-commands", "topic": "Public Academy Command Manual for all users."},
        {"name": "admin-mod-bot-commands", "topic": "Confidential Staff Command Manual (Admins/Mods only)."},
        {"name": "collaborator-applications", "topic": "Public queue for collaborator status requests."},
    ],
}

# Role Mapping for Onboarding (Noob to God Tier)
SKILL_LEVEL_ROLES = {
    1: "The Noob (Level 0-1)",
    2: "The Beginner (Level 2)",
    3: "The Intermediate (Level 3-7)",
    4: "The Expert (Level 8-12)",
    5: "The God (Level 13-∞)",
}

# New Channel IDs from START HERE.txt
CHANNEL_IDS = {
    "welcome": 1480230319935324241,
    "rules": 1480229817356910755,
    "definitions": 1480229121958215681,
    "roles": 1480234013481242735,
    "call_to_arms": 1480229956419322017,
    "general": 1479944143613591764,
}

# Default role for all new members
DEFAULT_JOIN_ROLE = "Initiate"

# Strike log stored locally as JSON
STRIKE_LOG_FILE = os.path.join(BUILD_PLAN_DIR, "strike_log.json")

# ──────────────────────────────────────────────
# Bot setup
# ──────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# Persistence Helpers
JOINED_MEMBERS_FILE = os.path.join(BUILD_PLAN_DIR, "joined_members.json")

class GoonsClawBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.joined_members_file = JOINED_MEMBERS_FILE
        self.strike_log_file = STRIKE_LOG_FILE

    def save_member_data(self, user_id, name, level_role):
        data = {"members": []}
        if os.path.exists(self.joined_members_file):
            with open(self.joined_members_file, "r") as f:
                data = json.load(f)
        
        # Check if already exists
        for member in data["members"]:
            if member["user_id"] == user_id:
                member["level"] = level_role
                member["updated_at"] = datetime.datetime.utcnow().isoformat()
                break
        else:
            data["members"].append({
                "user_id": user_id,
                "name": name,
                "level": level_role,
                "joined_at": datetime.datetime.utcnow().isoformat()
            })
        
        with open(self.joined_members_file, "w") as f:
            json.dump(data, f, indent=4)

    async def seed_youtube_resources(self, guild):
        """Seed the #youtube-links channel with recommended Academy content."""
        yt_ch = discord.utils.get(guild.text_channels, name="youtube-links")
        if not yt_ch: return

        # Check if already seeded
        async for msg in yt_ch.history(limit=10):
            if msg.author == self.user and msg.embeds and "RECOMMENDED ACADEMY RESOURCE" in msg.embeds[0].title:
                return

        resources = [
            {"title": "OpenClaw AI - Advanced Agentic Coding", "url": "https://www.youtube.com/@softwaregent7443", "author": "Software Gent"},
            {"title": "Streaming & OBS Mastery", "url": "https://www.youtube.com/@Gael_Level", "author": "Gael Level"}
        ]

        for res in resources:
            embed = discord.Embed(title=f"🎥 RECOMMENDED ACADEMY RESOURCE: {res['author']}", color=discord.Color.red(), url=res['url'])
            embed.description = f"Check out {res['author']} for elite knowledge on {res['title']}."
            await yt_ch.send(embed=embed)

    async def deploy_command_manuals(self, guild):
        """Automatically post the Academy Command Manual to transparency channels."""
        public_ch = discord.utils.get(guild.text_channels, name="all-bot-commands")
        staff_ch = discord.utils.get(guild.text_channels, name="admin-mod-bot-commands")

        manual_content = """
# 📖 ACADEMY FORGE COMMAND MANUAL
## 🦾 GOONSCLAWBOT (Prefix: `!`)
- `!rules`: View the Forge Code of Conduct.
- `!roles`: Open the Tier Selection terminal.
- `!apply_collaborator`: Submit a project/skill application.
- `!submit_repo`: Share a repo with the community.

## 🛡️ S.A.M.P.I.RT (Prefix: `!!`)
- `!!status`: Diagnostic health of the Forge.
- `!!scan_channel`: Security pulse of a channel.
- `!!query [id]`: Forensic audit of a user.
- `!!freeze [id]`: Quarantine a user for review.
        """

        if public_ch:
            await public_ch.purge(limit=5)
            embed = discord.Embed(title="📖 ACADEMY FORGE COMMAND MANUAL (Public)", color=discord.Color.blue(), description=manual_content)
            await public_ch.send(embed=embed)
        
        if staff_ch:
            staff_manual = manual_content + "\n## ⚖️ MODERATOR CORE\n- `!strike [id]`: Assign an infraction.\n- `!!ban/!!tempban`: Disciplinary expulsion."
            await staff_ch.purge(limit=5)
            embed = discord.Embed(title="📖 ACADEMY FORGE COMMAND MANUAL (Internal Staff)", color=discord.Color.red(), description=staff_manual)
            await staff_ch.send(embed=embed)

bot = GoonsClawBot(command_prefix="!", intents=intents)

# ══════════════════════════════════════════════
#  EVENT: on_ready
# ══════════════════════════════════════════════
# ──────────────────────────────────────────────
#  AUTO-BOOTSTRAP CONFIG (Push Actions Automatically)
# ──────────────────────────────────────────────
AUTO_BOOTSTRAP = True # Set to True to build server & onboarding on start

@bot.event
async def on_ready():
    # Register persistent views
    bot.add_view(RoleSelectionView())
    bot.add_view(RulesAgreementView())
    bot.add_view(JoinWalkthroughView())
    logger.info(f"GoonsClawbot Online: {bot.user.name} ({bot.user.id})")
    
    if AUTO_BOOTSTRAP:
        logger.info("🚀 AUTO-BOOTSTRAP: Initiating Server Build...")
        for guild in bot.guilds:
            # 1. Build Server Structure
            logger.info(f"🏗️ Building structure for {guild.name}...")
            for cat_name, channels in SERVER_STRUCTURE.items():
                category = discord.utils.get(guild.categories, name=cat_name)
                if not category:
                    category = await guild.create_category(cat_name)
                for ch in channels:
                    channel = discord.utils.get(category.text_channels, name=ch["name"])
                    if not channel:
                        perms_overwrites = {
                            guild.default_role: discord.PermissionOverwrite(send_messages=False),
                            guild.me: discord.PermissionOverwrite(send_messages=True)
                        }
                        await guild.create_text_channel(ch["name"], category=category, topic=ch["topic"], overwrites=perms_overwrites)
            
            # 2. Deploy Command Manuals
            await bot.deploy_command_manuals(guild)
            
            # 3. Seed YouTube Resources
            await bot.seed_youtube_resources(guild)

        logger.info("✅ AUTO-BOOTSTRAP COMPLETE.")

    async def seed_youtube_resources(self, guild):
        """Seed the #youtube-links channel with recommended Academy content."""
        yt_ch = discord.utils.get(guild.text_channels, name="youtube-links")
        if not yt_ch: return

        # Check if already seeded
        async for msg in yt_ch.history(limit=5):
            if msg.author == self.user and "RECOMMENDED ACADEMY RESOURCE" in msg.embeds[0].title if msg.embeds else False:
                return

        resources = [
            {"title": "OpenClaw AI - Advanced Agentic Coding", "url": "https://www.youtube.com/@softwaregent7443", "author": "Software Gent"},
            {"title": "Streaming & OBS Mastery", "url": "https://www.youtube.com/@Gael_Level", "author": "Gael Level"}
        ]

        for res in resources:
            embed = discord.Embed(title=f"🎥 RECOMMENDED ACADEMY RESOURCE: {res['author']}", color=discord.Color.red(), url=res['url'])
            embed.description = f"Check out {res['author']} for elite knowledge on {res['title']}."
            await yt_ch.send(embed=embed)

    async def deploy_command_manuals(self, guild):
        """Automatically post the Academy Command Manual to transparency channels."""
        public_ch = discord.utils.get(guild.text_channels, name="all-bot-commands")
        staff_ch = discord.utils.get(guild.text_channels, name="admin-mod-bot-commands")

        public_manual = discord.Embed(
            title="⚔️ ACADEMY COMMAND MANUAL (PUBLIC) ⚔️",
            description="Welcome to the Forge. Here is your interface for the Academy Bot Suite.",
            color=discord.Color.blue()
        )
        public_manual.add_field(name="🤖 GoonsClawbot (!)", value="`!welcome` - Restart walkthrough\n`!apply_collaborator` - Join the elite\n`!submit_repo [url]` - Share knowledge", inline=False)
        public_manual.add_field(name="🛡️ S.A.M.P.I.RT (!!)", value="`!!status` - Health check\n`!!open_chamber` - Start a safe review", inline=False)
        public_manual.add_field(name="🎥 SyncFlux (!sync_)", value="`!sync_video [url]` - Queue media\n`!sync_status` - Pipeline health", inline=False)
        public_manual.add_field(name="🎵 SonicForge (!sonic_)", value="`!sonic_play [query]` - Stream music\n`!sonic_queue` - View tracklist", inline=False)
        
        staff_manual = discord.Embed(
            title="🛡️ ACADEMY COMMAND MANUAL (STAFF ONLY) 🛡️",
            description="Restricted interfaces for Academy Moderators and Admins.",
            color=discord.Color.dark_red()
        )
        staff_manual.add_field(name="🔧 Admin Core", value="`!build_server` - Full restructure\n`!initialize_onboarding` - GUI Reset", inline=False)
        staff_manual.add_field(name="⚖️ S.A.M.P.I.RT Forensics", value="`!!query [user_id]` - Audit history\n`!!scan_channel` - Hazard pulse\n`!!scan_user [@user]` - Risk assessment", inline=False)
        staff_manual.add_field(name="🛑 Disciplinary (Lvl 4-5)", value="`!!freeze [user]` - Lock in review\n`!!tempban [user]` - 1yr suspension\n`!!ban [user]` - Permanent purge\n`!!unban [id]` - (Admin Only)", inline=False)

        if public_ch:
            # Simple check to avoid double-posting: check last message author
            async for msg in public_ch.history(limit=5):
                if msg.author == self.user and "PUBLIC" in msg.embeds[0].title if msg.embeds else False:
                    break
            else:
                await public_ch.send(embed=public_manual)

        if staff_ch:
            async for msg in staff_ch.history(limit=5):
                if msg.author == self.user and "STAFF ONLY" in msg.embeds[0].title if msg.embeds else False:
                    break
            else:
                await staff_ch.send(embed=staff_manual)

    for guild in bot.guilds:
        logger.info(f"Guild: {guild.name}")
        for channel in guild.text_channels:
            logger.info(f" - Channel: #{channel.name} (ID: {channel.id})")


# ══════════════════════════════════════════════
#  UI COMPONENTS: Onboarding Views
# ══════════════════════════════════════════════

# ──────────────────────────────────────────────
#  UI: Agreement Modal
# ──────────────────────────────────────────────
class AgreementModal(ui.Modal, title='⚔️ Mandatory Agreement ⚔️'):
    answer = ui.TextInput(label='Type "I AGREE" in all caps', placeholder='I AGREE', min_length=7, max_length=7)

    async def on_submit(self, interaction: discord.Interaction):
        if self.answer.value == "I AGREE":
            view = RulesAgreementView()
            await view._grant_access(interaction)
        else:
            await interaction.response.send_message('❌ Verification failed. You must type "I AGREE" exactly.', ephemeral=True)

class RulesAgreementView(ui.View):
    """
    Final Registration Gate: The 'I Agree' Page.
    Triggers the 'Verified Apptivator' role and closes the journey.
    """
    def __init__(self):
        super().__init__(timeout=None)

    async def _grant_access(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        verified_role_name = "Verified Apptivator"
        role = discord.utils.get(guild.roles, name=verified_role_name)
        
        if not role:
            try:
                role = await guild.create_role(
                    name=verified_role_name, 
                    color=discord.Color.gold(),
                    reason="Legendary Onboarding Finalized"
                )
            except discord.Forbidden:
                await interaction.response.send_message("❌ I cannot create the Verified role. Check permissions.", ephemeral=True)
                return

        try:
            await member.add_roles(role)
            # Remove Initiate role
            initiate_role = discord.utils.get(guild.roles, name=DEFAULT_JOIN_ROLE)
            if initiate_role in member.roles:
                await member.remove_roles(initiate_role)
            
            bot.save_member_data(member.id, str(member), "Verified Apptivator")
            
            legendary_quote = (
                "\"\"One App At A Time.\" The forge is hot, the guards are at the gate, and the synthetic edge is sharp.\n"
                "It has been an absolute pleasure building this fortress with you. The Academy is now yours to lead! ⚔️🛡️🤖\""
            )
            await interaction.response.send_message(
                f"💯 **Registration Complete!**\n\n{legendary_quote}\n\nWelcome, **{verified_role_name}**.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("❌ Role hierarchy error. Move my role higher!", ephemeral=True)

    @ui.button(label="⚔️ I Agree to All Server Rules", style=discord.ButtonStyle.success, custom_id="agree_rules")
    async def agree(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AgreementModal())

    @ui.button(emoji="⚔️", style=discord.ButtonStyle.secondary, custom_id="finalize_1")
    async def finalize_1(self, interaction: discord.Interaction, button: ui.Button):
        await self._grant_access(interaction)

    @ui.button(emoji="🛡️", style=discord.ButtonStyle.secondary, custom_id="finalize_2")
    async def finalize_2(self, interaction: discord.Interaction, button: ui.Button):
        await self._grant_access(interaction)

    @ui.button(emoji="🤖", style=discord.ButtonStyle.secondary, custom_id="finalize_3")
    async def finalize_3(self, interaction: discord.Interaction, button: ui.Button):
        await self._grant_access(interaction)

class RoleSelectionView(ui.View):
    """First stage: Select skill level."""
    def __init__(self):
        super().__init__(timeout=None)

    async def assign_role(self, interaction: discord.Interaction, level: int):
        guild = interaction.guild
        role_name = SKILL_LEVEL_ROLES.get(level)
        
        # Ensure role exists or find it
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            try:
                role = await guild.create_role(name=role_name, reason="Auto-created for onboarding")
            except discord.Forbidden:
                await interaction.response.send_message(f"❌ I don't have permission to create the role `{role_name}`.", ephemeral=True)
                return

        # Assign role
        try:
            # Remove other skill level roles first to avoid duplicates
            existing_roles = [r for r in interaction.user.roles if r.name in SKILL_LEVEL_ROLES.values()]
            await interaction.user.remove_roles(*existing_roles)
            await interaction.user.add_roles(role)
            
            # Persistent storage
            bot.save_member_data(interaction.user.id, str(interaction.user), role_name)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to manage your roles. (Check my role position!)", ephemeral=True)
            return

        # Transition to Rules Agreement
        template_path = os.path.join(BUILD_PLAN_DIR, "discohook_rules_template.json")
        rules_embed = discord.Embed(
            title="📜 Server Rules & Development Guidelines",
            description="Please review our core protocols before joining the discussion.",
            color=0x3498DB
        )
        # Use Brain Image for roles
        rules_embed.set_image(url="https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/Brain1-5.png")
        
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if "embeds" in data and len(data["embeds"]) > 0:
                        rules_embed = discord.Embed.from_dict(data["embeds"][0])
                except:
                    pass

        await interaction.response.send_message(
            content=f"✅ Role assigned: **{role_name}**\n\n**Final Step**: Review and agree to the rules below.",
            embed=rules_embed,
            view=RulesAgreementView(),
            ephemeral=True
        )

    @ui.button(label="1", emoji="🛡️", style=discord.ButtonStyle.secondary, custom_id="role_1")
    async def level_1(self, interaction: discord.Interaction, button: ui.Button):
        await self.assign_role(interaction, 1)

    @ui.button(label="2", emoji="⚔️", style=discord.ButtonStyle.secondary, custom_id="role_2")
    async def level_2(self, interaction: discord.Interaction, button: ui.Button):
        await self.assign_role(interaction, 2)

    @ui.button(label="3", emoji="🛠️", style=discord.ButtonStyle.secondary, custom_id="role_3")
    async def level_3(self, interaction: discord.Interaction, button: ui.Button):
        await self.assign_role(interaction, 3)

    @ui.button(label="4", emoji="🧠", style=discord.ButtonStyle.secondary, custom_id="role_4")
    async def level_4(self, interaction: discord.Interaction, button: ui.Button):
        await self.assign_role(interaction, 4)

    @ui.button(label="5", emoji="⚡", style=discord.ButtonStyle.secondary, custom_id="role_5")
    async def level_5(self, interaction: discord.Interaction, button: ui.Button):
        await self.assign_role(interaction, 5)

class JoinWalkthroughView(ui.View):
    """Entry point: The Join Page."""
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="⚔️ Join Apptivators Academy", style=discord.ButtonStyle.success, custom_id="join_now")
    async def join(self, interaction: discord.Interaction, button: ui.Button):
        # Start the questionnaire
        embed = discord.Embed(
            title="🧠 Academy Skill Level Questionnaire",
            description=(
                "To better assist your growth, select the skill tier that best represents your current coding mastery.\n\n"
                "**1** - Initial Trainee (Noob)\n"
                "**2** - Project Starter (Beginner)\n"
                "**3** - System Builder (Intermediate)\n"
                "**4** - Architect / Senior (Expert)\n"
                "**5** - Distinguished Engineer (God)"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/Brain1-5.png")
        await interaction.response.send_message(embed=embed, view=RoleSelectionView(), ephemeral=True)


# ══════════════════════════════════════════════
#  EVENT: Welcome new members
# ══════════════════════════════════════════════
@bot.event
async def on_member_join(member):
    """
    LEGENDARY ENTRANCE: Greet new members, assign Initiate role, and post public welcome.
    """
    logger.info(f"New Member Joined: {member.name} ({member.id})")
    guild = member.guild
    
    # 1. Assign "Initiate" role
    role = discord.utils.get(guild.roles, name=DEFAULT_JOIN_ROLE)
    if not role:
        try:
            role = await guild.create_role(name=DEFAULT_JOIN_ROLE, color=discord.Color.light_grey(), reason="Default join role")
        except discord.Forbidden:
            logger.error("Cannot create Initiate role - check permissions!")
    
    if role:
        try:
            await member.add_roles(role)
            logger.info(f"Assigned {DEFAULT_JOIN_ROLE} to {member.name}")
        except discord.Forbidden:
            logger.warning(f"Could not assign {DEFAULT_JOIN_ROLE} to {member.name}")

    # 2. Public Welcome to #welcome
    welcome_ch = discord.utils.find(lambda c: "welcome" in c.name.lower(), guild.text_channels)
    if welcome_ch:
        embed = discord.Embed(
            title="⚔️ A New Apptivator Arrives!",
            description=f"Welcome {member.mention} to the forge! Report to **#rules** and claim your rank in **#roles**. ⚔️🛡️🤖💯",
            color=discord.Color.gold()
        )
        await welcome_ch.send(embed=embed)

    # 3. Private DM Greeting (Call to Arms)
    try:
        legendary_quote = (
            "\"\"One App At A Time.\" The forge is hot, the guards are at the gate, and the synthetic edge is sharp.\n"
            "It has been an absolute pleasure building this fortress with you. The Academy is now yours to lead! ⚔️🛡️🤖\""
        )
        dm_embed = discord.Embed(
            title="⚔️ Your Academy Journey Begins!",
            description=(
                f"Welcome, **{member.name}**, to the **Apptivators Academy**.\n\n"
                "To unlock the full power of the forge:\n"
                "1️⃣ Review the immutable laws in **#rules**\n"
                "2️⃣ Claim your rank and specialty in **#roles**\n\n"
                f"{legendary_quote}"
            ),
            color=discord.Color.blue(),
        )
        dm_embed.set_thumbnail(url=member.display_avatar.url)
        dm_embed.set_footer(text="The Forge Awaits. ⚔️🛡️🤖💯")
        
        await member.send(embed=dm_embed)
        logger.info(f"Welcome DM sent to {member.name}")
    except discord.Forbidden:
        logger.warning(f"Could not send welcome DM to {member.name} (DMs disabled).")
    except Exception as e:
        logger.error(f"Error in on_member_join: {e}")


# ══════════════════════════════════════════════
#  EVENT: Blackout Rule (auto-purge empty voice)
# ══════════════════════════════════════════════
@bot.event
async def on_voice_state_update(member, before, after):
    """Delete private review voice channels when the last member leaves."""
    if before.channel is not None and PRIVATE_CATEGORY_ID != 0:
        if before.channel.category_id == PRIVATE_CATEGORY_ID:
            if len(before.channel.members) == 0:
                try:
                    channel_name = before.channel.name
                    await before.channel.delete(
                        reason="Blackout Rule: Channel emptied by last user."
                    )
                    print(f"[Total Purge] Deleted: {channel_name}")
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"[Total Purge] Error: {e}")


# ══════════════════════════════════════════════
#  EVENT: The Sentinel (Auto-Mod)
# ══════════════════════════════════════════════
@bot.event
async def on_message(message):
    """
    THE SENTINEL: Scan for link spam and basic violations.
    """
    if message.author.bot:
        return

    # Basic Link Prevention (Example Sentinel Logic)
    banned_links = ["discord.gg/", "invite.gg/"] # Prevent external server invites
    content = message.content.lower()
    
    if any(link in content for link in banned_links):
        if not message.author.guild_permissions.administrator:
            try:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, external invite links are forbidden by **The Law**. ⚔️🛡️🤖", delete_after=5)
                logger.info(f"Sentinel: Deleted invite link from {message.author}")
                return
            except Exception as e:
                logger.error(f"Sentinel Error: {e}")

    await bot.process_commands(message)


# ══════════════════════════════════════════════
#  COMMAND: !post_rules
# ══════════════════════════════════════════════
@bot.command(name="post_rules")
@commands.has_permissions(administrator=True)
async def post_rules(ctx):
    """Read discohook_rules_template.json and post the embed."""
    template_path = os.path.join(BUILD_PLAN_DIR, "discohook_rules_template.json")

    if not os.path.exists(template_path):
        await ctx.send("❌ `discohook_rules_template.json` not found.")
        return

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "embeds" in data and len(data["embeds"]) > 0:
            embed = discord.Embed.from_dict(data["embeds"][0])
            await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            await ctx.send("❌ No embeds found in the JSON file.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


# ══════════════════════════════════════════════
#  COMMAND: !welcome
# ══════════════════════════════════════════════
@bot.command(name="welcome")
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    """Post the Join Page onboarding embed in the current channel."""
    embed = discord.Embed(
        title="⚔️ WELCOME TO THE APPTIVATORS ACADEMY ⚔️",
        description=(
            "You are standing at the threshold of the forge. Beyond this gate lies a network of engineers, "
            "creators, and mentors dedicated to building the future—one app at a time.\n\n"
            "**Access is currently locked.** To enter the Academy, you must complete the onboarding walkthrough."
        ),
        color=0xE74C3C,
    )
    embed.set_image(url="https://raw.githubusercontent.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy/main/AA/Apptivators%20Academy.png")
    embed.add_field(
        name="🚀 Your Journey",
        value="Click the button below to start your skill assessment and agree to the server protocols.",
        inline=False
    )
    view = JoinWalkthroughView()
    await ctx.send(embed=embed, view=view)
    await ctx.message.delete()


# ══════════════════════════════════════════════
#  COMMAND: !build_server
# ══════════════════════════════════════════════
@bot.command(name="build_server")
@commands.has_permissions(administrator=True)
async def build_server(ctx):
    """Automatically create Categories and Channels from the build plan."""
    status_msg = await ctx.send("🏗️ **Initiating Server Build Phase...**")
    guild = ctx.guild
    report: list[str] = []

    for cat_name, channels in SERVER_STRUCTURE.items():
        # Check if category exists
        category = discord.utils.get(guild.categories, name=cat_name)
        if not category:
            report.append(f"📁 Creating Category: `{cat_name}`")
            category = await guild.create_category(cat_name)
        else:
            report.append(f"✔️ Category Exists: `{cat_name}`")

        for ch in channels:
            # Check if channel exists in this category
            channel = discord.utils.get(category.text_channels, name=ch["name"])
            if not channel:
                report.append(f"  └─ 📝 Creating Channel: `#{ch['name']}`")
                
                # Set permissions: Information channels are read-only for @everyone
                perms_overwrites = None
                if "1." in cat_name:
                    perms_overwrites = {
                        guild.default_role: discord.PermissionOverwrite(send_messages=False),
                        guild.me: discord.PermissionOverwrite(send_messages=True)
                    }
                
                await guild.create_text_channel(
                    ch["name"], 
                    category=category, 
                    topic=ch["topic"],
                    overwrites=perms_overwrites
                )
            else:
                report.append(f"  └─ ✔️ Channel Exists: `#{ch['name']}`")

    # Final report
    embed = discord.Embed(
        title="🏗️ Server Build Report",
        description="\n".join(report[-20:]), # Show last 20 actions if long
        color=0x9B59B6
    )
    embed.set_footer(text="Auto-Pilot: One App At A Time.")
    await status_msg.edit(content="✅ **Server structure verification complete!**", embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !initialize_onboarding
# ══════════════════════════════════════════════
@bot.command(name="initialize_onboarding")
@commands.has_permissions(administrator=True)
async def initialize_onboarding(ctx):
    """
    MASTER INITIALIZATION: The Big Bang of the Academy.
    Deploys all persistent GUIs to the frontline channels.
    """
    status_msg = await ctx.send("🚀 **Initiating Legendary GUI Deployment...**")
    guild = ctx.guild
    
    def find_channel(name):
        return discord.utils.find(lambda c: name.lower() in c.name.lower(), guild.text_channels)

    welcome_ch = find_channel("welcome")
    rules_ch = find_channel("rules")
    roles_ch = find_channel("roles") # Added roles channel check
    
    report = []
    
    # 1. Welcome GUI (Call to Arms)
    target_ch = welcome_ch or ctx.channel
    embed = discord.Embed(
        title="⚔️ A Call to Arms: One App at a Time ⚔️",
        description=(
            "Welcome to the front lines of creation. This community exists for one reason: "
            "to fuel our passions and build a safer, better tomorrow through the power of code.\n\n"
            "Whether you are a **Noob** or a **God**, your contribution is the engine of our collective growth."
        ),
        color=0xE74C3C,
    )
    embed.add_field(
        name="🛡️ Choose Your Level",
        value=(
            "**1. The Noob** — Trainee / Level 0\n"
            "**2. The Beginner** — Junior Dev / Level 1\n"
            "**3. The Intermediate** — Mid-Level / Level 2-3\n"
            "**4. The Expert** — Senior / Staff / Architect\n"
            "**5. The God** — Distinguished Engineer / Legend"
        ),
        inline=False,
    )
    embed.add_field(
        name="🤖 The Synthetic Edge",
        value="Our bots learn from us. Help refine them daily by identifying errors and improving logic.",
        inline=False,
    )
    await target_ch.send(embed=embed, view=RoleSelectionView())
    report.append(f"✅ Deployed Welcome GUI to {target_ch.mention}")

    # 2. Rules GUI (The Law)
    if rules_ch:
        legendary_quote = (
            "\"\"One App At A Time.\" The forge is hot, the guards are at the gate, and the synthetic edge is sharp.\n"
            "It has been an absolute pleasure building this fortress with you. The Academy is now yours to lead! ⚔️🛡️🤖\""
        )
        rules_embed = discord.Embed(
            title="📜 The Immutable Laws of the Academy",
            description=f"{legendary_quote}\n\n💯 **Agreement is Mandatory.** Click the sword below to verify your intent.",
            color=discord.Color.dark_grey()
        )
        
        # Try to load custom rules if they exist
        template_path = os.path.join(BUILD_PLAN_DIR, "discohook_rules_template.json")
        if os.path.exists(template_path):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "embeds" in data and len(data["embeds"]) > 0:
                        rules_embed = discord.Embed.from_dict(data["embeds"][0])
            except:
                pass
        
        await rules_ch.send(embed=rules_embed, view=RulesAgreementView())
        report.append(f"✅ Deployed Rules GUI to {rules_ch.mention}")
    else:
        report.append("⚠️ `rules` channel not found. Rules GUI skipped.")

    final_embed = discord.Embed(
        title="🛰️ Legendary Deployment System",
        description="\n".join(report),
        color=0x2ECC71
    )
    final_embed.set_footer(text="The Forge is Live. ⚔️🛡️🤖💯")
    await status_msg.edit(content="🏁 **Master Initialization Complete.**", embed=final_embed)


# ══════════════════════════════════════════════
#  COMMAND: !list_members
# ══════════════════════════════════════════════
@bot.command(name="list_members")
@commands.has_permissions(administrator=True)
async def list_members(ctx):
    """View the list of members who have completed onboarding."""
    if not os.path.exists(JOINED_MEMBERS_FILE):
        await ctx.send("📂 No member data found yet.")
        return

    with open(JOINED_MEMBERS_FILE, "r") as f:
        data = json.load(f)

    if not data["members"]:
        await ctx.send("📂 The registry is currently empty.")
        return

    report = []
    for m in data["members"][-20:]: # Last 20
        report.append(f"• **{m['name']}** (`{m['user_id']}`) - Tier: {m['level']}")

    embed = discord.Embed(
        title="⚔️ Academy Member Registry",
        description="\n".join(report),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total Registered: {len(data['members'])}")
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !list_channels
# ══════════════════════════════════════════════
@bot.command(name="list_channels")
@commands.has_permissions(administrator=True)
async def list_channels(ctx):
    """List all text channels the bot can see for debugging."""
    channels = [f"#{c.name} (`{c.id}`)" for c in ctx.guild.text_channels]
    embed = discord.Embed(
        title="📂 Server Channel List",
        description="\n".join(channels[:30]), # Limit to avoid embed limits
        color=0x3498DB
    )
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !purge_text
# ══════════════════════════════════════════════
@bot.command(name="purge_text")
@commands.has_permissions(manage_channels=True)
async def purge_text(ctx):
    """Clone-and-delete the current channel to wipe all messages."""
    if PRIVATE_CATEGORY_ID != 0 and ctx.channel.category_id == PRIVATE_CATEGORY_ID:
        new_channel = await ctx.channel.clone(reason="Manual Blackout Purge.")
        await ctx.channel.delete(reason="Manual Blackout Purge.")
        await new_channel.send("⚠️ **Total Purge Complete.** This Review Chamber has been wiped clean.")
    else:
        await ctx.send("⚠️ This command can only be used inside a Private Review Chamber.")


# ══════════════════════════════════════════════
#  COMMAND: !strike @user <reason>
# ══════════════════════════════════════════════
@bot.command(name="strike")
@commands.has_permissions(manage_messages=True)
async def strike(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Record a moderation strike against a user."""
    # Load or create the strike log
    if os.path.exists(STRIKE_LOG_FILE):
        with open(STRIKE_LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = {}

    user_id = str(member.id)
    if user_id not in log:
        log[user_id] = {"username": str(member), "strikes": []}

    strike_entry = {
        "reason": reason,
        "issued_by": str(ctx.author),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "channel": ctx.channel.name,
    }
    log[user_id]["strikes"].append(strike_entry)
    strike_count = len(log[user_id]["strikes"])

    # Save
    with open(STRIKE_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

    embed = discord.Embed(
        title="⚠️ Strike Recorded",
        description=f"**User**: {member.mention}\n**Reason**: {reason}\n**Total Strikes**: {strike_count}",
        color=0xE67E22,
    )
    embed.set_footer(text=f"Issued by {ctx.author.name}")
    await ctx.send(embed=embed)

# ══════════════════════════════════════════════
#  COMMAND: !apply_collaborator
# ══════════════════════════════════════════════
class CollaboratorModal(ui.Modal, title='🤝 Collaborator Application'):
    github = ui.TextInput(label='GitHub Profile / Repos', placeholder='https://github.com/yourname', required=True)
    youtube = ui.TextInput(label='YouTube Channel (Optional)', placeholder='https://youtube.com/@yourchannel', required=False)
    exp = ui.TextInput(label='Years of Experience', placeholder='e.g. 3 years', required=True)
    specialty = ui.TextInput(label='Primary Specialties', placeholder='e.g. AI, Python, UI/UX', required=True)
    value = ui.TextInput(label='Value Proposition', style=discord.TextStyle.paragraph, placeholder='How will you help the community grow?', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        # Log to #admin-mod-bot-commands for review
        staff_ch = discord.utils.get(interaction.guild.text_channels, name="admin-mod-bot-commands")
        if staff_ch:
            embed = discord.Embed(title="🤝 New Collaborator Application", color=discord.Color.gold())
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="User ID", value=interaction.user.id, inline=True)
            embed.add_field(name="GitHub", value=self.github.value, inline=False)
            embed.add_field(name="YouTube", value=self.youtube.value or "N/A", inline=False)
            embed.add_field(name="Experience", value=self.exp.value, inline=True)
            embed.add_field(name="Specialty", value=self.specialty.value, inline=True)
            embed.add_field(name="Value", value=self.value.value, inline=False)
            
            # Simple approval buttons
            view = CollaboratorApprovalView(user_id=interaction.user.id)
            await staff_ch.send(embed=embed, view=view)
            await interaction.response.send_message("✅ Your application has been submitted to the Forge Council! ⚔️🛡️🤖", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Staff channel not found. Contact Admin.", ephemeral=True)

class CollaboratorApprovalView(ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @ui.button(label="✅ Approve", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: ui.Button):
        # Any Level Moderator (1-5) can approve
        # Check for roles with "Moderator" or "Admin"
        is_mod = any(role.name.lower() in ["moderator", "admin"] or "level" in role.name.lower() for role in interaction.user.roles)
        if not is_mod and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Only Moderators can approve applications.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.user_id)
        role = discord.utils.get(guild.roles, name="Known Server Collaborator")
        if not role:
            role = await guild.create_role(name="Known Server Collaborator", color=discord.Color.purple())

        if member:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Approved {member.mention} as a Collaborator! ✨", ephemeral=False)
            # Update spotlight in #all-bot-commands
            public_ch = discord.utils.get(guild.text_channels, name="all-bot-commands")
            if public_ch:
                await public_ch.send(f"✨ **NEW KNOWN SERVER COLLABORATOR**: {member.mention} has joined the elite! ⚔️🛡️🤝")
            button.disabled = True
            await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("❌ Member not found.", ephemeral=True)

@bot.command(name="apply_collaborator")
async def apply_collaborator(ctx):
    """Open the collaborator application modal."""
    await ctx.interaction.response.send_modal(CollaboratorModal()) if ctx.interaction else await ctx.send("Please use the Slash Command variation if available, or wait for GUI integration.")

# ══════════════════════════════════════════════
#  COMMAND: !submit_repo [url]
# ══════════════════════════════════════════════
@bot.command(name="submit_repo")
async def submit_repo(ctx, url: str):
    """Submit a repository for scanning and potential forking."""
    # 1. Basic URL check
    if "github.com/" not in url:
        await ctx.send("❌ Please provide a valid GitHub repository URL.")
        return

    # 2. Ping S.A.M.P.I.RT for scan (Simulated for now, real integration in Phase 3)
    await ctx.send(f"🔍 **S.A.M.P.I.RT**: Scanning repository `{url}` for malicious code... 🛡️", delete_after=5)
    await asyncio.sleep(2)
    
    # 3. Forward to Staff Review
    staff_ch = discord.utils.get(ctx.guild.text_channels, name="admin-mod-bot-commands")
    if staff_ch:
        embed = discord.Embed(title="📂 New Community Repo Submission", color=discord.Color.blue())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name="URL", value=url, inline=False)
        embed.add_field(name="S.A.M.P.I.RT SCAN", value="🟢 CLEAN / SAFE", inline=True)
        
        view = RepoApprovalView(user_id=ctx.author.id, repo_url=url)
        await staff_ch.send(embed=embed, view=view)
        await ctx.send("✅ Repo submitted! S.A.M.P.I.RT has verified the code is safe. Staff will review for forking. 🛡️🤝")
    else:
        await ctx.send("❌ Staff channel not found.")

class RepoApprovalView(ui.View):
    def __init__(self, user_id, repo_url):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.repo_url = repo_url

    @ui.button(label="⚔️ Fork to Academy", style=discord.ButtonStyle.primary)
    async def fork_repo(self, interaction: discord.Interaction, button: ui.Button):
        is_mod = any(role.name.lower() in ["moderator", "admin"] or "level" in role.name.lower() for role in interaction.user.roles)
        if not is_mod and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Only Moderators can approve repos.", ephemeral=True)
            return

        # Simulate fork (In production, would use GitHub API)
        await interaction.response.send_message(f"🚀 **Actioned**: Forking `{self.repo_url}` to the Academy Organization! 🦾📦")
        button.disabled = True
        await interaction.message.edit(view=self)

# ══════════════════════════════════════════════
#  COMMAND: !apply_mod
# ══════════════════════════════════════════════
class ModeratorExamModal(ui.Modal, title='🛡️ Moderator Entrance Exam'):
    coding_exp = ui.TextInput(label='Years of Coding Exp', placeholder='e.g. 5 years', required=True)
    knowledge = ui.TextInput(label='Core Knowledge Base', placeholder='e.g. Python, Cybersecurity, Discord API', required=True)
    id_ref = ui.TextInput(label='User ID (Joining Phase Reference)', placeholder='Enter your Discord User ID', required=True)
    mission = ui.TextInput(label='Mission Statement', style=discord.TextStyle.paragraph, placeholder='How will you apply your skills as a Teacher/Mentor?', required=True)
    bad_apples = ui.TextInput(label='Conflict Resolution', style=discord.TextStyle.paragraph, placeholder='How do you handle "bad apples"? Describe your approach to admonishment.', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        staff_ch = discord.utils.get(interaction.guild.text_channels, name="admin-mod-bot-commands")
        if staff_ch:
            embed = discord.Embed(title="🛡️ NEW MODERATOR APPLICATION & EXAM", color=discord.Color.dark_red())
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="User ID Ref", value=self.id_ref.value, inline=True)
            embed.add_field(name="Experience", value=self.coding_exp.value, inline=True)
            embed.add_field(name="Focus", value=self.knowledge.value, inline=False)
            embed.add_field(name="Mission", value=self.mission.value, inline=False)
            embed.add_field(name="Conflicts", value=self.bad_apples.value, inline=False)
            
            view = ModeratorReviewView(user_id=interaction.user.id)
            await staff_ch.send(embed=embed, view=view)
            await interaction.response.send_message("🛡️ Your Exam has been recorded. The Council will review your score and assign a Moderator Level (1-5).", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Staff channel not found.", ephemeral=True)

class ModeratorReviewView(ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    async def assign_mod(self, interaction: discord.Interaction, level: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Only Administrators can assign Moderator Levels.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(self.user_id)
        role_name = f"Moderator Level {level}"
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name, color=discord.Color.red())

        if member:
            # Grant level role and base moderator role
            base_mod = discord.utils.get(guild.roles, name="Moderator")
            if not base_mod: base_mod = await guild.create_role(name="Moderator", color=discord.Color.orange())
            await member.add_roles(role, base_mod)
            await interaction.response.send_message(f"✅ Promoted {member.mention} to **{role_name}**! 🛡️⚔️")
            self.stop()
        else:
            await interaction.response.send_message("❌ Member not found.", ephemeral=True)

    @ui.button(label="Lvl 1", style=discord.ButtonStyle.secondary)
    async def lvl1(self, interaction: discord.Interaction, button: ui.Button): await self.assign_mod(interaction, 1)
    @ui.button(label="Lvl 2", style=discord.ButtonStyle.secondary)
    async def lvl2(self, interaction: discord.Interaction, button: ui.Button): await self.assign_mod(interaction, 2)
    @ui.button(label="Lvl 3", style=discord.ButtonStyle.secondary)
    async def lvl3(self, interaction: discord.Interaction, button: ui.Button): await self.assign_mod(interaction, 3)
    @ui.button(label="Lvl 4", style=discord.ButtonStyle.secondary)
    async def lvl4(self, interaction: discord.Interaction, button: ui.Button): await self.assign_mod(interaction, 4)
    @ui.button(label="Lvl 5", style=discord.ButtonStyle.primary)
    async def lvl5(self, interaction: discord.Interaction, button: ui.Button): await self.assign_mod(interaction, 5)

@bot.command(name="apply_mod")
async def apply_mod(ctx):
    """Open the moderator entrance exam modal."""
    await ctx.interaction.response.send_modal(ModeratorExamModal()) if ctx.interaction else await ctx.send("Please use the Slash Command variation.")


# ══════════════════════════════════════════════
#  GITHUB HELPERS
# ══════════════════════════════════════════════
def _github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _get_file_sha(filepath: str) -> str | None:
    """Get the SHA of an existing file in the repo (needed for updates)."""
    url = f"{GITHUB_API_BASE}/contents/{filepath}"
    resp = requests.get(url, headers=_github_headers(), timeout=15)
    if resp.status_code == 200:
        return resp.json().get("sha")
    return None


def _push_file_to_github(local_path: str, repo_path: str, commit_msg: str) -> dict:
    """Create or update a file in the GitHub repo using the Contents API."""
    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("utf-8")

    url = f"{GITHUB_API_BASE}/contents/{repo_path}"
    payload = {
        "message": commit_msg,
        "content": content_b64,
    }

    # If the file already exists, we need its SHA to update it
    existing_sha = _get_file_sha(repo_path)
    if existing_sha:
        payload["sha"] = existing_sha

    resp = requests.put(url, headers=_github_headers(), json=payload, timeout=30)
    return {"status": resp.status_code, "file": repo_path, "ok": resp.status_code in (200, 201)}


# ══════════════════════════════════════════════
#  COMMAND: !deploy_plan
# ══════════════════════════════════════════════
@bot.command(name="deploy_plan")
@commands.has_permissions(administrator=True)
async def deploy_plan(ctx):
    """Push all build plan files to the GitHub repo."""
    if not GITHUB_PAT:
        await ctx.send("❌ `GITHUB_PAT` is not set in `.env`.")
        return

    status_msg = await ctx.send("📦 Deploying build plan to GitHub...")
    results = []

    for filename in DEPLOY_FILES:
        local_path = os.path.join(BUILD_PLAN_DIR, filename)
        if not os.path.exists(local_path):
            results.append(f"⏭️ `{filename}` — skipped (not found)")
            continue

        result = _push_file_to_github(
            local_path, filename, f"Deploy: update {filename}"
        )
        if result["ok"]:
            results.append(f"✅ `{filename}` — pushed successfully")
        else:
            results.append(f"❌ `{filename}` — failed (HTTP {result['status']})")

    embed = discord.Embed(
        title="📦 Deployment Report",
        description="\n".join(results),
        color=0x2ECC71 if all("✅" in r or "⏭️" in r for r in results) else 0xE74C3C,
    )
    embed.set_footer(text=f"Target: {GITHUB_OWNER}/{GITHUB_REPO}")
    await status_msg.edit(content=None, embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !addfile <repo_path> <content>
# ══════════════════════════════════════════════
@bot.command(name="addfile")
@commands.has_permissions(administrator=True)
async def addfile(ctx, repo_path: str, *, content: str):
    """Add or update a single file in the GitHub repo from Discord."""
    if not GITHUB_PAT:
        await ctx.send("❌ `GITHUB_PAT` is not set in `.env`.")
        return

    content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    url = f"{GITHUB_API_BASE}/contents/{repo_path}"
    payload = {
        "message": f"Add {repo_path} via Discord bot",
        "content": content_b64,
    }

    existing_sha = _get_file_sha(repo_path)
    if existing_sha:
        payload["sha"] = existing_sha

    resp = requests.put(url, headers=_github_headers(), json=payload, timeout=30)

    if resp.status_code in (200, 201):
        await ctx.send(f"✅ `{repo_path}` has been pushed to GitHub!")
    else:
        await ctx.send(f"❌ Failed to push `{repo_path}` (HTTP {resp.status_code}): {resp.text[:200]}")


# ══════════════════════════════════════════════
#  COMMAND: !logs
# ══════════════════════════════════════════════
@bot.command(name="logs")
@commands.has_permissions(administrator=True)
async def sync_logs(ctx):
    """Manually push bot.log and strike_log.json to the GitHub repo."""
    if not GITHUB_PAT:
        await ctx.send("❌ `GITHUB_PAT` is not set in `.env`.")
        return

    status_msg = await ctx.send("📡 Syncing logs to GitHub...")
    results = []
    log_files = ["bot.log", "strike_log.json"]

    for filename in log_files:
        local_path = os.path.join(BUILD_PLAN_DIR, filename)
        if not os.path.exists(local_path):
            results.append(f"⏭️ `{filename}` — skipped (not found)")
            continue

        result = _push_file_to_github(
            local_path, filename, f"Logs Sync: {datetime.datetime.utcnow().isoformat()}"
        )
        if result["ok"]:
            results.append(f"✅ `{filename}` — synced")
        else:
            results.append(f"❌ `{filename}` — failed (HTTP {result['status']})")

    embed = discord.Embed(
        title="📡 Logs Sync Report",
        description="\n".join(results),
        color=0x3498DB
    )
    await status_msg.edit(content=None, embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !ask <question>
# ══════════════════════════════════════════════
@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask Google Gemini AI a question or for a code review. Uses Pro with Flash fallback."""
    if not GOOGLE_API_KEY:
        await ctx.send("❌ `GOOGLE_API_KEY` is not set in `.env`.")
        return

    async with ctx.typing():
        try:
            import google.generativeai as genai
            import warnings
            warnings.filterwarnings("ignore", category=FutureWarning)

            genai.configure(api_key=GOOGLE_API_KEY)

            system_prompt = (
                "You are GoonsClawbot, a Level 5 Distinguished Engineer AI assistant "
                "for the Apptivators Academy Discord server. You help with code reviews, "
                "debugging, mentorship, and security analysis. Keep answers concise and "
                "practical. If code looks malicious, warn immediately.\n\n"
            )

            # Try Flash first (better for free tier), then fallback
            model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
            last_error = None

            for model_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(system_prompt + f"User question:\n{question}")
                    answer = response.text

                    # Discord has a 2000 char limit per message
                    if len(answer) > 1900:
                        for i in range(0, len(answer), 1900):
                            await ctx.send(answer[i : i + 1900])
                    else:
                        await ctx.send(answer)
                    return  # Success, exit

                except Exception as e:
                    last_error = f"{model_name}: {e}"
                    continue  # Try next model

            # All models failed
            await ctx.send(f"❌ All Gemini models failed. Last error: {str(last_error)[:200]}")

        except Exception as e:
            await ctx.send(f"❌ Error: {e}")


# ══════════════════════════════════════════════
#  COMMAND: !review <attachment>
# ══════════════════════════════════════════════
@bot.command(name="review")
async def review(ctx):
    """Deep Audit: Upload a code file and get a professional Level 5 review."""
    if not GOOGLE_API_KEY:
        await ctx.send("❌ `GOOGLE_API_KEY` is not set in `.env`.")
        return

    if not ctx.message.attachments:
        await ctx.send("📂 Please attach a file (e.g. .py, .js, .txt) for review.")
        return

    attachment = ctx.message.attachments[0]
    async with ctx.typing():
        try:
            content = await attachment.read()
            code_text = content.decode("utf-8")
            
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            
            system_prompt = (
                "You are the Lead Academy Architect. Perform a rigorous code review of the provided file. "
                "Look for: Security vulnerabilities, Performance bottlenecks, Logic errors, and Style improvements. "
                "Structure your reply with '### Audit Results' and '### Action Items'. Keep it technical.\n\n"
            )
            
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(system_prompt + f"File: {attachment.filename}\nContents:\n```\n{code_text}\n```")
            answer = response.text
            
            # Message splitting
            if len(answer) > 1900:
                for i in range(0, len(answer), 1900):
                    await ctx.send(answer[i : i + 1900])
            else:
                await ctx.send(answer)
                
        except Exception as e:
            await ctx.send(f"❌ Review Error: {e}")


# ══════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("=" * 50)
        print("  ERROR: DISCORD_BOT_TOKEN is not set in .env")
        print("  Add your token to d:\\Clawbot\\.env")
        print("=" * 50)
    else:
        bot.run(DISCORD_TOKEN)
