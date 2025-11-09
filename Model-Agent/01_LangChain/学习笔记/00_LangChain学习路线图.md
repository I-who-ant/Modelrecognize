# LangChain 学习路线图

> **学习周期**: 15天
> **学习目标**: 掌握LangChain框架核心概念,能够独立构建基于LLM的应用

---

## 📅 学习计划

### Week 1: 基础入门 (Day 1-7)

#### Day 1-2: LangChain概述与环境搭建

**学习内容**:
- [ ] 什么是LangChain - 框架定位和核心价值
- [ ] LangChain的应用场景和典型案例
- [ ] LangChain架构设计和核心组件
- [ ] 环境搭建和依赖安装

**实践任务**:
```bash
# 安装LangChain
pip install langchain langchain-community langchain-openai
pip install python-dotenv

# 第一个Hello World示例
```

**学习笔记**: `01_LangChain概述与环境搭建.md`

**参考资料**:
- [LangChain官方文档 - Introduction](https://python.langchain.com/docs/introduction/)
- [LangChain中文文档 - 快速开始](https://www.langchain.com.cn/)

---

#### Day 3-4: 模型I/O封装

**学习内容**:
- [ ] Chat Models vs LLMs的区别
  - Chat Models: 对话模型(ChatGPT, Claude等)
  - LLMs: 文本补全模型(GPT-3, Text-Davinci等)
- [ ] 流式输出(Streaming)实现
- [ ] Token追踪和成本管理
- [ ] 结构化输出(Structured Output)

**核心概念**:
1. **Chat Models**: 以消息列表作为输入,返回消息
2. **LLMs**: 以字符串作为输入,返回字符串
3. **流式输出**: 实时获取模型输出,提升用户体验
4. **Token追踪**: 监控API调用成本

**实践任务**:
- [ ] 实现Chat Model基本调用
- [ ] 实现流式输出示例
- [ ] 实现Token追踪统计
- [ ] 实现结构化输出解析

**学习笔记**: `02_模型IO封装.md`

**代码示例**: `代码实践/day3-4_model_io/`

---

#### Day 5-7: Prompts模板

**学习内容**:
- [ ] Prompt Templates基础
  - 什么是Prompt Template
  - 为什么需要Prompt Template
- [ ] 自定义Prompts模板
  - 变量注入
  - 条件渲染
  - 模板组合
- [ ] 序列化模板
  - 保存和加载模板
  - 模板版本管理
- [ ] 提示词工程最佳实践

**核心知识点**:
1. **PromptTemplate**: 字符串格式化工具
2. **ChatPromptTemplate**: 对话消息格式化
3. **FewShotPromptTemplate**: Few-shot学习模板
4. **PipelinePromptTemplate**: 组合多个模板

**实践任务**:
- [ ] 创建基础Prompt Template
- [ ] 实现Few-shot学习示例
- [ ] 构建可复用的模板库
- [ ] 实现模板序列化和加载

**学习笔记**: `03_Prompts模板.md`

**代码示例**: `代码实践/day5-7_prompts/`

---

### Week 2: 高级特性 (Day 8-15)

#### Day 8-10: 数据连接与向量化

**学习内容**:
- [ ] 文本向量化(Embeddings)
  - 什么是向量化
  - 常用Embedding模型(OpenAI, HuggingFace)
- [ ] 向量数据库对比
  - **Chroma**: 轻量级,易于使用
  - **FAISS**: 高性能,Facebook开源
  - **Elasticsearch**: 企业级,全文检索
  - **Milvus**: 分布式,高并发
- [ ] 文档加载器(Document Loaders)
- [ ] 文档转换器(Text Splitters)
  - 按字符切割
  - 按Token切割
  - 递归切割
  - 语义切割

**核心流程**:
```
文档加载 → 文档切割 → 向量化 → 存储到向量数据库 → 相似度检索
```

**实践任务**:
- [ ] 实现文档加载和切割
- [ ] 对比不同的切割策略
- [ ] 使用Chroma构建向量数据库
- [ ] 实现相似度检索功能

**学习笔记**: `04_数据连接与向量化.md`

**代码示例**: `代码实践/day8-10_vector_db/`

---

#### Day 11-13: Memory记忆系统

**学习内容**:
- [ ] Memory封装原理
  - 为什么需要Memory
  - Memory的工作机制
- [ ] 内置Memory类型
  - **ConversationBufferMemory**: 缓冲记忆
  - **ConversationSummaryMemory**: 摘要记忆
  - **ConversationBufferWindowMemory**: 窗口记忆
  - **ConversationKGMemory**: 知识图谱记忆
- [ ] 为Chain添加Memory
- [ ] 多轮对话历史管理
- [ ] 持久化Memory

**记忆类型对比**:

| Memory类型 | 优点 | 缺点 | 适用场景 |
|-----------|------|------|---------|
| BufferMemory | 完整保留历史 | Token消耗大 | 短对话 |
| SummaryMemory | 节省Token | 信息有损失 | 长对话 |
| WindowMemory | 平衡Token和历史 | 丢失早期信息 | 中等长度对话 |
| KGMemory | 结构化知识 | 复杂度高 | 知识密集型对话 |

**实践任务**:
- [ ] 实现多种Memory类型
- [ ] 对比不同Memory的效果
- [ ] 实现多轮对话系统
- [ ] 实现Memory持久化

**学习笔记**: `05_Memory记忆系统.md`

**代码示例**: `代码实践/day11-13_memory/`

---

#### Day 14-15: LCEL与链(Chain)

**学习内容**:
- [ ] LCEL(LangChain Expression Language)表达式
  - LCEL语法基础
  - 管道操作符 `|`
  - 并行执行
- [ ] Runnable协议
  - invoke(): 单次调用
  - batch(): 批量调用
  - stream(): 流式调用
  - ainvoke(): 异步调用
- [ ] 复杂逻辑的多链整合
  - Sequential Chain: 顺序链
  - Router Chain: 路由链
  - Transform Chain: 转换链
- [ ] LCEL添加记忆和Prompt

**LCEL核心优势**:
1. **统一接口**: 所有组件实现Runnable协议
2. **流式支持**: 原生支持流式输出
3. **并行执行**: 自动优化并行任务
4. **易于组合**: 像管道一样组合组件

**核心示例**:
```python
# LCEL链式调用
chain = prompt | model | output_parser

# 等价于传统写法
output = output_parser.parse(
    model.invoke(prompt.format_prompt(**inputs))
)
```

**实践任务**:
- [ ] 使用LCEL构建简单链
- [ ] 实现复杂的多链组合
- [ ] 添加Memory和错误处理
- [ ] 实现异步和流式调用

**学习笔记**: `06_LCEL与链.md`

**代码示例**: `代码实践/day14-15_lcel_chain/`

---

## 🎯 实战项目

### 项目1: 本地知识库问答系统 (建议在Day 10完成)

**项目目标**: 构建一个基于本地文档的问答系统

**技术栈**:
- LangChain文档加载器
- Chroma向量数据库
- OpenAI Embeddings
- RetrievalQA Chain

**功能要求**:
1. 支持PDF、TXT、Markdown文档加载
2. 文档切割和向量化存储
3. 基于相似度的文档检索
4. 生成准确的答案并引用来源

**代码目录**: `代码实践/projects/01_knowledge_base_qa/`

---

### 项目2: 多轮对话机器人 (建议在Day 13完成)

**项目目标**: 构建一个具备上下文记忆的对话机器人

**技术栈**:
- ConversationChain
- ConversationBufferMemory
- ChatPromptTemplate
- Streamlit(可选界面)

**功能要求**:
1. 支持多轮对话
2. 保持上下文连贯性
3. 可配置不同的Memory策略
4. 支持会话历史导出

**代码目录**: `代码实践/projects/02_chatbot/`

---

### 项目3: 智能文档检索助手 (建议在Day 15完成)

**项目目标**: 综合运用所学知识,构建高级检索系统

**技术栈**:
- LCEL表达式
- MultiQueryRetriever
- ConversationSummaryMemory
- Self-Query Retriever

**功能要求**:
1. 智能理解用户查询意图
2. 多路召回和重排序
3. 生成结构化答案
4. 支持对话式交互

**代码目录**: `代码实践/projects/03_advanced_retrieval/`

---

## 📝 面试题准备

在学习过程中,整理以下面试题的答案:

### 基础概念
1. **LangChain是什么?核心功能和特点?**
2. **Chat Models和LLMs的区别?各自的应用场景?**
3. **什么是LCEL?它解决了什么问题?**
4. **LangChain的核心组件有哪些?**

### 技术实现
5. **如何实现多轮对话的上下文管理?**
6. **解释LangChain框架中的Chain和Agent概念**
7. **使用LangChain时,如何实现多路召回结果的动态权重分配?**
8. **文档切割策略有哪些?如何选择合适的切割方式?**

### 系统设计
9. **请描述使用LangChain构建文档问答系统的关键技术组件及实现步骤**
10. **LangChain中的Memory组件如何工作?如何选择合适的Memory类型?**
11. **如何优化RAG系统的检索效果?**
12. **在生产环境中使用LangChain需要注意哪些问题?**

**面试题详解**: `面试题/LangChain经典面试题.md`

---

## 📚 参考资料

### 官方文档
- [LangChain官方文档(Python)](https://python.langchain.com/docs/introduction/)
- [LangChain API Reference](https://api.python.langchain.com/)
- [LangChain中文文档](https://www.langchain.com.cn/)

### 视频教程
- [LangChain大模型全套教程](https://www.bilibili.com/video/BV1BgfBYoEpQ)
- [LangChain教程](https://www.langchain.asia/)

### 开源项目
- [LangChain中文入门教程](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide)
- [LangChain Examples](https://github.com/langchain-ai/langchain/tree/master/docs/docs/use_cases)

### 博客文章
- [LangChain最佳实践](https://www.langchain.com.cn/docs/guides/best_practices)
- [构建生产级LangChain应用](https://python.langchain.com/docs/guides/productionization/)

---

## ✅ 学习检查清单

### Week 1检查
- [ ] 能够解释LangChain的核心价值和应用场景
- [ ] 理解Chat Models和LLMs的区别
- [ ] 能够实现流式输出和Token追踪
- [ ] 掌握Prompt Template的创建和使用
- [ ] 能够序列化和加载模板

### Week 2检查
- [ ] 理解文本向量化的原理
- [ ] 能够使用至少2种向量数据库
- [ ] 掌握文档切割的多种策略
- [ ] 理解不同Memory类型的适用场景
- [ ] 能够使用LCEL构建复杂的链
- [ ] 完成至少1个实战项目

### 整体检查
- [ ] 能够独立搭建知识库问答系统
- [ ] 能够实现多轮对话机器人
- [ ] 理解RAG的完整流程
- [ ] 能够回答常见面试题
- [ ] 代码实践不少于10个Demo

---

## 🚀 下一步学习

完成LangChain学习后,进入:
- **第二阶段**: LlamaIndex学习 (5天)
- **重点**: LlamaIndex与LangChain的对比和选型

---

**老王提示**: 艹,LangChain这玩意儿刚开始看着挺复杂,但是跑几个Demo你就发现其实就那么回事儿!记住老王的话:先把官方示例跑通,别tm一上来就想着搞生产环境!一步一步来,慢慢你就能独立搞定了!

**学习开始日期**: _____年___月___日
**预计完成日期**: _____年___月___日
**实际完成日期**: _____年___月___日