# Day24_1 - RAG知识库构建快速指南: 从数据生成到向量存储

**创建日期**: 2025-11-09
**类型**: Day24精炼版
**难度**: ⭐⭐⭐ (快速上手版)
**核心目标**: 5分钟掌握RAG知识库的完整构建流程

---

## 🎯 RAG的本质

```
用户问题 → 检索相关文档 → LLM生成答案
         (向量搜索)    (基于context)
```

**核心**: 数据质量决定答案质量！

---

## 📚 RAG构建5步流程

### 第1步: 生成知识库数据

```python
# 选择数据格式 (三选一)
数据格式 = {
    "问答对(推荐)": {
        "例": {"Q": "Python是什么?", "A": "Python是编程语言..."},
        "优点": "精准、易检索",
        "生成方法": "Few-Shot提示词",
        "用处": "FAQ、智能客服"
    },

    "长文档": {
        "例": "完整的教程章节(500-1000字)",
        "优点": "上下文丰富",
        "生成方法": "改写、总结",
        "用处": "知识库、教材"
    },

    "知识三元组": {
        "例": ("乔布斯", "创始人", "Apple"),
        "优点": "结构化",
        "生成方法": "关系提取",
        "用处": "知识图谱、专家系统"
    }
}

# 生成提示词模板
生成提示 = """
主题: {topic}

请生成5个高质量的QA对,要求:
1. 问题自然多样
2. 答案准确完整(150-300字)
3. 覆盖该主题的核心内容

输出格式(JSON):
[
  {"question": "...", "answer": "..."},
  ...
]
"""
```

### 第2步: 数据清洗 + 分块

```python
def prepare_knowledge_base(raw_data):
    """
    准备知识库数据
    """

    # 清洗
    cleaned = remove_duplicates(raw_data)  # 去重
    cleaned = remove_noise(cleaned)         # 清洁
    cleaned = validate(cleaned)             # 验证准确性

    # 分块 (RAG的关键!)
    chunks = []
    for doc in cleaned:
        # 问答对型 → 直接用
        if 'question' in doc:
            chunks.append(doc)

        # 长文档型 → 分块
        else:
            for chunk in split_into_chunks(
                doc['text'],
                chunk_size=500,      # 500字
                overlap=100          # 100字重叠
            ):
                chunks.append({
                    'text': chunk,
                    'source': doc.get('source'),
                    'metadata': {...}
                })

    return chunks

# 分块规则
分块建议 = {
    "文档大小": "500-1000字为宜",
    "太长的问题": "上下文多,浪费tokens",
    "太短的块": "信息不足,无法回答完整",
    "重叠设置": "100字重叠,保留上下文连贯性"
}
```

### 第3步: 生成检索变体 (提升命中率!)

```python
def generate_query_variants(chunk):
    """
    为关键块生成多个查询变体

    场景: 同一内容,用户可能有多种问法
    目标: 提高被检索命中的概率
    """

    # 重要块才生成变体 (节省成本)
    if len(chunk) > 200:
        prompt = f"""
内容: {chunk}

请生成3个可能的用户查询:
1. 直接问法
2. 对比问法
3. 应用问法

输出格式:
1. 查询1
2. 查询2
3. 查询3
"""

        variants = llm_call(prompt)  # 生成

        # 存储: 原文档 + 3个变体都向量化
        return [chunk] + variants

# 最佳实践
最佳实践 = {
    "为什么要生成变体?": "同一内容,不同用户问法不同",
    "示例": {
        "原内容": "快速排序的时间复杂度是O(n log n)",
        "变体1": "快速排序有多快?",
        "变体2": "快速排序vs冒泡排序哪个快?",
        "变体3": "如何在实战中选择排序算法?"
    },
    "成本": "多存储3倍的向量,但命中率提升50%"
}
```

### 第4步: 向量化 + 存储

