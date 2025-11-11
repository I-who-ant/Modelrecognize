# 🎓 Kimi CLI 系统学习计划

**学习目标**: 深入掌握 Kimi CLI 的核心技术，为贡献代码和扩展功能打下坚实基础

**总学习时长**: 8-12 周（每周 10-15 小时）

**难度**: ⭐⭐⭐⭐☆ (中高级)

---

## 📋 学习计划总览

本学习计划分为 **6 个阶段**，**15 个模块**，**60+ 个学习点**。

```
阶段1: 基础准备（1-2周）
  └─ 模块01: Python 3.13+ 现代特性
  └─ 模块02: 异步编程基础

阶段2: CLI开发（1-2周）
  └─ 模块03: Click 命令行框架
  └─ 模块04: Prompt Toolkit 交互式界面
  └─ 模块05: Rich 富文本显示

阶段3: LLM应用开发（2-3周）
  └─ 模块06: Prompt Engineering
  └─ 模块07: Function Calling 工具调用
  └─ 模块08: Streaming 流式处理

阶段4: 协议与标准（1-2周）
  └─ 模块09: Agent Client Protocol (ACP)
  └─ 模块10: Model Context Protocol (MCP)
  └─ 模块11: Wire Protocol

阶段5: Kimi CLI 核心架构（2-3周）
  └─ 模块12: CLI 层与 App 层
  └─ 模块13: Soul 层（Agent 核心）
  └─ 模块14: Tools 工具系统
  └─ 模块15: Kosong 框架

阶段6: 实战与扩展（2-3周）
  └─ 实战项目1: 开发自定义工具
  └─ 实战项目2: 实现自定义 Agent
  └─ 实战项目3: 开发 MCP 服务器
  └─ 实战项目4: 贡献开源代码
```

---

## 📂 学习模块目录结构

