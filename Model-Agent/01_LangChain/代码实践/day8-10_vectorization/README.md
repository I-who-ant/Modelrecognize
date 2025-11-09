# Day 8-10 数据连接与向量化示例

本目录包含LangChain数据连接与向量化的完整示例代码,是实现RAG(检索增强生成)的核心基础。

## 📁 文件说明

| 文件 | 说明 | 核心知识点 |
|-----|------|-----------  |
| `01_document_loaders.py` | 文档加载器 | TextLoader/PDFLoader/WebLoader/DirectoryLoader |
| `02_text_splitting.py` | 文本切割策略 | RecursiveCharacterTextSplitter/chunk_size/overlap |
| `03_vector_stores.py` | 向量数据库对比 | Chroma/FAISS/检索策略/性能对比 |
| `04_rag_application.py` | 完整RAG应用 | RetrievalQA/检索优化/效果评估 |

## 🚀 快速开始

### 安装依赖

```bash
# 基础依赖
pip install langchain langchain-openai langchain-community python-dotenv

# 向量数据库
pip install chromadb faiss-cpu

# 可选依赖
pip install pypdf beautifulsoup4 tiktoken  # PDF/网页/Token计数
```

### 配置环境

创建 `.env` 文件:

```bash
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com/v1  # 可选
```

### 运行示例

```bash
# 文档加载器
python 01_document_loaders.py

# 文本切割
python 02_text_splitting.py

# 向量数据库
python 03_vector_stores.py

# 完整RAG应用
python 04_rag_application.py
```

## 📚 学习顺序

### 第1天: 文档加载和切割

1. **文档加载器** (`01`) - 掌握多种数据源加载
2. **文本切割** (`02`) - 理解chunk_size和overlap的影响

**学习目标**:
- 能使用至少3种文档加载器
- 理解Document对象结构
- 掌握RecursiveCharacterTextSplitter
- 会调优chunk_size和overlap

### 第2天: 向量化和存储

3. **向量数据库** (`03`) - 学会使用Chroma和FAISS

**学习目标**:
- 掌握Chroma和FAISS的基本使用
- 理解相似度检索/MMR/阈值检索
- 能根据场景选择合适的向量库
- 了解性能优化技巧

### 第3天: 完整RAG应用

4. **RAG应用** (`04`) - 实现端到端的检索增强生成

**学习目标**:
- 实现完整的RAG流程
- 掌握多种检索优化技巧
- 理解RAG效果评估
- 能解决常见问题

## 💡 核心概念

### 1. Document对象

```python
from langchain_core.documents import Document

doc = Document(
    page_content="文档内容",  # 必需
    metadata={               # 可选但重要
        "source": "file.txt",
        "page": 1
    }
)
```

**关键点**:
- `page_content`: 文本内容
- `metadata`: 元数据(用于过滤和追溯)

### 2. 文本切割

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 块大小
    chunk_overlap=50,      # 重叠
    separators=["\n\n", "\n", "。", " ", ""]  # 分隔符优先级
)

chunks = splitter.split_documents(docs)
```

**参数建议**:
- **chunk_size**: 200-1000字符(根据场景调整)
- **chunk_overlap**: 10-20%的chunk_size
- **separators**: 从粗到细(段落→句子→词)

### 3. 向量数据库

#### Chroma(推荐开发使用)

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="./chroma_db"  # 持久化
)

# 相似度检索
results = vectorstore.similarity_search("查询", k=3)
```

**特点**:
- ✅ 零配置,易用
- ✅ 支持持久化
- ✅ 强大的元数据过滤

#### FAISS(推荐生产使用)

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small")
)

# 保存和加载
vectorstore.save_local("faiss_index")
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(model="text-embedding-3-small"),
    allow_dangerous_deserialization=True
)
```

**特点**:
- ✅ 性能极高
- ✅ 内存高效
- ✅ 支持GPU加速

### 4. RAG流程

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# 创建检索器
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# 创建QA链
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    retriever=retriever,
    return_source_documents=True
)

# 提问
result = qa_chain.invoke({"query": "问题"})
print(result["result"])          # 答案
print(result["source_documents"])  # 来源
```

