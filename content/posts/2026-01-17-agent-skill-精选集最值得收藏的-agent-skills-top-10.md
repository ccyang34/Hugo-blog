---
title: "Agent Skill 精选集：最值得收藏的 Agent Skills Top 10"
date: 2026-01-17T22:26:53+08:00
lastmod: 2026-01-17T22:26:53+08:00
author: "AIGC胶囊"
categories: ["AI与技术"]
tags: ["AI工具", "Agent Skills", "Claude", "Codex", "GitHub", "效率工具", "技能推荐", "AI助手"]
---

**作者**: AIGC胶囊

如果你正在用 Claude Code 或 Codex，一定对 **Agent Skills** 不陌生。通过安装 **Agent Skills**，你可以让这些 AI 助手变得更强——不用每次都解释你的需求，它们直接就知道该怎么做。

最近有人在 GitHub 上做了一个采样调查，统计了哪些 Skills 的质量最佳和最受欢迎。我整理了这份 **Top 10 榜单**，加上使用场景和适合人群，帮你快速找到最有用的那几个。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/5EZ1TshXkh5xG9WntZJeZSrJGxBL4Z35JynPa6qvvcBPHEDpLgIbfSnQFII7Y6Wp5sdPicfq3BVrKdLedz53XCA/640?wx_fmt=jpeg&from=appmsg "null")

### Top 10 最受欢迎的 Agent Skills

#### **1. Skill Creator (技能生成器)**

*   **📝 简介：** Agent 的元技能。它能通过引导式对话，帮助用户将脑海中的想法或纸面上的 SOP 自动转化为符合标准的 `SKILL.md` 文件。
*   **🎯 适合场景：**
    *   当你发现现有的 Skill 无法满足特定需求时（例如：需要一个专门对接你们公司内部 ERP 的技能）。
    *   企业内部将业务流程（SOP）标准化并分发给 AI 使用。
*   **👥 适合人员：** 开发者、Prompt 工程师、企业 IT 管理员、超级个体。
*   **🔗 URL:** https://github.com/anthropics/skills/tree/main/skills/skill-creator

#### **2. Git PR Reviewer (代码审查专家)**

*   **📝 简介：** 集成 CI/CD 的代码审查工具。严格遵循 Google/Airbnb 规范，具备安全漏洞扫描能力，能对 Pull Request 提出行级修改建议。
*   **🎯 适合场景：**
    *   代码合并前的自动质量检查，防止低级错误和安全漏洞上线。
    *   Tech Lead 忙不过来时，作为第一道防线过滤垃圾代码。
*   **👥 适合人员：** 软件工程师、技术负责人 (Tech Lead)、DevOps 工程师。
*   **🔗 URL:** https://agentskills.io/skills/git-pr-reviewer

#### **3. Excel Data Analyst (Excel 分析师)**

*   **📝 简介：** 基于 Python Pandas 的数据处理专家。能自动清洗脏数据、处理缺失值、转换格式，并生成专业的数据透视表和图表。
*   **🎯 适合场景：**
    *   处理格式混乱的月度财务报表、销售流水。
    *   需要快速从一堆 CSV 中找出趋势或异常值，并制作汇报图表。
*   **👥 适合人员：** 财务会计、运营经理、数据分析师、小微企业主。
*   **🔗 URL:** https://github.com/anthropics/skills/tree/main/skills/data-analysis

#### **4. Slide Deck Builder (PPT 构建者)**

*   **📝 简介：** 自动化演示文稿生成器。能将 Markdown 大纲或长篇文章直接转换为设计精美的 `pptx` 文件，支持企业模版挂载。
*   **🎯 适合场景：**
    *   时间紧迫，需要快速产出方案初稿或会议汇报 PPT。
    *   将技术文档或产品白皮书快速转化为可视化的演示材料。
*   **👥 适合人员：** 咨询顾问、产品经理、市场人员、售前工程师。
*   **🔗 URL:** https://agentskills.io/skills/presentation-builder

#### **5. PDF Deep Reader (文档深度解析)**

*   **📝 简介：** 针对长文档（100页+）的智能阅读器。采用分块索引技术，能精准提取条款、跨页表格数据，并进行跨文档对比。
*   **🎯 适合场景：**
    *   审核冗长的法律合同，寻找风险条款。
    *   阅读几百页的上市公司财报或招股书，提取关键财务指标。
    *   学术研究时的文献综述整理。
*   **👥 适合人员：** 律师、法务、投资分析师、科研人员、学生。
*   **🔗 URL:** https://agentskills.io/skills/pdf-deep-reader

#### **6. Tech Stack Expert (技术栈专家 - Next.js/React)**

*   **📝 简介：** 封装了特定技术栈（如 Next.js 15+）最新最佳实践的编程助手。防止 AI 使用过时语法，提供架构级建议。
*   **🎯 适合场景：**
    *   项目初始化搭建（Scaffolding），确保目录结构规范。
    *   技术栈升级迁移（例如从 Pages Router 迁移到 App Router）。
    *   解决特定框架的疑难杂症（Hydration Error 等）。
