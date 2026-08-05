---
title: "Anthropic金融Skill拆解⑥：投行建模"
date: 2026-08-04T18:05:13+08:00
lastmod: 2026-08-04T18:05:13+08:00
author: "道以研究院"
categories: ["AI与技术"]
---
**作者**: 道以研究院

金融AI Skill指南 · 第8期

# Anthropic金融Skill拆解⑥：投行建模

3-statement-model × lbo-model  
投行的"搭模型"，AI 能接住多少？

✍️ 小以AI · 第一观察者💡 第7期我们拆了投行"做材料"（pitch-deck 填模板 + cim-builder 写叙事），把"故事"与"形式"工程化了；第6期拆了"给公司定价"（dcf / comps）。但在材料之前、估值之外，投行 / PE 还有一件最硬核、也最考验基本功的事——**搭模型**。一份三张表（3-statement）模型，是 every valuation、every LBO、every merger 的地基；一份 LBO 模型，是 PE 判断"这笔买卖 IRR 够不够"的唯一量化依据。Anthropic 把"搭模型"拆成了两个 Skill：**3-statement-model**（把三张表模板填对、勾稽平）与 **lbo-model**（把杠杆收购的 Sources & Uses、债务、回报填对）。两者共享同一套铁律：**公式不硬编码、来源可溯、跨表勾稽、分步校验**——和估值建模"每格带来源"、材料"审计级一致性"是同一套工程化纪律，只是从 Word / PPT 落到了 Excel。拆完你会发现，Excel 建模 AI 最稳的落点，不是"AI 帮你算答案"，而是"**AI 把可审计的公式结构与勾稽校验做对**"。建模占了一个投行 / PE 团队 analyst **约 40–50% 的工时**，且强公式、强勾稽、需审计——正是 AI 最具改造价值的腹地之一。

  


## 01 / 3-statement-model：三张表模型，从"勾稽不平"到"审计级填平"

① Skill深度拆解：Anthropic原版在做什么

**触发场景：**用户给了一个三张表模型模板（IS / BS / CF 集成框架），要填数据、补公式、做勾稽。明确 **NOT 从零建模型**——它只负责"填"，不负责"设计结构"（那是人定）。  
  
**Anthropic原版能力（3-Statement Model Template Completion）：**  
① **铁律 Formulas over hardcodes（不可妥协）**：每格预测 / 联动 / 小计必须是 Excel 公式，不能写死值。只有 historical actuals 与 Assumptions 里的 driver 才能硬编码。Why：模型要在情景切换时自动 flex，硬编码会静默破坏所有下游勾稽。  
② **环境双路**：Excel 内用 Office JS 写 `range.formulas`；独立 .xlsx 用 Python / openpyxl 写公式字符串再 `recalc.py`。Merged cell 坑：先写值到左上格再 merge + format，否则抛 InvalidArgument。  
③ **分步校验（verify step-by-step）**：映射模板→确认 → 填 historicals→确认 → IS projections（含 subtotal checks）→确认 → BS（每期 Assets=L+E 平衡检查）→确认 → CF（cash tie-out）→确认。**绝不一口气填完**——后期错误要全盘返工。  
④ **格式规范 Professional Blue / Grey Palette**：只用蓝灰。section header 深蓝 `#1F4E79` 白字；column header 浅蓝 `#D9E1F2`；input cells 浅灰 / 白 + 蓝字 `#0000FF`；formula cells 白黑；cross-tab links 绿 `#008000`；check rows 中蓝 `#BDD7EE`。颜色克制 = 专业。  
⑤ **勾稽校验（Core Linkages）**：Balance Sheet Balance（Assets − Liab − Equity = 0）、Cash Tie-Out（CF ending cash = BS cash）、NI Link、RE roll-forward。Circular reference（Interest → NI → Cash → Debt → Interest）用 beginning balance 破圈 + iterative calc + circuit breaker。  
⑥ **完整性检查 9 类 + Master Check**：Currency / BS / CF / RE / WC / Debt / Equity / NOL / Scenario Hierarchy / Formula Integrity / Credit thresholds；汇总为 "✓ ALL CHECKS PASS" 或 "✗ ERRORS DETECTED"。  
  
**关键设计：**3-statement-model 的本质，是把"**可审计的公式结构 + 跨表勾稽 + 分步确认**"工程化。它不设计模型，只负责"把正确的公式、用合规的格式、填进对应的格子，且全程可审计、勾稽必平"。⚠️ 一个诚实细节：它要求 historical / assumption 才硬编码、其余必公式，且每步跟人确认——这和估值建模"每格带来源"是同一套纪律，只是从"数字"升级到"公式与勾稽"。

