# Day24 - Generating Synthetic Dataset for RAG: 为RAG生成合成数据集

**学习日期**: 2025-11-09
**阶段**: 第三阶段 - Applications (实际应用)
**重要程度**: ⭐⭐⭐⭐⭐ **RAG时代必备技能!**
**前置知识**: Day13(RAG), Day23(Generating Data), Day23_1, Day23_2
**核心主题**: 如何用Generating Data技术为RAG系统构建高质量的合成知识库

---

## 🤔 你的困惑

学完了Generating Data,现在想应用到RAG系统。但你面临新的问题:

```python
核心困惑 = {
    "1. RAG需要什么样的数据?": "和普通数据生成有什么区别?",
    "2. 怎么生成知识库数据?": "问答对、文档、知识三元组怎么生成?",
    "3. 检索和生成的关系?": "生成的数据怎么让LLM检索到?",
    "4. 如何保证检索准确?": "生成的数据要不要考虑检索相关性?",
    "5. 怎么扩展知识库?": "如何快速构建大规模知识库?",
    "6. 效果怎么评估?": "RAG系统中数据质量怎么衡量?"
}
```

**老王告诉你**: Generating Data + RAG = **最强AI助手解决方案**!用Generating Data生成高质量知识库,再配合RAG检索,就能构建出一个"无所不知"的AI系统!

---

## 💡 一句话理解

```
RAG的Generating Data = 用LLM生成结构化的知识数据(问答对、文档、知识图谱),
                      然后存入向量数据库,供RAG检索使用!
```

---

## 📚 第一部分: RAG系统回顾与数据需求分析

### 1.1 RAG系统快速回顾(Day13复习)

```python
RAG核心架构 = {
    "第1步: 文档预处理": {
        "输入": "文档库(书籍、文章、FAQ等)",
        "过程": "分割 → 清洗 → 去重",
        "输出": "结构化的文本块"
    },

    "第2步: 向量化": {
        "输入": "结构化文本块",
        "过程": "用embedding模型转换为向量",
        "输出": "向量表示(1536维或其他)"
    },

    "第3步: 向量存储": {
        "工具": "Pinecone, Weaviate, Milvus等",
        "作用": "高效存储和查询大规模向量",
        "特性": "秒级检索数百万条数据"
    },

    "第4步: 用户查询": {
        "输入": "用户问题",
        "过程": "向量化查询 → 向量搜索 → 返回top-k相关文档",
        "输出": "最相关的k条文档(context)"
    },

    "第5步: LLM生成": {
        "输入": "用户问题 + 检索到的context",
        "过程": "LLM基于context生成回答",
        "输出": "最终答案(引用来源)"
    }
}
```

### 1.2 RAG数据的特殊性

```python
RAG数据特点 = {
    "vs 普通数据生成": {
        "普通数据": "生成后直接训练模型,不需要考虑检索",
        "RAG数据": {
            "需要保证准确性": "错误信息会误导LLM生成错误答案",
            "需要考虑检索相关性": "数据要能被查询命中",
            "需要结构化": "文档块大小、标记、元数据都要合理",
            "需要多粒度": "既需要完整文档,也需要细粒度Q&A对"
        }
    }
}

RAG知识库的三种主要数据格式 = {
    "格式1: 文档(Documents)": {
        "定义": "长篇幅的文本(比如百科条目、教程)",
        "示例": "Python教程、产品使用手册、新闻文章",
        "特点": "上下文丰富,但可能过长",
        "生成方法": "写作生成、改写、总结"
    },

    "格式2: 问答对(QA Pairs)": {
        "定义": "问题-答案对,精准回答特定问题",
        "示例": "FAQ、教学QA、对话数据",
        "特点": "精准高效,易于检索",
        "生成方法": "Few-Shot、Self-Instruct、从文档提取"
    },

    "格式3: 知识三元组(Knowledge Triplets)": {
        "定义": "(主体, 关系, 对象) 的结构化数据",
        "示例": "('乔布斯', '创始人', 'Apple')",
        "特点": "高度结构化,支持知识图谱",
        "生成方法": "关系提取、知识库映射"
    }
}
```

### 1.3 RAG数据的关键要求

