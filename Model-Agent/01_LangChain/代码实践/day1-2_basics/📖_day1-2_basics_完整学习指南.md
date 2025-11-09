# 📖 Day 1-2 LangChain 基础完整学习指南

## 目标概览

完成Day 1-2的学习后，你将能够：

- ✅ 快速初始化LangChain的ChatModel
- ✅ 理解和使用LLM的基本调用方法
- ✅ 掌握响应对象的结构和元数据
- ✅ 在不同LLM模型之间灵活切换（OpenAI、DeepSeek等）
- ✅ 理解参数调优（temperature、max_tokens等）
- ✅ 配置和验证开发环境

---

## 📚 核心学习内容

### 1️⃣ 环境配置与检查（第1天上午）

**时间**: 15分钟
**难度**: ⭐ 简单

#### 核心概念

LangChain的第一步就是配置好环境，确保API密钥正确，依赖安装完整。

```python
# 环境配置三步曲

# 第1步：安装依赖
pip install langchain langchain-openai python-dotenv

# 第2步：配置API密钥（创建.env文件）
OPENAI_API_KEY=sk-your-api-key-here

# 第3步：在代码中加载
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

#### 关键点

- 📌 **环境变量管理**：永远不要硬编码API密钥，使用`python-dotenv`加载
- 📌 **依赖版本**：确保`langchain`和`langchain-openai`版本兼容
- 📌 **验证环节**：运行`03_env_check.py`验证配置是否正确

#### 常见问题

**Q: ImportError: No module named 'langchain'**
```bash
# 解决方案
pip install --upgrade langchain langchain-openai
```

**Q: 'OPENAI_API_KEY' not found**
```python
# 检查.env文件位置
# 确保.env文件与脚本在同一目录或父目录
from dotenv import load_dotenv
load_dotenv(verbose=True)  # 显示加载过程
```

---

### 2️⃣ ChatModel基础概念（第1天下午）

**时间**: 30分钟
**难度**: ⭐⭐ 简单

#### 核心概念：什么是ChatModel？

ChatModel是LangChain对聊天模型的抽象，遵循标准的消息接口。

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 初始化一个ChatModel
llm = ChatOpenAI(
    model="gpt-3.5-turbo",      # 模型名称
    temperature=0.7,             # 随机性(0-1)
    max_tokens=500,              # 最大输出长度
    api_key="your-api-key"       # API密钥(也可从.env读取)
)

# 调用模型
response = llm.invoke("你好，请介绍一下LangChain")
print(response.content)  # 获取文本内容
```

#### ChatModel核心参数详解

| 参数 | 类型 | 默认值 | 说明 | 场景 |
|------|------|--------|------|------|
| `model` | str | - | 模型名称(如gpt-3.5-turbo) | 必填 |
| `temperature` | float | 1.0 | 随机性(0=确定, 1=随意) | 0=分析, 0.7=平衡, 1=创意 |
| `max_tokens` | int | - | 最大输出长度 | 控制输出长度和成本 |
| `api_key` | str | - | API密钥 | 通常从环境变量读取 |
| `timeout` | int | 600 | 请求超时(秒) | 处理长时间请求 |
| `top_p` | float | 1.0 | nucleus采样 | 与temperature配合使用 |

#### ChatModel vs LLM

```python
# ChatModel (现代、推荐)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 输入：消息列表
messages = [
    SystemMessage(content="你是Python导师"),
    HumanMessage(content="什么是装饰器?")
]
response = llm.invoke(messages)  # AIMessage对象

# LLM (传统、不推荐)
from langchain_openai import OpenAI
llm = OpenAI(model="text-davinci-003")

# 输入：字符串
response = llm.invoke("什么是装饰器?")  # 直接返回字符串
```

**关键区别**:
- ChatModel: 消息接口 → 更灵活，支持角色、上下文
- LLM: 字符串接口 → 简单但功能有限

---

### 3️⃣ 基础调用方法（第2天上午）

**时间**: 30分钟
**难度**: ⭐⭐ 简单

#### 方法对比

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 方法1: invoke() - 同步调用，等待完整响应
response = llm.invoke("写一个Python函数")
print(response.content)

# 方法2: stream() - 同步流式，逐块接收
for chunk in llm.stream("写一个Python函数"):
    print(chunk.content, end="", flush=True)

# 方法3: batch() - 批量调用多个请求
responses = llm.batch([
    "问题1",
    "问题2",
    "问题3"
])

# 方法4: invoke with messages - 使用消息接口
from langchain_core.messages import SystemMessage, HumanMessage

response = llm.invoke([
    SystemMessage(content="你是编程专家"),
    HumanMessage(content="如何优化这段代码?")
])
```

#### 响应对象结构

```python
response = llm.invoke("Python是什么?")

# 响应对象包含：
print(response.content)                    # 文本内容(str)
print(response.response_metadata)          # 元数据(dict)
print(response.usage_metadata)             # Token使用情况

