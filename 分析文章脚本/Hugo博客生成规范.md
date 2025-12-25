# Python 生成 Hugo 博客规范

本文档总结了在 Python 脚本中自动生成 Hugo 博客文章的最佳实践和规范。

---

## 一、目录结构配置

```python
import os

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Hugo 博客根目录（脚本在 分析文章脚本/ 子目录内）
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
# 或通过环境变量配置
HUGO_BLOG_DIR = os.getenv("HUGO_BLOG_DIR", ".")

# 文章目录
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")

# 图片目录（静态资源）
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

# 确保目录存在
os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
```

---

## 二、Front Matter 规范

Hugo 使用 YAML 格式的 Front Matter，放在文章开头的 `---` 之间。

### 2.1 必填字段

```yaml
---
title: "文章标题"
date: 2025-12-25T14:00:00+08:00
draft: false
---
```

### 2.2 推荐字段

```yaml
---
title: "大豆榨利深度分析报告"
date: 2025-12-25T14:00:00+08:00
lastmod: 2025-12-25T14:00:00+08:00
description: "自动化生成的压榨利润深度报告"
draft: false
categories: ["榨利深度分析"]
tags: ["大豆", "豆油", "豆粕", "期货"]
image: ../../images/charts/margin_chart_半年.png
author: ["AI分析师"]
---
```

### 2.3 Python 生成示例

```python
import pytz
from datetime import datetime

BEIJING_TZ = pytz.timezone('Asia/Shanghai')

def 生成front_matter(title, description, categories, tags, image_path=None):
    """生成 Hugo Front Matter"""
    now = datetime.now(BEIJING_TZ)
    date_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    front_matter = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
description: "{description}"
draft: false
categories: {categories}
tags: {tags}
"""
    if image_path:
        front_matter += f'image: {image_path}\n'
    
    front_matter += "---\n"
    return front_matter
```

---

## 三、图片引用规范

### 3.1 图片存放位置

```
Hugo-blog/
├── static/
│   └── images/
│       └── charts/          # 图表图片目录
│           ├── margin_chart_半年.png
│           └── margin_chart_一年.png
└── content/
    └── posts/
        └── 榨利深度分析报告.md
```

### 3.2 Markdown 中引用图片

```markdown
<!-- 方式1: 相对路径（推荐） -->
![半年走势](../../images/charts/margin_chart_半年.png)

<!-- 方式2: 绝对路径 -->
![半年走势](/images/charts/margin_chart_半年.png)
```

### 3.3 Python 保存图片

```python
import matplotlib.pyplot as plt

def 保存图表(fig, 文件名):
    """保存图表到 Hugo 静态目录"""
    完整路径 = os.path.join(HUGO_IMAGES_DIR, 文件名)
    fig.savefig(完整路径, dpi=100, bbox_inches='tight')
    plt.close()
    return 文件名
```

---

## 四、文件命名规范

### 4.1 固定文件名（覆盖更新）

适用于持续更新的报告：

```python
md_path = os.path.join(HUGO_CONTENT_DIR, "榨利深度分析报告.md")
```

### 4.2 日期文件名（历史归档）

适用于需要保留历史版本的报告：

```python
date_str = datetime.now().strftime('%Y-%m-%d')
slug = "oil-analysis"
filename = f"{date_str}-{slug}.md"
md_path = os.path.join(HUGO_CONTENT_DIR, filename)
```

---

## 五、完整生成函数示例

