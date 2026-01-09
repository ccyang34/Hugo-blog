---
title: "CC直接用，Manus核心Context技术被人做成了Skills"
date: 2026-01-09T10:44:06+08:00
lastmod: 2026-01-09T10:44:06+08:00
categories: ["未分类"]
---

planning-with-files是开源社区最近疯传的一个Skill，发布仅四天收获3.3k star。目前还在持续增长。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUX0oeYbb596zHiaN8GW1F43BEMfzDqxBBJMW3nkUTibOUW4GPWcbJmpFQ/640?wx_fmt=png&from=appmsg)爆火的原因很简单，因为这个项目的核心极具吸引力：它通过一个标准的Claude Skill，复刻了Meta斥资20亿美元收购的**Manus**公司的核心技术——**上下文工程（Context Engineering）**。

本文将带你深入代码层，看这个项目的Skill是如何用**仅用几百行指令和三个Markdown文件，就在你的本地终端里模拟了价值20亿美元的Agent核心工作流。**

**项目地址：https://github.com/OthmanAdi/planning-with-files**

## Manus的六大上下文工程原则

Manus之所以能从众多Agent创业公司中突围，并非因为它拥有更强的模型，而是它重新定义了模型与上下文交互的方式。在 `planning-with-files` 项目的 `reference.md` 中，详细记录了这六大原则：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUfico6kUia0j04dvsDZgBKVXorPwlDtWzibLdVB67xAJYmavnDYrxrc5wA/640?wx_fmt=png&from=appmsg)1. **文件系统作为外部记忆 (Filesystem as External Memory)**
* **原理**：不要依赖易失的Context Window。将磁盘视为无限的“外挂内存”，只在Context中保留文件路径。

3. **通过重复进行注意力操纵 (Attention Manipulation Through Repetition)**
* **原理**：对抗“Lost in the Middle”。在关键决策前反复读取计划文件，强行刷新模型的“注意力权重”。

5. **保留失败痕迹 (Keep Failure Traces)**
* **原理**：错误是宝贵的资产。显式记录失败尝试，让模型通过“反思”避免死循环，而不是掩盖错误。

7. **避免少样本过拟合 (Avoid Few-Shot Overfitting)**
* **原理**：在重复性任务中引入受控变体，防止模型陷入机械式的幻觉。

9. **稳定前缀优化缓存 (Stable Prefixes for Cache Optimization)**
* **原理**：通过固定的文件结构和前置指令，最大化KV-Cache命中率，降低Token成本。

11. **只增不改的上下文 (Append-Only Context)**
* **原理**：尽量以追加（Append）而非修改（Modify）的方式更新信息，维护上下文的连贯性。

## 架构落地：三文件模式

planning-with-files Skill将上述抽象原则具象化为一套严格的 **“三文件工作流”**。

当这个Skill被触发时（例如你要求“帮我策划并开发一个贪吃蛇游戏”），它会强制Claude在当前目录维护三个文件：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUoDLROQjajyYdhUfRicbibQN4cvuicrOaBaSiaPibTKp6Ts9QePC1viaoBWAQ/640?wx_fmt=png&from=appmsg)### 1. `task_plan.md`（指挥塔 寄存器）

这是整个架构的核心。它不存储具体知识，只存储**元数据**。

* **作用**：定义目标、拆解阶段、追踪进度、记录错误。
* **关键机制**：它是Agent的“罗盘”。无论任务进行到第几步，Agent**必须**在每次行动前读取此文件。

### 2. `notes.md`（知识库 堆内存）

* **作用**：存储调研笔记、网页摘要、中间代码。
* **关键机制**：**“Store, Don't Stuff”**。当Agent搜索到大量资料时，禁止直接输出到对话框，必须写入此文件。这保持了对话上下文的清爽。

### 3. `[deliverable].md`（产出物 IO缓冲区）

* **作用**：最终的交付结果（如 `game.py` 或 `report.md`）。
* **关键机制**：将“思考过程”与“最终结果”物理隔离。

