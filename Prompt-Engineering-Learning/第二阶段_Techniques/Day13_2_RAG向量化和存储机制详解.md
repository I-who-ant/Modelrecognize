# Day13_2 - RAG向量化和存储机制详解

## 核心理解

你的理解**完全正确**！RAG的向量化过程确实如此：

```
原始文档 → 切割分块 → Embedding编码 → 向量存储 → 索引优化 → 相似检索
```

就像 CherryStudio、Obsidian 插件、Logseq 等工具的知识库构建过程！

---

## 1. 向量化全过程详解

### 1.1 文档到向量的转换流程

#### 步骤1：文档切割
```python
# 原始文档示例
document = """
人工智能（AI）是计算机科学的一个分支，
它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

机器学习是人工智能的核心，是使计算机具有智能的根本途径。
深度学习则是机器学习研究中的一个新的领域，其动机在于建立、模拟人脑进行分析学习的神经网络。
"""

# 切割成块
chunks = [
    "人工智能（AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。",
    "机器学习是人工智能的核心，是使计算机具有智能的根本途径。",
    "深度学习则是机器学习研究中的一个新的领域，其动机在于建立、模拟人脑进行分析学习的神经网络。"
]
```

#### 步骤2：Embedding编码（关键！）
```python
"""
💡 核心理解：

Embedding Model = Transformer编码器 (通常是BERT/RoBERTa的Encoder部分)

工作原理：
1. 将文本标记化（tokenization）
2. 转换为词嵌入向量
3. 通过多层Transformer Encoder处理
4. 池化层提取固定维度向量（通常768, 1024, 2048等）

输出：每个文本块 → 对应的高维语义向量
"""

class EmbeddingProcess:
    def __init__(self):
        # 加载预训练的Embedding模型
        # 如：sentence-transformers, BGE, M3E等
        self.model = SentenceTransformer('shibing624/text2vec-base-chinese')

    def encode_document(self, text_chunks):
        """
        文档块 → 向量

        Args:
            text_chunks: 文本块列表

        Returns:
            向量列表
        """
        # 1. 批量编码
        vectors = self.model.encode(text_chunks)

        # 2. 归一化（可选，提升相似度计算效果）
        vectors = self.normalize(vectors)

        return vectors

    def normalize(self, vectors):
        """L2归一化"""
        import numpy as np
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / norms

# 实际演示
encoder = EmbeddingProcess()
chunk_vectors = encoder.encode_document(chunks)

print(f"文档块数量: {len(chunks)}")
print(f"每个向量维度: {chunk_vectors[0].shape}")  # 例如: (768,)
print(f"向量示例 (第1块): {chunk_vectors[0][:10]}...")  # 前10个维度
```

#### 步骤3：向量存储到数据库
```python
"""
💡 核心理解：

向量数据库 = 专门存储和检索高维向量的数据库

常见向量数据库：
- Chroma (轻量级，适合小规模)
- Pinecone (云服务，生产级)
- Weaviate (开源，可本地部署)
- Qdrant (Rust编写，高性能)
- FAISS (Facebook开发，可嵌入)

核心功能：
1. 存储向量 + 元数据
2. 快速相似度检索
3. 索引优化（HNSW, IVF等）
"""

class VectorStorage:
    def __init__(self):
        import chromadb  # 轻量级向量数据库
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
        )

    def store_vectors(self, chunks, vectors, metadatas=None):
        """
        存储向量到数据库

        Args:
            chunks: 文本内容
            vectors: 对应的向量
            metadatas: 元数据（来源、标题等）
        """
        # 生成唯一ID
        ids = [f"chunk_{i}" for i in range(len(chunks))]

        # 存储到向量数据库
        self.collection.add(
            embeddings=vectors,
            documents=chunks,
            metadatas=metadatas or [{}] * len(chunks),
            ids=ids
        )

        print(f"✅ 已存储 {len(chunks)} 个向量到知识库")

    def similarity_search(self, query_vector, top_k=5):
        """
        相似度检索

        Args:
            query_vector: 查询向量
            top_k: 返回最相似的k个结果

        Returns:
            相似文档列表
        """
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        return results

# 实际使用
storage = VectorStorage()
storage.store_vectors(chunks, chunk_vectors, metadatas=[
    {"source": "AI教程", "chunk_id": 0},
    {"source": "AI教程", "chunk_id": 1},
    {"source": "AI教程", "chunk_id": 2}
])

# 检索测试
query = "机器学习是什么？"
query_vector = encoder.encode_document([query])[0]
results = storage.similarity_search(query_vector, top_k=2)

print("\n🔍 检索结果:")
for i, (doc, score) in enumerate(zip(results['documents'][0], results['distances'][0])):
    print(f"  {i+1}. 相似度: {score:.4f}")
    print(f"     内容: {doc}")
    print()
```

