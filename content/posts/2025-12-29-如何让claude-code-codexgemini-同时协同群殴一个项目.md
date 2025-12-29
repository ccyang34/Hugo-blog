---
title: "如何让Claude Code /Codex/Gemini 同时协同群殴一个项目？"
date: 2025-12-29T17:42:32+08:00
lastmod: 2025-12-29T17:42:32+08:00
categories: ["AI 编程工具"]
tags: ["Schaltwerk", "AI 编程", "Git Worktree", "并行开发", "Claude Code", "Rust", "自动化", "代码审查"]
---

现在你在同一个项目里，可以同时启动十个 Claude Code 或者 Codex。

Schaltwerk 的核心逻辑只有三个字：并发流。

你可能会问，这么多 AI 同时改一个项目，代码岂不是要炸？

还真不会！因为它底层用了 Git Worktree。

Git Worktree 不熟悉也完全没关系，Schaltwerk 是一个完备的图形界面，它做了非常良好的封装，你根本不需要了解任何的原理，直接点两下就可以使用。

每一个 AI Agent 启动时，Schaltwerk 都会为它瞬间创建一个独立的工作树，一个完全隔离的平行宇宙。

- Agent A 在修 Bug。
- Agent B 在写新功能。
- Agent C 在重构文档。

它们互不干扰，文件系统完全隔离。

现在的开发流程变成了这样：

打开终端，一键安装，下面是 Mac 的一键安装，Windows 用户请观看文章后提供仓库链接。

```bash
brew install --cask 2mawi2/tap/schaltwerk
```

打开软件，配置本地相关的 CLI，它会自主地扫描本地安装的所有的 CLI 客户端，如果没安装的话，请按照相关的安装说明进行安装即可。

![7065889a-c842-434d-ba15-b84224f17771.png](https://mmbiz.qpic.cn/sz_mmbiz_png/4HWyricuhgQdRAdwUpiaCmflnSS1aRClMMzGSsJbDU6fINJibLr0Nf9iciccKTBUPibHyjiaoMxJL5mMHdWfFGhalvgDg/640?wx_fmt=png)

这个项目的细节做得非常的到位，完全为 AI Coding 而生，打开任意的一个项目，Schaltwerk 会自动打开 Claude.md 文件。

![10241035-3acc-401a-a0b8-58232ba6e313.png](https://mmbiz.qpic.cn/sz_mmbiz_png/4HWyricuhgQdRAdwUpiaCmflnSS1aRClMM3ODJqoH7PiboAbFgyYrJpSDlXGGklcybZIibe8nIGR6Ssw4YzQAsexdw/640?wx_fmt=png)

使用这个软件和其他的 VS Code 不一样，我们先不要急着写代码。

第一步先写 Spec。

![2b4f61a4-0aff-4cdc-a76b-2dd4a1e153ac.png](https://mmbiz.qpic.cn/sz_mmbiz_png/4HWyricuhgQdRAdwUpiaCmflnSS1aRClMMQjjgWGK0YibKicdZSHjibhEb2uR3o06lMZzFJYJWp4XTBmGKPI6t5hqHA/640?wx_fmt=png)

可以把你脑子里的三个需求依次写下来。

- 比如 给登录页加验证码。
- 比如 优化数据库查询。
- 比如 更新 API 文档。

![3a658c3e-3f0a-4f4e-a332-18a679bd8142.png](https://mmbiz.qpic.cn/sz_mmbiz_png/4HWyricuhgQdRAdwUpiaCmflnSS1aRClMMNayJMb8d7TXMFKicKv8SlY8EW7abfbyKibRyTagAGic4ibTMnanKTnAzeg/640?wx_fmt=png)

写完之后，我们可以对它的项目配置做一下更改，比如这里的描述，还有初始化的提示词，以及主分支，就是启动它的 Agent 的选项，这里的 3 处我选择了 Cloud Code，对于不同的任务，可以启用不同的 CLI 客户端。

连续点击启动 Start Agent 会弹出终端窗口，此时三个 AI 同时开始干活。

![5c67a06a-d6ba-413d-b109-e39a5b6dafed.png](https://mmbiz.qpic.cn/sz_mmbiz_png/4HWyricuhgQdRAdwUpiaCmflnSS1aRClMMFvXeunIR60hl7IG3jUF9kZCIQzsAcNDzlkafibt9RibQwF5uBk1bvEibA/640?wx_fmt=png)

你可以悠闲地喝口咖啡看着三个进度条同时推进。

谁先干完，你就切过去。

Schaltwerk 提供了 GitHub 风格的 Diff 视图，你只负责 Review。

行，就合并。不行，要么重写或者直接把这个平行宇宙销毁。

和之前直接开多个窗口不同，这里不需要你处理复杂的 Git 分支冲突，它把底层最繁琐的隔离工作全部自动化了。

你只负责定义需求，AI 负责并行实现，Schaltwerk 负责流量分发。

而且它是用 Rust 写的，速度极快。

下载地址：

https://link.bytenote.net/5MHVcn

快来把你的终端变成一条 24 小时运转的流水线。

[GLM4.7发布，较上一代提升明显！](https://mp.weixin.qq.com/s?__biz=MzIzMzQyMzUzNw==&mid=2247511218&idx=1&sn=acb3d7f9fe92c606dc8955df778d969b&scene=21#wechat_redirect)

[我发现Gemini + NotebookLM就是个人知识库的最终解！](https://mp.weixin.qq.com/s?__biz=MzIzMzQyMzUzNw==&mid=2247511194&idx=1&sn=492b587cc8ff1e0d689facc1b26753cc&scene=21#wechat_redirect)

[A社自家的Claude  Skills 仓库都有哪些宝贝技能？](https://mp.weixin.qq.com/s?__biz=MzIzMzQyMzUzNw==&mid=2247511164&idx=1&sn=345a980e8dfa31de7c4ecb53eeaa156d&scene=21#wechat_redirect)

[Claude Code 2.0.74更新，越来越IDE了！](https://mp.weixin.qq.com/s?__biz=MzIzMzQyMzUzNw==&mid=2247511159&idx=1&sn=d27a36318b5dad7f8bf69221b4375dc9&scene=21#wechat_redirect)

[如何把Claude Agent Skills打包部署成一个应用？](https://mp.weixin.qq.com/s?__biz=MzIzMzQyMzUzNw==&mid=2247511147&idx=1&sn=f5651efe87e14d9d7981aed36c6f3cb3&payreadticket=HNZkPsbPpABcpmTXeKYxtl6zWMhkDB8LQuvg_GER0HHfacJf7wbmlrLXIWdpmQR8tKzFFfY&scene=21#wechat_redirect)