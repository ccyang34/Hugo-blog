import akshare as ak
import pandas as pd
import requests
import time
import urllib3
import os

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def 获取豆二数据():
    print("🌱 正在从新浪财经获取豆二(B0)数据...")
    try:
        df = ak.futures_zh_daily_sina(symbol="B0")
        if df.empty: return None
        df = df.rename(columns={'date': '日期', 'settle': '豆二价格'})
        df['日期'] = pd.to_datetime(df['日期'])
        return df[['日期', '豆二价格']]
    except Exception as e:
        print(f"❌ 获取豆二数据失败: {e}")
        return None

def 获取元数据(类型, 名称):
    print(f"📊 正在从交易法门获取{名称}基差数据...")
    url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
    params = {'t': int(time.time() * 1000), 'type': 类型}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    
    try:
        res = requests.get(url, params=params, headers=headers, verify=False, timeout=30)
        data = res.json().get('data', {})
        
        date_col = next((k for k in data.keys() if 'category' in k.lower()), None)
        price_col = next((k for k in data.keys() if 'price' in k.lower() and 'value' in k.lower()), None)
        basis_col = next((k for k in data.keys() if 'basis' in k.lower() and 'value' in k.lower()), None)
        
        if not (date_col and price_col and basis_col): 
            print(f"⚠️ {名称}数据列解析失败: 找到的列 {list(data.keys())}")
            print(f"原始数据样本: { {k: data[k][:3] for k in data.keys() if isinstance(data[k], list)} }")
            return None
        
        dates, prices, basis = data[date_col], data[price_col], data[basis_col]
        print(f"🔍 {名称} 原始日期样本: 前两条={dates[:2]}, 最后两条={dates[-2:]}")
        min_len = min(len(dates), len(prices), len(basis))
        
        df = pd.DataFrame({
            '原始日期': dates[:min_len],
            f'{名称}价格': prices[:min_len],
            f'{名称}基差': basis[:min_len]
        })
        
        print(f"🧐 {名称} 12-20 至 12-24 的原始记录:")
        target_dates = ['12-20', '12-21', '12-22', '12-23', '12-24']
        print(df[df['原始日期'].isin(target_dates)])

        df['日期'] = df['原始日期']
        from datetime import datetime
        curr_year = datetime.now().year
        def try_parse_date(x):
            if '-' in str(x) and len(str(x)) <= 5:
                try: return pd.to_datetime(f"{curr_year}-{x}")
                except:
                    try: return pd.to_datetime(f"{curr_year-1}-{x}")
                    except: return pd.NaT
            return pd.to_datetime(x, errors='coerce')

        df['日期'] = df['日期'].apply(try_parse_date)
        return df.dropna()
    except Exception as e:
        print(f"❌ 获取{名称}数据异常: {e}")
        return None

if __name__ == "__main__":
    b0 = 获取豆二数据()
    y = 获取元数据('Y', '豆油')
    m = 获取元数据('M', '豆粕')
    
    if b0 is None or y is None or m is None:
        print("❌ 数据获取不完整")
    else:
        # 合并数据
        df = pd.merge(y, m, on='日期', how='inner')
        df = pd.merge(df, b0, on='日期', how='inner')
        
        # 计算榨利 (简单验证)
        df['榨利'] = (df['豆油价格'] + df['豆油基差']) * 0.185 + (df['豆粕价格'] + df['豆粕基差']) * 0.785 - df['豆二价格'] - 150
        
        print("\n" + "="*50)
        print("🚀 最终合并后的数据样例 (最新5天):")
        print("="*50)
        print(df.tail().to_string(index=False))
        print("\n📊 数据总量:", len(df))
        print("📅 时间范围:", df['日期'].min().strftime('%Y-%m-%d'), "至", df['日期'].max().strftime('%Y-%m-%d'))