# 详细的元数据信息
metadata = response.response_metadata
print(f"模型: {metadata.get('model_name')}")
print(f"完成时间: {metadata.get('finish_reason')}")

# Token详情
if 'token_usage' in metadata:
    usage = metadata['token_usage']
    print(f"输入Token: {usage.get('prompt_tokens')}")
    print(f"输出Token: {usage.get('completion_tokens')}")
    print(f"总Token: {usage.get('total_tokens')}")
```

---

### 4️⃣ 模型切换与互换性（第2天下午）

**时间**: 30分钟
**难度**: ⭐⭐⭐ 中等

#### LangChain的核心价值：模型互换性

这是LangChain最强大的特性之一！

```python
# 同一套业务逻辑，轻松切换模型

def ask_ai(question: str, model_type: str = "openai") -> str:
    """统一的问答接口"""

    if model_type == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo")

    elif model_type == "deepseek":
        from langchain_openai import ChatOpenAI
        # DeepSeek提供OpenAI兼容接口
        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key="your-deepseek-key",
            base_url="https://api.deepseek.com/v1"
        )

    elif model_type == "claude":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(model="claude-3-sonnet-20240229")

    elif model_type == "local":
        from langchain_community.llms import Ollama
        llm = Ollama(model="llama2")

    # 业务逻辑完全相同！
    response = llm.invoke(question)
    return response.content

# 使用示例
print(ask_ai("Python是什么?", "openai"))
print(ask_ai("Python是什么?", "deepseek"))
print(ask_ai("Python是什么?", "local"))
```

#### 常见模型配置

**OpenAI (官方推荐)**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key="sk-..."
)
```

**DeepSeek (国内高性价比)**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="sk-...",
    base_url="https://api.deepseek.com/v1"
)
```

**Claude (多模态支持)**
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    api_key="sk-ant-..."
)
```

**本地模型 (免费)**
```python
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama2",
    base_url="http://localhost:11434"
)
```

#### 模型选择决策树

```
成本敏感？
├─ 是 → DeepSeek (GPT-3.5质量, 1/3成本)
└─ 否 → GPT-4 (最强能力)

需要多模态(图片)?
├─ 是 → GPT-4V / Claude-3
└─ 否 → 任意模型

需要完全离线?
└─ 是 → Ollama (Llama2/Mistral)

需要稳定性保证?
└─ 是 → OpenAI (最成熟)
```

---

## 🎯 完整代码示例

### 示例1：基础Hello World

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # 初始化模型
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500
    )

    # 调用模型
    response = llm.invoke("用3句话介绍LangChain")

    # 输出结果
    print("回复:", response.content)
    print("Token使用:", response.response_metadata.get('token_usage'))

if __name__ == "__main__":
    main()
```

### 示例2：多模型对比

```python
from langchain_openai import ChatOpenAI
import json

def compare_models(question: str):
    """对比不同模型的回复"""

    models = [
        {
            "name": "GPT-3.5-turbo",
            "config": {"model": "gpt-3.5-turbo"}
        },
        {
            "name": "DeepSeek",
            "config": {
                "model": "deepseek-chat",
                "base_url": "https://api.deepseek.com/v1"
            }
        }
    ]

    results = {}

    for model_info in models:
        try:
            llm = ChatOpenAI(**model_info["config"])
            response = llm.invoke(question)

            results[model_info["name"]] = {
                "answer": response.content[:100] + "...",
                "tokens": response.response_metadata.get('token_usage', {})
            }
        except Exception as e:
            results[model_info["name"]] = {"error": str(e)}

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    compare_models("什么是大语言模型?")
```

### 示例3：参数调优

```python
from langchain_openai import ChatOpenAI

def demonstrate_parameters():
    """演示不同参数的影响"""

    question = "编一个有趣的编程笑话"

    # 参数1: temperature影响创意程度
    print("=== Temperature对比 ===")

    # 确定性回复(适合分析)
    deterministic = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print("确定性(T=0):", deterministic.invoke(question).content[:50])

    # 创意回复(适合创意)
    creative = ChatOpenAI(model="gpt-3.5-turbo", temperature=1)
    print("创意(T=1):", creative.invoke(question).content[:50])

    # 参数2: max_tokens控制长度
    print("\n=== Max_tokens对比 ===")

    long_response = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=200)
    short_response = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=50)

    print("长回复:", len(long_response.invoke(question).content), "字符")
    print("短回复:", len(short_response.invoke(question).content), "字符")

if __name__ == "__main__":
    demonstrate_parameters()
