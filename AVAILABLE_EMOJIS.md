# 🚨 Apptivators Academy: Available Emojis & Sirens 🚨

This document tracks the official visual sirens and emojis used by the **S.A.M.P.I.RT** security engine and other Forge bots to ensure consistent, large alerts across the server.

## S.A.M.P.I.RT Alert Sirens

Since the original animated `.gif` sirens were stored in the private Build Plan repository, you have two options to keep them "large as they are" in S.A.M.P.I.RT's alerts:

### Option 1: Standard Discord Emojis (Immediate Use)
You can use standard, built-in Discord emojis. When placed by themselves or at the top of an embed, they provide clear visual indicators:
- **CRITICAL**: 🚨 (`:rotating_light:`)
- **HIGH**: ⚠️ (`:warning:`)
- **MEDIUM**: 🛡️ (`:shield:`) or 🔵 (`:blue_circle:`)
- **LOW**: 🟢 (`:green_circle:`) or ✅ (`:white_check_mark:`)

### Option 2: High-Resolution Siren Globes (Now Default)
Since the GitHub token returned a permissions error for the private repository, we have successfully replaced the old private GIFs with **High-Resolution Static Siren Globes** directly in the public `openclaw` repository!

These large, high-quality siren images (`siren_red_large.png`, `siren_amber_large.png`, `siren_blue_large.png`, `siren_green_large.png`) are already injected into `sampi_rt_bot.py` and require no further setup on your part.

*If you ever want them to animate again, upload the original GIFs to Discord as Custom Emojis and map their Discord `<\:emoji_name:id>` tags into the `siren` field in `sampi_rt_bot.py`.*
