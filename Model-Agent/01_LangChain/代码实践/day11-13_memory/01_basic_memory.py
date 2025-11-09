"""
Memory基础示例 - ConversationBufferMemory和基础Memory类型

学习目标:
1. 理解Memory的基本概念和作用
2. 掌握ConversationBufferMemory的使用
3. 学会Memory与Chain的结合
4. 理解Memory的保存和加载
"""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def demo_problem_without_memory():
    """演示没有Memory的问题"""
    print("=" * 60)
    print("1. 问题演示 - LLM没有记忆")
    print("=" * 60)

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    print("\n没有Memory的对话:")

    # 第一轮
    response1 = llm.invoke("我叫张三，我是一名Python开发者")
    print(f"\n用户: 我叫张三，我是一名Python开发者")
    print(f"AI: {response1.content}")

    # 第二轮
    response2 = llm.invoke("我叫什么名字?")
    print(f"\n用户: 我叫什么名字?")
    print(f"AI: {response2.content}")

    # 第三轮
    response3 = llm.invoke("我是做什么的?")
    print(f"\n用户: 我是做什么的?")
    print(f"AI: {response3.content}")

    print("\n❌ 问题: LLM不记得之前说过的内容!")


def demo_basic_memory():
    """ConversationBufferMemory基础使用"""
    print("\n" + "=" * 60)
    print("2. ConversationBufferMemory - 完整对话历史")
    print("=" * 60)

    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory
    from langchain_openai import ChatOpenAI

    # 创建Memory
    memory = ConversationBufferMemory()

    # 创建对话链
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False  # 设为True可看到内部过程
    )

    print("\n有Memory的对话:")

    # 第一轮
    response1 = conversation.predict(input="我叫张三，我是一名Python开发者")
    print(f"\n用户: 我叫张三，我是一名Python开发者")
    print(f"AI: {response1}")

    # 第二轮
    response2 = conversation.predict(input="我叫什么名字?")
    print(f"\n用户: 我叫什么名字?")
    print(f"AI: {response2}")

    # 第三轮
    response3 = conversation.predict(input="我是做什么的?")
    print(f"\n用户: 我是做什么的?")
    print(f"AI: {response3}")

    print("\n✅ Memory让LLM记住了之前的对话!")

    # 查看Memory内容
    print("\n当前Memory内容:")
    print(memory.load_memory_variables({}))


def demo_manual_memory_management():
    """手动管理Memory"""
    print("\n" + "=" * 60)
    print("3. 手动管理Memory")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory

    memory = ConversationBufferMemory()

    print("\n手动添加对话:")

    # 手动添加对话
    memory.save_context(
        {"input": "你好，我是李四"},
        {"output": "你好李四!很高兴认识你。"}
    )
    print("  添加: 用户说'你好，我是李四'")

    memory.save_context(
        {"input": "我今年25岁"},
        {"output": "了解，你今年25岁。"}
    )
    print("  添加: 用户说'我今年25岁'")

    memory.save_context(
        {"input": "我喜欢打篮球"},
        {"output": "很好的爱好!篮球很有趣。"}
    )
    print("  添加: 用户说'我喜欢打篮球'")

    # 查看Memory
    print("\nMemory内容:")
    history = memory.load_memory_variables({})
    print(history["history"])

    print("\n获取消息列表:")
    messages = memory.chat_memory.messages
    for i, msg in enumerate(messages, 1):
        role = "用户" if msg.type == "human" else "AI"
        print(f"  {i}. [{role}] {msg.content}")


def demo_chat_message_history():
    """ChatMessageHistory使用"""
    print("\n" + "=" * 60)
    print("4. ChatMessageHistory - Memory的基础")
    print("=" * 60)

    from langchain.memory import ChatMessageHistory

    history = ChatMessageHistory()

    print("\n添加消息:")
    history.add_user_message("你好")
    history.add_ai_message("你好!有什么可以帮你的?")
    history.add_user_message("今天天气怎么样?")
    history.add_ai_message("抱歉，我不能访问实时天气信息。")

    print("\n消息列表:")
    for i, msg in enumerate(history.messages, 1):
        role = "用户" if msg.type == "human" else "AI"
        print(f"  {i}. [{role}] {msg.content}")

    print(f"\n总消息数: {len(history.messages)}")

    # 清空历史
    print("\n清空历史...")
    history.clear()
    print(f"清空后消息数: {len(history.messages)}")


