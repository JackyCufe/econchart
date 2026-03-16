"""
EconChart 烟雾测试（Smoke Tests）
覆盖所有图表类型和核心功能，确保常见输入不会 crash。
"""
from __future__ import annotations

import sys
import os
import math

import matplotlib
matplotlib.use("Agg")  # 必须在 pyplot import 前设置

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

# 将项目根目录添加到 sys.path，确保导入正确
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(autouse=True)
def close_all_figures():
    """每个测试后自动清理所有 matplotlib figure。"""
    yield
    plt.close("all")


@pytest.fixture
def coef_df() -> pd.DataFrame:
    """标准系数图数据（5行，含 variable/coef/se 列）。"""
    return pd.DataFrame({
        "variable": ["GDP", "CPI", "M2", "Interest", "FDI"],
        "coef": [0.35, -0.12, 0.08, -0.25, 0.15],
        "se":   [0.05,  0.03, 0.04,  0.06, 0.03],
    })


@pytest.fixture
def scatter_df() -> pd.DataFrame:
    """标准散点图数据。"""
    rng = np.random.default_rng(42)
    n = 30
    x = rng.uniform(0, 10, n)
    return pd.DataFrame({
        "x":     x,
        "y":     2 * x + rng.normal(0, 1, n),
        "group": ["A" if i % 2 == 0 else "B" for i in range(n)],
        "size":  rng.uniform(1, 10, n),
    })


@pytest.fixture
def bar_df() -> pd.DataFrame:
    """标准柱状图数据。"""
    return pd.DataFrame({
        "category": ["甲", "乙", "丙", "丁"],
        "value":    [10.0, 25.0, 18.0, 30.0],
        "value2":   [5.0, 15.0, 12.0, 20.0],
    })


@pytest.fixture
def line_df() -> pd.DataFrame:
    """标准折线图数据。"""
    return pd.DataFrame({
        "year": [2018, 2019, 2020, 2021, 2022],
        "gdp":  [6.7, 6.1, 2.3, 8.1, 5.5],
        "cpi":  [2.1, 2.9, 2.5, 0.9, 2.0],
    })


@pytest.fixture
def boxplot_df() -> pd.DataFrame:
    """标准箱线图数据。"""
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "A": rng.normal(0, 1, 50),
        "B": rng.normal(2, 1.5, 50),
        "C": rng.normal(-1, 0.5, 50),
    })


@pytest.fixture
def heatmap_df() -> pd.DataFrame:
    """5x5 相关矩阵数据。"""
    rng = np.random.default_rng(42)
    raw = rng.uniform(-1, 1, (5, 5))
    # 对称化并对角线置1，模拟相关矩阵
    mat = (raw + raw.T) / 2
    np.fill_diagonal(mat, 1.0)
    cols = ["A", "B", "C", "D", "E"]
    return pd.DataFrame(mat, index=cols, columns=cols)


@pytest.fixture
def hist_df() -> pd.DataFrame:
    """标准直方图数据。"""
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "income": rng.normal(5000, 1000, 100),
    })


# ============================================================
# 1. core/font_manager
# ============================================================

class TestFontManager:
    def test_setup_matplotlib_fonts_returns_string_or_none(self):
        """setup_matplotlib_fonts() 返回字符串（字体名），不崩溃。"""
        from core.font_manager import setup_matplotlib_fonts
        result = setup_matplotlib_fonts()
        assert result is None or isinstance(result, str), (
            f"Expected str or None, got {type(result)}"
        )
        # 按当前实现，总是返回 str（回退到 DejaVu Sans）
        assert isinstance(result, str)

    def test_get_chinese_font_no_exception(self):
        """get_chinese_font() 不抛异常，返回字符串。"""
        from core.font_manager import get_chinese_font
        result = get_chinese_font()
        assert isinstance(result, str)
        assert len(result) > 0


# ============================================================
# 2. core/theme
# ============================================================

