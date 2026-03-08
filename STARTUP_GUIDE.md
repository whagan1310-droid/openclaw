# 🚀 Apptivators Academy: Startup & Deployment Guide

Welcome to the official deployment guide for the Apptivators Academy infrastructure. This document provides step-by-step instructions to get the **GoonsClawbot** and server environment running from scratch.

## 🛠️ Prerequisites
- **Python 3.10+**: Ensure Python is installed and added to your PATH.
- **Git Bash**: Required for running the monorepo build scripts.
- **Discord Developer Account**: To create and manage your bot application.
- **Google AI Studio Key**: Required for the Gemini AI (`!ask`) features.

## 📦 Stage 1: Environment Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/whagan1310-droid/Apptivators-Academy.git
   cd Apptivators-Academy
   ```
2. **Create Virtual Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure Secrets**: Create a `.env` file in the root directory:
   ```env
   DISCORD_BOT_TOKEN=your_token_here
   GOOGLE_API_KEY=your_gemini_key_here
   GITHUB_PAT=your_github_pat_here
   ```

## 🏗️ Stage 2: Server Architecture Auto-Build
Before running the bot, use the structural setup script to generate the channel hierarchy defined in the build plan.
1. Run the setup script:
   ```powershell
   .\.venv\Scripts\python.exe setup_server.py
   ```
2. This will automatically create:
   - 📢 Welcome & Information Categories
   - 💻 Language-Specific Categories
   - 🔒 Secure Review Chambers

## 🤖 Stage 3: Bot Launch & Initialization
1. **Start the Bot**:
   ```powershell
   .\.venv\Scripts\python.exe goons_clawbot.py
   ```
2. **Initialize Onboarding**: In any text channel, run:
   ```
   !initialize_onboarding
   ```
   *This deploys the persistent Interactive GUIs to `#welcome` and `#rules`.*

## 🛡️ Verification Checklist
- [ ] Bot shows as "Online" in Discord.
- [ ] `#welcome` contains the Level 1-5 selection buttons.
- [ ] `#rules` contains the "Wonder Quote" and Agreement buttons.
- [ ] `!ask` responds correctly with Gemini AI.

---
*"One App At A Time."* ⚔️🛡️🤖