```

---

## 🚀 学习路径与时间管理

### 第1天（约2小时）

| 时间 | 任务 | 代码文件 |
|------|------|---------|
| 09:00-09:15 | 环境配置 | `03_env_check.py` |
| 09:15-10:00 | ChatModel基础 | `01_hello_world.py` |
| 10:00-11:00 | 参数调优实验 | 自己编写 |

### 第2天（约2小时）

| 时间 | 任务 | 代码文件 |
|------|------|---------|
| 09:00-10:00 | 国产模型测试 | `02_chinese_llm.py` |
| 10:00-10:30 | 模型互换性理解 | 自己编写 |
| 10:30-11:00 | 综合练习 | 自己编写 |

---

## 💡 关键知识点总结

### 1. ChatModel初始化三要素

```python
llm = ChatOpenAI(
    model="gpt-3.5-turbo",    # ✅ 必需：模型名称
    api_key="sk-...",          # ✅ 必需：API密钥(或从环境变量读)
    temperature=0.7            # ❓ 可选：控制创意程度
)
```

### 2. 基础调用模式

```python
# 最简单：一个问题
response = llm.invoke("问题")
answer = response.content

# 进阶：添加角色和上下文
from langchain_core.messages import SystemMessage, HumanMessage
response = llm.invoke([
    SystemMessage(content="你是Python专家"),
    HumanMessage(content="问题")
])
```

### 3. 参数调优的实践建议

| 场景 | temperature | max_tokens | 为什么 |
|------|------------|-----------|--------|
| 数据分析 | 0 | 500 | 需要确定性答案 |
| 内容生成 | 0.7-0.9 | 1000+ | 需要一定创意 |
| 创意写作 | 1.0 | 2000+ | 最大化创意和长度 |
| 代码生成 | 0-0.3 | 800 | 准确性重要 |

### 4. 模型互换性的威力

同一套代码，换一个初始化参数就能用不同模型：

```python
# 快速对比不同模型
models = [
    ChatOpenAI(model="gpt-3.5-turbo"),
    ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com/v1"),
]

for llm in models:
    response = llm.invoke("什么是AI?")
    # 业务逻辑完全相同
```

---

## 🎓 学习成果检查清单

完成Day 1-2学习后，你应该能够：

### 基础认知
- [ ] 解释什么是ChatModel，为什么比LLM更好
- [ ] 理解temperature、max_tokens的作用
- [ ] 知道ChatModel vs LLM的区别

### 实践能力
- [ ] 成功配置环境并验证API密钥
- [ ] 编写最基础的LLM调用代码
- [ ] 理解响应对象的结构和元数据
- [ ] 调整参数(temperature, max_tokens)并观察效果

### 进阶能力
- [ ] 使用消息接口(SystemMessage + HumanMessage)
- [ ] 在至少2个不同模型间切换
- [ ] 编写一个通用的模型调用函数
- [ ] 理解为什么LangChain的模型互换性很重要

### 成果验证
- [ ] ✅ 运行`03_env_check.py`无错误
- [ ] ✅ 运行`01_hello_world.py`获取正常回复
- [ ] ✅ 运行`02_chinese_llm.py`对比模型
- [ ] ✅ 自己编写一个带角色的对话脚本

---

## 📖 深入学习资源

### 官方文档
- [LangChain ChatOpenAI官方文档](https://python.langchain.com/docs/modules/model_io/llms/llm_caching)
- [OpenAI API参考](https://platform.openai.com/docs/api-reference/chat/create)
- [LangChain消息接口](https://python.langchain.com/docs/modules/model_io/messages/)

### 推荐阅读
- 理解Prompt Engineering的基础(Day 5-7会深入)
- 了解Token计数的原理(Day 3-4有详细讲解)
- DeepSeek官方文档(了解高性价比方案)

---

## 🔗 与其他模块的关联

```
Day 1-2: 基础 (你在这里)
    ↓
Day 3-4: 模型I/O (流式输出、Token追踪、结构化输出)
    ↓
Day 5-7: Prompt模板 (提高可复用性)
    ↓
Day 8-10: 数据连接 (加载文档、向量化)
    ↓
Day 11-13: 记忆系统 (实现有状态对话)
    ↓
Day 14-16: 链(Chains) (组合多个操作)
    ↓
Day 17-19: 代理(Agents) (自主决策和规划)
```

---

## 💪 老王的学习建议

> 这部分虽然看似简单，但是**基础很重要**！

### ✅ 必做的三件事

1. **亲自跑代码** - 不要只看，一定要在你的机器上运行每个例子，感受LLM的回复
2. **多试不同参数** - 改变temperature、max_tokens，看效果怎么变
3. **切换不同模型** - 用OpenAI、DeepSeek、本地模型都试一遍，理解互换性

### ❌ 常见的坑

- ❌ 只复制粘贴代码，不理解参数含义
- ❌ 硬编码API密钥(安全风险!)
- ❌ 忽视环境变量配置，导致后续项目出问题
- ❌ 不理解ChatModel和LLM的区别，后面会混淆

### 💡 提高效率的技巧

1. 创建一个`config.py`，集中管理所有模型配置
2. 编写一个`ask_ai()`函数封装LLM调用，后面复用
3. 记录每个模型的性能表现(速度、质量、成本)

---

**准备好了吗？开始Day 1-2的学习吧！下一步进入Day 3-4学习模型I/O的更多高级用法。** 💪

---

*最后更新: 2025-01-09*
*学习时间: 约4小时（Day 1-2）*
