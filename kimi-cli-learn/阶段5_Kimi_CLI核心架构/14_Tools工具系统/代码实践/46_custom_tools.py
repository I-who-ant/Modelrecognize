"""练习46: 自定义工具开发"""
from typing import Any
from pydantic import BaseModel, Field
import asyncio
import json


# ========== 1. 自定义工具基础 ==========

class ToolResult(BaseModel):
    success: bool
    content: Any
    error: str | None = None


class CustomToolBase:
    """自定义工具基类"""
    
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def get_schema(self) -> dict:
        """获取工具 Schema"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        raise NotImplementedError


# ========== 2. 示例：Git 工具 ==========

class GitStatusTool(CustomToolBase):
    """Git 状态查询工具"""
    
    def __init__(self):
        super().__init__(
            name="git_status",
            description="查询 Git 仓库状态",
            parameters={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "仓库路径，默认为当前目录"
                    }
                }
            }
        )
    
    async def execute(self, repo_path: str = ".") -> ToolResult:
        """执行 git status"""
        import subprocess
        
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return ToolResult(
                    success=True,
                    content={
                        "status": result.stdout,
                        "files_changed": len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                    }
                )
            else:
                return ToolResult(
                    success=False,
                    content=None,
                    error=result.stderr
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


# ========== 3. 示例：数据库工具 ==========

class DatabaseQueryTool(CustomToolBase):
    """数据库查询工具（SQLite）"""
    
    def __init__(self):
        super().__init__(
            name="db_query",
            description="查询 SQLite 数据库",
            parameters={
                "type": "object",
                "properties": {
                    "db_path": {"type": "string", "description": "数据库文件路径"},
                    "query": {"type": "string", "description": "SQL 查询语句"}
                },
                "required": ["db_path", "query"]
            }
        )
    
    async def execute(self, db_path: str, query: str) -> ToolResult:
        """执行查询"""
        import sqlite3
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute(query)
            
            # 获取结果
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                result = {
                    "columns": columns,
                    "rows": rows,
                    "count": len(rows)
                }
            else:
                conn.commit()
                result = {
                    "affected_rows": cursor.rowcount
                }
            
            conn.close()
            
            return ToolResult(success=True, content=result)
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


# ========== 4. 示例：API 调用工具 ==========

class RestAPITool(CustomToolBase):
    """REST API 调用工具"""
    
    def __init__(self):
        super().__init__(
            name="rest_api_call",
            description="调用 REST API",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "API URL"},
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "description": "HTTP 方法"
                    },
                    "headers": {
                        "type": "object",
                        "description": "请求头（可选）"
                    },
                    "body": {
                        "type": "object",
                        "description": "请求体（可选）"
                    }
                },
                "required": ["url", "method"]
            }
        )
    
    async def execute(
        self,
        url: str,
        method: str,
        headers: dict | None = None,
        body: dict | None = None
    ) -> ToolResult:
        """执行 API 调用"""
        # 实际应该使用 aiohttp 或 httpx
        # 这里仅演示
        
        result_data = {
            "url": url,
            "method": method,
            "status": 200,
            "response": {"message": f"模拟 {method} 请求到 {url}"}
        }
        
        return ToolResult(success=True, content=result_data)


# ========== 5. 工具装饰器（简化工具定义） ==========

def custom_tool(name: str, description: str, parameters: dict):
    """自定义工具装饰器"""
    def decorator(func):
        class DecoratedTool(CustomToolBase):
            def __init__(self):
                super().__init__(name, description, parameters)
                self.func = func
            
            async def execute(self, **kwargs):
                try:
                    if asyncio.iscoroutinefunction(self.func):
                        result = await self.func(**kwargs)
                    else:
                        result = self.func(**kwargs)
                    
                    return ToolResult(success=True, content=result)
                
                except Exception as e:
                    return ToolResult(
                        success=False,
                        content=None,
                        error=str(e)
                    )
        
        func.__tool_class__ = DecoratedTool
        return func
    
    return decorator


# ========== 6. 使用装饰器定义工具 ==========

@custom_tool(
    name="json_format",
    description="格式化 JSON",
    parameters={
        "type": "object",
        "properties": {
            "json_str": {"type": "string", "description": "JSON 字符串"},
            "indent": {"type": "integer", "description": "缩进空格数", "default": 2}
        },
        "required": ["json_str"]
    }
)
def format_json(json_str: str, indent: int = 2) -> str:
    """格式化 JSON"""
    obj = json.loads(json_str)
    return json.dumps(obj, indent=indent, ensure_ascii=False)


@custom_tool(
    name="text_analysis",
    description="分析文本统计信息",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "要分析的文本"}
        },
        "required": ["text"]
    }
)
def analyze_text(text: str) -> dict:
    """分析文本"""
    return {
        "length": len(text),
        "lines": len(text.split('\n')),
        "words": len(text.split()),
        "chars_no_spaces": len(text.replace(' ', '').replace('\n', ''))
    }


# ========== 7. 自定义工具注册器 ==========

class CustomToolRegistry:
    """自定义工具注册器"""
    
    def __init__(self):
        self.tools: dict[str, CustomToolBase] = {}
    
    def register(self, tool: CustomToolBase):
        """注册工具"""
        self.tools[tool.name] = tool
        print(f"✓ 注册自定义工具: {tool.name}")
    
    def register_from_decorator(self, func):
        """从装饰器函数注册工具"""
        if hasattr(func, '__tool_class__'):
            tool = func.__tool_class__()
            self.register(tool)
        else:
            raise ValueError(f"{func.__name__} 不是一个工具函数")
    
    def get_all_schemas(self) -> list[dict]:
        """获取所有工具 Schema"""
        return [tool.get_schema() for tool in self.tools.values()]
    
    async def execute(self, name: str, **kwargs) -> ToolResult:
        """执行工具"""
        if name not in self.tools:
            return ToolResult(
                success=False,
                content=None,
                error=f"未知工具: {name}"
            )
        
        tool = self.tools[name]
        return await tool.execute(**kwargs)


# ========== 演示函数 ==========

async def demo_git_tool():
    """演示 Git 工具"""
    print("\n" + "=" * 60)
    print("1. Git 工具演示")
    print("=" * 60)
    
    tool = GitStatusTool()
    
    # 获取 Schema
    schema = tool.get_schema()
    print(f"\n工具 Schema:\n{json.dumps(schema, indent=2, ensure_ascii=False)}")
    
    # 执行工具
    print("\n执行 git status:")
    result = await tool.execute(repo_path=".")
    
    if result.success:
        print(f"  文件变更数: {result.content['files_changed']}")
        if result.content['status']:
            print(f"  状态:\n{result.content['status']}")
    else:
        print(f"  错误: {result.error}")


async def demo_decorator_tools():
    """演示装饰器工具"""
    print("\n" + "=" * 60)
    print("2. 装饰器工具演示")
    print("=" * 60)
    
    # 创建注册器
    registry = CustomToolRegistry()
    
    # 注册工具
    registry.register_from_decorator(format_json)
    registry.register_from_decorator(analyze_text)
    
    # 测试 JSON 格式化
    print("\n测试 JSON 格式化:")
    result = await registry.execute(
        "json_format",
        json_str='{"name":"Kimi","age":1}'
    )
    print(f"  结果:\n{result.content}")
    
    # 测试文本分析
    print("\n测试文本分析:")
    result = await registry.execute(
        "text_analysis",
        text="Hello, Kimi!\nThis is a test."
    )
    print(f"  结果:\n{json.dumps(result.content, indent=2)}")


async def demo_tool_registry():
    """演示工具注册器"""
    print("\n" + "=" * 60)
    print("3. 工具注册器演示")
    print("=" * 60)
    
    registry = CustomToolRegistry()
    
    # 注册多个工具
    registry.register(GitStatusTool())
    registry.register_from_decorator(format_json)
    registry.register_from_decorator(analyze_text)
    
    # 列出所有工具
    print("\n所有工具:")
    for schema in registry.get_all_schemas():
        print(f"  - {schema['name']}: {schema['description']}")


async def main():
    """主函数"""
    print("\n=== 练习46: 自定义工具开发 ===")
    
    await demo_git_tool()
    await demo_decorator_tools()
    await demo_tool_registry()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 自定义工具基类：定义统一接口
# 2. 工具 Schema：使用 JSON Schema 定义参数
# 3. 装饰器：简化工具定义
# 4. 工具注册器：管理自定义工具
# 5. 实际应用：Git、数据库、API 工具示例

# 自定义工具开发步骤:
# 1. 继承 CustomToolBase
# 2. 定义 __init__（name、description、parameters）
# 3. 实现 execute 方法
# 4. 注册到工具注册器
# 5. 在 Soul 层中使用

# 或使用装饰器:
# @custom_tool(name, description, parameters)
# def my_tool(...):
#     ...
