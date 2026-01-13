---
title: "梁文锋署名新论文，DeepSeek V4架构首曝？直击Transformer致命缺陷"
date: 2026-01-13T09:37:20+08:00
lastmod: 2026-01-13T09:37:20+08:00
author: "新智元"
categories: ["未分类"]
---

### 

### 

---

**新智元报道**

编辑：编辑部##### **【新智元导读】深夜，梁文锋署名的DeepSeek新论文又来了。这一次，他们提出全新的Engram模块，解决了Transformer的记忆难题，让模型容量不再靠堆参数！**

  
刚刚 ，DeepSeek新论文发布了，梁文锋署名！

这一次，他们联手北大直接瞄准了「记忆」，是Transformer最致命的关键难题。

如今，MoE成为大模型主流架构，但本质仍是Transformer，因其缺少原生「知识查找」机制，很多检索能力被迫用大量计算去模拟。

33页论文中，团队提出了 MoE 互补的「条件记忆」稀疏轴，并通过一种全新的Engram模块去实现：

将经典哈希N-gram嵌入现代化，提供近似O(1)的确定性知识查找。

  


![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibibpgwe00RcrlBvoOdBntUyVTUexSIYwA0ksXPvAlPMibWRcwwuMZicrPw/640?wx_fmt=jpeg&from=appmsg)论文地址：https://github.com/deepseek-ai/Engram/blob/main/Engram_paper.pdf

通过「稀疏分配」（Sparsity Allocation）建模，他们意外发现MoE与Engram之间，存在「U形scaling law」。

这意味着，需调整两者之间资源比例，让计算与静态记忆间找到最优权衡。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibK9dfOmA9uz7201GWmPQvJUTF2n8mFWn7MOex9atvrxF8VL6C4r3Umw/640?wx_fmt=png&from=appmsg)沿着这个规律，将Engram扩展到27B参数后，并在严格等参数、等FLOPs下优于MoE基线。

**直白讲，MoE只解决「怎么少算」，Engram直接解决「别瞎算」。**

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibVneXvicQkn8IlCW2vH86iclpjYs3J1eubsRMQYVLHwZdPfibgLGdUAtRg/640?wx_fmt=png&from=appmsg)它把该查的交给 O(1)记忆，把注意力从局部琐碎中解救出来，结果不只是更会背知识，同时推理、代码、数学一起变强。

这可能成为稀疏LLM下一条主流路线，更重要的是，下一代V4或将集成这一新方法。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibFcWMdQy7h4wSYMByTbyJ5wlRYHaxQqxSgJh0zDUhp6cZ4eJ3XmGFHg/640?wx_fmt=png&from=appmsg)![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibDtXJMOxCYtcXpVLHWTEE0oram9DHczicFPyMFA6tt7mqoibYAIgomicqw/640?wx_fmt=png&from=appmsg)  
![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**不再苦算，给Transfomer插入「电子脑」**## 

当前，LLM越做越大已成为「铁律」，一条熟悉的路径是——

把参数做大，把计算做「稀疏」。

混合专家模型（MoE）就是典型代表，每个token只需激活少量专家，用「条件计算」让参数规模飙升，FLOPs还能控住。

从Artifical Analysis榜单中可以看出，现有的稀疏大模型，主流都是MoE。

但问题在于，Transformer缺少一种「原生的知识查找」能力，所以很多本该像检索一样 O(1)解决的事，被迫用一堆计算去「模拟检索」，效率很不划算。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibmpTDWXicuJ9xkXHiaW4z9OibPIGWMKLKj3GghgJfibVepa8THGyXAPibVTw/640?wx_fmt=png&from=appmsg)北大和DeepSeek新论文带来一个很有意思的观点：稀疏化不只服务「计算」，也可以服务「记忆」。

由此，团队提出了Engram，把语言建模中大量「固定、局部、刻板」的模式，交给一个可扩展的查表模块去承担。

这样一来，可以让Transformer主干把注意力和深度用在更需要「组合与推理」的地方。

**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**语言建模，两类任务**论文中，作者明确将语言建模拆成两类子任务：

* 一部分任务需「组合与推理」：上下文关系、长程依赖、逻辑推理、链式推理。
* 另一部分任务更像「模式检索」：实体名、固定搭配、常见短语、语法片段、重复出现的局部结构

