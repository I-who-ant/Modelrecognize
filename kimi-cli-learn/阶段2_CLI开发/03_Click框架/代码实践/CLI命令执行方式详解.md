# CLI 命令执行方式详解

> 艹，老王我把Python CLI的执行方式给你讲明白！为什么有时候要`python script.py`，有时候直接`kimi`就行？

## 📚 目录

1. [问题现象](#问题现象)
2. [本质区别](#本质区别)
3. [执行方式对比](#执行方式对比)
4. [从脚本到命令的演进](#从脚本到命令的演进)
5. [Kimi CLI 是如何安装的](#kimi-cli-是如何安装的)
6. [实战：让你的CLI像kimi一样使用](#实战让你的cli像kimi一样使用)

---

## 问题现象

### 方式1：需要 `python` 前缀

```bash
$ python git.py add file1.txt file2.txt
$ python script.py --version
```

### 方式2：直接使用命令

```bash
$ kimi --version
$ kimi chat --ui shell
```

**疑问**：为什么定义的函数是`cli()`，却可以用`kimi`调用？

---

## 本质区别

### 方式1：直接运行Python脚本

```python
# git.py
import click

@click.group()
def git():
    pass

@git.command()
def add():
    pass

if __name__ == '__main__':
    git()  # ← 注意这里调用了git()
```

**执行流程**：
1. 运行 `python git.py add`
2. Python 解释器加载 `git.py`
3. 检查 `if __name__ == '__main__':`（条件为真**）
4. 执行 `git()`
5. Click 解析命令行参数 `add`
6. 执行对应的命令

**特点**：
- ✅ 简单，适合开发测试
- ❌ 每次都要输入 `python script.py`
- ❌ 需要知道脚本的路径
- ❌ 不够专业

---**

### 方式2：安装为系统命令（推荐）

```bash
$ kimi chat
```

**执行流程**：
1. 运行 `kimi chat`
2. 系统在 `PATH` 中查找 `kimi` 命令
3. 找到可执行文件 `/path/to/bin/kimi`
4. 执行该文件（实际是一个Python脚本包装器）
5. 调用对应的Python函数
6. Click 解析命令行参数

**特点**：
- ✅ 像系统命令一样使用
- ✅ 不需要知道脚本路径
- ✅ 不需要 `python` 前缀
- ✅ 专业，用户友好

---

## 执行方式对比

### 表格对比

| 特性 | 直接运行脚本 | 安装为命令 |
|------|-------------|-----------|
| 执行方式 | `python script.py` | `command` |
| 需要路径 | ✅ 是 | ❌ 否 |
| 需要Python前缀 | ✅ 是 | ❌ 否 |
| 全局可用 | ❌ 否 | ✅ 是 |
| 适用场景 | 开发测试 | 生产使用 |
| 用户体验 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 示例对比

**直接运行脚本**：
```bash
# 需要知道脚本在哪里
$ cd /path/to/project
$ python git.py add file.txt

# 或者使用绝对路径
$ python /path/to/project/git.py add file.txt
```

**安装为命令**：
```bash
# 在任何目录都能使用
$ cd ~
$ kimi chat

$ cd /tmp
$ kimi --version
```

---

## 从脚本到命令的演进

### 阶段1：最简单的脚本

```python
# hello.py
print("Hello, World!")
```

运行：
```bash
$ python hello.py
Hello, World!
```

---

### 阶段2：带参数的脚本

```python
# greet.py
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "World"
print(f"Hello, {name}!")
```

运行：
```bash
$ python greet.py Alice
Hello, Alice!
```

**问题**：
- 需要手动解析参数
- 没有帮助信息
- 不够优雅

---

### 阶段3：使用 Click 框架

```python
# greet.py
import click

@click.command()
@click.option('--name', default='World', help='你的名字')
def greet(name):
    """打招呼命令"""
    click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    greet()
```

运行：
```bash
$ python greet.py --name Alice
Hello, Alice!

$ python greet.py --help
Usage: greet.py [OPTIONS]

  打招呼命令

Options:
  --name TEXT  你的名字
  --help       Show this message and exit.
```

**改进**：
- ✅ 自动解析参数
- ✅ 自动生成帮助信息
- ✅ 类型检查
- ❌ 仍需要 `python` 前缀

---

### 阶段4：安装为系统命令（终极形态）

**项目结构**：
```
my-cli/
├── setup.py          # 或 pyproject.toml
├── my_cli/
│   ├── __init__.py
│   └── cli.py
```

**cli.py**：
```python
# my_cli/cli.py
import click

@click.command()
@click.option('--name', default='World')
def greet(name):
    """打招呼命令"""
    click.echo(f"Hello, {name}!")
```

**setup.py**：
```python
from setuptools import setup, find_packages

setup(
    name='my-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
    ],
    entry_points={
        'console_scripts': [
            'greet=my_cli.cli:greet',  # ← 关键！定义命令名称
        ],
    },
)
```

**安装**：
```bash
$ pip install -e .
```

**使用**：
```bash
$ greet --name Alice
Hello, Alice!

$ greet --help
```

**magic发生了什么？**

1. `pip install -e .` 安装时
2. setuptools 读取 `entry_points`
3. 创建一个名为 `greet` 的可执行文件
4. 放到 Python 的 `bin` 目录（在 `PATH` 中）
5. 该文件是一个**包装器**，会调用 `my_cli.cli:greet`

---

## entry_points 详解

### 什么是 entry_points？

`entry_points` 是 Python 包安装时的配置，用于创建**命令行入口点**。

### 语法解析

```python
entry_points={
    'console_scripts': [
        'command_name=package.module:function',
    ],
}
```

**组成部分**：
- `command_name`: 在命令行中使用的命令名称（可以任意起）
- `package.module`: Python 模块路径
- `function`: 要调用的函数名

### 示例对比

#### 示例1：命令名与函数名相同

```python
# setup.py
entry_points={
    'console_scripts': [
        'greet=my_cli.cli:greet',
        #  ↑         ↑        ↑
        # 命令名   模块路径  函数名
    ],
}
```

```bash
$ greet --name Alice  # ← 使用命令名
```

#### 示例2：命令名与函数名不同

```python
# cli.py
@click.command()
def hello():  # ← 函数名是 hello
    click.echo("Hello!")

# setup.py
entry_points={
    'console_scripts': [
        'greet=my_cli.cli:hello',  # ← 命令名是 greet
    ],
}
```

```bash
$ greet  # ← 用的是命令名 greet，不是函数名 hello
Hello!
```

#### 示例3：Kimi CLI 的实际配置

```python
# kimi-cli-main/setup.py 或 pyproject.toml
entry_points={
    'console_scripts': [
        'kimi=kimi_cli.cli:kimi',
        # ↑            ↑       ↑
        # 命令名   模块路径  函数名
    ],
}
```

**对应关系**：
- 命令名：`kimi`（你在终端输入的）
- 模块：`kimi_cli.cli`（文件路径：`src/kimi_cli/cli.py`）
- 函数：`kimi`（定义的Click函数）

```python
# src/kimi_cli/cli.py
@click.group()
def kimi():  # ← 这个函数名
    """Kimi CLI"""
    pass
```

---

## Kimi CLI 是如何安装的

### 1. 项目结构

```
kimi-cli-main/
├── pyproject.toml    # 或 setup.py
├── src/
│   └── kimi_cli/
│       ├── __init__.py
│       └── cli.py
```

### 2. pyproject.toml 配置

```toml
[project.scripts]
kimi = "kimi_cli.cli:kimi"
#  ↑           ↑         ↑
# 命令名    模块路径   函数名
```

或者使用 `setup.py`：

```python
from setuptools import setup

setup(
    name='kimi-cli',
    entry_points={
        'console_scripts': [
            'kimi=kimi_cli.cli:kimi',
        ],
    },
)
```

### 3. 安装过程

```bash
# 开发模式安装（推荐）
$ cd kimi-cli-main
$ pip install -e .

# 或者正式安装
$ pip install .

# 或者从 PyPI 安装
$ pip install kimi-cli
```

### 4. 安装后发生了什么？

**第1步：创建包装脚本**

在 Python 的 `bin` 目录创建一个名为 `kimi` 的文件：

```python
# /path/to/python/bin/kimi (自动生成，不是你写的)
#!/path/to/python
# -*- coding: utf-8 -*-
import re
import sys
from kimi_cli.cli import kimi

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(kimi())
```

**第2步：添加到 PATH**

Python 的 `bin` 目录在 `PATH` 中，所以可以直接使用 `kimi` 命令。

```bash
$ which kimi
/home/user/.local/bin/kimi

$ echo $PATH
/home/user/.local/bin:/usr/bin:/bin:...
```

### 5. 执行流程

当你输入 `kimi chat` 时：

```
1. Shell 查找 PATH 中的 kimi
   ↓
2. 找到 /home/user/.local/bin/kimi
   ↓
3. 执行该脚本（是一个Python脚本）
   ↓
4. 脚本导入 kimi_cli.cli 模块
   ↓
5. 调用 kimi() 函数
   ↓
6. Click 解析参数 ['chat']
   ↓
7. 执行 chat 子命令
```

---

## 实战：让你的CLI像kimi一样使用

### 完整示例：创建一个可安装的CLI

**第1步：创建项目结构**

```bash
mkdir my-awesome-cli
cd my-awesome-cli

mkdir -p my_cli
touch my_cli/__init__.py
touch my_cli/cli.py
touch setup.py
```

项目结构：
```
my-awesome-cli/
├── setup.py
└── my_cli/
    ├── __init__.py
    └── cli.py
```

---

**第2步：编写CLI代码**

```python
# my_cli/cli.py
import click

@click.group()
@click.version_option(version='1.0.0')
def mycli():
    """My Awesome CLI Tool"""
    pass

@mycli.command()
@click.option('--name', default='World', help='你的名字')
def greet(name):
    """打招呼"""
    click.echo(f"Hello, {name}!")

@mycli.command()
@click.argument('numbers', nargs=-1, type=int)
def sum(numbers):
    """计算总和"""
    result = sum(numbers)
    click.echo(f"总和: {result}")

@mycli.group()
def config():
    """配置管理"""
    pass

@config.command()
def show():
    """显示配置"""
    click.echo("当前配置...")

if __name__ == '__main__':
    mycli()
```

---

**第3步：编写 setup.py**

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name='my-awesome-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
    ],
    entry_points={
        'console_scripts': [
            'mycli=my_cli.cli:mycli',  # ← 关键配置
            # 也可以有多个命令：
            # 'mygreet=my_cli.cli:greet',
        ],
    },
    author='Your Name',
    description='My awesome CLI tool',
    python_requires='>=3.8',
)
```

---

**第4步：安装**

```bash
# 开发模式安装（推荐，代码修改立即生效）
$ pip install -e .

# 或者正式安装
$ pip install .
```

安装成功后会显示：
```
Successfully installed my-awesome-cli-1.0.0
```

---

**第5步：使用**

现在可以像 `kimi` 一样使用了！

```bash
# 查看帮助
$ mycli --help
Usage: mycli [OPTIONS] COMMAND [ARGS]...

  My Awesome CLI Tool

Commands:
  config  配置管理
  greet   打招呼
  sum     计算总和

# 使用命令
$ mycli greet --name Alice
Hello, Alice!

$ mycli sum 1 2 3 4 5
总和: 15

$ mycli config show
当前配置...

# 查看版本
$ mycli --version
mycli, version 1.0.0
```

---

**第6步：卸载**

```bash
$ pip uninstall my-awesome-cli
```

---

## 两种方式的使用场景

### 方式1：`python script.py`

**适用场景**：
- ✅ 快速原型开发
- ✅ 学习练习
- ✅ 一次性脚本
- ✅ 不需要全局使用的工具

**示例**：
```python
# quick_script.py
import click

@click.command()
def test():
    click.echo("测试")

if __name__ == '__main__':
    test()
```

```bash
$ python quick_script.py
```

---

### 方式2：安装为命令

**适用场景**：
- ✅ 正式的CLI工具
- ✅ 需要频繁使用的命令
- ✅ 分发给其他用户
- ✅ 专业项目

**示例**：
```
# 安装后
$ mycli command
```

---

## 常见问题解答

### Q1: 为什么有时候 `pip install -e .` 后命令不可用？

**原因**：
- Python的 `bin` 目录不在 `PATH` 中
- 使用了虚拟环境但没有激活

**解决**：
```bash
# 检查命令是否安装
$ pip list | grep my-awesome-cli

# 查看命令位置
$ which mycli

# 如果找不到，检查PATH
$ echo $PATH

# 激活虚拟环境
$ source venv/bin/activate  # Linux/Mac
$ venv\Scripts\activate     # Windows
```

---

### Q2: 如何修改命令名？

修改 `setup.py` 中的 `entry_points`：

```python
entry_points={
    'console_scripts': [
        'new-name=my_cli.cli:mycli',  # ← 改这里
    ],
}
```

然后重新安装：
```bash
$ pip install -e . --force-reinstall
```

---

### Q3: 可以有多个命令入口吗？

**可以！**

```python
entry_points={
    'console_scripts': [
        'mycli=my_cli.cli:mycli',
        'greet=my_cli.cli:greet',  # ← 额外的命令
        'mysum=my_cli.cli:sum',    # ← 再来一个
    ],
}
```

安装后：
```bash
$ mycli --help
$ greet --name Alice
$ mysum 1 2 3
```

---

### Q4: 开发时每次改代码都要重新安装吗？

**不需要！** 使用 `-e` 参数（开发模式）：

```bash
$ pip install -e .
```

这样代码修改后**立即生效**，不需要重新安装。

---

## pyproject.toml vs setup.py

### 现代方式：pyproject.toml（推荐）

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-awesome-cli"
version = "1.0.0"
dependencies = [
    "click>=8.0",
]

[project.scripts]
mycli = "my_cli.cli:mycli"
```

### 传统方式：setup.py

```python
from setuptools import setup, find_packages

setup(
    name='my-awesome-cli',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['click>=8.0'],
    entry_points={
        'console_scripts': [
            'mycli=my_cli.cli:mycli',
        ],
    },
)
```

**两种方式效果一样**，推荐使用 `pyproject.toml`（更现代）。

---

## Kimi CLI 的完整安装流程

### 1. 克隆仓库

```bash
$ git clone https://github.com/xxx/kimi-cli.git
$ cd kimi-cli
```

### 2. 查看配置

```toml
# pyproject.toml
[project.scripts]
kimi = "kimi_cli.cli:kimi"
```

### 3. 安装

```bash
# 开发模式
$ pip install -e .

# 或从PyPI安装
$ pip install kimi-cli
```

### 4. 使用

```bash
$ kimi --version
$ kimi chat
$ kimi resume session_001
```

---

## 总结

### 核心要点

1. **直接运行脚本**：`python script.py`
   - 简单，适合开发测试
   - 需要 Python 前缀
   - 需要知道脚本路径

2. **安装为命令**：通过 `entry_points` 配置
   - 专业，用户友好
   - 不需要 Python 前缀
   - 全局可用

3. **关键配置**：`entry_points`
   ```python
   'command_name=package.module:function'
   ```

4. **命令名可以任意指定**，不一定要和函数名相同

### 实践建议

**开发阶段**：
```bash
# 使用开发模式安装
$ pip install -e .

# 直接使用命令
$ mycli --help
```

**测试阶段**：
```bash
# 也可以直接运行
$ python -m my_cli.cli --help
```

**发布阶段**：
```bash
# 打包发布
$ python -m build
$ pip install dist/my-awesome-cli-1.0.0.tar.gz
```

---

## 快速参考

### 从脚本到命令的步骤

1. **创建项目结构**
   ```
   my-cli/
   ├── setup.py
   └── my_cli/
       └── cli.py
   ```

2. **编写 CLI 代码**
   ```python
   # my_cli/cli.py
   @click.command()
   def mycli():
       pass
   ```

3. **配置 entry_points**
   ```python
   # setup.py
   entry_points={
       'console_scripts': [
           'mycli=my_cli.cli:mycli',
       ],
   }
   ```

4. **安装**
   ```bash
   $ pip install -e .
   ```

5. **使用**
   ```bash
   $ mycli
   ```

艹，看完这个，你应该完全明白为什么有时候要`python script.py`，有时候直接用命令名了！

**简单来说**：
- 没安装的脚本：`python script.py`
- 安装后的命令：`mycli`（通过 `entry_points` 配置）

**Kimi CLI 能直接用 `kimi` 命令，是因为它通过 `pip install` 安装了，并且在 `setup.py` 或 `pyproject.toml` 中配置了 `entry_points`！**
