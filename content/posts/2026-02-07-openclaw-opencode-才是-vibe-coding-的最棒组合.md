---
title: "Openclaw + OpenCode 才是 vibe coding 的最棒组合！"
date: 2026-02-07T00:29:09+08:00
lastmod: 2026-02-07T00:29:09+08:00
author: "苍何"
categories: ["未分类"]
---

**作者**: 苍何

这是苍何的第 485 篇原创！大家好，我是苍何。

兄弟们，真的炸裂。

我真的实现了躺在床上指挥 AI Agent 来 Coding，并自动发布到 GitHub ，然后自动部署到Vercel。

用 Openclaw+ OpenCode+GitHub+Vercel 实现了网站的开发，部署上线。

这个过程全程是由 Openclaw 在我的私人服务器完成的。

这已经不是 vibe coding 了，我大胆的来造一个新名词吧，姑且就叫 Agent Coding。

也许后面，人们会有更加炫酷的名字，但这一切都不重要了。

我很兴奋，为了防止你说我在瞎扯淡，我决定公布所有我和 Openclaw 的聊天记录。

我全程并没有使用什么高深的技术，也没有操作过服务器，我全程是用最简单的提示词来完成的。

这个项目是Openclaw全自主完成的：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVO8IgRALviaiaG2EBrqiatjWapALnYlEmPfBkbSPWq8d81ABiag8AOLQFeA/640?wx_fmt=png&from=appmsg)游戏完全可用：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dV6yabdfia3BktBVRX2dFosuYvSbUmnXT9pichFFicQbRx98LyiasHHrDtTQ/640?wx_fmt=png&from=appmsg)下面是我和 Openclaw 的全部聊天。

先安装 opencode：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVKhEic96LibHBibD821Kz0bUNFDPgeuFDk6FJAFvMibQQZFK2dCT8yCjaibA/640?from=appmsg)新建目录用做项目目录：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVJGmW0IbkZVMB1FzNaxJWFKx1lmcNqmslHmSNpv6tnBnericw2XaMT1w/640?from=appmsg)切换目录，启动 opencode：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVHerVeBTjmw2r4wp022q6DwAjibxmOPFA2ptT8OLKQ8N4CBicONxR9BAA/640?from=appmsg)用 opencode 来开发贪吃蛇游戏：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVgEztF7pzKhcIswyNTkld0dKG3gC1aBW4iaZWqicFia7KbVN5dic3pZeB4g/640?from=appmsg)提供我的 GitHub 信息，让他连：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVPkYgpaSj7VjQMMKnkBe8JQtMFU9WnFwWlIC1ZB7kjE1QiayRN5nc8fw/640?from=appmsg)按照它给的提示，创建一个 token，权限就给仓库权限，直接丢给他 token。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVFGMWBaa25rhib8xicMYE8lZJCAKltwbAapicK1u9UiaqOBxQ04ytqzibAAw/640?from=appmsg)
> 这里一定记得开启部分权限，防止它瞎搞。
> 
> 

它说已经推送好了：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dV7cHKQnzAhyMkKiaxEWsOSMT2icFzoic3oXkyltQuDiaGfXxBuuDPc27s5Q/640?from=appmsg)我打开 GitHub 看下，果然有了，已经自动将代码推送到 GitHub 了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVSxwKtk8H5MLLQR4cJjYZFdnGIwicAGNURcsjf69a5O1PIAwzFOv5qxg/640?from=appmsg)然后让它部署到Vercel，方便得到一个可访问的网页链接：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVCq7ZqmcfdW373cvGk3gjtaVSJ3HdoYJlWt9LdQz0TO2GrknxoXkCyw/640?from=appmsg)同样按照要求，给个 token，就已经完成了自动部署。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVkDWzzyThtKzJKPWxp28mHdhFXfrbxI6QO1Xribd0GFS2K7ibN6fSpzlQ/640?from=appmsg)🐂🍺，就已经完成了全链路的自动化，真的麻了，兄弟们，虽然只是跑通了闭环，但Openclaw 想象空间真的无限。

