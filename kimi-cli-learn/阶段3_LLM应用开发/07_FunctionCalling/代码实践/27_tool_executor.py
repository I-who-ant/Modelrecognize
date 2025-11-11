"""练习27: Tool 执行器实现"""
from typing import Any, Callable
from pydantic import BaseModel, Field
import json


# ========== 1. Tool 定义 ==========

class ToolCall(BaseModel):
    """工具调用请求"""
    id: str = Field(description="调用ID")
    name: str = Field(description="工具名称")
    arguments: dict[str, Any] = Field(description="参数")


class ToolResult(BaseModel):
    """工具执行结果"""
    tool_call_id: str
    name: str
    result: Any
    error: str | None = None


# ========== 2. Tool 执行器 ==========

class ToolExecutor:
    """工具执行器"""
    
    def __init__(self):
        self.tools: dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable):
        """注册工具函数"""
        self.tools[name] = func
        print(f"✓ 已注册工具: {name}")
    
    def execute(self, tool_call: ToolCall) -> ToolResult:
        """执行工具调用"""
        try:
            # 获取工具函数
            if tool_call.name not in self.tools:
                raise ValueError(f"未知工具: {tool_call.name}")
            
            func = self.tools[tool_call.name]
            
            # 执行函数
            print(f"\n▶ 执行工具: {tool_call.name}")
            print(f"  参数: {tool_call.arguments}")
            
            result = func(**tool_call.arguments)
            
            print(f"  结果: {result}")
            
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                result=result
            )
        
        except Exception as e:
            print(f"  ✗ 错误: {e}")
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                result=None,
                error=str(e)
            )
    
    def execute_batch(self, tool_calls: list[ToolCall]) -> list[ToolResult]:
        """批量执行工具调用"""
        return [self.execute(call) for call in tool_calls]


# ========== 3. 示例工具函数 ==========

def get_weather(city: str, unit: str = "celsius") -> dict:
    """获取天气（模拟）"""
    # 模拟数据
    weather_data = {
        "北京": {"temp": 15, "condition": "晴"},
        "上海": {"temp": 20, "condition": "多云"},
        "广州": {"temp": 25, "condition": "雨"},
    }
    
    data = weather_data.get(city, {"temp": 18, "condition": "未知"})
    
    if unit == "fahrenheit":
        data["temp"] = data["temp"] * 9/5 + 32
    
    return {
        "city": city,
        "temperature": data["temp"],
        "condition": data["condition"],
        "unit": unit
    }


def calculate(expression: str) -> float:
    """计算数学表达式"""
    try:
        # 安全求值（仅允许数学运算）
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        raise ValueError(f"计算失败: {e}")


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """搜索网页（模拟）"""
    # 模拟搜索结果
    results = [
        {"title": f"结果 {i+1}: {query}", "url": f"https://example.com/{i}"}
        for i in range(max_results)
    ]
    return results


# ========== 4. 高级执行器（支持异步） ==========

import asyncio

class AsyncToolExecutor:
    """异步工具执行器"""
    
    def __init__(self):
        self.tools: dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable):
        """注册工具（支持同步和异步函数）"""
        self.tools[name] = func
    
    async def execute(self, tool_call: ToolCall) -> ToolResult:
        """执行工具（自动处理同步/异步）"""
        try:
            func = self.tools[tool_call.name]
            
            # 判断是否为异步函数
            if asyncio.iscoroutinefunction(func):
                result = await func(**tool_call.arguments)
            else:
                result = func(**tool_call.arguments)
            
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                result=result
            )
        
        except Exception as e:
            return ToolResult(
                tool_call_id=tool_call.id,
                name=tool_call.name,
                result=None,
                error=str(e)
            )
    
    async def execute_batch(self, tool_calls: list[ToolCall]) -> list[ToolResult]:
        """并发执行多个工具调用"""
        tasks = [self.execute(call) for call in tool_calls]
        return await asyncio.gather(*tasks)


# ========== 演示函数 ==========

def demo_basic_execution():
    """演示基础执行"""
    print("\n" + "=" * 60)
    print("1. 基础工具执行")
    print("=" * 60)
    
    executor = ToolExecutor()
    
    # 注册工具
    executor.register("get_weather", get_weather)
    executor.register("calculate", calculate)
    executor.register("search_web", search_web)
    
    # 执行单个工具
    tool_call = ToolCall(
        id="call_001",
        name="get_weather",
        arguments={"city": "北京", "unit": "celsius"}
    )
    
    result = executor.execute(tool_call)
    print(f"\n最终结果: {result.model_dump()}")


def demo_batch_execution():
    """演示批量执行"""
    print("\n" + "=" * 60)
    print("2. 批量工具执行")
    print("=" * 60)
    
    executor = ToolExecutor()
    executor.register("get_weather", get_weather)
    executor.register("calculate", calculate)
    
    # 批量调用
    tool_calls = [
        ToolCall(id="call_001", name="get_weather", arguments={"city": "北京"}),
        ToolCall(id="call_002", name="calculate", arguments={"expression": "2 + 3 * 4"}),
        ToolCall(id="call_003", name="get_weather", arguments={"city": "上海"}),
    ]
    
    results = executor.execute_batch(tool_calls)
    
    print(f"\n批量执行完成，共 {len(results)} 个结果")
    for r in results:
        print(f"  {r.name}: {r.result}")


async def demo_async_execution():
    """演示异步执行"""
    print("\n" + "=" * 60)
    print("3. 异步并发执行")
    print("=" * 60)
    
    executor = AsyncToolExecutor()
    executor.register("get_weather", get_weather)
    executor.register("calculate", calculate)
    
    tool_calls = [
        ToolCall(id="call_001", name="get_weather", arguments={"city": "北京"}),
        ToolCall(id="call_002", name="calculate", arguments={"expression": "10 * 5"}),
    ]
    
    import time
    start = time.time()
    results = await executor.execute_batch(tool_calls)
    elapsed = time.time() - start
    
    print(f"\n并发执行耗时: {elapsed:.2f}秒")
    for r in results:
        print(f"  {r.name}: {r.result}")


def main():
    """主函数"""
    print("\n=== 练习27: Tool 执行器实现 ===")
    
    demo_basic_execution()
    demo_batch_execution()
    
    # 运行异步演示
    asyncio.run(demo_async_execution())
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 学习要点:
# 1. Tool Executor 负责调度和执行函数调用
# 2. 需要处理错误和异常情况
# 3. 支持批量执行可以提高效率
# 4. 异步执行器可以并发调用多个工具
