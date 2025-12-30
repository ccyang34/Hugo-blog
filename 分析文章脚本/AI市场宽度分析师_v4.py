
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import time
import os
import json
import json
import re
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# 设置中文字体，GitHub Actions 优先使用 Noto Sans CJK 
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans'] 
plt.rcParams['axes.unicode_minus'] = False


# ================= 配置区域 =================
# 请在环境变量中设置 DEEPSEEK_API_KEY，或直接在此处填入 (不推荐直接提交到代码库)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-063857d175bd48038684520e7b6ec934")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"  # DeepSeek 官方 API 地址



# Hugo 博客配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

ENABLE_HUGO_BLOG = True  # 是否启用Hugo博客保存功能
ENABLE_GIT_PUSH = os.getenv("ENABLE_GIT_PUSH", "false").lower() == "true"  # 是否启用Git自动推送
GIT_COMMIT_MESSAGE = os.getenv("GIT_COMMIT_MESSAGE", "AI市场分析日报自动更新")  # Git提交信息

# 时区配置
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

def get_beijing_time():
    """获取北京时间"""
    return datetime.now(BEIJING_TZ)

# ================= 数据获取与处理 (复用 v2 核心逻辑) =================

def fetch_data(retries=3, delay=2):
    url = 'https://sckd.dapanyuntu.com/api/api/industry_ma20_analysis_page?page=0'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://sckd.dapanyuntu.com/'
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[Error] Fetching data: {e}, retrying...")
        time.sleep(delay)
    return None

def process_data(data):
    dates = data['dates']
    industries = data['industries']
    raw_data = data['data']
    parsed_data = []
    for point in raw_data:
        d_idx, i_idx, val = point
        if d_idx < len(dates) and i_idx < len(industries):
            parsed_data.append({'date': dates[d_idx], 'industry': industries[i_idx], 'value': val})
    df = pd.DataFrame(parsed_data)

    df = df.drop_duplicates(subset=['industry', 'date'])
    pivot = df.pivot(index='industry', columns='date', values='value')
    return pivot, dates

def calculate_breadth_momentum(pivot, dates):
    """
    计算市场宽度动量 (3日/5日变化)
    """
    try:
        if len(dates) < 5:
            return None
            
        current = pivot[dates[-1]]
        prev_3d = pivot[dates[-3]]
        prev_5d = pivot[dates[-5]]
        
        momentum = pd.DataFrame({
            'Current': current,
            'Change3D': current - prev_3d,
            'Change5D': current - prev_5d
        })
        
        return momentum
    except Exception as e:
        print(f"[Warning] 动量计算失败: {e}")
        return None

def analyze_market_sentiment_snapshot():
    """
    基于实时快照分析市场情绪 (涨跌比/涨停数/中位数)
    """
    print("正在分析全市场实时情绪...")
    try:
        # 获取快照 (带缓存)
        # 注意: get_market_snapshot 返回的是 dict name map, 这里我们需要 raw dataframe
        # 所以直接调用 ak.stock_zh_a_spot() 或复用逻辑
        df = ak.stock_zh_a_spot()
        
        if df is None or df.empty:
            return None
            
        # df columns: 代码,名称,最新价,涨跌幅,涨跌额,成交量,成交额,振幅,最高,最低,今开,昨收...
        # 涨跌幅 column might be '涨跌幅' or 'changepercent' depending on source
        # Sina source: code, name, trade, pricechange, changepercent, buy, sell, settlement, open, high, low, volume, amount...
        
        # 统一列名查找
        pct_col = None
        for col in ['涨跌幅', 'changepercent', 'm:chg']:
            if col in df.columns:
                pct_col = col
                break
        
        if not pct_col:
            print("[Warning] 未找到涨跌幅列，无法分析情绪")
            return None
            
        # 清洗数据
        df[pct_col] = pd.to_numeric(df[pct_col], errors='coerce').fillna(0)
        
        total_count = len(df)
        up_count = len(df[df[pct_col] > 0])
        down_count = len(df[df[pct_col] < 0])
        flat_count = len(df[df[pct_col] == 0])
        
        limit_up = len(df[df[pct_col] > 9.5])
        limit_down = len(df[df[pct_col] < -9.5])
        
        median_change = df[pct_col].median()
        mean_change = df[pct_col].mean()
        
        # 成交额 (如果有)
        amount_col = None
        for col in ['成交额', 'amount']:
            if col in df.columns:
                amount_col = col
                break
        
        total_amount = 0
        if amount_col:
             total_amount = pd.to_numeric(df[amount_col], errors='coerce').sum()
        
        sentiment = {
            'total': total_count,
            'up': up_count,
            'down': down_count,
            'flat': flat_count,
            'limit_up': limit_up,
            'limit_down': limit_down,
            'median_change': median_change,
            'mean_change': mean_change,
            'total_amount': total_amount
        }
        
        print(f"情绪分析完成: 涨{up_count}/跌{down_count}, 涨停{limit_up}")
        return sentiment
        
    except Exception as e:
        print(f"[Warning] 情绪分析失败: {e}")
        return None