我甚至直接让但 Openclaw 记录下这个过程，并写一篇文章，推送到刚才这个仓库，这个由 Agent 自主开发部署的仓库。

提示词；这个过程太棒了，我打算写一篇文章，你帮我直接根据你刚才的步骤，生成一篇文章，标题是：用 Openclaw+ OpenCode+GitHub+Vercel 实现 Agent Coding，最好是有流程图详细解释下这个步骤

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVCQ6TEyVXgaSWdPiakeuBo7ibFw077ThLWe1RyjNnXnOXhRx5qQWuhpXw/640?from=appmsg)然后打开 GitHub 看，也已经有了描述：

![](https://mmbiz.qpic.cn/sz_mmbiz_png/y9icg8hcXLYvphl04YrHDwl9CrZbAq0dVLAA26bqA3YicSRMUr4j9ibxSVAI1KvL6Z0Kv2eLGV0oI6hUQPuuzcdMg/640?from=appmsg)下面，我把 Openclaw 生成的教程也贴出来，方便大家看看。Openclaw 的应用仿佛打开了潘多拉魔盒，未来，coding 的范式是不是可以变为 agent coding，每一个人都有一个专属 agent，帮我们 coding，或者做任何我们希望做的事情。



---

# 🐍 贪吃蛇游戏 + Agent Coding 完整教程


> 本文档由 **「OpenClaw AI Agent」** 全程自动生成，记录从需求到上线的完整开发流程。
> 
> 

📱 **「在线试玩」**: https://myopencode.vercel.app  
📝 **「项目源码」**: https://github.com/freestylefly/snake-game  
🤖 **「生成工具」**: OpenClaw + OpenCode + GitHub + Vercel



---

# 用 OpenClaw + OpenCode + GitHub + Vercel 实现 Agent Coding


> 从零开始，让 AI Agent 帮你写代码、管理版本、自动部署，全程无需离开终端！
> 
> 

## 📋 概述

本文将介绍如何构建一个完整的 **「AI 驱动开发工作流」**：

* **「OpenClaw」** - AI 助手运行平台，协调所有工具
* **「OpenCode」** - AI 编程助手，自动生成代码
* **「GitHub」** - 代码托管和版本管理
* **「Vercel」** - 自动化部署和托管

通过这个工作流，你只需要告诉 AI 要做什么，剩下的代码编写、提交、部署全部由 Agent 自动完成。



---

## 🔄 完整流程图


```
┌─────────────────────────────────────────────────────────────────────────────┐│  AgentCoding完整工作流 │└─────────────────────────────────────────────────────────────────────────────┘  
     ┌──────────────┐     │   用户需求    │  "帮我创建一个贪吃蛇游戏并部署上线"     └──────┬───────┘            │            ▼┌──────────────────────────────────────────────────────────────────┐│  Step1:环境准备(OpenClaw协调) ││  ┌─────────────┐┌─────────────┐┌─────────────┐ ││  │安装OpenCode││安装GitHubCLI││安装VercelCLI│ ││  │(AI编程)││(代码托管)││(自动部署)│ ││  └──────┬──────┘└──────┬──────┘└──────┬──────┘ │└─────────┼────────────────┼────────────────┼──────────────────────┘   ││ │   ▼▼ ▼┌──────────────────────────────────────────────────────────────────┐│  Step2:AgentCoding(OpenCode) ││  ┌─────────────────────────────────────────────────────────┐     ││  │用户:"创建一个贪吃蛇游戏"│ ││  │││ ││  │▼│ ││  │  ┌─────────────────────────────────────────────────┐    │     ││  ││OpenCodeAIAgent││ ││  ││┌──────────┐┌──────────┐┌──────────┐││ ││  │││生成HTML││生成CSS││生成JS│││ ││  │││index.html││style.css││game.js│││ ││  ││└──────────┘└──────────┘└──────────┘││ ││  │  └─────────────────────────────────────────────────┘    │     ││  └─────────────────────────────────────────────────────────┘     │└──────────────────────────────────────────────────────────────────┘          │          ▼┌──────────────────────────────────────────────────────────────────┐│  Step3:代码管理(GitHub) ││  ┌──────────────────────────────────────────────────────────┐    ││  │1.gitinit初始化仓库│ ││  │2.gitadd.添加文件│ ││  │3.gitcommit-m"Initial commit"提交│ ││  │4.创建GitHub仓库(通过API)│ ││  │5.gitpush-uoriginmaster推送到远程│ ││  └──────────────────────────────────────────────────────────┘    │└──────────────────────────────────────────────────────────────────┘          │          ▼┌──────────────────────────────────────────────────────────────────┐│  Step4:自动部署(Vercel) ││  ┌──────────────────────────────────────────────────────────┐    ││  │1.vercel--token<TOKEN>登录并关联│ ││  │2.自动检测项目类型(静态网站)│ ││  │3.构建并上传到VercelCDN│ ││  │  4. 分配域名: https://myopencode.vercel.app  │ ││  └──────────────────────────────────────────────────────────┘    │└──────────────────────────────────────────────────────────────────┘          │          ▼     ┌──────────────┐     │   网站上线    │  🎉 访问链接，游戏可玩！     └──────────────┘
```


---

## 🛠️ 详细步骤

### 第一步：环境准备

#### 1.1 安装 OpenCode（AI 编程助手）


```
# 安装 OpenCodenpm install -g opencode-ai  
# 验证安装opencode --version
```
#### 1.2 安装 GitHub CLI（代码管理）


```
# 下载并安装curl -fsSL https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_linux_amd64.tar.gz | tar -xz -C /tmpcp /tmp/gh_2.63.2_linux_amd64/bin/gh /usr/local/bin/  
# 验证gh --version
```
#### 1.3 安装 Vercel CLI（自动部署）


```
# 安装 Vercel CLInpm install -g vercel  
# 验证vercel --version
```


---

### 第二步：创建项目目录


```
# 创建项目目录mkdir -p ~/myopencodecd ~/myopencode  
# 初始化 Git 仓库git init  
# 配置 Git 用户信息git config --global user.email "your@email.com"git config --global user.name "yourname"
```


---

### 第三步：Agent Coding（核心步骤）

#### 方式一：使用 OpenCode 交互模式


```
# 启动 OpenCode（需要 PTY 模式）# 在 OpenClaw 中使用：bash pty:true workdir:~/myopencode command:"opencode"
```
然后在 OpenCode 中输入：


```
创建一个贪吃蛇游戏，使用 HTML5 Canvas，包含完整的游戏逻辑、得分系统和响应式设计
```
#### 方式二：使用 OpenCode 非交互模式


```
# 直接运行任务opencode run "Create a complete Snake game using HTML5 Canvas, CSS, and JavaScript"
```
#### 方式三：手动创建（备用方案）

如果 OpenCode 运行有问题，可以直接创建文件：

**「index. html:」**


```
<!DOCTYPE html><html lang="zh-CN"><head>    <meta charset="UTF-8">    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <title>贪吃蛇游戏</title>    <link rel="stylesheet" href="style.css"></head><body>    <div class="container">        <h1>🐍 贪吃蛇游戏</h1>        <div class="game-info">            <div class="score">得分: <span id="score">0</span></div>            <div class="high-score">最高分: <span id="highScore">0</span></div>        </div>        <canvas id="gameCanvas" width="400" height="400"></canvas>        <div class="controls">            <p>使用方向键 ↑↓←→ 控制蛇的移动</p>            <button id="startBtn">开始游戏</button>            <button id="pauseBtn">暂停</button>            <button id="restartBtn">重新开始</button>        </div>        <div id="gameOver" class="game-over hidden">            <h2>游戏结束!</h2>            <p>最终得分: <span id="finalScore">0</span></p>            <button id="playAgainBtn">再玩一次</button>        </div>    </div>    <script src="game.js"></script></body></html>
```
**「style. css:」**


```
\* {    margin: 0;    padding: 0;    box-sizing: border-box;}  
body {    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);    min-height: 100vh;    display: flex;    justify-content: center;    align-items: center;    color: #fff;}  
.container {    text-align: center;    padding: 20px;    background: rgba(255, 255, 255, 0.05);    border-radius: 20px;    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);}  
h1 {    background: linear-gradient(45deg, #00d4aa, #00a8e8);    -webkit-background-clip: text;    -webkit-text-fill-color: transparent;}  
#gameCanvas {    border: 3px solid #00d4aa;    border-radius: 10px;    background: #0a0a0a;}
```
**「game. js:」** (完整游戏逻辑代码)



---

### 第四步：推送到 GitHub

#### 4.1 提交代码


```
# 添加所有文件git add .  
# 提交git commit -m "Initial commit: Snake game with HTML5 Canvas"
```
#### 4.2 创建 GitHub 仓库并推送

**「方式一：使用 GitHub CLI」**


```
# 登录 GitHubecho "YOUR_GITHUB_TOKEN" | gh auth login --with-token  
# 创建仓库gh repo create snake-game --public --description "A classic Snake game"  
# 推送git push -u origin master
```
**「方式二：使用 API 直接创建」**


```
# 通过 API 创建仓库curl -X POST https://api.github.com/user/repos \  -H "Authorization: token YOUR_GITHUB_TOKEN" \  -H "Accept: application/vnd.github.v3+json" \  -d '{    "name": "snake-game",    "description": "A classic Snake game built with HTML5 Canvas",    "private": false  }'  
# 添加远程仓库并推送git remote add origin https://username:token@github.com/username/snake-game.gitgit push -u origin master
```


---

### 第五步：部署到 Vercel

#### 5.1 使用 Vercel CLI 部署


```
# 进入项目目录cd ~/myopencode  
# 使用 token 部署vercel --token YOUR_VERCEL_TOKEN --yes --prod
```
部署成功后，会输出类似：


```
Production: https://myopencode-xxx.vercel.app
```
#### 5.2 关联 GitHub 仓库（可选）

Vercel CLI 会自动检测并关联 GitHub 仓库，实现自动部署：

* 每次 push 到 GitHub，Vercel 自动重新部署
* 支持预览部署（Pull Request）



---

## 🎯 完整命令速查表



| 步骤 | 命令 |
| --- | --- |
| **「安装工具」** | `npm install -g opencode-ai vercel` |
| **「创建目录」** | `mkdir myopencode && cd myopencode && git init` |
| **「Agent 编程」** | `opencode run "创建贪吃蛇游戏"` |
| **「提交代码」** | `git add . && git commit -m "init"` |
| **「创建仓库」** | `gh repo create snake-game --public` |
| **「推送代码」** | `git push -u origin master` |
| **「部署」** | `vercel --token TOKEN --yes` |



---

## 💡 核心优势

### 1. **「全程自动化」**

* 从需求到上线，无需手动编写代码
* AI Agent 理解自然语言，自动生成完整项目

### 2. **「无缝集成」**

* OpenClaw 作为中控，协调所有工具
* GitHub 管理版本，Vercel 自动部署

### 3. **「即时反馈」**

* 几分钟内从想法到可访问的网站
* 每次修改自动重新部署

### 4. **「可扩展性」**

* 可以轻松扩展到更复杂的项目
* 支持 React、Vue、Next. js 等框架



---

## 🔧 常见问题

### Q 1: OpenCode 卡住不响应？

**「解决」**: 使用非交互模式或直接用 GPT/Claude 生成代码后手动保存

### Q 2: GitHub 推送失败？

**「解决」**: 检查 token 权限，需要 `repo` 权限

### Q 3: Vercel 部署失败？

**「解决」**: 确保项目结构正确，静态网站不需要额外构建配置



---

## 🚀 进阶玩法

### 自动评论到 PR


```
# OpenCode 审查代码后自动评论gh pr comment <PR_NUMBER> --body "$(cat review.md)"
```
### 定时自动更新


```
# 使用 cron 定时让 AI 更新网站内容cron action:add job:{  "schedule": {"kind": "cron", "expr": "0 9 \* \* 1"},  "payload": {"kind": "agentTurn", "message": "更新网站内容"}}
```
### 多 Agent 协作


```
# 同时运行多个 OpenCode 处理不同任务bash pty:true background:true command:"opencode '设计前端界面'"bash pty:true background:true command:"opencode '编写后端 API'"
```


---

## 📊 实际案例数据

本次贪吃蛇项目：

* **「开发时间」**: ~5 分钟（Agent 生成代码）
* **「代码行数」**: ~400 行（HTML/CSS/JS）
* **「部署时间」**: < 10 秒
* **「最终链接」**: https://myopencode.vercel.app



---

## 📝 总结

通过 **「OpenClaw + OpenCode + GitHub + Vercel」** 的组合，我们实现了一个完整的 AI 驱动开发工作流：

1. **「说」** - 告诉 AI 你要什么
2. **「写」** - AI 自动生成代码
3. **「存」** - 自动提交到 GitHub
4. **「上线」** - 一键部署到 Vercel

这种工作流特别适合：

* 快速原型开发
* 个人项目
* 学习新技术
* 自动化重复任务



---

## 🔗 相关链接

* OpenClaw: https://docs.openclaw.ai
* OpenCode: https://opencode.ai
* GitHub: https://github.com
* Vercel: https://vercel.com
* 本案例 GitHub 仓库: https://github.com/freestylefly/snake-game
* 在线演示: https://myopencode.vercel.app



---

## 🤖 OpenClaw 生成过程实录

本文档并非人工编写，而是由 **「OpenClaw AI Agent」** 在开发过程中自动生成：

### 生成流程

1. **「需求提出」** - 用户："帮我把整个过程写成一篇文章"
2. **「Agent 分析」** - OpenClaw 分析刚才的操作历史，提取关键步骤
3. **「内容生成」** - 自动编写完整教程，包含流程图、代码示例、速查表
4. **「自动推送」** - Agent 直接将 README 提交到 GitHub 仓库

### 真实的开发时间线


```
21:49 - 用户："帮我安装 opencode"21:53 - 创建项目目录 myopencode21:56 - 启动 opencode（交互模式）21:57 - OpenCode 卡住，改用直接创建文件21:58 - 贪吃蛇游戏代码生成完成22:05 - 用户提供 GitHub 账号 freestylefly22:10 - 创建 GitHub 仓库并推送代码22:13 - 用户要求部署到 Vercel22:20 - Vercel 部署成功，游戏上线22:28 - 用户："写一篇文章记录这个过程"22:31 - README 自动生成并推送到 GitHub
```
### 核心指令

整个开发过程只用了几个简单的自然语言指令：



| 时间 | 用户指令 | Agent 动作 |
| --- | --- | --- |
| 21:49 | "帮我安装 opencode" | 安装 OpenCode CLI |
| 21:53 | "帮我新建一个目录 myopencode" | 创建目录并初始化 git |
| 21:56 | "启动 opencode" | 运行交互式编程助手 |
| 22:05 | "https://github.com/freestylefly" | 配置 GitHub 连接 |
| 22:13 | "帮我部署到 vercel" | 安装 Vercel CLI 并部署 |
| 22:28 | "帮我写一篇文章..." | 生成完整教程文档 |
| 22:31 | "推送到刚才贪吃蛇仓库作为 readme" | 自动提交 README |

**「全程无需编写任何命令，只需用自然语言描述需求！」**



---

*本文档由 OpenClaw AI Agent 全程自动生成 | 2026-02-03*

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/U3PHOYSAaTFRwl77--YaAA)*
