# Day 14-15: LCEL和Chains

## 📚 学习目标

通过2天的学习，你将掌握：

1. **LCEL基础** - LangChain Expression Language
2. **Runnable协议** - 统一的调用接口
3. **管道组合** - 使用 | 操作符链接组件
4. **常用Chains** - LLMChain/SequentialChain/RouterChain
5. **LCEL高级特性** - Fallback/Parallel/Routing
6. **实战应用** - 构建复杂的工作流

## 🎯 为什么需要LCEL和Chains?

### 问题场景

**问题: 组件独立,难以组合**

```python
# 传统方式: 手动组合各个步骤
prompt = PromptTemplate.from_template("翻译: {text}")
formatted = prompt.format(text="Hello")
response = llm.invoke(formatted)
output = parser.parse(response.content)

# 步骤繁琐,难以复用
```

**解决方案: LCEL管道**

```python
# LCEL方式: 优雅的管道组合
chain = prompt | llm | parser

# 一行调用
output = chain.invoke({"text": "Hello"})
```

## 📖 核心概念

### 1. LCEL (LangChain Expression Language)

LCEL是LangChain的表达式语言,用于组合各种组件。

#### 核心理念

```python
# LCEL使用 | 操作符连接组件
chain = component1 | component2 | component3

# 等价于
output = component3(component2(component1(input)))
```

**优势**:
- ✅ 代码简洁优雅
- ✅ 易于理解和维护
- ✅ 支持流式输出
- ✅ 支持异步调用
- ✅ 自动处理输入输出

### 2. Runnable协议

所有LCEL组件都实现了Runnable协议。

#### 核心方法

```python
class Runnable:
    def invoke(self, input):
        """同步调用"""
        pass

    def stream(self, input):
        """流式输出"""
        pass

    async def ainvoke(self, input):
        """异步调用"""
        pass

    async def astream(self, input):
        """异步流式输出"""
        pass

    def batch(self, inputs):
        """批量处理"""
        pass
```

**统一接口的好处**:
- 所有组件调用方式一致
- 可以自由组合
- 支持多种调用模式

### 3. 基础LCEL组合

#### 示例1: Prompt + LLM

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
llm = ChatOpenAI(model="gpt-3.5-turbo")

chain = prompt | llm

response = chain.invoke({"topic": "程序员"})
print(response.content)
```

#### 示例2: Prompt + LLM + Parser

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()

# 直接返回字符串
output = chain.invoke({"topic": "程序员"})
print(output)  # 字符串而非AIMessage对象
```

#### 示例3: 多步骤组合

```python
from langchain_core.prompts import PromptTemplate

# 步骤1: 生成故事大纲
outline_prompt = PromptTemplate.from_template("写一个关于{theme}的故事大纲")
outline_chain = outline_prompt | llm | StrOutputParser()

# 步骤2: 扩展成完整故事
story_prompt = PromptTemplate.from_template("将以下大纲扩展成完整故事:\n{outline}")
story_chain = story_prompt | llm | StrOutputParser()

# 组合两个步骤
full_chain = outline_chain | (lambda x: {"outline": x}) | story_chain

# 一次调用完成全流程
story = full_chain.invoke({"theme": "未来科技"})
```

### 4. 常用Chains类型

#### LLMChain(基础链)

```python
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# 等价LCEL写法
chain = prompt | llm
```

#### SequentialChain(顺序链)

```python
from langchain.chains import SequentialChain

# 步骤1
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="output1")

# 步骤2(使用步骤1的输出)
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="output2")

# 顺序执行
sequential_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["input"],
    output_variables=["output1", "output2"]
)
```

**LCEL替代方案**:
```python
chain = (
    prompt1 | llm | StrOutputParser() |
    (lambda x: {"previous": x}) |
    prompt2 | llm | StrOutputParser()
)
```

#### TransformChain(转换链)

```python
from langchain.chains import TransformChain

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    # 自定义转换逻辑
    return {"output": text.upper()}

transform_chain = TransformChain(
    input_variables=["text"],
    output_variables=["output"],
    transform=transform_func
)

# LCEL替代
transform_chain = lambda x: {"output": x["text"].upper()}
```

### 5. LCEL高级特性

#### RunnablePassthrough(传递输入)

```python
from langchain_core.runnables import RunnablePassthrough

chain = {
    "context": retriever,  # 检索相关文档
    "question": RunnablePassthrough()  # 传递原始问题
} | prompt | llm

# 输入会被传递到question,同时检索到context
response = chain.invoke("LangChain是什么?")
```

