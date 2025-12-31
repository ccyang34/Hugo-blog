---
title: "Pyecharts测试"
date: 2025-12-31T12:48:00+08:00
lastmod: 2025-12-31T12:48:00+08:00
description: "使用 Pyecharts 生成交互式榨利图表的测试博客。"
draft: false
categories: ["技术测试"]
tags: ["Pyecharts", "可视化", "期货", "测试"]
---

## 📊 Pyecharts 交互式图表测试

本文使用 **Pyecharts** 生成交互式 HTML 图表，并嵌入 Hugo 博客进行展示测试。

### 数据快照

- **最新榨利**: `315.95` 元/吨
- **盘面榨利**: `-3.84` 元/吨
- **豆油价格**: `7878` 元/吨
- **豆粕价格**: `2778` 元/吨
- **豆二价格**: `3492` 元/吨

---

## � 榨利走势图

{{< rawhtml >}}
<iframe src="/charts/pyecharts_margin.html" width="100%" height="450px" frameborder="0" scrolling="no"></iframe>
{{< /rawhtml >}}

---

## 📈 期货价格走势图

{{< rawhtml >}}
<iframe src="/charts/pyecharts_price.html" width="100%" height="450px" frameborder="0" scrolling="no"></iframe>
{{< /rawhtml >}}

---

## 🛠️ 技术说明

- **图表库**: Pyecharts (基于 Apache ECharts)
- **嵌入方式**: iframe 嵌入独立 HTML 文件
- **交互功能**: 支持缩放、拖拽、悬停提示等
- **更新时间**: 2025-12-31 12:48:00
