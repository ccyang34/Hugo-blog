---
title: "免费开源工具－claude-code-router：让你丝滑纵享各种Claude Code模型"
date: 2025-12-29T21:46:07+08:00
lastmod: 2025-12-29T21:46:07+08:00
categories: ["AI编程工具"]
tags: ["Claude Code", "Claude Code Router", "AI编程", "模型路由", "开源工具", "配置教程", "成本优化", "多模型集成"]
---

Claude Code Router (CCR) 是一个中间件工具，简单来说，它就是 Claude Code 和各种 AI 模型之间的智能调度器。

最近“智谱”和“火山方舟”都推出了 **Coding Plan·限时优惠**，趁低价也薅了一拨羊毛，本篇就详细的记录了我如何使用 CCR：https://github.com/musistudio/claude-code-router 在 Claude Code 中丝滑的使用各类大模型进行编程。

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVwd6rDKLsqGKRyNF6wEBK0y1BtBcw47feX7MzHl8M1bFLS0ASRvRAqQ/640?wx_fmt=png&from=appmsg)

## Claude Code 简介

Claude Code 是由 Anthropic 公司推出的一款智能编程工具，基于 Claude Sonnet 模型开发。这款工具最大的亮点是能够通过自然语言指令直接在终端操作，无需复杂的配置，就能完成代码编辑、Bug 修复、代码搜索等任务。它支持多种编程语言，包括 Java、Python、go 等，并且可以直接集成到 VS Code、Cursor 等开发环境中，让开发者体验更流畅。

## 为什么需要 Claude Code Router (CCR)?

虽然 Claude Code 功能强大，但直接使用官方模型存在以下挑战：

### 现实问题

*   成本高昂：官方模型按 token 计费，长期或大规模使用费用显著
*   额度限制：存在每日、每周的调用限制，频繁调整的策略对重度用户不友好
*   灵活性不足：无法直接使用 DeepSeek、OpenRouter、本地 LLM 等第三方或自建模型

### 解决方案

通过在调用链路中插入路由/代理层，可以实现：

*   按任务类型或成本策略路由到不同模型
*   降低整体使用成本
*   提高服务可用性
*   获得更大的模型选择灵活性

### Claude Code Router (CCR) 智能路由代理

当需要更复杂的模型管理策略时，直连方式就显得力不从心了。智能路由层可以实现：

*   动态路由：根据任务类型、上下文长度、成本预算智能选择模型
*   多模型协作：让推理模型处理复杂逻辑，再将思路传递给主模型
*   高级策略：fallback 机制、并行调用、模型融合等

Claude Code Router 正好能实现我们需要的功能，它是一款开源的路由解决方案，提供企业级功能：

*   多 Provider 统一管理
*   灵活的路由规则引擎
*   请求/响应转换器（Transformer）
*   交互式模型切换（/model provider,model）
*   完整的日志与统计系统

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVOdrJAeEbCRWhoHYz2G3gBMck8z3D4R7rys4gIPZY5Z65iaq36nGIUCw/640?wx_fmt=png&from=appmsg)

## Claude Code 及 Claude Code Router 的安装与配置

### 官网

*   github: `https://github.com/musistudio/claude-code-router`
*   中文文档：`https://github.com/musistudio/claude-code-router/blob/main/README_zh.md`

### 安装方式

1.  **Claude Code 安装**
    ```bash
    npm install -g @anthropic-ai/claude-code
    ```
2.  **Claude Code Router (CCR) 安装**
    ```bash
    npm install -g @musistudio/claude-code-router
    ```

### 运行

1.  **启动**
    ```bash
    # 命令行模式
    ccr code
    ```
    ![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVJNtTDCpl4p43ROprU7UCAZtkQia7uuNjGPvbjl0ANvxbKB8YDygcCQg/640?wx_fmt=png&from=appmsg)
    点击 “Yes,proceed”，即可进入 Claude Code
    ![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVYW949tNBGPrEzQJsQeFiaPw3TgGzJN90UTApcGmWB1kEPvCtibnXOsUg/640?wx_fmt=png&from=appmsg)
