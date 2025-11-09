"""
ChatPromptTemplate示例

学习目标:
1. 掌握ChatPromptTemplate的使用
2. 理解多种消息类型的组合
3. 学会构建对话模板
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def demo_basic_chat_template():
    """基础ChatPromptTemplate"""
    print("=" * 60)
    print("1. 基础ChatPromptTemplate")
    print("=" * 60)

    # 方式1: 使用字符串元组(推荐)
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，你的专长是{specialty}"),
        ("human", "{question}")
    ])

    # 生成消息
    messages = template.format_messages(
        role="Python导师",
        specialty="用简单语言解释复杂概念",
        question="什么是装饰器?"
    )

    print("\n生成的消息列表:")
    for msg in messages:
        print(f"  {msg.__class__.__name__}: {msg.content}")

    # 直接使用LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    response = llm.invoke(messages)
    print(f"\nLLM回复:\n{response.content}")


def demo_message_types():
    """演示所有消息类型"""
    print("\n" + "=" * 60)
    print("2. 各种消息类型")
    print("=" * 60)

    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}"),
        ("human", "你好！"),
        ("ai", "你好！有什么我可以帮助你的吗？"),
        ("human", "{question}")
    ])

    messages = template.format_messages(
        role="客服助手",
        question="我想了解你们的产品"
    )

    print("\n对话历史:")
    for i, msg in enumerate(messages, 1):
        role = msg.__class__.__name__.replace("Message", "")
        print(f"{i}. [{role}] {msg.content}")


def demo_detailed_template():
    """使用消息模板类(详细控制)"""
    print("\n" + "=" * 60)
    print("3. 使用消息模板类")
    print("=" * 60)

    # 使用专门的消息模板类
    system_template = SystemMessagePromptTemplate.from_template( # 系统消息模板,用于设置模型行为
        """你是{role}，具有以下特点:
- 性格: {personality}
- 风格: {style}
- 专长: {expertise}"""
    )

    human_template = HumanMessagePromptTemplate.from_template( # 人类消息模板,用于用户输入
        "{user_input}"
    )

    template = ChatPromptTemplate.from_messages([ # 对话模板,将系统消息和人类消息组合起来
        system_template,
        human_template
    ])

    messages = template.format_messages( # 格式化消息,将模板中的变量替换为实际值
        role="AI助手",
        personality="友好、耐心",
        style="通俗易懂",
        expertise="技术解释",
        user_input="请解释什么是闭包"
    )

    print("\n详细配置的消息:")
    for msg in messages:
        print(f"\n{msg.__class__.__name__}:")
        print(msg.content)


def demo_multi_turn_conversation():
    """多轮对话模板"""
    print("\n" + "=" * 60)
    print("4. 多轮对话模板")
    print("=" * 60)

    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{subject}老师"),
        ("human", "什么是{concept_1}?"),
        ("ai", "让我来解释一下{concept_1}..."),
        ("human", "那{concept_2}呢?"),
        ("ai", "{concept_2}与{concept_1}有关..."),
        ("human", "{final_question}")
    ])

    messages = template.format_messages(
        subject="Python",
        concept_1="变量",
        concept_2="数据类型",
        final_question="能举个例子吗?"
    )

    print("\n对话流程:")
    for i, msg in enumerate(messages, 1):
        role_map = {
            "SystemMessage": "系统",
            "HumanMessage": "学生",
            "AIMessage": "老师"
        }
        role = role_map.get(msg.__class__.__name__, "未知")
        print(f"\n{i}. {role}:")
        print(f"   {msg.content}")


def demo_dynamic_messages():
    """动态构建消息列表"""
    print("\n" + "=" * 60)
    print("5. 动态构建消息")
    print("=" * 60)

    def build_conversation_template(history: list, system_msg: str):
        """根据对话历史动态构建模板"""
        messages = [("system", system_msg)]

        # 添加历史对话
        for turn in history:
            messages.append(("human", turn["user"]))
            messages.append(("ai", turn["assistant"]))

        # 添加当前问题
        messages.append(("human", "{current_question}"))

        return ChatPromptTemplate.from_messages(messages)

    # 模拟对话历史
    history = [
        {"user": "你好", "assistant": "你好！有什么可以帮你的?"},
        {"user": "我想学Python", "assistant": "很好！从哪里开始呢?"}
    ]

    template = build_conversation_template(
        history,
        "你是一个Python导师"
    )

    messages = template.format_messages(
        current_question="从基础语法开始吧"
    )

    print("\n动态构建的对话:")
    for msg in messages:
        print(f"{msg.__class__.__name__}: {msg.content[:50]}...")


def demo_conditional_template():
    """条件模板(使用jinja2)"""
    print("\n" + "=" * 60)
    print("6. 条件模板")
    print("=" * 60)

    from langchain_core.prompts import PromptTemplate

    # 使用jinja2实现条件逻辑
    system_template = PromptTemplate(
        input_variables=["role", "has_context", "context"],
        template="""你是一个{role}。

{% if has_context %}
相关背景信息:
{{context}}

请基于以上信息回答问题。
{% else %}
请基于你的知识回答问题。
{% endif %}""",
        template_format="jinja2"
    )

    # 有上下文的情况
    print("\n✅ 有上下文:")
    prompt_with_context = system_template.format(
        role="历史学家",
        has_context=True,
        context="明朝建立于1368年，由朱元璋建立。"
    )
    print(prompt_with_context)

    # 无上下文的情况
    print("\n❌ 无上下文:")
    prompt_without_context = system_template.format(
        role="历史学家",
        has_context=False,
        context=""
    )
    print(prompt_without_context)


def demo_structured_output_template():
    """结构化输出的聊天模板"""
    print("\n" + "=" * 60)
    print("7. 结构化输出模板")
    print("=" * 60)

    template = ChatPromptTemplate.from_messages([
        ("system", """你是一个数据分析助手。

请按以下JSON格式输出:
{{
    "summary": "一句话总结",
    "key_points": ["要点1", "要点2", "要点3"],
    "recommendation": "建议"
}}"""),
        ("human", "{data_description}")
    ])

    messages = template.format_messages(
        data_description="分析这个月的销售数据: 总销售额100万，同比增长20%，新客户占30%"
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(messages)

    print("\n数据分析结果:")
    print(response.content)


if __name__ == "__main__":
    print("💬 ChatPromptTemplate 完整示例\n")

    # 运行所有示例
    demo_basic_chat_template()
    demo_message_types()
    demo_detailed_template()
    demo_multi_turn_conversation()
    demo_dynamic_messages()
    demo_conditional_template()
    demo_structured_output_template()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. ChatPromptTemplate vs PromptTemplate:
   - ChatPromptTemplate: 用于Chat Models，支持多种消息类型
   - PromptTemplate: 用于LLMs，只是字符串

2. 消息类型:
   - system: 设定AI角色和行为
   - human/user: 用户输入
   - ai/assistant: AI回复

3. 创建方式:
   方式1(推荐): from_messages([("system", "..."), ("human", "...")])
   方式2: 使用专门的消息模板类

4. 使用场景:
   ✅ 对话系统
   ✅ 多轮交互
   ✅ 需要角色设定
   ✅ 上下文管理

5. 最佳实践:
   - system消息设定清晰的角色
   - 使用对话历史提供上下文
   - 结构化system指令
   - 动态构建消息列表

6. 注意事项:
   - 消息顺序很重要
   - system消息通常放在最前面
   - 可以有多个human-ai往返
    """)