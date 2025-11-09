"""
LCEL基础示例 - LangChain Expression Language核心用法

学习目标:
1. 理解LCEL的核心理念
2. 掌握使用 | 操作符组合组件
3. 学会Runnable协议的基本用法
4. 实现常见的LCEL模式
"""
from dotenv import load_dotenv

load_dotenv()


def demo_basic_lcel():
    """LCEL基础 - 管道操作符"""
    print("=" * 60)
    print("1. LCEL基础 - Prompt | LLM | Parser")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    # 传统方式
    print("\n传统方式(多步骤):")
    prompt = ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    formatted = prompt.format_messages(topic="程序员")
    response = llm.invoke(formatted)
    output = response.content

    print(f"结果: {output}")

    # LCEL方式
    print("\nLCEL方式(一行搞定):")
    chain = prompt | llm | StrOutputParser()

    output = chain.invoke({"topic": "程序员"})
    print(f"结果: {output}")

    print("\n✅ LCEL优势:")
    print("  - 代码简洁优雅")
    print("  - 易于理解和维护")
    print("  - 自动处理输入输出")


def demo_runnable_methods():
    """Runnable协议的核心方法"""
    print("\n" + "=" * 60)
    print("2. Runnable协议 - 统一接口")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    chain = (
        ChatPromptTemplate.from_template("用一句话介绍{topic}")
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )

    # 方法1: invoke (同步调用)
    print("\n1. invoke() - 同步调用:")
    result = chain.invoke({"topic": "LangChain"})
    print(f"结果: {result}")

    # 方法2: batch (批量处理)
    print("\n2. batch() - 批量处理:")
    results = chain.batch([
        {"topic": "Python"},
        {"topic": "JavaScript"},
        {"topic": "Rust"}
    ])
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r}")

    # 方法3: stream (流式输出)
    print("\n3. stream() - 流式输出:")
    print("结果: ", end="", flush=True)
    for chunk in chain.stream({"topic": "AI"}):
        print(chunk, end="", flush=True)
    print()

    print("\n✅ Runnable协议统一了:")
    print("  - invoke: 同步调用")
    print("  - batch: 批量处理")
    print("  - stream: 流式输出")
    print("  - ainvoke: 异步调用")
    print("  - astream: 异步流式")


def demo_multi_step_chain():
    """多步骤LCEL链"""
    print("\n" + "=" * 60)
    print("3. 多步骤LCEL链")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 步骤1: 生成大纲
    outline_prompt = ChatPromptTemplate.from_template(
        "为关于{topic}的文章写一个3点大纲"
    )
    outline_chain = outline_prompt | llm | StrOutputParser()

    # 步骤2: 扩展第一点
    expand_prompt = ChatPromptTemplate.from_template(
        "将以下要点扩展成一段话:\n{outline}"
    )

    # 组合两个步骤
    full_chain = (
        outline_chain
        | (lambda x: {"outline": x.split('\n')[0]})  # 取第一点
        | expand_prompt
        | llm
        | StrOutputParser()
    )

    print("\n执行多步骤链:")
    result = full_chain.invoke({"topic": "人工智能"})
    print(f"\n扩展后的段落:\n{result}")

    print("\n✅ 多步骤链的要点:")
    print("  - 使用 | 连接多个步骤")
    print("  - 中间可以插入lambda函数转换")
    print("  - 数据自动流转")


def demo_runnable_passthrough():
    """RunnablePassthrough - 传递输入"""
    print("\n" + "=" * 60)
    print("4. RunnablePassthrough - 保留原始输入")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    prompt = ChatPromptTemplate.from_template("""
基于以下信息回答问题:
姓名: {name}
年龄: {age}
职业: {job}

问题: {question}

回答:""")

    chain = (
        {
            "name": lambda x: x["name"],
            "age": lambda x: x["age"],
            "job": lambda x: x["job"],
            "question": RunnablePassthrough()  # 传递整个输入
        }
        | prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )

    # 简化写法
    simplified_chain = (
        {
            "name": lambda x: x["name"],
            "age": lambda x: x["age"],
            "job": lambda x: x["job"],
            "question": lambda x: x["question"]
        }
        | prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )

    result = simplified_chain.invoke({
        "name": "张三",
        "age": "30",
        "job": "工程师",
        "question": "这个人的职业是什么?"
    })

    print(f"\n结果: {result}")

    print("\n✅ RunnablePassthrough用途:")
    print("  - 将输入原样传递")
    print("  - 保留部分输入字段")
    print("  - 与其他数据组合")


