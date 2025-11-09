"""
Memory实战应用 - 对话式RAG、向量检索Memory和企业级实践

学习目标:
1. 掌握Memory与RAG的结合
2. 理解VectorStoreRetrieverMemory的使用
3. 学会实现对话式知识问答
4. 掌握企业级Memory管理
"""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def demo_conversational_rag():
    """Memory + RAG = 对话式知识问答"""
    print("=" * 60)
    print("1. 对话式RAG - Memory + 检索增强")
    print("=" * 60)

    try:
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain_core.documents import Document

        # 准备知识库
        docs = [
            Document(page_content="LangChain是一个用于开发LLM应用的框架"),
            Document(page_content="LangChain支持多种Memory类型,包括Buffer、Window、Summary等"),
            Document(page_content="ConversationBufferMemory保存完整对话历史"),
            Document(page_content="ConversationSummaryMemory将对话压缩成摘要"),
        ]

        # 创建向量库
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        # 创建Memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True  # 重要: 对话式RAG需要消息列表
        )

        # 创建对话式RAG链
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
            retriever=vectorstore.as_retriever(),
            memory=memory
        )

        print("\n对话式知识问答:")

        # 第1轮
        response1 = qa_chain.invoke({"question": "什么是LangChain?"})
        print(f"\n用户: 什么是LangChain?")
        print(f"AI: {response1['answer']}")

        # 第2轮(使用代词"它")
        response2 = qa_chain.invoke({"question": "它支持哪些Memory类型?"})
        print(f"\n用户: 它支持哪些Memory类型?")
        print(f"AI: {response2['answer']}")

        # 第3轮(继续使用代词)
        response3 = qa_chain.invoke({"question": "ConversationBufferMemory是做什么的?"})
        print(f"\n用户: ConversationBufferMemory是做什么的?")
        print(f"AI: {response3['answer']}")

        print("\n✅ Memory让RAG具备了上下文理解能力!")
        print("  - 可以使用代词引用之前的内容")
        print("  - 可以追问和深入讨论")
        print("  - 可以跨轮次理解问题")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_vector_store_backed_memory():
    """VectorStoreRetrieverMemory - 语义检索记忆"""
    print("\n" + "=" * 60)
    print("2. VectorStoreRetrieverMemory - 语义检索记忆")
    print("=" * 60)

    try:
        from langchain.memory import VectorStoreRetrieverMemory
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        from langchain.chains import ConversationChain
        from langchain_openai import ChatOpenAI

        # 创建向量库
        vectorstore = Chroma(
            collection_name="conversation_memory",
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
        )

        # 创建向量检索Memory
        memory = VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
        )

        print("\n添加记忆:")

        # 添加多条记忆
        memories = [
            ("我最喜欢的颜色是蓝色", "了解,你喜欢蓝色"),
            ("我的生日是5月1日", "记住了,5月1日是你的生日"),
            ("我住在上海", "好的,你住在上海"),
            ("我喜欢吃披萨", "披萨是美味的选择"),
            ("我有一只猫,叫咪咪", "很可爱的名字,咪咪"),
        ]

        for user_input, ai_output in memories:
            memory.save_context(
                {"input": user_input},
                {"output": ai_output}
            )
            print(f"  添加: {user_input}")

        print("\n语义检索相关记忆:")

        # 测试检索
        queries = [
            "我喜欢什么颜色?",
            "什么时候是我的生日?",
            "我的宠物叫什么名字?",
        ]

        for query in queries:
            relevant = memory.load_memory_variables({"prompt": query})
            print(f"\n查询: {query}")
            print(f"检索到的相关记忆:")
            print(f"{relevant['history']}")

        print("\n✅ 向量检索Memory的优势:")
        print("  - 语义相似度检索")
        print("  - 适合超长对话(> 100轮)")
        print("  - 只加载相关上下文")
        print("  - 降低Token消耗")

    except Exception as e:
        print(f"\n⚠️ 错误: {e}")


