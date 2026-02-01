---
title: "OpenClaw（Clawdbot） + Kimi 2.5 最新手把手教程，附飞书接入指南和 700+ Skill资源"
date: 2026-02-01T22:37:07+08:00
lastmod: 2026-02-01T22:37:07+08:00
author: "向阳乔木推荐看"
categories: ["未分类"]
---

**作者**: 向阳乔木推荐看

最近刷 X 帖子，看到很多海外博主推荐 Kimi 2.5 接入Clawdbot。

追求物美价廉，果然全世界人民都一样。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvDnBWd4gDdg0BIqcJKO2wOpfpP7KzOmiafJ4yEmgwP6eHS37XcWb764Q/640?wx_fmt=png&from=appmsg)前段时间，身边不少朋友测 Kimi 2.5 ，都夸前端审美优秀。

直到刷到下面帖子，震惊了！

**Kimi 2.5 在 Design Arena 设计榜，竟然打败了 Gemini 3 Pro和Claude，这可是开源模型啊。**

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvuSThUY7XCxxDrGGhticaicRIcpicjcviatfFfwxiartlgan8AZI9MPVbB1Q/640?wx_fmt=png&from=appmsg)看来前段时间研究 Clawbot，错过的东西有点多。

研究后，迅速把 Kimi 2.5 接入了 Clawdbot。

下面是一句话测试


> 写一个精美的Todolist网页
> 
> 

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvO575yiciaXWK9icic3AmRq6eeuyQ5RF8u6c00AdicwbEMFpE2H7I1B6Wtlg/640?wx_fmt=png&from=appmsg)出来效果如下：

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvyfPcH3NKqC1qk5L0xRGtsEguEnoODEqMp7MF7enic8BdBwldwVnuxtg/640?wx_fmt=png&from=appmsg)一句话直出，确实有点顶啊。

前端任务简单，又测了一个自己写的视频生成复杂 Skill。

流程很长，必须先调用Listenhub生成音频和字幕时间轴。

基于字幕生成图片提示词，调用即梦生图，再调用Manim生成透明文本动效，根据我的 IP 头像，生成片头和片尾。

最后用 ffmpeg 拼接，生成完整视频。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvz0iclmem0iaU57ickuqiagqianTmddXZ64m1gmak00icXAeW8YPrKISm5ebQ/640?wx_fmt=png&from=appmsg)之前我只用 Claude Opus 4.5 ，别的模型经常出问题。

没想到Kimi 2.5 也能搞定，出乎意料，视频如下：



[![📺 点击观看视频](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_jpg/jibL99tg2bCX3rUfiaGPmwmO9Z2icicbllRB7wxBgbhHCagMxIOReutsw84wIFJemxxicXjBiaicllgqyZdCj1QXATTdA/0?wx_fmt=jpeg)](https://mp.weixin.qq.com/s/8DwabUPPdOyOCAc_f8pKQw)



---

下面写个详细教程，教大家如何把Kimi 2.5 接入 Clawdbot（OpenClaw）。

另外，真的要吐槽下，Clawdbot一周竟然改了三次名字：

Clawdbot -> Moltbot -> OpenClaw

猜是最后一次改名，本篇教程应该是全网最准确的教程之一了，哈哈哈！

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSviaBoTg7gXC321lJbCDKF7ngWLcuP7peXHmt3d4CukTEeMMVErN9G9jA/640?wx_fmt=png&from=appmsg)为了接入Kimi K2.5 ，先开个 Kimi 会员套餐。


> https://www.kimi.com/membership/pricing
> 
> 

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvpXW9D6Q7k0KOwSNm98nC6sd7wbQqHDJr6d8vrrasg3AfG1X7lvJRag/640?wx_fmt=png&from=appmsg)订阅后点控制台创建API key


> https://www.kimi.com/code/console
> 
> 