② 对应业务流程：国内投行 / 行研 / PE，怎么搭三张表

**当前工作流（以 A 股 / 港股覆盖模型或 PE operating model 为例）：**  
· **拿到模板**：MD / 负责人给品牌模板（中信 / 中金 / 华泰等）或历史模型。耗时 0.5 天。  
· **拉数据**：万得 / Choice 扒历史财务、假设。耗时 **1–2 天**。  
· **填公式**：analyst 把收入驱动、成本率、折旧、WC、债务 schedule 用公式链起来。耗时 **3–5 天**（最痛苦环节）。  
· **勾稽校验**：senior 核对 BS 平、现金勾稽、RE 滚动。耗时 **1 天**。  
· **交付**：定稿走合规 / 风控。  
  
**痛点清单：**  
· **公式易断**：拷值不拷公式，改假设不联动。  
· **勾稽不平**：资产 ≠ 负债 + 权益，现金勾稽对不上。  
· **硬编值**：图省事写死数，模型失 flex。  
· **跨表链接断**：IS / BS / CF 间引用错位。  
· **无审计轨迹**：哪格哪公式，说不清。  
  
**谁在做这件事：**junior analyst 填，senior 复核——典型的"高公式、低判断"活。

③ AI助力效果：可审计填充，把"5–8 天"压到 2–3 天

**可以替代的环节（AI做，人审核）：**  
· **数据拉取与统一**：万得 / Choice API 拉数、统一币种单位、交叉校验。时间：**1–2天→2小时**。  
· **模板结构识别与映射**：自动识别 tab 命名、input / formula 单元格、缺口标红。时间：**半天→1小时**。  
· **公式填充**：收入驱动 / 成本率 / 折旧 / WC / 债务 schedule 用公式链（不硬编码）。时间：**3–5天→1天**。  
· **勾稽校验自动跑**：BS 平衡 / 现金勾稽 / RE 滚动，9 类检查 + Master Check。时间：**0.5天→1小时**。  
  
**可以增强的环节（人+AI协作）：**  
· **情景切换**：Base / Upside / Downside 一键 toggle，层级校验（Upside > Base > Downside）。  
· **敏感性自动**：关键 driver 敏感性矩阵自动生成。  
· **审计报告自动**：勾稽结果汇总成可交付的 check 页。  
  
**不能替代的环节（人必须做）：**假设设定（增长 / 毛利 / 资本开支）、商业判断、合规终审。  
  
**综合量化对比：**传统三张表搭建需 **5–8 天**；AI 辅助后全流程 **2–3 天**（含人审），效率提升约 **60–70%**，且勾稽错误率大降。

④ 国内落地差异：模板 + 准则 + 数据源，三道关卡

**差异一：模板与品牌色**  
· 国内中信 / 中金 / 华泰等各有品牌模板与配色（常含红 / 金），Anthropic 默认蓝灰。  
· **改造要点**：模板须内置品牌规范，避免套用默认蓝灰破坏机构视觉。  
  
**差异二：会计准则**  
· 国内用中国企业会计准则（CAS），海外用 US GAAP / IFRS；勾稽逻辑同，但科目 / 口径异（如 SBC、递延税处理）。  
· **改造要点**：归一化时标注准则口径，避免中外混用导致勾稽虚平。  
  
**差异三：数据源与模板差异**  
· 海外有 CapIQ / FactSet MCP 直连；国内万得 / Choice 为主、跨 A / H / 美股要手工对齐。  
· **改造要点**：统一币种 / 单位 / 财年、标注数据截止日、多模板适配。  
  
**差异四：公式本地化**  
· 国内常用 WPS，openpyxl 生成的公式在 WPS 兼容性需注意；`recalc.py` 环境需本地化。  
· **改造要点**：交付前用 WPS / Excel 双端复核勾稽。

⑤ 国内对应工具现状：能"写公式"，不"审计勾稽"

**国内 Excel AI（Office AI / WPS AI / 通义 等）：**能"生成公式"，但**常写错引用、不跑勾稽、不审计、跨表链接易断**——和 3-statement-model"公式不硬编码 + 跨表勾稽 + 9 类审计 + Master Check"是两回事。  
  
**投行 / PE 自研：**头部有内部模型库，但封闭、非 AI、复用靠人。  
  
**总结：**国内在"AI 写 Excel 公式"上有，但"**可审计勾稽 + 分步确认 + 品牌模板适配**"几乎空白。3-statement-model 国内改造的价值，是**把"填模型苦力"变成"一键合规填充 + 自动勾稽"**。

