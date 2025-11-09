"""
RAG(检索增强生成)完整应用示例

学习目标:
1. 掌握完整的RAG流程
2. 学会多种检索优化技巧
3. 理解RAG效果评估和优化
"""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def demo_basic_rag():
    """基础RAG流程"""
    print("=" * 60)
    print("1. 基础RAG流程 - 从加载到问答")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.chains import RetrievalQA

        # 步骤1: 准备示例数据
        data_dir = Path("rag_data")
        data_dir.mkdir(exist_ok=True)

        sample_file = data_dir / "langchain_intro.txt"
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write("""LangChain是一个用于开发大语言模型应用的框架。

核心组件包括:
1. 模型I/O: 封装了与语言模型的交互,包括Chat Models和LLMs
2. 数据连接: 提供文档加载器、文本切割器和向量存储
3. 链(Chains): 组合多个组件形成完整的工作流
4. 代理(Agents): 使LLM能够使用工具并做出决策
5. 内存(Memory): 在对话中保持上下文

LangChain支持多种LLM提供商,包括OpenAI、Anthropic、HuggingFace等。

使用LangChain可以快速构建问答系统、聊天机器人、文档分析工具等应用。""")

        print("步骤1: 加载文档")
        loader = TextLoader(str(sample_file), encoding='utf-8')
        docs = loader.load()
        print(f"  ✅ 加载了 {len(docs)} 个文档")

        print("\n步骤2: 切割文本")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20
        )
        splits = text_splitter.split_documents(docs)
        print(f"  ✅ 切割为 {len(splits)} 个块")

        print("\n步骤3: 创建向量库")
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )
        print("  ✅ 向量库创建成功")

        print("\n步骤4: 创建检索器")
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 2}  # 检索Top-2
        )
        print("  ✅ 检索器就绪")

        print("\n步骤5: 创建QA链")
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            retriever=retriever,
            return_source_documents=True
        )
        print("  ✅ QA链创建成功")

        print("\n步骤6: 测试问答")
        questions = [
            "LangChain有哪些核心组件?",
            "LangChain支持哪些LLM提供商?",
            "可以用LangChain构建什么应用?"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n问题{i}: {question}")
            result = qa_chain.invoke({"query": question})

            print(f"回答: {result['result']}")

            print(f"\n来源文档 ({len(result['source_documents'])}个):")
            for j, doc in enumerate(result['source_documents'], 1):
                print(f"  {j}. {doc.page_content[:100]}...")

        print("\n✅ 基础RAG流程完成!")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_custom_prompt_rag():
    """自定义Prompt的RAG"""
    print("\n" + "=" * 60)
    print("2. 自定义Prompt - 控制输出格式")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.chains import RetrievalQA
        from langchain_core.prompts import PromptTemplate
        from langchain_core.documents import Document

        # 准备数据
        docs = [
            Document(page_content="Python是一门简洁优雅的编程语言"),
            Document(page_content="Python广泛应用于数据科学和机器学习"),
            Document(page_content="Python有丰富的第三方库生态"),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        # 自定义Prompt模板
        custom_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""基于以下上下文信息回答问题。

要求:
1. 只使用提供的上下文信息
2. 如果上下文中没有相关信息,明确说明"根据提供的信息无法回答"
3. 回答要简洁明了,不超过3句话

上下文:
{context}

问题: {question}

回答:"""
        )

        # 创建自定义QA链
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            retriever=vectorstore.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_prompt}
        )

        print("\n测试自定义Prompt:")
        questions = [
            "Python有什么特点?",
            "Java和Python哪个更好?"  # 故意问上下文中没有的
        ]

        for question in questions:
            print(f"\n问题: {question}")
            result = qa_chain.invoke({"query": question})
            print(f"回答: {result['result']}")

        print("\n✅ 自定义Prompt的作用:")
        print("  - 控制输出格式")
        print("  - 限制回答范围")
        print("  - 添加特定要求")
        print("  - 减少幻觉(Hallucination)")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_mmr_retrieval():
    """MMR检索优化"""
    print("\n" + "=" * 60)
    print("3. MMR检索 - 平衡相关性和多样性")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain_core.documents import Document

        # 准备有重复内容的数据
        docs = [
            Document(page_content="Python简单易学"),
            Document(page_content="Python语法简洁"),
            Document(page_content="Python易于上手"),
            Document(page_content="Python性能较慢"),
            Document(page_content="Python有GIL限制"),
            Document(page_content="JavaScript用于Web开发"),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        query = "Python的特点"

        print("\n普通相似度检索(可能重复):")
        retriever_similarity = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        results_sim = retriever_similarity.invoke(query)
        for i, doc in enumerate(results_sim, 1):
            print(f"  {i}. {doc.page_content}")

        print("\nMMR检索(更多样化):")
        retriever_mmr = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 3,
                "fetch_k": 6,        # 先取6个候选
                "lambda_mult": 0.5   # 平衡参数
            }
        )
        results_mmr = retriever_mmr.invoke(query)
        for i, doc in enumerate(results_mmr, 1):
            print(f"  {i}. {doc.page_content}")

        print("\n✅ MMR参数说明:")
        print("  fetch_k: 初始候选数量")
        print("  lambda_mult: 0=最多样, 1=最相关")
        print("  k: 最终返回数量")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_metadata_filtering():
    """基于元数据的精准检索"""
    print("\n" + "=" * 60)
    print("4. 元数据过滤 - 精准检索")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.chains import RetrievalQA
        from langchain_core.documents import Document

        # 准备带丰富元数据的文档
        docs = [
            Document(
                page_content="Python 3.12发布了新的JIT编译器",
                metadata={"language": "Python", "version": "3.12", "type": "release"}
            ),
            Document(
                page_content="Python 3.11提升了性能",
                metadata={"language": "Python", "version": "3.11", "type": "performance"}
            ),
            Document(
                page_content="JavaScript ES2024新增了装饰器",
                metadata={"language": "JavaScript", "version": "ES2024", "type": "feature"}
            ),
            Document(
                page_content="TypeScript 5.0改进了类型推导",
                metadata={"language": "TypeScript", "version": "5.0", "type": "feature"}
            ),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        print("\n场景1: 只检索Python相关")
        results = vectorstore.similarity_search(
            "新特性",
            k=2,
            filter={"language": "Python"}
        )
        for doc in results:
            print(f"  - {doc.page_content}")

        print("\n场景2: 只检索性能相关")
        results = vectorstore.similarity_search(
            "改进",
            k=2,
            filter={"type": "performance"}
        )
        for doc in results:
            print(f"  - {doc.page_content}")

        print("\n场景3: Python 3.12相关")
        results = vectorstore.similarity_search(
            "更新",
            k=2,
            filter={"language": "Python", "version": "3.12"}
        )
        for doc in results:
            print(f"  - {doc.page_content}")

        print("\n✅ 元数据过滤优势:")
        print("  - 精准控制检索范围")
        print("  - 多维度筛选")
        print("  - 提高检索相关性")
        print("  - 支持时间/类别/来源等过滤")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_contextual_compression():
    """上下文压缩(重排序)"""
    print("\n" + "=" * 60)
    print("5. 上下文压缩 - 提取最相关部分")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.retrievers import ContextualCompressionRetriever
        from langchain.retrievers.document_compressors import LLMChainExtractor
        from langchain_core.documents import Document

        # 准备包含噪声的文档
        docs = [
            Document(
                page_content="""LangChain是一个框架,用于开发LLM应用。
它诞生于2022年,由Harrison Chase创建。
核心功能包括模型I/O、数据连接和链式调用。
LangChain支持Python和JavaScript两种语言。
目前已被广泛应用于企业级应用开发中。"""
            ),
            Document(
                page_content="""在使用LangChain时,需要注意API密钥的安全。
框架提供了丰富的文档加载器,支持PDF、CSV、Markdown等格式。
社区非常活跃,GitHub上有超过50k星标。
定期更新和维护,每周都有新功能发布。"""
            ),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        base_retriever = vectorstore.as_retriever()

        # 创建压缩器
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        compressor = LLMChainExtractor.from_llm(llm)

        # 创建压缩检索器
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

        query = "LangChain的核心功能有哪些?"

        print(f"\n问题: {query}")

        print("\n普通检索结果(有噪声):")
        normal_results = base_retriever.invoke(query)
        for i, doc in enumerate(normal_results, 1):
            print(f"\n文档{i}:")
            print(f"{doc.page_content}")

        print("\n压缩检索结果(只保留相关部分):")
        compressed_results = compression_retriever.invoke(query)
        for i, doc in enumerate(compressed_results, 1):
            print(f"\n文档{i}:")
            print(f"{doc.page_content}")

        print("\n✅ 上下文压缩优势:")
        print("  - 减少无关内容")
        print("  - 降低Token消耗")
        print("  - 提高回答质量")
        print("  - 聚焦核心信息")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_multi_query_retrieval():
    """多查询检索"""
    print("\n" + "=" * 60)
    print("6. 多查询检索 - 改写问题提高召回")
    print("=" * 60)

    try:
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.retrievers.multi_query import MultiQueryRetriever
        from langchain_core.documents import Document

        # 准备数据
        docs = [
            Document(page_content="机器学习是人工智能的一个分支"),
            Document(page_content="深度学习是机器学习的子领域"),
            Document(page_content="神经网络是深度学习的基础架构"),
            Document(page_content="卷积神经网络适用于图像处理"),
        ]

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        # 创建多查询检索器
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        retriever = MultiQueryRetriever.from_llm(
            retriever=vectorstore.as_retriever(),
            llm=llm
        )

        query = "深度学习的基础是什么?"

        print(f"\n原始问题: {query}")
        print("\nMultiQueryRetriever会自动生成多个相关查询:")
        print("(查看日志可看到生成的查询)")

        results = retriever.invoke(query)

        print(f"\n检索到 {len(results)} 个相关文档:")
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc.page_content}")

        print("\n✅ 多查询检索优势:")
        print("  - 自动改写问题")
        print("  - 提高召回率")
        print("  - 从不同角度检索")
        print("  - 减少单一查询的局限性")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_rag_evaluation():
    """RAG效果评估"""
    print("\n" + "=" * 60)
    print("7. RAG效果评估和优化")
    print("=" * 60)

    print("""
📊 RAG效果评估维度

1. 检索质量(Retrieval Quality):
   - 相关性(Relevance): 检索到的文档是否相关
   - 覆盖率(Coverage): 是否涵盖了问题的所有方面
   - 排序质量(Ranking): Top-K是否是最相关的

   评估方法:
   ✅ 人工标注相关性
   ✅ 计算Precision@K和Recall@K
   ✅ 使用MRR(Mean Reciprocal Rank)

2. 生成质量(Generation Quality):
   - 准确性(Accuracy): 答案是否正确
   - 忠实度(Faithfulness): 是否基于检索到的上下文
   - 完整性(Completeness): 是否回答了完整问题

   评估方法:
   ✅ 人工评分
   ✅ 使用LLM作为评判器
   ✅ 对比参考答案

3. 端到端质量:
   - 问答准确率
   - 用户满意度
   - 响应时间

🔧 常见问题和优化

问题1: 检索不到相关文档
原因:
- chunk_size太大或太小
- Embedding模型不适合
- 查询表述不清晰

优化:
✅ 调整chunk_size(尝试200/500/1000)
✅ 尝试不同Embedding模型
✅ 使用MultiQueryRetriever改写查询
✅ 添加Query Expansion

问题2: 检索到的文档相关但答案不对
原因:
- Prompt设计不好
- LLM理解有误
- 上下文太长/太杂

优化:
✅ 优化Prompt模板
✅ 使用ContextualCompressionRetriever
✅ 增加Few-Shot示例
✅ 调整k值(检索数量)

问题3: 答案有幻觉(Hallucination)
原因:
- LLM自行编造
- 上下文不足

优化:
✅ Prompt中明确要求"只基于上下文"
✅ 降低temperature
✅ 使用RetrievalQA而非普通Chain
✅ 添加来源引用要求

问题4: 性能太慢
原因:
- 向量库查询慢
- Embedding计算耗时
- LLM响应慢

优化:
✅ 使用FAISS替代Chroma
✅ 缓存Embedding
✅ 批量处理
✅ 使用更快的LLM模型

问题5: 成本太高
原因:
- Token消耗大
- API调用频繁

优化:
✅ 减小chunk_size
✅ 降低k值
✅ 使用缓存
✅ 选择更便宜的模型

💡 优化流程

1. 建立评估基准
   - 准备测试问题集
   - 标注参考答案
   - 设定评估指标

2. 逐步优化
   步骤1: 优化文本切割
      → 实验不同chunk_size
      → 调整overlap

   步骤2: 优化检索
      → 尝试不同检索策略(Similarity/MMR)
      → 调整k值
      → 添加元数据过滤

   步骤3: 优化生成
      → 优化Prompt模板
      → 调整LLM参数
      → 添加上下文压缩

   步骤4: 端到端优化
      → 监控性能
      → 收集用户反馈
      → 持续迭代

3. A/B测试
   - 对比不同配置
   - 基于真实用户反馈
   - 数据驱动决策

📈 最佳实践

1. 数据准备:
   ✅ 高质量的源文档
   ✅ 丰富的元数据
   ✅ 合理的切割策略

2. 检索优化:
   ✅ 实验调优参数
   ✅ 使用混合检索
   ✅ 添加重排序

3. 生成优化:
   ✅ 清晰的Prompt
   ✅ 合适的temperature
   ✅ Few-Shot示例

4. 监控和迭代:
   ✅ 记录日志
   ✅ 收集反馈
   ✅ 持续优化
    """)


if __name__ == "__main__":
    print("🤖 LangChain RAG 完整应用示例\n")

    # 运行所有示例
    demo_basic_rag()
    demo_custom_prompt_rag()
    demo_mmr_retrieval()
    demo_metadata_filtering()
    demo_contextual_compression()
    demo_multi_query_retrieval()
    demo_rag_evaluation()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. RAG核心流程:
   加载 → 切割 → 向量化 → 检索 → 生成

2. 基础RAG:
   - RetrievalQA.from_chain_type
   - 指定retriever和llm
   - 返回答案和来源

3. 检索优化:
   ✅ MMR: 平衡相关性和多样性
   ✅ 元数据过滤: 精准控制范围
   ✅ 上下文压缩: 减少噪声
   ✅ 多查询: 改写问题提高召回

4. Prompt优化:
   - 自定义Prompt模板
   - 明确输出要求
   - 限制回答范围
   - 减少幻觉

5. 效果评估:
   - 检索质量(相关性/覆盖率)
   - 生成质量(准确性/忠实度)
   - 端到端质量(满意度/性能)

6. 常见问题解决:
   检索不到 → 调chunk_size/改写查询
   答案不对 → 优化Prompt/压缩上下文
   有幻觉 → 限制回答范围/降低temperature
   太慢 → 换向量库/缓存/批处理
   太贵 → 减小chunk/降低k/换模型

7. 最佳实践:
   ✅ 高质量数据 + 丰富元数据
   ✅ 合理切割 + 充分overlap
   ✅ 实验调优 + 混合检索
   ✅ 清晰Prompt + 合适参数
   ✅ 持续监控 + 迭代优化

8. 进阶技巧:
   - 混合检索(向量+关键词)
   - 重排序(Re-ranking)
   - Query扩展
   - 分层检索
   - 缓存优化

🎯 下一步学习:
   → Memory系统(对话上下文)
   → LCEL和Chains(复杂工作流)
   → Agents(工具调用和决策)
    """)