def get_sector_map():
    """
    行业板块分类映射表 (优化版)
    
    分类逻辑：
    - 科技成长：政策支持+高成长+高估值
    - 可选消费：经济ngood时表现强势，受消费能力影响
    - 必选消费医药：防御属性+刚需，经济下行中相对抗跌
    - 能源资源：大宗商品+传统周期，受商品价格驱动
    - 高端制造：新能源+智能制造，受政策扶持+技术创新驱动
    - 传统制造：低端制造+建材，传统周期属性
    - 大金融：金融全板块
    - 基建物流：逆周期调节+政策对冲
    - 公用事业：防御+稳定分红
    - 房地产链：地产及后周期行业
    - 贸易综合：难以归类的综合性板块
    """
    return {
        # 1. 科技成长板块（政策支持+高成长+高估值）
        '科技成长': [
            # 半导体产业链
            '半导体', '电子元件', '光学光电子', '电子化学品',
            # 计算机与软件
            '计算机设备', '软件开发', '互联网服务',
            # 通信产业链
            '通信设备', '通信服务',
            # 新兴科技
            '消费电子'  # 保留在科技成长中，更符合产业属性
        ],
        
        # 2. 可选消费（经济ngood时表现强势）
        '可选消费': [
            # 高端消费
            '酿酒行业', 
            # 耐用消费品
            '家电行业', '珠宝首饰',
            # 汽车产业链
            '汽车整车', '汽车零部件', '汽车服务',
            # 休闲服务
            '旅游酒店', '商业百货', '纺织服装', '文化传媒', '教育',
            # 家居相关（地产后周期）
            '装修建材', '装修装饰', '家用轻工'
        ],
        
        # 3. 必选消费+医药（防御属性+刚需）
        '必选消费医药': [
            # 医药全产业链
            '医药商业', '中药', '化学制药', '生物制品', '医疗器械', '医疗服务', '美容护理',
            # 农业
            '农牧饲渔',
            # 基础消费（与高端酒类区分）
            '食品饮料'  
        ],
        
        # 4. 能源资源（大宗商品+传统周期）
        '能源资源': [
            # 能源
            '煤炭行业', '石油行业', '采掘行业',
            # 金属
            '钢铁行业', '有色金属', '贵金属', '小金属', '能源金属',
            # 基础材料
            '化学原料', '化学制品', '化纤行业', '非金属材料'
        ],
        
        # 5. 高端制造（新能源+智能制造）
        '高端制造': [
            # 新能源产业链
            '光伏设备', '风电设备', '电池', '电机', '电源设备', '电网设备',
            # 高端装备
            '专用设备', '通用设备',
            # 航空航天
            '航天航空',
            # 交运装备
            '交运设备', '船舶制造',
            # 精密制造（科技属性强）
            '仪器仪表'
        ],
        
        # 6. 传统制造（低端制造+建材）
        '传统制造': [
            # 建材建筑
            '水泥建材', 
            # 传统制造
            '塑料制品', '橡胶制品', '玻璃玻纤', '造纸印刷', '包装材料',
            # 化工相关
            '化肥行业', '农药兽药'
        ],
        
        # 7. 大金融（金融全板块）
        '大金融': [
            '银行', '证券', '保险', '多元金融'
        ],
        
        # 8. 基建物流（逆周期+政策对冲）
        '基建物流': [
            # 交通运输
            '铁路公路', '航运港口', '物流行业', '航空机场',
            # 基建工程
            '工程建设', '工程咨询服务', '工程机械',
            # 专业服务
            '专业服务'
        ],
        
        # 9. 公用事业（防御+稳定分红）
        '公用事业': [
            '公用事业', '电力行业', '燃气', '环保行业'
        ],
        
        # 10. 房地产链（独立板块）
        '房地产链': [
            # 地产开发
            '房地产开发', '房地产服务'
        ],
        
        # 11. 贸易综合（难以归类的板块）
        '贸易综合': [
            '贸易行业', '综合行业',
            # 娱乐相关（难以归类）
            '游戏'  
        ]
    }

# ================= 本地预分析 (为 AI 准备数据) =================


