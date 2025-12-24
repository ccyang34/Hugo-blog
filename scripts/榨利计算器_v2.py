#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榨利计算器 v2.0 - 改进版本
功能：获取豆油豆粕豆二数据，计算榨利，生成分析报告和博客文章
作者：CCY
版本：2.0
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import json
import requests
import time
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = [
    'SimHei', 'Microsoft YaHei', 'SimSun', 'FangSong',
    'STHeiti', 'PingFang HK', 'PingFang SC', 'Heiti TC', 'Arial Unicode MS'
]
plt.rcParams['axes.unicode_minus'] = False

class 榨利计算器V2:
    """榨利计算器改进版"""
    
    def __init__(self, 保留天数=180):
        """
        初始化
        Args:
            保留天数: 保留数据的天数，默认180天（半年）
        """
        self.保留天数 = 保留天数
        
        # 压榨产出比例
        self.豆油产出率 = 0.185  # 18.5%
        self.豆粕产出率 = 0.785  # 78.5%
        
        # 压榨成本（元/吨）
        self.压榨成本 = 150.0
        
        # 数据存储路径
        self.数据目录 = "data"
        self.图表目录 = "charts"
        self.博客目录 = "blog"
        
        # 创建目录
        for 目录 in [self.数据目录, self.图表目录, self.博客目录]:
            if not os.path.exists(目录):
                os.makedirs(目录)
        
        print("🚀 榨利计算器V2.0初始化完成")
        print(f"💰 压榨成本: {self.压榨成本} 元/吨")
        print(f"📅 数据保留期: {self.保留天数} 天")
    
    def 获取豆二数据(self):
        """获取豆二期货数据"""
        print("\n🌱 开始获取豆二期货数据...")
        
        try:
            # 获取豆二主力合约数据
            豆二数据 = ak.futures_zh_daily_sina(symbol="B0")
            
            if 豆二数据.empty:
                print("❌ 获取的豆二数据为空")
                return None
            
            print(f"✅ 成功获取豆二数据，共 {len(豆二数据)} 条记录")
            
            # 重命名列名
            豆二数据 = 豆二数据.rename(columns={
                'date': '日期',
                'open': '开盘价',
                'high': '最高价', 
                'low': '最低价',
                'close': '收盘价',
                'volume': '成交量',
                'hold': '持仓量',
                'settle': '结算价'
            })
            
            # 使用收盘价作为豆二价格
            豆二数据['豆二价格'] = 豆二数据['收盘价']
            豆二数据 = 豆二数据[['日期', '豆二价格']]
            豆二数据['日期'] = pd.to_datetime(豆二数据['日期'])
            
            # 按日期排序
            豆二数据 = 豆二数据.sort_values('日期')
            
            return 豆二数据
            
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None
    
    def 获取元爬虫数据(self, 产品类型='Y'):
        """获取豆油或豆粕数据"""
        产品映射 = {'Y': '豆油', 'M': '豆粕'}
        产品名称 = 产品映射.get(产品类型, '未知产品')
        
        print(f"\n📊 开始获取{产品名称}数据...")
        
        # API配置
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {
            't': int(time.time() * 1000),
            'type': 产品类型
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.jiaoyifamen.com/variety/varieties-varieties',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        try:
            # 发送请求
            response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
            
            if response.status_code == 200:
                print(f"✅ {产品名称}数据获取成功!")
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
        if not 原始数据 or 'data' not in 原始数据:
            return None
        
        数据内容 = 原始数据['data']
        
        # 查找数据字段
        日期数据 = None
        价格数据 = None
        基差数据 = None
        
        for 字段名 in 数据内容.keys():
            if 'category' in 字段名.lower():
                日期数据 = 数据内容[字段名]
            elif 'price' in 字段名.lower() and 'value' in 字段名.lower():
                价格数据 = 数据内容[字段名]
            elif 'basis' in 字段名.lower() and 'value' in 字段名.lower():
                基差数据 = 数据内容[字段名]
        
        if not (日期数据 and 价格数据 and 基差数据):
            return None
        
        # 创建DataFrame
        产品数据 = pd.DataFrame({
            '日期': 日期数据,
            '价格': 价格数据,
            '基差': 基差数据
        })
        
        # 数据清洗
        产品数据 = 产品数据[
            (产品数据['价格'] != 0) & 
            (产品数据['基差'] != 0) &
            (产品数据['价格'].notna()) &
            (产品数据['基差'].notna())
        ]
        
        # 处理日期
        try:
            产品数据['日期'] = pd.to_datetime(产品数据['日期'])
        except:
            # 如果日期格式不标准，尝试其他方法
            产品数据['日期'] = pd.to_datetime(产品数据['日期'], errors='coerce')
            产品数据 = 产品数据.dropna(subset=['日期'])
        
        # 排序
        产品数据 = 产品数据.sort_values('日期')
        
        # 根据产品类型重命名列
        if 产品类型 == 'Y':
            产品数据 = 产品数据.rename(columns={
                '价格': '豆油价格',
                '基差': '豆油基差'
            })
        elif 产品类型 == 'M':
            产品数据 = 产品数据.rename(columns={
                '价格': '豆粕价格',
                '基差': '豆粕基差'
            })
        
        return 产品数据
    
    def 合并并过滤数据(self, 豆油数据, 豆粕数据, 豆二数据):
        """合并数据并过滤到指定天数"""
        print("\n🔄 开始合并和过滤数据...")
        
        # 合并数据
        合并数据 = pd.merge(豆油数据, 豆粕数据, on='日期', how='inner')
        合并数据 = pd.merge(合并数据, 豆二数据, on='日期', how='inner')
        
        # 按日期排序
        合并数据 = 合并数据.sort_values('日期')
        
        # 过滤到指定天数
        最新日期 = 合并数据['日期'].max()
        过滤日期 = 最新日期 - timedelta(days=self.保留天数)
        过滤数据 = 合并数据[合并数据['日期'] >= 过滤日期].copy()
        
        print(f"✅ 数据合并完成，过滤后共 {len(过滤数据)} 条记录")
        print(f"📅 时间范围: {过滤数据['日期'].min().strftime('%Y-%m-%d')} 至 {过滤数据['日期'].max().strftime('%Y-%m-%d')}")
        
        return 过滤数据
    
    def 计算榨利(self, 数据):
        """计算榨利"""
        print("\n🧮 开始计算榨利...")
        
        # 计算现货价格
        数据['豆油现货价格'] = 数据['豆油价格'] + 数据['豆油基差']
        数据['豆粕现货价格'] = 数据['豆粕价格'] + 数据['豆粕基差']
        
        # 榨利计算
        数据['榨利'] = (
            数据['豆油现货价格'] * self.豆油产出率 + 
            数据['豆粕现货价格'] * self.豆粕产出率 - 
            数据['豆二价格'] - 
            self.压榨成本
        )
        
        # 榨利率
        数据['榨利率'] = (数据['榨利'] / 数据['豆二价格']) * 100
        
        # 榨利状态
        数据['榨利状态'] = 数据['榨利'].apply(
            lambda x: '盈利' if x > 0 else ('亏损' if x < 0 else '盈亏平衡')
        )
        
        print(f"✅ 榨利计算完成")
        print(f"💰 榨利范围: {数据['榨利'].min():.2f} 至 {数据['榨利'].max():.2f}")
        print(f"📊 平均榨利: {数据['榨利'].mean():.2f}")
        
        return 数据
    
    def 绘制半年走势图(self, 数据):
        """绘制半年榨利走势图"""
        print("\n📊 绘制半年榨利走势图...")
        
        时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        图表文件 = f"{self.图表目录}/榨利走势图_半年_{时间戳}.png"
        
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'榨利分析走势图（近{self.保留天数}天）', fontsize=16, fontweight='bold')
        
        # 1. 期货价格走势
        ax1.plot(数据['日期'], 数据['豆油价格'], label='豆油价格', color='red', linewidth=1.5)
        ax1.plot(数据['日期'], 数据['豆粕价格'], label='豆粕价格', color='blue', linewidth=1.5)
        ax1.plot(数据['日期'], 数据['豆二价格'], label='豆二价格', color='green', linewidth=1.5)
        ax1.set_title('期货价格走势', fontsize=12)
        ax1.set_ylabel('价格(元/吨)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 2. 基差走势
        ax2.plot(数据['日期'], 数据['豆油基差'], label='豆油基差', color='red', linewidth=1.5)
        ax2.plot(数据['日期'], 数据['豆粕基差'], label='豆粕基差', color='blue', linewidth=1.5)
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_title('现货基差走势', fontsize=12)
        ax2.set_ylabel('基差(元/吨)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 3. 榨利走势
        colors = ['red' if x < 0 else 'green' for x in 数据['榨利']]
        ax3.bar(数据['日期'], 数据['榨利'], color=colors, alpha=0.7, width=0.8)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax3.set_title('榨利走势', fontsize=12)
        ax3.set_ylabel('榨利(元/吨)')
        ax3.grid(True, alpha=0.3)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        
        # 4. 榨利分布
        ax4.hist(数据['榨利'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax4.axvline(x=数据['榨利'].mean(), color='red', linestyle='--', 
                   label=f'平均值: {数据["榨利"].mean():.2f}')
        ax4.axvline(x=0, color='black', linestyle='-', linewidth=1, label='盈亏平衡')
        ax4.set_title('榨利分布', fontsize=12)
        ax4.set_xlabel('榨利(元/吨)')
        ax4.set_ylabel('频次')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 调整布局
        plt.tight_layout()
        
        # 添加公式信息
        公式文本 = (
            f"榨利计算公式:\n"
            f"榨利 = (豆油现货价格 × 0.185 + 豆粕现货价格 × 0.785) - 豆二价格 - {self.压榨成本}元/吨\n"
            f"数据更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        fig.text(0.02, 0.02, 公式文本, fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        # 保存图表
        plt.savefig(图表文件, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 半年走势图已保存: {图表文件}")
        return 图表文件
    
    def 生成分析报告(self, 数据):
        """生成详细分析报告"""
        print("\n📈 生成分析报告...")
        
        时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        报告文件 = f"{self.数据目录}/榨利分析报告_{时间戳}.txt"
        
        # 计算统计数据
        盈利天数 = len(数据[数据['榨利'] > 0])
        亏损天数 = len(数据[数据['榨利'] < 0])
        盈亏平衡天数 = len(数据[数据['榨利'] == 0])
        总天数 = len(数据)
        盈利比例 = 盈利天数 / 总天数 * 100 if 总天数 > 0 else 0
        
        # 榨利统计
        榨利均值 = 数据['榨利'].mean()
        榨利标准差 = 数据['榨利'].std()
        榨利最大值 = 数据['榨利'].max()
        榨利最小值 = 数据['榨利'].min()
        
        # 相关性分析
        相关性矩阵 = 数据[['豆油价格', '豆粕价格', '豆二价格', '榨利']].corr()
        
        报告内容 = f"""榨利分析报告
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
数据来源: 元爬虫(豆油豆粕) + akshare(豆二)
分析周期: 近{self.保留天数}天

📊 数据概况
总记录数: {总天数:,} 条
时间范围: {数据['日期'].min().strftime('%Y-%m-%d')} 至 {数据['日期'].max().strftime('%Y-%m-%d')}

💰 价格统计
豆油价格: {数据['豆油价格'].min():.2f} - {数据['豆油价格'].max():.2f} (平均: {数据['豆油价格'].mean():.2f})
豆粕价格: {数据['豆粕价格'].min():.2f} - {数据['豆粕价格'].max():.2f} (平均: {数据['豆粕价格'].mean():.2f})
豆二价格: {数据['豆二价格'].min():.2f} - {数据['豆二价格'].max():.2f} (平均: {数据['豆二价格'].mean():.2f})

📈 榨利分析
榨利范围: {榨利最小值:.2f} - {榨利最大值:.2f}
平均榨利: {榨利均值:.2f} 元/吨
榨利标准差: {榨利标准差:.2f}
榨利率范围: {数据['榨利率'].min():.2f}% - {数据['榨利率'].max():.2f}%
平均榨利率: {数据['榨利率'].mean():.2f}%

📊 盈利情况
盈利天数: {盈利天数} 天 ({盈利比例:.1f}%)
亏损天数: {亏损天数} 天 ({亏损天数/总天数*100:.1f}%)
盈亏平衡天数: {盈亏平衡天数} 天 ({盈亏平衡天数/总天数*100:.1f}%)

🔗 相关性分析
豆油-豆粕价格相关性: {相关性矩阵.loc['豆油价格', '豆粕价格']:.4f}
豆油-豆二价格相关性: {相关性矩阵.loc['豆油价格', '豆二价格']:.4f}
豆粕-豆二价格相关性: {相关性矩阵.loc['豆粕价格', '豆二价格']:.4f}
榨利-豆二价格相关性: {相关性矩阵.loc['榨利', '豆二价格']:.4f}

📅 最新数据
最新日期: {数据['日期'].max().strftime('%Y-%m-%d')}
最新榨利: {数据['榨利'].iloc[-1]:.2f} 元/吨
最新榨利率: {数据['榨利率'].iloc[-1]:.2f}%

计算公式:
榨利 = (豆油现货价格 × 0.185 + 豆粕现货价格 × 0.785) - 豆二价格 - {self.压榨成本}元/吨
榨利率 = (榨利 / 豆二价格) × 100%

压榨参数:
豆油产出率: {self.豆油产出率*100}%
豆粕产出率: {self.豆粕产出率*100}%
压榨成本: {self.压榨成本} 元/吨
"""
        
        with open(报告文件, 'w', encoding='utf-8') as f:
            f.write(报告内容)
        
        print(f"✅ 分析报告已生成: {报告文件}")
        return 报告文件
    
    def 生成博客文章(self, 数据, 图表文件, 报告文件):
        """生成博客文章"""
        print("\n📝 生成博客文章...")
        
        时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 计算统计数据
        盈利天数 = len(数据[数据['榨利'] > 0])
        总天数 = len(数据)
        盈利比例 = 盈利天数 / 总天数 * 100 if 总天数 > 0 else 0
        
        # 获取文件名（不含路径）
        图表文件名 = os.path.basename(图表文件)
        报告文件名 = os.path.basename(报告文件)
        
        博客内容 = f"""---
title: "榨利分析报告 - {datetime.now().strftime('%Y年%m月%d日')}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
description: "大豆压榨利润分析报告，基于豆油、豆粕、豆二期货数据"
tags: ["榨利分析", "大豆期货", "农产品", "期货分析"]
categories: ["期货分析"]
draft: false
---

## 📊 榨利分析报告

本报告基于近**{self.保留天数}天**的大豆压榨相关数据，分析大豆压榨利润的变化趋势。

### 🔢 核心数据

- **分析周期**: {数据['日期'].min().strftime('%Y年%m月%d日')} - {数据['日期'].max().strftime('%Y年%m月%d日')}
- **数据记录**: {len(数据):,} 条
- **平均榨利**: {数据['榨利'].mean():.2f} 元/吨
- **盈利天数**: {盈利天数} 天 ({盈利比例:.1f}%)

### 💰 价格走势

![榨利走势图]({图表文件名})

### 📈 关键指标

| 指标 | 豆油价格 | 豆粕价格 | 豆二价格 | 榨利 |
|------|----------|----------|----------|------|
| 最小值 | {数据['豆油价格'].min():.2f} | {数据['豆粕价格'].min():.2f} | {数据['豆二价格'].min():.2f} | {数据['榨利'].min():.2f} |
| 最大值 | {数据['豆油价格'].max():.2f} | {数据['豆粕价格'].max():.2f} | {数据['豆二价格'].max():.2f} | {数据['榨利'].max():.2f} |
| 平均值 | {数据['豆油价格'].mean():.2f} | {数据['豆粕价格'].mean():.2f} | {数据['豆二价格'].mean():.2f} | {数据['榨利'].mean():.2f} |

### 🎯 榨利分析

#### 盈利状况
- **盈利天数**: {盈利天数} 天 ({盈利比例:.1f}%)
- **亏损天数**: {len(数据[数据['榨利'] < 0])} 天 ({len(数据[数据['榨利'] < 0])/总天数*100:.1f}%)
- **盈亏平衡**: {len(数据[数据['榨利'] == 0])} 天

#### 榨利分布
- **最高榨利**: {数据['榨利'].max():.2f} 元/吨
- **最低榨利**: {数据['榨利'].min():.2f} 元/吨
- **平均榨利**: {数据['榨利'].mean():.2f} 元/吨
- **榨利波动性**: {数据['榨利'].std():.2f}

### 🔗 相关性分析

价格相关性矩阵显示各品种间的相关关系：

- **豆油-豆粕相关性**: {数据['豆油价格'].corr(数据['豆粕价格']):.4f}
- **豆油-豆二相关性**: {数据['豆油价格'].corr(数据['豆二价格']):.4f}
- **豆粕-豆二相关性**: {数据['豆粕价格'].corr(数据['豆二价格']):.4f}

### 📊 计算公式

榨利计算采用以下公式：

```
榨利 = (豆油现货价格 × 18.5% + 豆粕现货价格 × 78.5%) - 豆二价格 - 压榨成本
```

其中：
- **豆油产出率**: 18.5%
- **豆粕产出率**: 78.5%
- **压榨成本**: {self.压榨成本} 元/吨

### 📅 数据更新

- **报告生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
- **数据来源**: 元爬虫(豆油豆粕) + akshare(豆二)
- **详细报告**: [{报告文件名}]({报告文件名})

---

*本报告基于公开市场数据，仅供参考，不构成投资建议。*
"""
        
        # 保存博客文章
        博客文件 = f"{self.博客目录}/榨利分析报告_{时间戳}.md"
        with open(博客文件, 'w', encoding='utf-8') as f:
            f.write(博客内容)
        
        print(f"✅ 博客文章已生成: {博客文件}")
        return 博客文件
    
    def 保存数据(self, 数据):
        """保存原始数据"""
        时间戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        数据文件 = f"{self.数据目录}/榨利数据_{时间戳}.csv"
        数据.to_csv(数据文件, index=False, encoding='utf-8')
        print(f"✅ 原始数据已保存: {数据文件}")
        return 数据文件
    
    def 运行完整分析(self):
        """运行完整的榨利分析流程"""
        print("=" * 80)
        print("🚀 榨利计算器V2.0 - 开始完整分析流程")
        print("=" * 80)
        
        try:
            # 1. 获取数据
            print("\n📡 第一步：获取数据")
            豆二数据 = self.获取豆二数据()
            豆油数据 = self.获取元爬虫数据('Y')
            豆粕数据 = self.获取元爬虫数据('M')
            
            if any(x is None for x in [豆二数据, 豆油数据, 豆粕数据]):
                print("❌ 数据获取失败，流程终止")
                return None
            
            # 2. 合并和过滤数据
            print("\n🔄 第二步：合并和过滤数据")
            合并数据 = self.合并并过滤数据(豆油数据, 豆粕数据, 豆二数据)
            
            # 3. 计算榨利
            print("\n🧮 第三步：计算榨利")
            榨利数据 = self.计算榨利(合并数据)
            
            # 4. 保存数据
            print("\n💾 第四步：保存数据")
            数据文件 = self.保存数据(榨利数据)
            
            # 5. 绘制图表
            print("\n📊 第五步：绘制图表")
            图表文件 = self.绘制半年走势图(榨利数据)
            
            # 6. 生成分析报告
            print("\n📈 第六步：生成分析报告")
            报告文件 = self.生成分析报告(榨利数据)
            
            # 7. 生成博客文章
            print("\n📝 第七步：生成博客文章")
            博客文件 = self.生成博客文章(榨利数据, 图表文件, 报告文件)
            
            print("=" * 80)
            print("✅ 榨利分析流程完成!")
            print(f"📊 数据文件: {数据文件}")
            print(f"📈 图表文件: {图表文件}")
            print(f"📝 博客文件: {博客文件}")
            print(f"📋 报告文件: {报告文件}")
            print("=" * 80)
            
            return {
                '数据文件': 数据文件,
                '图表文件': 图表文件,
                '博客文件': 博客文件,
                '报告文件': 报告文件,
                '数据': 榨利数据
            }
            
        except Exception as e:
            print(f"❌ 分析流程出错: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """主函数"""
    print("🌟 榨利计算器V2.0")
    print("作者: CCY")
    print("功能: 榨利分析、数据可视化、博客生成")
    
    # 创建计算器实例（保留半年数据）
    计算器 = 榨利计算器V2(保留天数=180)
    
    # 运行完整分析
    结果 = 计算器.运行完整分析()
    
    if 结果:
        print("\n🎉 分析完成！请查看生成的文件：")
        for 类型, 文件 in 结果.items():
            if 类型 != '数据':
                print(f"  {类型}: {文件}")
    else:
        print("\n❌ 分析失败，请检查网络连接和数据源。")

if __name__ == "__main__":
    main()