# 🗺️ Kimi CLI 学习路线图

**本文档**: 详细的学习路径、时间安排和检查点

---

## 📅 时间规划总览（12周）

```
Week 1-2:  阶段1 - 基础准备
Week 3-4:  阶段2 - CLI开发
Week 5-7:  阶段3 - LLM应用开发
Week 8-9:  阶段4 - 协议与标准
Week 10-11: 阶段5 - Kimi CLI核心架构
Week 12+:   阶段6 - 实战与扩展
```

---

## 🎯 阶段1: 基础准备（Week 1-2）

### Week 1: Python 3.13+ 现代特性

#### Day 1-2: 类型系统
- [ ] **学习目标**: 掌握 Python 类型系统
- [ ] **学习内容**:
  - Type Hints 基础（int, str, list, dict）
  - 泛型类型（List[str], Dict[str, int]）
  - Literal 类型（精确值限定）
  - Union 和 Optional
  - get_args() 和 get_origin()
- [ ] **实践任务**:
  ```python
  # 练习1: 实现一个类型安全的配置类
  from typing import Literal, Union, get_args

  ConfigType = Literal["dev", "prod", "test"]

  class Config:
      def __init__(self, env: ConfigType):
          if env not in get_args(ConfigType):
              raise ValueError(f"Invalid env: {env}")
          self.env = env
  ```
- [ ] **检查点**: 能熟练使用类型注解，并理解 mypy/pyright 类型检查

#### Day 3-4: 数据类
- [ ] **学习目标**: 掌握 dataclass 和 Pydantic
- [ ] **学习内容**:
  - dataclass 基础用法
  - dataclass 高级特性（slots, frozen, post_init）
  - Pydantic 模型定义
  - Pydantic 验证和序列化
- [ ] **实践任务**:
  ```python
  # 练习2: 实现 Kimi CLI 的配置模型
  from dataclasses import dataclass
  from pydantic import BaseModel, Field, SecretStr

  @dataclass(slots=True)
  class LLMModel:
      provider: str
      model: str
      max_context_size: int

  class LLMProvider(BaseModel):
      type: str
      base_url: str
      api_key: SecretStr
  ```
- [ ] **检查点**: 能定义复杂的数据模型并验证

#### Day 5: 上下文管理器
- [ ] **学习目标**: 理解上下文管理器
- [ ] **学习内容**:
  - `with` 语句
  - `__enter__` 和 `__exit__`
  - `contextlib` 模块
  - 异步上下文管理器
- [ ] **实践任务**:
  ```python
  # 练习3: 实现一个文件锁上下文管理器
  import contextlib

  @contextlib.contextmanager
  def file_lock(path: str):
      lock = acquire_lock(path)
      try:
          yield lock
      finally:
          release_lock(lock)
  ```
- [ ] **检查点**: 能编写自定义上下文管理器

#### Day 6-7: 生成器与迭代器
- [ ] **学习目标**: 掌握生成器和迭代器
- [ ] **学习内容**:
  - Generator 和 Iterator 区别
  - yield 关键字
  - 生成器表达式
  - itertools 常用工具
- [ ] **实践任务**:
  ```python
  # 练习4: 实现一个分批读取大文件的生成器
  def read_large_file_in_chunks(file_path: str, chunk_size: int):
      with open(file_path) as f:
          while True:
              chunk = f.read(chunk_size)
              if not chunk:
                  break
              yield chunk
  ```
- [ ] **检查点**: 能使用生成器优化内存使用

### Week 2: 异步编程

#### Day 8-9: asyncio 基础
- [ ] **学习目标**: 理解异步编程模型
- [ ] **学习内容**:
  - async/await 语法
  - 事件循环 (Event Loop)
  - asyncio.run()
  - Task 和 Future
