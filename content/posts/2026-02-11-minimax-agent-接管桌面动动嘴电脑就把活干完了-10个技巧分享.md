---
title: "MiniMax Agent 接管桌面：动动嘴，电脑就把活干完了 | 10+个技巧分享"
date: 2026-02-11T00:08:45+08:00
lastmod: 2026-02-11T00:08:45+08:00
author: "AI进修生"
categories: ["未分类"]
---

**作者**: AI进修生

MiniMax Agent，很多人都知道。

它的桌面端是 Web 端的进化版—— 能控制浏览器、处理本地文件，还继承了网页端的所有能力：Code 执行、PPT 生成、Deep Research、多模态处理（视频生成等）、MCP生态集成等。  


![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FmWtDnsEvDPleEIjVahiaulQOEbpoicKDC78CtzX8c0RbyueHvibGRgvnIhSxibdepNd0blUI0jN1nHc9GBjibC69VI0qLtCx7SZOek/640?wx_fmt=png&from=appmsg)https://agent.minimaxi.com/ （Win、Mac双端可用）![]()

现在 AI 的使用方式正在发生变化。很多人不再满足于单纯的对话框，而是开始用能感知本地环境、自主拆解复杂任务、拥有专家级能力的 AI Agent。ClaudeCode、[Clawdbot](https://mp.weixin.qq.com/s?__biz=MzkyMzY1NTM0Mw==&mid=2247514097&idx=1&sn=26157cd1759079088d0f85e38cf471ca&scene=21#wechat_redirect)都如此。

不过有些人说网页端就是个玩具，以此来凸显他们玩 Claude Code 的上大分了。

倒也大可不必。

早在 Aider、 Cursor 的 agent 出来的时候，我们就在玩这些了—— 不止是写代码，还有更多可能性。

## **01 环境配置与脚本自动化**

不知道大家在玩 [ClawdBot](https://mp.weixin.qq.com/s?__biz=MzkyMzY1NTM0Mw==&mid=2247514097&idx=1&sn=26157cd1759079088d0f85e38cf471ca&scene=21#wechat_redirect)的时候有没有遇到配置 fetch 失败的情况？我在连接 GitHub Copilot 和 Gemini Cli或者 Antigravity 的时候就报错失败。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FnibcFp2xfSJTcYtfKHt6wEiaTrmOZy7p2MA8zA60aL5qKzVvWCWuHBaL5eVCuW14oPGwM4AYG3eEJAVIxcG2zb8vtSyPicNU8lNE/640?wx_fmt=png&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkBnhqxeBotglZ3VD5SpvPKpFbuw5nuxHC7NGA5ia7jNO0rg7JicAHXTS8R9fclZ4T8bUJXnLOSvicATC5koAvusBQFkkaGhtPsOQ/640?wx_fmt=png&from=appmsg)![]()起初不知道原因，还导致我对 ClawdBot 这东西兴趣都降低了。

后来想到一个可能性 —— 终端环境变量（HTTP_PROXY、HTTPS_PROXY）没设置好。（魔法）

于是我把问题丢给 Minimax agent："帮我写个脚本，让终端环境变量可以永久设置、可以开关、还能检测网络通信状态。"

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FnQIg8FoicpNgNPwMjxWicXRy13cgG0ah1JVRKyibjvnm1UicSBMFDAaGeibvz34puECTydSVt9vRFEC3iasvUY0csERn1ibtnA7DSUoo/640?wx_fmt=png&from=appmsg)![]()它给出的方案包括：

* 永久设置环境变量（HTTP_PROXY、HTTPS_PROXY）
* 提供开关脚本（proxy-on.ps1 / proxy-off.ps1）
* 网络检测命令（Test-Connection）
![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FmNcib05ycaibu54MN71JehHCmAdicqnLwSHQW9pa28xCwzfvN0NIichmqYTNX17Fg6eyWaib80hXlNEM6REs1Haaic09GpY6KUT81uM/640?wx_fmt=png&from=appmsg)![]()问题解决后，我又让它把这套方法做成了 skill，Windows 和 Mac 的检查都做好。以后在新的电脑直接让他看 skills 就能复刻。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FnLfDU3cWEwJKMhF194e7o8QhK7PW2m7IpNiaxMnNibtibezBWjMOzV1e9KdGEAjkkLibbSWtRYAMibxa56XtK5icFiaKxxqFzqLJ7ia90/640?wx_fmt=png&from=appmsg)![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8Fky8QLTOaCGtqkJCibTeBk3Hbk4BRLVZAJ52NrKBGuREuBoyGEAgicTPKaB6BdQK3VuE814JTtBG5q5CcTsW1CxYAaubE7cBoaF0/640?wx_fmt=png&from=appmsg)![]()另外，我使用 claude code 的时候。经常是要设置中转地址。于是我便让他写成脚本，并且支持一键启用或者修改。提示词：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkxYYXyZxUqwCO6PUIFwPMd86C3RiaBMzFoNKEe4FqiaGD1Kfo61QXjCC5kb5TSbTibnKicCSESrMJMa1mHeFzwScuJiaDcy2TibZicMI/640?wx_fmt=png&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FkghVJQE5e7iaPiaSy06ocgcM5uogvjBVdsdj6rmIVhEibZdWRkFCkdN5Ma6iapCdmFVHxtia2FC3qpvYozZaMUJlfJNsqnrN4Jw86k/640?wx_fmt=png&from=appmsg)![]()我还想让它用短命令(如 `cc -new` )就能够支持在默认文件夹新建 Claude Code 工作空间，或者以界面的方式选择一个新的文件夹打开(`cc -o`)，



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/8uA0NGWE8FmWibNl8a19LQwumj9ypichONtBUGic6o7X68gicyia2q1SsB8C50YYX6CJN1k7Xn52fPU9r4XP0IZ0ibgBXHEm3o1zpgsMftqf86AbU/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

同时，这些短命令也支持快捷键； 不管我是在终端还是其他\*\*编程IDE的终端\*\*，都能快速使用配置好的 Claude Code 还能高效切换，保持Vibe 状态。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fnmic7ibDBjO9fwt0wIiajiaaWrHibdXurwDo9pq1FLTSic1z4pM1BBFzh6s5YzbYapRoTwiao26100JzRYQribQFpsTKtjicIm60ZJOS6w/640?wx_fmt=png&from=appmsg)![]()## **02 智能文件管理体系**

杂乱无章AI 整理CodeMedia另外，我们知道，在 AI 编程的时候，项目文件名基本上首次命名之后就不能再改了（路径也不能改）。因为像 Cursor、Claude Code这样的编码器，改了名称，聊天记录就会丢失，要改索引也麻烦。

我最早那个 AI 项目文件夹，现在看起来就是个命名灾难现场——一堆当时随手起的名字，后来想找几个博客项目都得翻半天。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FlMAsqvNGMQdjU6Jib33SUUcV4Sibovgwicmqic5saHvWZ3C9Gd4okgTQMG7ibZmiaBd5HwmvKqQLNFPSJPibHnPOXOialaZVnic9YJAWHc/640?wx_fmt=png&from=appmsg)![]()于是我便直接交给它。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fn0JvEHyQdkNIYhmkeFaLNhCw25Ma7sNnBbLMIBGjTUgNdYGzRXYNv4ibNTzD1xSe4icDDYA1TwRhdTvnczsp8YoNZ6m1HpAtu3Q/640?wx_fmt=png&from=appmsg)![]()得到：



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/8uA0NGWE8FkqtaIvbZB1hvDib2JCfsrMlibrqm6wLNX7kguEInhSYw2iaf9xZPRqXFAIvO9qa96qerIzLS929uj9QgN5n7ewFm4oaoVPib6NbibY/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

再举个例子，我的剪映 LUT 文件夹——里面有 125 个北欧冷色调滤镜 LUTs。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fk5XKmXRdxDVX5NBSOso2eguFYT46srvdqtaiahgqQcA5GmbpIbxJz9iaDaE2zPoIVdk5WNYUwshicuxxOPyQmxwibzRu8N8ISWibZg/640?wx_fmt=png&from=appmsg)![]()如果让 AI 去理解这些文件的内容特点，它能按照色调、风格这些维度重新分类。剪映草稿也可以试试。



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/8uA0NGWE8FkUpzYKvjQGdgZpqxwu4dRCzp0QWu1Zolb6FnKXy6icYBTkrO6SYueZmbrN24KNrxeE0jPd6uBjH4BFxq1dzGgMoRqmRdvQOBUg/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

视频的20s后的是我的一个音频文件夹，也就是配音场景的分类 —— 

提示词：因为我自己不能每次都点击听这些音频，然后这个文件夹音频我想用，你用一个网页或者其他呈现方式，能够让我一看到就全局管理，能够知道每一个文件是什么。这样下次我剪辑的时候就好弄了。

我喜欢这种意识流的提示词输入方式。

而我们把它的管理半径放大到整个电脑系统，那就可以。。。



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/8uA0NGWE8FmeIjo9XWr7jWtPPSiaPvicdcaCwmfUxiaOeC4HUsNiaRUAfkaH3B5B2DgxSJwicJU2XnGEfUugbV6Y6a4SI7ZDpZf5DibVar1pdlHQk/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

我电脑是3个T都不够我装的，什么录屏剪辑、 AI 项目、各种工业软件什么的。太多了。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fmhb4ULNV8US6vKiaPkAoj9v0iaTqMNLJYu3rnbkrIAPIiaeIaIJPibib3mt8MNMJQddicLEl7zWicE2DiciaZI6JUoHWGUqudXAjjSOE6Q/640?wx_fmt=png&from=appmsg)![]()这时候AI跑一跑，做个视图来说也很不错，进一步迭代优化，可以做一个更好的智能管理系统，点击也能有相应的执行动作。

总之，不管是编程项目、剪映文件还是那种不点击就读不了的音频文件，他们都可以用类似的方式。建立索引，换一种呈现方式。

这种方法我经常就用在那种 —— 过了许久，需要自己去重新找某个东西的情景下。

如果不用 AI，你自己一个个翻你以前自己的文件夹要挺久的。现在的话用AI 就可以一句话，让他开个线程，我们直接去做其他的事（这种活，我现在基本上是对着手机说一句话就指挥电脑干活的状态，省心不少）。

## **03 垃圾清理与系统瘦身**

再说垃圾清理的改造。可以让 AI 文件整理助手扫描 ，识别重复文件、空文件、安装包、临时文件，然后生成清理建议，一键移动到测试区。

以前用 C 盘扫描器这类工具，还得自己判断哪些能删。现在 AI 能智能分析，预判哪些可能是垃圾文件。对新手来说，有个可视化面板，知道哪些不该删，权限也更安全。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FnpvtdhP5lNCL3Yn9WgEdPHm7yAFlKAG9KmoNCX1Roo1sjHwwfo9y3e2z8dfgrw01Kno4a3icmAYHslnuO4XyCGtKmYEVN2Hk8s/640?wx_fmt=png&from=appmsg)![]()Minimax Agent 单独有一个文件整理专家：" 扫描 C:\Users\Aitrainee\Downloads，识别重复文件、空文件、安装包、临时文件，生成清理建议+ 一键移动到垃圾桶测试区：'帮我清理下载文件夹，找出重复文件、空空包和无用文件，生成清理建议。“

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_gif/8uA0NGWE8Fm5GibZdEqfnW8QUHx2loA3bIzxas5WMe8X1ACZ1odR8YibBHH9ut5UNfnBMKKytahc8dPcs0sNmzicHZV2o2icRd9p6gdSQNibjafk/640?wx_fmt=gif&from=appmsg)![]()## **04 视觉创作与桌面控制**

另外我在玩 Clawdbot 的时候，让他自己给自己画了一个图像。这不是用 AI 绘画模型，我是让它自己控制我 Windows 的绘画软件绘画的（用到了一个桌面控制的skills）。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FmOUNmkpAgymOHuNL2DyFeA3qadtcuaNjaicwtS4F1btTtJ4CBxNlTenmyx4TVBjMA9sWibKCY0sCy2MYUfgeqDpG3s3hCmNW6SE/640?wx_fmt=png&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkTm6ib10w8vmViagdibc2J4AtQNZlV0IdRwicAYzIUibic6j8wYbkuWyS3iaOWIrCjpTOHibmfJmicMqu1RZVO7hcjuqVRiabxN0amUyYQU/640?wx_fmt=png&from=appmsg)![]()我要求 MiniMax Agent 把下载文件夹第一张机器人图片 PS 一下。我下载文件夹有很多图片，它也确确实实找到了我说的那个第一个机器人图片。而且他也直接给他PS 出来了。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkQ1JlicDQXiaQFjo9J5w4qtM4wjxGib8IE81TZibwCpcnQGXpu6kAYPyibFdNjVpOEmuEZhghGibbxdyiaegXNSBD7MlC1WDTM1pjuuk/640?wx_fmt=png&from=appmsg)![]()甚至让他基于这张图片还可以做出来 GIF 或者视频等等。挺生动的，毕竟背靠海螺 AI 这个第一梯队的视频模型。



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/8uA0NGWE8FkefUx46yqfZicdBpsgV7mVPJZSEpqiap94kLqhCLEZLcC2FvicPA3mCkRbxFM7ldp3cUAu7ftzn6IksHoaR31OdFIDDic02IXibK9Q/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

除此以外，还可以提示它去做一些批量处理的操作：比如图片剪裁等等：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fl0ibXueicTdGeel3H974EpbicIC8x0Z0emXdnWcNYRwbickRg7G0FzjtftjyQibTHlMe0kurcWFaQwuBavyPvoAxFcNzyibfMXa3zEk/640?wx_fmt=png&from=appmsg)![]()另外补一句，操作桌面的这个 skills，可以让你的 agent 不只是能操作浏览器，而是能够控制键盘、鼠标等等。

ps：画出来的圆还真圆啊：（他也是控制鼠标绘制的，只不过读取像素挺精准的 ）



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/8uA0NGWE8FkDDJ3KFTqbtxlWMSMlNpiapglKY794ZuRSCldcxxnjvdROJVgCNfXHibgHtnGx1rVWmwX5kVBLiaXIfTw5F73qTfNicPKO47rN5X8/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

我用的两个桌面控制 Skills 如下：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FlhIQp32yr4WgwxRzsht0G8GLxv6L2Bt8Xrkq3uHHaISU1nwKY1ZRzKh9LcZoCs4lVTknQNjUjSwIJ2HqYpibzOej4nomyjFx7U/640?wx_fmt=png&from=appmsg)![]()我都是提示 Minimax Agent 安装的，不管这些安装还是其他的什么，我已经很久很久没动手了。

## **05 浏览器多标签控制**

另外我在用 ClawdBot 的时候，发现了一个问题：ClawdBot 操作浏览器默认是通过类似于 playwright-mcp 的方式打开一个独立的浏览器窗口，如果要打开本地浏览器，他需要安装一个官方的插件：

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FmRz1yTiaPdydptreoMI8uPX4ET2uI4lrVPnjczmZaZZ79JTiaWDxPA8GN8zl2iaImJeW9xCk675QwiaCz513V1GnjclLXaPjLibib8k/640?wx_fmt=png&from=appmsg)![]()但是这个插件一次只能控制一个标签，你得手动打开，类似于我以前介绍了这个 [Browser MCP](https://mp.weixin.qq.com/s?__biz=MzkyMzY1NTM0Mw==&mid=2247506492&idx=1&sn=8071925f63752a2e62f64334af1ad357&scene=21#wechat_redirect)。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FlrNX2U0zToZTkEY0zhFsIAmsiazbTcicYq8EgszfXYkcTic9NWFNdmxszxYLeBxrtKfW1eQSFFQy1rArgmgzjTkxmJUVCILIkOibQ/640?wx_fmt=png&from=appmsg)

所以我想让他安装一个新的、支持一次性控制多个标签页的，不用每个标签页手动切换—— mcp-chrome。![]()

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_gif/8uA0NGWE8FnTTGI6QL4GXcz8kU69XrtyYMkctLbwIo3jjKx3cjLymbh6iaVCHMUpqicDofEs7CibWwEicUDRYcAFBqTdlTfF9etD3AV54MeyAho/640?wx_fmt=gif&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FnDSIljj9wtTBEJibRawhlvsgYbIJpzokoNwSfw3nSNVFgfcMha0ZmTWtXsygC4mlXmDiaxlJInuhQLQ3fj0GS3EbzuF8RmbCgJk/640?wx_fmt=png&from=appmsg)![]()我让 MiniMax agent 去给我安装它，这是个安装起来有些难度的浏览器控制 MCP。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FlKMKTianTBPvnVhe8yG5Yx8UauJ4dzibvwaSVNCGyWHUwXXTMMgycIM6qmZ8tLZfLGcLKwlnI7G0je0icDMHLP5GQpSStNEuMMgE/640?wx_fmt=png&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FmjVv0uGycqbf07SLLvxibvTicEOu8vGbxY8bExusibzsJibcUcQZfjHnLGicPbPaGr636HEibS75ugSlYtsd0QE7WSRiaSHw1Cc2DE0A/640?wx_fmt=png&from=appmsg)他做得还不错，我在另外一台电脑上当时用 claude code 的 opus4 模型也对话了比较久的时间：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fk6qWAyfJQ7xdsE5FymmbhwozibzwKickmsxCUfUicicRX6uRtKj80iauwY6JLO9DfuTQS5SzDbrRGHm98ibvxIIibUIic8j674yCrX7ak/640?wx_fmt=png&from=appmsg)![]()因为 mcp-chrome-bridge 安装教程涉及了浏览器扩展还有需要注册什么东西，根据官方文档，需要以下步骤：

* 安装 Chrome 扩展 - 你已经完成了
* 安装 native messaging bridge：`npm install -g mcp-chrome-bridge`
* ⚠️ 注册 bridge（关键步骤，你可能漏了这步）
## **06 更多实战场景：简历、内容与社交**

再看我用 MiniMax agent 筛选候选人简历的案例：比如你的文件夹下有那些 PDF，你不用一个一个去打开查看，他自己会看，你可以让他批量处理，按照你的意愿整理提取。平常那些办公的细碎活都可以。

整理前（假设有8个简历）：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkrXCfAaiaXUAbdBMmwE2u7icbrFNKdmnQWibkXEQQRRRic3lEcPbCricDegibrEpAFaCsly8SVAdhnAkuR61lcK9JXibBXeicqYYXyBHk/640?wx_fmt=png&from=appmsg)![]()提示词：帮我整理文件夹里的简历，按姓名和工作年限重命名（如姓名_年限.pdf），并把工作年限大于 5 年的单独放一个Senior_Level的文件夹。D:\AI-Code2\MiniMAX\resumes 

就分好了：![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FncmcvLGpCPrqwNsIgaCbUfecJy6q5zrUicFgxw2HxTK3ljLYt6mJgGDNF7OpibRUAAzCwFClibGCicevtjAZu8IdpRK0SgESHevtY/640?wx_fmt=png&from=appmsg)![]() 启动浏览器访问微信文章：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkPqiacDaJ0A4xg32L3SLomBP7eABaMReClJJPQdVFqlcPicicH7gMKXoqoJ4KibZID2j3bIQbr2z9Ckl1ibibicluFSe3SPY3TKdt32U/640?wx_fmt=png&from=appmsg)![]()公众号文章转小红书：把我的这篇公众号文章拆成3条小红书图文笔记并发布。它生成的这三种笔记的内容也有参考性，发布前可以先让他跑一下这样的流程。后面也可进一步优化提示词，会更好。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Flh23ylo1yslyZia4ibiaLLtGB7SPRX1ckBYPAOx74cwAxapJyJHK4GDTkvm6ib6xEZHLMfyzAibw8ictJvUTl5NFicZ39ib43tKpJ4IH0/640?wx_fmt=png&from=appmsg)![]()热门视频检测：帮我去小红书上找带#AIVideo标签的视频。对于点赞超500的视频，附上视频链接，并反推视频的prompt，将链接与prompt存在桌面上一个名为Inspiration的文件夹里。

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FklibKh9WDHO6ZMljkZiautZSOFLh4GtibBtic8Eo4sLRp6iaoauyAj35WoYLpAWtiajricibZo5Wx5R418tjoNgItZcJcIGlYtDVBziacs/640?wx_fmt=png&from=appmsg)![]()![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fld0Eaiblbkusq4eNd0N16yBOl62pPYOOeHyyIHQWWiaP1EiaqlRfylQMHib5q8opicWnlddavvL2tLyQM3ls6TH0J4PK4zproiaOvAI/640?wx_fmt=png&from=appmsg)![]()建立自己设备的共享文件夹，

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FmrDF4kwzW0efibTjGNaqqKwoakLOjOle3Vmj72k6icONf83LmDIXWnXbpChKxFcWuzqHkxq0hHRLy9xcbBSibvTQ3P3PcKTu5qNU/640?wx_fmt=png&from=appmsg)![]()

做一张"AI发展里程碑"时间线：



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/8uA0NGWE8FmI4P2Rjhp3uzhjzACKZxlicsr0ibibbQEaA811RVY2lLRZuwt2IRLZNgeZaRox2nQRH28aaTEfqrt4KDUcxguOmKJEAZaTFWDVBM/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

或者 B 站博主分析：访问秋芝的Bilibili主页并打开最新5期视频。抓取每个视频前 20 条高赞评论，分析观众情感，找出最打动观众的 3个要素。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8FkvXLoGCaib0icibfDdiafhIWPo8EQGDg5tJ9rfpb5WHf87ugWrOfWUia7AE3cQe7dpSgwy7VsAOEE43t5n32fmFjl6owhma9rGTo9A/640?wx_fmt=png&from=appmsg)

[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_jpg/8uA0NGWE8FlO3x1hlXl2F8pCg4FKxmBHSHo1kV01SYuYZNGMXaM7smqHtyFBRne68qUBULDQgbb8Q1XYMeLkPNK4fMvZVcOSj1liacpgk0DQ/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)

## **Agent 其他玩法**

### 📂 文件管理类

* **照片按拍摄时间分类：**扫描 EXIF 信息，按"YYYY-MM"创建文件夹归档。
* **视频素材自动打标签：**识别人物/风景/产品，生成标签文件。
* **文档按主题归档：**读取 Word/PDF 前100字，按工作/学习/生活分类。
* **重复文件智能清理：**扫描 MD5 相同文件，保留最新版，其余移入"待删除"。
* **音频文件批量转录：**MP3/M4A 转录为同名 TXT 文件。
* **PPT 批量提取图片：**提取图片并按"文件名_序号"保存。
* **压缩包批量解压+整理：**解压 ZIP/RAR，删除空文件夹，归档压缩包。
### 🎨 创作生产类

* **批量生成社交媒体配图：**读取文案，为每条生成对应风格配图。
* **视频脚本→分镜头脚本：**自动拆分镜头描述+时长+构图建议，输出 Excel。
* **文章批量配插图：**扫描 Markdown，为每篇生成封面图和内容图。
* **批量生成短视频脚本：**根据关键词生成60秒脚本（钩子+内容+CTA）。
### 📊 数据处理 & 生活类

* **Excel 多表智能合并：**按 ID 合并总表，去重并排序。
* **日志提取关键信息：**提取 ERROR/WARNING 行，生成汇总报告。
* **旅行照片生成游记：**识别地点场景，按天生成图文文档。
* **菜谱图片生成购物清单：**识别食材用量，汇总 Excel 并标注重复。
### 🎯 其他场景

* **剪映草稿批量重命名：**识别草稿封面内容，生成有意义名称。
* **Telegram 聊天记录归档：**提取关键对话（重要/决策），生成 Markdown 归档。
* 应用内存占用分析与管理。
另外，他这还有个 Supabase 集成，有助于后端编码的实践练习。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/8uA0NGWE8Fk94KOkbnL1FyORDzh7bWbyXr40IHeT6niaftibdFcViaaBGe3e5KktErmyiboiaeExvofdWicQMqeE19djLGT7ia6nAaNEOhuBvdv2xo/640?wx_fmt=png&from=appmsg)![]()## **最大的变化：主动性**

传统方式How?Agent 思维Result!AI文件整理、网购、资讯监控、桌面控制、MCP 安装、任何痛点问题（部署、报错...）…… 当 AI 能感知你的本地环境、理解你的需求、自主执行任务时，很多事情的做法都会变。

最大的变化是什么？我觉得是**主动性**。对话式 AI，你问一句它答一句， Agent —— 它能自己动起来。

你给出 20% 的想法，它能自主完成的比对话式的多。这个"更多"是什么意思？就是它不仅执行你说的，还会带上那些只有实践能够获得的。

"研究一下个人 IP 怎么做"。Agent ：      
1. 搜索相关资料      
2. 整理成结构化文档      
3. 分析你的现状（比如你的公众号数据、抖音内容）      
4. 生成个性化的行动计划      
5. 迭代 Skills

你的脑力活动进一步解放。以前用传统工具，你得想清楚每一步怎么做。但用 AI Agent，你只需要说出目标，它自己拆解任务、执行操作。这不是说AI 替代了你，而是思维路径变了：

* **以前：**我要怎么做？（关注过程）
* **现在：**我想要什么结果？（关注目标）
很多时候，我们用传统工具形成的思维惯性，反而限制了我们对 AI 的使用。下次不妨试试，直接端到端地向 AI 提需求 —— 不要想"它能不能做到"，**先说出来，看它能做到多少，又能解放你哪一部分的脑力活动。**

**试试看吧。**

**相关指南：**

MiniMax Agent 桌面端用户指南

https://vrfi1sk8a0.feishu.cn/wiki/H7rQwDKpdiP2MekCcn8cy8Lxnwh

**🌟 知音难求，自我修****炼亦艰，抓住前沿技术的机遇，与我们一起成为创新的超级个体（把握AIGC时代的个人力量）。****点这里👇关注我，记得标星哦～**

![](https://i0.wp.com/mmbiz.qpic.cn/sz_mmbiz_png/8uA0NGWE8FkfaWdzx5xQicJfzXVRTScXPPfX3sE24ufMwwKV9o0da596j73yJ6RiciaciaewbRxS3AqkBRLqtva4TpiaE1ibiaBBFjIDGJlSD0U89s/640?wx_fmt=png&from=appmsg)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/U1x9DZmFfyJSRqK5dxKycQ)*
