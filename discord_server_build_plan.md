# Discord Server Build Plan

## 1. Compliance & Rules Check
Before building out the server, it is important to verify your requested mechanics against Discord's Terms of Service (ToS) and Community Guidelines:

*   **Malware Snapshot Rule**: Your rule stating *"If strike for Malware = strike. Strike Triggers Instant Snapshot All current user(s) Id That posted Flagged Malware"* is **COMPLIANT**. Discord encourages server owners to maintain safe environments. Logging User IDs (which are public numerical identifiers) of bad actors for moderation and ban purposes is standard practice and fully within ToS.
*   **OpenCode.ai / MIT License Linking**: Your question regarding *"Do a check to see if i can link https://opencode.ai/ as i have Fork of Repo... marked with MIT license"* is **COMPLIANT**. Linking to open-source projects, forks, and websites under an MIT license does not violate any Discord rules.

---

## 2. Bot Ecosystem & Integrations (Free Tier Focused)
The following bots run the server's automation, security, and UI enhancements. Tasks are **delegated** between bots to reduce load, avoid conflicts, and keep things free.

### Bot Task Delegation Table

| Task | Handled By | Notes |
|---|---|---|
| AI Chat & Code Reviews (`!ask`) | **GoonsClawbot** (custom) | Gemini 1.5 Flash API |
| GitHub Deployment (`!deploy_plan`, `!addfile`) | **GoonsClawbot** (custom) | GitHub REST API via PAT |
| Strike System (`!strike`) | **GoonsClawbot** (custom) | Logs to `strike_log.json` |
| Rules Embed (`!post_rules`) | **GoonsClawbot** (custom) | Reads `discohook_rules_template.json` |
| Private Channel Purge (`!purge_text` + auto) | **GoonsClawbot** (custom) | Blackout Rule enforcement |
| Welcome Embeds & Greetings | **Sapphire** ✅ on server | Configure via [sapph.xyz](https://sapph.xyz) dashboard |
| Reaction Roles (#roles) | **Sapphire** ✅ on server | Dropdown menus or emoji reactions |
| Join Roles (auto-assign on join) | **Sapphire** ✅ on server | Auto-assign a "New Member" role |
| Auto-Moderation & Logging | **Sapphire** ✅ on server | AI-powered mod (beta), audit logs |
| Backup Moderation & Auto-Responders | **Dyno** | Custom commands, auto-mod rules |
| Music Playback | **FredBoat / Jockie Music / Uzox** | Free YouTube/SoundCloud/Spotify |
| Channel Archiving & Knowledge Base | **ArchiveMind** | Searchable archive of inactive channels |
| Support Tickets (#help-desk) | **Helper.gg** | Organized ticketing system |
| Temporary Voice Channels | **TempVoice** | Auto-delete when empty |

### Custom Bot: GoonsClawbot (Separate Application)
GoonsClawbot runs as its **own separate Discord application** so it does not conflict with OpenClaw or any other bot sharing tokens.
*   **Script**: `goons_clawbot.py` (Python, `discord.py`)
*   **Permissions**: Administrator
*   **Access**: Locked down to Admin Roles & authorized Bot roles ONLY

#### How to Create the Separate Bot Application
1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Click **New Application** and name it **GoonsClawbot**.
3.  Go to the **Bot** tab and click **Reset Token** to generate a new, unique token.
4.  Under *Privileged Gateway Intents*, enable:
    *   ✅ Server Members Intent
    *   ✅ Message Content Intent
5.  Save the new token into your `d:\Clawbot\.env` file as `DISCORD_BOT_TOKEN`.
6.  Go to **OAuth2 > URL Generator**, select scopes `bot` + `applications.commands`, and permissions `Administrator`.
7.  Copy the generated invite URL and use it to add GoonsClawbot to your server.
8.  Restart the bot: `d:\Clawbot\.venv\Scripts\python.exe d:\Clawbot\goons_clawbot.py`

### Sapphire Bot Configuration Guide (Already on Server)
Sapphire handles UI-heavy and event-driven tasks so GoonsClawbot can focus on AI, GitHub, and security. Configure Sapphire via its web dashboard at **[sapph.xyz](https://sapph.xyz)**.

#### Welcome Embeds (offloads `!welcome` from GoonsClawbot)
1.  Go to **sapph.xyz > Your Server > Modules > Welcome**.
2.  Enable the module and select the `#welcome` channel.
3.  Customize the embed: set the title to `⚔️ Welcome to Apptivators Academy!`, add the Call to Arms description, set the color, and add a thumbnail/banner image.
4.  Enable variables like `{user.mention}`, `{server.name}`, and `{server.memberCount}`.

#### Reaction Roles (for #roles channel)
1.  Go to **sapph.xyz > Your Server > Modules > Reaction Roles**.
2.  Create a new reaction role panel targeting the `#roles` channel.
3.  Add roles for Skill Levels and Interests:
    *   1️⃣ The Noob (Level 0) — 2️⃣ The Beginner (Level 1) — 3️⃣ The Intermediate (Level 2-3) — 4️⃣ The Expert (Level 4) — 5️⃣ The God (Level 5)
    *   🐍 Python — ☕ Java — 🌐 Web Dev — 🤖 AI/ML — 🔒 Cybersecurity — 🎓 Mentor
4.  Choose display mode: **Dropdown Menu** (cleanest) or **Button Reactions**.

#### Auto-Moderation & Logging
1.  Go to **sapph.xyz > Your Server > Modules > Auto-Moderation**.
2.  Enable filters for spam, excessive mentions, invite links, and (beta) AI-powered language detection.
3.  Under **Modules > Logging**, enable audit logs and select an admin-only `#mod-logs` channel.

#### Join Roles
1.  Go to **sapph.xyz > Your Server > Modules > Join Roles**.
2.  Assign a default "New Member" role on join so users get baseline permissions while they complete onboarding.


---

## 3. Server Channel Structure

### Welcome & Information
*   `#welcome`: Landing page. Features the Best FREE UI Logo Banner and the "Call To Arms" onboarding embed (via Sapphire).
*   `#rules`: Contains server guidelines. **Edits applied**: Removed the word "Email" (replaced with "User Id"). Mentions the strict anti-malware policy (Instant Snapshot of User IDs). Includes instructions on how Admins/Mods/Bots can open private channels for false-positive reporting.
*   `#announcements`: A space for admins to post important updates, new events, or community milestones.
*   `#roles`: Self-assignable tags (e.g., "Python Learner," "Mentor") via Sapphire reaction roles.
*   `#github-shared-links`: Public channel hooked to GitHub Webhooks. *Integrated with: https://github.com/whagan1310-droid?tab=repositories*

> **📚 Main Server GitHub Repo Library (Public):** [Apptivators Academy](https://github.com/whagan1310-droid/Apptivators-Academy) — This is the community's central code repository. All shared code, assets, snippets, and collaborative projects live here.

### Community & Collaboration
*   `#resources`: Curated tutorials, guides, and learning materials.
*   `#showcase`: Space to share finished projects, receive feedback, and collaborate.
*   `#memes`: A lighthearted space for tech and programming-related humor.
*   `#career-growth`: Sharing job opportunities, internships, and interview prep.

### Support & Technical Help
*   `#help-desk`: Primary ticket-based area for technical assistance (Integrated with Helper.gg bot).
*   `#code-reviews`: Space to post code snippets for pro-level feedback (OpenCode AI / Gemini can auto-respond here).
*   `#quick-questions`: For short, simple questions that don't require deep discussion.
*   `#learning-groups`: Channels for specific study groups (e.g., zero-to-employed bootcamps).

### Language-Specific Categories
*   *Web Development*: `#html-css`, `#javascript`, `#react`, `#angular`
*   *Backend & Data*: `#python`, `#java`, `#c-plus-plus`, `#rust`
*   *Specialty Topics*: `#ai-machine-learning`, `#devops`, `#cybersecurity`

---

## 4. Onboarding: ⚔️ A Call to Arms: One App at a Time ⚔️

Welcome to the front lines of creation. This community exists for one reason: to fuel our passions and build a safer, better tomorrow through the power of code. Whether you are a "Noob" or a "God," your contribution is the engine of our collective growth.

**Requirement:** Choose your purpose for joining the Server and give yourself a Skill Level Rating (1-5). Everyone has a place.

*   **1. The Noob (Trainee / Level 0)**
    *   *Profile*: Struggles with basic syntax and logic. Relies heavily on tutorials/AI.
    *   *Focus*: Learning fundamentals (variables, loops) and setting up dev environments.
*   **2. The Beginner (Junior Developer / Level 1)**
    *   *Profile*: Can build small, functional apps. Knows core language and basic Git.
    *   *Focus*: Writing workable code and learning to debug independently.
*   **3. The Intermediate (Mid-Level Developer / Level 2-3)**
    *   *Profile*: The "workhorse" building defined features with minimal supervision. Knows APIs, databases.
    *   *Focus*: Code quality, performance optimization, and CI/CD pipelines.
*   **4. The Expert (Senior / Staff / Principal Architect)**
    *   *Profile*: Solves complex architectural problems and mentors others. Sets technical strategy.
    *   *Focus*: System reliability, cross-functional leadership, and setting engineering standards.
*   **5. The "God" (Distinguished Engineer / Living Legend)**
    *   *Profile*: Impacts the entire industry. Authors major industry standards or frameworks.
    *   *Focus*: Innovation, visionary leadership, and long-term technical evolution.

### 🛡️ The Guard: Safety & Moderation
Security is a shared responsibility. We treat every member with respect and every flag with caution.
*   **Level 2 & Up**: You are our active mentors. If you see a question, answer it. If you see a struggle, guide it.
*   **Level 4 & 5 (Community Leaders)**: We look to you as our shields. Use your expertise to identify Malware, sniff out False Positives, and debug critical `.bat` or `.lua` errors.
*   **The Golden Rule**: Treat all Ban Flags as False Positives first. We are a community of humans, not just data points. However, if code is *Confirmed Malware*, it is your duty to flag it immediately.

### 💡 The Forge: Learning & Growth
Every new language is a milestone; every forward-thinking AI prompt is a tool for a new era.
*   **Contribute Everywhere**: Fill the channels. If a channel doesn't exist for your niche, request it or create it.
*   **Value is Knowledge**: Share sites, documentation, and repos. A repository with a solid DOCS page is worth its weight in gold.
*   **The Master Archive**: Add everything—code, assets, snippets—to our Community GitHub Repo. This is our collective legacy.

### ⚠️ The Protocol: Public vs. Private
*   **Public Channels**: Remember, the world is watching. Post references, links, and educational content here so the community can LEARN. This is where we showcase our progress and share valuable resources.
*   **Private Channels (The Review Chamber)**: This is our high-security zone for code reviews, sensitive scripts, and deep-dives. We ensure total security here before code is promoted to a Public Channel.
    *   **The Blackout Rule**: Some code is meant to NEVER SEE THE LIGHT OF DAY.
    *   **Total Purge**: To maintain absolute security, you must destroy everything before leaving the channel. When all members exit, the channel will be automatically cleared to ensure a clean slate for the next user. (A bot workflow handles this).

### 🤖 The Synthetic Edge
Our Technical Bots are powerful, but they learn from us. Help us refine them daily by identifying errors and improving their logic. With AI and human intuition combined, we are unstoppable.

*"One App At A Time."*
Build it. Share it. Protect it.

---

## 5. Server Rules & Development Guidelines

### 1. Open Source & Code Sharing Policy
*   **Freely Shared Code**: This is a collaborative space. Any and all code viewable in public channels is shared freely for the community to learn from and use.
*   **Private Collaboration**: If you have proprietary work or code you do not wish to share publicly, please use the Private Channels available upon request. *(Note: Private Channels have elevated controls and are managed by Admins, Moderators, and Bots for specific purposes.)*
*   **Documentation Requirements**: When sharing or requesting help with code, you must provide one of the following:
    *   The open code snippet directly.
    *   References to a GitHub, GitLab, or Bitbucket repository.
    *   Direct links to the source or a clear claim of authorship.
*   **Third-Party Compliance**: All shared material must adhere to the rules of the third-party site it originates from (e.g., GitHub's Terms of Service).

### 2. Malicious Content & Security
*   **Zero Tolerance for Malware**: If a bot, moderator, or admin marks code as Malicious, it will be immediately removed from public view.
*   **Strike System**: Members posting malicious code will receive a formal Strike on their record. This includes phishing, malware, or deceptive scripts.
*   **Immediate Review**: Once flagged, the user's status is placed "Under Review." No final ban will occur until a full human review is completed.

### 3. Fair Review & Ban Appeals
*   **Right to Explain**: If you are flagged for a serious violation, you have one (1) chance to explain your actions. This explanation will be recorded as part of your case file.
*   **Agreement Requirement**: A ban requires a finding of fault and the unanimous agreement of at least three (3) Admins or Moderators.
*   **Case Records**: All Discord text interactions between the member and Staff/Bots are kept under a unique Ban File Number.
*   **Full Disclosure**: Banned members will receive a full copy of their case file via email. Note: You must provide a valid email address to start the review process. Failure to participate in the review or provide an email will result in an automatic, final ban.
*   **Data Destruction**: Upon a confirmed final ban, all code submitted by that member to the server will be destroyed.
*   **Reinstatement**: All moderators have the right to review past bans for potential reinstatement if new evidence or significant growth is shown.

### 4. Community Conduct (The Human Element)
*   **Zero Harassment**: We have a strict policy against bullying, hate speech, and harassment.
*   **No Personal Attacks**: This includes religion bashing, political "smashing," or discrimination of any kind. This is a multicultural server; keep your personal worldviews to yourself to ensure a creative environment.
*   **Truthfulness**: Do not spread "Fake News," misinformation, or intentional lies. Content that could lead to physical or societal harm will be removed.
*   **The Coding Creed**: Coding doesn't care who you pray to or support. In the end, it’s just binary:
    *   `01101011 01100101 01100101 01110000 00100000 01101001 01110100 00100000 01110011 01101001 01101101 01110000 01101100 01100101` (Keep it simple)
    *   `01101111 01101110 01100101 00100000 01100001 01110000 01110000 00100000 01100001 01110100 00100000 01100001 00100000 01110100 01101001 01101101 01100101` (One app at a time)

## 6. Implementation Tips & Server Setup

### Setting Up Official Rules Screening (Membership Screening)
Discord's built-in "Rules Screening" is the most effective way to ensure members see and agree to these rules before participating.
1.  **Enable Community**: You must first set your server as a "Community". Go to **Server Settings > Enable Community** and follow the prompts.
2.  **Access Rules Screening**: Navigate to **Server Settings > Safety Setup**. Under *DM and Spam Protection*, click **Edit** next to "Members must accept rules before they can talk or DM".
3.  **Configure Rules**: Click **Get Started** to add your specific rules regarding open code sharing, zero tolerance for malware, and ban procedures.
4.  **Finalize**: Once saved, new members will be met with a snapshot of these rules and must check a box to agree before they can interact.

### Creating Visual Rule "Snapshots" (Embeds & Banners)
To make your rules channel look professional rather than a plain text list, use these methods:
*   **Embeds with Discohook**: Use [Discohook](https://discohook.org/) to create professional-looking embedded messages. Set up a webhook in your `#rules` channel, paste the URL into Discohook, and format your rules. *(A JSON template for this is available if needed).*
*   **Rules Banner**: Create a custom image banner (recommended size 750 x 350 pixels). Add your Best FREE UI Logo and the word "Rules," then post it at the top of your `#rules` channel for a polished look.
*   **Read-Only Configuration**: To ensure only your "snapshot" is visible, right-click the `#rules` channel, select **Edit Channel > Permissions**, and disable "Send Messages" for the `@everyone` role.

### Managing the "Open Code" Policy
*   **Pinned Messages**: Pin the rules message so it stays accessible at the top of the channel's pin icon.
*   **Strike Recording**: Use Dyno, MEE6, or your custom GoonsClawbot to record "strikes." Commands like `!strike @user [reason]` can help moderators manage permanent case records internally.

---

## 7. API Keys and Tokens Configuration (Free Tiers)

To power your custom Discord Bot and the Gemini AI Integration without spending money, you will need to acquire specific access keys. **Always attempt to use the Free Tiers first before considering any paid upgrades.** Keep these keys absolutely secret; never post them in any public or shared channels.

### 1. Discord Bot Token (Always Free)
To run your custom scripts (like the Auto-Purge bot or OpenCode AI), Discord requires a Bot Token.
*   **Where to get it**: Go to the [Discord Developer Portal](https://discord.com/developers/applications).
*   **Steps**:
    1. Click **New Application** and name your bot (e.g., "GoonsClawbot"is added already and has admin Permissions).
    2. Go to the **Bot** tab on the left menu.
    3. Under *Privileged Gateway Intents*, turn on **Server Members Intent** and **Message Content Intent** (required for the bot to read messages and manage users).
    4. Click the **Reset Token** button to generate your unique Bot Token. Copy this and save it securely.

### 2. Google Gemini API Key (Generous Free Tier)
To give your bot AI capabilities (processing text, images, and code reviews), you need access to the Google Gemini API. The **Gemini 1.5 Flash** model has an extremely generous free tier perfect for Discord servers.
*   **Where to get it**: Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Steps**:
    1. Sign in with a Google account.
    2. Click **Get API key** (or "Create API Key").
    3. Generate the key for a new project.
    4. *Note on Free Tier*: The free tier for Gemini 1.5 Flash allows for up to 15 Requests Per Minute (RPM) completely free of charge. You do not need to enter billing information to use the free tier.

### How to Apply the Keys
All secrets are stored locally in `d:\Clawbot\.env` (protected by `.gitignore` — **never committed to any public repo**). Your Python scripts load them automatically via `os.getenv()`.

The `.env` file contains:
*   `DISCORD_BOT_TOKEN` — Your Discord bot token
*   `GOOGLE_API_KEY` — Your Gemini 1.5 Flash API key
*   `GITHUB_PAT` — Your fine-grained GitHub Personal Access Token

To load them manually in PowerShell before running a script:
```powershell
Get-Content .env | ForEach-Object { if ($_ -match '^([^#].+?)=(.+)$') { [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
```

---

## 8. GitHub Deployment & Repository Integration

### Deployment Target
Once the custom bot is built and all build plan files are finalized, the entire build plan will be pushed to:

> 📦 **[Discord-Build-Plan-Apptivators-Academy](https://github.com/whagan1310-droid/Discord-Build-Plan-Apptivators-Academy)**

This repository serves as the **public-facing blueprint** for the Discord server. It will contain:
*   `discord_server_build_plan.md` — The master plan
*   `discord_channel_definitions.md` — Channel purpose definitions
*   `github_readme_template.md` — The Apptivators Academy README
*   `discohook_rules_template.json` — Visual rules embed template
*   `auto_purge_bot.py` — Custom bot scripts (purge, rules posting, etc.)
*   `openclaw_bot_integration_guide.md` — OpenClaw/Gemini integration steps

### Authentication
A fine-grained GitHub Personal Access Token (PAT) is stored securely in the local `.env` file. It is used by the custom bot for automated pushes and API access across repositories.
*   **Reference**: [GitHub Docs — Fine-Grained PATs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#fine-grained-personal-access-tokens)
*   **Reference**: [GitHub REST API Docs](https://docs.github.com/en/rest)

### Public GitHub Resources (Reference Links)
*   [GitHub Docs (Main)](https://docs.github.com/en)
*   [GitHub REST API](https://docs.github.com/en/rest)
*   [GitHub Webhooks](https://docs.github.com/en/webhooks)
*   [GitHub Actions (CI/CD)](https://docs.github.com/en/actions)
*   [Fine-Grained Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Deployment Trigger
The custom bot will include a `!deploy_plan` admin command that:
1.  Reads all build plan files from the local `d:\Clawbot` directory.
2.  Authenticates with GitHub using the PAT from `.env`.
3.  Commits and pushes the files to the `Discord-Build-Plan-Apptivators-Academy` repo.
4.  Reports success/failure back to the admin in Discord.

### 📖 Reference: Building a Discord Bot That Writes to GitHub

> **Key Concept**: The Discord-GitHub webhook integration only sends *notifications from GitHub to Discord*. It does **not** allow a Discord bot to interact with the repository. To make a Discord bot add content to a GitHub repo, you must write custom code that uses the **GitHub REST API**.

#### Prerequisites
*   A **GitHub account** and a **Personal Access Token (PAT)** with the necessary repository permissions (e.g., `repo` or `public_repo` scope). Using a PAT is more secure than a password.
*   A **Discord bot account** set up in the [Discord Developer Portal](https://discord.com/developers/applications) with its own bot token.
*   A **self-hosted environment** (e.g., your own computer, a VPS, or a cloud service) to run your bot, as it needs to be online to listen for commands.
*   A **programming language environment** installed (e.g., Python with `discord.py` and `requests`, or Node.js with `discord.js` and `@octokit/rest`).

#### Step 1: Generate a GitHub Personal Access Token (PAT)
1.  Go to your GitHub account settings: **Developer settings > Personal access tokens > Tokens (classic)**.
2.  Click **Generate new token (classic)** and give it a descriptive name.
3.  Select the appropriate scopes (permissions) for repository access (e.g., `repo` for private repos or `public_repo` for public ones).
4.  Copy the generated token immediately (you will not be able to see it again).
5.  Store this token securely in your `.env` file as `GITHUB_PAT`. ✅ *(Already done)*

#### Step 2: Set Up Your Discord Bot Project
1.  Create a project directory and install the necessary libraries:
    *   **Python**: `pip install discord.py requests python-dotenv`
    *   **Node.js**: `npm install discord.js @octokit/rest dotenv`
2.  Store both your GitHub PAT and Discord bot token as environment variables in `.env`. ✅ *(Already done)*

#### Step 3: Implement GitHub API Logic in Your Bot
*   Use an HTTP library or a dedicated GitHub library (like `Octokit` in Node.js or `requests` in Python) to make authenticated API calls to GitHub when your bot receives a specific command.
*   Example: A command like `!addfile <filename> <content>` would trigger the bot to send a `PUT` request to the [GitHub Contents API](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents) to create/update a file in the repository.

#### Step 4: Host and Run the Bot 24/7
*   The bot needs to be running continuously to listen for commands.
*   **Free/Low-Cost Options**: Your local machine, [Replit](https://replit.com), [Railway.app](https://railway.app), or [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/).
*   **Alternative (No Code)**: Use a third-party integration service like [Relay.app](https://relay.app) or [n8n.io](https://n8n.io) if you prefer a less technical solution.
