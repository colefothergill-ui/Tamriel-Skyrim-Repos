"""
custom_scan.py
Scan repository for banned terms and validate campaign state.

Usage:
  python scripts/custom_scan.py

Checks:
- Scans markdown files and JSON files for banned WoW/BFA terms
- Identifies references to removed PC "Suroe Dragonseal"
- Updates state/campaign_state.json to mark validation complete
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN_STATE_PATH = ROOT / "state" / "campaign_state.json"

# Banned terms that should not appear in the campaign vault
BANNED_TERMS = [
    "WoW",
    "World of Warcraft",
    "BFA",
    "Battle for Azeroth",
    "Azeroth",
    "Suroe Dragonseal",
    "Suroe",
    "sin'dorei",
    "Kaldorei",
    "blood elf",
    "night elf",
    "Dracon'Thor'reth",
]

# File patterns to scan
SCAN_PATTERNS = [
    "**/*.md",
    "**/*.json",
]

# Directories to exclude from scanning
EXCLUDE_DIRS = [
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
]


def should_scan_file(file_path: Path) -> bool:
    """Return True if the file should be scanned for banned terms."""
    # Skip files in excluded directories
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in file_path.parts:
            return False
    
    # Skip the copilot-instructions.md as it's allowed to reference banned terms
    if file_path.name == "copilot-instructions.md":
        return False
    
    # Skip this script itself
    if file_path.name == "custom_scan.py":
        return False
    
    return True


def scan_file_for_banned_terms(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Scan a file for banned terms.
    Returns list of (line_number, term, line_content) tuples.
    """
    violations = []
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                for term in BANNED_TERMS:
                    if term.lower() in line.lower():
                        violations.append((line_num, term, line.strip()))
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        pass
    
    return violations


def scan_repository() -> List[Tuple[Path, int, str, str]]:
    """
    Scan the repository for banned terms.
    Returns list of (file_path, line_number, term, line_content) tuples.
    """
    all_violations = []
    
    for pattern in SCAN_PATTERNS:
        for file_path in ROOT.glob(pattern):
            if not file_path.is_file():
                continue
            
            if not should_scan_file(file_path):
                continue
            
            violations = scan_file_for_banned_terms(file_path)
            for line_num, term, line_content in violations:
                relative_path = file_path.relative_to(ROOT)
                all_violations.append((relative_path, line_num, term, line_content))
    
    return all_violations


def update_campaign_state() -> None:
    """Update campaign_state.json to mark validation as complete."""
    try:
        # Ensure the state directory exists
        CAMPAIGN_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing state or create new
        if CAMPAIGN_STATE_PATH.exists():
            with CAMPAIGN_STATE_PATH.open("r", encoding="utf-8") as f:
                state = json.load(f)
        else:
            state = {}
        
        # Update the campaign_state to true
        state["campaign_state"] = True
        
        # Write back to file
        with CAMPAIGN_STATE_PATH.open("w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        
        print(f"✓ Updated {CAMPAIGN_STATE_PATH.relative_to(ROOT)} - campaign_state: true")
    except Exception as e:
        print(f"ERROR: Failed to update campaign_state.json: {e}")
        sys.exit(1)


def main():
    print("=" * 70)
    print("Campaign Vault Custom Scan")
    print("=" * 70)
    print()
    
    print("Scanning for banned terms...")
    violations = scan_repository()
    
    if violations:
        print(f"\n⚠ FOUND {len(violations)} VIOLATIONS:\n")
        
        # Group violations by file
        violations_by_file = {}
        for file_path, line_num, term, line_content in violations:
            if file_path not in violations_by_file:
                violations_by_file[file_path] = []
            violations_by_file[file_path].append((line_num, term, line_content))
        
        # Print violations organized by file
        for file_path in sorted(violations_by_file.keys()):
            print(f"\n{file_path}:")
            for line_num, term, line_content in violations_by_file[file_path]:
                print(f"  Line {line_num}: Found '{term}'")
                # Show first 80 chars of the line
                preview = line_content[:80] + "..." if len(line_content) > 80 else line_content
                print(f"    {preview}")
        
        print("\n" + "=" * 70)
        print("VALIDATION FAILED: Banned terms found in repository")
        print("=" * 70)
        sys.exit(1)
    else:
        print("✓ No banned terms found")
    
    print()
    update_campaign_state()
    
    print()
    print("=" * 70)
    print("✓ VALIDATION PASSED: Repository is clean")
    print("=" * 70)


if __name__ == "__main__":
    main()
