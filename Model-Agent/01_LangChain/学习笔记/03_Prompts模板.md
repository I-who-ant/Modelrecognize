# Day 5-7: Prompts模板

> **学习日期**: _____年___月___日 - _____年___月___日
> **学习目标**: 掌握LangChain的Prompts模板系统，学会优雅地管理提示词，提升Prompt工程能力

---

## 📖 为什么需要Prompt模板?

### 问题场景

**没有模板时的困境**:

```python
# 硬编码的Prompt，维护困难
def translate(text, target_lang):
    prompt = f"Please translate the following text to {target_lang}: {text}"
    return llm.invoke(prompt)

# 问题：
# 1. Prompt散落在代码各处，难以维护
# 2. 修改Prompt需要改代码
# 3. 无法复用Prompt逻辑
# 4. 难以版本管理
# 5. 团队协作困难
```

**使用模板后**:

```python
from langchain_core.prompts import PromptTemplate

# 定义可复用的模板
translate_template = PromptTemplate(
    input_variables=["text", "target_lang"],
    template="Please translate the following text to {target_lang}:\n\n{text}"
)

# 灵活使用
prompt = translate_template.format(text="Hello", target_lang="Chinese")
```

**优势**:
- ✅ 集中管理Prompt
- ✅ 支持变量替换
- ✅ 可序列化和版本控制
- ✅ 易于测试和调试
- ✅ 团队协作友好

---

## 🎯 PromptTemplate基础

### 核心概念

```
┌──────────────────────────────────────────┐
│         PromptTemplate 组成               │
├──────────────────────────────────────────┤
│                                          │
│  Template String (模板字符串)             │
│  ┌────────────────────────────────┐     │
│  │ "Translate {text} to {lang}"   │     │
│  └────────────────────────────────┘     │
│           ↓                              │
│  Input Variables (输入变量)               │
│  ┌────────────────────────────────┐     │
│  │ ["text", "lang"]               │     │
│  └────────────────────────────────┘     │
│           ↓                              │
│  Format Method (格式化方法)               │
│  ┌────────────────────────────────┐     │
│  │ format(text="Hi", lang="中文")  │     │
│  └────────────────────────────────┘     │
│           ↓                              │
│  Final Prompt (最终Prompt)               │
│  ┌────────────────────────────────┐     │
│  │ "Translate Hi to 中文"          │     │
│  └────────────────────────────────┘     │
│                                          │
└──────────────────────────────────────────┘
```

### 基础示例

```python
from langchain_core.prompts import PromptTemplate

# 方式1: 使用from_template快速创建
template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}"
)

# 方式2: 完整定义
template = PromptTemplate(
    input_variables=["adjective", "content"],
    template="Tell me a {adjective} joke about {content}"
)

# 使用模板
prompt = template.format(adjective="funny", content="programming")
print(prompt)
# 输出: Tell me a funny joke about programming

# 直接传给LLM
response = llm.invoke(template.format(adjective="funny", content="AI"))
```

### 变量验证

```python
# LangChain会自动验证变量
template = PromptTemplate(
    input_variables=["name", "age"],
    template="Hello {name}, you are {age} years old"
)

# ✅ 正确使用
template.format(name="张三", age=25)

# ❌ 会报错：缺少必需变量
template.format(name="张三")  # 缺少age

# ❌ 会报错：多余变量
template.format(name="张三", age=25, city="北京")
```

---

## 💬 ChatPromptTemplate

### 为什么需要ChatPromptTemplate?

Chat Models使用**消息列表**而不是单个字符串，所以需要专门的模板:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

# 构建对话模板
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，擅长{skill}"),
    ("human", "{user_input}"),
])

# 生成消息列表
messages = chat_template.format_messages(
    role="Python导师",
    skill="解释复杂概念",
    user_input="什么是装饰器?"
)

# 直接传给Chat Model
response = chat_model.invoke(messages)
```

### 消息类型

LangChain支持多种消息类型的模板:

| 类型 | 简写 | 用途 |
|-----|------|------|
| SystemMessagePromptTemplate | "system" | 设定AI角色和行为 |
| HumanMessagePromptTemplate | "human" / "user" | 用户输入 |
| AIMessagePromptTemplate | "ai" / "assistant" | AI回复 |

### 完整示例

```python
from langchain_core.prompts import ChatPromptTemplate

