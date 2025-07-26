# AllStory 📖

> 一个专为TRPG设计的可控AI助手，致力于成为你最得力的DM/KP。

### ✨ 项目简介 (Introduction)

在TRPG（桌面角色扮演游戏）的世界里，城主（DM）或守秘人（KP）是灵魂人物，但他们也面临着巨大的挑战：繁重的世界观构建、即时响应玩家天马行空操作的压力、以及在长团中维持NPC和剧情一致性的困难。

传统的通用大语言模型（LLM）虽然强大，但其输出的“自由度”过高，往往导致剧情偏离、角色OOC（Out of Character）等问题，难以满足严肃跑团所需的可控性。

**AllStory** 正是为此而生。我们采用了一种创新的**“每回合无状态（Stateless）生成”**范式，彻底解决了长上下文带来的记忆污染和幻觉问题。在每一回合，AllStory都会根据精确管理的世界观、短期记忆和长期关键事件，从零开始构建一个“绝对干净”的上下文（Prompt），交给AI进行生成。这确保了：

* **高度可控性**：DM/KP可以精准地控制剧情走向和世界状态。
* **长期一致性**：核心设定和关键记忆永不丢失，NPC人设稳定。
* **动态与创意**：在严格的逻辑框架内，AI依然能迸发出惊人的创意，为你的故事增添无限可能。

### 🛡️ 徽章 (Badges)

<!-- 
    徽章 (Badges) 是展示项目状态的图标，非常专业。你需要进行一些简单的配置来激活它们。
-->

<!-- 
    许可证 (License): 徽章会显示你的项目使用的开源许可证。
    **这是什么？** 它定义了其他人可以如何使用、修改和分发你的代码。如果你没有，其他人会不清楚是否能合法使用你的项目。
    **如何获得？** 
    1. 在你的项目根目录创建一个名为 `LICENSE` 的文件。
    2. 选择一个许可证。对于开源项目，`MIT License` 是一个非常流行且宽松的选择。你可以从 https://choosealicense.com/licenses/mit/ 复制MIT许可证的文本，粘贴到你的`LICENSE`文件中，并将年份和你的名字/团队名填上。
    3. 一旦你添加了`LICENSE`文件，下面的徽章就会生效。
-->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- 
    构建状态 (Build Status): 这个徽章显示你的代码最新提交后是否能成功构建和测试。
    **这是什么？** 它来自持续集成/持续部署 (CI/CD) 服务，如 GitHub Actions。
    **如何获得？** 
    1. 在你的项目根目录创建一个 `.github/workflows` 文件夹。
    2. 在该文件夹中创建一个 `main.yml` 或 `ci.yml` 文件，定义自动化流程（例如：安装依赖 -> 运行测试）。
    3. GitHub Actions 会根据这个文件自动运行。配置完成后，你可以从Actions页面获取这个徽章的Markdown代码。
    **下面的链接是占位符，你需要替换它。**
-->

