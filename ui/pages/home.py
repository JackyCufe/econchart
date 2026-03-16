"""
EconChart 首页。
展示产品介绍、功能特性及快速入门引导。
"""
from __future__ import annotations

import streamlit as st


def render_home() -> None:
    """渲染首页内容。"""
    st.markdown(
        """
        <div style="text-align:center; padding: 2rem 0 1rem;">
            <h1 style="font-size:2.8rem; color:#2C3E50; margin-bottom:0.5rem;">
                📊 EconChart
            </h1>
            <p style="font-size:1.2rem; color:#666; margin:0;">
                学术图表美化器 · 中国期刊专版
            </p>
            <p style="color:#888; margin-top:0.5rem; font-size:0.95rem;">
                贴入数据 → 选图类型 → 选期刊格式 → 下载 300 DPI 图
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            #### 🎯 支持图类型
            - 📌 系数图（回归结果可视化）
            - 🔵 散点图（带回归线）
            - 📊 柱状图（分组/堆叠）
            - 📈 折线图（时间序列）
            - 📦 箱线图
            - 🌡️ 热力图（相关矩阵）
            - 📉 分布直方图
            """
        )

    with col2:
        st.markdown(
            """
            #### 📰 支持期刊格式
            - 经济研究（宋体 + Times New Roman）
            - 管理世界（黑体 + Arial）
            - 中国工业经济
            - 金融研究
            - 通用学术
            """
        )

    with col3:
        st.markdown(
            """
            #### ⚡ 核心特性
            - 自动检测中文字体
            - 三线表风格（无上/右边框）
            - 免费预览（96 DPI）
            - 高清导出（300 DPI）
            - 与 EconKit 无缝衔接
            """
        )

    st.divider()

    st.markdown("### 🚀 快速开始")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**① 粘贴数据**\n\n将 CSV 格式数据粘贴到输入框，或上传 CSV/Excel 文件。")
    with col_b:
        st.info("**② 选择图类型**\n\n选择适合论文的图表类型，如系数图或散点图。")
    with col_c:
        st.info("**③ 下载图片**\n\n免费获得预览图，升级后导出 300 DPI 无水印版本。")

    st.divider()

    st.markdown(
        """
        <div style="text-align:center; color:#999; font-size:0.85rem;">
            EconChart by <a href="https://econkit.com" style="color:#3498DB;">EconKit</a> ·
            专为中国经管学者设计
        </div>
        """,
        unsafe_allow_html=True,
    )
