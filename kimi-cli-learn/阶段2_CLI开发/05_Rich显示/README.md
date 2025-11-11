# 模块05: Rich 富文本显示

**学习时长**: 3天

**学习目标**: 掌握 Rich 库，理解 Kimi CLI 的美观输出

---

## 📋 学习内容概览

1. **基础显示** (Day 24)
2. **Markdown 渲染** (Day 25)
3. **进度条与表格** (Day 26)

---

## 🎯 学习目标

- ✅ 掌握 Rich Console 基础
- ✅ 能渲染 Markdown
- ✅ 能创建进度条和表格
- ✅ 理解 Kimi CLI 的输出美化

---

## 📚 学习资源

### 官方文档
- [Rich 官方文档](https://rich.readthedocs.io/)
- [Rich GitHub](https://github.com/Textualize/rich)

### 推荐教程
- Rich 入门教程
- 终端美化最佳实践

---

## 📖 详细学习内容

### 📝 01: 基础显示 (Day 24)

#### 学习内容

**Console 基础**:
```python
from rich.console import Console

console = Console()

# 基础打印
console.print("Hello, [bold magenta]World[/bold magenta]!")

# 样式文本
console.print("This is [bold]bold[/bold]")
console.print("This is [italic]italic[/italic]")
console.print("This is [underline]underlined[/underline]")
console.print("This is [red]red[/red]")
console.print("This is [on blue]on blue background[/on blue]")

# 组合样式
console.print("[bold red on white]Bold Red on White[/bold red on white]")
```

**Panel 面板**:
```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# 简单面板
console.print(Panel("这是一个面板"))

# 自定义标题和样式
console.print(
    Panel(
        "重要信息",
        title="提示",
        border_style="green"
    )
)

# 多行内容
content = """
第一行
第二行
第三行
"""
console.print(Panel(content, title="内容", expand=False))
```

**Rule 分隔线**:
```python
from rich.console import Console
from rich.rule import Rule

console = Console()

console.rule("[bold red]Chapter 1")
console.print("内容...")
console.rule()  # 简单分隔线
```

**语法高亮**:
```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

code = '''
def hello(name: str) -> None:
    print(f"Hello {name}!")
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/ui/shell/display.py
from rich.console import Console
from rich.markdown import Markdown

class Display:
    def __init__(self):
        self.console = Console()

    def show_message(self, message: str, markdown: bool = True):
        """显示消息"""
        if markdown:
            self.console.print(Markdown(message))
        else:
            self.console.print(message)

    def show_tool_call(self, tool_name: str, args: dict):
        """显示工具调用"""
        from rich.panel import Panel
        import json

        content = json.dumps(args, indent=2, ensure_ascii=False)
        self.console.print(
            Panel(
                content,
                title=f"🔧 调用工具: {tool_name}",
                border_style="cyan"
            )
        )
```

#### 实践练习

**练习18**: 美化命令行输出
```python
# 文件: 代码实践/18_rich_basics.py

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = Console()

def demo_basic_styles():
    """演示基础样式"""
    console.rule("[bold cyan]基础样式")

    console.print("普通文本")
    console.print("[bold]粗体文本[/bold]")
    console.print("[italic]斜体文本[/italic]")
    console.print("[underline]下划线文本[/underline]")
    console.print("[red]红色文本[/red]")
    console.print("[bold yellow on blue]粗体黄色文字蓝色背景[/bold yellow on blue]")
    console.print()

def demo_panels():
    """演示面板"""
    console.rule("[bold cyan]面板")

    # 简单面板
    console.print(Panel("这是一个简单的面板"))

    # 带标题的面板
    console.print(
        Panel(
            "这是一个带标题的面板",
            title="信息",
            border_style="green"
        )
    )

    # 错误面板
    console.print(
        Panel(
            "发生错误：文件未找到",
            title="❌ 错误",
            border_style="red"
        )
    )

    # 成功面板
    console.print(
        Panel(
            "操作成功完成！",
            title="✅ 成功",
            border_style="green"
        )
    )
    console.print()

def demo_syntax_highlighting():
    """演示语法高亮"""
    console.rule("[bold cyan]语法高亮")

    python_code = '''
def fibonacci(n: int) -> list[int]:
    """生成斐波那契数列"""
    if n <= 0:
        return []

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])

    return fib[:n]

# 调用
result = fibonacci(10)
print(result)
'''

    syntax = Syntax(
        python_code,
        "python",
        theme="monokai",
        line_numbers=True,
        word_wrap=True
    )

    console.print(Panel(syntax, title="Python 代码", border_style="cyan"))
    console.print()

def demo_text_formatting():
    """演示文本格式化"""
    console.rule("[bold cyan]文本格式化")

    # 创建 Text 对象
    text = Text()
    text.append("这是 ")
    text.append("红色", style="bold red")
    text.append(" 和 ")
    text.append("蓝色", style="bold blue")
    text.append(" 文本")

    console.print(text)

    # 渐变文本
    text2 = Text("渐变文本示例")
    text2.stylize("bold magenta")
    console.print(text2)
    console.print()

def demo_lists():
    """演示列表"""
    console.rule("[bold cyan]列表")

    # 有序列表
    console.print("[bold]有序列表:[/bold]")
    for i, item in enumerate(["第一项", "第二项", "第三项"], 1):
        console.print(f"  {i}. {item}")

    console.print()

    # 无序列表
    console.print("[bold]无序列表:[/bold]")
    for item in ["苹果", "香蕉", "橙子"]:
        console.print(f"  • {item}")

    console.print()

def demo_logging():
    """演示日志输出"""
    console.rule("[bold cyan]日志输出")

    console.log("普通日志消息")
    console.log("调试信息", style="dim")
    console.log("[bold yellow]警告信息[/bold yellow]")
    console.log("[bold red]错误信息[/bold red]")
    console.log("[bold green]成功信息[/bold green]")
    console.print()

def main():
    """主函数"""
    console.print(
        Panel.fit(
            "[bold cyan]Rich 基础演示[/bold cyan]\n"
            "展示 Rich 库的基本功能",
            border_style="cyan"
        )
    )
    console.print()

    demo_basic_styles()
    demo_panels()
    demo_syntax_highlighting()
    demo_text_formatting()
    demo_lists()
    demo_logging()

    console.print(
        Panel.fit(
            "[bold green]演示完成！[/bold green]",
            border_style="green"
        )
    )


if __name__ == '__main__':
    main()


# 扩展练习:
# 1. 创建自定义主题
# 2. 实现彩虹文本效果
# 3. 创建加载动画
# 4. 实现日志级别过滤
```

#### 检查点
- [ ] 掌握 Console 基础用法
- [ ] 能使用 Panel 和 Rule
- [ ] 能实现语法高亮
- [ ] 理解 Rich 样式系统

---

### 📝 02: Markdown 渲染 (Day 25)

#### 学习内容

**Markdown 基础**:
```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

markdown_text = """
# 标题 1

这是一段普通文本。

## 标题 2

- 列表项 1
- 列表项 2
- 列表项 3

### 代码块

```python
def hello():
    print("Hello, World!")
```

**粗体** 和 *斜体* 文本。
"""

md = Markdown(markdown_text)
console.print(md)
```

**实时 Markdown 显示**:
```python
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import time

console = Console()

markdown_content = ""

with Live(Markdown(markdown_content), console=console, refresh_per_second=10) as live:
    # 模拟逐步添加内容
    lines = [
        "# 实时更新",
        "",
        "这是第一行。",
        "",
        "这是第二行。",
        "",
        "```python",
        "print('Hello')",
        "```",
    ]

    for line in lines:
        markdown_content += line + "\n"
        live.update(Markdown(markdown_content))
        time.sleep(0.5)
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/ui/shell/display.py
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

class StreamingDisplay:
    """流式显示 Markdown"""

    def __init__(self):
        self.console = Console()

    async def stream_markdown(self, content_stream):
        """流式显示 Markdown 内容"""
        content = ""

        with Live(
            Markdown(content),
            console=self.console,
            refresh_per_second=10
        ) as live:
            async for chunk in content_stream:
                content += chunk
                live.update(Markdown(content))
```

#### 实践练习

**练习19**: Markdown 查看器
```python
# 文件: 代码实践/19_markdown_viewer.py

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from pathlib import Path
import sys

console = Console()

def view_markdown_file(file_path: Path):
    """查看 Markdown 文件"""
    if not file_path.exists():
        console.print(f"[red]错误: 文件不存在: {file_path}[/red]")
        return

    if not file_path.suffix == '.md':
        console.print(f"[yellow]警告: {file_path} 可能不是 Markdown 文件[/yellow]")

    # 读取文件
    content = file_path.read_text(encoding='utf-8')

    # 显示文件信息
    console.print(
        Panel(
            f"文件: [cyan]{file_path}[/cyan]\n"
            f"大小: {file_path.stat().st_size} 字节",
            title="📄 文件信息",
            border_style="blue"
        )
    )
    console.print()

    # 渲染 Markdown
    md = Markdown(content)
    console.print(md)

def demo_markdown_features():
    """演示 Markdown 功能"""
    markdown_text = """
# Markdown 功能演示

## 1. 标题

使用 `#` 创建标题，支持 1-6 级标题。

## 2. 文本样式

- **粗体文本**
- *斜体文本*
- ~~删除线~~
- `行内代码`

## 3. 列表

### 无序列表

- 项目 1
- 项目 2
  - 子项 2.1
  - 子项 2.2
- 项目 3

### 有序列表

1. 第一步
2. 第二步
3. 第三步

## 4. 引用

> 这是一段引用文本。
> 可以有多行。

## 5. 代码块

### Python 代码

```python
def fibonacci(n: int) -> list[int]:
    if n <= 0:
        return []
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

print(fibonacci(10))
```

### JavaScript 代码

```javascript
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5));
```

## 6. 链接

[Rich 官方文档](https://rich.readthedocs.io/)

## 7. 表格

| 姓名 | 年龄 | 城市 |
|------|------|------|
| Alice | 25 | Beijing |
| Bob | 30 | Shanghai |
| Charlie | 28 | Shenzhen |

## 8. 分隔线

---

## 总结

Rich 的 Markdown 渲染功能强大，支持大部分 Markdown 语法！
"""

    console.print(Panel.fit(
        "[bold cyan]Markdown 功能演示[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    md = Markdown(markdown_text)
    console.print(md)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 查看指定文件
        file_path = Path(sys.argv[1])
        view_markdown_file(file_path)
    else:
        # 演示 Markdown 功能
        demo_markdown_features()


if __name__ == '__main__':
    main()


# 使用示例:
# python 19_markdown_viewer.py README.md


# 扩展练习:
# 1. 添加文件监视（自动刷新）
# 2. 添加目录导航
# 3. 支持 GitHub Flavored Markdown
# 4. 添加搜索功能
```

#### 检查点
- [ ] 掌握 Markdown 渲染
- [ ] 能实现实时更新
- [ ] 理解 Live 组件
- [ ] 理解 Kimi CLI 的流式显示

---

### 📝 03: 进度条与表格 (Day 26)

#### 学习内容

**Progress 进度条**:
```python
from rich.console import Console
from rich.progress import Progress
import time

console = Console()

# 基础进度条
with Progress() as progress:
    task = progress.add_task("[cyan]Processing...", total=100)

    while not progress.finished:
        progress.update(task, advance=1)
        time.sleep(0.01)

console.print("[green]完成！[/green]")
```

**多任务进度条**:
```python
from rich.progress import Progress
import time

with Progress() as progress:
    task1 = progress.add_task("[red]下载文件1...", total=1000)
    task2 = progress.add_task("[green]下载文件2...", total=1000)
    task3 = progress.add_task("[cyan]下载文件3...", total=1000)

    while not progress.finished:
        progress.update(task1, advance=10)
        progress.update(task2, advance=8)
        progress.update(task3, advance=12)
        time.sleep(0.02)
```

**Table 表格**:
```python
from rich.console import Console
from rich.table import Table

console = Console()

# 创建表格
table = Table(title="用户列表")

# 添加列
table.add_column("ID", justify="right", style="cyan", no_wrap=True)
table.add_column("姓名", style="magenta")
table.add_column("年龄", justify="right", style="green")
table.add_column("城市", style="yellow")

# 添加行
table.add_row("1", "Alice", "25", "Beijing")
table.add_row("2", "Bob", "30", "Shanghai")
table.add_row("3", "Charlie", "28", "Shenzhen")

console.print(table)
```

**Tree 树形结构**:
```python
from rich.console import Console
from rich.tree import Tree

console = Console()

tree = Tree("📁 项目根目录")

src = tree.add("📁 src")
src.add("📄 main.py")
src.add("📄 utils.py")

tests = tree.add("📁 tests")
tests.add("📄 test_main.py")

tree.add("📄 README.md")
tree.add("📄 requirements.txt")

console.print(tree)
```

**Kimi CLI 中的应用**:
```python
# 工具调用进度显示
from rich.progress import Progress

async def execute_tools_with_progress(tools: list):
    """带进度条执行工具"""
    with Progress() as progress:
        task = progress.add_task(
            "[cyan]执行工具...",
            total=len(tools)
        )

        for tool in tools:
            await tool.execute()
            progress.update(task, advance=1)
```

#### 实践练习

**练习20**: 文件处理进度可视化
```python
# 文件: 代码实践/20_progress_and_tables.py

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.tree import Tree
from pathlib import Path
import time
import random

console = Console()

def demo_progress_bar():
    """演示进度条"""
    console.rule("[bold cyan]进度条演示")

    with Progress() as progress:
        task1 = progress.add_task("[red]任务 1", total=100)
        task2 = progress.add_task("[green]任务 2", total=100)
        task3 = progress.add_task("[cyan]任务 3", total=100)

        while not progress.finished:
            progress.update(task1, advance=random.randint(1, 5))
            progress.update(task2, advance=random.randint(1, 3))
            progress.update(task3, advance=random.randint(1, 7))
            time.sleep(0.05)

    console.print("[green]✅ 所有任务完成！[/green]\n")

def demo_custom_progress():
    """演示自定义进度条"""
    console.rule("[bold cyan]自定义进度条")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[cyan]处理文件...", total=100)

        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

    console.print("[green]✅ 处理完成！[/green]\n")

def demo_tables():
    """演示表格"""
    console.rule("[bold cyan]表格演示")

    # 简单表格
    table = Table(title="学生成绩表")

    table.add_column("学号", justify="right", style="cyan", no_wrap=True)
    table.add_column("姓名", style="magenta")
    table.add_column("数学", justify="right", style="green")
    table.add_column("英语", justify="right", style="yellow")
    table.add_column("总分", justify="right", style="bold blue")

    students = [
        ("001", "张三", "95", "88", "183"),
        ("002", "李四", "87", "92", "179"),
        ("003", "王五", "92", "85", "177"),
        ("004", "赵六", "78", "90", "168"),
    ]

    for student in students:
        table.add_row(*student)

    console.print(table)
    console.print()

    # 带样式的表格
    table2 = Table(title="项目状态", show_header=True, header_style="bold magenta")

    table2.add_column("项目名称", style="cyan")
    table2.add_column("状态", justify="center")
    table2.add_column("进度", justify="right")

    table2.add_row("项目A", "[green]运行中[/green]", "85%")
    table2.add_row("项目B", "[yellow]暂停[/yellow]", "42%")
    table2.add_row("项目C", "[red]错误[/red]", "12%")
    table2.add_row("项目D", "[green]完成[/green]", "100%")

    console.print(table2)
    console.print()

def demo_tree():
    """演示树形结构"""
    console.rule("[bold cyan]树形结构演示")

    tree = Tree("📁 kimi-cli-learn")

    stage1 = tree.add("📁 阶段1_基础准备")
    module01 = stage1.add("📁 01_Python现代特性")
    module01.add("📄 README.md")
    module01.add("📁 代码实践")

    module02 = stage1.add("📁 02_异步编程")
    module02.add("📄 README.md")
    module02.add("📁 代码实践")

    stage2 = tree.add("📁 阶段2_CLI开发")
    module03 = stage2.add("📁 03_Click框架")
    module03.add("📄 README.md")

    tree.add("📄 学习路线图.md")
    tree.add("📄 README.md")

    console.print(tree)
    console.print()

def demo_file_processing():
    """演示文件处理进度"""
    console.rule("[bold cyan]文件处理模拟")

    files = [
        "document1.pdf",
        "image1.png",
        "video1.mp4",
        "document2.pdf",
        "image2.jpg",
    ]

    with Progress() as progress:
        overall = progress.add_task("[cyan]总进度", total=len(files))

        for file in files:
            file_task = progress.add_task(
                f"[green]处理 {file}",
                total=100
            )

            # 模拟文件处理
            for _ in range(100):
                time.sleep(0.01)
                progress.update(file_task, advance=1)

            progress.update(overall, advance=1)
            progress.remove_task(file_task)

    console.print("[green]✅ 所有文件处理完成！[/green]\n")

def main():
    """主函数"""
    console.print(
        Panel.fit(
            "[bold cyan]进度条与表格演示[/bold cyan]\n"
            "展示 Rich 的进度条和表格功能",
            border_style="cyan"
        )
    )
    console.print()

    demo_progress_bar()
    demo_custom_progress()
    demo_tables()
    demo_tree()
    demo_file_processing()


if __name__ == '__main__':
    from rich.panel import Panel
    main()


# 扩展练习:
# 1. 实现文件下载进度条
# 2. 创建实时刷新的系统监控表格
# 3. 实现嵌套进度条
# 4. 创建交互式表格（可排序）
```

#### 检查点
- [ ] 掌握 Progress 进度条
- [ ] 能创建复杂表格
- [ ] 能使用 Tree 组件
- [ ] 理解 Rich 布局系统

---

## 📊 模块总结

### 知识点检查
- [ ] Console 基础
- [ ] Markdown 渲染
- [ ] Progress 进度条
- [ ] Table 表格

### 代码练习
- [ ] 练习18: Rich 基础
- [ ] 练习19: Markdown 查看器
- [ ] 练习20: 进度条与表格

### 输出成果
- [ ] 3个练习代码
- [ ] 学习笔记
- [ ] Kimi CLI UI 分析

---

## 🔄 下一步

完成本模块后，进入 **阶段3: LLM应用开发** → **模块06: Prompt Engineering**。

---

*Created by 老王 | Last Updated: 2025-01-10*
