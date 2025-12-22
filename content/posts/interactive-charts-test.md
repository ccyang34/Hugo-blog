---
title: "交互式图表框架测试"
date: 2025-12-22T18:27:00+08:00
categories: ["技术"]
tags: ["图表", "可视化", "测试"]
draft: false
---

本文测试多种图表框架在 Hugo 博客中的移动端兼容性。

<!--more-->

---

## 1. Chart.js (Canvas)

<canvas id="chartjs-line" style="width: 100%; max-height: 300px;"></canvas>

---

## 2. ApexCharts

<div id="apex-bar" style="width: 100%; min-height: 300px;"></div>

---

## 3. ECharts

<div id="echart-pie" style="width: 100%; height: 300px;"></div>

---

## 4. Plotly.js

<div id="plotly-scatter" style="width: 100%; height: 300px;"></div>

---

## 5. Google Charts

<div id="google-gauge" style="width: 100%; height: 300px;"></div>

---

## 6. PyEcharts (Python生成)

<div id="pyechart-demo" style="width: 100%; height: 300px;"></div>

---

## 兼容性对比

| 库 | 渲染方式 | 移动端 | 体积 |
|---|---------|-------|------|
| Chart.js | Canvas | ✅ | 小 |
| ApexCharts | SVG | ✅ | 中 |
| ECharts | Canvas | ⚠️ | 大 |
| Plotly | SVG | ✅ | 大 |
| Google Charts | SVG | ✅ | 云端 |
| PyEcharts | Canvas | ⚠️ | 大 |

---

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- ApexCharts -->
<script src="https://cdn.jsdelivr.net/npm/apexcharts@3.44.0/dist/apexcharts.min.js"></script>

<!-- ECharts -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

<!-- Plotly -->
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

<!-- Google Charts -->
<script src="https://www.gstatic.com/charts/loader.js"></script>

<script>
// 等待所有库加载
window.addEventListener('load', function() {
    setTimeout(function() {
        
        // 1. Chart.js
        try {
            var ctx = document.getElementById('chartjs-line');
            if (ctx && typeof Chart !== 'undefined') {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
                        datasets: [{
                            label: '销售额',
                            data: [12, 19, 3, 5, 2, 3],
                            borderColor: '#3b82f6',
                            tension: 0.4
                        }]
                    },
                    options: { responsive: true }
                });
                console.log('Chart.js OK');
            }
        } catch(e) { console.error('Chart.js:', e); }
        
        // 2. ApexCharts
        try {
            var apexEl = document.getElementById('apex-bar');
            if (apexEl && typeof ApexCharts !== 'undefined') {
                new ApexCharts(apexEl, {
                    chart: { type: 'bar', height: 280 },
                    series: [{ name: '数量', data: [44, 55, 41, 67, 22, 43] }],
                    xaxis: { categories: ['A', 'B', 'C', 'D', 'E', 'F'] },
                    colors: ['#10b981']
                }).render();
                console.log('ApexCharts OK');
            }
        } catch(e) { console.error('ApexCharts:', e); }
        
        // 3. ECharts
        try {
            var echartEl = document.getElementById('echart-pie');
            if (echartEl && typeof echarts !== 'undefined') {
                var myChart = echarts.init(echartEl);
                myChart.setOption({
                    title: { text: '占比分析', left: 'center' },
                    series: [{
                        type: 'pie',
                        radius: '60%',
                        data: [
                            { value: 335, name: 'A类' },
                            { value: 310, name: 'B类' },
                            { value: 234, name: 'C类' }
                        ]
                    }]
                });
                window.addEventListener('resize', function() { myChart.resize(); });
                console.log('ECharts OK');
            }
        } catch(e) { console.error('ECharts:', e); }
        
        // 4. Plotly
        try {
            var plotlyEl = document.getElementById('plotly-scatter');
            if (plotlyEl && typeof Plotly !== 'undefined') {
                Plotly.newPlot(plotlyEl, [{
                    x: [1, 2, 3, 4, 5],
                    y: [1, 4, 9, 16, 25],
                    mode: 'lines+markers',
                    type: 'scatter',
                    marker: { color: '#8b5cf6', size: 10 }
                }], {
                    margin: { t: 30, l: 40, r: 20, b: 40 },
                    responsive: true
                });
                console.log('Plotly OK');
            }
        } catch(e) { console.error('Plotly:', e); }
        
        // 5. Google Charts
        // 6. PyEcharts (使用 PyEcharts 官方 CDN)
        try {
            var pyechartEl = document.getElementById('pyechart-demo');
            if (pyechartEl && typeof echarts !== 'undefined') {
                var pyChart = echarts.init(pyechartEl, 'white', {renderer: 'canvas'});
                pyChart.setOption({
                    title: { text: 'PyEcharts 风格柱状图', left: 'center' },
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: ['一月', '二月', '三月', '四月', '五月', '六月'] },
                    yAxis: { type: 'value' },
                    series: [{
                        name: '销售额',
                        type: 'bar',
                        data: [520, 630, 788, 600, 912, 745],
                        itemStyle: { color: '#5470c6' }
                    }]
                });
                window.addEventListener('resize', function() { pyChart.resize(); });
                console.log('PyEcharts OK');
            }
        } catch(e) { console.error('PyEcharts:', e); }
        
        // 7. Google Charts
        try {
            if (typeof google !== 'undefined' && google.charts) {
                google.charts.load('current', { packages: ['gauge'] });
                google.charts.setOnLoadCallback(function() {
                    var data = google.visualization.arrayToDataTable([
                        ['Label', 'Value'],
                        ['速度', 80],
                        ['温度', 55]
                    ]);
                    var chart = new google.visualization.Gauge(document.getElementById('google-gauge'));
                    chart.draw(data, { width: 300, height: 280 });
                    console.log('Google Charts OK');
                });
            }
        } catch(e) { console.error('Google Charts:', e); }
        
    }, 500);
});
</script>