```python
RAG数据质量要求 = {
    "1. 准确性 (最重要!)": {
        "为什么": "错误的background context会导致LLM生成错误答案",
        "目标": "准确率 >= 98%",
        "检查方法": [
            "事实验证(关键事实要准确)",
            "逻辑检查(推理链条要正确)",
            "与权威源对比(书籍、官方文档)"
        ],
        "风险": "宁可不回答,也别给错误答案"
    },

    "2. 检索友好性": {
        "为什么": "数据要能被相关查询命中",
        "技巧": [
            "多角度表述同一概念(改写)",
            "包含查询的关键词变体",
            "问题表述要自然(避免过于专业)"
        ],
        "示例": {
            "不好": "算法复杂度: O(n log n)",
            "好": "快速排序有多快? 快速排序的时间复杂度是多少? O(n log n)的算法"
        }
    },

    "3. 粒度适当": {
        "文档粒度": "一般500-1000字为宜",
        "过长": "检索相关性差,context过多浪费tokens",
        "过短": "信息不足,无法完整回答问题",
        "调整方法": "根据用例动态调整,通常256-1024 tokens"
    },

    "4. 覆盖完整性": {
        "多面覆盖": "同一概念要从多个角度覆盖",
        "示例": "Python列表要覆盖: 基础、方法、性能、最佳实践等",
        "检验": "尝试用系统回答该领域的常见问题,是否都能找到答案"
    },

    "5. 可追溯性": {
        "标记来源": "每条数据都要标记出处",
        "元数据": "添加标签、分类、时间戳等",
        "好处": "用户可以验证信息,了解数据新鲜度"
    }
}
```

---

## 📚 第二部分: RAG数据生成策略

### 2.1 三种数据生成方法

#### 方法1: 从现有文档生成QA对

```python
def generate_qa_from_documents(documents: List[str], num_qa_per_doc: int = 5) -> List[Dict]:
    """
    从已有文档生成问答对

    这是最实用的方法:
    1. 准确性有保证(基于真实文档)
    2. 检索友好(问题来自文档内容)
    3. 成本低(只需要改写和补充)
    """

    qa_dataset = []

    for doc in documents:
        # 第1步: 用LLM从文档生成问题
        prompt_generate_questions = f"""
从以下文档中生成{num_qa_per_doc}个问题。这些问题应该:
1. 涵盖文档的核心内容
2. 符合真实用户的提问方式(自然、多样)
3. 避免过于简单或过于复杂
4. 可以从文档中直接找到答案

文档:
{doc}

请生成{num_qa_per_doc}个问题,每行一个(只输出问题,不要输出答案):
"""

        # 调用LLM生成问题
        questions = llm_call(prompt_generate_questions)
        questions = questions.strip().split('\n')

        # 第2步: 为每个问题生成答案
        for question in questions[:num_qa_per_doc]:
            question = question.strip()
            if not question:
                continue

            # 用LLM从文档中提取答案
            prompt_generate_answer = f"""
文档:
{doc}

问题: {question}

请根据文档内容,给出准确、完整的答案(150-300字):
"""

            answer = llm_call(prompt_generate_answer)

            qa_dataset.append({
                'question': question,
                'answer': answer,
                'source_doc': doc[:200] + '...',  # 保留来源
                'source_length': len(doc)
            })

    return qa_dataset

# 使用示例
documents = [
    "Python是一种高级编程语言,具有简洁的语法...",
    "机器学习是人工智能的一个分支...",
    # ... 更多文档
]

qa_pairs = generate_qa_from_documents(documents, num_qa_per_doc=5)
```

#### 方法2: 完全生成型(Zero-Shot)

