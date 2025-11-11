# PromptToolkit 在 Kimi CLI 中的应用分析

> 艹，老王把 Kimi CLI 中 PromptToolkit 的真实应用全部掰开了讲！从架构到代码，让你彻底理解这个框架的实战用法！

---

## 📚 目录

1. [项目背景](#项目背景)
2. [整体架构](#整体架构)
3. [核心类：CustomPromptSession](#核心类custompromptsession)
4. [补全系统](#补全系统)
5. [快捷键绑定](#快捷键绑定)
6. [状态管理与显示](#状态管理与显示)
7. [完整应用流程](#完整应用流程)
8. [对比分析：Click vs PromptToolkit](#对比分析click-vs-prompttoolkit)

---

## 项目背景

### Kimi CLI 是什么？

**Kimi CLI** 是一个交互式命令行 AI 助手，核心特点：
- 🤖 **AI Agent**：调用 Kimi API，使用 ReAct 思维链
- 💬 **交互式 Shell**：多轮对话，实时补全
- 🔧 **工具系统**：能执行文件操作、命令行等
- 🧠 **思维模式**：支持深度思考（thinking mode）

### 为什么选择 PromptToolkit？

| 需求 | Click | PromptToolkit | 选择 |
|------|-------|---------------|------|
| 定义单次命令 | ✅ | ❌ | Click |
| **交互式会话** | ❌ | ✅ | **PromptToolkit** |
| **实时补全** | ❌ | ✅ | **PromptToolkit** |
| **快捷键** | ❌ | ✅ | **PromptToolkit** |
| **历史记录** | ❌ | ✅ | **PromptToolkit** |
| **多行输入** | ❌ | ✅ | **PromptToolkit** |

**结论**：Kimi CLI 是一个交互式 shell，而不是命令行工具，所以必须用 PromptToolkit！

---

## 整体架构

### 文件结构

```
src/kimi_cli/ui/shell/
├── prompt.py          # ✅ CustomPromptSession（核心类）
├── setup.py           # Setup 交互式配置
├── metacmd.py         # 元命令定义
└── console.py         # Rich 输出
```

### 核心流程

```
kimi start (CLI 入口)
    ↓
ShellApp 初始化
    ↓
CustomPromptSession 创建 (PromptToolkit)
    ↓
while True:
    获取用户输入 (含补全、历史、快捷键)
    ↓
    解析模式（Agent/Shell）和思维模式
    ↓
    发送给 Soul（LLM 代理执行）
    ↓
    显示结果
```

### 架构图

```
┌─────────────────────────────────────────────────────────┐
│         CustomPromptSession (PromptToolkit)              │
│                                                          │
│  +──────────────────────────────────────────────────+  │
│  │ PromptSession                                    │  │
│  │  • message: 动态提示符                            │  │
│  │  • completer: MetaCommand + FileMention          │  │
│  │  • key_bindings: 自定义快捷键                    │  │
│  │  • history: 历史记录                            │  │
│  │  • bottom_toolbar: 状态栏                       │  │
│  +──────────────────────────────────────────────────+  │
│                           ↓                             │
│  +──────────────────────────────────────────────────+  │
│  │ 功能层                                          │  │
│  │  • Mode 切换 (Agent ↔ Shell)                    │  │
│  │  • Thinking 模式                               │  │
│  │  • 图片粘贴                                     │  │
│  │  • Toast 通知                                  │  │
│  +──────────────────────────────────────────────────+  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 核心类：CustomPromptSession

### 整体设计

```python
class CustomPromptSession:
    def __init__(
        self,
        *,
        status_provider: Callable[[], StatusSnapshot],
        model_capabilities: set[ModelCapability],
        initial_thinking: bool,
    ) -> None:
        # 初始化历史记录
        # 初始化补全器
        # 初始化快捷键
        # 创建 PromptSession
```

### 关键属性

| 属性 | 用途 | 类型 |
|------|------|------|
| `_mode` | 当前模式（Agent/Shell） | `PromptMode` |
| `_thinking` | 是否启用思维模式 | `bool` |
| `_session` | 真正的 PromptSession | `PromptSession` |
| `_attachment_parts` | 粘贴的图片存储 | `dict` |

### 初始化过程详解

#### 1️⃣ 历史记录初始化

```python
# 每个工作目录都有独立的历史记录
history_dir = get_share_dir() / "user-history"
work_dir_id = md5(str(Path.cwd()).encode(encoding="utf-8")).hexdigest()
self._history_file = (history_dir / work_dir_id).with_suffix(".jsonl")

# 加载历史
history_entries = _load_history_entries(self._history_file)
history = InMemoryHistory()
for entry in history_entries:
    history.append_string(entry.content)
```

**为什么这样设计？**
- 不同项目目录有不同历史
- 使用 MD5 避免长路径问题
- 格式用 JSONL，易于扩展

#### 2️⃣ 补全器初始化

```python
# 合并两个补全器
self._agent_mode_completer = merge_completers(
    [
        MetaCommandCompleter(),      # 完成 /xxx 命令
        FileMentionCompleter(Path.cwd()),  # 完成 @xxxx 文件
    ],
    deduplicate=True,
)
```

#### 3️⃣ 快捷键初始化

```python
_kb = KeyBindings()

# Ctrl+X: 切换模式
@_kb.add("c-x", eager=True)
def _switch_mode(event: KeyPressEvent) -> None:
    self._mode = self._mode.toggle()
    self._apply_mode(event)
    event.app.invalidate()

# Alt+Enter / Ctrl+J: 换行
@_kb.add("escape", "enter", eager=True)
@_kb.add("c-j", eager=True)
def _insert_newline(event: KeyPressEvent) -> None:
    event.current_buffer.insert_text("\n")

# Tab: 切换思维模式
@_kb.add("tab", filter=~has_completions & is_agent_mode, eager=True)
def _switch_thinking(event: KeyPressEvent) -> None:
    self._thinking = not self._thinking
    _toast_thinking(self._thinking)
```

#### 4️⃣ PromptSession 创建

```python
self._session = PromptSession(
    message=self._render_message,           # 动态提示符
    completer=self._agent_mode_completer,   # 补全
    complete_while_typing=True,             # 实时补全
    key_bindings=_kb,                       # 快捷键
    clipboard=clipboard,                    # 剪贴板
    history=history,                        # 历史
    bottom_toolbar=self._render_bottom_toolbar,  # 底部栏
)
```

---

## 补全系统

### 两个自定义 Completer

#### 1️⃣ MetaCommandCompleter

**作用**：完成 `/xxx` 元命令

```python
class MetaCommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        # 只有当光标在 "/" 后面时才补全
        text = document.text_before_cursor
        last_space = text.rfind(" ")
        token = text[last_space + 1 :]

        if not token.startswith("/"):
            return

        typed = token[1:]

        # 返回所有匹配的命令
        for cmd in get_meta_commands():
            names = [cmd.name] + list(cmd.aliases)
            if any(n.lower().startswith(typed.lower()) for n in names):
                yield Completion(
                    text=f"/{cmd.name}",
                    start_position=-len(token),
                    display=cmd.slash_name(),
                    display_meta=cmd.description,
                )
```

**例子**：
```
>>> /he<TAB>
/help (list all commands)
/hex (convert to hex)
```

#### 2️⃣ FileMentionCompleter

**作用**：完成 `@xxxx` 文件路径

**核心特性**：
- 索引工作目录所有文件
- 忽略 `.git`、`node_modules` 等垃圾目录
- 定期更新缓存（2秒）
- 限制结果数量（1000）
- 支持模糊搜索

```python
class FileMentionCompleter(Completer):
    def __init__(
        self,
        root: Path,
        *,
        refresh_interval: float = 2.0,
        limit: int = 1000,
    ) -> None:
        self._root = root
        self._refresh_interval = refresh_interval
        self._limit = limit

        # 用 WordCompleter + FuzzyCompleter 实现模糊搜索
        self._word_completer = WordCompleter(
            self._get_paths,
            WORD=False,
            pattern=self._FRAGMENT_PATTERN,
        )
        self._fuzzy = FuzzyCompleter(
            self._word_completer,
            WORD=False,
        )
```

**被忽略的目录**（很多！）：
```
.git, .vscode, node_modules, __pycache__, .venv,
.pytest_cache, .mypy_cache, .ruff_cache, build,
dist, target, venv, .dart_tool, ...
```

**例子**：
```
>>> @src<TAB>
src/main.py
src/utils.py
src/config.py

>>> @kimi_cli<TAB>
kimi_cli/cli.py
kimi_cli/soul.py
kimi_cli/llm.py
```

### 合并补全器

```python
self._agent_mode_completer = merge_completers(
    [
        MetaCommandCompleter(),
        FileMentionCompleter(Path.cwd()),
    ],
    deduplicate=True,
)
```

**关键点**：
- `deduplicate=True` 避免重复结果
- 同时支持 `/xxx` 和 `@xxx` 补全

---

## 快捷键绑定

### 所有快捷键

| 快捷键 | 功能 | 条件 |
|--------|------|------|
| **Ctrl+X** | 切换 Agent/Shell 模式 | 总是可用 |
| **Tab** | 切换思维模式 | Agent 模式 + 没有补全菜单 |
| **Ctrl+J** / **Alt+Enter** | 插入换行 | 总是可用 |
| **Ctrl+V** | 粘贴（文本/图片） | 剪贴板可用 |
| **Enter** | 接受第一个补全 | 有补全菜单 |

### 实现细节

#### 模式切换（Ctrl+X）

```python
@_kb.add("c-x", eager=True)
def _switch_mode(event: KeyPressEvent) -> None:
    # 切换模式
    self._mode = self._mode.toggle()

    # 根据新模式调整补全设置
    self._apply_mode(event)

    # 重绘界面
    event.app.invalidate()

def _apply_mode(self, event: KeyPressEvent | None = None) -> None:
    buff = event.current_buffer if event else self._session.default_buffer

    if self._mode == PromptMode.SHELL:
        # Shell 模式：禁用补全
        buff.completer = DummyCompleter()
        buff.complete_while_typing = Never()
    else:
        # Agent 模式：启用补全
        buff.completer = self._agent_mode_completer
        buff.complete_while_typing = Always()
```

**为什么要切换补全？**
- Agent 模式：使用 AI 执行命令，需要补全 `/xxx` 和 `@xxx`
- Shell 模式：执行系统命令，补全会干扰（系统命令有自己的补全）

#### 思维模式（Tab）

```python
@_kb.add("tab", filter=~has_completions & is_agent_mode, eager=True)
def _switch_thinking(event: KeyPressEvent) -> None:
    # 检查模型是否支持
    if "thinking" not in self._model_capabilities:
        console.print("[yellow]该模型不支持思维模式[/yellow]")
        return

    # 切换
    self._thinking = not self._thinking

    # 显示 Toast 提示
    _toast_thinking(self._thinking)

    # 重绘（提示符会改变）
    event.app.invalidate()
```

**关键过滤器**：
- `~has_completions`：只有当没有补全菜单时才工作
- `is_agent_mode`：只有在 Agent 模式时才工作

#### 粘贴图片（Ctrl+V）

```python
@_kb.add("c-v", eager=True)
def _paste(event: KeyPressEvent) -> None:
    # 先尝试粘贴图片
    if self._try_paste_image(event):
        return

    # 否则粘贴文本
    clipboard_data = event.app.clipboard.get_data()
    event.current_buffer.paste_clipboard_data(clipboard_data)
```

---

## 状态管理与显示

### 三个关键状态

#### 1️⃣ 动态提示符

```python
def _render_message(self) -> FormattedText:
    # 根据模式选择符号
    symbol = PROMPT_SYMBOL if self._mode == PromptMode.AGENT else PROMPT_SYMBOL_SHELL

    # 思维模式时改变符号
    if self._mode == PromptMode.AGENT and self._thinking:
        symbol = PROMPT_SYMBOL_THINKING

    # 显示用户名 + 符号
    return FormattedText([("bold", f"{getpass.getuser()}{symbol} ")])
```

**三种提示符**：
- `✨` (PROMPT_SYMBOL)：Agent 模式正常
- `💫` (PROMPT_SYMBOL_THINKING)：Agent 模式 + 思维
- `$` (PROMPT_SYMBOL_SHELL)：Shell 模式

#### 2️⃣ 底部工具栏

```python
def _render_bottom_toolbar(self) -> FormattedText:
    # 获取可用列数
    app = get_app_or_none()
    columns = app.output.get_size().columns

    fragments: list[tuple[str, str]] = []

    # 1. 时间
    now_text = datetime.now().strftime("%H:%M")
    fragments.append(("", now_text))
    columns -= len(now_text)

    # 2. 模式
    mode = str(self._mode).lower()  # "agent" 或 "shell"
    if self._mode == PromptMode.AGENT and self._thinking:
        mode += " (thinking)"
    fragments.append(("", f"{mode}"))
    columns -= len(mode)

    # 3. Toast 提示（如果有）
    current_toast = _current_toast()
    if current_toast is not None:
        fragments.append(("", current_toast.message))
        columns -= len(current_toast.message)
        current_toast.duration -= _REFRESH_INTERVAL
        if current_toast.duration <= 0.0:
            _toast_queue.popleft()
    else:
        # 4. 快捷键提示
        shortcuts = [
            *self._shortcut_hints,
            "ctrl-d: exit",
        ]
        for shortcut in shortcuts:
            if columns > len(shortcut) + 2:
                fragments.append(("", shortcut))
                columns -= len(shortcut) + 2

    # 5. 上下文使用率
    status = self._status_provider()
    status_text = self._format_status(status)
    fragments.append(("", status_text))

    return FormattedText(fragments)
```

**底部栏显示内容**（从左到右）：
```
14:23  agent (thinking)  ctrl-x: switch mode | ctrl-j: newline   context: 45.2%
```

#### 3️⃣ Toast 通知系统

```python
_toast_queue = deque[_ToastEntry]()

def toast(
    message: str,
    duration: float = 5.0,
    topic: str | None = None,
    immediate: bool = False,
) -> None:
    """显示临时通知"""
    entry = _ToastEntry(topic=topic, message=message, duration=duration)

    if topic is not None:
        # 同一 topic 只能有一个 toast
        for existing in list(_toast_queue):
            if existing.topic == topic:
                _toast_queue.remove(existing)

    if immediate:
        _toast_queue.appendleft(entry)  # 立即显示
    else:
        _toast_queue.append(entry)  # 排队
```

**例子**：
```
toast("thinking on, tab to toggle", topic="thinking", immediate=True)
# 显示 3 秒后自动消失
```

### 后台刷新任务

```python
def __enter__(self) -> "CustomPromptSession":
    # 创建后台刷新任务
    async def _refresh(interval: float) -> None:
        while True:
            app = get_app_or_none()
            if app is not None:
                # 重绘UI（更新工具栏）
                app.invalidate()

            await asyncio.sleep(interval)

    self._status_refresh_task = asyncio.create_task(_refresh(1.0))
    return self

def __exit__(self, exc_type, exc_value, traceback) -> None:
    # 清理后台任务
    if self._status_refresh_task is not None:
        self._status_refresh_task.cancel()
```

---

## 完整应用流程

### 用户输入流程

```python
async def prompt(self) -> UserInput:
    # 1. 获取用户输入（含补全、历史、快捷键等）
    with patch_stdout(raw=True):
        command = str(await self._session.prompt_async()).strip()

    # 2. 保存到历史
    self._append_history_entry(command)

    # 3. 解析富文本内容（处理图片占位符）
    content: list[ContentPart] = []
    # ... 解析图片占位符 @[image:xxx]

    # 4. 返回解析后的输入
    return UserInput(
        mode=self._mode,
        thinking=self._thinking,
        content=content,
        command=command,
    )
```

### 历史记录管理

```python
def _append_history_entry(self, text: str) -> None:
    entry = _HistoryEntry(content=text.strip())

    if not entry.content:
        return

    # 去重：不保存重复的连续输入
    if entry.content == self._last_history_content:
        return

    # 追加到 JSONL 文件
    with self._history_file.open("a", encoding="utf-8") as f:
        f.write(entry.model_dump_json(ensure_ascii=False) + "\n")

    self._last_history_content = entry.content
```

**历史文件格式**（JSONL）：
```json
{"content":"hello world"}
{"content":"show me the code"}
{"content":"list files"}
```

---

## Setup 中的 PromptToolkit 应用

### 交互式配置

```python
async def _setup() -> _SetupResult | None:
    # 1. 选择平台（ChoiceInput）
    platform_name = await _prompt_choice(
        header="Select the API platform",
        choices=[p.name for p in _PLATFORMS],
    )

    # 2. 输入 API Key（PromptSession）
    api_key = await _prompt_text("Enter your API key", is_password=True)

    # 3. 选择模型（ChoiceInput）
    model_id = await _prompt_choice(
        header="Select the model",
        choices=model_ids,
    )
```

### 两个辅助函数

#### ChoiceInput

```python
async def _prompt_choice(*, header: str, choices: list[str]) -> str | None:
    try:
        return await ChoiceInput(
            message=header,
            options=[(choice, choice) for choice in choices],
            default=choices[0],
        ).prompt_async()
    except (EOFError, KeyboardInterrupt):
        return None
```

**特点**：
- 用方向键选择
- 用 Enter 确认
- 可取消（Ctrl+C）

#### PromptSession（密码）

```python
async def _prompt_text(prompt: str, *, is_password: bool = False) -> str | None:
    session = PromptSession()
    try:
        return str(
            await session.prompt_async(
                f" {prompt}: ",
                is_password=is_password,  # 不显示密码
            )
        ).strip()
    except (EOFError, KeyboardInterrupt):
        return None
```

**关键参数**：
- `is_password=True`：输入时不显示字符

---

## 对比分析：Click vs PromptToolkit

### 设计对比

| 方面 | Click | PromptToolkit |
|------|-------|---------------|
| **定位** | 命令行工具框架 | 交互式 Shell 框架 |
| **应用模式** | 一次性执行（`python script.py cmd`） | 持久会话（REPL） |
| **补全** | 不支持 | ✅ 完整（Completer） |
| **快捷键** | 不支持 | ✅ 丰富（KeyBindings） |
| **历史** | 不支持 | ✅ 内置（History） |
| **多行输入** | 不支持 | ✅ 支持（multiline） |

### 何时选择哪一个？

#### 选择 Click：
- ✅ 构建 `git`、`docker` 这样的命令行工具
- ✅ 需要定义复杂的命令结构
- ✅ 自动生成帮助文档

#### 选择 PromptToolkit：
- ✅ 构建 `python REPL`、`ipython` 这样的交互式 shell
- ✅ 需要补全和历史记录
- ✅ 需要快捷键支持

### Kimi CLI 的混合应用

```
kimi (Click 入口点)
  ↓
shell 命令（Click）
  ↓
CustomPromptSession（PromptToolkit）
  ↓
交互式会话
```

**分层设计**：
- 最外层：Click（参数解析）
- 内层：PromptToolkit（交互式会话）

---

## 实战要点总结

### 1️⃣ 自定义 Completer

```python
class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        # 获取光标前的文本
        text = document.text_before_cursor

        # 生成补全建议
        for suggestion in self._get_suggestions(text):
            yield Completion(
                text=suggestion,
                start_position=-len(prefix),  # 替换长度
                display=display_text,          # 显示文本
                display_meta=description,      # 描述
            )
```

### 2️⃣ 自定义 KeyBindings

```python
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()

@kb.add("c-x")
def _(event):
    # 处理 Ctrl+X
    event.app.invalidate()  # 重绘

@kb.add("tab", filter=some_condition)
def _(event):
    # 有条件的快捷键
    pass
```

### 3️⃣ 动态工具栏

```python
def my_toolbar():
    # 返回 FormattedText
    return FormattedText([
        ("", "time: 14:23"),
        ("", " | "),
        ("bold red", "error message"),
    ])

session = PromptSession(bottom_toolbar=my_toolbar)
```

### 4️⃣ 后台更新

```python
async def refresh_ui():
    while True:
        app = get_app_or_none()
        if app:
            app.invalidate()  # 触发重绘
        await asyncio.sleep(1)

task = asyncio.create_task(refresh_ui())
```

### 5️⃣ 异步输入

```python
# 同步获取
text = session.prompt(">>> ")

# 异步获取（推荐在 async 上下文中）
text = await session.prompt_async(">>> ")
```

---

## 常见问题

### Q1: 为什么用 `InMemoryHistory` 而不是 `FileHistory`？

**A**: Kimi CLI 自己管理历史文件（存在特定目录，使用 JSONL 格式）。这样可以：
- 每个工作目录独立历史
- 以后可扩展存储额外信息（时间戳、上下文等）
- 避免与 PromptToolkit 默认行为冲突

### Q2: 为什么底部工具栏需要后台刷新任务？

**A**: 底部栏包含时间和 Toast 通知，需要定期更新。后台任务每秒调用 `app.invalidate()` 触发重绘。

### Q3: 怎样支持图片粘贴？

**A**:
```python
# 监听 Ctrl+V
@_kb.add("c-v")
def _paste(event):
    # 1. 用 PIL 从剪贴板获取图片
    image = ImageGrab.grabclipboard()

    # 2. 转成 Base64
    png_base64 = base64.b64encode(image_bytes).decode("ascii")

    # 3. 创建占位符（如 [image:xxx,w×h]）
    placeholder = f"[image:{id},w×h]"

    # 4. 插入到输入框
    event.current_buffer.insert_text(placeholder)

    # 5. 存储实际图片数据
    self._attachment_parts[id] = image_part
```

### Q4: MetaCommandCompleter 和 FileMentionCompleter 如何合并？

**A**:
```python
from prompt_toolkit.completion import merge_completers

completer = merge_completers(
    [MetaCommandCompleter(), FileMentionCompleter(Path.cwd())],
    deduplicate=True,
)
# 返回两个补全器的并集，去重
```

---

## 总结：三个关键设计

### 1️⃣ 分层补全

```
输入文本
  ↓
MetaCommandCompleter 检查 /xxx
  ↓
FileMentionCompleter 检查 @xxx
  ↓
显示补全建议
```

### 2️⃣ 模式动态切换

```
按 Ctrl+X
  ↓
切换 mode: Agent ↔ Shell
  ↓
更新 completer（启用或禁用）
  ↓
重绘 UI（提示符改变）
```

### 3️⃣ 异步响应式 UI

```
后台刷新任务（1秒间隔）
  ↓
调用 app.invalidate()
  ↓
重新渲染工具栏（时间、Toast、状态）
  ↓
用户看到实时更新
```

---

## 深度阅读

### 推荐阅读源码

| 文件 | 重点 |
|------|------|
| `src/kimi_cli/ui/shell/prompt.py` | CustomPromptSession 完整实现 |
| `src/kimi_cli/ui/shell/setup.py` | Setup 流程中的 PromptToolkit 应用 |
| `src/kimi_cli/ui/shell/metacmd.py` | 元命令定义（MetaCommandCompleter 使用） |

### 进阶话题

1. **多线程下的 Completer**：Kimi CLI 中 `FileMentionCompleter` 扫描文件系统，用 `complete_in_thread=True` 避免阻塞 UI
2. **Async/Await 集成**：所有 PromptSession 操作都用 `prompt_async()` 以支持并发
3. **剪贴板集成**：支持图片粘贴，需要 PIL + 特殊处理
4. **性能优化**：缓存文件列表，定期刷新，限制结果数量

---

**最后的话**

> 艹！PromptToolkit 在 Kimi CLI 中的应用就是这样！从基础的补全和快捷键，到动态工具栏和后台刷新，再到图片粘贴和 Toast 通知，完整的交互式 Shell 就是这样搭建起来的。现在理解透彻了吧！💪

---

**文件位置**：`src/kimi_cli/ui/shell/prompt.py` (767 行)
**关键类**：`CustomPromptSession`
**核心概念**：Completer、KeyBindings、PromptSession、FormattedText
