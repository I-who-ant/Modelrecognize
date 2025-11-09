# Agent 学习路线图

> **学习周期**: 20天
> **学习目标**: 掌握AI Agent核心技术,能够设计和实现具备规划、记忆、工具使用能力的智能体系统

---

## 📅 学习计划

### Week 3: Agent基础 (Day 21-27)

#### Day 21-22: Agent核心概念

**学习内容**:
- [ ] Agents介绍
  - 什么是AI Agent
  - Agent与传统程序的区别
  - Agent的应用场景和价值
- [ ] Agent的核心组成
  - **Planning(规划)**: 任务拆解和决策
  - **Memory(记忆)**: 上下文和经验存储
  - **Tools(工具)**: 与外部世界交互
  - **Action(执行)**: 执行决策和观察结果
- [ ] Agents流程与决策图
  - 感知→思考→决策→执行→观察的循环
  - Agent的决策树和状态机

**Agent核心架构**:
```
用户请求(User Request)
    ↓
Agent大脑(LLM) ←→ 记忆系统(Memory)
    ↓
规划模块(Planning)
    ↓
工具选择(Tool Selection)
    ↓
执行动作(Action Execution)
    ↓
观察结果(Observation)
    ↓
反思改进(Reflection) → 循环
```

**Agent与Chat的区别**:
| 对比维度 | 传统Chat | AI Agent |
|---------|---------|----------|
| 交互模式 | 一问一答 | 多步骤推理 |
| 能力范围 | 仅回答问题 | 可执行任务 |
| 工具使用 | 无 | 可调用外部工具 |
| 自主性 | 被动响应 | 主动规划 |
| 记忆能力 | 短期对话 | 长期经验积累 |

**实践任务**:
- [ ] 理解Agent的工作原理
- [ ] 阅读本项目的Agent资源文档
- [ ] 绘制Agent架构图
- [ ] 编写简单的Agent伪代码

**学习笔记**: `01_Agent核心概念.md`

**参考资料**:
- 本项目:`/Prompt-Engineering-Guide-main/pages/research/llm-agents.zh.mdx`
- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

#### Day 23-24: 规划(Planning)

**学习内容**:
- [ ] 子任务拆解(Task Decomposition)
  - Chain of Thought(CoT): 思维链
  - Tree of Thoughts(ToT): 思维树
  - 自动任务分解策略
- [ ] 反思与改进(Reflection)
  - ReAct框架
  - Reflexion机制
  - Self-Critique自我批评
- [ ] 规划算法实现
  - 无反馈规划
  - 有反馈的规划

**任务拆解策略对比**:

| 策略 | 原理 | 优点 | 缺点 | 适用场景 |
|-----|------|------|------|---------|
| CoT | 线性推理链 | 简单直接 | 无法纠错 | 简单任务 |
| ToT | 树形探索 | 可回溯 | 计算成本高 | 复杂推理 |
| ReAct | 思考+行动 | 可观察反馈 | 需要工具支持 | 需要验证的任务 |
| Reflexion | 自我反思 | 持续改进 | 实现复杂 | 长期任务 |

**核心概念**:
1. **Chain of Thought**: 逐步推理,每步基于前一步
2. **Tree of Thoughts**: 生成多个可能路径,选择最优
3. **ReAct**: Reasoning + Acting,思考与行动交替
4. **Reflexion**: 从失败中学习,自我改进

**实践任务**:
- [ ] 实现CoT推理示例
- [ ] 实现简单的任务拆解算法
- [ ] 使用ReAct框架解决问题
- [ ] 实现Reflexion反思机制

**学习笔记**: `02_规划Planning.md`

**代码示例**: `代码实践/day23-24_planning/`