### 1.2 向量化的核心：Embedding Model

#### Embedding Model的原理
```python
"""
💡 深度解析Embedding Model：

1. 基础结构：
   - Tokenizer: 将文本转换为token ID
   - Embedding Layer: 将token ID转换为向量
   - Transformer Encoder: 多层自注意力处理
   - Pooling Layer: 池化为固定维度向量

2. 训练目标（对比学习）：
   - 正样本对：语义相似的文本 → 距离近
   - 负样本对：语义不相似的文本 → 距离远
   - 损失函数：Triplet Loss, Contrastive Loss等

3. 代表模型：
   - BERT系列：bert-base, roberta-base
   - Sentence-BERT：专门优化的句子编码器
   - BGE：智源研究院开发，中文效果好
   - M3E：Moka开发，多语言支持
"""

class DeepEmbeddingExplained:
    def __init__(self):
        # 这里展示内部结构（简化版）
        self.tokenizer = None  # 文本分词器
        self.embedding_layer = None  # 词嵌入层
        self.transformer_layers = []  # 多层Transformer Encoder
        self.pooling_layer = None  # 池化层

    def encode_step_by_step(self, text):
        """
        逐步展示编码过程
        """
        # 步骤1：分词
        tokens = self.tokenizer.tokenize(text)
        print(f"1️⃣ 分词结果: {tokens}")

        # 步骤2：转换为ID
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        print(f"2️⃣ Token IDs: {token_ids}")

        # 步骤3：词嵌入
        token_embeddings = self.embedding_layer(token_ids)
        print(f"3️⃣ 词嵌入形状: {token_embeddings.shape}")

        # 步骤4：Transformer编码
        contextual_embeddings = self.transformer_layers(token_embeddings)
        print(f"4️⃣ 上下文嵌入形状: {contextual_embeddings.shape}")

        # 步骤5：池化
        sentence_embedding = self.pooling_layer(contextual_embeddings)
        print(f"5️⃣ 句子向量形状: {sentence_embedding.shape}")

        return sentence_embedding

# 使用真实模型演示
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('shibing624/text2vec-base-chinese')

# 查看模型信息
print(f"📊 模型信息:")
print(f"   名称: {model.get_sentence_embedding_dimension()}")
print(f"   最大序列长度: {model.max_seq_length}")

# 编码示例
texts = ["机器学习是AI的核心", "深度学习是机器学习的一种", "今天天气很好"]
embeddings = model.encode(texts)

print(f"\n📈 编码结果:")
print(f"   输入文本数: {len(texts)}")
print(f"   输出向量形状: {embeddings.shape}")
print(f"   每个向量维度: {embeddings.shape[1]}")

# 计算相似度
import numpy as np
similarity_matrix = np.dot(embeddings, embeddings.T)
print(f"\n🔗 相似度矩阵:")
print(similarity_matrix)
```

