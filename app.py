"""
EconChart - 学术图表美化器（中国期刊专版）
入口文件，负责页面配置、字体初始化和路由。
"""
from __future__ import annotations

import os
import sys

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.font_manager import setup_matplotlib_fonts

# 初始化字体（全局，仅执行一次）
_ACTIVE_FONT = setup_matplotlib_fonts()

st.set_page_config(
    page_title="EconChart - 学术图表美化器",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _load_css() -> None:
    """加载自定义样式。"""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if not os.path.exists(css_path):
        return
    with open(css_path, encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def _render_nav() -> str:
    """渲染顶部导航，返回当前选中页面名称。"""
    col_logo, col_nav = st.columns([1, 3])
    with col_logo:
        st.markdown(
            "<span style='font-size:1.4rem; font-weight:700; color:#2C3E50;'>"
            "📊 EconChart</span>",
            unsafe_allow_html=True,
        )
    with col_nav:
        page = st.radio(
            "nav",
            ["🏠 首页", "📐 图表编辑器"],
            horizontal=True,
            label_visibility="collapsed",
            key="main_nav",
        )
    st.divider()
    return page


def main() -> None:
    """应用入口。"""
    _load_css()
    page = _render_nav()

    if page == "🏠 首页":
        from ui.pages.home import render_home
        render_home()
    elif page == "📐 图表编辑器":
        from ui.pages.editor import render_editor
        render_editor()
    else:
        st.error(f"未知页面：{page}")

    # 底部状态信息（调试用，生产可移除）
    if st.session_state.get("show_debug"):
        st.caption(f"字体：{_ACTIVE_FONT}")


if __name__ == "__main__":
    main()
