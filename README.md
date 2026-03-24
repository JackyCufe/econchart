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

**专为中国经管类期刊设计的学术图表美化器**

**Academic Chart Beautifier for Chinese Economics & Management Journals**

无需 Stata / R / Origin | 一键生成符合投稿规范的高质量图表

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red.svg)](https://streamlit.io/)
[![ModelScope](https://img.shields.io/badge/🤖_Demo-ModelScope-624aff)](https://modelscope.cn/studios/JackyCufe/EconChart)

**🚀 在线体验（无需安装）：**

[![ModelScope](https://img.shields.io/badge/在线Demo-ModelScope（国内推荐）-624aff?style=for-the-badge)](https://modelscope.cn/studios/JackyCufe/EconChart)
[![HuggingFace](https://img.shields.io/badge/在线Demo-HuggingFace（国际）-orange?style=for-the-badge)](https://huggingface.co/spaces/JackyCufe/EconChart)

适用期刊：经济研究 / 管理世界 / 中国工业经济 / 金融研究 / 经济学季刊

</div>

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

## 📁 项目结构

```
econchart/
├── app.py                    # Streamlit 入口
├── requirements.txt
├── README.md
├── assets/
│   └── style.css             # 自定义样式
├── core/
│   ├── font_manager.py       # 中文字体自动检测
│   ├── theme.py              # 期刊主题定义
│   └── exporter.py           # 图表导出（PNG/SVG/PDF）
├── charts/                   # 图表绘制模块（7 种）
│   ├── coefficient_plot.py
│   ├── scatter.py
│   ├── bar.py
│   ├── line.py
│   ├── boxplot.py
│   ├── heatmap.py
│   └── histogram.py
└── ui/
    ├── components/
    │   ├── data_input.py     # 数据输入（CSV 粘贴 / 上传）
    │   └── chart_config.py   # 图表参数配置 UI
    └── pages/
        ├── home.py           # 首页
        └── editor.py         # 图表编辑器
```

---

## 🛠️ 技术栈

- **[Streamlit](https://streamlit.io/)** ≥ 1.32 — 界面框架
- **[matplotlib](https://matplotlib.org/)** ≥ 3.7 — 图表绘制
- **[pandas](https://pandas.pydata.org/)** ≥ 2.0 — 数据处理
- **[scipy](https://scipy.org/)** ≥ 1.11 — 统计计算
- **[Pillow](https://python-pillow.org/)** ≥ 10.0 — 图片处理

### 中文字体自动检测顺序

1. **Linux/Docker**：WenQuanYi Micro Hei / WenQuanYi Zen Hei
2. **macOS**：PingFang SC / STSong / Songti SC
3. **Windows**：SimSun / SimHei / Microsoft YaHei
4. **兜底**：DejaVu Sans（英文字体）
