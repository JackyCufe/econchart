"""
EconChart Studio — 单页引导式作图
流程：数据输入 → 图类型 → 参数配置 + 预览 → 导出
支持撤销（最多10步）
"""
from __future__ import annotations

import logging
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from core.exporter import export_figure, get_mime_type
from core.theme import get_theme, THEME_NAMES

logger = logging.getLogger(__name__)

CHART_TYPES = [
    {"name": "系数图",     "icon": "📊", "desc": "回归系数可视化，带置信区间"},
    {"name": "散点图",     "icon": "⚬",  "desc": "变量关系探索"},
    {"name": "柱状图",     "icon": "▊",  "desc": "分类对比"},
    {"name": "折线图",     "icon": "📈", "desc": "趋势变化"},
    {"name": "箱线图",     "icon": "▭",  "desc": "分布与离群值"},
    {"name": "热力图",     "icon": "🌡️", "desc": "相关矩阵"},
    {"name": "分布直方图", "icon": "▟",  "desc": "频率分布"},
]
CHART_NAMES = [c["name"] for c in CHART_TYPES]

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
6.1,7.8,B"""

SAMPLE_DATA = {"系数图": COEF_SAMPLE, "散点图": SCATTER_SAMPLE}


# ── Session helpers ────────────────────────────────────────────────────────────

def _init_state():
    st.session_state.setdefault("ec_df", None)
    st.session_state.setdefault("ec_chart", "系数图")
    st.session_state.setdefault("ec_history", [])
    st.session_state.setdefault("ec_pasted", "")
    st.session_state.setdefault("ec_upload_key", "")


def _push_history(df, chart):
    h = st.session_state["ec_history"]
    h.append({"df": df.copy() if df is not None else None, "chart": chart})
    if len(h) > 10:
        h.pop(0)


def _undo():
    h = st.session_state["ec_history"]
    if not h:
        return
    prev = h.pop()
    st.session_state["ec_df"] = prev["df"]
    st.session_state["ec_chart"] = prev["chart"]


# ── 数据解析 ───────────────────────────────────────────────────────────────────

def _parse_csv_text(text: str) -> pd.DataFrame:
    import io
    text = text.strip()
    sep = "\t" if "\t" in text else ","
    df = pd.read_csv(io.StringIO(text), sep=sep)
    if df.empty or df.shape[1] < 2:
        raise ValueError("列数不足，请检查格式（第一行应为列名，逗号/Tab分隔）")
    return df


def _parse_upload(file) -> pd.DataFrame:
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith((".xlsx", ".xls")):
        return pd.read_excel(file, engine="openpyxl")
    raise ValueError(f"不支持的格式：{file.name}，请上传 CSV 或 Excel")


# ── 图表构建 ───────────────────────────────────────────────────────────────────

def _build_chart(chart_type: str, df: pd.DataFrame, config: dict, theme_name: str):
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
    raise ValueError(f"不支持的图类型：{chart_type}")


# ── 主页面 ─────────────────────────────────────────────────────────────────────

def render_studio():
    _init_state()

    st.markdown(
        "<h2 style='margin-bottom:0'>📊 EconChart</h2>"
        "<p style='color:#888;margin-top:4px'>学术图表美化器 · 中国经管期刊专版</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Step 1: 数据输入 ───────────────────────────────────────────────────────
    # 注意：df 在此处动态读取，不在顶部固定，确保上传后立即生效
    def get_df():
        return st.session_state["ec_df"]

    def get_chart():
        return st.session_state["ec_chart"]

    # ── 数据输入用 fragment 包裹：输入时只刷新此区域，不触发全页 reflow ─────
    # @st.fragment  # disabled: requires streamlit>=1.37
    def _data_input_fragment():
        with st.expander("① 数据输入", expanded=(get_df() is None)):
            tab_paste, tab_upload = st.tabs(["📝 粘贴 CSV", "📁 上传文件"])

            with tab_paste:
                sample_cols = st.columns(len([k for k in SAMPLE_DATA]))
                sample_items = list(SAMPLE_DATA.items())
                for i, (name, sample) in enumerate(sample_items):
                    if sample_cols[i].button(f"📋 示例·{name}", key=f"sample_{name}", use_container_width=True):
                        try:
                            new_df = _parse_csv_text(sample)
                            _push_history(get_df(), get_chart())
                            st.session_state["paste_area"] = sample
                            st.session_state["ec_pasted"] = sample
                            st.session_state["ec_chart"] = name
                            st.session_state["ec_df"] = new_df
                            st.rerun()  # was scope="app"
                        except Exception as e:
                            st.error(f"❌ 示例加载失败：{e}")

                text = st.text_area(
                    "粘贴数据",
                    height=160,
                    placeholder="第一行为列名，逗号或 Tab 分隔...",
                    label_visibility="collapsed",
                    key="paste_area",
                )
                if st.button("✅ 确认加载", key="btn_confirm_paste", type="primary", use_container_width=True):
                    if text.strip():
                        try:
                            new_df = _parse_csv_text(text)
                            _push_history(get_df(), get_chart())
                            st.session_state["ec_df"] = new_df
                            st.session_state["ec_pasted"] = text
                            st.rerun()  # was scope="app"
                        except Exception as e:
                            st.error(f"❌ {e}")
                    else:
                        st.warning("请先粘贴数据")

            # ── 上传文件 ──────────────────────────────────────────────────────
            with tab_upload:
                uploaded = st.file_uploader(
                    "上传 CSV / Excel",
                    type=["csv", "xlsx", "xls"],
                    label_visibility="collapsed",
                    key="file_upload",
                )
                if uploaded is not None:
                    file_key = f"{uploaded.name}_{uploaded.size}"
                    if st.session_state["ec_upload_key"] != file_key:
                        try:
                            new_df = _parse_upload(uploaded)
                            _push_history(get_df(), get_chart())
                            st.session_state["ec_df"] = new_df
                            st.session_state["ec_upload_key"] = file_key
                            st.success(f"✅ 已加载 {len(new_df):,} 行 × {len(new_df.columns)} 列")
                            st.dataframe(new_df.head(5), use_container_width=True)
                            st.rerun()  # was scope="app"
                        except Exception as e:
                            st.error(f"❌ 解析失败：{e}")
                    else:
                        df_loaded = get_df()
                        if df_loaded is not None:
                            st.success(f"✅ 已加载 {len(df_loaded):,} 行 × {len(df_loaded.columns)} 列")
                            st.dataframe(df_loaded.head(5), use_container_width=True)

            current_df = get_df()
            if current_df is not None:
                st.info(f"📊 当前数据：{len(current_df):,} 行 × {len(current_df.columns)} 列 — {', '.join(current_df.columns[:5])}{'...' if len(current_df.columns) > 5 else ''}")

    _data_input_fragment()

    # ── 数据未加载时提示 ───────────────────────────────────────────────────────
    df = get_df()
    if df is None:
        st.info("⬆️ 请在「① 数据输入」中粘贴或上传数据，或点击「📋 示例·系数图」一键加载")
        return

    chart_type = get_chart()

    # ── Step 2: 图类型选择（平铺按钮，不用 expander 避免展开/折叠高度跳变）────
    st.markdown("#### ② 选择图表类型")
    cols = st.columns(len(CHART_TYPES))
    for i, ct in enumerate(CHART_TYPES):
        is_active = chart_type == ct["name"]
        label = f"{'✅ ' if is_active else ''}{ct['icon']} {ct['name']}"
        btn_type = "primary" if is_active else "secondary"
        if cols[i].button(label, key=f"chart_{i}", use_container_width=True, type=btn_type):
            st.session_state["ec_chart"] = ct["name"]
            chart_type = ct["name"]
            st.rerun()
    st.caption(next((c["desc"] for c in CHART_TYPES if c["name"] == chart_type), ""))

    # ── Step 3: 配置 + 预览 ────────────────────────────────────────────────────
    st.markdown("#### ③ 配置与预览")
    col_cfg, col_preview = st.columns([2, 3], gap="large")

    with col_cfg:
        theme_name = st.selectbox("期刊主题", THEME_NAMES, key="theme_sel")

        # 当前图类型所需数据格式提示
        FORMAT_HINTS = {
            "系数图": ("必须包含列：`variable`（变量名）、`coef`（系数）、`se`（标准误）",
                       "variable,coef,se\nGDP增长率,0.234,0.045\n研发投入,0.187,0.032"),
            "散点图": ("必须包含列：数值型 X 列、数值型 Y 列（可选分组列）",
                       "x,y,group\n1.2,2.3,A\n2.1,3.5,B"),
            "柱状图": ("必须包含列：分类列（X）+ 数值列（Y，可多列）",
                       "region,gdp,income\n东部,5.2,3.1\n西部,3.8,2.4"),
            "折线图": ("必须包含列：时间/序号列（X）+ 数值列（Y，可多列）",
                       "year,gdp,cpi\n2018,6.7,2.1\n2019,6.1,2.9"),
            "箱线图": ("必须包含列：数值列（可多列）+ 可选分组列",
                       "score,group\n85,A\n90,B\n78,A"),
            "热力图": ("必须为纯数值列（相关矩阵）",
                       "gdp,income,edu\n1.0,0.8,0.6\n0.8,1.0,0.7"),
            "分布直方图": ("必须包含数值列",
                           "value\n1.2\n2.3\n3.1"),
        }
        hint_text, hint_example = FORMAT_HINTS.get(chart_type, ("", ""))
        with st.expander("📌 数据格式要求", expanded=False):
            st.caption(hint_text)
            st.code(hint_example, language="csv")

        st.markdown("---")
        from ui.components.chart_config import render_chart_config
        try:
            config = render_chart_config(chart_type, df)
        except Exception as e:
            st.error(f"配置加载错误：{e}")
            config = {}

    with col_preview:
        preview_slot = st.empty()
        with st.spinner("绘制中..."):
            try:
                fig = _build_chart(chart_type, df, config, theme_name)
                with preview_slot.container():
                    st.pyplot(fig, use_container_width=True)
                plt.close(fig)

                # 导出区
                st.markdown("---")
                c1, c2 = st.columns(2)
                fmt = c1.selectbox("格式", ["png", "svg", "pdf"], key="exp_fmt")
                dpi_label = c2.selectbox(
                    "分辨率",
                    ["96 DPI（预览）", "150 DPI（免费）", "300 DPI（🔒 付费）"],
                    key="exp_dpi",
                )
                dpi = {"96 DPI（预览）": 96, "150 DPI（免费）": 150, "300 DPI（🔒 付费）": 150}[dpi_label]

                fig_exp = _build_chart(chart_type, df, config, theme_name)
                data = export_figure(fig_exp, fmt=fmt, dpi=dpi, watermark=True)
                plt.close(fig_exp)

                st.download_button(
                    f"⬇️ 下载 {fmt.upper()} ({dpi} DPI)",
                    data=data,
                    file_name=f"econchart.{fmt}",
                    mime=get_mime_type(fmt),
                    use_container_width=True,
                )
            except ValueError as e:
                _, hint_example = FORMAT_HINTS.get(chart_type, ("", ""))
                st.warning(f"⚠️ {e}")
                st.info(f"💡 请检查左侧「数据格式要求」，确认列名与要求一致。\n\n**{chart_type}示例数据：**")
                st.code(hint_example, language="csv")
            except Exception as e:
                logger.exception("Chart render error")
                st.error(f"❌ 绘制失败：{e}")

    # ── 撤销 ──────────────────────────────────────────────────────────────────
    if st.session_state["ec_history"]:
        st.divider()
        if st.button("↩️ 撤销上一步", key="btn_undo"):
            _undo()
            st.rerun()
