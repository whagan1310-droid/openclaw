# 🦞 Build Your Own OpenClaw — Full Implementation Plan

> **Generated:** March 7, 2026
> **Source repo:** https://github.com/whagan1310-droid/openclaw
> **Upstream:** https://github.com/openclaw/openclaw (273K+ ⭐, MIT License)
> **Project dir:** `d:\Clawbot`

---

## 1. Repository Analysis

### What is OpenClaw?

OpenClaw is a personal AI assistant you run on your own devices. It answers you on the channels you already use (WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, BlueBubbles, IRC, Microsoft Teams, Matrix, Feishu, LINE, Mattermost, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo, WebChat). It can speak and listen on macOS/iOS/Android, and can render a live Canvas you control.

The Gateway is just the control plane — the product is the assistant.

### Tech Stack

| Layer | Technology |
|---|---|
| **Core Runtime** | Node.js ≥22, TypeScript, pnpm monorepo |
| **Gateway** | WebSocket server on `ws://127.0.0.1:18789` |
| **Agent** | Pi agent runtime (RPC mode, tool/block streaming) |
| **Build** | tsdown (bundler), tsx (dev runner), Vitest (tests) |
| **macOS App** | Swift / SwiftUI (menu bar app) |
| **iOS App** | Swift / SwiftUI (XcodeGen project) |
| **Android App** | Kotlin / Jetpack Compose |
| **Voice** | Swabble (Swift Package for wake word detection) |
| **Linting** | oxlint, oxfmt, SwiftLint, ktlint |
| **Config** | JSON5 (`~/.openclaw/openclaw.json`) |
| **Packaging** | Docker, npm, launchd/systemd daemon |

### Architecture Overview

```
WhatsApp / Telegram / Slack / Discord / Google Chat / Signal / iMessage /
BlueBubbles / IRC / Microsoft Teams / Matrix / Feishu / LINE / Mattermost /
Nextcloud Talk / Nostr / Synology Chat / Tlon / Twitch / Zalo / WebChat
                          │
                          ▼
              ┌───────────────────────┐
              │       Gateway         │
              │   (control plane)     │
              │ ws://127.0.0.1:18789  │
              └──────────┬────────────┘
                         │
              ┌──────────┼──────────────┐
              │          │              │
         Pi agent     CLI          WebChat UI
         (RPC)    (openclaw …)     (Lit components)
              │
    ┌─────────┼─────────────┐
    │         │             │
 macOS app  iOS node   Android node
```

### Source Directory Map (`src/` — 50+ modules)

| Directory | Purpose |
|---|---|
| `src/gateway/` | WebSocket server, HTTP endpoints, Tailscale integration |
| `src/agents/` | Agent config, prompt injection, workspace mgmt |
| `src/channels/` | Channel routing engine, message normalization |
| `src/sessions/` | Session lifecycle, pruning, agent-to-agent tools |
| `src/whatsapp/` | WhatsApp connector (Baileys library) |
| `src/telegram/` | Telegram connector (grammY framework) |
| `src/discord/` | Discord connector (discord.js) |
| `src/slack/` | Slack connector (Bolt framework) |
| `src/signal/` | Signal connector (signal-cli) |
| `src/imessage/` | iMessage connector (legacy + BlueBubbles) |
| `src/line/` | LINE connector (@line/bot-sdk) |
| `src/browser/` | CDP-based browser control (Playwright) |
| `src/canvas-host/` | A2UI visual workspace host |
| `src/cron/` | Cron job scheduling engine |
| `src/cli/` | CLI command framework (Commander.js) |
| `src/config/` | JSON5 configuration system |
| `src/providers/` | LLM provider abstraction (OpenAI, Anthropic, Google, etc.) |
| `src/media/` | Media processing pipeline (sharp for images) |
| `src/media-understanding/` | Image/audio/video analysis via LLM |
| `src/link-understanding/` | URL content extraction (@mozilla/readability) |
| `src/tts/` | Text-to-speech (ElevenLabs, node-edge-tts) |
| `src/memory/` | Long-term memory (LanceDB vector store) |
| `src/context-engine/` | Context management and token budgeting |
| `src/security/` | Sandbox, pairing, auth (Docker isolation) |
| `src/pairing/` | DM pairing codes and allowlists |
| `src/hooks/` | Lifecycle hooks for message processing |
| `src/web/` | Web UI (Dashboard + WebChat, Lit components) |
| `src/wizard/` | Onboarding wizard (interactive CLI) |
| `src/plugin-sdk/` | Plugin SDK for extensibility |
| `src/plugins/` | Built-in plugins (channels, tools, features) |
| `src/tui/` | Terminal UI interface |
| `src/terminal/` | Terminal/PTY management |
| `src/process/` | Process execution (bash, sandboxed exec) |
| `src/daemon/` | Daemon management (launchd/systemd) |
| `src/routing/` | Message routing logic |
| `src/shared/` | Shared types and utilities |
| `src/types/` | TypeScript type definitions |
| `src/utils/` | Utility functions |
| `src/secrets/` | Secret management |
| `src/infra/` | Infrastructure utilities |
| `src/logging/` | Logging framework (tslog) |
| `src/i18n/` | Internationalization |
| `src/markdown/` | Markdown parsing/rendering |
| `src/acp/` | Agent Client Protocol integration |
| `src/auto-reply/` | Auto-reply logic |
| `src/compat/` | Backward compatibility layer |
| `src/node-host/` | Device node hosting (camera, screen, location) |
| `src/docs/` | Documentation generation |
| `src/scripts/` | Build/dev scripts |

