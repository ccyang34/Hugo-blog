import os
import re
import json
import requests
import time

# 配置
POSTS_DIR = "/Users/ccy/Hugo-blog/content/posts"
DEEPSEEK_API_KEY = "sk-f637d9858dda4c86bd3ec411a6b4bb81"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 预设分类及其描述
PRESET_CATEGORIES = {
    "研究报告": "长篇、深度、结构化的正式报告。",
    "期货分析": "针对大豆、油脂、豆油、棕榈油、基差、榨利等期货品种的产业链分析与行情研判。",
    "市场分析": "针对股票、宏观经济、行业资金流向等非期货品种的周期性复盘。",
    "投资策略": "偏向方法论、配置逻辑、模型工具的使用、避坑指南。",
    "投资理财": "泛理财、公募基金、个人财务规划。",
    "AI与技术": "AI工具（如Claude, NotebookLM, Gemini, ChatGPT）、编程开发、自动化脚本、量化技术、技术干货。",
    "新闻资讯": "宏观新闻事件点评、行业突发新闻。",
    "个人随笔": "生活、运动（乒乓球）、学习方法、随感、认知进化。"
}

# 强制词云
AI_FORCE_KEYWORDS = ["NotebookLM", "Claude", "Gemini", "ChatGPT", "AI", "Agent", "Manus", "AnyGen"]
MARKET_PRIORITY_KEYWORDS = ["资金流向", "股市", "A股", "行情日报", "宽度分析"]

def call_deepseek_category(title, content_preview):
    """调用 DeepSeek API 获取最合适的分类"""
    
    # 市场分析优先级判断：如果包含资金流向等核心词，即使有 AI 也是市场分析
    for kw in MARKET_PRIORITY_KEYWORDS:
        if kw.lower() in title.lower():
            return "市场分析"

    # 强制 AI 逻辑检查
    for kw in AI_FORCE_KEYWORDS:
        if kw.lower() in title.lower():
            return "AI与技术"

    prompt = f"""你是一个专业的博客文章分类专家。请根据以下文章的标题和内容片段，将其归入最合适的【唯一】一个分类中。

## 候选分类及定义：
{json.dumps(PRESET_CATEGORIES, ensure_ascii=False, indent=2)}

## 待分类文章信息：
标题：{title}
内容片段：{content_preview[:800]}

## 要求：
1. 仅返回分类名称，不要包含任何解释或标点符号。
2. 必须且只能从候选分类中选择一个。
3. 如果文章同时涉及多个领域，选择最核心的主题。
4. 特别注意：涉及到 AI 工具（如 NotebookLM）的应用虽然有个人感悟，但其技术属性更强，应归入“AI与技术”。

分类结果："""
    
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': '你是一个精准的分类助手。'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.3
    }

    try:
        response = requests.post(f"{DEEPSEEK_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content'].strip()
        for cat in PRESET_CATEGORIES.keys():
            if cat in result:
                return cat
        return result
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Frontmatter
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)
    # 确保 body 从正确的结尾开始 (跳过 ---)
    body_start_match = re.search(r'^---\s*\n.*?\n---\s*\n', content, re.DOTALL)
    if not body_start_match:
        # 兼容性处理
        body = content[match.end():].lstrip('- \n')
    else:
        body = content[body_start_match.end():]

    # 提取标题
    title_match = re.search(r'title:\s*["\']?(.*?)["\']?\n', frontmatter)
    title = title_match.group(1) if title_match else os.path.basename(filepath)

    # 检查当前分类
    current_cat_match = re.search(r'categories:\s*\["(.*?)"\]', frontmatter)
    current_cat = current_cat_match.group(1) if current_cat_match else ""
    if not current_cat:
        current_cat_match = re.search(r'categories:\s*\n\s*-\s*["\']?(.*?)["\']?\n', frontmatter)
        current_cat = current_cat_match.group(1) if current_cat_match else ""

    needs_recollect = current_cat in ["未分类", "实战指南", "", "[]", "None"] or 'categories:' not in frontmatter
    
    if not needs_recollect:
        # 如果当前分类已经是 7 大类之一，且不含强制定正词，则跳过
        if current_cat in PRESET_CATEGORIES:
            # 特殊情况：如果是 AI 词但被分到了别的类，强制重分
            is_ai_misclassified = current_cat != "AI与技术" and any(kw.lower() in title.lower() for kw in AI_FORCE_KEYWORDS)
            if not is_ai_misclassified:
                return False

    # 获取 AI 分类
    print(f"🔍 正在为文章分析分类: {title} (当前状态: {current_cat or '缺失'})...")
    new_category = call_deepseek_category(title, body[:1000])
    
    if not new_category or new_category not in PRESET_CATEGORIES:
        print(f"⚠️ 分类返回异常: {new_category}，跳过该文件。")
        return False

    # 更新 categories 字段
    if 'categories:' in frontmatter:
        # 更加健壮的正则表达式替换
        new_frontmatter = re.sub(r'categories:.*?\n(\s*-.*?\n)*', f'categories: ["{new_category}"]\n', frontmatter + "\n", flags=re.DOTALL).strip()
    else:
        new_frontmatter = frontmatter.strip() + f'\ncategories: ["{new_category}"]'
    
    if new_frontmatter == frontmatter:
        return False

    new_content = f"---\n{new_frontmatter}\n---\n{body}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 更新成功 -> {new_category}")
    return True

if __name__ == "__main__":
    count = 0
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    print(f"🚀 开始检查并清理博客文章分类 (共 {len(files)} 篇)...")
    
    for filename in files:
        if process_file(os.path.join(POSTS_DIR, filename)):
            count += 1
        time.sleep(0.05)
        
    print(f"\n✨ 分类任务完成！总计修正数量: {count}")
