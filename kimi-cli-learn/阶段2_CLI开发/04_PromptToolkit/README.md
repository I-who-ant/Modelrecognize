# 模块04: Prompt Toolkit 交互式界面

**学习时长**: 4天

**学习目标**: 掌握 Prompt Toolkit，理解 Kimi CLI 的交互式 Shell 模式

---

## 📋 学习内容概览

1. **基础输入** (Day 20)
2. **自动补全** (Day 21)
3. **快捷键绑定** (Day 22)
4. **多行编辑与模式切换** (Day 23)

---

## 🎯 学习目标

- ✅ 掌握 PromptSession 基础使用
- ✅ 能实现自定义自动补全
- ✅ 能绑定自定义快捷键
- ✅ 理解 Vi/Emacs 编辑模式
- ✅ 理解 Kimi CLI 的 Ctrl-X 模式切换

---

## 📚 学习资源

### 官方文档
- [Prompt Toolkit 官方文档](https://python-prompt-toolkit.readthedocs.io/)
- [Prompt Toolkit GitHub](https://github.com/prompt-toolkit/python-prompt-toolkit)

### 推荐教程
- Prompt Toolkit 入门教程
- 构建交互式 CLI 应用

---

## 📖 详细学习内容

### 📝 01: 基础输入 (Day 20)

#### 学习内容

**PromptSession 基础**:

```python
from prompt_toolkit import PromptSession

# 创建会话
session = PromptSession()

# 获取用户输入
while True:
    try:
        text = session.prompt('>>> ')
        print(f'你输入了: {text}')
    except KeyboardInterrupt:
        continue
    except EOFError:
        break
```

**自定义提示符**: # 自定义提示符, 包含用户名和主机名
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

session = PromptSession()

# 使用 HTML 格式化提示符
prompt_text = HTML('<b>用户名</b>@<ansicyan>主机</ansicyan> $ ') # 自定义提示符, 包含用户名和主机名
text = session.prompt(prompt_text)
```

**输入验证**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator): # 验证输入是否为数字
    def validate(self, document):
        text = document.text 

        if not text.isdigit():
            raise ValidationError(
                message='请输入数字',
                cursor_position=len(text)
            )

session = PromptSession(validator=NumberValidator())
number = session.prompt('请输入数字: ')
```

**输入历史记录**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

# 使用文件保存历史
session = PromptSession(
    history=FileHistory('.my_history')
)

# 现在可以用上下箭头翻历史记录
while True:
    text = session.prompt('>>> ')
    print(text)
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/ui/shell/input.py
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

class ShellInput:
    def __init__(self, history_file: Path):
        self.session = PromptSession(
            history=FileHistory(str(history_file)), # 使用文件保存历史记录
            multiline=True,  # 支持多行输入
            enable_history_search=True,  # 启用历史搜索
        )

    async def get_input(self) -> str:
        """获取用户输入"""
        return await self.session.prompt_async('> ')
```

#### 实践练习

**练习14**: 交互式计算器
```python
# 文件: 代码实践/14_prompt_toolkit_basics.py

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.styles import Style

class ExpressionValidator(Validator):
    """验证数学表达式"""

    def validate(self, document):
        text = document.text.strip() # 移除首尾空格

        if not text:
            return

        # 简单验证：尝试求值
        try:
            eval(text, {"__builtins__": {}}, {}) # 
        except Exception as e:
            raise ValidationError(
                message=f'无效的表达式: {str(e)}',
                cursor_position=len(text)
            )

# 自定义样式
style = Style.from_dict({
    'prompt': 'ansicyan bold',
    'result': 'ansigreen',
    'error': 'ansired',
})

def main():
    """交互式计算器"""
    print("交互式计算器")
    print("输入数学表达式，按 Enter 计算")
    print("Ctrl-D 退出\n")

    session = PromptSession(
        validator=ExpressionValidator(),
        validate_while_typing=False,  # 仅在提交时验证
        history=InMemoryHistory(),
    )

    while True:
        try:
            # 自定义提示符
            prompt = HTML('<prompt>calc</prompt> >>> ') # 自定义提示符, 包含 calc 前缀
            text = session.prompt(prompt)

            if not text.strip():
                continue

            # 计算结果（安全的 eval）
            result = eval(text, {"__builtins__": {}}, {})
            print(f"  = {result}\n")

        except KeyboardInterrupt:
            continue
        except EOFError:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}\n")


if __name__ == '__main__':
    main()#


# 扩展练习:
# 1. 添加变量存储功能（如 x = 10）
# 2. 添加数学函数支持（sin, cos, sqrt 等）
# 3. 添加历史记录保存到文件
# 4. 添加更丰富的提示符（显示上次结果）
```

#### 检查点
- [ ] 理解 PromptSession 基础用法
_- [ ] 能自定义提示符样式
- [ ] 能实现输入验证
- [ ] 能使用历史记录功能_

---

### 📝 02: 自动补全 (Day 21)

#### 学习内容

**WordCompleter 单词补全**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# 定义补全词汇
completer = WordCompleter(
    ['add', 'delete', 'list', 'update', 'help', 'exit'],
    ignore_case=True  # 忽略大小写
)

session = PromptSession(completer=completer)

while True:
    text = session.prompt('>>> ')
    print(text)
```

**自定义 Completer**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

class PathCompleter(Completer):
    """文件路径补全器"""

    def get_completions(self, document, complete_event):
        from pathlib import Path

        text = document.text_before_cursor.strip() # 移除首尾空格

        # 获取当前目录
        if '/' in text:
            directory = Path(text).parent # 获取目录部分
            prefix = Path(text).name # 获取文件名部分
        else:
            directory = Path.cwd() # 当前目录
            prefix = text # 完整路径作为前缀

        # 列出目录内容
        try:
            for path in directory.iterdir():
                if path.name.startswith(prefix):
                    yield Completion(
                        path.name,
                        start_position=-len(prefix),
                        display=f"{path.name}/" if path.is_dir() else path.name
                    )
        except (PermissionError, FileNotFoundError):
            pass

session = PromptSession(completer=PathCompleter())
text = session.prompt('输入路径: ')
```

**动态补全**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

class CommandCompleter(Completer):
    """命令补全器（根据上下文动态补全）"""

    def __init__(self):
        self.commands = { # 定义命令补全词汇
            'user': ['create', 'delete', 'list', 'update'],
            'project': ['init', 'build', 'deploy', 'test'],
            'config': ['get', 'set', 'list', 'delete'],
        }

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()

        if len(words) == 0:
            # 补全一级命令
            for cmd in self.commands.keys():
                yield Completion(cmd, start_position=0)

        elif len(words) == 1:
            # 补全一级命令
            for cmd in self.commands.keys():
                if cmd.startswith(words[0]):
                    yield Completion(
                        cmd,
                        start_position=-len(words[0])
                    )

        elif len(words) == 2:
            # 补全二级命令
            first_cmd = words[0]
            if first_cmd in self.commands:
                for sub_cmd in self.commands[first_cmd]:
                    if sub_cmd.startswith(words[1]):
                        yield Completion(
                            sub_cmd,
                            start_position=-len(words[1])
                        )

session = PromptSession(completer=CommandCompleter())

while True:
    try:
        text = session.prompt('>>> ')
        print(f"执行: {text}")
    except (KeyboardInterrupt, EOFError):
        break
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/ui/shell/completer.py
from prompt_toolkit.completion import Completer, Completion

class ShellCompleter(Completer):
    """Shell 模式的自动补全器"""

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # 文件路径补全
        if '/' in text or text.startswith('.'):
            yield from self._file_path_completions(text)

        # 命令补全
        else:
            yield from self._command_completions(text)

    def _file_path_completions(self, text: str):
        """文件路径补全"""
        # 实现逻辑...
        pass

    def _command_completions(self, text: str):
        """命令补全"""
        # 实现逻辑...
        pass
```

#### 实践练习

**练习15**: 文件管理器自动补全
```python
# 文件: 代码实践/15_auto_completion.py

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from pathlib import Path

class FileManagerCompleter(Completer):
    """文件管理器补全器

    支持:
    - 命令补全（ls, cd, cat, mkdir, rm）
    - 文件路径补全
    - 命令参数补全
    """

    def __init__(self):
        self.commands = {
            'ls': 'List directory contents',
            'cd': 'Change directory',
            'cat': 'Display file contents',
            'mkdir': 'Create directory',
            'rm': 'Remove file or directory',
            'pwd': 'Print working directory',
            'help': 'Show help',
            'exit': 'Exit the file manager',
        }

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()

        if len(words) == 0 or (len(words) == 1 and not text.endswith(' ')):
            # 补全命令
            yield from self._complete_commands(words[0] if words else '')

        else:
            # 补全路径
            path_text = words[-1] if words else ''
            yield from self._complete_paths(path_text)

    def _complete_commands(self, prefix: str):
        """补全命令"""
        for cmd, desc in self.commands.items():
            if cmd.startswith(prefix):
                yield Completion(
                    cmd,
                    start_position=-len(prefix),
                    display=f"{cmd}",
                    display_meta=desc  # 显示描述
                )

    def _complete_paths(self, prefix: str):
        """补全文件路径"""
        try:
            # 解析路径
            if '/' in prefix:
                directory = Path(prefix).parent
                file_prefix = Path(prefix).name
            else:
                directory = Path.cwd()
                file_prefix = prefix

            # 列出目录内容
            if not directory.exists():
                return

            for path in sorted(directory.iterdir()):
                if path.name.startswith(file_prefix):
                    # 目录加 /
                    display = f"{path.name}/" if path.is_dir() else path.name

                    yield Completion(
                        path.name,
                        start_position=-len(file_prefix),
                        display=display,
                        display_meta="DIR" if path.is_dir() else "FILE"
                    )

        except (PermissionError, FileNotFoundError):
            pass


def main():
    """交互式文件管理器"""
    print("交互式文件管理器")
    print("支持命令: ls, cd, cat, mkdir, rm, pwd, help, exit")
    print("使用 Tab 进行自动补全\n")

    session = PromptSession(
        completer=FileManagerCompleter(),
        complete_while_typing=True,  # 输入时自动补全
    )

    current_dir = Path.cwd()

    while True:
        try:
            # 提示符显示当前目录
            prompt = f"{current_dir.name}> "
            text = session.prompt(prompt).strip()

            if not text:
                continue

            # 解析命令
            parts = text.split()
            cmd = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            # 执行命令
            if cmd == 'exit':
                print("再见！")
                break

            elif cmd == 'pwd':
                print(current_dir)

            elif cmd == 'ls':
                path = Path(args[0]) if args else current_dir
                for item in sorted(path.iterdir()):
                    print(item.name)

            elif cmd == 'cd':
                if not args:
                    print("用法: cd <directory>")
                else:
                    new_dir = (current_dir / args[0]).resolve()
                    if new_dir.is_dir():
                        current_dir = new_dir
                    else:
                        print(f"错误: {args[0]} 不是目录")

            elif cmd == 'cat':
                if not args:
                    print("用法: cat <file>")
                else:
                    file_path = current_dir / args[0]
                    if file_path.is_file():
                        print(file_path.read_text())
                    else:
                        print(f"错误: {args[0]} 不是文件")

            elif cmd == 'mkdir':
                if not args:
                    print("用法: mkdir <directory>")
                else:
                    (current_dir / args[0]).mkdir(exist_ok=True)
                    print(f"创建目录: {args[0]}")

            elif cmd == 'help':
                print("\n可用命令:")
                for cmd, desc in FileManagerCompleter().commands.items():
                    print(f"  {cmd:10} - {desc}")
                print()

            else:
                print(f"未知命令: {cmd}")

        except KeyboardInterrupt:
            continue
        except EOFError:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == '__main__':
    main()


# 扩展练习:
# 1. 添加命令历史记录
# 2. 添加 --help 参数补全
# 3. 添加更多命令（cp, mv, find）
# 4. 添加通配符支持（*.txt）
```

#### 检查点
- [ ] 理解 Completer 接口
- [ ] 能实现自定义补全器
- [ ] 理解动态补全逻辑
- [ ] 能处理上下文相关的补全

---

### 📝 03: 快捷键绑定 (Day 22)

#### 学习内容

**KeyBindings 基础**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings # 从 prompt_toolkit.key_binding 导入 KeyBindings 类

bindings = KeyBindings()

@bindings.add('c-t')  # Ctrl+T
def _(event):
    """Ctrl+T: 插入时间戳"""
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    event.current_buffer.insert_text(timestamp)

@bindings.add('c-q')  # Ctrl+Q
def _(event):
    """Ctrl+Q: 退出"""
    event.app.exit()

session = PromptSession(key_bindings=bindings)
text = session.prompt('>>> ')
```

**编辑模式**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.enums import EditingMode

# Vi 模式
session_vi = PromptSession(editing_mode=EditingMode.VI)

# Emacs 模式（默认）
session_emacs = PromptSession(editing_mode=EditingMode.EMACS)
```

**模式切换**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.enums import EditingMode

bindings = KeyBindings()

@bindings.add('c-x', 'c-e')  # Ctrl+X, Ctrl+E
def _(event):
    """切换 Vi/Emacs 模式"""
    if event.app.editing_mode == EditingMode.VI:
        event.app.editing_mode = EditingMode.EMACS
        print("切换到 Emacs 模式")
    else:
        event.app.editing_mode = EditingMode.VI
        print("切换到 Vi 模式")

session = PromptSession(key_bindings=bindings)
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/ui/shell/input.py
from prompt_toolkit.key_binding import KeyBindings

def create_key_bindings() -> KeyBindings:
    """创建快捷键绑定"""
    bindings = KeyBindings()

    @bindings.add('c-x', 'c-m')  # Ctrl+X, Ctrl+M
    def _(event):
        """切换多行模式"""
        # 切换逻辑...
        pass

    @bindings.add('c-x', 'c-e')  # Ctrl+X, Ctrl+E
    def _(event):
        """切换编辑模式（Vi/Emacs）"""
        # 切换逻辑...
        pass

    return bindings
```

#### 实践练习

**练习16**: 文本编辑器快捷键
```python
# 文件: 代码实践/16_key_bindings.py

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.formatted_text import HTML
import datetime

class Editor:
    """简单的文本编辑器"""

    def __init__(self):
        self.content_lines = []
        self.current_mode = EditingMode.EMACS
        self.bindings = self._create_key_bindings()

    def _create_key_bindings(self) -> KeyBindings:
        """创建快捷键绑定"""
        bindings = KeyBindings()

        @bindings.add('c-t')  # Ctrl+T
        def _(event):
            """插入当前时间"""
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            event.current_buffer.insert_text(timestamp)

        @bindings.add('c-x', 'c-e')  # Ctrl+X, Ctrl+E
        def _(event):
            """切换编辑模式"""
            if self.current_mode == EditingMode.VI:
                self.current_mode = EditingMode.EMACS
                event.app.editing_mode = EditingMode.EMACS
                print("\n[切换到 Emacs 模式]")
            else:
                self.current_mode = EditingMode.VI
                event.app.editing_mode = EditingMode.VI
                print("\n[切换到 Vi 模式]")

        @bindings.add('c-x', 'c-s')  # Ctrl+X, Ctrl+S
        def _(event):
            """保存当前行"""
            text = event.current_buffer.text
            if text.strip():
                self.content_lines.append(text)
                print(f"\n[已保存: {text}]")
                event.current_buffer.text = ''

        @bindings.add('c-x', 'c-p')  # Ctrl+X, Ctrl+P
        def _(event):
            """打印所有内容"""
            print("\n========== 内容 ==========")
            for i, line in enumerate(self.content_lines, 1):
                print(f"{i}: {line}")
            print("==========================")

        @bindings.add('c-x', 'c-c')  # Ctrl+X, Ctrl+C
        def _(event):
            """清空内容"""
            self.content_lines.clear()
            print("\n[已清空所有内容]")

        return bindings

    def run(self):
        """运行编辑器"""
        print("简单文本编辑器")
        print("快捷键:")
        print("  Ctrl+T        - 插入时间戳")
        print("  Ctrl+X Ctrl+E - 切换 Vi/Emacs 模式")
        print("  Ctrl+X Ctrl+S - 保存当前行")
        print("  Ctrl+X Ctrl+P - 打印所有内容")
        print("  Ctrl+X Ctrl+C - 清空所有内容")
        print("  Ctrl+D        - 退出\n")

        session = PromptSession(
            key_bindings=self.bindings,
            editing_mode=self.current_mode,
            multiline=False,
        )

        while True:
            try:
                # 显示提示符
                mode_text = "Vi" if self.current_mode == EditingMode.VI else "Emacs"
                prompt = HTML(f'<b>[{mode_text}]</b> > ')

                text = session.prompt(prompt)

                if text.strip():
                    self.content_lines.append(text)
                    print(f"[已添加行 {len(self.content_lines)}]")

            except KeyboardInterrupt:
                continue
            except EOFError:
                print("\n退出编辑器")
                break


if __name__ == '__main__':
    editor = Editor()
    editor.run()


# 扩展练习:
# 1. 添加撤销/重做功能（Ctrl+Z/Ctrl+Y）
# 2. 添加搜索功能（Ctrl+F）
# 3. 添加行号跳转（Ctrl+G）
# 4. 添加保存到文件功能
```

#### 检查点
- [ ] 理解 KeyBindings 机制
- [ ] 能绑定自定义快捷键
- [ ] 理解 Vi/Emacs 编辑模式
- [ ] 能实现模式切换

---

### 📝 04: 多行编辑与模式切换 (Day 23)

#### 学习内容

**多行输入**:
```python
from prompt_toolkit import PromptSession

# 启用多行模式
session = PromptSession(multiline=True)

text = session.prompt('输入 SQL (Ctrl+D 提交):\n')
print(f"你输入了:\n{text}")
```

**条件多行**:
```python
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer

def is_multiline(text):
    """判断是否需要继续输入（检查括号是否匹配）"""
    open_brackets = text.count('(') + text.count('[') + text.count('{')
    close_brackets = text.count(')') + text.count(']') + text.count('}')
    return open_brackets > close_brackets

session = PromptSession(
    multiline=is_multiline,  # 动态判断
    lexer=PygmentsLexer(PythonLexer),  # 语法高亮
)

text = session.prompt('>>> ')
```

**Kimi CLI 的多行与模式切换**:
```python
# src/kimi_cli/ui/shell/input.py
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

class MultiModeInput:
    """支持多模式的输入系统"""

    def __init__(self):
        self.multiline = False  # 多行模式状态
        self.bindings = self._create_key_bindings()

    def _create_key_bindings(self) -> KeyBindings:
        bindings = KeyBindings()

        @bindings.add('c-x', 'c-m')  # Ctrl+X, Ctrl+M
        def _(event):
            """切换多行模式"""
            self.multiline = not self.multiline
            mode = "多行" if self.multiline else "单行"
            print(f"\n[切换到 {mode} 模式]")

        return bindings

    async def get_input(self) -> str:
        """获取用户输入"""
        session = PromptSession(
            multiline=self.multiline,
            key_bindings=self.bindings,
        )

        return await session.prompt_async('> ')
```

#### 实践练习

**练习17**: Kimi CLI Shell 模式分析
```markdown
# 文件: 代码实践/17_kimi_shell_analysis.md

# Kimi CLI Shell 模式分析

## 1. 核心组件

### 输入系统 (src/kimi_cli/ui/shell/input.py)
- `ShellInput` 类：管理用户输入
- 支持多行编辑
- 历史记录持久化
- 自动补全集成

### 显示系统 (src/kimi_cli/ui/shell/display.py)
- 使用 Rich 渲染 Markdown
- 流式显示 LLM 响应
- 工具调用可视化

### 主应用 (src/kimi_cli/ui/shell/app.py)
- `ShellApp` 类：Shell 模式主循环
- 输入-处理-输出循环
- 异常处理和重试

## 2. 快捷键设计

### Kimi CLI 的快捷键
- `Ctrl+X Ctrl+M`: 切换多行/单行模式
- `Ctrl+X Ctrl+E`: 切换 Vi/Emacs 编辑模式
- `Ctrl+C`: 中断当前操作
- `Ctrl+D`: 退出 Shell
- 上/下箭头: 浏览历史记录
- `Tab`: 自动补全

## 3. 多行模式实现

### 触发条件
- 用户按 `Ctrl+X Ctrl+M` 手动切换
- 或根据输入内容自动判断

### 提交方式
- 单行模式: `Enter` 提交
- 多行模式: `Meta+Enter` 或 `Esc Enter` 提交

### 代码示例
```python
from prompt_toolkit import PromptSession

session = PromptSession(
    multiline=True,
    prompt_continuation='... ',  # 续行提示符
)

text = session.prompt('>>> ')
```

## 4. 自动补全实现

### 补全策略
1. 文件路径补全
2. 命令补全
3. 历史记录补全

### 代码示例
```python
from prompt_toolkit.completion import Completer, Completion

class ShellCompleter(Completer):
    def get_completions(self, document, complete_event):
        # 根据上下文返回补全建议
        pass
```

## 5. 样式与主题

### 提示符样式
```python
from prompt_toolkit.formatted_text import HTML

prompt = HTML('<b>kimi</b> <ansicyan>></ansicyan> ')
```

### 语法高亮
```python
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.markdown import MarkdownLexer

session = PromptSession(
    lexer=PygmentsLexer(MarkdownLexer)
)
```

## 6. 学习要点

- [ ] 理解 Prompt Toolkit 的事件循环
- [ ] 掌握快捷键绑定机制
- [ ] 理解多行输入的实现
- [ ] 掌握自动补全的设计模式
- [ ] 理解样式和主题系统

## 7. 练习任务

- [ ] 阅读 Kimi CLI Shell 模式源码
- [ ] 实现一个简化版的 Shell
- [ ] 添加自定义快捷键
- [ ] 实现文件路径补全
```

#### 检查点
- [ ] 理解多行输入机制
- [ ] 理解 Kimi CLI 的模式切换
- [ ] 能实现条件多行
- [ ] 能分析 Kimi CLI Shell 实现

---

## 📊 模块总结

### 知识点检查
- [ ] PromptSession 基础
- [ ] 自动补全系统
- [ ] 快捷键绑定
- [ ] 多行编辑

### 代码练习
- [ ] 练习14: 交互式计算器
- [ ] 练习15: 文件管理器补全
- [ ] 练习16: 文本编辑器快捷键
- [ ] 练习17: Kimi CLI Shell 分析

### 输出成果
- [ ] 4个练习代码
- [ ] Kimi CLI Shell 分析文档
- [ ] 学习笔记

---

## 🔄 下一步

完成本模块后，进入 **模块05: Rich 显示**。

---

*Created by 老王 | Last Updated: 2025-01-10*
