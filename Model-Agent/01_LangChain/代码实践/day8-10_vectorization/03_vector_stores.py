"""
向量数据库对比完整示例

学习目标:
1. 掌握Chroma和FAISS的使用
2. 理解不同检索策略
3. 学会选择合适的向量库
"""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def demo_chroma_basic():
    """Chroma基础使用"""
    print("=" * 60)
    print("1. Chroma - 开发友好的向量库")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document

        # 准备文档
        docs = [
            Document(
                page_content="Python是一门简洁优雅的编程语言",
                metadata={"source": "doc1", "topic": "Python"}
            ),
            Document(
                page_content="JavaScript主要用于Web前端开发",
                metadata={"source": "doc2", "topic": "JavaScript"}
            ),
            Document(
                page_content="Rust是一门注重内存安全的系统编程语言",
                metadata={"source": "doc3", "topic": "Rust"}
            ),
            Document(
                page_content="TypeScript是JavaScript的超集",
                metadata={"source": "doc4", "topic": "TypeScript"}
            ),
        ]

        # 创建Chroma向量库
        print("\n正在创建Chroma向量库...")
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory="./chroma_db"  # 持久化目录
        )

        print("✅ 向量库创建成功!")

        # 相似度检索
        print("\n测试1: 相似度检索")
        query = "前端开发用什么语言?"
        results = vectorstore.similarity_search(query, k=2)

        for i, doc in enumerate(results):
            print(f"\n  结果 {i+1}:")
            print(f"    内容: {doc.page_content}")
            print(f"    来源: {doc.metadata['source']}")

        # 带分数的检索
        print("\n测试2: 带相似度分数的检索")
        results_with_scores = vectorstore.similarity_search_with_score(query, k=2)

        for i, (doc, score) in enumerate(results_with_scores):
            print(f"\n  结果 {i+1} (相似度: {score:.4f}):")
            print(f"    内容: {doc.page_content}")

        # 元数据过滤
        print("\n测试3: 基于元数据过滤")
        results = vectorstore.similarity_search(
            "编程语言",
            k=2,
            filter={"topic": "Python"}
        )

        print(f"  找到 {len(results)} 个Python相关结果")
        for doc in results:
            print(f"    - {doc.page_content}")

        print("\n✅ Chroma特点:")
        print("  - 安装简单,零配置")
        print("  - 支持持久化")
        print("  - 元数据过滤能力强")
        print("  - API友好")
        print("  - 适合开发和小型项目")

    except ImportError as e:
        print(f"\n⚠️ 依赖未安装: {e}")
        print("请运行: pip install chromadb")
    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_faiss_basic():
    """FAISS基础使用"""
    print("\n" + "=" * 60)
    print("2. FAISS - 高性能向量检索")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document

        # 准备文档
        docs = [
            Document(page_content="机器学习是人工智能的一个分支"),
            Document(page_content="深度学习是机器学习的子领域"),
            Document(page_content="神经网络是深度学习的基础"),
            Document(page_content="Transformer是NLP领域的重要架构"),
        ]

        # 创建FAISS索引
        print("\n正在创建FAISS索引...")
        vectorstore = FAISS.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        print("✅ FAISS索引创建成功!")

        # 相似度检索
        print("\n测试1: 相似度检索")
        query = "深度学习的基础是什么?"
        results = vectorstore.similarity_search(query, k=2)

        for i, doc in enumerate(results):
            print(f"\n  结果 {i+1}:")
            print(f"    {doc.page_content}")

        # 带分数的检索
        print("\n测试2: 带距离分数的检索")
        results_with_scores = vectorstore.similarity_search_with_score(query, k=2)

        for i, (doc, score) in enumerate(results_with_scores):
            print(f"\n  结果 {i+1} (距离: {score:.4f}):")
            print(f"    {doc.page_content}")

        # 保存和加载
        print("\n测试3: 保存和加载索引")
        save_path = "./faiss_index"
        vectorstore.save_local(save_path)
        print(f"  ✅ 索引已保存到: {save_path}")

        # 加载索引
        loaded_vectorstore = FAISS.load_local(
            save_path,
            OpenAIEmbeddings(model="text-embedding-3-small"),
            allow_dangerous_deserialization=True
        )
        print("  ✅ 索引加载成功")

        # 测试加载的索引
        results = loaded_vectorstore.similarity_search("机器学习", k=1)
        print(f"  测试查询结果: {results[0].page_content}")

        print("\n✅ FAISS特点:")
        print("  - 性能极高(Meta开源)")
        print("  - 支持GPU加速")
        print("  - 内存高效")
        print("  - 适合大规模检索")
        print("  - 元数据过滤能力较弱")

    except ImportError as e:
        print(f"\n⚠️ 依赖未安装: {e}")
        print("请运行: pip install faiss-cpu")
    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_retrieval_strategies():
    """不同检索策略对比"""
    print("\n" + "=" * 60)
    print("3. 检索策略对比")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document

        # 准备测试数据
        docs = [
            Document(page_content="Python是一门编程语言", metadata={"lang": "Python"}),
            Document(page_content="Python广泛用于数据科学", metadata={"lang": "Python"}),
            Document(page_content="Python简单易学", metadata={"lang": "Python"}),
            Document(page_content="JavaScript用于前端开发", metadata={"lang": "JavaScript"}),
            Document(page_content="Java是企业级开发的首选", metadata={"lang": "Java"}),
            Document(page_content="TypeScript是JavaScript的超集", metadata={"lang": "TypeScript"}),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        query = "适合数据分析的编程语言"

        # 策略1: 相似度检索(默认)
        print("\n策略1: Similarity Search (相似度检索)")
        retriever1 = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        results1 = retriever1.invoke(query)
        for i, doc in enumerate(results1):
            print(f"  {i+1}. {doc.page_content}")

        # 策略2: MMR(最大边际相关性)
        print("\n策略2: MMR (平衡相关性和多样性)")
        retriever2 = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "fetch_k": 10,       # 先取10个候选
                "lambda_mult": 0.5   # 多样性权重(0=最多样,1=最相关)
            }
        )
        results2 = retriever2.invoke(query)
        for i, doc in enumerate(results2):
            print(f"  {i+1}. {doc.page_content}")

        # 策略3: 相似度阈值
        print("\n策略3: Similarity Score Threshold (相似度阈值)")
        retriever3 = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "score_threshold": 0.5,  # 只返回相似度>0.5的
                "k": 3
            }
        )
        results3 = retriever3.invoke(query)
        print(f"  符合阈值的结果数: {len(results3)}")
        for i, doc in enumerate(results3):
            print(f"  {i+1}. {doc.page_content}")

        print("\n✅ 策略选择建议:")
        print("  - Similarity: 最常用,效果稳定")
        print("  - MMR: 需要多样性,避免重复")
        print("  - Threshold: 严格控制质量")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_incremental_update():
    """增量更新"""
    print("\n" + "=" * 60)
    print("4. 向量库增量更新")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document

        # 初始文档
        initial_docs = [
            Document(page_content="文档1", metadata={"id": "doc1"}),
            Document(page_content="文档2", metadata={"id": "doc2"}),
        ]

        vectorstore = Chroma.from_documents(
            documents=initial_docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        print(f"\n初始文档数: {vectorstore._collection.count()}")

        # 添加新文档
        print("\n添加新文档...")
        new_docs = [
            Document(page_content="文档3", metadata={"id": "doc3"}),
            Document(page_content="文档4", metadata={"id": "doc4"}),
        ]

        ids = vectorstore.add_documents(new_docs)
        print(f"  新增文档ID: {ids}")
        print(f"  当前文档数: {vectorstore._collection.count()}")

        # 删除文档
        print("\n删除文档...")
        vectorstore.delete(ids=[ids[0]])  # 删除第一个新增的
        print(f"  删除后文档数: {vectorstore._collection.count()}")

        print("\n✅ 增量更新场景:")
        print("  - 定时添加新文档")
        print("  - 删除过期内容")
        print("  - 更新文档内容")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_performance_comparison():
    """性能对比"""
    print("\n" + "=" * 60)
    print("5. Chroma vs FAISS 性能对比")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma, FAISS
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document
        import time

        # 准备测试数据(100个文档)
        docs = [
            Document(page_content=f"这是第{i}个文档,内容是关于技术主题{i%10}的描述")
            for i in range(100)
        ]

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # 测试Chroma
        print("\n测试Chroma:")
        start = time.time()
        chroma_store = Chroma.from_documents(documents=docs, embedding=embeddings)
        chroma_build_time = time.time() - start
        print(f"  构建时间: {chroma_build_time:.2f}秒")

        start = time.time()
        for _ in range(10):
            chroma_store.similarity_search("技术主题5", k=5)
        chroma_search_time = (time.time() - start) / 10
        print(f"  平均检索时间: {chroma_search_time:.4f}秒")

        # 测试FAISS
        print("\n测试FAISS:")
        start = time.time()
        faiss_store = FAISS.from_documents(documents=docs, embedding=embeddings)
        faiss_build_time = time.time() - start
        print(f"  构建时间: {faiss_build_time:.2f}秒")

        start = time.time()
        for _ in range(10):
            faiss_store.similarity_search("技术主题5", k=5)
        faiss_search_time = (time.time() - start) / 10
        print(f"  平均检索时间: {faiss_search_time:.4f}秒")

        # 对比总结
        print("\n性能对比:")
        print(f"  Chroma构建: {chroma_build_time:.2f}s | FAISS构建: {faiss_build_time:.2f}s")
        print(f"  Chroma检索: {chroma_search_time:.4f}s | FAISS检索: {faiss_search_time:.4f}s")

        print("\n⚠️ 注意: 这只是简单测试,实际性能取决于:")
        print("  - 文档数量")
        print("  - 向量维度")
        print("  - 硬件配置")
        print("  - 查询复杂度")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_vector_store_selection():
    """向量库选择指南"""
    print("\n" + "=" * 60)
    print("6. 向量库选择指南")
    print("=" * 60)

    print("""
📊 向量库对比表

┌─────────────┬──────────┬──────────┬────────────┬──────────────┐
│   数据库    │   类型   │   性能   │  易用性    │   适用场景   │
├─────────────┼──────────┼──────────┼────────────┼──────────────┤
│   Chroma    │  嵌入式  │    ★★★   │   ★★★★★   │  开发/小型   │
│   FAISS     │  嵌入式  │  ★★★★★  │   ★★★     │  高性能检索  │
│ Elasticsearch│ 服务器  │   ★★★★   │   ★★★     │  企业级应用  │
│   Milvus    │  服务器  │  ★★★★★  │   ★★      │  大规模生产  │
│  Pinecone   │ 云服务   │  ★★★★★  │  ★★★★★   │  云原生应用  │
│   Qdrant    │  服务器  │  ★★★★   │   ★★★     │  复杂查询    │
└─────────────┴──────────┴──────────┴────────────┴──────────────┘

🎯 选择建议

开发阶段:
✅ Chroma
   - 零配置,快速上手
   - 支持持久化
   - 元数据过滤强大

生产环境 - 小规模(<10万文档):
✅ FAISS
   - 高性能
   - 内存高效
   - 本地部署简单

生产环境 - 中规模(10万-百万):
✅ Elasticsearch
   - 成熟稳定
   - 全文+向量检索
   - 运维体系完善

生产环境 - 大规模(百万+):
✅ Milvus
   - 专业向量库
   - 分布式架构
   - 高并发支持

云原生应用:
✅ Pinecone
   - 完全托管
   - 自动扩展
   - 零运维

💡 决策流程

1. 是否是开发/原型阶段?
   是 → Chroma

2. 文档规模多大?
   < 10万 → FAISS
   10万-百万 → Elasticsearch
   > 百万 → Milvus

3. 是否需要云服务?
   是 → Pinecone

4. 是否需要混合检索(全文+向量)?
   是 → Elasticsearch

5. 是否需要复杂的元数据过滤?
   是 → Chroma/Qdrant

⚠️ 注意事项

1. 性能不是唯一考虑因素
2. 运维成本很重要
3. 团队技术栈匹配度
4. 社区活跃度和文档质量
5. 成本(云服务费用vs自建成本)
    """)


def demo_embedding_cache():
    """Embedding缓存优化"""
    print("\n" + "=" * 60)
    print("7. Embedding缓存优化")
    print("=" * 60)

    try:
        from langchain.embeddings import CacheBackedEmbeddings
        from langchain.storage import LocalFileStore
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain_core.documents import Document
        import time

        # 准备测试数据
        docs = [
            Document(page_content=f"文档{i}的内容")
            for i in range(20)
        ]

        # 不使用缓存
        print("\n测试1: 不使用缓存")
        embeddings_no_cache = OpenAIEmbeddings(model="text-embedding-3-small")

        start = time.time()
        FAISS.from_documents(docs, embeddings_no_cache)
        time_no_cache = time.time() - start
        print(f"  首次构建: {time_no_cache:.2f}秒")

        start = time.time()
        FAISS.from_documents(docs, embeddings_no_cache)
        time_no_cache_2 = time.time() - start
        print(f"  二次构建: {time_no_cache_2:.2f}秒 (重复计算)")

        # 使用缓存
        print("\n测试2: 使用缓存")
        store = LocalFileStore("./embedding_cache/")

        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
            underlying_embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            document_embedding_cache=store,
            namespace="test-embeddings"
        )

        start = time.time()
        FAISS.from_documents(docs, cached_embeddings)
        time_with_cache_1 = time.time() - start
        print(f"  首次构建: {time_with_cache_1:.2f}秒")

        start = time.time()
        FAISS.from_documents(docs, cached_embeddings)
        time_with_cache_2 = time.time() - start
        print(f"  二次构建: {time_with_cache_2:.2f}秒 (使用缓存)")

        print("\n✅ 缓存效果:")
        print(f"  加速比: {time_no_cache_2 / time_with_cache_2:.1f}x")
        print("\n  使用场景:")
        print("  - 开发调试(频繁重建)")
        print("  - 相同文档多次处理")
        print("  - 降低API调用成本")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


