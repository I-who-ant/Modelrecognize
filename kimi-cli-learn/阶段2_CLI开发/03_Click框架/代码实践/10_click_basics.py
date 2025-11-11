"""
练习10: Click 基础实践

学习目标:
- 掌握 @click.command() 和 @click.option()
- 理解位置参数和选项参数
- 掌握基本参数类型
"""

import click
from pathlib import Path


@click.command() # 定义命令行命令为 ls
@click.option( # 定义选项参数 --path, -p
    '--path', '-p',
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help='要列出的目录路径'
)
@click.option( # 定义选项参数 --all, -a
    '--all', '-a',
    'show_all',
    is_flag=True,
    help='显示隐藏文件'
)
@click.option( # 定义选项参数 --long, -l
    '--long', '-l',
    'long_format',
    is_flag=True,
    help='使用长格式（显示详细信息）'
)
def ls(path: Path, show_all: bool, long_format: bool):
    """列出目录内容（类似 ls 命令）

    示例:
        python 10_click_basics.py --path /home
        python 10_click_basics.py -p . -a
        python 10_click_basics.py -l
    """
    click.echo(f"目录: {path}") # 打印目录路径
    click.echo("-" * 50) # 打印分隔线

    items = list(path.iterdir())

    for item in items:
        # 跳过隐藏文件
        if not show_all and item.name.startswith('.'):
            continue

        if long_format:
            # 长格式：显示大小、类型
            item_type = "DIR" if item.is_dir() else "FILE"
            size = item.stat().st_size if item.is_file() else "-"
            click.echo(f"{item_type:5} {size:>10} {item.name}")
        else:
            # 简单格式
            click.echo(item.name)


@click.command()
@click.argument('src', type=click.Path(exists=True, path_type=Path)) # 定义位置参数 src, 必须存在的路径
@click.argument('dst', type=click.Path(path_type=Path)) # 定义位置参数 dst, 路径可以不存在
@click.option('--force', '-f', is_flag=True, help='强制覆盖')
def copy(src: Path, dst: Path, force: bool):
    """复制文件或目录

    SRC: 源路径
    DST: 目标路径

    示例:
        python 10_click_basics.py copy src.txt dst.txt
        python 10_click_basics.py copy src.txt dst.txt --force
    """
    import shutil  # 导入 shutil 模块，用于文件复制

    if dst.exists() and not force:
        click.echo(f"错误: {dst} 已存在，使用 --force 强制覆盖", err=True)
        return

    try:
        if src.is_file():
            shutil.copy2(src, dst)
            click.echo(f"✅ 复制文件: {src} -> {dst}") # 打印复制文件成功信息
        else:
            shutil.copytree(src, dst, dirs_exist_ok=force)
            click.echo(f"✅ 复制目录: {src} -> {dst}")
    except Exception as e:
        click.echo(f"❌ 复制失败: {e}", err=True)


if __name__ == '__main__':
    # 手动测试（实际应该用 click.group）
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'copy': # 如果命令行参数中包含 'copy'
        # 移除 'copy' 参数
        sys.argv.pop(1)
        copy()
    else:
        ls()


# 扩展练习:
# 1. 添加 --sort 选项（按名称/大小/时间排序）
# 2. 添加 --filter 选项（按扩展名过滤）
# 3. 添加递归列出（-R）功能
# 4. 添加颜色显示（使用 click.style）