def demo_return_messages():
    """返回消息列表vs字符串"""
    print("\n" + "=" * 60)
    print("5. return_messages参数")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory

    # 默认返回字符串
    print("\n默认方式(return_messages=False):")
    memory1 = ConversationBufferMemory()
    memory1.save_context({"input": "你好"}, {"output": "你好!"})
    memory1.save_context({"input": "天气不错"}, {"output": "是的，很好"})

    result1 = memory1.load_memory_variables({})
    print(f"类型: {type(result1['history'])}")
    print(f"内容:\n{result1['history']}")

    # 返回消息列表
    print("\n返回消息列表(return_messages=True):")
    memory2 = ConversationBufferMemory(return_messages=True)
    memory2.save_context({"input": "你好"}, {"output": "你好!"})
    memory2.save_context({"input": "天气不错"}, {"output": "是的，很好"})

    result2 = memory2.load_memory_variables({})
    print(f"类型: {type(result2['history'])}")
    print(f"消息数: {len(result2['history'])}")
    for msg in result2['history']:
        print(f"  - {msg.__class__.__name__}: {msg.content}")

    print("\n✅ 使用场景:")
    print("  return_messages=False: 大多数场景,简单易用")
    print("  return_messages=True: 需要访问单个消息或metadata时")


def demo_custom_memory_keys():
    """自定义Memory键"""
    print("\n" + "=" * 60)
    print("6. 自定义Memory键")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import LLMChain
    from langchain_core.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI

    # 自定义键
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # Prompt中使用的键
        input_key="question",       # 输入键
        output_key="answer"         # 输出键
    )

    # 自定义Prompt
    template = """以下是历史对话:
{chat_history}

当前问题: {question}
回答:"""

    prompt = PromptTemplate(
        input_variables=["chat_history", "question"],
        template=template
    )

    # 创建Chain
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

    print("\n使用自定义键的对话:")

    response1 = chain.predict(question="我喜欢Python")
    print(f"\n问题: 我喜欢Python")
    print(f"回答: {response1}")

    response2 = chain.predict(question="我喜欢什么?")
    print(f"\n问题: 我喜欢什么?")
    print(f"回答: {response2}")


def demo_memory_persistence():
    """Memory持久化"""
    print("\n" + "=" * 60)
    print("7. Memory持久化 - 保存和恢复")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    import json

    # 创建Memory并添加对话
    memory = ConversationBufferMemory()
    memory.save_context({"input": "我叫王五"}, {"output": "你好王五!"})
    memory.save_context({"input": "我在上海工作"}, {"output": "上海是个好地方!"})

    print("\n原始Memory:")
    print(memory.load_memory_variables({}))

    # 序列化保存
    messages = memory.chat_memory.messages
    serialized = [
        {"type": msg.type, "content": msg.content}
        for msg in messages
    ]

    save_path = Path("memory_data")
    save_path.mkdir(exist_ok=True)

    file_path = save_path / "conversation.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Memory已保存到: {file_path}")

    # 加载恢复
    print("\n从文件恢复Memory...")
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    from langchain.schema import HumanMessage, AIMessage

    restored_memory = ConversationBufferMemory()
    for msg in loaded_data:
        if msg["type"] == "human":
            restored_memory.chat_memory.add_user_message(msg["content"])
        else:
            restored_memory.chat_memory.add_ai_message(msg["content"])

    print("恢复的Memory:")
    print(restored_memory.load_memory_variables({}))

    print("\n✅ Memory成功恢复!")


