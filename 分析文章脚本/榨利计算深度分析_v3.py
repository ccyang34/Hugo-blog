#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榨利计算器 v3 - 升级版
1. 移除 CSV 保存逻辑
2. 图表与博客生成统一在 blog 目录下
3. 生成支持 Hugo 的 Markdown 文档
4. 集成 DeepSeek AI 深度分析
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import requests
import time
import urllib3
import pytz
import json

# ================= 配置区域 =================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-063857d175bd48038684520e7b6ec934")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# Hugo 博客配置
# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR) # 假设脚本在 Hugo-blog/分析文章脚本，上级是 Hugo-blog
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "img", "charts")

# 时区配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class 榨利计算器V3:
    """榨利计算器V3类"""
    
    def __init__(self):
        """初始化"""
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = [
            'SimHei', 'Microsoft YaHei', 'SimSun', 'STHeiti', 'PingFang SC', 'Arial Unicode MS'
        ]
        plt.rcParams['axes.unicode_minus'] = False
        
        # 压榨参数
        self.豆油产出率 = 0.185
        self.豆粕产出率 = 0.785
        self.压榨成本 = 150.0
        
        # 确保目录存在
        os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
        os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
        # 本地备份目录
        self.输出目录 = os.path.join(SCRIPT_DIR, "blog")
        os.makedirs(self.输出目录, exist_ok=True)
        
        print(f"🚀 榨利计算器V3 AI版初始化完成")
        print(f"📂 内容目录: {HUGO_CONTENT_DIR}")
        print(f"📂 图片目录: {HUGO_IMAGES_DIR}")

    def 获取豆二数据(self):
        """获取豆二(B0)期货数据"""
        print("🌱 获取豆二数据...")
        try:
            df = ak.futures_zh_daily_sina(symbol="B0")
            if df.empty: return None
            df = df.rename(columns={'date': '日期', 'settle': '豆二价格'})
            df['日期'] = pd.to_datetime(df['日期'])
            return df[['日期', '豆二价格']]
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None

    def 获取元数据(self, 类型, 名称):
        """使用元爬虫获取数据"""
        print(f"📊 获取{名称}数据...")
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {'t': int(time.time() * 1000), 'type': 类型}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        
        try:
            res = requests.get(url, params=params, headers=headers, verify=False, timeout=30)
            data = res.json().get('data', {})
            
            date_col = next((k for k in data.keys() if 'category' in k.lower()), None)
            price_col = next((k for k in data.keys() if 'price' in k.lower() and 'value' in k.lower()), None)
            basis_col = next((k for k in data.keys() if 'basis' in k.lower() and 'value' in k.lower()), None)
            
            if not (date_col and price_col and basis_col): return None
            
            dates, prices, basis = data[date_col], data[price_col], data[basis_col]
            min_len = min(len(dates), len(prices), len(basis))
            
            df = pd.DataFrame({
                '日期': dates[:min_len],
                f'{名称}价格': prices[:min_len],
                f'{名称}基差': basis[:min_len]
            })
            
            curr_year = datetime.now().year
            def try_parse_date(x):
                if '-' in str(x) and len(str(x)) <= 5:
                    try: return pd.to_datetime(f"{curr_year}-{x}")
                    except:
                        try: return pd.to_datetime(f"{curr_year-1}-{x}")
                        except: return pd.NaT
                return pd.to_datetime(x, errors='coerce')

            df['日期'] = df['日期'].apply(try_parse_date)
            df = df.dropna(subset=['日期'])
            df[f'{名称}价格'] = pd.to_numeric(df[f'{名称}价格'], errors='coerce')
            df[f'{名称}基差'] = pd.to_numeric(df[f'{名称}基差'], errors='coerce')
            return df.dropna()
        except Exception as e:
            print(f"❌ 获取{名称}数据异常: {e}")
            return None

    def 绘制图表(self, df, 天数, 名称):
        """统一绘图函数"""
        print(f"🎨 绘制{名称}走势图...")
        data = df.tail(天数).copy() if 天数 < len(df) else df.copy()
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14), dpi=100)
        
        ax1.plot(data['日期'], data['豆油价格'], 'r-', label='豆油价格', linewidth=1.5)
        ax1.set_ylabel('豆油价格', color='r')
        ax1.tick_params(axis='y', labelcolor='r')
        ax1.grid(True, alpha=0.3)
        ax1_r = ax1.twinx()
        ax1_r.plot(data['日期'], data['豆粕价格'], 'b-', label='豆粕价格', linewidth=1.5)
        ax1_r.plot(data['日期'], data['豆二价格'], 'g-', label='豆二价格', linewidth=1.5)
        ax1_r.set_ylabel('豆粕/豆二价格')
        ax1.set_title(f'大豆压榨相关品种价格走势 ({名称})', fontsize=14)
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_r.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        ax2.plot(data['日期'], data['豆油基差'], 'r--', label='豆油基差')
        ax2.plot(data['日期'], data['豆粕基差'], 'b--', label='豆粕基差')
        ax2.axhline(0, color='black', alpha=0.3)
        ax2.set_title(f'品种基差走势 ({名称})', fontsize=12)
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(data['日期'], data['榨利'], color='purple', label='盘面榨利', linewidth=2)
        ax3.axhline(0, color='red', linestyle='--', alpha=0.6, label='盈亏平衡')
        max_v, min_v = data['榨利'].max(), data['榨利'].min()
        max_d = data.loc[data['榨利'].idxmax(), '日期']
        min_d = data.loc[data['榨利'].idxmin(), '日期']
        ax3.annotate(f'最高: {max_v:.0f}', xy=(max_d, max_v), xytext=(0, 10), textcoords='offset points', ha='center', color='purple')
        ax3.annotate(f'最低: {min_v:.0f}', xy=(min_d, min_v), xytext=(0, -20), textcoords='offset points', ha='center', color='purple')
        ax3.set_title(f'压榨利润(榨利)走势 ({名称})', fontsize=14)
        ax3.legend(loc='upper left')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        文件名 = f"margin_chart_{名称}_{datetime.now().strftime('%Y%m%d')}.png"
        # 同时保存到博客目录和备份目录
        plt.savefig(os.path.join(HUGO_IMAGES_DIR, 文件名))
        plt.savefig(os.path.join(self.输出目录, 文件名))
        plt.close()
        return 文件名

    def 调用DeepSeek分析(self, df_half_year):
        """调用 DeepSeek API 进行深度分析"""
        print("🤖 正在调用 DeepSeek 进行深度分析...")
        
        # 准备数据摘要
        latest = df_half_year.iloc[-1]
        stats = {
            'avg_margin': df_half_year['榨利'].mean(),
            'max_margin': df_half_year['榨利'].max(),
            'min_margin': df_half_year['榨利'].min(),
            'latest_margin': latest['榨利'],
            'win_days': len(df_half_year[df_half_year['榨利'] > 0]),
            'total_days': len(df_half_year),
            'latest_y_basis': latest['豆油基差'],
            'latest_m_basis': latest['豆粕基差']
        }
        
        # 构建提示词
        prompt = f"""
你是一位资深的农产品期货分析师，请根据以下近半年的大豆压榨利润（榨利）数据进行深度分析：

1. **核心指标**:
   - 最新榨利: {stats['latest_margin']:.2f} 元/吨
   - 半年平均榨利: {stats['avg_margin']:.2f} 元/吨
   - 半年最高榨利: {stats['max_margin']:.2f} 元/吨
   - 半年最低榨利: {stats['min_margin']:.2f} 元/吨
   - 盈利天数占比: {stats['win_days']}/{stats['total_days']} ({(stats['win_days']/stats['total_days']*100):.1f}%)

2. **最新基差状态**:
   - 豆油基差: {stats['latest_y_basis']:.0f} 元/吨
   - 豆粕基差: {stats['latest_m_basis']:.0f} 元/吨

请根据以上数据给出 3-5 段深度解读，包括：
- 当前榨利水平在历史区间的位置评价。
- 基差变动对当前榨利的影响分析。
- 对未来短期压榨利润走势的预测与建议。
- 风险提示。

请直接返回 Markdown 格式的分析内容，不要包含任何自我介绍或多余的解释。
"""
        
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的期货行业研究员，擅长农产品产业链分析。"},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(DEEPSEEK_BASE_URL + "/chat/completions", headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"❌ DeepSeek API 请求失败: {response.status_code}, {response.text}")
                return "AI 分析暂时不可用，请参考上方基础指标。"
        except Exception as e:
            print(f"❌ 调用 DeepSeek 发生异常: {e}")
            return "AI 分析请求执行异常。"

    def 生成博客(self, df, 图片列表):
        """生成整合了 AI 分析的 Hugo Markdown"""
        print("📝 正在整合 AI 报告并生成博客...")
        latest = df.iloc[-1]
        date_str = latest['日期'].strftime('%Y-%m-%d')
        
        # 获取 AI 分析
        ai_report = self.调用DeepSeek分析(df.tail(180))
        
        content = f"""---
title: "大豆压榨利润(榨利)深度分析报告 - {date_str}"
date: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')}
description: "基于 DeepSeek AI 深度解读的豆油、豆粕压榨利润分析报告。涵盖最新基差、盘面榨利及未来走势预测。"
categories: ["分析报告"]
tags: ["豆油", "豆粕", "大豆", "榨利", "AI分析"]
image: ../../img/charts/{图片列表[0]}
---

## 🛰️ 核心摘要

截至 **{date_str}**，盘面数据概览：

- **当前榨利**: `{latest['榨利']:.2f}` 元/吨 (压榨成本按 {self.压榨成本} 元/吨计)
- **豆油基差**: `{latest['豆油基差']:.0f}` | **豆粕基差**: `{latest['豆粕基差']:.0f}`

---

## 🤖 AI 深度解读 (Powered by DeepSeek)

{ai_report}

---

## 📈 走势可视化

### 1. 全历史走势
展现长周期内压榨利润的周期性规律与极端位置。
![全历史走势](../../img/charts/{图片列表[3]})

### 2. 近两年细节
![近两年走势](../../img/charts/{图片列表[2]})

### 3. 近一年细节
![近一年走势](../../img/charts/{图片列表[1]})

### 4. 近半年精细分析
![近半年走势](../../img/charts/{图片列表[0]})

---

## 🔍 相关性与公式
> **计算公式**: 榨利 = (豆油现货价格 × 18.5% + 豆粕现货价格 × 78.5%) - 豆二价格 - {self.压榨成本}
> *注：数据来源于交易法门(基差)与新浪财经(期货)，报告自动生成。*

---
> 数据更新时间: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}
"""
        # 保存到博客目录
        md_name = "榨利深度分析报告.md"
        with open(os.path.join(HUGO_CONTENT_DIR, md_name), 'w', encoding='utf-8') as f:
            f.write(content)
        # 备份一份在本地 blog 目录
        with open(os.path.join(self.输出目录, md_name), 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ 完整报告已生成: {md_name}")

    def 运行(self):
        """执行流程"""
        豆二 = self.获取豆二数据()
        豆油 = self.获取元数据('Y', '豆油')
        豆粕 = self.获取元数据('M', '豆粕')
        
        if 豆二 is None or 豆油 is None or 豆粕 is None: return
        
        df = pd.merge(豆油, 豆粕, on='日期', how='inner')
        df = pd.merge(df, 豆二, on='日期', how='inner')
        df['榨利'] = (
            (df['豆油价格'] + df['豆油基差']) * self.豆油产出率 +
            (df['豆粕价格'] + df['豆粕基差']) * self.豆粕产出率 -
            df['豆二价格'] - self.压榨成本
        )
        
        图片 = []
        图片.append(self.绘制图表(df, 180, "半年"))
        图片.append(self.绘制图表(df, 365, "一年"))
        图片.append(self.绘制图表(df, 730, "两年"))
        图片.append(self.绘制图表(df, 9999, "全历史"))
        
        self.生成博客(df, 图片)
        print("🎉 任务完成！")

if __name__ == "__main__":
    榨利计算器V3().运行()
