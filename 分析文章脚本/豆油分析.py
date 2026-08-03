import akshare as ak
import pandas as pd
import numpy as np
import requests
import time

print('=' * 60)
print('豆油期货主力合约切换与走势分析')
print('=' * 60)

# 获取豆油主力合约数据
print('\n📡 获取豆油主力合约(Y0)数据...')
y0 = ak.futures_zh_daily_sina(symbol='Y0')
y0 = y0.rename(columns={'date':'日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','volume':'成交量','hold':'持仓量','settle':'结算价'})
y0['日期'] = pd.to_datetime(y0['日期'])
print(f'最新日期: {y0["日期"].max().strftime("%Y-%m-%d")}')
print(f'最新收盘价: {y0["收盘价"].iloc[-1]:.2f} 元/吨')
print(f'最新结算价: {y0["结算价"].iloc[-1]:.2f} 元/吨')
print(f'最新持仓量: {y0["持仓量"].iloc[-1]:,.0f} 手')
print(f'近5日均价: {y0["收盘价"].tail(5).mean():.2f} 元/吨')
print(f'近20日均价: {y0["收盘价"].tail(20).mean():.2f} 元/吨')

# 获取豆二、豆粕数据
print('\n📡 获取豆二(B0)数据...')
b0 = ak.futures_zh_daily_sina(symbol='B0')
b0 = b0.rename(columns={'date':'日期','close':'收盘价'})
b0['日期'] = pd.to_datetime(b0['日期'])
print(f'豆二最新价: {b0["收盘价"].iloc[-1]:.2f} 元/吨')

print('\n📡 获取豆粕(M0)数据...')
m0 = ak.futures_zh_daily_sina(symbol='M0')
m0 = m0.rename(columns={'date':'日期','close':'收盘价'})
m0['日期'] = pd.to_datetime(m0['日期'])
print(f'豆粕最新价: {m0["收盘价"].iloc[-1]:.2f} 元/吨')

# 获取基差数据
print('\n📡 获取豆油基差数据...')
url = 'https://www.jiaoyifamen.com/tools/api//future-basis/query'
params = {'t': int(time.time() * 1000), 'type': 'Y'}
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.jiaoyifamen.com/'}
response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
latest_basis = None
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
            latest_basis = basis_val[-1]
            print(f'豆油最新基差: {latest_basis} 元/吨')
            print(f'基差日期: {cat[-1]}')
            
            y_price = y0['收盘价'].iloc[-1]
            basis_rate = (latest_basis / y_price) * 100
            print(f'豆油基差率: {basis_rate:.2f}%')

# 获取汇率数据
print('\n📡 获取汇率数据...')
usd_rate = None
try:
    usd_cny = ak.currency_boc_sina('美元')
    if not usd_cny.empty:
        print(f'汇率数据列: {list(usd_cny.columns)}')
        if '现汇卖出价' in usd_cny.columns:
            usd_rate = usd_cny['现汇卖出价'].iloc[-1]
        elif '现汇买入价' in usd_cny.columns:
            usd_rate = usd_cny['现汇买入价'].iloc[-1]
        elif len(usd_cny.columns) > 0:
            usd_rate = usd_cny.iloc[-1, -1]
        print(f'美元兑人民币汇率: {usd_rate:.4f}')
except Exception as e:
    print(f'汇率获取失败: {e}')
    usd_rate = 7.2  # 默认值

# 计算榨利
print('\n🔢 榨利计算...')
豆油产出率 = 0.185
豆粕产出率 = 0.785
压榨成本 = 150.0

盘面榨利 = y0['收盘价'].iloc[-1] * 豆油产出率 + m0['收盘价'].iloc[-1] * 豆粕产出率 - b0['收盘价'].iloc[-1] - 压榨成本
print(f'盘面榨利(不含基差): {盘面榨利:.2f} 元/吨')

if latest_basis is not None:
    m_basis_url = 'https://www.jiaoyifamen.com/tools/api//future-basis/query'
    m_params = {'t': int(time.time() * 1000), 'type': 'M'}
    m_response = requests.get(m_basis_url, params=m_params, headers=headers, timeout=30, verify=False)
    m_basis = 0
    if m_response.status_code == 200:
        m_data = m_response.json()
        if 'data' in m_data:
            for k, v in m_data['data'].items():
                if 'basis' in k.lower() and 'value' in k.lower():
                    m_basis = v[-1]
                    break
    print(f'豆粕最新基差: {m_basis} 元/吨')
    
    现货榨利 = (y0['收盘价'].iloc[-1] + latest_basis) * 豆油产出率 + (m0['收盘价'].iloc[-1] + m_basis) * 豆粕产出率 - b0['收盘价'].iloc[-1] - 压榨成本
    print(f'现货榨利(含基差): {现货榨利:.2f} 元/吨')

# 趋势分析
print('\n📊 走势分析...')
close = y0['收盘价']
ma5 = close.rolling(5).mean().iloc[-1]
ma20 = close.rolling(20).mean().iloc[-1]
ma60 = close.rolling(60).mean().iloc[-1]
print(f'5日均线: {ma5:.2f}')
print(f'20日均线: {ma20:.2f}')
print(f'60日均线: {ma60:.2f}')

if close.iloc[-1] > ma5 > ma20 > ma60:
    print('趋势判断: 多头排列，偏多')
elif close.iloc[-1] < ma5 < ma20 < ma60:
    print('趋势判断: 空头排列，偏空')
else:
    print('趋势判断: 震荡整理')

# 波动率分析
vol = close.pct_change().rolling(20).std().iloc[-1] * 100
print(f'20日波动率: {vol:.2f}%')

# 主力合约切换分析
print('\n📊 主力合约切换分析...')
contracts = ['Y2609', 'Y2605', 'Y2601', 'Y2509']
for contract in contracts:
    try:
        df = ak.futures_zh_daily_sina(symbol=contract)
        if df is not None and not df.empty:
            df = df.rename(columns={'date':'日期','close':'收盘价','hold':'持仓量'})
            df['日期'] = pd.to_datetime(df['日期'])
            print(f'{contract}: 收盘价 {df["收盘价"].iloc[-1]:.2f}, 持仓 {df["持仓量"].iloc[-1]:,.0f}')
    except:
        pass

print('\n' + '=' * 60)