```
kimi-cli-learn/
├── README.md                          # 本文件（学习计划总览）
├── 学习路线图.md                       # 详细学习路径和里程碑
│
├── 阶段1_基础准备/
│   ├── 01_Python现代特性/
│   │   ├── README.md                  # 模块学习指南
│   │   ├── 01_类型系统.md             # Type Hints, Literal, get_args
│   │   ├── 02_数据类.md               # dataclass, Pydantic
│   │   ├── 03_上下文管理器.md          # contextlib, 自定义管理器
│   │   ├── 04_生成器与迭代器.md        # yield, Generator, Iterator
│   │   └── 代码实践/                   # 练习代码
│   │       ├── type_hints_practice.py
│   │       ├── dataclass_practice.py
│   │       └── ...
│   │
│   └── 02_异步编程/
│       ├── README.md
│       ├── 01_asyncio基础.md          # async/await, 事件循环
│       ├── 02_异步IO.md               # aiohttp, aiofiles
│       ├── 03_并发控制.md              # gather, wait, Task
│       ├── 04_异步生成器.md            # async for, AsyncGenerator
│       └── 代码实践/
│           ├── async_http.py
│           ├── async_file_io.py
│           └── ...
│
├── 阶段2_CLI开发/
│   ├── 03_Click框架/
│   │   ├── README.md
│   │   ├── 01_基础用法.md             # @click.command, @click.option
│   │   ├── 02_参数类型.md              # Path, Choice, IntRange
│   │   ├── 03_子命令.md                # @click.group
│   │   ├── 04_上下文传递.md            # @click.pass_context
│   │   └── 代码实践/
│   │       ├── basic_cli.py
│   │       ├── multi_command_cli.py
│   │       └── kimi_cli_params_analysis.md  # 分析 Kimi CLI 参数设计
│   │
│   ├── 04_PromptToolkit/
│   │   ├── README.md
│   │   ├── 01_基础输入.md             # PromptSession
│   │   ├── 02_自动补全.md              # Completer
│   │   ├── 03_快捷键绑定.md            # KeyBindings
│   │   ├── 04_自定义样式.md            # Style, ANSI colors
│   │   └── 代码实践/
│   │       ├── interactive_shell.py
│   │       ├── file_completer.py
│   │       └── kimi_shell_mode_analysis.md
│   │
│   └── 05_Rich显示/
│       ├── README.md
│       ├── 01_基础显示.md             # Console, print
│       ├── 02_Markdown渲染.md         # Markdown
│       ├── 03_进度条.md                # Progress
│       ├── 04_表格与面板.md            # Table, Panel
│       └── 代码实践/
│           ├── rich_output.py
│           └── kimi_ui_analysis.md
│
├── 阶段3_LLM应用开发/
│   ├── 06_PromptEngineering/
│   │   ├── README.md
│   │   ├── 01_System_Prompt设计.md    # 角色定义、指令
│   │   ├── 02_Few_Shot示例.md         # 示例学习
│   │   ├── 03_Chain_of_Thought.md     # 思维链
│   │   ├── 04_ReAct_Pattern.md        # Reasoning + Acting
│   │   └── 代码实践/
│   │       ├── system_prompt_examples.md
│   │       ├── few_shot_learning.py
│   │       └── kimi_agent_spec_analysis.md  # 分析 Kimi 的 Agent 规范
│   │
│   ├── 07_FunctionCalling/
│   │   ├── README.md
│   │   ├── 01_OpenAI_Function_Calling.md  # 格式与原理
│   │   ├── 02_工具定义.md              # JSON Schema
│   │   ├── 03_工具调用流程.md          # 调用、执行、返回
│   │   ├── 04_错误处理.md              # 重试、回退
│   │   └── 代码实践/
│   │       ├── tool_definition.py
│   │       ├── function_calling_demo.py
│   │       └── kimi_tools_analysis.md
│   │
│   └── 08_Streaming流式处理/
│       ├── README.md
│       ├── 01_SSE协议.md              # Server-Sent Events
│       ├── 02_流式解析.md              # 逐块处理
│       ├── 03_异步流.md                # AsyncGenerator
│       ├── 04_实时显示.md              # 渐进式输出
│       └── 代码实践/
│           ├── sse_client.py
│           ├── stream_parser.py
│           └── kimi_streaming_analysis.md
│
├── 阶段4_协议与标准/
│   ├── 09_ACP协议/
│   │   ├── README.md
│   │   ├── 01_协议概述.md             # ACP 是什么
│   │   ├── 02_消息格式.md              # JSON-RPC 2.0
│   │   ├── 03_生命周期.md              # 连接、请求、响应
│   │   ├── 04_工具调用.md              # Tool Use
│   │   ├── 05_IDE集成.md              # Zed、Cursor
│   │   └── 代码实践/
│   │       ├── acp_server.py          # 简单 ACP 服务器
│   │       ├── acp_client.py          # ACP 客户端
│   │       └── kimi_acp_implementation.md  # 分析 Kimi 的 ACP 实现
│   │
│   ├── 10_MCP协议/
│   │   ├── README.md
│   │   ├── 01_协议概述.md             # MCP 是什么
│   │   ├── 02_工具定义.md              # Tool Schema
│   │   ├── 03_资源管理.md              # Resources
│   │   ├── 04_Prompts模板.md          # Prompt Templates
│   │   ├── 05_开发MCP服务器.md        # fastmcp
│   │   └── 代码实践/
│   │       ├── mcp_server_basic.py    # 基础 MCP 服务器
│   │       ├── mcp_server_advanced.py # 高级功能
│   │       └── kimi_mcp_integration.md
│   │
│   └── 11_Wire协议/
│       ├── README.md
│       ├── 01_协议概述.md             # Wire Protocol 介绍
│       ├── 02_消息格式.md              # 数据结构
│       ├── 03_通信流程.md              # 请求-响应
│       └── 代码实践/
│           └── kimi_wire_server_analysis.md
│
├── 阶段5_Kimi_CLI核心架构/
│   ├── 12_CLI层与App层/
│   │   ├── README.md
│   │   ├── 01_cli_py源码分析.md       # 入口、参数解析
│   │   ├── 02_app_py源码分析.md       # KimiCLI 类
│   │   ├── 03_Session管理.md          # 会话生命周期
│   │   ├── 04_Config配置.md           # 配置加载与管理
│   │   └── 代码实践/
│   │       ├── custom_cli_params.py   # 添加自定义参数
│   │       └── session_playground.py
│   │
│   ├── 13_Soul层/
│   │   ├── README.md
│   │   ├── 01_kimisoul_py源码分析.md  # Agent 执行引擎
│   │   ├── 02_agent_py源码分析.md     # Agent 规范加载
│   │   ├── 03_context_py源码分析.md   # 上下文管理
│   │   ├── 04_runtime_py源码分析.md   # 运行时环境
│   │   ├── 05_工具调用流程.md          # 完整调用链
│   │   └── 代码实践/
│   │       ├── custom_agent.md        # 自定义 Agent 规范
│   │       ├── agent_execution_demo.py
│   │       └── tool_call_trace.md     # 追踪工具调用
│   │
│   ├── 14_Tools工具系统/
│   │   ├── README.md
│   │   ├── 01_文件工具.md              # read, write, patch, grep, glob
│   │   ├── 02_Bash工具.md             # 命令执行
│   │   ├── 03_Task工具.md             # 子 Agent
│   │   ├── 04_Todo工具.md             # 任务管理
│   │   ├── 05_Web工具.md              # 搜索、抓取
│   │   ├── 06_Think工具.md            # 内部推理
│   │   ├── 07_MCP工具.md              # MCP 集成
│   │   └── 代码实践/
│   │       ├── custom_tool_development.md  # 开发自定义工具
│   │       ├── my_custom_tool.py
│   │       └── tool_integration_test.py
│   │
│   └── 15_Kosong框架/
│       ├── README.md
│       ├── 01_框架概述.md             # Kosong 是什么
│       ├── 02_ChatProvider抽象.md     # 统一接口
│       ├── 03_LLM实现.md              # Kimi, OpenAI, Anthropic
│       ├── 04_流式支持.md              # Streaming
│       ├── 05_提示词缓存.md            # Prompt Caching
│       └── 代码实践/
│           ├── kosong_usage.py        # 使用示例
│           ├── custom_provider.py     # 实现自定义 Provider
│           └── kosong_vs_langchain.md # 对比分析
│
└── 阶段6_实战与扩展/
    ├── 实战项目1_自定义工具/
    │   ├── README.md
    │   ├── 需求设计.md
    │   ├── 工具实现/
    │   │   ├── tools/code_analyzer.py    # 代码分析工具
    │   │   └── tests/
    │   └── 集成测试.md
    │
    ├── 实战项目2_自定义Agent/
    │   ├── README.md
    │   ├── Agent规范设计.md
    │   ├── agents/code_reviewer.md       # 代码审查 Agent
    │   └── 测试与优化.md
    │
    ├── 实战项目3_MCP服务器/
    │   ├── README.md
    │   ├── 服务器设计.md
    │   ├── mcp_servers/
    │   │   └── database_mcp_server.py    # 数据库操作 MCP 服务器
    │   └── 部署与测试.md
    │
    └── 实战项目4_贡献代码/
        ├── README.md
        ├── 01_Fork与环境搭建.md
        ├── 02_Issue选择与分析.md
        ├── 03_功能开发.md
        ├── 04_测试与文档.md
        └── 05_提交PR.md
```