## 三文件如何工作？

对于Claude Code用户来说，安装这个Skill后，最直观的变化是你的工作目录下会多出三个文件。但这不仅仅是文件，它们构成了一个**基于文件的状态机（File-Based State Machine）**。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUYOo4BCVSWczXa1szbPfico348PfxzD64cMdn3Cu2XjQ4qV1BvKXLavg/640?wx_fmt=png&from=appmsg)让我们透视一下当你输入“帮我策划并开发一个贪吃蛇游戏”时，这套协议是如何接管Claude的行为的：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUBFJsUXb0Ef2389ibWibfYsj4JSNYibOvxMp6Kzy8Wdx8CagjUbxLNNBNw/640?wx_fmt=png&from=appmsg)### 阶段0：协议握手与状态机初始化

Claude Code识别到复杂任务，Skill激活。它首先创建 **`task_plan.md`**。 这不是普通的文档，它是Agent的**程序计数器（Program Counter）**。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFU8yx4zecwDibkA7bBDNjQT7jh0Hmezfrxw9KDkCicIYiaSdIB2VYvnCicYg/640?wx_fmt=png&from=appmsg)* 它定义了 `Goal`（全局指令）。
* 它将任务拆解为 `Phases`（指令流水线）。
* 它标记了 `Status`（当前指针位置）。

**此时，无状态（Stateless）的LLM第一次拥有了“状态”。**

### 阶段1：Read-Before-Decide（对抗遗忘）

在开始写任何代码之前，Skill强制Claude执行 `read_file task_plan.md`。 这一步至关重要。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFU61XetH7p1IcD8icAOdKJRwmKsLpOmzCmnibdxKEyerA5syHINibBvYnlw/640?wx_fmt=png&from=appmsg)* 如果没有这一步，Claude可能会基于上文的闲聊或20轮之前的记忆开始瞎猜。
* 有了这一步，Claude的Context尾部被注入了最新的状态：“我现在处于Phase 2，目标是修改Login接口，且之前在Phase 1已经确认了Token格式。”
* 这相当于在每次CPU时钟周期开始时，强制执行一次**Fetch Instruction**。

### 阶段2：Data Offloading（数据卸载）

Claude需要查阅OAuth2.0的最新协议。

* **传统模式**：Claude搜索网页，把5000字的协议全文塞进对话框。你的Token在燃烧，模型被无关信息淹没。
* **本模式**：Claude搜索网页，提炼核心参数，写入 **`notes.md`**。在对话框里，它只说：“协议参数已存入notes。”
* 这相当于操作系统的**Swap机制,**把不常用的数据换出到磁盘，保持主存（Context Window）的清爽。

### 阶段3：State Commit（状态固化）

代码修改完成，测试通过。Claude**必须**编辑 `task_plan.md`：

* 将 `[ ] Phase 2` 改为 `[x] Phase 2`。
* 更新 `Status` 到 `Phase 3`。 这相当于**Write Back**。它赋予了LLM**时间感，**明确地知道什么是“过去”（已完成），什么是“未来”（待完成）。

## 它解决了什么？

这套Skill不是为了炫技，而是精准打击了LLM在长程任务中的四大死穴：

### 痛点1：易失性记忆 (Volatile Memory)

* **现象**：多轮对话后，Claude code忘了之前定义的变量或需求。
* **解法**：**文件系统持久化**。即使对话Session重置，只要 `notes.md` 和 `task_plan.md` 还在，Agent就能瞬间“恢复记忆”，继续工作。

### 痛点2：目标漂移 (Goal Drift)

* **现象**：执行50步后，Claude code沉迷于细枝末节，忘了原始目标。
* **解法**：**Read-Before-Decide（行动前读取）**。
+ Skill强制规定：`Before major decisions, READ task_plan.md`。
+ 利用Transformer的近因效应，刚读入的Plan处于Context最末端，权重最高，时刻提醒Agent“不要跑偏”。

### 痛点3：隐藏错误 (Hidden Errors)

