# Day40: 针对性提示词适配

> **核心内容**: 针对不同模型的特点优化提示词，实现跨模型迁移

---

## 📝 模型特性差异

### GPT-4 特点

**优势**:
- 理解复杂指令能力强
- 多步推理表现好
- 创意能力突出

**提示词策略**:
```
✅ 适合复杂的分步指令
✅ 支持角色扮演和情景设定
✅ 可以使用更自然的语言

示例:
"你是一位资深的Python导师。请用苏格拉底式提问法,
引导学生理解装饰器的概念,而不是直接给出答案。"
```

---

### Claude 3.5 特点

**优势**:
- 遵循指令非常准确
- 代码能力强
- 输出结构化能力好

**提示词策略**:
```
✅ 使用清晰的结构化指令
✅ 明确输出格式要求
✅ 适合复杂的代码任务

示例:
"任务: 实现二叉树遍历

要求:
1. 使用Python实现
2. 包含前序、中序、后序三种遍历
3. 每个函数添加docstring
4. 提供测试用例

输出格式:
- 代码块
- 时间复杂度分析
- 使用示例"
```

**Claude特有技巧**:
- 使用XML标签分隔内容
```xml
<context>
这是背景信息
</context>

<task>
这是具体任务
</task>

<output_format>
期望的输出格式
</output_format>
```

---

### Gemini 特点

**优势**:
- 超长上下文理解
- 多模态能力
- 搜索增强

**提示词策略**:
```
✅ 可以提供大量上下文
✅ 适合需要"记忆"大量信息的任务
✅ 可以引用外部知识

示例:
"以下是一本200页的PDF文档内容:
[粘贴全文]

请基于这本书回答:
1. 核心论点是什么?
2. 作者的方法论有哪些?
3. 与[另一本书]的观点有何异同?"
```

---

## 🎯 跨模型提示词适配

### 场景1: 代码生成

**GPT-4版本**:
```
请帮我写一个Python函数,实现快速排序算法。
要求清晰易读,并解释关键步骤。
```

**Claude版本** (更结构化):
```
任务: 实现快速排序

语言: Python

要求:
1. 函数签名: quick_sort(arr: List[int]) -> List[int]
2. 包含详细的中文注释
3. 处理边界情况(空数组、单元素)
4. 时间复杂度: O(n log n)平均

输出:
- 完整代码
- 复杂度分析
- 测试用例
```

**适配要点**:
- GPT-4: 自然语言描述即可
- Claude: 明确列出所有要求，使用结构化格式

---

### 场景2: 长文档分析

**GPT-4版本** (16K上下文):
```
# 策略: 分段处理
先读取文档摘要:
[前5页内容]

基于摘要,我想深入了解第3章的内容。
请分析第3章: [第3章内容]
```

**Gemini版本** (1M上下文):
```
# 策略: 一次性处理
以下是完整的50页文档:
[粘贴全部内容]

请综合分析:
1. 整体结构
2. 各章节要点
3. 前后逻辑关系
```

**适配要点**:
- 短上下文模型: 分段+聚焦
- 长上下文模型: 一次性+全局

---

### 场景3: 创意写作

**GPT-4版本** (发挥创意优势):
```
场景: 2157年的火星殖民地

人物:
- 李墨: 农业工程师,35岁
- 背景: 地球切断供给,殖民地面临危机

请创作一个3000字的科幻短篇,要求:
1. 展现人物的内心挣扎和成长
2. 融入硬科幻元素(火星农业技术)
3. 结局给人希望但不完美

风格: 类似《火星救援》的真实感
```

**Claude版本** (更侧重结构):
```
创作科幻短篇

第一步: 规划结构
- 开端 (500字): 危机降临
- 发展 (1000字): 尝试与挫折
- 高潮 (1000字): 关键突破
- 结局 (500字): 希望与余味

第二步: 创作各部分
[按步骤生成]

第三步: 整合润色
```

**适配要点**:
- GPT-4: 一次性生成,发挥想象力
- Claude: 分步规划,结构化创作

---

## 💡 模型迁移最佳实践

### 1. 提示词模板化