## 🎯 使用场景

### 场景1: 个人知识库问答

```python
# 加载个人笔记
loader = DirectoryLoader("notes/", glob="*.md", loader_cls=TextLoader)
docs = loader.load()

# 切割
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.split_documents(docs)

# 创建向量库
vectorstore = Chroma.from_documents(splits, OpenAIEmbeddings())

# 问答
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
```

### 场景2: PDF技术文档助手

```python
# 加载PDF
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("technical_doc.pdf")
pages = loader.load()

# 按章节切割(保留元数据)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80
)
splits = splitter.split_documents(pages)

# FAISS高性能检索
vectorstore = FAISS.from_documents(splits, OpenAIEmbeddings())
```

### 场景3: 多文档混合检索

```python
# 加载多个文档
docs = []
for file in ["doc1.txt", "doc2.pdf", "doc3.md"]:
    loader = get_loader_for_file(file)  # 根据文件类型选择加载器
    docs.extend(loader.load())

# 基于元数据过滤
results = vectorstore.similarity_search(
    "查询",
    k=3,
    filter={"source": "doc1.txt"}  # 只在doc1中检索
)
```

## 🔧 参数调优指南

### chunk_size选择

| 场景 | 推荐chunk_size | 原因 |
|-----|---------------|------|
| 短问答 | 200-500 | 精准匹配,快速检索 |
| 长文本理解 | 500-1000 | 保留足够上下文 |
| 代码文档 | 1000-2000 | 保持代码完整性 |
| 技术文档 | 300-800 | 平衡精度和完整性 |

### k值(检索数量)选择

| 场景 | 推荐k值 | 原因 |
|-----|--------|------|
| 精确问答 | 1-3 | 降低噪声,提高精度 |
| 综合分析 | 5-10 | 更全面的信息 |
| 对话系统 | 3-5 | 平衡上下文和响应速度 |

### 检索策略选择

| 策略 | 使用场景 | 特点 |
|-----|---------|------|
| similarity | 通用场景 | 最常用,效果稳定 |
| mmr | 需要多样性 | 避免重复,更全面 |
| similarity_score_threshold | 严格控制质量 | 只返回高相关度结果 |

## ⚠️ 常见问题

### Q1: 检索不到相关文档?

**诊断**:
```python
# 查看检索到什么
results = vectorstore.similarity_search_with_score("查询", k=5)
for doc, score in results:
    print(f"Score: {score:.4f}")
    print(f"Content: {doc.page_content[:100]}")
```

**解决方案**:
1. ✅ 调整chunk_size(尝试更大或更小)
2. ✅ 增加k值
3. ✅ 使用MultiQueryRetriever改写查询
4. ✅ 检查是否有拼写错误

### Q2: 答案不对或有幻觉?

**解决方案**:
1. ✅ 优化Prompt模板,明确"只基于上下文"
2. ✅ 降低temperature(设为0)
3. ✅ 使用ContextualCompressionRetriever减少噪声
4. ✅ 添加来源引用要求

示例Prompt:
```python
custom_prompt = PromptTemplate(
    template="""基于以下上下文回答问题。如果上下文中没有相关信息,明确说明"根据提供的信息无法回答"。

上下文: {context}

问题: {question}

回答:"""
)
```

### Q3: 性能太慢?

**优化策略**:
1. ✅ 使用FAISS替代Chroma
2. ✅ 缓存Embedding
3. ✅ 减小chunk_size和k值
4. ✅ 批量处理

```python
# 使用Embedding缓存
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

store = LocalFileStore("./cache/")
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings=OpenAIEmbeddings(),
    document_embedding_cache=store
)
```

### Q4: 成本太高?

**降低成本**:
1. ✅ 使用text-embedding-3-small($0.02/1M tokens)
2. ✅ 使用本地Embedding模型
3. ✅ 缓存Embedding避免重复计算
4. ✅ 减小chunk_size和k值

```python
# 本地模型(免费)
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## 📊 向量库选择决策树

```
是否是开发/原型阶段?
├─ 是 → Chroma (零配置,易用)
└─ 否 → 文档规模多大?
    ├─ < 10万文档 → FAISS (高性能,简单)
    ├─ 10万-百万 → Elasticsearch (成熟稳定)
    └─ > 百万文档 → Milvus (专业向量库)