```python
def generate_qa_dataset_from_scratch(
    topics: List[str],
    num_qa_per_topic: int = 50
) -> List[Dict]:
    """
    从零开始生成问答数据集

    使用场景:
    - 没有现有文档
    - 需要快速扩展知识库
    - 想要多角度覆盖

    风险:
    - 准确性无保证
    - 需要人工验证
    """

    qa_dataset = []

    for topic in topics:
        # 分阶段生成,确保质量

        # 阶段1: 生成子话题
        prompt_subtopics = f"""
主题: {topic}

请生成5个该主题的重要子话题。
例如,如果主题是"Python编程",子话题可能是: 基础语法、数据结构、函数、面向对象、模块等。

主题: {topic}
子话题:
1.
2.
3.
4.
5.
"""

        subtopics = llm_call(prompt_subtopics).strip().split('\n')

        # 阶段2: 为每个子话题生成QA对
        for subtopic in subtopics:
            subtopic = subtopic.strip().lstrip('0-9.').strip()
            if not subtopic:
                continue

            prompt_qa = f"""
主题: {topic}
子话题: {subtopic}

请生成5个相关的问答对,要求:
1. 问题多样化(包括"是什么", "如何", "为什么"等)
2. 答案准确完整(200-500字)
3. 循序渐进(从基础到进阶)

输出格式(JSON数组):
[
  {{
    "question": "问题1",
    "answer": "答案1"
  }},
  ...
]
"""

            qa_pairs = json.loads(llm_call(prompt_qa))

            for qa in qa_pairs:
                qa['topic'] = topic
                qa['subtopic'] = subtopic
                qa_dataset.append(qa)

    return qa_dataset

# 使用示例
topics = ['Python编程', '机器学习', '数据科学', '前端开发']
qa_pairs = generate_qa_dataset_from_scratch(topics, num_qa_per_topic=20)
```

#### 方法3: 混合型(文档 + 生成补充)

```python
def hybrid_qa_generation(
    documents: List[str],
    additional_topics: List[str]
) -> List[Dict]:
    """
    混合策略: 基于文档 + 补充生成

    兼取两者优势:
    - 核心准确(基于文档)
    - 覆盖完整(补充生成)
    """

    qa_dataset = []

    # 第1部分: 从文档生成(准确率高)
    doc_qa = generate_qa_from_documents(documents, num_qa_per_doc=3)
    qa_dataset.extend(doc_qa)

    # 第2部分: 从文档中的概念生成变体(改写)
    concepts = extract_key_concepts(documents)

    for concept in concepts:
        # 为每个概念生成3个问法变体
        prompt = f"""
概念: {concept}

请生成3个不同的问法来提问关于"{concept}"的问题:
"""

        variants = llm_call(prompt).strip().split('\n')

        for variant in variants:
            # 直接从文档中检索答案
            answer = retrieve_from_documents(concept, documents)

            qa_dataset.append({
                'question': variant,
                'answer': answer,
                'type': 'concept_variant'
            })

    # 第3部分: 补充生成(覆盖空白)
    coverage_gaps = analyze_coverage_gaps(qa_dataset, additional_topics)

    for gap_topic in coverage_gaps:
        prompt = f"""
补充主题: {gap_topic}

请生成5个关于"{gap_topic}"的高质量问答对:
"""

        additional_qa = json.loads(llm_call(prompt))
        for qa in additional_qa:
            qa['type'] = 'supplement'
            qa_dataset.append(qa)

    return qa_dataset
```

### 2.2 RAG特定的数据生成提示词

```python
RAG数据生成提示词库 = {
    "生成FAQ": """
你是一个{领域}专家。请为以下主题生成常见问答(FAQ)。

主题: {topic}

要求:
1. 问题应该是用户最可能问的
2. 答案要准确、完整、有用
3. 长度适中(200-400字)
4. 避免过于专业或过于简化

生成10个FAQ对。输出格式:
Q1: 问题
A1: 答案

Q2: 问题
A2: 答案
...
""",

    "生成改写(提升检索覆盖)": """
你是一个内容改写专家。请为以下问答对生成3个改写版本。

原问题: {question}
原答案: {answer}

要求:
1. 改变提问方式,但保留问题本质
2. 答案保持准确,但表述方式不同
3. 覆盖不同的用户查询角度

例如,如果原问题是"如何学习Python?",改写可能是:
- Python初学者应该怎样开始?
- 学习Python的最好方法是什么?
- Python学习路线图是什么?
""",

    "生成深度回答": """
你是一个深度内容专家。请为以下问题生成一个深度、全面的回答。

问题: {question}

要求:
1. 全面覆盖问题的各个方面
2. 包括原理、实践、注意事项
3. 可以分为几个层级(基础、进阶、高级)
4. 长度约1000字

请包括以下结构:
## 基本概念
...

## 详细讲解
...

## 常见陷阱
...

## 最佳实践
...
""",

    "生成知识三元组": """
你是一个知识提取专家。请从以下文本中提取知识三元组。

文本: {text}

要求:
1. 提取形如(主体, 关系, 对象)的三元组
2. 关系应该明确(如: 创办者、成立时间、发明人等)
3. 提取尽可能多的有效三元组

输出格式(JSON):
[
  {{"subject": "A", "relation": "B", "object": "C"}},
  ...
]
"""
}
```