#### 向量相似度计算
```python
"""
💡 核心理解：

相似度度量方法：

1. 余弦相似度 (Cosine Similarity)：
   - 公式: cos(θ) = (A·B) / (|A||B|)
   - 范围: [-1, 1]，通常使用[0, 1]
   - 优点: 关注角度，不受向量长度影响
   - 用途: 语义相似度（最常用）

2. 欧几里得距离 (Euclidean Distance)：
   - 公式: √Σ(Ai-Bi)²
   - 特点: 考虑绝对距离
   - 用途: 几何空间距离

3. 点积 (Dot Product)：
   - 公式: A·B = Σ(Ai×Bi)
   - 特点: 简单快速
   - 用途: 快速相似度计算
"""

import numpy as np

def calculate_similarities():
    # 示例向量
    vec_a = embeddings[0]  # "机器学习是AI的核心"
    vec_b = embeddings[1]  # "深度学习是机器学习的一种"
    vec_c = embeddings[2]  # "今天天气很好"

    # 1. 余弦相似度
    cos_sim_ab = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    cos_sim_ac = np.dot(vec_a, vec_c) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_c))

    print("💫 余弦相似度:")
    print(f"   机器学习 vs 深度学习: {cos_sim_ab:.4f} (高度相关)")
    print(f"   机器学习 vs 天气: {cos_sim_ac:.4f} (几乎无关)")

    # 2. 欧几里得距离
    euclidean_ab = np.linalg.norm(vec_a - vec_b)
    euclidean_ac = np.linalg.norm(vec_a - vec_c)

    print(f"\n📏 欧几里得距离:")
    print(f"   机器学习 vs 深度学习: {euclidean_ab:.4f}")
    print(f"   机器学习 vs 天气: {euclidean_ac:.4f}")

    # 3. 点积
    dot_ab = np.dot(vec_a, vec_b)
    dot_ac = np.dot(vec_a, vec_c)

    print(f"\n⚡ 点积:")
    print(f"   机器学习 vs 深度学习: {dot_ab:.4f}")
    print(f"   机器学习 vs 天气: {dot_ac:.4f}")

calculate_similarities()
```

---

## 2. 向量数据库存储与索引

### 2.1 索引优化算法

#### HNSW算法（Hierarchical Navigable Small World）
```python
"""
💡 HNSW核心思想：

一种图索引算法，用于加速高维向量检索

结构：
- 多层图结构（0到L层）
- 上层节点少，下层节点多
- 每层都是一个小世界网络

检索过程：
1. 从顶层开始
2. 贪心搜索最近邻居
3. 逐层下探
4. 在底层找到最相似向量

优点：
- 构建后查询极快（毫秒级）
- 支持动态插入
- 内存效率高
"""

class HNSWSimplified:
    """HNSW简化实现"""
    def __init__(self, M=16, max_layer=6):
        self.M = M  # 每个节点的最大连接数
        self.max_layer = max_layer  # 最大层数
        self.levels = [[] for _ in range(max_layer)]  # 每层的节点
        self.vectors = []  # 存储向量数据
        self.node_id_counter = 0  # 节点ID计数器

    def build_index(self, vectors):
        """构建HNSW索引"""
        print(f"🏗️ 开始构建HNSW索引...")
        print(f"   数据量: {len(vectors)}")
        print(f"   向量维度: {vectors[0].shape}")

        for i, vector in enumerate(vectors):
            # 为每个向量分配随机层级（概率递减）
            level = self.get_random_level()
            node_id = self.node_id_counter
            self.node_id_counter += 1

            # 在每层添加节点
            for l in range(level + 1):
                self.levels[l].append({
                    'id': node_id,
                    'vector': vector,
                    'neighbors': []
                })

            if i % 100 == 0:
                print(f"   进度: {i}/{len(vectors)}")

        # 构建连接关系
        self.build_connections()

        print(f"✅ HNSW索引构建完成")
        for l in range(self.max_layer):
            print(f"   第{l}层: {len(self.levels[l])} 个节点")

    def get_random_level(self):
        """随机分配层级（概率为1/2^level）"""
        import random
        level = 0
        while random.random() < 0.5 and level < self.max_layer - 1:
            level += 1
        return level

    def build_connections(self):
        """构建节点连接关系"""
        for level in range(self.max_layer):
            for node in self.levels[level]:
                # 简化：每个节点连接到最近的M个邻居
                neighbors = self.find_nearest_neighbors(node['vector'], level, self.M)
                node['neighbors'] = [n['id'] for n in neighbors]

    def search(self, query_vector, k=5):
        """搜索最相似的k个向量"""
        # 1. 从最顶层开始
        current_level = self.max_layer - 1
        candidates = [self.levels[current_level][0]]  # 从第一个节点开始

        # 2. 逐层搜索
        for level in range(current_level, -1, -1):
            # 在当前层贪心搜索
            while True:
                found_better = False
                for neighbor_id in candidates[-1]['neighbors']:
                    neighbor = self.find_node_by_id(neighbor_id, level)
                    if neighbor and self.is_closer(neighbor['vector'], candidates[-1]['vector'], query_vector):
                        candidates.append(neighbor)
                        found_better = True
                        break

                if not found_better:
                    break

        # 3. 在底层找到最相似的k个
        candidates.sort(key=lambda n: self.distance(n['vector'], query_vector))
        return candidates[:k]

    def distance(self, vec_a, vec_b):
        """计算距离（使用余弦距离）"""
        return 1 - np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))

# 演示HNSW
hnsw = HNSWSimplified()
hnsw.build_index(chunk_vectors)

# 搜索示例
query_vec = encoder.encode_document(["机器学习"])[0]
results = hnsw.search(query_vec, k=2)

print(f"\n🔍 HNSW搜索结果:")
for i, result in enumerate(results):
    print(f"   {i+1}. 节点ID: {result['id']}")
    print(f"      距离: {result['distance']:.4f}")
```

