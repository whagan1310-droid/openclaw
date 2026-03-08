# Local LLaMA Setup Guide for OpenClaw (Windows)

> **Goal**: Run a free, local LLaMA model on your PC so your OpenClaw bot has a working LLM brain — no API keys, no monthly bills.

---

## Overview

OpenClaw has **built-in Ollama support** with auto-discovery, streaming, and tool calling. The easiest path is:

1. Install **Ollama** (a lightweight local LLM runtime)
2. Pull a **LLaMA model** (or any open-source model)
3. Point OpenClaw at Ollama with one config change

That's it. No API keys to pay for.

---

## Prerequisites

| Requirement | Minimum | Recommended |
|---|---|---|
| **RAM** | 8 GB | 16–32 GB |
| **Disk space** | ~5 GB (for a small model) | ~20 GB (for a larger model) |
| **GPU (optional but helps)** | Any NVIDIA card with 6+ GB VRAM | NVIDIA RTX 3060 12 GB or better |
| **OS** | Windows 10/11 | Windows 11 |

> [!TIP]
> You can run models **CPU-only** (no GPU needed), just slower. If you have an NVIDIA GPU, Ollama will use it automatically.

---

## Step 1 — Install Ollama

1. Go to **https://ollama.ai** and click **Download for Windows**
2. Run the installer — it's a straightforward next-next-finish wizard
3. Once installed, Ollama runs as a background service automatically

**Verify it's running** — open PowerShell and run:

```powershell
ollama --version
```

You should see a version number (e.g., `ollama version 0.6.x`).

---

## Step 2 — Pull a LLaMA Model

Open PowerShell and pull the model you want. Here are the best options ranked by quality vs. hardware demand:

### Option A: LLaMA 3.3 (Recommended starter)

```powershell
ollama pull llama3.3
```

- **Size**: ~4.7 GB download
- **RAM needed**: ~8 GB
- **Quality**: Excellent for general chat, coding help, Q&A

### Option B: DeepSeek R1 32B (Reasoning model)

```powershell
ollama pull deepseek-r1:32b
```

- **Size**: ~19 GB download
- **RAM needed**: ~24 GB
- **Quality**: Very strong reasoning; needs good hardware

### Option C: Qwen 2.5 Coder 32B (Best for coding)

```powershell
ollama pull qwen2.5-coder:32b
```

- **Size**: ~19 GB download
- **RAM needed**: ~24 GB
- **Quality**: Exceptional at code generation and review

### Option D: Mistral (Lightweight alternative)

```powershell
ollama pull mistral
```

- **Size**: ~4.1 GB download
- **RAM needed**: ~8 GB
- **Quality**: Good general-purpose model, fast responses

> [!IMPORTANT]
> **Start with `llama3.3`** if you're unsure — it's the best balance of quality and performance for most PCs.

After pulling, verify the model is available:

```powershell
ollama list
```

---

## Step 3 — Test the Model Locally

Before connecting to OpenClaw, make sure the model works:

```powershell
ollama run llama3.3
```

This opens an interactive chat. Type a message and press Enter. If you get a response, the model is working. Type `/bye` to exit.

You can also verify the API is running:

```powershell
curl http://localhost:11434/api/tags
```

You should see a JSON response listing your installed models.

---

## Step 4 — Configure OpenClaw to Use Ollama

### 4a. Set the Ollama API key environment variable

Ollama doesn't need a real API key, but OpenClaw needs a value set to enable the provider. Open PowerShell and run:

```powershell
# Set it for the current session
$env:OLLAMA_API_KEY = "ollama-local"

# OR set it permanently (recommended)
[System.Environment]::SetEnvironmentVariable("OLLAMA_API_KEY", "ollama-local", "User")
```

> [!NOTE]
> After setting the permanent variable, **restart your terminal** (or reboot) for it to take effect.

Alternatively, use the OpenClaw CLI:

```powershell
openclaw config set models.providers.ollama.apiKey "ollama-local"
```

### 4b. Set the model as your primary model

Create or edit your OpenClaw config file at `~/.openclaw/openclaw.json` (or wherever your config lives):

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/llama3.3",
      },
    },
  },
}
```

> [!TIP]
> Replace `llama3.3` with whichever model you pulled in Step 2 (e.g., `ollama/mistral`, `ollama/deepseek-r1:32b`).

### 4c. Alternative: Use the `openclaw.podman.env` file

Since you already have this file in your project, uncomment and set the Ollama key:

```env
# In openclaw.podman.env, change this line:
OLLAMA_API_KEY=ollama-local
```

---

## Step 5 — Verify the Connection

1. Make sure Ollama is running (it should auto-start, but if not):

```powershell
ollama serve
```

2. Check available models through OpenClaw:

```powershell
openclaw models list
```

You should see your Ollama models listed with `$0.00` cost.

3. Check channel status:

```powershell
openclaw channels status --probe
```

---

## Step 6 — Send a Test Message

Send a message to your bot through whichever channel you have configured (Telegram, Discord, etc.). The bot should now respond using the local LLaMA model!

---

## Troubleshooting

### "No models available"

OpenClaw auto-discovers only models with **tool support**. If your model isn't showing up:

```powershell
# Pull a model known to support tools
ollama pull llama3.3

# Or define the model explicitly in config (see explicit config below)
```

### "Connection refused"

Make sure Ollama is running:

```powershell
# Check if running
tasklist | findstr ollama

# Start it manually if needed
ollama serve
```

### Responses are very slow

- **Close other apps** to free up RAM
- **Try a smaller model**: `ollama pull mistral` or `ollama pull llama3.2:3b`
- **Check GPU utilization**: If you have an NVIDIA GPU, run `nvidia-smi` to confirm it's being used

### Model not responding or returning garbage

Try a different model — some quantized variants don't work well with tool calling:

```powershell
ollama pull llama3.3
ollama pull qwen2.5-coder:32b
```

---

## Explicit Configuration (Advanced)

If auto-discovery doesn't work or you want full control, define the provider manually:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "ollama/llama3.3",
      },
    },
  },
  models: {
    providers: {
      ollama: {
        baseUrl: "http://127.0.0.1:11434",
        apiKey: "ollama-local",
        api: "ollama",
        models: [
          {
            id: "llama3.3",
            name: "LLaMA 3.3",
            reasoning: false,
            input: ["text"],
            cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
            contextWindow: 8192,
            maxTokens: 81920,
          },
        ],
      },
    },
  },
}
```

> [!WARNING]
> Do **NOT** use the `/v1` URL (e.g., `http://localhost:11434/v1`). This breaks tool calling. Always use the base URL: `http://127.0.0.1:11434`

---

## Quick Reference

| Command | What it does |
|---|---|
| `ollama pull llama3.3` | Download a model |
| `ollama list` | List installed models |
| `ollama run llama3.3` | Interactive chat with a model |
| `ollama serve` | Start the Ollama server |
| `ollama rm <model>` | Delete a model to free disk space |
| `openclaw models list` | See what models OpenClaw can use |
| `openclaw config set models.providers.ollama.apiKey "ollama-local"` | Enable Ollama in OpenClaw |

---

## Summary

```
1. Install Ollama          → https://ollama.ai (download + install)
2. Pull a model            → ollama pull llama3.3
3. Set the env variable    → OLLAMA_API_KEY=ollama-local
4. Configure OpenClaw      → set primary model to "ollama/llama3.3"
5. Restart and test        → openclaw models list
```

**Total cost: $0. Forever.**
