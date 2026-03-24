"""
数据输入组件。
支持粘贴 CSV 文本（Tab/逗号分隔）或上传 CSV/Excel 文件。
"""
from __future__ import annotations

import io
import logging
from typing import Optional

import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

COEF_SAMPLE = """variable,coef,se
GDP增长率,0.234,0.045
研发投入,0.187,0.032
人力资本,-0.056,0.028
对外开放度,0.312,0.067
政府支出,-0.143,0.051
_cons,0.892,0.123"""

SCATTER_SAMPLE = """x,y,group
1.2,2.3,A
2.1,3.5,A
3.4,4.2,B
4.5,5.1,B
5.2,6.3,A
6.1,7.8,B
7.3,8.4,A
8.2,9.1,B"""

SAMPLE_DATA: dict[str, str] = {
    "系数图": COEF_SAMPLE,
    "散点图": SCATTER_SAMPLE,
}

MAX_PREVIEW_ROWS = 20


def _parse_text(text: str) -> Optional[pd.DataFrame]:
    """
    尝试解析文本为 DataFrame。
    自动检测分隔符（Tab 或逗号）。
    """
    text = text.strip()
    if not text:
        return None

    sep = "\t" if "\t" in text else ","
    try:
        df = pd.read_csv(io.StringIO(text), sep=sep)
        if df.empty or df.shape[1] < 2:
            raise ValueError("解析结果列数不足，请检查数据格式")
        return df
    except Exception as exc:
        logger.warning("Failed to parse pasted text: %s", exc)
        raise ValueError(f"数据格式错误：{exc}") from exc


def _parse_file(file) -> Optional[pd.DataFrame]:
    """解析上传的 CSV 或 Excel 文件。"""
    name: str = file.name.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(file)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            raise ValueError(f"不支持的文件格式：{file.name}（请上传 CSV 或 Excel）")

        if df.empty:
            raise ValueError("文件内容为空")
        return df
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"文件解析失败：{exc}") from exc


def render_data_input(chart_type: str = "系数图") -> Optional[pd.DataFrame]:
    """
    渲染数据输入区域，返回解析后的 DataFrame（失败时返回 None）。

    包含：
    - 粘贴 CSV 文本框
    - 上传 CSV/Excel 文件
    - 示例数据按钮
    - 数据预览表格
    """
    st.markdown("### 📋 数据输入")
    st.caption("支持粘贴 CSV（逗号/Tab 分隔）或上传文件")
    if st.button("📂 加载示例数据", key="btn_sample", use_container_width=True):
        sample = SAMPLE_DATA.get(chart_type, COEF_SAMPLE)
        st.session_state["pasted_data"] = sample

    tab_paste, tab_upload = st.tabs(["📝 粘贴数据", "📁 上传文件"])

    df: Optional[pd.DataFrame] = None

    with tab_paste:
        default_text = st.session_state.get("pasted_data", "")
        text = st.text_area(
            "粘贴 CSV 数据",
            value=default_text,
            height=180,
            placeholder="粘贴数据（第一行为列名，逗号或 Tab 分隔）...",
            label_visibility="collapsed",
            key="text_area_paste",
        )
        if text.strip():
            try:
                df = _parse_text(text)
            except ValueError as exc:
                st.error(f"❌ {exc}")

    with tab_upload:
        uploaded = st.file_uploader(
            "上传文件",
            type=["csv", "xlsx", "xls"],
            label_visibility="collapsed",
            key="file_uploader",
        )
        if uploaded:
            try:
                df = _parse_file(uploaded)
                st.success(f"✅ 已加载：{uploaded.name}（{len(df)} 行 × {len(df.columns)} 列）")
            except ValueError as exc:
                st.error(f"❌ {exc}")

    if df is not None and not df.empty:
        preview = df.head(MAX_PREVIEW_ROWS)
        st.caption(f"数据预览（前 {len(preview)} 行 / 共 {len(df)} 行）")
        st.dataframe(preview, use_container_width=True)

    return df