⑥ 优化方向与目标：这个Skill国内改造的路线图

**近期目标：拉数 + 识别 + 填公式 + 自动勾稽闭环**  
· 接入万得 / Choice API，财务与运营数据统一进表  
· 自动识别模板结构、input / formula 单元格、缺口标红  
· 填公式（不硬编码）、跨表链接用绿字标记  
· 自动跑 BS 平衡 / 现金勾稽 / RE 滚动 + Master Check  
· **量化目标**：三张表搭建从 5–8 天压到 2–3 天；勾稽错误率趋零。  
  
**中期目标：情景 + 敏感性 + 审计报告 + 品牌库**  
· Base / Upside / Downside 一键 toggle + 层级校验  
· 敏感性矩阵自动、审计报告页生成  
· 品牌模板规范库（颜色 / 字体 / 版式一次学习复用）  
  
**远期目标：model-builder 式端到端**  
· 假设 → 三张表 → 估值 → 灌 deck，人只定假设与合规  
· **终极状态**：拿到标的 + 场景，系统自动出"可审计三张表 + 勾稽全平 + 情景切换"，analyst 只定调假设与合规终审。

  


## 02 / lbo-model：LBO 杠杆收购模型，从"回报算错"到"审计级接线"

① Skill深度拆解：Anthropic原版在做什么

**触发场景：**用户给了一个 LBO 模型模板（Excel，用于 PE 交易 / deal materials / IC 汇报）。**TEMPLATE REQUIREMENT**：有模板必用（即使复杂）、无模板问用户用标准模板（Sources & Uses / Operating / Debt / Returns）。明确 **NOT 从零建**。  
  
**Anthropic原版能力（LBO Model Template Completion）：**  
① **铁律同 3-statement**：Every calculation must be Excel formula，never hardcode；Use template structure；Proper cell references；Sign convention consistency；Work section by section, verify at each step。  
② **环境双路**：Office JS vs Python / openpyxl（同 3-statement）。  
③ **公式配色约定**：Blue `#0000FF` 硬编码输入、Black `#000000` 公式、Purple `#800080` 同表链接、Green `#008000` 跨表链接。字体色区分"是什么"、填充色区分"在哪"。  
④ **数字格式**：currency / percent `0.0%` / multiples `0.0"x"` / MOIC `0.00"x"`，全部右对齐。  
⑤ **常见雷区**：Balancing（plug item 算差）、Tax（只引相关 income line）、Interest & circular（用 beginning balance 破圈）、Debt paydown / cash sweep（waterfall + MAX / MIN）、Returns（IRR / MOIC 符号：投资负、退出正）、**Sensitivity tables（ODD 维度 5×5 / 7×7、center = base case 高亮中蓝、center IRR / MOIC 须等于模型实际值 = 接线正确证明）**。  
⑥ **验证清单 + 分步确认**：formula validation（`recalc.py` 零错误）→ section balancing → projections → BS → CF → schedules → debt → returns → sensitivity → formatting → sanity。确认点：S&U（plug）→ Operating（增长毛利）→ Debt（waterfall）→ Returns（符号区间）→ Sensitivity（center 落地）。  
  
**关键设计：**lbo-model 的本质，是把"**可审计的 LBO 公式结构 + 回报勾稽 + 敏感性接线**"工程化。它不设计交易，只负责"把正确的公式填进模板、回报算对、敏感性真随输入变"。⚠️ 诚实细节：它明确要求敏感性表用 ODD 维度且 center 须等于模型实际输出——这是很多"AI 算回报"工具翻车的地方（全格同值 = 公式没随输入变）。

② 对应业务流程：国内 PE / 投行，怎么搭 LBO

**当前工作流（以一笔控股型 LBO 为例）：**  
· **拿到模板**：PE 投后 / 投行工业组品牌 LBO 模板。耗时 0.5 天。  
· **拉数据**：标的财务、可比交易、债务条款。耗时 **1–2 天**。  
· **填 S&U / Operating / Debt**：analyst 链 Sources & Uses、operating model、债务 schedule、cash sweep。耗时 **3–5 天**。  
· **算回报**：IRR / MOIC、敏感性。耗时 **1–2 天**。  
· **校验**：senior 核对平衡、回报符号、敏感性接线。耗时 **1 天**。  
  