#### RunnableParallel(并行执行)

```python
from langchain_core.runnables import RunnableParallel

# 并行执行多个任务
parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain,
    story=story_chain
)

results = parallel_chain.invoke({"topic": "AI"})
# {
#   "joke": "...",
#   "poem": "...",
#   "story": "..."
# }
```

#### RunnableBranch(条件路由)

```python
from langchain_core.runnables import RunnableBranch

def is_question(x):
    return "?" in x["text"]

branch = RunnableBranch(
    (is_question, question_chain),  # 如果是问题,走question_chain
    default_chain  # 否则走default_chain
)

chain = branch | llm
```

#### with_fallbacks(失败回退)

```python
# 主链失败时自动切换到备选链
chain = primary_chain.with_fallbacks([
    fallback_chain1,
    fallback_chain2
])

# 按顺序尝试,直到成功
```

### 6. LCEL与传统Chains对比

| 特性 | 传统Chains | LCEL |
|------|-----------|------|
| 语法 | 类实例化 | 管道操作符 \| |
| 简洁性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 灵活性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 流式支持 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 异步支持 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 学习曲线 | 较陡 | 平缓 |

**推荐**: 新项目优先使用LCEL

## 🔧 LCEL实战模式

### 模式1: 简单提示+生成

```python
chain = prompt | llm | StrOutputParser()
```

### 模式2: RAG(检索增强生成)

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)
```

### 模式3: 多步骤处理

```python
chain = (
    step1_prompt | llm | StrOutputParser() |
    (lambda x: {"step1_output": x}) |
    step2_prompt | llm | StrOutputParser() |
    (lambda x: {"step2_output": x}) |
    step3_prompt | llm | StrOutputParser()
)
```

### 模式4: 并行+聚合

```python
from langchain_core.runnables import RunnableParallel

chain = (
    RunnableParallel(
        summary=summary_chain,
        sentiment=sentiment_chain,
        keywords=keywords_chain
    )
    | aggregate_chain
)
```

### 模式5: 条件路由

```python
from langchain_core.runnables import RunnableBranch

chain = (
    RunnableBranch(
        (lambda x: x["type"] == "question", qa_chain),
        (lambda x: x["type"] == "translation", translate_chain),
        default_chain
    )
)
```

## 📊 Chains选择决策树

```
需求类型?
├─ 简单提示+生成
│   └─ prompt | llm
│
├─ 多步骤处理
│   ├─ 步骤独立?
│   │   ├─ 是 → RunnableParallel(并行)
│   │   └─ 否 → 顺序链接 (step1 | step2 | step3)
│   │
│   └─ 有条件分支?
│       └─ RunnableBranch
│
├─ RAG应用
│   └─ {context: retriever, question: ...} | prompt | llm
│
├─ 需要失败处理?
│   └─ chain.with_fallbacks([...])
│
└─ 需要重试?
    └─ chain.with_retry(...)
```

## ⚠️ 常见问题

### Q1: LCEL vs 传统Chains如何选择?

**推荐LCEL的场景**:
- ✅ 新项目
- ✅ 需要流式输出
- ✅ 需要灵活组合
- ✅ 追求代码简洁

**使用传统Chains的场景**:
- 老项目维护
- 团队不熟悉LCEL
- 使用特定功能的预定义Chain

### Q2: 如何调试LCEL链?

**方法1: 打印中间结果**

```python
def debug_print(x):
    print(f"中间结果: {x}")
    return x

chain = prompt | llm | debug_print | parser
```

**方法2: 使用verbose**

```python
chain = prompt | llm.with_config(verbose=True) | parser
```

**方法3: 分步执行**

```python
# 分开调试
step1 = prompt.invoke({"topic": "AI"})
print(f"Step1: {step1}")

step2 = llm.invoke(step1)
print(f"Step2: {step2}")

step3 = parser.invoke(step2)
print(f"Step3: {step3}")
```

### Q3: LCEL如何处理错误?

**方法1: with_fallbacks**

```python
chain = primary_llm.with_fallbacks([backup_llm])
```

**方法2: with_retry**

```python
chain = llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_multiplier=1
)
```

**方法3: try-except包装**

```python
def safe_invoke(chain, input):
    try:
        return chain.invoke(input)
    except Exception as e:
        return f"错误: {e}"