---

## 🎯 学习目标拆解

### 阶段1: 基础准备（1-2周）

**目标**: 掌握 Python 3.13+ 现代特性和异步编程

**输出**:
- ✅ 能熟练使用类型系统（Type Hints, Literal, Union）
- ✅ 掌握 dataclass 和 Pydantic 数据验证
- ✅ 理解异步编程模型（async/await）
- ✅ 能编写异步 HTTP 和文件 I/O 代码

**考核**: 实现一个异步爬虫，抓取多个网页并保存

---

### 阶段2: CLI开发（1-2周）

**目标**: 掌握现代 CLI 开发技术栈

**输出**:
- ✅ 能使用 Click 构建复杂的命令行应用
- ✅ 掌握 Prompt Toolkit 实现交互式界面
- ✅ 能用 Rich 创建美观的终端输出

**考核**: 开发一个交互式文件管理器 CLI

---

### 阶段3: LLM应用开发（2-3周）

**目标**: 理解 LLM 应用开发核心技术

**输出**:
- ✅ 能设计高质量的 System Prompt
- ✅ 理解 Function Calling 原理和实现
- ✅ 能处理流式响应并实时显示

**考核**: 实现一个支持工具调用的 AI 对话应用

---

### 阶段4: 协议与标准（1-2周）