### Native Apps

| Directory | Platform | Language | Build System |
|---|---|---|---|
| `apps/macos/` | macOS menu bar app | Swift/SwiftUI | Swift Package Manager |
| `apps/ios/` | iOS + watchOS apps | Swift/SwiftUI | XcodeGen + Xcode |
| `apps/android/` | Android app | Kotlin/Compose | Gradle |
| `Swabble/` | Voice wake word engine | Swift | Swift Package Manager |

### Key Dependencies

| Package | Purpose |
|---|---|
| `@whiskeysockets/baileys` | WhatsApp Web API |
| `grammy` | Telegram Bot API |
| `discord.js` + `@discordjs/voice` | Discord bot + voice |
| `@slack/bolt` + `@slack/web-api` | Slack bot |
| `@line/bot-sdk` | LINE messaging |
| `playwright-core` | Browser automation |
| `@mariozechner/pi-agent-core` | Pi agent runtime |
| `@mariozechner/pi-ai` | AI provider abstraction |
| `express` | HTTP server |
| `ws` | WebSocket server |
| `commander` | CLI framework |
| `sharp` | Image processing |
| `node-edge-tts` | Text-to-speech |
| `sqlite-vec` | Vector search (memory) |
| `zod` | Schema validation |
| `croner` | Cron scheduler |
| `chokidar` | File watching |

---

## 2. Feature List

### Core Platform
- [x] Gateway WebSocket control plane with sessions, presence, config, cron, webhooks
- [x] CLI surface: `gateway`, `agent`, `send`, `wizard`, `doctor`
- [x] Pi agent runtime in RPC mode with tool streaming and block streaming
- [x] Session model: main for direct chats, group isolation, activation modes
- [x] Media pipeline: images/audio/video, transcription, size caps
- [x] Multi-agent routing: route channels/accounts to isolated agents

### Channels (22+ integrations)
- [x] WhatsApp (Baileys)
- [x] Telegram (grammY)
- [x] Discord (discord.js)
- [x] Slack (Bolt)
- [x] Signal (signal-cli)
- [x] iMessage (legacy + BlueBubbles)
- [x] IRC
- [x] Microsoft Teams
- [x] Google Chat
- [x] Matrix
- [x] Feishu / LINE / Mattermost / Nextcloud Talk / Nostr
- [x] Synology Chat / Tlon / Twitch / Zalo / WebChat

### Tools & Automation
- [x] Browser control: dedicated Chrome/Chromium with CDP
- [x] Canvas A2UI: agent-driven visual workspace
- [x] Nodes: camera snap/clip, screen record, location.get, notifications
- [x] Cron jobs + webhooks + Gmail Pub/Sub
- [x] Skills platform: bundled, managed, and workspace skills (ClawHub)

