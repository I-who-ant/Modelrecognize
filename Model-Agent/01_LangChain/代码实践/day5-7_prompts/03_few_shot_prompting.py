"""
Few-Shot Prompting示例

学习目标:
1. 理解Few-Shot Learning的原理
2. 掌握FewShotPromptTemplate的使用
3. 学会动态示例选择
"""
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate,
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def demo_basic_few_shot():
    """基础Few-Shot示例"""
    print("=" * 60)
    print("1. 基础Few-Shot")
    print("=" * 60)

    # 定义示例
    examples = [
        {
            "question": "什么是Python?",
            "answer": "Python是一门解释型、面向对象的编程语言，以简洁易读著称。"
        },
        {
            "question": "什么是JavaScript?",
            "answer": "JavaScript是一门主要用于Web开发的脚本语言，可以在浏览器中运行。"
        },
        {
            "question": "什么是Java?",
            "answer": "Java是一门编译型、面向对象的编程语言，以"一次编写，到处运行"闻名。"
        }
    ]

    # 定义示例格式模板
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="问题: {question}\n答案: {answer}"
    )

    # 创建Few-Shot模板
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="你是一个编程语言专家。请用一句话简洁地回答问题。\n",
        suffix="\n问题: {input}\n答案:",
        input_variables=["input"]
    )

    # 使用
    prompt = few_shot_prompt.format(input="什么是Rust?")
    print(prompt)
    print("\n" + "-" * 60)

    # 调用LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(prompt)
    print(f"\nLLM回复:\n{response.content}")


def demo_chat_few_shot():
    """Chat模式的Few-Shot"""
    print("\n" + "=" * 60)
    print("2. Chat模式Few-Shot")
    print("=" * 60)

    # 定义示例(对话格式)
    examples = [
        {
            "input": "2 + 2",
            "output": "4"
        },
        {
            "input": "5 * 3",
            "output": "15"
        },
        {
            "input": "10 - 7",
            "output": "3"
        }
    ]

    # 定义示例模板
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}")
    ])

    # 创建Few-Shot Chat模板
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )

    # 完整的对话模板
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个计算器。只输出数字结果，不要解释。"),
        few_shot_prompt,
        ("human", "{input}")
    ])

    # 使用
    messages = final_prompt.format_messages(input="8 + 6")

    print("\n生成的对话:")
    for msg in messages:
        role = msg.__class__.__name__.replace("Message", "")
        print(f"[{role}] {msg.content}")

    # 调用LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(messages)
    print(f"\n计算结果: {response.content}")


def demo_dynamic_few_shot():
    """动态Few-Shot(示例选择器)"""
    print("\n" + "=" * 60)
    print("3. 动态Few-Shot(根据输入选择示例)")
    print("=" * 60)

    from langchain_core.example_selectors import (
        SemanticSimilarityExampleSelector
    )
    from langchain_community.vectorstores import Chroma

    # 准备大量示例
    examples = [
        {"input": "快乐", "output": "悲伤"},
        {"input": "高", "output": "低"},
        {"input": "炎热", "output": "寒冷"},
        {"input": "聪明", "output": "愚蠢"},
        {"input": "胖", "output": "瘦"},
        {"input": "美丽", "output": "丑陋"},
        {"input": "强大", "output": "弱小"},
        {"input": "快速", "output": "缓慢"},
    ]

    # 创建示例选择器(基于语义相似度)
    try:
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            Chroma,
            k=2  # 选择最相关的2个示例
        )

        # 创建动态Few-Shot模板
        dynamic_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=PromptTemplate(
                input_variables=["input", "output"],
                template="输入: {input}\n输出: {output}"
            ),
            prefix="给出下列词的反义词:\n",
            suffix="\n输入: {adjective}\n输出:",
            input_variables=["adjective"]
        )

        # 测试不同输入
        test_inputs = ["大", "光明", "勇敢"]

        for test_input in test_inputs:
            print(f"\n输入词: {test_input}")
            prompt = dynamic_prompt.format(adjective=test_input)
            print(f"选择的示例和生成的Prompt:\n{prompt}")
            print("-" * 40)

    except Exception as e:
        print(f"动态示例选择需要额外依赖: {e}")
        print("请安装: pip install chromadb")