def demo_multi_memory_combination():
    """组合多种Memory"""
    print("\n" + "=" * 60)
    print("3. 组合多种Memory - 分层记忆")
    print("=" * 60)

    from langchain.memory import (
        ConversationBufferWindowMemory,
        ConversationSummaryMemory,
        CombinedMemory
    )
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 短期Memory: 最近5轮
    short_term_memory = ConversationBufferWindowMemory(
        k=5,
        memory_key="recent_history",
        input_key="input"
    )

    # 长期Memory: 完整摘要
    long_term_memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="summary",
        input_key="input"
    )

    # 组合Memory
    memory = CombinedMemory(memories=[short_term_memory, long_term_memory])

    print("\n组合Memory结构:")
    print("  短期Memory: 保留最近5轮完整对话")
    print("  长期Memory: 所有对话的摘要")

    # 模拟添加对话
    conversations = [
        ("我是一名AI研究员", "很高兴认识你!"),
        ("我在研究Transformer模型", "Transformer是很重要的架构"),
        ("我发表过关于注意力机制的论文", "很impressive!"),
    ]

    for user_input, ai_output in conversations:
        short_term_memory.save_context(
            {"input": user_input},
            {"output": ai_output}
        )
        long_term_memory.save_context(
            {"input": user_input},
            {"output": ai_output}
        )

    print("\n查看组合Memory:")
    combined = memory.load_memory_variables({})
    print(f"\n短期记忆(最近对话):\n{combined.get('recent_history', 'N/A')}")
    print(f"\n长期记忆(摘要):\n{combined.get('summary', 'N/A')}")

    print("\n✅ 分层Memory的好处:")
    print("  - 短期:完整上下文,精准理解")
    print("  - 长期:关键信息,节省Token")
    print("  - 结合两者优势")


def demo_memory_with_streaming():
    """Memory + 流式输出"""
    print("\n" + "=" * 60)
    print("4. Memory + 流式输出")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

    memory = ConversationBufferMemory()

    # 启用流式输出
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )

    conversation = ConversationChain(llm=llm, memory=memory)

    print("\n流式对话(实时输出):")

    print("\n用户: 请介绍一下LangChain")
    print("AI: ", end="", flush=True)
    conversation.predict(input="请介绍一下LangChain")

    print("\n\n用户: 它有哪些核心组件?")
    print("AI: ", end="", flush=True)
    conversation.predict(input="它有哪些核心组件?")

    print("\n\n✅ Memory + 流式输出:")
    print("  - 保留对话上下文")
    print("  - 实时响应用户")
    print("  - 提升用户体验")