**目标**: 深入理解 ACP、MCP、Wire 协议

**输出**:
- ✅ 理解 ACP 协议规范和实现
- ✅ 能开发 MCP 服务器
- ✅ 了解 Wire 协议通信机制

**考核**: 开发一个简单的 MCP 工具服务器，并与 Kimi CLI 集成

---

### 阶段5: Kimi CLI 核心架构（2-3周）

**目标**: 深入理解 Kimi CLI 源码

**输出**:
- ✅ 理解 CLI/App/Soul 三层架构
- ✅ 掌握 Agent 执行流程
- ✅ 能开发自定义工具
- ✅ 理解 Kosong 框架设计

**考核**: 为 Kimi CLI 添加一个自定义工具并提交 PR

---

### 阶段6: 实战与扩展（2-3周）

**目标**: 综合应用，贡献开源

**输出**:
- ✅ 完成 4 个实战项目
- ✅ 至少 1 个 PR 被合并
- ✅ 形成自己的技术积累

**考核**: 贡献代码到 Kimi CLI 项目

---

## 📊 学习进度追踪

| 阶段 | 模块 | 状态 | 完成时间 | 笔记链接 |
|-----|------|------|---------|---------|
| 阶段1 | 01_Python现代特性 | ⏸️ 未开始 | - | - |
| 阶段1 | 02_异步编程 | ⏸️ 未开始 | - | - |
| 阶段2 | 03_Click框架 | ⏸️ 未开始 | - | - |
| 阶段2 | 04_PromptToolkit | ⏸️ 未开始 | - | - |
| 阶段2 | 05_Rich显示 | ⏸️ 未开始 | - | - |
| 阶段3 | 06_PromptEngineering | ⏸️ 未开始 | - | - |
| 阶段3 | 07_FunctionCalling | ⏸️ 未开始 | - | - |
| 阶段3 | 08_Streaming流式处理 | ⏸️ 未开始 | - | - |
| 阶段4 | 09_ACP协议 | ⏸️ 未开始 | - | - |
| 阶段4 | 10_MCP协议 | ⏸️ 未开始 | - | - |
| 阶段4 | 11_Wire协议 | ⏸️ 未开始 | - | - |
| 阶段5 | 12_CLI层与App层 | ⏸️ 未开始 | - | - |
| 阶段5 | 13_Soul层 | ⏸️ 未开始 | - | - |
| 阶段5 | 14_Tools工具系统 | ⏸️ 未开始 | - | - |
| 阶段5 | 15_Kosong框架 | ⏸️ 未开始 | - | - |
| 阶段6 | 实战项目1 | ⏸️ 未开始 | - | - |
| 阶段6 | 实战项目2 | ⏸️ 未开始 | - | - |
| 阶段6 | 实战项目3 | ⏸️ 未开始 | - | - |
| 阶段6 | 实战项目4 | ⏸️ 未开始 | - | - |

**图例**:
- ⏸️ 未开始
- 🔄 进行中
- ✅ 已完成
- ⚠️ 遇到困难

---

## 💡 学习方法建议

### 1. 理论与实践结合

- 📖 **30% 时间看文档和理论**
- 💻 **70% 时间写代码和实践**

### 2. 源码阅读策略

**三步走**:
1. **宏观理解**: 先看架构图和整体流程
2. **中观分析**: 逐个模块阅读核心代码
3. **微观深入**: 理解关键算法和设计模式

