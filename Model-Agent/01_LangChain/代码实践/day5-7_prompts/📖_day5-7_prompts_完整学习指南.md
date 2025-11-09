# 📖 Day 5-7 Prompts模板完整学习指南

## 目标概览

完成Day 5-7的学习后，你将能够：

- ✅ 掌握PromptTemplate和ChatPromptTemplate的创建与使用
- ✅ 实现Few-Shot学习提高模型输出质量
- ✅ 使用动态示例选择器实现智能Prompting
- ✅ 序列化和管理Prompt，构建Prompt库
- ✅ 理解Prompt工程的最佳实践
- ✅ 设计和优化复杂的多步骤Prompt

---

## 📚 核心学习内容

### 1️⃣ PromptTemplate基础（第5天上午）

**时间**: 45分钟
**难度**: ⭐⭐ 简单

#### 核心概念：为什么需要PromptTemplate？

在实际项目中，你会发现：

- ❌ 直接拼接字符串很容易出错
- ❌ 难以管理和版本控制Prompt
- ❌ 无法复用Prompt
- ❌ 修改Prompt需要改代码

**PromptTemplate的作用**：
- ✅ 模板化管理Prompt
- ✅ 自动验证变量
- ✅ 易于版本控制
- ✅ 支持序列化和加载

#### 三种创建方式

```python
from langchain_core.prompts import PromptTemplate

# 方式1：from_template (最简洁，推荐)
template1 = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}"
)

# 方式2：完整定义(更灵活)
template2 = PromptTemplate(
    input_variables=["adjective", "content"],
    template="Tell me a {adjective} joke about {content}",
    template_format="f-string"  # 默认
)

# 方式3：从文件加载(后面学)
# template = load_prompt_from_config("prompt.yaml")
```

#### 变量验证和使用

```python
template = PromptTemplate(
    input_variables=["name", "age", "city"],
    template="My name is {name}, I am {age} years old, and I live in {city}."
)

# ✅ 正确使用：提供所有变量
prompt = template.format(name="张三", age=25, city="北京")
# 输出: My name is 张三, I am 25 years old, and I live in 北京.

# ❌ 错误：缺少变量
try:
    template.format(name="张三", age=25)  # 缺少city
except KeyError as e:
    print(f"错误: 缺少变量 {e}")

# ✅ 多余变量会被忽略(不会报错)
prompt = template.format(
    name="张三", age=25, city="北京", country="中国"
)  # country会被忽略
```

#### 实践示例

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 定义模板
template = PromptTemplate.from_template(
    """你是一个{role}。

请用{length}字以内用{language}语言回答下面的问题：
{question}"""
)

# 使用模板
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = template.format(
    role="Python专家",
    length="100",
    language="简体中文",
    question="什么是装饰器?"
)

response = llm.invoke(prompt)
print(response.content)
```

---

### 2️⃣ ChatPromptTemplate进阶（第5天下午）

**时间**: 45分钟
**难度**: ⭐⭐⭐ 中等

#### 核心概念：ChatPromptTemplate的威力

ChatPromptTemplate专门为对话模型设计，支持消息角色(System, Human, AI)。

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# 方式1：from_messages (最推荐)
template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("human", "{question}")
])

# 使用时自动生成消息列表
messages = template.format_messages(
    role="Python导师",
    question="什么是装饰器?"
)
# 输出: [SystemMessage(...), HumanMessage(...)]

# 方式2：完整定义
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_template = SystemMessagePromptTemplate.from_template(
    "You are a {role}."
)
human_template = HumanMessagePromptTemplate.from_template(
    "{question}"
)

template = ChatPromptTemplate.from_messages([
    system_template,
    human_template
])
```

#### ChatPromptTemplate的优势

对比普通PromptTemplate：