#### IVF算法（Inverted File Index）
```python
"""
💡 IVF核心思想：

一种基于聚类的索引算法

原理：
1. 对所有向量进行聚类（如K-means）
2. 选择聚类中心作为倒排索引的"桶"
3. 每个向量归属到最近的聚类中心
4. 检索时先找到相关聚类，再在桶内搜索

优点：
- 减少搜索空间
- 适合大规模数据
- 可结合PQ进行压缩

流程：
预处理 → 聚类 → 构建索引 → 查询
"""

from sklearn.cluster import KMeans
import numpy as np

class IVFIndex:
    """IVF索引实现"""
    def __init__(self, n_clusters=100):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.cluster_centers = None
        self.cluster_assignments = {}
        self.vectors_by_cluster = {}

    def build_index(self, vectors):
        """构建IVF索引"""
        print(f"🏗️ 开始构建IVF索引...")
        print(f"   聚类数量: {self.n_clusters}")
        print(f"   数据量: {len(vectors)}")

        # 1. K-means聚类
        self.cluster_centers = self.kmeans.fit(vectors).cluster_centers_

        # 2. 分配向量到聚类
        cluster_labels = self.kmeans.predict(vectors)

        # 3. 按聚类组织向量
        for i, (vector, label) in enumerate(zip(vectors, cluster_labels)):
            if label not in self.vectors_by_cluster:
                self.vectors_by_cluster[label] = []
            self.vectors_by_cluster[label].append({
                'id': i,
                'vector': vector
            })

        print(f"✅ IVF索引构建完成")
        for cluster_id in range(self.n_clusters):
            size = len(self.vectors_by_cluster.get(cluster_id, []))
            print(f"   聚类 {cluster_id}: {size} 个向量")

    def search(self, query_vector, n_clusters_to_search=10, k=5):
        """搜索最相似的k个向量"""
        # 1. 找到最近的n个聚类中心
        distances_to_centers = []
        for i, center in enumerate(self.cluster_centers):
            dist = np.linalg.norm(query_vector - center)
            distances_to_centers.append((dist, i))

        distances_to_centers.sort()
        nearest_clusters = [cluster_id for _, cluster_id in distances_to_centers[:n_clusters_to_search]]

        # 2. 在选定的聚类中搜索
        all_candidates = []
        for cluster_id in nearest_clusters:
            candidates = self.vectors_by_cluster.get(cluster_id, [])
            for candidate in candidates:
                dist = np.linalg.norm(query_vector - candidate['vector'])
                all_candidates.append((dist, candidate))

        # 3. 返回最相似的k个
        all_candidates.sort(key=lambda x: x[0])
        return all_candidates[:k]

# 演示IVF
ivf = IVFIndex(n_clusters=10)
ivf.build_index(chunk_vectors)

# 搜索
results = ivf.search(query_vec, k=2)

print(f"\n🔍 IVF搜索结果:")
for i, (dist, candidate) in enumerate(results):
    print(f"   {i+1}. 聚类: {candidate['id']}")
    print(f"      距离: {dist:.4f}")
```

