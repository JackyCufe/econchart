"""
图表导出模块。
支持 PNG / SVG / PDF 格式，可选水印叠加。
免费版：低 DPI + 水印；付费版：高 DPI 无水印（预留接口）。
"""
from __future__ import annotations

import io
import logging
from typing import Literal

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

FormatType = Literal["png", "svg", "pdf"]

WATERMARK_TEXT = "EconChart - econkit.com"
WATERMARK_ALPHA = 0.15
WATERMARK_FONTSIZE = 14


def add_watermark(fig: plt.Figure, text: str = WATERMARK_TEXT) -> None:
    """在 fig 右下角叠加半透明水印文字（不新建子图，直接在 figure 坐标系绘制）。"""
    fig.text(
        0.98,
        0.02,
        text,
        transform=fig.transFigure,
        fontsize=WATERMARK_FONTSIZE,
        color="gray",
        alpha=WATERMARK_ALPHA,
        ha="right",
        va="bottom",
        rotation=0,
        fontstyle="italic",
    )


def export_figure(
    fig: plt.Figure,
    fmt: FormatType = "png",
    dpi: int = 96,
    watermark: bool = True,
) -> bytes:
    """
    将 matplotlib Figure 导出为字节流。

    Args:
        fig:        matplotlib Figure 对象
        fmt:        导出格式，"png" | "svg" | "pdf"
        dpi:        输出分辨率
        watermark:  True 时叠加水印（免费版）

    Returns:
        图片字节数据

    Raises:
        ValueError: 不支持的格式
    """
    if fmt not in ("png", "svg", "pdf"):
        raise ValueError(f"Unsupported export format: '{fmt}'. Use png/svg/pdf.")

    if watermark:
        add_watermark(fig)

    buf = io.BytesIO()

    save_kwargs: dict = {"format": fmt, "bbox_inches": "tight"}
    if fmt == "png":
        save_kwargs["dpi"] = dpi

    try:
        fig.savefig(buf, **save_kwargs)
    except Exception as exc:
        logger.error("Failed to export figure: %s", exc)
        raise

    buf.seek(0)
    return buf.read()


def get_mime_type(fmt: FormatType) -> str:
    """返回格式对应的 MIME 类型。"""
    mapping = {
        "png": "image/png",
        "svg": "image/svg+xml",
        "pdf": "application/pdf",
    }
    if fmt not in mapping:
        raise ValueError(f"Unknown format: {fmt}")
    return mapping[fmt]