def demo_enterprise_memory_management():
    """企业级Memory管理"""
    print("\n" + "=" * 60)
    print("5. 企业级Memory管理方案")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    import json
    from datetime import datetime

    class EnterpriseMemoryManager:
        """企业级Memory管理器"""

        def __init__(self, storage_dir: Path):
            self.storage_dir = storage_dir
            self.storage_dir.mkdir(exist_ok=True)
            self.memories = {}  # {user_id: memory}

        def get_memory(self, user_id: str) -> ConversationBufferMemory:
            """获取用户Memory,不存在则创建"""
            if user_id not in self.memories:
                memory = ConversationBufferMemory()
                # 尝试从文件加载
                self._load_from_disk(user_id, memory)
                self.memories[user_id] = memory
            return self.memories[user_id]

        def save_memory(self, user_id: str):
            """保存Memory到磁盘"""
            if user_id in self.memories:
                self._save_to_disk(user_id, self.memories[user_id])

        def clear_memory(self, user_id: str):
            """清空用户Memory"""
            if user_id in self.memories:
                self.memories[user_id].clear()
                # 删除磁盘文件
                file_path = self.storage_dir / f"{user_id}.json"
                if file_path.exists():
                    file_path.unlink()

        def get_statistics(self, user_id: str) -> dict:
            """获取Memory统计信息"""
            if user_id not in self.memories:
                return {"message_count": 0}

            memory = self.memories[user_id]
            messages = memory.chat_memory.messages

            return {
                "message_count": len(messages),
                "user_messages": len([m for m in messages if m.type == "human"]),
                "ai_messages": len([m for m in messages if m.type == "ai"]),
                "last_updated": datetime.now().isoformat()
            }

        def _save_to_disk(self, user_id: str, memory: ConversationBufferMemory):
            """内部方法:保存到磁盘"""
            messages = memory.chat_memory.messages
            data = {
                "user_id": user_id,
                "saved_at": datetime.now().isoformat(),
                "messages": [
                    {"type": msg.type, "content": msg.content}
                    for msg in messages
                ]
            }

            file_path = self.storage_dir / f"{user_id}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        def _load_from_disk(self, user_id: str, memory: ConversationBufferMemory):
            """内部方法:从磁盘加载"""
            file_path = self.storage_dir / f"{user_id}.json"
            if not file_path.exists():
                return

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            from langchain.schema import HumanMessage, AIMessage

            for msg in data.get("messages", []):
                if msg["type"] == "human":
                    memory.chat_memory.add_user_message(msg["content"])
                else:
                    memory.chat_memory.add_ai_message(msg["content"])

    # 使用示例
    print("\n企业级Memory管理器使用:")

    manager = EnterpriseMemoryManager(Path("./enterprise_memory"))

    # 用户1的对话
    user1_memory = manager.get_memory("user_001")
    user1_memory.save_context(
        {"input": "我需要技术支持"},
        {"output": "好的,请问遇到什么问题?"}
    )
    manager.save_memory("user_001")

    # 用户2的对话
    user2_memory = manager.get_memory("user_002")
    user2_memory.save_context(
        {"input": "我要查询订单"},
        {"output": "请提供订单号"}
    )
    manager.save_memory("user_002")

    # 获取统计
    stats1 = manager.get_statistics("user_001")
    stats2 = manager.get_statistics("user_002")

    print(f"\n用户1统计: {stats1}")
    print(f"用户2统计: {stats2}")

    print("\n✅ 企业级Memory管理特性:")
    print("  - 多用户隔离")
    print("  - 持久化存储")
    print("  - 统计和监控")
    print("  - 自动保存/加载")
    print("  - 内存管理")


