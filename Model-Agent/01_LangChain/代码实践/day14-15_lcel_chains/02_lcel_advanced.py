"""
LCEL高级应用 - 条件路由、失败回退、复杂工作流

学习目标:
1. 掌握RunnableBranch条件路由
2. 学会使用with_fallbacks处理失败
3. 实现复杂的工作流
4. 掌握LCEL的高级技巧
"""
from dotenv import load_dotenv

load_dotenv()


def demo_runnable_branch():
    """RunnableBranch - 条件路由"""
    print("=" * 60)
    print("1. RunnableBranch - 条件路由")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableBranch

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 定义不同类型的处理链
    translation_chain = (
        ChatPromptTemplate.from_template("将以下文本翻译成中文:\n{text}")
        | llm | StrOutputParser()
    )

    summary_chain = (
        ChatPromptTemplate.from_template("总结以下文本:\n{text}")
        | llm | StrOutputParser()
    )

    qa_chain = (
        ChatPromptTemplate.from_template("回答问题:\n{text}")
        | llm | StrOutputParser()
    )

    # 条件判断函数
    def is_translation(x):
        return "翻译" in x.get("text", "")

    def is_summary(x):
        return "总结" in x.get("text", "")

    # 创建路由链
    branch = RunnableBranch(
        (is_translation, translation_chain),
        (is_summary, summary_chain),
        qa_chain  # 默认链
    )

    print("\n测试不同类型的输入:")

    # 测试1: 翻译请求
    result1 = branch.invoke({"text": "请翻译: Hello World"})
    print(f"\n翻译请求结果: {result1}")

    # 测试2: 总结请求
    result2 = branch.invoke({"text": "请总结: LangChain是一个很好用的框架"})
    print(f"\n总结请求结果: {result2}")

    # 测试3: 问答请求(默认)
    result3 = branch.invoke({"text": "什么是AI?"})
    print(f"\n问答请求结果: {result3}")

    print("\n✅ 条件路由的用途:")
    print("  - 根据输入选择不同处理流程")
    print("  - 实现智能分派")
    print("  - 提高灵活性")


def demo_with_fallbacks():
    """with_fallbacks - 失败回退"""
    print("\n" + "=" * 60)
    print("2. with_fallbacks - 失败回退机制")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    # 主链(可能失败)
    primary_llm = ChatOpenAI(
        model="gpt-4",  # 假设这个可能失败
        temperature=0,
        request_timeout=1  # 短超时,容易失败
    )

    # 备用链
    backup_llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("用一句话介绍{topic}")

    # 创建带回退的链
    chain_with_fallback = (
        prompt
        | primary_llm.with_fallbacks([backup_llm])
        | StrOutputParser()
    )

    print("\n使用带回退的链:")
    try:
        result = chain_with_fallback.invoke({"topic": "LangChain"})
        print(f"结果: {result}")
        print("(如果主模型失败,会自动使用备用模型)")
    except Exception as e:
        print(f"错误: {e}")

    print("\n✅ 失败回退的好处:")
    print("  - 提高系统可靠性")
    print("  - 自动降级处理")
    print("  - 用户无感知")


def demo_complex_workflow():
    """复杂工作流示例"""
    print("\n" + "=" * 60)
    print("3. 复杂工作流 - 内容生成系统")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnableParallel

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # 步骤1: 生成大纲
    outline_chain = (
        ChatPromptTemplate.from_template("为'{topic}'写一个文章大纲(3个要点)")
        | llm | StrOutputParser()
    )

    # 步骤2: 并行生成每个章节
    def generate_sections(outline: str):
        """并行生成所有章节"""
        points = [p.strip() for p in outline.split('\n') if p.strip() and not p.startswith('#')][:3]

        section_chain = (
            ChatPromptTemplate.from_template("扩展以下要点成一段话:\n{point}")
            | llm | StrOutputParser()
        )

        results = section_chain.batch([{"point": p} for p in points])
        return "\n\n".join(results)

    # 步骤3: 生成结论
    conclusion_chain = (
        ChatPromptTemplate.from_template("为以下文章写一个简短结论:\n{content}")
        | llm | StrOutputParser()
    )

    # 组合完整工作流
    full_workflow = (
        outline_chain
        | (lambda x: {"content": generate_sections(x)})
        | (lambda x: x["content"] + "\n\n结论:\n" + conclusion_chain.invoke(x))
    )

    print("\n执行复杂工作流:")
    article = full_workflow.invoke({"topic": "人工智能的未来"})
    print(f"\n生成的文章:\n{article}")

    print("\n✅ 复杂工作流特点:")
    print("  - 多个步骤串联")
    print("  - 并行处理提高效率")
    print("  - 灵活的数据转换")


def demo_conditional_formatting():
    """条件格式化"""
    print("\n" + "=" * 60)
    print("4. 条件格式化 - 动态选择Prompt")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 定义不同风格的prompt
    formal_prompt = ChatPromptTemplate.from_template(
        "请用正式的语气回答:\n{question}"
    )

    casual_prompt = ChatPromptTemplate.from_template(
        "请用轻松随意的语气回答:\n{question}"
    )

    # 动态选择prompt
    def select_prompt(inputs):
        style = inputs.get("style", "casual")
        question = inputs.get("question", "")

        if style == "formal":
            return formal_prompt.invoke({"question": question})
        else:
            return casual_prompt.invoke({"question": question})

    chain = select_prompt | llm | StrOutputParser()

    print("\n测试不同风格:")

    # 正式风格
    result1 = chain.invoke({"style": "formal", "question": "什么是机器学习?"})
    print(f"\n正式风格:\n{result1}")

    # 随意风格
    result2 = chain.invoke({"style": "casual", "question": "什么是机器学习?"})
    print(f"\n随意风格:\n{result2}")

    print("\n✅ 条件格式化用途:")
    print("  - 个性化输出")
    print("  - 适应不同场景")
    print("  - 提高灵活性")