注意：API key只显示一次，复制保存到安全的地方，后面要用。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvBCic6jibmu2JRBBPCPlXnupyXSHyGpDomACaCFYr3w8HRZnXb7aGxnmw/640?wx_fmt=png&from=appmsg)### 安装OpenClaw

以Mac电脑为例，打开终端（推荐Warp，好像也有Windows版）

复制粘贴如下指令，回车。


```
  
  
1  
curl -fsSL https://openclaw.ai/install.sh | bash

  
  

```
![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvAToUeuen9CJb0fteqY98cQNibQmd2dCib6PvQA5M0Hsksyck8BE1RiaEw/640?wx_fmt=png&from=appmsg)安装后进入设置流程。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSv58g8yvkdT8LBxkalxiapVMWjwMVrrEBgEtQH7cdxGQ5oKXxCgsbHKicg/640?wx_fmt=png&from=appmsg)左右方向键选Yes，回车。

Onboarding mode 选 QuickStart。

往下继续走，后面会看到 Model/auth Provider

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvjiaJEuD2VqDX6viabG19gtLA09XzCibPibwLDfSUHSI0WWCgPBmx2NmQaA/640?wx_fmt=png&from=appmsg)选Kimi Code API Key，套餐买的是这个。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvnlBibwhCzw83kXSVibplSsXMIKgFKicnL3ECsiaLdY3ngiabw0zzGyLY1oQ/640?wx_fmt=png&from=appmsg)粘贴上面复制的API key，回车。  
![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvVHD8vTjibzHwjZf2Zicgq19sktsfC4vmTxDutRRgtyPic0icNFV5ZEJQfg/640?wx_fmt=png&from=appmsg)选第一个，设为默认模型。  
![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvz2aXaUy3ibmYmBVaAWZjDRCZSF212QFFfkW7Z8cflVFgKZHjd1IVLxA/640?wx_fmt=png&from=appmsg)跳过了Telegram、Discord的机器人配置，后面教大家配置飞书。

然后就到配置Skill，根据自己需要勾选。

上下箭头移动，空格选中，都选好以后，回车确认，进入下一步。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvUNmagXwgaNXgYJv9Fsp9ADsRZM20QfQWKS5TniaRc1glyNLiaafOmmmg/640?wx_fmt=png&from=appmsg)然后是一系列配置，没有API或暂时用不上，但Hook三个都有用，建议选上：

第一个是启动时注入Markdown文件，在会话开始时注入类似README的内容。

第二个是操作日志记录，记录本次会话中执行的命令与操作上下文。

第三个是开始新会话时保存当前会话上下文摘要，便于后续无缝衔接。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvV64vEDbullEKPTBmE9DJQCbqvJYbE0KKjHHOt0btR8z1r6mFDdFjzg/640?wx_fmt=png&from=appmsg)如果你的电脑正在运行网关或以前安装过，建议选重启。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvBaibazlMlfic12hx8RkdrD5ctadVicCJvlWI4jHzJko02ymMKqYn5DZ5w/640?wx_fmt=png&from=appmsg)问你想在哪用（孵化）你的机器人，两个选项：

1. 1. TUI，意思是终端UI，基本上就是命令行对话
2. 2. Web UI，有一个对话的网页

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvIvWROOHbD9v1iaOAYicgHFiagoI9asj1zPtF9n30DxYc0RjMlbP6B5g0w/640?wx_fmt=png&from=appmsg)默认推荐TUI，其实我觉得对新手来说，可能Web UI更友好。

两者不是互斥关系，其实都会安装。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvPeY6WML40caEj8VzKnhp9slT0JRSequuT6qEwQLppwFhNvvMVOB5YQ/640?wx_fmt=png&from=appmsg)如果想进入TUI，输入：`openclaw tui`

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvBjf622ClQLcDJXek1FtruEV16SwrBdbHEnlbwfNoSFqDP5zk4J3c0Q/640?wx_fmt=png&from=appmsg)到这里，其实已经装好了。

以后用 Web UI 或 TUI 对话就行。

但是，OpenClaw 最有意思的地方是支持大量 IM 工具接入。