```python
# 普通PromptTemplate
template1 = PromptTemplate.from_template(
    "You are a {role}.\nHuman: {question}\nAssistant:"
)
prompt1 = template1.format(role="expert", question="问题")
# 输出：字符串

# ChatPromptTemplate
template2 = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("human", "{question}")
])
messages = template2.format_messages(role="expert", question="问题")
# 输出：[SystemMessage, HumanMessage]

# ChatPromptTemplate的优势：
# 1. 结构清晰，易于管理
# 2. 支持完整的消息接口
# 3. 便于添加更多角色(system, human, ai)
# 4. LLM会更好地理解角色信息
```

#### 实践示例：多轮对话模板

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

template = ChatPromptTemplate.from_messages([
    ("system", """你是一个友好的编程助手。
    - 给出的代码要有注释
    - 解释复杂的概念要用简单的语言
    - 每个回答不超过500字"""),
    ("human", "请介绍{language}的基本特点"),
    ("ai", "{previous_response}"),  # 添加历史
    ("human", "{follow_up_question}")
])

messages = template.format_messages(
    language="Python",
    previous_response="Python是一门简洁易学的语言...",
    follow_up_question="那Ruby呢?"
)
```

---

### 3️⃣ Few-Shot Learning（第6天上午）

**时间**: 1小时
**难度**: ⭐⭐⭐⭐ 困难

#### 核心概念：什么是Few-Shot？

Few-Shot（少样本学习）：通过给出几个示例来指导模型，而不是长篇大论的说明。

```python
# Zero-Shot: 没有示例
prompt = "什么的反义词是什么？high的反义词是什么？"

# Few-Shot: 给出示例
prompt = """
例子：
问题: 什么的反义词？happy的反义词是什么？
答案: sad

问题: 什么的反义词？tall的反义词是什么？
答案: short

现在你来回答：
问题: 什么的反义词？big的反义词是什么？
答案:"""
```

#### 基本的Few-Shot实现

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# 定义示例
examples = [
    {
        "input": "happy",
        "output": "sad"
    },
    {
        "input": "tall",
        "output": "short"
    },
    {
        "input": "bright",
        "output": "dark"
    }
]

# 定义如何格式化每个示例
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

# 创建Few-Shot模板
template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="给出单词的反义词：",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"]
)

# 使用
prompt = template.format(word="big")
print(prompt)
```

#### 动态示例选择(最强功能)

**场景**: 不同的问题需要不同的示例，自动选择最相关的示例！

```python
from langchain_core.prompts.few_shot import FewShotPromptTemplate, SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 示例库
examples = [
    {"input": "幸福", "output": "快乐是内心的满足感"},
    {"input": "悲伤", "output": "悲伤是对损失的感受"},
    {"input": "勇气", "output": "勇气是在恐惧中坚持的能力"},
    {"input": "智慧", "output": "智慧是正确判断和行动的能力"},
]

# 创建向量存储，使用语义相似度选择示例
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    Chroma,
    k=2  # 每次选择2个最相关的示例
)

# 创建Few-Shot模板
template = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate(
        input_variables=["input", "output"],
        template="词语: {input}\n定义: {output}"
    ),
    prefix="根据示例定义词语：",
    suffix="词语: {word}\n定义:",
    input_variables=["word"]
)

# 使用：会自动选择最相关的示例！
prompt = template.format(word="希望")
print(prompt)  # 会自动选择与"希望"最相关的示例
```

#### Few-Shot的威力对比

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

question = "请分析以下句子的情感：产品太差了，浪费钱"

# Zero-Shot: 直接问
print("Zero-Shot:")
response = llm.invoke(f"""分析情感，回答格式：
情感: [positive/negative/neutral]
置信度: [0-100]
原因: [简短原因]

句子: {question}""")
print(response.content)

