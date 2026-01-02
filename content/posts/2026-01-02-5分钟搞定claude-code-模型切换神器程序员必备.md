---
title: "5分钟搞定！Claude Code 模型切换神器，程序员必备！"
date: 2026-01-02T11:23:41+08:00
lastmod: 2026-01-02T11:23:41+08:00
categories: ["开发工具"]
tags: ["Claude Code", "AI编程", "效率工具", "命令行", "模型切换", "vibe coding", "开源工具", "开发者效率"]
---

最近都在使用 `Claude Code` 来 `vibe coding`。过程中需要不停的去切换不同的国内模型，每次切换模型就像打仗一样——先退出当前会话、复制粘贴一长串环境变量、输入 anthropic key、再启动 CLI... 这一套下来至少 3 分钟，思路都被打断了！

作为一个囊中羞涩的程序员，用不起原生 Claude 模型，只能在各大国产模型间横跳。但每次切换都这么繁琐，实在忍无可忍...

**好消息是：5 分钟读完这篇文章，你的痛点将彻底消失！**

> 不要问为什么不使用原生 Claude 模型，**问** 就一个字，**穷**

---

## 📑 目录

*   🔍 寻找解决方案
*   🚀 安装步骤
*   🎬 演示效果
*   📋 支持模型
*   ✨ 核心优势

---

## 🔍 寻找解决方案

首先搜了一下 GitHub，发现了一个 `claude code router` 就实现了这个功能！它可以对接不同的模型，原理是转译 OpenAI 协议（绝大部分模型都支持）到 Anthropic 协议。

🛠️ **方案解析**：

*   需要本地启动一个后台服务
*   利用 express 作为 proxy 进行转译

❌ **个人感觉：太复杂了！**

💡 **灵光一现**：不如直接利用快捷命令，读取不同环境变量，达到切换不同的模型的目的！

🚀 **说干就干！**

由于时间关系，已经做好了一套工具脚本，放在了 GitHub 上了，请参考仓库（https://github.com/OldManZhang/claude-code-base-model-shortcut-command-line.git）

## 🚀 安装步骤

> 所有的安装步骤都是在 Mac 环境中进行，Win 用户请自行适配。

1.  git clone 仓库
2.  cp bin/cc ~/.local/bin/ `cc` 是一份 shell 脚本，使用文本工具就可以查看和编辑
3.  如果需要，添加 ~/.local/bin 到 PATH 环境变量中；如果已经配置就可以忽略
4.  添加大模型的配置文件到 ~/.cc/configs/env.[model]
5.  重启 terminal
6.  cc model 即可

## 🎬 演示效果

💡 **Tip**: 下方演示建议配合动图观看，效果更直观！一个命令切换模型，无缝衔接编程体验～

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/gNxJ6Lnlg8lbLicVajNKXRS6k20Jia1qmH7moic36hIZSpxKWA8JTmJGALr75iaISHFevRQX3Qfo6GWPmQDAMTjvag/640?wx_fmt=gif&from=appmsg)

### 直接看演示