**参考资料**:
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601)
- [ReAct论文](https://arxiv.org/abs/2210.03629)

---

#### Day 25-27: 记忆(Memory)与工具(Tools)

**Day 25: 记忆系统设计**

**学习内容**:
- [ ] Agent记忆系统
  - **短期记忆(Short-term Memory)**: 当前任务上下文
  - **长期记忆(Long-term Memory)**: 历史经验和知识
  - **工作记忆(Working Memory)**: 任务执行过程中的临时信息
- [ ] 记忆的存储和检索
  - 向量数据库存储
  - 记忆的相关性检索
  - 记忆的遗忘机制
- [ ] 记忆格式
  - 自然语言格式
  - 结构化数据格式
  - 嵌入向量格式

**记忆架构**:
```
短期记忆 (上下文窗口)
   ↓
工作记忆 (当前任务状态)
   ↓
长期记忆 (向量数据库)
   ↑
检索机制 (相似度搜索)
```

**Day 26-27: 工具使用(Tools)**

**学习内容**:
- [ ] 预制工具(Tool)
  - 搜索工具(Google, Bing, DuckDuckGo)
  - 计算工具(Calculator, WolframAlpha)
  - 数据库工具(SQL Query)
  - API调用工具
- [ ] 预制工具集(Toolkits)
  - LangChain Toolkits
  - 自定义Toolkit设计
- [ ] 自定义工具开发
  - 工具的定义(名称、描述、参数)
  - 工具的实现
  - 工具的注册和调用
- [ ] 执行(Action)机制
  - 工具选择策略
  - 参数提取
  - 错误处理
  - 结果解析

**工具定义模板**:
```python
{
    "name": "search",
    "description": "搜索互联网获取最新信息。当需要查找实时信息时使用。",
    "parameters": {
        "query": "搜索关键词",
        "num_results": "返回结果数量(默认5)"
    }
}
```

**实践任务**:
- [ ] 设计Agent的记忆系统
- [ ] 实现记忆的存储和检索
- [ ] 使用预制工具构建Agent
- [ ] 开发至少2个自定义工具
- [ ] 实现工具调用和错误处理

**学习笔记**:
- `03_记忆Memory系统.md`
- `04_工具Tools使用.md`

**代码示例**: `代码实践/day25-27_memory_tools/`

---

### Week 4: Function Calling (Day 28-34)

#### Day 28-29: Function Calling基础

**学习内容**:
- [ ] Function Calling诞生背景
  - 传统Prompt方式的局限性
  - 结构化输出的需求
  - Function Calling的优势
- [ ] 如何理解Function Calling
  - 不是真正的"函数调用"
  - 是一种结构化输出协议
  - LLM理解工具并决定调用
- [ ] Function Calling工作流程
  ```
  用户输入 → LLM分析
     ↓
  生成Function Call(函数名+参数)
     ↓
  客户端执行函数 → 获取结果
     ↓
  结果返回LLM → 生成最终回答
  ```

**Function Calling vs Prompt Engineering**:

| 对比维度 | Prompt Engineering | Function Calling |
|---------|-------------------|------------------|
| 输出格式 | 自然语言(需解析) | 结构化JSON |
| 准确性 | 依赖Prompt质量 | 高准确性 |
| 可靠性 | 可能格式错误 | 保证格式正确 |
| 灵活性 | 高度灵活 | 相对固定 |
| 实现难度 | 简单 | 需要设计函数定义 |

**实践任务**:
- [ ] 理解Function Calling的工作原理
- [ ] 定义第一个Function
- [ ] 实现Function Call的解析
- [ ] 处理Function调用结果

**学习笔记**: `05_FunctionCalling基础.md`

**代码示例**: `代码实践/day28-29_function_calling_basics/`

**参考资料**:
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)

---

#### Day 30-31: Function Calling实战

**学习内容**:
- [ ] Function Calling实现过程
  1. 定义Functions(函数签名)
  2. 发送请求给LLM
  3. 解析LLM返回的Function Call
  4. 执行对应函数
  5. 将结果返回LLM
  6. 获取最终答案
- [ ] 远程Function Calling调用
  - API调用封装
  - 异步调用处理
  - 超时和重试机制
  - 错误处理和降级
