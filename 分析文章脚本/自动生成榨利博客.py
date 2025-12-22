#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成榨利博客 - 基于榨利计算器，生成半年全数据图表并发布为Hugo博客
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
import os
import shutil
import json
import requests
import time

class 榨利博客生成器:
    """榨利分析与博客生成器"""
    
    def __init__(self):
        """初始化"""
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 压榨参数
        self.豆油产出率 = 0.185
        self.豆粕产出率 = 0.785
        self.压榨成本 = 150.0
        
        # 路径配置
        self.博客根目录 = "/Users/ccy/Hugo-blog"
        self.图片存储路径 = os.path.join(self.博客根目录, "static/img/charts")
        self.文章存储路径 = os.path.join(self.博客根目录, "content/posts")
        
        # 确保目录存在
        os.makedirs(self.图片存储路径, exist_ok=True)
        os.makedirs(self.文章存储路径, exist_ok=True)
        
        print("🚀 博客生成器初始化完成")

    def 获取数据(self):
        """获取并处理所有必要数据 (复用原逻辑)"""
        print("\n📡 开始获取数据...")
        
        # 1. 获取豆二数据 (Akshare)
        try:
            豆二数据 = ak.futures_zh_daily_sina(symbol="B0")
            豆二数据 = 豆二数据.rename(columns={'date': '日期', 'close': '豆二价格'})
            豆二数据['日期'] = pd.to_datetime(豆二数据['日期'])
            豆二数据 = 豆二数据[['日期', '豆二价格']]
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None

        # 2. 获取豆油豆粕数据 (元爬虫)
        def 获取元数据(类型, 名称):
            url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
            params = {'t': int(time.time() * 1000), 'type': 类型}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                res = requests.get(url, params=params, headers=headers, verify=False, timeout=30)
                data = res.json().get('data', {})
                
                # 解析逻辑简化版
                date_col = next((k for k in data.keys() if 'category' in k.lower()), None)
                price_col = next((k for k in data.keys() if 'price' in k.lower() and 'value' in k.lower()), None)
                basis_col = next((k for k in data.keys() if 'basis' in k.lower() and 'value' in k.lower()), None)
                
                if not (date_col and price_col and basis_col): return None
                
                df = pd.DataFrame({
                    '日期': data[date_col],
                    f'{名称}价格': data[price_col],
                    f'{名称}基差': data[basis_col]
                })
                
                # 日期处理
                当前年份 = datetime.now().year
                df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(f"{当前年份}-{x}") if '-' in str(x) and len(str(x)) <= 5 else pd.to_datetime(x))
                
                # 数据清洗
                cols = [f'{名称}价格', f'{名称}基差']
                df[cols] = df[cols].replace({'': np.nan, 0: np.nan}).astype(float)
                return df.dropna()
            except Exception as e:
                print(f"❌ 获取{名称}数据失败: {e}")
                return None

        豆油数据 = 获取元数据('Y', '豆油')
        豆粕数据 = 获取元数据('M', '豆粕')
        
        if 豆油数据 is None or 豆粕数据 is None: return None
        
        # 3. 合并数据
        print("🔄 合并数据中...")
        合并 = pd.merge(豆油数据, 豆粕数据, on='日期', how='inner')
        合并 = pd.merge(合并, 豆二数据, on='日期', how='inner')
        
        # 4. 计算榨利
        print("🧮 计算榨利指标...")
        合并['榨利'] = (
            (合并['豆油价格'] + 合并['豆油基差']) * self.豆油产出率 + 
            (合并['豆粕价格'] + 合并['豆粕基差']) * self.豆粕产出率 - 
            合并['豆二价格'] - self.压榨成本
        )
        合并['榨利率'] = (合并['榨利'] / 合并['豆二价格']) * 100
        
        return 合并

    def 绘制半年图表(self, 数据):
        """只绘制半年全数据图表"""
        print("\n🎨 绘制半年走势图...")
        
        # 筛选半年数据
        截止日期 = 数据['日期'].max()
        起始日期 = 截止日期 - timedelta(days=180)
        区间数据 = 数据[数据['日期'] >= 起始日期].copy()
        
        if 区间数据.empty:
            print("❌ 数据不足，无法绘图")
            return None
            
        时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        文件名 = f"margin_analysis_halfyear_{时间戳}.png"
        保存路径 = os.path.join(self.图片存储路径, 文件名)
        
        # 绘图逻辑 (复用原有的 3x1 布局)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))
        
        # 1. 价格
        ax1.plot(区间数据['日期'], 区间数据['豆油价格'], 'r-', label='豆油价格', linewidth=1.5)
        ax1.set_ylabel('豆油价格', color='r')
        ax1.tick_params(axis='y', labelcolor='r')
        ax1.grid(True, alpha=0.3)
        
        ax1_r = ax1.twinx()
        ax1_r.plot(区间数据['日期'], 区间数据['豆粕价格'], 'b-', label='豆粕价格', linewidth=1.5)
        ax1_r.plot(区间数据['日期'], 区间数据['豆二价格'], 'g-', label='豆二价格', linewidth=1.5)
        ax1_r.set_ylabel('豆粕/豆二价格')
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_r.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        ax1.set_title('近半年期货价格走势', fontsize=12)
        
        # 2. 基差
        ax2.plot(区间数据['日期'], 区间数据['豆油基差'], 'r-', label='豆油基差')
        ax2.plot(区间数据['日期'], 区间数据['豆粕基差'], 'b-', label='豆粕基差')
        ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax2.legend(loc='upper left')
        ax2.set_title('近半年基差走势', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # 3. 榨利
        ax3.plot(区间数据['日期'], 区间数据['榨利'], color='purple', label='盘面榨利', linewidth=2)
        ax3.axhline(0, color='red', linestyle='--', alpha=0.5, label='盈亏平衡')
        
        # 标注最值
        max_idx = 区间数据['榨利'].idxmax()
        min_idx = 区间数据['榨利'].idxmin()
        ax3.annotate(f"最高: {区间数据.loc[max_idx, '榨利']:.0f}", 
                    xy=(区间数据.loc[max_idx, '日期'], 区间数据.loc[max_idx, '榨利']),
                    xytext=(0, 10), textcoords='offset points', ha='center', color='purple')
        ax3.annotate(f"最低: {区间数据.loc[min_idx, '榨利']:.0f}", 
                    xy=(区间数据.loc[min_idx, '日期'], 区间数据.loc[min_idx, '榨利']),
                    xytext=(0, -15), textcoords='offset points', ha='center', color='purple')
        
        ax3.legend(loc='upper left')
        ax3.set_title('近半年榨利走势', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(保存路径, dpi=100)
        plt.close()
        
        print(f"✅ 图表已保存: {保存路径}")
        return 文件名, 区间数据

    def 生成博客文章(self, 图片文件名, 区间数据):
        """生成 Hugo Markdown 文章"""
        print("\n📝 生成博客文章...")
        
        当前时间 = datetime.now()
        日期字符串 = 当前时间.strftime("%Y-%m-%d")
        时间字符串 = 当前时间.strftime("%Y-%m-%d %H:%M")
        文件时间戳 = 当前时间.strftime("%Y%m%d_%H%M%S")
        
        # 统计数据
        最新数据 = 区间数据.iloc[-1]
        平均榨利 = 区间数据['榨利'].mean()
        盈利天数 = len(区间数据[区间数据['榨利'] > 0])
        总天数 = len(区间数据)
        盈利比例 = (盈利天数 / 总天数) * 100
        
        # 文章内容
        内容 = f"""---
title: "豆油压榨利润深度分析报告 ({日期字符串})"
date: {当前时间.strftime("%Y-%m-%d %H:%M")}
image: img/charts/{图片文件名}
description: "基于最近半年数据的豆油压榨利润深度分析，包含价格、基差及榨利走势的详细图表。"
categories:
    - 市场分析
tags:
    - 豆油
    - 榨利
    - 数据可视化
---

## 摘要

截至 **{最新数据['日期'].strftime('%Y-%m-%d')}**，豆油压榨利润分析如下：

- **最新榨利**: {最新数据['榨利']:.2f} 元/吨
- **半年平均**: {平均榨利:.2f} 元/吨
- **盈利概率**: {盈利比例:.1f}% ({盈利天数}/{总天数} 天)

## 走势分析图表

下图展示了最近半年的期货价格、现货基差以及盘面榨利的综合走势：

![榨利分析图表](/img/charts/{图片文件名})

## 详细数据解读

### 1. 价格端
- **豆油价格**: {最新数据['豆油价格']:.0f} 元/吨
- **豆粕价格**: {最新数据['豆粕价格']:.0f} 元/吨
- **豆二价格**: {最新数据['豆二价格']:.0f} 元/吨

### 2. 基差端
- **豆油基差**: {最新数据['豆油基差']:.0f} 元/吨
- **豆粕基差**: {最新数据['豆粕基差']:.0f} 元/吨

### 3. 利润端
当前盘面榨利为 **{最新数据['榨利']:.2f}** 元/吨，
相较于半年度平均水平 ({平均榨利:.2f})，
当前处于 **{'高于' if 最新数据['榨利'] > 平均榨利 else '低于'}** 平均水平的位置。

> 数据来源：新浪财经 (期货)、交易法门 (基差)
> 自动生成时间：{时间字符串}
"""
        
        文件名 = f"soy-oil-margin-analysis-{文件时间戳}.md"
        完整路径 = os.path.join(self.文章存储路径, 文件名)
        
        with open(完整路径, 'w', encoding='utf-8') as f:
            f.write(内容)
            
        print(f"✅ 博客文章已生成: {完整路径}")
        return 完整路径

    def 运行(self):
        """主运行流程"""
        数据 = self.获取数据()
        if 数据 is not None:
            结果 = self.绘制半年图表(数据)
            if 结果:
                文件名, 区间数据 = 结果
                self.生成博客文章(文件名, 区间数据)

if __name__ == "__main__":
    app = 榨利博客生成器()
    app.运行()
