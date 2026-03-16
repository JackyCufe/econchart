"""
图表配置面板组件。
根据图类型动态渲染对应参数配置 UI。
"""
from __future__ import annotations

import streamlit as st
import pandas as pd
from typing import Any, Optional

from core.theme import THEME_NAMES

# 图类型定义
CHART_TYPES = [
    "系数图",
    "散点图",
    "柱状图",
    "折线图",
    "箱线图",
    "热力图",
    "分布直方图",
]

CHART_ICONS = {
    "系数图": "📌",
    "散点图": "🔵",
    "柱状图": "📊",
    "折线图": "📈",
    "箱线图": "📦",
    "热力图": "🌡️",
    "分布直方图": "📉",
}


def render_chart_type_selector() -> str:
    """渲染图类型选择器，返回选中的图类型。"""
    st.markdown("### 📐 图表类型")
    options = [f"{CHART_ICONS.get(t, '')} {t}" for t in CHART_TYPES]
    idx = st.radio(
        "选择图类型",
        options=options,
        label_visibility="collapsed",
        key="chart_type_radio",
    )
    # 提取纯名称
    return idx.split(" ", 1)[-1] if " " in idx else idx


def render_theme_selector() -> str:
    """渲染期刊主题选择器，返回主题名称。"""
    st.markdown("### 🎨 期刊主题")
    return st.selectbox(
        "选择期刊格式",
        THEME_NAMES,
        key="theme_selector",
        label_visibility="collapsed",
    )


def _col_options(df: Optional[pd.DataFrame], numeric_only: bool = False) -> list[str]:
    """从 DataFrame 提取列名列表。"""
    if df is None:
        return []
    if numeric_only:
        return list(df.select_dtypes(include="number").columns)
    return list(df.columns)


def render_coef_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """系数图配置面板。"""
    st.markdown("#### 系数图参数")
    cols = _col_options(df)

    ci_type = st.selectbox(
        "置信区间类型",
        ["se (±1.96 SE)", "95ci (直接 CI 列)", "90ci (±1.645 SE)"],
        key="coef_ci_type",
    )
    ci_map = {"se (±1.96 SE)": "se", "95ci (直接 CI 列)": "95ci", "90ci (±1.645 SE)": "90ci"}

    title = st.text_input("图标题", value="回归系数图", key="coef_title")
    xlabel = st.text_input("X 轴标签", value="系数估计值", key="coef_xlabel")
    zero_line = st.checkbox("显示 x=0 参考线", value=True, key="coef_zeroline")
    sort_by = st.selectbox("排序方式", ["none", "coef_asc", "coef_desc"], key="coef_sort")

    exclude_input = st.text_input(
        "排除变量（逗号分隔，如 _cons）",
        value="",
        key="coef_exclude",
    )
    exclude_vars = [v.strip() for v in exclude_input.split(",") if v.strip()] or None

    return {
        "ci_type": ci_map.get(ci_type, "se"),
        "title": title,
        "xlabel": xlabel,
        "zero_line": zero_line,
        "sort_by": sort_by,
        "exclude_vars": exclude_vars,
    }


def render_scatter_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """散点图配置面板。"""
    st.markdown("#### 散点图参数")
    cols = _col_options(df)
    num_cols = _col_options(df, numeric_only=True)

    x_col = st.selectbox("X 轴列", cols, key="scatter_x")
    y_col = st.selectbox("Y 轴列", cols, key="scatter_y")
    color_col = st.selectbox("分组着色列（可选）", ["（无）"] + cols, key="scatter_color")
    size_col = st.selectbox("气泡大小列（可选）", ["（无）"] + num_cols, key="scatter_size")

    add_regression = st.checkbox("添加回归线", value=True, key="scatter_reg")
    add_confidence = st.checkbox("添加置信区间带", value=True, key="scatter_ci")
    title = st.text_input("图标题", value="", key="scatter_title")
    xlabel = st.text_input("X 轴标签", value="", key="scatter_xlabel")
    ylabel = st.text_input("Y 轴标签", value="", key="scatter_ylabel")

    return {
        "x_col": x_col,
        "y_col": y_col,
        "color_col": None if color_col == "（无）" else color_col,
        "size_col": None if size_col == "（无）" else size_col,
        "add_regression": add_regression,
        "add_confidence": add_confidence,
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
    }


