# Day 11-13: Memory内存系统

## 📚 学习目标

通过3天的学习，你将掌握：

1. **Memory基础概念** - 为什么需要Memory
2. **ConversationBufferMemory** - 完整对话历史
3. **ConversationSummaryMemory** - 摘要压缩
4. **ConversationBufferWindowMemory** - 滑动窗口
5. **ConversationKGMemory** - 知识图谱记忆
6. **VectorStoreBackedMemory** - 向量检索记忆
7. **Memory持久化** - 保存和恢复对话

## 🎯 为什么需要Memory?

### 问题场景

**问题: LLM是无状态的**

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# 第一轮对话
response1 = llm.invoke("我叫张三")
print(response1.content)  # "你好,张三!"

# 第二轮对话
response2 = llm.invoke("我叫什么名字?")
print(response2.content)  # "对不起,我不知道" ❌
```

**问题分析**:
- LLM本身没有记忆
- 每次调用都是独立的
- 无法记住之前的对话内容

**解决方案: Memory系统**

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 添加Memory
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# 第一轮对话
conversation.predict(input="我叫张三")

# 第二轮对话
response = conversation.predict(input="我叫什么名字?")
print(response)  # "你叫张三" ✅
```

## 📖 核心概念

### 1. Memory基础结构

#### ChatMessageHistory

存储对话历史的基础类:

```python
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

# 添加消息
history.add_user_message("你好")
history.add_ai_message("你好!有什么可以帮你的?")
history.add_user_message("今天天气怎么样?")

# 获取消息
messages = history.messages
print(messages)
# [
#   HumanMessage(content='你好'),
#   AIMessage(content='你好!有什么可以帮你的?'),
#   HumanMessage(content='今天天气怎么样?')
# ]
```

**核心方法**:
- `add_user_message(text)`: 添加用户消息
- `add_ai_message(text)`: 添加AI消息
- `messages`: 获取所有消息列表
- `clear()`: 清空历史

### 2. Memory类型对比

| Memory类型 | 存储方式 | Token消耗 | 适用场景 |
|-----------|---------|----------|---------|
| **ConversationBufferMemory** | 完整历史 | ⭐⭐⭐⭐⭐ | 短对话,精确上下文 |
| **ConversationBufferWindowMemory** | 最近N轮 | ⭐⭐⭐ | 长对话,控制成本 |
| **ConversationSummaryMemory** | 摘要压缩 | ⭐⭐ | 长对话,保留要点 |
| **ConversationSummaryBufferMemory** | 摘要+最近 | ⭐⭐⭐ | 混合策略 |
| **ConversationKGMemory** | 知识图谱 | ⭐⭐ | 实体关系记忆 |
| **VectorStoreBackedMemory** | 向量检索 | ⭐ | 超长对话,语义检索 |

### 3. ConversationBufferMemory(完整历史)

#### 基础使用

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# 创建Memory
memory = ConversationBufferMemory()

# 创建对话链
conversation = ConversationChain(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    memory=memory,
    verbose=True  # 显示内部过程
)

# 多轮对话
conversation.predict(input="我是一名Python开发者")
conversation.predict(input="我最喜欢的框架是Django")
conversation.predict(input="我是做什么的?")
# 输出: "你是一名Python开发者,最喜欢的框架是Django"
```

#### 直接使用Memory

```python
memory = ConversationBufferMemory()

# 手动添加消息
memory.save_context(
    {"input": "你好"},
    {"output": "你好!有什么可以帮你?"}
)

memory.save_context(
    {"input": "我叫张三"},
    {"output": "很高兴认识你,张三!"}
)

# 获取历史
print(memory.load_memory_variables({}))
# {
#   'history': 'Human: 你好\nAI: 你好!有什么可以帮你?\nHuman: 我叫张三\nAI: 很高兴认识你,张三!'
# }
```

**特点**:
- ✅ 保留完整对话历史
- ✅ 上下文最完整
- ❌ Token消耗大
- ❌ 不适合长对话

**使用场景**:
- 短对话(< 10轮)
- 需要精确上下文
- 客服咨询初期

### 4. ConversationBufferWindowMemory(滑动窗口)

#### 基础使用

```python
from langchain.memory import ConversationBufferWindowMemory

# 只保留最近3轮对话
memory = ConversationBufferWindowMemory(k=3)

