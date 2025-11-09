# 📖 Day 8-10 数据连接与向量化完整学习指南

## 目标概览

完成Day 8-10的学习后，你将能够：

- ✅ 使用多种Document Loaders加载不同格式的数据(Text/PDF/Web/CSV)
- ✅ 掌握文本切割策略，理解chunk_size和overlap的影响
- ✅ 使用Chroma和FAISS构建向量数据库
- ✅ 实现完整的RAG(Retrieval-Augmented Generation)流程
- ✅ 优化检索策略(Similarity/MMR/Threshold)
- ✅ 解决常见的检索问题(检索不到、幻觉、性能等)
- ✅ 根据场景选择合适的向量库

---

## 📚 核心学习内容

### 1️⃣ Document Loaders（第8天上午）

**时间**: 1小时
**难度**: ⭐⭐ 简单

#### 核心概念：什么是Document Loader？

Document Loader的作用：
- 从各种数据源读取文档
- 将数据转换为LangChain的Document对象
- 提取并保存元数据

#### Document对象结构

```python
from langchain_core.documents import Document

doc = Document(
    page_content="文档的主要内容，可以是任意长度的文本",  # 必需
    metadata={  # 可选但重要！
        "source": "file.txt",      # 来源（用于追踪）
        "page": 1,                 # 页码
        "author": "老王",          # 作者
        "created_at": "2025-01-09",# 创建时间
        "topic": "LangChain",       # 话题分类
        # 可以添加任意自定义字段
    }
)

print(doc.page_content)   # 访问内容
print(doc.metadata)       # 访问元数据
print(doc.metadata['source'])  # 访问特定字段
```

#### 常用Document Loaders

```python
from langchain_community.document_loaders import (
    TextLoader,           # 纯文本文件
    DirectoryLoader,      # 批量加载目录
    PyPDFLoader,          # PDF文件
    WebBaseLoader,        # 网页内容
    CSVLoader,            # CSV文件
    UnstructuredMarkdownLoader  # Markdown文件
)

# 1. TextLoader - 单个文本文件
loader = TextLoader("document.txt", encoding='utf-8')
docs = loader.load()

# 2. DirectoryLoader - 批量加载目录
loader = DirectoryLoader(
    path="./documents",
    glob="*.txt",           # 文件模式
    loader_cls=TextLoader,  # 使用的加载器
    show_progress=True      # 显示进度
)
docs = loader.load()

# 3. PyPDFLoader - PDF文件
loader = PyPDFLoader("paper.pdf")
pages = loader.load()  # 每页是一个Document

# 4. WebBaseLoader - 网页
loader = WebBaseLoader(
    ["https://python.langchain.com/docs/get_started/introduction"]
)
docs = loader.load()

# 5. CSVLoader - CSV数据
loader = CSVLoader(file_path="data.csv")
docs = loader.load()

# 6. 自定义Document创建
docs = [
    Document(
        page_content="内容1",
        metadata={"source": "manual", "type": "example"}
    ),
    Document(
        page_content="内容2",
        metadata={"source": "manual", "type": "example"}
    )
]
```

#### 最佳实践：添加丰富的元数据

```python
from pathlib import Path
from langchain_core.documents import Document

def load_documents_with_metadata(directory: str):
    """加载文档并添加丰富的元数据"""

    docs = []
    for file_path in Path(directory).glob("*.txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 添加丰富的元数据
        metadata = {
            "source": str(file_path),
            "filename": file_path.name,
            "file_size": file_path.stat().st_size,
            "created_at": file_path.stat().st_mtime,
            "content_length": len(content),
            "word_count": len(content.split()),
        }

        docs.append(Document(page_content=content, metadata=metadata))

    return docs

# 使用
docs = load_documents_with_metadata("./knowledge_base") # 加载并添加元数据

# 可以基于元数据过滤
large_docs = [doc for doc in docs if doc.metadata['file_size'] > 10000] # 过滤文件大小超过10KB的文档
```

---

### 2️⃣ 文本切割策略（第8天下午）

**时间**: 1小时
**难度**: ⭐⭐⭐ 中等

#### 核心概念：为什么需要文本切割？

