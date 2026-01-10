---
title: "NotebookLM 平替来了：开源自托管的 Open Notebook，把资料留在自己电脑里"
date: 2026-01-11T01:10:33+08:00
lastmod: 2026-01-11T01:10:33+08:00
categories: ["AI与技术"]
tags: ["开源项目", "AI工具", "NotebookLM", "自托管", "学习助手", "多模态", "REST API", "本地模型"]
---

嗨，我是小华同学，专注解锁高效工作与前沿AI工具！每日精选开源技术、实战技巧，助你省时50%、领先他人一步。👉免费订阅，与10万+技术人共享升级秘籍！

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/mRgvnruIwyCMXsVvwpicauWciaAGzibsM2icM2Oj0tBlPgIicjO5h0Kw8xtianRt1ccjJERZMiajKicsN0NWaO5W5c2tZQ/640?wx_fmt=png&from=appmsg)

> 如果你用过 NotebookLM，大概率会爱上这种“把资料丢进去→对着资料问问题→沉淀笔记”的学习方式。但很多人卡在同一个点：**资料隐私、模型选择、可扩展性**。

我最近在折腾一个开源项目：**Open Notebook**——它把 NotebookLM 的核心体验做成了**可自托管**版本，主打“Take Control of Your Learning. Privately.”（学习资料尽量掌控在自己手里）。

### 它解决了什么

**你控数据**：应用可自托管，研究资料/笔记放在自己的机器或服务器上。

**你控模型**：内置支持 16+ 模型/服务商（OpenAI、Anthropic、Ollama、LM Studio 等），可以按成本/效果自由切换；也能走本地模型路线。

**你控工作流**：不仅“聊天问答”，还支持“内容转换（Transformations）”、播客生成、以及完整 REST API 方便自动化集成。

## 我觉得最香的功能点

**多模态资料一站式管理**：PDF、网页、音频、视频、Office 文档等都能塞进同一个 Notebook。

**全文检索 + 向量检索**：不是只靠“对话记忆”，而是能在你所有资料里搜索。

**播客生成（多说话人）**：支持 1-4 位说话人，还能做“Episode Profiles”，适合把学习资料变成通勤可听内容。

**推理模型支持**：例如 DeepSeek-R1、Qwen3 这类 thinking/reasoning 模型也在支持列表里。

**REST API**：这点对程序员很关键——可以把“采集→处理→输出”接进自己的脚本/工作流（比如定时抓网页/论文→自动总结→发到你的笔记系统）。

> 小提醒：如果你选用的是云端模型（比如 OpenAI/Anthropic），被选中的上下文仍可能会发送给对应服务商；想更“本地化”，就优先用 Ollama/LM Studio 之类本地端点。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/mRgvnruIwyCMXsVvwpicauWciaAGzibsM2icbp1FyXqEuTdK6V5I29QicGM0MflcO13J9gjg7AKQyVQSBiaRV7P90voA/640?wx_fmt=png&from=appmsg)

## 5 分钟上手

### 方式 A：Docker（官方推荐）

核心流程就 4 步：准备模型 API Key（或配好 Ollama）→ 写 `docker-compose.yml` → `docker compose up -d` → 打开本地地址。

```
# 启动（示例指令，具体 compose 文件按官方指南）
docker compose up -d
# 打开（生产默认）
# http://localhost:8502
```

### 方式 B：用官方 boilerplate 更省事（自托管模板）

如果你懒得自己搭目录结构，可以直接用 `open-notebook-boilerplate`：复制 env、填 Key、一键起服务。

```
git clone https://github.com/lfnovo/open-notebook-boilerplate
cd open-notebook-boilerplate
cp docker.env.example docker.env
docker compose up
# 然后打开：
# http://localhost:8080
```

## 我会怎么用它

**论文/技术文档速读**：PDF 丢进去 → 让它先给“主旨/结论/争议点/可复现步骤” → 追问细节 → 把结论写进 Notes。

**视频学习转可复习笔记**：YouTube/链接导入 → 让它按章节总结 + 生成“复习清单/练习题”。

**把资料变成通勤播客**：同一主题的多篇文章/笔记聚合 → 多说话人播客输出 → 通勤听一遍，回家再做二次笔记。

## 总结

资料敏感、想尽量自托管的人（研究、咨询、产品、法务、投研等）。

喜欢折腾模型/成本优化的人：同一套笔记系统，模型随时换。

程序员/独立开发者：想用 API 把它接进自己的自动化管道。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/mRgvnruIwyCMXsVvwpicauWciaAGzibsM2icFm5bjXUUtjqZfjz1BCOsiapj8vOu2tcSaIBQWlEa2nOOjmtesrlT0CQ/640?wx_fmt=png&from=appmsg)

## 项目地址

https://github.com/lfnovo/open-notebook

---

热门阅读
[牛，AI 写代码进入“编排时代”：Vibe Kanban 让多个 Agent 并行干活～～～](https://mp.weixin.qq.com/s?__biz=Mzk0MjcxOTM2Nw==&mid=2247500617&idx=1&sn=ff4012d72aa320b11ea87fa96546b182&scene=21#wechat_redirect)
[年会/活动要抽奖？这个开源 3D 抽奖球直接把现场气氛拉满,支持 Excel 导入 + 结果导出](https://mp.weixin.qq.com/s?__biz=Mzk0MjcxOTM2Nw==&mid=2247500547&idx=1&sn=e2e0cb8879c404bee4d5fffbf5b7ba65&scene=21#wechat_redirect)
[前端的同学，终于要起飞啦，Github 6.3k star + ，免费可商用的UI元素库！！！](https://mp.weixin.qq.com/s?__biz=Mzk0MjcxOTM2Nw==&mid=2247498204&idx=1&sn=54985349b350f372ffe424aa0fdfe977&scene=21#wechat_redirect)
[GitHub 4k star 开源一站式ai数字人](https://mp.weixin.qq.com/s?__biz=Mzk0MjcxOTM2Nw==&mid=2247497462&idx=1&sn=31c8d009d172d1922f5b0a7ae78acf36&scene=21#wechat_redirect)
[免费！免费！免费！重要的事情说三遍，Github star 1.1k 开源项目，真的太好用啦，新手抓紧冲啊~~~](https://mp.weixin.qq.com/s?__biz=Mzk0MjcxOTM2Nw==&mid=2247497996&idx=1&sn=a0a2150213fe0ec1312aff9e386fcc4e&scene=21#wechat_redirect)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/HmvPUuyw-7NJ6uZ8UPL7TQ)*