class TestTheme:
    EXPECTED_THEMES = ["经济研究", "管理世界", "中国工业经济", "金融研究", "通用学术"]

    def test_themes_contains_all_five(self):
        """THEMES 字典包含全部5个主题。"""
        from core.theme import THEMES
        for name in self.EXPECTED_THEMES:
            assert name in THEMES, f"缺少主题：{name}"

    def test_each_theme_has_required_fields(self):
        """每个 theme 都有必要字段。"""
        from core.theme import THEMES
        for name in self.EXPECTED_THEMES:
            theme = THEMES[name]
            assert hasattr(theme, "colors"), f"{name} 缺少 colors"
            assert len(theme.colors) > 0, f"{name} colors 为空"
            assert hasattr(theme, "font_size_title"), f"{name} 缺少 font_size_title"
            assert hasattr(theme, "fig_width"), f"{name} 缺少 fig_width"
            assert hasattr(theme, "fig_height"), f"{name} 缺少 fig_height"
            assert theme.fig_width > 0
            assert theme.fig_height > 0

    def test_get_theme_valid(self):
        """get_theme() 对已知主题正常返回。"""
        from core.theme import get_theme
        theme = get_theme("经济研究")
        assert theme.name == "经济研究"

    def test_get_theme_invalid_raises(self):
        """get_theme() 对未知主题抛出 ValueError。"""
        from core.theme import get_theme
        with pytest.raises(ValueError, match="Unknown theme"):
            get_theme("不存在的主题")


# ============================================================
# 3. core/exporter
# ============================================================

