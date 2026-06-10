from __future__ import annotations

import streamlit as st

# 自動車保有時に自動追加する比較軸
AUTOMOTIVE_AXIS_IDS = [
    "car_insurance",
    "gasoline_rate",
]


def merge_automotive_axes(
    selected_axes: list[str],
    axis_defs: dict,
    has_car: bool,
) -> list[str]:
    if not has_car:
        return selected_axes

    merged = list(selected_axes)
    added_labels: list[str] = []
    for axis_id in AUTOMOTIVE_AXIS_IDS:
        if axis_id in axis_defs and axis_id not in merged:
            merged.append(axis_id)
            added_labels.append(axis_defs[axis_id]["label"])

    if added_labels and merged != selected_axes:
        st.session_state.axes_pick = merged
        st.info(
            "🚗 自動車保有のため、比較軸に追加しました: "
            + "、".join(added_labels)
        )
    return merged
