# 模块03: Click 命令行框架

**学习时长**: 5天

**学习目标**: 掌握 Click 框架，理解 Kimi CLI 的参数设计

---

## 📋 学习内容概览

1. **Click 基础** (Day 15-16)
2. **参数类型与验证** (Day 17)
3. **子命令与命令组** (Day 18)
4. **上下文传递与回调** (Day 19)

---

## 🎯 学习目标

- ✅ 掌握 @click.command() 和 @click.option()
- ✅ 理解 Click 参数类型系统
- ✅ 能创建多命令 CLI 应用
- ✅ 掌握上下文传递机制
- ✅ 理解 Kimi CLI 的参数设计

---

## 📚 学习资源

### 官方文档
- [Click 官方文档](https://click.palletsprojects.com/)
- [Click 中文文档](https://click-docs-zh-cn.readthedocs.io/)

### 推荐教程
- Real Python: Building Command Line Interfaces with Click
- Click 进阶教程

---

## 📖 详细学习内容

### 📝 01: Click 基础 (Day 15-16)

#### 学习内容

**基础命令定义**:
```python
import click

@click.command()
@click.option('--name', '-n', default='World', help='要打招呼的名字')
@click.option('--count', '-c', default=1, help='重复次数')
def hello(name: str, count: int):
    """简单的打招呼程序"""
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
```

**运行方式**:
```bash
# 使用默认值
python hello.py
# Hello World!

# 使用参数
python hello.py --name Alice --count 3
# Hello Alice!
# Hello Alice!
# Hello Alice!

# 使用短选项
python hello.py -n Bob -c 2
```

**参数类型**:
```python
import click

@click.command()
@click.option('--port', type=int, default=8000, help='端口号')
@click.option('--host', type=str, default='localhost', help='主机地址')
@click.option('--debug', is_flag=True, help='调试模式')
def serve(port: int, host: str, debug: bool):
    """启动开发服务器"""
    mode = "调试" if debug else "生产"
    click.echo(f'服务器运行在 {host}:{port} ({mode}模式)')

# 使用
# python serve.py --port 3000 --debug
```

**位置参数**:
```python
import click

@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
def copy(src: str, dst: str):
    """复制文件

    SRC: 源文件路径
    DST: 目标文件路径
    """
    click.echo(f'复制 {src} -> {dst}')

# 使用
# python copy.py input.txt output.txt
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/cli.py
import click
from typing import Literal, get_args
from pathlib import Path

UIMode = Literal["shell", "print", "acp", "wire"]

@click.command()
@click.option(
    "--work-dir",
    "-w",
    "work_dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd,
    help="工作目录",
)
@click.option(
    "--ui",
    "ui",
    type=click.Choice(get_args(UIMode)),  # 从 Literal 获取选项
    default="shell",
    help="UI 模式",
)
@click.option(
    "--yolo",
    is_flag=True,
    help="YOLO 模式（自动确认）",
)
def kimi(
    work_dir: Path,
    ui: UIMode,
    yolo: bool,
):
    """Kimi CLI - 你的 AI 编程助手"""
    # 启动应用
    pass
```

#### 实践练习

**练习10**: 文件管理 CLI
```python
# 文件: 代码实践/10_click_basics.py

import click
from pathlib import Path

@click.command()
@click.option(
    '--path', '-p',
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help='要列出的目录路径'
)
@click.option(
    '--all', '-a',
    'show_all',
    is_flag=True,
    help='显示隐藏文件'
)
@click.option(
    '--long', '-l',
    'long_format',
    is_flag=True,
    help='使用长格式（显示详细信息）'
)
def ls(path: Path, show_all: bool, long_format: bool):
    """列出目录内容（类似 ls 命令）"""
    click.echo(f"目录: {path}")
    click.echo("-" * 50)

    for item in path.iterdir():
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
@click.argument('src', type=click.Path(exists=True, path_type=Path))
@click.argument('dst', type=click.Path(path_type=Path))
@click.option('--force', '-f', is_flag=True, help='强制覆盖')
def copy(src: Path, dst: Path, force: bool):
    """复制文件或目录

    SRC: 源路径
    DST: 目标路径
    """
    import shutil

    if dst.exists() and not force:
        click.echo(f"错误: {dst} 已存在，使用 --force 强制覆盖", err=True)
        return

    try:
        if src.is_file():
            shutil.copy2(src, dst)
            click.echo(f"✅ 复制文件: {src} -> {dst}")
        else:
            shutil.copytree(src, dst, dirs_exist_ok=force)
            click.echo(f"✅ 复制目录: {src} -> {dst}")
    except Exception as e:
        click.echo(f"❌ 复制失败: {e}", err=True)


if __name__ == '__main__':
    # 手动测试（实际应该用 click.group）
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'copy':
        copy()
    else:
        ls()


# 扩展练习:
# 1. 添加 --sort 选项（按名称/大小/时间排序）
# 2. 添加 --filter 选项（按扩展名过滤）
# 3. 添加递归列出（-R）功能
# 4. 添加颜色显示（使用 click.style）
```

#### 检查点
- [ ] 能使用 @click.command() 定义命令
- [ ] 理解 @click.option() 和 @click.argument() 的区别
- [ ] 能使用 is_flag、type、default 等参数
- [ ] 理解 click.echo() 的作用

---

### 📝 02: 参数类型与验证 (Day 17)

#### 学习内容

**内置参数类型**:
```python
import click

@click.command()
@click.option('--port', type=click.IntRange(1, 65535), help='端口号（1-65535）')
@click.option('--env', type=click.Choice(['dev', 'prod', 'test']), help='环境')
@click.option('--config', type=click.Path(exists=True, dir_okay=False), help='配置文件')
@click.option('--output-dir', type=click.Path(file_okay=False, dir_okay=True), help='输出目录')
def deploy(port: int, env: str, config: str, output_dir: str):
    """部署应用"""
    click.echo(f"部署到 {env} 环境，端口 {port}")
    click.echo(f"配置文件: {config}")
    click.echo(f"输出目录: {output_dir}")
```

**自定义参数类型**:
```python
import click

class EmailParamType(click.ParamType):
    """自定义邮箱参数类型"""
    name = "email"

    def convert(self, value, param, ctx):
        if '@' not in value:
            self.fail(f'{value} 不是有效的邮箱地址', param, ctx)
        return value

EMAIL = EmailParamType()

@click.command()
@click.option('--email', type=EMAIL, required=True, help='用户邮箱')
def register(email: str):
    """用户注册"""
    click.echo(f"注册邮箱: {email}")

# 使用
# python register.py --email test@example.com  ✅
# python register.py --email invalid           ❌ 报错
```

**参数验证回调**:
```python
import click

def validate_even(ctx, param, value):
    """验证参数是否为偶数"""
    if value % 2 != 0:
        raise click.BadParameter('必须是偶数')
    return value

@click.command()
@click.option(
    '--count',
    type=int,
    callback=validate_even,
    help='计数（必须是偶数）'
)
def process(count: int):
    """处理数据"""
    click.echo(f"处理 {count} 条数据")

# 使用
# python process.py --count 10  ✅
# python process.py --count 9   ❌ 报错: 必须是偶数
```

**环境变量支持**:
```python
import click

@click.command()
@click.option(
    '--api-key',
    envvar='API_KEY',  # 从环境变量读取
    required=True,
    help='API 密钥（或设置 API_KEY 环境变量）'
)
def api_call(api_key: str):
    """调用 API"""
    click.echo(f"使用 API Key: {api_key[:5]}...")

# 使用
# export API_KEY="sk-xxxxx"
# python api_call.py  （自动从环境变量读取）
# python api_call.py --api-key "sk-yyyyy"  （覆盖环境变量）
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/cli.py
@click.option(
    "--model-name",
    "-m",
    "model_name",
    envvar="KIMI_MODEL",  # 支持环境变量
    help="模型名称",
)
@click.option(
    "--provider-config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    envvar="KIMI_PROVIDER_CONFIG",
    help="LLM Provider 配置文件路径",
)
```

#### 实践练习

**练习11**: 参数验证系统
```python
# 文件: 代码实践/11_click_validation.py

import click
from pathlib import Path
import re

# 自定义参数类型: URL
class URLParamType(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(value):
            self.fail(f'{value} 不是有效的 URL', param, ctx)
        return value

URL = URLParamType()

# 验证回调函数
def validate_positive(ctx, param, value):
    """验证正数"""
    if value <= 0:
        raise click.BadParameter('必须是正数')
    return value

def validate_file_extension(ctx, param, value):
    """验证文件扩展名"""
    if value is None:
        return value

    allowed_extensions = ['.txt', '.md', '.json', '.yaml']
    path = Path(value)

    if path.suffix not in allowed_extensions:
        raise click.BadParameter(
            f'不支持的文件类型 {path.suffix}，'
            f'仅支持: {", ".join(allowed_extensions)}'
        )
    return value

@click.command()
@click.option(
    '--url',
    type=URL,
    required=True,
    help='目标 URL'
)
@click.option(
    '--timeout',
    type=int,
    default=30,
    callback=validate_positive,
    help='超时时间（秒，必须为正数）'
)
@click.option(
    '--output',
    type=click.Path(dir_okay=False, path_type=Path),
    callback=validate_file_extension,
    help='输出文件路径'
)
@click.option(
    '--api-key',
    envvar='MY_API_KEY',
    required=True,
    hide_input=True,  # 隐藏输入（用于密码）
    help='API 密钥（或设置 MY_API_KEY 环境变量）'
)
def fetch(url: str, timeout: int, output: Path, api_key: str):
    """从 URL 获取数据

    示例:

        python 11_click_validation.py --url https://example.com --timeout 10 --output data.json --api-key secret
    """
    click.echo(f"✅ URL: {url}")
    click.echo(f"✅ 超时: {timeout} 秒")
    click.echo(f"✅ 输出: {output}")
    click.echo(f"✅ API Key: {api_key[:5]}...")

    # 实际获取数据的逻辑
    click.echo("\n开始获取数据...")


if __name__ == '__main__':
    fetch()


# 扩展练习:
# 1. 添加邮箱类型验证
# 2. 添加 IPv4 地址类型验证
# 3. 添加日期格式验证（YYYY-MM-DD）
# 4. 添加多值参数验证（逗号分隔的列表）
```

#### 检查点
- [ ] 掌握 Click 内置参数类型
- [ ] 能创建自定义参数类型
- [ ] 能使用 callback 验证参数
- [ ] 理解环境变量支持

---

### 📝 03: 子命令与命令组 (Day 18)

#### 学习内容

**命令组基础**:
```python
import click

@click.group()
def cli():
    """文件管理工具"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def list(path: str):
    """列出文件"""
    click.echo(f"列出 {path} 的文件")

@cli.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dst', type=click.Path())
def copy(src: str, dst: str):
    """复制文件"""
    click.echo(f"复制 {src} -> {dst}")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def delete(path: str):
    """删除文件"""
    click.echo(f"删除 {path}")

if __name__ == '__main__':
    cli()

# 使用
# python tool.py list /path/to/dir
# python tool.py copy src.txt dst.txt
# python tool.py delete file.txt
```

**嵌套命令组**:
```python
import click

@click.group()
def cli():
    """主命令"""
    pass

@cli.group()
def user():
    """用户管理"""
    pass

@user.command()
@click.argument('username')
def create(username: str):
    """创建用户"""
    click.echo(f"创建用户: {username}")

@user.command()
@click.argument('username')
def delete(username: str):
    """删除用户"""
    click.echo(f"删除用户: {username}")

@cli.group()
def project():
    """项目管理"""
    pass

@project.command()
@click.argument('name')
def init(name: str):
    """初始化项目"""
    click.echo(f"初始化项目: {name}")

if __name__ == '__main__':
    cli()

# 使用
# python app.py user create alice
# python app.py user delete bob
# python app.py project init my-project
```

**命令别名**:
```python
import click

class AliasedGroup(click.Group):
    """支持别名的命令组"""

    def get_command(self, ctx, cmd_name):
        # 定义别名映射
        aliases = {
            'ls': 'list',
            'cp': 'copy',
            'rm': 'delete',
        }

        # 查找别名
        cmd_name = aliases.get(cmd_name, cmd_name)
        return click.Group.get_command(self, ctx, cmd_name)

@click.group(cls=AliasedGroup)
def cli():
    """支持别名的 CLI"""
    pass

@cli.command()
def list():
    """列出文件（别名: ls）"""
    click.echo("列出文件")

@cli.command()
def copy():
    """复制文件（别名: cp）"""
    click.echo("复制文件")

# 使用
# python app.py list  或  python app.py ls
# python app.py copy  或  python app.py cp
```

#### 实践练习

**练习12**: 多命令 CLI 应用
```python
# 文件: 代码实践/12_click_groups.py

import click
from pathlib import Path
import json

# 全局配置（可以在命令间共享）
class Config:
    def __init__(self):
        self.verbose = False
        self.config_file = None

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@click.option('--config', type=click.Path(exists=True), help='配置文件')
@pass_config
def cli(config: Config, verbose: bool, config_file: str):
    """项目管理工具

    支持项目初始化、构建、部署等功能
    """
    config.verbose = verbose
    config.config_file = config_file

    if verbose:
        click.echo("🔧 详细模式已启用")


# ========== 项目管理 ==========
@cli.group()
def project():
    """项目管理命令"""
    pass

@project.command()
@click.argument('name')
@click.option('--template', type=click.Choice(['python', 'node', 'rust']), default='python')
@pass_config
def init(config: Config, name: str, template: str):
    """初始化新项目

    NAME: 项目名称
    """
    if config.verbose:
        click.echo(f"使用模板: {template}")

    project_dir = Path(name)
    if project_dir.exists():
        click.echo(f"❌ 项目 {name} 已存在", err=True)
        return

    project_dir.mkdir()
    click.echo(f"✅ 创建项目: {name} ({template})")

@project.command()
@pass_config
def build(config: Config):
    """构建项目"""
    if config.verbose:
        click.echo("开始构建...")
    click.echo("✅ 构建完成")

@project.command()
@click.option('--env', type=click.Choice(['dev', 'prod']), default='dev')
@pass_config
def deploy(config: Config, env: str):
    """部署项目"""
    if config.verbose:
        click.echo(f"部署到 {env} 环境")
    click.echo(f"✅ 部署完成 ({env})")


# ========== 依赖管理 ==========
@cli.group()
def deps():
    """依赖管理命令"""
    pass

@deps.command()
@click.argument('package')
@pass_config
def add(config: Config, package: str):
    """添加依赖

    PACKAGE: 包名
    """
    if config.verbose:
        click.echo(f"正在添加 {package}...")
    click.echo(f"✅ 已添加: {package}")

@deps.command()
@pass_config
def list(config: Config):
    """列出所有依赖"""
    deps_list = ["click", "requests", "pydantic"]

    if config.verbose:
        click.echo("依赖列表:")

    for dep in deps_list:
        click.echo(f"  - {dep}")


# ========== 配置管理 ==========
@cli.command()
@click.argument('key')
@click.argument('value', required=False)
@pass_config
def config(config: Config, key: str, value: str):
    """查看或设置配置

    KEY: 配置键
    VALUE: 配置值（可选，不提供则查看当前值）
    """
    config_file = Path('.project-config.json')

    # 读取现有配置
    if config_file.exists():
        with open(config_file) as f:
            cfg = json.load(f)
    else:
        cfg = {}

    if value is None:
        # 查看配置
        current = cfg.get(key, "未设置")
        click.echo(f"{key} = {current}")
    else:
        # 设置配置
        cfg[key] = value
        with open(config_file, 'w') as f:
            json.dump(cfg, f, indent=2)
        click.echo(f"✅ 已设置: {key} = {value}")


if __name__ == '__main__':
    cli()


# 使用示例:
# python 12_click_groups.py --verbose project init my-app --template python
# python 12_click_groups.py project build
# python 12_click_groups.py project deploy --env prod
# python 12_click_groups.py deps add requests
# python 12_click_groups.py deps list
# python 12_click_groups.py config api_key sk-xxxxx
# python 12_click_groups.py config api_key


# 扩展练习:
# 1. 添加 test 命令组（运行测试）
# 2. 添加 clean 命令（清理临时文件）
# 3. 实现配置文件的完整 CRUD
# 4. 添加命令自动补全脚本生成
```

#### 检查点
- [ ] 能使用 @click.group() 创建命令组
- [ ] 理解嵌套命令组
- [ ] 能在命令间传递上下文
- [ ] 理解命令别名机制

---

### 📝 04: 上下文传递与回调 (Day 19)

#### 学习内容

**Context 上下文对象**:
```python
import click

@click.group()
@click.pass_context
def cli(ctx):
    """主命令"""
    # ctx.obj 可以存储全局数据
    ctx.obj = {'verbose': False}

@cli.command()
@click.pass_context
def status(ctx):
    """查看状态"""
    verbose = ctx.obj.get('verbose')
    click.echo(f"详细模式: {verbose}")
```

**自定义上下文类**:
```python
import click

class AppContext:
    def __init__(self):
        self.verbose = False
        self.config_path = None
        self.session = None

    def log(self, msg: str):
        if self.verbose:
            click.echo(f"[LOG] {msg}")

pass_app_context = click.make_pass_decorator(AppContext, ensure=True)

@click.group()
@click.option('--verbose', '-v', is_flag=True)
@pass_app_context
def cli(ctx: AppContext, verbose: bool):
    """应用主命令"""
    ctx.verbose = verbose
    ctx.log("应用启动")

@cli.command()
@pass_app_context
def process(ctx: AppContext):
    """处理数据"""
    ctx.log("开始处理...")
    click.echo("处理完成")
```

**参数回调函数**:
```python
import click
from pathlib import Path

def validate_and_create_dir(ctx, param, value):
    """验证目录，不存在则创建"""
    if value is None:
        return value

    path = Path(value)
    if not path.exists():
        click.confirm(f'目录 {path} 不存在，是否创建?', abort=True)
        path.mkdir(parents=True)
        click.echo(f"已创建目录: {path}")

    return path

@click.command()
@click.option(
    '--output-dir',
    type=click.Path(path_type=Path),
    callback=validate_and_create_dir,
    help='输出目录'
)
def export(output_dir: Path):
    """导出数据"""
    click.echo(f"导出到: {output_dir}")
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/cli.py
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.pass_context
def kimi(ctx: click.Context, ...):
    """Kimi CLI 主命令"""
    # 使用 context_settings 自定义行为
    pass

# src/kimi_cli/app.py
class KimiCLI:
    @staticmethod
    async def create(...) -> "KimiCLI":
        """创建 KimiCLI 实例（工厂方法）"""
        # 初始化配置、会话等
        pass
```

#### 实践练习

**练习13**: 分析 Kimi CLI 参数设计
```markdown
# 文件: 代码实践/13_kimi_cli_params_analysis.md

# Kimi CLI 参数设计分析

## 1. 参数分类

### 核心参数
- `--work-dir` / `-w`: 工作目录（Path 类型）
- `--ui`: UI 模式（Literal 类型 + Choice）
- `--command` / `-c`: 执行的命令

### LLM 配置参数
- `--model-name` / `-m`: 模型名称（支持环境变量）
- `--provider-config`: Provider 配置文件
- `--api-key`: API 密钥（支持环境变量）
- `--base-url`: API 基础 URL

### 行为控制参数
- `--yolo`: 自动确认模式（Flag）
- `--dry-run`: 演练模式，不实际执行
- `--debug`: 调试模式

### 输入输出参数
- `--input-format`: 输入格式（text/stream-json）
- `--output-format`: 输出格式
- `--file` / `-f`: 输入文件

## 2. 设计亮点

### 类型安全
```python
UIMode = Literal["shell", "print", "acp", "wire"]

@click.option(
    "--ui",
    type=click.Choice(get_args(UIMode)),  # 从 Literal 获取
    default="shell",
)
def kimi(ui: UIMode):  # 类型安全
    pass
```

**优点**:
- Literal 定义可能值
- get_args() 自动提取选项
- 类型检查器（mypy/pyright）能验证

### 环境变量支持
```python
@click.option(
    "--api-key",
    envvar="KIMI_API_KEY",  # 环境变量
    help="API 密钥",
)
```

**优点**:
- 敏感信息不暴露在命令行
- 支持 .env 文件
- CI/CD 友好

### Path 类型处理
```python
@click.option(
    "--work-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd,
)
```

**优点**:
- 自动验证路径存在性
- 返回 pathlib.Path 对象
- 支持默认值函数

## 3. 最佳实践

1. **参数命名规范**
   - 长选项用 `--`（如 `--work-dir`）
   - 短选项用 `-`（如 `-w`）
   - 使用 kebab-case 命名

2. **类型安全**
   - 使用 Literal 限定可能值
   - 使用 get_args() 自动提取
   - 提供完整的类型注解

3. **环境变量**
   - 敏感信息用环境变量
   - 命名规范: `KIMI_XXX`
   - 提供默认值

4. **帮助文本**
   - 每个参数都有清晰的 help
   - 命令有完整的 docstring
   - 使用示例

## 4. 改进建议

1. **添加参数验证**
   ```python
   def validate_work_dir(ctx, param, value):
       if not value.exists():
           raise click.BadParameter(f"目录不存在: {value}")
       return value
   ```

2. **添加配置文件支持**
   ```python
   @click.option(
       "--config",
       type=click.Path(exists=True),
       help="配置文件路径"
   )
   ```

3. **添加日志级别控制**
   ```python
   @click.option(
       "--log-level",
       type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']),
       default='INFO'
   )
   ```

## 5. 练习任务

- [ ] 为 Kimi CLI 添加一个新参数
- [ ] 实现自定义参数类型
- [ ] 添加参数验证回调
- [ ] 编写单元测试
```

#### 检查点
- [ ] 理解 Click Context 对象
- [ ] 能使用 @click.pass_context
- [ ] 能创建自定义上下文类
- [ ] 理解参数回调机制
- [ ] 能分析 Kimi CLI 的参数设计

---

## 📊 模块总结

### 知识点检查
- [ ] Click 基础命令定义
- [ ] 参数类型与验证
- [ ] 命令组与子命令
- [ ] 上下文传递

### 代码练习
- [ ] 练习10: Click 基础
- [ ] 练习11: 参数验证
- [ ] 练习12: 多命令 CLI
- [ ] 练习13: Kimi CLI 参数分析

### 输出成果
- [ ] 4个练习代码
- [ ] Kimi CLI 参数分析文档
- [ ] 学习笔记

---

## 🔄 下一步

完成本模块后，进入 **模块04: Prompt Toolkit**。

---

*Created by 老王 | Last Updated: 2025-01-10*
