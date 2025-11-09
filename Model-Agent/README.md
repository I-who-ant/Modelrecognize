# 阶段3:大模型Agent应用架构 - 学习路线规划

> **创建时间**: 2025-11-09
> **学习周期**: 50天
> **学习目标**: 掌握LangChain、LlamaIndex、Agent开发及可视化框架,能够独立构建AI Agent应用

---

## 📋 总体规划

### 学习周期分配
- **LangChain**: 15天 (第1-15天)
- **LlamaIndex**: 5天 (第16-20天)
- **Agent**: 20天 (第21-40天)
- **可视化开发框架**: 10天 (第41-50天)

### 学习方法论
1. **理论先行**: 先看官方文档和教程,理解核心概念
2. **动手实践**: 每个知识点都要跑通Demo,写代码验证
3. **笔记总结**: 用Markdown记录学习笔记,整理知识体系
4. **面试准备**: 整理常见面试题,加深理解
5. **项目实战**: 每个阶段结束后做一个综合项目

---

## 📚 学习路径

### 第一部分: LangChain (15天)

**学习重点**:
- LangChain框架核心概念和架构设计
- 提示词工程、模型I/O封装、数据连接
- Memory记忆管理、链(Chain)设计
- LCEL表达式和Runnable协议

**学习路线**:

#### Week 1 (Day 1-7): 基础入门
- **Day 1-2**: LangChain概述与环境搭建
  - 什么是LangChain
  - 安装配置LangChain开发环境
  - 跑通第一个Hello World示例
  - 理解LangChain的架构设计

- **Day 3-4**: 模型I/O封装
  - Chat Models vs LLMs的区别
  - 流式输出实现
  - Token追踪和成本管理
  - 结构化输出处理

- **Day 5-7**: Prompts模板
  - Prompts模板基础
  - 自定义Prompts模板
  - 序列化模板
  - 提示词工程最佳实践

#### Week 2 (Day 8-15): 高级特性
- **Day 8-10**: 数据连接与向量化
  - 文本向量化实现方式
  - 向量数据库对比(Chroma/ES/FAISS/Milvus)
  - 文档转换与切割策略
  - 检索增强生成(RAG)基础

- **Day 11-13**: Memory记忆系统
  - Memory封装原理
  - 内置链的使用
  - 为链添加Memory
  - 多轮对话历史记录管理

- **Day 14-15**: LCEL与链(Chain)
  - LCEL表达式语法
  - LCEL Runnable协议设计
  - 复杂逻辑的多链整合
  - LCEL添加记忆和提示词

**实践项目**:
- 本地知识库问答系统
- 多轮对话机器人
- 文档智能检索助手

