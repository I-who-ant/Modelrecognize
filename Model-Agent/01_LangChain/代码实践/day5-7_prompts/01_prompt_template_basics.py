"""
PromptTemplate基础示例

学习目标:
1. 掌握PromptTemplate的创建方法
2. 理解变量替换和验证
3. 学会基础和高级用法
"""
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def demo_basic_template():
    """基础模板示例"""
    print("=" * 60)
    print("1. 基础PromptTemplate")
    print("=" * 60)

    # 方式1: from_template (推荐，简洁)
    template1 = PromptTemplate.from_template(
        "Tell me a {adjective} joke about {content}"
    )

    # 方式2: 完整定义
    template2 = PromptTemplate(
        input_variables=["adjective", "content"],
        template="Tell me a {adjective} joke about {content}"
    )

    # 使用模板
    prompt = template1.format(adjective="funny", content="programming")
    print(f"\n生成的Prompt:\n{prompt}\n")

    # 直接使用LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
    response = llm.invoke(prompt)
    print(f"LLM回复:\n{response.content}")


def demo_variable_validation():
    """变量验证示例"""
    print("\n" + "=" * 60)
    print("2. 变量验证")
    print("=" * 60)

    template = PromptTemplate(
        input_variables=["name", "age", "city"],
        template="My name is {name}, I am {age} years old, and I live in {city}."
    )

    # ✅ 正确使用
    print("\n✅ 正确使用:")
    prompt = template.format(name="张三", age=25, city="北京")
    print(prompt)

    # ❌ 错误使用示例
    print("\n❌ 错误使用演示:")
    try:
        template.format(name="张三", age=25)  # 缺少city
    except KeyError as e:
        print(f"缺少变量错误: {e}")

    try:
        # 注意: LangChain不会报多余变量的错
        prompt = template.format(name="张三", age=25, city="北京", country="中国")
        print(f"多余变量(会忽略): {prompt}")
    except Exception as e:
        print(f"错误: {e}")


def demo_partial_variables():
    """部分变量填充"""
    print("\n" + "=" * 60)
    print("3. 部分变量(Partial Variables)")
    print("=" * 60)

    # 场景：有些变量是固定的，可以预先填充
    template = PromptTemplate(
        input_variables=["topic", "language", "length"],
        template="Write a {length} word article about {topic} in {language}"
    )

    # 预填充语言和长度
    chinese_template = template.partial(language="Chinese", length=200)

    # 使用时只需提供topic
    prompt = chinese_template.format(topic="AI")
    print(f"\n预填充后使用:\n{prompt}")

    # 使用函数动态获取值
    from datetime import datetime

    template_with_date = PromptTemplate(
        input_variables=["task"],
        template="Today is {date}, please {task}",
        partial_variables={
            "date": lambda: datetime.now().strftime("%Y-%m-%d")
        }
    )

    prompt = template_with_date.format(task="summarize the news")
    print(f"\n动态获取日期:\n{prompt}")


def demo_template_composition():
    """模板组合"""
    print("\n" + "=" * 60)
    print("4. 模板组合")
    print("=" * 60)

    # 定义子模板
    intro_template = PromptTemplate.from_template(
        "You are a {role}."
    )

    task_template = PromptTemplate.from_template(
        "Your task is to {task}."
    )

    # 手动组合
    full_template = PromptTemplate.from_template(
        """{intro}

{task}

Input: {input}
Output:"""
    )

    # 使用
    intro = intro_template.format(role="translator")
    task = task_template.format(task="translate English to Chinese")
    final_prompt = full_template.format(
        intro=intro,
        task=task,
        input="Hello World"
    )

    print(f"组合后的Prompt:\n{final_prompt}")


def demo_template_formats():
    """不同的模板格式"""
    print("\n" + "=" * 60)
    print("5. 模板格式")
    print("=" * 60)

    # f-string格式(默认)
    template_f = PromptTemplate(
        input_variables=["name"],
        template="Hello {name}!",
        template_format="f-string"
    )

    # jinja2格式(支持条件和循环)
    template_jinja = PromptTemplate(
        input_variables=["name", "items"],
        template="""
Hello {{name}}!

{% if items %}
Your items:
{% for item in items %}
- {{item}}
{% endfor %}
{% endif %}
        """,
        template_format="jinja2"
    )

    print("\nf-string格式:")
    print(template_f.format(name="张三"))

    print("\njinja2格式(支持条件和循环):")
    print(template_jinja.format(
        name="李四",
        items=["Apple", "Banana", "Orange"]
    ))


def demo_multiline_template():
    """多行模板最佳实践"""
    print("\n" + "=" * 60)
    print("6. 多行模板")
    print("=" * 60)

    # 使用三引号定义清晰的多行模板
    template = PromptTemplate.from_template(
        """You are a professional {role}.

Your expertise includes:
- {skill_1}
- {skill_2}
- {skill_3}

Task: {task}

Requirements:
1. Be concise and clear
2. Use examples when helpful
3. Provide actionable advice

Question: {question}

Your answer:"""
    )

    prompt = template.format(
        role="Python Developer",
        skill_1="Web Development",
        skill_2="Data Analysis",
        skill_3="Machine Learning",
        task="Code Review",
        question="How to optimize this function?"
    )

    print(prompt)


if __name__ == "__main__":
    print("📝 LangChain PromptTemplate 完整示例\n")

    # 运行所有示例
    demo_basic_template()
    demo_variable_validation()
    demo_partial_variables()
    demo_template_composition()
    demo_template_formats()
    demo_multiline_template()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 创建方法:
   - from_template(): 简洁，推荐
   - PromptTemplate(): 完整定义

2. 变量使用:
   - 使用{}包裹变量名
   - LangChain会自动验证必需变量
   - 支持partial部分填充

3. 模板格式:
   - f-string: 默认，简单变量替换
   - jinja2: 支持条件、循环等逻辑

4. 最佳实践:
   - 使用三引号定义多行模板
   - 给变量起描述性名称
   - 添加清晰的指令和要求
   - 考虑使用partial预填充常量

5. 优势:
   ✅ 集中管理Prompt
   ✅ 避免字符串拼接
   ✅ 易于测试和维护
   ✅ 支持版本控制
    """)