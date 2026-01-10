---
title: "Anthropic工程师都在用的AI编程秘技！让AI\"采访\"你做出完美应用"
date: 2026-01-02T00:29:08+08:00
lastmod: 2026-01-02T00:29:08+08:00
categories: ["AI与技术"]
tags: ["AI编程", "规范驱动开发", "访谈式开发", "Claude Code", "GPT Codex", "需求澄清", "代码生成", "开发效率"]
---
## 引言

在使用 AI 编程工具时，很多人习惯直接抛出一个模糊的需求，然后期待 AI 能“猜”出完美的实现。但结果往往是：AI 写出的代码和你心中所想相去甚远，于是陷入无尽的修改循环。

今天介绍一个来自 Anthropic 工程师的高效技巧——**规范驱动的访谈式开发**。这个方法的核心思路是：让 AI 先系统性地“采访”你，把零散的想法整理成一份完整细致的规范文档，然后再根据这份规范去实现应用。

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCXlR1MsVfBkPKHiatdRTMsgax3fUPdJCiaD86ZPSibnyvSKVgPZbfgoibpQ/640?wx_fmt=png&from=appmsg)

这个技巧适用于 Claude Code、Codex、Cursor、Augment 等多种主流 AI 编程工具。

## 核心理念

### 什么是规范驱动开发？

规范驱动开发的流程可以概括为三个阶段：

1.  **起点**：给 AI 一个简短但方向明确的初始说明
2.  **访谈**：让 AI 使用 `askUserQuestionTool` 对你进行系统化采访，问题涵盖功能、交互、视觉、技术实现等各个方面
3.  **输出**：AI 将问答整理成结构化的规格文档，再据此实现应用

这里提到的 `AskUserQuestionTool` 是 Claude Code 推出的交互式面板工具，允许用户通过单选、多选等方式快速回答问题。虽然这个工具只在 Claude Code 中原生存在，但只要在提示词中说明“请先像 AskUserQuestionTool 那样采访我、把需求问清楚再写规范”，其他 AI 工具通常也能理解并配合执行。

### 为什么这个方法有效？

*   **消除歧义**：通过系统性提问，确保 AI 真正理解你的需求
*   **覆盖盲区**：AI 会问到很多你可能没想到的细节和边缘情况
*   **提高质量**：基于完整规范的实现，比基于模糊描述的实现质量高得多
*   **减少返工**：前期多花时间在需求澄清上，后期修改成本大大降低

## 实战案例一：macOS 新年焰火应用

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCG2ZxPVib6XEnvEjdLtYGTzjTn55ZVufM3meOGDmhsacXC6mbbc45lgg/640?wx_fmt=png&from=appmsg)
![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVChiaLZFNr9tUC8mVib5F8IW1XCz9FFVxLhtdazomXJRByBQ3HVyzdCMcw/640?wx_fmt=png&from=appmsg)

### 访谈过程

以制作一个 macOS 新年焰火应用为例，整个访谈过程分为五个部分：

**第一部分：技术与平台信息**

*   目标平台是 iOS、macOS，还是需要多平台适配？
*   应用需要支持怎样的屏幕方向？
*   焰火效果的核心视觉希望是写实、卡通还是艺术化？
*   画面里除了焰火，还需要城市天际线、文字等元素吗？

**第二部分：技术实现细节**

*   粒子系统和物理模拟应该到什么程度？
*   性能要求如何？
*   是否要区分不同类型焰火的轨迹和爆炸方式？
*   “新年快乐 2026”这段文字应该如何与焰火配合展示？

**第三部分：视觉细节与体验流程**

*   背景如何设计？
*   时间线怎样推进？
*   是否需要不同阶段的氛围变化？
*   完整的焰火发射逻辑是什么？

**第四部分：交互细节和技术考量**

*   退出应用时的界面和控制方式
*   是否需要快捷键、调试开关？
*   项目结构和代码风格偏好

**第五部分：最终确认**

*   控制面板里需要哪些选项？
*   默认值是什么？
*   遇到异常状态时如何处理？

