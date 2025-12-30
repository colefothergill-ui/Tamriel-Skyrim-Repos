# Skyrim Fate Core Campaign Vault

Welcome to the **Skyrim Fate Core Campaign Vault** — a comprehensive repository for running a gritty, branching Fate Core campaign set in **4E 201 Skyrim**.

## Repo Purpose

This vault serves as the **single source of truth** for:
- Campaign state (hold control, party alignment, major flags)
- Progress clocks (master, act, and faction-level)
- NPCs, factions, modules, and session logs
- Story hooks and GM workflow tools

The **Dragonborn is absent**. Your PCs shape the outcome of the civil war — and the Thalmor endgame lurking beneath it.

---

## Folder Map

```
/clocks/          — skyrim_clocks.json (master, act, faction clocks)
/state/           — campaign_state.json (hold control, flags, party data)
/modules/         — Act modules and narrative frameworks
/factions/        — Faction packs (Stormcloaks, Imperials, Thalmor, guilds, etc.)
/npcs/            — Named NPCs with aspects, stunts, and relationship clocks
/pcs/             — Player character sheets
/hooks/           — Story hooks organized by act and faction
/logs/            — Session logs with clock/state updates
/rules/           — Fate Core mechanics and quickrefs
/fate-core/       — Fate system toolkit and story tree frameworks
```

---

## Workflow

After each session:
1. **Update `/logs/`** — Use the session template; record key events, PC actions, and narrative outcomes.
2. **Update `/clocks/skyrim_clocks.json`** — Tick relevant master, act, and faction clocks based on session outcomes.
3. **Update `/state/campaign_state.json`** — Adjust hold control, major flags, party alignment, and allies/enemies lists.
4. **Update NPC clocks** — If relationship or personal clocks tick, update individual NPC files in `/npcs/`.
5. **Review `/hooks/`** — Check for triggered hooks or new complications to weave into the next session.

---

## Explicit Details

- **Era:** 4E 201 — The civil war is active; the Dragonborn's absence means no prophecy safety net.
- **PCs Shape Outcomes:** Player decisions determine which holds fall, who rules Skyrim, and whether the Thalmor endgame is exposed or executed.
- **Thalmor Endgame:** The Aldmeri Dominion is manipulating both sides. Proof of this manipulation is a **major campaign flag**.
- **No Dragonborn:** Dragons may still emerge (optional), but the PCs are the heroes — no NPC will solve the war or Thalmor crisis for them.
- **Gritty Tone:** War has costs. Diplomacy, espionage, and moral compromise are as important as combat.

---

## Quick Start

1. Read `MASTER_KEY.md` for campaign premise, play pillars, and clock philosophy.
2. Read `INDEX.md` for a structured outline of all campaign elements.
3. Review `/modules/` for the Five Acts structure.
4. Check `/state/campaign_state.json` and `/clocks/skyrim_clocks.json` before each session.
5. Use `/hooks/` to pull story complications and faction entanglements into play.

---

## License & Attribution

This campaign uses **Fate Core** by Evil Hat Productions.  
Skyrim and The Elder Scrolls are trademarks of Bethesda Softworks LLC.  
This repository is a fan-made campaign framework for personal use.