- [ ] **实践任务**:
  ```python
  # 练习5: 实现异步计时器
  import asyncio

  async def async_timer(seconds: int, name: str):
      print(f"{name} 开始")
      await asyncio.sleep(seconds)
      print(f"{name} 完成")

  async def main():
      await asyncio.gather(
          async_timer(1, "Task1"),
          async_timer(2, "Task2"),
          async_timer(3, "Task3"),
      )

  asyncio.run(main())
  ```
- [ ] **检查点**: 能编写基础异步代码

#### Day 10-11: 异步 I/O
- [ ] **学习目标**: 掌握异步文件和网络 I/O
- [ ] **学习内容**:
  - aiohttp 使用
  - aiofiles 文件操作
  - httpx 异步客户端
- [ ] **实践任务**:
  ```python
  # 练习6: 异步爬虫
  import aiohttp
  import asyncio

  async def fetch_url(session, url):
      async with session.get(url) as response:
          return await response.text()

  async def main():
      urls = ['http://example.com'] * 10
      async with aiohttp.ClientSession() as session:
          tasks = [fetch_url(session, url) for url in urls]
          results = await asyncio.gather(*tasks)
          print(f"Fetched {len(results)} pages")

  asyncio.run(main())
  ```
- [ ] **检查点**: 能编写高效的异步 I/O 代码

#### Day 12-13: 并发控制
- [ ] **学习目标**: 掌握异步并发控制
- [ ] **学习内容**:
  - asyncio.gather()
  - asyncio.wait()
  - asyncio.create_task()
  - Semaphore 信号量
- [ ] **实践任务**:
  ```python
  # 练习7: 限流异步下载器
  import asyncio

  async def download_with_limit(url, semaphore):
      async with semaphore:
          await download(url)

  async def main():
      semaphore = asyncio.Semaphore(5)  # 最多5个并发
      tasks = [download_with_limit(url, semaphore) for url in urls]
      await asyncio.gather(*tasks)
  ```
- [ ] **检查点**: 能控制并发数量和流量

#### Day 14: 异步生成器
- [ ] **学习目标**: 掌握异步生成器
- [ ] **学习内容**:
  - async for
  - AsyncGenerator
  - yield in async function
- [ ] **实践任务**:
  ```python
  # 练习8: 实现流式响应解析器
  from typing import AsyncGenerator

  async def stream_response(url: str) -> AsyncGenerator[str, None]:
      async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
              async for chunk in response.content.iter_chunked(1024):
                  yield chunk.decode()

  async def main():
      async for chunk in stream_response("http://api.example.com/stream"):
          print(chunk, end='')
  ```
- [ ] **检查点**: 能处理流式数据

**阶段1 总结检查**:
- [ ] 完成所有 8 个练习
- [ ] 代码提交到 Git
- [ ] 编写学习笔记
- [ ] **综合项目**: 实现一个异步爬虫，爬取多个网站并保存

---

## 🖥️ 阶段2: CLI开发（Week 3-4）

### Week 3: Click 和 Prompt Toolkit

#### Day 15-16: Click 基础
- [ ] **学习目标**: 掌握 Click 框架
- [ ] **学习内容**:
  - @click.command() 装饰器
  - @click.option() 参数定义
  - @click.argument() 位置参数
  - 参数类型（Path, Choice, IntRange）
- [ ] **实践任务**:
  ```python
  # 练习9: 实现一个文件管理 CLI
  import click
  from pathlib import Path

  @click.group()
  def cli():
      """文件管理工具"""
      pass

  @cli.command()
  @click.option('--path', '-p', type=click.Path(exists=True))
  @click.option('--recursive', '-r', is_flag=True)
  def list_files(path, recursive):
      """列出文件"""
      pass

  @cli.command()
  @click.argument('src', type=click.Path(exists=True))
  @click.argument('dst', type=click.Path())
  def copy(src, dst):
      """复制文件"""
      pass
  ```
- [ ] **检查点**: 能创建多命令 CLI 应用

