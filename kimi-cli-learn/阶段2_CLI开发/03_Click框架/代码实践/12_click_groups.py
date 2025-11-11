"""练习12: Click 命令组实践 - 多命令CLI应用"""
import click
from pathlib import Path
import json

class Config: # 定义配置类 Config
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True) # 定义传递配置对象的装饰器 pass_config

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@pass_config
def cli(config: Config, verbose: bool):
    """项目管理工具"""
    config.verbose = verbose
    if verbose:
        click.echo("🔧 详细模式已启用")

@cli.group() # 定义子命令组 project
def project():
    """项目管理命令"""
    pass

@project.command() # 定义子命令 init
@click.argument('name') # 定义位置参数 name
@click.option('--template', type=click.Choice(['python', 'node']), default='python') # 定义选项参数 template

@pass_config # 定义传递配置对象的装饰器 pass_config
def init(config: Config, name: str, template: str):
    """初始化新项目"""
    if config.verbose: # 如果启用了详细模式
        click.echo(f"使用模板: {template}")
    project_dir = Path(name) # 创建项目目录路径对象
    if project_dir.exists():
        click.echo(f"❌ 项目 {name} 已存在", err=True)
        return
    project_dir.mkdir()
    click.echo(f"✅ 创建项目: {name}")

@project.command() # 定义子命令 build
@pass_config
def build(config: Config):
    """构建项目"""
    click.echo("✅ 构建完成")

@cli.command() # 定义子命令 config
@click.argument('key')
@click.argument('value', required=False)
def config(key: str, value: str):
    """配置管理"""
    if value:
        click.echo(f"✅ 设置: {key} = {value}")
    else:
        click.echo(f"{key} = 未设置")

if __name__ == '__main__':
    cli()