```python
# 通用模板
class PromptTemplate:
    def __init__(self, task, context, requirements, output_format):
        self.task = task
        self.context = context
        self.requirements = requirements
        self.output_format = output_format

    def for_gpt4(self):
        """GPT-4风格: 自然语言"""
        return f"""
{self.context}

任务: {self.task}

请{self.requirements},输出格式:{self.output_format}
"""

    def for_claude(self):
        """Claude风格: 结构化"""
        return f"""
<context>
{self.context}
</context>

<task>
{self.task}
</task>

<requirements>
{self.requirements}
</requirements>

<output_format>
{self.output_format}
</output_format>
"""

# 使用
template = PromptTemplate(
    task="分析用户反馈情感",
    context="以下是100条用户评论",
    requirements="统计正面/负面/中性数量,提取关键问题",
    output_format="JSON格式,包含统计数据和问题列表"
)

gpt4_prompt = template.for_gpt4()
claude_prompt = template.for_claude()
```

---

### 2. 响应解析适配

```python
def parse_response(response, model_type):
    """根据模型类型解析响应"""

    if model_type == "gpt-4":
        # GPT-4可能返回Markdown格式
        # 提取代码块
        code = extract_code_blocks(response)
        analysis = extract_text_sections(response)
        return {"code": code, "analysis": analysis}

    elif model_type == "claude":
        # Claude倾向返回结构化格式
        # 可能使用XML标签
        code = extract_between_tags(response, "code")
        analysis = extract_between_tags(response, "analysis")
        return {"code": code, "analysis": analysis}

    elif model_type == "gemini":
        # Gemini可能包含搜索引用
        content = extract_main_content(response)
        citations = extract_citations(response)
        return {"content": content, "citations": citations}
```

---

### 3. 错误恢复策略

```python
def robust_query(prompt, preferred_model="gpt-4"):
    """带错误恢复的查询"""
    models = [
        ("gpt-4", adapt_for_gpt4),
        ("claude-3.5", adapt_for_claude),
        ("gemini-1.5-pro", adapt_for_gemini)
    ]

    # 尝试首选模型
    try:
        adapted_prompt = adapt_for_model(prompt, preferred_model)
        return query_model(preferred_model, adapted_prompt)
    except Exception as e:
        print(f"{preferred_model}失败: {e}")

        # 降级到备选模型
        for model, adapter in models:
            if model != preferred_model:
                try:
                    adapted_prompt = adapter(prompt)
                    return query_model(model, adapted_prompt)
                except:
                    continue

    raise Exception("所有模型都失败")
```

---

## 📊 模型适配速查表

| 特性 | GPT-4 | Claude 3.5 | Gemini 1.5 Pro |
|------|-------|-----------|----------------|
| **语言风格** | 自然对话 | 结构化指令 | 自然+搜索 |
| **最佳提示长度** | 中等(500字) | 详细(1000字) | 可很长(10K+) |
| **输出控制** | 温度参数 | 明确格式要求 | 指定输出结构 |
| **代码任务** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **创意任务** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **长文档** | 需分段 | 200K够用 | 1M超强 |
| **结构化输出** | JSON模式 | XML标签 | 格式指定 |

---

## 🎯 实战案例

### 案例: 实现相同任务的跨模型提示词

**任务**: 分析一篇技术博客并生成摘要

**GPT-4版本**:
```
请阅读以下技术博客并生成摘要:

[博客全文]

要求:
- 100字以内的核心摘要
- 3-5个关键要点
- 适合的读者群体
- 阅读时长估计
```

**Claude版本**:
```
<task>分析技术博客并生成结构化摘要</task>

<article>
[博客全文]
</article>

<requirements>
请按以下格式输出:

1. 核心摘要 (100字以内)
2. 关键要点 (3-5条,每条一句话)
3. 目标读者 (明确读者特征)
4. 阅读时长 (估算分钟数)
</requirements>

<output_format>
使用Markdown格式,每个部分用##标题分隔
</output_format>
```

**Gemini版本**:
```
分析技术博客: [URL或全文]

任务:
1. 生成摘要
2. 提取要点
3. 与相关技术文章对比 (利用搜索能力)
4. 推荐延伸阅读

请综合利用文章内容和你的知识库,生成全面的分析。
```

**输出对比**:
- GPT-4: 自然流畅,创意性强
- Claude: 结构清晰,格式规范
- Gemini: 信息丰富,有外部引用

---

## 💡 关键要点

### 通用原则:
1. **了解模型特点**: 发挥优势,规避劣势
2. **清晰具体**: 所有模型都喜欢明确指令
3. **示例引导**: Few-Shot在任何模型都有效
4. **迭代优化**: 测试不同版本,找到最佳适配

### 适配策略:
- GPT-4: 自然语言,发挥创造力
- Claude: 结构化,明确要求
- Gemini: 利用长上下文和多模态
- 开源模型: 更依赖提示词工程,需要更精确的指令

---

**第五阶段完成！**

下一步: 第六阶段 - Risks (风险识别与安全防护)
