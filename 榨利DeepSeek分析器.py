#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
榨利DeepSeek分析器
使用DeepSeek API分析榨利数据并提供购买决策建议
具备独立数据获取能力，无需依赖现有CSV文件
"""

import pandas as pd
import requests
import json
import os
import time
from datetime import datetime, timedelta
import numpy as np
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties

# 设置中文字体（适配 macOS）
try:
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

class 榨利DeepSeek分析器:
    """榨利DeepSeek分析器类"""
    
    def __init__(self, api_key="sk-063857d175bd48038684520e7b6ec934", base_url="https://api.deepseek.com/v1"):
        """初始化DeepSeek分析器"""
        self.api_key = api_key
        self.base_url = base_url
        self.model = "deepseek-chat"
        
        # 压榨产出比例
        self.豆油产出率 = 0.185  # 18.5%
        self.豆粕产出率 = 0.785  # 78.5%
        
        # 压榨成本（元/吨）
        self.压榨成本 = 150.0
        
        # 微信推送配置
        self.WXPUSHER_APP_TOKEN = "AT_UHus2F8p0yjnG6XvGEDzdCp5GkwvLdkc"
        self.WXPUSHER_TOPIC_IDS = [42353]
        self.WXPUSHER_URL = "https://wxpusher.zjiecode.com/api/send/message"
        
        print("🚀 榨利DeepSeek分析器初始化完成")
        print(f"🔑 API密钥: {self.api_key[:10]}...")
        print(f"🌐 API地址: {self.base_url}")
        print(f"💰 压榨成本: {self.压榨成本} 元/吨")
        print(f"📱 微信推送: 主题ID {self.WXPUSHER_TOPIC_IDS[0]}")
    
    def 获取豆二数据(self):
        """使用akshare获取豆二(B0)期货数据"""
        print("\n🌱 开始获取豆二(B0)期货数据...")
        
        try:
            # 获取豆二主力合约数据
            豆二数据 = ak.futures_zh_daily_sina(symbol="B0")
            
            if 豆二数据.empty:
                print("❌ 获取的豆二数据为空")
                return None
            
            print(f"✅ 成功获取豆二数据，共 {len(豆二数据)} 条记录")
            print(f"📅 时间范围: {豆二数据['date'].min()} 至 {豆二数据['date'].max()}")
            
            # 重命名列名为中文
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
            
            # 只保留需要的列
            豆二数据 = 豆二数据[['日期', '豆二价格']]
            
            # 转换日期格式
            豆二数据['日期'] = pd.to_datetime(豆二数据['日期'])
            
            return 豆二数据
            
        except Exception as e:
            print(f"❌ 获取豆二数据失败: {e}")
            return None
    
    def 获取元爬虫数据(self, 产品类型='Y'):
        """使用元爬虫获取豆油或豆粕数据"""
        
        产品映射 = {'Y': '豆油', 'M': '豆粕'}
        产品名称 = 产品映射.get(产品类型, '未知产品')
        
        print(f"\n📊 开始获取{产品名称}数据...")
        
        # API URL
        url = "https://www.jiaoyifamen.com/tools/api//future-basis/query"
        
        # 请求参数
        params = {
            't': int(time.time() * 1000),  # 时间戳
            'type': 产品类型  # 类型参数
        }
        
        # 请求头
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Priority': 'u=1, i',
            'Referer': 'https://www.jiaoyifamen.com/variety/varieties-varieties',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'token': 'null'
        }
        
        try:
            # 发送GET请求，添加SSL验证处理
            response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
            
            if response.status_code == 200:
                print(f"✅ {产品名称}数据获取成功!")
                
                # 获取响应内容
                数据 = response.json()
                
                # 解析数据
                解析结果 = self.解析元爬虫数据(数据, 产品类型)
                
                if 解析结果 is not None:
                    print(f"📈 成功解析{产品名称}数据，共 {len(解析结果)} 条记录")
                    return 解析结果
                else:
                    print(f"❌ 解析{产品名称}数据失败")
                    return None
                    
            else:
                print(f"❌ {产品名称}数据请求失败，状态码: {response.status_code}")
                return None
                
        except requests.exceptions.SSLError as e:
            print(f"⚠️ SSL连接错误，尝试不验证SSL证书...")
            try:
                # 禁用SSL验证重试
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.get(url, params=params, headers=headers, timeout=30, verify=False)
                
                if response.status_code == 200:
                    print(f"✅ {产品名称}数据获取成功!")
                    
                    # 获取响应内容
                    数据 = response.json()
                    
                    # 解析数据
                    解析结果 = self.解析元爬虫数据(数据, 产品类型)
                    
                    if 解析结果 is not None:
                        print(f"📈 成功解析{产品名称}数据，共 {len(解析结果)} 条记录")
                        return 解析结果
                    else:
                        print(f"❌ 解析{产品名称}数据失败")
                        return None
                else:
                    print(f"❌ {产品名称}数据请求失败，状态码: {response.status_code}")
                    return None
                    
            except Exception as e2:
                print(f"❌ 获取{产品名称}数据异常: {e2}")
                return None
                
        except Exception as e:
            print(f"❌ 获取{产品名称}数据异常: {e}")
            return None
    
    def 解析元爬虫数据(self, 原始数据, 产品类型):
        """解析元爬虫返回的数据结构"""
        
        if not 原始数据 or 'data' not in 原始数据:
            return None
        
        数据内容 = 原始数据['data']
        
        # 查找关键字段
        日期数据 = None
        价格数据 = None
        基差数据 = None
        
        # 查找日期字段
        for 字段名 in 数据内容.keys():
            if 字段名 == 'category':
                日期数据 = 数据内容[字段名]
                print(f"� 找到日期字段: {字段名}, 数据量: {len(日期数据)}")
                break
        
        # 如果没找到category，尝试查找包含category的字段
        if 日期数据 is None:
            for 字段名 in 数据内容.keys():
                if 'category' in 字段名.lower():
                    日期数据 = 数据内容[字段名]
                    print(f"📅 找到日期字段: {字段名}, 数据量: {len(日期数据)}")
                    break
        
        # 查找价格字段
        for 字段名 in 数据内容.keys():
            if 'price' in 字段名.lower() and 'value' in 字段名.lower():
                价格数据 = 数据内容[字段名]
                print(f"💰 找到价格字段: {字段名}, 数据量: {len(价格数据)}")
                break
        
        # 查找基差字段
        for 字段名 in 数据内容.keys():
            if 'basis' in 字段名.lower() and 'value' in 字段名.lower():
                基差数据 = 数据内容[字段名]
                print(f"📊 找到基差字段: {字段名}, 数据量: {len(基差数据)}")
                break
        
        # 检查数据长度是否一致
        if not (日期数据 and 价格数据 and 基差数据):
            print("❌ 缺少必要的数据字段")
            return None
        
        if len(日期数据) != len(价格数据) or len(日期数据) != len(基差数据):
            print(f"⚠️ 数据长度不一致: 日期({len(日期数据)}), 价格({len(价格数据)}), 基差({len(基差数据)})")
            
            # 取最小长度
            最小长度 = min(len(日期数据), len(价格数据), len(基差数据))
            日期数据 = 日期数据[:最小长度]
            价格数据 = 价格数据[:最小长度]
            基差数据 = 基差数据[:最小长度]
            
            print(f"🔄 调整为统一长度: {最小长度}")
        
        # 创建DataFrame
        产品数据 = pd.DataFrame({
            '日期': 日期数据,
            '价格': 价格数据,
            '基差': 基差数据
        })
        
        # 过滤无效数据
        产品数据 = 产品数据[
            (产品数据['价格'] != 0) & 
            (产品数据['基差'] != 0) &
            (产品数据['价格'] != "NaN") &
            (产品数据['基差'] != "NaN")
        ]
        
        # 转换日期格式 - 处理月-日格式的日期
        try:
            # 尝试直接转换
            产品数据['日期'] = pd.to_datetime(产品数据['日期'])
        except Exception as e:
            print(f"⚠️ 日期转换失败: {e}")
            print(f"📅 尝试处理月-日格式日期...")
            
            # 假设日期是月-日格式，需要添加年份
            # 使用当前年份作为默认年份
            当前年份 = datetime.now().year
            
            # 为每个日期添加年份
            带年份日期 = []
            for 日期字符串 in 产品数据['日期']:
                if isinstance(日期字符串, str) and '-' in 日期字符串:
                    try:
                        # 解析月-日格式
                        月, 日 = 日期字符串.split('-')
                        完整日期 = f"{当前年份}-{月}-{日}"
                        带年份日期.append(完整日期)
                    except:
                        带年份日期.append(日期字符串)
                else:
                    带年份日期.append(日期字符串)
            
            # 再次尝试转换
            产品数据['日期'] = pd.to_datetime(带年份日期, errors='coerce')
            
            # 过滤掉转换失败的日期
            产品数据 = 产品数据.dropna(subset=['日期'])
            
            print(f"✅ 日期转换完成，剩余 {len(产品数据)} 条有效记录")
        
        # 根据产品类型设置列名
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
    
    def 合并数据(self, 豆油数据, 豆粕数据, 豆二数据):
        """合并豆油、豆粕和豆二数据"""
        print("\n🔄 开始合并数据...")
        
        if 豆油数据 is None or 豆粕数据 is None or 豆二数据 is None:
            print("❌ 数据不完整，无法合并")
            return None
        
        # 合并豆油和豆粕数据
        合并数据 = pd.merge(豆油数据, 豆粕数据, on='日期', how='inner')
        
        # 合并豆二数据
        合并数据 = pd.merge(合并数据, 豆二数据, on='日期', how='inner')
        
        print(f"✅ 数据合并完成，共 {len(合并数据)} 条有效记录")
        
        return 合并数据
    
    def 计算榨利(self, 合并数据):
        """计算榨利"""
        print("\n🧮 开始计算榨利...")
        
        if 合并数据 is None or 合并数据.empty:
            print("❌ 数据为空，无法计算榨利")
            return None
        
        # 计算现货价格
        合并数据['豆油现货价格'] = 合并数据['豆油价格'] + 合并数据['豆油基差']
        合并数据['豆粕现货价格'] = 合并数据['豆粕价格'] + 合并数据['豆粕基差']
        
        # 榨利计算公式：榨利 = ((豆油价格 + 豆油基差) × 0.185 + (豆粕价格 + 豆粕基差) × 0.785) - 豆二价格 - 压榨成本
        合并数据['榨利'] = (
            (合并数据['豆油价格'] + 合并数据['豆油基差']) * self.豆油产出率 + 
            (合并数据['豆粕价格'] + 合并数据['豆粕基差']) * self.豆粕产出率 - 
            合并数据['豆二价格'] - 
            self.压榨成本
        )
        
        # 计算榨利率
        合并数据['榨利率'] = (合并数据['榨利'] / 合并数据['豆二价格']) * 100
        
        print(f"✅ 榨利计算完成")
        print(f"� 榨利范围: {合并数据['榨利'].min():.2f} 至 {合并数据['榨利'].max():.2f}")
        print(f"📊 平均榨利: {合并数据['榨利'].mean():.2f}")
        
        return 合并数据
    
    def 独立获取数据(self):
        """独立获取榨利数据，不依赖现有CSV文件"""
        print("\n🔄 开始独立获取榨利数据...")
        
        # 1. 获取豆二数据
        豆二数据 = self.获取豆二数据()
        if 豆二数据 is None:
            print("❌ 豆二数据获取失败")
            return None
        
        # 2. 获取豆油数据
        豆油数据 = self.获取元爬虫数据('Y')
        if 豆油数据 is None:
            print("❌ 豆油数据获取失败")
            return None
        
        # 3. 获取豆粕数据
        豆粕数据 = self.获取元爬虫数据('M')
        if 豆粕数据 is None:
            print("❌ 豆粕数据获取失败")
            return None
        
        # 4. 合并数据
        合并数据 = self.合并数据(豆油数据, 豆粕数据, 豆二数据)
        if 合并数据 is None:
            print("❌ 数据合并失败")
            return None
        
        # 5. 计算榨利
        榨利数据 = self.计算榨利(合并数据)
        
        print("✅ 独立数据获取完成")
        return 榨利数据
    
    def 获取最新数据文件(self):
        """获取最新的榨利数据文件（备用方法）"""
        print("\n🔍 查找最新的榨利数据文件...")
        
        # 查找所有榨利数据文件
        数据文件 = [f for f in os.listdir('.') if f.startswith('榨利数据_') and f.endswith('.csv')]
        
        if not 数据文件:
            print("❌ 未找到榨利数据文件")
            return None
        
        # 按修改时间排序，获取最新的文件
        数据文件.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        最新文件 = 数据文件[0]
        
        print(f"✅ 找到最新数据文件: {最新文件}")
        return 最新文件
    
    def 读取数据(self, 文件路径):
        """读取榨利数据文件（备用方法）"""
        print(f"\n📂 开始读取数据文件: {文件路径}")
        
        try:
            if not os.path.exists(文件路径):
                print(f"❌ 文件不存在: {文件路径}")
                return None
            
            # 读取CSV文件
            数据 = pd.read_csv(文件路径, encoding='utf-8-sig')
            
            if 数据.empty:
                print("❌ 读取的数据为空")
                return None
            
            # 转换日期格式
            if '日期' in 数据.columns:
                数据['日期'] = pd.to_datetime(数据['日期'])
            
            print(f"✅ 成功读取数据，共 {len(数据)} 条记录")
            print(f"📅 时间范围: {数据['日期'].min()} 至 {数据['日期'].max()}")
            
            return 数据
            
        except Exception as e:
            print(f"❌ 读取数据失败: {e}")
            return None
    
    def 提取近两年数据(self, 榨利数据):
        """提取近两年的数据"""
        print("\n⏰ 提取近两年数据...")
        
        if 榨利数据 is None or 榨利数据.empty:
            print("❌ 榨利数据为空")
            return None
        
        # 获取当前日期
        当前日期 = datetime.now()
        
        # 计算两年前的日期
        两年前日期 = 当前日期 - timedelta(days=730)
        
        # 过滤近两年数据
        近两年数据 = 榨利数据[榨利数据['日期'] >= 两年前日期]
        
        if 近两年数据.empty:
            print("❌ 近两年数据为空")
            return None
        
        print(f"✅ 提取到近两年数据，共 {len(近两年数据)} 条记录")
        print(f"📅 时间范围: {近两年数据['日期'].min()} 至 {近两年数据['日期'].max()}")
        
        return 近两年数据
    
    def 生成数据摘要(self, 近两年数据):
        """生成数据摘要统计"""
        print("\n📊 生成数据摘要统计...")
        
        if 近两年数据 is None or 近两年数据.empty:
            return None
        
        # 计算基本统计信息
        摘要 = {}
        
        # 榨利统计
        摘要['榨利统计'] = {
            '最小值': 近两年数据['榨利'].min(),
            '最大值': 近两年数据['榨利'].max(),
            '平均值': 近两年数据['榨利'].mean(),
            '标准差': 近两年数据['榨利'].std(),
            '中位数': 近两年数据['榨利'].median(),
            '盈利天数': len(近两年数据[近两年数据['榨利'] > 0]),
            '亏损天数': len(近两年数据[近两年数据['榨利'] < 0]),
            '盈利比例': (len(近两年数据[近两年数据['榨利'] > 0]) / len(近两年数据)) * 100
        }
        
        # 价格统计
        for 价格列 in ['豆油价格', '豆粕价格', '豆二价格', '豆油现货价格', '豆粕现货价格']:
            if 价格列 in 近两年数据.columns:
                摘要[价格列] = {
                    '最小值': 近两年数据[价格列].min(),
                    '最大值': 近两年数据[价格列].max(),
                    '平均值': 近两年数据[价格列].mean(),
                    '标准差': 近两年数据[价格列].std()
                }
        
        # 基差统计
        for 基差列 in ['豆油基差', '豆粕基差']:
            if 基差列 in 近两年数据.columns:
                摘要[基差列] = {
                    '最小值': 近两年数据[基差列].min(),
                    '最大值': 近两年数据[基差列].max(),
                    '平均值': 近两年数据[基差列].mean(),
                    '标准差': 近两年数据[基差列].std()
                }
        
        # 榨利率统计
        if '榨利率' in 近两年数据.columns:
            摘要['榨利率统计'] = {
                '最小值': 近两年数据['榨利率'].min(),
                '最大值': 近两年数据['榨利率'].max(),
                '平均值': 近两年数据['榨利率'].mean(),
                '标准差': 近两年数据['榨利率'].std()
            }
        
        print("✅ 数据摘要统计生成完成")
        return 摘要
    
    def 准备完整分析数据(self, 近两年数据):
        """准备完整的分析数据，包括历史价格数据"""
        print("\n📋 准备完整分析数据...")
        
        if 近两年数据 is None or 近两年数据.empty:
            return None
        
        # 选择关键数据列
        关键数据 = 近两年数据[['日期', '豆油价格', '豆粕价格', '豆二价格', '豆油基差', '豆粕基差', 
                          '豆油现货价格', '豆粕现货价格', '榨利', '榨利率']].copy()
        
        # 按日期排序
        关键数据 = 关键数据.sort_values('日期')
        
        # 转换为字符串格式，便于传递给DeepSeek
        关键数据['日期'] = 关键数据['日期'].dt.strftime('%Y-%m-%d')
        
        print(f"✅ 完整分析数据准备完成，包含 {len(关键数据)} 条记录")
        
        return 关键数据
    
    def 构建分析提示词(self, 数据摘要, 近两年数据):
        """构建DeepSeek分析提示词"""
        print("\n💬 构建DeepSeek分析提示词...")
        
        if 数据摘要 is None or 近两年数据 is None:
            return None
        
        # 获取最新数据
        最新数据 = 近两年数据.iloc[-1]
        最新日期 = 最新数据['日期'].strftime('%Y-%m-%d')
        
        # 准备完整的历史数据
        完整数据 = self.准备完整分析数据(近两年数据)
        
        # 转换为CSV格式的字符串
        历史数据字符串 = 完整数据.to_csv(index=False, encoding='utf-8-sig') if 完整数据 is not None else ""
        
        # 计算分位数
        p_price = int((最新数据['豆油价格']-数据摘要['豆油价格']['最小值'])/(数据摘要['豆油价格']['最大值']-数据摘要['豆油价格']['最小值'])*100)
        p_basis = int((最新数据['豆油基差']-数据摘要['豆油基差']['最小值'])/(数据摘要['豆油基差']['最大值']-数据摘要['豆油基差']['最小值'])*100)
        p_margin = int((最新数据['榨利']-数据摘要['榨利统计']['最小值'])/(数据摘要['榨利统计']['最大值']-数据摘要['榨利统计']['最小值'])*100)
        
        # 计算近期趋势
        近期数据 = 近两年数据.tail(20)
        价格趋势 = "上涨" if 近期数据['豆油价格'].iloc[-1] > 近期数据['豆油价格'].iloc[0] else "下跌"
        榨利趋势 = "走扩" if 近期数据['榨利'].iloc[-1] > 近期数据['榨利'].iloc[0] else "收窄"
        
        提示词 = f"""你是一位专注于**豆油及大豆压榨产业链**的资深商品研究总监。请基于以下数据撰写一份深度详实、逻辑缜密的豆油采购决策报告。