[![Build Status](https://github.com/YOUR_USERNAME/AllStory/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/AllStory/actions/workflows/ci.yml)

<!-- 
    代码覆盖率 (Code Coverage): 显示你的自动化测试覆盖了多少比例的代码。
    **这是什么？** 它衡量你的测试的完善程度。
    **如何获得？** 
    1. 使用 `pytest-cov` 等工具生成覆盖率报告。
    2. 将报告上传到 `Codecov` 或 `Coveralls` 等第三方服务。
    3. 从这些服务获取徽章链接。
    **下面的链接是占位符，你需要替换它。**
-->

[![codecov](https://codecov.io/gh/YOUR_USERNAME/AllStory/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/AllStory)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js-black.svg)](https://nextjs.org/)

### ⚙️ 核心架构与技术实现 (How It Works)

AllStory的核心是一个精巧的**回合制循环系统**。我们放弃了让AI处理冗长对话历史的传统做法，转而在每一回合都为AI“量身定做”一份全新的、高度浓缩的记忆和指令。

整个流程如下：

1. **前端交互**: 玩家通过 **Next.js** 构建的前端界面输入操作。

2. **后端并发处理**: **FastAPI** 接收到请求后，通过 `asyncio.gather` 并发执行两个核心任务：

   * **任务A: 判定与生成 (The Judgment & Generation Pipeline)**

     1. **输入分析 (`API-1`)**: 使用强引导性的Prompt，让Kimi模型判断玩家输入是否需要进行“技能判定”，并结构化地输出判定的类型、数量和难度。
     2. **规则裁定**: Python后端解析`API-1`的输出，结合预设的角色卡和技能列表，通过代码逻辑完成“摇骰子”，得出成功或失败的结果。
     3. **上下文构建**: 这是AllStory的魔法核心。程序会自动组合以下元素，形成一个全新的Prompt：

        * **AI友好的世界观**: 经过特殊设计的世界观描述，更易于AI理解和遵循。
        * **短期记忆 (Queue)**: 一个存储过去10回合交互记录的`.txt`文件，形成流畅的对话上下文。
        * **长期记忆 (JSON Switch)**: 一个开关式的JSON数据库。它以地理坐标节点的形式组织，记录了主线/支线任务的完成状态、关键NPC的生死等。系统仅加载玩家当前位置相关的JSON节点，极大地节约了Token并保证了相关性。
     4. **内容生成 (`API-2`)**: 将这份“完美上下文”发送给Kimi模型，生成本回合的剧情描述和NPC对话。

   * **任务B: 记忆沉淀 (The Memory Solidification Pipeline)**

     1. 在后台，第三个模型(`API-3`)会分析**上一回合**的交互内容。
     2. 它负责判断哪些信息需要超越10回合的短期记忆限制，成为永久记忆（例如：一个重要NPC的死亡，一个地标的摧毁）。
     3. 这些信息会被更新到长期记忆的JSON文件中。这个机制巧妙地模拟了人类的“遗忘曲线”，非核心信息会随时间自然淡出，让体验更真实，同时避免了无关信息干扰AI的判断。

3. **结果返回**: 任务A生成的AI输出，与规则裁定的骰子结果（如“魅力鉴定：1d20+2=15，成功！”）相结合，最终呈现给玩家一个完整、沉浸的回合体验。

### 🚀 快速上手 (Getting Started)

#### 环境要求

* Python 3.8+
* Node.js 和 npm/yarn (用于前端)
* Kimi / Moonshot AI 的 API Key

#### 安装与运行

1. **克隆仓库**

   ```bash
   git clone https://github.com/YOUR_USERNAME/AllStory.git
   cd AllStory
   ```

2. **后端设置 (FastAPI)**

   ```bash
   # 进入后端目录
   cd backend 

   # (推荐) 创建并激活虚拟环境
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # 安装依赖
   pip install -r requirements.txt

   # 配置API Key
   cp .env.example .env
   ```

   然后，编辑`.env`文件，填入你的`MOONSHOT_API_KEY`。

3. **前端设置 (Next.js)**

   ```bash
   # 进入前端目录
   cd ../frontend

   # 安装依赖
   npm install
   ```

4. **启动服务**

   * **启动后端API服务:**

     ```bash
     # 在 backend 目录下运行
     uvicorn main:app --reload --host 0.0.0.0 --port 8000
     ```
   * **启动前端开发服务:**

     ```bash
     # 在 frontend 目录下运行
     npm run dev
     ```

   现在，你可以在浏览器中打开 `http://localhost:3000` 来体验AllStory了！

### 🗺️ 未来计划 (Roadmap)

* [ ] 开发更友好的Web界面，支持拖拽式角色卡管理。
* [ ] 集成更多TRPG规则，如《龙与地下城》(D\&D) 和《克苏鲁的呼唤》(CoC)。
* [ ] 探索本地化模型部署，降低对API的依赖。
* [ ] 引入矢量数据库，实现更智能的长期记忆检索。
* [ ] 支持多人协作DM模式。

### 🤝 贡献指南 (Contributing)

我们欢迎任何形式的贡献！无论是提交Bug报告、提出新功能建议，还是直接贡献代码。请阅读我们的 `CONTRIBUTING.md` (待创建) 文件以了解详细信息。

### 📜 许可证 (License)

本项目采用 [MIT License](./LICENSE) 开源许可证。