# Few-Shot: 给示例
print("\nFew-Shot:")
response = llm.invoke(f"""示例：
句子: 这个产品太棒了，强烈推荐！
情感: positive
置信度: 95
原因: 使用了"棒"和"强烈推荐"等正面词汇

句子: 这个产品太差了，浪费钱
情感: negative
置信度: 90
原因: 使用了"差"和"浪费"等负面词汇

现在分析：
句子: {question}
情感:""")
print(response.content)
```

**结果**：Few-Shot通常会显著提高输出质量和一致性！

---

### 4️⃣ Prompt序列化与管理（第6天下午 + 第7天）

**时间**: 1.5小时
**难度**: ⭐⭐⭐ 中等

#### 为什么需要序列化？

- ✅ 版本控制：Prompt也是代码，需要Git管理
- ✅ 团队协作：非技术人员可以编辑YAML配置
- ✅ 配置管理：不同环境用不同Prompt
- ✅ 易于审核：Prompt变更有完整记录

#### 序列化格式对比

**YAML格式(推荐)**

```yaml
# prompts/translation.yaml
_type: prompt
input_variables:
  - text
  - language
template: |
  翻译以下文本到{language}:

  {text}

  翻译结果:
template_format: f-string
```

**JSON格式**

```json
{
  "_type": "prompt",
  "input_variables": ["text", "language"],
  "template": "翻译以下文本到{language}:\n\n{text}\n\n翻译结果:",
  "template_format": "f-string"
}
```

**Few-Shot YAML**

```yaml
_type: few_shot
input_variables:
  - word
examples:
  - input: happy
    output: sad
  - input: tall
    output: short
example_prompt:
  _type: prompt
  input_variables: [input, output]
  template: "Input: {input}\nOutput: {output}"
prefix: "给出反义词:"
suffix: "Input: {word}\nOutput:"
template_format: f-string
```

#### 加载和保存Prompt

```python
from langchain_core.prompts import PromptTemplate, load_prompt
from pathlib import Path

# 创建目录
Path("prompts").mkdir(exist_ok=True)

# 方式1: 直接保存
template = PromptTemplate.from_template(
    "翻译{text}到{language}"
)
template.save("prompts/translate.json")

# 方式2: 加载
loaded = load_prompt("prompts/translate.json")
prompt = loaded.format(text="Hello", language="Chinese")

# 方式3: 使用YAML(推荐)
# 手动创建YAML文件，然后加载
loaded = load_prompt("prompts/translate.yaml")
```

#### 完整的Prompt库管理方案

```python
from pathlib import Path
from langchain_core.prompts import load_prompt
from typing import Dict

class PromptLibrary:
    """Prompt库管理器"""

    def __init__(self, lib_dir: str = "prompts_library"):
        self.lib_dir = Path(lib_dir)
        self.lib_dir.mkdir(exist_ok=True)
        self._cache = {}

    def load_prompt(self, category: str, name: str):
        """加载Prompt"""
        key = f"{category}/{name}"

        if key not in self._cache:
            path = self.lib_dir / category / f"{name}.yaml"
            self._cache[key] = load_prompt(str(path))

        return self._cache[key]

    def list_prompts(self) -> Dict[str, list]:
        """列出所有Prompt"""
        result = {}
        for category_dir in self.lib_dir.iterdir():
            if category_dir.is_dir():
                result[category_dir.name] = [
                    f.stem for f in category_dir.glob("*.yaml")
                ]
        return result

# 使用
library = PromptLibrary()

# 列出所有Prompt
print(library.list_prompts())
# 输出: {'translation': ['en_to_zh', 'zh_to_en'], 'summary': ['brief', 'detailed']}

# 加载使用
template = library.load_prompt("translation", "en_to_zh")
prompt = template.format(text="Hello World")
```

---

## 🎯 完整代码示例

### 示例1：基础翻译Prompt

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 定义模板
template = PromptTemplate.from_template(
    """You are a professional translator.

Translate the following {source_lang} text to {target_lang}.
Keep the original meaning and tone.

Source text:
{text}

Translation:"""
)

# 使用
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
prompt = template.format(
    source_lang="English",
    target_lang="Chinese",
    text="The quick brown fox jumps over the lazy dog."
)

response = llm.invoke(prompt)
print(response.content)
```

### 示例2：Few-Shot情感分析

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

