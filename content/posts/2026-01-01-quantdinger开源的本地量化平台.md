---
title: "QuantDinger—开源的本地量化平台"
date: 2026-01-01T22:03:26+08:00
lastmod: 2026-01-01T22:03:26+08:00
categories: ["AI与技术"]
tags: ["量化交易", "本地部署", "AI研究", "多市场数据", "策略回测", "自动化交易", "Docker", "开源工具"]
---
## 介绍

**QuantDinger** 是一个**本地优先**的量化交易工作空间，专为交易员、研究人员和技术爱好者设计。

与昂贵的 SaaS 平台不同，QuantDinger 将**数据所有权**归还给用户。它具有内置的**基于大语言模型(LLM)的多代理研究团队**，能够自主地从网络收集金融情报，将其与本地市场数据结合，生成专业的分析报告，并无缝集成到您的策略开发、回测和实盘交易流程中。

### 核心价值

*   **隐私优先**：所有策略、交易日志和 API 密钥都存储在您本地的 SQLite 数据库中。
*   **AI赋能**：不仅仅是代码补全，还提供一个真正的 AI 研究分析师（基于 OpenRouter/LLM）。
*   **多市场支持**：原生支持加密**货币**、**美国股票**、**国内/香港股票**、**外汇**和**期货市场**。
*   **开箱即用**：通过 Docker 一键部署，无需复杂的环境配置。

## 可视化展示

### 专业量化仪表盘

实时监控市场动态、资产状况和策略执行状态。