## 豆油品种特性背景（请在分析时充分考虑）：
1. **压榨产业链核心**：豆油是大豆压榨的副产品（出油率18.5%），与豆粕联动（粕油比），**榨利是核心驱动指标**
2. **原料高度依赖进口**：中国大豆80%+依赖进口（巴西、美国、阿根廷），受国际大豆价格和汇率影响大
3. **明显季节性**：美豆生长季（5-9月）天气炒作，南美收获季（2-5月）供应压力集中
4. **替代关系**：与棕榈油、菜油存在强替代关系，豆棕价差是重要参考指标
5. **榨利驱动逻辑**：榨利高→油厂开机率高→豆油供应增加→利空油价；榨利低→开机率下降→利多油价
6. **政策敏感**：关税调整、国储抛储/收储、进口配额等政策影响显著

## 当前市场数据：
- **统计周期**：{近两年数据['日期'].min().strftime('%Y-%m-%d')} 至 {最新日期} ({len(近两年数据)}个交易日)
- **豆油期货**：当前 `{最新数据['豆油价格']:.0f}` | 区间 `[{数据摘要['豆油价格']['最小值']:.0f}, {数据摘要['豆油价格']['最大值']:.0f}]` | 均值 `{数据摘要['豆油价格']['平均值']:.0f}` | **分位数 P{p_price}%**
- **现货基差**：当前 `{最新数据['豆油基差']:.0f}` | 区间 `[{数据摘要['豆油基差']['最小值']:.0f}, {数据摘要['豆油基差']['最大值']:.0f}]` | 均值 `{数据摘要['豆油基差']['平均值']:.0f}` | **分位数 P{p_basis}%**
- **盘面榨利**：当前 `{最新数据['榨利']:.0f}` | 区间 `[{数据摘要['榨利统计']['最小值']:.0f}, {数据摘要['榨利统计']['最大值']:.0f}]` | 均值 `{数据摘要['榨利统计']['平均值']:.0f}` | **分位数 P{p_margin}%**
- **现货折算**：`{最新数据['豆油现货价格']:.0f}` 元/吨 | 压榨成本基准：`{self.压榨成本}` 元/吨
- **近期趋势**：价格{价格趋势}，榨利{榨利趋势}

