# Day 11-13 Memory内存系统示例

本目录包含LangChain Memory系统的完整示例代码，让你的AI拥有"记忆力"！

## 📁 文件说明

| 文件 | 说明 | 核心知识点 |
|-----|------|-----------|
| `01_basic_memory.py` | Memory基础 | ConversationBufferMemory/ChatMessageHistory/多用户管理 |
| `02_advanced_memory.py` | 高级Memory类型 | Window/Summary/SummaryBuffer/Token监控 |
| `03_memory_applications.py` | Memory实战应用 | Memory+RAG/VectorMemory/企业级管理 |

## 🚀 快速开始

### 安装依赖

```bash
# 基础依赖
pip install langchain langchain-openai langchain-community python-dotenv

# Memory相关
pip install tiktoken  # Token计数

# RAG相关(可选)
pip install chromadb  # 向量库
```

### 配置环境

创建 `.env` 文件:

```bash
OPENAI_API_KEY=your_openai_api_key
```

### 运行示例

```bash
# Memory基础
python 01_basic_memory.py

# 高级Memory类型
python 02_advanced_memory.py

# Memory实战应用
python 03_memory_applications.py
```

## 📚 学习顺序

### 第1天: Memory基础

1. **理解问题** - 为什么需要Memory
2. **ConversationBufferMemory** - 完整对话历史
3. **手动管理Memory** - save_context/load_memory_variables
4. **Memory持久化** - 保存和恢复

### 第2天: 高级Memory类型

5. **ConversationBufferWindowMemory** - 滑动窗口(控制成本)
6. **ConversationSummaryMemory** - 摘要压缩(降低Token)
7. **ConversationSummaryBufferMemory** - 混合策略(推荐)
8. **Token监控** - 成本控制

### 第3天: Memory实战应用

9. **Memory + RAG** - 对话式知识问答
10. **VectorStoreRetrieverMemory** - 语义检索记忆
11. **组合Memory** - 分层记忆策略
12. **企业级管理** - 多用户/持久化/监控

---

**老王提示**: Memory是实现智能对话的核心！选对Memory类型,能让你的AI既聪明又省钱。

**核心原则**: 没有完美的Memory,只有合适的Memory!根据场景选择,持续监控Token,动态调整策略!💪

**下一步**: 掌握了Memory系统,接下来学习LCEL和Chains(Day 14-15),构建复杂的工作流和应用!