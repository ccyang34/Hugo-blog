---
title: "“Claude Cowork 杀死了我的创业公司”"
date: 2026-01-15T21:08:31+08:00
lastmod: 2026-01-15T21:08:31+08:00
author: "十字路口Crossing"
categories: ["未分类"]
---

**作者**: 十字路口Crossing

> AI 不再仅仅是操作和交互的对象，它开始成为 Coworker。

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOOXz1rTnlfCtSJHcYqV9VdQpnPeiaJBdCHHicboFvWp3WVIibiazBWibH5TA/640?wx_fmt=other&from=appmsg)👦🏻 作者: 镜山

🧑‍🎨 排版: NCon

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOZibDerVSzNaJ3EBJ8bAJpdiaKVtC7Qj9TbGG8nSFbX0ANnibDXpib001Lw/640?wx_fmt=other&from=appmsg)在 AI 领域，其实有一种大家都心照不宣的恐惧，叫 「被 Sherlocked」。

  


这个词最早来自苹果开发者社区：你辛辛苦苦做出一个体验不错的第三方工具，结果下一次系统更新，苹果直接把同样的功能做到系统里，还免费。

  


然后，你的产品就在商业层面被直接 Over 掉了。

  


就在昨天，类似的「体验」，落在了一个叫 Eigent 的 Multi Agent 平台创业团队身上。

  


起因是 Anthropic 发布了 Claude Cowork。这是一个非常明确的信号：AI 助手开始越过「对话框」，尝试成为真正的数字同事。

  


它可以直接读取本地文件、理解你的工作环境，甚至顺手帮你整理下载文件夹。

  


站在用户视角，这回的生产力提升很大；但站在另一边，对于那些正在做「AI 自动化 Agent」的初创团队，很难不感到压力。

  


于是，一家做同样场景的、叫做 Eigent 的团队 CEO 李国豪 (Guohao Li) 在 X 上发了一条略带自嘲的推文火了：


> Claude Cowork 刚刚「杀死」了我们的创业项目，所以我们做了一件最理性的事：把它开源了。

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOLr975gwJWWBvibqc0baicw3bKAMRWNhkf0onSLgXtAAwZd7J10f1n3Tw/640?wx_fmt=other&from=appmsg)  


1 天时间，这条 X 推文超过 6000 次点赞、近 100 万次浏览。

  


这也勾起了我们的好奇：这是一个什么项目？

### 🚥

接下来，分享我们对这个项目的全面拆解。

## 为什么 Claude Cowork 和 Eigent 会出现？

要理解为什么 Eigent 的开源会引起这么大的关注，前提是先搞清楚：


> Anthropic 通过 Claude Cowork，到底重新定义了什么。

  


首先就是，Claude Cowork 被认为是一个面向非开发者、覆盖大量日常工作场景的「Claude Code」。把这种「写代码」的能力扩展到了，范围更大的执行场景里。

  


它有这么几个特点：

  


【1】需要本地持续运行一段时间（重点是连续运行）的任务场景。

【2】不用再去打开终端，不用去面对代码，直接在 Cowork 里就能执行任务。

【3】能够直接访问用户的本地指定文件夹，Claude可以在该文件夹中读取、编辑或创建文件。

【4】Browser Use：Cowork 集成了外部工具，如Chrome，增强了Claude的功能。

【5】用户可以将多个任务排队，Claude 可以同时处理这些任务，无需等一个任务完成后再开始下一个任务。

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOW2LibwbSm1Bt9adib5u5JvW4UBupsIyZdibZfZqsY1l7oCPbDJCTvBSpA/640?wx_fmt=other&from=appmsg)  


我们找到了几个 Eigent 的案例，一起来看看。

  


首先，Eigent 接收到你的任务，就会自动将其拆解，并把各个子任务分配给合适的 Agent。然后，这些 Agent 将像团队成员一样，在桌面环境中协作完成任务。

  


比如下面这个任务：


```
  
  
  
让它去调研 Claude 的功能 “Cowork”，并撰写一份比较报告，对比 Claude Cowork 与 Eigent 的多 Agent 工作流。
```


[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbO6YCeIvYvMhwq6ucNALSzVl6sicy1wAnvIZDl95PpLN1qJfZ9pWqLfVg/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/KPYp0hKNAspQ5OC8bsMlZw)

  


再比如，Eigent 执行 Claude Cowork 很吸引大家关注的「清理桌面」任务：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOQT27GsoYAlEwWDvSFibVG2MOX1ht3QKY5V66xZYSz1iaXHdvaTcxHSIQ/640?wx_fmt=other&from=appmsg)  


你会发现，它可以用一些比较模糊的提示词，一步步把整个桌面整理好，特别是那种很复杂很凌乱的桌面，上面已经放满了各种文件，最后都会被分类放到几个特别的文件夹里：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOjyt3oFA3mDYx65y9PdgFuPy92DkVkz7TMdichOBr2GUA0UVyiaM8O6qA/640?wx_fmt=other&from=appmsg)  


