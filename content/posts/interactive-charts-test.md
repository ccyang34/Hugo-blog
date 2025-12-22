---
title: "交互式图表框架测试"
date: 2025-12-22T18:27:00+08:00
categories: ["技术"]
tags: ["ECharts", "图表", "可视化", "测试"]
draft: false
---

本文测试多种交互式图表框架在 Hugo 博客中的表现。

<!--more-->

## 1. ECharts 折线图

<div id="echart-line" style="width: 100%; height: 400px; margin: 20px 0; background: #f5f5f5; border-radius: 8px;"></div>

## 2. ECharts 柱状图

<div id="echart-bar" style="width: 100%; height: 350px; margin: 20px 0; background: #f5f5f5; border-radius: 8px;"></div>

## 3. ECharts 饼图

<div id="echart-pie" style="width: 100%; height: 350px; margin: 20px 0; background: #f5f5f5; border-radius: 8px;"></div>

## 4. ECharts K线图

<div id="echart-candlestick" style="width: 100%; height: 450px; margin: 20px 0; background: #f5f5f5; border-radius: 8px;"></div>

## 5. ECharts 雷达图

<div id="echart-radar" style="width: 100%; height: 400px; margin: 20px 0; background: #f5f5f5; border-radius: 8px;"></div>

---

## 总结

| 图表类型 | 用途 | 交互特性 |
|---------|------|---------|
| 折线图 | 趋势分析 | 悬停提示、缩放 |
| 柱状图 | 对比分析 | 渐变色、动画 |
| 饼图 | 结构分析 | 环形、高亮 |
| K线图 | 行情展示 | 十字光标 |
| 雷达图 | 多维评估 | 面积填充 |

<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<script>
(function() {
    function initCharts() {
        if (typeof echarts === 'undefined') {
            setTimeout(initCharts, 100);
            return;
        }
        
        // 1. 折线图
        var chartLine = echarts.init(document.getElementById('echart-line'));
        chartLine.setOption({
            title: { text: '豆油期货价格走势', left: 'center' },
            tooltip: { trigger: 'axis' },
            legend: { data: ['收盘价', 'MA5', 'MA20'], top: 30 },
            grid: { top: 80, bottom: 30, left: 50, right: 20 },
            xAxis: { type: 'category', data: ['12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07', '12-08', '12-09', '12-10', '12-11', '12-12'] },
            yAxis: { type: 'value', min: 7500, max: 8200 },
            series: [
                { name: '收盘价', type: 'line', data: [7680, 7720, 7690, 7750, 7810, 7780, 7850, 7820, 7900, 7880, 7950, 7920], smooth: true },
                { name: 'MA5', type: 'line', data: [7650, 7670, 7690, 7710, 7730, 7760, 7790, 7810, 7840, 7860, 7890, 7910], smooth: true, lineStyle: { type: 'dashed' } },
                { name: 'MA20', type: 'line', data: [7600, 7620, 7640, 7660, 7680, 7700, 7720, 7740, 7760, 7780, 7800, 7820], smooth: true, lineStyle: { type: 'dotted' } }
            ]
        });
        
        // 2. 柱状图
        var chartBar = echarts.init(document.getElementById('echart-bar'));
        chartBar.setOption({
            title: { text: '月度成交量对比', left: 'center' },
            tooltip: { trigger: 'axis' },
            grid: { left: 50, right: 20 },
            xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
            yAxis: { type: 'value', name: '万手' },
            series: [{
                name: '成交量',
                type: 'bar',
                data: [120, 200, 150, 80, 70, 110],
                itemStyle: { color: '#5470c6' }
            }]
        });
        
        // 3. 饼图
        var chartPie = echarts.init(document.getElementById('echart-pie'));
        chartPie.setOption({
            title: { text: '持仓结构分析', left: 'center' },
            tooltip: { trigger: 'item' },
            legend: { orient: 'vertical', left: 'left', top: 'middle' },
            series: [{
                name: '持仓占比',
                type: 'pie',
                radius: ['40%', '70%'],
                data: [
                    { value: 1048, name: '多头' },
                    { value: 735, name: '空头' },
                    { value: 580, name: '套保' },
                    { value: 484, name: '套利' }
                ]
            }]
        });
        
        // 4. K线图
        var chartK = echarts.init(document.getElementById('echart-candlestick'));
        chartK.setOption({
            title: { text: '豆油期货K线图', left: 'center' },
            tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
            grid: { left: 60, right: 20 },
            xAxis: { type: 'category', data: ['12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07', '12-08', '12-09', '12-10'] },
            yAxis: { type: 'value', min: 7600, max: 8000 },
            series: [{
                name: '日K',
                type: 'candlestick',
                data: [
                    [7680, 7720, 7650, 7740],
                    [7720, 7690, 7680, 7750],
                    [7690, 7750, 7670, 7770],
                    [7750, 7810, 7730, 7830],
                    [7810, 7780, 7760, 7820],
                    [7780, 7850, 7770, 7870],
                    [7850, 7820, 7800, 7860],
                    [7820, 7900, 7810, 7920],
                    [7900, 7880, 7870, 7930],
                    [7880, 7950, 7860, 7980]
                ],
                itemStyle: { color: '#ef5350', color0: '#26a69a', borderColor: '#ef5350', borderColor0: '#26a69a' }
            }]
        });
        
        // 5. 雷达图
        var chartRadar = echarts.init(document.getElementById('echart-radar'));
        chartRadar.setOption({
            title: { text: '投资组合评估', left: 'center' },
            tooltip: {},
            legend: { data: ['当前组合', '基准组合'], top: 30 },
            radar: {
                indicator: [
                    { name: '收益率', max: 100 },
                    { name: '夏普比', max: 100 },
                    { name: '最大回撤', max: 100 },
                    { name: '波动率', max: 100 },
                    { name: '流动性', max: 100 },
                    { name: '多样化', max: 100 }
                ]
            },
            series: [{
                type: 'radar',
                data: [
                    { value: [85, 72, 60, 55, 80, 75], name: '当前组合', areaStyle: { opacity: 0.3 } },
                    { value: [70, 65, 50, 60, 70, 65], name: '基准组合', areaStyle: { opacity: 0.3 } }
                ]
            }]
        });
        
        // 响应式
        window.addEventListener('resize', function() {
            chartLine.resize();
            chartBar.resize();
            chartPie.resize();
            chartK.resize();
            chartRadar.resize();
        });
    }
    
    if (document.readyState === 'complete') {
        initCharts();
    } else {
        window.addEventListener('load', initCharts);
    }
})();
</script>
