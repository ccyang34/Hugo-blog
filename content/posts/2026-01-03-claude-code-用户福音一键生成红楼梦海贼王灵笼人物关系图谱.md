---
title: "Claude Code 用户福音！一键生成红楼梦、海贼王、灵笼人物关系图谱"
date: 2026-01-03T17:44:18+08:00
lastmod: 2026-01-03T17:44:18+08:00
categories: ["AI与技术"]
tags: ["Claude Code", "AI Skills", "人物关系图谱", "Graphviz", "自动化调研", "Vibe Coding", "GLM-4"]
---
昨天在 Twitter 上闲逛，偶然翻到了王树义老师的帖子，他建了个 Claude Skills，可以让 Claude Code 自动完成调研并绘制复杂的（不限于）人物关系图谱，我试了一下，果然好用！

我测试了几个，如下（可以点击图片放大观看）：

> 《红楼梦》关系图谱
> 
> ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBcGooBqMG8VPicJqsXibbNKVIMzRXQ0ibHZI6Q3MkicIbUkCHqf84pGoHGg/640?wx_fmt=png&from=appmsg)

> 《海贼王》关系图谱
> 
> ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBKPLdq20jLL0k7UJDGJ7ZIYOiaZicGT1yhWTQbbSSTIYGQL2epChOTwIw/640?wx_fmt=png&from=appmsg)

> 《火影忍者》关系图谱
> 
> ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBltQNWJiclCUhtlbc4LXpYASW25JgHImZaN8kIOX6sKKXgSfKVoyqxEg/640?wx_fmt=png&from=appmsg)

> 《进击的巨人》关系图谱
> 
> ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBUBJaiaicWqgbtuU3XPHAXTkQXqM0xfVSwOYbfL2r0DMsz0UibyO43pybw/640?wx_fmt=png&from=appmsg)

> 《灵笼》关系图谱
> 
> ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBETRJEbSKK3rkAnhicwUcmS2ZadaOe5OIJ3Tn8DODYYnXjraTKHddJicA/640?wx_fmt=png&from=appmsg)

当然，只要有这些基础数据，就可以放飞想象力，去搞一些好玩的（或者奇奇怪怪）的东西。

比如，把火影忍者的 `.dot` 文件扔给 Gemini 3.0 Pro（Opus 4.5 也行），创建一个可交互的火影忍者网站之类...（刚才随手让 Gemini 做了一个：https://gemini.google.com/share/cbe47322bb6a）

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBwtypGOia0kahvtSibCN1LZicI4eStfkmWyfkwibMz7SSQzKpB8kgQWm3KQ/640?wx_fmt=png&from=appmsg)
![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBWfB6MR7d4y160VkJ0Ywun57KcicS9VUiaRibLlPXGuibsJrFOJJ3GyMDIg/640?wx_fmt=png&from=appmsg)

---

## 实现方法很简单

1.  安装 Graphviz（Mac 系统）：
    ```bash
    brew install graphviz
    ```
2.  把王老师写的这个 skills 放到 Claude Code 的 skills 文件夹里：
    ```
    https://github.com/wshuyi/research-to-diagram
    ```
3.  在 Claude Code 里触发 skills：
    > “深度调研《火影忍者》中的人物关系，并绘制人物关系图谱，最后输入 PDF 文件”
4.  请注意，由于 skills 中是这样写的：
    ![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvB4gLUUqlXYjk7ibu9Y96ZDXqetzxaibJlFibcWelWvFM2cMwxO6uvpia44w/640?wx_fmt=png&from=appmsg)
    因此，需要在描述需求时用到类似的关键词才能正确触发；正确触发时会显示“Research-to-diagram”这个 skill 的名字；skill 完成后会输出 PDF 文件到 local 文件夹中~

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBHyG7wQk22DKPUXUhtpSkLgvYdhLyDbFsM5cLZGQwFkIHdBs0Isn6Dw/640?wx_fmt=png&from=appmsg)

可以看到，我使用 GLM-4 来跑这种简单的 Claude Code 任务或者 skill 的~见 https://models.aigc.green/ | GLM-4 比 Opus 4.5 便宜了将近 20 倍！是真的香！

![](https://mmbiz.qpic.cn/sz_mmbiz_png/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBYjtMJdUSqJCeyEAUmURKEYzZVgZSqZRocGGk9Jvdicja3Sy61M86aFg/640?wx_fmt=png&from=appmsg)

Credit to 王树义老师，原贴在这里：
> https://x.com/wshuyi/status/2007007130969313438

祝玩耍愉快 have fun~

P.S. 再次感慨，有了 Claude Code 的 skills，真的好久没碰 n8n 了。

---

本篇文章由 VS Code（Antigravity）+ uPic + Doocs + COSE 一气呵成！（创作者的心流啊！！！）见：[再见 Obsidian，如何用 VS Code 打造最强个人笔记系统（保姆级教程）](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247492340&idx=1&sn=5b0218145b61bbd9609fe3cce88b4ee8&scene=21#wechat_redirect)

---

欢迎加入我的知识星球，一起快乐的 Vibe Coding 吧~

---

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/ZE6szyic2s2cmiaLyN7AtCdIH3ic5wnJvvBXVPAkLouO5nde87D7b7RNlb9LBKibrSzowmaLsxhxj3OSvpBA2IfvTQ/640?wx_fmt=jpeg&from=appmsg)

打算用一年时间通过 Vibe Coding 打造 50 个实用项目

-   [再见 Obsidian，如何用 VS Code 打造最强个人笔记系统（保姆级教程）](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247492340&idx=1&sn=5b0218145b61bbd9609fe3cce88b4ee8&scene=21#wechat_redirect)
-   [200 个 Nano Banana Pro Prompt 合辑站 + Prompt 爬取工具](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247492170&idx=1&sn=7bc35120cc213aabcfb9187195538542&scene=21#wechat_redirect)
-   [【N 多干货】如何 Vibe Coding 一个 EPUB 转视频播客的 Web 工具站（开发笔记）](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247491026&idx=1&sn=2a312db6daa625bc5345f3bbdaed02f2&scene=21#wechat_redirect)
-   [可以在历史长河中听豆瓣高分历史好书播客了](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247490458&idx=1&sn=bb8dcbabf8a99dbc71f66d2cc65037dd&scene=21#wechat_redirect)
-   [搓了个“Vibe Coding 新手学院”](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247490291&idx=1&sn=131609aeb9bbc01663f38e3ff4747fea&scene=21#wechat_redirect)
-   [Nano Banana Pro Prompt 格式范式升级，顺手 vibe 了一个 JSON Prompt Builder](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247490023&idx=1&sn=b17bdbc0492d65f61ae3b648b1e30052&scene=21#wechat_redirect)
-   [搓了个抖音无水印视频提取器（Mac 版）](https://mp.weixin.qq.com/s?__biz=MzI2NzM4MTQwMg==&mid=2247490347&idx=1&sn=0f388a5eebcab9646c10fd1b895c56d0&scene=21#wechat_redirect)