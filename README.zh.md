[![English](https://img.shields.io/badge/README-English-blue)](README.md)

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
