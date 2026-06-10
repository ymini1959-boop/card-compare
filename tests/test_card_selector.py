import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.ui.card_selector import finalize_card_selection


def test_finalize_preserves_url_order_over_issuer_multiselect_order():
    """URL順 paypay → rakuten でも multiselect が発行会社順で返しても維持する。"""
    previous = ["paypay-gold", "rakuten-premium", "amex-gold"]
    # 発行会社ブロック順: 楽天 → Amex → PayPay の picks（options 順）
    picks_by_issuer = [
        ["rakuten-premium"],
        ["amex-gold"],
        ["paypay-gold"],
    ]
    assert finalize_card_selection(previous, picks_by_issuer) == [
        "paypay-gold",
        "rakuten-premium",
        "amex-gold",
    ]


def test_finalize_appends_new_card_at_end():
    previous = ["rakuten-premium"]
    picks_by_issuer = [
        ["rakuten-premium"],
        [],
        [],
        [],
        [],
        [],
        ["paypay-gold"],
        [],
        [],
        [],
    ]
    assert finalize_card_selection(previous, picks_by_issuer) == [
        "rakuten-premium",
        "paypay-gold",
    ]


def test_finalize_drops_deselected():
    previous = ["rakuten-premium", "paypay-gold", "amex-gold"]
    picks_by_issuer = [
        ["rakuten-premium"],
        [],
        ["paypay-gold"],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    assert finalize_card_selection(previous, picks_by_issuer) == [
        "rakuten-premium",
        "paypay-gold",
    ]


def test_finalize_preserves_click_order_within_issuer():
    """同一発行会社でプレミアム→ゴールドと選んでも tier_order に並べ替えない。"""
    previous = ["rakuten-premium"]
    # multiselect は tier_order で gold が先に返る
    picks_by_issuer = [["rakuten-gold", "rakuten-premium"]]
    assert finalize_card_selection(previous, picks_by_issuer) == [
        "rakuten-premium",
        "rakuten-gold",
    ]


def test_finalize_three_rakuten_cards_in_selection_order():
    previous = ["rakuten-gold", "rakuten-premium"]
    picks_by_issuer = [
        ["rakuten-gold", "rakuten-premium", "rakuten-black"],
    ]
    assert finalize_card_selection(previous, picks_by_issuer) == [
        "rakuten-gold",
        "rakuten-premium",
        "rakuten-black",
    ]


def test_finalize_respects_max_cards():
    previous = ["a", "b", "c", "d"]
    picks_by_issuer = [["a"], ["b"], ["c"], ["d"]]
    assert finalize_card_selection(previous, picks_by_issuer, max_cards=3) == [
        "a",
        "b",
        "c",
    ]
