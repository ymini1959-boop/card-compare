from __future__ import annotations

import streamlit as st

from src.data_loader import load_axes

AUTOMOTIVE_AXIS_IDS = [
    "car_insurance",
    "gasoline_rate",
]


def _valid_automotive_ids() -> set[str]:
    axes_data = load_axes()
    valid = {a["id"] for cat in axes_data["categories"] for a in cat["axes"]}
    return {ax for ax in AUTOMOTIVE_AXIS_IDS if ax in valid}


def _merge_automotive(axis_ids: list[str], valid: set[str]) -> list[str]:
    merged = list(axis_ids)
    for axis_id in AUTOMOTIVE_AXIS_IDS:
        if axis_id in valid and axis_id not in merged:
            merged.append(axis_id)
    return merged


def prepare_automotive_axis_defaults(
    default_axes: list[str],
    has_car: bool,
) -> list[str]:
    """軸ピッカー表示前に呼ぶ（session_state.axes_pick をここで更新）。"""
    if not has_car:
        st.session_state["_last_has_car"] = False
        return default_axes

    valid = _valid_automotive_ids()
    merged_defaults = _merge_automotive(default_axes, valid)

    if "axes_pick" in st.session_state:
        pick_merged = _merge_automotive(list(st.session_state.axes_pick), valid)
        if pick_merged != st.session_state.axes_pick:
            st.session_state.axes_pick = pick_merged
    else:
        st.session_state.axes_pick = merged_defaults

    if not st.session_state.get("_last_has_car", False):
        st.session_state["_show_automotive_hint"] = True
    st.session_state["_last_has_car"] = True
    return merged_defaults


def apply_automotive_axes(
    selected_axes: list[str],
    axis_defs: dict,
    has_car: bool,
) -> list[str]:
    """ピッカー表示後に比較用リストへ反映（session_state は触らない）。"""
    if not has_car:
        return selected_axes

    valid = set(axis_defs.keys())
    merged = _merge_automotive(selected_axes, valid)

    if st.session_state.pop("_show_automotive_hint", False):
        added = [
            axis_defs[ax]["label"]
            for ax in AUTOMOTIVE_AXIS_IDS
            if ax in merged and ax not in selected_axes
        ]
        if added:
            st.info(
                "🚗 自動車保有のため、比較軸に追加しました: "
                + "、".join(added)
            )
    return merged
