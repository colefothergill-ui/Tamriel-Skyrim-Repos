"""
build_context.py
Print a GM Context Pack to stdout (read-only).
Combines:
- state/campaign_state.json
- state/campaign_position.json (if present)
- clocks/skyrim_clocks.json
- most recent log file (if any)

Usage:
  python scripts/build_context.py
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOCKS = ROOT / "clocks" / "skyrim_clocks.json"
STATE = ROOT / "state" / "campaign_state.json"
POS = ROOT / "state" / "campaign_position.json"
LOGS_DIR = ROOT / "logs"

def load_json(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_latest_log() -> Path | None:
    if not LOGS_DIR.exists():
        return None
    candidates = []
    for p in LOGS_DIR.glob("*.md"):
        if p.name.lower().startswith("session_template"):
            continue
        candidates.append(p)
    if not candidates:
        return None
    return sorted(candidates, key=lambda x: x.name)[-1]

def main() -> None:
    clocks = load_json(CLOCKS)
    state = load_json(STATE)
    pos = load_json(POS) if POS.exists() else {}

    latest = find_latest_log()
    log_head = ""
    if latest:
        txt = latest.read_text(encoding="utf-8", errors="ignore")
        log_head = "\n".join(txt.splitlines()[:30])

    print("# GM Context Pack\n")
    print("## Position (fast pointer)")
    if pos:
        print(f"- Current Act: {pos.get('current_act','TODO')}")
        print(f"- Hold: {pos.get('current_hold','TODO')}")
        print(f"- Location: {pos.get('current_location','')}")
        print(f"- Focus factions: {pos.get('focus_factions',[])}")
        print(f"- Last log: {pos.get('last_log','')}")
    else:
        print("- TODO: Add state/campaign_position.json for faster recall.")

    print("\n## Party + Flags")
    print(f"- Alignment: {state.get('party',{}).get('alignment','TODO')}")
    print(f"- Allies: {state.get('party',{}).get('allies',[])}")
    print(f"- Enemies: {state.get('party',{}).get('enemies',[])}")
    print(f"- Flags: {state.get('major_flags',{})}")

    print("\n## Key Clocks (master)")
    for k, v in clocks.get("master_clocks", {}).items():
        print(f"- {k}: {v.get('current',0)}/{v.get('max',0)}")

    print("\n## Suggested next files to open")
    act = pos.get("current_act")
    if isinstance(act, int):
        print(f"- modules/acts/ACT_0{act}_... (TODO: ensure file exists and is filled)")
    else:
        print("- modules/acts/ACT_01_BATTLE_OF_WHITERUN.md (start here)")

    print("- story_branches/BRANCH_MATRIX.md")
    print("- story_branches/SECRET_TURNS.md")
    print("- hooks/HOOK_BANK.md")

    if log_head:
        print("\n## Latest Log (head)")
        print("```")
        print(log_head)
        print("```")

if __name__ == "__main__":
    main()