def demo_length_based_selector():
    """基于长度的示例选择"""
    print("\n" + "=" * 60)
    print("4. 基于长度的示例选择")
    print("=" * 60)

    from langchain_core.example_selectors import LengthBasedExampleSelector

    # 准备示例
    examples = [
        {"input": "hi", "output": "你好"},
        {"input": "good morning", "output": "早上好"},
        {"input": "how are you doing today?", "output": "你今天怎么样?"},
        {"input": "what is your name and where are you from?", "output": "你叫什么名字，来自哪里?"}
    ]

    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    )

    # 创建长度选择器
    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=50  # Token限制
    )

    # 创建模板
    dynamic_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="Translate English to Chinese:\n",
        suffix="\nInput: {input}\nOutput:",
        input_variables=["input"]
    )

    # 短输入(会包含更多示例)
    print("\n短输入:")
    short_prompt = dynamic_prompt.format(input="hello")
    print(short_prompt)
    print(f"示例数: {short_prompt.count('Input:') - 1}")

    # 长输入(会减少示例数量)
    print("\n长输入:")
    long_prompt = dynamic_prompt.format(
        input="This is a very long sentence that will reduce the number of examples included"
    )
    print(long_prompt)
    print(f"示例数: {long_prompt.count('Input:') - 1}")


def demo_custom_example_selector():
    """自定义示例选择器"""
    print("\n" + "=" * 60)
    print("5. 自定义示例选择器")
    print("=" * 60)

    from langchain_core.example_selectors.base import BaseExampleSelector
    from typing import Dict, List

    class CustomExampleSelector(BaseExampleSelector):
        """自定义：根据输入长度选择示例"""

        def __init__(self, examples: List[Dict[str, str]]):
            self.examples = examples

        def add_example(self, example: Dict[str, str]) -> None:
            self.examples.append(example)

        def select_examples(self, input_variables: Dict[str, str]) -> List[Dict]:
            # 自定义逻辑：根据输入长度选择
            input_text = input_variables.get("input", "")
            input_length = len(input_text)

            if input_length < 10:
                return self.examples[:3]  # 短输入，多示例
            elif input_length < 20:
                return self.examples[:2]  # 中等输入
            else:
                return self.examples[:1]  # 长输入，少示例

    # 使用自定义选择器
    examples = [
        {"input": "cat", "output": "猫"},
        {"input": "dog", "output": "狗"},
        {"input": "bird", "output": "鸟"},
        {"input": "fish", "output": "鱼"}
    ]

    selector = CustomExampleSelector(examples)

    template = FewShotPromptTemplate(
        example_selector=selector,
        example_prompt=PromptTemplate(
            input_variables=["input", "output"],
            template="{input} -> {output}"
        ),
        prefix="翻译:\n",
        suffix="\n{input} -> ",
        input_variables=["input"]
    )

    # 测试
    print("\n短输入(< 10字符):")
    print(template.format(input="apple"))

    print("\n中等输入(10-20字符):")
    print(template.format(input="beautiful day"))

    print("\n长输入(> 20字符):")
    print(template.format(input="this is a very long sentence"))


if __name__ == "__main__":
    print("🎓 Few-Shot Prompting 完整示例\n")

    # 运行所有示例
    demo_basic_few_shot()
    demo_chat_few_shot()
    demo_dynamic_few_shot()
    demo_length_based_selector()
    demo_custom_example_selector()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. Few-Shot Learning:
   - 通过示例引导模型行为
   - 比Zero-Shot效果更稳定
   - 适合格式化输出和风格保持

2. 示例选择策略:
   ✅ 静态: 固定示例(简单场景)
   ✅ 语义相似度: 选择最相关示例(需要embedding)
   ✅ 长度限制: 根据Token限制调整示例数
   ✅ 自定义: 自己实现选择逻辑

3. 使用场景:
   - 需要特定格式输出
   - 需要保持特定风格
   - Zero-Shot效果不佳
   - 复杂的转换任务

4. 最佳实践:
   - 示例要有代表性
   - 示例格式要一致
   - 3-5个示例通常够用
   - 考虑Token成本

5. 注意事项:
   ⚠️ Few-Shot会增加Token消耗
   ⚠️ 示例质量很重要
   ⚠️ 动态选择需要额外依赖
   ⚠️ 要有fallback策略

6. 何时使用:
   ✅ 输出格式复杂
   ✅ 需要特定风格
   ✅ 分类/转换任务
   ❌ 简单问答(Zero-Shot就够)
   ❌ Token预算紧张
    """)