后者的一个共同点很明显，即它们往往局部、稳定、重复出现。

若是用多层注意力和FFN去「算」他们，模型做得到，但成本极高，还会挤占早期层的表达空间。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibFw7gLECmARuHKfnIickeaB5KdpWHgkibl6FC2ibs9COy5YWr5Zics6D4eQ/640?wx_fmt=png&from=appmsg)为了识别实体「戴安娜，威尔士王妃」（Diana，Princess of Wales），LLM必须消耗多层注意力和FFN来逐步组合特征，这个过程理论上是可以通过一次知识查找操作来完成的。

而Engram想做的事情很直接——

把这类「局部静态模式」转移到一个廉价的知识查找原语。

它用确定性的查表快速给出候选信息，再由上下文决定是否采纳。

  
![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**Engram核心架构：暴力查表+记忆开关**Engram一词源于神经学，本意为「记忆痕迹」，是一种可扩展、可检索的记忆单元。

它可以用于存储LLM在推理过程中，可能已接触过的模式、信息片段。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibsBeyUHRG1H5vuclbpx3oneokpPox05Wmm1AD65yOnB67AtCrxcDsBg/640?wx_fmt=png&from=appmsg)可以将Engram理解为，把经典「哈希N-gram嵌入」现代化，做成插在Transformer中间层的一个「可扩展查表模块」。

如图1所示，Engram是一个条件记忆模块，旨在通过从结构上将静态模式存储与动态计算分离开来，从而增强Transformer骨干网络。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibiceKYrwhuEkyxI1Hc2PRrxQnibyQTDn74BGfp0H0UVx9yJoLqV4MeiaLQ/640?wx_fmt=png&from=appmsg)形式化地说，给定输入序列X=(x_1,...,x_T)和第l层的隐藏状态H^(l)∈R^Txd，该模块分两个功能阶段来处理每个位置t：**检索**和**融合**。

接下来，一起看看Engram的关键设计点。

**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**基于哈希N-gram的稀疏检索**第一阶段主要负责将局部上下文映射到静态的记忆条目中，这通过分词器压缩（tokenizer compression）和确定性哈希检索嵌入来实现。

**分词器压缩**

为了最大化语义密度，作者引入了一个词表投影层。

他们预先计算了一个满射函数P:V→V'，利用归一化的文本等价性（比如NFKC、小写化等手段）将原始Token ID坍缩成规范标识符。

这个过程能让128k大小的分词器有效词表大小减少23%。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibAPYOeB2apdwXTib3RGsibbmJL51Y3eFhDkiaYTq6BPzXLK0xp6wXxJGxw/640?wx_fmt=png&from=appmsg)**多头哈希**

要想直接参数化所有可能的N-grams组合空间，计算上是行不通的。作者采用了一种基于哈希的方法。

为了减少冲突，给每个N-gram阶数n分配了K个不同的哈希头。

每个头k通过一个确定性函数φ_n,k,将压缩后的上下文映射到嵌入表E_n,k中的一个索引：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibSskIDoNRiadzjo57D3APaEb3eJM6dtTUGgD7ApN8cBnicfVc8ibk1IJkQ/640?wx_fmt=png&from=appmsg)**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**上下文感知门控**### 检索到的嵌入e_t充当的是上下文无关的先验信息。不过，它们容易受到哈希冲突或多义词带来的噪声干扰。

为了增强表达力并解决这种歧义，作者采用了一套受注意力机制启发的上下文感知门控机制。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibEP2QJpia1hQOkd6dDl4e1KhNLv7gHQWf14v8mZyYV2ibCGgNloWL0r7A/640?wx_fmt=png&from=appmsg)他们利用当前的隐藏状态h_t作为动态的Query，而检索到的记忆e_t则作为Key和Value投影的来源：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibnBm5LSQxPzY5HAPntwSsVVOvYZErzh3Lly03Asibx1iblx69qKKzRia4Q/640?wx_fmt=png&from=appmsg)其中W_K，W_V是可学习的投影矩阵。