**工具**:
- VSCode + Python Extension
- 使用 Debug 模式单步调试
- 使用 `git log` 查看提交历史

### 3. 渐进式学习

**不要跳跃**:
- 阶段1完成80%以上再进入阶段2
- 每个模块完成练习代码
- 遇到困难及时记录和求助

### 4. 输出倒逼输入

**学习输出**:
- ✅ 每个模块写学习笔记
- ✅ 实践代码提交到 Git
- ✅ 写技术博客
- ✅ 分享给他人（最佳学习方式）

### 5. 社区参与

**积极参与**:
- GitHub Issues: 提问和回答
- 加入 Discord/Telegram 群组
- 参加线上分享会
- 写 PR 贡献代码

---

## 📚 推荐学习资源

### 官方文档

- **Kimi CLI**: https://github.com/MoonshotAI/kimi-cli
- **ACP 协议**: https://agentclientprotocol.github.io/
- **MCP 协议**: https://modelcontextprotocol.io/
- **Python 3.13**: https://docs.python.org/3.13/

### 书籍

- 《Fluent Python》(第2版): Python 高级特性
- 《Python Asyncio》: 异步编程深入
- 《Building LLM Powered Applications》: LLM 应用开发

### 在线课程

- Real Python: Python 高级教程
- FastAPI 官方教程: 异步 Web 开发
- LangChain 文档: Agent 架构参考

### 技术博客

- MoonshotAI 技术博客
- Anthropic 技术博客
- OpenAI 开发者博客

---

## 🆘 遇到问题怎么办？

### 问题解决流程

1. **自己调试**: 使用 Debug、日志、print
2. **查阅文档**: 官方文档、源码注释
3. **搜索引擎**: Google、Stack Overflow
4. **社区求助**: GitHub Issues、Discord
5. **请教老王**: 我随时在线！😄

### 常见问题 FAQ

**Q1: Python 3.13 安装失败？**
- 使用 pyenv 管理多版本 Python
- 参考官方安装文档

**Q2: 异步编程难以理解？**
- 从同步代码开始，逐步改造
- 使用 asyncio.run() 简化入门
- 多写实践代码

**Q3: 源码太复杂看不懂？**
- 从入口开始，使用 Debug 单步执行
- 画架构图和流程图
- 先理解核心流程，忽略细节

**Q4: 如何找到合适的 Issue？**
- 找 `good first issue` 标签
- 从文档优化开始
- 先修小 bug，再加新功能

---

## 🎉 学习里程碑

### 🏆 初级里程碑（2周）

- ✅ 完成阶段1和阶段2
- ✅ 能开发基本的 CLI 应用
- ✅ 理解异步编程基础

### 🏆 中级里程碑（6周）

- ✅ 完成阶段3、4、5
- ✅ 理解 Kimi CLI 核心架构
- ✅ 能开发自定义工具

### 🏆 高级里程碑（12周）

- ✅ 完成所有6个阶段
- ✅ 至少1个 PR 被合并
- ✅ 能独立扩展 Kimi CLI

---

## 📝 学习日志模板

**日期**: 2025-01-10

**今日学习**:
- 阶段: 阶段1
- 模块: 01_Python现代特性
- 主题: 类型系统
- 时长: 2小时

**学习内容**:
- Type Hints 基础语法
- Literal 类型使用
- Union 和 Optional

**实践代码**:
- type_hints_practice.py

**遇到问题**:
- get_args() 使用不熟悉

**解决方案**:
- 查阅官方文档
- 写测试代码验证

**明天计划**:
- 学习 dataclass
- 完成练习代码

---

## 🚀 开始学习

**第一步**: 阅读完本 README

**第二步**: 查看 `学习路线图.md` 了解详细路径

**第三步**: 进入 `阶段1_基础准备/01_Python现代特性/` 开始学习

**第四步**: 按模块逐步推进，完成练习代码

**第五步**: 定期更新学习进度追踪表

---

**加油！为贡献代码打下坚实基础！💪**

*Created by 老王 | Last Updated: 2025-01-10*