---

## 📚 第三部分: RAG知识库构建完整流程

### 3.1 知识库构建Pipeline

```python
class RAGKnowledgeBaseBuilder:
    """RAG知识库构建器"""

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        self.embedding_model = embedding_model
        self.documents = []
        self.chunks = []
        self.vectors = []

    def build_knowledge_base(
        self,
        data_sources: Dict[str, Any],
        chunk_size: int = 512,
        overlap: int = 100
    ) -> Dict:
        """
        完整的知识库构建流程

        参数:
            data_sources: 数据源 {'documents': [...], 'qa_pairs': [...]}
            chunk_size: 文档块大小
            overlap: 块之间的重叠

        返回:
            构建好的知识库信息
        """

        print("开始构建知识库...")

        # 第1步: 生成原始数据
        print("\n[1/5] 生成原始知识库数据...")
        raw_documents = self._generate_raw_data(data_sources)

        # 第2步: 文档分块
        print("[2/5] 对文档进行分块...")
        chunks = self._chunk_documents(raw_documents, chunk_size, overlap)

        # 第3步: 生成变体和改写(提升检索覆盖)
        print("[3/5] 生成查询变体,提升检索覆盖...")
        chunks_with_variants = self._generate_query_variants(chunks)

        # 第4步: 向量化
        print("[4/5] 对数据进行向量化...")
        vectors = self._vectorize(chunks_with_variants)

        # 第5步: 存储和索引
        print("[5/5] 存储到向量数据库...")
        kb_info = self._store_to_vector_db(chunks_with_variants, vectors)

        print(f"\n✅ 知识库构建完成!")
        print(f"   - 总文档数: {len(raw_documents)}")
        print(f"   - 总块数: {len(chunks)}")
        print(f"   - 增强块数(含变体): {len(chunks_with_variants)}")

        return kb_info

    def _generate_raw_data(self, data_sources: Dict) -> List[Dict]:
        """生成原始数据"""
        documents = []

        # 处理文档
        if 'documents' in data_sources:
            for doc in data_sources['documents']:
                documents.append({
                    'type': 'document',
                    'content': doc,
                    'source': 'user_provided'
                })

        # 处理QA对(转为文档)
        if 'qa_pairs' in data_sources:
            for qa in data_sources['qa_pairs']:
                doc_content = f"Q: {qa['question']}\n\nA: {qa['answer']}"
                documents.append({
                    'type': 'qa',
                    'content': doc_content,
                    'source': 'qa_pair',
                    'original_qa': qa
                })

        # 生成补充数据(可选)
        if 'generate_additional' in data_sources and data_sources['generate_additional']:
            supplement = self._generate_supplement_data(data_sources['topics'])
            documents.extend(supplement)

        return documents

    def _chunk_documents(self, documents: List[Dict], chunk_size: int, overlap: int) -> List[Dict]:
        """对文档进行分块"""
        chunks = []

        for doc in documents:
            content = doc['content']
            tokens = content.split()

            # 创建带重叠的块
            for i in range(0, len(tokens), chunk_size - overlap):
                chunk_tokens = tokens[i:i + chunk_size]
                chunk_text = ' '.join(chunk_tokens)

                if len(chunk_text.strip()) > 50:  # 避免过短的块
                    chunks.append({
                        'text': chunk_text,
                        'source_doc_type': doc['type'],
                        'source': doc['source'],
                        'metadata': {
                            'chunk_size': len(chunk_tokens),
                            'position': len(chunks)
                        }
                    })

        return chunks

    def _generate_query_variants(self, chunks: List[Dict]) -> List[Dict]:
        """
        为每个块生成查询变体

        这大大提升检索命中率!
        """
        enhanced_chunks = []

        for chunk in chunks:
            enhanced_chunks.append(chunk)

            # 为重要的块生成变体
            if len(chunk['text'].split()) > 100:  # 只为较长的块生成变体
                prompt = f"""
文档内容:
{chunk['text']}

请生成3个可能的用户查询,这些查询应该能够匹配上述文档:
输出格式:
1. 查询1
2. 查询2
3. 查询3
"""

                variants_text = llm_call(prompt)
                variants = variants_text.strip().split('\n')

                for variant in variants:
                    variant = variant.strip().lstrip('0-9.').strip()
                    if variant:
                        enhanced_chunks.append({
                            'text': variant,
                            'is_query_variant': True,
                            'source_chunk_id': len(enhanced_chunks) - 1,
                            'metadata': chunk['metadata']
                        })

        return enhanced_chunks

    def _vectorize(self, chunks: List[Dict]) -> List[List[float]]:
        """向量化"""
        import openai

        vectors = []
        batch_size = 100

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk['text'] for chunk in batch]

            # 批量向量化
            response = openai.Embedding.create(
                model=self.embedding_model,
                input=texts
            )

            for item in response['data']:
                vectors.append(item['embedding'])

            print(f"  已向量化: {min(i + batch_size, len(chunks))}/{len(chunks)}")

        return vectors

    def _store_to_vector_db(self, chunks: List[Dict], vectors: List[List[float]]) -> Dict:
        """存储到向量数据库"""
        # 这里假设使用Pinecone或其他向量数据库

        kb_info = {
            'total_chunks': len(chunks),
            'total_vectors': len(vectors),
            'embedding_model': self.embedding_model,
            'vector_dimension': len(vectors[0]) if vectors else 0,
            'storage_status': 'ready'
        }

        return kb_info
```