def demo_multi_user_memory():
    """多用户Memory管理"""
    print("\n" + "=" * 60)
    print("8. 多用户Memory管理")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    # 用户Memory存储
    user_memories = {}

    def get_user_memory(user_id: str):
        """获取用户的Memory"""
        if user_id not in user_memories:
            user_memories[user_id] = ConversationBufferMemory()
        return user_memories[user_id]

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 用户1的对话
    print("\n用户1的对话:")
    user1_memory = get_user_memory("user_001")
    conversation1 = ConversationChain(llm=llm, memory=user1_memory)

    response = conversation1.predict(input="我叫张三")
    print(f"  用户1: 我叫张三")
    print(f"  AI: {response}")

    # 用户2的对话
    print("\n用户2的对话:")
    user2_memory = get_user_memory("user_002")
    conversation2 = ConversationChain(llm=llm, memory=user2_memory)

    response = conversation2.predict(input="我叫李四")
    print(f"  用户2: 我叫李四")
    print(f"  AI: {response}")

    # 用户1继续对话
    print("\n用户1继续对话:")
    response = conversation1.predict(input="我叫什么名字?")
    print(f"  用户1: 我叫什么名字?")
    print(f"  AI: {response}")

    # 用户2继续对话
    print("\n用户2继续对话:")
    response = conversation2.predict(input="我叫什么名字?")
    print(f"  用户2: 我叫什么名字?")
    print(f"  AI: {response}")

    print(f"\n✅ 系统管理了{len(user_memories)}个用户的独立Memory")


def demo_memory_clear():
    """清空Memory"""
    print("\n" + "=" * 60)
    print("9. 清空Memory")
    print("=" * 60)

    from langchain.memory import ConversationBufferMemory

    memory = ConversationBufferMemory()

    # 添加一些对话
    memory.save_context({"input": "消息1"}, {"output": "回复1"})
    memory.save_context({"input": "消息2"}, {"output": "回复2"})
    memory.save_context({"input": "消息3"}, {"output": "回复3"})

    print(f"\n清空前消息数: {len(memory.chat_memory.messages)}")

    # 清空Memory
    memory.clear()

    print(f"清空后消息数: {len(memory.chat_memory.messages)}")

    print("\n✅ Memory已清空,可以开始新的对话")


if __name__ == "__main__":
    print("💾 LangChain Memory基础示例\n")

    # 运行所有示例
    demo_problem_without_memory()
    demo_basic_memory()
    demo_manual_memory_management()
    demo_chat_message_history()
    demo_return_messages()
    demo_custom_memory_keys()
    demo_memory_persistence()
    demo_multi_user_memory()
    demo_memory_clear()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 为什么需要Memory:
   - LLM本身是无状态的
   - 每次调用相互独立
   - Memory让LLM有了"记忆力"

2. ConversationBufferMemory:
   - 保存完整对话历史
   - 最简单直接的Memory类型
   - 适合短对话(< 10轮)

3. Memory核心组件:
   - ChatMessageHistory: 存储消息列表
   - Memory类: 管理和格式化历史
   - Chain: 自动使用Memory

4. Memory基础操作:
   ✅ save_context(): 手动添加对话
   ✅ load_memory_variables(): 获取历史
   ✅ clear(): 清空历史
   ✅ chat_memory.messages: 访问消息列表

5. 重要参数:
   - memory_key: Prompt中使用的键(默认"history")
   - return_messages: 返回消息列表还是字符串
   - input_key/output_key: 自定义输入输出键

6. Memory持久化:
   - 序列化到JSON文件
   - 使用数据库(SQLite/Redis等)
   - 重启后恢复对话状态

7. 多用户场景:
   - 每个用户独立的Memory实例
   - 使用字典管理: {user_id: memory}
   - 支持并发访问

8. 最佳实践:
   ✅ 根据对话长度选择Memory类型
   ✅ 定期清空或归档历史
   ✅ 监控Token消耗
   ✅ 为生产环境实现持久化

9. 下一步:
   → ConversationBufferWindowMemory (滑动窗口)
   → ConversationSummaryMemory (摘要压缩)
   → VectorStoreRetrieverMemory (语义检索)
    """)