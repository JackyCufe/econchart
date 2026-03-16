"""
期刊主题定义模块。
每个主题包含：字体、字号、颜色方案、尺寸、DPI 配置。
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JournalTheme:
    name: str
    font_body: str           # 正文字体（中文）
    font_en: str             # 英文字体
    font_size_title: float
    font_size_label: float
    font_size_tick: float
    font_size_legend: float
    dpi_preview: int         # 预览 DPI（免费）
    dpi_export: int          # 导出 DPI（付费功能）
    colors: list[str]        # 颜色方案（有序列表）
    fig_width: float         # 英寸
    fig_height: float        # 英寸
    spine_top: bool          # 是否显示顶部边框（三线表风格）
    spine_right: bool        # 是否显示右侧边框


THEMES: dict[str, JournalTheme] = {
    "经济研究": JournalTheme(
        name="经济研究",
        font_body="SimSun",
        font_en="Times New Roman",
        font_size_title=12,
        font_size_label=10,
        font_size_tick=9,
        font_size_legend=9,
        dpi_preview=96,
        dpi_export=300,
        colors=["#2C3E50", "#E74C3C", "#3498DB", "#27AE60", "#F39C12"],
        fig_width=6.5,
        fig_height=4.5,
        spine_top=False,
        spine_right=False,
    ),
    "管理世界": JournalTheme(
        name="管理世界",
        font_body="SimHei",
        font_en="Arial",
        font_size_title=13,
        font_size_label=11,
        font_size_tick=10,
        font_size_legend=10,
        dpi_preview=96,
        dpi_export=300,
        colors=["#1A237E", "#D32F2F", "#1976D2", "#388E3C", "#F57C00"],
        fig_width=7.0,
        fig_height=5.0,
        spine_top=False,
        spine_right=False,
    ),
    "中国工业经济": JournalTheme(
        name="中国工业经济",
        font_body="SimSun",
        font_en="Times New Roman",
        font_size_title=12,
        font_size_label=10,
        font_size_tick=9,
        font_size_legend=9,
        dpi_preview=96,
        dpi_export=300,
        colors=["#37474F", "#B71C1C", "#0288D1", "#2E7D32", "#E65100"],
        fig_width=6.5,
        fig_height=4.5,
        spine_top=False,
        spine_right=False,
    ),
    "金融研究": JournalTheme(
        name="金融研究",
        font_body="SimSun",
        font_en="Times New Roman",
        font_size_title=12,
        font_size_label=10,
        font_size_tick=9,
        font_size_legend=9,
        dpi_preview=96,
        dpi_export=300,
        colors=["#004D40", "#BF360C", "#01579B", "#1B5E20", "#E65100"],
        fig_width=6.5,
        fig_height=4.5,
        spine_top=False,
        spine_right=False,
    ),
    "通用学术": JournalTheme(
        name="通用学术",
        font_body="SimHei",
        font_en="DejaVu Sans",
        font_size_title=12,
        font_size_label=10,
        font_size_tick=9,
        font_size_legend=9,
        dpi_preview=96,
        dpi_export=300,
        colors=["#2C3E50", "#E74C3C", "#3498DB", "#27AE60", "#F39C12",
                "#8E44AD", "#16A085"],
        fig_width=7.0,
        fig_height=5.0,
        spine_top=False,
        spine_right=False,
    ),
}

THEME_NAMES: list[str] = list(THEMES.keys())


def get_theme(name: str) -> JournalTheme:
    """
    获取指定名称的期刊主题。
    找不到时抛出 ValueError（快速失败）。
    """
    if name not in THEMES:
        raise ValueError(
            f"Unknown theme: '{name}'. Available: {THEME_NAMES}"
        )
    return THEMES[name]