我找了做这个任务的一段视频，放在了下面。

  




[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOvf7JTTEFCVXszicLPvz59WlFKDrLSHHSQvd8P8lLbVSahYJlYFiaehibQ/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/KPYp0hKNAspQ5OC8bsMlZw)

  


我们再来看看细节，在最终任务结束的做侧边栏里，Eigent 总共整理了 55 个文件以及一些其他图片、音频等等，整个流程还是蛮顺的：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbO9MEiattu5LicWdY6ia0EeRznHULCPp4tIvHHyicdmOGwBMjU2Af8E3Gg5w/640?wx_fmt=other&from=appmsg)  


所以，这种 「Multi Agent 并行工作模式 + 本地权限 + Browser Use」 的能力，让很多日常工作场景达到了闭环。

  


比如，你可以让它访问本地文件夹，把下载目录按类型整理清楚；你也可以把几百张收据截图丢给它，让它自己生成一张结构化的 Excel 支出表。

  


如果把视角稍微拉远一点，其实会发现一个容易被忽略的事实：Eigent 和 Claude Cowork，做的并不是两件不同的事。

  


它们的目标几乎一致：让 AI 变成可以直接介入工作流的执行者。

## Eigent 到底是什么？

首先，Eigent 是 GitHub 上的一个开源项目。

  


简单说，它是一个开源的桌面应用。它做的事情就是用多 Agent 框架，然后把那些原本又长又杂、要来回切好几个工具的工作流程，变成可以自动跑起来的任务。

  


GitHub 项目链接如下，有非常完整的部署 Guide Book：

**https://github.com/eigent-ai/eigent?tab=readme-ov-file**

  
除此之外，Eigent 也是非常早的发布 Multi Agent 框架的开发团队（与 CAMEL 其实是同一个团队），在23年初就已经开始在探索 Agent 的 Scaling laws 了，此前还开源了其他几个项目，大概一共 36k+ 星，具体的 GitHub Stars 可以参考以下几个链接：

**https://github.com/camel-ai/camel**

**https://github.com/camel-ai/owl**

**https://github.com/camel-ai/oasis**

  


目前，Eigent 这个项目已经获得了 4.1k Star：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbO3iaBTsicHV66wlv4FfXofjVHS6Gdq3xj5LeFXJAxUtoGRvP4ssK7R4qQ/640?wx_fmt=other&from=appmsg)  


可以说，前面那些「被巨头杀死」的叙事，让 Eigent 进入了更多人的视野。但让它没有迅速退场的原因，仍然来自技术层面。

  


我们仔细拆解了下这个项目，发现 Eigent 的团队把注意力投向了：分布式系统。

  


这也解释了为什么 Eigent 的核心架构被称为 Workforce（劳动力），在这个架构下，AI 被当作一组可以拆分、调度和协作的执行节点来组织。每个节点都有明确的角色和任务，协同合作以完成复杂的工作流程。

  


我找到了 Eigent 团队发出来的一张架构图：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOYZ4PWWeJXKo32Y7RpnmhTzyK3hYHqYBm8HaYzgibuJyjDcDt2QWtpIg/640?wx_fmt=other&from=appmsg)  


Eigent 和 CAMEL AI 其实是同一个团队，Eigent 的 Multi Agent 架构，其实是基于背后 C AMEL 之前做的 Agent 框架。整个 CAMEL Workforce System 里的这些任务需要多个人或者多个系统来合作完成。

  


整个系统会自动分配任务、管理进度，确保每个步骤都能顺利完成。  


  


在 Eigent 的架构中，任务执行被拆分成了不同层级：

  


【1】Task Manager

  


负责理解用户的整体目标，然后把模糊的需求拆解成具体、可执行的小任务，并给出一个整体的推进计划。

  


【2】Coordinator

  


主要负责调度和组织工作，分配任务，处理任务间的依赖关系，然后在所有任务完成后把结果汇总起来。

  


【3】Worker Nodes

  


这一层专注于具体操作，比如查信息、写代码、处理数据或文档。多个工作节点可以同时工作，彼此不干扰。

  


这种拆解方式其实是借鉴了分布式系统，把复杂的任务分成几个小问题，再通过并行执行来加速整个过程。

  


从实际效果来看，最大的变化就是效率的提升。

  


传统的单 Agent 通常是线性推进任务：先搜索、再阅读、整理，最后输出，每一步都依赖上一阶段。

  


而 Eigent 这类 Multi Agent 工具，则更像是并行调度：当一个节点在检索资料时，另一个节点已经开始搭建报告框架，第三个节点甚至能提前生成草稿或代码框架。

  


尤其是在一些长链路的复杂任务中，并行执行的效率提升会更明显些。虽然这个提升会根据场景有所不同，但核心还是很明确的：任务效率很大程度上取决于系统的组织方式，而不仅仅是模型的能力。

  


在 Google 的开发者社区里，Eigent 也被认为是利用 Gemini 3 的比较适配的多 Agent 平台。

  


