#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆油期货历史规律深度挖掘分析
- 基差规律
- 主力合约切换规律
- 季节性规律
- 价格周期性规律
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

SCRIPT_DIR = '/Users/ccy/Hugo-Blog/分析文章脚本'
HUGO_IMAGES_DIR = '/Users/ccy/Hugo-Blog/static/images/charts'
import os
os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)

class 豆油历史规律分析:
    """豆油期货历史规律深度挖掘"""
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.jiaoyifamen.com/'}
        print("=" * 70)
        print("🫘 豆油期货历史规律深度挖掘分析")
        print("=" * 70)
    
    def 获取历史数据(self, symbol, name):
        """获取期货历史数据"""
        print(f"\n📡 获取{name}({symbol})历史数据...")
        try:
            df = ak.futures_zh_daily_sina(symbol=symbol)
            if df is None or df.empty:
                return None
            df = df.rename(columns={
                'date': '日期', 'open': '开盘', 'high': '最高', 
                'low': '最低', 'close': '收盘', 'volume': '成交量',
                'hold': '持仓量', 'settle': '结算'
            })
            df['日期'] = pd.to_datetime(df['日期'])
            df = df.sort_values('日期').reset_index(drop=True)
            print(f"  ✅ 获取成功，数据范围: {df['日期'].min().strftime('%Y-%m-%d')} ~ {df['日期'].max().strftime('%Y-%m-%d')}")
            print(f"  ✅ 共 {len(df)} 个交易日")
            return df
        except Exception as e:
            print(f"  ❌ 获取失败: {e}")
            return None
    
    def 获取基差历史(self, 产品类型):
        """获取基差历史数据"""
        print(f"\n📡 获取{'豆油' if 产品类型 == 'Y' else '豆粕'}基差历史数据...")
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        params = {'t': int(time.time() * 1000), 'type': 产品类型}
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=30, verify=False)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    cat = data['data'].get('category', [])
                    basis_val = None
                    for k, v in data['data'].items():
                        if 'basis' in k.lower() and 'value' in k.lower():
                            basis_val = v
                            break
                    if cat and basis_val:
                        curr_year = datetime.now().year
                        dates = []
                        for x in cat:
                            if isinstance(x, str) and '-' in x:
                                try:
                                    dates.append(pd.to_datetime(f"{curr_year}-{x}"))
                                except:
                                    dates.append(pd.NaT)
                            else:
                                dates.append(pd.to_datetime(x, errors='coerce'))
                        
                        df = pd.DataFrame({'日期': dates[:len(basis_val)], '基差': basis_val})
                        df = df.dropna()
                        df['基差'] = pd.to_numeric(df['基差'], errors='coerce')
                        if len(df) > 0:
                            print(f"  ✅ 获取成功，共 {len(df)} 条基差记录")
                            return df
            print(f"  ⚠️ 基差数据为空或获取失败")
        except Exception as e:
            print(f"  ❌ 获取失败: {e}")
        return pd.DataFrame({'日期': [], '基差': []})
    
    def 分析主力合约切换规律(self):
        """分析主力合约切换规律"""
        print("\n" + "=" * 70)
        print("📊 主力合约切换规律分析")
        print("=" * 70)
        
        # 获取各合约数据
        contracts = ['Y2509', 'Y2601', 'Y2605', 'Y2609', 'Y2701', 'Y2705', 'Y2709']
        contract_data = {}
        
        for contract in contracts:
            df = self.获取历史数据(contract, contract)
            if df is not None:
                contract_data[contract] = df
        
        if not contract_data:
            print("❌ 无合约数据")
            return None
        
        # 分析切换规律
        print("\n📈 主力合约持仓量变化:")
        results = []
        for contract, df in sorted(contract_data.items()):
            if '持仓量' in df.columns:
                max_hold = df['持仓量'].max()
                max_date = df.loc[df['持仓量'].idxmax(), '日期']
                first_date = df['日期'].min()
                last_date = df['日期'].max()
                results.append({
                    '合约': contract,
                    '首日': first_date.strftime('%Y-%m-%d'),
                    '末日': last_date.strftime('%Y-%m-%d'),
                    '最大持仓': max_hold,
                    '最大持仓日': max_date.strftime('%Y-%m-%d')
                })
        
        results_df = pd.DataFrame(results)
        print(results_df.to_string(index=False))
        
        # 规律总结
        print("\n📋 主力合约切换规律总结:")
        if len(results) >= 2:
            # 计算合约切换间隔
            for i in range(1, len(results)):
                prev_end = pd.to_datetime(results[i-1]['末日'])
                curr_start = pd.to_datetime(results[i]['首日'])
                days_diff = (curr_start - prev_end).days
                print(f"  {results[i-1]['合约']} → {results[i]['合约']}: 间隔 {days_diff} 天")
        
        return results_df
    
    def 分析基差规律(self):
        """分析基差历史规律"""
        print("\n" + "=" * 70)
        print("📊 基差规律深度分析")
        print("=" * 70)
        
        y_basis = self.获取基差历史('Y')
        m_basis = self.获取基差历史('M')
        
        if y_basis is None or len(y_basis) == 0:
            print("❌ 无法获取豆油基差数据")
            return None
        
        # 基本统计
        print("\n📈 豆油基差基本统计:")
        print(f"  均值: {y_basis['基差'].mean():.2f} 元/吨")
        print(f"  中位数: {y_basis['基差'].median():.2f} 元/吨")
        print(f"  标准差: {y_basis['基差'].std():.2f} 元/吨")
        print(f"  最大值: {y_basis['基差'].max():.2f} 元/吨")
        print(f"  最小值: {y_basis['基差'].min():.2f} 元/吨")
        
        # 百分位分析
        print("\n📊 基差百分位分析:")
        percentiles = [10, 25, 50, 75, 90]
        for p in percentiles:
            vals = y_basis['基差'].dropna()
            if len(vals) > 0:
                val = np.percentile(vals, p)
                print(f"  P{p}: {val:.2f} 元/吨")
        
        # 正负基差天数统计
        positive_days = (y_basis['基差'] > 0).sum()
        negative_days = (y_basis['基差'] < 0).sum()
        total = len(y_basis)
        print(f"\n📈 基差方向统计:")
        print(f"  现货升水(基差>0): {positive_days} 天 ({positive_days/total*100:.1f}%)")
        print(f"  现货贴水(基差<0): {negative_days} 天 ({negative_days/total*100:.1f}%)")
        
        # 月度基差规律
        if '日期' in y_basis.columns and len(y_basis) > 0:
            y_basis = y_basis.copy()
            y_basis['月份'] = y_basis['日期'].dt.month
            monthly = y_basis.groupby('月份')['基差'].agg(['mean', 'std', 'count'])
            print("\n📅 月度基差均值规律:")
            month_names = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
            for m in range(1, 13):
                if m in monthly.index and not pd.isna(monthly.loc[m,'mean']):
                    print(f"  {month_names[m-1]}: 均值={monthly.loc[m,'mean']:.1f}, 样本={monthly.loc[m,'count']:.0f}")
        
        return y_basis
    
    def 分析季节性规律(self, df):
        """分析价格季节性规律"""
        print("\n" + "=" * 70)
        print("📊 价格季节性规律分析")
        print("=" * 70)
        
        if df is None or '收盘' not in df.columns:
            print("❌ 无价格数据")
            return None
        
        # 添加时间特征
        df = df.copy()
        df['月份'] = df['日期'].dt.month
        df['年份'] = df['日期'].dt.year
        df['周'] = df['日期'].dt.isocalendar().week
        
        # 月度收益率
        print("\n📅 月度价格收益率规律:")
        month_names = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        monthly_ret = df.groupby('月份')['收盘'].last() / df.groupby('月份')['收盘'].first() - 1
        for m in range(1, 13):
            if m in monthly_ret.index:
                ret = monthly_ret[m] * 100
                sign = '+' if ret > 0 else ''
                print(f"  {month_names[m-1]}: {sign}{ret:.1f}%")
        
        # 季度规律
        df['季度'] = (df['月份'] - 1) // 3 + 1
        print("\n📅 季度价格规律:")
        quarterly = df.groupby('季度')['收盘'].agg(['first', 'last', 'mean'])
        for q in [1, 2, 3, 4]:
            if q in quarterly.index:
                q_ret = (quarterly.loc[q, 'last'] / quarterly.loc[q, 'first'] - 1) * 100
                q_avg = quarterly.loc[q, 'mean']
                sign = '+' if q_ret > 0 else ''
                print(f"  Q{q}: 均价={q_avg:.0f}, 季度涨跌={sign}{q_ret:.1f}%")
        
        # 年度规律
        print("\n📅 年度涨跌规律:")
        yearly = df.groupby('年份')['收盘'].agg(['first', 'last'])
        yearly_ret = (yearly['last'] / yearly['first'] - 1) * 100
        for year in sorted(yearly_ret.index):
            ret = yearly_ret[year]
            sign = '+' if ret > 0 else ''
            print(f"  {year}年: {sign}{ret:.1f}%")
        
        return df
    
    def 分析波动率规律(self, df):
        """分析波动率规律"""
        print("\n" + "=" * 70)
        print("📊 波动率规律分析")
        print("=" * 70)
        
        if df is None:
            return None
        
        df = df.copy()
        df['日收益'] = df['收盘'].pct_change() * 100
        df['波动率'] = df['日收益'].rolling(20).std()
        
        print("\n📈 月度波动率均值:")
        df['月份'] = df['日期'].dt.month
        monthly_vol = df.groupby('月份')['波动率'].mean()
        month_names = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        for m in range(1, 13):
            if m in monthly_vol.index and not np.isnan(monthly_vol[m]):
                print(f"  {month_names[m-1]}: {monthly_vol[m]:.2f}%")
        
        return df
    
    def 绘制综合分析图(self, y_df, m_df, y_basis):
        """绘制综合分析图表"""
        print("\n📊 绘制综合分析图表...")
        
        fig, axes = plt.subplots(3, 2, figsize=(16, 14))
        fig.suptitle('豆油期货历史规律综合分析', fontsize=16, fontweight='bold')
        
        # 1. 价格走势与均线
        ax1 = axes[0, 0]
        if y_df is not None and not y_df.empty:
            ax1.plot(y_df['日期'], y_df['收盘'], 'b-', linewidth=0.8, label='收盘价')
            if len(y_df) > 60:
                ma60 = y_df['收盘'].rolling(60).mean()
                ax1.plot(y_df['日期'], ma60, 'r--', linewidth=1, label='60日均线')
            ax1.set_title('豆油期货价格走势', fontsize=12)
            ax1.set_ylabel('价格(元/吨)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # 2. 基差走势
        ax2 = axes[0, 1]
        if y_basis is not None and not y_basis.empty:
            ax2.bar(y_basis['日期'], y_basis['基差'], width=1, color=['green' if x > 0 else 'red' for x in y_basis['基差']], alpha=0.7)
            ax2.axhline(0, color='black', linestyle='-', linewidth=0.5)
            ax2.set_title('豆油基差走势', fontsize=12)
            ax2.set_ylabel('基差(元/吨)')
            ax2.grid(True, alpha=0.3)
            
            # 添加均值线
            mean_basis = y_basis['基差'].mean()
            ax2.axhline(mean_basis, color='blue', linestyle='--', label=f'均值:{mean_basis:.0f}')
            ax2.legend()
        
        # 3. 月度收益率热力图
        ax3 = axes[1, 0]
        if y_df is not None and not y_df.empty:
            y_df = y_df.copy()
            y_df['年份'] = y_df['日期'].dt.year
            y_df['月份'] = y_df['日期'].dt.month
            
            # 计算月度收益率
            monthly_ret = []
            for year in sorted(y_df['年份'].unique()):
                year_data = y_df[y_df['年份'] == year]
                monthly = year_data.groupby('月份')['收盘'].agg(['first', 'last'])
                for m in range(1, 13):
                    if m in monthly.index:
                        ret = (monthly.loc[m, 'last'] / monthly.loc[m, 'first'] - 1) * 100 if monthly.loc[m, 'first'] > 0 else 0
                        monthly_ret.append({'年份': year, '月份': m, '收益率': ret})
            
            if monthly_ret:
                ret_df = pd.DataFrame(monthly_ret)
                pivot = ret_df.pivot(index='年份', columns='月份', values='收益率')
                im = ax3.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=-10, vmax=10)
                ax3.set_xticks(range(12))
                ax3.set_xticklabels(['1','2','3','4','5','6','7','8','9','10','11','12'])
                ax3.set_yticks(range(len(pivot)))
                ax3.set_yticklabels(pivot.index)
                ax3.set_title('月度收益率热力图(%)', fontsize=12)
                plt.colorbar(im, ax=ax3, label='收益率%')
        
        # 4. 主力合约持仓量对比
        ax4 = axes[1, 1]
        contracts = ['Y2509', 'Y2601', 'Y2605', 'Y2609']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        for i, contract in enumerate(contracts):
            try:
                df = ak.futures_zh_daily_sina(symbol=contract)
                if df is not None and not df.empty:
                    ax4.plot(df['date'], df['hold'], label=contract, linewidth=1, color=colors[i % len(colors)])
            except:
                pass
        ax4.set_title('主力合约持仓量对比', fontsize=12)
        ax4.set_ylabel('持仓量(手)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. 价格分布
        ax5 = axes[2, 0]
        if y_df is not None and not y_df.empty:
            ax5.hist(y_df['收盘'].dropna(), bins=50, color='steelblue', alpha=0.7, edgecolor='white')
            mean_price = y_df['收盘'].mean()
            ax5.axvline(mean_price, color='red', linestyle='--', label=f'均值:{mean_price:.0f}')
            ax5.axvline(y_df['收盘'].median(), color='green', linestyle='--', label=f'中位数:{y_df["收盘"].median():.0f}')
            ax5.set_title('价格分布', fontsize=12)
            ax5.set_xlabel('价格(元/吨)')
            ax5.legend()
        
        # 6. 榨利历史
        ax6 = axes[2, 1]
        if y_df is not None and not y_df.empty and m_df is not None and not m_df.empty:
            # 合并数据计算榨利
            merged = pd.merge(y_df[['日期', '收盘']].rename(columns={'收盘': '豆油'}),
                             m_df[['日期', '收盘']].rename(columns={'收盘': '豆粕'}),
                             on='日期', how='inner')
            
            # 简化榨利计算
            merged['榨利'] = merged['豆油'] * 0.185 + merged['豆粕'] * 0.785 - 3670 - 150
            ax6.fill_between(merged['日期'], 0, merged['榨利'], 
                            where=(merged['榨利'] > 0), color='green', alpha=0.5, label='盈利')
            ax6.fill_between(merged['日期'], 0, merged['榨利'],
                            where=(merged['榨利'] <= 0), color='red', alpha=0.5, label='亏损')
            ax6.axhline(0, color='black', linewidth=0.5)
            ax6.set_title('盘面榨利历史', fontsize=12)
            ax6.set_ylabel('榨利(元/吨)')
            ax6.legend()
            ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filepath = os.path.join(HUGO_IMAGES_DIR, '豆油历史规律分析.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  ✅ 图表已保存: {filepath}")
        return filepath
    
    def 启动(self):
        """执行完整分析"""
        print("\n" + "=" * 70)
        print("🔍 开始历史规律深度挖掘")
        print("=" * 70)
        
        # 获取主数据
        y_df = self.获取历史数据('Y0', '豆油主力')
        m_df = self.获取历史数据('M0', '豆粕主力')
        b_df = self.获取历史数据('B0', '豆二主力')
        y_basis = self.获取基差历史('Y')
        
        # 执行各项分析
        self.分析主力合约切换规律()
        self.分析基差规律()
        if y_df is not None:
            self.分析季节性规律(y_df)
            self.分析波动率规律(y_df)
        
        # 绘制综合图表
        chart_path = self.绘制综合分析图(y_df, m_df, y_basis)
        
        print("\n" + "=" * 70)
        print("✅ 历史规律分析完成!")
        print("=" * 70)
        
        return {
            'y_df': y_df,
            'm_df': m_df,
            'y_basis': y_basis,
            'chart_path': chart_path
        }

if __name__ == "__main__":
    分析器 = 豆油历史规律分析()
    结果 = 分析器.启动()
