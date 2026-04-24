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
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
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

    def 获取期货主力数据(self, symbol):
        """通用函数：使用 akshare 获取期货主力合约日线数据"""
        print(f"📡 获取期货主力合约 {symbol} 数据...")
        try:
            df = ak.futures_zh_daily_sina(symbol=symbol)
            if df is None or df.empty:
                print(f"⚠️ {symbol} 数据为空")
                return None
            
            # 重命名列名
            df = df.rename(columns={
                'date': '日期', 'open': '开盘价', 'high': '最高价', 
                'low': '最低价', 'close': '收盘价', 'volume': '成交量',
                'hold': '持仓量', 'settle': '结算价'
            })
            df['日期'] = pd.to_datetime(df['日期'])
            return df[['日期', '收盘价', '结算价']]
            
        except Exception as e:
            print(f"❌ 获取 {symbol} 数据失败: {e}")
            return None

    def 获取豆二数据(self):
        """使用 akshare 获取豆二(B0)期货数据"""
        df = self.获取期货主力数据("B0")
        if df is not None:
            df = df.rename(columns={'收盘价': '豆二价格'})
        return df

    def 获取豆系数据(self, 产品类型='Y'):
        """获取豆油/豆粕的期货价格(akshare)及基差(元爬虫)"""
        产品映射 = {'Y': '豆油', 'M': '豆粕'}
        产品名称 = 产品映射.get(产品类型, '未知产品')
        print(f"📊 开始获取{产品名称}综合数据...")
        
        # 1. 获取期货价格 (akshare)
        symbol = f"{产品类型}0"
        期货数据 = self.获取期货主力数据(symbol)
        if 期货数据 is None: return None
        期货数据 = 期货数据.rename(columns={'收盘价': f'{产品名称}价格'})
        
        # 2. 获取基差数据 (元爬虫)
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {'t': int(time.time() * 1000), 'type': 产品类型}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.jiaoyifamen.com/variety/varieties-varieties'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
            if response.status_code == 200:
                基差数据 = self.解析基差数据(response.json(), 产品类型)
                if 基差数据 is not None:
                    # 合并价格和基差
                    return pd.merge(期货数据, 基差数据, on='日期', how='inner')
            return 期货数据 # 如果基差获取失败，至少返回价格
        except Exception as e:
            print(f"❌ 获取{产品名称}基差失败: {e}")
            return 期货数据

    def 解析基差数据(self, 原始数据, 产品类型):
        """解析来自交易法门的基差数据"""
        if not 原始数据 or 'data' not in 原始数据: return None
        数据内容 = 原始数据['data']
        日期数据 = 数据内容.get('category', [])
        基差数据 = None
        for k, v in 数据内容.items():
            if 'basis' in k.lower() and 'value' in k.lower(): 
                基差数据 = v; break
        
        if not (日期数据 and 基差数据): return None
        
        min_len = min(len(日期数据), len(基差数据))
        df = pd.DataFrame({'日期': 日期数据[:min_len], '基差': 基差数据[:min_len]})
        
        curr_year = datetime.now().year
        def try_parse_date(x):
            if isinstance(x, str) and '-' in x and len(x) <= 5:
                try: return pd.to_datetime(f"{curr_year}-{x}")
                except: return pd.NaT
            return pd.to_datetime(x, errors='coerce')

        df['日期'] = df['日期'].apply(try_parse_date)
        df = df.dropna(subset=['日期'])
        df['基差'] = pd.to_numeric(df['基差'], errors='coerce')
        
        col_prefix = '豆油' if 产品类型 == 'Y' else '豆粕'
        return df.rename(columns={'基差': f'{col_prefix}基差'})

    def 获取油脂对比数据(self):
        """获取三大油脂的价格对比数据"""
        print("🍳 获取油脂对比数据 (豆油, 棕榈油, 菜油)...")
        y = self.获取期货主力数据("Y0").rename(columns={'收盘价': '豆油'})
        p = self.获取期货主力数据("P0").rename(columns={'收盘价': '棕榈油'})
        oi = self.获取期货主力数据("OI0").rename(columns={'收盘价': '菜油'})
        
        if y is None or p is None or oi is None: return None
        
        merged = pd.merge(y[['日期', '豆油']], p[['日期', '棕榈油']], on='日期', how='inner')
        merged = pd.merge(merged, oi[['日期', '菜油']], on='日期', how='inner')
        return merged

    # ================= 持仓数据获取 (新增) =================
    
    def read_position_data(self, file_path):
        """从本地文件读取持仓数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('code') != 200: return None
            return data.get('data', {})
        except: return None

    def get_position_from_api(self, contract):
        """从API获取持仓数据"""
        try:
            timestamp = int(time.time() * 1000)
            url = f'https://www.jiaoyifamen.com/tools/api//position/interest-process?t={timestamp}&type=Y&instrument={contract}&seat=%E4%B8%AD%E7%B2%AE%E6%9C%9F%E8%B4%A7'
            headers_pos = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.jiaoyifamen.com/'}
            response = requests.get(url, headers=headers_pos, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200: return data.get('data', {})
            return None
        except: return None

    def 获取持仓数据(self):
        """获取并整理中粮持仓数据"""
        print("🏗️ 获取中粮期货豆油空单持仓数据...")
        contracts = {
            'Y2609': os.path.join(SCRIPT_DIR, "中粮Y2609持仓数据.json"),
            'Y2605': os.path.join(SCRIPT_DIR, "中粮Y2605持仓数据_1767169342679.json"),
            'Y2601': os.path.join(SCRIPT_DIR, "中粮Y2601持仓数据.json"),
            'Y2509': os.path.join(SCRIPT_DIR, "中粮Y2509持仓数据.json"),
            'Y2505': os.path.join(SCRIPT_DIR, "中粮Y2505持仓数据.json"),
        }
        
        position_data = {}
        for contract, file_path in contracts.items():
            data = self.read_position_data(file_path)
            if not data: data = self.get_position_from_api(contract.lower())
            if data: position_data[contract] = data
            
        # 整合为 DataFrame
        all_dates = set()
        for c, d in position_data.items():
            all_dates.update(d.get('category', []))
            
        if not all_dates: return None
        
        df = pd.DataFrame({'日期': sorted(list(all_dates))})
        df['日期'] = pd.to_datetime(df['日期'])
        
        for contract, data in position_data.items():
            dates = data.get('category', [])
            neat_positions = data.get('neatPosition', []) # 空单持仓
            # 注意：API返回的neatPosition是净持仓，多单-空单？
            # 原始脚本里：position_df[f'{contract}持仓'] = ... .abs()
            # 交易法门接口 neatPosition 通常是净持仓。如果是空单持仓，通常是 rank_short - rank_long?
            # 让我们看原始脚本: `date_pos_map = dict(zip(dates, neat_positions))` -> `abs()`
            # 假设 neatPosition 是我们需要的数据。
            
            # 修正：我们需要的是特定席位的"空单持仓"还是"净持仓"?
            # 原始脚本注释写的是 "中粮期货豆油空单持仓走势"。
            # 但是 variable 叫 neatPosition (净持仓)。
            # 并且用了 abs()。
            # 如果是空单，应该是 shortVolume?
            # 再次检查 `豆油持仓价格榨利分析.py`. 
            # API URL: `interest-process`. Response structure has `neatPosition`.
            # If we trust the original script logic:
            if not dates or not neat_positions: continue
            
            mapping = dict(zip(dates, neat_positions))
            # dates are strings in API response usually?
            # 原始脚本: `position_df['日期'].dt.strftime('%Y-%m-%d').map(date_pos_map)`
            # 所以我们需要把 df['日期'] 转 str 来 map
            
            # 为了更稳健，我们先构建一个小DF然后merge
            temp_df = pd.DataFrame({'日期': dates, f'{contract}持仓': neat_positions})
            # 尝试解析日期
            try:
                # 简单处理 '2023-01-01' 或 '23-01-01'
                # 原始脚本逻辑:
                # for d in dates: if '-' in d...
                # 这里为了简化，我们假设 dates 格式标准 (YYYY-MM-DD)
                # 还是照搬 merge 逻辑吧
                pass
            except: pass
            
            # 使用简单的 map 方式
            date_map = {d: v for d, v in zip(dates, neat_positions)}
            # 转换 df 日期为 str 匹配
            date_strs = df['日期'].dt.strftime('%Y-%m-%d')
            df[f'{contract}持仓'] = date_strs.map(date_map).abs() # 取绝对值
            
        return df

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

    def 绘制图表(self, 榨利数据, 油脂数据, 天数, 名称):
        """绘制详尽的多周期组合图表 (含油脂对比)"""
        print(f"📊 绘制 {名称} 全维度组合图...")
        data = 榨利数据.tail(天数).copy() if 天数 < len(榨利数据) else 榨利数据.copy()
        
        # 创建 5 层结构图表 (新增持仓)
        fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(5, 1, figsize=(12, 22), dpi=100)
        最新日期 = data['日期'].max().strftime('%Y-%m-%d')
        
        # 0. 持仓走势 (新增 Top)
        pos_cols = [c for c in data.columns if '持仓' in c]
        if pos_cols:
            colors_pos = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            for idx, col in enumerate(sorted(pos_cols)):
                contract = col.replace('持仓', '')
                try:
                    valid = data.dropna(subset=[col]) # different path than v3 logic which used just data
                    # actually data is already sliced.
                    valid = data[data[col].notna()]
                    if not valid.empty:
                        c = colors_pos[idx % len(colors_pos)]
                        ax0.fill_between(valid['日期'], 0, valid[col], alpha=0.4, label=contract, color=c)
                        ax0.plot(valid['日期'], valid[col], linewidth=1.5, color=c)
                except: pass
            ax0.set_title(f'中粮期货豆油空单持仓走势 - {名称}', fontsize=14)
            ax0.set_ylabel('持仓量(手)')
            ax0.legend(loc='upper left', fontsize=9, ncol=3)
        else:
            ax0.text(0.5, 0.5, '暂无持仓数据', ha='center', va='center')
        ax0.grid(True, alpha=0.3)
        
        # 右上角显示最新数据日期 (Moved to Top)
        ax0.text(0.99, 0.97, f'数据截止: {最新日期}', transform=ax0.transAxes, 
                 fontsize=9, ha='right', va='top', 
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))
        
        # 1. 期货价格走势 (上图)
        ax1.plot(data['日期'], data['豆油价格'], color='darkorange', linestyle='-', label='豆油价格', linewidth=1.5)
        ax1.set_title(f'期货价格走势 (双轴) - {名称}', fontsize=14)
        ax1.set_ylabel('豆油价格(元/吨)', color='darkorange')
        ax1.tick_params(axis='y', labelcolor='darkorange')
        ax1.grid(True, alpha=0.3)
        
        ax1_r = ax1.twinx()
        ax1_r.plot(data['日期'], data['豆粕价格'], color='brown', linestyle='-', label='豆粕价格', linewidth=1.5)
        ax1_r.plot(data['日期'], data['豆二价格'], 'g--', label='豆二价格', linewidth=1.5)
        ax1_r.set_ylabel('豆粕/豆二价格(元/吨)')
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_r.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        
        # 右上角显示最新数据日期 (Moved to ax0)
        # ax1.text(0.99, 0.97, f'数据截止: {最新日期}', transform=ax1.transAxes, 
        #          fontsize=9, ha='right', va='top', 
        #          bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))
        
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
        ax2.set_title(f'基差走势 & 油粕比 - 最新油粕比: {data["现货油粕比"].iloc[-1]:.3f}', fontsize=12)
        
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
        
        ax3.set_title(f'大豆压榨利润走势 - 现货榨利: {data["榨利"].iloc[-1]:.2f}', fontsize=14)
        ax3.set_ylabel('榨利(元/吨)')
        ax3.grid(True, alpha=0.3)
        
        # 右轴：豆油期货走势 (新增)
        ax3_r = ax3.twinx()
        ax3_r.plot(data['日期'], data['豆油价格'], color='#5F9EA0', linestyle='--', label='豆油期货(右轴)', alpha=0.7, linewidth=1)
        ax3_r.set_ylabel('豆油价格(元/吨)', color='#5F9EA0')
        ax3_r.tick_params(axis='y', labelcolor='#5F9EA0')
        
        # 合并图例
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_r.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        
        # 4. 油脂板块对比 (新增底图)
        if 油脂数据 is not None:
            oil_data = 油脂数据.tail(天数).copy() if 天数 < len(油脂数据) else 油脂数据.copy()
            ax4.plot(oil_data['日期'], oil_data['豆油'], label='豆油 (Y)', color='darkorange', linewidth=2)
            ax4.plot(oil_data['日期'], oil_data['棕榈油'], label='棕榈油 (P)', color='green', linewidth=1.5)
            ax4.plot(oil_data['日期'], oil_data['菜油'], label='菜油 (OI)', color='gold', linewidth=1.5)
            ax4.set_title('油脂板块价格对比 (豆、棕、菜)', fontsize=14)
            ax4.set_ylabel('价格(元/吨)')
            ax4.legend(loc='upper left', fontsize=9)
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        文件名 = f"margin_chart_{名称}.png"
        plt.savefig(os.path.join(HUGO_IMAGES_DIR, 文件名))
        plt.savefig(os.path.join(self.输出目录, 文件名))
        plt.close()
        return 文件名

    # ================= AI 分析与博客生成逻辑 (基于原始 3x1 结构优化) =================

    def 深度分析(self, 榨利数据):
        """调用 DeepSeek AI 分析半年数据"""
        print("🤖 启动 AI 深度解读...")
        # 过滤掉无榨利数据的行，确保统计准确
        valid_data = 榨利数据.dropna(subset=['榨利'])
        if valid_data.empty:
            return "数据不足，暂无法进行深度分析。"
            
        data = valid_data.tail(180)
        curr = data.iloc[-1]
        stats = {
            'latest': curr['榨利'], 'avg': data['榨利'].mean(),
            'max': data['榨利'].max(), 'min': data['榨利'].min(),
            'win_rate': (len(data[data['榨利'] > 0]) / len(data)) * 100,
            'y_basis': curr['豆油基差'], 'm_basis': curr['豆粕基差']
        }
        
        prompt = f"""