# 示例
examples = [
    {
        "text": "这款产品太棒了！强烈推荐！",
        "sentiment": "positive",
        "confidence": "95"
    },
    {
        "text": "质量不好，售后也差，后悔买了",
        "sentiment": "negative",
        "confidence": "90"
    },
    {
        "text": "产品还可以，没什么特别的",
        "sentiment": "neutral",
        "confidence": "70"
    }
]

# 格式化示例
example_prompt = PromptTemplate(
    input_variables=["text", "sentiment", "confidence"],
    template="""文本: {text}
情感: {sentiment}
置信度: {confidence}%"""
)

# 创建Few-Shot模板
template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="分析文本的情感。\n\n示例：",
    suffix="\n\n现在分析：\n文本: {text}\n情感:",
    input_variables=["text"]
)

# 使用
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = template.format(text="这个产品不错，值得购买")
response = llm.invoke(prompt)
print(response.content)
```

### 示例3：多角色对话Prompt

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 定义对话模板
template = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的代码审查专家。

你的职责：
1. 检查代码质量和最佳实践
2. 指出潜在的bug和性能问题
3. 提供改进建议
4. 使用简洁的语言解释

格式：
[问题] 问题描述
[严重程度] 高/中/低
[建议] 改进方案"""),
    ("human", "请审查这段代码：\n```\n{code}\n```")
])

# 使用
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

messages = template.format_messages(code="""
def calculate(a, b):
    result = a / b
    return result
""")

response = llm.invoke(messages)
print(response.content)
```

---

## 🚀 学习路径与时间管理

### Day 5 (约2小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-09:30 | PromptTemplate基础 | `01_prompt_template_basics.py` |
| 09:30-10:30 | ChatPromptTemplate实践 | `02_chat_prompt_template.py` |
| 10:30-11:00 | 自己实现第一个模板 | 自编写 |

### Day 6 (约2小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-10:00 | Few-Shot学习 | `03_few_shot_prompting.py` |
| 10:00-10:30 | 动态示例选择 | 自编写 |
| 10:30-11:00 | 对比Zero/Few效果 | 自编写 |

### Day 7 (约2小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-10:00 | Prompt序列化 | `04_prompt_serialization.py` |
| 10:00-11:00 | 构建Prompt库 | 自编写 |

---

## 💡 关键知识点总结

### 1. PromptTemplate vs ChatPromptTemplate

| 特性 | PromptTemplate | ChatPromptTemplate |
|------|-----------------|------------------|
| 输入 | 字符串 | 消息列表 |
| 输出 | 字符串 | AIMessage对象 |
| 角色支持 | ❌ | ✅ System/Human/AI |
| 用途 | LLM(文本模型) | ChatModel(对话模型) |
| 推荐度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 2. Few-Shot的三个层次

```python
# 初级：静态示例
examples = [{"input": "...", "output": "..."}]
template = FewShotPromptTemplate(examples=examples, ...)

# 中级：自定义示例选择
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(...)
template = FewShotPromptTemplate(example_selector=example_selector, ...)

# 高级：语义相似度动态选择
example_selector = SemanticSimilarityExampleSelector.from_examples(...)
template = FewShotPromptTemplate(example_selector=example_selector, ...)
```

### 3. Prompt工程的金律

| 原则 | 说明 | 示例 |
|------|------|------|
| 清晰指令 | 具体说明任务要求 | ❌"分析这个"vs ✅"用100字总结主要观点" |
| 上下文 | 给出足够的背景信息 | ✅"你是Python专家"比❌"帮助"更好 |
| 格式说明 | 明确输出格式 | ✅"格式: JSON"vs ❌"随意" |
| 示例 | Few-Shot效果好 | ✅给3-5个例子 > ❌长说明 |
| 简洁 | 降低成本和混淆 | ✅20字指令 > ❌200字说明 |

### 4. 何时使用Few-Shot？

✅ **应该用Few-Shot**:
- 输出格式复杂(如特定JSON结构)
- 需要保持特定风格或语气
- Zero-Shot效果不稳定
- 任务是分类或配对(对立概念)

❌ **不需要Few-Shot**:
- 简单的问答任务
- 知识库查询
- 成本关键的场景(Few-Shot会增加Token)