* **现象**：API调用失败，Claude code默默重试，导致死循环或成本爆炸。
* **解法**：**Error Persistence（错误持久化）**。
+ `task_plan.md` 中包含 `## Errors Encountered` 章节。
+ Agent被要求将所有失败显式写入。下次读取计划时，它会看到“路径A失败过”，从而自动推理出路径B。

### 痛点4：上下文填充 (Context Stuffing)

* **现象**：把无关紧要的搜索结果全塞进Context，导致模型变笨、变慢、变贵。
* **解法**：**Offloading（卸载）**。
+ 所有长文本默认进 `notes.md`。Context中只保留一句：“已将搜索结果存入notes.md，关键点如下...”。

## Skill剖析

这个Skill的神奇之处在于它并没有修改Claude的模型权重，完全通过 `SKILL.md` 中的Prompt Engineering实现。

让我们看看 `planning-with-files/SKILL.md` 的关键片段：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUonF3ogKDfSpHOria6bG1KJFjh97CAddfQ0zeqj2CPOJp1sbV1zdGlTw/640?wx_fmt=png&from=appmsg)**1. 自动触发机制**： YAML头部定义了Skill的元数据。当用户输入“帮我规划...”、“研究...”或“这个任务很复杂”时，Claude会语义匹配 `description`，自动挂载此Skill。

**2. 负面约束 (Negative Constraints)**：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdHDoxNlibQYpyLVlYbRl7PFUcm80GvUYTyQxZibcu5tBbUXSVOPFxDumqjO8U785MviaCHY4IibcwYCvw/640?wx_fmt=png&from=appmsg)Skill使用了极强的命令语气，在System Prompt层级锁定了Agent的行为模式。

**3. 循环定义**： Skill显式定义了 `Read Plan -> Act -> Update Plan` 的闭环逻辑，将Agent从线性的问答机器变成了有状态的循环执行者。

## 如何安装与使用

### 安装

在你的终端中运行（假设你已配置Claude Code）：


```
cd ~/.claude/skills  
git clone https://github.com/OthmanAdi/planning-with-files.git
```
### 验证

重启Claude Code，输入： `> /skills` 你应该能看到 `planning-with-files` 出现在可用Skill列表中。

### 使用

直接对Claude说：

“研究一下Rust语言在嵌入式开发中的优势，并写一份报告。”

你会看到Claude**自动**：

1. 创建 `task_plan.md`。
2. 规划“搜索”、“阅读”、“撰写”三个阶段。
3. 执行搜索，将结果写入 `notes.md`。
4. 每完成一步，自动更新 `task_plan.md` 的Checkbox。
5. 最后生成报告。

## 结语

尽管业界对于Manus是否具备底层技术壁垒存在争议，但不可否认，它依然属于Context Engineering的优秀范例。

这说明除了提升模型本身以外，**构建良好的认知架构（Cognitive Architecture）** 同样重要。通过简单的文件读写和流程约束，就能让现有的模型发挥出超越参数规模的稳定性。

对于每一位AI开发者来说，理解并掌握这种“文件即记忆”的设计模式，是2026年的必修课。

来已来，有缘一起同行！

![图片](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/Iurk1iaf4xdG2f1hZialLRKViaL7icSibRcjXFz7E4XsNic3e2j4M4tcJsq5sH3MqSYnUPyh8P5qkJ51QZn4Qpxy8Vhw/640?wx_fmt=other&from=appmsg&watermark=1&wxfrom=5&wx_lazy=1&tp=webp#imgIndex=13)<本文完结>

1. **转载请与本喵联系，私自抓取转载将被起诉**

🎉**让我们一起创造更多美好！** 🎉  
如果您觉得这篇文章对您有帮助感谢您为我**【点赞】**、**【在看】**  
**<您为我点赞在看，只有我能看到>**  
**👉****微信号：xiumaoprompt****添加请注明来意！**

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/vn8ybmLmKvjnPKtRj9v9iw)*