if __name__ == "__main__":
    print("🗄️ LangChain Vector Stores 完整示例\n")

    # 运行所有示例
    demo_chroma_basic()
    demo_faiss_basic()
    demo_retrieval_strategies()
    demo_incremental_update()
    demo_performance_comparison()
    demo_vector_store_selection()
    demo_embedding_cache()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 向量库核心功能:
   - 存储向量
   - 相似度检索
   - 元数据过滤

2. Chroma特点:
   ✅ 零配置,易用
   ✅ 支持持久化
   ✅ 强大的元数据过滤
   ✅ 适合开发和小型项目

3. FAISS特点:
   ✅ 性能极高
   ✅ 内存高效
   ✅ GPU加速支持
   ✅ 适合大规模检索

4. 检索策略:
   - Similarity: 最常用
   - MMR: 平衡相关性和多样性
   - Threshold: 质量控制

5. 选择建议:
   开发: Chroma
   小规模生产: FAISS
   中大规模: Elasticsearch/Milvus
   云原生: Pinecone

6. 性能优化:
   - 使用Embedding缓存
   - 批量处理
   - 选择合适的向量维度
   - 增量更新而非重建

7. 注意事项:
   ⚠️ FAISS元数据过滤能力弱
   ⚠️ Chroma性能不如FAISS
   ⚠️ 考虑运维成本
   ⚠️ 评估实际需求再选型

8. 下一步:
   向量库准备好后:
   → 实现完整RAG流程
   → 优化检索效果
   → 生产环境部署
    """)