class TestExporter:
    @pytest.fixture
    def simple_fig(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        return fig

    def test_export_png_with_watermark(self, simple_fig):
        """export_figure png + watermark=True → bytes，不为空。"""
        from core.exporter import export_figure
        data = export_figure(simple_fig, "png", dpi=96, watermark=True)
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_export_png_without_watermark(self, simple_fig):
        """export_figure png + watermark=False → bytes，不为空。"""
        from core.exporter import export_figure
        data = export_figure(simple_fig, "png", dpi=150, watermark=False)
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_export_invalid_format_raises(self, simple_fig):
        """无效格式应抛出 ValueError，不静默失败。"""
        from core.exporter import export_figure
        with pytest.raises(ValueError, match="Unsupported export format"):
            export_figure(simple_fig, "bmp")  # type: ignore

    def test_export_svg(self, simple_fig):
        """SVG 导出正常返回 bytes。"""
        from core.exporter import export_figure
        data = export_figure(simple_fig, "svg", watermark=False)
        assert isinstance(data, bytes)
        assert len(data) > 0


# ============================================================
# 4. charts/coefficient_plot
# ============================================================

class TestCoefficientPlot:
    def test_normal_input_returns_figure(self, coef_df):
        """正常输入（5行 df）→ Figure。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df)
        assert isinstance(fig, plt.Figure)

    def test_ci_type_se(self, coef_df):
        """ci_type='se' → Figure。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df, ci_type="se")
        assert isinstance(fig, plt.Figure)

    def test_ci_type_95ci(self, coef_df):
        """ci_type='95ci' with se column → Figure。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df, ci_type="95ci")
        assert isinstance(fig, plt.Figure)

    def test_ci_type_90ci(self, coef_df):
        """ci_type='90ci' → Figure。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df, ci_type="90ci")
        assert isinstance(fig, plt.Figure)

    def test_nan_coef_no_crash(self, coef_df):
        """含 NaN 的 coef 行 → 不 crash（coef 转换 errors='raise' 会报错，期望能处理）。"""
        from charts.coefficient_plot import plot_coefficients
        df = coef_df.copy()
        df.loc[2, "coef"] = float("nan")
        # _validate_data 用 errors='raise'，NaN 本身不触发异常（NaN 是有效 float）
        # 预期不 crash
        fig = plot_coefficients(df)
        assert isinstance(fig, plt.Figure)

    def test_missing_se_column_raises(self):
        """缺少 se 列时应抛出 ValueError。"""
        from charts.coefficient_plot import plot_coefficients
        df = pd.DataFrame({
            "variable": ["A", "B"],
            "coef": [0.1, 0.2],
            # 无 se 列
        })
        with pytest.raises((KeyError, ValueError)):
            plot_coefficients(df, ci_type="se")

    def test_missing_required_column_raises(self):
        """缺少 variable 列时应抛出 ValueError。"""
        from charts.coefficient_plot import plot_coefficients
        df = pd.DataFrame({
            "coef": [0.1, 0.2],
            "se":   [0.01, 0.02],
        })
        with pytest.raises(ValueError, match="必要列"):
            plot_coefficients(df)

    def test_sort_by_coef_asc(self, coef_df):
        """sort_by='coef_asc' → Figure 正常生成。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df, sort_by="coef_asc")
        assert isinstance(fig, plt.Figure)

    def test_with_title(self, coef_df):
        """传入 title → 正常渲染。"""
        from charts.coefficient_plot import plot_coefficients
        fig = plot_coefficients(coef_df, title="回归结果")
        assert isinstance(fig, plt.Figure)


# ============================================================
# 5. charts/scatter
# ============================================================

class TestScatter:
    def test_normal_xy_returns_figure(self, scatter_df):
        """正常 x/y 列 → Figure。"""
        from charts.scatter import plot_scatter
        fig = plot_scatter(scatter_df, x_col="x", y_col="y")
        assert isinstance(fig, plt.Figure)

    def test_add_regression_true(self, scatter_df):
        """add_regression=True → Figure（含回归线）。"""
        from charts.scatter import plot_scatter
        fig = plot_scatter(scatter_df, x_col="x", y_col="y", add_regression=True)
        assert isinstance(fig, plt.Figure)

    def test_nan_in_data_no_crash(self, scatter_df):
        """含 NaN → 不崩（回归线内部 dropna 处理）。"""
        from charts.scatter import plot_scatter
        df = scatter_df.copy()
        df.loc[0, "x"] = float("nan")
        df.loc[5, "y"] = float("nan")
        fig = plot_scatter(df, x_col="x", y_col="y", add_regression=True)
        assert isinstance(fig, plt.Figure)

    def test_group_col(self, scatter_df):
        """group_col 分组 → Figure。"""
        from charts.scatter import plot_scatter
        fig = plot_scatter(scatter_df, x_col="x", y_col="y", color_col="group")
        assert isinstance(fig, plt.Figure)

    def test_missing_column_raises(self, scatter_df):
        """缺少列时抛出 ValueError。"""
        from charts.scatter import plot_scatter
        with pytest.raises(ValueError, match="缺少列"):
            plot_scatter(scatter_df, x_col="nonexistent", y_col="y")


# ============================================================
# 6. charts/bar
# ============================================================

class TestBar:
    def test_category_value_returns_figure(self, bar_df):
        """category + value → Figure。"""
        from charts.bar import plot_bar
        fig = plot_bar(bar_df, x_col="category", y_cols=["value"])
        assert isinstance(fig, plt.Figure)

    def test_horizontal_bar(self, bar_df):
        """水平柱状图（horizontal=True）→ Figure。"""
        from charts.bar import plot_bar
        fig = plot_bar(bar_df, x_col="category", y_cols=["value"], horizontal=True)
        assert isinstance(fig, plt.Figure)

    def test_grouped_bar(self, bar_df):
        """分组柱状图（多 y 列）→ Figure。"""
        from charts.bar import plot_bar
        fig = plot_bar(bar_df, x_col="category", y_cols=["value", "value2"])
        assert isinstance(fig, plt.Figure)

    def test_stacked_bar(self, bar_df):
        """堆叠柱状图（stacked=True）→ Figure。"""
        from charts.bar import plot_bar
        fig = plot_bar(bar_df, x_col="category", y_cols=["value", "value2"], stacked=True)
        assert isinstance(fig, plt.Figure)

    def test_missing_x_col_raises(self, bar_df):
        """缺少 x_col 抛出 ValueError。"""
        from charts.bar import plot_bar
        with pytest.raises(ValueError, match="缺少列"):
            plot_bar(bar_df, x_col="nonexistent", y_cols=["value"])


# ============================================================
# 7. charts/line
# ============================================================

class TestLine:
    def test_single_y_returns_figure(self, line_df):
        """x + y → Figure。"""
        from charts.line import plot_line
        fig = plot_line(line_df, x_col="year", y_cols=["gdp"])
        assert isinstance(fig, plt.Figure)

    def test_multiple_y_cols(self, line_df):
        """多条线（多个 y 列）→ Figure。"""
        from charts.line import plot_line
        fig = plot_line(line_df, x_col="year", y_cols=["gdp", "cpi"])
        assert isinstance(fig, plt.Figure)

    def test_with_ci(self, line_df):
        """add_ci=True → 正常渲染。"""
        from charts.line import plot_line
        fig = plot_line(line_df, x_col="year", y_cols=["gdp"], add_ci=True)
        assert isinstance(fig, plt.Figure)

    def test_missing_x_col_raises(self, line_df):
        """缺少 x_col 抛出 ValueError。"""
        from charts.line import plot_line
        with pytest.raises(ValueError, match="缺少列"):
            plot_line(line_df, x_col="nonexistent", y_cols=["gdp"])


# ============================================================
# 8. charts/boxplot
# ============================================================

class TestBoxplot:
    def test_single_variable(self, boxplot_df):
        """单变量 → Figure。"""
        from charts.boxplot import plot_boxplot
        fig = plot_boxplot(boxplot_df, y_cols=["A"])
        assert isinstance(fig, plt.Figure)

    def test_multiple_variables(self, boxplot_df):
        """多变量 → Figure。"""
        from charts.boxplot import plot_boxplot
        fig = plot_boxplot(boxplot_df, y_cols=["A", "B", "C"])
        assert isinstance(fig, plt.Figure)

    def test_missing_col_raises(self, boxplot_df):
        """缺少列抛出 ValueError。"""
        from charts.boxplot import plot_boxplot
        with pytest.raises(ValueError, match="缺少列"):
            plot_boxplot(boxplot_df, y_cols=["nonexistent"])


# ============================================================
# 9. charts/heatmap
# ============================================================

class TestHeatmap:
    def test_5x5_correlation_matrix(self, heatmap_df):
        """5x5 相关矩阵 → Figure。"""
        from charts.heatmap import plot_heatmap
        fig = plot_heatmap(heatmap_df)
        assert isinstance(fig, plt.Figure)

    def test_all_ones_no_crash(self):
        """值全为 1（对角矩阵）→ 不崩。"""
        from charts.heatmap import plot_heatmap
        cols = ["X1", "X2", "X3", "X4", "X5"]
        df = pd.DataFrame(np.ones((5, 5)), index=cols, columns=cols)
        fig = plot_heatmap(df)
        assert isinstance(fig, plt.Figure)

    def test_no_numeric_data_raises(self):
        """无数值列应抛出 ValueError。"""
        from charts.heatmap import plot_heatmap
        df = pd.DataFrame({"label": ["a", "b", "c"]})
        with pytest.raises(ValueError, match="没有数值列"):
            plot_heatmap(df)

    def test_with_title(self, heatmap_df):
        """传入 title → 正常渲染。"""
        from charts.heatmap import plot_heatmap
        fig = plot_heatmap(heatmap_df, title="相关性热力图")
        assert isinstance(fig, plt.Figure)


# ============================================================
# 10. charts/histogram
# ============================================================

class TestHistogram:
    def test_single_variable_distribution(self, hist_df):
        """单变量分布 → Figure。"""
        from charts.histogram import plot_histogram
        fig = plot_histogram(hist_df, col="income")
        assert isinstance(fig, plt.Figure)

    def test_nan_in_data_no_crash(self, hist_df):
        """含 NaN → 不崩（dropna 处理）。"""
        from charts.histogram import plot_histogram
        df = hist_df.copy()
        df.loc[[0, 10, 20], "income"] = float("nan")
        fig = plot_histogram(df, col="income")
        assert isinstance(fig, plt.Figure)

    def test_no_kde(self, hist_df):
        """add_kde=False → 正常渲染。"""
        from charts.histogram import plot_histogram
        fig = plot_histogram(hist_df, col="income", add_kde=False)
        assert isinstance(fig, plt.Figure)

    def test_missing_col_raises(self, hist_df):
        """缺少列抛出 ValueError。"""
        from charts.histogram import plot_histogram
        with pytest.raises(ValueError, match="缺少列"):
            plot_histogram(hist_df, col="nonexistent")

    def test_all_nan_raises(self):
        """全部 NaN 应抛出 ValueError（无有效数据）。"""
        from charts.histogram import plot_histogram
        df = pd.DataFrame({"v": [float("nan"), float("nan")]})
        with pytest.raises(ValueError, match="没有有效数据"):
            plot_histogram(df, col="v")


# ============================================================
# 11. 边界条件
# ============================================================

class TestEdgeCases:
    def test_single_row_coef_plot(self):
        """单行数据 → 系数图不崩。"""
        from charts.coefficient_plot import plot_coefficients
        df = pd.DataFrame({"variable": ["GDP"], "coef": [0.5], "se": [0.1]})
        fig = plot_coefficients(df)
        assert isinstance(fig, plt.Figure)

    def test_single_row_scatter(self):
        """单行数据 → 散点图不崩（回归线点不够会跳过）。"""
        from charts.scatter import plot_scatter
        df = pd.DataFrame({"x": [1.0], "y": [2.0]})
        fig = plot_scatter(df, x_col="x", y_col="y", add_regression=True)
        assert isinstance(fig, plt.Figure)

    def test_single_row_bar(self):
        """单行数据 → 柱状图不崩。"""
        from charts.bar import plot_bar
        df = pd.DataFrame({"cat": ["A"], "val": [10.0]})
        fig = plot_bar(df, x_col="cat", y_cols=["val"])
        assert isinstance(fig, plt.Figure)

    def test_single_row_line(self):
        """单行数据 → 折线图不崩。"""
        from charts.line import plot_line
        df = pd.DataFrame({"x": [2020], "y": [5.5]})
        fig = plot_line(df, x_col="x", y_cols=["y"])
        assert isinstance(fig, plt.Figure)

    def test_empty_dataframe_coef_raises(self):
        """空 DataFrame → 系数图应抛出明确异常，不 crash with IndexError。"""
        from charts.coefficient_plot import plot_coefficients
        df = pd.DataFrame(columns=["variable", "coef", "se"])
        with pytest.raises((ValueError, Exception)) as exc_info:
            plot_coefficients(df)
        # 确保不是 IndexError 类型（即有明确错误处理）
        assert not isinstance(exc_info.value, IndexError), (
            "空 DataFrame 应抛出 ValueError，而非 IndexError"
        )

    def test_empty_dataframe_scatter_raises(self):
        """空 DataFrame → 散点图应能处理（不崩）或抛出明确异常。"""
        from charts.scatter import plot_scatter
        df = pd.DataFrame({"x": pd.Series([], dtype=float), "y": pd.Series([], dtype=float)})
        # 空数据：散点图不崩（空图也可以）
        try:
            fig = plot_scatter(df, x_col="x", y_col="y", add_regression=False)
            assert isinstance(fig, plt.Figure)
        except (ValueError, Exception) as e:
            assert not isinstance(e, IndexError), f"不应 IndexError: {e}"

    def test_chinese_column_names(self):
        """列名含中文 → 正常渲染。"""
        from charts.bar import plot_bar
        df = pd.DataFrame({
            "地区": ["北京", "上海", "广州", "深圳"],
            "GDP增速": [6.1, 5.8, 7.2, 6.5],
        })
        fig = plot_bar(df, x_col="地区", y_cols=["GDP增速"])
        assert isinstance(fig, plt.Figure)

    def test_chinese_column_names_line(self):
        """折线图列名含中文 → 正常渲染。"""
        from charts.line import plot_line
        df = pd.DataFrame({
            "年份": [2019, 2020, 2021, 2022],
            "增长率": [6.1, 2.3, 8.1, 5.5],
        })
        fig = plot_line(df, x_col="年份", y_cols=["增长率"])
        assert isinstance(fig, plt.Figure)

    def test_chinese_column_names_scatter(self):
        """散点图列名含中文 → 正常渲染。"""
        from charts.scatter import plot_scatter
        rng = np.random.default_rng(42)
        df = pd.DataFrame({
            "人均收入": rng.uniform(3000, 10000, 20),
            "消费支出": rng.uniform(2000, 8000, 20),
        })
        fig = plot_scatter(df, x_col="人均收入", y_col="消费支出", add_regression=True)
        assert isinstance(fig, plt.Figure)
