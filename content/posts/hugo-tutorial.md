---
title: "Hugo 入门精简教程"
date: 2025-12-22T09:01:00+08:00
draft: false
tags: ["Hugo", "Tutorial"]
categories: ["技术"]
---
## 什么是 Hugo？

Hugo 是一个用 Go 语言编写的静态网站生成器。它以极快的构建速度和简单易用的特性深受开发者喜爱。

## 常用命令指南

### 1. 本地预览服务器
在撰写文章时，你可以通过以下命令在本地实时预览效果：
```bash
hugo server -D
```
- `-D` 参数表示连同草稿（draft: true）一起显示。

### 2. 创建新博文
```bash
hugo new content content/posts/my-new-post.md
```
这将会在 `content/posts/` 目录下创建一个包含基础元数据的 Markdown 文件。

### 3. 构建静态站点
```bash
hugo
```
运行后，生成的静态文件会存放于 `public/` 目录中。在我们的 GitHub Pages 流程中，这一步是由 GitHub Actions 自动完成的。

## 写作建议

1. **Front Matter**：文章顶部的 `---` 区域用于定义标题、日期、标签等信息。
2. **Markdown**：使用简洁的 Markdown 语法进行排版。
3. **Draft 状态**：当你还在修改文章时，可以将 `draft` 设为 `true`。发布时记得改为 `false`。

祝你写作愉快！
