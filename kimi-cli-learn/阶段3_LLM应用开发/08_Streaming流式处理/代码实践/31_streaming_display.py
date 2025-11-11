"""练习31: 流式显示实现"""
from typing import AsyncIterator
import asyncio
import sys


# ========== 1. 基础流式显示 ==========

async def basic_stream_display(text_stream: AsyncIterator[str]):
    """基础流式显示（逐字输出）"""
    async for chunk in text_stream:
        print(chunk, end='', flush=True)
    print()  # 最后换行


# ========== 2. 带缓冲的流式显示 ==========

class BufferedStreamDisplay:
    """带缓冲的流式显示器"""
    
    def __init__(self, buffer_size: int = 10, flush_interval: float = 0.1):
        self.buffer = []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.last_flush = asyncio.get_event_loop().time()
    
    async def write(self, chunk: str):
        """写入数据块"""
        self.buffer.append(chunk)
        
        current_time = asyncio.get_event_loop().time()
        
        # 缓冲区满或时间间隔到达时刷新
        if (len(self.buffer) >= self.buffer_size or
            current_time - self.last_flush >= self.flush_interval):
            await self.flush()
    
    async def flush(self):
        """刷新缓冲区"""
        if self.buffer:
            text = ''.join(self.buffer)
            print(text, end='', flush=True)
            self.buffer.clear()
            self.last_flush = asyncio.get_event_loop().time()
    
    async def close(self):
        """关闭并刷新剩余内容"""
        await self.flush()
        print()  # 换行


# ========== 3. Rich 流式显示 ==========

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

class RichStreamDisplay:
    """使用 Rich 的流式显示器"""
    
    def __init__(self):
        self.console = Console()
        self.buffer = ""
    
    async def display_markdown(self, text_stream: AsyncIterator[str]):
        """流式显示 Markdown"""
        with Live(console=self.console, refresh_per_second=10) as live:
            async for chunk in text_stream:
                self.buffer += chunk
                
                # 实时渲染 Markdown
                md = Markdown(self.buffer)
                live.update(Panel(md, title="AI 回复", border_style="cyan"))
    
    async def display_plain(self, text_stream: AsyncIterator[str]):
        """流式显示纯文本（带样式）"""
        self.console.print("[bold cyan]AI:[/bold cyan] ", end='')
        
        async for chunk in text_stream:
            self.console.print(chunk, end='', style="white")
        
        self.console.print()  # 换行


# ========== 4. 进度指示器 ==========

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

class StreamingProgress:
    """流式处理进度指示器"""
    
    def __init__(self):
        self.console = Console()
    
    async def display_with_progress(self, text_stream: AsyncIterator[str]):
        """带进度条的流式显示"""
        chunks_count = 0
        text_buffer = ""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]接收中...", total=None)
            
            async for chunk in text_stream:
                chunks_count += 1
                text_buffer += chunk
                
                # 更新进度描述
                progress.update(
                    task,
                    description=f"[cyan]已接收 {chunks_count} 个数据块"
                )
                
                # 小延迟以显示进度
                await asyncio.sleep(0.01)
            
            progress.update(task, description="[green]✓ 接收完成")
        
        # 显示完整文本
        self.console.print("\n[bold]完整回复:[/bold]")
        self.console.print(Panel(text_buffer, border_style="green"))


# ========== 5. 模拟数据流 ==========

async def mock_text_stream(text: str, delay: float = 0.05) -> AsyncIterator[str]:
    """模拟文本流（逐字符）"""
    for char in text:
        await asyncio.sleep(delay)
        yield char


async def mock_chunk_stream(text: str, chunk_size: int = 5) -> AsyncIterator[str]:
    """模拟文本流（按块）"""
    for i in range(0, len(text), chunk_size):
        await asyncio.sleep(0.1)
        yield text[i:i+chunk_size]


async def mock_llm_stream() -> AsyncIterator[str]:
    """模拟 LLM 流式返回"""
    response = """
# Python 异步编程

异步编程是现代 Python 的重要特性。主要优势：

1. **高并发**：处理大量 I/O 操作
2. **高性能**：避免线程开销
3. **简洁代码**：async/await 语法

示例代码：

```python
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

非常适合网络请求、数据库查询等场景！
"""
    
    async for chunk in mock_chunk_stream(response.strip(), chunk_size=10):
        yield chunk


# ========== 演示函数 ==========

async def demo_basic_display():
    """演示基础流式显示"""
    print("\n" + "=" * 60)
    print("1. 基础流式显示")
    print("=" * 60)
    
    print("\n逐字显示: ", end='')
    text = "你好，我是AI助手！"
    await basic_stream_display(mock_text_stream(text, delay=0.05))


async def demo_buffered_display():
    """演示带缓冲的显示"""
    print("\n" + "=" * 60)
    print("2. 带缓冲的流式显示")
    print("=" * 60)
    
    display = BufferedStreamDisplay(buffer_size=5, flush_interval=0.2)
    
    print("\n缓冲输出: ", end='')
    text = "这是一段比较长的文本，用于测试缓冲流式显示效果。"
    
    async for char in mock_text_stream(text, delay=0.03):
        await display.write(char)
    
    await display.close()


async def demo_rich_display():
    """演示 Rich 流式显示"""
    print("\n" + "=" * 60)
    print("3. Rich 流式显示")
    print("=" * 60)
    
    display = RichStreamDisplay()
    
    print("\n3.1 纯文本显示:")
    await display.display_plain(mock_chunk_stream("你好！我是AI助手，很高兴为你服务！"))
    
    print("\n3.2 Markdown 显示:")
    await display.display_markdown(mock_llm_stream())


async def demo_progress_display():
    """演示进度指示器"""
    print("\n" + "=" * 60)
    print("4. 带进度的流式显示")
    print("=" * 60)
    
    display = StreamingProgress()
    await display.display_with_progress(mock_llm_stream())


async def main():
    """主函数"""
    print("\n=== 练习31: 流式显示实现 ===")
    
    await demo_basic_display()
    await demo_buffered_display()
    await demo_rich_display()
    await demo_progress_display()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 流式显示需要 flush=True 确保立即输出
# 2. 缓冲可以减少 I/O 调用，提高性能
# 3. Rich 提供了更好的视觉效果和交互体验
# 4. 进度指示器可以改善用户体验
# 5. Kimi CLI 使用 Rich + Live 实现流式 Markdown 显示