def prepare_context_for_ai(pivot, dates, momentum_df=None, sentiment_data=None):
    latest_date = dates[-1]
    
    # --- 1. 全市场分布统计 (Market Distribution) ---
    current_vals = pivot[latest_date]
    total_inds = len(current_vals)
    overheated = (current_vals > 80).sum()
    oversold = (current_vals < 20).sum()
    neutral = total_inds - overheated - oversold
    median_breadth = current_vals.median()
    avg_breadth = current_vals.mean()
    
    # --- 2. 构建完整历史数据矩阵 (Full History) ---
    # 使用所有可用日期，不进行截断
    full_dates = dates
    
    sector_map = get_sector_map()
    ind_to_sector = {}
    for sec, inds in sector_map.items():
        for ind in inds:
            ind_to_sector[ind] = sec
            
    # 构建 CSV 头: 行业,板块,日期1,日期2...
    history_csv_lines = [f"行业名称,所属板块,{','.join(full_dates)}"]
    
    # 按最新宽度降序排列
    sorted_inds = current_vals.sort_values(ascending=False).index
    
    for ind in sorted_inds:
        sector = ind_to_sector.get(ind, "其他")
        # 获取该行业在所有日期的值序列
        vals = pivot.loc[ind, full_dates]
        # 格式化数值，保留1位小数
        vals_str = ",".join([f"{v:.1f}" if pd.notnull(v) else "" for v in vals])
        history_csv_lines.append(f"{ind},{sector},{vals_str}")
    
    full_history_str = "\n".join(history_csv_lines)

    # --- 3. 补充动量与情绪数据 ---
    momentum_str = ""
    if momentum_df is not None:
        # 找出动量最强(Change5D Max)和动量最弱(Change5D Min)的前5名
        top_momentum = momentum_df.sort_values('Change5D', ascending=False).head(5)
        bottom_momentum = momentum_df.sort_values('Change5D', ascending=True).head(5)
        
        momentum_str = "\n[行业动量异动 (5日宽度变化)]\n"
        momentum_str += "加速向上 (Leaders):\n"
        for idx, row in top_momentum.iterrows():
            momentum_str += f"- {idx}: 当前{row['Current']:.1f}%, 5日变动+{row['Change5D']:.1f}%\n"
            
        momentum_str += "加速向下 (Laggards):\n"
        for idx, row in bottom_momentum.iterrows():
            momentum_str += f"- {idx}: 当前{row['Current']:.1f}%, 5日变动{row['Change5D']:.1f}%\n"

    sentiment_str = ""
    if sentiment_data:
        sentiment_str = f"""
    [全市场实时情绪快照]
    - 上涨家数: {sentiment_data['up']} / 下跌家数: {sentiment_data['down']}
    - 涨停家数: {sentiment_data['limit_up']} / 跌停家数: {sentiment_data['limit_down']}
    - 涨跌幅中位数: {sentiment_data['median_change']:.2f}%
    - 总成交额: {sentiment_data['total_amount']/100000000:.1f} 亿
        """

    # --- 4. 构建发送给 AI 的结构化上下文 ---
    context = f"""
    [分析基准]
    数据截止日期: {latest_date}
    包含历史天数: {len(full_dates)} 天

    [市场全景统计]
    - 全市场平均宽度: {avg_breadth:.1f}%
    - 宽度中位数: {median_breadth:.1f}%
    - 极度过热(>80%)行业数: {overheated} / {total_inds}
    - 极度冰点(<20%)行业数: {oversold} / {total_inds}
    - 正常区间(20-80%)行业数: {neutral} / {total_inds}

    {sentiment_str}

    {momentum_str}

    [全行业完整历史数据 (CSV矩阵)]
    {full_history_str}
    """
    return context

# ================= AI 分析模块 (DeepSeek) =================


def call_deepseek_analysis(context):
    if not DEEPSEEK_API_KEY or "sk-" not in DEEPSEEK_API_KEY:
        print("[Warning] 未配置 DEEPSEEK_API_KEY，跳过 AI 分析。")
        return "未配置 API Key，无法生成 AI 报告。"

    system_prompt = """你是一位拥有20年经验的A股首席策略分析师。请基于提供的全市场行业宽度数据（Market Breadth）、动量异动数据和实时市场情绪快照，撰写一份深度市场分析报告。

    **分析逻辑与要求：**

    1.  **全景定调 (The Big Picture)**:
        *   结合“实时情绪快照”（涨跌比、涨停数、中位数）判断当日盘面强弱。
        *   结合“过热/冰点”行业分布，判断市场是否处于极端位置。
        *   **关键判断**: 市场是在加速上行、高位分歧、还是底部反弹？

    2.  **结构与主线 (Structure & Rotation)**:
        *   利用**[行业动量异动]**数据，识别“加速向上”的板块。这些是当前的主线。
        *   对比“当前宽度”高但“5日变动”为负的板块，警惕高位退潮。
        *   **深度挖掘**: 找出“强中之强”（领涨行业）和“弱中之强”（底部刚启动）。
        
    3.  **异动与背离 (Divergence)**:
        *   寻找“背离”现象：例如某些高位板块虽然宽度仍高，但周变化开始转负（高位派发迹象）。
        *   寻找“广度推力”：是否有大量行业在短时间内同时大幅上涨？

    4.  **实战策略 (Actionable Strategy)**:
        *   给出具体的仓位建议（0-10成）。
        *   **进攻方向**: 具体到细分行业，优先选择动量加速向上的板块。
        *   **防御/规避**: 点名需要回避的风险板块（高位动能衰竭）。

    **输出格式要求：**
    *   使用 Markdown 格式。
    *   **必须引用数据**: 在分析时，必须引用具体的宽度数值、5日变化率或情绪指标（涨停数等）作为支撑。
    *   语气专业、客观、有洞察力。不要使用模棱两可的废话。
    *   字数控制在 800-1000 字之间，内容要详实。

    **报告结构：**
    # 深度市场宽度日报
    ## 📊 市场全景与情绪
    ## 🚀 行业动量与主线扫描
    ## ⚠️ 异动背离与风险
    ## 💡 交易策略与建议
    
    **重要：** 请在报告的最后，**必须**以 JSON 格式列出你最看好的 1-2 个具体的“进攻方向”板块名称，并为每个板块推荐 5 只最具代表性的龙头股/强势股代码（6位数字代码）。格式如下：
    ```json
    {
        "recommendations": [
            {"sector": "半导体", "stocks": ["688981", "603501", "002371", "600584", "002156"]},
            {"sector": "酿酒行业", "stocks": ["600519", "000858", "000568", "600809", "000596"]}
        ]
    }
    ```
    （请确保 JSON 格式标准，sector 与输入名称一致，stocks 为字符串列表）
    """

    user_prompt = f"这是最新的全市场行业宽度数据，请开始分析：\n{context}"

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5, # 降低温度以增加分析的严谨性
        "max_tokens": 2000
    }

    try:
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=60 # 增加超时时间，因为生成内容变长了
        )
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return content
        else:
            return f"AI 请求失败: {response.text}"
    except Exception as e:
        return f"AI 请求异常: {e}"