def demo_runnable_parallel():
    """RunnableParallel - 并行执行"""
    print("\n" + "=" * 60)
    print("5. RunnableParallel - 并行执行多任务")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableParallel
    import time

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # 创建3个独立的链
    joke_chain = (
        ChatPromptTemplate.from_template("讲一个关于{topic}的笑话")
        | llm | StrOutputParser()
    )

    poem_chain = (
        ChatPromptTemplate.from_template("写一首关于{topic}的诗")
        | llm | StrOutputParser()
    )

    fact_chain = (
        ChatPromptTemplate.from_template("说一个关于{topic}的事实")
        | llm | StrOutputParser()
    )

    # 并行执行
    parallel_chain = RunnableParallel(
        joke=joke_chain,
        poem=poem_chain,
        fact=fact_chain
    )

    print("\n并行执行3个任务:")
    start = time.time()
    results = parallel_chain.invoke({"topic": "人工智能"})
    duration = time.time() - start

    print(f"\n笑话:\n{results['joke']}")
    print(f"\n诗歌:\n{results['poem']}")
    print(f"\n事实:\n{results['fact']}")
    print(f"\n执行时间: {duration:.2f}秒")

    print("\n✅ 并行执行的优势:")
    print("  - 节省时间")
    print("  - 独立任务同时处理")
    print("  - 自动聚合结果")


def demo_simple_rag_with_lcel():
    """简化的RAG模式"""
    print("\n" + "=" * 60)
    print("6. LCEL实现简单RAG")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    # 模拟知识库
    knowledge_base = {
        "langchain": "LangChain是一个用于开发大语言模型应用的框架",
        "lcel": "LCEL是LangChain Expression Language的缩写",
        "memory": "Memory让LLM能够记住对话历史"
    }

    # 简单检索函数
    def retrieve(question: str) -> str:
        """根据问题检索相关知识"""
        question_lower = question.lower()
        for key, value in knowledge_base.items():
            if key in question_lower:
                return value
        return "没有找到相关信息"

    # RAG链
    prompt = ChatPromptTemplate.from_template("""
基于以下上下文回答问题:

上下文: {context}

问题: {question}

回答:""")

    rag_chain = (
        {
            "context": lambda x: retrieve(x["question"]),
            "question": RunnablePassthrough()
        }
        | (lambda x: {"context": x["context"], "question": x["question"]})
        | prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )

    questions = [
        "什么是LangChain?",
        "LCEL是什么意思?",
        "Memory有什么用?"
    ]

    for q in questions:
        result = rag_chain.invoke({"question": q})
        print(f"\n问题: {q}")
        print(f"回答: {result}")

    print("\n✅ RAG模式要点:")
    print("  - 检索相关上下文")
    print("  - 传递问题")
    print("  - 结合上下文生成答案")


if __name__ == "__main__":
    print("⛓️ LCEL基础示例\n")

    # 运行所有示例
    demo_basic_lcel()
    demo_runnable_methods()
    demo_multi_step_chain()
    demo_runnable_passthrough()
    demo_runnable_parallel()
    demo_simple_rag_with_lcel()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. LCEL核心理念:
   - 使用 | 操作符连接组件
   - 数据自动流转
   - 代码简洁优雅

2. Runnable协议:
   ✅ invoke: 同步调用
   ✅ batch: 批量处理
   ✅ stream: 流式输出
   ✅ ainvoke: 异步调用

3. 基本模式:
   - prompt | llm
   - prompt | llm | parser
   - step1 | step2 | step3

4. 核心组件:
   - RunnablePassthrough: 传递输入
   - RunnableParallel: 并行执行
   - Lambda: 转换数据

5. 最佳实践:
   ✅ 保持链的简洁
   ✅ 合理使用并行
   ✅ 善用lambda转换
   ✅ 模块化组织

6. 下一步:
   → 条件路由(RunnableBranch)
   → 失败回退(with_fallbacks)
   → 复杂工作流
    """)