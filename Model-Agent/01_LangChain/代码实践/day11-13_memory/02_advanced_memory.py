"""
高级Memory类型示例 - 窗口Memory、摘要Memory和混合策略

学习目标:
1. 掌握ConversationBufferWindowMemory的使用
2. 理解ConversationSummaryMemory的工作原理
3. 学会使用ConversationSummaryBufferMemory混合策略
4. 选择合适的Memory类型
"""
from dotenv import load_dotenv

load_dotenv()


def demo_buffer_window_memory():
    """ConversationBufferWindowMemory - 滑动窗口"""
    print("=" * 60)
    print("1. ConversationBufferWindowMemory - 滑动窗口")
    print("=" * 60)

    from langchain.memory import ConversationBufferWindowMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    # 只保留最近3轮对话
    memory = ConversationBufferWindowMemory(k=3)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    conversation = ConversationChain(llm=llm, memory=memory)

    print("\n进行5轮对话,只保留最近3轮:")

    # 进行5轮对话
    responses = []
    for i in range(1, 6):
        input_text = f"这是第{i}轮对话"
        response = conversation.predict(input=input_text)
        print(f"\n第{i}轮 - 用户: {input_text}")
        print(f"       AI: {response}")

    # 查看Memory(只有最近3轮)
    print("\n当前Memory内容(只保留最近3轮):")
    history = memory.load_memory_variables({})
    print(history["history"])

    print(f"\n实际消息数: {len(memory.chat_memory.messages)}")
    print("(k=3意味着保留3轮对话,即6条消息)")

    print("\n✅ 使用场景:")
    print("  - 长对话(> 10轮)")
    print("  - 成本敏感")
    print("  - 只需关注最近话题")


def demo_window_memory_comparison():
    """对比不同k值的效果"""
    print("\n" + "=" * 60)
    print("2. 不同k值的Token消耗对比")
    print("=" * 60)

    from langchain.memory import ConversationBufferWindowMemory
    from langchain.callbacks import get_openai_callback
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 测试不同k值
    k_values = [1, 3, 5]

    for k in k_values:
        print(f"\n测试 k={k}:")
        memory = ConversationBufferWindowMemory(k=k)
        conversation = ConversationChain(llm=llm, memory=memory)

        with get_openai_callback() as cb:
            # 进行10轮对话
            for i in range(10):
                conversation.predict(input=f"第{i+1}轮对话")

            print(f"  总Token: {cb.total_tokens}")
            print(f"  成本: ${cb.total_cost:.4f}")
            print(f"  Memory中消息数: {len(memory.chat_memory.messages)}")

    print("\n✅ k值选择建议:")
    print("  k=1: 只记住上一轮(简单问答)")
    print("  k=3-5: 平衡记忆和成本(推荐)")
    print("  k=10+: 较长上下文(特殊需求)")


def demo_summary_memory():
    """ConversationSummaryMemory - 摘要压缩"""
    print("\n" + "=" * 60)
    print("3. ConversationSummaryMemory - 摘要压缩")
    print("=" * 60)

    from langchain.memory import ConversationSummaryMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 创建摘要Memory
    memory = ConversationSummaryMemory(llm=llm)

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True  # 显示摘要过程
    )

    print("\n进行多轮对话:")

    # 第1轮
    print("\n--- 第1轮 ---")
    conversation.predict(input="我叫张三，我是一名软件工程师")

    # 第2轮
    print("\n--- 第2轮 ---")
    conversation.predict(input="我在北京工作，已经5年了")

    # 第3轮
    print("\n--- 第3轮 ---")
    conversation.predict(input="我擅长Python和Go语言")

    # 第4轮
    print("\n--- 第4轮 ---")
    response = conversation.predict(input="请总结一下我的信息")
    print(f"\n用户: 请总结一下我的信息")
    print(f"AI: {response}")

    # 查看摘要
    print("\n当前Memory摘要:")
    history = memory.load_memory_variables({})
    print(history["history"])

    print("\n✅ 摘要Memory特点:")
    print("  - 大幅减少Token消耗")
    print("  - 保留关键信息")
    print("  - 需要额外LLM调用生成摘要")
    print("  - 可能丢失细节")