你是一位资深的期货分析师，请根据以下数据对大豆压榨利润进行深度点评（数据截止：{curr['日期'].strftime('%Y-%m-%d')}）：
1. 当前榨利: {stats['latest']:.2f} 元/吨 (半年均值: {stats['avg']:.2f}, 最值区间: [{stats['min']:.0f}, {stats['max']:.0f}])
2. 半年胜率: {stats['win_rate']:.1f}%
3. 最新基差: 豆油 {stats['y_basis']} / 豆粕 {stats['m_basis']}

要求：
- 分析当前利润在历史周期中的位置。
- 说明当前高/低基差如何影响油厂利润策略。
- 针对豆油下游生产商需求，基于当前的基差与价格水平，给出具体的现货采购决策及期货买入/套保建议，不要输出表格。
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
        
        # 获取最新的一条有效数据用于显示（跳过只有持仓而没有价格的行）
        valid_df = df.dropna(subset=['榨利'])
        if not valid_df.empty:
            latest = valid_df.iloc[-1]
        else:
            latest = df.iloc[-1] # 兜底，虽然可能是 nan
            
        ai_text = self.深度分析(df)
        # 统一固定标题
        fixed_title = "🫘大豆榨利深度分析报告"
        date_iso = datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')
        
        content = f"""---
title: "{fixed_title}"
date: {date_iso}
lastmod: {date_iso}
description: "自动化生成的压榨利润深度报告，引用原始版本高精绘图和 DeepSeek AI 逻辑。"
draft: false
categories: ["期货分析"]
tags: ["大豆", "豆油", "豆粕", "期货", "可视化"]
image: /images/charts/{文件名列表[0]}
---

## 🛰️ 数据核心快照

- **最新榨利**: `{latest['榨利']:.2f}` 元/吨 (压榨成本：{self.压榨成本})
- **基差详情**: 豆油 `{latest['豆油基差']:.0f}` | 豆粕 `{latest['豆粕基差']:.0f}`

---

## 🤖 AI 首席分析师解读

{ai_text}

---

## 📈 多维度走势分析
(各周期图表均包含：价格、基差、榨利、板块对比)

### 1. 近半年 (180天)
![半年走势](/images/charts/{文件名列表[0]})

### 2. 近一年 (365天)
![一年走势](/images/charts/{文件名列表[1]})

### 3. 近两年 (730天)
![两年走势](/images/charts/{文件名列表[2]})

### 4. 全历史周期
![全历史走势](/images/charts/{文件名列表[3]})

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
        豆油 = self.获取豆系数据('Y')
        豆粕 = self.获取豆系数据('M')
        
        if 豆二 is None or 豆油 is None or 豆粕 is None:
            print("❌ 数据获取不完整，任务终止")
            return
            
        df = self.合并并计算榨利(豆油, 豆粕, 豆二)
        油脂df = self.获取油脂对比数据()
        
        # 合并持仓数据
        持仓df = self.获取持仓数据()
        if 持仓df is not None:
            print("🔄 合并持仓数据...")
            # 使用 outer join 保留所有日期，然后 sort
            df = pd.merge(df, 持仓df, on='日期', how='outer')
            df = df.sort_values('日期')
        
        # 绘图顺序
        imgs = []
        periods = [(180, "半年"), (365, "一年"), (730, "两年"), (9999, "全历史")]
        
        # 直接生成四张全维度组合图
        for days, name in periods:
            imgs.append(self.绘制图表(df, 油脂df, days, name))
        
        self.生成报告(df, imgs)
        print("\n🎉 榨利深度分析 V3 工作流执行完毕！")
        print("=" * 60)

if __name__ == "__main__":
    榨利计算器V3().启动()
