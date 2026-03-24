"""
EconChart - 学术图表美化器（中国期刊专版）
单页交互式引导作图，支持撤销。
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from core.font_manager import setup_matplotlib_fonts

_ACTIVE_FONT = setup_matplotlib_fonts()

st.set_page_config(
    page_title="EconChart - 学术图表美化器",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _load_css() -> None:
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if not os.path.exists(css_path):
        return
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main() -> None:
    _load_css()
    from ui.pages.studio import render_studio
    render_studio()


if __name__ == "__main__":
    main()