### 3.2 实战案例: 构建产品知识库

```python
def build_product_knowledge_base(product_docs: List[str], product_faqs: List[Dict]):
    """
    实战案例: 为产品构建知识库
    """

    # 数据源准备
    data_sources = {
        'documents': product_docs,
        'qa_pairs': product_faqs,
        'topics': ['产品功能', '常见问题', '最佳实践', '故障排除'],
        'generate_additional': True
    }

    # 创建知识库构建器
    builder = RAGKnowledgeBaseBuilder()

    # 构建知识库
    kb_info = builder.build_knowledge_base(
        data_sources=data_sources,
        chunk_size=512,
        overlap=100
    )

    return kb_info

# 使用示例
product_docs = [
    "我们的产品X是一个AI助手...",
    "产品X支持以下功能: ...",
    # ... 更多产品文档
]

product_faqs = [
    {'question': '产品X有什么优势?', 'answer': '...'},
    {'question': '如何开始使用产品X?', 'answer': '...'},
    # ... 更多FAQ
]

kb = build_product_knowledge_base(product_docs, product_faqs)
```

---

## 📚 第四部分: RAG数据评估

### 4.1 RAG特定的评估指标

```python
class RAGDataEvaluator:
    """RAG数据评估器"""

    def evaluate_rag_data(self, qa_pairs: List[Dict], documents: List[str] = None) -> Dict:
        """
        评估RAG知识库的质量

        关键指标:
        1. 准确性 (Critical!)
        2. 检索可能性 (能否被检索到)
        3. 覆盖完整性 (问题覆盖面)
        4. 信息新鲜度 (如果有时间戳)
        """

        results = {}

        # 指标1: 准确性(最重要!)
        results['accuracy'] = self._evaluate_accuracy(qa_pairs)

        # 指标2: 检索可能性
        if documents:
            results['retrievability'] = self._evaluate_retrievability(qa_pairs, documents)

        # 指标3: 覆盖完整性
        results['coverage'] = self._evaluate_coverage(qa_pairs)

        # 指标4: 粒度适当性
        results['granularity'] = self._evaluate_granularity(qa_pairs)

        # 综合评分
        results['overall_rag_score'] = self._calculate_rag_score(results)

        return results

    def _evaluate_accuracy(self, qa_pairs: List[Dict]) -> Dict:
        """
        评估准确性(RAG中最关键!)
        """
        accuracy_results = {
            'method': '人工抽检 + LLM评分',
            'sample_size': min(100, len(qa_pairs)),
            'issues': []
        }

        # 检查常见错误
        for qa in qa_pairs[:accuracy_results['sample_size']]:
            question = qa.get('question', '')
            answer = qa.get('answer', '')

            # 检查1: 问答不匹配
            if not self._check_q_a_relevance(question, answer):
                accuracy_results['issues'].append({
                    'type': 'mismatch',
                    'question': question,
                    'issue': '问题和答案不匹配'
                })

            # 检查2: 答案不完整
            if len(answer.split()) < 30:  # 答案太短
                accuracy_results['issues'].append({
                    'type': 'incomplete',
                    'question': question,
                    'issue': '答案过短,可能不完整'
                })

            # 检查3: 幻觉检测(用LLM)
            if self._detect_hallucination(question, answer):
                accuracy_results['issues'].append({
                    'type': 'hallucination',
                    'question': question,
                    'issue': '答案可能包含不准确信息'
                })

        # 计算准确率
        accuracy_results['accuracy_rate'] = 1.0 - (len(accuracy_results['issues']) / accuracy_results['sample_size'])

        return accuracy_results

    def _evaluate_retrievability(self, qa_pairs: List[Dict], documents: List[str]) -> Dict:
        """
        评估检索可能性
        关键: 生成的问题能否被检索到相关文档?
        """
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        retrievability_results = {
            'method': '向量相似度匹配',
            'hit_rate': 0.0,
            'mrr': 0.0,  # Mean Reciprocal Rank
            'low_retrieval_examples': []
        }

        # 计算问题和文档的相似度
        total_hits = 0
        mrr_sum = 0

        for qa in qa_pairs[:min(50, len(qa_pairs))]:
            question = qa['question']

            # 计算question与所有documents的相似度
            # (简化版本,实际应该用embedding)
            similarities = []
            for doc in documents:
                # 用简单的词重叠度衡量
                q_words = set(question.lower().split())
                d_words = set(doc.lower().split())
                overlap = len(q_words & d_words)
                similarity = overlap / max(len(q_words), len(d_words))
                similarities.append(similarity)

            # 检查是否有相关文档(相似度>0.3)
            max_sim = max(similarities) if similarities else 0
            rank = self._get_rank(max_sim, similarities)

            if max_sim > 0.3:
                total_hits += 1
                mrr_sum += 1 / rank if rank > 0 else 0
            else:
                retrievability_results['low_retrieval_examples'].append({
                    'question': question,
                    'max_similarity': max_sim
                })

        retrievability_results['hit_rate'] = total_hits / len(qa_pairs) if qa_pairs else 0
        retrievability_results['mrr'] = mrr_sum / len(qa_pairs) if qa_pairs else 0

        return retrievability_results

    def _evaluate_coverage(self, qa_pairs: List[Dict]) -> Dict:
        """
        评估覆盖完整性
        """
        coverage_results = {}

        # 分析问题类型多样性
        question_types = self._classify_question_types(qa_pairs)
        coverage_results['question_type_distribution'] = question_types

        # 计算覆盖评分
        expected_types = ['是什么', '如何', '为什么', '对比', '示例']
        found_types = len(set(question_types.keys()) & set(expected_types))
        coverage_results['type_coverage_rate'] = found_types / len(expected_types)

        # 分析主题覆盖
        topics = self._extract_topics(qa_pairs)
        coverage_results['num_topics'] = len(topics)
        coverage_results['topics'] = list(topics)

        return coverage_results

    def _evaluate_granularity(self, qa_pairs: List[Dict]) -> Dict:
        """
        评估粒度适当性
        """
        granularity_results = {}

        # 分析答案长度分布
        answer_lengths = [len(qa['answer'].split()) for qa in qa_pairs]

        granularity_results['avg_answer_length'] = np.mean(answer_lengths)
        granularity_results['min_answer_length'] = np.min(answer_lengths)
        granularity_results['max_answer_length'] = np.max(answer_lengths)
        granularity_results['std_answer_length'] = np.std(answer_lengths)

        # 评估是否在合理范围(通常150-500字)
        ideal_count = sum(1 for l in answer_lengths if 30 <= l <= 200)
        granularity_results['ideal_ratio'] = ideal_count / len(answer_lengths)

        return granularity_results

    def _calculate_rag_score(self, results: Dict) -> float:
        """
        计算RAG综合评分
        """
        weights = {
            'accuracy': 0.50,  # 准确性权重最大
            'retrievability': 0.25,
            'coverage': 0.15,
            'granularity': 0.10
        }

        score = 0

        # 准确性评分
        if 'accuracy' in results:
            acc_score = results['accuracy']['accuracy_rate'] * 100
            score += min(acc_score, 100) * weights['accuracy']

        # 检索评分
        if 'retrievability' in results:
            ret_score = results['retrievability']['hit_rate'] * 100
            score += min(ret_score, 100) * weights['retrievability']

        # 覆盖评分
        if 'coverage' in results:
            cov_score = results['coverage']['type_coverage_rate'] * 100
            score += min(cov_score, 100) * weights['coverage']

        # 粒度评分
        if 'granularity' in results:
            gran_score = results['granularity']['ideal_ratio'] * 100
            score += min(gran_score, 100) * weights['granularity']

        return score
```