### 2.2 完整的RAG存储系统

```python
"""
💡 完整流程示例：

类似CherryStudio的知识库构建过程
"""

class RAGKnowledgeBase:
    """RAG知识库完整实现"""
    def __init__(self, embedding_model_name='shibing624/text2vec-base-chinese'):
        # 1. 加载Embedding模型
        from sentence_transformers import SentenceTransformer
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # 2. 初始化向量数据库
        import chromadb
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(
            name="my_knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )

        # 3. 文档处理器
        self.document_processor = DocumentProcessor()

        print(f"✅ RAG知识库初始化完成")
        print(f"   Embedding模型: {embedding_model_name}")
        print(f"   向量维度: {self.embedding_model.get_sentence_embedding_dimension()}")

    def add_documents(self, documents):
        """添加文档到知识库"""
        print(f"\n📚 开始处理 {len(documents)} 个文档...")

        all_chunks = []
        all_vectors = []
        all_metadatas = []
        all_ids = []

        for doc_idx, doc in enumerate(documents):
            print(f"\n处理文档 {doc_idx + 1}/{len(documents)}: {doc.get('title', 'Untitled')}")

            # 1. 文档分块
            chunks = self.document_processor.chunk_document(doc)

            # 2. 编码为向量
            if chunks:
                vectors = self.embedding_model.encode([chunk['content'] for chunk in chunks])

                # 3. 准备存储数据
                for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
                    chunk_id = f"{doc_idx}_{i}"
                    all_chunks.append(chunk['content'])
                    all_vectors.append(vector)
                    all_metadatas.append(chunk['metadata'])
                    all_ids.append(chunk_id)

        # 4. 批量存储到向量数据库
        if all_chunks:
            print(f"\n💾 存储到向量数据库...")
            self.collection.add(
                embeddings=all_vectors,
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )

            print(f"✅ 成功存储 {len(all_chunks)} 个文档块")
        else:
            print("⚠️ 没有可存储的内容")

    def query(self, question, top_k=5):
        """问答检索"""
        print(f"\n❓ 问题: {question}")

        # 1. 编码问题为向量
        query_vector = self.embedding_model.encode([question])[0]

        # 2. 检索相似文档
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        # 3. 返回结果
        retrieved_info = []
        for i in range(len(results['documents'][0])):
            retrieved_info.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })

        return retrieved_info

    def get_statistics(self):
        """获取知识库统计信息"""
        count = self.collection.count()
        return {
            'total_chunks': count,
            'embedding_dimension': self.embedding_model.get_sentence_embedding_dimension()
        }

class DocumentProcessor:
    """文档处理器"""
    def chunk_document(self, document, chunk_size=200, overlap=50):
        """将文档分块"""
        content = document.get('content', '')
        if not content:
            return []

        chunks = []
        start = 0

        while start < len(content):
            end = start + chunk_size
            chunk_content = content[start:end]

            # 寻找合适的断句位置
            if end < len(content):
                for separator in ['\n\n', '\n', '. ', '! ', '? ']:
                    separator_pos = chunk_content.rfind(separator)
                    if separator_pos != -1:
                        end = start + separator_pos + len(separator)
                        chunk_content = content[start:end]
                        break

            chunk = {
                'content': chunk_content.strip(),
                'metadata': {
                    'source': document.get('title', 'Unknown'),
                    'chunk_id': len(chunks)
                }
            }
            chunks.append(chunk)

            # 滑动窗口
            start = max(start + chunk_size - overlap, end)

        return chunks

# 实际演示
print("=" * 60)
print("🌟 RAG知识库完整演示")
print("=" * 60)

# 创建知识库
rag = RAGKnowledgeBase()

# 示例文档
documents = [
    {
        'title': 'AI基础教程',
        'content': '''
        人工智能（AI）是计算机科学的重要分支，旨在创造能够模拟、延伸和扩展人类智能的机器。

        机器学习是AI的核心技术之一，它使计算机能够从数据中学习，而无需明确编程。

        深度学习是机器学习的一个子领域，它使用多层神经网络来学习数据的复杂模式。

        自然语言处理（NLP）是AI的另一个重要分支，专注于计算机与人类语言的交互。
        '''
    },
    {
        'title': '向量数据库',
        'content': '''
        向量数据库是专门用于存储和检索高维向量的数据库系统。

        它广泛应用于推荐系统、图像搜索、自然语言处理等领域。

        主要的向量数据库包括Pinecone、Weaviate、Chroma和Qdrant等。

        向量数据库使用特殊的索引算法来加速相似性搜索，如HNSW和IVF。
        '''
    }
]

# 添加文档到知识库
rag.add_documents(documents)

# 查看统计信息
stats = rag.get_statistics()
print(f"\n📊 知识库统计:")
print(f"   总文档块数: {stats['total_chunks']}")
print(f"   向量维度: {stats['embedding_dimension']}")

# 问答测试
questions = [
    "什么是机器学习？",
    "向量数据库有什么作用？",
    "深度学习和机器学习的关系？"
]

for question in questions:
    results = rag.query(question)

    print(f"\n📖 检索到的相关内容:")
    for i, result in enumerate(results[:2]):  # 只显示前2个
        print(f"   {i+1}. 相似度: {1-result['distance']:.4f}")
        print(f"      内容: {result['content'][:100]}...")
        print(f"      来源: {result['metadata']['source']}")

print(f"\n🎉 演示完成！")
print("=" * 60)
```

