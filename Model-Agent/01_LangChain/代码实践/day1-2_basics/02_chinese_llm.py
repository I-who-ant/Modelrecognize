"""
使用国产大模型示例
演示LangChain的模型互换能力

学习目标:
1. 理解LangChain如何支持多种模型
2. 掌握模型切换的方法
3. 对比不同模型的调用方式
"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()


def test_openai():
    """测试OpenAI模型"""
    print("\n--- 测试 OpenAI GPT-3.5 ---")

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )

    start_time = time.time()
    response = llm.invoke("用一句话介绍LangChain的核心价值")
    elapsed = time.time() - start_time

    print(f"响应: {response.content}")
    print(f"耗时: {elapsed:.2f}秒")
    print(f"Token: {response.response_metadata.get('token_usage', 'N/A')}")


def test_deepseek():
    """测试DeepSeek模型"""
    print("\n--- 测试 DeepSeek ---")

    # DeepSeek兼容OpenAI接口,可以使用ChatOpenAI类
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
        temperature=0.7
    )

    start_time = time.time()
    response = llm.invoke("用一句话介绍LangChain的核心价值")
    elapsed = time.time() - start_time

    print(f"响应: {response.content}")
    print(f"耗时: {elapsed:.2f}秒")
    print(f"Token: {response.response_metadata.get('token_usage', 'N/A')}")


def test_zhipu():
    """测试智谱GLM模型"""
    print("\n--- 测试 智谱GLM ---")

    try:
        from langchain_community.chat_models import ChatZhipuAI

        llm = ChatZhipuAI(
            model="glm-4",
            api_key=os.getenv("ZHIPU_API_KEY"),
            temperature=0.7
        )

        start_time = time.time()
        response = llm.invoke("用一句话介绍LangChain的核心价值")
        elapsed = time.time() - start_time

        print(f"响应: {response.content}")
        print(f"耗时: {elapsed:.2f}秒")
    except ImportError:
        print("提示: 需要安装 langchain-community")
        print("命令: pip install langchain-community")


def test_ollama_local():
    """测试本地Ollama模型(可选)"""
    print("\n--- 测试 本地Ollama模型 ---")

    try:
        from langchain_community.chat_models import ChatOllama

        # 需要先本地运行: ollama run llama2
        llm = ChatOllama(
            model="llama2",
            temperature=0.7
        )

        start_time = time.time()
        response = llm.invoke("What is LangChain in one sentence?")
        elapsed = time.time() - start_time

        print(f"响应: {response.content}")
        print(f"耗时: {elapsed:.2f}秒")
    except Exception as e:
        print(f"提示: {str(e)}")
        print("如需使用Ollama,请先安装并运行本地模型")
        print("参考: https://ollama.ai/")


if __name__ == "__main__":
    print("=" * 50)
    print("LangChain 多模型支持测试")
    print("=" * 50)

    # 测试OpenAI
    if os.getenv("OPENAI_API_KEY"):
        test_openai()
    else:
        print("\n⚠️  未配置OPENAI_API_KEY,跳过OpenAI测试")

    # 测试DeepSeek
    if os.getenv("DEEPSEEK_API_KEY"):
        test_deepseek()
    else:
        print("\n⚠️  未配置DEEPSEEK_API_KEY,跳过DeepSeek测试")

    # 测试智谱
    if os.getenv("ZHIPU_API_KEY"):
        test_zhipu()
    else:
        print("\n⚠️  未配置ZHIPU_API_KEY,跳过智谱GLM测试")

    # 测试本地Ollama(可选)
    # test_ollama_local()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)

    print("\n💡 关键点:")
    print("1. LangChain支持多种模型,切换非常简单")
    print("2. 只需修改初始化参数,业务代码无需改动")
    print("3. 这就是LangChain的核心价值之一:模型互换性")