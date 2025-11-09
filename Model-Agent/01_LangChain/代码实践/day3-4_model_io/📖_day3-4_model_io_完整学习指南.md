# 📖 Day3-4 Model I/O 完整学习指南

**创建日期**: 2025-11-09
**类型**: LangChain实战总结
**难度**: ⭐⭐⭐ (中等偏易)
**目标**: 掌握LangChain的模型I/O操作，能够构建完整的LLM应用

---

## 🎯 Day3-4 的核心目标

```
学习目标：掌握如何在LangChain中与LLM交互

从这部分学完，你将能够：
✅ 理解Chat Models和LLMs的区别
✅ 实现流式输出提升用户体验
✅ 追踪Token使用控制成本
✅ 解析LLM输出获得结构化数据
✅ 构建完整的LLM应用系统
```

---

## 📚 Day3-4 包含的4个核心内容

### 1️⃣ Chat Models vs LLMs (01_chat_vs_llm.py)

#### 核心概念

```
Chat Models (推荐,99%场景使用):
  ├─ 输入: 消息列表 (Message objects)
  │  ├─ SystemMessage: 系统提示词
  │  ├─ HumanMessage: 用户问题
  │  └─ AIMessage: AI回答
  ├─ 输出: AIMessage对象
  ├─ 支持: 多轮对话、上下文管理
  └─ 例子: ChatOpenAI("gpt-3.5-turbo")

LLMs (传统,逐步被淘汰):
  ├─ 输入: 字符串
  ├─ 输出: 字符串
  ├─ 支持: 文本补全
  └─ 例子: OpenAI("gpt-3.5-turbo-instruct")
```

#### 代码示例

```python
# Chat Model (推荐)
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

messages = [
    SystemMessage(content="你是Python导师"),
    HumanMessage(content="什么是装饰器?")
]

response = chat.invoke(messages)
print(response.content)

# 多轮对话
conversation = [
    SystemMessage(content="你是友好的AI助手"),
    HumanMessage(content="LangChain是什么?"),
    AIMessage(content="LangChain是..."),  # 前面的AI回答
    HumanMessage(content="它有什么优势?")   # 继续对话
]
response = chat.invoke(conversation)
```

#### 关键要点

```
为什么用Chat Models?
✅ 支持对话历史和上下文
✅ 更灵活的角色设置
✅ 现代LLM的标准方式
✅ 为Agent和Chain做准备

什么时候用LLM?
❌ 几乎没有
❌ 除非用很旧的模型
```

---

### 2️⃣ 流式输出 (02_streaming.py)

#### 核心概念

```
流式输出的作用:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
问题: LLM响应慢，用户要等待

传统方式:
  用户等待 → ... → 收到完整响应

流式方式:
  用户等待 → 实时看内容 → 看完 ✅

优势:
✅ 实时反馈，提升用户体验
✅ 适合长文本生成
✅ 避免用户感到应用"卡死"
✅ 看起来更"聪明"
```

#### 代码示例

```python
# 方式1: 同步流式输出
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

print("回答: ", end="", flush=True)
for chunk in llm.stream("用100字介绍LangChain"):
    print(chunk.content, end="", flush=True)
print()  # 换行

# 方式2: 异步流式输出(推荐Web应用)
import asyncio

async def async_stream_example():
    async for chunk in llm.astream("解释什么是异步编程"):
        print(chunk.content, end="", flush=True)

asyncio.run(async_stream_example())

# 方式3: 使用回调自动处理流式
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm_streaming = ChatOpenAI(
    model="gpt-3.5-turbo",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

llm_streaming.invoke("介绍LangChain")  # 自动流式输出!
```

#### 关键要点

```
流式输出的特性:
✅ 总Token数不变，成本相同
✅ 网络请求略多，但可接受
✅ 需要正确的flush处理
✅ 适合聊天、长文本、Web应用

使用场景:
✅ ChatGPT式的聊天机器人
✅ 代码生成工具
✅ 文章生成应用
✅ 任何需要实时反馈的场景
```

---

### 3️⃣ Token追踪和成本控制 (03_token_tracking.py)

#### 核心概念

```
为什么追踪Token?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LLM费用 = Token数 × 单价

Token消耗量决定成本，必须控制!

三个追踪方法:

方法1: 从响应获取
  response.response_metadata['token_usage']

方法2: 回调函数追踪多次调用
  with get_openai_callback() as cb:
      llm.invoke(...)  # 多次调用
      print(cb.total_tokens)
      print(cb.total_cost)

方法3: 自定义回调
  BaseCallbackHandler子类
  详细记录每一次调用
```

#### 代码示例

