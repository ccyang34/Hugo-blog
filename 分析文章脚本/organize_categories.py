import os
import re

# 配置
POSTS_DIR = "/Users/ccy/Hugo-blog/content/posts"

# 关键词定义
FUTURES_KEYWORDS = ["榨利", "豆油", "棕榈油", "菜油", "基差", "持仓", "期货", "大豆", "油脂", "豆粕", "crush-margin", "压榨"]
INVESTMENT_KEYWORDS = ["投资", "理财", "基金", "股票", "A股", "公募基金", "配置框架", "资产配置", "有色金属", "证券", "市值", "大类资产"]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Frontmatter (YAML 部分)
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)
    body = content[match.end():]

    # 排除性关键词 (如果包含这些，即使有投资关键词也不归入投资理财)
    EXCLUDE_FROM_INVESTMENT = ["Claude", "AI", "Agent", "编程", "代码", "程序员", "Github", "开源", "开发", "工具"]

    # 判断类别
    is_futures = any(kw in filepath or kw in frontmatter for kw in FUTURES_KEYWORDS)
    is_investment = any(kw in filepath or kw in frontmatter for kw in INVESTMENT_KEYWORDS)
    
    # 投资理财的额外检查
    if is_investment:
        # 如果包含排除词，则取消投资理财分类
        if any(ex in filepath or ex in frontmatter for ex in EXCLUDE_FROM_INVESTMENT):
            is_investment = False

    new_category = None
    if is_futures:
        new_category = "期货"
    elif is_investment:
        new_category = "投资理财"

    if not new_category:
        return False # 不相关的照旧不改

    # 更新 categories 字段
    # 匹配 categories: [...] 或 categories: "..." 或 categories: \n - ...
    if 'categories:' in frontmatter:
        # 替换现有的 categories 字段
        updated_frontmatter = re.sub(r'categories:\s*\[?.*?\]?\n', f'categories: ["{new_category}"]\n', frontmatter)
    else:
        # 如果没有 categories 字段，则添加一个
        updated_frontmatter = frontmatter + f'\ncategories: ["{new_category}"]'
    
    if updated_frontmatter == frontmatter:
        return False

    new_content = f"---\n{updated_frontmatter}\n---\n{body}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {os.path.basename(filepath)} -> {new_category}")
    return True

if __name__ == "__main__":
    count = 0
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            if process_file(os.path.join(POSTS_DIR, filename)):
                count += 1
    print(f"\n✨ 总计更新文章数量: {count}")
