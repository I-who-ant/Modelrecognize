# PromptToolkit 完全指南

> 艹，老王我把PromptToolkit框架给你讲明白！从基础到高级，从简单应用到Kimi CLI实战！

## 📚 目录

1. [核心概念](#核心概念)
2. [PromptSession API详解](#promptsession-api详解)
3. [补全系统](#补全系统)
4. [快捷键绑定](#快捷键绑定)
5. [样式与主题](#样式与主题)
6. [Kimi CLI实战](#kimi-cli实战)
7. [vs Click框架对比](#vs-click框架对比)

---

## 核心概念

### PromptToolkit 是什么？

PromptToolkit 是一个**强大的交互式命令行库**，提供：

- 🎯 **交互式输入**：PromptSession
- 📝 **自动补全**：Completer系统
- ⌨️ **快捷键**：KeyBindings
- 🎨 **样式**：Rich样式支持
- 📚 **历史记录**：History管理
- 🔍 **多行编辑**：Multiline支持

### Click vs PromptToolkit

| 特性 | Click | PromptToolkit |
|------|-------|---------------|
| 命令定义 | ✅ 装饰器简洁 | ❌ 手动实现 |
| 交互式输入 | ❌ 基础 | ✅ 强大 |
| 自动补全 | ❌ 不支持 | ✅ 完整 |
| 快捷键 | ❌ 不支持 | ✅ 丰富 |
| 多行编辑 | ❌ 不支持 | ✅ 支持 |
| 历史记录 | ❌ 不支持 | ✅ 内置 |
| 适用场景 | 命令行工具 | 交互式shell |

**总结**：
- **Click**：适合定义**命令式**CLI（像Git）
- **PromptToolkit**：适合构建**交互式**CLI（像Python REPL）

---

## PromptSession API详解

### 1. 基础用法

```python
from prompt_toolkit import PromptSession

# 创建会话
session = PromptSession()

# 获取输入
text = session.prompt('>>> ')
print(f"你输入了: {text}")
```

### 2. 完整参数详解

```python
session = PromptSession(
    # ========== 提示符相关 ==========
    message='>>> ',                    # 默认提示符（字符串）

    # ========== 补全相关 ==========
    completer=None,                    # Completer实例（自动补全）
    complete_while_typing=True,        # 输入时实时补全

    # ========== 验证相关 ==========
    validator=None,                    # Validator实例（输入验证）
    validate_while_typing=False,       # 输入时实时验证

    # ========== 历史相关 ==========
    history=None,                      # History实例（记录历史）
    enable_history_search=True,        # 启用历史搜索（Ctrl+R）

    # ========== 编辑相关 ==========
    multiline=False,                   # 支持多行输入
    editing_mode=EditingMode.EMACS,   # 编辑模式（Vi/Emacs）
    key_bindings=None,                 # KeyBindings实例（快捷键）

    # ========== 样式相关 ==========
    style=None,                        # Style实例（样式主题）
    lexer=None,                        # Lexer实例（语法高亮）

    # ========== 其他 ==========
    search_ignore_case=False,          # 历史搜索是否忽略大小写
    mouse_support=False,               # 是否支持鼠标
    complete_in_thread=True,           # 是否在线程中补全
)
```

### 3. 参数详细解析

#### **message（提示符）**

```python
# 字符串提示符
session = PromptSession(message='>>> ')

# HTML 格式的提示符
from prompt_toolkit.formatted_text import HTML

prompt = HTML('<b>kimi</b> <ansicyan>></ansicyan> ')
session = PromptSession(message=prompt)

# 自定义样式的提示符
from prompt_toolkit.formatted_text import ANSI

prompt = ANSI('\x1b[1mPython\x1b[0m >>> ')
session = PromptSession(message=prompt)
```

**输出效果**：
```
>>> 普通提示符
kimi > 带颜色的提示符
Python >>> ANSI格式提示符
```

---

#### **completer（补全）**

```python
# 1. 内置补全器
from prompt_toolkit.completion import WordCompleter

completer = WordCompleter(
    ['help', 'exit', 'list', 'add'],
    ignore_case=True  # 忽略大小写
)
session = PromptSession(completer=completer)

# 2. 路径补全
from prompt_toolkit.completion import PathCompleter

completer = PathCompleter()
session = PromptSession(completer=completer)

# 3. 自定义补全
from prompt_toolkit.completion import Completer, Completion

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        # 返回 Completion 对象
        yield Completion('hello', start_position=0)

session = PromptSession(completer=MyCompleter())
```

---

#### **validator（验证）**

```python
from prompt_toolkit.validation import Validator, ValidationError

# 1. 自定义验证器
class NumberValidator(Validator):
    def validate(self, document):
        text = document.text.strip()

        if not text.isdigit():
            raise ValidationError(
                message='请输入数字',
                cursor_position=len(text)
            )

session = PromptSession(validator=NumberValidator())

# 2. 验证时机
session = PromptSession(
    validator=MyValidator(),
    validate_while_typing=False,  # 仅在提交时验证
)

# 3. 验证失败时不提交
text = session.prompt('输入数字: ')  # 输入错误会显示错误但不返回
```

---

#### **history（历史记录）**

```python
from prompt_toolkit.history import FileHistory, InMemoryHistory

# 1. 文件历史（持久化）
session = PromptSession(
    history=FileHistory('.my_history')  # 保存到文件
)

# 2. 内存历史（临时）
session = PromptSession(
    history=InMemoryHistory()  # 仅在内存中保存
)

# 3. 启用历史搜索
session = PromptSession(
    history=FileHistory('.history'),
    enable_history_search=True  # Ctrl+R 搜索历史
)
```

**历史记录使用**：
```
按上/下箭头翻看历史
按 Ctrl+R 搜索历史
```

---

#### **multiline（多行模式）**

```python
# 1. 固定多行
session = PromptSession(multiline=True)
text = session.prompt('输入 (Ctrl+D 提交):\n')

# 2. 动态多行判断
def is_multiline(text):
    """检查括号是否匹配"""
    open_count = text.count('(') + text.count('[') + text.count('{')
    close_count = text.count(')') + text.count(']') + text.count('}')
    return open_count > close_count

session = PromptSession(multiline=is_multiline)

# 3. 多行提示符
session = PromptSession(
    multiline=True,
    prompt_continuation='... '  # 续行提示符
)
```

**输出**：
```
>>> print("hello"
...         "world")
```

---

#### **editing_mode（编辑模式）**

```python
from prompt_toolkit.enums import EditingMode

# Emacs 模式（默认）
session = PromptSession(editing_mode=EditingMode.EMACS)

# Vi 模式
session = PromptSession(editing_mode=EditingMode.VI)
```

**快捷键对比**：

| 操作 | Emacs | Vi |
|------|-------|-----|
| 光标开头 | Ctrl+A | ^ |
| 光标结尾 | Ctrl+E | $ |
| 删除到行尾 | Ctrl+K | D |
| 撤销 | Ctrl+/ | u |

---

#### **key_bindings（快捷键）**

```python
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

@bindings.add('c-x', 'c-e')  # Ctrl+X, Ctrl+E
def _(event):
    """自定义快捷键"""
    event.app.exit()

session = PromptSession(key_bindings=bindings)
```

---

#### **style（样式）**

```python
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'prompt': 'bold ansicyan',
    'validation': 'ansired',
    'input': 'ansigreen',
})

session = PromptSession(style=style)
```

---

### 4. 同步 vs 异步

```python
# 同步方式
text = session.prompt('>>> ')

# 异步方式
import asyncio

async def main():
    text = await session.prompt_async('>>> ') # 异步输入, 等待用户输入
    print(text)

asyncio.run(main())
```

---

## 补全系统

### 1. 内置补全器

```python
from prompt_toolkit.completion import (
    WordCompleter,        # 单词补全
    PathCompleter,        # 路径补全
    FuzzyCompleter,       # 模糊补全
    NestedCompleter,      # 嵌套补全
)

# WordCompleter
word_completer = WordCompleter(['hello', 'world']) # 单词补全

# PathCompleter
path_completer = PathCompleter() # 路径补全

# FuzzyCompleter（模糊匹配） 
fuzzy_completer = FuzzyCompleter(
    WordCompleter(['hello', 'world'])
)

# NestedCompleter（嵌套命令） 
completer = NestedCompleter({ 
    'user': {
        'create': None,
        'delete': None,
        'list': None,
    },
    'project': {
        'init': None,
        'build': None,
    }
})
```

---

### 2. 自定义补全器

```python
from prompt_toolkit.completion import Completer, Completion

class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        """
        返回补全建议

        参数:
            document: 输入的文档对象
            complete_event: 补全事件

        返回:
            Completion 对象的生成器
        """
        text = document.text_before_cursor

        # 示例：补全命令
        if text == 'hel':
            yield Completion('hello', start_position=-3) # 从光标前 3 个字符开始替换
            yield Completion('help', start_position=-3) #
```

---

### 3. Completion 对象详解

```python
Completion(
    text='hello',                    # 补全文本
    start_position=-5,               # 从光标前 5 个字符开始替换
    display='hello (function)',       # 显示的补全建议
    display_meta='Returns greeting',  # 显示的元信息
)
```

---

## 快捷键绑定

### 1. 基础快捷键

```python
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

# 单个快捷键
@bindings.add('c-t')  # Ctrl+T
def _(event):
    """插入时间戳"""
    import datetime
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    event.current_buffer.insert_text(timestamp)

# 多键组合
@bindings.add('c-x', 'c-e')  # Ctrl+X, Ctrl+E
def _(event):
    """退出"""
    event.app.exit()

session = PromptSession(key_bindings=bindings)
```

---

### 2. 快捷键修饰符

```python
@bindings.add('c-a')      # Ctrl+A
@bindings.add('m-a')      # Meta+A (Alt+A)
@bindings.add('s-a')      # Shift+A
@bindings.add('c-s-a')    # Ctrl+Shift+A
@bindings.add('escape', 'a')  # Escape, A
```

---

### 3. 事件对象API

```python
@bindings.add('c-t')
def _(event):
    # 获取当前缓冲区
    buffer = event.current_buffer

    # 插入文本
    buffer.insert_text('hello')

    # 获取光标位置
    cursor_position = buffer.cursor_position

    # 获取当前行
    current_line = buffer.document.current_line

    # 获取整个文本
    full_text = buffer.text

    # 删除
    buffer.delete(-1)  # 向前删除

    # 退出应用
    event.app.exit()
```

---

## 样式与主题

### 1. 基础样式

```python
from prompt_toolkit.styles import Style

style = Style.from_dict({
    # 命名空间 -> 样式
    'prompt': 'bold ansicyan',
    'input': 'ansigreen',
    'error': 'ansired',
})

session = PromptSession(style=style)
```

---

### 2. 颜色和属性

```python
# 颜色
'ansired', 'ansigreen', 'ansiyellow', 'ansiblue',
'ansimagenta', 'ansicyan', 'ansiwhite',

# 属性
'bold', 'underline', 'blink', 'italic', 'reverse',

# 组合
'bold ansicyan underline',

# 背景色
'bg:ansired ansiwhite',  # 红色背景，白色文字
```

---

### 3. 语法高亮

```python
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer

session = PromptSession(
    lexer=PygmentsLexer(PythonLexer) # 语法高亮
)
```

---

## Kimi CLI实战

### Kimi CLI 的PromptToolkit使用

```python
# src/kimi_cli/ui/shell/input.py

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.enums import EditingMode

class ShellInput:
    """Kimi CLI 的交互式输入"""

    def __init__(self, history_file: Path):
        self.session = PromptSession(
            # 历史记录
            history=FileHistory(str(history_file)),
            enable_history_search=True,

            # 补全
            completer=KimiCompleter(),
            complete_while_typing=True,

            # 编辑
            multiline=True,
            editing_mode=EditingMode.EMACS,

            # 快捷键
            key_bindings=self._create_key_bindings(),

            # 样式
            style=self._create_style(),
        )

    def _create_key_bindings(self) -> KeyBindings:
        """创建快捷键"""
        bindings = KeyBindings()

        @bindings.add('c-x', 'c-e')
        def _(event):
            """切换编辑模式"""
            if event.app.editing_mode == EditingMode.VI:
                event.app.editing_mode = EditingMode.EMACS
            else:
                event.app.editing_mode = EditingMode.VI

        return bindings

    def _create_style(self):
        """创建样式"""
        from prompt_toolkit.styles import Style

        return Style.from_dict({
            'prompt': 'bold ansicyan',
            'input': 'ansiwhite',
        })

    async def get_input(self) -> str:
        """获取用户输入"""
        return await self.session.prompt_async('kimi > ')
```

---

## vs Click框架对比

### 设计理念

**Click**：
```python
# 声明式：通过装饰器定义命令
@click.command()
@click.option('--name')
def greet(name):
    click.echo(f"Hello {name}!")
```

**PromptToolkit**：
```python
# 命令式：通过代码实现交互逻辑
session = PromptSession()
while True:
    text = session.prompt('>>> ')
    process(text)
```

---

### 使用场景对比

| 场景 | Click | PromptToolkit |
|------|-------|---------------|
| Git风格CLI | ✅ 完美 | ❌ 不适合 |
| Python REPL | ❌ 不适合 | ✅ 完美 |
| 交互式shell | ❌ 基础 | ✅ 强大 |
| 命令行工具 | ✅ 最佳 | ❌ 过度 |
| 快捷键支持 | ❌ 无 | ✅ 丰富 |
| 自动补全 | ❌ 无 | ✅ 强大 |

---

### 组合使用

**两者结合**：
```python
# Click 定义命令式入口
@click.command()
def kimi():
    """Kimi CLI"""
    pass

# PromptToolkit 实现交互式Shell
if __name__ == '__main__':
    # 如果带参数，使用 Click 处理
    # 如果没参数，启动 PromptToolkit Shell
    if len(sys.argv) > 1:
        kimi()
    else:
        shell = ShellApp()
        shell.run()
```

---

## 完整示例：文件管理器

```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from pathlib import Path

class FileManagerCompleter(Completer):
    """文件管理器补全"""

    def __init__(self, current_dir: Path):
        self.current_dir = current_dir
        self.commands = ['ls', 'cd', 'cat', 'mkdir', 'rm', 'exit']

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()

        if len(words) == 0 or not text.endswith(' '):
            # 补全命令
            for cmd in self.commands:
                if cmd.startswith(words[0] if words else ''):
                    yield Completion(cmd, start_position=-len(words[0] if words else ''))
        else:
            # 补全路径
            path_part = words[-1] if words else ''
            yield from self._complete_path(path_part)

    def _complete_path(self, prefix):
        """补全文件路径"""
        try:
            directory = Path(prefix).parent if '/' in prefix else self.current_dir

            for path in directory.iterdir():
                if path.name.startswith(Path(prefix).name):
                    yield Completion(
                        path.name,
                        start_position=-len(Path(prefix).name),
                        display=f"{path.name}/" if path.is_dir() else path.name
                    )
        except:
            pass

def main():
    """交互式文件管理器"""
    current_dir = Path.cwd()

    session = PromptSession(
        completer=FileManagerCompleter(current_dir),
        history=FileHistory('.fm_history'),
        complete_while_typing=True,
    )

    while True:
        try:
            prompt = f"{current_dir.name} > "
            text = session.prompt(prompt).strip()

            if not text:
                continue

            parts = text.split()
            cmd, args = parts[0], parts[1:] if len(parts) > 1 else []

            if cmd == 'exit':
                break
            elif cmd == 'ls':
                for item in current_dir.iterdir():
                    print(item.name)
            elif cmd == 'cd' and args:
                new_dir = (current_dir / args[0]).resolve()
                if new_dir.is_dir():
                    current_dir = new_dir

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    main()
```

---

## 学习要点总结

### 核心概念
- **PromptSession**：交互式输入的主要接口
- **Completer**：自动补全系统
- **Validator**：输入验证
- **KeyBindings**：快捷键绑定
- **History**：历史记录管理

### 关键特性
- 🎯 强大的自动补全
- ⌨️ 丰富的快捷键支持
- 📚 历史记录持久化
- 🎨 美观的样式系统
- 🔄 支持异步操作

### vs Click的区别
- Click：**命令式**（Git风格）
- PromptToolkit：**交互式**（REPL风格）

### 应用场景
- PromptToolkit：Python REPL、交互式Shell、文件管理器
- Click：命令行工具、CLI应用、参数解析

艹，看完这个，你应该对PromptToolkit有完整的理解了！从基础用法到Kimi CLI实战！