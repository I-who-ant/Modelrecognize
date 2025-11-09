"""
Chat Models vs LLMs 对比示例

学习目标:
1. 理解Chat Models的消息结构
2. 对比Chat Models和LLMs的使用方式
3. 理解什么场景用什么模型
"""
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()


def demo_chat_model():
    """演示Chat Model的使用"""
    print("=" * 60)
    print("Chat Model 示例")
    print("=" * 60)

    # 初始化Chat Model
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    # 方式1: 直接传字符串(会自动转换为HumanMessage)
    print("\n--- 方式1: 直接传字符串 ---")
    response = chat.invoke("你好，请介绍一下你自己")
    print(f"回复: {response.content}\n")

    # 方式2: 使用消息对象(推荐)
    print("--- 方式2: 使用消息对象 ---")
    messages = [
        SystemMessage(content="你是一个专业的Python编程导师，擅长用简单的语言解释复杂概念"),
        HumanMessage(content="什么是装饰器?")
    ]
    response = chat.invoke(messages)
    print(f"回复: {response.content}\n")

    # 方式3: 多轮对话
    print("--- 方式3: 多轮对话 ---")
    conversation = [
        SystemMessage(content="你是一个友好的AI助手"),
        HumanMessage(content="LangChain是什么?"),
        AIMessage(content="LangChain是一个用于构建LLM应用的框架..."),
        HumanMessage(content="它有什么优势?")
    ]
    response = chat.invoke(conversation)
    print(f"回复: {response.content}\n")

    # 查看响应对象的结构
    print("--- 响应对象结构 ---")
    print(f"类型: {type(response)}")
    print(f"内容: {response.content[:100]}...")
    print(f"元数据: {response.response_metadata.keys()}")


def demo_llm():
    """演示传统LLM的使用"""
    print("\n" + "=" * 60)
    print("LLM (文本补全) 示例")
    print("=" * 60)

    # 初始化LLM
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.7
    )

    # LLM只接受字符串
    prompt = "完成这句话：Python是一门"
    response = llm.invoke(prompt)

    print(f"\n输入: {prompt}")
    print(f"输出: {response}")


def compare_models():
    """对比两种模型"""
    print("\n" + "=" * 60)
    print("Chat Model vs LLM 对比")
    print("=" * 60)

    question = "解释一下什么是机器学习"

    # Chat Model
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chat_response = chat.invoke(question)

    # LLM
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
    llm_response = llm.invoke(question)

    print(f"\n问题: {question}\n")
    print("--- Chat Model 回复 ---")
    print(chat_response.content[:200] + "...\n")
    print("--- LLM 回复 ---")
    print(llm_response[:200] + "...\n")

    # Token对比
    chat_tokens = chat_response.response_metadata.get('token_usage', {})
    print("--- Token使用对比 ---")
    print(f"Chat Model: {chat_tokens}")
    print(f"LLM: (需要手动计算)\n")


if __name__ == "__main__":
    # 运行所有示例
    demo_chat_model()
    demo_llm()
    compare_models()

    print("=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. Chat Models:
   - 输入: 消息列表 (SystemMessage, HumanMessage, AIMessage)
   - 输出: AIMessage对象
   - 支持多轮对话上下文
   - 适合: 聊天机器人、助手、需要角色设定的场景

2. LLMs:
   - 输入: 字符串
   - 输出: 字符串
   - 单次文本补全
   - 适合: 简单文本生成

3. 推荐: 99%场景使用Chat Models!
    """)