# 方式1: 使用字符串元组(推荐，简洁)
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，你的特点是{trait}"),
    ("human", "你好！"),
    ("ai", "你好！有什么我可以帮助你的吗？"),
    ("human", "{user_question}")
])

# 方式2: 使用消息模板类(详细控制)
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

system_template = SystemMessagePromptTemplate.from_template(
    "你是{role}，你的特点是{trait}"
)
human_template = HumanMessagePromptTemplate.from_template(
    "{user_question}"
)

template = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])

# 使用
messages = template.format_messages(
    role="Python专家",
    trait="用简单语言解释复杂概念",
    user_question="什么是闭包?"
)
```

### 部分变量 (Partial Variables)

有些变量可以预先设置:

```python
# 创建带部分变量的模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}，今天是{date}"),
    ("human", "{question}")
])

# 部分填充
from datetime import datetime

partial_template = template.partial(
    date=lambda: datetime.now().strftime("%Y-%m-%d")
)

# 使用时只需提供剩余变量
messages = partial_template.format_messages(
    role="助手",
    question="今天天气如何?"
)
```

---

## 🎨 自定义Prompts模板

### 条件渲染

使用Jinja2语法实现条件逻辑:

```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    """
你是一个{role}。

{% if experience %}
你有{experience}年的经验。
{% endif %}

{% if specialties %}
你的专长包括:
{% for specialty in specialties %}
- {{specialty}}
{% endfor %}
{% endif %}

请回答: {question}
    """,
    template_format="jinja2"
)

# 使用
prompt = template.format(
    role="软件工程师",
    experience=5,
    specialties=["Python", "AI", "Web开发"],
    question="如何优化数据库查询?"
)
```

### 自定义格式化函数

```python
from langchain_core.prompts import StringPromptTemplate
from pydantic import BaseModel, validator

class CustomPromptTemplate(StringPromptTemplate):
    """自定义Prompt模板"""

    template: str
    """模板字符串"""

    def format(self, **kwargs) -> str:
        # 自定义格式化逻辑
        # 例如：自动大写某些关键词
        formatted_kwargs = {}
        for key, value in kwargs.items():
            if key == "name":
                formatted_kwargs[key] = value.upper()
            else:
                formatted_kwargs[key] = value

        return self.template.format(**formatted_kwargs)

# 使用
template = CustomPromptTemplate(
    input_variables=["name", "task"],
    template="Hello {name}, please {task}"
)

prompt = template.format(name="john", task="write code")
print(prompt)
# 输出: Hello JOHN, please write code
```

### 组合模板

```python
from langchain_core.prompts import PromptTemplate

# 定义子模板
context_template = PromptTemplate.from_template(
    "Context: {context}"
)

question_template = PromptTemplate.from_template(
    "Question: {question}"
)

# 组合
combined_template = PromptTemplate.from_template(
    """{context_part}

{question_part}

Please answer based on the context above."""
)

# 使用
context = context_template.format(context="LangChain is a framework...")
question = question_template.format(question="What is LangChain?")

final_prompt = combined_template.format(
    context_part=context,
    question_part=question
)
```

---

## 📚 Few-Shot提示词

### 什么是Few-Shot Learning?

Few-Shot Learning是通过提供**少量示例**来引导模型的行为:

```
Zero-Shot (零样本):
"将下面的英文翻译成中文: Hello"

Few-Shot (少样本):
"将下面的英文翻译成中文:
示例1: Apple → 苹果
示例2: Book → 书
现在翻译: Hello"
```

### FewShotPromptTemplate

```python
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate
)

# 1. 定义示例
examples = [
    {
        "question": "什么是Python?",
        "answer": "Python是一门解释型、面向对象的编程语言。"
    },
    {
        "question": "什么是JavaScript?",
        "answer": "JavaScript是一门主要用于Web开发的脚本语言。"
    }
]

# 2. 定义示例格式模板
example_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="问题: {question}\n答案: {answer}"
)

# 3. 创建Few-Shot模板
few_shot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    prefix="你是一个编程语言专家，请简洁地回答问题。\n",
    suffix="问题: {input}\n答案:",
    input_variables=["input"]
)

# 4. 使用
prompt = few_shot_template.format(input="什么是Rust?")
print(prompt)
```

**输出**:
```
你是一个编程语言专家，请简洁地回答问题。