![QuantDinger Dashboard](https://mmbiz.qpic.cn/sz_mmbiz_png/8wiaQU8PwroKNiao7wJ7HtibuNa7OPH5rniaT5ZW7qRiaicWZJjnwITlTiajhrqm70GM0KXJncmPG281vKUbqkpJfgzlQ/640?wx_fmt=png&from=appmsg)

QuantDinger仪表盘

### AI深度研究

多代理协作进行市场情绪与技术分析。

![AI Market Analysis](https://mmbiz.qpic.cn/sz_mmbiz_png/8wiaQU8PwroKNiao7wJ7HtibuNa7OPH5rniajUfjxBZJR26nazKKVuZYPHe5NnXziaNgP5QBEpHwzbrQw5UCrxv7wJA/640?wx_fmt=png&from=appmsg)

### 智能交易助手

自然语言界面，实时市场洞察。

![Trading Assistant](https://mmbiz.qpic.cn/sz_mmbiz_png/8wiaQU8PwroKNiao7wJ7HtibuNa7OPH5rniacSfEQLU7xAWZwbvSwYvxCTFg5pYEMfl4DibralG3RoClkaJRKkHcOaw/640?wx_fmt=png&from=appmsg)

### 交互式指标分析

丰富的技术指标库，支持拖拽分析。

![Indicator Analysis](https://mmbiz.qpic.cn/sz_mmbiz_png/8wiaQU8PwroKNiao7wJ7HtibuNa7OPH5rniaxI2g69WdYZZlJlgl19ialEWhJIicyC0owJuSvgNvyFtic3icQTdgFFqowA/640?wx_fmt=png&from=appmsg)

### Python策略生成

内置编辑器，AI辅助策略编码。

![Code Generation](https://mmbiz.qpic.cn/sz_mmbiz_png/8wiaQU8PwroKNiao7wJ7HtibuNa7OPH5rnia3kWtaCiccmXgIzdOrGzOE9TQH1AAh8wIQjQicmiaLeh2eSG1A5Sa4M32A/640?wx_fmt=png&from=appmsg)

---

## 主要功能

### 1. **通用数据引擎**

不再担心数据 API 的接入问题，QuantDinger 提供强大的数据源工厂模式：

*   **加密货币**：直接 API 连接支持 10 多个交易所，并结合 CCXT 提供 100 多个市场数据源。
*   **股票**：整合了 Yahoo Finance、Finnhub、Tiingo（美国）和 AkShare（国内/香港）。
*   **期货/外汇**：支持 OANDA 及主要期货数据源。
*   **代理支持**：内建代理配置，适配受限网络环境。

### 2. **AI多代理研究**

您的不知疲倦的分析团队：

*   **协调员代理**：分解任务并管理工作流。
*   **研究代理**：进行全网搜索（Google/Bing），收集宏观新闻。
*   **加密/股票代理**：专注于特定市场的技术和资金流分析。
*   **报告生成**：自动生成结构化的每日/每周研究报告。

### 3. **强大的策略运行时**

*   **基于线程的执行器**：独立线程池管理策略执行。
*   **自动恢复**：系统重启后自动恢复运行中的策略。
*   **挂单任务**：可靠的后台队列，确保精确信号执行，防止滑点。

### 4. **现代技术栈**

*   **后端**：Python（Flask）+ SQLite + Redis（可选）— 简单、强大、可扩展。
*   **前端**：Vue 2 + Ant Design Vue + KlineCharts/ECharts — 响应式和交互式。
*   **部署**：Docker Compose 编排。

QuantDinger 提供的强大工具和功能，能够大幅提升量化交易的效率与灵活性，助力交易员与研究人员打造个性化的交易策略，并实现高效的市场分析与决策。

## 支持的交易所与返利

QuantDinger 支持直接连接到主要的加密货币交易所，以实现低延迟的交易执行，同时使用 CCXT 提供广泛的市场数据覆盖。

💡 **独家优惠**：通过下面的合作伙伴链接创建账户，即可享受降低的交易费用和独家奖励。这样做不仅能享受优惠，还能在不增加任何额外费用的情况下支持我们的项目！

#### 交易所 功能 注册链接奖励

*   🥇 **全球最大交易所**
    支持现货、期货、保证金交易
*   🚀 **Web3 & 衍生品平台**
    支持现货、永久合约、期权交易
*   👥 **社交交易**
    支持复制交易、期货交易

#### 其他支持的交易所（直接支持/通过CCXT）：

### 多语言支持

QuantDinger 为全球用户打造，具备全面的国际化支持：

所有界面元素、错误信息和文档都已完全翻译。系统会根据浏览器设置自动检测语言，或可以在应用内手动切换语言。

### 支持的市场

| 市场类型 | 数据源 | 交易支持 |
| :--- | :--- | :--- |
| **加密货币** | Binance、OKX、Bitget 等 100+交易所 | ✅ 完全支持 |
| **美国股票** | Yahoo Finance、Finnhub、Tiingo | ✅ 通过经纪商API支持 |
| **中国/香港股票** | AkShare、东方财富 | ⚡ 仅数据支持 |
| **外汇** | Finnhub、OANDA | ✅ 通过经纪商API支持 |
| **期货** | 交易所API、AkShare | ⚡ 仅数据支持 |

---

### 架构（当前代码库）

```
┌─────────────────────────────┐
│ quantdinger_vue             │
│(Vue2+AntDesignVue)          │
└──────────────┬──────────────┘
               │ HTTP (/api/*)
               ▼
┌─────────────────────────────┐
│ backend_api_python          │
│(Flask+策略执行引擎)         │
└──────────────┬──────────────┘
               │
               ├─SQLite(quantdinger.db)
               ├─Redis(可选缓存)
               └─数据提供商/LLMs/交易所
```

### 仓库结构

```
├─ backend_api_python/ # Flask API + AI + 回测 + 策略运行时
│  ├─ app/ # 应用目录
│  ├─ env.example # 复制到 .env 进行本地配置
│  ├─ requirements.txt # 依赖文件
│  └─ run.py # 入口文件
└─ quantdinger_vue/ # Vue 2 UI（开发服务器代理 /api -> 后端）
```

## 快速开始

### 选项 1：Docker 部署（推荐）

这是启动 QuantDinger 的最快方式。

#### 1. 准备配置

**Linux/macOS:**

```bash
cp docker.env.example backend_api_python/.env
nano backend_api_python/.env
```

**Windows PowerShell:**

```powershell
Copy-Item docker.env.example backend_api_python/.env
notepad backend_api_python/.env
```

**必要设置：**

*   `SECRET_KEY` - 应用程序密钥，使用随机字符串。
*   `ADMIN_USER` / `ADMIN_PASSWORD` - 登录凭证。
*   `OPENROUTER_API_KEY` - OpenRouter API 密钥（AI分析所需）。

#### 2. 构建和启动

```bash
# 构建镜像并启动（首次运行）：
docker-compose up -d --build
# 后续启动（无需重建）：
docker-compose up -d
```

#### 3. 访问应用程序

*   **前端 UI**: http://localhost
*   **后端 API**: http://localhost:5000

#### Docker 命令参考

```bash
# 查看运行状态：
docker-compose ps
# 查看日志：
docker-compose logs -f
# 仅查看后端日志：
docker-compose logs -f backend
# 仅查看前端日志：
docker-compose logs -f frontend
# 停止服务：
docker-compose down
# 停止并移除卷（警告：这将删除数据库！）：
docker-compose down -v
# 重启服务：
docker-compose restart
# 重建并重启：
docker-compose up -d --build
# 进入后端容器：
docker exec -it quantdinger-backend /bin/bash
# 进入前端容器：
docker exec -it quantdinger-frontend /bin/sh
```

#### Docker 架构

```
┌─────────────────┐    ┌─────────────────┐
│前端              │    │后端              │
│(Nginx)          │────▶│(Python)         │
│端口:80          │    │端口:5000        │
└─────────────────┘    └─────────────────┘
        │                    │
        └────────────────────┘
           Docker网络
```

*   **前端**：使用 Vue.js 构建的应用，由 Nginx 提供服务，代理 API 请求到后端。
*   **后端**：使用 Python Flask 提供 API 服务。

#### 数据持久化

以下数据将挂载到主机并在容器重启时保持持久化：

```yaml
volumes:
  - ./backend_api_python/quantdinger.db:/app/quantdinger.db   # 数据库
  - ./backend_api_python/logs:/app/logs                       # 日志
  - ./backend_api_python/data:/app/data                       # 数据目录
  - ./backend_api_python/.env:/app/.env                       # 配置文件
```

#### 自定义配置

**修改端口** - 编辑 `docker-compose.yml` 文件：

```yaml
services:
  frontend:
    ports:
      - "8080:80" # 修改为端口 8080
  backend:
    ports:
      - "5001:5000" # 修改为端口 5001
```

**配置 HTTPS** - 使用反向代理（如 Caddy/Nginx）：

```bash
# 使用 Caddy（自动 HTTPS）
caddy reverse-proxy --from yourdomain.com --to localhost:80
```

#### 生产环境推荐

**安全性：**

```bash
# 生成强密码 SECRET_KEY
openssl rand -hex 32
# 设置安全的管理员密码：
ADMIN_PASSWORD=your-very-secure-password
```

**资源限制** - 添加到 `docker-compose.yml`：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

**日志管理：**

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"
```

#### Docker 排查故障

**前端无法连接到后端：**

```bash
docker-compose logs backend
curl http://localhost:5000/api/health
```

**数据库权限问题：**

```bash
chmod 666 backend_api_python/quantdinger.db
```

**构建失败：**

```bash
# 清理 Docker 缓存并重新构建：
docker-compose build --no-cache
```

**内存不足：**

```bash
# 检查内存使用情况：
docker stats
# 添加交换空间（Linux）：
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 更新

```bash
# 拉取最新代码：
git pull
# 重新构建并重启：
docker-compose up -d --build
```

#### 备份

```bash
# 备份数据库：
cp backend_api_python/quantdinger.db backup/quantdinger_$(date +%Y%m%d).db
# 备份配置文件：
cp backend_api_python/.env backup/.env_$(date +%Y%m%d)
```

### 选项 2：本地开发

#### 前提条件

*   推荐使用 Python 3.10 及以上版本
*   推荐使用 Node.js 16 及以上版本

#### 1. 启动后端（Flask API）

```bash
cd backend_api_python
pip install -r requirements.txt
cp env.example .env   # Windows: 复制 env.example 为 .env
python run.py
```

后端将可以通过 `http://localhost:5000` 访问。

#### 2. 启动前端（Vue UI）

```bash
cd quantdinger_vue
npm install
npm run serve
```

前端开发服务器运行在 `http://localhost:8000`，并将 `/api/*` 请求代理到 `http://localhost:5000`（参见 `quantdinger_vue/vue.config.js` 配置）。

## 配置文件（.env）

使用 `backend_api_python/env.example` 作为模板。常见的配置项包括：

*   **认证**：`SECRET_KEY, ADMIN_USER`, `ADMIN_PASSWORD`
*   **服务器**：`PYTHON_API_HOST`, `PYTHON_API_PORT`, `PYTHON_API_DEBUG`
*   **数据库**：`SQLITE_DATABASE_FILE`（可选；默认为 `backend_api_python/quantdinger.db`）
*   **AI / LLM**：`OPENROUTER_API_KEY, OPENROUTER_MODEL`, timeouts
*   **网页搜索**：`SEARCH_PROVIDER`, `SEARCH_GOOGLE_*`, `SEARCH_BING_API_KEY`
*   **代理（可选）**：`PROXY_PORT` 或 `PROXY_URL`
*   **工作者**：`ENABLE_PENDING_ORDER_WORKER`, `DISABLE_RESTORE_RUNNING_STRATEGIES`

## API

后端提供 REST API 接口，支持登录、市场数据、指标、回测、策略和 AI 分析。

*   健康检查：`GET /health`（也支持 `GET /api/health` 用于部署检查）
*   认证（前端兼容）：`POST /api/user/login`，`POST /api/user/logout`，`GET /api/user/info`

完整路由列表，请查看 `backend_api_python/app/routes/`。

https://github.com/brokermr810/QuantDinger?tab=readme-ov-file