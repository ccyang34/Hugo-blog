#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三大油脂（豆、棕、菜）量价一体化智能监测系统 v3.0
功能：
1. 实时抓取 Y0, P0, OI0 今日行情并给出采购指令
2. 自动生成最近五年（2021-至今）的实战买点全景图
3. 自动生成 Hugo 博客 Markdown 文章
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
import os

warnings.filterwarnings('ignore')

# 适配字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'Heiti SC']
plt.rcParams['axes.unicode_minus'] = False

SYMBOLS = {
    'Y0': '豆油',
    'P0': '棕榈油',
    'OI0': '菜油'
}

# 🎨 各品种风格配置：(折线颜色, 战略色, 战术色, 文字背景色)
STYLE_CONFIG = {
    'Y0':  {'line': '#1976D2', 'strat': '#0D47A1', 'tact': '#42A5F5', 'bg': '#E3F2FD'}, # 蓝色系-豆油
    'P0':  {'line': '#E65100', 'strat': '#BF360C', 'tact': '#FB8C00', 'bg': '#FFF3E0'}, # 橙色系-棕榈油
    'OI0': {'line': '#2E7D32', 'strat': '#1B5E20', 'tact': '#66BB6A', 'bg': '#E8F5E9'}  # 绿色系-菜油
}

def 核心信号决策引擎(df):
# ... (逻辑保持不变)
    return df

def 生成长周期报表(df_result, symbol, name):
    """
    生成最近五年的长图
    """
    print(f"\n🎨 正在绘制{name}({symbol})历史五年实战拆解对照图...")
    style = STYLE_CONFIG.get(symbol, {'line': '#90A4AE', 'strat': '#7B1FA2', 'tact': '#D32F2F', 'bg': 'white'})
    
    today = datetime.now()
    years = [today.year - 4, today.year - 3, today.year - 2, today.year - 1, today.year]
    
    fig, axes = plt.subplots(len(years), 1, figsize=(16, 28))
    title = f'{name}主力 {symbol} 战略采购五年全景图 ({years[0]}-{years[-1]})'
    fig.suptitle(title, fontsize=24, fontweight='bold', y=0.99, color=style['line'])

    for i, year in enumerate(years):
        ax = axes[i]
        d_y = df_result[df_result['date'].dt.year == year]
        if d_y.empty: continue
        
        ax.plot(d_y['date'], d_y['close'], color=style['line'], alpha=0.7, linewidth=1.5, label='收盘价')
        
        # 月度分割线
        for month in range(1, 13):
            try:
                m_sep = datetime(year, month, 1)
                ax.axvline(m_sep, color='#212121', linestyle='-', linewidth=1.2, alpha=0.2)
                ax.text(m_sep, ax.get_ylim()[1], f' {month}月', fontweight='bold', alpha=0.4, fontsize=10)
            except:
                continue

        # 信号点标注
        buys = d_y[d_y['is_buy']]
        ax.scatter(buys[buys['weight'] == 6.0]['date'], buys[buys['weight'] == 6.0]['close'], color=style['strat'], marker='D', s=160, label='战略(6x)', zorder=10)
        ax.scatter(buys[buys['weight'] == 3.0]['date'], buys[buys['weight'] == 3.0]['close'], color=style['tact'], marker='^', s=130, label='战术(3x)', zorder=10)
        ax.scatter(buys[buys['weight'] == 1.0]['date'], buys[buys['weight'] == 1.0]['close'], color='#455A64', marker='o', s=100, label='保底(1x)', zorder=10)

        ax.set_title(f'🚀 {year}年度 实战部署节点', fontsize=18, fontweight='bold', loc='left')
        ax.grid(True, axis='y', alpha=0.1)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.legend(loc='upper right', fontsize=11)
        
        y_m = d_y['close'].mean()
        y_s = (d_y['close'] * d_y['weight']).sum() / d_y['weight'].sum()
        ax.text(0.015, 0.05, f"年度结算：比市场平均采购价节省 {y_m - y_s:.1f} 元/吨", transform=ax.transAxes, 
                fontsize=15, fontweight='bold', color=style['strat'], bbox=dict(boxstyle='round,pad=0.5', facecolor=style['bg'], edgecolor=style['line'], alpha=0.9))

    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        
    img_name = f'oil_analysis_{symbol}.png'
    save_path = os.path.join(static_dir, img_name)
    plt.savefig(save_path, dpi=120)
    plt.close() 
    print(f"✅ 图片已导出：{save_path}")
    return img_name