#### Day 17-18: Click 高级
- [ ] **学习目标**: 掌握 Click 高级特性
- [ ] **学习内容**:
  - @click.group() 子命令
  - @click.pass_context 上下文传递
  - Callback 验证
  - 环境变量支持
- [ ] **实践任务**:
  ```python
  # 练习10: 分析 Kimi CLI 的参数设计
  # 阅读 kimi-cli/src/kimi_cli/cli.py
  # 理解参数设计模式
  ```
- [ ] **检查点**: 理解复杂 CLI 参数设计

#### Day 19-20: Prompt Toolkit 基础
- [ ] **学习目标**: 掌握交互式界面开发
- [ ] **学习内容**:
  - PromptSession 基础
  - 自动补全 (Completer)
  - 快捷键绑定 (KeyBindings)
  - 自定义样式 (Style)
- [ ] **实践任务**:
  ```python
  # 练习11: 实现一个交互式计算器
  from prompt_toolkit import PromptSession
  from prompt_toolkit.completion import WordCompleter

  def main():
      session = PromptSession()
      completer = WordCompleter(['add', 'sub', 'mul', 'div'])

      while True:
          try:
              text = session.prompt('>>> ', completer=completer)
              # 执行计算
          except KeyboardInterrupt:
              break
  ```
- [ ] **检查点**: 能创建交互式 CLI

#### Day 21: Prompt Toolkit 高级
- [ ] **学习目标**: 掌握高级交互特性
- [ ] **学习内容**:
  - 模式切换 (Vi/Emacs)
  - 多行编辑
  - 历史记录
  - 自定义 Lexer
- [ ] **实践任务**:
  ```python
  # 练习12: 分析 Kimi CLI Shell 模式
  # 阅读 kimi-cli/src/kimi_cli/ui/shell/
  # 理解 Ctrl-X 模式切换实现
  ```
- [ ] **检查点**: 理解 Kimi CLI 的 Shell 模式

### Week 4: Rich 和综合项目

#### Day 22-23: Rich 显示
- [ ] **学习目标**: 掌握富文本显示
- [ ] **学习内容**:
  - Console 基础
  - Markdown 渲染
  - Progress 进度条
  - Table 和 Panel
- [ ] **实践任务**:
  ```python
  # 练习13: 美化输出
  from rich.console import Console
  from rich.markdown import Markdown
  from rich.table import Table

  console = Console()

  # Markdown
  console.print(Markdown("# Hello World"))

  # Table
  table = Table(title="Files")
  table.add_column("Name")
  table.add_column("Size")
  console.print(table)
  ```
- [ ] **检查点**: 能创建美观的终端输出

#### Day 24-28: CLI 综合项目
- [ ] **项目**: 开发一个交互式文件管理器
- [ ] **功能需求**:
  - 使用 Click 定义命令
  - 使用 Prompt Toolkit 实现交互式界面
  - 使用 Rich 美化输出
  - 支持文件浏览、复制、删除
  - 支持自动补全和快捷键
- [ ] **检查点**: 完整的 CLI 应用

**阶段2 总结检查**:
- [ ] 完成所有练习
- [ ] 完成综合项目
- [ ] 理解 Kimi CLI 的 UI 设计
- [ ] 代码提交并写文档

---

## 🤖 阶段3: LLM应用开发（Week 5-7）

### Week 5: Prompt Engineering

#### Day 29-30: System Prompt 设计
- [ ] **学习目标**: 掌握 Prompt 设计原则
- [ ] **学习内容**:
  - System Prompt 结构
  - 角色定义
  - 指令清晰性
  - 输出格式约束
- [ ] **实践任务**:
  ```markdown
  # 练习14: 设计一个代码审查 Agent
  You are a professional code reviewer.

  Your responsibilities:
  - Analyze code quality
  - Identify potential bugs
  - Suggest improvements
  - Follow PEP 8 style guide

  Output format:
  ✅ Strengths: ...
  ⚠️  Issues: ...
  💡 Suggestions: ...
  ```
