---
title: "他来了，deepseek v4pro，国产之光，腾讯救星"
date: 2026-04-24T11:42:38+08:00
lastmod: 2026-04-24T11:42:38+08:00
author: "AIGCHUB"
categories: ["AI与技术"]
tags: ["DeepSeek V4", "MoE", "长上下文", "AI Agent", "推理模型", "大模型", "技术路径", "上下文扩展"]
---

**作者**: AIGCHUB
---
## 描述

最近 DeepSeek 发布了 V4 预览版，从技术路径上看，这一代的重点已经非常明确：不是单纯做更大的模型，而是把「超长上下文」做成一个可用、可规模化的能力。

先看模型本身： V4 系列包含两个 MoE 模型——V4-Pro（1.6T 参数，49B 激活）和 V4-Flash（284B 参数，13B 激活），都支持 100万 token 上下文。这个量级已经不只是长文本理解，而是开始覆盖 multi-doc、agent 轨迹甚至复杂任务历史。

关键不在“能不能做”，而在“成本能不能接受”。

这一点上，V4 的优化比较有意思：
* Hybrid Attention（CSA + HCA）：用压缩+稀疏的方式处理长序列，本质是在 attention 结构上做“信息筛选”
* mHC（Manifold-Constrained Hyper-Connections）：对残差连接做约束，提高稳定性
* Muon Optimizer：优化收敛速度（这一点对大规模训练很关键）

从结果上看比较直观： 在百万 token 设置下，V4-Pro 的单 token FLOPs 只有 V3.2 的约 27%，KV cache 只有 **10%**。这意味着长上下文不再是“理论能力”，而是开始具备工程可行性。

性能方面，V4-Pro-Max 在多个 benchmark 上已经接近甚至超过现有顶级模型（包括代码、推理、agent任务）。尤其是 SWE、Tool 等 agent 相关指标，提升比较明显。

一个值得关注的趋势是： 长上下文 + 高效率 → 推动 test-time scaling 和 agent 体系真正落地

当上下文可以承载更长轨迹，模型才有可能做更复杂的规划、反思和多轮决策，这一点对 agentic AI 非常关键。

整体来看，DeepSeek-V4 这一步，不只是“更强模型”，而是在回答一个更现实的问题： 大模型在长上下文场景下，是否可以成为基础设施级能力。

#大模型话题# #DeepSeek话题# #LLM话题# #长上下文话题# #MoE话题# #Agent话题# #AI工程话题# #推理模型话题#

## 图片 (4张)

![图片1](https://i0.wp.com/sns-webpic-qc.xhscdn.com/202604241142/bdc7393088647ba52ac815c13070d5a6/1040g2sg31vb1nls53q705o71njf08o43cqtgm08!nd_dft_wgth_jpg_3)

![图片2](https://i0.wp.com/sns-webpic-qc.xhscdn.com/202604241142/16ec808d31203a07d1b210566e04119e/1040g2sg31vb1nls53q7g5o71njf08o4395hv9m8!nd_dft_wgth_jpg_3)

![图片3](https://i0.wp.com/sns-webpic-qc.xhscdn.com/202604241142/f22817792a301f47e518b975140f54c7/1040g2sg31vb1nls53q805o71njf08o43chtf61o!nd_dft_wlteh_jpg_3)

![图片4](https://i0.wp.com/sns-webpic-qc.xhscdn.com/202604241142/c9586a70a144374b0c62647abfcab263/1040g2sg31vb1nls53q8g5o71njf08o43hh4voc0!nd_dft_wgth_jpg_3)

*来源: [小红书](https://www.xiaohongshu.com/discovery/item/69eadd76000000001e00ec6f)*