---

## 3. 关键概念总结

### 3.1 核心流程图
```
📄 原始文档
   ↓
✂️ 智能分块 (按语义/长度)
   ↓
🧠 Embedding编码 (Transformer Encoder)
   ↓
📊 高维向量 (768/1024/2048维)
   ↓
💾 向量数据库 (Chroma/Pinecone/Weaviate)
   ↓
🔍 索引优化 (HNSW/IVF/PQ)
   ↓
❓ 用户查询
   ↓
🧮 查询向量化
   ↓
⚡ 相似度搜索 (余弦相似度)
   ↓
📋 返回最相关文档
```

### 3.2 关键参数
- **分块大小**: 200-1000字符
- **分块重叠**: 50-200字符
- **向量维度**: 384/768/1024/2048
- **检索数量**: top_k=5-10
- **相似度阈值**: 0.6-0.8

### 3.3 实际应用案例
- **CherryStudio**: 使用BGE模型 + ChromaDB
- **Obsidian插件**: 使用OpenAI Embeddings + 本地向量库
- **Logseq**: 使用多模型 + 动态切换
- **Notion AI**: 内部专有模型 + 云端向量数据库

---

## 4. 最佳实践建议

### 4.1 Embedding模型选择
```python
# 中文场景推荐
EMBEDDING_MODELS = {
    'BGE-base-zh': {
        'dimension': 768,
        'language': '中文',
        'strength': '通用效果好'
    },
    'M3E-base': {
        'dimension': 768,
        'language': '中英双语',
        'strength': '多语言支持'
    },
    'text2vec': {
        'dimension': 768,
        'language': '中文',
        'strength': '轻量级、快速'
    }
}
```

### 4.2 分块策略优化
```python
CHUNKING_STRATEGIES = {
    'fixed_size': {
        'chunk_size': 500,
        'overlap': 50,
        'use_case': '一般场景'
    },
    'semantic_aware': {
        'chunk_size': 800,
        'overlap': 100,
        'use_case': '专业文档'
    },
    'hierarchical': {
        'chunk_size': 1000,
        'overlap': 200,
        'use_case': '长文档'
    }
}
```

### 4.3 检索优化技巧
1. **查询扩展**: 使用同义词、相关词
2. **混合检索**: 稠密 + 稀疏检索
3. **重排序**: 交叉编码器二次排序
4. **多样性**: MMR算法避免重复

---

## 🎯 核心要点回顾

1. **向量化**: Embedding模型将文本转换为高维语义向量
2. **存储**: 向量数据库提供高效的相似度检索
3. **索引**: HNSW/IVF等算法优化检索速度
4. **检索**: 余弦相似度找到最相关文档
5. **应用**: 类似CherryStudio的知识库构建过程

**一句话总结**: RAG通过Embedding模型将文档编码为向量，存储在优化过的向量数据库中，实现高效的语义检索！