- ❌ 整个文档太长，超过LLM的上下文窗口
- ❌ 一次加载整个文档到内存，消耗资源
- ✅ 切割成小块，便于向量化和检索

#### RecursiveCharacterTextSplitter详解

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 块大小(字符数)
    chunk_overlap=50,    # 块重叠(保留上下文)
    separators=[
        "\n\n",         # 优先在段落分隔
        "\n",           # 其次在行分隔
        "。",           # 中文句号
        "!",            # 感叹号
        "?",            # 问号
        "，",           # 中文逗号
        " ",            # 空格
        ""              # 最后才按字符分割
    ]
)

chunks = splitter.split_documents(documents) # 对文档进行切割
```

#### chunk_size的选择指南

| 场景 | 推荐大小 | 原因 |
|------|---------|------|
| 短问答 | 200-400 | 精准匹配，减少噪声 |
| 一般阅读理解 | 400-800 | 平衡精度和上下文 |
| 长文本理解 | 800-1500 | 保留更多上下文 |
| 代码文档 | 1000-2000 | 保持代码完整性 |
| 技术文档 | 500-1000 | 平衡章节完整性 |

#### overlap的重要性

```python
# overlap太小：关键信息可能被分割
# "...这个概念很重要。 下一个概念..."
# ❌ chunk1: "...这个概念很重要。"
# ❌ chunk2: "下一个概念..."  # 缺少上下文

# overlap充分：保留关键上下文
# ✅ chunk1: "...这个概念很重要。 下一个概念"
# ✅ chunk2: "这个概念很重要。 下一个概念..." # 有共同的过渡句

# 推荐：overlap = 10-20% of chunk_size
# chunk_size=500, overlap=50-100
```

#### 文本切割完整示例

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 加载文档
loader = TextLoader("technical_doc.txt", encoding='utf-8')
docs = loader.load()

print(f"加载了{len(docs)}个文档，总大小{sum(len(d.page_content) for d in docs)}字符")

# 2. 切割文本
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=60,
    separators=["\n\n", "\n", "。", " ", ""]
)

chunks = splitter.split_documents(docs)

print(f"切割后得到{len(chunks)}个块")

# 3. 检查切割效果
for i, chunk in enumerate(chunks[:3]):  # 查看前3个
    print(f"\n=== Chunk {i+1} ===")
    print(f"大小: {len(chunk.page_content)}字符")
    print(f"内容: {chunk.page_content[:100]}...")
    print(f"元数据: {chunk.metadata}")
```

#### 文本切割的陷阱

```python
# ❌ 陷阱1: 使用简单的分割方式
from langchain.text_splitter import CharacterTextSplitter
splitter = CharacterTextSplitter(chunk_size=1000)  # 不推荐，没有overlap

# ✅ 改进：使用递归分割
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", " ", ""]
)

# ❌ 陷阱2: 丢失元数据
chunks = splitter.split_text(raw_text)  # 只返回字符串，丢失元数据

# ✅ 改进：保留元数据
chunks = splitter.split_documents(documents)  # 返回Document对象，保留元数据
```

---

### 3️⃣ 向量数据库（第9天）

**时间**: 1.5小时
**难度**: ⭐⭐⭐ 中等

#### 核心概念：什么是向量数据库？

向量数据库存储文本的向量表示(Embeddings)，支持高效的语义相似度检索。

#### Chroma vs FAISS 对比

| 特性 | Chroma | FAISS |
|------|--------|-------|
| 零配置 | ✅ | ❌ |
| 持久化 | ✅ | ✅ |
| 元数据过滤 | ✅ 强大 | ⭐ 基础 |
| 性能 | ⭐ 中等 | ✅ 极高 |
| 内存高效 | ⭐ | ✅ |
| 生产推荐 | 开发/小规模 | 生产/大规模 |

#### Chroma快速开始

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 1. 加载和切割文档
loader = TextLoader("documents.txt")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# 2. 创建向量库
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 持久化
)

# 3. 相似度检索
results = vectorstore.similarity_search("什么是LangChain?", k=3)

