---
title: EconChart 学术图表美化器
emoji: 📊
colorFrom: purple
colorTo: pink
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
license: MIT
tags:
  - econometrics
  - charts
  - academic
  - streamlit
  - python
---

<div align="center">

# 📊 EconChart

**Academic Chart Beautifier for Chinese Economics & Management Journals**

**专为中国经管类期刊设计的学术图表美化器**

No Stata / R / Origin needed | One-click publication-ready charts

无需 Stata / R / Origin | 一键生成符合投稿规范的高质量图表

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red.svg)](https://streamlit.io/)
[![ModelScope](https://img.shields.io/badge/🤖_Demo-ModelScope-624aff)](https://modelscope.cn/studios/JackyCufe/EconChart)

**🚀 Live Demo (no install needed):**

[![ModelScope](https://img.shields.io/badge/Demo-ModelScope（China）-624aff?style=for-the-badge)](https://modelscope.cn/studios/JackyCufe/EconChart)
[![HuggingFace](https://img.shields.io/badge/Demo-HuggingFace（Global）-orange?style=for-the-badge)](https://huggingface.co/spaces/JackyCufe/EconChart)

Target journals: 经济研究 / 管理世界 / 中国工业经济 / 金融研究 / 经济学季刊

</div>

---

## ✨ Supported Chart Types

| Chart | Description |
|-------|-------------|
| 📌 **Coefficient Plot** | Regression result visualization with 95%/90% CI |
| 📈 **Line Chart** | Time series, trend comparison |
| 📊 **Bar Chart** | Grouped / stacked bars |
| 🔵 **Scatter Plot** | With regression fit line |
| 📦 **Box Plot** | Distribution comparison |
| 🌡️ **Heatmap** | Correlation matrix visualization |
| 📉 **Histogram** | Variable distribution analysis |

## 🗞️ Supported Journal Formats

| Journal | Body Font | English Font | Width |
|---------|-----------|-------------|-------|
| 经济研究 | SimSun | Times New Roman | 6.5" |
| 管理世界 | SimHei | Arial | 7.0" |
| 中国工业经济 | SimSun | Times New Roman | 6.5" |
| 金融研究 | SimSun | Times New Roman | 6.5" |
| General Academic | SimHei | DejaVu Sans | 7.0" |

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501.

---

## 🔗 Works with EconPrep & EconKit

```
[EconPrep] Data Cleaning
      ↓
[EconKit] Empirical Analysis → Export coefficient table
      ↓
[EconChart] Chart Beautification → Submit to journal
```

The coefficient plot accepts a regression table with `variable / coef / se` columns directly from EconKit output.

---

## 🛠️ Tech Stack

- **Streamlit** ≥ 1.32 — UI framework
- **matplotlib** ≥ 3.7 — Chart rendering
- **pandas** ≥ 2.0 — Data processing
- **scipy** ≥ 1.11 — Statistical computation
- **Pillow** ≥ 10.0 — Image processing

---
---

## ✨ 支持图类型

| 图类型 | 说明 |
|--------|------|
| 📌 **系数图** | 回归结果可视化，支持 95%/90% CI |
| 📈 **折线图** | 时间序列、趋势对比 |
| 📊 **柱状图** | 分组 / 堆叠柱状图 |
| 🔵 **散点图** | 带回归拟合线 |
| 📦 **箱线图** | 分布对比 |
| 🌡️ **热力图** | 相关矩阵可视化 |
| 📉 **直方图** | 变量分布分析 |

## 🗞️ 支持期刊格式

| 期刊 | 正文字体 | 英文字体 | 图宽 |
|------|---------|---------|------|
| 经济研究 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 管理世界 | 黑体 (SimHei) | Arial | 7.0" |
| 中国工业经济 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 金融研究 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 通用学术 | 黑体 (SimHei) | DejaVu Sans | 7.0" |

## 🚀 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

访问 http://localhost:8501 即可使用。

---

## 🔗 与 EconKit / EconPrep 配合使用

```
[EconPrep] 数据清洗
      ↓
[EconKit] 实证分析 → 导出系数表
      ↓
[EconChart] 美化图表 → 投稿
```

系数图支持直接粘贴回归系数表（含 variable / coef / se 列），无缝衔接 EconKit 输出。

---

## 🛠️ 技术栈

- **Streamlit** ≥ 1.32 — 界面框架
- **matplotlib** ≥ 3.7 — 图表绘制
- **pandas** ≥ 2.0 — 数据处理
- **scipy** ≥ 1.11 — 统计计算
- **Pillow** ≥ 10.0 — 图片处理

### 中文字体自动检测顺序

1. **Linux/Docker**：WenQuanYi Micro Hei / WenQuanYi Zen Hei
2. **macOS**：PingFang SC / STSong / Songti SC
3. **Windows**：SimSun / SimHei / Microsoft YaHei
4. **兜底**：DejaVu Sans（英文字体）