*   **👥 适合人员：** 前端工程师、全栈开发者、架构师。
*   **🔗 URL:** https://github.com/vercel/agent-skills

#### **7. Postgres DB Admin (数据库管理员)**

*   **📝 简介：** 安全的 SQL 操作专家。默认开启只读保护，支持查询性能分析（Explain）和索引优化建议，杜绝删库风险。
*   **🎯 适合场景：**
    *   线上生产环境的故障排查与数据验证。
    *   编写复杂的统计 SQL，或优化运行缓慢的查询语句。
*   **👥 适合人员：** 后端工程师、DBA、运维人员。
*   **🔗 URL:** https://agentskills.io/skills/postgres-admin

#### **8. Research Synthesis (研报综述)**

*   **📝 简介：** 严谨的研究助理。执行“搜索-筛选-验证-引用-撰写”的标准化流程，输出包含真实参考文献的深度报告。
*   **🎯 适合场景：**
    *   进入一个新行业前的尽职调查（Due Diligence）。
    *   撰写需要高度事实准确性的技术白皮书或学术论文。
*   **👥 适合人员：** 行业研究员、投资经理、策划人员、专栏作者。
*   **🔗 URL:** https://github.com/anthropics/skills/tree/main/skills/research-assistant

#### **9. Linear/Jira Ticket Manager (任务管理)**

*   **📝 简介：** 需求转化专家。能将模糊的口头需求拆解为结构化的开发工单，自动补全验收标准（AC）和技术细节。
*   **🎯 适合场景：**
    *   产品需求评审会后，快速将会议记录转化为 Jira/Linear 任务。
    *   帮助非技术背景的 PM 撰写工程师能看懂的需求文档。
*   **👥 适合人员：** 产品经理 (PM)、项目经理、Scrum Master。
*   **🔗 URL:** https://agentskills.io/skills/linear-integration

#### **10. Brand Voice Guard (品牌语调守门员)**

*   **📝 简介：** 内容合规与润色专家。基于企业 Tone of Voice 指南，自动审核并改写文案，确保对外发声风格统一。
*   **🎯 适合场景：**
    *   社交媒体（小红书/Twitter）文案的批量生成与风格统一。
    *   客服邮件回复的语气检查，防止因为语气生硬导致投诉。
*   **👥 适合人员：** 社交媒体运营、市场营销、公关 (PR)、客服主管。
*   **🔗 URL:** https://agentskills.io/skills/brand-voice-guard

### 怎么用这些 Skills

安装 Skill 的方法很简单：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/5EZ1TshXkh5xG9WntZJeZSrJGxBL4Z353WA9aibpSqARlPCXBRabmsib8ag5bb5sEYIiar9WsZyQ0XHfiayKM11jbg/640?wx_fmt=jpeg&from=appmsg "null")

1.  **Claude Code / Codex 用户**: 把 Skill 文件夹放到 `~/.claude/skills/` 或 `~/.codex/skills/` 目录下。
2.  **Gemini CLI 用户**: 放到 `~/.gemini/skills/` 目录下。

安装后，当你的请求匹配到某个 Skill 的场景时，AI 会自动调用它。

而且现在 Claude Code 已经支持 Skill 的热重载了，不用每次修改或增加 Skill 都重启一次，这个点还是相当爽的，相信后面 Codex 和 Gemini 一定会跟进。

### 注意点

Agent Skills 虽好，但也不要贪杯。前不久报道出来的黑客利用 Skill 后面进行攻击的例子，永远记住人红是非多，人多的地方一定有隐藏的危机值得你警惕。Agent Skills 是现在的 AI 界的当红炸子鸡，一定会被黑客盯上并利用，所以你下载 Skill 最好是选择权威与开源的站点进行下载。

### 我的建议

如果你刚开始接触 Agent Skills，推荐先试试这三个：

1.  **Docx / PDF / XLSX**（文档三件套）——日常办公刚需。
2.  **Git PR Reviewer**——如果你是开发者，这个能省很多时间。
3.  **Brand Voice Guard**——如果你负责内容输出，这个能保持一致性。

如果你想自己开发 Skill，从 **Skill Creator** 开始，参考格式把自己的工作流固化进去。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/5EZ1TshXkh5xG9WntZJeZSrJGxBL4Z35dX7pQIiauRswM4BagYC2YSaMKbUWyZeeOGiaOmqdTFfCpTDxAaiaoTgFg/640?wx_fmt=jpeg&from=appmsg "null")

你最想用哪个 Skill？或你正在使用哪些 Skill 呢？评论区聊聊。

我是 AIGC 胶囊，谢谢你读我的文章。
如果觉得不错，随手点个赞、在看、转发三连吧🙂
如果想第一时间收到推送，也可以给我个星标⭐

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/u5cgGk52w-2AbCS_5vZwtg)*