去年 2025 年 12 月里，  Google for Developers 发布过一个《Real-World Agent Examples with Gemini 3》，在这里面，Eigent 被选为了 6 个官方示例之一。

  


在 Google 的介绍里，Eigent 被定义为一个 local-first 的 Multi Agent 平台，着重强调了其在企业级浏览器自动化（比如 Salesforce 流程）里的实际场景应用。

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOYYoIKyPEYVtMyJ2DM8TOdJlKBLLYysVd94Vls9cZAkpr7LcS3F9o9g/640?wx_fmt=other&from=appmsg)  


与之相似的背书，其实还有很多，比如，HuggingFace 的 Co-founder 曾为这个项目点赞：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOibEmzzqLicuiajWnCnGS0ialnZDSa3z8bTKQxVpPKmv1avicrr3jldvk3QA/640?wx_fmt=other&from=appmsg)  


巧的是 4 天前，Eigent 团队曾发过一个叫做 SETA 的项目，是一个非常大的开源终端 Agent 训练 RL 环境，也被 Andrej Karpathy，John Schulman 等人点赞：

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOoDleQsWaEmSxzL1egrv3zrU1ticZGPQKxjmic3vt5gNFse2romw11icVA/640?wx_fmt=other&from=appmsg)  


在执行层面，Eigent 不仅停留在概念上。

  


它通过 MCP 集成了大量实际工具，支持网页操作、代码执行和常用办公平台的应用。

  


不过，Multi Agent 系统也都会遇到一个问题：协调成本。

  


为了解决这个问题，Eigent 同样引入了自我反思和重规划机制，能在任务被卡住时自动调整方向。同时，在关键节点，系统也设置了 Human-in-the-Loop 接口，让人类可以干预决策，避免失控。

  


在技术架构之外，Eigent 的另一个关键选择，是 Local-First（本地优先）。

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOn67rvrAibl0P7U0ng76oiaGHwBFPrIfngJl4Mlu2ov7Y5g3uBv2JlGng/640?wx_fmt=other&from=appmsg)  


用户也可以用自己的 API Key，来选择不同的模型接入到 Eigent 里，不只局限在某个单一模型。

  




[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOmy8DQkRt9alkpF9VM0nVov85vDUfadaDzWviaZPHMyRgwibLwMB1AnMg/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/KPYp0hKNAspQ5OC8bsMlZw)

  


很多传统 Agent 产品都运行在云端环境中。这种模式在个人使用场景下确实很便利，但在一些比较敏感的场景下，就会有点尴尬。

  


Eigent 的应对方式相对简单直接：它允许系统在用户的本地或私有环境中运行，并提供可替换的模型能力。

  


用户可以选择继续使用 SGLang、云端模型，或者切换到本地部署的开源模型，比如通过 Ollama 或 vLLM 运行 DeepSeek 等模型。

  


在这种配置下，系统甚至可以在离线状态下完成任务。

  


所以，这一整套技术架构和流程顺下来，就会很好地支撑起 Eigent 的功能。

  


最后，再来说说 Eigent 的开源，这回他们用的是 Apache 2.0 协议，这基本上意味着团队实际上放弃了对代码使用方式的大部分限制。

  


代码可以被修改、商用，甚至重新封装发布。

  


下面，我们总结下。

  


如果我们把 Claude Cowork 和 Eigent 放在一起对比观察，会发现一个非常有意思的共识。

  


尽管它们的背景完全不同，但它们都在试图解决同一个核心问题：单体 AI Agent 的困境。

  


我们可以把这个问题想象成，你招来了一个非常聪明的实习生，但如果你让他去做一项复杂任务，那么他大概率会遇到瓶颈，甚至交出一份不完整的答案。

  


因为这个任务太复杂，每个步骤之间相互依赖。Eigent 和 Claude Cowork 的出现，则展现了在这类场景下，多 Agent 能力所带来的体验。

### 🚥

所以，把视线从「被巨头碾压」的戏剧性叙事中移开，通过 Claude Cowork 和 Eigent 这类产品，我们或许能看到一个共识：


> 在过去的几年里，我们正在目睹 AI 从「单纯工具」到「智能助手」的转变，但这一切的变化，也只是 AI 成为「真实劳动力」的开始。

  


AI 不再仅仅是操作和交互的对象，它开始成为 Coworker。

  


如果你也想去试试这个开源项目到底能做到什么程度，不妨去 GitHub 上给它点个 Star，下载下来跑跑看。

  


GitHub 链接：**https://github.com/eigent-ai/eigent**

**官网链接：****https://www.eigent.ai/******

  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOK3rdZmooCG81pM15RCSbCjp5swH0AtYzRT90I92H5ZBz9jovVhtGsg/640?wx_fmt=other&from=appmsg)  


  


![loading](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/FFcNSoQ3Kicu9N5g3FSR7LopEGdtibBHbOyhK1QqSclYf3ZneZ33KGkTLjmEicGqe8otZpia6N2KC7DTdGPwrGjnvA/640?wx_fmt=other&from=appmsg)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/KPYp0hKNAspQ5OC8bsMlZw)*