- [ ] **检查点**: 能设计高质量 System Prompt

#### Day 31-32: Few-Shot Learning
- [ ] **学习目标**: 掌握 Few-Shot 技术
- [ ] **学习内容**:
  - Few-Shot 原理
  - 示例选择策略
  - 示例格式设计
- [ ] **实践任务**:
  ```python
  # 练习15: Few-Shot Prompt
  few_shot_prompt = """
  User: 实现一个排序函数
  Assistant: 好的,我来实现快速排序:
  ```python
  def quick_sort(arr):
      # ...
  ```

  User: 实现一个搜索函数
  Assistant: 好的,我来实现二分搜索:
  ```python
  def binary_search(arr, target):
      # ...
  ```
  """
  ```
- [ ] **检查点**: 能设计有效的 Few-Shot 示例

#### Day 33: Chain of Thought
- [ ] **学习目标**: 理解思维链
- [ ] **学习内容**:
  - CoT 原理
  - 步骤拆解
  - 推理过程显式化
- [ ] **实践任务**:
  ```markdown
  # 练习16: CoT Prompt
  Let's think step by step:
  1. First, identify the problem
  2. Then, break it down into sub-problems
  3. Solve each sub-problem
  4. Combine the solutions
  ```
- [ ] **检查点**: 能设计 CoT Prompt

#### Day 34-35: ReAct Pattern
- [ ] **学习目标**: 掌握 ReAct 模式
- [ ] **学习内容**:
  - Reasoning + Acting
  - 工具调用决策
  - 观察-思考-行动循环
- [ ] **实践任务**:
  ```markdown
  # 练习17: ReAct Prompt
  Thought: I need to find information about Python
  Action: search("Python programming language")
  Observation: Python is a high-level language...

  Thought: Now I should summarize the key points
  Action: summarize(observation)
  Observation: Key points: 1) ... 2) ... 3) ...

  Thought: I have enough information to answer
  Final Answer: ...
  ```
- [ ] **检查点**: 理解 ReAct 执行流程

### Week 6: Function Calling

#### Day 36-37: Function Calling 基础
- [ ] **学习目标**: 理解 Function Calling
- [ ] **学习内容**:
  - OpenAI Function Calling 格式
  - JSON Schema 定义
  - 工具描述设计
- [ ] **实践任务**:
  ```python
  # 练习18: 定义工具
  tools = [
      {
          "type": "function",
          "function": {
              "name": "read_file",
              "description": "Read contents of a file",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "file_path": {
                          "type": "string",
                          "description": "Path to the file"
                      }
                  },
                  "required": ["file_path"]
              }
          }
      }
  ]
  ```
- [ ] **检查点**: 能定义规范的工具 Schema

#### Day 38-39: 工具调用流程
- [ ] **学习目标**: 实现完整调用流程
- [ ] **学习内容**:
  - 工具调用解析
  - 工具执行
  - 结果返回
  - 错误处理
- [ ] **实践任务**:
  ```python
  # 练习19: 实现工具调用系统
  async def execute_tool_call(tool_call):
      tool_name = tool_call["function"]["name"]
      arguments = json.loads(tool_call["function"]["arguments"])

      # 查找工具
      tool = get_tool(tool_name)

      # 执行工具
      result = await tool.execute(**arguments)

      return {
          "tool_call_id": tool_call["id"],
          "role": "tool",
          "content": json.dumps(result)
      }
  ```
- [ ] **检查点**: 能实现工具调用系统

#### Day 40-42: 分析 Kimi CLI 工具系统
- [ ] **任务**: 深入分析 Kimi CLI Tools
- [ ] **学习内容**:
  - 阅读 `src/kimi_cli/tools/` 所有工具
  - 理解工具注册机制
  - 分析工具执行流程
- [ ] **输出**: 写分析文档

### Week 7: Streaming 和综合项目