---
**UI 设计规范：**
1. **头部数据区**：必须使用引用块 (>) 包裹，数据行必须使用 `|` 分隔，严禁换行。
2. **排版布局**：标题仅使用 ####，正文使用无序列表 (-)，段落之间严禁空行。
3. **视觉降噪**：严禁空行，严禁使用 #/##/### 标题，严禁使用表格。

请严格按此模板输出：

#### 📊 市场仪表盘 ({最新日期})
> 📉 **期货**: {最新数据['豆油价格']:.0f} | 📦 **基差**: {最新数据['豆油基差']:.0f} | 💰 **榨利**: {最新数据['榨利']:.0f} | 📏 **价格P**: {p_price}% | 📏 **榨利P**: {p_margin}%
#### 🚦 交易指令
> 🟢/🔴 **信号**: [买入/卖出/观望] | 🎯 **目标**: [数值] | 🛑 **止损**: [数值]
#### 🫘 豆油品种深度分析
- **榨利周期定位**：[当前榨利P{p_margin}%处于什么阶段？是压榨利润扩张期还是收缩期？对油厂开机率有何影响？]
- **估值判断**：[结合P{p_price}%价格分位数，评估当前豆油价格的性价比和安全边际]
- **基差信号**：[P{p_basis}%基差分位数意味着什么？现货端是供应压力还是需求支撑？]
- **原料端逻辑**：[当前进口大豆成本、到港节奏、油厂库存对豆油价格的影响]
- **替代逻辑**：[当前豆棕价差处于什么水平？是否存在替代驱动的机会或风险？]
- **风险提示**：[主要风险点及应对预案，包括榨利变化、政策、汇率、天气等]
#### 🛒 精细化采购建议
- **期货策略**：[具体的建仓区间、分批节奏、严格的止损止盈位设置]
- **现货策略**：[针对不同库存水平的采购建议，包括基差合同的点价时机]
- **套期保值**：[对于生产企业或贸易商的对冲建议，考虑榨利套保策略]
#### 📅 历史参考数据
```csv
{历史数据字符串}
```"""
        
        print("✅ 紧凑型分析提示词构建完成")
        return 提示词
        
        print("✅ 增强型分析提示词构建完成")
        return 提示词
    
    def 调用DeepSeekAPI(self, 提示词):
        """调用DeepSeek API进行分析"""
        print("\n🤖 调用DeepSeek API进行分析...")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": 提示词
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.5 
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                    timeout=120  # 增加超时时间到120秒
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        分析结果 = result['choices'][0]['message']['content']
                        print("✅ DeepSeek API调用成功")
                        return 分析结果
                else:
                    print(f"⚠️ API调用失败 (尝试 {attempt+1}/{max_retries}), 状态码: {response.status_code}")
                    time.sleep(2)
            except Exception as e:
                print(f"⚠️ API调用异常 (尝试 {attempt+1}/{max_retries}): {e}")
                time.sleep(2)
        
        return None
    
    def 绘制榨利趋势图(self, 近两年数据, 时间戳):
        """绘制榨利和豆油价格趋势图"""
        print("\n📈 正在生成榨利趋势图...")
        
        图片路径 = f"static/images/margin-charts"
        if not os.path.exists(图片路径):
            os.makedirs(图片路径)
            
        文件名 = f"margin-trend-{时间戳}.png"
        完整路径 = os.path.join(图片路径, 文件名)
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # 绘制价格 (左轴)
        ax1.set_xlabel('日期')
        ax1.set_ylabel('豆油期货价格', color='tab:blue')
        ax1.plot(近两年数据['日期'], 近两年数据['豆油价格'], color='tab:blue', label='豆油价格', alpha=0.8)
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        # 创建第二个 Y 轴绘制榨利
        ax2 = ax1.twinx()
        ax2.set_ylabel('压榨利润 (元/吨)', color='tab:red')
        ax2.plot(近两年数据['日期'], 近两年数据['榨利'], color='tab:red', label='盘面榨利', linewidth=2)
        ax2.tick_params(axis='y', labelcolor='tab:red')
        
        # 填充盈利/亏损区域
        ax2.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax2.fill_between(近两年数据['日期'], 0, 近两年数据['榨利'], where=(近两年数据['榨利'] >= 0), color='green', alpha=0.1)
        ax2.fill_between(近两年数据['日期'], 0, 近两年数据['榨利'], where=(近两年数据['榨利'] < 0), color='red', alpha=0.1)
        
        plt.title('豆油价格 vs 压榨利润 (近两年趋势)')
        fig.tight_layout()
        plt.grid(True, alpha=0.3)
        
        plt.savefig(完整路径, dpi=150)
        plt.close()
        
        print(f"✅ 趋势图已生成: {完整路径}")
        return f"/images/margin-charts/{文件名}"

    def 保存分析结果(self, 分析结果, 数据来源, 近两年数据=None):
        """保存分析结果到 Hugo 博客目录并生成图表"""
        print("\n💾 保存分析结果至博客...")
        
        # 结果保存路径
        博客目录 = "content/posts"
        if not os.path.exists(博客目录):
            os.makedirs(博客目录)
            
        当前日期 = datetime.now()
        时间戳 = 当前日期.strftime("%Y%m%d_%H%M%S")
        文件名 = f"soy-oil-margin-analysis-{时间戳}.md"
        结果文件 = os.path.join(博客目录, 文件名)
        
        # 绘制趋势图
        图表路径 = ""
        if 近两年数据 is not None:
            图表路径 = self.绘制榨利趋势图(近两年数据, 时间戳)
        
        # 移除连续多余空行，确保紧致
        import re
        精化结果 = re.sub(r'\n{3,}', '\n\n', 分析结果.strip())
        
        # 构建 Hugo Front Matter
        报告标题 = f"豆油压榨利润深度分析报告 ({当前日期.strftime('%Y年%m月%d日')})"
        
        图表引用 = f"\n![榨利趋势图]({图表路径})\n" if 图表路径 else ""
        
        报告内容 = f"""---
