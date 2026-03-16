"""
图表编辑器页面（主功能页）。
布局：左侧 1/3 配置区 + 右侧 2/3 预览区。
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from core.exporter import export_figure, get_mime_type
from core.theme import get_theme, THEME_NAMES
from ui.components.data_input import render_data_input
from ui.components.chart_config import (
    render_chart_type_selector,
    render_theme_selector,
    render_chart_config,
    CHART_TYPES,
)

logger = logging.getLogger(__name__)


def _build_chart(chart_type: str, df: pd.DataFrame, config: dict, theme_name: str):
    """根据图类型和配置构建 matplotlib Figure。"""
    theme = get_theme(theme_name)

    if chart_type == "系数图":
        from charts.coefficient_plot import plot_coefficients
        return plot_coefficients(data=df, theme=theme, **config)

    if chart_type == "散点图":
        from charts.scatter import plot_scatter
        return plot_scatter(data=df, theme=theme, **config)

    if chart_type == "柱状图":
        from charts.bar import plot_bar
        return plot_bar(data=df, theme=theme, **config)

    if chart_type == "折线图":
        from charts.line import plot_line
        return plot_line(data=df, theme=theme, **config)

    if chart_type == "箱线图":
        from charts.boxplot import plot_boxplot
        return plot_boxplot(data=df, theme=theme, **config)

    if chart_type == "热力图":
        from charts.heatmap import plot_heatmap
        return plot_heatmap(data=df, theme=theme, **config)

    if chart_type == "分布直方图":
        from charts.histogram import plot_histogram
        return plot_histogram(data=df, theme=theme, **config)

    raise ValueError(f"不支持的图类型：'{chart_type}'")


def _render_export_panel(fig: plt.Figure) -> None:
    """渲染导出操作面板。"""
    st.markdown("### 💾 导出图表")

    col_fmt, col_dpi = st.columns(2)
    with col_fmt:
        fmt = st.selectbox("格式", ["png", "svg", "pdf"], key="export_fmt")
    with col_dpi:
        dpi_option = st.selectbox(
            "分辨率",
            ["96 DPI（免费）", "150 DPI（免费）", "300 DPI（🔒 付费）"],
            key="export_dpi",
        )

    dpi_map = {"96 DPI（免费）": 96, "150 DPI（免费）": 150, "300 DPI（🔒 付费）": 300}
    dpi = dpi_map[dpi_option]
    is_paid = dpi == 300

    watermark = True  # 免费版始终带水印（未来根据登录状态判断）

    if is_paid:
        st.warning("🔒 300 DPI 无水印版本为付费功能，即将上线。当前仍可下载 150 DPI 版本。")
        dpi = 150  # 降级处理

    try:
        data = export_figure(fig, fmt=fmt, dpi=dpi, watermark=watermark)
        mime = get_mime_type(fmt)
        filename = f"econchart_export.{fmt}"

        st.download_button(
            label=f"⬇️ 下载 {fmt.upper()} ({dpi} DPI)",
            data=data,
            file_name=filename,
            mime=mime,
            use_container_width=True,
            key="download_btn",
        )
    except Exception as exc:
        st.error(f"导出失败：{exc}")


def render_editor() -> None:
    """渲染图表编辑器主页面。"""
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        # ① 图类型选择
        chart_type = render_chart_type_selector()

        st.divider()

        # ② 数据输入
        df = render_data_input(chart_type=chart_type)

        st.divider()

        # ③ 期刊主题选择
        theme_name = render_theme_selector()

        st.divider()

        # ④ 图表参数配置
        st.markdown("### ⚙️ 图表参数")
        if df is not None and not df.empty:
            try:
                config = render_chart_config(chart_type, df)
            except Exception as exc:
                st.error(f"配置面板错误：{exc}")
                config = {}
        else:
            render_chart_config(chart_type, None)
            config = None

    with col_right:
        st.markdown("### 👁️ 实时预览")

        if df is None or df.empty:
            st.info("⬅️ 请在左侧粘贴数据或上传文件，图表将在此实时预览。")
            return

        if config is None:
            st.warning("数据加载中...")
            return

        with st.spinner("绘制中..."):
            try:
                fig = _build_chart(chart_type, df, config, theme_name)
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                # 重新生成用于导出（避免 close 后无法使用）
                fig_export = _build_chart(chart_type, df, config, theme_name)
                st.divider()
                _render_export_panel(fig_export)
                plt.close(fig_export)

            except ValueError as exc:
                st.error(f"❌ 图表绘制失败：{exc}")
            except Exception as exc:
                logger.exception("Unexpected error during chart rendering")
                st.error(f"❌ 意外错误：{exc}")