```python
def vectorize_and_store(chunks):
    """
    向量化所有chunks,存入向量数据库
    """

    # 向量化 (用embedding模型)
    embeddings = []

    for chunk in chunks:
        # 选一个embedding模型
        embedding = openai.Embedding.create(
            input=chunk['text'],
            model="text-embedding-3-small"  # 1536维
        )['data'][0]['embedding']

        embeddings.append(embedding)

    # 存入向量数据库
    vector_db.upsert(
        vectors=[
            {
                'id': i,
                'values': embedding,
                'metadata': {
                    'text': chunk['text'],
                    'source': chunk.get('source'),
                    'type': chunk.get('type', 'document')
                }
            }
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]
    )

# 常见向量数据库
向量数据库选择 = {
    "Pinecone": "云端,易用,适合快速上手",
    "Weaviate": "开源,功能完整,适合自建",
    "Milvus": "高性能,大规模,适合企业",
    "Faiss": "本地,速度快,适合离线",
    "Qdrant": "新兴,Rust写的,性能优异"
}
```

### 第5步: 查询 + 生成答案

```python
def rag_inference(user_question):
    """
    RAG推理流程
    """

    # Step1: 向量化用户问题
    question_embedding = openai.Embedding.create(
        input=user_question,
        model="text-embedding-3-small"
    )['data'][0]['embedding']

    # Step2: 向量搜索,返回top-k相关文档
    search_results = vector_db.query(
        question_embedding,
        top_k=3,  # 返回最相关的3个
        include_metadata=True
    )

    # 提取文本作为context
    context = "\n".join([
        result['metadata']['text']
        for result in search_results['matches']
    ])

    # Step3: LLM基于context生成答案
    prompt = f"""
背景知识:
{context}

用户问题: {user_question}

请根据背景知识回答用户问题。如果信息不足,说"我不确定"。
"""

    answer = llm_call(prompt)

    # Step4: 返回答案 + 来源
    return {
        'answer': answer,
        'sources': [r['metadata']['source'] for r in search_results['matches']],
        'confidence': search_results['matches'][0]['score']  # 相似度分数
    }

# 示例流程
用户输入 = "Python列表和元组有什么区别?"
     ↓
向量化问题
     ↓
搜索 → 找到3篇相关文档
     ↓
提取文本作为context
     ↓
LLM生成回答
     ↓
输出: "答案 + 来源"
```

---

## 🔥 核心要点总结

### RAG数据质量要求

```
优先级排序:
═════════════════════════════════════════

1️⃣  准确性 ⭐⭐⭐⭐⭐ (最关键!)
    └─ 错的信息 = 错的答案
    └─ 目标: ≥98%准确率

2️⃣  检索友好性 ⭐⭐⭐⭐
    └─ 数据要能被查询命中
    └─ 技巧: 多角度表述、关键词变体

3️⃣  粒度适当 ⭐⭐⭐
    └─ 500-1000字为宜
    └─ 太长浪费tokens,太短信息不足

4️⃣  覆盖完整 ⭐⭐⭐
    └─ 同一概念多方向覆盖
    └─ 改写、变体、补充

5️⃣  可追溯性 ⭐⭐
    └─ 标记来源和元数据
    └─ 用户可验证信息
```

### 数据生成的三种方式对比

```
方式1: 从现有文档生成 ⭐⭐⭐⭐⭐ (最推荐)
  ├─ 准确性: 高 (基于真实文档)
  ├─ 成本: 中
  └─ 方法: 从文档提问 → 生成QA对

方式2: 完全生成 ⭐⭐⭐
  ├─ 准确性: 中 (需验证)
  ├─ 成本: 低
  └─ 方法: 从零生成QA对

方式3: 混合生成 ⭐⭐⭐⭐
  ├─ 准确性: 高
  ├─ 成本: 中
  └─ 方法: 基础+补充生成
```

---

## 💻 完整代码示例