用熟悉的聊天工具跟 Openclaw 说话，下指令，很像当领导的感觉。

下面介绍飞书等接入方法。

## 飞书接入Openclaw

有人开发了飞书的OpenClaw插件


> https://github.com/m1heng/clawdbot-feishu
> 
> 

复制下面指令，粘贴到终端回车。


```
  
  
1  
openclaw plugins install @m1heng-clawd/feishu

  
  

```
安装后会显示如下界面。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvcoicX1tRNoZEZ7VrJQvDzWrpReonSQrspAWdmL0AOnO5FQlNXqLsQ7g/640?wx_fmt=png&from=appmsg)打开飞书开放平台


> https://open.feishu.cn/app?lang=zh-CN
> 
> 

点击「创建企业自建应用」，填写应用名称和描述  
![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSv7r4fsr9yY1ITlKeHfjib2teFpdTMa73jqHI2bEoDLajRgGwKzT8QNLg/640?wx_fmt=png&from=appmsg)然后在“添加应用能力”->找到机器人，点击“添加”。（有些权限开通需要先有机器人能力）

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvLD8wQws0ialETv9Xh7dp2qCrefbvZiaJSw3VUW3YrRMf5PibnXs7LQJ8g/640?wx_fmt=png&from=appmsg)在应用的「凭证与基础信息」页面复制 App ID 和 App Secret。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvkwiaPM9L5cSZWkeRQu4n4ich6TA76x6prAdehvuibVqnBst0fKu0JFY5w/640?wx_fmt=png&from=appmsg)在终端中输入


> openclaw config set channels.feishu.appId "换成你的App ID"  
> openclaw config set channels.feishu.appSecret "换成你的App Secret"  
> openclaw config set channels.feishu.enabled true
> 
> 

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvJiafdb9dKSibNQTuribcWibhBHcnJf62AylOJ8mExMMb40pHF7fxduseGQ/640?wx_fmt=png&from=appmsg)然后需要重启网关，终端输入下面指令回车


> openclaw gateway restart
> 
> 

上面操作很重要，否则下面飞书配置事件和回调时会出错。（未建立连接）

回到飞书应用「权限管理」页面，点击开通权限，输入im:message。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvokOTn471CsfKFZ9PJ9lr8h3vQL6IecDicN4YVY76kV3Phgf1CNxLwLQ/640?wx_fmt=png&from=appmsg)继续搜索关键词，把下面这些应用身份权限开通：

* • contact:user.base:readonly
* • im:message
* • im:message.p2p_msg:readonly （需要bot能力）
* • im:message.group_at_msg:readonly （需要bot能力）
* • im:message:send_as_bot
* • im:resource (上传图片或文件资源)

**重点来了，很多人这里配置会出错。**

事件配置和回调配置中，订阅方式都选“长链接”。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSv5gnbld7VNib0fhRzDf3SBqjt0rCsKJkZvKibeNVOhe29NZFB6WPBIqYg/640?wx_fmt=png&from=appmsg)![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvm40icVJ07kctLlDOt4EVUMuWiaUbPiayjKVSibRfpKzXsLY982JMzyUHkQ/640?wx_fmt=png&from=appmsg)然后，在事件配置中点“添加事件”，把下面这几个加上

* • im.message.receive_v1（必需）
* • im.message.message_read_v1
* • im.chat.member.bot.added_v1
* • im.chat.member.bot.deleted_v1

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvqhHHUWv9mmEyfuwqAEMVPuzu26XaicMJ7M7kUq5AOGrvPdPCibznXoqA/640?wx_fmt=png&from=appmsg)配置完成后，在「版本管理与发布」页面创建版本并发布。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvQGPVQSo9ApHiaG6yKdzZdDlcZNLZa2U2t1MVJD2cB6H9Wcxqj7ltopg/640?wx_fmt=png&from=appmsg)这时打开飞书，搜索“OpenClaw”，就能找到应用机器人。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvDNDFNO4GTYicpny02vDDgStvGvIbZxDAIbO2jAZFQTOYqYBMtp4Jn2w/640?wx_fmt=png&from=appmsg)别看截图多复杂，其实只需要花费几分钟就能搞定。