- [ ] 支持Function Calling的国产模型
  - **文心一言**: 百度
  - **通义千问**: 阿里
  - **智谱GLM**: 智谱AI
  - **Kimi**: 月之暗面
  - **DeepSeek**: DeepSeek

**Function定义示例**:
```python
functions = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称,例如:北京、上海"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }
]
```

**实践任务**:
- [ ] 实现完整的Function Calling流程
- [ ] 开发多Function协同调用
- [ ] 实现远程API调用工具
- [ ] 对比不同模型的Function Calling能力
- [ ] 实现错误处理和重试机制

**学习笔记**: `06_FunctionCalling实战.md`

**代码示例**: `代码实践/day30-31_function_calling_practice/`

---

#### Day 32-34: Agent认知框架

**学习内容**:
- [ ] **ReAct(Reasoning and Acting)**
  - 思考(Thought): LLM推理
  - 行动(Action): 执行工具
  - 观察(Observation): 获取反馈
  - 循环迭代直到完成任务

**ReAct执行流程**:
```
Thought 1: 我需要搜索关于XX的信息
Action 1: search("XX相关信息")
Observation 1: [搜索结果]

Thought 2: 基于搜索结果,我需要进一步了解YY
Action 2: search("YY详细信息")
Observation 2: [搜索结果]

Thought 3: 现在我有足够信息回答用户问题了
Answer: [最终答案]
```

- [ ] **Plan-and-Execute**
  - Plan: 制定完整计划
  - Execute: 逐步执行
  - Re-plan: 根据执行结果调整计划

**Plan-and-Execute流程**:
```
1. Planning Phase
   - 分析任务
   - 拆解子任务
   - 制定执行计划

2. Execution Phase
   - 按计划执行每个步骤
   - 收集执行结果

3. Re-planning Phase (可选)
   - 检查执行结果
   - 调整后续计划
```

- [ ] **Self-Ask**
  - 自我提问驱动推理
  - 分解复杂问题为子问题
  - 逐个回答子问题

- [ ] **Thinking and Self-Reflection**
  - 思考过程的显式化
  - 自我评估和纠错
  - 持续改进策略

**认知框架对比**:

| 框架 | 核心思想 | 优点 | 缺点 | 适用场景 |
|-----|---------|------|------|---------|
| ReAct | 思考+行动交替 | 可观察,可调试 | 可能循环次数多 | 需要工具的任务 |
| Plan-and-Execute | 先规划后执行 | 结构清晰 | 计划可能不准确 | 复杂多步骤任务 |
| Self-Ask | 自我提问 | 分解清晰 | 依赖问题质量 | 推理密集型任务 |
| Self-Reflection | 自我反思 | 持续改进 | 成本较高 | 需要优化的场景 |

**实践任务**:
- [ ] 实现ReAct Agent
- [ ] 实现Plan-and-Execute Agent
- [ ] 实现Self-Ask Agent
- [ ] 对比不同框架的效果
- [ ] 选择合适框架解决实际问题

**学习笔记**: `07_Agent认知框架.md`

**代码示例**: `代码实践/day32-34_cognitive_frameworks/`