conversation = ConversationChain(
    llm=ChatOpenAI(),
    memory=memory
)

# 进行5轮对话
conversation.predict(input="第1轮")
conversation.predict(input="第2轮")
conversation.predict(input="第3轮")
conversation.predict(input="第4轮")
conversation.predict(input="第5轮")

# 查看历史(只有最近3轮)
print(memory.load_memory_variables({}))
# 只包含第3、4、5轮对话
```

**特点**:
- ✅ 控制Token消耗
- ✅ 保留最近上下文
- ❌ 丢失早期信息
- ❌ 可能遗忘重要信息

**参数调优**:
- `k=1`: 只记住上一轮(适合简单问答)
- `k=3-5`: 平衡记忆和成本(推荐)
- `k=10+`: 较长上下文

**使用场景**:
- 长对话(> 10轮)
- 成本敏感
- 只需关注最近话题

### 5. ConversationSummaryMemory(摘要压缩)

#### 基础使用

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 创建摘要Memory
memory = ConversationSummaryMemory(llm=llm)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# 多轮对话
conversation.predict(input="我是一名软件工程师")
conversation.predict(input="我在北京工作")
conversation.predict(input="我已经工作5年了")
conversation.predict(input="请总结我的信息")

# 查看摘要
print(memory.load_memory_variables({}))
# {
#   'history': '用户是一名在北京工作的软件工程师,有5年工作经验'
# }
```

**工作原理**:

```
原始对话(100 tokens):
Human: 我是软件工程师
AI: 了解,请继续
Human: 我在北京工作
AI: 好的,北京是个好地方
Human: 我工作5年了
AI: 很不错的经验

↓ 压缩

摘要(20 tokens):
用户是在北京工作的软件工程师,有5年经验
```

**特点**:
- ✅ 大幅减少Token消耗
- ✅ 保留关键信息
- ❌ 需要额外LLM调用生成摘要
- ❌ 可能丢失细节

**使用场景**:
- 超长对话(> 20轮)
- 信息密集对话
- 成本优先

### 6. ConversationSummaryBufferMemory(混合策略)

结合摘要和窗口的优势:

```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=100  # Token上限
)

# 工作原理:
# 1. 最近的对话保持完整
# 2. 超过Token限制的旧对话被压缩成摘要
```

**特点**:
- ✅ 平衡完整性和成本
- ✅ 最近对话完整,旧对话摘要
- ✅ 灵活的Token控制

**使用场景**:
- 中长对话(10-50轮)
- 需要平衡记忆和成本
- 推荐的默认选择

### 7. ConversationKGMemory(知识图谱记忆)

提取实体和关系:

```python
from langchain.memory import ConversationKGMemory

memory = ConversationKGMemory(llm=llm)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

conversation.predict(input="张三在北京工作")
conversation.predict(input="他是李四的同事")

# 内部维护知识图谱:
# 张三 --工作地点--> 北京
# 张三 --同事--> 李四
```

**特点**:
- ✅ 提取结构化信息
- ✅ 保留实体关系
- ❌ 需要额外LLM调用
- ❌ 不适合简单对话

**使用场景**:
- 复杂实体关系
- 需要知识推理
- 多人对话

### 8. VectorStoreBackedMemory(向量检索记忆)

使用向量检索相关历史:

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 创建向量库
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings()
)

# 创建Memory
memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
)

# 添加记忆
memory.save_context(
    {"input": "我最喜欢的颜色是蓝色"},
    {"output": "了解,你喜欢蓝色"}
)

memory.save_context(
    {"input": "我的生日是5月1日"},
    {"output": "记住了,5月1日是你的生日"}
)

# 查询相关记忆
result = memory.load_memory_variables({"prompt": "我喜欢什么颜色?"})
# 自动检索到 "我最喜欢的颜色是蓝色" 这条记忆
```

**特点**:
- ✅ 语义检索相关记忆
- ✅ 适合超长对话
- ✅ 只加载相关上下文
- ❌ 可能漏掉非语义相关但重要的信息

**使用场景**:
- 超长对话(> 100轮)
- 话题跳跃频繁
- 需要精准上下文

## 🔧 Memory进阶技巧

### 1. 自定义Memory Key

```python
from langchain.memory import ConversationBufferMemory

