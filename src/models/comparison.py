from dataclasses import dataclass, field
from typing import Any


@dataclass
class CardResult:
    card_id: str
    card_name: str
    effective_rate: float
    effective_annual_fee: int
    annual_bonus_points: int
    annual_bonus_yen: int
    total_points_value: int
    ecosystem_scores: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    static_values: dict[str, Any] = field(default_factory=dict)
    supermarket_rate: float = 0.0
    convenience_rate: float = 0.0
    daily_effective_rate: float = 0.0
    car_insurance_score: int = 0
    car_insurance_summary: str = "なし"


@dataclass
class ComparisonRow:
    axis_id: str
    axis_label: str
    values: dict[str, str]
    is_computed: bool = False