2.  **重启**
    ```bash
    # 重启
    ccr restart
    ```
    ![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVObf8UGDkIZb9IdtvNaPyBTjInr6goh3yMu1NRZokVVGMjiaCXC7vylw/640?wx_fmt=png&from=appmsg)
    每次修改完配置文件都需要重启 CCR 服务。
3.  **UI界面**
    ```bash
    # UI 管理界面
    ccr ui
    ```
    ![](https://mmbiz.qpic.cn/mmbiz_jpg/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znV6z2slAGU4VlMH4anKk9Jssxx3SeWltibeumMJMolXYDGCrJ55aQPVzw/640?wx_fmt=jpeg&from=appmsg)

## Claude Code Router 多模型集成

### 配置文件

配置文件一般存放在用户目录下的 `.claude-code-router` 目录，如果没有可以自行创建或执行 `ccr ui` 通过 UI 界面来配置生成。

`~/.claude-code-router/config.json`：

我的配置文件如下，可复制修改使用

```json
{
  "LOG": true,
  "LOG_LEVEL": "debug",
  "CLAUDE_PATH": "",
  "HOST": "127.0.0.1",
  "PORT": 3456,
  "APIKEY": "",
  "API_TIMEOUT_MS": "600000",
  "PROXY_URL": "",
  "transformers": [],
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "<your-api-key>",
      "models": [
        "google/gemini-2.5-pro",
        "google/gemini-2.5-flash",
        "anthropic/claude-sonnet-4",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet:thinking"
      ],
      "transformer": {
        "use": [
          "openrouter"
        ]
      }
    },
    {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/v1/chat/completions",
      "api_key": "ollama",
      "models": [
        "qwen2.5-coder:latest"
      ]
    },
    {
      "name": "volcengine",
      "api_base_url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
      "api_key": "<your-api-key>",
      "models": [
        "doubao-seed-code-preview-251028"
      ],
      "transformer": {
        "use": [
          [
            "maxtoken",
            {
              "max_tokens": 100000
            }
          ],
          "openrouter"
        ]
      }
    },
    {
      "name": "siliconflow",
      "api_base_url": "https://api.siliconflow.cn/v1/chat/completions",
      "api_key": "<your-api-key>",
      "models": [
        "moonshotai/Kimi-K2-Instruct"
      ],
      "transformer": {
        "use": [
          [
            "maxtoken",
            {
              "max_tokens": 16384
            }
          ]
        ]
      }
    },
    {
      "name": "bigmodel",
      "api_base_url": "https://open.bigmodel.cn/api/anthropic/v1/messages",
      "api_key": "<your-api-key>",
      "models": [
        "glm-4.6",
        "glm-4.5-air"
      ],
      "transformer": {
        "use": [
          "Anthropic"
        ]
      }
    }
  ],
  "Router": {
    "default": "bigmodel,glm-4.6",
    "background": "ollama,qwen2.5-coder:latest",
    "think": "siliconflow,moonshotai/Kimi-K2-Instruct",
    "longContext": "openrouter,google/gemini-2.5-pro",
    "longContextThreshold": 60000,
    "webSearch": "openrouter,google/gemini-2.5-flash",
    "image": ""
  },
  "CUSTOM_ROUTER_PATH": ""
}
```

*   将 `<your-api-key>` 替换成自已的就可以了。
*   default 设置可以自行替换，我的配置里为智普 glm-4.6，如果要换成火山豆包，将 `bigmodel,glm-4.6` 替换为： `volcengine,doubao-seed-code-preview-251028`

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVoOzb3uxImp2HVjOg5rayZiaESeB38ghVibMibd6z6zkKPSdMx6B2z75GQ/640?wx_fmt=png&from=appmsg)

