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

### Option 2: Custom Animated GIFs (Highly Recommended)
To preserve the exact colored glowing siren visual you had originally:
1. Upload the `red_siren.gif`, `amber_siren.gif`, `blue_siren.gif`, and `green_siren.gif` files as **Custom Emojis** in your Discord Server Settings.
2. Once uploaded, type `\:red_siren:` in your Discord chat to get the exact ID (it will look like `<a:red_siren:123456789012345>`).
3. Copy those exact IDs into the S.A.M.P.I.RT alert map here:

```python
# In bots/S.A.M.P.I.RT/sampi_rt_bot.py
ALERT_ASSETS = {
    "CRITICAL": {
        "color": discord.Color.red(),
        "siren": "<a:red_siren:YOUR_RED_ID_HERE>", # Replace with custom emoji ID
        "avatar": "https://raw.githubusercontent.com/whagan1310-droid/openclaw/main/docs/assets/bots/sampirt_crimson.png",
        "label": "🚨 CRITICAL: SECURITY BREACH NEUTRALIZED 🚨"
    },
    # ... update HIGH, MEDIUM, LOW equivalently
}
```

By using Custom Emojis inside the `siren` field of the embed thumbnail/image, Discord will render the animated GIFs directly from your server's emoji library in high resolution!