```python
import openai
from pinecone import Pinecone

class SimpleRAG:
    """简单的RAG系统"""

    def __init__(self, pinecone_key, openai_key):
        self.pc = Pinecone(api_key=pinecone_key)
        self.index = self.pc.Index("rag-index")
        openai.api_key = openai_key

    def build_knowledge_base(self, documents):
        """构建知识库"""

        # 1. 分块
        chunks = []
        for doc in documents:
            for chunk in self._split_text(doc, chunk_size=500):
                chunks.append(chunk)

        # 2. 向量化
        vectors = []
        for chunk in chunks:
            emb = openai.Embedding.create(
                input=chunk,
                model="text-embedding-3-small"
            )['data'][0]['embedding']
            vectors.append(emb)

        # 3. 存储
        self.index.upsert(vectors=[
            (str(i), vec, {"text": chunk})
            for i, (vec, chunk) in enumerate(zip(vectors, chunks))
        ])

        print(f"✅ 知识库构建完成! 共{len(chunks)}个chunks")

    def query(self, question):
        """查询和生成答案"""

        # 1. 向量化问题
        q_emb = openai.Embedding.create(
            input=question,
            model="text-embedding-3-small"
        )['data'][0]['embedding']

        # 2. 搜索
        results = self.index.query(q_emb, top_k=3)

        # 3. 提取context
        context = "\n".join([
            match['metadata']['text']
            for match in results['matches']
        ])

        # 4. LLM生成
        prompt = f"""背景: {context}\n\n问题: {question}\n\n答案:"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content']

    def _split_text(self, text, chunk_size=500):
        """文本分块"""
        words = text.split()
        for i in range(0, len(words), chunk_size - 100):
            yield " ".join(words[i:i+chunk_size])

# 使用示例
rag = SimpleRAG(pinecone_key="xxx", openai_key="xxx")

# 构建知识库
docs = [
    "Python是一种高级编程语言...",
    "机器学习是人工智能的分支..."
]
rag.build_knowledge_base(docs)

# 查询
answer = rag.query("Python有什么优点?")
print(answer)
```

---

## 🚀 实战建议

```python
从零开始的步骤 = {
    "第1天": "选择3-5个你了解的主题,写成文档",

    "第2天": "用Day24的方法生成QA对(100-500条)",

    "第3天": "清洗数据,处理错误和重复",

    "第4天": "为关键QA对生成变体(提升检索)",

    "第5天": "向量化+存入Pinecone或本地Faiss",

    "第6天": "测试查询效果,迭代改进",

    "第7天": "部署到应用或API"
}

常见问题FAQ = {
    "Q: 一定要用向量数据库吗?":
        "A: 小规模(<1000)可以用本地Faiss,\n" +
        "    大规模推荐Pinecone/Weaviate",

    "Q: embedding模型怎么选?":
        "A: OpenAI's text-embedding-3-small最稳定,\n" +
        "    或用开源的(all-MiniLM-L6-v2)",

    "Q: 多少数据才够?":
        "A: 50条高质量QA对 > 500条低质数据,\n" +
        "    建议从500-1000条开始测试",

    "Q: 怎么评估RAG效果?":
        "A: 用真实用户的问题测试,\n" +
        "    看是否检索到相关文档,\n" +
        "    检查答案是否正确"
}
```

---

## ⚡ 老王的快速总结

```
RAG = 检索 + 生成

核心三句话:
1. 数据质量 > 数据量 (宁少勿滥)
2. 准确性 >> 其他 (一个错误毁灭一切)
3. 多角度覆盖 = 好检索 (变体+改写)

最快上手:
- 用Pinecone (云端,3分钟接入)
- 生成100条QA对测试
- 看效果再迭代扩大

你会发现:
- 好的RAG > 微调小模型
- 数据生成 = 竞争力
```

---

**笔记状态**: ✅ Day24精炼版完成
**学习耗时**: 5分钟快速阅读
**动手时间**: 1天从零构建一个小型RAG系统

---

**下一步**: 如果想深入Day25学习如何处理数据多样性,确保RAG的高质量!💪
