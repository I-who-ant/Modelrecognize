# Day 5-7 Prompts模板示例

本目录包含LangChain Prompts模板的完整示例代码。

## 📁 文件说明

| 文件 | 说明 | 核心知识点 |
|-----|------|-----------|
| `01_prompt_template_basics.py` | PromptTemplate基础 | 创建、变量、partial |
| `02_chat_prompt_template.py` | ChatPromptTemplate | 消息类型、对话模板 |
| `03_few_shot_prompting.py` | Few-Shot学习 | 示例选择、动态Few-Shot |
| `04_prompt_serialization.py` | 序列化和管理 | 保存/加载、版本控制 |

## 🚀 快速开始

### 安装依赖

```bash
pip install langchain langchain-openai langchain-community python-dotenv pyyaml chromadb
```

### 运行示例

```bash
# PromptTemplate基础
python 01_prompt_template_basics.py

# ChatPromptTemplate
python 02_chat_prompt_template.py

# Few-Shot Prompting
python 03_few_shot_prompting.py

# 序列化
python 04_prompt_serialization.py
```

## 📚 学习顺序

1. **基础模板** (`01`) - 理解PromptTemplate的核心用法
2. **Chat模板** (`02`) - 掌握ChatPromptTemplate和消息组合
3. **Few-Shot** (`03`) - 学习示例驱动的Prompting
4. **序列化** (`04`) - 学会管理和版本控制Prompt

## 💡 核心知识点

### 1. PromptTemplate vs ChatPromptTemplate

```python
# PromptTemplate - 用于LLMs
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Translate {text} to {language}"
)
prompt = template.format(text="Hello", language="Chinese")

# ChatPromptTemplate - 用于Chat Models(推荐)
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("human", "{question}")
])
messages = template.format_messages(
    role="翻译专家",
    question="如何翻译这段话?"
)
```

**关键区别**:
- PromptTemplate: 输出字符串
- ChatPromptTemplate: 输出消息列表

### 2. Few-Shot Learning

```python
from langchain_core.prompts import FewShotPromptTemplate

# 定义示例
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
]

# 创建Few-Shot模板
template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    ),
    prefix="Give me the opposite:\n",
    suffix="\nInput: {word}\nOutput:",
    input_variables=["word"]
)
```

**作用**: 通过示例引导模型输出格式和风格

### 3. 序列化

```python
# 保存
template.save("prompts/translate.yaml")

# 加载
from langchain_core.prompts import load_prompt
template = load_prompt("prompts/translate.yaml")
```

**好处**: 版本控制、团队协作、非技术人员可编辑

## 🎯 使用场景

### 场景1: 多语言翻译

```python
template = PromptTemplate.from_template(
    """Translate the following text to {target_lang}:

{text}

Translation:"""
)
```

### 场景2: 角色扮演对话

```python
template = ChatPromptTemplate.from_messages([
    ("system", """你是{character}，性格特点：
- {trait_1}
- {trait_2}
请保持角色一致性。"""),
    ("human", "{user_input}")
])
```

### 场景3: 结构化输出

```python
template = PromptTemplate.from_template(
    """Analyze the sentiment of: {text}

Output format:
- Sentiment: [positive/negative/neutral]
- Confidence: [0-100]
- Keywords: [list 3-5 keywords]"""
)
```

## ⚠️ 常见问题

### Q1: 何时使用Few-Shot?

**使用Few-Shot**:
- 输出格式复杂，需要示例说明
- 需要保持特定风格
- Zero-Shot效果不佳

**使用Zero-Shot**:
- 任务简单明确
- 希望节省Token
- 模型已经理解任务类型

### Q2: 如何选择模板格式?

- **f-string** (默认): 简单变量替换，99%场景够用
- **jinja2**: 需要条件、循环等复杂逻辑

```python
# f-string
template = "Hello {name}!"

# jinja2
template = """
{% if name %}
Hello {{name}}!
{% else %}
Hello stranger!
{% endif %}
"""
```

### Q3: 序列化用JSON还是YAML?

**推荐YAML**:
- ✅ 更易读
- ✅ 支持多行字符串
- ✅ 可以添加注释

**JSON的优势**:
- 机器处理更方便
- 严格的语法检查

## 📊 Prompt工程最佳实践

### 1. 清晰的指令

```python
# ❌ 不好
template = "关于{topic}"

# ✅ 好
template = """请用100字以内解释{topic}

要求:
1. 通俗易懂
2. 举例说明
3. 突出要点"""
```

### 2. 控制输出长度

```python
template = PromptTemplate.from_template(
    "用{length}字回答: {question}"
)
```

### 3. 结构化输出

```python
template = PromptTemplate.from_template(
    """分析: {text}

输出格式:
- 摘要: [一句话]
- 要点: [3-5个]
- 建议: [具体建议]"""
)
```

## 🔧 调试技巧

### 1. 查看生成的Prompt

```python
template = PromptTemplate.from_template(...)
prompt = template.format(...)
print("=== Generated Prompt ===")
print(prompt)
```

### 2. 测试不同变量

```python
test_cases = [
    {"text": "short", "lang": "Chinese"},
    {"text": "a very long sentence...", "lang": "Japanese"}
]

for case in test_cases:
    print(template.format(**case))
```

### 3. 验证变量

```python
# 检查模板需要哪些变量
print(template.input_variables)
# 输出: ['text', 'language']
```

## ✅ 学习检查清单

完成Day 5-7学习后，确保你能够:

- [ ] 创建基础的PromptTemplate
- [ ] 使用ChatPromptTemplate组合消息
- [ ] 实现Few-Shot提示词
- [ ] 使用示例选择器(静态/动态)
- [ ] 序列化和加载模板
- [ ] 组织Prompt库
- [ ] 理解Prompt工程最佳实践
- [ ] 使用jinja2实现条件逻辑
- [ ] 创建可复用的模板

## 📖 扩展阅读

- [LangChain Prompt Templates文档](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Few-Shot Examples文档](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples/)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

## 💾 生成的文件

运行示例后会生成:

```
代码实践/day5-7_prompts/
├── prompts_library/          # Prompt库
│   ├── translation/          # 翻译类
│   │   ├── simple.yaml
│   │   ├── formal.yaml
│   │   └── with_context.yaml
│   ├── summary/              # 总结类
│   │   ├── brief.yaml
│   │   └── detailed.yaml
│   └── education/            # 教育类
│       └── explain.yaml
└── ...
```

---

**老王提示**: Prompt模板是LLM应用开发的基础！把Prompt当代码一样管理，你的项目会更专业、更易维护。记住：**好的Prompt设计是成功的一半**！💪

**重点**:
1. 模板化思维 - 复用和管理Prompt
2. Few-Shot是杀手锏 - 复杂任务必用
3. 序列化很重要 - 便于版本控制
4. Prompt工程是艺术 - 需要不断优化