def demo_batch_processing():
    """批量处理优化"""
    print("\n" + "=" * 60)
    print("5. 批量处理 - 性能优化")
    print("=" * 60)

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser
    import time

    chain = (
        ChatPromptTemplate.from_template("用一个词描述{word}")
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        | StrOutputParser()
    )

    words = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]

    # 方法1: 循环调用(慢)
    print("\n方法1: 循环调用")
    start = time.time()
    results1 = []
    for word in words:
        result = chain.invoke({"word": word})
        results1.append(result)
    time1 = time.time() - start
    print(f"结果: {results1}")
    print(f"耗时: {time1:.2f}秒")

    # 方法2: 批量调用(快)
    print("\n方法2: 批量调用")
    start = time.time()
    results2 = chain.batch([{"word": w} for w in words])
    time2 = time.time() - start
    print(f"结果: {results2}")
    print(f"耗时: {time2:.2f}秒")

    print(f"\n批量处理速度提升: {time1/time2:.1f}x")

    print("\n✅ 批量处理优势:")
    print("  - 显著提高效率")
    print("  - 减少网络开销")
    print("  - 适合大量数据处理")


def demo_lcel_best_practices():
    """LCEL最佳实践总结"""
    print("\n" + "=" * 60)
    print("6. LCEL最佳实践")
    print("=" * 60)

    print("""
🎯 LCEL最佳实践指南

1. 保持链的简洁
────────────────
✅ 好的实践:
chain = prompt | llm | parser

❌ 避免:
chain = (
    prompt | llm |
    lambda x: x.content |
    lambda x: x.strip() |
    lambda x: x.lower() |
    # ... 太多转换
)

2. 合理使用并行
────────────────
✅ 独立任务并行:
parallel_chain = RunnableParallel(
    task1=chain1,
    task2=chain2
)

❌ 串行执行独立任务:
result1 = chain1.invoke(input)
result2 = chain2.invoke(input)  # 应该并行

3. 善用条件路由
────────────────
✅ 根据输入类型分派:
branch = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default_chain
)

4. 实现失败处理
────────────────
✅ 使用fallbacks:
chain = primary.with_fallbacks([backup])

✅ 使用重试:
chain = llm.with_retry(stop_after_attempt=3)

5. 批量处理优化
────────────────
✅ 使用batch:
results = chain.batch(inputs)

❌ 避免循环invoke:
for inp in inputs:
    result = chain.invoke(inp)

6. 模块化组织
────────────────
✅ 创建可复用组件:
def create_summary_chain(llm):
    return summary_prompt | llm | parser

✅ 组合使用:
chain = create_summary_chain(llm)

7. 适当的错误处理
────────────────
✅ 关键步骤加try-except:
try:
    result = chain.invoke(input)
except Exception as e:
    result = fallback_chain.invoke(input)

8. 性能监控
────────────────
✅ 使用callbacks:
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke(input)
    print(f"Token: {cb.total_tokens}")

9. 调试技巧
────────────────
✅ 分步执行:
step1 = prompt.invoke(input)
step2 = llm.invoke(step1)
step3 = parser.invoke(step2)

✅ 打印中间结果:
def debug(x):
    print(f"中间值: {x}")
    return x

chain = prompt | llm | debug | parser

10. 文档化
────────────────
✅ 添加注释和文档:
def create_rag_chain(retriever, llm):
    \"\"\"
    创建RAG链

    Args:
        retriever: 文档检索器
        llm: 语言模型

    Returns:
        完整的RAG链
    \"\"\"
    return (
        {"context": retriever, "question": ...}
        | prompt | llm | parser
    )
    """)


if __name__ == "__main__":
    print("🚀 LCEL高级应用示例\n")

    # 运行所有示例
    demo_runnable_branch()
    demo_with_fallbacks()
    demo_complex_workflow()
    demo_conditional_formatting()
    demo_batch_processing()
    demo_lcel_best_practices()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. RunnableBranch:
   - 条件路由
   - 智能分派
   - 灵活处理

2. with_fallbacks:
   - 失败回退
   - 提高可靠性
   - 自动降级

3. 复杂工作流:
   - 多步骤串联
   - 并行处理
   - 灵活转换

4. 性能优化:
   ✅ 使用batch批量处理
   ✅ 并行执行独立任务
   ✅ 合理使用缓存

5. 最佳实践:
   ✅ 保持简洁
   ✅ 模块化组织
   ✅ 错误处理
   ✅ 性能监控
   ✅ 充分文档化

🎓 LCEL学习完成!

你已经掌握了:
- LCEL基础语法
- Runnable协议
- 管道组合
- 条件路由
- 失败回退
- 复杂工作流
- 性能优化

下一步:
→ 实战项目
→ Agent开发
→ 生产部署
    """)