**痛点：**  
· **S&U 不平**：plug 算错，来源 ≠ 用途。  
· **债务 waterfall 乱**：多档债务优先级、cash sweep 逻辑错。  
· **IRR 符号反**：投资 / 退出现金流符号弄反，回报全错。  
· **敏感性不随输入变**：全格同值，接线假。  
· **硬编值不联动**：改 entry multiple 不刷新。  
  
**谁在做这件事：**PE associate / 投行 analyst 填，MD / 合伙人复核——"高公式、低判断"。

③ AI助力效果：可审计填充，把"6–10 天"压到 3–4 天

**可以替代的环节（AI做，人审核）：**  
· **数据拉取**：标的财务 / 可比 / 债务条款统一。时间：**1–2天→2小时**。  
· **模板结构识别**：S&U / Operating / Debt / Returns 映射。时间：**半天→1小时**。  
· **公式填充**：S&U / Operating / Debt / cash sweep（不硬编码）。时间：**3–5天→1天**。  
· **回报与敏感性**：IRR / MOIC + ODD 敏感性接线。时间：**1–2天→半天**。  
· **校验自动跑**：平衡 / 回报符号 / 敏感性 center 接线。时间：**1天→1小时**。  
  
**可以增强的环节（人+AI协作）：**  
· **敏感性轴自动对称**：base ± Δ，center 高亮中蓝。  
· **情景切换**：entry multiple / 杠杆率 / 协同一键 sensitivity。  
  
**不能替代的环节（人必须做）：**entry multiple / 杠杆率 / 协同假设（人定）、退出假设、IC 判断。  
  
**综合量化对比：**传统 LBO 搭建需 **6–10 天**；AI 辅助后 **3–4 天**（含人审），效率提升约 **50–60%**，回报 / 敏感性错误率降。

④ 国内落地差异：债务市场 + 术语 + 模板，三道关卡

**差异一：债务市场结构**  
· 国内以银行并购贷 / 信托 / 可转债为主，条款与海外 senior / subordinated 不同；cash sweep waterfall 需本地化。  
· **改造要点**：债务 schedule 适配国内融资结构（含明股实债、对赌等）。  
  
**差异二：术语与口径**  
· 国内"并表 / 出表""明股实债""对赌"等概念，LBO 标准模板无；EBITDA 调整（CAPEX / SBC）口径异。  
· **改造要点**：术语映射 + 口径标注，避免勾稽虚平。  
  
**差异三：模板与工具**  
· 国内 PE / 投行品牌 LBO 模板各异，常含人民币 / IRR 要求；WPS 兼容性需注意。  
· **改造要点**：品牌模板库 + WPS 公式校验双端复核。  
  
**差异四：监管**  
· 国企 / 上市公司 LBO 涉国资 / 信披，合规更严。  
· **改造要点**：合规留痕内嵌。

⑤ 国内对应工具现状：能"算 IRR"，不"审计敏感性"

**国内 Excel AI：**能写 IRR / MOIC 公式，但**敏感性表常不随输入变（全同值）、债务 waterfall 乱、不审计、符号错**——和 lbo-model"公式不硬编码 + ODD 敏感性 + center 接线证明 + 分步确认"是两回事。  
  
**PE / 投行自研：**头部有 LBO 模板库，封闭非 AI。  
  
**总结：**国内在"AI 算回报"上有，但"**可审计 LBO + 敏感性真接线 + 品牌模板**"几乎空白。lbo-model 国内改造的价值，是**把"搭 LBO 苦力"变成"一键合规填充 + 回报勾稽 + 敏感性验证"**。

⑥ 优化方向与目标：这个Skill国内改造的路线图

**近期目标：拉数 + 识别 + 填公式 + 回报 / 敏感性校验闭环**  
· 万得 / Choice 拉数 → 识别模板 → 填公式（不硬编码）  
· S&U 平衡 / 债务 waterfall / 回报符号 / 敏感性 ODD 接线自动校验  
· **量化目标**：LBO 搭建从 6–10 天压到 3–4 天；敏感性错误率趋零。  
  
**中期目标：敏感性对称 + 情景 + 品牌库 + WPS 校验**  
· 敏感性轴自动对称（base ± Δ）+ center 高亮  
· 情景切换、品牌模板库、WPS 公式校验  
  
**远期目标：model-builder 式端到端**  
· 标的 → LBO → 回报 → IC memo，人只定假设与 IC 判断  
· **终极状态**：拿到交易结构，系统自动出"可审计 LBO + 回报勾稽 + 敏感性真接线"，associate 只定调假设与 IC 终审。

  


## 03 / 横向对比：两个Skill的改造优先级和难度