```python
import os
import pytz
from datetime import datetime

BEIJING_TZ = pytz.timezone('Asia/Shanghai')
HUGO_CONTENT_DIR = "content/posts"
HUGO_IMAGES_DIR = "static/images/charts"

def 生成hugo博客(title, content, categories, tags, images=None):
    """
    生成 Hugo 博客文章
    
    参数:
        title: 文章标题
        content: 文章正文（Markdown 格式）
        categories: 分类列表，如 ["期货分析"]
        tags: 标签列表，如 ["大豆", "豆油"]
        images: 图片文件名列表（可选）
    
    返回:
        保存的文件路径
    """
    now = datetime.now(BEIJING_TZ)
    date_str = now.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    # 构建 Front Matter
    image_line = ""
    if images:
        image_line = f"image: ../../images/charts/{images[0]}\n"
    
    hugo_content = f"""---
title: "{title}"
date: {date_str}
lastmod: {date_str}
description: "自动生成的分析报告"
draft: false
categories: {categories}
tags: {tags}
{image_line}---

{content}

---
*数据来源: AkShare | AI 分析: DeepSeek | 生成时间: {now.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 保存文件
    os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
    md_path = os.path.join(HUGO_CONTENT_DIR, f"{title}.md")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(hugo_content)
    
    print(f"✅ 博客文章已保存: {md_path}")
    return md_path
```

---

## 六、GitHub Actions 兼容性

确保脚本在云端运行时也能正确定位目录：

```python
# 通过环境变量指定博客根目录
HUGO_BLOG_DIR = os.getenv("HUGO_BLOG_DIR", ".")

# GitHub Actions 中设置
# env:
#   HUGO_BLOG_DIR: "."
```

---

## 七、注意事项

| 项目 | 规范 |
|------|------|
| 编码 | 统一使用 `UTF-8` |
| 时区 | 使用 `Asia/Shanghai` 北京时间 |
| 日期格式 | ISO 8601: `2025-12-25T14:00:00+08:00` |
| 图片格式 | 推荐 PNG，分辨率 100 DPI |
| 路径分隔符 | 使用 `os.path.join()` 保证跨平台兼容 |
| Front Matter | YAML 格式，title 用双引号包裹 |
| **AI 内容** | **禁止用 ` ```markdown ` 包裹整篇文章（文章本身就是 Markdown）** |

### ⚠️ AI 返回内容处理（重要）

调用 AI（如 DeepSeek）生成报告时，**禁止用 ` ```markdown ` 包裹整篇返回内容**：

- ✅ **允许**：文章内嵌入 `python`、`json`、`sql` 等代码块
- ❌ **禁止**：用 ` ```markdown ` 包裹整篇文章（因为文章本身就是 Markdown 文件）

**错误示例（AI 返回内容）**：
```
```markdown
# 分析报告标题
这是正文内容...
```　
```

**正确示例（AI 返回内容）**：
```
# 分析报告标题
这是正文内容...
```

**处理函数**：

```python
def 清理ai输出(ai_text):
    """移除 AI 返回内容中包裹整篇文章的 markdown 代码块"""
    text = ai_text.strip()
    
    # 只移除包裹整篇文章的 ```markdown ... ```
    if text.startswith("```markdown"):
        text = text[len("```markdown"):].lstrip()
        if text.endswith("```"):
            text = text[:-3].rstrip()
    
    return text
```

**或在 AI prompt 中明确要求**：
```
请直接返回 Markdown 内容，不要用 ```markdown 代码块包裹整篇回复。
```



## 八、快速模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hugo 博客生成模板"""

import os
import pytz
from datetime import datetime

# ================= 配置 =================
BEIJING_TZ = pytz.timezone('Asia/Shanghai')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HUGO_BLOG_DIR = os.path.dirname(SCRIPT_DIR)
HUGO_CONTENT_DIR = os.path.join(HUGO_BLOG_DIR, "content", "posts")
HUGO_IMAGES_DIR = os.path.join(HUGO_BLOG_DIR, "static", "images", "charts")

# ================= 主函数 =================
def main():
    os.makedirs(HUGO_CONTENT_DIR, exist_ok=True)
    os.makedirs(HUGO_IMAGES_DIR, exist_ok=True)
    
    now = datetime.now(BEIJING_TZ)
    
    content = f"""---
title: "我的分析报告"
date: {now.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
lastmod: {now.strftime('%Y-%m-%dT%H:%M:%S+08:00')}
description: "自动生成的报告"
draft: false
categories: ["分析报告"]
tags: ["示例"]
---

## 报告内容

这里是正文...

---
*生成时间: {now.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    md_path = os.path.join(HUGO_CONTENT_DIR, "我的分析报告.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 完成: {md_path}")

if __name__ == "__main__":
    main()
```
