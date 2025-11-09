# Day 3-4 模型I/O封装示例

本目录包含LangChain模型I/O封装的详细示例代码。

## 📁 文件说明

| 文件 | 说明 | 核心知识点 |
|-----|------|-----------|
| `01_chat_vs_llm.py` | Chat Models vs LLMs对比 | 消息类型、模型选择 |
| `02_streaming.py` | 流式输出完整示例 | stream/astream、回调函数 |
| `03_token_tracking.py` | Token追踪和成本控制 | 回调、tiktoken、成本估算 |
| `04_structured_output.py` | 结构化输出 | Pydantic、JsonParser、验证 |
| `05_comprehensive.py` | 综合示例 | 所有功能组合使用 |

## 🚀 快速开始

### 安装依赖

```bash
pip install langchain langchain-openai python-dotenv tiktoken pydantic
```

### 运行示例

```bash
# Chat Models vs LLMs
python 01_chat_vs_llm.py

# 流式输出
python 02_streaming.py

# Token追踪
python 03_token_tracking.py

# 结构化输出
python 04_structured_output.py

# 综合示例
python 05_comprehensive.py
```

## 📚 学习顺序

建议按以下顺序学习:

1. **Chat vs LLM** (`01`) - 理解两种模型的区别
2. **流式输出** (`02`) - 提升用户体验
3. **Token追踪** (`03`) - 控制成本
4. **结构化输出** (`04`) - 获取可靠数据
5. **综合示例** (`05`) - 组合使用

## 💡 核心知识点

### 1. Chat Models vs LLMs

```python
# Chat Model (推荐)
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatOpenAI(model="gpt-3.5-turbo")
messages = [
    SystemMessage(content="你是Python导师"),
    HumanMessage(content="什么是装饰器?")
]
response = chat.invoke(messages)

# LLM (传统)
from langchain_openai import OpenAI
llm = OpenAI(model="gpt-3.5-turbo-instruct")
response = llm.invoke("Python是")
```

**关键区别**:
- Chat Model: 消息列表 → 消息对象
- LLM: 字符串 → 字符串

### 2. 流式输出

```python
# 同步流式
for chunk in llm.stream("写一首诗"):
    print(chunk.content, end="", flush=True)

# 异步流式
async for chunk in llm.astream("解释概念"):
    print(chunk.content, end="", flush=True)
```

**优势**: 实时反馈，更好的用户体验

### 3. Token追踪

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    llm.invoke("问题")
    print(f"Tokens: {cb.total_tokens}")
    print(f"成本: ${cb.total_cost}")
```

**用途**: 成本控制、性能监控

### 4. 结构化输出

```python
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

class Person(BaseModel):
    name: str
    age: int

parser = PydanticOutputParser(pydantic_object=Person)
prompt = f"提取人物信息\n{parser.get_format_instructions()}"
response = llm.invoke(prompt)
person = parser.parse(response.content)
```

**优势**: 类型安全、自动验证

## 🎯 实战场景

### 场景1: 聊天机器人

- 使用Chat Model
- 启用流式输出
- 追踪Token控制成本

### 场景2: 信息提取

- 使用结构化输出
- Pydantic模型定义
- 批量处理数据

### 场景3: 内容生成

- 使用流式输出
- 限制max_tokens
- 监控Token使用

## ⚠️ 常见问题

### Q1: 流式输出成本更高吗?

**不会**！流式输出的总Token数和成本与普通调用完全相同，只是返回方式不同。

### Q2: 如何选择Chat Model还是LLM?

**99%场景使用Chat Model**:
- 支持对话历史
- 可设置System Prompt
- 更接近现代LLM的使用方式

### Q3: 结构化输出是否可靠?

**需要注意**:
- LLM可能不完全遵守格式
- 使用temperature=0提高一致性
- 使用OutputFixingParser自动修复
- 必须有异常处理

### Q4: Token追踪overhead大吗?

**很小**！使用回调函数的性能开销可以忽略不计。

## 📊 性能对比

| 功能 | 额外开销 | 推荐使用 |
|-----|---------|---------|
| 流式输出 | 网络请求略多 | ✅ 长文本生成 |
| Token追踪 | 几乎无 | ✅ 所有场景 |
| 结构化输出 | format_instructions占Token | ✅ 数据提取 |

## 🔧 调试技巧

### 1. 查看LLM的原始响应

```python
response = llm.invoke(prompt)
print("原始响应:", response.content)
print("元数据:", response.response_metadata)
```

### 2. 流式输出调试

```python
for i, chunk in enumerate(llm.stream(prompt)):
    print(f"Chunk {i}: {chunk.content}")
```

### 3. Token计算验证

```python
import tiktoken
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
tokens = len(encoding.encode(text))
print(f"Token数: {tokens}")
```

## ✅ 学习检查清单

完成Day 3-4学习后，确保你能够:

- [ ] 解释Chat Models和LLMs的区别
- [ ] 实现流式输出(同步和异步)
- [ ] 使用至少2种方法追踪Token
- [ ] 使用Pydantic定义数据模型
- [ ] 实现结构化输出
- [ ] 估算API调用成本
- [ ] 处理解析错误
- [ ] 组合使用多种功能

## 📖 扩展阅读

- [LangChain Chat Models文档](https://python.langchain.com/docs/modules/model_io/chat/)
- [Output Parsers文档](https://python.langchain.com/docs/modules/model_io/output_parsers/)
- [Tiktoken GitHub](https://github.com/openai/tiktoken)
- [Pydantic文档](https://docs.pydantic.dev/)

---

**老王提示**: 这部分内容很实用，每个示例都要跑一遍！特别是Token追踪和结构化输出，这在生产环境中非常重要。别tm只看不练！💪