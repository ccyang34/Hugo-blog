---
title: "量化交易大冒险-FamaFrench因子模型篇"
date: 2026-08-05T15:27:40+08:00
lastmod: 2026-08-05T15:27:40+08:00
categories: ["量化"]
tags: ["量化", "多因子", "因子", "量化选股", "投资策略", "量化策略"]
---

真是的，大雄！你又蹲在地上对着空钱包叹气？不就是买了大公司的股票以为稳赚，结果反而亏了买新漫画的钱嘛！

喂喂，别抱着头就想钻时光抽屉！上次教你的 APT 太复杂，这次我教你个超好用的法宝——Fama-French 三因子模型！

它可比 CAPM 厉害多了！除了大盘涨跌，还发现两个赚钱秘密：小公司比大公司涨得快，就像小个子同学进步空间更大；便宜的股票比贵的更划算，就像打折的铜锣烧性价比更高！

量化交易用它，一眼就能找出又小又便宜的好股票，再也不用瞎买大公司当冤大头，稳稳攒够买漫画和我的铜锣烧的零花钱啦！

量化金融—资产定价模型 Chapter 3

ドラえもんのうた (哆啦A梦之歌) (TV Version)

![图片1](https://mmbiz.qpic.cn/sz_mmbiz_png/rFibyZZ6fR61sPP9icZT7AVKqfniciaHib1diaNmnR8NcbOl74V33sMomMWwkXVzMag7FdBNqP4kwlMGx9NLE2TNs06uEP7O1kASpmKD3iazZetpBQ/0?wx_fmt=png&from=appmsg)

![图片2](https://mmbiz.qpic.cn/mmbiz_png/rFibyZZ6fR62UBFhNFiaqXBQIaJFdX10MUVWn0Wvam3MCwOuDZDe6icfDWjxAjDXYoJzhic2TaSuYd4pNibNDibHzLWCW5ezHwak0wDjHhZmyhlB8/0?wx_fmt=png&from=appmsg)

![图片3](https://mmbiz.qpic.cn/sz_mmbiz_png/rFibyZZ6fR63gxI34Q6ncXjshCpiaHrzT58riann0fUKvibCFNm0AiasYROBEVVRWZuVvGhBtovaWLCoDxheR2E4ej1gFBYYR7dqPciahJvLRqGD8/0?wx_fmt=png&from=appmsg)

![图片4](https://mmbiz.qpic.cn/mmbiz_png/rFibyZZ6fR63MEnIq6BFor4HKibtnib0BO0S7O9icmRVxZtUia6c3NlvntTqeKuwyqLKyLwX7I9hQ7N40WwvhS4o8SGQaib1LlyxqjKl0EZGpgdZs/0?wx_fmt=png&from=appmsg)

![图片5](https://mmbiz.qpic.cn/mmbiz_png/rFibyZZ6fR60C7LicpSmnF9Wp3m5nUIeEGmwicd6ehk1ITqYfEL5sFSTbSUo4fMdnuVgSGRmumnQxVngzHKiaM4zd2lodBX2Ie2VLoKyfuicYTgg/0?wx_fmt=png&from=appmsg)

![图片6](https://mmbiz.qpic.cn/sz_mmbiz_png/rFibyZZ6fR606q2DkShrAib8W2YL7nzt4rsE3J7sKPP5xecmfQicIs7T3toG6qK1ibEJDwCanicmpxKccgFeaO0A0YanKn5JoJrZh4TScXm7Bq5c/0?wx_fmt=png&from=appmsg)

![图片7](https://mmbiz.qpic.cn/mmbiz_png/rFibyZZ6fR60Ajibouw3LPnJPkf4h4G5wD5hE2SYbfJsiahs91LrxY3hhdicUoAlqKZTfK1uriaWIh0wPIG0znFVantghtjkUQ0yrwuDqeR5G7PA/0?wx_fmt=png&from=appmsg)

![图片8](https://mmbiz.qpic.cn/mmbiz_png/rFibyZZ6fR63klQQYz0LeQTcgX7WumtyVozWfXIvwzFhvkQ9ibEfMtn3bwmqOiaxvbp9nwMXuacldfP3dVQJOnicGDRxsJFicQtibNsNQLBS8WgYs/0?wx_fmt=png&from=appmsg)

---
*来源: [微信公众号](https://mp.weixin.qq.com/s/1TSr9Z8e-zXTIipsDddl0w)*