```python
# 方法1: 单次调用的Token追踪
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")
response = llm.invoke("介绍LangChain")

usage = response.response_metadata.get("token_usage", {})
print(f"Prompt Tokens: {usage.get('prompt_tokens', 0)}")
print(f"Completion Tokens: {usage.get('completion_tokens', 0)}")
print(f"Total Tokens: {usage.get('total_tokens', 0)}")

# 方法2: 多次调用的成本统计
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    llm.invoke("什么是LangChain?")
    llm.invoke("它有什么优势?")
    llm.invoke("如何开始使用?")

    print(f"总Token: {cb.total_tokens}")
    print(f"总成本: ${cb.total_cost:.6f}")

# 方法3: 手动计算Token
import tiktoken

def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

tokens = count_tokens("这是一个例子")
print(f"Token数: {tokens}")
```

#### 成本优化策略

```
1. 限制输出长度
   llm = ChatOpenAI(..., max_tokens=50)

2. 选择性价比高的模型
   gpt-3.5-turbo < gpt-4-turbo < gpt-4

3. 优化Prompt减少输入Token
   冗长Prompt: "请你用详细语言，尽可能完整地解释..."
   简洁Prompt: "解释..."

4. 使用缓存避免重复调用

5. 实现用户级配额限制
   每个用户最多消耗X个Token
```

#### 价格表

```

模型                  输入(每百万)    输出(每百万)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
gpt-3.5-turbo        $0.50          $1.50
gpt-4-turbo          $10.00         $30.00
gpt-4                $30.00         $60.00

成本计算:
  cost = (prompt_tokens × input_price +
          completion_tokens × output_price) / 1,000,000

```

#### 关键要点

```
最佳实践:
✅ 始终追踪Token使用
✅ 监控异常高的消耗
✅ 定期审计和优化
✅ 为用户设置预警
✅ 考虑使用本地模型降低成本

Token计算规则:
  英文: ~4字符 = 1 token
  中文: ~1.5-2汉字 = 1 token
  代码: ~1符号 = 1 token
```

---

### 4️⃣ 结构化输出 (04_structured_output.py)

#### 核心概念

```
问题: LLM的输出是自由文本，难以处理

解决方案: 结构化输出
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

让LLM返回我们需要的格式：
  ├─ JSON
  ├─ Pydantic模型
  ├─ 特定的字段结构
  └─ 验证后的数据

四种主要方式:

1. PydanticOutputParser (最推荐)
   ├─ 类型安全
   ├─ 自动验证
   ├─ IDE自动补全
   └─ 最佳实践

2. JsonOutputParser
   ├─ 简单灵活
   ├─ 返回字典
   └─ 适合简单场景

3. StructuredOutputParser
   ├─ 配置简单
   ├─ 固定字段
   └─ 快速上手

4. OutputFixingParser
   ├─ 自动修复错误
   ├─ 提高可靠性
   └─ 必须搭配其他解析器
```

#### 代码示例

```python
# 方式1: Pydantic Parser (最推荐!)
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Person(BaseModel):
    """人物信息"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")
    city: str = Field(description="城市")

parser = PydanticOutputParser(pydantic_object=Person)

# 获取格式说明
format_instructions = parser.get_format_instructions()

# 构建Prompt
text = "张三是一位25岁的软件工程师，在北京工作"

prompt = f"""
从以下文本提取人物信息:
{text}

{format_instructions}
"""

# 调用LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
response = llm.invoke(prompt)

# 解析为Python对象
try:
    person = parser.parse(response.content)
    print(f"姓名: {person.name}")
    print(f"年龄: {person.age}")
    print(f"职业: {person.occupation}")
    print(f"城市: {person.city}")
except Exception as e:
    print(f"解析失败: {e}")

# 方式2: JSON Parser
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = f"""
以JSON格式返回以下产品信息:
- name: 名称
- price: 价格
- stock: 库存

产品: "iPhone 15 Pro，价格7999元，库存20台"

{parser.get_format_instructions()}
"""

response = llm.invoke(prompt)
data = parser.parse(response.content)  # 返回字典
print(data)

# 方式3: 自动修复错误
from langchain.output_parsers import OutputFixingParser

# 原始解析器
pydantic_parser = PydanticOutputParser(pydantic_object=Person)

# 包装为自动修复版本
fixing_parser = OutputFixingParser.from_llm(
    parser=pydantic_parser,
    llm=llm
)

# 即使LLM输出有格式错误，也会自动修复
result = fixing_parser.parse(bad_json_output)
```

#### 复杂场景示例

