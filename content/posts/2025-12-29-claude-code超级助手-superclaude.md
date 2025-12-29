---
title: "Claude Code超级助手 - SuperClaude"
date: 2025-12-29T21:40:45+08:00
lastmod: 2025-12-29T21:40:45+08:00
categories: ["AI编程工具"]
tags: ["SuperClaude", "Claude Code", "AI开发助手", "配置框架", "MCP集成", "AI编程", "开源工具"]
---

SuperClaude是一个专门为Claude Code设计的综合配置框架，旨在将Claude Code转变为一个专业的AI开发助手。它通过结构化的配置文件和专业化的工作流程，极大地增强了Claude Code的开发能力。

前天发布“[AI Coding 开发范式：OpenSpec，从0到1实践指南](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=4&sn=79ab623381f29ce8440edf32bb530fd3&scene=21#wechat_redirect)”免费开源工具－claude-code-router：让你丝滑纵享各种Claude Code模型”时，说一个人带着6个MCP干项目简直不要太爽，今天又发现一个一次性集成30个命令、16个智能体、7大行为模式和8个MCP集成服务（还在不断扩展ing...），零编程经验也能开发复杂项目的Claude Code超级助手具－－SuperClaude，下面我就来介绍一个它的详细使用。

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rgibyk9H4duOs1AlPETicvB7n4vhxMkicSZ4SKQgYziaIiciccHmaYe3iaPecxMS7jrsRibTUYia0ez3IcBSWQ/640?wx_fmt=png&from=appmsg)

## 项目介绍

SuperClaude 是一个轻量级的嵌入式配置框架，它将 Claude Code 从一个通用的 AI 助手转变为一个专门的上下文感知开发伙伴。它应用软件工程原理，无需额外的代码或外部工具。

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVwd6rDKLsqGKRyNF6wEBK0y1BtBcw47feX7MzHl8M1bFLS0ASRvRAqQ/640?wx_fmt=png&from=appmsg)

项目URL：https://github.com/SuperClaude-Org/SuperClaude_Framework

`没有安装Claude code的用户需要先安装Claude code，参考：`

`[免费开源工具－claude-code-router：让你丝滑纵享各种Claude Code模型](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=2&sn=8ee3a55528520d59877008e7d132a618&scene=21#wechat_redirect)`

## 安装

### 环境检查

首先检查下Python环境，这个应该大家都有：

```
❯ python --version  
Python 3.14.0  

❯ pip --version  
pip 24.2 from /opt/anaconda3/lib/python3.12/site-packages/pip (python 3.12)  
```

### 安装

官方给了三种方式

* **方式一：pipx**

```
pipx install SuperClaude && pipx upgrade SuperClaude && SuperClaude install  

 installed package superclaude 4.1.9, installed using Python 3.13.3  
 These apps are now globally available  
   - superclaude  
done! ✨ 🌟 ✨  
superclaude is already at latest version 4.1.9 (location:  
/Users/sun/.local/pipx/venvs/superclaude)  
📦 Installing SuperClaude commands to /Users/sun/.claude/commands/sc...  

✅ Installed 31 commands:  
   - /agent  
   - /document  
   - /spawn  
   - /estimate  
   - /spec-panel  
   - /index-repo  
   - /implement  
   - /troubleshoot  
   - /business-panel  
   - /improve  
   - /recommend  
   - /explain  
   - /reflect  
   - /analyze  
   - /workflow  
   - /select-tool  
   - /help  
   - /load  
   - /README  
   - /sc  
   - /research  
   - /index  
   - /build  
   - /save  
   - /git  
   - /task  
   - /design  
   - /pm  
   - /cleanup  
   - /test  
   - /brainstorm  

📁 Installation directory: /Users/sun/.claude/commands/sc  

💡 Tip: Restart Claude Code to use the new commands  
```

* **方式二：pip**

```
pip install SuperClaude && pip upgrade SuperClaude && SuperClaude install  
```

* **方式三：npm**

```
npm install -g @bifrost_inc/superclaude && superclaude install  
```

## 使用

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rgibyk9H4duOs1AlPETicvB7ndJSLbjthe1DL0Sm1GrGiayiaPOlqV7qXhQwXsXD7aqYbJoxhLBVtaTfw/640?wx_fmt=png&from=appmsg)

SuperClaude 的所有功能都通过命令调用。基本语法如下：