整轮访谈下来，AI 一共提出了 **39 个问题**，几乎把每一个可能的细节都覆盖到了。

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCbqMFs5KpFy8rv9kouMdq8dV3WHB0Pj1MNUjE9Cwhm6BXJibHwlIrUZg/640?wx_fmt=png&from=appmsg)

### 构建过程

拿到规范文档后，新开一个对话窗口，将文档交给 Claude Opus 4.5，并提示使用 XcodeBuildMCP 工具。这个 MCP 的优势在于：可以在后台创建 Xcode 工程、添加文件、执行构建，**全程无需打开 Xcode 程序**。

https://github.com/cameroncooke/XcodeBuildMCP

AI 制定了 9 个步骤的开发计划，然后开始自动执行：

*   调用 MCP 创建项目
*   逐步生成核心代码文件
*   遇到构建错误时自动发现并修复
*   在“发现错误—修复—再次构建”的循环中持续迭代

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCJ0HhxJy3ZDusoTh07iaEe3knQ8iasXMKDHf2NWW1U9oCJH2a72sqMc1g/640?wx_fmt=png&from=appmsg)

### 迭代优化

基础版本完成后，根据体验反馈继续优化：

*   增强上海天际线的表现，加入灯光效果
*   提升焰火的亮度和火花细节
*   让“新年快乐 2026”配合更大、更绚丽的焰火出现
*   生成应用图标并打包安装

### 最终效果

*   点击屏幕任意位置发射焰火，每点击 20 次触发多重烟花模式
*   鼠标移到右侧边缘弹出控制面板，提供 6 种焰火样式（心形、双层、纵向拉伸等）
*   背景隐约可见东方明珠和上海中心大厦的剪影
*   整体氛围契合新年气氛

## 实战案例二：Three.js 冬季小屋场景

### 基于现有文档的访谈

这个案例展示了另一种使用方式：对一份已有的计划文档进行深度访谈补充。

项目是一个基于 Three.js 的冬季小屋场景，初步计划包括：

*   添加极光天空效果
*   丰富室内圣诞装饰
*   实现景深缩放功能

让 Claude Code 读取这份计划文档，然后调用 SPEC interview skill 展开访谈：

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCTuMGPGcqtYsaicKFbzvf9ia7s7ZcwjD3vWicaXEuATq9ntJbXBu04wg7A/640?wx_fmt=png&from=appmsg)
![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCEFPuPX3Dvy0omUJhkjAKchPbucka8IGESW4tKa5lPgAPWuaranEYjA/640?wx_fmt=png&from=appmsg)

**极光相关**

*   视觉风格偏现实还是梦幻？
*   颜色和流动节奏的感觉
*   实现方式和性能约束
*   是否根据时间或用户操作动态变化？

**室内装饰相关**

*   除了圣诞树还有哪些元素？（壁炉、礼物、摆件等）
*   空间布局偏好
*   室内光影是否受壁炉火光影响？

**镜头与交互**

*   相机从室外推入室内时，外部场景如何处理？
*   窗外是否继续可见极光？

### 实现效果

将完善后的规格文档交给 Claude Opus 4.5，生成的场景包含：

*   画面上方紫色调的极光缓慢流动
*   滚动滚轮推入小屋内部
*   圣诞树、壁炉和玻璃窗户
*   窗外仍能看到极光变幻
*   小火车沿 8 字轨迹绕场景运动
*   小熊和礼物包装盒等细节

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVC2le9wRnZVlX6I4jxfibAnUTyK6icZsUxUUjWB3asINtCPctD45fYjTBA/640?wx_fmt=png&from=appmsg)
![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCHicudNiau8LgMnFDGGzxic4AkoQ408xKDbfX6AfXLfbm00uJ2sAN4C2Ng/640?wx_fmt=png&from=appmsg)

### 不同 AI 的效果对比

将同一份规范文档发给 GPT 5.2 Codex 进行对比测试：

*   Codex 能完成基础功能和结构
*   但存在明显闪烁、圣诞树造型不够美观、礼物包装盒细节有问题
*   在这个具体项目上，编码表现不如 Claude Opus 4.5

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCJBG5ic4Y4MaQoFIM3iaUXQLibvy4IfJHPlqz1tH37ibIezIjS79oyYgx1g/640?wx_fmt=png&from=appmsg)

