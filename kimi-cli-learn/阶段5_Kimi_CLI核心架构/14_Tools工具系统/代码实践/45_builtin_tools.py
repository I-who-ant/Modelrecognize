"""练习45: 内置工具实现"""
from pathlib import Path
import subprocess
import asyncio
from typing import Any
from pydantic import BaseModel


# ========== 1. 工具基础 ==========

class ToolResult(BaseModel):
    """工具结果"""
    success: bool
    content: Any
    error: str | None = None


class BaseTool:
    """工具基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError


# ========== 2. 文件工具 ==========

class ReadTool(BaseTool):
    """读取文件工具"""
    
    def __init__(self):
        super().__init__(
            name="read",
            description="读取文件内容"
        )
    
    async def execute(
        self,
        file_path: str,
        start_line: int | None = None,
        end_line: int | None = None
    ) -> ToolResult:
        """读取文件"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"文件不存在: {file_path}"
                )
            
            with open(path, 'r', encoding='utf-8') as f:
                if start_line is None:
                    content = f.read()
                else:
                    lines = f.readlines()
                    end = end_line or len(lines)
                    content = ''.join(lines[start_line-1:end])
            
            return ToolResult(success=True, content=content)
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


class WriteTool(BaseTool):
    """写入文件工具"""
    
    def __init__(self):
        super().__init__(
            name="write",
            description="写入文件内容"
        )
    
    async def execute(
        self,
        file_path: str,
        content: str,
        mode: str = "overwrite"
    ) -> ToolResult:
        """写入文件"""
        try:
            path = Path(file_path)
            
            # 创建父目录
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入模式
            write_mode = 'w' if mode == "overwrite" else 'a'
            
            with open(path, write_mode, encoding='utf-8') as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                content=f"成功写入 {len(content)} 字符到 {file_path}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


class GlobTool(BaseTool):
    """文件搜索工具"""
    
    def __init__(self):
        super().__init__(
            name="glob",
            description="搜索文件"
        )
    
    async def execute(
        self,
        pattern: str,
        directory: str = "."
    ) -> ToolResult:
        """搜索文件"""
        try:
            base_path = Path(directory)
            matches = list(base_path.glob(pattern))
            
            # 转换为字符串列表
            files = [str(p.relative_to(base_path)) for p in matches]
            
            return ToolResult(
                success=True,
                content={
                    "count": len(files),
                    "files": files
                }
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


# ========== 3. Bash 工具 ==========

class BashTool(BaseTool):
    """Bash 命令执行工具"""
    
    def __init__(self):
        super().__init__(
            name="bash",
            description="执行 Bash 命令"
        )
        self.timeout = 30.0
    
    async def execute(
        self,
        command: str,
        work_dir: str | None = None
    ) -> ToolResult:
        """执行命令"""
        try:
            # 执行命令
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=work_dir
            )
            
            # 等待完成（带超时）
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            # 解码输出
            stdout_text = stdout.decode('utf-8')
            stderr_text = stderr.decode('utf-8')
            
            return ToolResult(
                success=process.returncode == 0,
                content={
                    "stdout": stdout_text,
                    "stderr": stderr_text,
                    "returncode": process.returncode
                }
            )
        
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                content=None,
                error=f"命令超时 ({self.timeout}s)"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=str(e)
            )


# ========== 4. Web 工具 ==========

class WebSearchTool(BaseTool):
    """网页搜索工具（模拟）"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="搜索网页"
        )
    
    async def execute(
        self,
        query: str,
        max_results: int = 5
    ) -> ToolResult:
        """执行搜索"""
        # 模拟搜索结果
        results = [
            {
                "title": f"搜索结果 {i+1}: {query}",
                "url": f"https://example.com/result{i}",
                "snippet": f"关于 {query} 的相关内容..."
            }
            for i in range(max_results)
        ]
        
        return ToolResult(
            success=True,
            content={
                "query": query,
                "count": len(results),
                "results": results
            }
        )


class WebFetchTool(BaseTool):
    """网页抓取工具（模拟）"""
    
    def __init__(self):
        super().__init__(
            name="web_fetch",
            description="抓取网页内容"
        )
    
    async def execute(self, url: str) -> ToolResult:
        """抓取网页"""
        # 实际应该使用 aiohttp 或 httpx
        return ToolResult(
            success=True,
            content=f"模拟抓取 {url} 的内容"
        )


# ========== 5. 工具注册表 ==========

class BuiltinToolRegistry:
    """内置工具注册表"""
    
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self._register_all()
    
    def _register_all(self):
        """注册所有内置工具"""
        tools = [
            ReadTool(),
            WriteTool(),
            GlobTool(),
            BashTool(),
            WebSearchTool(),
            WebFetchTool(),
        ]
        
        for tool in tools:
            self.tools[tool.name] = tool
            print(f"✓ 注册工具: {tool.name}")
    
    def get(self, name: str) -> BaseTool | None:
        """获取工具"""
        return self.tools.get(name)
    
    def list_all(self) -> list[str]:
        """列出所有工具"""
        return list(self.tools.keys())
    
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

async def demo_file_tools():
    """演示文件工具"""
    print("\n" + "=" * 60)
    print("1. 文件工具演示")
    print("=" * 60)
    
    registry = BuiltinToolRegistry()
    
    # 写入文件
    print("\n写入文件:")
    result = await registry.execute(
        "write",
        file_path="/tmp/demo.txt",
        content="Hello, Kimi!\n这是测试内容。"
    )
    print(f"  {result.content}")
    
    # 读取文件
    print("\n读取文件:")
    result = await registry.execute(
        "read",
        file_path="/tmp/demo.txt"
    )
    print(f"  内容: {result.content}")
    
    # 搜索文件
    print("\n搜索文件:")
    result = await registry.execute(
        "glob",
        pattern="*.txt",
        directory="/tmp"
    )
    print(f"  找到 {result.content['count']} 个文件")


async def demo_bash_tool():
    """演示 Bash 工具"""
    print("\n" + "=" * 60)
    print("2. Bash 工具演示")
    print("=" * 60)
    
    registry = BuiltinToolRegistry()
    
    # 执行命令
    print("\n执行命令: ls -la /tmp/*.txt")
    result = await registry.execute(
        "bash",
        command="ls -la /tmp/*.txt"
    )
    
    if result.success:
        print(f"  输出:\n{result.content['stdout']}")
    else:
        print(f"  错误: {result.error}")


async def demo_web_tools():
    """演示 Web 工具"""
    print("\n" + "=" * 60)
    print("3. Web 工具演示")
    print("=" * 60)
    
    registry = BuiltinToolRegistry()
    
    # 搜索
    print("\n网页搜索:")
    result = await registry.execute(
        "web_search",
        query="Python asyncio",
        max_results=3
    )
    
    if result.success:
        for r in result.content["results"]:
            print(f"  - {r['title']}")


async def main():
    """主函数"""
    print("\n=== 练习45: 内置工具实现 ===")
    
    await demo_file_tools()
    await demo_bash_tool()
    await demo_web_tools()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 文件工具：Read、Write、Glob 实现文件操作
# 2. Bash 工具：异步执行命令，处理超时
# 3. Web 工具：搜索和抓取网页内容
# 4. 工具注册表：统一管理所有工具
# 5. 错误处理：每个工具都有完善的错误处理
# 6. 异步设计：所有工具都是异步的

# Kimi CLI 内置工具:
# - read: 读取文件
# - write: 写入文件
# - glob: 搜索文件
# - bash: 执行命令
# - web_search: 搜索网页
# - web_fetch: 抓取网页
# - task: 子任务执行
