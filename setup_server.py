import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# ──────────────────────────────────────────────
#  Setup & Config
# ──────────────────────────────────────────────
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Define the server structure from discord_channel_definitions.md
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
}

@bot.event
async def on_ready():
    print(f"🚀 Auto-Builder Online: {bot.user.name}")
    print("⚠️  Warning: This script will create categories and channels in your server.")
    print("   Type 'BUILD' in the console to confirm and start.")

async def build_server(guild):
    """Main logic to build categories and channels."""
    print(f"🏗️  Building structure for: {guild.name}")
    
    for cat_name, channels in SERVER_STRUCTURE.items():
        # Check if category exists
        category = discord.utils.get(guild.categories, name=cat_name)
        if not category:
            print(f"📁 Creating Category: {cat_name}")
            category = await guild.create_category(cat_name)
        else:
            print(f"✔️ Category Already Exists: {cat_name}")

        for ch in channels:
            # Check if channel exists in this category
            channel = discord.utils.get(category.text_channels, name=ch["name"])
            if not channel:
                print(f"  └─ 📝 Creating Channel: {ch['name']}")
                # Set permissions: Information channels are read-only for @everyone
                perms_overwrites = {} 
                if "1." in cat_name:
                    perms_overwrites = {
                        guild.default_role: discord.PermissionOverwrite(send_messages=False),
                        guild.me: discord.PermissionOverwrite(send_messages=True)
                    }
                
                print(f"DEBUG: perms_overwrites type: {type(perms_overwrites)}, content: {perms_overwrites}")
                await guild.create_text_channel(
                    ch["name"], 
                    category=category, 
                    topic=ch["topic"],
                    overwrites=perms_overwrites
                )
            else:
                print(f"  └─ ✔️ Channel Already Exists: {ch['name']}")

    print("\n✅ Server Build Complete!")
    await bot.close()

# Custom console input loop to prevent accidental runs
async def input_loop():
    while not bot.is_closed():
        await asyncio.sleep(1)
        if bot.is_ready():
            user_input = await asyncio.get_event_loop().run_in_executor(None, input, ">> ")
            if user_input.upper() == "BUILD":
                # Assuming the bot is in one guild for this setup
                if bot.guilds:
                    await build_server(bot.guilds[0])
                else:
                    print("❌ Error: Bot is not in any servers.")
            elif user_input.upper() == "EXIT":
                await bot.close()

async def main():
    # Start the input loop and the bot concurrently
    await asyncio.gather(
        bot.start(TOKEN),
        input_loop()
    )

if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not found in .env")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass
