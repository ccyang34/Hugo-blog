---
title: "用 Claude Code 接管Google Antigravity后，治好了我的token焦虑，额度根本用不完！"
date: 2025-12-30T20:04:44+08:00
lastmod: 2025-12-30T20:04:44+08:00
categories: ["AI与技术"]
tags: ["Google Antigravity", "Claude Code", "AI 中转", "免费额度", "大模型", "开发工具", "Antigravity Tools", "API 代理"]
---
Google Antigravity 随着 Gemini 3 发布有一段时间了，跟 Gemini 3 的光芒闪耀比起来，Antigravity 就像个副产品。

**刚开始发布的时候，大家对 Antigravity 的讨论最多的就是：怎么登录？登不上去啊？怎么卡在这个界面不动了。**

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJOR2amTcPcLAf8kIx8dxLmLzCCSGs6snBoEkEQB8AAe1WbJRWI7UTTPxg/640?wx_fmt=png&from=appmsg)

后来，大家通过各种方法能登录的都登上去了，剩下登不上去的就不关注了。

最近大家对于 Antigravity 的评价是：Google 真大方啊，Antigravity 内置的 Gemini 和 Claude 免费额度太够用了，根本用不完啊！

Antigravity 内置的大模型不只是 Gemini 系列的，还有 Claude Sonnet 4.5 和 Claude Opus 4.5，而这些都有大量免费额度。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORZ97YkEB2dcM5AyHCSUA5PZ3cZicmU2XOjwfesdPFOuo2sVT3Gd4u2RQ/640?wx_fmt=png&from=appmsg)

最近几天都是晚上用 3、4 个小时，主要用 Claude Opus 4.5，用完一看额度，还剩余百分之七、八十，当然，第二天又重置了。

据说，额度是 Claude 官方订阅 20 刀版本的 3 倍左右。当然了，说的是 Google One Pro，如果是 Ultra 订阅的话，几乎是无限量的。免费账号也有额度，但是比较少，而且是一周重置一次。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORxcjRDGhfsFXqORzq0uaN3T6AcvCm8kKGMMtqTGVwqmicuvuVMnj5iaicg/640?wx_fmt=png&from=appmsg)

**那如何在 Claude Code 中使用 Antigravity 的额度呢？**

## Antigravity Tools 安装

就要用到上面截图中的这个工具了，一个非常牛逼的开源工具，叫做 Antigravity Tools。

仓库地址：https://github.com/lbjlaq/Antigravity-Manager

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORImetMkASMs6zaev9kiboWpuMgo8TqIMFlaSDBfrr46EGHeTYibr8QIog/640?wx_fmt=png&from=appmsg)

这是一个专为开发者和 AI 爱好者设计的全功能桌面应用。它将多账号管理、协议转换和智能请求调度完美结合，为您提供一个稳定、极速且成本低廉的本地 AI 中转站。

可以将常见的 Web 端 Session (Google/Anthropic) 转化为标准化的 API 接口，彻底消除不同厂商间的协议鸿沟。

接下来介绍一下，如何把 Antigravity 账号添加进来，其实就是添加 Google 账号，并且如果你有多个账号的话，可以都加进来，每个账号都有额度，这一个用完了，可以快速切换另一个，相当于一个 token 弹药库了，只要你账号够多，你的额度就相当于无限了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORW59CX3lRW8ovY4ibkkAmRdf0k5NIyEpycd7Q2wbgia1EOuBjdZv5UHAA/640?wx_fmt=png&from=appmsg)

首先安装软件就不用说了，照着官方仓库提示就可以了。目前只有 Mac 版。

安装好之后，点击「添加账号」。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORAAyqrQ0qngKSEMoxNks6yCWZ4KYbRiaYFov3V51t2S3kGPDhtsl4jgw/640?wx_fmt=png&from=appmsg)

之后，在弹出界面中，默认使用 OAuth 授权就好了。

可以点「开始 OAuth 授权」，这样会自动打开默认浏览器，如果你有 Google 账号，自动完成登录授权，回到这个界面，授权成功，账号就添加上了。

如果你有多个账号呢，一般都是在不同的浏览器打开，比如我有两个账号，一个用 Google，也是默认浏览器，另一个用 Firefox。

Firefox 不是默认浏览器，所以就复制授权链接，然后在 Firefox 中打开链接，完成授权，这样，就把两个账号都加进来了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORn5g8CtFPZFwxrFTR7wCl1RwPbqpd70rNqwTeIWwicJWOCCOZR69libeA/640?wx_fmt=png&from=appmsg)

这一步完成后，就可以当做一个管理面板使用了，在仪表盘可以查看全局使用情况。

进入账号管理界面，可看到全部账号的具体使用情况，点击刷新按钮可以刷新使用量。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORWCZfMyAWUic75xpxsTkwVrQ80OMC2VYk2F4fDH5Er761KPy9c5c4nAA/640?wx_fmt=png&from=appmsg)

点击每个账号后面的「信息」图标，可以查看具体每个模型的使用量。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORPXXjcMXwvRs7nmGJbQMsJ9FIf5kqr61gib6zZHFiaL27OmslXt9ZjsDg/640?wx_fmt=png&from=appmsg)

如果你不用 Claude Code 的话，到这一步就可以了，能够方便的查看剩余额度，用起来比较安心。

## 在 Claude Code 中使用

如果你打算在 Claude Code 或其他终端使用配额的话，还需要进行下一步，就是 API 反代，也就是建立一个中转代理，让 Claude Code 的请求从这里中转一次，然后最终调用 Antigravity 的 API。

非常简单，打开 API 反代界面。

未启动状态，右侧显示的是启动服务字样，点击启动即可。监听端口和 API 密钥是关键参数。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJOR5XQTDzxpVfDEuNwkEPiaEXDrB4S5j5vgxicg028DR0ayXPJHHtG47IkQ/640?wx_fmt=png&from=appmsg)

界面往下拉，看到下面，支持 OpenAI 协议、Anthropic 协议和 Gemini 协议，也就是说还可以在 Codex 和 Gemini Cli 中使用。但是如果在 Codex 接入，需要加一个模型映射，比如把 gpt-5-codex 映射到 gemini-3-pro-high。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORXelVUPfrChBrumJ27bKNSPK6wiaXIkwBgVFXFiardSDreibcPCbEF4bkA/640?wx_fmt=png&from=appmsg)

如果你用 Claude Code 一直是配置环境变量的，那把环境变量中的这两个参数换成 API 反代里的两个参数就行了。

[实测，Claude Code 配合国内大模型，一样很牛x（完整配置教程）](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476164&idx=1&sn=7c32aefd98b5f47002ab9b00a4c39202&token=49127848&lang=zh_CN&scene=21#wechat_redirect) 这篇文章有介绍如何使用 Claude Code，如何接入大模型 API，如何使用 CC-Switch 的完整教程。

```
export ANTHROPIC_API_KEY="sk-xxx"
export ANTHROPIC_BASE_URL="http://127.0.0.1:8045"
```

如果你用的是 CC-Switch，添加一个供应商，同样是将这两个参数配置进去。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORgneqo0yUSPGVU0TSCEHD1NvfdEkPjzChfAKvJFYcVjKoPFNSPiaRSZg/640?wx_fmt=png&from=appmsg)

模型用哪个，直接到工具中复制即可。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORBkIib5oJJ6vtQ3Je4ibr3VBtd38EH0ibSuNd7GEESNK420eR8D4iaS6Ptw/640?wx_fmt=png&from=appmsg)

然后在终端打开 Claude，就能愉快的使用了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORaiavuxoZiaR65nbVBA0Buq6cDYXpibo9bQUFia9Cmpvo6kAKicwCS614tLA/640?wx_fmt=png&from=appmsg)

## 一些限制和问题

1.  如果你的 Antigravity 还是无法登录，除了网络问题，那大概就是账号的地区不被支持，可以到下面这个地址把地区改了。
    https://policies.google.com/terms?hl=zh_CN
    ![](https://mmbiz.qpic.cn/sz_mmbiz_png/iaWSDo4TfyZh2vwpuB5cI125VbHPibLJORFibB6ItNBgiav7Ogvy6uib5KZA3jLXBjImTqFia0ib5He0Dic5hDU5p8GgvA/640?wx_fmt=png&from=appmsg)
2.  免费 Google 账号额度最少，而且一周重置一次。Pro 账号额度大概是 Cursor 20 刀的 3 倍左右，真实量不知道，只是大概。如果是 Ultra 订阅的话，那就随便用了。
3.  Antigravity 中的 Claude 模型和 Claude 官方的模型有所差异，据说是经过 Google 调教过的，速度更快，但是效果比 Claude 官方略差一点，一般人感觉不到的。

**有事儿没事儿都可以加好友，不限于技术交流、AI、独立开发等，备注『公众号』就可以了。**

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/iaWSDo4TfyZgHJiaAp4jogHHb5OmibicrBib6ZedMP9avevfrrscVDlSkicZibk92OoKkpQ03gDTdjXLaVbbAOxoAVrIA/640?wx_fmt=jpeg)

**往期文章**

-   [我用 Gemini 3 手搓了一个地球虫洞，这效果太离谱了！](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476642&idx=1&sn=d23615f03fca792209406a9c2b2369b2&scene=21#wechat_redirect)
-   [实测 Nano Banana Pro 和 即梦10几种场景，到底差距有多大？](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476572&idx=1&sn=825c787412d9a00de0d787256590a65d&scene=21#wechat_redirect)
-   [免费使用 Gemini 3 的几种方法](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476530&idx=1&sn=cccf31b35f5cd9806817037abb2f2a61&scene=21#wechat_redirect)
-   [Gemini 3.0 来了，前端不存在了！](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476511&idx=1&sn=b286cf6591ae573e5c27aebcef0fc25a&scene=21#wechat_redirect)
-   [Gemini 这个功能才是真的利器，强烈建议豆包、Kimi 跟进一下！](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476452&idx=1&sn=af65202666a3ba9a9b9cdced8da7d219&scene=21#wechat_redirect)
-   [“黑熊精录音棚唱歌”的视频是怎么做的？](https://mp.weixin.qq.com/s?__biz=MzAxMjA0MDk2OA==&mid=2449476271&idx=1&sn=f402bdd0f1498e7a0c5aff9c931a39bf&scene=21#wechat_redirect)