### 配置详解

1.  **基础配置**
    *   PROXY_URL：代理服务器地址，用于外部 API 请求
    *   LOG：是否启用日志文件（`true/false`）
    *   LOG_LEVEL：日志级别（`fatal/error/warn/info/debug/trace`）
    *   APIKEY：可选的访问密钥，启用后客户端需在 `Authorization` 或 `x-api-key` 头中提供
    *   HOST：服务监听地址（默认 `127.0.0.1`，未设置 APIKEY 时强制为本地）
    *   NON_INTERACTIVE_MODE：非交互模式，适配 CI/Docker 等自动化环境
    *   API_TIMEOUT_MS：上游模型调用超时时间（毫秒）
2.  **日志系统**
    CCR 采用双日志架构：
    *   服务器日志：记录 HTTP 请求、API 调用等，使用 pino 写入 ~/.claude-code-router/logs/ccr-*.log
    *   应用日志：记录路由决策、业务事件，写入 ~/.claude-code-router/claude-code-router.log
3.  **Providers 配置**
    *   name：Provider 标识符
    *   api_base_url：API 基础地址
    *   api_key：认证密钥
    *   models：支持的模型列表
    *   transformer：请求/响应转换规则，用于适配不同 API 协议
4.  **Router 配置**
    *   default：默认模型路由
    *   background：后台任务使用的模型（通常选择本地或低成本模型）
    *   think：复杂推理任务模型
    *   longContext：长上下文任务模型
    *   longContextThreshold：长上下文阈值（token 数）
    *   webSearch：需要联网搜索的任务模型

### 动态切换模型

在 Claude Code 里输入：

```
/model openrouter,anthropic/claude-3.5-sonnet
```

后续请求都用这个模型，随时切换，灵活如你！

## 用量及费用统计

ccusage 是一个用于统计 Claude Code 使用量的工具，它从 ~/.claude/projects 目录读取了大模型的对话历史记录，从而统计每天的 tokens 消耗量。

*   安装
    ```bash
    npm i -g ccusage
    ```
*   查看用量
    ```bash
    ccusage daily
    ```
    ![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rjBgVSZQJicXup4PRkcb7znVfjkfsFrDRMyNe3zEv9ic5JELCYBNDmEz6G7Owy7zuQ9ayUuT5Gz8S3g/640?wx_fmt=png&from=appmsg)

## 总结：CCR 让 AI 模型“打工人”各显神通

Claude Code Router 不是简单的“API 代理”，而是 AI 模型的智能调度中心。它让你像打车一样，按需分配 AI 模型，省钱、省心、效率爆表。无论你是 AI 极客、企业开发者，还是自动化工作流玩家，CCR 都能帮你把 AI 模型用到极致。

还在为 Claude 太贵、Gemini 失忆、DeepSeek 慢、Qwen 智商堪忧而发愁？用 CCR，把所有 AI 模型变成你的“打工人”，让他们各司其职，卷出新高度！

---

如果您正在学习 AI Agent，想利用 Coze/dify/n8n 做一些 RPA 方面的工作流搭建，欢迎在评论区留言或入群交流！

![](https://mmbiz.qpic.cn/mmbiz_png/8IDdJUwH9rhJKna6Qn0g7RPzAXukAfqVQ1DHLeEXQNwiciagUNw9M8bK3ZLibQJVMBVbp3vNm3eBd9rYC1J9Dznug/640?wx_fmt=png&from=appmsg)

喜欢本篇内容请给我们点个在看

![图片](https://mmbiz.qpic.cn/mmbiz_png/kzAe1ibcVjhyzsCzlSDxIBhtQGI78X7iaxhcBBWAxtBFbNnu1CDVOJv3RVXON6uZaZiaJiadLauopZOMgQAOreHcqA/640?wx_fmt=png&wxfrom=13&tp=wxpic)

欢迎**【关注】**&**【星标】**&**【转发】**