for i, doc in enumerate(results):
    print(f"\n=== 结果{i+1} ===")
    print(f"内容: {doc.page_content}")
    print(f"来源: {doc.metadata.get('source')}")

# 4. 加载已有的向量库
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

#### FAISS高性能应用

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1. 创建FAISS向量库
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# 2. 保存和加载
vectorstore.save_local("faiss_index")

# 加载已有索引
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# 3. 检索
results = vectorstore.similarity_search("问题", k=5)

# 4. 带分数的检索(了解相关度)
results_with_scores = vectorstore.similarity_search_with_score("问题", k=5)

for doc, score in results_with_scores:
    print(f"相关度: {score:.4f}")  # 分数越低越相关
    print(f"内容: {doc.page_content}")
```

#### Embedding模型选择

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# 选项1: OpenAI (最强质量，收费)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # $0.02/1M tokens
    api_key="sk-..."
)

# 选项2: 本地免费模型 (推荐开发使用)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 选项3: 国内服务(阿里云、华为等)
# 根据服务商API配置

# 如何选择？
# 开发阶段 → 本地免费模型
# 生产环境 → 评估质量和成本，可用OpenAI或其他商业服务
```

---

### 4️⃣ RAG应用（第10天）

**时间**: 1.5小时
**难度**: ⭐⭐⭐⭐ 困难

#### 核心概念：什么是RAG？

**RAG = Retrieval-Augmented Generation**

流程：用户问题 → 检索相关文档 → 用文档增强Prompt → 生成答案

```
用户问题: "LangChain有什么优势?"
    ↓
检索向量库，找到top-3相关文档
    ↓
原始Prompt + 检索到的文档
    ↓
LLM生成答案(基于现实数据，不幻觉)
    ↓
用户看到答案 + 来源引用
```

#### 最简单的RAG实现

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. 创建向量库(假设已有)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

# 2. 创建检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 相似度检索
    search_kwargs={"k": 3}     # 返回top-3
)

# 3. 创建LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 4. 创建QA链
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # 将检索结果直接放入prompt
    retriever=retriever,
    return_source_documents=True  # 返回来源
)

# 5. 提问
result = qa_chain.invoke({"query": "什么是LangChain?"})

print("答案:", result["result"])
print("来源:")
for doc in result["source_documents"]:
    print(f"  - {doc.metadata.get('source')}")
```

#### 高级检索策略

```python
from langchain_community.vectorstores import Chroma

# 策略1: 相似度检索(默认，通用)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 策略2: MMR (Maximum Marginal Relevance)
# 不仅检索相关性高的，还要多样性
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10}
    # fetch_k: 先取10个，再用MMR筛选到3个
)

# 策略3: 相似度阈值
# 只返回相似度超过阈值的结果
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 3}
)

# 各策略对比
# 相似度: 最快，适合通用场景
# MMR: 更多样，适合需要不同角度的场景
# 阈值: 最严格，避免低质量结果
```

#### 完整RAG应用示例

```python
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 自定义Prompt
custom_prompt = PromptTemplate(
    template="""基于以下上下文回答问题。

要求:
1. 只使用提供的上下文信息
2. 如果上下文中没有答案，明确说"根据提供的资料无法回答"
3. 回答要简洁明了，不超过200字

上下文:
{context}

问题: {question}

回答:""",
    input_variables=["context", "question"]
)

# 创建QA链(使用自定义Prompt)
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": custom_prompt,
        "document_variable_name": "context"
    }
)

# 使用
result = qa_chain.invoke({"query": "提问"})
answer = result["result"]
sources = result["source_documents"]
```

#### 常见问题及解决方案

```python
# 问题1: 检索不到相关文档

# 诊断
results = vectorstore.similarity_search_with_score("查询", k=5)
print(f"最高相关度: {results[0][1]:.4f}")  # 分数接近1说明相关度低

# 解决方案
# a) 调整chunk_size - 试试更小或更大的块
# b) 增加k值 - 从3增加到5或10
# c) 更换检索策略 - 试试MMR
# d) 优化查询 - 用更清晰的表述

# 问题2: LLM生成幻觉(编造答案)

