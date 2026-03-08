# OpenClaw Bot Integration Guide (GoonsClawbot#5107)

This guide provides the exact steps to configure your OpenClaw bot (`GoonsClawbot#5107`) to act as the primary AI assistant on your server, utilizing your requested Gemini API key.

## 1. Configure the Discord Channel

To connect OpenClaw to your `GoonsClawbot#5107` Discord application, you need your Discord Bot Token (from the Discord Developer Portal). Make sure you have invited the bot to your server with Admin permissions.

Open your terminal in the `d:\Clawbot` directory and run:

```bash
# Set your gateway mode to local for self-hosting
openclaw config set gateway.mode local

# Add your Discord Bot Token (Use the RAW token, no prefixes)
# Example: openclaw config set channels.discord.token YOUR_DISCORD_BOT_TOKEN
```

🚨 **CRITICAL SECURITY NOTE**: Never post or share your Discord Bot Token publicly!

## 2. Configure the Gemini 1.5 Flash Provider

You've successfully generated your Gemini API key. Now we need to tell OpenClaw to use it as the main intelligence provider.

```bash
# Add your Gemini API Key
openclaw config set provider.gemini.apiKey YOUR_GEMINI_API_KEY

# Explicitly set the model to 1.5 Flash to ensure you stay within the free tier limits (up to 15 Requests Per Minute)
openclaw config set provider.gemini.model gemini-1.5-flash
```

🚨 **CRITICAL SECURITY NOTE**: Your Gemini API Key is now saved in the build plan. Please ensure these `.md` files are kept **strictly private** to your machine and not uploaded to a public repository like GitHub. Your public GitHub repo should *never* contain real keys.

## 3. Customize the Bot's Persona (System Prompt)

To ensure GoonsClawbot strictly follows your server's "Call to Arms" and acts as a Level 5 Architect, you must customize its system prompt. 

Create a file named `persona.txt` (or configure via the OpenClaw configuration file directly) with the following instructions:

```text
You are GoonsClawbot, a Level 5 (Distinguished Engineer) AI assistant for a collaborative programming Discord server. 

Your objectives are:
1. Code Reviews: Analyze snippets provided in public and private channels. Provide constructive, high-level feedback.
2. Security: Identify malicious code, malware, or phishing attempts immediately. Treat flags as false positives first, but unequivocally flag confirmed malware.
3. Mentorship: Guide users from Level 0 to Level 4. Encourage learning over spoon-feeding.
4. The Coding Creed: Emphasize "Keep it simple" and "One app at a time."

When reviewing code, always prioritize security, readability, and performance. If code appears malicious, output a high-priority warning starting with "[CONFIRMED MALWARE FLAG]".
```

## 4. Run the OpenClaw Gateway

Once configured, start your OpenClaw gateway to bring GoonsClawbot online:

```bash
# If using the developer CLI inside your Clawbot directory:
pnpm openclaw gateway run --bind loopback --port 18789 --force
```

## Next Steps for the Server
1.  **Deploy GoonsClawbot**: Once the bot starts responding in `#code-reviews`, test it by asking it to review a simple Python script.
2.  **Run the Python Auto-Purge Script**: You can run the `auto_purge_bot.py` script concurrently in a separate background terminal. Your OpenClaw bot (`GoonsClawbot`) will handle the conversational intelligence and code reviews, while the lightweight Python script handles the server infrastructure rules (purging private channels, posting the rules embed).
