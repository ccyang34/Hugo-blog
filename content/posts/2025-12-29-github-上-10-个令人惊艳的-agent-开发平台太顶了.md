---
title: "GitHub 上 10 个令人惊艳的 Agent 开发平台，太顶了。"
date: 2025-12-29T16:46:47+08:00
lastmod: 2025-12-29T16:46:47+08:00
categories: ["人工智能"]
tags: ["AI Agent", "开源项目", "大模型", "自主智能体", "多智能体协作", "LLM", "LangChain", "AutoGPT"]
---

## 01 AutoGPT

AutoGPT 是 AI Agent 领域的鼻祖级项目，现在已经 18 万+的 Star 了。

与聊天机器人不一样，AutoGPT 能够自主地将一个大目标拆解为子任务，并利用互联网搜索、本地文件等操作来一步步实现目标。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknTOt4PB8OAjWydI4b882X41re0mJIL2ug5pIW3hhpGsiappgiaRCy6ia3A/640?wx_fmt=png&from=appmsg)

AutoGPT 具备强大的工具调用和环境交互能力。

它能够通过访问互联网搜索最新信息、管理本地文件的读写、执行代码以及保留长期和短期记忆来辅助决策。

核心机制是一个思考-计划-行动的循环：模型会评估当前状态，制定下一步计划，执行操作，并根据反馈结果进行自我修正，这使得它能够处理比单一对话更复杂、耗时更长的自动化工作流。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknSJ40icf8Tltja31gmJym93YKETPRibIOcMYWnXjxMwysW6seVhacyARA/640?wx_fmt=png&from=appmsg)

AutoGPT 这个开源项目绝对是推动 AI Agent 领域的快速发展，是研究自主智能体（Autonomous Agents）的必看项目。

* 开源地址: https://github.com/Significant-Gravitas/AutoGPT

## 02 Dify

Dify 目前 12 万+ 的 Star 了。

它不仅仅是 Agent 框架，还是融合了 Backend-as-a-Service (BaaS) 和 LLMOps 理念的大模型应用开发平台。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknalaxJseAJOcOUDZbuLKSrO8JCZE9wXQ9G616tiaicnZfndE31AUq0Q7A/640?wx_fmt=png&from=appmsg)

它提供了可视化的 Prompt 编排、运营管理、知识库 RAG 集成等功能。

通过 Dify，不需要从头编写后端代码，即可快速将简单的 Prompt 转化为功能完备、可投入生产的 AI 应用。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahknrpx6rML2Ja3KNuIRD7g0e3XLGiaoS86aR65iahZuvmSVkFjeemn1gEGA/640?wx_fmt=gif&from=appmsg)

Dify 支持可视化编排，拖拽节点来定义复杂的 Agent 逻辑和工具调用。并且内置了高质量的 RAG 引擎，能够自动处理文档解析、分段和向量化，轻松构建企业级知识库。

它提供了可视化的 Prompt 编排、运营管理、知识库 RAG 集成等功能。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknFMXU4ST1RxaUdAMibyBM9lzbmzDsPLxEQMeHBY1ibEscj6BDa8ib0xbBw/640?wx_fmt=gif&from=appmsg)

关于它和 Dify、n8n、Coze 的区别，让 Nano Banana Pro 画了一个图：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhkncxFYmmRUsWwbf3xRoM2vDpUQIxwcx7sUz7icedttrGP3a4JYrs07czA/640?wx_fmt=png&from=appmsg)

* 开源地址: https://github.com/langgenius/dify

## 03 LangChain

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahknicm82vlorNEh8CeTPtd7dAIhyicS5IwS3Kd1Hr9o04rTUiabR5EsXAw2g/640?wx_fmt=png&from=appmsg)

虽然 LangChain 是一个通用的 LLM 开发框架，但它目前是构建 Agent 的事实标准基础设施之一。

对于初学者来说，它的学习曲线还是很陡峭的，一旦掌握了会发现它确实是构建复杂逻辑最稳健的地基。