需要云服务?
└─ 是 → Pinecone (完全托管)

需要混合检索(全文+向量)?
└─ 是 → Elasticsearch

需要复杂元数据过滤?
└─ 是 → Chroma/Qdrant
```

## 📈 最佳实践

### 1. 数据准备

```python
# ✅ 好的实践
docs = [
    Document(
        page_content=content,
        metadata={
            "source": "file.pdf",
            "page": 1,
            "chapter": "第三章",
            "date": "2025-01-09",
            "topic": "技术",
            "author": "张三"
        }
    )
]

# ❌ 不好的实践
docs = [Document(page_content=content)]  # 缺少元数据
```

### 2. 文本切割

```python
# ✅ 好的实践
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,  # 10%的chunk_size
    separators=["\n\n", "\n", "。", "!", "?", "，", " ", ""]  # 中文优化
)

# ❌ 不好的实践
splitter = CharacterTextSplitter(chunk_size=5000)  # 太大,无overlap
```

### 3. 检索优化

```python
# ✅ 好的实践 - 多策略组合
from langchain.retrievers import EnsembleRetriever

vector_retriever = vectorstore.as_retriever(search_type="mmr")
bm25_retriever = BM25Retriever.from_documents(docs)

ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)

# ❌ 不好的实践 - 单一策略
retriever = vectorstore.as_retriever()  # 只用基础相似度
```

### 4. Prompt设计

```python
# ✅ 好的实践 - 清晰的指令和约束
prompt = """基于以下上下文回答问题。

要求:
1. 只使用提供的上下文信息
2. 如果不确定,明确说明
3. 简洁明了,不超过3句话

上下文: {context}
问题: {question}

回答:"""

# ❌ 不好的实践 - 模糊的指令
prompt = "用这些信息回答: {context}\n问题: {question}"
```

## ✅ 学习检查清单

完成Day 8-10学习后,确保你能够:

- [ ] 使用至少3种文档加载器(Text/PDF/Web)
- [ ] 创建带丰富元数据的Document对象
- [ ] 配置RecursiveCharacterTextSplitter
- [ ] 根据场景选择合适的chunk_size和overlap
- [ ] 使用Chroma创建和查询向量库
- [ ] 使用FAISS进行高性能检索
- [ ] 实现完整的RAG流程(加载→切割→向量化→检索→生成)
- [ ] 使用不同检索策略(Similarity/MMR/Threshold)
- [ ] 基于元数据进行精准过滤
- [ ] 优化RAG效果(Prompt/检索策略/参数调优)
- [ ] 选择合适的向量数据库
- [ ] 评估和优化RAG系统

## 📖 扩展阅读

- [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [RAG教程](https://python.langchain.com/docs/use_cases/question_answering/)
- [Chroma文档](https://docs.trychroma.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)

## 💾 生成的文件

运行示例后会生成:

```
代码实践/day8-10_vectorization/
├── sample_data/              # 文档加载器示例数据
│   ├── sample.txt
│   ├── doc1.txt
│   ├── doc2.txt
│   └── ...
├── rag_data/                 # RAG示例数据
│   └── langchain_intro.txt
├── chroma_db/                # Chroma持久化目录
├── faiss_index/              # FAISS索引文件
└── embedding_cache/          # Embedding缓存
```

---

**老王提示**: 数据连接和向量化是RAG的核心基础！别小看文本切割,chunk_size选不好,再牛逼的模型也救不了你的检索效果!记住:

1. **文档加载** - 多格式支持 + 丰富元数据
2. **文本切割** - chunk_size实验调优 + 充分overlap
3. **向量化** - 选对Embedding模型(成本vs效果)
4. **向量库** - 开发用Chroma,生产看规模
5. **RAG流程** - 端到端打通,持续优化
6. **效果优化** - 混合检索 + 重排序 + Query改写

**核心原则**: 好的切割策略 = RAG成功的一半！💪

**下一步**: 掌握了数据连接和向量化,接下来学习Memory系统(Day 11-13)来实现有记忆的对话!