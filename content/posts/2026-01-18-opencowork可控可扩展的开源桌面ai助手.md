---
title: "OpenCowork：可控、可扩展的开源桌面AI助手"
date: 2026-01-18T01:04:07+08:00
lastmod: 2026-01-18T01:04:07+08:00
categories: ["AI与技术"]
tags: ["OpenCowork", "桌面Agent", "开源AI助手", "Skills系统", "MCP协议", "本地文件操作", "终端命令", "AI工作流"]
---

OpenCowork是Cowork的开源版本，主打“不锁模型”：只要是具备 Agent 能力的模型（MiniMax/Claude/GPT 等）都能接入，把 PC 变成 AI 工作伙伴。

核心能力很直观：能读写/创建/修改本地文件，也能执行终端命令，适合开发、脚本与日常整理；同时支持 Windows、macOS、Linux。

架构上用 Electron，主进程负责协调、渲染进程做 UI；关键调度中心是 AgentRuntime，启动时会把 Skills 和 MCP 客户端加载好，统一负责工具调用与结果回传。

因为AI能操作本机电脑，所以安全做得很硬：只允许访问你授权的文件夹，路径会校验并保护敏感位置；写文件、跑命令等高风险操作必须弹窗确认。

Skills 用来“长技能树”：从 `~/.opencowork/skills/` 动态加载 YAML/JSON 配置与指令资源，由 SkillManager 运行时管理。

MCP 则把外部工具接进来：MCPClientService 连接 MCP 服务器，自动发现工具，并用 `server__tool` 命名区分来源。

上手也快：先在设置里填 API Key / API URL / Model，再选授权目录。比如“读取 /Users/username/project/README.md”，会走 `read_file`；“创建 hello.py 并写入 print("Hello World")”，确认后用 `write_file`。

进阶玩法：用 doc-coauthoring 按“上下文收集→结构优化→读者测试”写设计文档；web-artifacts-builder 生成 React 应用并打包成单一 HTML；再配 `~/.opencowork/mcp.json` 接入 git 工具查提交历史。

一句话：开源、可控又能扩展。先少授权、勤确认；再用 Skills 固化流程，用 MCP 接外部工具。Apache 2.0 协议，也欢迎一起共建生态。

项目地址：https://github.com/Safphere/opencowork

<a class="wx_topic_link" topic-id="mkgdhjes-419xfc" style="color: #576B95 !important;" data-topic="1">#桌面Agent</a> <a class="wx_topic_link" topic-id="mkgdhjes-tjo7jf" style="color: #576B95 !important;" data-topic="1">#开源AI助手</a> <a class="wx_topic_link" topic-id="mkgdhjes-vl662k" style="color: #576B95 !important;" data-topic="1">#Skills系统</a> <a class="wx_topic_link" topic-id="mkgdhjes-epqiln" style="color: #576B95 !important;" data-topic="1">#MCP协议</a> <a class="wx_topic_link" topic-id="mkgdhjes-56zm29" style="color: #576B95 !important;" data-topic="1">#OpenCowork</a>
<a class="wx_topic_link" topic-id="mkgdkdrq-macst1" style="color: #576B95 !important;" data-topic="1">#Cowork</a>

![图片1](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabVEeXG3B6ygLEf5CeEXGO3VTguzdZZooat0WVGx362ldV6wFQH8giaww/0?wx_fmt=png&from=appmsg)

![图片2](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabM42gxjNUXRq38RLxXwou2GV3TJLosD3RFhfX3noxRtbmQU4Q6yA0qA/0?wx_fmt=png&from=appmsg)

![图片3](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciab4iaz0ADJU3VK7xREAg05FUtfatot61r1IpTYg56apysibMP1laWJ4hfA/0?wx_fmt=png&from=appmsg)

![图片4](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciab62hf1OCyM6l7lRrfxMDIreYQSgKt8EccsWwPZQ4kpAjX4VPLJOmyAw/0?wx_fmt=png&from=appmsg)

![图片5](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciab46SJjcubNdacbSkW3ibSo01j6LTZms1jkkpvutlKaTR89tMHY8JK5ZQ/0?wx_fmt=png&from=appmsg)

![图片6](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabX5tujELK5ph22wy89CtVLxEKzrsMBibs6BibDeRJDGZdq3dbiclwxqF3g/0?wx_fmt=png&from=appmsg)

![图片7](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabALZCj0xJibwhmlzv7EM3n54ERKSBViaWjgTBqc1yDZVX5hI6HbmAs6aA/0?wx_fmt=png&from=appmsg)

![图片8](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabPVLFbWKRpYwur42fRK7ICMSS1vePibBN5yQJ50iboyrR4dHBSA2BKZwg/0?wx_fmt=png&from=appmsg)

![图片9](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabpnkxuibrUhxmcF77JTuYWbJf60VB3yWrBzsibtmibos50z2uOFX4OQ6Vg/0?wx_fmt=png&from=appmsg)

![图片10](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/NyOPFgr71zibzCT6KH4KCwtPYLPEcDiciabbUKt8ibLcNXmAhMoHuK7dibuOl5jdML1pJPjR62lAgayKPUVoprXoDIQ/0?wx_fmt=png&from=appmsg)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/c6cCoTCAPV12G3tlnUvMXg)*