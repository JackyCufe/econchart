# EconChart - 学术图表美化器

专为中国经管类期刊设计的在线图表生成工具。

## 支持图类型

- 📌 系数图（回归结果可视化，支持 95%/90% CI）
- 📈 折线图（时间序列）
- 📊 柱状图（分组/堆叠）
- 🔵 散点图（带回归线）
- 📦 箱线图
- 🌡️ 热力图（相关矩阵）
- 📉 分布直方图

## 支持期刊格式

| 期刊 | 正文字体 | 英文字体 | 图宽 |
|------|---------|---------|------|
| 经济研究 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 管理世界 | 黑体 (SimHei) | Arial | 7.0" |
| 中国工业经济 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 金融研究 | 宋体 (SimSun) | Times New Roman | 6.5" |
| 通用学术 | 黑体 (SimHei) | DejaVu Sans | 7.0" |

## 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 项目结构

```
econchart/
├── app.py              # 入口文件
├── requirements.txt    # 依赖清单
├── assets/
│   └── style.css       # 自定义样式
├── core/
│   ├── font_manager.py # 中文字体检测
│   ├── theme.py        # 期刊主题定义
│   └── exporter.py     # 图表导出（PNG/SVG/PDF）
├── charts/             # 图表绘制模块（7 种）
└── ui/                 # Streamlit UI 组件和页面
```

## 特性说明

### 中文字体自动检测

按优先级检测：
- Linux/Docker：WenQuanYi Micro Hei / WenQuanYi Zen Hei
- macOS：PingFang SC / STSong / Songti SC
- Windows：SimSun / SimHei / Microsoft YaHei

找不到中文字体时回退到 `DejaVu Sans`（英文字体）。

### 免费 vs 付费

| 功能 | 免费 | 付费 |
|------|------|------|
| 预览图 | ✅ 96 DPI | ✅ |
| PNG 导出 | ✅ 150 DPI + 水印 | ✅ 300 DPI 无水印 |
| SVG 导出 | ✅ | ✅ |
| PDF 导出 | ✅ | ✅ |

### 与 EconKit 配合

```
EconKit（实证分析）→ 导出系数表 → EconChart（美化图表）→ 投稿
```

系数图支持直接粘贴回归系数表（含 variable / coef / se 列）。

## 工程规范

遵循 deepvcode 规范：
- 单文件 ≤ 400 行
- 函数 ≤ 50 行
- 防御性编程，快速失败
- 按功能域划分目录

## 开发计划

- [ ] 用户账号 & 付费解锁 300 DPI
- [ ] 更多图类型（地图、网络图）
- [ ] 批量导出
- [ ] 图表模板保存
- [ ] API 接口（供 EconKit 直接调用）