还有一种偷懒配置方法，就是让 AI 帮你配置

**“帮我把飞书接入 openclaw，插件安装指令：openclaw plugins install @m1heng-clawd/feishu”**

不过插件安装后，需要在终端输入下面命令重启网关。


> openclaw gateway restart
> 
> 

然后，再发飞书App ID和Secret 给它配置完成。

（注意：飞书开放平台还是需要自己手动配）

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvD0Mf0CRCmmxIVbdUQDhnpQSGDicJw20NjkC7F116cNHffjiaQ3QvkFJg/640?wx_fmt=png&from=appmsg)OpenClaw 一大亮点是支持各种各样的IM软件。

常见的有 TG、 Discord、WhatsApp、IMessage 等等。

个人感觉飞书对国人最友好， TG 最简单的，Discord 配置起来稍微复杂，但展示格式最好。

朋友写的Discord机器人配置教程。


> https://x.com/AppSaildotDEV/status/2016384987596206383
> 
> 

## 安装使用常见的坑

朋友YC写的教程，我读完，发现也遇到过不少。


> https://x.com/lyc_zh/status/2016984907226939820
> 
> 

另外，蝗虫群友发了一张AI生成的图，觉得对理解Openclaw的运行机制有帮助。

从你说话，到机器人回复你，经过了很复杂的流程处理。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvibQ5DZ201rGmX4hyCiaIosuUdE1RHJrPlwtFBKD1tID8AIDiaU61fR6wQ/640?wx_fmt=png&from=appmsg)**推荐大家记住几个常用的命令：**

启动Openclaw的TUI


> openclaw tui
> 
> 

重启网关


> openclaw gateway restart
> 
> 

开启新对话


> /new
> 
> 

添加备用模型


> openclaw models fallbacks add [模型公司代号/模型名称]
> 
> 

例如：openai-codex/gpt-5.2-codex

设置默认模型


> openclaw models set [模型公司代号/模型名称]
> 
> 

例如：kimi-code/kimi-for-coding

另外，既然已经连上Openclaw了，不会的都可以问它。

比如我问如何给不同会话线程指定不同的模型，其实场景还挺多的。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvH55JC6ibJhlkKPIRSWPIfuxefkEwQicKfmp8uoOia5D4ecNlO0NEzEF8A/640?wx_fmt=png&from=appmsg)## 一点想法

发现很多人安装OpenClaw，不知道用来做什么。

我觉得是缺乏场景和专属自己的Skill。

OpenClaw 会自动加载 Claude 全局安装的Skill，这点还挺方便的。

![](https://i0.wp.com/mmbiz.qpic.cn/mmbiz_png/jibL99tg2bCUWAUy7dwQIC3fjEjxMibCSvwCUdXAE8lRldFaWrHrhq7HRjj3zKe8o8fXbghlGyIH0c2enc3f5DuA/640?wx_fmt=png&from=appmsg)如果不会写Skill，可以从模仿或使用别人的Skill开始。

分享一个 OpenClaw 精选 Skill 库，已收录 700 多个Skill。


> https://github.com/VoltAgent/awesome-openclaw-skills
> 
> 

## 写在后面

这可能是我写的最细的教程之一了。

但这只是入门。

OpenClaw的玩法远不止这些，长期记忆，心跳问询，异步工作，定时脚本...

另外，我还没来得及研究Kimi K2.5的多Agent集群。

感觉跟OpenClaw的理念很搭。

不过，折腾归折腾。

但一定要记得：**工具的价值在于真正被使用。**

希望这篇教程能帮到想深入使用 OpenClaw 的朋友。

如果觉得这篇不错，请一键三连支持乔帮主。

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/8DwabUPPdOyOCAc_f8pKQw)*