问题: 什么是Python?
答案: Python是一门解释型、面向对象的编程语言。

问题: 什么是JavaScript?
答案: JavaScript是一门主要用于Web开发的脚本语言。

问题: 什么是Rust?
答案:
```

### 动态Few-Shot (示例选择器)

根据输入动态选择最相关的示例:

```python
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 准备大量示例
examples = [
    {"input": "快乐", "output": "悲伤"},
    {"input": "高", "output": "低"},
    {"input": "炎热", "output": "寒冷"},
    {"input": "聪明", "output": "愚蠢"},
    {"input": "胖", "output": "瘦"},
]

# 创建示例选择器
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k=2  # 选择最相关的2个示例
)

# 创建动态Few-Shot模板
dynamic_template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate(
        input_variables=["input", "output"],
        template="输入: {input}\n输出: {output}"
    ),
    prefix="给出下列词的反义词:\n",
    suffix="输入: {adjective}\n输出:",
    input_variables=["adjective"]
)

# 使用
prompt = dynamic_template.format(adjective="大")
print(prompt)
# 会自动选择最相关的示例(如"高→低")
```

---

## 💾 序列化模板

### 为什么要序列化?

1. **版本控制**: 将Prompt存为文件，使用Git管理
2. **团队协作**: 非技术人员也能编辑Prompt
3. **A/B测试**: 轻松切换不同版本的Prompt
4. **多语言支持**: 不同语言的Prompt分开管理

### 保存和加载

```python
from langchain_core.prompts import PromptTemplate
import json

# 创建模板
template = PromptTemplate(
    input_variables=["product", "language"],
    template="Translate the product name '{product}' to {language}"
)

# 保存为JSON
template_json = template.save("prompts/translate_template.json")

# 保存为YAML
template_yaml = template.save("prompts/translate_template.yaml")

# 从文件加载
from langchain_core.prompts import load_prompt

loaded_template = load_prompt("prompts/translate_template.json")
```

**JSON格式示例**:

```json
{
    "_type": "prompt",
    "input_variables": ["product", "language"],
    "template": "Translate the product name '{product}' to {language}",
    "template_format": "f-string"
}
```

**YAML格式示例**:

```yaml
_type: prompt
input_variables:
  - product
  - language
template: "Translate the product name '{product}' to {language}"
template_format: f-string
```

### 组织Prompt库

```
prompts/
├── common/
│   ├── translate.yaml
│   ├── summarize.yaml
│   └── explain.yaml
├── chat/
│   ├── customer_service.yaml
│   ├── tutor.yaml
│   └── assistant.yaml
└── analysis/
    ├── sentiment.yaml
    └── extract.yaml
```

---

## 🎓 提示词工程最佳实践

### 1. 清晰的指令

```python
# ❌ 不好：模糊
template = PromptTemplate.from_template(
    "关于{topic}"
)

# ✅ 好：明确
template = PromptTemplate.from_template(
    """请用100字以内，通俗易懂的语言解释以下概念：

主题: {topic}

要求:
1. 避免使用专业术语
2. 使用比喻或例子
3. 突出核心要点"""
)
```

### 2. 结构化输出要求

```python
template = PromptTemplate.from_template(
    """分析以下产品评价的情感倾向：

评价: {review}

请按以下格式输出:
- 情感: [positive/negative/neutral]
- 置信度: [0-100]
- 关键词: [列出3-5个关键词]
- 原因: [一句话说明判断依据]"""
)
```

### 3. 提供上下文

```python
template = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的{role}。

背景信息:
{context}

你的任务是{task}。

请注意:
{constraints}"""),
    ("human", "{question}")
])
```

### 4. 控制输出长度

```python
template = PromptTemplate.from_template(
    """请用{length}字左右回答以下问题：

问题: {question}

答案:"""
)

# 使用
prompt = template.format(length=50, question="什么是LangChain?")
```

### 5. 角色扮演

```python
template = ChatPromptTemplate.from_messages([
    ("system", """你是{character}，具有以下特点：
- 性格: {personality}
- 说话风格: {style}
- 专长: {expertise}