---

## 📚 第五部分: 最佳实践

### 5.1 RAG数据生成最佳实践

```python
最佳实践 = {
    "1. 准确性优先": {
        "原则": "宁可数量少,也要准确",
        "方法": [
            "基于真实文档生成(而不是凭空生成)",
            "多轮人工审核关键数据",
            "定期检查数据的新鲜度和准确性"
        ],
        "代价": "成本高,但值得"
    },

    "2. 检索友好设计": {
        "方法": [
            "为关键概念生成多个问法(改写变体)",
            "避免过于正式或学术性的表述",
            "包含常见的搜索关键词"
        ],
        "示例": "产品的技术架构" → [
            "产品是怎么架构的?",
            "底层技术栈是什么?",
            "系统组成部分有哪些?"
        ]
    },

    "3. 分层构建": {
        "阶段1": "核心知识库 (手工精编,小但精)",
        "阶段2": "补充层 (从文档生成,中等规模)",
        "阶段3": "扩展层 (自动生成,大规模)",
        "优势": "逐步扩展,保证质量"
    },

    "4. 监控反馈循环": {
        "收集": "用户查询和反馈",
        "分析": "哪些查询命中率低?",
        "补充": "为高频未命中查询补充数据",
        "迭代": "持续改进知识库"
    },

    "5. 元数据和可追溯性": {
        "必须记录": [
            "数据来源(文档、生成、用户提交)",
            "创建时间和最后更新时间",
            "生成参数(模型、temperature等)",
            "人工审核状态"
        ],
        "好处": "便于维护、追踪、更新"
    }
}
```