```

### Q4: 如何优化LCEL性能?

**策略1: 并行执行**

```python
# 将独立任务并行化
chain = RunnableParallel(task1=..., task2=..., task3=...)
```

**策略2: 批量处理**

```python
# 使用batch而非循环invoke
results = chain.batch([input1, input2, input3])
```

**策略3: 异步调用**

```python
# 使用异步
import asyncio

results = await asyncio.gather(*[
    chain.ainvoke(input1),
    chain.ainvoke(input2),
    chain.ainvoke(input3)
])
```

**策略4: 缓存结果**

```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

set_llm_cache(InMemoryCache())
```

## 📈 最佳实践

### 1. 保持链的简洁

```python
# ✅ 好的实践 - 简洁明了
chain = prompt | llm | parser

# ❌ 不好的实践 - 过度复杂
chain = (
    prompt |
    llm |
    lambda x: x.content |
    lambda x: x.strip() |
    lambda x: x.lower() |
    lambda x: x.split() |
    # ... 太多步骤
)
```

### 2. 合理命名变量

```python
# ✅ 好的实践 - 语义化命名
translation_chain = translate_prompt | llm | parser
summary_chain = summary_prompt | llm | parser

# ❌ 不好的实践 - 无意义命名
chain1 = prompt1 | llm | parser
chain2 = prompt2 | llm | parser
```

### 3. 模块化组织

```python
# ✅ 好的实践 - 模块化
def create_translation_chain(llm):
    return translate_prompt | llm | parser

def create_summary_chain(llm):
    return summary_prompt | llm | parser

# 组合使用
translation = create_translation_chain(llm)
summary = create_summary_chain(llm)

# ❌ 不好的实践 - 重复代码
chain1 = translate_prompt | ChatOpenAI() | StrOutputParser()
chain2 = summary_prompt | ChatOpenAI() | StrOutputParser()
```

### 4. 错误处理

```python
# ✅ 好的实践 - 失败回退
chain = primary_chain.with_fallbacks([backup_chain])

# ❌ 不好的实践 - 无错误处理
chain = prompt | llm | parser  # 失败了怎么办?
```

### 5. 性能优化

```python
# ✅ 好的实践 - 并行执行独立任务
parallel_chain = RunnableParallel(
    task1=chain1,
    task2=chain2
)

# ❌ 不好的实践 - 串行执行独立任务
result1 = chain1.invoke(input)
result2 = chain2.invoke(input)  # 可以并行
```

## 🎓 学习检查清单

完成Day 14-15学习后,确保你能够:

- [ ] 理解LCEL的核心理念
- [ ] 使用 | 操作符组合组件
- [ ] 掌握Runnable协议的核心方法
- [ ] 使用RunnablePassthrough传递输入
- [ ] 使用RunnableParallel并行执行
- [ ] 使用RunnableBranch实现条件路由
- [ ] 实现失败回退(with_fallbacks)
- [ ] 实现重试机制(with_retry)
- [ ] 调试LCEL链
- [ ] 优化LCEL性能
- [ ] 构建复杂的工作流

## 📖 扩展阅读

- [LCEL文档](https://python.langchain.com/docs/expression_language/)
- [Runnable接口](https://python.langchain.com/docs/expression_language/interface)
- [LCEL Cookbook](https://python.langchain.com/docs/expression_language/cookbook/)
- [Chains文档](https://python.langchain.com/docs/modules/chains/)

---

**老王提示**: LCEL是LangChain的精髓！用好 | 操作符,你就能像搭积木一样构建复杂应用。记住:

1. **简单任务** - `prompt | llm | parser`
2. **RAG应用** - `{context: retriever, question: ...} | prompt | llm`
3. **多步骤** - `step1 | step2 | step3`
4. **并行执行** - `RunnableParallel(...)`
5. **条件路由** - `RunnableBranch(...)`

**核心原则**: 保持链的简洁、模块化、可复用!

**LCEL三大优势**:
1. **简洁优雅** - 代码可读性极高
2. **功能强大** - 流式/异步/并行都支持
3. **易于组合** - 像乐高积木一样自由组合

**重点**:
1. LCEL用 | 连接组件,形成数据流管道
2. 所有组件都实现Runnable协议,统一接口
3. 支持流式、异步、批量、并行等多种模式
4. 比传统Chains更简洁、灵活、强大
5. 新项目强烈推荐使用LCEL