为了保证梯度稳定性，他们在计算标量门α_t∈(0,1)之前，先对Query和Key进行RMSNorm处理：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibhWPLdhomr3BETDG1iczmssxmWuSjYxpAD5xYicvRJibhtX4OBE8ms0mGA/640?wx_fmt=png&from=appmsg)最后，为了扩大感受野并增强模型的非线性，作者还引入了一个短的深度因果卷积：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibpAlGt5OicxwjRZowfj82fXVHwvEnLb8oEOic5XkiabnuqUTnJQdlruMpg/640?wx_fmt=png&from=appmsg)**门控可视化**

为了实证验Engram是否按预期行为，作者在图7中可视化了Engram-27B在各种样本上的门控标量α_t。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibHibrVIf2DPGJYFPDVwTHF4DbgCr0tZ7bOzbh4DTcBzialibibquiaqH4Ulw/640?wx_fmt=png&from=appmsg)结果展示了，明显的选择性模式。门控机制在完成局部、静态模式时一致地激活（显示为红色）。

在英文中，观察到在多Token命名实体（如Alexander the Great、the Milky Way）和固定短语（如By the way，Princess of Wales）上有强烈的激活。

关键是，这种行为有效地跨语言泛化。

在中文demo中，Engram识别并检索独特的习语表达和历史实体，比如「四大发明」和「张仲景」。

这些定性结果证实，Engram成功识别并处理了固定的语言依赖关系，有效地将Transformer骨干网络从记忆这些静态关联中解放出来。

**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**系统效率：计算与存储解耦**扩展记忆增强型模型往往受限于GPU高带宽内存（HBM）的容量。

然而，Engram的确定性检索机制天生就支持将参数存储与计算资源解耦。

与依赖运行时隐藏状态进行动态路由的混合专家模型（MoE）不同，Engram的检索索引仅取决于输入的Token序列。

这种可预测性为训练和推理提供了专门的优化策略，如图2所示。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibOP4ia7CMJhh5ceHXhtKib4xNwrUMOh3gKBGLIUPUffHGXZ0NlbnfYl9g/640?wx_fmt=png&from=appmsg)**训练阶段**，为了容纳大规模嵌入表，他们采用标准的模型并行策略，将表分片存储在可用的GPU上。

**推理阶段**，这种确定性特性使得「预取和重叠」策略成为可能。

  
![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**U型Scaling Law，揭秘最优分配比**Engram作为条件记忆的一种实现形式，在结构上与MoE专家提供的条件计算是互补的。

这里，主要研究了以下两个关键问题：

**1. 有限约束下的分配**

**2. 无限内存场景**

作者通过三个参数指标来分析MoE和Engram之间的权衡：

* P_tot:总可训练参数，不包括词表嵌和LM头。
* P_act：每个Token的激活参数量。这个数值决定了训练成本（FLOPs）。
* P_sparse≜P_tot-P_act：非激活参数，这代表了「免费」的参数预算，可用于在不增加计算成本的情况下扩展模型规模。

作者将分配比例ρ∈[0,1]定义为分配给MoE专家容量的非激活参数预算的比例：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibPjplKXOFHwicBZWmGZpLD9Dj9VMT9rgKou6CUAfB8MnAY7F6icAlwXlg/640?wx_fmt=png&from=appmsg)直观来说：

* ρ=1对应纯MoE模型（所有非激活参数都是参与路由的专家）。
* ρ＜1则减少路由专家的数量，并将释放出来的参数重新分配给Engram嵌入槽位。

**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**结果与分析**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibZEAKs6xroaSjmzCCHyk05gIHxKAll6DJoZIaOrBrj1bTWFY82HWIcg/640?wx_fmt=png&from=appmsg)图3（左）展示了验证损失与分配比例ρ之间存在一致的U型关系。

这种U型关系证实了两个模块之间的结构互补性：

* MoE主导（ρ→100）：模型缺乏用于存储静态模式的专用内存，迫使它只能通过增加深度和计算量来低效地重建这些模式。
* Engram主导（ρ→0%）：模型失去了条件计算能力，从而损害了那些需要动态、上下文依赖推理的任务；在这种场景下，记忆无法替代计算。

接下来，作者探索了一种互补的设置：激进的内存扩展。

图3（右）表明，扩展内存槽位的数量能带来清晰且一致的验证损失改善。

在探索的范围内，曲线遵循严格的幂律，这表明Engram提供了一种可预测的扩展调节手段：更大的内存能持续带来收益，而无需额外的计算量。

