"""
流式输出示例

学习目标:
1. 掌握stream()方法实现流式输出
2. 理解astream()异步流式输出
3. 对比流式vs非流式的用户体验
"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import sys
import time
import asyncio

load_dotenv()


def demo_normal_invoke():
    """演示普通调用(非流式)"""
    print("=" * 60)
    print("普通调用 (非流式)")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    print("\n正在等待响应...")
    start_time = time.time()

    response = llm.invoke("用100字介绍一下LangChain框架")

    elapsed = time.time() - start_time

    print(f"\n等待了 {elapsed:.2f} 秒后才看到完整回复:")
    print(response.content)
    print(f"\n用户体验: 需要等待 {elapsed:.2f} 秒 ❌")


def demo_stream():
    """演示流式输出"""
    print("\n" + "=" * 60)
    print("流式输出")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    print("\n实时显示:")
    start_time = time.time()

    for chunk in llm.stream("用100字介绍一下LangChain框架"):
        print(chunk.content, end="", flush=True)
        # 模拟看到内容的延迟
        sys.stdout.flush()

    elapsed = time.time() - start_time

    print(f"\n\n总耗时: {elapsed:.2f} 秒")
    print("用户体验: 实时看到内容 ✅")


def demo_stream_with_details():
    """演示流式输出的详细信息"""
    print("\n" + "=" * 60)
    print("流式输出 - 详细信息")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    print("\n显示每个chunk的结构:\n")

    chunk_count = 0
    for chunk in llm.stream("说一句话"):
        chunk_count += 1
        print(f"Chunk {chunk_count}:")
        print(f"  内容: '{chunk.content}'")
        print(f"  类型: {type(chunk)}")
        if hasattr(chunk, 'response_metadata'):
            print(f"  元数据: {chunk.response_metadata}")
        print()


async def demo_astream():
    """演示异步流式输出"""
    print("=" * 60)
    print("异步流式输出 (astream)")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    print("\n异步实时显示:")

    async for chunk in llm.astream("用一句话解释什么是异步编程"):
        print(chunk.content, end="", flush=True)

    print("\n")


def demo_multiple_streams():
    """演示同时处理多个流式请求"""
    print("\n" + "=" * 60)
    print("批量流式处理")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    questions = [
        "什么是Python?",
        "什么是JavaScript?",
        "什么是Rust?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n问题 {i}: {question}")
        print("回答: ", end="", flush=True)

        for chunk in llm.stream(question):
            print(chunk.content, end="", flush=True)

        print()  # 换行


def demo_stream_with_callback():
    """演示流式输出配合回调函数"""
    print("\n" + "=" * 60)
    print("流式输出 + 回调函数")
    print("=" * 60)

    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )

    print("\n使用回调处理器自动输出:\n")
    llm.invoke("介绍一下流式输出的优势")
    print("\n")


if __name__ == "__main__":
    # 运行所有示例
    print("🌊 LangChain 流式输出完整示例\n")

    # 1. 对比普通vs流式
    demo_normal_invoke()
    demo_stream()

    # 2. 详细信息
    demo_stream_with_details()

    # 3. 异步流式
    print("\n" + "=" * 60)
    print("运行异步示例...")
    print("=" * 60)
    asyncio.run(demo_astream())

    # 4. 批量处理
    demo_multiple_streams()

    # 5. 回调函数
    demo_stream_with_callback()

    # 总结
    print("=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 流式输出的优势:
   ✅ 实时反馈,提升用户体验
   ✅ 适合长文本生成
   ✅ 避免用户等待超时
   ✅ 看起来更"智能"

2. 使用方法:
   - 同步: llm.stream(message)
   - 异步: llm.astream(message)
   - 回调: StreamingStdOutCallbackHandler

3. 适用场景:
   - 聊天机器人
   - 长文章生成
   - Web应用(配合SSE)
   - 需要实时反馈的任何场景

4. 注意事项:
   - 总Token数和成本不变
   - 网络请求略多
   - 需要proper的flush处理
    """)