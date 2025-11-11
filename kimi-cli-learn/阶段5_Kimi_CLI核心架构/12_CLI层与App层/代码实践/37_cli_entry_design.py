"""练习37: CLI 入口设计"""
import click
from pathlib import Path
from typing import Literal
from dataclasses import dataclass


# ========== 1. CLI 配置 ==========

@dataclass
class CLIConfig:
    """CLI 配置"""
    ui_mode: Literal["shell", "print", "acp", "wire"]
    model: str
    provider: str
    work_dir: Path
    verbose: bool


# ========== 2. 参数验证 ==========

class WorkDirPath(click.Path):
    """工作目录路径验证器"""
    
    def __init__(self):
        super().__init__(
            exists=False,  # 允许不存在（会自动创建）
            file_okay=False,
            dir_okay=True,
            path_type=Path
        )
    
    def convert(self, value, param, ctx):
        path = super().convert(value, param, ctx)
        
        # 自动创建目录
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            click.echo(f"✓ 创建工作目录: {path}")
        
        return path


# ========== 3. Kimi CLI 入口设计 ==========

@click.group()
@click.version_option(version="1.0.0", prog_name="kimi")
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="显示详细日志"
)
@click.pass_context
def kimi(ctx, verbose: bool):
    """Kimi CLI - AI 编程助手"""
    # 初始化全局上下文
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    
    if verbose:
        click.echo("🔧 详细模式已启用")


# ========== 4. 主要命令 ==========

@kimi.command()
@click.option(
    "--ui",
    type=click.Choice(["shell", "print", "acp", "wire"]),
    default="shell",
    help="UI 模式"
)
@click.option(
    "--model", "-m",
    default="gpt-4",
    help="使用的模型"
)
@click.option(
    "--provider", "-p",
    type=click.Choice(["openai", "anthropic", "local"]),
    default="openai",
    help="LLM 提供商"
)
@click.option(
    "--work-dir", "-w",
    type=WorkDirPath(),
    default=Path.cwd(),
    help="工作目录"
)
@click.pass_context
def chat(ctx, ui: str, model: str, provider: str, work_dir: Path):
    """启动聊天会话"""
    config = CLIConfig(
        ui_mode=ui,
        model=model,
        provider=provider,
        work_dir=work_dir,
        verbose=ctx.obj["verbose"]
    )
    
    click.echo(f"🚀 启动 Kimi CLI")
    click.echo(f"   UI 模式: {config.ui_mode}")
    click.echo(f"   模型: {config.model}")
    click.echo(f"   提供商: {config.provider}")
    click.echo(f"   工作目录: {config.work_dir}")
    
    # 这里会调用 App 层
    # from kimi.app import App
    # app = App(config)
    # app.run()
    
    click.echo("\n💬 聊天会话已启动（演示模式）")


@kimi.command()
@click.argument("session_id", required=False)
def resume(session_id: str | None):
    """恢复之前的会话"""
    if session_id:
        click.echo(f"📂 恢复会话: {session_id}")
    else:
        click.echo("📋 列出所有会话:")
        # 列出所有会话
        sessions = ["session_001", "session_002"]
        for sid in sessions:
            click.echo(f"  - {sid}")


@kimi.command()
def list_sessions():
    """列出所有会话"""
    click.echo("📋 所有会话:")
    sessions = [
        {"id": "session_001", "created_at": "2024-01-01 10:00"},
        {"id": "session_002", "created_at": "2024-01-02 15:30"},
    ]
    
    for s in sessions:
        click.echo(f"  {s['id']:15} {s['created_at']}")


@kimi.command()
@click.argument("session_id")
@click.confirmation_option(prompt="确定要删除此会话吗？")
def delete_session(session_id: str):
    """删除会话"""
    click.echo(f"🗑️  删除会话: {session_id}")


# ========== 5. 配置管理命令 ==========

@kimi.group()
def config():
    """配置管理"""
    pass


@config.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str):
    """设置配置项"""
    click.echo(f"✓ 设置 {key} = {value}")


@config.command()
@click.argument("key", required=False)
def get(key: str | None):
    """获取配置项"""
    if key:
        click.echo(f"{key} = <value>")
    else:
        click.echo("所有配置:")
        click.echo("  model = gpt-4")
        click.echo("  provider = openai")


@config.command()
def show():
    """显示所有配置"""
    click.echo("📋 当前配置:")
    click.echo("  model: gpt-4")
    click.echo("  provider: openai")
    click.echo("  temperature: 0.7")


# ========== 6. 工具管理命令 ==========

@kimi.group()
def tools():
    """工具管理"""
    pass


@tools.command()
def list():
    """列出所有可用工具"""
    click.echo("🔧 可用工具:")
    tools_list = ["read", "write", "bash", "web"]
    for tool in tools_list:
        click.echo(f"  - {tool}")


@tools.command()
@click.argument("tool_name")
@click.option("--enable/--disable", default=True)
def toggle(tool_name: str, enable: bool):
    """启用/禁用工具"""
    status = "启用" if enable else "禁用"
    click.echo(f"✓ {status}工具: {tool_name}")


# ========== 演示函数 ==========

def demo_cli():
    """演示 CLI 功能"""
    print("\n" + "=" * 60)
    print("Kimi CLI 命令演示")
    print("=" * 60)
    
    print("\n1. 启动聊天:")
    print("   $ kimi chat --ui shell --model gpt-4")
    
    print("\n2. 恢复会话:")
    print("   $ kimi resume session_001")
    
    print("\n3. 配置管理:")
    print("   $ kimi config set model gpt-4")
    print("   $ kimi config show")
    
    print("\n4. 工具管理:")
    print("   $ kimi tools list")
    print("   $ kimi tools toggle bash --enable")


if __name__ == "__main__":
    # 演示
    # demo_cli()
    
    # 实际运行 CLI
    kimi()


# 学习要点:
# 1. Click 提供了强大的 CLI 框架
# 2. 使用 @click.group() 创建命令组
# 3. 使用 @click.command() 创建子命令
# 4. 使用 @click.option() 添加选项
# 5. 使用 @click.argument() 添加参数
# 6. ctx.obj 用于在命令间传递上下文
# 7. 自定义类型验证器提供更好的用户体验