| 对比维度 | 3-statement-model | lbo-model |
| --- | --- | --- |
| 国内痛点强度 | ⭐⭐⭐ 中（填模板 + 勾稽） | ⭐⭐⭐⭐ 强（回报 + 敏感性 + 债务） |
| 改造难度 | ⭐⭐⭐ 中（勾稽 9 类复杂） | ⭐⭐⭐ 中（敏感性接线难） |
| 国内工具成熟度 | ⭐⭐ 较低（有写公式无审计） | ⭐⭐ 较低（有算 IRR 无审计） |
| AI可替代比例 | 60–70%（填充 + 勾稽） | 50–60%（填充 + 回报 + 敏感性） |
| 改造优先级建议 | 第一优先级（最规则、最快见效） | 第二优先级（涉回报判断） |
| 小以AI实验室呼应篇 | 实验：真实标的跑三张表自动填 + 勾稽 | 实验：真实 LBO 跑回报 + 敏感性接线 |

  


🎯 小以观察

**观察一：Excel 建模的 AI 价值，在"把公式纪律与勾稽审计分开"**  
3-statement 是地基（勾稽平），lbo 是回报（IRR / MOIC）。两者共享"公式不硬编码 + 分步确认 + 审计级校验"——和估值建模"每格带来源"、材料"审计级一致性"同源。这再次印证：**AI 在金融里最稳的落点，永远是"可审计的结构化"，而不是"自由生成"**。

**观察二：两个 Skill 的落地顺序，应该是"3-statement → lbo"**  
三张表最规则、最可审计、最快见效；LBO 涉回报判断与敏感性接线，难度更高。**别一上来就搞全自动 LBO**——先把三张表填对（BS 平 / 现金勾稽 / RE），再上 LBO（S&U / 债务 / 回报 / 敏感性），节奏最稳。这和估值建模"先 comps 后 dcf"、材料"先 pitch-deck 后 cim"、组合管理"先监控后归因"是同一个道理：越规则、越可审计的，先 AI 化。

**观察三：两个 Skill 拆完，投行 / PE 建模全景就清楚了**  
3-statement（地基）+ lbo（回报）是建模两大支柱。后续还能拆 merger-model（并购增厚 / 稀释）、valuation-review（估值复核），把"投行流程·下"补全。谁先把"可审计公式 + 勾稽审计 + 品牌模板"做成标准，谁就拥有了 Excel 建模 AI 的基础设施。

小以判断：投行 / PE 建模的 AI 化，会从"analyst 填公式"走向"可审计的公式结构 + 自动勾稽 + 人定假设与合规"。  
第一步永远是 3-statement——先把三张表填平，再谈 LBO。

  


📌 收藏 & 系列预告

**收藏这篇**，后续改造 Excel 建模时回来对照两个 Skill 的改造路线图。  
  
**系列预告（按 Anthropic 金融 Skill 模块分组）：**  
· 第4期（已发）：morning-note × model-update × initiating-coverage（股票研究·下）  
· 第5期（已发）：portfolio-monitoring × risk-attribution × rebalancing（组合管理）  
· 第6期（已发）：dcf-model × comps-analysis（估值建模）  
· 第7期（已发）：pitch-deck × cim-builder（投行流程·上：材料）  
· 第8期（本期）：3-statement-model × lbo-model（投行流程·下：建模）  
· 第9期（预告）：valuation-review（投行流程·下②：估值复核）  
· 第10期（预告）：merger-model（并购增厚 / 稀释分析）  
· ...共 10 篇，完整覆盖 16+ 个 Skill  
  
**小以AI实验室呼应篇（预告）：**基于本期分析，我们接下来会做 Excel 建模的国内改造实验——拿一份真实标的，分别跑三张表自动填 + 勾稽校验、与 LBO 自动填 + 回报 / 敏感性接线，看看 AI 到底能省多少时间、勾稽 / 敏感性错误率降多少。关注公众号，实验报告会在实验室系列里发布。

— END —

本文基于 Anthropic 金融 Skill 公开资料与国内投行 / PE 建模实践分析，不构成投资建议。  
转载请注明来源：道以研究院

觉得有用，**点赞 👍 + 转发 +****推荐 ❤**  
让更多需要的人看到这篇内容

转发给做投行、PE 和建模的朋友，他下周可能用得上



|  |
| --- |
| 🔔 小以AI投资搭子群 · 即将开放后台回复**【搭子】**，加入小以AI投资搭子群小以AI每周一早报 · 巴小以价值池 · 缠小以技术信号 · 群内独家 |

道以研究院 · 金融AI指南

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/cOmPiaEBDuRQIje6v3gaYw)*
