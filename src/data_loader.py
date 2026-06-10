from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_cards() -> dict[str, dict]:
    cards = {}
    for path in sorted((DATA_DIR / "cards").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cards[data["id"]] = data
    return cards


def load_axes() -> dict:
    return json.loads((DATA_DIR / "axes.json").read_text(encoding="utf-8"))


def load_rules() -> dict:
    rules_path = DATA_DIR / "rules" / "2026-06.json"
    return json.loads(rules_path.read_text(encoding="utf-8"))


def load_issuers() -> list[dict]:
    data = json.loads((DATA_DIR / "issuers.json").read_text(encoding="utf-8"))
    return data["issuers"]


def cards_by_issuer(cards: dict[str, dict] | None = None) -> dict[str, list[str]]:
    cards = cards or load_cards()
    grouped: dict[str, list[str]] = {}
    for cid, card in cards.items():
        group = card.get("issuer_group", "other")
        grouped.setdefault(group, []).append(cid)
    for group in grouped:
        grouped[group].sort(key=lambda c: cards[c].get("tier_order", 99))
    return grouped