### Voice
- [x] Voice Wake: wake words on macOS/iOS
- [x] Talk Mode: continuous voice on macOS/iOS/Android
- [x] TTS: ElevenLabs streaming + system TTS fallback

### Apps
- [x] macOS menu bar app (voice wake, PTT, talk mode, WebChat, debug)
- [x] iOS node (canvas, voice wake, talk mode, camera, screen recording)
- [x] Android node (chat, voice, canvas, camera, contacts, calendar, SMS)
- [x] Apple Watch companion app

### Runtime & Safety
- [x] Channel routing, retry policy, streaming/chunking
- [x] Presence, typing indicators, usage tracking
- [x] Model selection, failover, session pruning
- [x] Security: DM pairing, Docker sandboxing, per-session isolation
- [x] Tailscale Serve/Funnel for remote access

### Chat Commands
- `/status` — session status (model + tokens)
- `/new` or `/reset` — reset session
- `/compact` — compact session context
- `/think <level>` — off|minimal|low|medium|high|xhigh
- `/verbose on|off`
- `/usage off|tokens|full`
- `/restart` — restart gateway
- `/activation mention|always` — group activation

---

## 3. Build Instructions

### Prerequisites

```
Node.js >= 22.12.0  (https://nodejs.org)
pnpm >= 10.23.0     (npm install -g pnpm)
Git + Git Bash       (https://git-scm.com)
```

Optional (for native apps):
```
Xcode + XcodeGen    (macOS/iOS apps)
Android Studio      (Android app)
Docker              (sandboxing)
```

### Step 1: Clone & Install

```bash
cd d:\Clawbot
git clone https://github.com/whagan1310-droid/openclaw.git .
pnpm install
```

### Step 2: Build

```bash
# Build the Canvas A2UI, TypeScript, and plugin SDK
pnpm build

# Build the web UI (dashboard + webchat)
pnpm ui:build
```

### Step 3: Configure

Create `~/.openclaw/openclaw.json`:

```json
{
  "agent": {
    "model": "openai/gpt-4o"
  }
}
```

