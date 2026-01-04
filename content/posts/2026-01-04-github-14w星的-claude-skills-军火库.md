---
title: "GitHub 1.4w星的 Claude Skills “军火库”"
date: 2026-01-04T12:36:36+08:00
lastmod: 2026-01-04T12:36:36+08:00
categories: ["AI 绘画"]
tags: ["AI绘画", "Stable Diffusion", "Prompt", "提示词", "Midjourney", "文生图", "AI艺术", "教程"]
---

## 什么是 AI 绘画提示词（Prompt）？

AI 绘画提示词（Prompt）是用户输入给 AI 绘画模型（如 Stable Diffusion、Midjourney 等）的文本描述，用于指导模型生成符合预期的图像。

你可以把它理解为向一位“画家”下达的“绘画指令”。指令越清晰、越具体，“画家”创作出的作品就越接近你的想象。

## 为什么提示词如此重要？

提示词是连接人类创意与 AI 生成能力的桥梁。它直接决定了：

*   **生成内容**：画什么（主体、场景）。
*   **画面风格**：怎么画（写实、动漫、油画、水彩）。
*   **构图与细节**：画面布局、光影、质感、色彩等。

掌握提示词技巧，意味着你能够更精准地驾驭 AI，将脑海中的创意高效地转化为视觉作品。

## 提示词的基本结构

一个有效的提示词通常包含以下几个部分，按重要性从前到后排列：

1.  **主体描述**：核心描绘对象，如“一位身着汉服的少女”。
2.  **细节与属性**：对主体的细化，如“精致的妆容、飘逸的长发、手持团扇”。
3.  **场景与环境**：主体所处的背景，如“站在樱花盛开的古典庭院中”。
4.  **艺术风格**：期望的画面风格，如“中国风插画、工笔画风格、柔光”。
5.  **画质与渲染**：技术性参数，如“高清、8K、细节丰富、电影感光影”。
6.  **负面提示词**：明确不希望出现的元素，如“丑陋、畸形、多余的手指、水印”。

## 核心技巧：如何写出高质量的提示词？

### 1. 具体化与细节化

避免使用模糊、宽泛的词汇。用具体的名词、形容词和细节来填充画面。

*   **差**：“一只猫”
*   **优**：“一只毛茸茸的橘猫，睁着圆溜溜的琥珀色大眼睛，好奇地望向镜头，背景是洒满阳光的窗台”

### 2. 使用权重控制

通过语法（如括号 `()`、方括号 `[]`）或特定符号（如 `:`）来调整关键词的重要性。

*   `(keyword)`：增加该关键词的权重（通常乘以1.1）。
*   `((keyword))`：权重更高（约1.21）。
*   `[keyword]`：降低权重。
*   `(keyword:1.5)`：明确指定权重系数为1.5。

**示例**：`(masterpiece), best quality, 1girl, (flowing silver hair:1.3), blue eyes` 会强调“飘逸的银发”。

### 3. 组合与融合概念

尝试将不同领域、风格的元素进行创意组合，往往能产生意想不到的效果。

*   **示例**：“赛博朋克风格的唐代宫殿”、“用乐高积木搭建的梵高《星空》”。

### 4. 善用艺术家与风格名称

在提示词中加入你喜欢的艺术家（如“by Hayao Miyazaki”）、艺术运动（如“Art Nouveau”）或特定风格（如“isometric pixel art”），能快速锁定画面基调。

### 5. 迭代与优化

AI 绘画是一个迭代过程。根据初次生成的结果，调整你的提示词：

*   如果主体不突出，增加其描述权重或细节。
*   如果风格不对，更换或添加更明确的风格词。
*   如果出现瑕疵，在负面提示词中加以限制。

## 进阶：提示词工程

### 1. 结构化提示词

将提示词分块编写，逻辑更清晰，便于调整：

```
[主体与核心细节], [场景与环境], [艺术风格与媒介], [画质与渲染参数], [色彩与光影]
```

### 2. 使用触发词与 LoRA 模型

*   **触发词**：某些特定模型或 LoRA 需要对应的触发词来激活其特性，例如“`chilloutmix`”模型常用“`masterpiece, best quality`”开头。
*   **LoRA**：小型模型文件，用于实现特定画风、人物或概念。使用时需在提示词中引用其名称，如 `<lora:japanese_anime_style:0.7>`。

### 3. 探索负面提示词的威力

一个强大的负面提示词可以显著提升画面质量，过滤掉常见缺陷。一个通用的高质量负面提示词示例：

```
(worst quality, low quality:1.4), (bad anatomy), inaccurate limb, (bad hands), missing fingers, extra digit, fewer digits, (mutated hands and fingers:1.5), disconnected limbs, mutation, ugly, disgusting, blurry, amputation, text, watermark, signature
```

## 常用高质量提示词分类参考

### 画质与通用正向词
```
masterpiece, best quality, ultra-detailed, 8K, HDR, sharp focus
```

### 艺术风格
*   **写实摄影**：`photorealistic, 35mm film, f/2.8, depth of field`
*   **动漫/二次元**：`anime style, manga, cel-shading, vibrant colors`
*   **油画**：`oil painting, impasto, by Van Gogh`
*   **水彩**：`watercolor painting, soft edges, fluid colors`
*   **概念艺术**：`concept art, matte painting, cinematic, epic composition`

### 光照与氛围
```
dramatic lighting, volumetric fog, god rays, sunset glow, neon lights, studio lighting
```

### 视角与构图
```
extreme close-up, bird's-eye view, Dutch angle, rule of thirds, symmetrical composition
```

## 总结

1.  **清晰具体**是 Prompt 的灵魂。
2.  **结构化和权重**是控制画面的方向盘。
3.  **迭代优化**是通向理想成图的必经之路。
4.  **善用负面提示词**能事半功倍。
5.  多观察优秀作品，分析其提示词，是快速提升的最佳途径。

AI 绘画是创意与技术的结合。掌握提示词，就是掌握了释放 AI 无限潜力的钥匙。现在，开始你的创作吧！

---
*来源：小红书*