def 生成年度汇总对比图(all_results):
    """
    将所有品种当年的监测图合并为一张图
    """
    today = datetime.now()
    year = today.year
    print(f"\n🎨 正在绘制 {year} 年度三大油脂实战部署汇总图...")
    
    fig, axes = plt.subplots(len(all_results), 1, figsize=(16, 6 * len(all_results)))
    title = f'三大油脂 {year} 年度战略采购实战汇总图'
    fig.suptitle(title, fontsize=22, fontweight='bold', y=0.98)

    for i, res in enumerate(all_results):
        ax = axes[i]
        symbol = res['symbol']
        style = STYLE_CONFIG.get(symbol, {'line': '#90A4AE', 'strat': '#7B1FA2', 'tact': '#D32F2F', 'bg': 'white'})
        df_result = res['df_result']
        d_y = df_result[df_result['date'].dt.year == year]
        if d_y.empty: continue
        
        ax.plot(d_y['date'], d_y['close'], color=style['line'], alpha=0.7, linewidth=1.5, label='收盘价')
        
        # 月度分割线
        for month in range(1, 13):
            try:
                m_sep = datetime(year, month, 1)
                ax.axvline(m_sep, color='#212121', linestyle='-', linewidth=1.5, alpha=0.2)
                ax.text(m_sep, ax.get_ylim()[1], f' {month}月', fontweight='bold', alpha=0.4, fontsize=10)
            except:
                continue

        # 信号点标注
        buys = d_y[d_y['is_buy']]
        ax.scatter(buys[buys['weight'] == 6.0]['date'], buys[buys['weight'] == 6.0]['close'], color=style['strat'], marker='D', s=140, label='战略(6x)', zorder=10)
        ax.scatter(buys[buys['weight'] == 3.0]['date'], buys[buys['weight'] == 3.0]['close'], color=style['tact'], marker='^', s=110, label='战术(3x)', zorder=10)
        ax.scatter(buys[buys['weight'] == 1.0]['date'], buys[buys['weight'] == 1.0]['close'], color='#455A64', marker='o', s=80, label='保底(1x)', zorder=10)

        ax.set_title(f'📊 {res["name"]} ({res["symbol"]})', fontsize=16, fontweight='bold', loc='left', color=style['line'])
        ax.grid(True, axis='y', alpha=0.1)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.legend(loc='upper right', fontsize=10)
        
        y_m = d_y['close'].mean()
        y_s = (d_y['close'] * d_y['weight']).sum() / d_y['weight'].sum()
        ax.text(0.015, 0.05, f"年度结算：节省 {y_m - y_s:.1f} 元/吨", transform=ax.transAxes, 
                fontsize=13, fontweight='bold', color=style['strat'], bbox=dict(boxstyle='round,pad=0.4', facecolor=style['bg'], edgecolor=style['line'], alpha=0.8))

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    img_name = f'oil_analysis_summary_{year}.png'
    save_path = os.path.join(static_dir, img_name)
    plt.savefig(save_path, dpi=120)
    plt.close()
    print(f"✅ 年度汇总图已导出：{save_path}")
    return img_name

def 生成Hugo博客(results, summary_img):
    today_str = datetime.now().strftime('%Y-%m-%d')
    title = "三大油脂（豆棕菜）买入节点分析追踪图"
    
    content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
tags: ["油脂", "策略", "买入节点", "期货"]
categories: ["市场分析"]
---

## 🚀 年度实战部署总览 ({datetime.now().year}年)

以下是豆、棕、菜三大油脂当年的信号触发及采购成本优化汇总情况：

![三大油脂年度汇总对比图](/images/{summary_img})

---

## 📈 三大油脂实时监测快照 ({today_str})

本系统基于最近五年历史回测，自动生成今日作战指令。

| 品种 | 当前价格 | 月内乖离率 | 建议动作 | 权重 | 决策依据 |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for res in results:
        latest = res['latest']
        action = "💡 发现买点" if latest['is_buy'] else "🧤 暂无信号"
        content += f"| {res['name']} | {latest['close']:.0f} | {latest['bias']:.2f}% | {action} | {latest['weight']}x | {latest['reason'] if latest['reason'] else '保持底仓'} |\n"

    content += "\n--- \n\n## 🔍 历史实战复盘全景图 (最近5年)\n\n"
    
    for res in results:
        content += f"### 📊 {res['name']} ({res['symbol']})\n"
        content += f"![{res['name']}五年复盘图](/images/{res['img_name']})\n\n"

    # 保存文章
    posts_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts')
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
        
    post_filename = "三大油脂（豆棕菜）买入节点分析追踪图.md"
    post_path = os.path.join(posts_dir, post_filename)
    
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"🚀 Hugo 博客文章已生成：{post_path}")

def 启动监测():
    print("="*65)
    print(f"📡 三大油脂智能监测系统 | 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*65)
    
    all_results = []
    
    for symbol, name in SYMBOLS.items():
        try:
            print(f"\n>>> 正在拉取 {name}({symbol}) 行情数据...")
            df_raw = ak.futures_main_sina(symbol=symbol)
            df = df_raw[['日期', '收盘价']].rename(columns={'日期':'date', '收盘价':'close'})
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            df_result = 核心信号决策引擎(df)
            img_name = 生成长周期报表(df_result, symbol, name)
            
            latest = df_result.iloc[-1]
            all_results.append({
                'symbol': symbol,
                'name': name,
                'latest': latest,
                'img_name': img_name,
                'df_result': df_result
            })
            
            print(f"[{name}] 当前价格: {latest['close']:.0f} | 乖离率: {latest['bias']:.2f}% | 信号: {'YES' if latest['is_buy'] else 'NO'}")
                    
        except Exception as e:
            print(f"❌ {name}({symbol}) 运行失败: {e}")
    
    if all_results:
        summary_img = 生成年度汇总对比图(all_results)
        生成Hugo博客(all_results, summary_img)
    
    print("\n" + "="*65)

if __name__ == "__main__":
    启动监测()