Supported model prefixes:
- `openai/` — GPT-4o, GPT-4.1, etc. (needs `OPENAI_API_KEY`)
- `anthropic/` — Claude Opus/Sonnet (needs `ANTHROPIC_API_KEY`)
- `google/` — Gemini (needs Google auth)
- `xai/` — Grok (needs `XAI_API_KEY`)
- See [Models docs](https://docs.openclaw.ai/concepts/models) for full list

### Step 4: Run Onboarding Wizard

```bash
pnpm openclaw onboard --install-daemon
```

The wizard walks you through:
1. Setting up the gateway
2. Choosing your AI model + API key
3. Configuring channels (Discord, Telegram, etc.)
4. Installing skills
5. Setting up the daemon (auto-start on boot)

### Step 5: Start the Gateway

```bash
# Production mode
pnpm openclaw gateway --port 18789 --verbose

# Development mode (auto-reload on changes)
pnpm gateway:watch
```

### Step 6: Test

```bash
# Send a test message via CLI
pnpm openclaw agent --message "Hello, OpenClaw!"

# Check system health
pnpm openclaw doctor

# Run unit tests
pnpm test

# Run gateway tests
pnpm test:gateway
```

---

## 4. Channel Setup Guides

### Discord

1. Go to https://discord.com/developers/applications
2. Create a new application → Bot → copy the token
3. Enable "Message Content Intent" under Privileged Gateway Intents
4. Add to `openclaw.json`:
   ```json
   {
     "channels": {
       "discord": {
         "token": "YOUR_DISCORD_BOT_TOKEN"
       }
     }
   }
   ```
5. Invite the bot to your server with the OAuth2 URL

### Telegram

1. Talk to @BotFather on Telegram → `/newbot`
2. Copy the bot token
3. Add to `openclaw.json`:
   ```json
   {
     "channels": {
       "telegram": {
         "token": "YOUR_TELEGRAM_BOT_TOKEN"
       }
     }
   }
   ```

### WhatsApp

1. OpenClaw uses the Baileys library (no official API needed)
2. Add to `openclaw.json`:
   ```json
   {
     "channels": {
       "whatsapp": {
         "enabled": true
       }
     }
   }
   ```
3. On first start, scan the QR code with your phone

### WebChat (Built-in)

WebChat works out of the box when the Gateway is running. Access it at the Gateway dashboard URL.

---

## 5. Customization

### Agent Persona

Create/edit files in `~/.openclaw/workspace/`:
- `AGENTS.md` — Agent instructions and behavior
- `SOUL.md` — Personality and tone
- `TOOLS.md` — Tool usage guidelines

### Custom Skills

Create skills in `~/.openclaw/workspace/skills/<skill-name>/SKILL.md`:

```markdown
---
name: my-custom-skill
description: Does something awesome
---

## Instructions
When asked to do X, follow these steps:
1. Step one
2. Step two
```

### Security Configuration

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

- `"off"` — No sandboxing (tools run on host)
- `"non-main"` — Sandbox non-main sessions in Docker
- DM pairing: unknown senders get a pairing code by default

---

## 6. Development Workflow

### Dev Commands

```bash
# Start gateway in dev mode (skips channels, auto-reload)
pnpm gateway:dev

# Start gateway with file watching
pnpm gateway:watch

# Run TUI (terminal UI)
pnpm tui:dev

# Start web UI dev server
pnpm ui:dev

# Run all checks (lint + typecheck)
pnpm check

# Format code
pnpm format

# Run specific test file
pnpm exec vitest run src/path/to/file.test.ts
```

### Native App Development

```bash
# macOS app
cd apps/macos && swift build

# iOS app
pnpm ios:gen    # Generate Xcode project
pnpm ios:open   # Open in Xcode
pnpm ios:build  # Build for simulator

# Android app
pnpm android:assemble  # Build debug APK
pnpm android:install   # Install on device
pnpm android:test      # Run unit tests
```

### Test Suite

```bash
pnpm test              # All unit tests (parallel)
pnpm test:fast         # Fast unit tests only
pnpm test:gateway      # Gateway integration tests
pnpm test:channels     # Channel-specific tests
pnpm test:e2e          # End-to-end tests
pnpm test:extensions   # Extension tests
pnpm test:ui           # Web UI tests
pnpm test:live         # Live API tests (requires API keys)
```

---

## 7. Phased Build Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Clone repository and install dependencies
- [ ] Build TypeScript project
- [ ] Configure LLM provider (API key)
- [ ] Run onboarding wizard
- [ ] Start Gateway and verify CLI messaging works
- [ ] Run `openclaw doctor` to validate setup

### Phase 2: Channel Integration (Week 2-3)
- [ ] Set up Discord bot and connect
- [ ] Set up Telegram bot and connect
- [ ] Set up WhatsApp (QR code pairing)
- [ ] Test WebChat interface
- [ ] Configure DM pairing security

### Phase 3: Tools & Automation (Week 3-4)
- [ ] Enable browser control (install Chromium)
- [ ] Set up cron jobs for scheduled tasks
- [ ] Install skills from ClawHub
- [ ] Configure Canvas A2UI (if on macOS)
- [ ] Set up webhooks for external integrations

### Phase 4: Customization & Branding (Week 4-5)
- [ ] Write custom AGENTS.md persona
- [ ] Create SOUL.md personality file
- [ ] Write custom skills
- [ ] Customize WebChat UI theme
- [ ] Harden security (sandbox, pairing policies)

### Phase 5: Native Apps (Optional, Week 5+)
- [ ] Build macOS menu bar app
- [ ] Build iOS app (requires Mac + Xcode)
- [ ] Build Android app (requires Android Studio)
- [ ] Set up Tailscale for remote access

---

## 8. Useful Links

- **Website:** https://openclaw.ai
- **Docs:** https://docs.openclaw.ai
- **Getting started:** https://docs.openclaw.ai/start/getting-started
- **Configuration reference:** https://docs.openclaw.ai/gateway/configuration
- **Models guide:** https://docs.openclaw.ai/concepts/models
- **Security guide:** https://docs.openclaw.ai/gateway/security
- **Skills docs:** https://docs.openclaw.ai/tools/skills
- **ClawHub (skill registry):** https://clawhub.com
- **Discord community:** https://discord.gg/clawd
- **DeepWiki:** https://deepwiki.com/openclaw/openclaw
- **Vision doc:** https://github.com/openclaw/openclaw/blob/main/VISION.md