def render_bar_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """柱状图配置面板。"""
    st.markdown("#### 柱状图参数")
    cols = _col_options(df)
    num_cols = _col_options(df, numeric_only=True)

    x_col = st.selectbox("X 轴（分类）列", cols, key="bar_x")
    y_cols = st.multiselect("Y 轴列（可多选）", num_cols, default=num_cols[:1], key="bar_y")
    stacked = st.checkbox("堆叠模式", value=False, key="bar_stacked")
    horizontal = st.checkbox("水平方向", value=False, key="bar_horizontal")
    error_col = st.selectbox("误差棒列（可选）", ["（无）"] + num_cols, key="bar_error")
    title = st.text_input("图标题", value="", key="bar_title")

    return {
        "x_col": x_col,
        "y_cols": y_cols or num_cols[:1],
        "stacked": stacked,
        "horizontal": horizontal,
        "error_col": None if error_col == "（无）" else error_col,
        "title": title,
    }


def render_line_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """折线图配置面板。"""
    st.markdown("#### 折线图参数")
    cols = _col_options(df)
    num_cols = _col_options(df, numeric_only=True)

    x_col = st.selectbox("X 轴列（时间/分类）", cols, key="line_x")
    y_cols = st.multiselect("Y 轴列（可多选）", num_cols, default=num_cols[:1], key="line_y")
    add_markers = st.checkbox("显示数据点标记", value=True, key="line_markers")
    add_ci = st.checkbox("显示置信区间带（近似）", value=False, key="line_ci")
    title = st.text_input("图标题", value="", key="line_title")
    ylabel = st.text_input("Y 轴标签", value="", key="line_ylabel")

    return {
        "x_col": x_col,
        "y_cols": y_cols or num_cols[:1],
        "add_markers": add_markers,
        "add_ci": add_ci,
        "title": title,
        "ylabel": ylabel,
    }


def render_boxplot_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """箱线图配置面板。"""
    st.markdown("#### 箱线图参数")
    cols = _col_options(df)
    num_cols = _col_options(df, numeric_only=True)

    y_cols = st.multiselect("数值列（可多选）", num_cols, default=num_cols[:1], key="box_y")
    group_col = st.selectbox("分组列（可选）", ["（无）"] + cols, key="box_group")
    show_outliers = st.checkbox("显示离群点", value=True, key="box_outliers")
    title = st.text_input("图标题", value="", key="box_title")
    ylabel = st.text_input("Y 轴标签", value="", key="box_ylabel")

    return {
        "y_cols": y_cols or num_cols[:1],
        "group_col": None if group_col == "（无）" else group_col,
        "show_outliers": show_outliers,
        "title": title,
        "ylabel": ylabel,
    }


def render_heatmap_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """热力图配置面板。"""
    st.markdown("#### 热力图参数")

    annotate = st.checkbox("显示数值", value=True, key="heat_annotate")
    fmt = st.selectbox("数值格式", [".2f", ".3f", ".0f", ".1f"], key="heat_fmt")
    title = st.text_input("图标题", value="", key="heat_title")

    return {"annotate": annotate, "fmt": fmt, "title": title}


def render_histogram_config(df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """分布直方图配置面板。"""
    st.markdown("#### 直方图参数")
    num_cols = _col_options(df, numeric_only=True)

    col = st.selectbox("数值列", num_cols, key="hist_col")
    bins = st.slider("分组数量（Bins）", 5, 100, 20, key="hist_bins")
    add_kde = st.checkbox("叠加 KDE 曲线", value=True, key="hist_kde")
    density = st.checkbox("Y 轴显示密度", value=False, key="hist_density")
    title = st.text_input("图标题", value="", key="hist_title")
    xlabel = st.text_input("X 轴标签", value="", key="hist_xlabel")

    return {
        "col": col,
        "bins": bins,
        "add_kde": add_kde,
        "density": density,
        "title": title,
        "xlabel": xlabel,
    }


CONFIG_RENDERERS = {
    "系数图": render_coef_config,
    "散点图": render_scatter_config,
    "柱状图": render_bar_config,
    "折线图": render_line_config,
    "箱线图": render_boxplot_config,
    "热力图": render_heatmap_config,
    "分布直方图": render_histogram_config,
}


def render_chart_config(chart_type: str, df: Optional[pd.DataFrame]) -> dict[str, Any]:
    """
    根据图类型渲染对应参数配置面板，返回配置字典。
    找不到对应渲染器时抛出 ValueError。
    """
    renderer = CONFIG_RENDERERS.get(chart_type)
    if renderer is None:
        raise ValueError(f"未知图类型：'{chart_type}'")
    return renderer(df)
