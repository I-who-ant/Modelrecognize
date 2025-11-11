"""练习19: Markdown 查看器"""
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
import sys

console = Console()

def view_markdown_file(file_path: Path):
    if not file_path.exists():
        console.print(f"[red]文件不存在: {file_path}[/red]")
        return
    content = file_path.read_text(encoding='utf-8')
    md = Markdown(content)
    console.print(md)

def demo_markdown():
    text = "# 标题\n\n**粗体** 和 *斜体*\n\n```python\nprint('Hello')\n```"
    console.print(Markdown(text))

def main():
    if len(sys.argv) > 1:
        view_markdown_file(Path(sys.argv[1]))
    else:
        demo_markdown()

if __name__ == '__main__':
    main()