def demo_summary_buffer_memory():
    """ConversationSummaryBufferMemory - 混合策略"""
    print("\n" + "=" * 60)
    print("4. ConversationSummaryBufferMemory - 混合策略(推荐)")
    print("=" * 60)

    from langchain.memory import ConversationSummaryBufferMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 创建混合Memory
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=200  # Token上限
    )

    conversation = ConversationChain(llm=llm, memory=memory)

    print("\n混合策略工作原理:")
    print("  1. 最近的对话保持完整")
    print("  2. 超过Token限制的旧对话被压缩成摘要")
    print("  3. 平衡完整性和成本")

    print("\n进行多轮对话:")

    topics = [
        "我是一名AI研究员",
        "我在研究大语言模型",
        "我特别关注Prompt Engineering",
        "我发表过3篇论文",
        "我在斯坦福大学工作",
        "我的研究方向是Few-Shot Learning",
    ]

    for i, topic in enumerate(topics, 1):
        response = conversation.predict(input=topic)
        print(f"\n第{i}轮 - 用户: {topic}")
        print(f"       AI: {response[:50]}...")

    # 查看Memory结构
    print("\n当前Memory内容:")
    history = memory.load_memory_variables({})
    print(history["history"])

    print("\n✅ 混合策略优势:")
    print("  - 最近对话完整,旧对话摘要")
    print("  - 灵活的Token控制")
    print("  - 推荐的默认选择")


def demo_memory_comparison():
    """对比不同Memory类型"""
    print("\n" + "=" * 60)
    print("5. Memory类型对比实验")
    print("=" * 60)

    from langchain.memory import (
        ConversationBufferMemory,
        ConversationBufferWindowMemory,
        ConversationSummaryMemory
    )
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI
    from langchain.callbacks import get_openai_callback

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 准备测试对话
    test_inputs = [
        "我叫李明",
        "我是一名数据科学家",
        "我在上海工作",
        "我擅长机器学习",
        "我喜欢Python",
        "我有5年经验",
        "我喜欢什么编程语言?",
    ]

    # 测试1: BufferMemory
    print("\n测试1: ConversationBufferMemory (完整历史)")
    memory1 = ConversationBufferMemory()
    conv1 = ConversationChain(llm=llm, memory=memory1)

    with get_openai_callback() as cb1:
        for inp in test_inputs:
            conv1.predict(input=inp)

    print(f"  Token消耗: {cb1.total_tokens}")
    print(f"  成本: ${cb1.total_cost:.4f}")

    # 测试2: WindowMemory
    print("\n测试2: ConversationBufferWindowMemory (k=3)")
    memory2 = ConversationBufferWindowMemory(k=3)
    conv2 = ConversationChain(llm=llm, memory=memory2)

    with get_openai_callback() as cb2:
        for inp in test_inputs:
            conv2.predict(input=inp)

    print(f"  Token消耗: {cb2.total_tokens}")
    print(f"  成本: ${cb2.total_cost:.4f}")
    print(f"  节省: {(1 - cb2.total_tokens/cb1.total_tokens)*100:.1f}%")

    # 测试3: SummaryMemory
    print("\n测试3: ConversationSummaryMemory (摘要)")
    memory3 = ConversationSummaryMemory(llm=llm)
    conv3 = ConversationChain(llm=llm, memory=memory3)

    with get_openai_callback() as cb3:
        for inp in test_inputs:
            conv3.predict(input=inp)

    print(f"  Token消耗: {cb3.total_tokens}")
    print(f"  成本: ${cb3.total_cost:.4f}")
    print(f"  节省: {(1 - cb3.total_tokens/cb1.total_tokens)*100:.1f}%")


def demo_memory_token_monitoring():
    """监控Memory的Token消耗"""
    print("\n" + "=" * 60)
    print("6. 监控Memory的Token消耗")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI
    import tiktoken

    memory = ConversationBufferMemory()
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    conversation = ConversationChain(llm=llm, memory=memory)

    # 初始化Token计数器
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    print("\n进行对话并监控Token:")

    for i in range(5):
        input_text = f"这是第{i+1}轮对话，内容是关于LangChain的"
        conversation.predict(input=input_text)

        # 计算当前Memory的Token数
        history_text = memory.load_memory_variables({})["history"]
        token_count = len(enc.encode(history_text))

        print(f"\n第{i+1}轮后 Memory Token数: {token_count}")

    print("\n✅ Token监控的意义:")
    print("  - 预估成本")
    print("  - 避免超过模型限制")
    print("  - 决定何时清空或压缩Memory")


