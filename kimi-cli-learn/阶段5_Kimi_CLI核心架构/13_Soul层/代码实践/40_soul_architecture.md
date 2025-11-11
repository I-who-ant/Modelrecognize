# 练习40: Soul 层架构设计

## Soul 层概述

Soul 层是 Kimi CLI 的核心，负责 **Agent 执行引擎** 的实现。它是整个系统的"灵魂"。

## 核心职责

### 1. LLM 调用管理

- **模型抽象**: 统一不同 LLM 提供商的接口（OpenAI、Anthropic、本地模型）
- **流式处理**: 支持流式输出，提升用户体验
- **上下文管理**: 管理对话历史和上下文窗口

### 2. Agent 循环（ReAct 模式）

```
┌─────────────────────────────────────┐
│         Agent 执行循环               │
├─────────────────────────────────────┤
│ 1. 接收用户输入                      │
│    ↓                                 │
│ 2. 调用 LLM 思考                     │
│    ↓                                 │
│ 3. LLM 决定：                        │
│    - 直接回复？ → 返回结果            │
│    - 调用工具？ → 执行步骤 4          │
│    ↓                                 │
│ 4. 执行工具调用                      │
│    ↓                                 │
│ 5. 将工具结果返回 LLM                │
│    ↓                                 │
│ 6. 回到步骤 2（最多 N 轮）            │
└─────────────────────────────────────┘
```

### 3. 工具调度

- **工具注册**: 管理可用工具列表
- **工具选择**: LLM 决定调用哪些工具
- **工具执行**: 调度工具执行器
- **结果处理**: 格式化工具结果返回给 LLM

## Soul 层架构

```python
class Soul:
    """Soul 层 - Agent 执行引擎"""
    
    def __init__(self, config: SoulConfig):
        # LLM 客户端
        self.llm = self._create_llm(config)
        
        # 工具管理器
        self.tool_manager = ToolManager()
        
        # 消息历史
        self.messages: list[dict] = []
        
        # 系统提示词
        self.system_prompt = self._build_system_prompt()
    
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """主要聊天接口（流式）"""
        pass
    
    async def _agent_loop(self, max_turns: int = 5):
        """Agent 循环"""
        pass
    
    async def _execute_tool_calls(self, tool_calls: list):
        """执行工具调用"""
        pass
```

## 关键设计模式

### 1. LLM 抽象层（Kosong 框架）

```python
class LLMProvider(ABC):
    """LLM 提供商抽象基类"""
    
    @abstractmethod
    async def astream_chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ) -> AsyncIterator[ChatChunk]:
        """流式聊天"""
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI 实现"""
    pass

class AnthropicProvider(LLMProvider):
    """Anthropic 实现"""
    pass
```

### 2. 工具管理器

```python
class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools: dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool
    
    def get_tool_schemas(self) -> list[dict]:
        """获取所有工具的 Schema"""
        return [tool.get_schema() for tool in self.tools.values()]
    
    async def execute(self, tool_call: ToolCall):
        """执行工具调用"""
        tool = self.tools[tool_call.name]
        return await tool.execute(tool_call.arguments)
```

### 3. 消息管理

```python
class MessageManager:
    """消息管理器"""
    
    def __init__(self, max_tokens: int = 4000):
        self.messages: list[dict] = []
        self.max_tokens = max_tokens
    
    def add_user_message(self, content: str):
        """添加用户消息"""
        self.messages.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content: str, tool_calls=None):
        """添加助手消息"""
        msg = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)
    
    def add_tool_result(self, tool_call_id: str, result: str):
        """添加工具结果"""
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result
        })
    
    def trim_to_fit(self):
        """裁剪历史以适应上下文窗口"""
        # 保留系统提示词和最近的消息
        pass
```

## Agent 循环实现

```python
async def _agent_loop(self, max_turns: int = 5):
    """Agent 执行循环"""
    
    for turn in range(max_turns):
        # 1. 调用 LLM
        response = await self.llm.astream_chat(
            messages=self.messages,
            tools=self.tool_manager.get_tool_schemas()
        )
        
        # 2. 收集响应
        full_content = ""
        tool_calls = []
        
        async for chunk in response:
            if chunk.delta.content:
                full_content += chunk.delta.content
                yield chunk.delta.content  # 流式输出
            
            if chunk.delta.tool_calls:
                tool_calls.extend(chunk.delta.tool_calls)
        
        # 3. 添加助手消息
        self.messages.append({
            "role": "assistant",
            "content": full_content,
            "tool_calls": tool_calls if tool_calls else None
        })
        
        # 4. 如果没有工具调用，结束循环
        if not tool_calls:
            break
        
        # 5. 执行工具调用
        for tc in tool_calls:
            result = await self.tool_manager.execute(tc)
            self.messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result)
            })
        
        # 继续下一轮
    
    # 达到最大轮次
    if turn == max_turns - 1:
        yield "\n\n[达到最大思考轮次]"
```

## 系统提示词设计

```python
def _build_system_prompt(self) -> str:
    """构建系统提示词"""
    return """
你是 Kimi，一个专业的 AI 编程助手。

## 能力
- 代码编写和审查
- 文件读写
- 命令执行
- 网络搜索

## 工具使用规范
1. 必要时才调用工具
2. 一次调用多个工具以提高效率
3. 工具执行失败时，分析原因并重试

## 交互风格
- 简洁清晰
- 代码规范
- 注重最佳实践
"""
```

## 错误处理

```python
async def chat(self, user_input: str) -> AsyncIterator[str]:
    """聊天接口（带错误处理）"""
    try:
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # 执行 Agent 循环
        async for chunk in self._agent_loop():
            yield chunk
    
    except LLMError as e:
        yield f"\n\n❌ LLM 错误: {e}"
    
    except ToolExecutionError as e:
        yield f"\n\n❌ 工具执行错误: {e}"
    
    except Exception as e:
        yield f"\n\n❌ 未知错误: {e}"
        # 记录日志
        logger.exception("Soul.chat 发生错误")
```

## 性能优化

### 1. 工具并发执行

```python
async def _execute_tool_calls(self, tool_calls: list):
    """并发执行多个工具调用"""
    tasks = [
        self.tool_manager.execute(tc)
        for tc in tool_calls
    ]
    return await asyncio.gather(*tasks)
```

### 2. 流式输出优化

```python
# 使用缓冲减少 I/O
buffer = []
async for chunk in llm_stream:
    buffer.append(chunk)
    if len(buffer) >= 10:  # 每 10 个字符刷新一次
        yield ''.join(buffer)
        buffer.clear()
```

### 3. 上下文窗口管理

```python
def trim_messages(self):
    """智能裁剪消息历史"""
    # 保留系统提示词
    # 保留最近的 N 条消息
    # 优先保留包含工具调用的消息
    pass
```

## 学习要点

1. **Soul 层是 Agent 的核心**: 实现了完整的 ReAct 循环
2. **抽象层设计**: LLM 抽象允许支持多种模型
3. **工具管理**: 统一的工具接口和调度机制
4. **流式处理**: 提升用户体验的关键
5. **错误处理**: 优雅降级，不中断对话
6. **消息管理**: 上下文窗口优化

## 下一步

- 练习41: Soul 层核心实现
- 练习42: Agent 循环实现
- 练习43: Soul 层集成测试
