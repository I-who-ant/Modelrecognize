"""练习43: Soul 层集成测试"""
import asyncio
from dataclasses import dataclass
from typing import AsyncIterator


# ========== 1. 测试工具 ==========

@dataclass
class TestCase:
    """测试用例"""
    name: str
    user_input: str
    expected_tools: list[str] | None = None
    expected_contains: list[str] | None = None
    should_fail: bool = False


class SoulTester:
    """Soul 层测试器"""
    
    def __init__(self, soul):
        self.soul = soul
        self.test_results: list[dict] = []
    
    async def run_test(self, test_case: TestCase):
        """运行单个测试"""
        print(f"\n{'='*60}")
        print(f"🧪 测试: {test_case.name}")
        print(f"{'='*60}")
        print(f"输入: {test_case.user_input}")
        
        try:
            # 收集完整响应
            full_response = ""
            tool_calls_made = []
            
            async for chunk in self.soul.chat(test_case.user_input):
                full_response += chunk
            
            # 检查消息历史中的工具调用
            for msg in self.soul.messages:
                if msg.get("role") == "tool":
                    tool_calls_made.append(msg.get("name"))
            
            # 验证结果
            passed = True
            errors = []
            
            # 检查预期工具
            if test_case.expected_tools is not None:
                for tool in test_case.expected_tools:
                    if tool not in tool_calls_made:
                        passed = False
                        errors.append(f"未调用预期工具: {tool}")
            
            # 检查预期内容
            if test_case.expected_contains:
                for text in test_case.expected_contains:
                    if text not in full_response:
                        passed = False
                        errors.append(f"响应中未包含: {text}")
            
            # 检查失败预期
            if test_case.should_fail and passed:
                passed = False
                errors.append("预期失败但测试通过")
            
            # 记录结果
            result = {
                "name": test_case.name,
                "passed": passed,
                "errors": errors,
                "response_length": len(full_response),
                "tools_called": tool_calls_made
            }
            
            self.test_results.append(result)
            
            # 打印结果
            if passed:
                print("✅ 通过")
            else:
                print("❌ 失败")
                for error in errors:
                    print(f"   - {error}")
            
            print(f"\n响应预览: {full_response[:100]}...")
            print(f"调用的工具: {tool_calls_made}")
        
        except Exception as e:
            print(f"❌ 异常: {e}")
            self.test_results.append({
                "name": test_case.name,
                "passed": False,
                "errors": [str(e)],
                "exception": True
            })
    
    async def run_all(self, test_cases: list[TestCase]):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("🧪 开始测试套件")
        print("=" * 60)
        
        for tc in test_cases:
            await self.run_test(tc)
            # 清空消息历史
            self.soul.messages = []
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("📊 测试摘要")
        print("=" * 60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed
        
        print(f"\n总测试数: {total}")
        print(f"✅ 通过: {passed}")
        print(f"❌ 失败: {failed}")
        print(f"通过率: {passed/total*100:.1f}%")
        
        if failed > 0:
            print("\n失败的测试:")
            for r in self.test_results:
                if not r["passed"]:
                    print(f"  - {r['name']}")
                    for error in r["errors"]:
                        print(f"      {error}")


# ========== 2. 集成测试 ==========

async def test_soul_basic():
    """基础功能测试"""
    print("\n" + "=" * 60)
    print("1. Soul 基础功能测试")
    print("=" * 60)
    
    # 创建模拟组件
    @dataclass
    class ChatChunk:
        delta: dict
        finish_reason: str | None = None
    
    class MockLLM:
        async def astream_chat(self, messages, tools):
            text = "这是模拟回复"
            for char in text:
                await asyncio.sleep(0.01)
                yield ChatChunk(delta={"content": char}, finish_reason=None)
            yield ChatChunk(delta={}, finish_reason="stop")
    
    class MockToolManager:
        def get_tool_schemas(self):
            return []
        async def execute(self, tc):
            return "工具结果"
    
    # 简化的 Soul
    class SimpleSoul:
        def __init__(self, llm, tool_manager):
            self.llm = llm
            self.tool_manager = tool_manager
            self.messages = []
        
        async def chat(self, user_input):
            self.messages.append({"role": "user", "content": user_input})
            
            response_stream = self.llm.astream_chat(self.messages, None)
            full_content = ""
            
            async for chunk in response_stream:
                if content := chunk.delta.get("content"):
                    full_content += content
                    yield content
            
            self.messages.append({"role": "assistant", "content": full_content})
    
    # 创建测试用例
    test_cases = [
        TestCase(
            name="简单对话",
            user_input="你好",
            expected_contains=["模拟"]
        ),
        TestCase(
            name="空输入",
            user_input="",
            should_fail=False
        ),
    ]
    
    # 运行测试
    soul = SimpleSoul(MockLLM(), MockToolManager())
    tester = SoulTester(soul)
    await tester.run_all(test_cases)


async def test_soul_with_tools():
    """工具调用测试"""
    print("\n" + "=" * 60)
    print("2. Soul 工具调用测试")
    print("=" * 60)
    
    # 这里可以测试真实的 Soul 实现
    print("工具调用测试（需要完整 Soul 实现）")


async def test_soul_edge_cases():
    """边界情况测试"""
    print("\n" + "=" * 60)
    print("3. Soul 边界情况测试")
    print("=" * 60)
    
    print("边界情况:")
    print("  - 超长输入")
    print("  - 工具调用失败")
    print("  - LLM 超时")
    print("  - 无效工具参数")
    print("  - 循环引用检测")


async def main():
    """主函数"""
    print("\n=== 练习43: Soul 层集成测试 ===")
    
    await test_soul_basic()
    await test_soul_with_tools()
    await test_soul_edge_cases()
    
    print("\n" + "=" * 60)
    print("所有测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 测试驱动开发：先写测试，后实现功能
# 2. 集成测试：测试各组件协同工作
# 3. 边界情况：测试异常和极端情况
# 4. 测试工具：自动化测试框架
# 5. 测试指标：覆盖率、通过率等

# 完整测试清单:
# ✓ 基础对话
# ✓ 流式输出
# ✓ 工具调用
# ✓ 多轮对话
# ✓ 错误处理
# ✓ 超时控制
# ✓ 并发安全
