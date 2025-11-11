# 模块06: Prompt Engineering

**学习时长**: 7天

**学习目标**: 掌握 Prompt 工程，理解 Kimi CLI 的 Agent 规范设计

---

## 📋 学习内容概览

1. **System Prompt 设计** (Day 29-30)
2. **Few-Shot Learning** (Day 31-32)
3. **Chain of Thought** (Day 33)
4. **ReAct Pattern** (Day 34-35)

---

## 🎯 学习目标

- ✅ 能设计高质量的 System Prompt
- ✅ 掌握 Few-Shot 示例技术
- ✅ 理解思维链（CoT）原理
- ✅ 掌握 ReAct 模式
- ✅ 理解 Kimi CLI 的 Agent 规范

---

## 📚 学习资源

### 官方文档
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)

### 推荐教程
- Prompt Engineering Guide
- LangChain Prompting 最佳实践

---

## 📖 详细学习内容

### 📝 01: System Prompt 设计 (Day 29-30)

#### 核心概念

**System Prompt 作用**:
- 定义 AI 的角色和能力
- 设定行为准则
- 规范输出格式
- 提供上下文信息

**设计原则**:
1. 清晰明确：避免模糊指令
2. 结构化：使用标题、列表组织
3. 具体化：提供具体示例
4. 可测试：定义可验证的标准

#### 实践练习

**练习21**: 参考 `代码实践/21_agent_spec_design.md`

设计一个代码审查 Agent 的完整规范，包括：
- 角色定位
- 审查标准
- 输出格式
- 具体示例

---

### 📝 02: Few-Shot Learning (Day 31-32)

#### 核心概念

**Few-Shot 原理**:
通过提供少量示例，让模型理解任务模式并泛化到新场景。

**示例设计要点**:
1. 多样性：覆盖不同场景
2. 相关性：与任务相关
3. 质量：正确、清晰
4. 数量：通常 3-5 个示例最佳

#### 实践练习

**练习22**: 参考 `代码实践/22_few_shot_examples.py`

设计以下场景的 Few-Shot 示例：
- 代码生成
- 文本分类
- 数据转换
- 工具调用

---

### 📝 03: Chain of Thought (Day 33)

#### 核心概念

**CoT 优势**:
- 提升复杂推理能力
- 使思考过程可追溯
- 减少错误率
- 便于调试

**两种模式**:
1. Zero-Shot CoT: "Let's think step by step"
2. Few-Shot CoT: 示例中包含推理过程

#### 实践练习

**练习23**: 参考 `代码实践/23_chain_of_thought.md`

对比直接回答和 CoT 回答的效果差异。

---

### 📝 04: ReAct Pattern (Day 34-35)

#### 核心概念

**ReAct = Reasoning + Acting**

循环结构：
```
Thought → Action → Observation → Thought → ...
```

**适用场景**:
- 需要工具调用
- 多步骤推理
- 动态决策

#### Kimi CLI 中的应用

```markdown
User: Analyze the error in main.py

Thought: I need to first read the file to see the code
Action: read_file("main.py")
Observation: [File content with error on line 15]

Thought: I see a TypeError. Let me search for similar patterns
Action: grep("TypeError", ".")
Observation: [Found similar errors in utils.py]

Thought: Now I understand the pattern. Let me fix it
Action: write_file("main.py", [corrected content])
Observation: File updated successfully

Final Answer: Fixed the TypeError by adding type checking...
```

#### 实践练习

**练习24**: 参考 `代码实践/24_react_pattern.md`

实现一个 ReAct Agent，能够：
- 分析问题
- 选择工具
- 执行操作
- 综合结果

---

## 📊 模块总结

### 知识点检查
- [ ] System Prompt 设计原则
- [ ] Few-Shot 示例设计
- [ ] Chain of Thought 应用
- [ ] ReAct 模式理解

### 代码练习
- [ ] 练习21: Agent 规范设计
- [ ] 练习22: Few-Shot 示例
- [ ] 练习23: CoT 对比
- [ ] 练习24: ReAct 实现

### 输出成果
- [ ] Agent 规范文档
- [ ] Prompt 模板库
- [ ] Kimi CLI Agent 分析
- [ ] 学习笔记

---

## 🔄 下一步

完成本模块后，进入 **模块07: Function Calling**。

---

*Created by 老王 | Last Updated: 2025-01-10*
