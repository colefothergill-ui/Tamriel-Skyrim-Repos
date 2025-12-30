"""
dragonbreak_cue.py
Detects soft-cues before Dragonbreak moments.

Usage:
  python scripts/dragonbreak_cue.py

Behavior:
- Checks campaign state and clocks for Dragonbreak eligibility
- Suggests Dragonbreak moments when conditions are met
- Does not modify any repository files (read-only)
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
CLOCKS_FILE = ROOT / "clocks" / "skyrim_clocks.json"
STATE_FILE = ROOT / "state" / "campaign_state.json"

# Dragonbreak scene prefix flavor text
DRAGONBREAK_SCENE_PREFIX = """
╔═══════════════════════════════════════════════════════════════════╗
║                    🌀 DRAGONBREAK MOMENT 🌀                        ║
╚═══════════════════════════════════════════════════════════════════╝

Your vision blurs. For a heartbeat, you're both here and... not.
The wind whispers a name you've never heard—but mourn.

Time fractures. The world remembers what hasn't happened yet.

[This is a rare mythic thread opportunity. The choice is risky and tempting.]
"""


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {e}")
        sys.exit(1)


def check_clock_thresholds(clocks_data: Dict[str, Any]) -> List[str]:
    """Check if any clocks meet Dragonbreak threshold conditions."""
    triggers = []

    # Check master clocks
    master = clocks_data.get("master_clocks", {})
    for clock_name, clock_data in master.items():
        current = clock_data.get("current", 0)
        max_val = clock_data.get("max", 1)
        threshold = max_val * 0.5  # 50% or more

        if current >= threshold:
            triggers.append(f"Master clock '{clock_name}' at {current}/{max_val} (≥50%)")

    # Check act clocks
    act = clocks_data.get("act_clocks", {})
    for clock_name, clock_data in act.items():
        current = clock_data.get("current", 0)
        max_val = clock_data.get("max", 1)
        threshold = max_val * 0.5  # 50% or more

        if current >= threshold:
            triggers.append(f"Act clock '{clock_name}' at {current}/{max_val} (≥50%)")

    # Check faction clocks
    faction = clocks_data.get("faction_clocks", {})
    for clock_name, clock_data in faction.items():
        current = clock_data.get("current", 0)
        max_val = clock_data.get("max", 1)

        # Check if 1 tick from milestone
        if current >= max_val - 1:
            triggers.append(f"Faction clock '{clock_name}' at {current}/{max_val} (1 tick from complete)")

    return triggers


def check_location(state_data: Dict[str, Any]) -> List[str]:
    """Check if current location is mythic/ancient."""
    triggers = []

    # Mythic location keywords
    mythic_keywords = [
        "ruin", "ruins", "barrow", "dwemer", "dwarven", "shrine",
        "ancient", "forgotten", "hidden", "cursed", "forbidden",
        "temple", "sanctuary", "crypt", "tomb"
    ]

    current_location = state_data.get("current_location", "").lower()

    for keyword in mythic_keywords:
        if keyword in current_location:
            triggers.append(f"Current location '{current_location}' is mythic/ancient (keyword: {keyword})")
            break

    return triggers


def main() -> None:
    print("=" * 70)
    print("Dragonbreak Cue Detector")
    print("=" * 70)
    print()

    # Load data files
    clocks_data = load_json_file(CLOCKS_FILE)
    state_data = load_json_file(STATE_FILE)

    # Check for Dragonbreak conditions
    all_triggers = []

    print("Checking clock thresholds...")
    clock_triggers = check_clock_thresholds(clocks_data)
    all_triggers.extend(clock_triggers)

    print("Checking location context...")
    location_triggers = check_location(state_data)
    all_triggers.extend(location_triggers)

    print()
    print("=" * 70)

    if all_triggers:
        print("🌀 DRAGONBREAK MOMENT ELIGIBLE 🌀")
        print()
        print("Conditions met:")
        for trigger in all_triggers:
            print(f"  • {trigger}")
        print()
        print("Recommendation: Offer a Dragonbreak moment at the next decision point.")
        print()
        print("Scene prefix to use:")
        print(DRAGONBREAK_SCENE_PREFIX)
    else:
        print("No Dragonbreak conditions met at this time.")
        print()
        print("Dragonbreak moments should only appear when:")
        print("  • A major/act clock is at 50% or more")
        print("  • A faction clock is 1 tick from complete")
        print("  • The location is ancient/mythic/hidden")

    print("=" * 70)


if __name__ == "__main__":
    main()
