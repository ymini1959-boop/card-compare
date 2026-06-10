from src.calculator.ecosystem_scores import build_ecosystem_scores
from src.calculator.generic import calculate as generic_calculate
from src.models.comparison import CardResult
from src.models.profile import ResolvedProfile


def calculate(card: dict, profile: ResolvedProfile, rules: dict) -> CardResult:
    result = generic_calculate(card, profile, rules)
    result.ecosystem_scores = build_ecosystem_scores(card, profile)
    notes = list(result.notes)
    if card.get("jcb_ols_note"):
        notes.append(card["jcb_ols_note"])
    result.notes = notes
    return result
