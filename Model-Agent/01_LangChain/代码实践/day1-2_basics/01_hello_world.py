"""
LangChain Hello World示例
展示最基本的LLM调用

学习目标:
1. 理解如何初始化LangChain的ChatModel
2. 掌握基本的invoke调用方式
3. 了解响应对象的结构
"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


def main():
    """基础LLM调用示例"""

    print("=" * 50)
    print("LangChain Hello World 示例")
    print("=" * 50)

    # 1. 初始化模型
    # temperature: 控制输出随机性(0=确定性,1=创造性)
    # max_tokens: 限制输出长度
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # 2. 调用模型
    print("\n正在调用LLM...")
    response = llm.invoke("你好,请用3句话介绍一下LangChain框架")

    # 3. 打印结果
    print("\n=== LangChain回复 ===")
    print(response.content)

    # 4. 查看元数据
    print("\n=== 调用信息 ===")
    metadata = response.response_metadata
    print(f"使用的模型: {metadata.get('model_name', 'N/A')}")
    print(f"消耗Token: {metadata.get('token_usage', 'N/A')}")

    # 5. Token详细信息
    if 'token_usage' in metadata:
        usage = metadata['token_usage']
        print(f"  - Prompt Tokens: {usage.get('prompt_tokens', 0)}")
        print(f"  - Completion Tokens: {usage.get('completion_tokens', 0)}")
        print(f"  - Total Tokens: {usage.get('total_tokens', 0)}")


if __name__ == "__main__":
    # 检查API Key是否配置
    if not os.getenv("OPENAI_API_KEY"):
        print("错误: 请先在.env文件中配置OPENAI_API_KEY")
        print("示例: OPENAI_API_KEY=sk-xxx")
        exit(1)

    main()