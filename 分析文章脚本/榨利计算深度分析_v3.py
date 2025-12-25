#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榨利计算器 v3 - 深度分析增强版
1. 引用原始版本稳定数据获取逻辑 (akshare + 元爬虫)
2. 引用原始版本 3x1 详尽图表绘制逻辑
3. 集成 DeepSeek AI 深度分析
4. 自动生成 Hugo Markdown 博客并同步图片
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import os
import json
import requests
import time
import urllib3
import pytz

# ================= 配置区域 =================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-063857d175bd48038684520e7b6ec934")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Hugo 博客配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

# 时区配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class 榨利计算器V3:
    """榨利计算深度分析器 V3"""
    
    def __init__(self):
        """初始化"""
        # 设置中文字体，GitHub Actions 优先使用 Noto Sans CJK
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        # 压榨产出比例
        self.豆油产出率 = 0.185
        self.豆粕产出率 = 0.785
        self.压榨成本 = 150.0
        
        # 确保目录存在
        os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
        os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
        self.输出目录 = os.path.join(SCRIPT_DIR, "blog")
        os.makedirs(self.输出目录, exist_ok=True)
        
        print("🚀 榨利计算器V3 AI深度分析版初始化完成")

    # ================= 数据获取逻辑 (引用自 榨利计算器.py) =================

    def 获取豆二数据(self):
        """使用akshare获取豆二(B0)期货数据"""
        print("\n🌱 开始获取豆二(B0)期货数据...")
        try:
            # 获取豆二主力合约数据
            豆二数据 = ak.futures_zh_daily_sina(symbol="B0")
            if 豆二数据.empty: return None
            
            # 重命名列名为中文
            豆二数据 = 豆二数据.rename(columns={
                'date': '日期', 'open': '开盘价', 'high': '最高价', 
                'low': '最低价', 'close': '收盘价', 'volume': '成交量',
                'hold': '持仓量', 'settle': '结算价'
            })
            
            # 使用收盘价作为基础，结算价用于展示
            豆二数据['豆二价格'] = 豆二数据['收盘价']
            豆二数据['日期'] = pd.to_datetime(豆二数据['日期'])
            return 豆二数据[['日期', '豆二价格', '结算价']]
            
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None

    def 获取元爬虫数据(self, 产品类型='Y'):
        """引用原始稳健的元爬虫获取逻辑"""
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
        """引用原始稳健的数据解析逻辑"""
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
        
        # 转换日期，处理非闰年2-29等异常
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
        # 豆油基差率（基差/期货价格）
        合并['豆油基差率'] = 合并['豆油基差'] / 合并['豆油价格'] * 100  # 百分比
        合并['榨利率'] = (合并['榨利'] / 合并['豆二价格']) * 100
        return 合并

    # ================= 图表绘制逻辑 (基于原始 3x1 结构优化) =================

    def 绘制图表(self, 榨利数据, 天数, 名称):
        """绘制详尽的多周期图表"""
        print(f"📊 绘制{名称}走势图...")
        data = 榨利数据.tail(天数).copy() if 天数 < len(榨利数据) else 榨利数据.copy()
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14), dpi=100)
        最新日期 = data['日期'].max().strftime('%Y-%m-%d')
        
        # 1. 期货价格走势 (上图)
        ax1.plot(data['日期'], data['豆油价格'], color='darkorange', linestyle='-', label='豆油价格', linewidth=1.5)
        ax1.set_title(f'期货价格走势 (双轴) - {名称}', fontsize=14)
        ax1.set_ylabel('豆油价格(元/吨)', color='darkorange')
        ax1.tick_params(axis='y', labelcolor='darkorange')
        ax1.grid(True, alpha=0.3)
        
        ax1_r = ax1.twinx()
        ax1_r.plot(data['日期'], data['豆粕价格'], 'b-', label='豆粕价格', linewidth=1.5)
        ax1_r.plot(data['日期'], data['豆二价格'], 'g--', label='豆二价格', linewidth=1.5)
        ax1_r.set_ylabel('豆粕/豆二价格(元/吨)')
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_r.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        
        # 右上角显示最新数据日期
        ax1.text(0.99, 0.97, f'数据截止: {最新日期}', transform=ax1.transAxes, 
                 fontsize=9, ha='right', va='top', 
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))
        
        # 2. 基差走势 (中图) - 含现货油粕比面积图
        ax2.plot(data['日期'], data['豆油基差'], color='darkorange', linestyle='--', label='豆油基差', alpha=0.8)
        ax2.plot(data['日期'], data['豆粕基差'], 'b--', label='豆粕基差', alpha=0.8)
        ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_ylabel('基差(元/吨)')
        ax2.grid(True, alpha=0.3)
        
        # 右轴：现货油粕比面积图 + 豆油基差率折线
        ax2_r = ax2.twinx()
        ax2_r.fill_between(data['日期'], data['现货油粕比'].min() * 0.98, data['现货油粕比'], alpha=0.25, color='green', label='现货油粕比')
        ax2_r.plot(data['日期'], data['豆油基差率'], color='purple', linestyle='-', linewidth=1.5, label='豆油基差率(%)')
        ax2_r.set_ylabel('油粕比 / 基差率(%)', color='green')
        ax2_r.tick_params(axis='y', labelcolor='green')
        
        # 合并图例
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_r.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        ax2.set_title(f'基差走势 & 油粕比 - 最新油粕比: {data["现货油粕比"].iloc[-1]:.3f} | 基差率: {data["豆油基差率"].iloc[-1]:.1f}%', fontsize=12)
        
        # 3. 榨利走势 (下图) - 含盘面榨利面积图
        # 盘面榨利面积图（不含基差）
        ax3.fill_between(data['日期'], 0, data['盘面榨利'], alpha=0.3, color='orange', label='盘面榨利(不含基差)')
        # 含基差榨利折线
        ax3.plot(data['日期'], data['榨利'], color='purple', label='现货榨利(含基差)', linewidth=2)
        ax3.axhline(0, color='red', linestyle='-', alpha=0.6, label='盈亏平衡')
        
        # 标注含基差榨利最值
        max_v, min_v = data['榨利'].max(), data['榨利'].min()
        max_d = data.loc[data['榨利'].idxmax(), '日期']
        min_d = data.loc[data['榨利'].idxmin(), '日期']
        ax3.annotate(f'最高: {max_v:.0f}', xy=(max_d, max_v), xytext=(0, 10), textcoords='offset points', ha='center', color='purple', fontsize=8)
        ax3.annotate(f'最低: {min_v:.0f}', xy=(min_d, min_v), xytext=(0, -20), textcoords='offset points', ha='center', color='purple', fontsize=8)
        
        ax3.set_title(f'大豆压榨利润走势 - 现货榨利: {data["榨利"].iloc[-1]:.2f} | 盘面榨利: {data["盘面榨利"].iloc[-1]:.2f}', fontsize=14)
        ax3.set_ylabel('榨利(元/吨)')
        ax3.legend(loc='upper left', fontsize=9)
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        文件名 = f"margin_chart_{名称}.png"
        plt.savefig(os.path.join(HUGO_IMAGES_DIR, 文件名))
        plt.savefig(os.path.join(self.输出目录, 文件名))
        plt.close()
        return 文件名

    # ================= AI 分析与博客生成逻辑 =================

    def 深度分析(self, 榨利数据):
        """调用 DeepSeek AI 分析半年数据"""
        print("🤖 启动 AI 深度解读...")
        data = 榨利数据.tail(180)
        curr = data.iloc[-1]
        stats = {
            'latest': curr['榨利'], 'avg': data['榨利'].mean(),
            'max': data['榨利'].max(), 'min': data['榨利'].min(),
            'win_rate': (len(data[data['榨利'] > 0]) / len(data)) * 100,
            'y_basis': curr['豆油基差'], 'm_basis': curr['豆粕基差']
        }
        
        prompt = f"""
你是一位资深的期货分析师，请根据以下数据对大豆压榨利润进行深度点评：
1. 当前榨利: {stats['latest']:.2f} 元/吨 (半年均值: {stats['avg']:.2f}, 最值区间: [{stats['min']:.0f}, {stats['max']:.0f}])
2. 半年胜率: {stats['win_rate']:.1f}%
3. 最新基差: 豆油 {stats['y_basis']} / 豆粕 {stats['m_basis']}

要求：
- 分析当前利润在历史周期中的位置。
- 说明当前高/低基差如何影响油厂利润策略。
- 针对豆油下游生产商需求，基于当前的基差与价格水平，给出具体的现货采购决策及期货买入/套保建议。
- 给出短期持仓或企业避险建议。
- 保持专业、犀利、结构化。

**重要格式要求**：直接输出纯 Markdown 文本，禁止使用 ```markdown 或任何代码块包裹整篇文章。
"""
        try:
            headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "system", "content": "你是一个资深大宗商品研究员。"}, {"role": "user", "content": prompt}]
            }
            res = requests.post(DEEPSEEK_BASE_URL + "/chat/completions", headers=headers, json=payload, timeout=60)
            return res.json()['choices'][0]['message']['content']
        except:
            return "AI 分析连接超时，请关注盘面基差变化。"

    def 生成报告(self, df, 文件名列表):
        """生成最终 Hugo 博客文章"""
        print("📝 整合报告中...")
        latest = df.iloc[-1]
        date_str = latest['日期'].strftime('%Y-%m-%d')
        ai_text = self.深度分析(df)
        
        content = f"""---
title: "大豆榨利深度分析报告"
date: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')}
lastmod: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')}
description: "自动化生成的压榨利润深度报告，引用原始版本高精绘图和 DeepSeek AI 逻辑。"
draft: false
categories: ["榨利深度分析"]
tags: ["大豆", "豆油", "豆粕", "期货", "可视化"]
image: ../../images/charts/{文件名列表[0]}
---

## 🛰️ 数据核心快照

- **最新榨利**: `{latest['榨利']:.2f}` 元/吨 (压榨成本：{self.压榨成本})
- **基差详情**: 豆油 `{latest['豆油基差']:.0f}` | 豆粕 `{latest['豆粕基差']:.0f}`

---

## 🤖 AI 首席分析师解读

{ai_text}

---

## 📈 多维度走势分析

### 近半年明细 (高精度)
![半年走势](../../images/charts/{文件名列表[0]})

### 近一年对比
![一年走势](../../images/charts/{文件名列表[1]})

### 近两年对比
![两年走势](../../images/charts/{文件名列表[2]})

### 全历史周期
展现大周期的榨利轮回。
![全历史走势](../../images/charts/{文件名列表[3]})

---

## 🛠️ 计算说明
> 榨利 = (豆油现货价格 × 18.5% + 豆粕现货价格 × 78.5%) - 豆二价格 - {self.压榨成本}
> 数据源：交易法门(基差) / Akshare(期货)
> 更新时间：{datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}
"""
        # 保存固定文件名的博客
        md_path = os.path.join(HUGO_CONTENT_DIR, "榨利深度分析报告.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        # 同时也保存到本地输出目录
        with open(os.path.join(self.输出目录, "榨利深度分析报告.md"), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 深度报告已更新: {md_path}")

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
        
        # 绘图顺序：半年、一年、两年、全历史
        imgs = []
        imgs.append(self.绘制图表(df, 180, "半年"))
        imgs.append(self.绘制图表(df, 365, "一年"))
        imgs.append(self.绘制图表(df, 730, "两年"))
        imgs.append(self.绘制图表(df, 9999, "全历史"))
        
        self.生成报告(df, imgs)
        print("\n🎉 榨利深度分析 V3 工作流执行完毕！")
        print("=" * 60)

if __name__ == "__main__":
    榨利计算器V3().启动()