def demo_memory_best_practices():
    """Memory最佳实践"""
    print("\n" + "=" * 60)
    print("7. Memory选择和使用最佳实践")
    print("=" * 60)

    print("""
📊 Memory选择决策

场景1: 短对话客服(< 10轮)
✅ 推荐: ConversationBufferMemory
   - 完整上下文
   - 精准理解
   - Token成本可控

场景2: 长对话客服(10-20轮)
✅ 推荐: ConversationBufferWindowMemory (k=5)
   - 控制成本
   - 保留最近话题
   - 响应速度快

场景3: 超长对话(20-50轮)
✅ 推荐: ConversationSummaryBufferMemory
   - 平衡完整性和成本
   - 最近对话完整
   - 旧对话摘要

场景4: 极长对话(> 50轮)
✅ 推荐: ConversationSummaryMemory
   - 大幅降低成本
   - 保留关键信息
   - 适合信息密集对话

🎯 参数调优建议

ConversationBufferWindowMemory:
- k=1: 只记上一轮(简单QA)
- k=3: 客服场景(推荐)
- k=5-7: 复杂咨询
- k=10+: 特殊需求

ConversationSummaryBufferMemory:
- max_token_limit=100: 严格控制
- max_token_limit=200: 平衡选择(推荐)
- max_token_limit=500: 宽松策略

⚠️ 注意事项

1. Token成本:
   - Buffer < Window < SummaryBuffer < Summary
   - 但Summary需要额外调用生成摘要

2. 信息完整性:
   - Buffer > SummaryBuffer > Window > Summary
   - 根据场景权衡

3. 响应速度:
   - Window > Buffer > SummaryBuffer > Summary
   - Summary需要额外生成摘要

4. 适用性:
   - 不是所有对话都需要Memory
   - 简单单轮问答可以不用Memory
   - 需要上下文的才用Memory

💡 实战技巧

1. 动态切换策略:
   - 前5轮: BufferMemory
   - 5-20轮: WindowMemory (k=5)
   - 20+轮: SummaryBufferMemory

2. 定期清理:
   - 话题切换时清空Memory
   - 用户明确结束对话后清空
   - 定时归档历史对话

3. 分层Memory:
   - 短期Memory: 当前对话
   - 长期Memory: 用户画像
   - 知识Memory: 领域知识

4. 成本控制:
   - 监控Token消耗
   - 设置Token上限
   - 超限自动压缩或清空
    """)


if __name__ == "__main__":
    print("🔄 LangChain 高级Memory类型示例\n")

    # 运行所有示例
    demo_buffer_window_memory()
    demo_window_memory_comparison()
    demo_summary_memory()
    demo_summary_buffer_memory()
    demo_memory_comparison()
    demo_memory_token_monitoring()
    demo_memory_best_practices()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. ConversationBufferWindowMemory:
   - 只保留最近k轮对话
   - 控制Token消耗
   - 适合长对话

2. ConversationSummaryMemory:
   - 压缩成摘要
   - 大幅减少Token
   - 需要额外LLM调用

3. ConversationSummaryBufferMemory:
   - 混合策略(推荐)
   - 最近完整+旧摘要
   - 平衡完整性和成本

4. Memory选择:
   < 10轮 → BufferMemory
   10-20轮 → WindowMemory (k=3-5)
   20-50轮 → SummaryBufferMemory
   > 50轮 → SummaryMemory

5. Token管理:
   - 监控消耗
   - 设置上限
   - 动态调整策略

6. 最佳实践:
   ✅ 根据场景选择Memory
   ✅ 监控Token消耗
   ✅ 定期清理历史
   ✅ 考虑成本和效果平衡

7. 下一步:
   → VectorStoreRetrieverMemory (语义检索)
   → Memory + RAG (对话式问答)
   → 多Memory组合
    """)