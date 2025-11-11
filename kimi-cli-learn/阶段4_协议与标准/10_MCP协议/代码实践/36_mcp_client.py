"""练习36: MCP 客户端与测试"""
from typing import Any
from pydantic import BaseModel
import asyncio
import json


# ========== 1. 导入 MCP 类型 ==========

class MCPToolSchema(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]


class MCPToolCall(BaseModel):
    name: str
    arguments: dict[str, Any]


class MCPToolResult(BaseModel):
    content: Any
    is_error: bool = False


# ========== 2. MCP 客户端 ==========

class MCPClient:
    """MCP 客户端"""
    
    def __init__(self, server):
        """
        参数:
            server: MCP Server 实例
        """
        self.server = server
        self.available_tools: list[MCPToolSchema] = []
    
    async def initialize(self):
        """初始化客户端（获取工具列表）"""
        self.available_tools = self.server.list_tools()
        print(f"✓ 已连接到 MCP Server: {self.server.name}")
        print(f"  可用工具数: {len(self.available_tools)}")
    
    def get_tool_names(self) -> list[str]:
        """获取工具名称列表"""
        return [tool.name for tool in self.available_tools]
    
    def get_tool_schema(self, name: str) -> MCPToolSchema | None:
        """获取工具 Schema"""
        for tool in self.available_tools:
            if tool.name == name:
                return tool
        return None
    
    async def call_tool(self, name: str, arguments: dict[str, Any]) -> MCPToolResult:
        """调用工具"""
        print(f"\n🔧 调用工具: {name}")
        print(f"   参数: {json.dumps(arguments, ensure_ascii=False)}")
        
        tool_call = MCPToolCall(name=name, arguments=arguments)
        result = await self.server.execute_tool(tool_call)
        
        if result.is_error:
            print(f"   ✗ 错误: {result.content}")
        else:
            print(f"   ✓ 成功: {result.content}")
        
        return result
    
    def format_tools_for_llm(self) -> list[dict]:
        """格式化工具为 LLM Function Calling 格式"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            }
            for tool in self.available_tools
        ]


# ========== 3. MCP 工具测试器 ==========

class MCPToolTester:
    """MCP 工具测试器"""
    
    def __init__(self, client: MCPClient):
        self.client = client
        self.test_results: list[dict] = []
    
    async def test_tool(
        self,
        tool_name: str,
        test_cases: list[dict[str, Any]]
    ):
        """测试工具"""
        print(f"\n{'='*60}")
        print(f"测试工具: {tool_name}")
        print(f"{'='*60}")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}:")
            
            # 调用工具
            result = await self.client.call_tool(
                tool_name,
                test_case["arguments"]
            )
            
            # 记录结果
            self.test_results.append({
                "tool": tool_name,
                "case": i,
                "arguments": test_case["arguments"],
                "expected": test_case.get("expected"),
                "result": result.content,
                "is_error": result.is_error,
                "passed": not result.is_error
            })
    
    def print_summary(self):
        """打印测试摘要"""
        print(f"\n{'='*60}")
        print("测试摘要")
        print(f"{'='*60}")
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        
        print(f"\n总测试数: {total}")
        print(f"通过: {passed}")
        print(f"失败: {total - passed}")
        print(f"通过率: {passed/total*100:.1f}%")


# ========== 4. 模拟 Agent 使用 MCP 工具 ==========

class SimpleAgent:
    """简单的 Agent（模拟使用 MCP 工具）"""
    
    def __init__(self, mcp_client: MCPClient):
        self.client = mcp_client
    
    async def process_task(self, task: str):
        """处理任务（简化版，基于关键词）"""
        print(f"\n📝 任务: {task}")
        
        # 简单规则：根据关键词选择工具
        if "读取" in task or "查看" in task:
            # 提取文件路径（简化）
            file_path = "/tmp/test.txt"
            result = await self.client.call_tool(
                "read_file",
                {"file_path": file_path}
            )
            return f"文件内容: {result.content}"
        
        elif "写入" in task or "保存" in task:
            result = await self.client.call_tool(
                "write_file",
                {"file_path": "/tmp/agent_output.txt", "content": "Agent 生成的内容"}
            )
            return result.content
        
        elif "计算" in task:
            # 提取表达式（简化）
            expr = "2 + 3"
            result = await self.client.call_tool(
                "calculate",
                {"expression": expr}
            )
            return f"计算结果: {result.content}"
        
        else:
            return "无法处理此任务"


# ========== 演示函数 ==========

async def demo_mcp_client():
    """演示 MCP 客户端"""
    print("\n" + "=" * 60)
    print("1. MCP 客户端基础使用")
    print("=" * 60)
    
    # 导入 MCP Server（来自练习35）
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent))
    
    # 这里需要先运行练习35，或者直接导入
    # 为了演示，我们创建一个简化版
    class MockMCPServer:
        name = "mock-server"
        def list_tools(self):
            return [
                MCPToolSchema(
                    name="read_file",
                    description="读取文件",
                    input_schema={"type": "object", "properties": {"file_path": {"type": "string"}}}
                )
            ]
        async def execute_tool(self, call):
            return MCPToolResult(content="模拟结果", is_error=False)
    
    server = MockMCPServer()
    client = MCPClient(server)
    await client.initialize()
    
    # 获取工具列表
    print("\n可用工具:")
    for name in client.get_tool_names():
        print(f"  - {name}")
    
    # 调用工具
    await client.call_tool("read_file", {"file_path": "/tmp/test.txt"})


async def demo_tool_testing():
    """演示工具测试"""
    print("\n" + "=" * 60)
    print("2. MCP 工具测试")
    print("=" * 60)
    
    # 创建模拟服务器
    class MockMCPServer:
        name = "test-server"
        def list_tools(self):
            return [
                MCPToolSchema(
                    name="calculate",
                    description="计算",
                    input_schema={}
                )
            ]
        async def execute_tool(self, call):
            try:
                result = eval(call.arguments["expression"])
                return MCPToolResult(content=result, is_error=False)
            except:
                return MCPToolResult(content="错误", is_error=True)
    
    server = MockMCPServer()
    client = MCPClient(server)
    await client.initialize()
    
    # 测试工具
    tester = MCPToolTester(client)
    await tester.test_tool(
        "calculate",
        [
            {"arguments": {"expression": "2+3"}, "expected": 5},
            {"arguments": {"expression": "10*5"}, "expected": 50},
            {"arguments": {"expression": "invalid"}, "expected": "error"},
        ]
    )
    
    tester.print_summary()


async def main():
    """主函数"""
    print("\n=== 练习36: MCP 客户端与测试 ===")
    
    await demo_mcp_client()
    await demo_tool_testing()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. MCP 客户端负责与 MCP Server 通信
# 2. 客户端需要获取并维护工具列表
# 3. 工具测试确保工具功能正确
# 4. Agent 通过客户端调用 MCP 工具
# 5. 可以将 MCP 工具转换为 LLM Function Calling 格式
