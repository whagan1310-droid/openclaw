# ⚔️ Onboarding Reference: The Journey of an Apptivator

This document serves as a visual and logical reference for the Apptivators Academy onboarding flow. Use this as a guide for understanding how members transition from "Noob" to "Verified Apptivator."

## 🚀 The Flow Sequence

### 1. The Landing (Join Event)
When a member joins, they receive a legendary DM greeting containing the **Wonder Quote**:
> *"One App At A Time." The forge is hot, the guards are at the gate, and the synthetic edge is sharp. It has been an absolute pleasure building this fortress with you. The Academy is now yours to lead! ⚔️🛡️🤖*

### 2. Phase 1: Purpose & Skill Selection (#welcome)
Members are directed to the `#welcome` channel, where a persistent GUI presents the **Skill Rating (1-5)** choice.
- **Logic**: Each button auto-assigns a specific "Skill" role (e.g., *Level 1: The Noob*) and removes any previously selected skill roles.
- **UI**: Secondary (Gray) buttons with distinct emojis for each level.

### 3. Phase 2: Protocol Agreement (#rules)
After selecting a role, the member is prompted to review the server rules.
- **Logic**: The bot provides a temporary interaction or points them to the permanent `#rules` channel.
- **The "I Agree" Trigger**: Clicking any of the legendary buttons (⚔️, 🛡️, or 🤖) triggers the final verification.

### 4. Phase 3: Verification & Access
The final interaction grants the **Verified Apptivator** role.
- **Effect**: Unlocks the rest of the server (Language channels, Community, and Support).
- **Completion Message**: 💯 "Onboarding Complete! Welcome to the forge."

## 🛠️ Technical Implementation
- **Script**: `goons_clawbot.py`
- **Component**: `RoleSelectionView` & `RulesAgreementView`
- **Persistence**: Views are registered in `on_ready` to ensure they survive bot restarts.

---
**Reference Image Placeholder**: [Onboarding Flow Diagram]