---

## 🎓 学习成果检查清单

完成Day 5-7学习后，你应该能够：

### 基础认知
- [ ] 理解为什么需要PromptTemplate
- [ ] 解释PromptTemplate vs ChatPromptTemplate的区别
- [ ] 说出Few-Shot的优势场景

### 实践能力
- [ ] 创建基础的PromptTemplate
- [ ] 使用ChatPromptTemplate组合多条消息
- [ ] 实现静态Few-Shot
- [ ] 序列化和加载Prompt

### 进阶能力
- [ ] 使用SemanticSimilarityExampleSelector
- [ ] 构建Prompt库和管理系统
- [ ] 使用Jinja2实现条件逻辑
- [ ] 设计多步骤复杂Prompt

### 成果验证
- [ ] ✅ 运行`01_prompt_template_basics.py`
- [ ] ✅ 运行`02_chat_prompt_template.py`
- [ ] ✅ 运行`03_few_shot_prompting.py`
- [ ] ✅ 运行`04_prompt_serialization.py`
- [ ] ✅ 自己创建3个不同类型的Prompt
- [ ] ✅ 构建一个简单的Prompt库

---

## 📖 深入学习资源

### 官方文档
- [LangChain Prompts文档](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Few-Shot Examples详解](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples/)
- [Prompt模板最佳实践](https://python.langchain.com/docs/guides/debugging)

### 推荐阅读
- OpenAI Prompt Engineering Guide (提升Prompt质量)
- Few-Shot Learning论文(理解背后原理)
- 企业级Prompt管理方案

---

## 🔗 与其他模块的关联

```
Day 1-2: 基础调用
    ↓
Day 3-4: 模型I/O
    ↓
Day 5-7: Prompt模板 (你在这里)
    ↓
Day 8-10: 数据连接 (用Prompt指导检索结果处理)
    ↓
Day 11-13: 内存系统 (Prompt+历史对话)
    ↓
Day 14-16: Chains (组合多个Prompt)
    ↓
Day 17-19: Agents (动态Prompt生成)
```

---

## 💪 老王的学习建议

> **Prompt工程是一门艺术和科学的结合！**

### ✅ 必做的三件事

1. **实验不同的Few-Shot数量** - 试试1个、3个、5个示例，看效果怎么变
2. **建立自己的Prompt库** - 整理常用的Prompt，便于复用和版本控制
3. **对比Zero-Shot vs Few-Shot效果** - 亲自感受Few-Shot的威力

### ❌ 常见的坑

- ❌ 写得太罗嗦 - Prompt应该简洁明确，不是长篇大论
- ❌ 只用Zero-Shot - 复杂任务一定要用Few-Shot
- ❌ 不管理Prompt - 把Prompt当一次性代码，后来维护困难
- ❌ 忽视示例质量 - Few-Shot的示例要代表性强

### 💡 提高效率的技巧

1. 创建一个`prompts/`目录，用YAML管理所有Prompt
2. 编写一个`PromptLibrary`类，方便加载和缓存
3. 记录每个Prompt的效果(成功率、输出质量)
4. 定期审查和优化Prompt

### 🚀 进阶优化

```python
# 高级技巧：Prompt版本管理
class PromptVersion:
    """Prompt版本管理"""
    def __init__(self, name: str):
        self.name = name
        self.versions = []

    def add_version(self, version_num: float, template: str, notes: str):
        """添加新版本"""
        self.versions.append({
            "version": version_num,
            "template": template,
            "notes": notes,
            "date": datetime.now()
        })

    def get_version(self, version_num: float = None):
        """获取特定版本（默认最新）"""
        if version_num is None:
            return self.versions[-1]
        return next(v for v in self.versions if v["version"] == version_num)
```

---

**准备好优化你的Prompt了吗？下一步是Day 8-10，学习如何加载和处理大量数据！** 💪

---

*最后更新: 2025-01-09*
*学习时间: 约6小时（Day 5-7）*