关于扩展效率关键的一点是：虽然OverEncoding的直接平均方法也能受益于更大的内存表，但Engram在相同的内存预算下解锁了更大的扩展潜力。

结合分配定律，这些结果验证了——

条件记忆可以作为稀疏容量的一个独特且可扩展的维度，与MoE的条件计算相辅相成。

  


![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**爆杀传统MoE，知识推理数学全面涨**基于Engram架构以及实验得出的分配定律，作者将Engram扩展到了数十亿参数的级别，以此来验证其在现实世界LLM预训练中的有效性。

他们训练了以下四个模型：

· Dense-4B （总参数4.1B）

· MoE-27B （总参数26.7B）

· Engram-27B （总参数26.7B） 

· Engram-40B （总参数39.5B）

  


**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**实验结果**首先，与先前的文献结论一致，稀疏架构表现出了优于密集模型的扩展定律。

在相同的训练计算预算下，所有三个稀疏变体（MoE-27B，Engram-27B/40B）在所有基准测试中都显著击败了等FLOPs的Dense-4B基线。

更重要的是，Engram-27B始终优于等参数且等FLOPs的MoE-27B基线。

有趣的是，这些收益并不仅限于知识密集型任务（MMLU：+3.0，MMLU-Pro：+1.8，CMMLU：+4.0）。

在通用推理领域（BBH：+5.0，ARC-Challenge：+3.7，DROP：+3.3），以及代码和数学推理（HumanEval：+3.0，MBPP：+1.6，GSM8K：+2.2，MATH：+2.4）中，提升更为显著。

这些结果支持了他们的假设：引入一个专用的知识查找原语所带来的表示效率提升，要超过将所有稀疏预算都分配给条件计算的效果。

最后，扩展到Engram-40B进一步降低了预训练损失，并在大多数基准测试中提升了性能。

可以观察到，Engram-40B与基线之间的训练损失差距在训练后期仍在持续扩大，这表明扩大的内存容量在当前的Token预算内尚未完全饱和。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibqNV1UqEoBJqAr3QOQT0ibKuKq5T0tdRLLkGKPLe2CRFqcr7fZA0b2zQ/640?wx_fmt=png&from=appmsg)  
![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**注意力彻底解放，32k上下文性能狂飙**## 

通过将局部依赖建模的任务卸载给静态查找，Engram架构保留了宝贵的注意力容量来管理全局上下文。

通过长上下文扩展训练，作者证明了Engram在长程检索和推理任务上带来了显著的提升。

**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb351381bTy5MO2IN89mV41M88GEiaCCibDxJoaQjYV6HfRtafnmEmfM3R1p0tmkHgBOVuXBD6UJKpsQ/640?wx_fmt=png&from=appmsg)**

**实验结果**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibQwgrmA5cKxTzkBiaibibFeFZbsU65pe05DvxNySGWsibDnVVpKtK2REGrg/640?wx_fmt=png&from=appmsg)**1. 超越注意力机制的长上下文能力**

虽然注意力机制和位置编码提供了处理上下文的结构基础，但结果表明，长上下文性能并非仅由架构先验决定。

轨迹可见，长上下文性能与基座模型的通用建模能力本质上是挂钩的。

因此，严格的架构比较必须通过对齐基座模型的Loss来控制这一干扰变量，而不仅仅是简单地对齐训练步数。

**2. 受控设定下的架构优越性**

在上述原则的指导下，作者将Engram与MoE 基线进行了对比。当控制了基座能力后，Engram模块的效率增益就变得非常明显：

* **等Loss设定（46k vs. 基线）**：当对比预训练Loss对齐的Engram-27B（46k）和完全训练的MoE-27B（50k）时，Engram 展现出了显著的增益。
* **等FLOPs设定（50k vs. 基线）**：在标准的等计算预算下，Engram-27B（50k）进一步拉大了这一差距，确立了全面的最佳性能。
* **极端设定（≈82%计算量）**：即便是提前停止训练的Engram-27B（41k），在面对完全训练的MoE-27B（50k）时依然极具竞争力。这凸显了Engram架构内在的优越性。

## 

## 

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**计算+记忆双轴时代，直接融入V4？**## 

