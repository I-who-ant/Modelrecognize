"""练习35: 简单的 MCP Server 实现"""
from typing import Any, Callable
from pydantic import BaseModel, Field
import json
import asyncio


# ========== 1. MCP 数据模型 ==========

class MCPToolSchema(BaseModel):
    """MCP 工具定义"""
    name: str = Field(description="工具名称")
    description: str = Field(description="工具描述")
    input_schema: dict[str, Any] = Field(description="输入参数 Schema")


class MCPToolCall(BaseModel):
    """MCP 工具调用"""
    name: str
    arguments: dict[str, Any]


class MCPToolResult(BaseModel):
    """MCP 工具结果"""
    content: Any
    is_error: bool = False


# ========== 2. MCP 工具装饰器 ==========

class MCPTool:
    """MCP 工具"""
    
    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
    
    def get_schema(self) -> MCPToolSchema:
        """获取工具 Schema"""
        return MCPToolSchema(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema
        )
    
    async def execute(self, arguments: dict[str, Any]) -> MCPToolResult:
        """执行工具"""
        try:
            # 调用处理函数
            if asyncio.iscoroutinefunction(self.handler):
                result = await self.handler(**arguments)
            else:
                result = self.handler(**arguments)
            
            return MCPToolResult(content=result, is_error=False)
        
        except Exception as e:
            return MCPToolResult(
                content=f"错误: {str(e)}",
                is_error=True
            )


# ========== 3. MCP Server ==========

class SimpleMCPServer:
    """简单的 MCP Server"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: dict[str, MCPTool] = {}
    
    def tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any]
    ):
        """工具装饰器"""
        def decorator(func: Callable) -> Callable:
            tool = MCPTool(
                name=name,
                description=description,
                input_schema=input_schema,
                handler=func
            )
            self.tools[name] = tool
            print(f"✓ 注册 MCP 工具: {name}")
            return func
        
        return decorator
    
    def list_tools(self) -> list[MCPToolSchema]:
        """列出所有工具"""
        return [tool.get_schema() for tool in self.tools.values()]
    
    async def execute_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
        """执行工具"""
        if tool_call.name not in self.tools:
            return MCPToolResult(
                content=f"未知工具: {tool_call.name}",
                is_error=True
            )
        
        tool = self.tools[tool_call.name]
        return await tool.execute(tool_call.arguments)


# ========== 4. 示例 MCP Server ==========

def create_file_mcp_server() -> SimpleMCPServer:
    """创建文件工具 MCP Server"""
    server = SimpleMCPServer(name="file-tools")
    
    @server.tool(
        name="read_file",
        description="读取文件内容",
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["file_path"]
        }
    )
    def read_file(file_path: str) -> str:
        """读取文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"文件不存在: {file_path}")
    
    @server.tool(
        name="write_file",
        description="写入文件内容",
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "文件路径"},
                "content": {"type": "string", "description": "文件内容"}
            },
            "required": ["file_path", "content"]
        }
    )
    def write_file(file_path: str, content: str) -> str:
        """写入文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"成功写入 {len(content)} 字符到 {file_path}"
    
    @server.tool(
        name="list_files",
        description="列出目录中的文件",
        input_schema={
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "目录路径"}
            },
            "required": ["directory"]
        }
    )
    def list_files(directory: str) -> list[str]:
        """列出文件"""
        import os
        try:
            return os.listdir(directory)
        except FileNotFoundError:
            raise Exception(f"目录不存在: {directory}")
    
    return server


def create_calculator_mcp_server() -> SimpleMCPServer:
    """创建计算器 MCP Server"""
    server = SimpleMCPServer(name="calculator")
    
    @server.tool(
        name="calculate",
        description="计算数学表达式",
        input_schema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式，如: 2+3*4"
                }
            },
            "required": ["expression"]
        }
    )
    def calculate(expression: str) -> float:
        """计算表达式"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return float(result)
        except Exception as e:
            raise Exception(f"计算错误: {e}")
    
    return server


# ========== 演示函数 ==========

async def demo_file_server():
    """演示文件工具服务器"""
    print("\n" + "=" * 60)
    print("1. 文件工具 MCP Server")
    print("=" * 60)
    
    server = create_file_mcp_server()
    
    # 列出工具
    print("\n可用工具:")
    for tool_schema in server.list_tools():
        print(f"  - {tool_schema.name}: {tool_schema.description}")
    
    # 测试写入文件
    print("\n测试写入文件:")
    write_call = MCPToolCall(
        name="write_file",
        arguments={
            "file_path": "/tmp/test.txt",
            "content": "Hello, MCP!"
        }
    )
    result = await server.execute_tool(write_call)
    print(f"  结果: {result.content}")
    
    # 测试读取文件
    print("\n测试读取文件:")
    read_call = MCPToolCall(
        name="read_file",
        arguments={"file_path": "/tmp/test.txt"}
    )
    result = await server.execute_tool(read_call)
    print(f"  结果: {result.content}")
    
    # 测试列出文件
    print("\n测试列出文件:")
    list_call = MCPToolCall(
        name="list_files",
        arguments={"directory": "/tmp"}
    )
    result = await server.execute_tool(list_call)
    print(f"  结果 (前5个): {result.content[:5]}")


async def demo_calculator_server():
    """演示计算器服务器"""
    print("\n" + "=" * 60)
    print("2. 计算器 MCP Server")
    print("=" * 60)
    
    server = create_calculator_mcp_server()
    
    # 测试计算
    expressions = ["2 + 3", "10 * 5", "(100 - 20) / 4"]
    
    for expr in expressions:
        call = MCPToolCall(
            name="calculate",
            arguments={"expression": expr}
        )
        result = await server.execute_tool(call)
        print(f"  {expr} = {result.content}")


async def demo_tool_schema():
    """演示工具 Schema"""
    print("\n" + "=" * 60)
    print("3. MCP 工具 Schema")
    print("=" * 60)
    
    server = create_file_mcp_server()
    
    print("\nread_file 工具 Schema:")
    schema = server.tools["read_file"].get_schema()
    print(json.dumps(schema.model_dump(), indent=2, ensure_ascii=False))


async def main():
    """主函数"""
    print("\n=== 练习35: 简单的 MCP Server 实现 ===")
    
    await demo_file_server()
    await demo_calculator_server()
    await demo_tool_schema()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. MCP Server 提供标准化的工具接口
# 2. 每个工具都有清晰的 Schema 定义
# 3. 支持同步和异步工具函数
# 4. 统一的错误处理机制
# 5. 工具装饰器简化了工具注册