它有很多高度模块化的组件，包括链 Chains、代理 Agents 和记忆 Memory。

开发者可以像搭积木一样，将提示词管理、文档加载、向量检索以及模型调用串联成一个完整的工作流。

特别是其强大的 Agent 机制，大模型充当推理引擎，动态决定调用哪些外部工具，比如 Google 搜索、计算器或 API 啥的来解决问题。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahkn0GicLNVWiaz9DhbcB12PpFPSwz5IB7FsN7dYgpl277tnlRRWI9ibUDHVA/640?wx_fmt=png&from=appmsg)

特别是其子项目 LangGraph，专门用于构建有状态的、多角色的 Agent 应用。

它提供了高度可控的循环计算能力，让开发者能够精细地控制 Agent 的决策流程，是 Python 开发者构建复杂 Agent 的首选底层框架。

* 开源地址：https://github.com/langchain-ai/langchain

## 04 MetaGPT

MetaGPT 现在在 GitHub 上有 6 万多 Star 了。

如果想研究多智能体协作，这个开源项目可以说是最重要的框架之一。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknVFgzvu0590eRKcJjb3o3SHj1EOkkD6aOJrmh5uL3BGu3zBGwicnV02A/640?wx_fmt=png&from=appmsg)

它模拟了一个虚拟的软件公司，内部包含产品经理、架构师、项目经理和工程师等不同角色的 Agent。

只要输入一句话需求，这些 Agent 就会协同工作，输出用户故事、竞品分析、设计图甚至可运行的代码。

适合对多智能体协作（Multi-Agent Collaboration）感兴趣的开发者，特别适合那种流程固定、对输出稳定性要求高的场景。

* 开源地址: https://github.com/geekan/MetaGPT

## 05 Microsoft AutoGen

微软开源的框架，之前也介绍过，现在已经 的 Star 了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahkn3C972JHjNUH31bn5DlMibSEKb4iaknxqicDyibxFQejucT5kDWqvqqnNCw/640?wx_fmt=png&from=appmsg)

它专注于多智能体对话。可以定义多个可以相互对话的 Agent，可以是 LLM、人类或工具，它们通过对话来协作解决任务。

该框架高度抽象和灵活，支持多种对话模式，是目前工业界和学术界探索多智能体系统（Multi-Agent Systems）最主流的框架之一。

* 开源地址: https://github.com/microsoft/autogen

## 06 Flowise

Flowise 是一个低代码/无代码的 UI 可视化工具，现在 48k 的 Star 了。

如果你被 LangChain 晦涩的文档劝退了，不妨先试试 Flowise。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahknia3h2Rdl6qP5b2LvA82GLtwWzq6ZeBsSGETmKqmZN7eQ2HgGp0wvNJw/640?wx_fmt=gif&from=appmsg)

通过拖拽的方式构建大模型应用，它底层基于 LangChain，用户可以通过连接不同的节点，比如 PDF 加载器、OpenAI 模型、Agent执行器等来构建自定义的逻辑流。

对于不擅长写代码但想快速搭建 Agent 原型的用户来说，这是一个非常友好的平台。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknCicJRkjJOMkK0Mau8CK5nJ39icNZytdib4K93oGJTU64G6738GA0aJaSA/640?wx_fmt=jpeg&from=appmsg)

* 开源地址: https://github.com/FlowiseAI/Flowise

## 07 CrewAI

CrewAI 是近年来异军突起的 Python 框架，它主打角色扮演（Role-Playing）的编排， 现在已经 42k 的 Star 了。

这个开源项目不像 AutoGen 那么抽象，写 CrewAI 的代码感觉就像是在给员工写任务书，非常清晰易懂，是 Python 开发者上手多智能体的首选。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahkn23tCIUNcC9a6qPyFrP6t8D18fMEejU51CJtH3zPYY8THVsBlL4l4NQ/640?wx_fmt=png&from=appmsg)