```
% cc list
ℹ Available configurations:

Environment variables:
  CC_DEFAULT_PROVIDER=minimax
  LLM_PROVIDER=<not set>

Configuration directory: /Users/robinzhang/.cc/configs

  anthropic
  glm
  kimi
  minimax ℹ [default]
  openai

% cat ~/.cc/configs/env.kimi

# Claude-specific configuration
export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
export ANTHROPIC_AUTH_TOKEN=sk-kimi-1234. # change your own key
export ANTHROPIC_MODEL=kimi-for-coding
export ANTHROPIC_SMALL_FAST_MODEL=kimi-for-coding

% cc kimi
ℹ Loading configuration for kimi...

✓ Configuration loaded for kimi

ℹ Environment variables set:
  ANTHROPIC_BASE_URL=****
  ANTHROPIC_AUTH_TOKEN=****
  ANTHROPIC_MODEL=****
  ANTHROPIC_SMALL_FAST_MODEL=****

✓ Now you can use Claude with kimi configuration

ℹ Starting Claude CLI...


╭─── Claude Code v2.0.71 ────────────────────────────────────────────────────────────────╮
│                         │ Tips for getting started                                     │
│      Welcome back!      │ Run /init to create a CLAUDE.md file with i…                 │
│                         │ Note: You have launched claude in your home…                 │
│      * ▗ ▗   ▖ ▖ *      │ ────────────────────────────────────────────                 │
│     *           *       │ Recent activity                                              │
│      *   ▘▘ ▝▝   *      │ No recent activity                                           │
│                         │                                                              │
│   kimi-for-coding · API Usage Billing   │                                              │
│        /Users/robinzhang               │                                              │
╰────────────────────────────────────────────────────────────────────────────────────────╯


% cc minimax
ℹ Using default provider from CC_DEFAULT_PROVIDER: minimax

ℹ Loading configuration for minimax...

✓ Configuration loaded for minimax

ℹ Environment variables set:
  ANTHROPIC_BASE_URL=****
  ANTHROPIC_AUTH_TOKEN=****
  ANTHROPIC_MODEL=****
  ANTHROPIC_SMALL_FAST_MODEL=****

✓ Now you can use Claude with minimax configuration

ℹ Starting Claude CLI...


╭─── Claude Code v2.0.71 ────────────────────────────────────────────────────────────────╮
│                      │ Tips for getting started                                        │
│    Welcome back!     │ Run /init to create a CLAUDE.md file with instru…               │
│                      │ Note: You have launched claude in your home dire…               │
│    * ▗ ▗   ▖ ▖ *     │ ─────────────────────────────────────────────────               │
│   *           *      │ Recent activity                                                 │
│    *   ▘▘ ▝▝   *     │ No recent activity                                              │
│                      │                                                                │
│   MiniMax-M2 · API Usage Billing   │                                                   │
│     /Users/robinzhang              │                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────╯
```

从这里开始，就可以快乐地进行 `vibe coding` 了。

## 📋 支持的国产模型

`Minimax-m2`、`kimi-coding-plan`、`GLM` 都支持。

## ✨ 核心优势

| 特性 | 描述 |
| --- | --- |
| 🚀 **纯脚本无依赖** | 无需安装任何第三方库，一键运行 |
| ⚙️ **配置文件自由定制** | 支持自定义模型参数，满足个性化需求 |
| ⚡ **切换速度超快** | 从 3 分钟缩短到 3 秒，效率提升 60 倍 |
| 🔐 **避免重复输入密钥** | 一次配置，永久使用，安全便捷 |

## 🎯 适合人群

**💻 经常在多个 AI 模型间横跳的开发者**

**🤖 追求高效编程体验的程序员**

**⏰ 讨厌重复劳动的时间管理者**

### 🎉 最终效果

> **再也不用记复杂的切换命令啦！**
>
> 一个 `cc` 命令，从 kimi 到 minimax，从 openai 到 glm…… 轻松切换，流畅编程！

---

## 💬 互动时间

### 🤔 你还在用什么方法切换模型？

欢迎在评论区分享你的方法：

*   📝 命令行脚本
*   🔧 图形化工具
*   📋 复制粘贴大法
*   🧠 纯手工记忆
*   💡 其他奇技淫巧

### 🎯 你在使用 vibe coding 中遇到什么问题？

*   模型切换太繁琐？
*   编程思路总是被打断？
*   环境配置让人崩溃？
*   还是遇到了其他痛点？

## 💌 留言区等你！

**如果这个工具对你有帮助，欢迎给个 ⭐ Star 支持一下！**

**GitHub 仓库：OldManZhang/claude-code-base-model-shortcut-command-line**

#### 引用链接

`[1]` 🔍 寻找解决方案: *#寻找解决方案*  
`[2]` 🚀 安装步骤: *#安装步骤*  
`[3]` 🎬 演示效果: *#直接看演示*  
`[4]` 📋 支持模型: *#支持的国产模型*  
`[5]` ✨ 核心优势: *#优点总结*  
`[6]` OldManZhang/claude-code-base-model-shortcut-command-line: *https://github.com/OldManZhang/claude-code-base-model-shortcut-command-line.git*