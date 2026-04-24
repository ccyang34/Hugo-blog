#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合数据分析报告 - 增强版
1. 获取综合数据（持仓、价格、基差、榨利）
2. 生成多维度图表
3. 调用 DeepSeek API 生成深度分析
4. 自动生成 Hugo 博客文章
"""
import json
import requests
import time
import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import akshare as ak
import urllib3
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pytz

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 配置区域 =================
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Hugo 博客配置
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

# 时区配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    'Accept': 'application/json, text/plain, */*',
}

# ================= 持仓数据获取 =================
def read_position_data(file_path):
    """从本地文件读取持仓数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data.get('code') != 200:
            return None
        return data.get('data', {})
    except Exception as e:
        return None

def get_position_from_api(contract):
    """从API获取持仓数据"""
    try:
        timestamp = int(time.time() * 1000)
        url = f'https://www.jiaoyifamen.com/tools/api//position/interest-process?t={timestamp}&type=Y&instrument={contract}&seat=%E4%B8%AD%E7%B2%AE%E6%9C%9F%E8%B4%A7'
        headers_pos = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.jiaoyifamen.com/variety/seat-positionBuilding'
        }
        response = requests.get(url, headers=headers_pos, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                return data.get('data', {})
        return None
    except:
        return None

# ================= 基差数据获取 =================
def get_basis_data(product_type='Y'):
    """获取基差数据"""
    try:
        timestamp = int(time.time() * 1000)
        url = f'https://www.jiaoyifamen.com/tools/api//future-basis/query?t={timestamp}&type={product_type}'
        response = requests.get(url, headers=headers, timeout=30, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                return data.get('data', {})
        return None
    except:
        return None

def get_soybean_data():
    """获取豆二期货数据"""
    try:
        data = ak.futures_zh_daily_sina(symbol="B0")
        if data.empty:
            return None
        data = data.rename(columns={
            'date': '日期', 'close': '豆二价格'
        })
        data['日期'] = pd.to_datetime(data['日期'])
        return data[['日期', '豆二价格']]
    except Exception as e:
        print(f"获取豆二数据失败: {e}")
        return None

def parse_basis_data(raw_data, product_type):
    """解析基差数据"""
    if not raw_data:
        return None
    
    dates = raw_data.get('category', [])
    prices = raw_data.get('priceValue', [])
    basis = raw_data.get('basisValue', [])
    
    if not (dates and prices and basis):
        return None
    
    min_len = min(len(dates), len(prices), len(basis))
    
    curr_year = datetime.now().year
    parsed_dates = []
    for d in dates[:min_len]:
        try:
            if isinstance(d, str) and '-' in d and len(d) <= 5:
                parsed_dates.append(pd.to_datetime(f"{curr_year}-{d}"))
            else:
                parsed_dates.append(pd.to_datetime(d))
        except:
            parsed_dates.append(pd.NaT)
    
    prefix = '豆油' if product_type == 'Y' else '豆粕'
    df = pd.DataFrame({
        '日期': parsed_dates,
        f'{prefix}盘面价格': prices[:min_len],
        f'{prefix}基差': basis[:min_len]
    })
    df = df.dropna()
    df[f'{prefix}盘面价格'] = pd.to_numeric(df[f'{prefix}盘面价格'], errors='coerce')
    df[f'{prefix}基差'] = pd.to_numeric(df[f'{prefix}基差'], errors='coerce')
    return df.dropna()

def calculate_margin(oil_data, meal_data, soybean_data):
    """计算榨利"""
    oil_rate = 0.185
    meal_rate = 0.785
    cost = 150.0
    
    merged = pd.merge(oil_data, meal_data, on='日期', how='inner')
    merged = pd.merge(merged, soybean_data, on='日期', how='inner')
    
    # 现货榨利（含基差）
    merged['现货榨利'] = (
        (merged['豆油盘面价格'] + merged['豆油基差']) * oil_rate +
        (merged['豆粕盘面价格'] + merged['豆粕基差']) * meal_rate -
        merged['豆二价格'] - cost
    )
    
    # 盘面榨利（不含基差）
    merged['盘面榨利'] = (
        merged['豆油盘面价格'] * oil_rate +
        merged['豆粕盘面价格'] * meal_rate -
        merged['豆二价格'] - cost
    )
    
    # 现货油粕比
    merged['现货油粕比'] = (merged['豆油盘面价格'] + merged['豆油基差']) / (merged['豆粕盘面价格'] + merged['豆粕基差'])
    
    # 豆油基差率
    merged['豆油基差率'] = merged['豆油基差'] / merged['豆油盘面价格'] * 100
    
    return merged

# ================= 数据获取主函数 =================
def get_all_data():
    """获取所有数据并返回整合后的DataFrame"""
    print("=" * 60)
    print("📊 综合数据分析报告生成器 v2.0")
    print("=" * 60)
    
    # 1. 读取持仓数据
    print("\n1. 读取中粮持仓数据...")
    contracts = {
        'Y2609': os.path.join(SCRIPT_DIR, "中粮Y2609持仓数据.json"),
        'Y2605': os.path.join(SCRIPT_DIR, "中粮Y2605持仓数据_1767169342679.json"),
        'Y2601': os.path.join(SCRIPT_DIR, "中粮Y2601持仓数据.json"),
        'Y2509': os.path.join(SCRIPT_DIR, "中粮Y2509持仓数据.json"),
        'Y2505': os.path.join(SCRIPT_DIR, "中粮Y2505持仓数据.json"),
    }
    
    position_data = {}
    for contract, file_path in contracts.items():
        data = read_position_data(file_path)
        if data:
            position_data[contract] = data
            print(f"  ✓ {contract}: {len(data.get('category', []))}天")
        else:
            data = get_position_from_api(contract.lower())
            if data:
                position_data[contract] = data
                print(f"  ✓ {contract} (API): {len(data.get('category', []))}天")
            else:
                print(f"  ✗ {contract}: 无数据")
    
    # 2. 获取基差数据
    print("\n2. 获取豆油/豆粕基差数据...")
    
    print("  获取豆油数据...")
    oil_raw = get_basis_data('Y')
    oil_data = parse_basis_data(oil_raw, 'Y') if oil_raw else None
    if oil_data is not None:
        print(f"  ✓ 豆油数据: {len(oil_data)}天")
    
    print("  获取豆粕数据...")
    meal_raw = get_basis_data('M')
    meal_data = parse_basis_data(meal_raw, 'M') if meal_raw else None
    if meal_data is not None:
        print(f"  ✓ 豆粕数据: {len(meal_data)}天")
    
    print("  获取豆二数据...")
    soybean_data = get_soybean_data()
    if soybean_data is not None:
        print(f"  ✓ 豆二数据: {len(soybean_data)}天")
    
    # 3. 计算榨利
    margin_data = None
    if oil_data is not None and meal_data is not None and soybean_data is not None:
        print("\n3. 计算榨利...")
        margin_data = calculate_margin(oil_data, meal_data, soybean_data)
        print(f"  ✓ 榨利数据: {len(margin_data)}天")
    else:
        print("\n3. ✗ 榨利数据计算失败（缺少基础数据）")
    
    # 4. 整合持仓数据
    print("\n4. 整合持仓数据...")
    
    all_dates = set()
    for contract, data in position_data.items():
        dates = data.get('category', [])
        all_dates.update(dates)
    all_dates = sorted(list(all_dates))
    
    position_df = pd.DataFrame({'日期': all_dates})
    position_df['日期'] = pd.to_datetime(position_df['日期'])
    
    for contract, data in position_data.items():
        dates = data.get('category', [])
        neat_positions = data.get('neatPosition', [])
        date_pos_map = dict(zip(dates, neat_positions))
        position_df[f'{contract}持仓'] = position_df['日期'].dt.strftime('%Y-%m-%d').map(date_pos_map)
        position_df[f'{contract}持仓'] = position_df[f'{contract}持仓'].abs()
    
    print(f"  ✓ 持仓数据整合完成: {len(position_df)}天")
    
    # 5. 合并所有数据
    print("\n5. 合并所有数据...")
    
    if margin_data is not None:
        final_df = pd.merge(position_df, margin_data, on='日期', how='outer')
    else:
        final_df = position_df
    
    final_df = final_df.sort_values('日期', ascending=True)
    
    cutoff_date = datetime.now() - relativedelta(months=18)
    final_df = final_df[final_df['日期'] >= cutoff_date]
    print(f"  ✓ 筛选最近一年半数据（从 {cutoff_date.strftime('%Y-%m-%d')} 开始）")
    
    if '盘面榨利' in final_df.columns:
        final_df['盘面榨利'] = final_df['盘面榨利'].round(2)
    if '现货榨利' in final_df.columns:
        final_df['现货榨利'] = final_df['现货榨利'].round(2)
    
    print(f"  ✓ 数据合并完成，共 {len(final_df)} 行")
    
    return final_df, position_data, margin_data

# ================= 图表绘制 =================
def setup_chinese_font():
    """设置中文字体"""
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

def plot_full_chart(df, position_cols, output_dir, days=180, name="半年"):
    """
    绘制完整综合分析图（4行子图上下组合）：
    1. 持仓走势图
    2. 榨利走势图
    3. 期货价格走势图
    4. 基差走势图
    """
    print(f"📊 绘制完整综合分析图 - {name}...")
    setup_chinese_font()
    
    # 使用日期范围筛选（从今天往前推指定天数）
    end_date = datetime.now()
    start_date = end_date - pd.Timedelta(days=days)
    data = df[(df['日期'] >= start_date) & (df['日期'] <= end_date)].copy()
    
    if len(data) == 0:
        print(f"  ⚠ 无数据（{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}）")
        return None
    
    latest_date = data['日期'].max().strftime('%Y-%m-%d')
    
    # 创建4行子图
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(14, 20), dpi=100)
    
    # ===== 第1行：持仓走势图 =====
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    for idx, col in enumerate(sorted(position_cols)):
        contract = col.replace('持仓', '')
        valid_data = data[data[col].notna()]
        if len(valid_data) > 0:
            ax1.fill_between(valid_data['日期'], 0, valid_data[col], 
                           alpha=0.4, label=contract, color=colors[idx % len(colors)])
            ax1.plot(valid_data['日期'], valid_data[col], 
                    linewidth=1.5, color=colors[idx % len(colors)])
    
    ax1.set_title(f'中粮期货豆油空单持仓走势 - {name}', fontsize=14, fontweight='bold')
    ax1.set_ylabel('持仓量（手）', fontsize=11)
    ax1.legend(loc='upper left', fontsize=9, ncol=3)
    ax1.grid(True, alpha=0.3)
    ax1.text(0.99, 0.97, f'数据截止: {latest_date}', transform=ax1.transAxes,
             fontsize=9, ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='wheat', alpha=0.7))
    
    # ===== 第2行：榨利走势图 =====
    margin_data = data.dropna(subset=['现货榨利'])
    if len(margin_data) > 0:
        ax2.fill_between(margin_data['日期'], 0, margin_data['盘面榨利'], 
                        alpha=0.3, color='orange', label='盘面榨利(不含基差)')
        ax2.plot(margin_data['日期'], margin_data['现货榨利'], 
                color='purple', label='现货榨利(含基差)', linewidth=2)
        ax2.axhline(0, color='red', linestyle='-', alpha=0.6, label='盈亏平衡')
        
        # 标注最值
        max_v = margin_data['现货榨利'].max()
        min_v = margin_data['现货榨利'].min()
        max_d = margin_data.loc[margin_data['现货榨利'].idxmax(), '日期']
        min_d = margin_data.loc[margin_data['现货榨利'].idxmin(), '日期']
        ax2.annotate(f'最高: {max_v:.0f}', xy=(max_d, max_v), xytext=(0, 10),
                    textcoords='offset points', ha='center', color='purple', fontsize=9)
        ax2.annotate(f'最低: {min_v:.0f}', xy=(min_d, min_v), xytext=(0, -20),
                    textcoords='offset points', ha='center', color='purple', fontsize=9)
        
        latest_margin = margin_data.iloc[-1]
        ax2.set_title(f'大豆压榨利润走势 - 现货榨利: {latest_margin["现货榨利"]:.2f} | 盘面榨利: {latest_margin["盘面榨利"]:.2f}', 
                     fontsize=14, fontweight='bold')
    
    ax2.set_ylabel('榨利(元/吨)', fontsize=11)
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # ===== 第3行：期货价格走势图 =====
    price_data = data.dropna(subset=['豆油盘面价格'])
    if len(price_data) > 0:
        ax3.plot(price_data['日期'], price_data['豆油盘面价格'], color='darkorange', 
                 linestyle='-', label='豆油盘面价格', linewidth=2)
        ax3.set_ylabel('豆油价格(元/吨)', color='darkorange', fontsize=11)
        ax3.tick_params(axis='y', labelcolor='darkorange')
        
        ax3_r = ax3.twinx()
        ax3_r.plot(price_data['日期'], price_data['豆粕盘面价格'], 'b-', label='豆粕盘面价格', linewidth=1.5)
        ax3_r.plot(price_data['日期'], price_data['豆二价格'], 'g--', label='豆二价格', linewidth=1.5)
        ax3_r.set_ylabel('豆粕/豆二价格(元/吨)', fontsize=11)
        
        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_r.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
    
    ax3.set_title(f'期货价格走势 (双轴)', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # ===== 第4行：基差走势图 =====
    basis_data = data.dropna(subset=['豆油基差'])
    if len(basis_data) > 0:
        ax4.plot(basis_data['日期'], basis_data['豆油基差'], color='darkorange', 
                 linestyle='--', label='豆油基差', linewidth=2, alpha=0.8)
        ax4.plot(basis_data['日期'], basis_data['豆粕基差'], 'b--', label='豆粕基差', linewidth=1.5, alpha=0.8)
        ax4.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax4.set_ylabel('基差(元/吨)', fontsize=11)
        
        ax4_r = ax4.twinx()
        if '现货油粕比' in basis_data.columns:
            ax4_r.fill_between(basis_data['日期'], basis_data['现货油粕比'].min() * 0.98, 
                              basis_data['现货油粕比'], alpha=0.25, color='green', label='现货油粕比')
        if '豆油基差率' in basis_data.columns:
            ax4_r.plot(basis_data['日期'], basis_data['豆油基差率'], color='purple', 
                      linestyle='-', linewidth=1.5, label='豆油基差率(%)')
        ax4_r.set_ylabel('油粕比 / 基差率(%)', color='green', fontsize=11)
        ax4_r.tick_params(axis='y', labelcolor='green')
        
        lines1, labels1 = ax4.get_legend_handles_labels()
        lines2, labels2 = ax4_r.get_legend_handles_labels()
        ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
        
        latest_basis = basis_data.iloc[-1]
        ax4.set_title(f'基差走势 & 油粕比 - 最新油粕比: {latest_basis.get("现货油粕比", 0):.3f} | 基差率: {latest_basis.get("豆油基差率", 0):.1f}%', fontsize=12)
    
    ax4.set_xlabel('日期', fontsize=11)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    filename = f"full_analysis_chart_{name}.png"
    plt.savefig(os.path.join(output_dir, filename))
    plt.savefig(os.path.join(HUGO_IMAGES_DIR, filename))
    plt.close()
    print(f"  ✓ 保存: {filename}")
    return filename

# ================= 构建分析提示词 =================
def build_analysis_prompt(df):
    """构建 DeepSeek 分析提示词"""
    latest = df.dropna().iloc[-1] if not df.dropna().empty else df.iloc[-1]
    recent_30 = df.tail(30).dropna()
    recent_90 = df.tail(90).dropna()
    recent_180 = df.tail(180).dropna()
    
    position_cols = [col for col in df.columns if '持仓' in col]
    
    # 构建持仓变化描述
    position_info = []
    for col in sorted(position_cols):
        contract = col.replace('持仓', '')
        recent_vals = df[col].dropna().tail(30)
        if len(recent_vals) >= 2:
            start_val = recent_vals.iloc[0]
            end_val = recent_vals.iloc[-1]
            change = end_val - start_val
            change_pct = (change / start_val * 100) if start_val > 0 else 0
            position_info.append(f"  - {contract}: 最新持仓 {end_val:.0f} 手，近30天变化 {change:+.0f} 手 ({change_pct:+.1f}%)")
    
    position_text = "\n".join(position_info) if position_info else "  无持仓数据"
    
    # 构建价格和榨利统计
    price_stats = ""
    if '豆油盘面价格' in df.columns and not recent_30['豆油盘面价格'].dropna().empty:
        oil_price = recent_30['豆油盘面价格'].dropna()
        price_stats += f"""
【豆油】
  - 最新盘面价格: {latest.get('豆油盘面价格', 'N/A')} 元/吨
  - 最新基差: {latest.get('豆油基差', 'N/A')} 元/吨
  - 近30天价格区间: {oil_price.min():.0f} ~ {oil_price.max():.0f}
  - 近30天价格均值: {oil_price.mean():.0f}"""
    
    if '豆粕盘面价格' in df.columns and not recent_30['豆粕盘面价格'].dropna().empty:
        meal_price = recent_30['豆粕盘面价格'].dropna()
        price_stats += f"""
【豆粕】
  - 最新盘面价格: {latest.get('豆粕盘面价格', 'N/A')} 元/吨
  - 最新基差: {latest.get('豆粕基差', 'N/A')} 元/吨
  - 近30天价格区间: {meal_price.min():.0f} ~ {meal_price.max():.0f}
  - 近30天价格均值: {meal_price.mean():.0f}"""
    
    if '豆二价格' in df.columns:
        soy_price = recent_30['豆二价格'].dropna()
        if not soy_price.empty:
            price_stats += f"""
【豆二（大豆原料）】
  - 最新价格: {latest.get('豆二价格', 'N/A')} 元/吨
  - 近30天价格区间: {soy_price.min():.0f} ~ {soy_price.max():.0f}"""
    
    margin_stats = ""
    if '现货榨利' in df.columns and not recent_30['现货榨利'].dropna().empty:
        spot_margin = recent_30['现货榨利'].dropna()
        spot_180 = recent_180['现货榨利'].dropna()
        
        margin_stats = f"""
【榨利分析】
  - 最新现货榨利: {latest.get('现货榨利', 'N/A'):.2f} 元/吨
  - 最新盘面榨利: {latest.get('盘面榨利', 'N/A'):.2f} 元/吨
  - 近30天现货榨利区间: {spot_margin.min():.2f} ~ {spot_margin.max():.2f}
  - 近30天现货榨利均值: {spot_margin.mean():.2f}
  - 近半年现货榨利区间: {spot_180.min():.2f} ~ {spot_180.max():.2f}
  - 近半年现货榨利均值: {spot_180.mean():.2f}
  - 榨利盈利天数占比（半年）: {(len(spot_180[spot_180 > 0]) / len(spot_180) * 100):.1f}%"""
    
    # 生成最近10天的详细数据表格
    recent_10 = df.tail(10).copy()
    recent_10['日期'] = recent_10['日期'].dt.strftime('%Y-%m-%d')
    data_table = recent_10.to_string(index=False)
    
    prompt = f"""你是一位资深的期货分析师和大宗商品研究员，擅长分析豆油、豆粕及大豆压榨产业链。

请根据以下综合数据，撰写一份专业的豆油市场深度分析报告。

## 数据概览

**数据日期**: {latest['日期'].strftime('%Y-%m-%d') if hasattr(latest['日期'], 'strftime') else latest['日期']}
**数据周期**: 最近18个月

### 一、中粮期货持仓数据（空单持仓）
{position_text}

### 二、豆油/豆粕/豆二价格与基差数据
{price_stats}

### 三、压榨利润分析
{margin_stats}

### 四、最近10天详细数据
```
{data_table}
```

## 分析要求

请从以下维度进行深入分析：

1. **持仓分析**
   - 分析中粮期货在各豆油合约上的空单持仓变化趋势（合约换月出现大幅减仓增仓是正常的）
   - 解读持仓变化反映的市场预期和套保需求
   - 评估大型机构持仓对后市价格的潜在影响

2. **价格与基差分析**
   - 分析豆油当前价格在历史区间中的位置
   - 解读当前基差水平（贴水/升水）及其含义
   - 分析现货与期货的价差走势对企业采购决策的影响

3. **榨利深度解读**
   - 分析当前压榨利润在历史周期中的位置
   - 评估油厂开机意愿及对供给端的影响
   - 解读现货榨利与盘面榨利的差异及套利机会

4. **产业链供需判断**
   - 结合持仓、价格、基差、榨利等多维数据
   - 给出对豆油供需格局的综合判断

5. **操作建议**
   - 针对豆油现货采购商：给出具体的采购时机和策略建议
   - 针对期货投资者：给出方向性判断和风险提示
   - 针对油厂：给出套保策略建议

## 输出格式要求

- 使用清晰的 Markdown 格式
- 分析需专业、有深度、有数据支撑
- 结论明确，操作建议具体可行
- 语言简洁有力，避免空泛表述
- **重要**：直接输出纯 Markdown 文本，禁止使用 ```markdown 或任何代码块包裹整篇报告
"""
    
    return prompt

# ================= 调用 DeepSeek API =================
def call_deepseek_analysis(prompt):
    """调用 DeepSeek API 进行分析"""
    print("\n🤖 正在调用 DeepSeek AI 进行深度分析...")
    
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        print("[Warning] 未配置 DEEPSEEK_API_KEY，跳过 AI 分析。")
        return None
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一位资深大宗商品分析师，专注于油脂油料产业链研究，擅长从多维度数据中提取洞见。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    try:
        print("  请求发送中，请稍候（可能需要30-60秒）...")
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print("  ✓ AI 分析完成！")
            return content
        else:
            print(f"  ✗ API 请求失败: {response.status_code}")
            return None
    except requests.Timeout:
        print("  ✗ API 请求超时")
        return None
    except Exception as e:
        print(f"  ✗ API 请求异常: {e}")
        return None

# ================= 生成 Hugo 博客 =================
def generate_hugo_blog(df, analysis_text, chart_files):
    """生成 Hugo 博客文章"""
    print("\n📝 生成 Hugo 博客文章...")
    
    latest = df.dropna().iloc[-1] if not df.dropna().empty else df.iloc[-1]
    date_str = latest['日期'].strftime('%Y-%m-%d') if hasattr(latest['日期'], 'strftime') else str(latest['日期'])
    
    # Hugo frontmatter
    date_iso = datetime.now(BEIJING_TZ).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # 构建图表引用
    charts_section = ""
    if chart_files.get('半年'):
        charts_section += f"""
### 📊 综合分析 - 近半年
![综合分析-半年](/images/charts/{chart_files['半年']})
"""
    if chart_files.get('一年'):
        charts_section += f"""
### 📊 综合分析 - 近一年
![综合分析-一年](/images/charts/{chart_files['一年']})
"""
    if chart_files.get('一年半'):
        charts_section += f"""
### � 综合分析 - 近一年半
![综合分析-一年半](/images/charts/{chart_files['一年半']})
"""

    # 数据快照
    position_cols = [col for col in df.columns if '持仓' in col]
    position_snapshot = ""
    for col in sorted(position_cols):
        contract = col.replace('持仓', '')
        val = latest.get(col, 0)
        if pd.notna(val):
            position_snapshot += f"- **{contract}**: `{val:.0f}` 手\n"
    
    content = f"""---
title: "🫘豆油综合数据深度分析报告"
date: {date_iso}
lastmod: {date_iso}
description: "整合中粮持仓、价格基差、压榨利润等多维度数据，结合 DeepSeek AI 生成的专业分析报告。"
draft: false
categories: ["期货分析"]
tags: ["豆油", "持仓分析", "基差", "榨利", "期货", "可视化"]
image: /images/charts/{chart_files.get('半年', 'full_analysis_chart_半年.png')}
---

## 🛰️ 数据核心快照

**数据截止日期**: `{date_str}`

### 中粮期货空单持仓
{position_snapshot}

### 价格与基差
- **豆油盘面价格**: `{latest.get('豆油盘面价格', 'N/A')}` 元/吨
- **豆油基差**: `{latest.get('豆油基差', 'N/A')}` 元/吨
- **豆粕盘面价格**: `{latest.get('豆粕盘面价格', 'N/A')}` 元/吨
- **豆粕基差**: `{latest.get('豆粕基差', 'N/A')}` 元/吨

### 压榨利润
- **现货榨利**: `{latest.get('现货榨利', 'N/A'):.2f}` 元/吨
- **盘面榨利**: `{latest.get('盘面榨利', 'N/A'):.2f}` 元/吨

---

## 🤖 AI 首席分析师解读

{analysis_text}

---

## 📈 多维度走势图表

{charts_section}

---

## �️ 计算说明

> **榨利公式**: 榨利 = (豆油现货价格 × 18.5% + 豆粕现货价格 × 78.5%) - 豆二价格 - 150元
> 
> **数据来源**: 
> - 持仓数据: 交易法门（中粮期货豆油持仓）
> - 价格与基差: 交易法门 API
> - 期货行情: AkShare（新浪财经）
> - AI 分析: DeepSeek
>
> **更新时间**: {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}

---

*本报告由 AI 自动生成，仅供参考，不构成投资建议。*
"""
    
    # 保存到 Hugo content 目录
    md_path = os.path.join(HUGO_CONTENT_DIR, "豆油综合分析报告.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Hugo 博客已保存: {md_path}")
    return md_path

# ================= 主函数 =================
def main():
    # 确保目录存在
    os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
    os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
    output_dir = os.path.join(SCRIPT_DIR, "charts")
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 获取所有数据
    df, position_data, margin_data = get_all_data()
    
    if df is None or df.empty:
        print("\n❌ 数据获取失败，无法生成报告")
        return
    
    # 2. 获取持仓列
    position_cols = [col for col in df.columns if '持仓' in col]
    
    # 3. 生成图表（只生成3张：半年、一年、一年半）
    print("\n6. 生成图表...")
    chart_files = {}
    
    if margin_data is not None:
        # 生成3个周期的完整综合分析图
        chart_files['半年'] = plot_full_chart(df, position_cols, output_dir, 180, "半年")
        chart_files['一年'] = plot_full_chart(df, position_cols, output_dir, 365, "一年")
        chart_files['一年半'] = plot_full_chart(df, position_cols, output_dir, 548, "一年半")
    
    print(f"  ✓ 已生成 {len([v for v in chart_files.values() if v])} 张图表")
    
    # 4. 构建分析提示词
    print("\n7. 构建分析提示词...")
    prompt = build_analysis_prompt(df)
    print(f"  ✓ 提示词构建完成，共 {len(prompt)} 字符")
    
    # 5. 调用 DeepSeek 分析
    analysis = call_deepseek_analysis(prompt)
    
    if analysis:
        # 6. 生成 Hugo 博客
        hugo_path = generate_hugo_blog(df, analysis, chart_files)
        
        # 7. 显示报告预览
        print("\n" + "=" * 60)
        print("📄 分析报告内容预览")
        print("=" * 60)
        print(analysis[:1500] + "..." if len(analysis) > 1500 else analysis)
    else:
        print("\n❌ AI 分析失败，请检查 API 配置")
    
    print("\n" + "=" * 60)
    print("🎉 综合数据分析报告生成完毕！")
    print("=" * 60)

if __name__ == "__main__":
    main()
