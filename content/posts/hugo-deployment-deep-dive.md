---
title: "从零到一：Hugo + GitHub Actions 部署实战全记录"
date: 2025-12-22T09:02:00+08:00
draft: false
tags: ["Hugo", "GitHub Actions", "Deployment"]
categories: ["AI与技术"]
---
## 序章

本文记录了本博客从环境搭建到成功部署至 GitHub Pages 的完整流程，包括在过程中遇到的坑以及如何修复它们的具体调试细节。

## 1. 环境准备与初始化

### 安装 Hugo (Mac 环境)
使用 Homebrew 安装 Extended 版本，确保能运行复杂的 CSS/SCSS 主题：
```bash
brew install hugo
```

### 初始化站点
```bash
hugo new site Hugo-blog --force
git init
```

### 集成 Ananke 主题
为了方便后续管理和更新，我们使用 Git 子模块的方式添加主题：
```bash
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke.git themes/ananke
echo "theme = 'ananke'" >> hugo.toml
```

## 2. GitHub Actions 自动化流水线

我们创建了 `.github/workflows/hugo.yml` 文件。这一步最关键的细节是使用官方推荐的 Action，并配置正确的权限。

### 关键配置片段：
- **权限设置**：必须赋予 `pages: write` 和 `id-token: write`，Actions 才能替代你发布内容。
- **发布源选择**：现代化的部署方式是利用 GitHub Actions 生成 Artifact 直接推送到 Pages 节点，而不再依赖 `gh-pages` 分支。

## 3. 调试实战：解决 404 错误

在推送完第一版代码后，我们遇到了经典的 **404 Not Found**。以下是排查和修复的过程：

### 坑 1：GitHub 端的 Source 设置
**现象**：代码推送到位，Actions 也跑完了，但访问链接报错。
**原因**：GitHub 仓库默认认为你会从某个“分支”部署，而我们使用的是 Actions 模式。
**解决**：进入 `Settings > Pages`，将 **Build and deployment > Source** 改为 **"GitHub Actions"**。

### 坑 2：工作流文件的小瑕疵
**现象**：在某些环境中构建流程略显冗余。
**排查**：我们发现 `runs-id: ubuntu-latest` 是一行多余配置（拼写错误且不必要）。
**修复**：清理配置，确保 `runs-on: ubuntu-latest` 是唯一的主机定义。

### 坑 3：baseURL 的坑
**现象**：页面 CSS 加载异常或跳转 404。
**原因**：`hugo.toml` 里的 `baseURL` 设置为了默认值，未与 GitHub Pages 的域名对应。
**修复**：将其改为 `https://ccyang34.github.io/Hugo-blog/`。

## 4. 总结

部署 Hugo 网站并不难，但 **GitHub Actions 的权限设置** 和 **Pages 端的 Source 指定** 是初学者最容易掉坑的地方。

一旦配置完成，你只需要关注 Markdown 写作本身，Git Push 之后的一切都会自动搞定。

---
*本文由 Antigravity 整理发布，记录了一次真实的 Pair Programming 实战。*