# ================= 个股深度分析模块 (Round 2) =================

def extract_recommended_sectors(ai_content):
    """
    从第一轮 AI 回复中提取推荐板块及个股 JSON
    返回数据结构: [{'sector': 'xx', 'stocks': ['code', ...]}, ...]
    """
    try:
        # 尝试匹配 ```json ... ``` 代码块
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', ai_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            data = json.loads(json_str)
            return data.get("recommendations", [])
        
        # 备用：尝试直接搜索 JSON 结构 (looking for "recommendations")
        json_match = re.search(r'(\{.*"recommendations".*\})', ai_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            data = json.loads(json_str)
            return data.get("recommendations", [])
            
        print("[Warning] 未能在 AI 回复中找到推荐板块 JSON。")
        return []
    except Exception as e:
        print(f"[Error] 解析推荐板块 JSON 失败: {e}")
        return []


# ================= 全局缓存 =================
MARKET_SNAPSHOT = None

def get_market_snapshot():
    """
    获取全市场实时行情快照 (带缓存) - 用于查找股票名称等基础信息
    使用 Sina 接口 (ak.stock_zh_a_spot)
    """
    global MARKET_SNAPSHOT
    if MARKET_SNAPSHOT is not None:
        return MARKET_SNAPSHOT
        
    print("正在获取全市场快照 (Sina) 以匹配股票名称...")
    try:
        # ak.stock_zh_a_spot() 返回所有A股实时行情，包含代码、名称
        df = ak.stock_zh_a_spot()
        if df is not None and not df.empty:
            # 建立 代码 -> 名称 的字典，方便查询
            # Sina 返回的代码通常是 sz000xxx 或 600xxx (不带前缀? 需检查test output)
            # Test output: "bj920000", "bj920001". 
            # Output from `test_combined_fix` showed "代码" column has prefixes!
            
            # 我们只需要做一个 map: code (without prefix if possible, or handle both) -> name
            # 存为 dict
            snapshot = {}
            for _, row in df.iterrows():
                full_code = str(row['代码']) 
                name = str(row['名称'])
                # 兼容带前缀和不带前缀
                # 比如 bj920000 -> 920000
                # sh600519 -> 600519
                # sz000001 -> 000001
                
                # Strip 2 char prefix if it is letters
                clean_code = full_code
                if len(full_code) > 2 and not full_code[0].isdigit():
                     clean_code = full_code[2:]
                
                snapshot[full_code] = name
                snapshot[clean_code] = name
                
            MARKET_SNAPSHOT = snapshot
            print(f"全市场快照获取成功，共 {len(df)} 只股票。")
            return MARKET_SNAPSHOT
    except Exception as e:
        print(f"[Warning] 获取全市场快照失败: {e}")
    
    return {}

def fetch_sector_stocks(recommendations):
    """
    获取推荐板块的“强势力”龙头股 (v3 增强版)
    逻辑：使用 AI 推荐的个股列表，不再依赖 Akshare 板块成分股接口 (因网络/接口不稳定/缺失)。
    """
    stock_map = {}
    print(f"正在准备 AI 推荐的板块个股数据...")
    
    # 获取快照以便查找名称
    snapshot = get_market_snapshot()
    
    for item in recommendations:
        sector = item.get('sector')
        stock_codes = item.get('stocks', [])
        
        if not sector or not stock_codes:
            continue
            
        print(f"  - 正在查询 [{sector}] 推荐个股: {stock_codes}")
        
        stocks_info = []
        for code in stock_codes:
            # 简单清理代码
            code = str(code).strip()
            
            # 查找名称
            name = snapshot.get(code, f"Code:{code}")
            
            stocks_info.append({
                'code': code,
                'name': name,
                'pe': 0, # 数据源缺失，暂置0
                'pb': 0
            })
            
        stock_map[sector] = stocks_info
            
    return stock_map

def calculate_technical_indicators(df):
    """
    计算技术指标: MA, RSI, ATR
    """
    try:
        # MA
        df['MA5'] = df['收盘'].rolling(window=5).mean()
        df['MA20'] = df['收盘'].rolling(window=20).mean()
        df['MA60'] = df['收盘'].rolling(window=60).mean()
        
        # RSI (14)
        delta = df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # ATR (14)
        # TR = Max(High-Low, Abs(High-PreClose), Abs(Low-PreClose))
        df['PreClose'] = df['收盘'].shift(1)
        df['H-L'] = df['最高'] - df['最低']
        df['H-PC'] = abs(df['最高'] - df['PreClose'])
        df['L-PC'] = abs(df['最低'] - df['PreClose'])
        df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
        df['ATR'] = df['TR'].rolling(window=14).mean()
        
        return df
    except Exception as e:
        print(f"    [Warning] 指标计算失败: {e}")
        return df

def get_sina_symbol(code):
    """
    转换代码为 Sina 格式 (sh600000, sz000001)
    """
    if code.startswith('6'):
        return f"sh{code}"
    elif code.startswith('0') or code.startswith('3'):
        return f"sz{code}"
    elif code.startswith('4') or code.startswith('8'):
        return f"bj{code}" 
    else:
        return code

def fetch_one_stock_history_robust(code, start_date, end_date):
    """
    获取个股历史数据 (优先 Sina，失败则降级为 Eastmoney)
    返回标准化 DataFrame: columns=[日期, 开盘, 收盘, 最高, 最低, 成交量, 涨跌幅, 换手率]
    """
    # 1. 尝试 Sina 接口 (ak.stock_zh_a_daily)
    try:
        sina_symbol = get_sina_symbol(code)
        # Sina 接口无需 start_date/end_date 过滤，它默认返回历史所有或近期数据
        # adjust='qfq' 前复权
        df = ak.stock_zh_a_daily(symbol=sina_symbol, adjust="qfq")
        
        if df is not None and not df.empty:
            # Sina 返回列名通常为英文: date, open, high, low, close, volume, outstanding_share, turnover
            # 需要重命名为中文以兼容后续逻辑
            rename_map = {
                'date': '日期',
                'open': '开盘',
                'close': '收盘',
                'high': '最高',
                'low': '最低',
                'volume': '成交量',
                'turnover': '换手率' # 注意：Sina 返回的 turnover 可能是小数 (0.01) 也可能是百分比，需检查
            }
            df = df.rename(columns=rename_map)
            
            # 手动过滤日期
            # 转换 start_date, end_date (string "YYYYMMDD") 到 datetime 或 string "YYYY-MM-DD" comparison
            start_dt = pd.to_datetime(start_date, format='%Y%m%d')
            end_dt = pd.to_datetime(end_date, format='%Y%m%d')
            
            df['日期'] = pd.to_datetime(df['日期']) # 确保是 datetime
            df = df[(df['日期'] >= start_dt) & (df['日期'] <= end_dt)].copy()
            
            if not df.empty:
                # 补充计算 '涨跌幅' (pct_chg)
                df = df.sort_values(by='日期')
                df['涨跌幅'] = df['收盘'].pct_change() * 100
                df['涨跌幅'] = df['涨跌幅'].fillna(0)
                
                # 格式化日期为字符串 YYYY-MM-DD
                df['日期'] = df['日期'].dt.strftime('%Y-%m-%d')
                
                # 确保 '换手率' 存在 (如果 Sina 没返回)
                if '换手率' not in df.columns:
                     df['换手率'] = 0.0
                     
                return df, "Sina"
    except Exception as e:
        # print(f"    [Debug] Sina 接口获取 {code} 失败: {e}，尝试 Eastmoney...")
        pass

    # 2. 失败 fallback: Eastmoney (ak.stock_zh_a_hist)
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if df is not None and not df.empty:
            return df, "Eastmoney"
    except Exception as e:
        print(f"    [Error] Eastmoney 接口获取 {code} 亦失败: {e}")
        
    return None, None

def fetch_stock_history(stock_map):
    """
    获取个股 60 天历史数据 (v3: 增加基本面和技术指标上下文)
    """
    context_parts = []
    
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - pd.Timedelta(days=120)).strftime("%Y%m%d") #以此确保有足够的窗口计算MA60
    
    for sector, stocks in stock_map.items():
        if not stocks:
            continue
            
        sector_context = f"### 板块：{sector}\n"
        
        for stock in stocks:
            code = stock['code']
            name = stock['name']
            pe = stock['pe']
            pb = stock['pb']
            
            print(f"  - 获取个股历史数据: {name} ({code})...")
            
            # 增加重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 使用封装的 Robust 函数 (Sina -> EM)
                    df, source = fetch_one_stock_history_robust(code, start_date, end_date)
                    
                    if df is not None and not df.empty:
                        # print(f"    (数据来源: {source})") 
                        
                        # 计算指标
                        df = calculate_technical_indicators(df)
                        
                        # 取最后 60 行用于展示
                        df_display = df.tail(60)
                        
                        if df_display.empty:
                            print(f"    [Warning] {name} 数据在过滤后为空。")
                            break

                        latest = df_display.iloc[-1]
                        
                        # 构建增强版上下文
                        stock_str = f"#### {name} ({code})\n"
                        stock_str += f"- **基本面**: PE(动态)={pe}, PB={pb}\n"
                        stock_str += f"- **最新指标**: MA5={latest['MA5']:.2f}, MA20={latest['MA20']:.2f}, MA60={latest['MA60']:.2f}, RSI(14)={latest['RSI']:.1f}, ATR(14)={latest['ATR']:.2f}\n"
                        stock_str += "日期,收盘,涨跌幅,换手率\n"
                        
                        for _, row in df_display.iterrows():
                            # 兼容可能存在的列名问题
                            date_str = str(row['日期'])
                            close_val = row['收盘']
                            pct_chg = row.get('涨跌幅', 0)
                            turnover = row.get('换手率', 0)
                            
                            stock_str += f"{date_str},{close_val},{pct_chg:.2f},{turnover}\n"
                        
                        sector_context += stock_str + "\n"
                        break # 成功则跳出重试
                    else:
                        raise Exception("Fetching returned None or Empty")
                        
                except Exception as e:
                    print(f"    [Warning] 获取 {name} 历史数据失败 (尝试 {attempt+1}/{max_retries}): {e}")
                    time.sleep(2) # 失败等待
        
        context_parts.append(sector_context)
        
    return "\n".join(context_parts)