# 原因：Prompt没有明确限制
# 解决方案：优化Prompt指令
custom_prompt = """基于以下上下文回答问题。
如果上下文中没有相关信息，明确说"无法回答"。
不要编造或猜测信息。

上下文: {context}
问题: {question}
回答:"""

# 问题3: 性能太慢

# 解决方案
# a) 使用FAISS替代Chroma
# b) 减小chunk_size和k值
# c) 使用缓存
# d) 在检索前预处理查询(如问题改写)
```

---

## 🎯 完整代码示例

### 示例1：个人知识库问答

```python
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

def create_personal_knowledge_base(notes_dir: str):
    """创建个人知识库问答系统"""

    # 1. 加载笔记
    loader = DirectoryLoader(
        notes_dir,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    docs = loader.load()
    print(f"✅ 加载了{len(docs)}个文档")

    # 2. 切割文本
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ 切割为{len(chunks)}个块")

    # 3. 创建向量库
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="./kb_db"
    )
    print(f"✅ 向量库已创建")

    # 4. 创建QA系统
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    return qa

# 使用
qa_system = create_personal_knowledge_base("./my_notes")

# 提问
result = qa_system.invoke({"query": "Python的装饰器是什么?"})
print("答案:", result["result"])
print("来源:", result["source_documents"][0].metadata.get('source'))
```

### 示例2：PDF技术文档助手

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def create_pdf_assistant(pdf_path: str):
    """创建PDF文档助手"""

    # 1. 加载PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # 添加页码到元数据
    for i, page in enumerate(pages):
        page.metadata['page_num'] = i + 1

    print(f"✅ 加载了{len(pages)}页PDF")

    # 2. 智能切割(保留章节)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", " ", ""]
    )
    chunks = splitter.split_documents(pages)

    # 3. 使用FAISS(高性能)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("pdf_index")

    # 4. 自定义Prompt
    prompt = PromptTemplate(
        template="""你是一个专业的技术文档助手。

请基于以下文档内容回答问题。引用相关段落。

文档内容:
{context}

问题: {question}

答案:""",
        input_variables=["context", "question"]
    )

    # 5. 创建QA链
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="mmr",  # 使用MMR获得多样化结果
            search_kwargs={"k": 3, "fetch_k": 10}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa

# 使用
qa = create_pdf_assistant("technical_paper.pdf")
result = qa.invoke({"query": "论文的主要贡献是什么?"})
```

---

## 🚀 学习路径与时间管理

### Day 8 (约3小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-10:00 | Document Loaders | `01_document_loaders.py` |
| 10:00-11:30 | 文本切割策略 | `02_text_splitting.py` |
| 11:30-12:00 | 实验chunk_size效果 | 自编写 |

### Day 9 (约2.5小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-10:30 | Chroma和FAISS对比 | `03_vector_stores.py` |
| 10:30-11:30 | 检索策略(Similarity/MMR) | 自编写 |

### Day 10 (约2.5小时)

| 时间 | 任务 | 文件 |
|------|------|------|
| 09:00-10:30 | 完整RAG应用 | `04_rag_application.py` |
| 10:30-11:30 | 优化和问题排查 | 自编写 |

---

## 💡 关键知识点总结

### 1. Document对象是基础

```python
doc = Document(
    page_content="内容",
    metadata={"source": "file.txt", ...}
)

# 关键：永远要添加metadata
# 特别是source字段，用于追踪和过滤
```

### 2. chunk_size选择的黄金法则

```python
# 根据任务类型选择
问答系统 → 200-500 (精准性)
阅读理解 → 500-1000 (平衡)
代码文档 → 1000-2000 (完整性)

# 确保overlap充分 (10-20%)
chunk_size = 500
overlap = 50-100  # ✅ 10-20%

# 测试不同参数，选择效果最好的
```

### 3. 向量库选择决策

```
开发/原型 → Chroma (零配置)
    ↓
生产/小规模(<10万文档) → FAISS
    ↓
大规模(>百万) → Milvus/Elasticsearch
    ↓
云服务 → Pinecone/Qwak
```

### 4. RAG的三个关键：