#### Day 43-44: 流式处理
- [ ] **学习目标**: 掌握流式响应
- [ ] **学习内容**:
  - SSE (Server-Sent Events) 协议
  - 流式解析
  - 实时显示
- [ ] **实践任务**:
  ```python
  # 练习20: 流式客户端
  async def stream_chat(messages):
      async with aiohttp.ClientSession() as session:
          async with session.post(
              "https://api.openai.com/v1/chat/completions",
              json={
                  "model": "gpt-3.5-turbo",
                  "messages": messages,
                  "stream": True
              },
              headers={"Authorization": f"Bearer {API_KEY}"}
          ) as response:
              async for line in response.content:
                  if line.startswith(b"data: "):
                      data = json.loads(line[6:])
                      if chunk := data["choices"][0]["delta"].get("content"):
                          print(chunk, end="", flush=True)
  ```
- [ ] **检查点**: 能处理流式响应

#### Day 45-49: LLM 应用综合项目
- [ ] **项目**: 实现一个支持工具调用的 AI 助手
- [ ] **功能需求**:
  - 支持多轮对话
  - 支持工具调用（文件读写、搜索）
  - 流式响应显示
  - ReAct 模式
- [ ] **技术栈**:
  - OpenAI API / Kimi API
  - aiohttp
  - Rich 显示
- [ ] **检查点**: 完整的 AI 应用

**阶段3 总结检查**:
- [ ] 完成所有练习
- [ ] 完成综合项目
- [ ] 理解 LLM 应用开发核心技术
- [ ] 写技术总结

---

## 🔗 阶段4: 协议与标准（Week 8-9）

### Week 8: ACP 和 MCP 协议

#### Day 50-52: ACP 协议
- [ ] **学习目标**: 深入理解 ACP
- [ ] **学习内容**:
  - ACP 协议规范
  - JSON-RPC 2.0 格式
  - 生命周期管理
  - 工具调用机制
- [ ] **实践任务**:
  ```python
  # 练习21: 实现简单 ACP 服务器
  import json
  from typing import Any

  class ACPServer:
      async def handle_request(self, request: dict) -> dict:
          method = request["method"]
          params = request.get("params", {})

          if method == "tools/list":
              return self.list_tools()
          elif method == "tools/call":
              return await self.call_tool(params)

      def list_tools(self) -> dict:
          return {
              "tools": [
                  {
                      "name": "read_file",
                      "description": "Read file",
                      "inputSchema": {...}
                  }
              ]
          }
  ```
- [ ] **检查点**: 能实现基础 ACP 服务器

#### Day 53-55: MCP 协议
- [ ] **学习目标**: 掌握 MCP 开发
- [ ] **学习内容**:
  - MCP 协议规范
  - 工具定义
  - Resources 管理
  - Prompts 模板
- [ ] **实践任务**:
  ```python
  # 练习22: 开发 MCP 服务器
  from fastmcp import FastMCP

  mcp = FastMCP("my-tools")

  @mcp.tool()
  def calculate(expression: str) -> float:
      """计算数学表达式"""
      return eval(expression)

  @mcp.resource("file://{path}")
  def read_file(path: str) -> str:
      """读取文件"""
      with open(path) as f:
          return f.read()
  ```
- [ ] **检查点**: 能开发 MCP 服务器

#### Day 56: Wire 协议
- [ ] **学习目标**: 了解 Wire 协议
- [ ] **学习内容**:
  - Wire 协议概述
  - 消息格式
  - 通信流程
- [ ] **实践任务**:
  - 阅读 Kimi CLI Wire Server 实现
  - 分析通信流程
- [ ] **检查点**: 理解 Wire 协议

### Week 9: 协议实战

#### Day 57-63: MCP 服务器项目
- [ ] **项目**: 开发一个实用的 MCP 工具服务器
- [ ] **功能建议**:
  - 数据库查询工具
  - 文件系统操作
  - 网络请求工具
  - 代码分析工具
