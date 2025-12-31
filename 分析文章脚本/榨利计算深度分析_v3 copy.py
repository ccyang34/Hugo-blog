#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榨利计算器 - Pyecharts 测试版
1. 引用原始版本稳定数据获取逻辑 (akshare + 元爬虫)
2. 使用 pyecharts 生成交互式 HTML 图表
3. 自动生成 Hugo Markdown 博客并嵌入 HTML 图表
4. 取消 DeepSeek AI 分析部分
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import requests
import time
import urllib3
import pytz

# Pyecharts 导入
from pyecharts.charts import Line, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# ================= 配置区域 =================
# Hugo 博客配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_STATIC_DIR = os.path.join(HUGO_BLOG_DIR, "static", "charts")

# 时区配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PyechartsTest:
    """Pyecharts 榨利图表测试器"""
    
    def __init__(self):
        """初始化"""
        # 压榨产出比例
        self.豆油产出率 = 0.185
        self.豆粕产出率 = 0.785
        self.压榨成本 = 150.0
        
        # 确保目录存在
        os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
        os.makedirs(HUGO_STATIC_DIR, exist_ok=True)
        self.输出目录 = os.path.join(SCRIPT_DIR, "blog")
        os.makedirs(self.输出目录, exist_ok=True)
        
        print("🚀 Pyecharts 榨利图表测试器初始化完成")

    # ================= 数据获取逻辑 =================

    def 获取豆二数据(self):
        """使用akshare获取豆二(B0)期货数据"""
        print("\n🌱 开始获取豆二(B0)期货数据...")
        try:
            豆二数据 = ak.futures_zh_daily_sina(symbol="B0")
            if 豆二数据.empty: return None
            
            豆二数据 = 豆二数据.rename(columns={
                'date': '日期', 'open': '开盘价', 'high': '最高价', 
                'low': '最低价', 'close': '收盘价', 'volume': '成交量',
                'hold': '持仓量', 'settle': '结算价'
            })
            
            豆二数据['豆二价格'] = 豆二数据['收盘价']
            豆二数据['日期'] = pd.to_datetime(豆二数据['日期'])
            return 豆二数据[['日期', '豆二价格', '结算价']]
            
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None

    def 获取元爬虫数据(self, 产品类型='Y'):
        """获取元爬虫数据"""
        产品映射 = {'Y': '豆油', 'M': '豆粕'}
        产品名称 = 产品映射.get(产品类型, '未知产品')
        print(f"📊 开始获取{产品名称}数据...")
        
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {'t': int(time.time() * 1000), 'type': 产品类型}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.jiaoyifamen.com/variety/varieties-varieties'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
            if response.status_code == 200:
                数据 = response.json()
                return self.解析元爬虫数据(数据, 产品类型)
            else:
                print(f"❌ {产品名称}数据请求失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 获取{产品名称}数据异常: {e}")
            return None

    def 解析元爬虫数据(self, 原始数据, 产品类型):
        """解析元爬虫数据"""
        if not 原始数据 or 'data' not in 原始数据: return None
        数据内容 = 原始数据['data']
        
        日期数据 = 数据内容.get('category')
        if 日期数据 is None:
            for k in 数据内容.keys():
                if 'category' in k.lower(): 日期数据 = 数据内容[k]; break
        
        价格数据, 基差数据 = None, None
        for k, v in 数据内容.items():
            if 'price' in k.lower() and 'value' in k.lower(): 价格数据 = v
            if 'basis' in k.lower() and 'value' in k.lower(): 基差数据 = v
            
        if not (日期数据 and 价格数据 and 基差数据): return None
        
        min_len = min(len(日期数据), len(价格数据), len(基差数据))
        产品数据 = pd.DataFrame({
            '日期': 日期数据[:min_len],
            '价格': 价格数据[:min_len],
            '基差': 基差数据[:min_len]
        })
        
        curr_year = datetime.now().year
        def try_parse_date(x):
            if isinstance(x, str) and '-' in x and len(x) <= 5:
                try: return pd.to_datetime(f"{curr_year}-{x}")
                except:
                    try: return pd.to_datetime(f"{curr_year-1}-{x}")
                    except: return pd.NaT
            return pd.to_datetime(x, errors='coerce')

        产品数据['日期'] = 产品数据['日期'].apply(try_parse_date)
        产品数据 = 产品数据.dropna(subset=['日期'])
        产品数据['价格'] = pd.to_numeric(产品数据['价格'], errors='coerce')
        产品数据['基差'] = pd.to_numeric(产品数据['基差'], errors='coerce')
        产品数据 = 产品数据.dropna()
        
        col_prefix = '豆油' if 产品类型 == 'Y' else '豆粕'
        return 产品数据.rename(columns={'价格': f'{col_prefix}价格', '基差': f'{col_prefix}基差'})

    def 合并并计算榨利(self, 豆油数据, 豆粕数据, 豆二数据):
        """合并数据并计算利润"""
        print("🔄 合并数据并计算榨利...")
        合并 = pd.merge(豆油数据, 豆粕数据, on='日期', how='inner')
        合并 = pd.merge(合并, 豆二数据, on='日期', how='inner')
        
        # 核心公式：含基差榨利
        合并['榨利'] = (
            (合并['豆油价格'] + 合并['豆油基差']) * self.豆油产出率 + 
            (合并['豆粕价格'] + 合并['豆粕基差']) * self.豆粕产出率 - 
            合并['豆二价格'] - self.压榨成本
        )
        # 盘面榨利：不含基差
        合并['盘面榨利'] = (
            合并['豆油价格'] * self.豆油产出率 + 
            合并['豆粕价格'] * self.豆粕产出率 - 
            合并['豆二价格'] - self.压榨成本
        )
        # 现货油粕比
        合并['现货油粕比'] = (合并['豆油价格'] + 合并['豆油基差']) / (合并['豆粕价格'] + 合并['豆粕基差'])
        # 豆油基差率
        合并['豆油基差率'] = 合并['豆油基差'] / 合并['豆油价格'] * 100
        合并['榨利率'] = (合并['榨利'] / 合并['豆二价格']) * 100
        return 合并

    # ================= Pyecharts 图表生成 =================

    def 生成pyecharts图表(self, 榨利数据, 天数=180):
        """使用 pyecharts 生成交互式榨利图表"""
        print(f"📊 使用 Pyecharts 生成交互式图表...")
        data = 榨利数据.tail(天数).copy() if 天数 < len(榨利数据) else 榨利数据.copy()
        
        # 准备数据
        日期列表 = data['日期'].dt.strftime('%Y-%m-%d').tolist()
        榨利列表 = [round(x, 2) for x in data['榨利'].tolist()]
        盘面榨利列表 = [round(x, 2) for x in data['盘面榨利'].tolist()]
        豆油价格列表 = [round(x, 2) for x in data['豆油价格'].tolist()]
        豆粕价格列表 = [round(x, 2) for x in data['豆粕价格'].tolist()]
        豆二价格列表 = [round(x, 2) for x in data['豆二价格'].tolist()]
        
        # 创建榨利走势图
        榨利图 = (
            Line(init_opts=opts.InitOpts(
                theme=ThemeType.MACARONS,
                width="100%",
                height="400px"
            ))
            .add_xaxis(日期列表)
            .add_yaxis(
                "现货榨利(含基差)",
                榨利列表,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2),
                label_opts=opts.LabelOpts(is_show=False),
                markpoint_opts=opts.MarkPointOpts(
                    data=[
                        opts.MarkPointItem(type_="max", name="最高"),
                        opts.MarkPointItem(type_="min", name="最低"),
                    ]
                ),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(y=0, name="盈亏平衡线")]
                ),
            )
            .add_yaxis(
                "盘面榨利(不含基差)",
                盘面榨利列表,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=1.5, type_="dashed"),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="大豆压榨利润走势",
                    subtitle=f"数据区间: {日期列表[0]} ~ {日期列表[-1]}"
                ),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(is_show=True, range_start=50, range_end=100),
                    opts.DataZoomOpts(type_="inside"),
                ],
                legend_opts=opts.LegendOpts(pos_top="5%"),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    name="元/吨",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
        )
        
        # 创建期货价格走势图
        价格图 = (
            Line(init_opts=opts.InitOpts(
                theme=ThemeType.MACARONS,
                width="100%",
                height="400px"
            ))
            .add_xaxis(日期列表)
            .add_yaxis(
                "豆油价格",
                豆油价格列表,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2, color="#FF6B6B"),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                "豆粕价格",
                豆粕价格列表,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=2, color="#4ECDC4"),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                "豆二价格",
                豆二价格列表,
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(width=1.5, type_="dashed", color="#45B7D1"),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="期货价格走势对比"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                datazoom_opts=[
                    opts.DataZoomOpts(is_show=True, range_start=50, range_end=100),
                    opts.DataZoomOpts(type_="inside"),
                ],
                legend_opts=opts.LegendOpts(pos_top="5%"),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    name="元/吨",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
        )
        
        # 保存为 HTML 文件
        榨利图文件名 = "pyecharts_margin.html"
        价格图文件名 = "pyecharts_price.html"
        
        榨利图.render(os.path.join(HUGO_STATIC_DIR, 榨利图文件名))
        价格图.render(os.path.join(HUGO_STATIC_DIR, 价格图文件名))
        
        # 同时保存到本地输出目录
        榨利图.render(os.path.join(self.输出目录, 榨利图文件名))
        价格图.render(os.path.join(self.输出目录, 价格图文件名))
        
        print(f"✅ Pyecharts 图表已生成: {榨利图文件名}, {价格图文件名}")
        return [榨利图文件名, 价格图文件名]

    def 生成博客(self, df, html文件列表):
        """生成 Hugo 博客文章，嵌入 Pyecharts HTML 图表"""
        print("📝 生成博客文章...")
        latest = df.iloc[-1]
        
        fixed_title = "Pyecharts测试"
        date_iso = datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        
        content = f"""---
title: "{fixed_title}"
date: {date_iso}
lastmod: {date_iso}
description: "使用 Pyecharts 生成交互式榨利图表的测试博客。"
draft: false
categories: ["技术测试"]
tags: ["Pyecharts", "可视化", "期货", "测试"]
---

## 📊 Pyecharts 交互式图表测试

本文使用 **Pyecharts** 生成交互式 HTML 图表，并嵌入 Hugo 博客进行展示测试。

### 数据快照

- **最新榨利**: `{latest['榨利']:.2f}` 元/吨
- **盘面榨利**: `{latest['盘面榨利']:.2f}` 元/吨
- **豆油价格**: `{latest['豆油价格']:.0f}` 元/吨
- **豆粕价格**: `{latest['豆粕价格']:.0f}` 元/吨
- **豆二价格**: `{latest['豆二价格']:.0f}` 元/吨

---

## � 榨利走势图

{{{{< rawhtml >}}}}
<iframe src="/charts/{html文件列表[0]}" width="100%" height="450px" frameborder="0" scrolling="no"></iframe>
{{{{< /rawhtml >}}}}

---

## 📈 期货价格走势图

{{{{< rawhtml >}}}}
<iframe src="/charts/{html文件列表[1]}" width="100%" height="450px" frameborder="0" scrolling="no"></iframe>
{{{{< /rawhtml >}}}}

---

## 🛠️ 技术说明

- **图表库**: Pyecharts (基于 Apache ECharts)
- **嵌入方式**: iframe 嵌入独立 HTML 文件
- **交互功能**: 支持缩放、拖拽、悬停提示等
- **更新时间**: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}
"""
        # 保存博客文件
        md_path = os.path.join(HUGO_CONTENT_DIR, "pyecharts测试.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        # 同时保存到本地输出目录
        with open(os.path.join(self.输出目录, "pyecharts测试.md"), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 博客文章已生成: {md_path}")

    def 启动(self):
        """执行完整工作流"""
        print("=" * 60)
        豆二 = self.获取豆二数据()
        豆油 = self.获取元爬虫数据('Y')
        豆粕 = self.获取元爬虫数据('M')
        
        if 豆二 is None or 豆油 is None or 豆粕 is None:
            print("❌ 数据获取不完整，任务终止")
            return
            
        df = self.合并并计算榨利(豆油, 豆粕, 豆二)
        
        # 生成 Pyecharts 图表
        html文件列表 = self.生成pyecharts图表(df, 180)
        
        # 生成博客
        self.生成博客(df, html文件列表)
        
        print("\n🎉 Pyecharts 测试工作流执行完毕！")
        print("=" * 60)


if __name__ == "__main__":
    PyechartsTest().启动()
