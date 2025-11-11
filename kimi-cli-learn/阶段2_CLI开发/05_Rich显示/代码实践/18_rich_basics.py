"""练习18: Rich 基础实践"""
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

def demo_basic_styles(): # 演示基本样式
    console.print("[bold]粗体[/bold]")
    console.print("[italic]斜体[/italic]")
    console.print("[red]红色[/red]")

def demo_panels():
    console.print(Panel("简单面板")) # 打印简单面板
    console.print(Panel("成功", title="✅ 成功", border_style="green")) # 打印成功面板

def demo_syntax(): # 演示语法高亮
    code = 'def hello():\n    print("Hello")'
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True) # 创建语法高亮实例
    console.print(Panel(syntax, title="代码", border_style="cyan")) # 打印代码面板

def main(): # 主函数
    demo_basic_styles()
    demo_panels()
    demo_syntax()

if __name__ == '__main__':
    main()