DeepSeek最新论文，打开了稀疏化的第二条路，是一条非常具有启发性的路线：

稀疏化模型进入了「计算+记忆」双轴时代。

* MoE继续负责动态计算与推理
* Engram负责存储与检索静态知识与局部模式

如上的U型scaling law证明了，稀疏预算全部给MoE，不是全局最优，留出一部分给Engram整体更强。

1. 稀疏化目标变得更丰富了

条件计算解决了FLOPs，条件记忆解决了容量与模式检索，两线均可互补。

2. Engram收益带有结构性

它让LLM知识能力暴涨同时，也间接提升了推理、数学、代码的性能，因为Transfomer主干的深度和注意力计算效用更「值钱」了。

3. 确定性查表，很适合系统优化

模型预取和卸载很大，为「更大参数、同等吞吐」提供了一种可行的工程路线。

如今，全网都在猜测，春节档的V4有很大概率会把Engram融入主干架构。

回看此前DeepSeek路线：

DeepSeek V2曾引入MLA，大幅提升了推理效率和KV缓存友好度；

DeepSeek V3持续优化MoE，实现无损负载均衡，训练更稳定，成本更低。

若是V4真的把Engram落地，那将不仅是参数规模的提升，更是架构范式的又一次跃迁。

再加上，此前爆出，V4代码实力可能赶超Claude、ChatGPT系列。

今年的春节大礼，真是让人期待。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibZ4bm3FeZ6CdibPfRhnDG9wYQxXypqvHALFnFSxBCBgR8OmGawXdqGibg/640?wx_fmt=png&from=appmsg)![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibpMT1hLqPhYm8wnxwT8yVlNbxIUGHgahvy2G5DsnfAIE4EjveZ7fvlA/640?wx_fmt=png&from=appmsg)![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibQuvW0gmJe3ZFxEoC9ORoemSThCWLysZan9lFwLhh94sqEWMwaKjzSw/640?wx_fmt=png&from=appmsg)# 

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3uEdSPKrwGNmZEOaaGyzVvZ8dTtE9jU1rFsda3llYbCZpmWfiazUYjWBLTGvlPpXucH8Q0lEUJN3Q/640?wx_fmt=png&from=appmsg)**作者介绍**# 

Xin Cheng

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ib4YEMKmz2l0oBDlXEUfQweicTJic9QzqSQO84AbZxakBNAt2wu5iaVI5bA/640?wx_fmt=png&from=appmsg)Xin Cheng目前在北京大学读博，主攻自然语言处理方向，研究重点是大语言模型和检索增强生成。

作为一名学术新秀，他在圈内已经做出了不少成绩，尤其是在NeurIPS、ACL和EMNLP这些顶会上，发了多篇一作论文。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/UicQ7HgWiaUb3kx5KHMlrHP7uvWown7E5ibRiaElfq9LjiakwMQjDVsOZbD6hKibCvzibHJib85EL0I7PD5a2qge3kMSibg/640?wx_fmt=png&from=appmsg)参考资料：HYZhttps://github.com/deepseek-ai/Engram/blob/main/Engram_paper.pdfhttps://x.com/karminski3/status/2010858438814023740https://x.com/LearnWithScribe/status/2010783721410981930?s=20  
**秒追ASI****⭐点赞、转发、在看一键三连⭐****点亮星标，锁定新智元极速推送！**![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/UicQ7HgWiaUb1y6B5OM79TFzpkceWtUkI6LEwv0uYicSoM5Q3I3kDNJhxWdL3tQvbOpU3Ty7icBqnDDNd4CCu4ibiaHw/640?wx_fmt=jpeg&from=appmsg)

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/UicQ7HgWiaUb14tKKLE6pVq7YVSJibxNhYCmEg58Ql8HbceG3TGfsewb8Xv49w3kzttrWd4WJiboVLRribHLK1PEZAA/640?wx_fmt=jpeg&from=appmsg)

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/UicQ7HgWiaUb3Spv8cZIZ7WYgABwLa0sqtkZ7jV1lzPtlWl7VHXia5cBBwXUVfsicjhtsIPWib5qds3GpH9wjKOYMwg/640?wx_fmt=jpeg&from=appmsg)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/ZdZzksl3iJyUHn9W-6nv5Q)*