请始终保持这个角色来回答问题。"""),
    ("human", "{question}")
])
```

---

## 🔗 Pipeline模板组合

### PipelinePromptTemplate

将多个模板组合成流水线:

```python
from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate

# 定义各个部分的模板
intro_template = PromptTemplate.from_template(
    "你是一个{role}，你的特长是{specialty}。"
)

context_template = PromptTemplate.from_template(
    "以下是相关背景信息：\n{context}"
)

question_template = PromptTemplate.from_template(
    "请回答：{question}"
)

# 组合成流水线
full_template = PromptTemplate.from_template(
    """{intro}

{context_section}

{question_section}"""
)

pipeline = PipelinePromptTemplate(
    final_prompt=full_template,
    pipeline_prompts=[
        ("intro", intro_template),
        ("context_section", context_template),
        ("question_section", question_template)
    ]
)

# 使用
prompt = pipeline.format(
    role="Python导师",
    specialty="解释复杂概念",
    context="装饰器是Python的高级特性...",
    question="请举一个装饰器的例子"
)
```

---

## ✅ Day 5-7 学习检查清单

完成以下任务，确保你掌握了本节内容:

- [ ] 理解为什么需要Prompt模板
- [ ] 掌握PromptTemplate的基本用法
- [ ] 掌握ChatPromptTemplate的消息组合
- [ ] 能够创建Few-Shot提示词
- [ ] 理解示例选择器的原理
- [ ] 能够序列化和加载模板
- [ ] 掌握自定义模板的方法
- [ ] 理解Prompt工程最佳实践
- [ ] 能够组合多个模板

---

## 🤔 思考题

1. **什么时候应该使用Few-Shot而不是Zero-Shot?**
   <details>
   <summary>点击查看答案</summary>

   Few-Shot适用于:
   - 任务格式复杂，需要示例说明
   - 输出格式有特定要求
   - Zero-Shot效果不佳
   - 需要保持特定的风格或语气

   Zero-Shot适用于:
   - 任务简单明确
   - 模型已经理解任务类型
   - 希望节省Token
   </details>

2. **如何选择动态还是静态Few-Shot示例?**
   <details>
   <summary>点击查看答案</summary>

   **动态(SemanticSimilarityExampleSelector)**:
   - 示例库很大
   - 输入多样化
   - 希望选择最相关的示例

   **静态(固定示例)**:
   - 示例数量少
   - 所有输入都相关
   - 希望节省成本(不需要embedding)
   </details>

3. **序列化模板的最佳实践是什么?**
   <details>
   <summary>点击查看答案</summary>

   - 使用YAML格式(更易读)
   - 按功能分类存储
   - 加入版本注释
   - 使用Git进行版本控制
   - 定期review和优化
   - 建立Prompt测试集
   </details>

---

## 📝 实践作业

### 作业1: 创建一个多语言翻译模板库

要求:
- 支持多种目标语言
- 使用Few-Shot示例
- 可序列化保存
- 支持专业术语翻译

### 作业2: 实现智能客服对话模板

要求:
- 定义多种客服角色(售前、售后、技术支持)
- 使用ChatPromptTemplate
- 包含上下文信息
- 支持多轮对话

### 作业3: 构建代码解释器模板

要求:
- 使用Few-Shot示例
- 支持多种编程语言
- 结构化输出(代码+解释)
- 可配置详细程度

---

## 📖 推荐阅读

1. **官方文档**:
   - [Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
   - [Few-Shot Examples](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples/)

2. **源码阅读**:
   - `langchain-master/libs/core/langchain_core/prompts/`

3. **Prompt工程资源**:
   - [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
   - [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)

---

## 📌 下一步学习

完成Day 5-7的学习后，进入:
- **Day 8-10**: 数据连接与向量化
  - 文档加载器
  - 文本切割策略
  - 向量数据库
  - RAG基础

---

**老王提示**: 艹，Prompt模板这部分看着简单，但是用好了能极大提升开发效率！特别是序列化功能，可以让你的Prompt管理得井井有条。记住老王的话：**好的Prompt设计是LLM应用成功的一半**！

**重点**:
1. **模板化思维**: 把Prompt当做代码一样管理
2. **Few-Shot是杀手锏**: 复杂任务必用Few-Shot
3. **序列化很重要**: 便于版本控制和团队协作
4. **Prompt工程是艺术**: 需要不断实践和优化

下一阶段我们学RAG，那才是真正的硬核技术！准备好了吗？💪

**学习完成时间**: _____年___月___日