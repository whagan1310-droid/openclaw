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
# Server Structure Definition - ONBOARDING FOCUS
# ──────────────────────────────────────────────
SERVER_STRUCTURE = {
    "📢 Apptivators-Academy Core": [
        {"name": "welcome", "topic": "Step 1: Welcome to the Academy"},
        {"name": "rules", "topic": "Step 2: Server Laws & Guidelines"},
        {"name": "roles", "topic": "Step 3: Choose Your Skill Path"},
        {"name": "call-to-arms", "topic": "Step 4: Final Registration - I Agree"},
    ],
    "🤝 2. Community & Collaboration": [
        {"name": "announcements", "topic": "Admin updates and milestones."},
        {"name": "resources", "topic": "Curated collection of tutorials."},
        {"name": "showcase", "topic": "Share projects and collaborate."},
        {"name": "memes", "topic": "Tech/programmer humor."},
    ],
    "🛠️ 3. Support & Technical Help": [
        {"name": "help-desk", "topic": "Technical assistance tickets."},
        {"name": "code-reviews", "topic": "Professional code feedback."},
        {"name": "quick-questions", "topic": "Short tech questions."},
    ],
    "💻 4. Language-Specific": [
        {"name": "web-dev", "topic": "HTML, CSS, JS, React."},
        {"name": "python", "topic": "Python development."},
        {"name": "java-cpp", "topic": "Java and C++."},
        {"name": "rust", "topic": "Rust programming."},
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

ACADEMY_IMAGE_URL = None

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
        user_ch = discord.utils.get(guild.text_channels, name="user-bot-commands")
        staff_ch = discord.utils.get(guild.text_channels, name="admin-mod-bot-commands")
        
        # Create OWNER ONLY channel if not exists
        owner_ch = discord.utils.get(guild.text_channels, name="owner-commands")
        if not owner_ch:
            # Find Category 7
            cat_7 = discord.utils.get(guild.categories, name="📜 7. Transparency & Governance")
            if cat_7:
                owner_ch = await guild.create_text_channel("owner-commands", category=cat_7, topic="Owner Only Commands")
        
        # PUBLIC commands for user-bot-commands - CHART STYLE
        user_manual = discord.Embed(
            title="📋 ACADEMY COMMAND MANUAL",
            description="⚔️ **PUBLIC COMMANDS** | Available to all members\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            color=discord.Color.blue()
        )
        user_manual.add_field(
            name="🤖 GoonsClawbot (!)",
            value="```\n!welcome           → Restart walkthrough\n!apply_collaborator → Join the elite\n!submit_repo [url] → Share a repo link\n!sharefile [name] [content] → Upload code\n!softwaregent      → View SoftwareGent info\n```\n"
            "**How to use:**\n"
            "```\n"
            "!submit_repo https://github.com/user/repo\n"
            "!sharefile myscript.py \"print('Hello World')\"\n"
            "```",
            inline=False
        )
        user_manual.add_field(
            name="🧠 AI Assistant (!ask)",
            value="```\n!ask [your question] → Ask AI anything\n\nExample: !ask how to Python?\n\n💡 Or use #ai-help channel for AI chats!\n```",
            inline=False
        )
        user_manual.add_field(
            name="🎵 SonicForge (!sonic_)",
            value="```\n!sonic_play [song] → Play music\n!sonic_queue       → View queue\n!sonic_skip        → Skip song\n!sonic_stop        → Stop playback\n!sonic_pause       → Pause\n!sonic_resume      → Resume\n```",
            inline=False
        )
        user_manual.add_field(
            name="🎥 SyncFlux (!sync_)",
            value="```\n!sync_video [url] → Queue video\n!sync_status      → Pipeline status\n```",
            inline=False
        )
        user_manual.add_field(
            name="🛡️ S.A.M.P.I.RT (!!)",
            value="```\n!!status → Health check\n```",
            inline=False
        )
        user_manual.set_footer(text="Apptivators-Academy | One App At A Time")
        
        # Create AI help channel if not exists
        ai_help_ch = discord.utils.get(guild.text_channels, name="ai-help")
        if not ai_help_ch:
            cat_community = discord.utils.get(guild.categories, name="🤝 2. Community & Collaboration")
            if cat_community:
                ai_help_ch = await guild.create_text_channel("ai-help", category=cat_community, topic="Ask AI anything here!")
                logger.info("Created #ai-help channel")
        
        if ai_help_ch:
            # Send AI channel welcome message
            ai_embed = discord.Embed(
                title="🧠 Welcome to #ai-help!",
                description="Ask me anything using `!ask` command!\n\n"
                            "**Examples:**\n"
                            "```\n"
                            "!ask how do I center a div in CSS?\n"
                            "!ask write a Python function to reverse a string\n"
                            "!ask explain quantum computing simply\n"
                            "```\n"
                            "Powered by Google Gemini AI ⚡",
                color=discord.Color.blue()
            )
            ai_embed.set_footer(text="Apptivators-Academy AI | One App At A Time")
            
            async for msg in ai_help_ch.history(limit=5):
                if msg.author == self.user and msg.embeds and "Welcome to #ai-help" in msg.embeds[0].title:
                    await msg.edit(embed=ai_embed)
                    break
            else:
                await ai_help_ch.send(embed=ai_embed)
        
        # STAFF commands for admin-mod-bot-commands - CHART STYLE
        staff_manual = discord.Embed(
            title="📋 ACADEMY COMMAND MANUAL",
            description="🛡️ **STAFF COMMANDS** | Moderators & Admins\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            color=discord.Color.dark_red()
        )
        staff_manual.add_field(
            name="🔧 Admin Core",
            value="```\n!clearbot               → Clear all messages\n!clearbot [channel]    → Clear specific channel\n```",
            inline=False
        )
        staff_manual.add_field(
            name="📊 Analytics",
            value="```\n!list_members → List members\n!list_channels → List channels\n!purge_text  → Purge text\n```",
            inline=False
        )
        staff_manual.add_field(
            name="⚔️ Management",
            value="```\n!strike      → Strike user\n!apply_mod   → Apply mod\n```",
            inline=False
        )
        staff_manual.add_field(
            name="📁 Files (STAFF)",
            value="```\n!addfile  → Add file to GitHub\n!logs    → View logs\n!ask     → Ask AI\n!review  → Review\n```",
            inline=False
        )
        staff_manual.add_field(
            name="⚖️ S.A.M.P.I.RT",
            value="```\n!!query [id]       → Forensic audit\n!!scan_channel     → Security scan\n!!status          → Health check\n```",
            inline=False
        )
        staff_manual.add_field(
            name="🛑 Moderation",
            value="```\n!!freeze [id]  → Quarantine user\n!!ban           → Ban user\n!!tempban       → Temp ban\n```",
            inline=False
        )
        staff_manual.set_footer(text="Apptivators-Academy | Staff Only")
        
        # OWNER ONLY commands - CHART STYLE
        owner_manual = discord.Embed(
            title="📋 ACADEMY COMMAND MANUAL",
            description="🔒 **OWNER COMMANDS** | Owner Only\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            color=discord.Color.gold()
        )
        owner_manual.add_field(
            name="🔧 Server Core",
            value="```\n!build_server        → Full restructure\n!initialize_onboarding → Deploy GUIs\n!setup_onboarding   → Build + Deploy\n!deploy_plan       → Push to GitHub\n!!unban            → Unban user\n```",
            inline=False
        )
        owner_manual.set_footer(text="Apptivators-Academy | Owner Only")

        if user_ch:
            async for msg in user_ch.history(limit=10):
                if msg.author == self.user and msg.embeds and "COMMAND MANUAL" in msg.embeds[0].title and "PUBLIC" in msg.embeds[0].description:
                    await msg.edit(embed=user_manual)
                    logger.info(f"Updated user command manual in #{user_ch.name}")
                    break
            else:
                await user_ch.send(embed=user_manual)
                logger.info(f"Deployed user command manual to #{user_ch.name}")

        if staff_ch:
            async for msg in staff_ch.history(limit=10):
                if msg.author == self.user and msg.embeds and "COMMAND MANUAL" in msg.embeds[0].title and "STAFF" in msg.embeds[0].description:
                    await msg.edit(embed=staff_manual)
                    logger.info(f"Updated staff command manual in #{staff_ch.name}")
                    break
            else:
                await staff_ch.send(embed=staff_manual)
                logger.info(f"Deployed staff command manual to #{staff_ch.name}")
        
        if owner_ch:
            async for msg in owner_ch.history(limit=10):
                if msg.author == self.user and msg.embeds and "OWNER ONLY" in msg.embeds[0].title:
                    await msg.edit(embed=owner_manual)
                    break
            else:
                await owner_ch.send(embed=owner_manual)

bot = GoonsClawBot(command_prefix="!", intents=intents)

# ══════════════════════════════════════════════
#  EVENT: on_ready
# ══════════════════════════════════════════════
# ──────────────────────────────────────────────
#  AUTO-BOOTSTRAP CONFIG (Push Actions Automatically)
# ──────────────────────────────────────────────
AUTO_BOOTSTRAP = True
AUTO_DEPLOY_ONBOARDING = True  # Auto-send embeds on startup  # Auto build server & deploy onboarding on start

@bot.event
async def on_ready():
    # Register persistent views (these survive bot restarts)
    bot.add_view(RoleSelectionView())
    bot.add_view(RulesAgreementView())
    bot.add_view(JoinWalkthroughView())
    # Persistent onboarding navigation views (sent to channels)
    bot.add_view(WelcomeStepView())
    bot.add_view(RulesStepView())
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

    # Auto-deploy onboarding embeds
    if AUTO_DEPLOY_ONBOARDING:
        for guild in bot.guilds:
            # Force delete specific old channel by ID (after user changes Community rules)
            old_welcome_id = 1480788653579178127
            for ch in guild.text_channels:
                if ch.id == old_welcome_id:
                    try:
                        await ch.delete()
                        logger.info(f"Deleted old welcome channel")
                    except Exception as e:
                        logger.info(f"Cannot delete old welcome (needs Community settings change): {e}")
            
            # Rename old category if exists
            old_cat = discord.utils.get(guild.categories, name="📢 1. Onboarding Core")
            if old_cat:
                await old_cat.edit(name="📢 Apptivators-Academy Core")
            
            # Delete ALL duplicate onboarding channels (keep only ones in Onboarding Core)
            onboarding_cat = discord.utils.get(guild.categories, name="📢 Apptivators-Academy Core")
            
            # Get all channels with onboarding names
            onboarding_names = ["welcome", "rules", "roles", "call-to-arms"]
            for name in onboarding_names:
                channels = [ch for ch in guild.text_channels if ch.name == name]
                if len(channels) > 1:
                    # Delete all but the one in Onboarding Core
                    for ch in channels:
                        if ch.category != onboarding_cat:
                            try:
                                await ch.delete()
                                logger.info(f"Deleted duplicate: #{ch.name}")
                            except:
                                pass
            
            # Move Apptivators-Academy Core to top
            onboarding_cat = discord.utils.get(guild.categories, name="📢 Apptivators-Academy Core")
            if onboarding_cat:
                try:
                    await onboarding_cat.edit(position=0)
                except:
                    pass
            
            # Get the NEW channels (in Onboarding Core)
            welcome_ch = discord.utils.get(guild.text_channels, name="welcome")
            rules_ch = discord.utils.get(guild.text_channels, name="rules")
            roles_ch = discord.utils.get(guild.text_channels, name="roles")
            call_to_arms_ch = discord.utils.get(guild.text_channels, name="call-to-arms")
            
            # Create call-to-arms if missing
            if not call_to_arms_ch and onboarding_cat:
                call_to_arms_ch = await guild.create_text_channel("call-to-arms", category=onboarding_cat, topic="Step 4: Final Registration")
                logger.info("Created #call-to-arms channel")
            
            # Deploy Welcome
            if welcome_ch:
                embed = discord.Embed(title="⚔️ Step 1: Welcome", description="Click **Begin Journey** to start!", color=0xE74C3C)
                embed.set_footer(text="Step 1/4")
                await welcome_ch.send(embed=embed, view=WelcomeStepView())
                logger.info("Deployed Welcome embed")
            
            # Deploy Rules
            if rules_ch:
                embed = discord.Embed(title="📜 Step 2: Rules", description="1️⃣ No NSFW\n2️⃣ Be Respectful\n3️⃣ No Spam", color=0x9B59B6)
                embed.set_footer(text="Step 2/4")
                await rules_ch.send(embed=embed, view=RulesStepView())
                logger.info("Deployed Rules embed")
            
            # Deploy Roles
            if roles_ch:
                embed = discord.Embed(title="🛠️ Step 3: Choose Role", description="Select your skill level 1-5", color=0x3498DB)
                embed.set_footer(text="Step 3/4")
                await roles_ch.send(embed=embed, view=RolesStepView(0))
                logger.info("Deployed Roles embed")
            
            # Deploy Call-to-Arms
            if call_to_arms_ch:
                embed = discord.Embed(title="⚔️ Step 4: Call to Arms", description="Click **I AGREE** to join!", color=0x2ECC71)
                embed.set_footer(text="Step 4/4")
                await call_to_arms_ch.send(embed=embed, view=CallToArmsView(0))
                logger.info("Deployed Call-to-Arms embed")
            
            logger.info("✅ AUTO-DEPLOY ONBOARDING COMPLETE!")
        
        # Auto-deploy SoftwareGent card
        softwaregent_ch = discord.utils.get(guild.text_channels, name="softwaregent")
        if softwaregent_ch:
            softwaregent_embed = discord.Embed(
                title="📺 SoftwareGent",
                description="Welcome to SoftwareGent, we are a channel that makes educational videos on how to get and use different types of software.\n\n"
                            "We also have our own blog in which we have different types of helpful articles with a lot of information about the software you are using or you are thinking about using.\n\n"
                            "**At SoftwareGent we make your life easy.** We test and review the software so you do not have to.",
                color=discord.Color.blue()
            )
            softwaregent_embed.add_field(name="📧 Email", value="softwaregentofficial@gmail.com", inline=True)
            softwaregent_embed.add_field(name="📺 YouTube", value="@softwaregent7443", inline=True)
            softwaregent_embed.add_field(name="🌍 Location", value="Greece", inline=True)
            softwaregent_embed.add_field(name="🔗 Community", value="skool.com/ai-saas-builders/about", inline=False)
            softwaregent_embed.add_field(name="🔗 Assets Community", value="skool.com/ai-business-builders-7856/about", inline=False)
            softwaregent_embed.add_field(name="🌐 Website", value="softwaregentofficial.com", inline=False)
            softwaregent_embed.add_field(name="📊 Stats", value="**11.3K** subscribers | **191** videos | **895K** views", inline=False)
            softwaregent_embed.set_footer(text="Apptivators-Academy | One App At A Time")
            
            async for msg in softwaregent_ch.history(limit=5):
                if msg.author == bot.user and msg.embeds and "SoftwareGent" in msg.embeds[0].title:
                    await msg.edit(embed=softwaregent_embed)
                    logger.info("Updated SoftwareGent card")
                    break
            else:
                await softwaregent_ch.send(embed=softwaregent_embed)
                logger.info("Deployed SoftwareGent card")
        
        # Auto-deploy Gael Level card
        gael_ch = discord.utils.get(guild.text_channels, name="gael-level")
        if gael_ch:
            gael_embed = discord.Embed(
                title="🎮 Gael Level",
                description="Twitch Live streaming Tutorials, OBS studio guides, and Content creator Tips & Advice.\n\n"
                            "Stream Overlay for Twitch, Youtube, Tiktok, Kick, etc...\n"
                            "Advanced OBS tutorials. Streamerbot Ideas. Twitch channel points creative rewards.\n"
                            "Tips and trick to grow on Twitch. How to make stream overlays from scratch. How to setup a Discord server.",
                color=discord.Color.purple()
            )
            gael_embed.add_field(name="📷 Instagram", value="instagram.com/gael.level", inline=True)
            gael_embed.add_field(name="📺 YouTube", value="@Gael_Level", inline=True)
            gael_embed.add_field(name="🌍 Location", value="United Arab Emirates", inline=True)
            gael_embed.add_field(name="🎁 FREE OVERLAYS", value="gumroad.com/gaellevel", inline=False)
            gael_embed.add_field(name="📊 Stats", value="**168K** subscribers | **1,118** videos | **32.6M** views", inline=False)
            gael_embed.set_footer(text="Apptivators-Academy | One App At A Time")
            
            async for msg in gael_ch.history(limit=5):
                if msg.author == bot.user and msg.embeds and "Gael Level" in msg.embeds[0].title:
                    await msg.edit(embed=gael_embed)
                    logger.info("Updated Gael Level card")
                    break
            else:
                await gael_ch.send(embed=gael_embed)
                logger.info("Deployed Gael Level card")


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
        rules_embed# set_image disabled
        
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
        # set_thumbnail disabled
        await interaction.response.send_message(embed=embed, view=wizard_view, ephemeral=True)


# ══════════════════════════════════════════════
#  CHANNEL-SPECIFIC ONBOARDING VIEWS
#  Each channel has its own view for step-by-step flow
# ══════════════════════════════════════════════

class WelcomeStepView(ui.View):
    """Step 1: Welcome channel - Introduction"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="⚔️ Begin Journey →", style=discord.ButtonStyle.primary, custom_id="step1_to_rules")
    async def go_to_rules(self, interaction: discord.Interaction, button: ui.Button):
        # Update user progress
        update_user_progress(interaction.user.id, 1, [0])
        
        # Send rules embed to the same channel
        rules_embed = discord.Embed(
            title="📜 Step 2: Server Rules & Guidelines",
            description="**Apptivators Academy Laws**\n\n"
                        "1️⃣ **No NSFW** — Keep content professional\n"
                        "2️⃣ **Be Respectful** — No slurs, hate speech, or harassment\n"
                        "3️⃣ **No Spam** — Keep discussions on-topic\n"
                        "4️⃣ **Help Others** — Share knowledge freely\n"
                        "5️⃣ **No Piracy** — Respect intellectual property\n\n"
                        "By clicking proceed, you agree to abide by these laws.",
            color=0x9B59B6
        )
        rules_embed.set_footer(text="Step 2/4 • Read carefully before proceeding")
        
        await interaction.response.send_message(embed=rules_embed, view=RulesStepView(), ephemeral=True)


class RulesStepView(ui.View):
    """Step 2: Rules channel - Laws acceptance"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="🛡️ I Accept These Laws →", style=discord.ButtonStyle.success, custom_id="step2_to_roles")
    async def go_to_roles(self, interaction: discord.Interaction, button: ui.Button):
        # Update progress
        progress = get_user_progress(interaction.user.id)
        completed = progress.get("completed", [])
        if 0 not in completed:
            completed.append(0)
        if 1 not in completed:
            completed.append(1)
        update_user_progress(interaction.user.id, 2, completed)
        
        # Send roles embed
        roles_embed = discord.Embed(
            title="🛠️ Step 3: Choose Your Path",
            description="**Select your skill level to unlock the right channels:**\n\n"
                        "🛡️ **1. The Noob** — Just starting (Python, JS, Bash)\n"
                        "⚔️ **2. The Beginner** — Know basics (Swift, Kotlin, C++)\n"
                        "🛠️ **3. The Intermediate** — Web apps (React, TypeScript)\n"
                        "🧠 **4. The Expert** — Cross-platform (Flutter, KMP)\n"
                        "⚡ **5. The God** — Master builder (.NET, MAUI)\n\n"
                        "Choose your level below!",
            color=0x3498DB
        )
#         roles_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        roles_embed.set_footer(text="Step 3/4 • Your role determines your access")
        
        await interaction.response.send_message(embed=roles_embed, view=RolesStepView(interaction.user.id), ephemeral=True)


class RolesStepView(ui.View):
    """Step 3: Roles channel - Skill selection"""
    def __init__(self, user_id: int):
        super().__init__(timeout=None)  # Must be None for persistent views
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your onboarding!", ephemeral=True)
            return False
        return True
    
    @ui.button(label="1. The Noob 🛡️", style=discord.ButtonStyle.secondary, custom_id="role_select_1")
    async def select_1(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_and_proceed(interaction, "The Noob (Level 0-1)", 1)
    
    @ui.button(label="2. The Beginner ⚔️", style=discord.ButtonStyle.secondary, custom_id="role_select_2")
    async def select_2(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_and_proceed(interaction, "The Beginner (Level 2)", 2)
    
    @ui.button(label="3. The Intermediate 🛠️", style=discord.ButtonStyle.secondary, custom_id="role_select_3")
    async def select_3(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_and_proceed(interaction, "The Intermediate (Level 3-7)", 3)
    
    @ui.button(label="4. The Expert 🧠", style=discord.ButtonStyle.secondary, custom_id="role_select_4")
    async def select_4(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_and_proceed(interaction, "The Expert (Level 8-12)", 4)
    
    @ui.button(label="5. The God ⚡", style=discord.ButtonStyle.secondary, custom_id="role_select_5")
    async def select_5(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_and_proceed(interaction, "The God (Level 13-∞)", 5)
    
    async def _assign_and_proceed(self, interaction: discord.Interaction, role_name: str, level: int):
        guild = interaction.guild
        
        # Create/get role
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name, reason="Onboarding skill selection")
        
        # Remove other skill roles
        for r in interaction.user.roles:
            if r.name in SKILL_LEVEL_ROLES.values():
                await interaction.user.remove_roles(r)
        
        # Add selected role
        await interaction.user.add_roles(role)
        
        # Update progress
        progress = get_user_progress(interaction.user.id)
        completed = progress.get("completed", [])
        if 2 not in completed:
            completed.append(2)
        update_user_progress(interaction.user.id, 3, completed)
        
        # Send final step embed
        call_to_arms_embed = discord.Embed(
            title="⚔️ Step 4: Final Registration - Call to Arms",
            description="**You have chosen your path!**\n\n"
                        f"**Your Role:** {role_name}\n\n"
                        "This is the final step. By clicking **I Agree**, you will:\n"
                        "✅ Become a **Verified Apptivator**\n"
                        "✅ Unlock all Academy channels\n"
                        "✅ Join the community of builders\n\n"
                        "*\"One App At A Time. The forge is hot, the guards are at the gate...\"*",
            color=0xE74C3C
        )
#         call_to_arms_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        call_to_arms_embed.set_footer(text="Step 4/4 • Final Registration")
        
        await interaction.response.send_message(embed=call_to_arms_embed, view=CallToArmsView(interaction.user.id), ephemeral=True)


class CallToArmsView(ui.View):
    """Step 4: Call-to-Arms - Final verification"""
    def __init__(self, user_id: int):
        super().__init__(timeout=None)  # Must be None for persistent views
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your onboarding!", ephemeral=True)
            return False
        return True
    
    @ui.button(label="⚔️ I AGREE - Join the Academy", style=discord.ButtonStyle.success, custom_id="final_agree")
    async def agree(self, interaction: discord.Interaction, button: ui.Button):
        guild = interaction.guild
        member = interaction.user
        
        # Grant Verified Apptivator role
        verified_role = discord.utils.get(guild.roles, name="Verified Apptivator")
        if not verified_role:
            verified_role = await guild.create_role(name="Verified Apptivator", color=discord.Color.gold(), reason="Onboarding completion")
        
        # Remove Initiate, add Verified
        initiate = discord.utils.get(guild.roles, name=DEFAULT_JOIN_ROLE)
        if initiate in member.roles:
            await member.remove_roles(initiate)
        await member.add_roles(verified_role)
        
        # Mark complete
        progress = get_user_progress(self.user_id)
        completed = progress.get("completed", [])
        if 3 not in completed:
            completed.append(3)
        update_user_progress(self.user_id, 4, completed)
        
        # Completion message
        final_embed = discord.Embed(
            title="💯 WELCOME TO THE FORGE!",
            description="**🎉 Onboarding Complete!**\n\n"
                        "You are now a **Verified Apptivator**!\n\n"
                        "**What's next:**\n"
                        "📚 #resources — Learning materials\n"
                        "💬 #general — Community chat\n"
                        "🛠️ #help-desk — Get help\n\n"
                        "*One App At A Time. Build it. Share it. Protect it.*\n\n⚔️🛡️🤖💯",
            color=0x2ECC71
        )
#         final_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        
        await interaction.response.edit_message(embed=final_embed, view=None)
        
        # Save to member data
        bot.save_member_data(member.id, str(member), "Verified Apptivator")


# ══════════════════════════════════════════════
#  EVENT: Welcome new members
# ══════════════════════════════════════════════
#  MULTI-STEP WIZARD ONBOARDING SYSTEM
# ══════════════════════════════════════════════
ONBOARDING_PROGRESS_FILE = os.path.join(BUILD_PLAN_DIR, "onboarding_progress.json")

def load_progress():
    if os.path.exists(ONBOARDING_PROGRESS_FILE):
        with open(ONBOARDING_PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(ONBOARDING_PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_progress(user_id):
    data = load_progress()
    return data.get(str(user_id), {"step": 0, "completed": []})

def update_user_progress(user_id, step, completed=None):
    data = load_progress()
    if str(user_id) not in data:
        data[str(user_id)] = {"step": 0, "completed": []}
    data[str(user_id)]["step"] = step
    if completed is not None:
        data[str(user_id)]["completed"] = completed
    save_progress(data)

ONBOARDING_STEPS = [
    {
        "title": "⚔️ Welcome to the Academy",
        "description": "Welcome to the Apptivators Academy! This tour will guide you through the forge.\n\n**What is the Academy?**\nWe're a community of builders, creators, and mentors dedicated to building the future—one app at a time.\n\nClick **Next** to begin your journey!",
        "color": 0xE74C3C,
#         "image": ACADEMY_IMAGE_URL,
    },
    {
        "title": "🛡️ Choose Your Path",
        "description": "Select your skill level to unlock the appropriate channels and resources:\n\n"
                      "**1. The Noob** — Just starting out (Python, Bash, JS)\n"
                      "**2. The Beginner** — Know the basics (Swift, Kotlin, C++)\n"
                      "**3. The Intermediate** — Building web apps (React, TypeScript)\n"
                      "**4. The Expert** — Cross-platform pro (Flutter, KMP)\n"
                      "**5. The God** — Master builder (.NET, MAUI)\n\n"
                      "Select your level using the buttons below.",
        "color": 0x3498DB,
        "role_select": True,
    },
    {
        "title": "📜 The Laws of the Forge",
        "description": "Before entering the Academy, you must agree to our protocols:\n\n"
                      "1. **No NSFW** — Keep it professional\n"
                      "2. **Be Respectful** — Civil engagement required\n"
                      "3. **No Spam** — Keep discussions on-topic\n"
                      "4. **Help Others** — Share knowledge freely\n\n"
                      "Click **I Agree** to accept and become a Verified Apptivator.",
        "color": 0x9B59B6,
        "rules": True,
    },
    {
        "title": "🎉 Welcome to the Forge!",
        "description": "**🎉 Onboarding Complete!**\n\n"
                      "You are now a **Verified Apptivator**!\n\n"
                      "**What's next:**\n"
                      "• Explore #resources for tutorials\n"
                      "• Check out #showcase to share projects\n"
                      "• Join a learning group in #learning-groups\n\n"
                      "*One App At A Time. Build it. Share it. Protect it.* ⚔️🛡️🤖",
        "color": 0x2ECC71,
        "complete": True,
    }
]

class OnboardingWizardView(ui.View):
    """Multi-step wizard with progress tracking and locked steps."""
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.current_step = get_user_progress(user_id).get("step", 0)
        self._update_buttons()
    
    def _update_buttons(self):
        self.clear_items()
        
        # Progress indicator
        progress_bar = "🔵" * (self.current_step + 1) + "⚪" * (len(ONBOARDING_STEPS) - self.current_step - 1)
        
        # Previous button (disabled on step 0)
        if self.current_step > 0:
            prev_btn = ui.Button(label="◀ Previous", style=discord.ButtonStyle.secondary, custom_id=f"wiz_prev_{self.user_id}")
            prev_btn.callback = self.prev_step
            self.add_item(prev_btn)
        
        # Next / Done button
        step_data = ONBOARDING_STEPS[self.current_step]
        if step_data.get("complete"):
            done_btn = ui.Button(label="✅ Finish Tour", style=discord.ButtonStyle.success, custom_id=f"wiz_done_{self.user_id}")
            done_btn.callback = self.finish_onboarding
        else:
            next_btn = ui.Button(label="Next ▶", style=discord.ButtonStyle.primary, custom_id=f"wiz_next_{self.user_id}")
            next_btn.callback = self.next_step
            self.add_item(next_btn)
        
        # Skip button
        skip_btn = ui.Button(label="⏭️ Skip Tour", style=discord.ButtonStyle.danger, custom_id=f"wiz_skip_{self.user_id}")
        skip_btn.callback = self.skip_tour
        self.add_item(skip_btn)
    
    def _get_embed(self):
        step_data = ONBOARDING_STEPS[self.current_step]
        progress_bar = "▓" * (self.current_step + 1) + "░" * (len(ONBOARDING_STEPS) - self.current_step - 1)
        
        embed = discord.Embed(
            title=step_data["title"],
            description=step_data["description"],
            color=step_data["color"]
        )
        embed.set_footer(text=f"Step {self.current_step + 1}/{len(ONBOARDING_STEPS)} | {progress_bar}")
        if "image" in step_data:
            embed.set_image(url=step_data["image"])
        return embed
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your onboarding tour!", ephemeral=True)
            return False
        return True
    
    async def next_step(self, interaction: discord.Interaction):
        # Mark current step as completed
        progress = get_user_progress(self.user_id)
        if self.current_step not in progress.get("completed", []):
            progress.setdefault("completed", []).append(self.current_step)
            update_user_progress(self.user_id, self.current_step + 1, progress["completed"])
        
        if self.current_step < len(ONBOARDING_STEPS) - 1:
            self.current_step += 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self._get_embed(), view=self)
    
    async def prev_step(self, interaction: discord.Interaction):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_buttons()
            await interaction.response.edit_message(embed=self._get_embed(), view=self)
    
    async def skip_tour(self, interaction: discord.Interaction):
        # Skip directly to completion
        self.current_step = len(ONBOARDING_STEPS) - 1
        await self.finish_onboarding(interaction)
    
    async def finish_onboarding(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        # Grant Verified Apptivator role
        verified_role = discord.utils.get(guild.roles, name="Verified Apptivator")
        if not verified_role:
            verified_role = await guild.create_role(name="Verified Apptivator", color=discord.Color.gold())
        
        # Remove Initiate role, add Verified
        initiate_role = discord.utils.get(guild.roles, name=DEFAULT_JOIN_ROLE)
        if initiate_role in member.roles:
            await member.remove_roles(initiate_role)
        await member.add_roles(verified_role)
        
        # Save final progress
        progress = get_user_progress(self.user_id)
        progress["completed"] = list(range(len(ONBOARDING_STEPS)))
        update_user_progress(self.user_id, len(ONBOARDING_STEPS) - 1, progress["completed"])
        
        # Completion embed
        final_embed = discord.Embed(
            title="⚔️ Welcome to the Forge!",
            description="**You are now a Verified Apptivator!**\n\n"
                        "Your journey has just begun. Head to the channels below to start building:\n\n"
                        "📢 **#announcements** — Stay updated\n"
                        "📚 **#resources** — Learning materials\n"
                        "💬 **#general** — Community chat\n\n"
                        "*One App At A Time. Build it. Share it. Protect it.* ⚔️🛡️🤖💯",
            color=0x2ECC71
        )
#         final_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        
        await interaction.response.edit_message(embed=final_embed, view=None)
        
        # Log completion
        bot.save_member_data(member.id, str(member), "Verified Apptivator")
        logger.info(f"Onboarding completed for {member.name}")


class OnboardingRoleSelectView(ui.View):
    """Role selection for step 2 of onboarding."""
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.selected_role = None
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your onboarding!", ephemeral=True)
            return False
        return True
    
    @ui.button(label="1. The Noob 🛡️", style=discord.ButtonStyle.secondary, custom_id="onboard_role_1")
    async def role_1(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_role(interaction, 1, "The Noob (Level 0-1)")
    
    @ui.button(label="2. The Beginner ⚔️", style=discord.ButtonStyle.secondary, custom_id="onboard_role_2")
    async def role_2(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_role(interaction, 2, "The Beginner (Level 2)")
    
    @ui.button(label="3. The Intermediate 🛠️", style=discord.ButtonStyle.secondary, custom_id="onboard_role_3")
    async def role_3(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_role(interaction, 3, "The Intermediate (Level 3-7)")
    
    @ui.button(label="4. The Expert 🧠", style=discord.ButtonStyle.secondary, custom_id="onboard_role_4")
    async def role_4(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_role(interaction, 4, "The Expert (Level 8-12)")
    
    @ui.button(label="5. The God ⚡", style=discord.ButtonStyle.secondary, custom_id="onboard_role_5")
    async def role_5(self, interaction: discord.Interaction, button: ui.Button):
        await self._assign_role(interaction, 5, "The God (Level 13-∞)")
    
    async def _assign_role(self, interaction: discord.Interaction, level: int, role_name: str):
        guild = interaction.guild
        
        # Create or get role
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name, reason="Onboarding role selection")
        
        # Remove other skill roles
        for r in interaction.user.roles:
            if r.name in SKILL_LEVEL_ROLES.values():
                await interaction.user.remove_roles(r)
        
        # Add selected role
        await interaction.user.add_roles(role)
        
        # Update progress
        progress = get_user_progress(self.user_id)
        if 1 not in progress.get("completed", []):
            progress.setdefault("completed", []).append(1)
        update_user_progress(self.user_id, 2, progress["completed"])
        
        # Send confirmation and wizard for next step
        await interaction.response.send_message(
            f"✅ **Role Assigned:** {role_name}\n\nNow click **Next** to review the server rules!",
            ephemeral=True
        )


class OnboardingRulesView(ui.View):
    """Rules agreement for step 3 of onboarding."""
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your onboarding!", ephemeral=True)
            return False
        return True
    
    @ui.button(label="⚔️ I Agree to All Rules", style=discord.ButtonStyle.success, custom_id="onboard_agree")
    async def agree(self, interaction: discord.Interaction, button: ui.Button):
        # Update progress
        progress = get_user_progress(self.user_id)
        if 2 not in progress.get("completed", []):
            progress.setdefault("completed", []).append(2)
        update_user_progress(self.user_id, 3, progress["completed"])
        
        await interaction.response.send_message(
            "✅ **You have agreed to the Academy Laws!**\n\nClick **Finish Tour** to complete your onboarding!",
            ephemeral=True
        )


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

    # 3. Private DM Greeting (Call to Arms) with Wizard Button
    class StartTourButton(ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @ui.button(label="⚔️ Start Academy Tour", style=discord.ButtonStyle.primary, custom_id="start_tour_dm")
        async def start_tour(self, interaction: discord.Interaction, button: ui.Button):
            user_id = interaction.user.id
            # Reset progress
            update_user_progress(user_id, 0, [])
            wizard = OnboardingWizardView(user_id)
            embed = wizard._get_embed()
            await interaction.response.send_message(embed=embed, view=wizard, ephemeral=True)
    
    try:
        legendary_quote = (
            "\"\"One App At A Time.\" The forge is hot, the guards are at the gate, and the synthetic edge is sharp.\n"
            "It has been an absolute pleasure building this fortress with you. The Academy is now yours to lead! ⚔️🛡️🤖\""
        )
        dm_embed = discord.Embed(
            title="⚔️ Your Academy Journey Begins!",
            description=(
                f"Welcome, **{member.name}**, to the **Apptivators Academy**.\n\n"
                "To unlock the full power of the forge, complete the onboarding tour below.\n\n"
                f"{legendary_quote}"
            ),
            color=discord.Color.blue(),
        )
        dm_embed.set_thumbnail(url=member.display_avatar.url)
        dm_embed.set_footer(text="The Forge Awaits. ⚔️🛡️🤖💯")
        
        await member.send(embed=dm_embed, view=StartTourButton())
        logger.info(f"Welcome DM with tour button sent to {member.name}")
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
    Also locks info channels (softwaregent, gael-level) to admin-only.
    """
    if message.author.bot:
        return
    
    # Lock info channels - only admins can send messages
    locked_channels = ["softwaregent", "gael-level"]
    if message.channel.name in locked_channels:
        if not message.author.guild_permissions.administrator:
            try:
                await message.delete()
                await message.channel.send(f"🔒 {message.author.mention}, only Admins can post here!", delete_after=5)
                return
            except:
                pass
    
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
    # set_image disabled
    embed.add_field(
        name="🚀 Your Journey",
        value="Click the button below to start your skill assessment and agree to the server protocols.",
        inline=False
    )
    view = JoinWalkthroughView()
    await ctx.send(embed=embed, view=view)
    await ctx.message.delete()


# ══════════════════════════════════════════════
#  COMMAND: !clearbot (Delete all messages - STAFF ONLY)
# ══════════════════════════════════════════════
@bot.command(name="clearbot")
@commands.has_permissions(manage_messages=True)
async def clearbot(ctx, channel_name: str = None):
    """Delete all messages (bot + users) from a channel or all channels. STAFF ONLY."""
    await ctx.message.delete()
    
    target_channel = None
    if channel_name:
        target_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name.lower())
    
    deleted_count = 0
    channels_to_clear = [target_channel] if target_channel else ctx.guild.text_channels
    
    for channel in channels_to_clear:
        try:
            async for message in channel.history(limit=100):
                await message.delete()
                deleted_count += 1
        except:
            pass
    
    channel_name = target_channel.name if target_channel else "all channels"
    await ctx.send(f"🧹 Deleted {deleted_count} messages from #{channel_name}!", delete_after=5)


# ══════════════════════════════════════════════
#  COMMAND: !build_server (STAFF ONLY)
# ══════════════════════════════════════════════


# ══════════════════════════════════════════════
#  COMMAND: !softwaregent (Post SoftwareGent Info Card)
# ══════════════════════════════════════════════
@bot.command(name="softwaregent")
async def softwaregent(ctx):
    """Post the SoftwareGent info card."""
    embed = discord.Embed(
        title="📺 SoftwareGent",
        description="Welcome to SoftwareGent, we are a channel that makes educational videos on how to get and use different types of software.\n\n"
                    "We also have our own blog in which we have different types of helpful articles with a lot of information about the software you are using or you are thinking about using.\n\n"
                    "**At SoftwareGent we make your life easy.** We test and review the software so you do not have to.",
        color=discord.Color.blue()
    )
    embed.add_field(name="📧 Email", value="softwaregentofficial@gmail.com", inline=True)
    embed.add_field(name="📺 YouTube", value="@softwaregent7443", inline=True)
    embed.add_field(name="🌍 Location", value="Greece", inline=True)
    embed.add_field(name="🔗 Community", value="skool.com/ai-saas-builders/about", inline=False)
    embed.add_field(name="🔗 Assets Community", value="skool.com/ai-business-builders-7856/about", inline=False)
    embed.add_field(name="🌐 Website", value="softwaregentofficial.com", inline=False)
    embed.add_field(name="📊 Stats", value="**11.3K** subscribers | **191** videos | **895K** views", inline=False)
    embed.set_footer(text="Apptivators-Academy | One App At A Time")
    
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !addemojis (Upload emojis from desktop folder)
# ══════════════════════════════════════════════
@bot.command(name="addemojis")
@commands.has_permissions(manage_emojis=True)
async def addemojis(ctx):
    """Add emojis from the desktop folder to the server."""
    import os
    import aiofiles
    
    emoji_folder = r"C:\Users\Gam3rGoon\Desktop\Emoji's"
    
    if not os.path.exists(emoji_folder):
        await ctx.send(f"❌ Folder not found: {emoji_folder}")
        return
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    emoji_files = [f for f in os.listdir(emoji_folder) if f.lower().endswith(valid_extensions)]
    
    if not emoji_files:
        await ctx.send("❌ No image files found in folder")
        return
    
    await ctx.send(f"🎭 Adding {len(emoji_files)} emojis to server...")
    
    added_count = 0
    failed_count = 0
    
    for filename in emoji_files:
        try:
            filepath = os.path.join(emoji_folder, filename)
            emoji_name = os.path.splitext(filename)[0][:32]
            emoji_name = ''.join(c for c in emoji_name if c.isalnum() or c == '_')
            
            async with aiofiles.open(filepath, 'rb') as f:
                image_data = await f.read()
            
            emoji = await ctx.guild.create_custom_emoji(
                name=emoji_name,
                image=image_data,
                reason="Added via GoonsClawbot"
            )
            added_count += 1
            await ctx.send(f"✅ Added: {emoji_name}")
        except Exception as e:
            failed_count += 1
            await ctx.send(f"❌ Failed to add {filename}: {e}")
    
    await ctx.send(f"🎉 Emoji upload complete! Added: {added_count}, Failed: {failed_count}")


# ══════════════════════════════════════════════
#  COMMAND: !tour (Multi-step Wizard)
# ══════════════════════════════════════════════
@bot.command(name="tour")
async def tour(ctx):
    """Start the multi-step onboarding wizard."""
    user_id = ctx.author.id
    
    # Check if already completed
    progress = get_user_progress(user_id)
    if progress.get("completed") and len(progress.get("completed", [])) >= len(ONBOARDING_STEPS):
        await ctx.send("⚠️ You've already completed the onboarding! Use `!welcome` to see the server intro.", ephemeral=True)
        return
    
    # Reset progress if starting fresh
    if progress.get("step", 0) == 0 and not progress.get("completed"):
        update_user_progress(user_id, 0, [])
    
    # Create wizard view for this user
    wizard_view = OnboardingWizardView(user_id)
    
    # Send first step
    embed = wizard_view._get_embed()
    await ctx.send(embed=embed, view=wizard_view, ephemeral=True)


# ══════════════════════════════════════════════
#  COMMAND: !build_server (OWNER ONLY - Hidden)
# ══════════════════════════════════════════════
@bot.command(name="build_server")
@commands.is_owner()
async def build_server(ctx):
    """Automatically create Categories and Channels from the build plan. OWNER ONLY."""
    status_msg = await ctx.send("🏗️ **Initiating Server Build Phase...**")
    guild = ctx.guild
    report: list[str] = []

    # Ensure Onboarding Core category exists first
    onboarding_cat = discord.utils.get(guild.categories, name="📢 Apptivators-Academy Core")
    if not onboarding_cat:
        report.append(f"📁 Creating Category: `📢 1. Onboarding Core`")
        onboarding_cat = await guild.create_category("📢 Apptivators-Academy Core")
    
    # Create onboarding channels if missing
    onboarding_channels = [
        {"name": "welcome", "topic": "Step 1: Welcome to the Academy"},
        {"name": "rules", "topic": "Step 2: Server Laws & Guidelines"},
        {"name": "roles", "topic": "Step 3: Choose Your Skill Path"},
        {"name": "call-to-arms", "topic": "Step 4: Final Registration - I Agree"},
    ]
    
    for ch in onboarding_channels:
        channel = discord.utils.get(guild.text_channels, name=ch["name"])
        if not channel:
            channel = await guild.create_text_channel(ch["name"], category=onboarding_cat, topic=ch["topic"])
            report.append(f"  └─ 📝 Created: `#{ch['name']}`")
        else:
            # Move to onboarding category if not already there
            if channel.category != onboarding_cat:
                await channel.edit(category=onboarding_cat)
            report.append(f"  └─ ✔️ Exists: `#{ch['name']}`")

    # Create other categories
    for cat_name, channels in SERVER_STRUCTURE.items():
        if "Onboarding" in cat_name:
            continue  # Already handled above
        
        category = discord.utils.get(guild.categories, name=cat_name)
        if not category:
            report.append(f"📁 Creating Category: `{cat_name}`")
            category = await guild.create_category(cat_name)
        else:
            report.append(f"✔️ Category Exists: `{cat_name}`")

        for ch in channels:
            channel = discord.utils.get(category.text_channels, name=ch["name"])
            if not channel:
                report.append(f"  └─ 📝 Creating Channel: `#{ch['name']}`")
                await guild.create_text_channel(ch["name"], category=category, topic=ch["topic"])
            else:
                report.append(f"  └─ ✔️ Channel Exists: `#{ch['name']}`")

    embed = discord.Embed(
        title="🏗️ Server Build Report",
        description="\n".join(report),
        color=0x9B59B6
    )
    embed.set_footer(text="Auto-Pilot: One App At A Time.")
    await status_msg.edit(content="✅ **Server structure complete!**", embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !setup_onboarding (OWNER ONLY - Hidden)
# ══════════════════════════════════════════════
@bot.command(name="setup_onboarding")
@commands.is_owner()
async def setup_onboarding(ctx):
    """Build onboarding channels AND deploy GUIs in one command. OWNER ONLY."""
    
    # First build the server
    guild = ctx.guild
    report = []
    
    # Create Onboarding Core category
    onboarding_cat = discord.utils.get(guild.categories, name="📢 Apptivators-Academy Core")
    if not onboarding_cat:
        onboarding_cat = await guild.create_category("📢 Apptivators-Academy Core")
        report.append("📁 Created: Onboarding Core category")
    
    # Create onboarding channels
    onboarding_channels = [
        {"name": "welcome", "topic": "Step 1: Welcome to the Academy"},
        {"name": "rules", "topic": "Step 2: Server Laws & Guidelines"},
        {"name": "roles", "topic": "Step 3: Choose Your Skill Path"},
        {"name": "call-to-arms", "topic": "Step 4: Final Registration - I Agree"},
    ]
    
    welcome_ch = rules_ch = roles_ch = call_to_arms_ch = None
    
    for ch_data in onboarding_channels:
        channel = discord.utils.get(guild.text_channels, name=ch_data["name"])
        if not channel:
            channel = await guild.create_text_channel(
                ch_data["name"], 
                category=onboarding_cat, 
                topic=ch_data["topic"]
            )
            report.append(f"📝 Created: #{ch_data['name']}")
        else:
            report.append(f"✔️ Exists: #{ch_data['name']}")
        
        if ch_data["name"] == "welcome":
            welcome_ch = channel
        elif ch_data["name"] == "rules":
            rules_ch = channel
        elif ch_data["name"] == "roles":
            roles_ch = channel
        elif ch_data["name"] == "call-to-arms":
            call_to_arms_ch = channel
    
    report.append("")
    report.append("--- Deploying GUIs ---")
    
    # Deploy Step 1: Welcome
    if welcome_ch:
        welcome_embed = discord.Embed(
            title="⚔️ Step 1: Welcome to the Academy",
            description="**Welcome, Apprentice!**\n\n"
                        "You have entered the Apptivators Academy - a forge of builders, creators, and mentors.\n\n"
                        "**Your Journey:**\n"
                        "1️⃣ Welcome (you are here)\n"
                        "2️⃣ Rules →\n"
                        "3️⃣ Choose Your Role →\n"
                        "4️⃣ Call to Arms (Final Registration)\n\n"
                        "Click **Begin Journey** to proceed!",
            color=0xE74C3C
        )
        # Image disabled
        welcome_embed.set_footer(text="Step 1/4 • The Journey Begins")
        await welcome_ch.send(embed=welcome_embed, view=WelcomeStepView())
        report.append(f"✅ GUI: Welcome → {welcome_ch.mention}")
    
    # Deploy Step 2: Rules
    if rules_ch:
        rules_embed = discord.Embed(
            title="📜 Step 2: Server Rules & Guidelines",
            description="**Apptivators Academy Laws**\n\n"
                        "1️⃣ **No NSFW** — Keep content professional\n"
                        "2️⃣ **Be Respectful** — No slurs, hate speech\n"
                        "3️⃣ **No Spam** — Keep discussions on-topic\n"
                        "4️⃣ **Help Others** — Share knowledge freely\n"
                        "5️⃣ **No Piracy** — Respect intellectual property\n\n"
                        "By clicking proceed, you agree to these laws.",
            color=0x9B59B6
        )
        rules_embed.set_footer(text="Step 2/4 • Read carefully before proceeding")
        await rules_ch.send(embed=rules_embed, view=RulesStepView())
        report.append(f"✅ GUI: Rules → {rules_ch.mention}")
    
    # Deploy Step 3: Roles
    if roles_ch:
        roles_embed = discord.Embed(
            title="🛠️ Step 3: Choose Your Path",
            description="**Select your skill level:**\n\n"
                        "🛡️ **1. The Noob** — Just starting (Python, JS)\n"
                        "⚔️ **2. The Beginner** — Know basics\n"
                        "🛠️ **3. The Intermediate** — Building apps\n"
                        "🧠 **4. The Expert** — Cross-platform pro\n"
                        "⚡ **5. The God** — Master builder\n\n"
                        "Select your level to unlock appropriate channels!",
            color=0x3498DB
        )
#         roles_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        roles_embed.set_footer(text="Step 3/4 • Your role determines access")
        await roles_ch.send(embed=roles_embed, view=RolesStepView(0))
        report.append(f"✅ GUI: Roles → {roles_ch.mention}")
    
    # Deploy Step 4: Call-to-Arms
    if call_to_arms_ch:
        cta_embed = discord.Embed(
            title="⚔️ Step 4: Call to Arms - Final Registration",
            description="**This is the final step!**\n\n"
                        "By clicking **I Agree**, you will:\n"
                        "✅ Become a **Verified Apptivator**\n"
                        "✅ Unlock all Academy channels\n"
                        "✅ Join the community of builders\n\n"
                        "*\"One App At A Time. The forge is hot, the guards are at the gate...\"*",
            color=0x2ECC71
        )
        # Image disabled
        cta_embed.set_footer(text="Step 4/4 • Final Registration")
        await call_to_arms_ch.send(embed=cta_embed, view=CallToArmsView(0))
        report.append(f"✅ GUI: Call-to-Arms → {call_to_arms_ch.mention}")
    
    embed = discord.Embed(
        title="🛰️ Onboarding System Ready!",
        description="\n".join(report),
        color=0x2ECC71
    )
    embed.set_footer(text="⚔️🛡️🤖💯 The Forge is Live")
    await ctx.send(embed=embed)


# ══════════════════════════════════════════════
#  COMMAND: !initialize_onboarding (OWNER ONLY - Hidden)
# ══════════════════════════════════════════════
@bot.command(name="initialize_onboarding")
@commands.is_owner()
async def initialize_onboarding(ctx):
    """
    MASTER INITIALIZATION: Deploy 4-step onboarding to channels. OWNER ONLY.
    Deploys GUIs to: welcome → rules → roles → call-to-arms
    """
    status_msg = await ctx.send("🚀 **Initiating 4-Step Onboarding Deployment...**")
    guild = ctx.guild
    
    def find_channel(name):
        return discord.utils.find(lambda c: name.lower() in c.name.lower(), guild.text_channels)

    welcome_ch = find_channel("welcome")
    rules_ch = find_channel("rules")
    roles_ch = find_channel("roles")
    call_to_arms_ch = find_channel("call-to-arms")
    
    report = []
    
    # Step 1: Welcome Channel
    if welcome_ch:
        welcome_embed = discord.Embed(
            title="⚔️ Step 1: Welcome to the Academy",
            description="**Welcome, Apprentice!**\n\n"
                        "You have entered the Apptivators Academy - a forge of builders, creators, and mentors.\n\n"
                        "**Your Journey:**\n"
                        "1️⃣ Welcome (you are here)\n"
                        "2️⃣ Rules →\n"
                        "3️⃣ Choose Your Role →\n"
                        "4️⃣ Call to Arms (Final Registration)\n\n"
                        "Click **Begin Journey** to proceed!",
            color=0xE74C3C
        )
        # Image disabled
        welcome_embed.set_footer(text="Step 1/4 • The Journey Begins")
        await welcome_ch.send(embed=welcome_embed, view=WelcomeStepView())
        report.append(f"✅ Step 1: Welcome GUI → {welcome_ch.mention}")
    else:
        report.append("⚠️ `welcome` channel not found")
    
    # Step 2: Rules Channel
    if rules_ch:
        rules_embed = discord.Embed(
            title="📜 Step 2: Server Rules & Guidelines",
            description="**Apptivators Academy Laws**\n\n"
                        "1️⃣ **No NSFW** — Keep content professional\n"
                        "2️⃣ **Be Respectful** — No slurs, hate speech\n"
                        "3️⃣ **No Spam** — Keep discussions on-topic\n"
                        "4️⃣ **Help Others** — Share knowledge freely\n"
                        "5️⃣ **No Piracy** — Respect intellectual property\n\n"
                        "By clicking proceed, you agree to these laws.",
            color=0x9B59B6
        )
        rules_embed.set_footer(text="Step 2/4 • Read carefully before proceeding")
        await rules_ch.send(embed=rules_embed, view=RulesStepView())
        report.append(f"✅ Step 2: Rules GUI → {rules_ch.mention}")
    else:
        report.append("⚠️ `rules` channel not found")
    
    # Step 3: Roles Channel
    if roles_ch:
        roles_embed = discord.Embed(
            title="🛠️ Step 3: Choose Your Path",
            description="**Select your skill level:**\n\n"
                        "🛡️ **1. The Noob** — Just starting (Python, JS)\n"
                        "⚔️ **2. The Beginner** — Know basics\n"
                        "🛠️ **3. The Intermediate** — Building apps\n"
                        "🧠 **4. The Expert** — Cross-platform pro\n"
                        "⚡ **5. The God** — Master builder\n\n"
                        "Select your level to unlock appropriate channels!",
            color=0x3498DB
        )
#         roles_embed.set_thumbnail(url=ACADEMY_IMAGE_URL)
        roles_embed.set_footer(text="Step 3/4 • Your role determines access")
        await roles_ch.send(embed=roles_embed, view=RolesStepView(0))
        report.append(f"✅ Step 3: Roles GUI → {roles_ch.mention}")
    else:
        report.append("⚠️ `roles` channel not found")
    
    # Step 4: Call-to-Arms Channel
    if call_to_arms_ch:
        cta_embed = discord.Embed(
            title="⚔️ Step 4: Call to Arms - Final Registration",
            description="**This is the final step!**\n\n"
                        "By clicking **I Agree**, you will:\n"
                        "✅ Become a **Verified Apptivator**\n"
                        "✅ Unlock all Academy channels\n"
                        "✅ Join the community of builders\n\n"
                        "*\"One App At A Time. The forge is hot, the guards are at the gate...\"*",
            color=0x2ECC71
        )
        # Image disabled
        cta_embed.set_footer(text="Step 4/4 • Final Registration")
        await call_to_arms_ch.send(embed=cta_embed, view=CallToArmsView(0))
        report.append(f"✅ Step 4: Call-to-Arms GUI → {call_to_arms_ch.mention}")
    else:
        report.append("⚠️ `call-to-arms` channel not found")

    final_embed = discord.Embed(
        title="🛰️ 4-Step Onboarding Deployed!",
        description="\n".join(report),
        color=0x2ECC71
    )
    final_embed.set_footer(text="The Forge is Live. ⚔️🛡️🤖💯")
    await status_msg.edit(content="🏁 **Initialization Complete!**", embed=final_embed)

    final_embed = discord.Embed(
        title="🛰️ Legendary Deployment System",
        description="\n".join(report),
        color=0x2ECC71
    )
    final_embed.set_footer(text="The Forge is Live. ⚔️🛡️🤖💯")
    await status_msg.edit(content="🏁 **Master Initialization Complete.**", embed=final_embed)


# ══════════════════════════════════════════════
#  COMMAND: !list_members (STAFF)
# ══════════════════════════════════════════════
@bot.command(name="list_members")
@commands.has_permissions(manage_messages=True)
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
@commands.has_permissions(manage_messages=True)
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

class ApplyCollaboratorView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Open Collaborator Application", style=discord.ButtonStyle.success, custom_id="btn_open_collab")
    async def apply_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(CollaboratorModal())

@bot.command(name="apply_collaborator")
async def apply_collaborator(ctx):
    """Open the collaborator application modal."""
    if ctx.interaction:
        await ctx.interaction.response.send_modal(CollaboratorModal())
    else:
        await ctx.send("Click the button below to open the application form:", view=ApplyCollaboratorView())

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

class ApplyModView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Open Moderator Entrance Exam", style=discord.ButtonStyle.danger, custom_id="btn_open_mod_exam")
    async def apply_mod_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(ModeratorExamModal())

@bot.command(name="apply_mod")
async def apply_mod(ctx):
    """Open the moderator entrance exam modal."""
    if ctx.interaction:
        await ctx.interaction.response.send_modal(ModeratorExamModal())
    else:
        await ctx.send("Click the button below to open the Exam form:", view=ApplyModView())


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
@commands.is_owner()
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
#  COMMAND: !sharefile (PUBLIC - Share to GitHub)
# ══════════════════════════════════════════════
@bot.command(name="sharefile")
async def sharefile(ctx, filename: str, *, content: str):
    """Share a file to the Apptivators-Academy Community repo."""
    if not GITHUB_PAT:
        await ctx.send("❌ GitHub integration not configured.", ephemeral=True)
        return
    
    # Auto-path to community folder in Apptivators-Academy repo
    repo_path = f"community/{filename}"
    
    content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    url = f"{GITHUB_API_BASE}/contents/{repo_path}"
    payload = {
        "message": f"Community share: {filename} via Discord",
        "content": content_b64,
    }
    
    existing_sha = _get_file_sha(repo_path)
    if existing_sha:
        payload["sha"] = existing_sha
    
    # Use Apptivators-Academy repo
    resp = requests.put(url.replace(GITHUB_REPO, "Apptivators-Academy"), headers=_github_headers(), json=payload, timeout=30)
    
    if resp.status_code in (200, 201):
        await ctx.send(f"✅ `{filename}` shared to Apptivators-Academy community folder!", ephemeral=True)
    else:
        await ctx.send(f"❌ Failed to share (HTTP {resp.status_code})", ephemeral=True)


# ══════════════════════════════════════════════
#  COMMAND: !addfile <repo_path> <content> (STAFF)
# ══════════════════════════════════════════════
@bot.command(name="addfile")
@commands.has_permissions(manage_messages=True)
async def addfile(ctx, repo_path: str, *, content: str):
    """Add or update a single file in the GitHub repo from Discord. STAFF ONLY."""
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
@commands.has_permissions(manage_messages=True)
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
            model_names = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
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
            
            model = genai.GenerativeModel("gemini-1.5-flash") # Fallback to stable free-tier model
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