```
/command [flags] [arguments]  

/命令名 --标志1 --标志2 --persona-角色名 "任务描述"  
```

**注意事项：**

* ✅ 使用直接斜杠格式：/build, /analyze, /review
* ✅ 标志使用双破折号：-flag
* ✅ Persona作为通用标志使用：-persona-名称

### 命令

**🧠 规划与设计 (4)**  
/brainstorm - 结构化头脑风暴  
/design - 系统架构  
/estimate - 时间/工作量估算  
/spec-panel - 规格分析

**💻 开发 (5)**  
/implement - 代码实现  
/build - 构建工作流  
/improve - 代码改进  
/cleanup - 重构  
/explain - 代码解释

**🧪 测试与质量 (4)**  
/test - 测试生成  
/analyze - 代码分析  
/troubleshoot - 调试  
/reflect - 回顾

**📚 文档 (2)**  
/document - 文档生成  
/help - 命令帮助

**🔧 版本控制 (1)**  
/git - Git操作

**📊 项目管理 (3)**  
/pm - 项目管理  
/task - 任务跟踪  
/workflow - 工作流自动化

**🔍 研究与分析 (2)**  
/research - 深度网络研究  
/business-panel - 业务分析

**🎯 实用工具 (9)**  
/agent - AI智能体  
/index-repo - 仓库索引  
/index - 索引别名  
/recommend - 命令推荐  
/select-tool - 工具选择  
/spawn - 并行任务  
/load - 加载会话  
/save - 保存会话  
/sc - 显示所有命令

### 常用示例：

* **核心开发流程命令**

```
# 这三个命令大概是比较常用的组合  
/sc:brainstorm "移动端支付系统"# 苏格拉底式提问，挖掘需求  
/sc:analyze --focus architecture   # 架构分析，感觉还挺全面  
/sc:implement "支付安全模块"# 多阶段实现，不只是简单的代码生成  
```

* **质量保证命令**

```
/sc:test --coverage             # 生成测试用例，覆盖率分析  
/sc:review --focus security     # 代码审查，安全视角    
/sc:troubleshoot "性能瓶颈" # 系统诊断，找根因  
```

* **高级工程命令**

```
/sc:refactor --scope module     # 模块级重构  
/sc:optimize --focus memory     # 性能优化  
/sc:design "微服务架构；TDD架构等" # 系统设计  
/sc:docs --format api          # 文档生成  
```

## FAQ

官方中文文档：https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/README-zh.md

## Claude Code及AI编程推荐阅读

[免费开源工具－claude-code-router：让你丝滑纵享各种Claude Code模型](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484948&idx=1&sn=ccb97242bfcb58fe43b1d98acb792aa2&scene=21#wechat_redirect)

[程序员必看｜让AI编程100%可控！从1到N使用OpenSpec规范驱动开发完整项目实战指南！](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=1&sn=a0277cb0b33e8a357a3855c70c29a5e5&scene=21#wechat_redirect)

[深度体验 Claude Code：一份从入门到精通的实战指南](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=3&sn=9ca7e99937e6f38d6511a4de8f90b2e3&scene=21#wechat_redirect)

[AI Coding 开发范式：OpenSpec，从0到1实践指南](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=4&sn=79ab623381f29ce8440edf32bb530fd3&scene=21#wechat_redirect)

[OpenSpec 实践指南：规范驱动开发的最佳实践](https://mp.weixin.qq.com/s?__biz=MzA4MjI5OTUyNA==&mid=2247484994&idx=5&sn=a46ece51de6eb658d5e30aed2f9d58e9&scene=21#wechat_redirect)

---

如果您正在学习AI Agent，想利用Coze/dify/n8n做一些RPA方面的工作流搭建，欢迎在评论区留言或入群交流！

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rhJKna6Qn0g7RPzAXukAfqVQ1DHLeEXQNwiciagUNw9M8bK3ZLibQJVMBVbp3vNm3eBd9rYC1J9Dznug/640?wx_fmt=png&from=appmsg)   喜欢本篇内容请给我们点个在看  

![图片](https://mmbiz.qpic.cn/mmbiz_png/kzAe1ibcVjhyzsCzlSDxIBhtQGI78X7iaxhcBBWAxtBFbNnu1CDVOJv3RVXON6uZaZiaJiadLauopZOMgQAOreHcqA/640?wx_fmt=png&wxfrom=13&tp=wxpic)欢迎**【关注】**&**【星标】**&**【转发】**