def call_deepseek_stock_review(stock_context):
    """
    第二轮 AI：个股深度评估 (v3 增强版)
    """
    if not stock_context:
        return ""
        
    print(f"[{get_beijing_time().strftime('%H:%M:%S')}] 正在请求 DeepSeek 进行个股深度评估 (v3 Round 2)...")
    
    system_prompt = """你是一位资深的量化交易员。根据提供的重点板块及其实力个股的数据（含基本面PE/PB和技术指标MA/RSI/ATR），请给出专业、犀利的短线点评。
    
    **分析要求：**
    1.  **基本面扫描**：结合PE/PB，快速判断估值安全性（过高需警惕，过低有安全垫）。
    2.  **技术面共振**：
        *   利用 **MA (均线)** 判断趋势（多头排列/空头排列/纠缠）。
        *   利用 **RSI** 判断情绪（>70超买需警惕回调，<30超卖可能有反弹）。
    3.  **交易建议 (带风控)**：
        *   **评级**：【积极买入】、【逢低关注】、【持有观察】或【卖出/规避】。
        *   **止损位计算**：请参考 **ATR (平均真实波幅)** 指标给出科学的止损位建议。通常止损位 = 当前价 - (2 * ATR)。请计算出具体数值。
        *   **低吸区间**：结合 MA20 或 MA5 给出支撑位。
        
    **输出格式：**
    ## 🚀 核心机会个股精评 (v3 智能增强版)
    
    ### [板块名称]
    #### [排名] [股票名称] (代码)
    *   **估值与趋势**: PE [...], 趋势处于 [...] (基于均线)。
    *   **指标信号**: RSI 为 [...], 显示 [...]。
    *   **交易建议**: 【...】
        *   🎯 **低吸区间**: ...
        *   🛡️ **ATR止损**: ... (建议设在 xxx 元)
    
    (保持内容精炼，数据说话。)
    """
    
    user_prompt = f"以下是基于智能策略（大市值+强动量）选出的推荐板块龙头股数据，请进行评估：\n\n{stock_context}"
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.4, # 降低温度，要求更严谨的计算
        "max_tokens": 1500
    }
    
    try:
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"AI 个股分析请求失败: {response.text}"
    except Exception as e:
        return f"AI 个股分析请求异常: {e}"