# 默认key是"history"
memory = ConversationBufferMemory()

# 自定义key
memory = ConversationBufferMemory(
    memory_key="chat_history",    # 在Prompt中使用的key
    input_key="question",          # 输入key
    output_key="answer"            # 输出key
)
```

### 2. 返回消息列表

```python
# 默认返回字符串
memory = ConversationBufferMemory()
print(memory.load_memory_variables({}))
# {'history': 'Human: 你好\nAI: 你好!'}

# 返回消息列表
memory = ConversationBufferMemory(return_messages=True)
print(memory.load_memory_variables({}))
# {
#   'history': [
#     HumanMessage(content='你好'),
#     AIMessage(content='你好!')
#   ]
# }
```

**使用场景**:
- 需要访问单个消息
- 需要消息的metadata
- 使用ChatPromptTemplate

### 3. Memory持久化

#### 方式1: 序列化到文件

```python
import json

# 保存Memory
history = memory.chat_memory.messages
serialized = [
    {"type": msg.type, "content": msg.content}
    for msg in history
]

with open("memory.json", "w") as f:
    json.dump(serialized, f)

# 加载Memory
with open("memory.json", "r") as f:
    data = json.load(f)

from langchain.schema import HumanMessage, AIMessage

memory = ConversationBufferMemory()
for msg in data:
    if msg["type"] == "human":
        memory.chat_memory.add_user_message(msg["content"])
    else:
        memory.chat_memory.add_ai_message(msg["content"])
```

#### 方式2: 使用数据库

```python
from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# SQLite数据库
history = SQLChatMessageHistory(
    session_id="user_123",
    connection_string="sqlite:///chat_history.db"
)

# 使用方式相同
history.add_user_message("你好")
history.add_ai_message("你好!")

# 获取消息
messages = history.messages
```

**支持的后端**:
- SQLite
- PostgreSQL
- Redis
- MongoDB
- DynamoDB

### 4. 多Memory组合

```python
from langchain.memory import CombinedMemory, ConversationBufferMemory

# 实体Memory
entity_memory = ConversationEntityMemory(llm=llm)

# 对话Memory
conversation_memory = ConversationBufferWindowMemory(k=5)

# 组合Memory
memory = CombinedMemory(memories=[entity_memory, conversation_memory])

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

## 📊 Memory选择决策树

```
对话轮数?
├─ < 10轮
│   └─ ConversationBufferMemory (完整历史)
│
├─ 10-20轮
│   ├─ 成本敏感?
│   │   ├─ 是 → ConversationBufferWindowMemory (k=5)
│   │   └─ 否 → ConversationSummaryBufferMemory
│   │
│   └─ ConversationBufferMemory (如果Token允许)
│
├─ 20-50轮
│   └─ ConversationSummaryBufferMemory (推荐)
│
└─ > 50轮
    ├─ 话题连贯?
    │   ├─ 是 → ConversationSummaryMemory
    │   └─ 否 → VectorStoreRetrieverMemory
    │
    └─ 实体关系复杂?
        └─ 是 → ConversationKGMemory

特殊场景:
- 客服场景 → ConversationBufferWindowMemory (k=3-5)
- 教育辅导 → ConversationSummaryBufferMemory
- 知识问答 → VectorStoreRetrieverMemory
- 角色扮演 → ConversationBufferMemory
```

## ⚠️ 常见问题

### Q1: Memory消耗Token太多?

**解决方案**:

1. **使用窗口Memory**
```python
memory = ConversationBufferWindowMemory(k=3)  # 只保留3轮
```

2. **使用摘要Memory**
```python
memory = ConversationSummaryMemory(llm=llm)
```

3. **混合策略**
```python
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=200  # 限制Token数
)
```

### Q2: 如何清空Memory?

```python
# 方法1: 清空对话历史
memory.clear()

# 方法2: 创建新的Memory实例
memory = ConversationBufferMemory()

# 方法3: 只删除特定消息
history = memory.chat_memory
history.messages = history.messages[-5:]  # 只保留最后5条
```

### Q3: Memory如何与Chain结合?

```python
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import PromptTemplate

# 方式1: ConversationChain(自动管理Memory)
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# 方式2: 自定义Chain
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""历史对话:
{history}

当前输入: {input}
回答:"""
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)
```

