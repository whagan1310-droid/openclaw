import discord
from discord.ext import commands
import os

# --- Configuration ---
# You will need to enable "Server Members Intent" and "Message Content Intent" in the Discord Developer Portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True # Required to detect when users leave voice channels

bot = commands.Bot(command_prefix='!', intents=intents)

# Category ID where the private review channels are created
# Replace this with the actual Category ID in your server
PRIVATE_CATEGORY_ID = 1480191656501186622

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    print('Bot is ready to enforce The Blackout Rule in Private Channels.')

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Triggers whenever a user's voice state changes (joins, leaves, moves).
    We use this to check if a Private Review voice channel is now empty.
    """
    
    # If the user left a channel (before.channel exists)
    if before.channel is not None:
        
        # Check if the channel is in our designated Private Review Category
        if before.channel.category_id == PRIVATE_CATEGORY_ID:
            
            # Check if the channel is now empty
            if len(before.channel.members) == 0:
                print(f"[Total Purge Initiated] - Channel {before.channel.name} is now empty.")
                
                # Fetch the associated text channel (assuming they share a name or are linked)
                # In modern Discord, Voice Channels can have their own text chat. 
                # If we are deleting the whole channel:
                try:
                    await before.channel.delete(reason="Blackout Rule: Channel emptied by last user.")
                    print(f"Successfully purged channel: {before.channel.name}")
                    
                    # Optional: Send a log to an admin channel
                    # admin_channel = bot.get_channel(ADMIN_LOG_CHANNEL_ID)
                    # await admin_channel.send(f"⚠️ **Total Purge Executed** on `{before.channel.name}` (Channel was emptied by {member.name}).")
                    
                except discord.Forbidden:
                    print(f"Error: Bot lacks permission to delete channel {before.channel.name}.")
                except discord.HTTPException as e:
                    print(f"Failed to delete channel {before.channel.name}: {e}")

@bot.command(name='purge_text')
@commands.has_permissions(manage_channels=True)
async def purge_text(ctx):
    """
    Manual override command for Admins/Mods to instantly wipe a text channel's history.
    Useful for text-only Private Review Chambers.
    """
    if ctx.channel.category_id == PRIVATE_CATEGORY_ID:
        # Clone the channel to keep permissions and placement, then delete the old one
        new_channel = await ctx.channel.clone(reason="Manual Blackout Purge request.")
        await ctx.channel.delete(reason="Manual Blackout Purge request.")
        await new_channel.send("⚠️ **Total Purge Complete**. This Review Chamber has been wiped clean.")
    else:
        await ctx.send("This command can only be used inside a Private Review Chamber.")

@bot.command(name='post_rules')
@commands.has_permissions(administrator=True)
async def post_rules(ctx):
    """
    Reads the discohook_rules_template.json file and posts the embed to the current channel.
    Usage: Run this command in the #rules channel to generate the official snapshot.
    """
    import json
    
    # Define the path to the JSON template (assumes it's in the same directory as the script)
    # Adjust this path if the bot is run from a different working directory
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'discohook_rules_template.json')
    
    if not os.path.exists(template_path):
        await ctx.send("❌ Error: `discohook_rules_template.json` not found in the bot directory.")
        return

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # The Discohook JSON has an 'embeds' array. We grab the first embed object.
        if 'embeds' in data and len(data['embeds']) > 0:
            embed_data = data['embeds'][0]
            embed = discord.Embed.from_dict(embed_data)
            
            # Send the embed and delete the original command message to keep the channel clean
            await ctx.send(embed=embed)
            await ctx.message.delete()
        else:
            await ctx.send("❌ Error: No embeds found in the JSON file.")
            
    except Exception as e:
        await ctx.send(f"❌ Error reading or parsing the template: {str(e)}")

# --- Run the Bot ---
# In a real environment, load this from an environment variable: os.getenv('DISCORD_BOT_TOKEN')
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("ERROR: DISCORD_BOT_TOKEN environment variable not set.")