- [ ] **检查点**: 能与 Kimi CLI 集成

**阶段4 总结检查**:
- [ ] 理解 ACP/MCP/Wire 协议
- [ ] 完成 MCP 服务器项目
- [ ] 能集成到 Kimi CLI

---

## 🏗️ 阶段5: Kimi CLI 核心架构（Week 10-11）

### Week 10: CLI/App/Soul 层

#### Day 64-66: CLI 层和 App 层
- [ ] **学习目标**: 理解架构设计
- [ ] **学习内容**:
  - 阅读 `cli.py` 源码
  - 阅读 `app.py` 源码
  - 理解初始化流程
  - 理解模式路由
- [ ] **实践任务**:
  - Debug 启动流程
  - 画架构图
  - 添加自定义参数
- [ ] **检查点**: 理解前两层架构

#### Day 67-70: Soul 层
- [ ] **学习目标**: 深入 Agent 核心
- [ ] **学习内容**:
  - 阅读 `soul/kimisoul.py`
  - 阅读 `soul/agent.py`
  - 阅读 `soul/context.py`
  - 阅读 `soul/runtime.py`
- [ ] **实践任务**:
  - Debug Agent 执行流程
  - 追踪工具调用
  - 分析上下文管理
- [ ] **检查点**: 理解 Agent 执行引擎

### Week 11: Tools 和 Kosong

#### Day 71-74: Tools 系统
- [ ] **学习目标**: 掌握工具开发
- [ ] **学习内容**:
  - 阅读所有工具实现
  - 理解工具注册
  - 理解工具执行
- [ ] **实践任务**:
  ```python
  # 练习23: 开发自定义工具
  from kimi_cli.tools.utils import ToolResult

  async def my_tool(param: str) -> ToolResult:
      """我的自定义工具"""
      result = do_something(param)
      return ToolResult(
          success=True,
          message="成功",
          data=result
      )
  ```
- [ ] **检查点**: 能开发自定义工具

#### Day 75-77: Kosong 框架
- [ ] **学习目标**: 理解 LLM 抽象层
- [ ] **学习内容**:
  - 阅读 `llm.py`
  - 理解 ChatProvider 抽象
  - 理解多提供商支持
- [ ] **实践任务**:
  - 实现自定义 ChatProvider
  - 对比 Kosong 和 LangChain
- [ ] **检查点**: 理解 Kosong 设计

**阶段5 总结检查**:
- [ ] 深入理解 Kimi CLI 架构
- [ ] 能阅读和修改源码
- [ ] 完成自定义工具开发

---

## 🚀 阶段6: 实战与扩展（Week 12+）

### 实战项目1: 自定义工具（1周）
- [ ] 需求设计
- [ ] 工具实现
- [ ] 测试验证
- [ ] 文档编写

### 实战项目2: 自定义 Agent（1周）
- [ ] Agent 规范设计
- [ ] 测试与优化
- [ ] 性能调优

### 实战项目3: MCP 服务器（1周）
- [ ] 服务器设计
- [ ] 功能实现
- [ ] 集成测试

### 实战项目4: 贡献代码（持续）
- [ ] Fork 项目
- [ ] 选择 Issue
- [ ] 开发功能
- [ ] 提交 PR
- [ ] Code Review

---

## ✅ 总体检查清单

### 技能检查
- [ ] Python 3.13+ 现代特性熟练
- [ ] 异步编程熟练
- [ ] CLI 开发熟练
- [ ] LLM 应用开发熟练
- [ ] ACP/MCP 协议理解
- [ ] Kimi CLI 源码理解
- [ ] 能开发自定义工具
- [ ] 能贡献开源代码

### 项目输出
- [ ] 所有练习代码
- [ ] 5个综合项目
- [ ] 学习笔记
- [ ] 技术博客
- [ ] 至少1个 PR

---

**持续更新，加油！💪**
