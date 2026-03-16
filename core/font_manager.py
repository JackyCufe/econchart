"""
自动检测系统可用中文字体，按优先级注册到 matplotlib。
支持 macOS / Linux(Docker) / Windows。
"""
from __future__ import annotations

import logging
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

logger = logging.getLogger(__name__)

FONT_PRIORITY = [
    # Linux/Docker（WenQuanYi）
    "WenQuanYi Micro Hei",
    "WenQuanYi Zen Hei",
    # macOS
    "PingFang SC",
    "STSong",
    "Songti SC",
    "Heiti SC",
    # Windows
    "SimSun",
    "SimHei",
    "Microsoft YaHei",
    # 通用
    "Arial Unicode MS",
]

_cached_font: str | None = None


def _get_available_font_names() -> set[str]:
    """返回系统已安装字体名称集合（小写）。"""
    return {f.name for f in fm.fontManager.ttflist}


def get_chinese_font() -> str:
    """返回可用中文字体名，找不到返回 'DejaVu Sans'。"""
    global _cached_font
    if _cached_font is not None:
        return _cached_font

    available = _get_available_font_names()
    for font_name in FONT_PRIORITY:
        if font_name in available:
            _cached_font = font_name
            logger.info("Found Chinese font: %s", font_name)
            return font_name

    logger.warning(
        "No Chinese font found. Falling back to DejaVu Sans. "
        "Chinese characters may not render correctly."
    )
    _cached_font = "DejaVu Sans"
    return _cached_font


def setup_matplotlib_fonts() -> str:
    """
    配置 matplotlib rcParams 以支持中文显示。
    返回实际使用的字体名。
    """
    font_name = get_chinese_font()

    matplotlib.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [font_name, "DejaVu Sans"],
            "axes.unicode_minus": False,  # 正确显示负号
        }
    )

    logger.info("Matplotlib fonts configured: %s", font_name)
    return font_name
