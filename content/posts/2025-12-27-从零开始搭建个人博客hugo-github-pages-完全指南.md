---
title: "从零开始搭建个人博客：Hugo + GitHub Pages 完全指南"
date: 2025-12-27T17:59:35+08:00
lastmod: 2025-12-27T17:59:35+08:00
categories: ["技术教程"]
tags: ["Hugo", "GitHub Pages", "静态网站", "博客搭建", "Markdown", "版本控制", "Web开发", "个人项目"]
---

## 前言

你是否想过拥有一个完全由自己掌控、快速、安全且免费的博客？告别臃肿的动态 CMS，拥抱简洁高效的静态网站生成器吧！本文将手把手教你使用 Hugo 和 GitHub Pages，从零开始搭建并部署你的个人博客。

## 为什么选择 Hugo + GitHub Pages？

### Hugo 的优势

*   **极速生成**：号称“世界上最快的静态网站生成器”，数千篇文章也能秒级构建。
*   **简单易用**：单二进制文件，无需复杂环境配置。
*   **丰富主题**：海量开源主题可供选择，一键应用。
*   **Markdown 友好**：专注内容创作，语法简洁。

### GitHub Pages 的优势

*   **完全免费**：提供 `username.github.io` 域名和托管服务。
*   **无缝集成**：与 Git 工作流完美结合，推送即部署。
*   **稳定可靠**：由 GitHub 基础设施保障。

## 准备工作

1.  **安装 Hugo**
    访问 [Hugo 官方安装指南](https://gohugo.io/installation/)，根据你的操作系统选择安装方式。
    在终端输入 `hugo version` 验证是否安装成功。
2.  **注册 GitHub 账号**
    如果你还没有账号，请前往 [GitHub](https://github.com) 注册。
3.  **安装 Git**
    下载并安装 [Git](https://git-scm.com/)。

## 第一步：在本地创建 Hugo 站点

打开终端，执行以下命令：

```bash
# 创建一个名为 myblog 的新站点
hugo new site myblog
cd myblog

# 初始化 Git 仓库
git init
```

## 第二步：为网站添加主题

Hugo 社区提供了大量主题，我们以简洁的 `PaperMod` 主题为例。

```bash
# 将主题添加为子模块
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# 复制主题示例配置到项目根目录
cp themes/PaperMod/exampleSite/config.yml .
```

接着，用文本编辑器打开根目录的 `config.yml` 文件，根据注释修改 `baseURL`、`title` 等基本配置。

## 第三步：创建你的第一篇文章

使用 Hugo 命令快速创建一篇博文：

```bash
hugo new posts/my-first-post.md
```

这条命令会在 `content/posts/` 目录下生成一个 Markdown 文件。用你喜欢的编辑器打开它，开始写作吧！文件头部是 Front Matter，用于设置标题、日期等元数据。

```yaml
---
title: "我的第一篇文章"
date: 2023-10-27T11:30:00+08:00
draft: false # 设为 false 以发布文章
---

这里是文章的正文，使用 **Markdown** 语法。
```

## 第四步：本地预览

在项目根目录运行以下命令启动本地服务器：

```bash
hugo server -D
```

打开浏览器访问 `http://localhost:1313`，你就能看到网站效果了。`-D` 参数意味着会渲染草稿（draft: true）的文章，方便预览。

## 第五步：部署到 GitHub Pages

### 1. 创建 GitHub 仓库

在 GitHub 上创建一个名为 `你的用户名.github.io` 的公开仓库（例如：`zhangsan.github.io`）。

### 2. 配置 Hugo 的发布目录

修改 `config.yml`，确保 `baseURL` 设置为 `https://你的用户名.github.io/`，并添加 `publishDir` 设置：

```yaml
baseURL: "https://zhangsan.github.io/"
languageCode: "zh-cn"
title: "我的个人博客"
theme: "PaperMod"

# 新增以下配置
publishDir: "docs" # 将生成的静态文件输出到 docs 文件夹
```

### 3. 生成静态文件并推送

在终端执行：

```bash
# 生成静态网站到 docs 文件夹（不再使用默认的 public）
hugo

# 将更改添加到 Git
git add .
git commit -m "初始化博客并生成首次构建"

# 添加远程仓库（请替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git

# 推送代码到 GitHub
git push -u origin main
```

### 4. 在 GitHub 上启用 Pages

1.  进入你的仓库页面，点击 **Settings**。
2.  在左侧边栏找到 **Pages**。
3.  在 **Source** 分支下拉菜单中，选择 `main` 分支，并将文件夹设置为 `/docs`。
4.  点击 **Save**。

稍等片刻（通常一两分钟），你的博客就可以通过 `https://你的用户名.github.io` 访问了！

![部署成功示意图](https://example.com/images/deploy-success.png)

## 进阶与优化

*   **自定义域名**：在仓库 Pages 设置中绑定你自己的域名。
*   **使用 GitHub Actions 自动化**：创建 workflow 文件，实现提交源码后自动构建和部署。
*   **评论系统**：集成 Giscus（基于 GitHub Discussions）或 Utterances 等静态博客评论工具。
*   **网站分析**：使用 Google Analytics 4 或 Umami 进行访问统计。

## 常见问题

**Q：为什么我推送后网站没有更新？**
A：GitHub Pages 构建需要一点时间，请等待几分钟并刷新。可以在仓库的 **Actions** 标签页查看构建状态。

**Q：如何更新主题？**
A：进入项目目录，运行 `git submodule update --remote --merge`。

**Q：我想修改主题样式怎么办？**
A：建议在项目根目录创建 `assets/css/extended/custom.css` 文件，并在 `config.yml` 中配置引入，以覆盖主题默认样式。

## 结语

恭喜你！你已经成功拥有了一个快速、现代且完全免费的个人博客。接下来，专注于创作精彩的内容吧。Hugo 的强大功能和 GitHub 生态的丰富工具，将为你提供持续的支持。

> **提示**：博客的核心永远是内容。工具只是手段，坚持写作和分享才是最重要的。

有任何问题，欢迎在 Hugo 社区或 GitHub 上讨论。Happy Blogging！

**相关资源**

*   [Hugo 官方文档](https://gohugo.io/documentation/)
*   [PaperMod 主题文档](https://github.com/adityatelange/hugo-PaperMod/wiki)
*   [GitHub Pages 文档](https://docs.github.com/zh/pages)