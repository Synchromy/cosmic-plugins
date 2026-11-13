"""Shared helpers for the adapters: read core/ and keep or drop per-assistant blocks in the skill."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r'<!-- only: (\w+) -->\n(.*?)<!-- end -->\n', re.S)


def copy() -> dict:
    return json.loads((ROOT / 'core' / 'copy.json').read_text())


def version() -> str:
    return (ROOT / 'VERSION').read_text().strip()


def skill_for(target: str) -> str:
    """The core skill with blocks for `target` kept (markers removed) and every other block dropped."""
    text = (ROOT / 'core' / 'skills' / 'cosmic' / 'SKILL.md').read_text()
    return BLOCK.sub(lambda m: m.group(2) if m.group(1) == target else '', text)