值得一提的是，访谈技巧同样可以在 GPT 5.2 Codex 中使用。虽然它本身倾向于简洁回复、较少主动提问，但通过专门的 skill 引导，也能被激发出系统化的访谈能力，提出 15 个连续的问题。

![](https://mmbiz.qpic.cn/mmbiz_png/VzoLjU1b4d9m1Mb7CJeSic1CFJEyTcOVCH6ydlXUfaZ64QsfDgVJL2lxMqobaHLEmeO7hWsgZjPicq4qRRLzZiaLA/640?wx_fmt=png&from=appmsg)

## 实践建议

### 如何开始

1.  **准备初始说明**：写一段简短但方向明确的需求描述
2.  **触发访谈**：在提示词中明确要求 AI 先进行系统化采访
3.  **认真回答**：访谈过程中尽量详细地回答每个问题
4.  **审阅规范**：检查生成的规范文档是否准确反映你的需求
5.  **开始实现**：将规范文档交给 AI 进行代码实现

### 提示词模板

请阅读这份 `@SPEC.md` 文件，并使用 `AskUserQuestionTool` 针对任何方面对我进行详细访谈：包括技术实现、UI 与 UX（用户界面与体验）、潜在疑虑、权衡取舍等，但请确保提出的问题不是那种显而易见的问题。

请保持极高的深度，并持续对我进行访谈，直到内容完整为止，最后再将规范说明（Spec）写入该文件中。

### 适用场景

这个方法特别适合：

*   想法还比较模糊，需要帮助梳理的项目
*   涉及较多细节和交互的应用
*   希望减少后期返工的正式项目
*   多人协作时需要明确需求边界

## 总结

让 AI 不只是帮你写代码，而是先把你真正想要的东西问清楚，再帮你一步一步落地实现。

## 广告

过去我已创作了 380+ 篇AI主题原创内容，我对继续写作充满信心，因为这是我的爱好，我非常热爱这件事。

如果喜欢我的文章和视频，欢迎加入我的知识星球，我会分享最新的 AI 资讯、源代码，回答你的问题。我们下次再见啦！

![图片](https://mmbiz.qpic.cn/mmbiz_jpg/VzoLjU1b4dib9FYdh0X6q5ACd47ns7cTMOaSTmXAmvALDAuhFIL0n7tW78YnOdgY68jkia2lM5ZVMkNoTY0cez7g/640?wx_fmt=other&from=appmsg&wxfrom=5&wx_lazy=1&wx_co=1&randomid=mw9koxju&tp=webp#imgIndex=33)

**最近文章，请看这里：**

**[2025最强AI编程组合：Opus 4.5 + GPT 5.2 Codex 实战开发安卓APP](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494997&idx=1&sn=3049d892c46101661f025a3403cf6f22&scene=21#wechat_redirect)**

**[开源神器！让AI一键生成PPT级信息图，197套模板随便用](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494975&idx=1&sn=902fc55c28f24302420fe012a2b85629&scene=21#wechat_redirect)**

**[实测 MiniMax-M2.1，编码真的强](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494947&idx=1&sn=0a2b3fc54b0497c359b68ac79028a2f8&scene=21#wechat_redirect)**

**[OpenAI最强编程模型来了！GPT-5.2-Codex vs Opus 4.5 对决](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494883&idx=1&sn=90f9db5c7202ee81694e5a37828d94c2&scene=21#wechat_redirect)**

**[28天上线全球爆款：OpenAI 用 Codex 重新定义人机协作开发](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494817&idx=1&sn=96c2edf32fc02aa6b50ab441934538c7&scene=21#wechat_redirect)**

**[Cursor Plan模式真香](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494586&idx=1&sn=041768142c5778573e59967cfe05e9dd&scene=21#wechat_redirect)**

**[解读 Anthropic 博文：适用于长期运行 Agents 的有效框架](https://mp.weixin.qq.com/s?__biz=MzI5MjQ3ODY3Mw==&mid=2247494450&idx=1&sn=20f7121741ab3f69f83ca48948273eaa&scene=21#wechat_redirect)**