**参考资料**:
- [LangChain官方文档(Python)](https://python.langchain.com/docs/introduction/)
- [LangChain中文文档](https://www.langchain.com.cn/)
- [LangChain大模型全套教程](https://www.bilibili.com/video/BV1BgfBYoEpQ)
- [LangChain教程](https://www.langchain.asia/)

---

### 第二部分: LlamaIndex (5天)

**学习重点**:
- LlamaIndex核心概念和数据索引
- RAG检索增强应用
- LlamaIndex与LangChain对比

**学习路线**:

#### Day 16-20: LlamaIndex深度学习
- **Day 16**: LlamaIndex基础
  - 什么是LlamaIndex
  - LlamaIndex的优势和劣势
  - 环境搭建和快速开始

- **Day 17-18**: 索引与检索
  - 文档索引构建
  - 索引结构分析
  - 查询和检索优化

- **Day 19**: RAG应用实践
  - LlamaIndex与RAG检索增强联合应用
  - 文档问答系统实战
  - 性能优化技巧

- **Day 20**: 框架对比与选型
  - LlamaIndex与LangChain对比分析
  - 不同场景下的框架选择
  - 综合项目实战

**实践项目**:
- 企业文档智能问答系统
- 知识库检索增强应用

**参考资料**:
- [LlamaIndex官方文档](https://docs.llamaindex.ai/en/stable/)
- [LlamaIndex使用指南](https://llama-index.readthedocs.io/zh/latest/guides/primer.html)
- [LlamaIndex零基础全套课程](https://www.bilibili.com/video/BV1JDpFeEEay/)

---

### 第三部分: Agent (20天)

**学习重点**:
- Agent核心技术和认知框架
- ReAct、Plan-and-Execute等思维模式
- Function Calling实现
- 多Agent协作系统

**学习路线**:

#### Week 3 (Day 21-27): Agent基础
- **Day 21-22**: Agent核心概念
  - Agents介绍和应用场景
  - Agents流程与决策图
  - Agent的关键组成部分

- **Day 23-24**: 规划(Planning)
  - 子任务拆解策略
  - 反思与改进机制
  - 规划算法实现

- **Day 25-27**: 记忆(Memory)与工具(Tools)
  - Agent记忆系统设计
  - 预制工具(Tool)使用
  - 预制工具集(Toolkits)
  - 自定义工具开发
  - 执行(Action)机制

#### Week 4 (Day 28-34): Function Calling
- **Day 28-29**: Function Calling基础
  - Function Calling诞生背景
  - 如何理解Function Calling
  - Function Calling实现过程

- **Day 30-31**: Function Calling实战
  - 远程Function Calling调用
  - 支持Function Calling的国产模型
  - 错误处理与调试

- **Day 32-34**: Agent认知框架
  - ReAct(思考-行动-观察)
  - Plan-and-Execute
  - Self-Ask
  - Thinking and Self-Reflection

#### Week 5 (Day 35-40): 多Agent系统
- **Day 35-36**: AutoGPT与CAMEL
  - AutoGPT快速打造智能体
  - CAMEL策略详解
  - 实战应用

- **Day 37-38**: AutoGen框架
  - AutoGen架构设计
  - 多Agent协作机制
  - 实践案例

- **Day 39-40**: MetaGPT
  - MetaGPT核心概念
  - 软件开发Agent实战
  - 综合项目总结

**实践项目**:
- 智能客服Agent系统
- 数据分析助手Agent
- 多Agent协作开发系统

**参考资料**:
- [Agent教程](https://github.com/datawhalechina/agent-tutorial)
- [AI Agent视频讲解](https://www.bilibili.com/video/BV1dxm6YPEDB)
- [AI Agent入门到精通实战教程](https://www.bilibili.com/video/BV1SqKHeUEm5/)

---

### 第四部分: 可视化开发框架/Agent IDE (10天)

**学习重点**:
- GPTs与Assistants API
- Coze扣子平台使用
- Dify开源应用编排

**学习路线**:

#### Week 6 (Day 41-50): 可视化开发实战
- **Day 41-43**: GPTs与Assistants API
  - GPTs基础使用
  - Assistants API开发
  - Assistants thread和messages
  - 原生API与开源大模型集成

- **Day 44-46**: Coze扣子平台
  - Coze基础概念
  - AI Agent人设设计
  - AI Agent插件系统
  - AI Agent工作流
  - 知识库、数据库和变量管理
  - AI Agent发布与部署
  - 构建知识库实操

- **Day 47-50**: Dify开源平台
  - Dify基础架构
  - 应用编排工具使用
  - 工作流设计
  - 知识库问答系统搭建
  - 综合项目实战

**实践项目**:
- 基于GPTs的专属助手
- Coze平台知识库问答应用
- Dify工作流自动化系统

**参考资料**:
- [快速上手OpenAI GPTs](https://www.bilibili.com/video/BV1gG411X7q7/)
- [Coze零基础视频教程](https://www.bilibili.com/video/BV1AWQzYHEaU/)
- [Dify搭建简单的知识库问答工作流](https://www.bilibili.com/video/BV1M29PYiEHx/)
- [Dify官方文档](https://docs.dify.ai/zh-hans)

---

## 🎯 学习建议

### 学习策略
1. **不要死磕底层**: 先跑通几个Demo,理解框架的使用方式,再慢慢深入原理
2. **动手为主**: 每个知识点都要亲自写代码验证,不要只看教程
3. **做笔记**: 用Markdown记录学习过程,整理知识体系
4. **解决实际问题**: 学到能独立用框架接API、处理数据、搭出可用的AI工具就够用了
5. **边做边补**: 细节可以边做项目边补充,不要追求完美

### 重点关注
- **LangChain**: 核心组件(Models、Prompts、Memory、Chains)的使用
- **LlamaIndex**: 文档索引和RAG应用
- **Agent**: ReAct框架、Function Calling、多Agent协作
- **可视化框架**: 快速搭建应用的能力

### 学习成果检验
- 能够独立搭建本地知识库问答系统
- 能够设计并实现一个具备规划、记忆、工具使用的Agent
- 能够使用可视化平台快速搭建AI应用
- 能够回答面试中的常见问题

---

## 📝 面试题准备

每个部分都整理了经典面试题,详见各子目录下的`面试题`文件夹:

### LangChain面试题
1. LangChain是什么?核心功能和特点?
2. Chain和Agent概念及应用场景
3. 多路召回结果的动态权重分配
4. 文档问答系统的关键技术组件
5. Memory组件的工作原理

### LlamaIndex面试题
1. LlamaIndex是什么及主要功能
2. 文档索引的构建和索引结构
3. 非结构化数据的处理和管理
4. 文档预处理确保检索质量
5. 复杂查询和多步骤推理任务

### Agent面试题
1. Agent的定义和核心作用
2. 子任务拆解和反思机制
3. Memory在Agent系统中的作用
4. 远程Function Calling实现
5. Plan-and-Execute优化任务执行

### 可视化框架面试题
1. Dify应用编排实操步骤
2. Assistants API构建AI助手
3. AI Agent人设设计
4. Coze知识库构建和管理

---

## 🚀 开始学习

### 环境准备
```bash
# 创建Python虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装基础依赖
pip install langchain langchain-community langchain-openai
pip install llama-index
pip install openai anthropic
pip install chromadb faiss-cpu
pip install streamlit gradio  # 可视化工具
```

### 学习顺序
1. 按照 `01_LangChain` → `02_LlamaIndex` → `03_Agent` → `04_可视化开发框架` 的顺序学习
2. 每个阶段学完后,在`代码实践`目录下完成项目
3. 在`学习笔记`目录下记录学习心得
4. 在`面试题`目录下整理常见问题

### 目录说明
```
Model-Agent/
├── 01_LangChain/           # LangChain学习(15天)
│   ├── 学习笔记/           # 学习笔记Markdown文件
│   ├── 代码实践/           # 实践代码和Demo
│   ├── 面试题/             # 面试题整理
│   └── 参考资料/           # 参考文档和资源链接
├── 02_LlamaIndex/          # LlamaIndex学习(5天)
│   ├── 学习笔记/
│   ├── 代码实践/
│   ├── 面试题/
│   └── 参考资料/
├── 03_Agent/               # Agent学习(20天)
│   ├── 学习笔记/
│   ├── 代码实践/
│   ├── 面试题/
│   └── 参考资料/
└── 04_可视化开发框架/     # 可视化框架学习(10天)
    ├── 学习笔记/
    ├── 代码实践/
    ├── 面试题/
    └── 参考资料/
```

---

## 📖 补充资源

### 推荐阅读
- 本项目中的 `Prompt-Engineering-Guide-main/pages/research/llm-agents.zh.mdx` - LLM Agent综述
- 本项目中的 `DeepSearchAgent-Demo-main` - Agent实战案例

### 社区资源
- [Datawhale Agent教程](https://github.com/datawhalechina/agent-tutorial)
- [LangChain中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)

### 实战项目参考
- 智能客服系统
- 文档问答助手
- 数据分析Agent
- 自动化工作流
- 多Agent协作系统

---

## ✅ 学习检查清单

- [ ] LangChain基础概念掌握
- [ ] 完成LangChain实战项目
- [ ] LlamaIndex索引系统理解
- [ ] 完成RAG应用实践
- [ ] Agent核心技术掌握
- [ ] 完成Function Calling实战
- [ ] 多Agent系统设计能力
- [ ] GPTs/Coze/Dify平台使用
- [ ] 能够独立搭建AI应用
- [ ] 面试题准备充分

---

**老王提示**: 艹,这个学习计划可够你喝一壶的!但是老王我保证,只要你按照这个路线踏实学下来,50天后你绝对能独立搞定Agent应用开发!记住:别tm想太多,先动手跑起来再说,遇到问题再深究原理!

**开始时间**: 2025-11-09
**预计完成**: 2025-12-29

加油,崽芽子们!💪