```python
# 定义复杂的数据模型
from typing import List

class ProductReview(BaseModel):
    """产品评价"""
    product_name: str = Field(description="产品名称")
    rating: int = Field(description="评分1-5分", ge=1, le=5)
    pros: List[str] = Field(description="优点列表")
    cons: List[str] = Field(description="缺点列表")
    sentiment: str = Field(description="情感: positive/negative/neutral")
    recommended: bool = Field(description="是否推荐")

# 提取复杂结构化数据
parser = PydanticOutputParser(pydantic_object=ProductReview)

review_text = """
MacBook Pro很不错！
优点：性能强，屏幕好，续航长
缺点：太贵，有点重
总体推荐，评分5分
"""

prompt = f"""
从以下评价提取信息:
{review_text}

{parser.get_format_instructions()}
"""

response = llm.invoke(prompt)
review = parser.parse(response.content)

print(f"产品: {review.product_name}")
print(f"评分: {review.rating}/5")
print(f"优点: {', '.join(review.pros)}")
print(f"缺点: {', '.join(review.cons)}")
print(f"推荐: {'是' if review.recommended else '否'}")
```

#### 关键要点

```
最佳实践:
✅ 复杂场景用Pydantic (类型安全)
✅ 简单场景用JSON (灵活快速)
✅ 使用OutputFixingParser提高可靠性
✅ 设置temperature=0提高一致性
✅ 必须有异常处理

常见问题:
❌ LLM可能不完全遵守格式
❌ 需要清晰的format_instructions
❌ 成本会略高(格式说明占Token)

解决方案:
✅ 在Prompt中给出示例
✅ 使用OutputFixingParser
✅ 设置验证器(validators)
✅ 实现重试机制
```

---

## 🎓 完整学习路径

### 推荐学习顺序

```
第1步: Chat vs LLM (01)
  学习时间: 15分钟
  理解: Message对象、Chat模型的优势
  任务: 写一个简单的Chat调用

第2步: 流式输出 (02)
  学习时间: 20分钟
  理解: stream/astream、回调函数
  任务: 实现同步和异步流式输出

第3步: Token追踪 (03)
  学习时间: 25分钟
  理解: Token计算、成本控制、优化策略
  任务: 实现完整的成本追踪系统

第4步: 结构化输出 (04)
  学习时间: 30分钟
  理解: Pydantic、OutputParser、验证
  任务: 实现信息提取系统

第5步: 综合项目
  学习时间: 1-2小时
  任务: 构建完整的LLM应用
```

---

## 💻 实战项目示例

