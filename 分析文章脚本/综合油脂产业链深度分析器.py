#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合油脂产业链深度分析器 - 全维度专业版
1. 整合持仓、价格、基差、榨利、外盘多维度数据
2. 生成 5 层全维度深度分析组合图
3. AI 驱动的深度产业链分析
4. 自动化 Hugo 博客发布
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 时区与警告配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class 综合分析器:
    def __init__(self):
        # 字体设置
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 参数设置
        self.豆油率, self.豆粕率, self.成本 = 0.185, 0.785, 150.0
        
        # 目录准备
        os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
        os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
        self.output_dir = os.path.join(SCRIPT_DIR, "charts_pro")
        os.makedirs(self.output_dir, exist_ok=True)

    # ================= 数据采集模块 =================

    def 获取持仓数据(self):
        """整合中粮持仓数据"""
        print("📊 正在搜寻中粮持仓数据...")
        contracts = ['Y2609', 'Y2605', 'Y2601', 'Y2509', 'Y2505']
        all_pos = []
        for c in contracts:
            path = os.path.join(SCRIPT_DIR, f"中粮{c}持仓数据.json")
            if not os.path.exists(path): continue
            try:
                with open(path, 'r') as f:
                    data = json.load(f).get('data', {})
                    df = pd.DataFrame({'date': data['category'], f'{c}_pos': data['neatPosition']})
                    df['date'] = pd.to_datetime(df['date'])
                    df[f'{c}_pos'] = df[f'{c}_pos'].abs()
                    all_pos.append(df)
            except: pass
        if not all_pos: return None
        res = all_pos[0]
        for item in all_pos[1:]:
            res = pd.merge(res, item, on='date', how='outer')
        return res.sort_values('date')

    def 获取期货主力数据(self, symbol):
        """获取 akshare 期货主力数据（含实时行情拼接）"""
        print(f"📡 正在获取 {symbol} 市场数据...")
        try:
            # 1. 历史数据
            df = ak.futures_main_sina(symbol=symbol.upper())
            if df is None or df.empty: return None
            
            mapping = {'日期': 'date', '开盘价': 'open', '最高价': 'high', '最低价': 'low', '收盘价': 'close', '成交量': 'volume', '持仓量': 'hold', '动态结算价': 'settle'}
            df = df.rename(columns=mapping)
            df['date'] = pd.to_datetime(df['date'])
            
            # 2. 实时行情拼接
            try:
                rt = ak.futures_zh_spot(symbol=symbol.upper())
                if rt is not None and not rt.empty:
                    df_last = rt.iloc[0]
                    today = pd.Timestamp.now().normalize()
                    if df['date'].max().date() < today.date():
                        new_row = {'date': today, 'open': float(df_last['open']), 'high': float(df_last['high']), 'low': float(df_last['low']), 'close': float(df_last['current_price']), 'volume': int(df_last['volume']), 'hold': int(df_last['hold']), 'settle': float(df_last['last_settle_price'])}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            except: pass
            
            return df.sort_values('date')
        except Exception as e:
            print(f"❌ 获取 {symbol} 失败: {e}")
            return None

    def 获取外盘数据(self):
        """获取美豆数据 (CBOT S)"""
        print("🌎 获取美豆(S)数据...")
        try:
            df = ak.futures_foreign_hist(symbol="S")
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df[['date', 'close']].sort_values('date') # akshare 默认返回 'close'
            return None
        except: return None

    def 获取基差数据(self, type='Y'):
        """从交易法门获取基差"""
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {'t': int(time.time() * 1000), 'type': type}
        try:
            res = requests.get(url, params=params, timeout=30, verify=False).json()
            if 'data' not in res: return None
            d = res['data']
            dates, vals = d.get('category', []), d.get('basisValue', [])
            if not (dates and vals): return None
            df = pd.DataFrame({'date': dates, f'{type}_basis': vals})
            df['date'] = df['date'].apply(lambda x: pd.to_datetime(f"{datetime.now().year}-{x}") if '-' in str(x) and len(str(x)) <= 5 else pd.to_datetime(x))
            return df.dropna()
        except: return None

    # ================= 可视化模块 =================

    def 绘制全维度组合图(self, df, 天数, 名称):
        """绘制 5 层结构全维度分析图"""
        print(f"🎨 绘制 {名称} 全维度深度研判图...")
        data = df.tail(天数).copy()
        
        fig, axes = plt.subplots(5, 1, figsize=(14, 25), dpi=100)
        (ax1, ax2, ax3, ax4, ax5) = axes
        
        # 1. 持仓层 (模拟持仓逻辑，此处保留接口)
        ax1.set_title(f"持仓与资金流向 - {名称}", fontsize=14)
        ax1.plot(data['date'], data['Y_hold'], color='red', label='豆油持仓量')
        ax1.set_ylabel("持仓(手)")
        ax1.grid(True, alpha=0.3); ax1.legend()

        # 2. 基差与油粕比层
        ax2.plot(data['date'], data['Y_basis'], color='darkorange', label='豆油基差')
        ax2.axhline(0, color='gray', linestyle='--')
        ax2.set_ylabel("基差(元/吨)")
        ax2_r = ax2.twinx()
        ax2_r.plot(data['date'], data['oil_meal_ratio'], color='green', alpha=0.5, label='现货油粕比')
        ax2_r.set_ylabel("油粕比")
        ax2.legend(loc='upper left'); ax2_r.legend(loc='upper right')
        ax2.set_title("基差走势与供需强弱")

        # 3. 榨利层
        ax3.fill_between(data['date'], 0, data['paper_margin'], alpha=0.3, color='orange', label='盘面榨利')
        ax3.plot(data['date'], data['spot_margin'], color='purple', linewidth=2, label='现货榨利')
        ax3.axhline(0, color='red', linestyle='-')
        ax3.set_title(f"大豆压榨利润 (最新: {data['spot_margin'].iloc[-1]:.0f}元/吨)")
        ax3.legend(); ax3.grid(True, alpha=0.3)

        # 4. 油脂对比层
        ax4.plot(data['date'], data['Y_close'], label='豆油(Y)', color='darkorange', linewidth=2)
        ax4.plot(data['date'], data['P_close'], label='棕榈油(P)', color='brown')
        ax4.plot(data['date'], data['OI_close'], label='菜油(OI)', color='gold')
        ax4.set_title("三大油脂共振走势")
        ax4.legend(); ax4.grid(True, alpha=0.3)

        # 5. 期货价格走势 (含美豆参考)
        ax5.plot(data['date'], data['Y_close'], color='darkorange', label='豆油(内盘)')
        ax5_r = ax5.twinx()
        if 'US_close' in data.columns:
            ax5_r.plot(data['date'], data['US_close'], color='blue', linestyle='--', alpha=0.6, label='美豆(外盘)')
            ax5_r.set_ylabel("美豆(美分/蒲式耳)")
        ax5.set_title("内外盘联动走势")
        ax5.legend(loc='upper left'); ax5_r.legend(loc='upper right')

        plt.tight_layout()
        fname = f"full_pro_analysis_{名称}.png"
        plt.savefig(os.path.join(HUGO_IMAGES_DIR, fname))
        plt.close()
        return fname

    # ================= AI 与 报告模块 =================

    def 深度分析(self, df):
        """调用 AI 生成深度解读"""
        print("🤖 启动 AI 全维度产业链洞察...")
        latest = df.iloc[-1]
        prompt = f"""
你是一位顶级油脂产业链分析师。请结合以下【全维度数据】进行深度推演：

1. **持仓研判**: 中粮期货在豆油主力上的空单规模。
2. **基差提示**: 豆油当前基差 {latest.get('Y_basis','N/A')}，反映现货贴水/升水状况。
3. **榨利核心**: 现货榨利 {latest['spot_margin']:.2f} 元/吨，盘面榨利 {latest['paper_margin']:.2f} 元/吨。
4. **内外盘联动**: 豆油价格 {latest['Y_close']} 与美豆参考价 {latest.get('US_close','N/A')} 的偏离。
5. **板块比价**: 油粕比 {latest['oil_meal_ratio']:.3f}。

分析要求：
- 请分析当前榨利水平对油厂开机意愿的传导。
- 结合基差和持仓，判断主力资金的操作逻辑（套保还是趋势）。
- 给出明确的行业采购策略建议。
- 禁止使用表格，直接输出 Markdown 文本。
"""
        try:
            res = requests.post(DEEPSEEK_BASE_URL + "/chat/completions", 
                                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                                json={"model": "deepseek-chat", "messages": [{"role": "system", "content": "你是一位资深期货专家。"}, {"role": "user", "content": prompt}]},
                                timeout=60).json()
            return res['choices'][0]['message']['content']
        except: return "AI 分析连接异常。"

    def 生成报告(self, df, imgs):
        """生成整合版报告"""
        print("📝 生成全维度分析报告...")
        latest = df.iloc[-1]
        ai_text = self.深度分析(df)
        date_iso = datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        
        content = f"""---
title: "综合油脂产业链深度分析报告"
date: {date_iso}
description: "全维度整合：持仓、榨利、基差、内外盘联动。一站式产业链深度穿透。"
draft: false
categories: ["期货分析"]
tags: ["豆油", "榨利", "持仓", "宏观"]
image: /images/charts/{imgs[0]}
---

## 🛰️ 全维度数据快照 (截止: {latest['date'].strftime('%Y-%m-%d')})

- **压榨利润**: 现货 `{latest['spot_margin']:.2f}` | 盘面 `{latest['paper_margin']:.2f}`
- **核心基差**: 豆油 `{latest.get('Y_basis','N/A')}` | 豆粕 `{latest.get('M_basis','N/A')}`
- **板块比价**: 现货油粕比 `{latest['oil_meal_ratio']:.3f}`

---

## 🤖 产业链首席分析师解读

{ai_text}

---

## 📈 深度全维度走势研判

### 1. 近半年 (180天)
![深度研判-半年](/images/charts/{imgs[0]})

### 2. 近一年 (365天)
![深度研判-一年](/images/charts/{imgs[1]})

### 3. 全历史轮回
![深度研判-全历史](/images/charts/{imgs[2]})

---

## 🛠️ 计算逻辑与声明
> 数据源：Akshare / 交易法门 / DeepSeek
> 榨利 = (豆油价+基差)*0.185 + (豆粕价+基差)*0.785 - 豆二价 - 150
> 生成时间：{datetime.now(BEIJING_TZ).strftime('%H:%M:%S')}
"""
        md_path = os.path.join(HUGO_CONTENT_DIR, "综合油脂产业链深度分析报告.md")
        with open(md_path, 'w', encoding='utf-8') as f: f.write(content)
        print(f"✅ 报告已发布: {md_path}")
    def 运行(self):
        print("🚀 启动综合油脂产业链深度分析器...")
        
        # 1. 采集基础数据
        y0 = self.获取期货主力数据('y0')
        m0 = self.获取期货主力数据('m0')
        p0 = self.获取期货主力数据('p0')
        oi0 = self.获取期货主力数据('oi0')
        b0 = self.获取期货主力数据('b0')
        us = self.获取外盘数据()
        y_basis = self.获取基差数据('Y')
        m_basis = self.获取基差数据('M')

        # 2. 数据对齐与合并
        if y0 is None: 
            print("❌ 核心数据获取失败")
            return
            
        df = y0[['date', 'close', 'hold']].rename(columns={'close':'Y_close', 'hold':'Y_hold'})
        for other, name in [(p0, 'P_close'), (oi0, 'OI_close'), (m0, 'M_close'), (b0, 'B_close')]:
            if other is not None:
                df = pd.merge(df, other[['date', 'close']].rename(columns={'close': name}), on='date', how='inner')
        
        if us is not None:
            df = pd.merge(df, us[['date', 'close']].rename(columns={'close': 'US_close'}), on='date', how='left')
        
        for basis, name in [(y_basis, 'Y_basis'), (m_basis, 'M_basis')]:
            if basis is not None:
                df = pd.merge(df, basis, on='date', how='left')
        
        df = df.ffill()

        # 3. 持仓整合
        pos = self.获取持仓数据()
        if pos is not None:
            df = pd.merge(df, pos, on='date', how='left').ffill()

        # 4. 计算分析指标
        df['spot_margin'] = (df['Y_close'] + df.get('Y_basis', 0)) * self.豆油率 + (df['M_close'] + df.get('M_basis', 0)) * self.豆粕率 - df['B_close'] - self.成本
        df['paper_margin'] = df['Y_close'] * self.豆油率 + df['M_close'] * self.豆粕率 - df['B_close'] - self.成本
        df['oil_meal_ratio'] = (df['Y_close'] + df.get('Y_basis', 0)) / (df['M_close'] + df.get('M_basis', 0))

        # 5. 绘图
        imgs = []
        for d, n in [(180, "半年"), (365, "一年"), (9999, "全历史")]:
            imgs.append(self.绘制全维度组合图(df, d, n))

        # 6. 生成报告
        self.生成报告(df, imgs)


if __name__ == "__main__":
    综合分析器().运行()