**参考资料**:
- [ReAct论文](https://arxiv.org/abs/2210.03629)
- [Plan-and-Solve论文](https://arxiv.org/abs/2305.04091)

---

### Week 5: 多Agent系统 (Day 35-40)

#### Day 35-36: AutoGPT与CAMEL

**Day 35: AutoGPT**

**学习内容**:
- [ ] AutoGPT核心概念
  - 自主任务执行
  - 长期记忆管理
  - 自我驱动的目标设定
- [ ] AutoGPT快速打造智能体
  - 安装和配置
  - 定义任务目标
  - 执行和监控
- [ ] AutoGPT的局限性
  - 成本问题(大量API调用)
  - 可能陷入循环
  - 需要人工监督

**AutoGPT工作流程**:
```
设定目标 → 任务拆解
   ↓
自主执行任务 ← 调用工具
   ↓
评估进度 → 调整计划
   ↓
持续迭代直到目标完成
```

**Day 36: CAMEL策略**

**学习内容**:
- [ ] CAMEL(Communicative Agents for Mind Exploration of Large Scale Language Model Society)
  - 角色扮演式多Agent协作
  - Agent间的沟通机制
  - 任务分配和协调
- [ ] CAMEL实现
  - 定义不同角色的Agent
  - 设计通信协议
  - 实现协作机制

**CAMEL角色示例**:
```
AI用户: 提出需求和问题
   ↕️
AI助手: 提供解决方案
   ↕️
AI评审: 评估方案质量
```

**实践任务**:
- [ ] 部署AutoGPT并执行任务
- [ ] 分析AutoGPT的执行日志
- [ ] 实现简单的CAMEL系统
- [ ] 设计多角色协作场景

**学习笔记**:
- `08_AutoGPT智能体.md`
- `09_CAMEL策略.md`

**代码示例**: `代码实践/day35-36_autogpt_camel/`

**参考资料**:
- [AutoGPT GitHub](https://github.com/Significant-Gravitas/AutoGPT)
- [CAMEL论文](https://arxiv.org/abs/2303.17760)

---

#### Day 37-38: AutoGen框架

**学习内容**:
- [ ] AutoGen架构设计
  - ConversableAgent: 可对话的Agent
  - AssistantAgent: 助手Agent
  - UserProxyAgent: 用户代理Agent
  - GroupChat: 群聊模式
- [ ] 多Agent协作机制
  - 一对一对话
  - 群聊协作
  - 嵌套聊天(Nested Chat)
  - 顺序聊天
- [ ] AutoGen核心特性
  - 代码执行能力
  - 人类参与(Human-in-the-loop)
  - 工具使用
  - 可定制的对话模式

**AutoGen对话模式**:

| 模式 | 描述 | 适用场景 |
|-----|------|---------|
| Two-Agent Chat | 两个Agent对话 | 简单任务 |
| Group Chat | 多个Agent群聊 | 复杂协作 |
| Nested Chat | 嵌套对话 | 分层任务 |
| Sequential Chat | 顺序对话 | 流水线任务 |

**AutoGen协作示例**:
```python
# 创建Agent
assistant = AssistantAgent("assistant")
user_proxy = UserProxyAgent("user_proxy")

# 启动对话
user_proxy.initiate_chat(
    assistant,
    message="帮我写一个排序算法"
)
```

**实践任务**:
- [ ] 安装和配置AutoGen
- [ ] 创建基本的Agent对话
- [ ] 实现GroupChat多Agent协作
- [ ] 开发代码生成和执行Agent
- [ ] 实现人类参与的工作流

**学习笔记**: `10_AutoGen框架.md`

**代码示例**: `代码实践/day37-38_autogen/`

**参考资料**:
- [AutoGen官方文档](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)

---

#### Day 39-40: MetaGPT

**学习内容**:
- [ ] MetaGPT核心概念
  - 软件开发的Agent化
  - 角色专业化(产品经理、架构师、工程师、QA)
  - 标准化工作流(SOP)
- [ ] MetaGPT架构
  - 角色定义
  - 工作流设计
  - 文档驱动开发
  - 代码生成和测试
- [ ] 软件开发Agent实战
  - 需求分析Agent
  - 架构设计Agent
  - 代码实现Agent
  - 测试Agent

**MetaGPT工作流**:
```
需求输入
   ↓
产品经理Agent → PRD文档
   ↓
架构师Agent → 设计文档
   ↓
工程师Agent → 代码实现
   ↓
QA Agent → 测试报告
   ↓
最终交付
```

**MetaGPT vs 其他框架**:

| 框架 | 定位 | 特点 | 适用场景 |
|-----|------|------|---------|
| MetaGPT | 软件开发 | 角色专业化、SOP | 软件项目 |
| AutoGen | 通用协作 | 灵活对话模式 | 各类协作任务 |
| AutoGPT | 自主执行 | 自驱动 | 开放式任务 |
| CAMEL | 角色扮演 | 沟通协调 | 创意探索 |

**实践任务**:
- [ ] 安装和配置MetaGPT
- [ ] 使用MetaGPT生成软件项目
- [ ] 分析生成的PRD和设计文档
- [ ] 评估生成代码的质量
- [ ] 自定义MetaGPT角色和工作流

**综合项目**:
- [ ] 选择一个实际项目需求
- [ ] 对比AutoGen和MetaGPT的实现
- [ ] 总结多Agent系统的设计经验

**学习笔记**: `11_MetaGPT框架.md`

**代码示例**: `代码实践/day39-40_metagpt/`

**参考资料**:
- [MetaGPT论文](https://arxiv.org/abs/2308.00352)
- [MetaGPT GitHub](https://github.com/geekan/MetaGPT)

---

## 🎯 实战项目

### 项目1: 智能客服Agent系统

**项目目标**: 构建一个能够自主处理客户咨询的Agent系统

**技术栈**:
- LangChain Agent框架
- ReAct认知框架
- Function Calling
- 知识库检索(LlamaIndex)

**功能要求**:
1. 理解客户问题并分类
2. 从知识库检索相关信息
3. 调用订单查询工具
4. 调用售后服务API
5. 生成专业的回复
6. 记录对话历史

**技术亮点**:
- 多工具协同使用
- 基于ReAct的推理
- 长期记忆管理
- 人类接管机制

**代码目录**: `代码实践/projects/01_customer_service_agent/`

---

### 项目2: 数据分析助手Agent

**项目目标**: 构建一个能够自主进行数据分析的Agent

**技术栈**:
- LangChain Agent
- Python Code Interpreter
- Pandas工具
- 数据可视化工具

**功能要求**:
1. 理解数据分析需求
2. 自动生成数据处理代码
3. 执行代码并获取结果
4. 生成数据可视化图表
5. 撰写分析报告

**技术亮点**:
- 代码生成和执行
- 错误处理和修复
- 迭代优化分析
- 结果可视化

**代码目录**: `代码实践/projects/02_data_analysis_agent/`

---

### 项目3: 多Agent协作开发系统

**项目目标**: 使用MetaGPT或AutoGen构建多Agent协作系统

**技术栈**:
- MetaGPT或AutoGen
- 多Agent协作框架
- 代码生成和测试工具

**功能要求**:
1. 输入项目需求
2. 自动生成PRD文档
3. 生成系统架构设计
4. 生成核心代码
5. 生成测试用例
6. 输出完整项目

**技术亮点**:
- 角色专业化设计
- SOP工作流
- 文档驱动开发
- 质量保证机制

**代码目录**: `代码实践/projects/03_multi_agent_dev/`

---

## 📝 面试题准备

### 基础概念
1. **什么是AI Agent?在AI应用中,Agent的核心作用是什么?**
2. **Agent与传统的Chat应用有什么本质区别?**
3. **Agent的核心组成部分有哪些?各自的作用是什么?**

### Planning & Memory
4. **Agent系统中,如何进行子任务拆解和反思?**
5. **Chain of Thought和Tree of Thoughts有什么区别?**
6. **Agent中的记忆(Memory)如何作用于系统的学习和决策?**
7. **短期记忆和长期记忆如何设计和管理?**

### Tools & Function Calling
8. **什么是Function Calling?它解决了什么问题?**
9. **在Agent系统中,如何实现远程Function Calling?**
10. **如何设计一个好的工具(Tool)定义?**
11. **工具调用失败时如何处理?**

### 认知框架
12. **解释ReAct框架的工作原理**
13. **Plan-and-Execute与ReAct的区别和适用场景**
14. **如何选择合适的Agent认知框架?**

### 多Agent系统
15. **AutoGPT、AutoGen、MetaGPT有什么区别?**
16. **多Agent系统中如何进行协作和通信?**
17. **如何设计多Agent系统的角色分工?**
18. **多Agent系统的挑战和解决方案?**

### 系统设计
19. **如何设计一个生产级的Agent系统?**
20. **Agent系统的性能优化有哪些关键点?**
21. **如何评估Agent系统的表现?**
22. **Agent系统的安全性和可控性如何保证?**

**面试题详解**: `面试题/Agent经典面试题.md`

---

## 📚 参考资料

### 官方文档
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoGen文档](https://microsoft.github.io/autogen/)
- [MetaGPT文档](https://docs.deepwisdom.ai/)

### 教程资源
- [Agent教程](https://github.com/datawhalechina/agent-tutorial)
- [AI Agent视频讲解](https://www.bilibili.com/video/BV1dxm6YPEDB)
- [AI Agent入门到精通](https://www.bilibili.com/video/BV1SqKHeUEm5/)

### 论文阅读
- [ReAct论文](https://arxiv.org/abs/2210.03629)
- [AutoGPT论文](https://arxiv.org/abs/2306.02224)
- [MetaGPT论文](https://arxiv.org/abs/2308.00352)
- [CAMEL论文](https://arxiv.org/abs/2303.17760)

### 开源项目
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- [AutoGen](https://github.com/microsoft/autogen)
- [MetaGPT](https://github.com/geekan/MetaGPT)
- [LangChain Agent Examples](https://github.com/langchain-ai/langchain/tree/master/docs/docs/modules/agents)

---

## ✅ 学习检查清单

### Week 3检查 (基础)
- [ ] 理解Agent的核心概念和架构
- [ ] 掌握任务拆解和规划方法
- [ ] 理解ReAct框架原理
- [ ] 能够设计Agent的记忆系统
- [ ] 能够开发自定义工具
- [ ] 实现基本的Agent应用

### Week 4检查 (Function Calling)
- [ ] 理解Function Calling原理
- [ ] 能够定义Function定义
- [ ] 实现完整的Function Calling流程
- [ ] 掌握多种Agent认知框架
- [ ] 能够根据场景选择合适框架
- [ ] 实现复杂的Agent推理

### Week 5检查 (多Agent)
- [ ] 理解多Agent协作机制
- [ ] 能够使用AutoGen构建多Agent系统
- [ ] 能够使用MetaGPT生成软件项目
- [ ] 理解不同多Agent框架的区别
- [ ] 能够设计多Agent协作流程
- [ ] 完成至少1个综合项目

### 整体检查
- [ ] 能够独立设计和实现Agent系统
- [ ] 掌握至少2种Agent认知框架
- [ ] 能够开发多种类型的Agent工具
- [ ] 理解多Agent协作的原理和实现
- [ ] 能够评估和优化Agent性能
- [ ] 能够回答Agent相关面试题
- [ ] 代码实践不少于15个Demo
- [ ] 完成至少2个实战项目

---

## 🚀 下一步学习

完成Agent学习后,进入:
- **第四阶段**: 可视化开发框架学习 (10天)
- **重点**: 快速搭建Agent应用的能力

---

**老王提示**: 艹,Agent这部分是整个学习路线中最tm重要也最复杂的!但是老王我保证,只要你踏踏实实把这20天学下来,你绝对能成为Agent开发的高手!

**关键点**:
1. **先理解后实践**: Agent的概念比较抽象,先理解原理再动手
2. **多跑Demo**: 每个框架都要亲自跑一遍,看看效果
3. **对比分析**: 不同框架、不同认知模式要对比着学
4. **实战为王**: 最后一定要做实战项目,把知识串起来

记住老王的话:Agent不是简单的工具调用,是具备"智能"的系统!理解这一点,你就入门了!

**学习开始日期**: _____年___月___日
**预计完成日期**: _____年___月___日
**实际完成日期**: _____年___月___日