### Q4: 如何在多用户场景使用Memory?

```python
# 每个用户独立的Memory
user_memories = {}

def get_memory(user_id):
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory()
    return user_memories[user_id]

# 使用
user_id = "user_123"
memory = get_memory(user_id)
conversation = ConversationChain(llm=llm, memory=memory)
```

### Q5: Memory与RAG如何结合?

```python
from langchain.chains import ConversationalRetrievalChain

# 结合Memory和RAG
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
)

# 多轮问答
qa_chain.invoke({"question": "什么是LangChain?"})
qa_chain.invoke({"question": "它有哪些核心组件?"})  # "它"指代LangChain
```

## 📈 最佳实践

### 1. 选择合适的Memory类型

```python
# ✅ 好的实践 - 根据场景选择
class ChatbotConfig:
    def get_memory(self, scenario: str):
        if scenario == "customer_service":
            # 客服: 最近5轮就够
            return ConversationBufferWindowMemory(k=5)
        elif scenario == "education":
            # 教育: 需要完整上下文
            return ConversationSummaryBufferMemory(
                llm=self.llm,
                max_token_limit=500
            )
        elif scenario == "knowledge_qa":
            # 知识问答: 语义检索
            return VectorStoreRetrieverMemory(
                retriever=self.vectorstore.as_retriever()
            )
        else:
            # 默认
            return ConversationBufferMemory()

# ❌ 不好的实践 - 所有场景都用同一种
memory = ConversationBufferMemory()  # 不考虑场景差异
```

### 2. 监控Token消耗

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    conversation.predict(input="你好")
    print(f"Token消耗: {cb.total_tokens}")
    print(f"成本: ${cb.total_cost:.4f}")
```

### 3. 定期保存Memory

```python
import schedule
import time

def save_memory():
    # 保存到数据库
    save_to_db(memory)

# 每10分钟保存一次
schedule.every(10).minutes.do(save_memory)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### 4. 优雅的错误处理

```python
class SafeMemory:
    def __init__(self, base_memory):
        self.memory = base_memory
        self.backup = []

    def save_context(self, inputs, outputs):
        try:
            self.memory.save_context(inputs, outputs)
            self.backup.append((inputs, outputs))
        except Exception as e:
            print(f"Memory保存失败: {e}")

    def restore_from_backup(self):
        for inputs, outputs in self.backup:
            try:
                self.memory.save_context(inputs, outputs)
            except:
                pass
```

## 🎓 学习检查清单

完成Day 11-13学习后,确保你能够:

- [ ] 理解为什么LLM需要Memory
- [ ] 使用ConversationBufferMemory实现基本对话
- [ ] 配置ConversationBufferWindowMemory控制窗口大小
- [ ] 使用ConversationSummaryMemory压缩对话
- [ ] 选择合适的Memory类型(根据场景)
- [ ] 保存和恢复Memory状态
- [ ] 在多用户场景中管理Memory
- [ ] 结合Memory和RAG实现对话式问答
- [ ] 监控和优化Memory的Token消耗
- [ ] 理解各种Memory的优缺点和适用场景

## 📖 扩展阅读

- [LangChain Memory文档](https://python.langchain.com/docs/modules/memory/)
- [Memory Types详解](https://python.langchain.com/docs/modules/memory/types/)
- [ChatMessageHistory后端](https://python.langchain.com/docs/integrations/memory/)
- [对话式RAG](https://python.langchain.com/docs/use_cases/question_answering/chat_history/)

---

**老王提示**: Memory是实现智能对话的关键！选对Memory类型,能让你的AI既聪明又省钱。记住:

1. **短对话** - ConversationBufferMemory(完整最好)
2. **长对话** - ConversationBufferWindowMemory(成本可控)
3. **超长对话** - ConversationSummaryMemory(压缩摘要)
4. **推荐默认** - ConversationSummaryBufferMemory(平衡之选)

**核心原则**: 没有完美的Memory,只有合适的Memory!根据场景选择,持续监控Token,动态调整策略!💪

**重点**:
1. Memory让LLM有了"记忆力"
2. 不同Memory类型适合不同场景
3. Token消耗是选择Memory的关键考虑因素
4. 持久化Memory才能实现真正的长期对话
5. Memory + RAG = 强大的对话式知识问答系统