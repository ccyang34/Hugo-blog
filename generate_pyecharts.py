#!/usr/bin/env python3
"""生成 PyEcharts 图表并输出嵌入式 HTML"""
from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts

# 1. 柱状图
bar = Bar()
bar.add_xaxis(["一月", "二月", "三月", "四月", "五月", "六月"])
bar.add_yaxis("销售额", [520, 630, 788, 600, 912, 745])
bar.set_global_opts(title_opts=opts.TitleOpts(title="PyEcharts 柱状图"))

# 2. 折线图  
line = Line()
line.add_xaxis(["周一", "周二", "周三", "周四", "周五", "周六", "周日"])
line.add_yaxis("访问量", [820, 932, 901, 934, 1290, 1330, 1320])
line.set_global_opts(title_opts=opts.TitleOpts(title="PyEcharts 折线图"))

# 3. 饼图
pie = Pie()
pie.add("", [("A类", 335), ("B类", 310), ("C类", 234), ("D类", 135)])
pie.set_global_opts(title_opts=opts.TitleOpts(title="PyEcharts 饼图"))

# 输出嵌入式 HTML
print("<!-- PyEcharts 柱状图 -->")
print('<div id="pyechart-bar" style="width: 100%; height: 350px;"></div>')
print(bar.render_embed())

print("\n<!-- PyEcharts 折线图 -->")
print('<div id="pyechart-line" style="width: 100%; height: 350px;"></div>')
print(line.render_embed())

print("\n<!-- PyEcharts 饼图 -->")
print('<div id="pyechart-pie" style="width: 100%; height: 350px;"></div>')
print(pie.render_embed())
