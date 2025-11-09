# LlamaIndex 学习路线图

> **学习周期**: 5天
> **学习目标**: 掌握LlamaIndex框架,理解与LangChain的区别,能够构建高效的RAG应用

---

## 📅 学习计划

### Day 16: LlamaIndex基础

**学习内容**:
- [ ] 什么是LlamaIndex
  - LlamaIndex的定位和核心价值
  - 为什么需要LlamaIndex
  - LlamaIndex vs LangChain初步对比
- [ ] LlamaIndex的优势和劣势
  - **优势**: 专注数据索引、高效检索、易于上手
  - **劣势**: 生态相对小、社区资源少
- [ ] 环境搭建和快速开始
  - 安装依赖
  - 第一个Hello World示例
- [ ] LlamaIndex核心概念
  - Index(索引)
  - Query Engine(查询引擎)
  - Retriever(检索器)

**核心理念**:
> LlamaIndex是一个"data framework",专注于连接LLM与外部数据
> LangChain是一个"application framework",专注于构建LLM应用

**实践任务**:
- [ ] 安装LlamaIndex
- [ ] 运行官方Quick Start示例
- [ ] 理解Index的创建过程
- [ ] 实现简单的文档查询

**安装命令**:
```bash
pip install llama-index
pip install llama-index-llms-openai
pip install llama-index-embeddings-openai
```

**学习笔记**: `01_LlamaIndex基础概念.md`

**代码示例**: `代码实践/day16_basics/`

