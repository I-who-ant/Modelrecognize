"""
Token追踪示例

学习目标:
1. 掌握多种Token追踪方法
2. 理解Token计算和成本估算
3. 学会在生产环境中控制API成本
"""
from langchain_openai import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict
from dotenv import load_dotenv
import tiktoken

load_dotenv()


def count_tokens_manual(text: str, model: str = "gpt-3.5-turbo") -> int:
    """手动计算Token数量"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except KeyError:
        # 如果模型不支持,使用默认编码
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def demo_basic_tracking():
    """演示基础Token追踪"""
    print("=" * 60)
    print("方法1: 从响应元数据获取Token信息")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # 发送请求
    response = llm.invoke("用一句话介绍LangChain")

    # 获取Token使用情况
    usage = response.response_metadata.get("token_usage", {})

    print(f"\n问题: 用一句话介绍LangChain")
    print(f"回答: {response.content}\n")

    print("Token使用情况:")
    print(f"  Prompt Tokens: {usage.get('prompt_tokens', 0)}")
    print(f"  Completion Tokens: {usage.get('completion_tokens', 0)}")
    print(f"  Total Tokens: {usage.get('total_tokens', 0)}")


def demo_callback_tracking():
    """演示使用回调函数追踪Token"""
    print("\n" + "=" * 60)
    print("方法2: 使用回调函数追踪多次调用")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    with get_openai_callback() as cb:
        # 多次调用
        llm.invoke("什么是LangChain?")
        llm.invoke("它有什么优势?")
        llm.invoke("如何开始使用?")

        # 统计信息
        print("\n累计统计:")
        print(f"  Total Tokens: {cb.total_tokens}")
        print(f"  Prompt Tokens: {cb.prompt_tokens}")
        print(f"  Completion Tokens: {cb.completion_tokens}")
        print(f"  Total Cost (USD): ${cb.total_cost:.6f}")
        print(f"  Successful Requests: {cb.successful_requests}")


class DetailedTokenCounter(BaseCallbackHandler):
    """自定义Token计数器回调"""

    def __init__(self):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.request_count = 0
        self.request_details = []

    def on_llm_start(self, serialized: Dict[str, Any], prompts: list, **kwargs) -> None:
        """LLM开始调用时"""
        self.request_count += 1
        print(f"\n📤 请求 #{self.request_count} 开始...")

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """LLM调用结束时"""
        if hasattr(response, 'llm_output') and response.llm_output:
            token_usage = response.llm_output.get('token_usage', {})

            prompt = token_usage.get('prompt_tokens', 0)
            completion = token_usage.get('completion_tokens', 0)
            total = token_usage.get('total_tokens', 0)

            self.prompt_tokens += prompt
            self.completion_tokens += completion
            self.total_tokens += total

            # 记录详情
            self.request_details.append({
                'request': self.request_count,
                'prompt_tokens': prompt,
                'completion_tokens': completion,
                'total_tokens': total
            })

            print(f"✅ 请求 #{self.request_count} 完成 - Tokens: {total}")

    def report(self):
        """输出详细报告"""
        print("\n" + "=" * 60)
        print("Token使用详细报告")
        print("=" * 60)

        print(f"\n总请求数: {self.request_count}")
        print(f"总Token数: {self.total_tokens}")
        print(f"  - Prompt Tokens: {self.prompt_tokens}")
        print(f"  - Completion Tokens: {self.completion_tokens}")

        # 计算成本(GPT-3.5-turbo价格)
        cost = (self.prompt_tokens * 0.5 + self.completion_tokens * 1.5) / 1_000_000
        print(f"\n预估成本: ${cost:.6f}")

        print("\n各请求详情:")
        for detail in self.request_details:
            print(f"  请求 #{detail['request']}: "
                  f"Prompt={detail['prompt_tokens']}, "
                  f"Completion={detail['completion_tokens']}, "
                  f"Total={detail['total_tokens']}")


def demo_custom_callback():
    """演示自定义回调"""
    print("\n" + "=" * 60)
    print("方法3: 自定义Token追踪回调")
    print("=" * 60)

    counter = DetailedTokenCounter()
    llm = ChatOpenAI(model="gpt-3.5-turbo", callbacks=[counter])

    questions = [
        "什么是机器学习?",
        "什么是深度学习?",
        "什么是强化学习?"
    ]

    for q in questions:
        llm.invoke(q)

    # 输出报告
    counter.report()


def estimate_cost(prompt_tokens: int, completion_tokens: int,
                 model: str = "gpt-3.5-turbo") -> float:
    """估算API调用成本"""
    # 价格表(每百万Token的美元价格)
    prices = {
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }

    price = prices.get(model, prices["gpt-3.5-turbo"])
    cost = (prompt_tokens * price["input"] +
            completion_tokens * price["output"]) / 1_000_000
    return cost


def demo_cost_estimation():
    """演示成本估算"""
    print("\n" + "=" * 60)
    print("成本估算工具")
    print("=" * 60)

    # 模拟Token使用
    scenarios = [
        {"name": "短对话", "prompt": 100, "completion": 50},
        {"name": "中等对话", "prompt": 500, "completion": 300},
        {"name": "长文生成", "prompt": 1000, "completion": 2000},
    ]

    models = ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]

    print("\n不同场景的成本对比:\n")

    for scenario in scenarios:
        print(f"{scenario['name']}:")
        print(f"  Prompt Tokens: {scenario['prompt']}")
        print(f"  Completion Tokens: {scenario['completion']}")

        for model in models:
            cost = estimate_cost(
                scenario['prompt'],
                scenario['completion'],
                model
            )
            print(f"  {model:20s}: ${cost:.6f}")
        print()


def demo_manual_token_counting():
    """演示手动Token计算"""
    print("=" * 60)
    print("手动Token计算")
    print("=" * 60)

    texts = [
        "Hello, world!",
        "LangChain是一个强大的框架",
        "人工智能正在改变世界"
    ]

    print("\nToken计算结果:\n")

    for text in texts:
        tokens = count_tokens_manual(text)
        print(f"文本: {text}")
        print(f"Token数量: {tokens}")
        print(f"平均每字符Token: {tokens/len(text):.2f}\n")


def demo_optimize_cost():
    """演示成本优化技巧"""
    print("\n" + "=" * 60)
    print("成本优化技巧")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    print("\n技巧1: 限制max_tokens减少输出长度")
    with get_openai_callback() as cb:
        llm_limited = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=50)
        llm_limited.invoke("详细介绍LangChain框架")
        print(f"限制Token后成本: ${cb.total_cost:.6f}")

    print("\n技巧2: 使用更便宜的模型")
    with get_openai_callback() as cb:
        llm.invoke("LangChain是什么?")
        print(f"gpt-3.5-turbo成本: ${cb.total_cost:.6f}")

    print("\n技巧3: 优化Prompt减少输入Token")
    # 冗长的prompt
    verbose_prompt = "请你用详细的语言,尽可能完整地,不遗漏任何细节地解释什么是LangChain"
    # 简洁的prompt
    concise_prompt = "解释LangChain"

    verbose_tokens = count_tokens_manual(verbose_prompt)
    concise_tokens = count_tokens_manual(concise_prompt)

    print(f"冗长Prompt: {verbose_tokens} tokens")
    print(f"简洁Prompt: {concise_tokens} tokens")
    print(f"节省: {verbose_tokens - concise_tokens} tokens")


if __name__ == "__main__":
    print("📊 LangChain Token追踪完整示例\n")

    # 运行所有示例
    demo_basic_tracking()
    demo_callback_tracking()
    demo_custom_callback()
    demo_cost_estimation()
    demo_manual_token_counting()
    demo_optimize_cost()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. Token追踪方法:
   ✅ 方法1: response.response_metadata['token_usage']
   ✅ 方法2: get_openai_callback() 上下文管理器
   ✅ 方法3: 自定义BaseCallbackHandler回调类

2. 成本控制:
   - 设置max_tokens限制输出
   - 选择性价比高的模型
   - 优化Prompt减少输入Token
   - 使用缓存避免重复调用
   - 实现用户级配额限制

3. Token计算:
   - 使用tiktoken库手动计算
   - 英文: ~4字符 = 1 token
   - 中文: ~1.5-2汉字 = 1 token

4. 生产环境最佳实践:
   - 始终追踪Token使用量
   - 监控异常高的Token消耗
   - 设置预警阈值
   - 定期优化Prompt
   - 考虑使用本地模型降低成本
    """)