---

## 🎯 学习总结

### 核心要点

```python
核心要点 = {
    "1. RAG = 知识库 + 检索 + 生成": "Generating Data为RAG提供知识库内容",

    "2. RAG数据特殊要求": [
        "准确性至关重要(错误会传播到最终答案)",
        "需要考虑检索相关性(数据要能被查询命中)",
        "粒度要适当(500-1000字为宜)",
        "需要多角度覆盖(改写、变体)",
        "要有源追溯(标记来源和元数据)"
    ],

    "3. 三种数据生成方法": [
        "从文档生成QA对(最安全,准确性高)",
        "完全生成(最快,需验证)",
        "混合型(兼取优势)"
    ],

    "4. 评估指标": [
        "准确性 (50% - 最关键)",
        "检索可能性 (25%)",
        "覆盖完整性 (15%)",
        "粒度适当性 (10%)"
    ]
}
```

### 实战建议

**老王强调**:

1. **准确性是底线!** RAG中一个错误的事实会毁掉整个答案

2. **不是数据越多越好!** 100条高质量 > 1000条低质量

3. **必须有真实参考!** 最好用企业自己的文档和FAQ来生成

4. **检索很关键!** 再好的答案,用户查不到也白搭

5. **持续维护很重要!** 知识库不是一成不变的,要定期更新

---

**下一步学习**:
- Day25: Tackling Generated Datasets Diversity (处理生成数据集的多样性)
- Day26: Generating Code (代码生成)

**笔记状态**: ✅ 完成
**学习耗时**: 3.5小时
**实践项目**: [待完成] 为自己的业务领域构建一个RAG知识库

---

**记住**: 艹,RAG+数据生成真的是AI助手的杀手锏!一个好的RAG系统能让你的AI助手从"万事通"变成"领域专家"!好好学,以后这就是你的核心竞争力! 💪