### 项目1: AI聊天机器人

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def chatbot_app():
    """完整的聊天机器人应用"""

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        streaming=True  # 启用流式输出
    )

    # 系统提示
    system_prompt = "你是一个友好的Python编程助手，用简单语言解释复杂概念"

    conversation = [SystemMessage(content=system_prompt)]

    while True:
        user_input = input("用户: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        conversation.append(HumanMessage(content=user_input))

        print("助手: ", end="", flush=True)
        for chunk in llm.stream(conversation):
            print(chunk.content, end="", flush=True)
        print()  # 换行

        # 添加助手回答到对话历史
        # (实际上可以从response获取)

if __name__ == "__main__":
    chatbot_app()
```

### 项目2: 信息提取系统

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback

class JobPosting(BaseModel):
    """职位信息"""
    title: str = Field(description="职位名称")
    company: str = Field(description="公司名")
    salary: str = Field(description="薪资范围")
    location: str = Field(description="工作地点")
    requirements: list = Field(description="要求列表")

def extract_job_info(text: str) -> JobPosting:
    """从文本中提取职位信息"""

    parser = PydanticOutputParser(pydantic_object=JobPosting)

    prompt = f"""
从以下文本提取职位信息:
{text}

{parser.get_format_instructions()}
"""

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    with get_openai_callback() as cb:
        response = llm.invoke(prompt)
        job = parser.parse(response.content)
        print(f"成本: ${cb.total_cost:.6f}")

    return job

# 使用
text = """
Python开发工程师招聘
公司: 某某AI公司
薪资: 15-25K
地点: 北京、上海
要求: 3年Python经验，熟悉LLM应用
"""

job = extract_job_info(text)
print(f"职位: {job.title}")
print(f"公司: {job.company}")
print(f"薪资: {job.salary}")
```

---

## ✅ 学习检查清单

完成Day3-4后，确保你能够:

```
□ 解释Chat Models和LLMs的区别 : Chat Models是基于LLMs的一种特殊模型,它添加了对话历史管理功能,能够更好地理解上下文和保持对话连贯性。

□ 能够正确构造Message对象列表 : 包括SystemMessage、HumanMessage、 AIMessage等

□ 实现同步流式输出(stream()) : 能够实时返回模型生成的文本,适用于需要快速响应的场景。

□ 实现异步流式输出(astream()) : 与同步流式输出类似,但在异步环境中使用,能够更好地利用资源。

□ 使用StreamingStdOutCallbackHandler : 用于将流式输出直接打印到标准输出,方便调试和用户交互。

□ 从响应元数据获取Token信息 : 可以获取模型生成的Token数,用于成本计算和优化。

□ 使用get_openai_callback()追踪多次调用 : 能够方便地统计多次调用的成本和Token使用情况。

□ 用tiktoken手动计算Token数 : 可以在本地计算Token数,避免调用API时的额外成本。

□ 理解LLM API的定价模型 : 知道不同模型的成本结构,能够合理规划资源使用。

□ 实现基本的成本优化策略 : 如缓存常用结果、批量处理等,减少API调用次数和成本 : 缓存常用结果可以避免重复调用,批量处理可以减少Token使用。

□ 定义Pydantic数据模型 : 用于结构化输出,确保数据格式正确。

□ 使用PydanticOutputParser : 从LLM输出中解析Pydantic模型。

□ 使用JsonOutputParser : 从LLM输出中解析JSON格式数据。

□ 使用OutputFixingParser处理错误 : 自动修复LLM输出中的格式错误。

□ 实现信息提取功能 : 从文本中提取结构化信息。

□ 批量处理多个数据 : 同时处理多个输入,提高效率。

□ 组合使用多种功能(流式+追踪+结构化) : 实现复杂的LLM应用

□ 在实际项目中应用这些技术 : 如聊天机器人、信息提取系统等
```

---

## 🔗 与其他部分的关系

```
Day 1-2: 基础和提示词设计
    ↓
Day 3-4: 模型I/O (当前)
    └─ 学会与LLM交互的方式
    ↓
Day 5+: Chain、Agent、RAG等
    └─ 使用这些基础构建复杂系统
```

---

## 💡 常见问题解答

### Q1: 流式输出成本会更高吗?

**A**: 不会! 流式输出的总Token数和成本与普通调用完全相同，只是返回方式不同。

### Q2: 什么时候用LLM而不是Chat Model?

**A**: 99%场景都应该用Chat Model。LLM只在用很旧的模型时才使用。

### Q3: 结构化输出可靠吗?

**A**: LLM可能不完全遵守格式，需要:
- 使用temperature=0
- 清晰的format_instructions
- OutputFixingParser自动修复
- 异常处理和重试

### Q4: 如何让LLM更准确地遵守结构?

**A**: 在Prompt中给出具体示例:

```python
prompt = f"""
从文本提取信息，必须严格遵守以下JSON格式:

{{
  "name": "张三",
  "age": 25,
  "city": "北京"
}}

原始文本: ...
{parser.get_format_instructions()}
"""
```

---

## 📊 性能和成本总结

```
| 功能 | 额外开销 | 推荐使用 |
|------|---------|---------|
| 流式输出 | 网络请求略多 | ✅ 长文本、Web应用 |
| Token追踪 | 几乎无 | ✅ 所有场景 |
| 结构化输出 | format_instructions占Token | ✅ 需要结构化数据 |
| 异步 | 取决于应用 | ✅ 高并发场景 |
```

---

## 🎯 Day3-4之后能做什么

学完Day3-4后，你可以:

```
✅ 构建基础的聊天机器人
✅ 实现信息提取系统
✅ 控制API成本
✅ 为Web应用提供流式响应
✅ 获得结构化的LLM输出

为接下来学习做准备:
  → Day 5+: 学习Chain和Agent
  → 高级功能: RAG、微调、部署等
```

---

## 💪 老王的建议

```
艹，这部分内容很实用，有几个建议:

1. 一定要跑代码，别tm只看
   每个示例都试一遍，理解实际效果

2. 最实用的技能:
   ✅ 流式输出 (提升用户体验)
   ✅ Token追踪 (控制成本)
   ✅ 结构化输出 (获得可用数据)

3. 生产环境必须做的:
   ✅ 配置异常处理
   ✅ 实现重试机制
   ✅ 监控Token使用
   ✅ 设置用户级配额

4. 常见坑:
   ❌ 忘记处理LLM的输出错误
   ❌ 没有追踪成本，费用超支
   ❌ 流式输出的flush处理不对
   ❌ 结构化输出没有验证

   都要注意!

5. 和第二部分(提示词)的关系:
   第2部分教你怎样问 (提示词)
   第3-4部分教你怎样用 (交互方式)
   两个都重要!
```

---

**笔记状态**: ✅ 完成
**学习时间**: 1-2小时深度学习
**实践时间**: 2-3小时动手项目
**总掌握时间**: 4-5小时

这部分内容是LangChain的核心基础，理解透彻了，后面的Chain、Agent、RAG等高级功能会轻松很多！🚀
