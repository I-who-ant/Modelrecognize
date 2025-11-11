"""练习44: 工具设计模式"""
from abc import ABC, abstractmethod
from typing import Any, Callable
from pydantic import BaseModel, Field
import asyncio


# ========== 1. 工具基类设计 ==========

class ToolSchema(BaseModel):
    """工具 Schema"""
    name: str
    description: str
    input_schema: dict[str, Any]


class ToolResult(BaseModel):
    """工具执行结果"""
    success: bool
    content: Any
    error: str | None = None


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_input_schema(self) -> dict[str, Any]:
        """获取输入 Schema"""
        pass
    
    def get_schema(self) -> ToolSchema:
        """获取完整 Schema"""
        return ToolSchema(
            name=self.name,
            description=self.description,
            input_schema=self.get_input_schema()
        )
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
    
    async def safe_execute(self, **kwargs) -> ToolResult:
        """安全执行（带错误处理）"""
        try:
            return await self.execute(**kwargs)
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"{type(e).__name__}: {str(e)}"
            )


# ========== 2. 装饰器模式 ==========

def tool(
    name: str,
    description: str,
    input_schema: dict[str, Any]
):
    """工具装饰器"""
    def decorator(func: Callable):
        class DecoratedTool(BaseTool):
            def __init__(self):
                super().__init__(name, description)
                self.func = func
            
            def get_input_schema(self) -> dict:
                return input_schema
            
            async def execute(self, **kwargs):
                if asyncio.iscoroutinefunction(self.func):
                    result = await self.func(**kwargs)
                else:
                    result = self.func(**kwargs)
                
                return ToolResult(success=True, content=result)
        
        # 将工具类附加到函数
        func.__tool_class__ = DecoratedTool
        return func
    
    return decorator


# ========== 3. 策略模式（不同工具类型） ==========

class FileTool(BaseTool):
    """文件工具基类"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.allowed_extensions = [".txt", ".py", ".md"]
    
    def validate_file_path(self, file_path: str) -> bool:
        """验证文件路径"""
        from pathlib import Path
        path = Path(file_path)
        return path.suffix in self.allowed_extensions


class ReadFileTool(FileTool):
    """读取文件工具"""
    
    def __init__(self):
        super().__init__(
            name="read_file",
            description="读取文件内容"
        )
    
    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                }
            },
            "required": ["file_path"]
        }
    
    async def execute(self, file_path: str) -> ToolResult:
        """执行读取"""
        if not self.validate_file_path(file_path):
            return ToolResult(
                success=False,
                content=None,
                error=f"不支持的文件类型: {file_path}"
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return ToolResult(
                success=True,
                content=content
            )
        
        except FileNotFoundError:
            return ToolResult(
                success=False,
                content=None,
                error=f"文件不存在: {file_path}"
            )


class NetworkTool(BaseTool):
    """网络工具基类"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.timeout = 10.0
        self.max_retries = 3


# ========== 4. 组合模式（工具组） ==========

class ToolGroup:
    """工具组"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.tools: list[BaseTool] = []
    
    def add_tool(self, tool: BaseTool):
        """添加工具"""
        self.tools.append(tool)
    
    def get_all_schemas(self) -> list[ToolSchema]:
        """获取所有工具 Schema"""
        return [tool.get_schema() for tool in self.tools]
    
    async def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """执行指定工具"""
        for tool in self.tools:
            if tool.name == tool_name:
                return await tool.safe_execute(**kwargs)
        
        return ToolResult(
            success=False,
            content=None,
            error=f"未找到工具: {tool_name}"
        )


# ========== 5. 工厂模式 ==========

class ToolFactory:
    """工具工厂"""
    
    _registry: dict[str, type[BaseTool]] = {}
    
    @classmethod
    def register(cls, tool_type: str, tool_class: type[BaseTool]):
        """注册工具类"""
        cls._registry[tool_type] = tool_class
    
    @classmethod
    def create(cls, tool_type: str) -> BaseTool:
        """创建工具实例"""
        if tool_type not in cls._registry:
            raise ValueError(f"未知工具类型: {tool_type}")
        
        tool_class = cls._registry[tool_type]
        return tool_class()


# 注册默认工具
ToolFactory.register("read_file", ReadFileTool)


# ========== 演示函数 ==========

async def demo_basic_tool():
    """演示基础工具"""
    print("\n" + "=" * 60)
    print("1. 基础工具使用")
    print("=" * 60)
    
    # 创建工具
    tool = ReadFileTool()
    
    # 获取 Schema
    schema = tool.get_schema()
    print(f"\n工具名称: {schema.name}")
    print(f"描述: {schema.description}")
    print(f"输入 Schema: {schema.input_schema}")
    
    # 创建测试文件
    with open("/tmp/test_tool.txt", "w") as f:
        f.write("测试内容")
    
    # 执行工具
    result = await tool.safe_execute(file_path="/tmp/test_tool.txt")
    print(f"\n执行结果:")
    print(f"  成功: {result.success}")
    print(f"  内容: {result.content}")


async def demo_decorator_tool():
    """演示装饰器工具"""
    print("\n" + "=" * 60)
    print("2. 装饰器工具")
    print("=" * 60)
    
    @tool(
        name="calculate",
        description="计算数学表达式",
        input_schema={
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    )
    def calculate(expression: str) -> float:
        """计算"""
        return eval(expression)
    
    # 创建工具实例
    calc_tool = calculate.__tool_class__()
    
    # 执行
    result = await calc_tool.safe_execute(expression="2 + 3 * 4")
    print(f"计算结果: {result.content}")


async def demo_tool_group():
    """演示工具组"""
    print("\n" + "=" * 60)
    print("3. 工具组")
    print("=" * 60)
    
    # 创建工具组
    group = ToolGroup("文件操作", "文件相关工具")
    group.add_tool(ReadFileTool())
    
    # 列出所有工具
    print("\n工具组包含:")
    for schema in group.get_all_schemas():
        print(f"  - {schema.name}: {schema.description}")
    
    # 执行工具
    result = await group.execute_tool("read_file", file_path="/tmp/test_tool.txt")
    print(f"\n执行结果: {result.content}")


async def demo_tool_factory():
    """演示工具工厂"""
    print("\n" + "=" * 60)
    print("4. 工具工厂")
    print("=" * 60)
    
    # 使用工厂创建工具
    tool = ToolFactory.create("read_file")
    print(f"创建工具: {tool.name}")
    
    # 执行
    result = await tool.safe_execute(file_path="/tmp/test_tool.txt")
    print(f"执行结果: {result.success}")


async def main():
    """主函数"""
    print("\n=== 练习44: 工具设计模式 ===")
    
    await demo_basic_tool()
    await demo_decorator_tool()
    await demo_tool_group()
    await demo_tool_factory()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 基类设计：定义统一的工具接口
# 2. 装饰器模式：简化工具定义
# 3. 策略模式：不同类型工具的继承体系
# 4. 组合模式：工具组管理多个工具
# 5. 工厂模式：动态创建工具实例
# 6. 错误处理：safe_execute 提供统一错误处理