def demo_memory_optimization_strategies():
    """Memory优化策略"""
    print("\n" + "=" * 60)
    print("6. Memory优化策略")
    print("=" * 60)

    print("""
🚀 Memory优化策略大全

策略1: 动态切换Memory类型
────────────────────────
class AdaptiveMemoryManager:
    def get_memory(self, turn_count: int):
        if turn_count < 5:
            # 前5轮:完整历史
            return ConversationBufferMemory()
        elif turn_count < 20:
            # 5-20轮:滑动窗口
            return ConversationBufferWindowMemory(k=5)
        else:
            # 20+轮:摘要压缩
            return ConversationSummaryBufferMemory(
                llm=llm,
                max_token_limit=200
            )

策略2: 定期清理和归档
────────────────────────
class MemoryArchiver:
    def should_archive(self, memory):
        \"\"\"判断是否需要归档\"\"\"
        message_count = len(memory.chat_memory.messages)
        return message_count > 50

    def archive_and_clear(self, user_id, memory):
        \"\"\"归档并清空\"\"\"
        # 保存到数据库
        self.save_to_db(user_id, memory)
        # 清空Memory
        memory.clear()

策略3: Token预算控制
────────────────────────
class TokenBudgetMemory:
    def __init__(self, max_tokens=500):
        self.max_tokens = max_tokens
        self.memory = ConversationBufferMemory()

    def save_context(self, inputs, outputs):
        self.memory.save_context(inputs, outputs)

        # 检查Token数
        history = self.memory.load_memory_variables({})
        tokens = count_tokens(history["history"])

        if tokens > self.max_tokens:
            # 超限:删除最早的消息
            self.memory.chat_memory.messages.pop(0)
            self.memory.chat_memory.messages.pop(0)

策略4: 分场景Memory配置
────────────────────────
MEMORY_CONFIGS = {
    "customer_service": {
        "type": "window",
        "k": 5
    },
    "education": {
        "type": "summary_buffer",
        "max_tokens": 500
    },
    "casual_chat": {
        "type": "buffer",
        "max_rounds": 10
    }
}

策略5: Memory预热
────────────────────────
def preload_user_context(user_id):
    \"\"\"预加载用户上下文\"\"\"
    memory = ConversationBufferMemory()

    # 从数据库加载用户画像
    profile = db.get_user_profile(user_id)

    # 注入背景信息
    memory.save_context(
        {"input": "我的基本信息"},
        {"output": f"姓名:{profile.name},年龄:{profile.age}"}
    )

    return memory

策略6: 混合存储
────────────────────────
class HybridMemoryStorage:
    def __init__(self):
        self.hot_memory = {}      # 内存(热数据)
        self.cold_storage = db    # 数据库(冷数据)

    def get_memory(self, user_id):
        # 优先从内存获取
        if user_id in self.hot_memory:
            return self.hot_memory[user_id]

        # 从数据库加载
        memory = self.cold_storage.load(user_id)
        self.hot_memory[user_id] = memory
        return memory

⚡ 性能优化建议

1. 批量操作:
   - 批量保存Memory
   - 减少磁盘I/O

2. 异步处理:
   - 异步保存Memory
   - 不阻塞主流程

3. 缓存策略:
   - LRU缓存常用Memory
   - 定期清理不活跃Memory

4. 压缩存储:
   - JSON压缩
   - 只存储必要字段

💰 成本控制

1. Token限制:
   - 设置max_token_limit
   - 自动压缩超限Memory

2. 存储成本:
   - 定期归档旧对话
   - 删除过期数据

3. 计算成本:
   - 减少Summary调用
   - 使用更便宜的模型生成摘要
    """)


if __name__ == "__main__":
    print("🎯 Memory实战应用示例\n")

    # 运行所有示例
    demo_conversational_rag()
    demo_vector_store_backed_memory()
    demo_multi_memory_combination()
    demo_memory_with_streaming()
    demo_enterprise_memory_management()
    demo_memory_optimization_strategies()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. Memory + RAG:
   - ConversationalRetrievalChain
   - return_messages=True(必须)
   - 支持代词引用和追问

2. VectorStoreRetrieverMemory:
   - 语义检索相关记忆
   - 适合超长对话
   - 只加载相关上下文

3. 组合Memory:
   - CombinedMemory
   - 短期+长期
   - 分层记忆策略

4. 企业级管理:
   - 多用户隔离
   - 持久化存储
   - 统计和监控
   - 自动保存/加载

5. 优化策略:
   ✅ 动态切换Memory类型
   ✅ 定期清理和归档
   ✅ Token预算控制
   ✅ 分场景配置
   ✅ Memory预热
   ✅ 混合存储

6. 性能优化:
   - 批量操作
   - 异步处理
   - 缓存策略
   - 压缩存储

7. 成本控制:
   - Token限制
   - 存储优化
   - 计算优化

8. 最佳实践:
   ✅ 根据场景选择Memory
   ✅ 监控Token消耗
   ✅ 定期清理历史
   ✅ 实现持久化
   ✅ 多用户隔离
   ✅ 异常处理

🎓 Memory系统学习完成!

你已经掌握了:
- 6种Memory类型的使用
- Memory与RAG的结合
- 企业级Memory管理
- 性能和成本优化

下一步:
→ LCEL和Chains(Day 14-15)
→ 构建复杂的工作流
→ 实现生产级应用
    """)