**参考资料**:
- [LlamaIndex官方文档](https://docs.llamaindex.ai/en/stable/)
- [LlamaIndex快速开始](https://docs.llamaindex.ai/en/stable/getting_started/starter_example/)

---

### Day 17-18: 索引与检索

#### Day 17: 文档索引构建

**学习内容**:
- [ ] 索引类型详解
  - **VectorStoreIndex**: 向量存储索引(最常用)
  - **ListIndex**: 列表索引
  - **TreeIndex**: 树形索引
  - **KeywordTableIndex**: 关键词表索引
- [ ] 文档加载器(Data Connectors)
  - SimpleDirectoryReader
  - PDFReader
  - NotionReader
  - 自定义Reader
- [ ] 索引构建流程
  ```
  文档加载 → Node解析 → 向量化 → 构建索引 → 持久化
  ```

**核心概念**:
1. **Document**: 原始文档对象
2. **Node**: 文档的基本单元(类似LangChain的chunk)
3. **Index**: 数据的组织结构
4. **Vector Store**: 向量存储后端

**实践任务**:
- [ ] 加载不同格式的文档
- [ ] 创建VectorStoreIndex
- [ ] 对比不同索引类型的效果
- [ ] 实现索引的持久化和加载

**学习笔记**: `02_文档索引构建.md`

**代码示例**: `代码实践/day17_indexing/`

---

#### Day 18: 查询和检索优化

**学习内容**:
- [ ] Query Engine(查询引擎)
  - 默认查询引擎
  - 自定义查询引擎
  - 查询参数配置
- [ ] Retriever(检索器)
  - VectorIndexRetriever
  - KeywordTableRetriever
  - 混合检索
- [ ] 检索优化技术
  - Top-K参数调优
  - 相似度阈值设置
  - Re-ranking重排序
  - 查询转换(Query Transformation)

**检索策略对比**:

| 检索方式 | 原理 | 优点 | 缺点 | 适用场景 |
|---------|------|------|------|---------|
| 向量检索 | 语义相似度 | 理解语义 | 计算成本高 | 概念性查询 |
| 关键词检索 | 精确匹配 | 速度快 | 无法理解语义 | 精确查找 |
| 混合检索 | 结合两者 | 综合效果好 | 实现复杂 | 生产环境推荐 |

**实践任务**:
- [ ] 使用Query Engine进行查询
- [ ] 实现混合检索策略
- [ ] 对比不同Top-K值的效果
- [ ] 实现查询结果的重排序

**学习笔记**: `03_查询与检索优化.md`

**代码示例**: `代码实践/day18_retrieval/`

**参考资料**:
- [LlamaIndex Retrieval Guide](https://docs.llamaindex.ai/en/stable/module_guides/querying/)

---

### Day 19: RAG应用实践

**学习内容**:
- [ ] LlamaIndex与RAG检索增强
  - RAG的基本原理
  - LlamaIndex在RAG中的角色
  - 端到端RAG系统构建
- [ ] 文档问答系统实战
  - 多文档处理
  - 上下文窗口管理
  - 引用来源追踪
- [ ] 性能优化技巧
  - 索引优化
  - 查询优化
  - 缓存策略
  - 成本控制

**RAG系统架构**:
```
用户查询
  ↓
查询理解(Query Understanding)
  ↓
文档检索(Document Retrieval) ← LlamaIndex核心
  ↓
上下文增强(Context Augmentation)
  ↓
答案生成(Answer Generation)
  ↓
结果后处理(Post-processing)
```

**优化要点**:
1. **索引优化**: 选择合适的索引类型
2. **切片策略**: 合理设置chunk size
3. **检索召回**: 调整Top-K和相似度阈值
4. **Prompt工程**: 优化生成Prompt模板
5. **缓存机制**: 减少重复计算

**实践任务**:
- [ ] 构建完整的RAG问答系统
- [ ] 实现多文档联合检索
- [ ] 添加引用来源追踪
- [ ] 进行性能测试和优化

**学习笔记**: `04_RAG应用实践.md`

**代码示例**: `代码实践/day19_rag_practice/`

**参考资料**:
- [LlamaIndex RAG教程](https://docs.llamaindex.ai/en/stable/examples/usecases/10k_sub_question/)

---

### Day 20: 框架对比与选型

**学习内容**:
- [ ] LlamaIndex与LangChain深度对比
  - 设计理念差异
  - 功能特性对比
  - 性能对比
  - 生态系统对比
- [ ] 不同场景下的框架选择
  - 简单问答系统: LlamaIndex优先
  - 复杂Agent应用: LangChain优先
  - 企业级应用: 两者结合
- [ ] 综合项目实战
  - 结合LangChain和LlamaIndex
  - 发挥各自优势
  - 构建生产级应用

**框架对比表**:

| 对比维度 | LlamaIndex | LangChain |
|---------|-----------|-----------|
| **核心定位** | Data Framework | Application Framework |
| **主要用途** | 数据索引和检索 | 端到端应用开发 |
| **学习曲线** | ⭐⭐⭐ (较易) | ⭐⭐⭐⭐ (较难) |
| **数据处理** | ⭐⭐⭐⭐⭐ (强) | ⭐⭐⭐ (中) |
| **Agent支持** | ⭐⭐ (弱) | ⭐⭐⭐⭐⭐ (强) |
| **社区生态** | ⭐⭐⭐ (中等) | ⭐⭐⭐⭐⭐ (丰富) |
| **文档质量** | ⭐⭐⭐⭐ (好) | ⭐⭐⭐⭐ (好) |
| **性能表现** | ⭐⭐⭐⭐ (优) | ⭐⭐⭐ (良) |
| **适用场景** | RAG、问答系统 | Agent、工作流 |

**选型建议**:
1. **纯RAG应用** → 优先LlamaIndex
2. **需要Agent** → 优先LangChain
3. **复杂应用** → LangChain + LlamaIndex
4. **快速原型** → LlamaIndex (更简单)
5. **生产环境** → 根据具体需求评估

**实践任务**:
- [ ] 对比同一任务在两个框架的实现
- [ ] 分析两者的性能差异
- [ ] 尝试结合使用两个框架
- [ ] 总结各自的最佳实践

**学习笔记**: `05_框架对比与选型.md`

**代码示例**: `代码实践/day20_comparison/`

---

## 🎯 实战项目

### 项目1: 企业文档智能问答系统

**项目目标**: 构建一个企业级的文档问答系统

**技术栈**:
- LlamaIndex VectorStoreIndex
- OpenAI Embeddings & GPT-4
- Streamlit界面(可选)

**功能要求**:
1. 支持多种文档格式(PDF, Word, TXT, Markdown)
2. 文档预处理和索引构建
3. 智能检索和答案生成
4. 引用来源追踪
5. 相关文档推荐

**技术亮点**:
- 混合检索策略
- 查询结果重排序
- 上下文窗口优化
- 缓存机制提升性能

**代码目录**: `代码实践/projects/01_enterprise_qa/`

---

### 项目2: 知识库检索增强应用

**项目目标**: 构建一个支持持续学习的知识库系统

**技术栈**:
- LlamaIndex TreeIndex
- Chroma向量数据库
- LangChain Memory(可选)

**功能要求**:
1. 增量式文档索引更新
2. 知识图谱可视化
3. 多路召回和融合
4. 个性化检索排序
5. 知识库统计分析

**技术亮点**:
- 增量索引更新策略
- 多索引并行检索
- 自定义评分函数
- 检索质量评估

**代码目录**: `代码实践/projects/02_knowledge_base/`

---

## 📝 面试题准备

### 基础概念
1. **LlamaIndex是什么?它的主要功能和目标是什么?**
2. **LlamaIndex和LangChain的核心区别是什么?**
3. **LlamaIndex中的Index有哪些类型?各自适用于什么场景?**

### 技术实现
4. **LlamaIndex如何构建文档索引?描述索引结构**
5. **在LlamaIndex中,如何处理和管理大量非结构化数据?**
6. **如何对文档进行预处理,以确保索引的效率和检索质量?**
7. **LlamaIndex中的Query Engine和Retriever有什么区别?**

### 系统设计
8. **LlamaIndex如何处理复杂的查询和多步骤推理任务?**
9. **如何在LlamaIndex中实现混合检索策略?**
10. **在生产环境中使用LlamaIndex需要考虑哪些性能优化?**
11. **如何评估LlamaIndex检索系统的质量?有哪些指标?**

### 对比分析
12. **什么场景下选择LlamaIndex而不是LangChain?**
13. **如何结合LlamaIndex和LangChain构建应用?**
14. **LlamaIndex在RAG系统中的优势是什么?**

**面试题详解**: `面试题/LlamaIndex经典面试题.md`

---

## 📚 参考资料

### 官方文档
- [LlamaIndex官方文档](https://docs.llamaindex.ai/en/stable/)
- [LlamaIndex API Reference](https://docs.llamaindex.ai/en/stable/api_reference/)
- [LlamaIndex使用指南](https://llama-index.readthedocs.io/zh/latest/guides/primer.html)

### 视频教程
- [LlamaIndex零基础全套课程](https://www.bilibili.com/video/BV1JDpFeEEay/)
- [LlamaIndex教程合集](https://llama-index.readthedocs.io/zh/latest/guides/tutorials.html)

### 开源项目
- [LlamaIndex Examples](https://github.com/run-llama/llama_index/tree/main/docs/examples)
- [LlamaIndex中文教程](https://github.com/liaokongVFX/llama-index-chinese)

### 博客文章
- [LlamaIndex最佳实践](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/)
- [构建高效的RAG系统](https://docs.llamaindex.ai/en/stable/understanding/putting_it_all_together/q_and_a/)

---

## ✅ 学习检查清单

### Day 16检查
- [ ] 理解LlamaIndex的核心定位
- [ ] 能够创建基本的索引
- [ ] 完成Quick Start示例
- [ ] 理解Index、QueryEngine、Retriever的关系

### Day 17-18检查
- [ ] 掌握至少3种索引类型
- [ ] 能够加载不同格式的文档
- [ ] 理解Node的概念和作用
- [ ] 能够实现混合检索策略
- [ ] 掌握检索优化的基本方法

### Day 19检查
- [ ] 能够构建完整的RAG系统
- [ ] 理解RAG的端到端流程
- [ ] 掌握性能优化的关键点
- [ ] 能够追踪引用来源

### Day 20检查
- [ ] 清楚LlamaIndex和LangChain的区别
- [ ] 能够根据场景选择合适的框架
- [ ] 理解两者结合使用的方式
- [ ] 完成至少1个综合项目

### 整体检查
- [ ] 能够独立构建企业级问答系统
- [ ] 理解索引优化的关键技术
- [ ] 能够评估检索质量
- [ ] 能够回答常见面试题
- [ ] 代码实践不少于5个Demo

---

## 🚀 下一步学习

完成LlamaIndex学习后,进入:
- **第三阶段**: Agent开发学习 (20天)
- **重点**: 将LlamaIndex作为Agent的工具使用

---

**老王提示**: 艹,LlamaIndex这玩意儿比LangChain简单多了!专注做好一件事——数据索引和检索。如果你只是想搞个文档问答系统,直接用LlamaIndex就行,别tm搞那么复杂!5天时间把这个框架吃透,后面Agent开发时还能用上!

**重要**: LlamaIndex是专注于数据的框架,LangChain是专注于应用的框架。理解这个区别,你就能正确选型了!

**学习开始日期**: _____年___月___日
**预计完成日期**: _____年___月___日
**实际完成日期**: _____年___月___日