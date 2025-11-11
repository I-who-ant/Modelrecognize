# Click 装饰器完全指南

> 艹，老王我把Click框架的所有装饰器都给你讲明白！看完这个，你就知道怎么像`kimi-cli-main`那样定义命令了！

## 📚 目录

1. [核心概念](#核心概念)
2. [命令定义装饰器](#命令定义装饰器)
3. [参数装饰器](#参数装饰器)
4. [高级装饰器](#高级装饰器)
5. [Kimi CLI 实战分析](#kimi-cli-实战分析)

---

## 核心概念

### Click 是什么？

Click 是一个**命令行界面创建工具包**，通过**装饰器**将普通Python函数转换为命令行命令。

### 装饰器的作用

```python
@click.command()  # ← 这个装饰器把下面的函数变成了CLI命令
def hello():
    print("Hello!")
```

运行时：
```bash
$ python script.py
Hello!
```

**装饰器做了什么？**
- 解析命令行参数
- 验证参数类型
- 显示帮助信息
- 处理错误

---

## 命令定义装饰器

### 1. `@click.command()`

**作用**：将函数定义为一个CLI命令

**基础用法**：
```python
@click.command()
def greet():
    """这是帮助文档：打招呼命令"""
    click.echo("你好！")
```

运行：
```bash
$ python script.py
你好！

$ python script.py --help
Usage: script.py [OPTIONS]

  这是帮助文档：打招呼命令

Options:
  --help  Show this message and exit.
```

**参数说明**：
- `name`: 命令名称（默认使用函数名）
- `help`: 帮助文本（默认使用函数文档字符串）

```python
@click.command(name="say-hello", help="自定义帮助文本")
def greet():
    click.echo("你好！")
```

---

### 2. `@click.group()`

**作用**：创建命令组（可以包含多个子命令）

**基础用法**：
```python
@click.group()
def cli():
    """这是主命令"""
    pass

@cli.command()
def init():
    """初始化项目"""
    click.echo("初始化...")

@cli.command()
def build():
    """构建项目"""
    click.echo("构建...")
```

运行：
```bash
$ python script.py --help
Usage: script.py [OPTIONS] COMMAND [ARGS]...

  这是主命令

Commands:
  build  构建项目
  init   初始化项目

$ python script.py init
初始化...

$ python script.py build
构建...
```

**Kimi CLI 中的实际使用**：
```python
# 来自 kimi-cli-main/src/kimi_cli/cli.py

@click.group()
def kimi():
    """Kimi CLI - AI 编程助手"""
    pass

@kimi.command()  # ← 子命令1
def chat():
    """启动聊天"""
    pass

@kimi.command()  # ← 子命令2
def resume():
    """恢复会话"""
    pass
```

---

## 参数装饰器

### 3. `@click.option()`

**作用**：添加命令行选项（可选参数，以`--`或`-`开头）

**基础语法**：
```python
@click.option('--name', '-n', default='World', help='你的名字')
```

**完整示例**：
```python
@click.command()
@click.option('--name', '-n', default='World', help='你的名字')
@click.option('--count', '-c', default=1, help='重复次数')
def greet(name, count):
    """打招呼命令"""
    for _ in range(count):
        click.echo(f"Hello {name}!")
```

运行：
```bash
$ python script.py --name Alice --count 3
Hello Alice!
Hello Alice!
Hello Alice!

$ python script.py -n Bob -c 2
Hello Bob!
Hello Bob!
```

#### **Option 参数详解**

| 参数 | 说明 | 示例 |
|------|------|------|
| 第一个参数 | 完整选项名 | `'--name'` |
| 第二个参数 | 短选项名（可选） | `'-n'` |
| `default` | 默认值 | `default='World'` |
| `help` | 帮助文本 | `help='你的名字'` |
| `type` | 参数类型 | `type=int` |
| `required` | 是否必需 | `required=True` |
| `is_flag` | 是否为布尔标志 | `is_flag=True` |
| `multiple` | 是否允许多次指定 | `multiple=True` |
| `prompt` | 交互式提示 | `prompt='请输入名字'` |

#### **常用模式**

**1. 布尔标志（Flag）**
```python
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def cmd(verbose): # verbose指:是否启用详细模式
    if verbose:
        click.echo("详细模式已启用")
```

```bash
$ python script.py -v
详细模式已启用
```

**2. 类型转换**
```python
@click.option('--count', type=int, default=1)
@click.option('--ratio', type=float, default=1.0)
@click.option('--name', type=str)
```

**3. 多选项（Multiple）**
```python
@click.option('--exclude', '-e', multiple=True, help='排除的文件')
def cmd(exclude):
    for item in exclude:
        click.echo(f"排除: {item}") # 输出每个排除的文件
```

```bash
$ python script.py -e file1.txt -e file2.txt
排除: file1.txt
排除: file2.txt
```

**4. 选择列表（Choice）**
```python
@click.option('--level', type=click.Choice(['debug', 'info', 'warning']))
def cmd(level):
    click.echo(f"日志级别: {level}")
```

```bash
$ python script.py --level debug
日志级别: debug

$ python script.py --level invalid
Error: Invalid value for '--level': invalid is not one of debug, info, warning.
```

**5. 文件路径（Path）**
```python
@click.option('--config', type=click.Path(exists=True), help='配置文件路径')
def cmd(config):
    click.echo(f"配置文件: {config}")
```

**6. 交互式提示（Prompt）**
```python
@click.option('--password', prompt=True, hide_input=True)
def cmd(password):
    click.echo(f"密码长度: {len(password)}")
```

```bash
$ python script.py
Password: ****
密码长度: 4
```

---

### 4. `@click.argument()`

**作用**：添加位置参数（必需参数，不需要`--`）

**基础用法**：
```python
@click.command()
@click.argument('name')
def greet(name):
    """向某人打招呼"""
    click.echo(f"Hello {name}!")
```

```bash
$ python script.py Alice
Hello Alice!
```

#### **Argument vs Option**

| 特性 | Argument | Option |
|------|----------|--------|
| 前缀 | 无 | `--` 或 `-` |
| 必需性 | 默认必需 | 默认可选 |
| 位置 | 固定位置 | 任意位置 |
| 用途 | 核心参数 | 配置参数 |


**示例对比**：
```python
# 使用 Argument（位置参数）
@click.command()
@click.argument('source')
@click.argument('dest')
def copy(source, dest): # source指:源文件路径, dest指:目标文件路径
    click.echo(f"复制 {source} 到 {dest}")

# 使用方式：必须按顺序提供
# $ python script.py file1.txt file2.txt 
```

```python
# 使用 Option（选项参数）
@click.command()
@click.option('--source', required=True)
@click.option('--dest', required=True)
def copy(source, dest):
    click.echo(f"复制 {source} 到 {dest}")

# 使用方式：可以任意顺序，带有名称
# $ python script.py --dest file2.txt --source file1.txt
```

#### **Argument 参数**

```python
@click.argument('filename',
                type=click.Path(exists=True),  # 文件必须存在
                nargs=-1)                       # 接受多个参数
```

| 参数 | 说明 | 示例 |
|------|------|------|
| `type` | 参数类型 | `type=click.Path()` |
| `nargs` | 参数数量 | `nargs=-1`（无限个） |
| `required` | 是否必需 | `required=False` |

**多个参数示例**：
```python
@click.command()
@click.argument('files', nargs=-1, type=click.Path())
def process(files):
    for f in files:
        click.echo(f"处理: {f}")
```

```bash
$ python script.py file1.txt file2.txt file3.txt
处理: file1.txt
处理: file2.txt
处理: file3.txt
```

---

## 高级装饰器

### 5. `@click.pass_context`

**作用**：将Click上下文对象传递给函数

**上下文对象包含**：
- `ctx.obj`: 自定义数据对象
- `ctx.parent`: 父命令上下文
- `ctx.invoked_subcommand`: 被调用的子命令

**基础用法**：
```python
@click.group()
@click.pass_context
def cli(ctx):
    # 初始化上下文数据
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = True

@cli.command()
@click.pass_context
def cmd(ctx):
    # 访问上下文数据
    if ctx.obj['verbose']:
        click.echo("详细模式")
```

**Kimi CLI 实际使用**：
```python
# 来自 kimi-cli-main/src/kimi_cli/cli.py

@click.group()
@click.option('--verbose', '-v', is_flag=True)
@click.pass_context
def kimi(ctx, verbose):
    """Kimi CLI"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose  # ← 保存到上下文

@kimi.command()
@click.pass_context
def chat(ctx):
    """启动聊天"""
    verbose = ctx.obj['verbose']  # ← 从上下文读取
    if verbose:
        click.echo("详细日志已启用")
```

---

### 6. `@click.version_option()`

**作用**：自动添加`--version`选项

```python
@click.command()
@click.version_option(version='1.0.0', prog_name='MyApp')
def cli():
    pass
```

```bash
$ python script.py --version
MyApp, version 1.0.0
```

---

### 7. `@click.confirmation_option()`

**作用**：要求用户确认

```python
@click.command()
@click.confirmation_option(prompt='确定要删除吗？')
def delete():
    click.echo("已删除")
```

```bash
$ python script.py
确定要删除吗？ [y/N]: y
已删除
```

---

### 8. `@click.password_option()`

**作用**：添加密码输入选项

```python
@click.command()
@click.password_option()
def login(password):
    click.echo(f"密码长度: {len(password)}")
```

---

## Kimi CLI 实战分析

### Kimi CLI 的命令结构

让我们分析`kimi-cli-main/src/kimi_cli/cli.py`的实际代码：

```python
# ========== 主命令组 ==========
@click.group() # 定义主命令组,可以包含子命令
@click.version_option(version=__version__, prog_name="kimi") # 添加版本选项 :version是指指定版本号, prog_name是指指定程序名称
@click.option( # 添加全局verbose选项 :verbose是指是否启用详细日志模式
    "--verbose", "-v",
    is_flag=True,
    help="显示详细日志"
)
@click.pass_context # 传递上下文对象,用于在命令间传递数据
def kimi(ctx, verbose): # verbose是指是否启用详细日志模式
    """Kimi CLI - AI 编程助手"""
    # 初始化上下文
    ctx.ensure_object(dict) # 确保上下文对象存在,如果不存在则创建一个空字典
    ctx.obj["verbose"] = verbose # 保存verbose到上下文对象
```

**解释**：
1. `@click.group()`: 定义主命令组，可以包含子命令
2. `@click.version_option()`: 添加`--version`选项
3. `@click.option('--verbose', ...)`: 添加全局`-v`选项
4. `@click.pass_context`: 接收上下文对象，用于在命令间传递数据

---

### 子命令：`chat`

```python
@kimi.command()  # ← 注册为kimi的子命令
@click.option( # 添加UI模式选项 :ui是指指定聊天界面模式
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
    "--work-dir", "-w", # 添加工作目录选项 :work_dir是指指定工作目录
    type=click.Path(file_okay=False, dir_okay=True),
    default=Path.cwd(),
    help="工作目录"
)
@click.pass_context
def chat(ctx, ui, model, work_dir):
    """启动聊天会话"""
    # 获取全局verbose设置
    verbose = ctx.obj["verbose"]

    if verbose: # 如果启用了详细日志模式
        click.echo(f"UI: {ui}, Model: {model}, Dir: {work_dir}") # 打印详细日志

    # 启动聊天...
```

**装饰器分析**：

| 装饰器 | 作用 |
|--------|------|
| `@kimi.command()` | 将此函数注册为`kimi`的子命令 |
| `@click.option('--ui', ...)` | UI模式选项，限定4个选择 |
| `@click.option('--model', '-m', ...)` | 模型选项，有短选项`-m` |
| `@click.option('--work-dir', ...)` | 工作目录，类型为路径 |
| `@click.pass_context` | 接收上下文，获取全局配置 |

**使用方式**：
```bash
# 基础使用
$ kimi chat

# 指定UI模式
$ kimi chat --ui print

# 使用短选项
$ kimi chat -m gpt-3.5-turbo -w /tmp/work

# 带全局verbose
$ kimi -v chat --ui shell
```

---

### 子命令：`resume`

```python
@kimi.command()
@click.argument('session_id', required=False)
def resume(session_id):
    """恢复之前的会话"""
    if session_id:
        click.echo(f"恢复会话: {session_id}")
    else:
        # 列出所有会话
        click.echo("可用会话:")
        click.echo("  - session_001")
        click.echo("  - session_002")
```

**装饰器分析**：
- `@kimi.command()`: 子命令
- `@click.argument('session_id', required=False)`: 可选的位置参数

**使用方式**：
```bash
# 不提供参数，列出所有会话
$ kimi resume

# 提供session_id，恢复特定会话
$ kimi resume session_001
```

---

### 嵌套命令组：`config`

```python
@kimi.group()  # ← 子命令组
def config():
    """配置管理"""
    pass

@config.command()  # ← config组的子命令
@click.argument('key')
@click.argument('value')
def set(key, value):
    """设置配置项"""
    click.echo(f"设置 {key} = {value}")

@config.command()
@click.argument('key', required=False)
def get(key):
    """获取配置项"""
    if key:
        click.echo(f"{key} = <value>")
    else:
        click.echo("所有配置...")
```

**命令层次**：
```
kimi                    ← 主命令组
├── chat               ← 子命令
├── resume             ← 子命令
└── config             ← 子命令组
    ├── set            ← config的子命令
    └── get            ← config的子命令
```

**使用方式**：
```bash
$ kimi config set model gpt-4
设置 model = gpt-4

$ kimi config get model
model = <value>

$ kimi config get
所有配置...
```

---

## 装饰器顺序规则

**重要**：装饰器的顺序很重要！

### 正确顺序（从下往上）

```python
@click.command()           # 1. 最上面：命令/组定义
@click.option(...)         # 2. 中间：参数定义
@click.pass_context        # 3. 最下面：上下文传递
def my_command(ctx, ...):
    pass
```

### 错误示例（会报错）

```python
@click.pass_context        # ✗ 错误：这个应该在最下面
@click.option(...)
@click.command()
def my_command(ctx, ...):
    pass
```

---

## 常见模式总结

### 1. 简单命令
```python
@click.command()
@click.option('--name', default='World')
def greet(name):
    click.echo(f"Hello {name}!")
```

### 2. 带子命令的命令组
```python
@click.group()
def cli():
    pass

@cli.command()
def cmd1():
    pass

@cli.command()
def cmd2():
    pass
```

### 3. 带全局配置的命令组
```python
@click.group()
@click.option('--verbose', is_flag=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.command()
@click.pass_context
def cmd(ctx):
    if ctx.obj['verbose']:
        click.echo("详细模式")
```

### 4. 位置参数 + 选项参数
```python
@click.command()
@click.argument('source')
@click.argument('dest')
@click.option('--force', is_flag=True)
def copy(source, dest, force):
    if force:
        click.echo(f"强制复制 {source} 到 {dest}")
    else:
        click.echo(f"复制 {source} 到 {dest}")
```

---

## 类型转换参考

### 内置类型

```python
@click.option('--count', type=int)        # 整数
@click.option('--ratio', type=float)      # 浮点数
@click.option('--name', type=str)         # 字符串（默认）
@click.option('--flag', type=bool)        # 布尔值
```

### Click 特殊类型

```python
# 文件路径
@click.option('--config', type=click.Path(exists=True))

# 文件对象
@click.option('--input', type=click.File('r'))

# 选择列表
@click.option('--level', type=click.Choice(['a', 'b', 'c']))

# 整数范围
@click.option('--count', type=click.IntRange(0, 10))

# 浮点数范围
@click.option('--ratio', type=click.FloatRange(0.0, 1.0))

# UUID
@click.option('--id', type=click.UUID)

# 日期时间
@click.option('--date', type=click.DateTime())
```

---

## 快速参考表

### 常用装饰器

| 装饰器 | 作用 | 示例 |
|--------|------|------|
| `@click.command()` | 定义命令 | `@click.command()` |
| `@click.group()` | 定义命令组 | `@click.group()` |
| `@click.option()` | 添加选项 | `@click.option('--name')` |
| `@click.argument()` | 添加参数 | `@click.argument('file')` |
| `@click.pass_context` | 传递上下文 | `@click.pass_context` |
| `@click.version_option()` | 版本选项 | `@click.version_option('1.0')` |

### 常用参数

| 参数 | 用途 | 示例 |
|------|------|------|
| `default` | 默认值 | `default='value'` |
| `help` | 帮助文本 | `help='描述'` |
| `type` | 类型转换 | `type=int` |
| `required` | 是否必需 | `required=True` |
| `is_flag` | 布尔标志 | `is_flag=True` |
| `multiple` | 多次指定 | `multiple=True` |
| `prompt` | 交互提示 | `prompt='输入'` |

---

## 实战练习

### 练习1：实现Git风格的CLI

```python
@click.group()
def git():
    """Git 命令行工具"""
    pass

@git.command()
@click.argument('files', nargs=-1)
@click.option('--all', '-a', is_flag=True)
def add(files, all):
    """添加文件到暂存区"""
    if all:
        click.echo("添加所有文件")
    else:
        for f in files:
            click.echo(f"添加: {f}")

@git.command()
@click.option('--message', '-m', required=True, prompt='提交信息')
def commit(message):
    """提交更改"""
    click.echo(f"提交: {message}")

if __name__ == '__main__':
    git()
```

**使用**：
```bash
$ python git.py add file1.txt file2.txt
$ python git.py add --all
$ python git.py commit -m "Initial commit"
```

---

## 总结

**Click装饰器的本质**：
1. **`@click.command()`** 和 **`@click.group()`**: 定义命令结构
2. **`@click.option()`** 和 **`@click.argument()`**: 定义参数
3. **`@click.pass_context`**: 在命令间传递数据

**设计原则**：
- 命令名称使用小写，多个单词用`-`连接
- 选项名称使用`--`，短选项使用单个`-`
- 位置参数用于核心、必需的输入
- 选项参数用于配置、可选的输入
- 使用`help`提供清晰的文档

**学习建议**：
1. 先理解`@click.command()`基础用法
2. 掌握`@click.option()`的各种参数
3. 学习`@click.group()`创建子命令
4. 最后学习`@click.pass_context`传递数据

艹，看完这个，你应该能完全理解Kimi CLI是怎么定义那些命令的了！有啥不懂的继续问老王我！