1. **检索质量**：好的chunk_size + 合适的Embedding模型
2. **Prompt设计**：明确指令 + 限制幻觉 + 要求引用来源
3. **后处理**：重排序 + 过滤 + 缓存

### 5. Embedding模型对比

| 模型 | 成本 | 质量 | 推荐场景 |
|------|------|------|---------|
| text-embedding-3-small | 低 | ⭐⭐⭐⭐ | 开发、一般场景 |
| text-embedding-3-large | 中 | ⭐⭐⭐⭐⭐ | 关键应用 |
| all-MiniLM-L6-v2 | 免费 | ⭐⭐⭐ | 离线开发 |

---

## 🎓 学习成果检查清单

完成Day 8-10学习后，你应该能够：

### 基础认知
- [ ] 说出常见的文档加载器及其用途
- [ ] 理解chunk_size对检索效果的影响
- [ ] 解释为什么需要overlap
- [ ] 对比Chroma和FAISS的优缺点

### 实践能力
- [ ] 使用DirectoryLoader批量加载文档
- [ ] 创建带丰富元数据的Document对象
- [ ] 使用RecursiveCharacterTextSplitter切割文本
- [ ] 创建Chroma或FAISS向量库
- [ ] 实现完整的RAG流程

### 进阶能力
- [ ] 使用不同检索策略(Similarity/MMR/Threshold)
- [ ] 自定义RAG的Prompt
- [ ] 基于元数据进行精准过滤
- [ ] 优化RAG系统(调整chunk_size, k值等)
- [ ] 排查常见问题(检索不到、幻觉等)

### 成果验证
- [ ] ✅ 运行`01_document_loaders.py`
- [ ] ✅ 运行`02_text_splitting.py`
- [ ] ✅ 运行`03_vector_stores.py`
- [ ] ✅ 运行`04_rag_application.py`
- [ ] ✅ 自己实现一个RAG应用(个人笔记或PDF)

---

## 📖 深入学习资源

### 官方文档
- [LangChain Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [Text Splitters详解](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [RAG教程](https://python.langchain.com/docs/use_cases/question_answering/)

### 推荐工具和资源
- [Chroma官方文档](https://docs.trychroma.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Embedding模型对比](https://huggingface.co/spaces/mteb/leaderboard)

---

## 🔗 与其他模块的关联

```
Day 1-2: 基础调用
    ↓
Day 3-4: 模型I/O
    ↓
Day 5-7: Prompt模板
    ↓
Day 8-10: 数据连接与向量化 (你在这里)
    ↓
Day 11-13: 内存系统 (加上对话历史)
    ↓
Day 14-16: Chains (组合多个Prompt+RAG)
    ↓
Day 17-19: Agents (自主选择使用哪个工具)
```

---

## 💪 老王的学习建议

> **数据是RAG的基础，garbage in garbage out！**

### ✅ 必做的三件事

1. **亲自调参** - 尝试不同的chunk_size (200, 500, 1000)，看对检索效果的影响
2. **对比检索策略** - 用同一个问题，分别试试Similarity、MMR、Threshold，对比结果
3. **构建完整应用** - 从加载→切割→向量化→检索→生成，一条龙走通

### ❌ 常见的坑

- ❌ 忽视chunk_size - 太大导致检索精度下降，太小导致丢失上下文
- ❌ 不测试检索效果 - 直接用默认参数，导致检索质量差
- ❌ 丢失元数据 - 用split_text()返回字符串，后来无法追踪来源
- ❌ 不优化Prompt - 让LLM随意编造答案，出现幻觉
- ❌ 用昂贵的Embedding - text-embedding-3-small已经够好，无需用large

### 💡 高效优化的顺序

1. **第一优化**：调整chunk_size和overlap
2. **第二优化**：换成更好的Embedding模型(如果cost允许)
3. **第三优化**：优化Prompt，加上限制条款
4. **第四优化**：尝试不同检索策略(如MMR)
5. **第五优化**：加入重排序、过滤等后处理

---

**准备好构建你的第一个RAG应用了吗？下一步是Day 11-13，学习如何给应用加上记忆！** 💪

---

*最后更新: 2025-01-09*
*学习时间: 约8小时（Day 8-10）*