title: "{报告标题}"
date: {当前日期.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
categories: ["市场分析"]
tags: ["豆油", "榨利", "DeepSeek", "图表分析"]
---

### 🫘 豆油策略内参 `{当前日期.strftime("%m-%d")}`

{图表引用}

{精化结果}

> _数据来源: {数据来源}_
> _Generated by DeepSeek AI_
"""
        
        with open(结果文件, 'w', encoding='utf-8') as f:
            f.write(报告内容)
        
        print(f"✅ 博文已生成并保存至: {结果文件}")
        return 结果文件

    def 发布至博客(self, 结果文件):
        """将生成的博文自动推送到 GitHub"""
        print("\n🚀 开始自动发布至远程仓库...")
        import subprocess
        
        try:
            # 执行 Git 命令
            subprocess.run(["git", "add", 结果文件], check=True)
            subprocess.run(["git", "commit", "-m", f"Auto-post: {os.path.basename(结果文件)}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ 博客已成功推送到远程仓库！")
            return True
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False
    
    def 微信推送分析报告(self, 报告文件, 分析结果):
        """通过WxPusher发送分析报告到微信"""
        print("\n📱 发送微信推送...")
        
        try:
            # 读取报告内容
            with open(报告文件, 'r', encoding='utf-8') as f:
                报告内容 = f.read()
            
            # 构建推送内容 - 直接发送完整的markdown格式报告内容
            推送内容 = 报告内容
            
            # 构建请求数据
            推送数据 = {
                "appToken": self.WXPUSHER_APP_TOKEN,
                "content": 推送内容,
                "summary": "豆油购买决策分析",
                "contentType": 3,  # 3表示markdown格式
                "topicIds": self.WXPUSHER_TOPIC_IDS,
                "verifyPay": False
            }
            
            # 发送请求
            response = requests.post(
                self.WXPUSHER_URL,
                json=推送数据,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    print(f"✅ 微信推送成功: {result.get('msg', '推送成功')}")
                    return True
                else:
                    print(f"❌ 微信推送失败: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"❌ 微信推送请求失败: HTTP {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 微信推送异常: {e}")
            return False
    
    def 运行完整分析(self, 数据文件=None, 使用独立数据=True):
        """运行完整的DeepSeek分析流程"""
        print("=" * 70)
        print("🚀 开始DeepSeek榨利分析流程")
        print("=" * 70)
        
        # 1. 获取数据
        if 使用独立数据:
            print("🔄 使用独立数据获取模式")
            # 独立获取数据
            榨利数据 = self.独立获取数据()
            if 榨利数据 is None:
                print("❌ 独立数据获取失败，尝试使用现有数据文件")
                使用独立数据 = False
        
        if not 使用独立数据:
            print("📂 使用现有数据文件模式")
            # 获取或使用指定的数据文件
            if not 数据文件:
                数据文件 = self.获取最新数据文件()
                if not 数据文件:
                    return
            
            # 读取数据
            榨利数据 = self.读取数据(数据文件)
            if 榨利数据 is None:
                print("❌ 数据读取失败，流程终止")
                return
        
        # 2. 提取近两年数据
        近两年数据 = self.提取近两年数据(榨利数据)
        if 近两年数据 is None:
            print("❌ 近两年数据提取失败，流程终止")
            return
        
        # 3. 生成数据摘要
        数据摘要 = self.生成数据摘要(近两年数据)
        if 数据摘要 is None:
            print("❌ 数据摘要生成失败，流程终止")
            return
        
        # 4. 构建分析提示词
        提示词 = self.构建分析提示词(数据摘要, 近两年数据)
        if 提示词 is None:
            print("❌ 提示词构建失败，流程终止")
            return
        
        # 5. 调用DeepSeek API
        分析结果 = self.调用DeepSeekAPI(提示词)
        if 分析结果 is None:
            print("❌ DeepSeek API调用失败，流程终止")
            return
        
        # 6. 保存分析结果
        数据来源 = "独立获取数据" if 使用独立数据 else 数据文件
        结果文件 = self.保存分析结果(分析结果, 数据来源, 近两年数据)
        
        # 7. 发送微信推送
        if 结果文件:
            # 这里的推送内容不包含图片路径（WxPusher 网页端可能不直接支持本地路径）
            推送成功 = self.微信推送分析报告(结果文件, 分析结果)
            if 推送成功:
                print("📱 微信推送发送成功")
            else:
                print("⚠️ 微信推送发送失败，但不影响分析结果")

        # 8. 发布至博客 (可选)
        # self.发布至博客(结果文件)
        
        print("\n" + "=" * 70)
        print("✅ DeepSeek榨利分析流程完成!")
        print("=" * 70)
        
        if 结果文件:
            print(f"📊 分析报告: {结果文件}")
        
        # 显示部分分析结果，重点突出豆油相关内容
        print("\n📋 DeepSeek分析摘要 (重点：豆油买货时机):")
        print("-" * 70)
        
        # 提取豆油相关的内容作为摘要
        豆油关键词 = ['豆油', '买货', '买入', '采购', '时机', '价格区间']
        分析行列表 = 分析结果.split('\n')
        
        豆油相关内容 = []
        for 行 in 分析行列表:
            if any(关键词 in 行 for 关键词 in 豆油关键词):
                豆油相关内容.append(行.strip())
        
        if 豆油相关内容:
            # 显示前10行豆油相关内容
            for i, 内容 in enumerate(豆油相关内容[:10]):
                if 内容:
                    print(f"{i+1:2d}. {内容}")
        else:
            # 如果没有找到豆油相关内容，显示前500个字符
            摘要 = 分析结果[:500] + "..." if len(分析结果) > 500 else 分析结果
            print(摘要)
        
        print("-" * 70)
        
        print("=" * 70)
        
        return {
            '分析报告': 结果文件,
            '分析结果': 分析结果
        }

if __name__ == "__main__":
    # 创建分析器实例
    分析器 = 榨利DeepSeek分析器()
    
    # 运行完整分析
    分析器.运行完整分析()