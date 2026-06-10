from __future__ import annotations

import streamlit as st

from src.data_loader import load_axes
from src.models.profile import PRIORITY_OPTIONS


def _all_axis_defs(axes_data: dict) -> dict[str, dict]:
    defs = {}
    for cat in axes_data["categories"]:
        for axis in cat["axes"]:
            defs[axis["id"]] = {
                **axis,
                "category": cat["label"],
                "category_id": cat["id"],
            }
    return defs


def _ordered_axis_ids(axes_data: dict) -> list[str]:
    return [a["id"] for cat in axes_data["categories"] for a in cat["axes"]]


def render_axis_picker(
    default_axes: list[str] | None = None,
    preset_key: str | None = None,
) -> tuple[list[str], dict]:
    axes_data = load_axes()
    axis_defs = _all_axis_defs(axes_data)
    presets = axes_data["presets"]
    all_axis_ids = _ordered_axis_ids(axes_data)

    st.caption("タップで比較軸を一括選択")
    priority_keys = list(PRIORITY_OPTIONS.keys()) + ["daily", "car", "all"]
    cols_per_row = 2
    for row_start in range(0, len(priority_keys), cols_per_row):
        row_keys = priority_keys[row_start : row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, key in zip(cols, row_keys):
            label = {
                "daily": "日常買い物",
                "car": "自動車",
                "all": "すべて",
            }.get(key, PRIORITY_OPTIONS.get(key, key))
            if col.button(label, key=f"preset_{key}", use_container_width=True):
                st.session_state["axis_preset"] = key

    if "axis_preset" in st.session_state:
        preset_key = st.session_state["axis_preset"]

    if preset_key and preset_key in presets:
        default_selected = [a for a in presets[preset_key] if a in axis_defs]
    elif default_axes:
        default_selected = [a for a in default_axes if a in axis_defs]
    else:
        default_selected = [a for a in presets["reward"] if a in axis_defs]

    if "axes_pick" not in st.session_state:
        st.session_state.axes_pick = [a for a in default_selected if a in all_axis_ids]

    applied = st.session_state.get("_axes_preset_applied")
    if preset_key and preset_key != applied:
        st.session_state.axes_pick = [a for a in default_selected if a in all_axis_ids]
        st.session_state._axes_preset_applied = preset_key

    selected_ids = st.multiselect(
        "比較する項目",
        options=all_axis_ids,
        format_func=lambda aid: axis_defs[aid]["label"],
        key="axes_pick",
    )

    if not selected_ids:
        st.warning("比較軸を1つ以上選択してください。")
        selected_ids = default_selected

    st.markdown(
        f'<p style="font-size:0.75rem;color:#64748b;margin:0.5rem 0 0;">'
        f'選択中 <strong style="color:#1a4d7c;">{len(selected_ids)}</strong> 項目</p>',
        unsafe_allow_html=True,
    )
    return selected_ids, axis_defs
