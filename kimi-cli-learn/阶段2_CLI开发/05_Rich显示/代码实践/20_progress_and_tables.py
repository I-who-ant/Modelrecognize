"""练习20: 进度条与表格实践"""
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
import time

console = Console() # 创建控制台实例

def demo_progress():
    with Progress() as progress:
        task = progress.add_task("[cyan]处理中...", total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

def demo_table():
    table = Table(title="成绩表")
    table.add_column("姓名", style="cyan")
    table.add_column("分数", justify="right", style="green")
    table.add_row("张三", "95")
    table.add_row("李四", "87")
    console.print(table)

def main(): # 主函数
    demo_progress()
    console.print()
    demo_table()

if __name__ == '__main__':
    main()