它让开发者可以轻松定义具有特定角色、目标和背景故事的 Agent，并将它们组成一个团队来按顺序或层级执行任务。

它的设计非常直观，不仅易于上手，而且能很好地与 LangChain 工具生态集成。

* 开源地址: https://github.com/crewAIInc/crewAI

## 08 ChatDev

这个 28K 星星的开源项目是清华大学团队 OpenBMB 开源。

类似于 MetaGPT，ChatDev 也是打造了一个虚拟的软件开发公司。

它通过聊天链的方式，让不同角色的智能体（CEO、CTO、程序员、测试员）在如设计、编码、测试、文档等环节进行深度协作。

其特点是过程可视化强，像是在玩一个模拟经营游戏一样看着软件被开发出来。

看着一个个小人儿协作写代码确实很治愈，它为我们展示了未来软件开发的终极形态，非常有启发性。

* 开源地址: https://github.com/OpenBMB/ChatDev

## 09 SuperAGI

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7Ahkn0tXJNOBZcqX8DtRqytLchYg6lJ4CTgpHfnuRggYS0ZIB6nuHj8Eic1A/640?wx_fmt=png&from=appmsg)

这个自主 AI 智能体框架现在已经 15K 的 Star 了。对于需要长期稳定运行、监控多个 Agent 的企业级场景来说，这个开源项目基建非常必要。

它有一套完整的基础设施，开发者用它可以构建、管理和运行自主 Agent。

它拥有图形化界面、Agent 市场、Tools、并发代理运行等功能，旨在解决 AutoGPT 在生产环境中使用难的问题，是一个功能比较完备的 Agent 管理平台。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknMHnE9fLkTPO0DfkCAmzyiakGSCJIdiach2n3nGMojRNZHXHFiblDvs5icA/640?wx_fmt=png&from=appmsg)

而且还能通过可视化的仪表盘同时运行和监控多个 Agent，查看其思维链（Chain of Thought）和执行日志。

开发者可以将自己开发的自定义工具包、智能体模板发布到市场中供社区复用。

* 开源地址: https://github.com/TransformerOptimus/SuperAGI

## 10 Letta

大模型最让人头疼的就是聊着聊着就忘了，Letta 恰好切中了这个痛点。

如果你想开发一个能陪伴用户几个月、甚至几年的伴侣型应用，一定要看看这个可以构建有状态（Stateful）AI 智能体的开源框架。

它也是著名的 MemGPT 项目的继任者和正式化版本。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknuEBficB3owD1gxdnjAicXEEf19ZXicLwkZLicYm510ksX9lRnUultn8yKw/640?wx_fmt=png&from=appmsg)

Letta 通过引入类似操作系统的内存管理机制，让 AI 智能体能够拥有持久化的长期记忆，并在不同的会话和时间跨度中保持一致的身份和知识。

Letta 延续并强化了大模型即操作系统的理念。

它通过一种分层内存结构，将信息在当前上下文窗口和外部数据库之间动态调度。

智能体具备自我编辑记忆的能力，能够自主决定何时将关键信息写入长期存储或从历史记录中检索数据，从而在不增加 Token 消耗的前提下，实现了理论上无限的上下文窗口。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRruxic8L4xgA3agWibTlcb7AhknL839Vyz2XtvcnOicMK8Gpg1V6nZKOUXNp4zheFGTkQsfYaHkvfhnyVA/640?wx_fmt=png&from=appmsg)

* 开源地址：https://github.com/letta-ai/letta

## 11 点击下方卡片，关注逛逛 GitHub

这个公众号历史发布过很多有趣的开源项目，如果你懒得翻文章一个个找，你直接关注微信公众号：逛逛 GitHub ，后台对话聊天就行了：

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/ePw3ZeGRrux2sRxwJzmfe1lK8ic33XvtVPsIPCMV7hjicmScibtxIZ1NsjXxNoVNMb3zLy32Al7PSpfbVAtrACYqQ/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&tp=webp#imgIndex=11)