# ================= 可视化模块 =================

def plot_market_breadth(pivot, dates):
    """
    绘制市场宽度全景图
    """
    try:
        print("正在生成市场宽度全景图...")
        latest_date = dates[-1]
        current_vals = pivot[latest_date].sort_values(ascending=True)
        
        # 设置中文字体，GitHub Actions 优先使用 Noto Sans CJK
        plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建画布
        plt.figure(figsize=(10, 15)) # 高一点，因为行业很多
        
        # 颜色映射
        colors = []
        for val in current_vals:
            if val >= 80:
                colors.append('#ff4d4f') # 红色 过热
            elif val <= 20:
                colors.append('#1890ff') # 蓝色 冰点
            else:
                colors.append('#8c8c8c') # 灰色 正常
        
        # 绘制条形图
        bars = plt.barh(current_vals.index, current_vals.values, color=colors, height=0.6)
        
        # 添加数值标签
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                     f'{width:.1f}', va='center', fontsize=9)
            
        plt.title(f'A股全市场行业宽度排行 ({latest_date})', fontsize=16, pad=20)
        plt.xlabel('MA20上方个股占比 (%)', fontsize=12)
        plt.xlim(0, 105) # 留出标签空间
        plt.grid(axis='x', linestyle='--', alpha=0.3)
        
        # 添加参考线
        plt.axvline(x=20, color='#1890ff', linestyle='--', alpha=0.5)
        plt.axvline(x=80, color='#ff4d4f', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        # 保存路径
        # 图片保存到 static/images/charts/
        static_img_dir = HUGO_IMAGES_DIR
        
        if not os.path.exists(static_img_dir):
            os.makedirs(static_img_dir, exist_ok=True)
            
        # 固定文件名
        filename = "A股市场宽度全景图.png"
        save_path = os.path.join(static_img_dir, filename)
        
        plt.savefig(save_path, dpi=120, bbox_inches='tight')
        plt.close()
        
        print(f"[Info] 市场宽度全景图已生成: {save_path}")
        

        # 返回用于 Markdown 引用的相对路径
        return f"/images/charts/{filename}"
        
    except Exception as e:
        print(f"[Error] 绘图失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def plot_sector_momentum(momentum_df, date_str):
    """
    绘制行业动量散点图 (X: 当前宽度, Y: 5日变化)
    """
    try:
        if momentum_df is None:
            return None
            
        print("正在生成行业动量散点图...")
        
        plt.figure(figsize=(12, 10))
        
        x = momentum_df['Current']
        y = momentum_df['Change5D']
        
        # 绘制散点
        # 根据象限设置颜色
        colors = []
        for idx, row in momentum_df.iterrows():
            curr = row['Current']
            chg = row['Change5D']
            if curr > 50 and chg > 0:
                colors.append('#ff4d4f') # 强+强 (红)
            elif curr > 50 and chg < 0:
                colors.append('#faad14') # 强+弱 (黄)
            elif curr < 50 and chg > 0:
                colors.append('#1890ff') # 弱+强 (蓝)
            else:
                colors.append('#8c8c8c') # 弱+弱 (灰)
                
        plt.scatter(x, y, c=colors, alpha=0.7, s=100)
        
        # 添加标签 (只标记极值点以避免拥挤)
        # 逻辑: 距离中心点 (50, 0) 最远的 N 个点，或者每个象限选几个
        for idx, row in momentum_df.iterrows():
            curr = row['Current']
            chg = row['Change5D']
            
            # 简单的过滤逻辑：只显示特别显著的
            if abs(chg) > 10 or curr > 85 or curr < 15:
                plt.text(curr+1, chg, idx, fontsize=9, alpha=0.8)
        
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        plt.axvline(x=50, color='black', linestyle='--', alpha=0.3)
        
        plt.title(f'行业宽度动量分析 (5日变化 vs 当前水平) - {date_str}', fontsize=16)
        plt.xlabel('当前市场宽度 (MA20%)', fontsize=12)
        plt.ylabel('5日宽度变化 (%)', fontsize=12)
        
        # 添加象限说明
        plt.text(95, 15, '领涨/主线\n(强势加速)', ha='right', va='top', fontsize=12, color='#ff4d4f', fontweight='bold')
        plt.text(95, -15, '高位滞涨\n(动能衰竭)', ha='right', va='bottom', fontsize=12, color='#faad14', fontweight='bold')
        plt.text(5, 15, '底部反转\n(蓄势待发)', ha='left', va='top', fontsize=12, color='#1890ff', fontweight='bold')
        plt.text(5, -15, '低位弱势\n(继续探底)', ha='left', va='bottom', fontsize=12, color='#8c8c8c', fontweight='bold')
        
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()
        
        # 保存
        static_img_dir = HUGO_IMAGES_DIR
        if not os.path.exists(static_img_dir):
            os.makedirs(static_img_dir, exist_ok=True)
            
        filename = "A股行业动量分析图.png"
        save_path = os.path.join(static_img_dir, filename)
        
        plt.savefig(save_path, dpi=120, bbox_inches='tight')
        plt.close()
        
        print(f"[Info] 行业动量图已生成: {save_path}")
        return f"/images/charts/{filename}"
        
    except Exception as e:
        print(f"[Error] 动量图绘制失败: {e}")
        return None

# ================= Hugo博客集成模块 =================


def save_to_hugo_blog(content, beijing_time, image_path=None, extra_images=None):
    """
    保存报告到Hugo博客，并支持Git自动推送
    extra_images: list of tuples (title, path)
    """
    # 构建Hugo博客文件路径
    
    # 检查Hugo博客路径是否存在
    if not os.path.exists(HUGO_BLOG_DIR):
        print(f"[Warning] Hugo博客路径不存在: {HUGO_BLOG_DIR}")
        return False
        
    if not os.path.exists(HUGO_CONTENT_DIR):
        print(f"[Warning] Hugo内容目录不存在: {HUGO_CONTENT_DIR}")
        return False
    
    # 构建文件名 (固定中文文件名，不带日期)
    date_str = beijing_time.strftime('%Y-%m-%d')
    hugo_filename = "A股市场宽度分析日报.md"
    hugo_file_path = os.path.join(HUGO_CONTENT_DIR, hugo_filename)
    
    featured_image = image_path if image_path else ""
    
    # 统一固定标题
    fixed_title = "📈A股市场宽度分析日报"
    date_iso = beijing_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # 构建Hugo Front Matter
    front_matter = f"""---
title: "{fixed_title}"
date: {date_iso}
lastmod: {date_iso}
description: "基于市场宽度指标的A股深度分析报告，包含AI智能解读和投资建议"
tags: ["A股", "市场分析", "AI分析", "投资策略", "股票市场"]
categories: ["市场分析", "投资策略"]
author: ["AI分析师"]
image: "{featured_image}"
draft: false
---

"""
    
    # 插入图片 (如果有)
    image_section = ""
    if image_path:
        image_section += f"## 📊 市场宽度全景图\n\n![A股市场宽度全景图]({image_path})\n\n"
    
    if extra_images:
        for title, path in extra_images:
            image_section += f"## {title}\n\n![{title}]({path})\n\n"

    # 组合完整内容
    full_content = front_matter + image_section + content
    
    try:
        # 保存到Hugo博客目录
        with open(hugo_file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"[Info] 报告已保存到Hugo博客: {hugo_file_path}")
        
        # 如果启用Git推送
        if ENABLE_GIT_PUSH:
            push_to_git(HUGO_BLOG_DIR, hugo_filename)
        
        return True
        
    except Exception as e:
        print(f"[Error] 保存到Hugo博客失败: {e}")
        return False

def push_to_git(hugo_blog_path, filename):
    """
    推送到Git仓库 (GitHub环境优化版)
    """
    try:
        import subprocess
        
        # 切换到Hugo博客目录
        original_cwd = os.getcwd()
        os.chdir(hugo_blog_path)
        
        # Git添加新文件
        new_file_path = os.path.join(HUGO_CONTENT_DIR, filename)
        subprocess.run(['git', 'add', new_file_path], check=True, capture_output=True)
        
        # 检查是否有变更需要提交
        result = subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True)
        if result.stdout.strip():
            # 有变更，执行提交
            subprocess.run(['git', 'commit', '-m', GIT_COMMIT_MESSAGE], check=True, capture_output=True)
            
            # 尝试推送到main分支，如果失败则尝试master分支
            try:
                subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
                print("[Info] Git推送成功 (main分支)")
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(['git', 'push', 'origin', 'master'], check=True, capture_output=True)
                    print("[Info] Git推送成功 (master分支)")
                except subprocess.CalledProcessError as e:
                    print(f"[Warning] Git推送到master分支也失败: {e}")
        else:
            print("[Info] 没有变更需要提交和推送")
        
        # 恢复原始工作目录
        os.chdir(original_cwd)
        
    except subprocess.CalledProcessError as e:
        print(f"[Warning] Git操作失败: {e}")
        # 尝试恢复工作目录
        try:
            os.chdir(original_cwd)
        except:
            pass
    except Exception as e:
        print(f"[Warning] Git推送异常: {e}")
        # 尝试恢复工作目录
        try:
            os.chdir(original_cwd)
        except:
            pass

# ================= 主程序 =================

def main():
    beijing_time = get_beijing_time()
    print(f"[{beijing_time.strftime('%H:%M:%S')}] 开始执行市场分析任务...")
    
    # 1. 获取数据
    data = fetch_data()
    if not data:
        print("[Error] 数据获取失败，任务终止。")
        return

    # 2. 处理数据
    pivot, dates = process_data(data)
    
    # 检查最新数据日期是否为今天
    latest_date = dates[-1]
    today_date = beijing_time.strftime('%Y-%m-%d')
    
    # [DEV MODE] v3 测试阶段，如果是周末，允许跑昨天的最新数据，仅给 Warning 不 return
    if latest_date != today_date:
        print(f"[Warning] 数据最新日期 ({latest_date}) 不等于今天 ({today_date})。")
        # return # v3 暂时注释掉，允许回测演示
    

    # 3. 生成数据上下文
    # 计算动量
    momentum_df = calculate_breadth_momentum(pivot, dates)
    
    # 获取实时情绪
    sentiment_data = analyze_market_sentiment_snapshot()
    
    context = prepare_context_for_ai(pivot, dates, momentum_df, sentiment_data)
    print("--- 生成的数据上下文 ---")
    print(context)
    
    # 生成可视化图表
    image_rel_path = plot_market_breadth(pivot, dates)
    
    extra_images = []
    # 生成动量图
    momentum_img_path = plot_sector_momentum(momentum_df, dates[-1])
    if momentum_img_path:
        extra_images.append(("🚀 行业动量分析图", momentum_img_path))
    
    # 4. 调用 AI 分析 (Round 1: 市场宽度)
    print(f"[{get_beijing_time().strftime('%H:%M:%S')}] 正在请求 DeepSeek 进行分析 (Round 1)...")
    ai_report_round1 = call_deepseek_analysis(context)
    
    # --- Round 2: 推荐板块个股挖掘 ---
    ai_report_round2 = ""
    
    # 1. 提取推荐板块
    recommended_sectors = extract_recommended_sectors(ai_report_round1)
    
    if recommended_sectors:
        print(f"--- 捕获推荐板块: {recommended_sectors} ---")
        
        # 2. 获取龙头股数据
        stock_map = fetch_sector_stocks(recommended_sectors)
        
        if stock_map:
            # 3. 获取历史行情上下文
            stock_context = fetch_stock_history(stock_map)
            
            # 4. 调用 AI 分析 (Round 2)
            if stock_context:
                ai_report_round2 = call_deepseek_stock_review(stock_context)
            else:
                print("[Warning] 未能构建有效的个股历史数据上下文，跳过 Round 2。")
        else:
            print("[Warning] 未能获取任何板块成分股，跳过 Round 2。")
    else:
        print("[Info] 第一轮报告未明确推荐板块或解析失败，跳过 Round 2 个股分析。")


    # 5. 组合最终报告
    beijing_time = get_beijing_time()
    report_header = f"""
> **推送时间**: {beijing_time.strftime('%Y-%m-%d %H:%M')} (北京时间) | 每个交易日下午 15:30 推送
> **最新数据日期**: {latest_date}
> **市场宽度定义**: 市场宽度（Market Breadth）是指当前处于 20 日均线（MA20）之上的股票占比。宽度越高，说明市场参与度越广，赚钱效应越强；反之则表明市场情绪低迷，仅少数个股活跃。
> - **< 20%**: 极度冰点，往往是底部区域
> - **20-80%**: 正常震荡区间
> - **> 80%**: 极度过热，往往是顶部区域

---
"""
    
    final_report = report_header + ai_report_round1 + "\n\n" + ai_report_round2 + f"""

---
*数据来源: 大盘云图 | AI 分析: DeepSeek*
    """
    
    # 6. 保存与推送
    # 保存到当前目录（作为备份）
    filename = "A股市场宽度分析日报.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_report)
    print(f"[Info] 报告已保存至 {filename}")
    

    # 如果启用Hugo博客保存功能
    if ENABLE_HUGO_BLOG:
        print("[Info] 正在保存到Hugo博客...")
        hugo_success = save_to_hugo_blog(final_report, beijing_time, image_rel_path, extra_images)
        if not hugo_success:
            print("[Warning] Hugo博客保存失败，但报告已保存到当前目录")
    


if __name__ == "__main__":
    main()
