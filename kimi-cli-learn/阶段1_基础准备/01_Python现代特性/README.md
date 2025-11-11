# 模块01: Python 3.13+ 现代特性

**学习时长**: 7天

**学习目标**: 掌握 Python 3.13+ 的现代特性，为阅读 Kimi CLI 源码打下基础

---

## 📋 学习内容概览

1. **类型系统** (Day 1-2)
2. **数据类** (Day 3-4)
3. **上下文管理器** (Day 5)
4. **生成器与迭代器** (Day 6-7)

---

## 🎯 学习目标

- ✅ 能熟练使用 Type Hints、Literal、Union 等类型注解
- ✅ 理解泛型类型和 get_args()、get_origin() 的使用
- ✅ 掌握 dataclass 和 Pydantic 数据模型
- ✅ 能编写自定义上下文管理器
- ✅ 理解生成器和迭代器的区别与应用

---

## 📚 学习资源

### 官方文档
- [Python 3.13 typing 模块](https://docs.python.org/3.13/library/typing.html)
- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [PEP 586 – Literal Types](https://peps.python.org/pep-0586/)
- [dataclasses 文档](https://docs.python.org/3.13/library/dataclasses.html)
- [Pydantic 文档](https://docs.pydantic.dev/)

### 推荐教程
- Real Python: Python Type Checking Guide
- Real Python: Data Classes in Python
- Real Python: Context Managers and Python's with Statement

---

## 📖 详细学习内容

### 📝 01: 类型系统 (Day 1-2)

#### 学习内容

**基础类型注解**:
```python
# 基本类型
name: str = "Alice"
age: int = 25
height: float = 1.75
is_active: bool = True

# 容器类型
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
```

**Literal 类型**:

```python
from typing import Literal

# 限定为精确值
Mode = Literal["dev", "prod", "test"]

def set_mode(mode: Mode) -> None: # 类型注解
    """设置运行模式"""
    # 类型检查器会检查参数是否为 Literal 中的值
    print(f"Mode: {mode}")

# 正确
set_mode("dev")

# 类型错误
set_mode("unknown")  # 类型检查器会报错
```


**Union 和 Optional**:
```python
from typing import Union, Optional

# Union: 多种可能类型
def process(value: Union[int, str]) -> str:
    return str(value)

# Optional: 可能为 None (等价于 Union[T, None])
def find_user(user_id: int) -> Optional[str]:
    # 可能返回 str 或 None
    # 根据用户ID查找用户名
    # -> Optional[str]: 可能返回 str 或 None
    # 从数据库获取用户名
    return database.get(user_id)


```



**泛型类型**:
```python
from typing import List, Dict, Tuple, Set

# 泛型容器
users: List[str] = ["Alice", "Bob"]
config: Dict[str, int] = {"timeout": 30}
point: Tuple[float, float] = (1.5, 2.3)
tags: Set[str] = {"python", "typing"}
```

**类型检查工具函数**:
```python
from typing import get_args, get_origin, Literal

UIMode = Literal["shell", "print", "acp", "wire"]

# 获取所有可能的值
print(get_args(UIMode))  # ('shell', 'print', 'acp', 'wire')

# 获取原始类型
from typing import List
print(get_origin(List[int]))  # list
```

**Kimi CLI 中的实际应用**:
```python
# src/kimi_cli/cli.py
from typing import Literal, get_args

UIMode = Literal["shell", "print", "acp", "wire"]
InputFormat = Literal["text", "stream-json"]
OutputFormat = Literal["text", "stream-json"]

@click.option(
    "--ui",
    "ui",
    type=click.Choice(get_args(UIMode)),  # 从 Literal 获取选项
    default="shell",
)
def kimi(ui: UIMode):
    # ui 类型被限定为 4 个值之一
    # shell : 交互式 shell 模式
    # print : 打印模式
    # acp : Agent Client Protocol 模式
    # wire :  wire 协议模式
    pass
```


#### 实践练习

**练习1**: 类型安全的配置类
```python
# 文件: 代码实践/01_type_system_practice.py

from typing import Literal, Union, Optional, get_args

# 定义配置类型
Environment = Literal["development", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

class Config:
    """类型安全的配置类"""

    def __init__(
        self,
        env: Environment,
        log_level: LogLevel = "INFO",
        port: int = 8000,
        debug: bool = False,
    ):
        # 验证环境
        if env not in get_args(Environment):
            raise ValueError(f"Invalid environment: {env}")

        self.env = env
        self.log_level = log_level
        self.port = port
        self.debug = debug

    def is_production(self) -> bool:
        return self.env == "production"

# 测试
if __name__ == "__main__":
    # 正确用法
    config = Config("development", log_level="DEBUG", debug=True)
    print(f"Environment: {config.env}")
    print(f"Is production: {config.is_production()}")

    # 类型检查器会报错（运行时也会报错）
    # config = Config("invalid")
```

**练习2**: 模拟 Kimi CLI 的参数类型

```python
# 文件: 代码实践/02_kimi_types_practice.py

from typing import Literal, get_args
from pathlib import Path

# 定义类型
UIMode = Literal["shell", "print", "acp", "wire"]
InputFormat = Literal["text", "stream-json"]

class KimiConfig:
    """Kimi CLI 配置"""

    def __init__(
        self,
        work_dir: Path,
        ui: UIMode = "shell",
        input_format: InputFormat = "text",
        model_name: str | None = None,
        yolo: bool = False,
    ):  # 初始化配置 , 通过 " ): " 可以指定默认值,这是 Python 的一种语法糖
        
        self.work_dir = work_dir.absolute() # 工作目录, 绝对路径
        self.ui = ui # 用户界面模式
        self.input_format = input_format # 输入格式
        self.model_name = model_name # 模型名称
        
        # 是否开启 YOLO 模型: 开启后会在模型推理中使用 YOLO 模型进行目标检测, 并在结果中添加目标框 ,从而可以在打印模式下显示目标框
        # 注意: 开启后会增加模型推理的时间, 建议仅在需要可视化目标检测结果时开启
        self.yolo = yolo 
        
        

    def __repr__(self) -> str: # 表示方法, 用于打印对象
        return (
            f"KimiConfig(work_dir={self.work_dir}, ui={self.ui}, "
            f"input_format={self.input_format}, model={self.model_name}, yolo={self.yolo})"
        )

# 测试
if __name__ == "__main__":
    config = KimiConfig(
        work_dir=Path.cwd(), # 当前工作目录
        ui="shell", # 用户界面模式
        input_format="text", # 输入格式
        model_name="kimi-for-coding", # 模型名称
        yolo=True, # 是否开启 YOLO 模型
    )
    print(config) # 打印配置
```

#### 检查点
- [ ] 能正确使用各种类型注解
- [ ] 理解 Literal 的作用和使用场景
- [ ] 掌握 get_args() 和 get_origin()
- [ ] 代码通过 pyright/mypy 类型检查

---

### 📝 02: 数据类 (Day 3-4)

#### 学习内容

**dataclass 基础**:
```python
from dataclasses import dataclass

@dataclass # 数据类, 用于存储数据
class Person:
    name: str
    age: int
    email: str

    def greet(self) -> str: # 打招呼方法, 返回打招呼字符串
        return f"Hi, I'm {self.name}, {self.age} years old"

# 使用
person = Person("Alice", 25, "alice@example.com") # 创建 Person 对象
print(person)  # Person(name='Alice', age=25, email='alice@example.com')
```

**dataclass 高级特性**:
```python
from dataclasses import dataclass, field

@dataclass(slots=True, frozen=True)
class Point: 
    """
    slots=True: 优化内存使用
    frozen=True: 不可变对象
    """
    x: float
    y: float

    def distance(self) -> float: # 计算点到原点的距离
        return (self.x ** 2 + self.y ** 2) ** 0.5

@dataclass
class Config: # 配置类, 用于存储配置信息
    name: str
    values: list[int] = field(default_factory=list)  # 可变默认值
    _private: str = field(default="", repr=False)    # 不显示在 repr 中

# Kimi CLI 中的应用
from dataclasses import dataclass

@dataclass(slots=True)
class LLM:
    """LLM 模型配置"""
    chat_provider: ChatProvider # 聊天提供商
    max_context_size: int = 100_000 # 最大上下文大小
    capabilities: set[str] = field(default_factory=set) # 能力集

    @property
    def model_name(self) -> str: # 模型名称属性, 返回聊天提供商的模型名称
        return self.chat_provider.model_name
```

**Pydantic 数据验证**:
```python
from pydantic import BaseModel, Field, validator, SecretStr

class LLMProvider(BaseModel): # LLM 提供商配置类, 用于存储 LLM 提供商的配置信息
    """LLM 提供商配置"""
    type: str = Field(..., description="Provider type")
    base_url: str = Field(..., description="API base URL")
    api_key: SecretStr = Field(..., description="API key")
    custom_headers: dict[str, str] | None = None

    @validator('base_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('base_url must start with http:// or https://')
        return v

class LLMModel(BaseModel): # LLM 模型配置类, 用于存储 LLM 模型的配置信息
    """LLM 模型配置"""
    provider: str # 提供商名称
    model: str # 模型名称
    max_context_size: int = 100_000 # 最大上下文大小
    capabilities: set[str] = Field(default_factory=set) # 能力集

# 使用
provider = LLMProvider( 
    type="kimi",
    base_url="https://api.moonshot.cn/v1",
    api_key=SecretStr("sk-xxx"),
)

model = LLMModel(
    provider="kimi",
    model="kimi-for-coding",
    max_context_size=128_000,
    capabilities={"thinking", "image_in"},
)

# 验证失败示例
# provider = LLMProvider(
#     type="kimi",
#     base_url="invalid-url",  # ValueError
#     api_key=SecretStr("sk-xxx"),
# )
```

#### 实践练习

**练习3**: 实现 Kimi CLI 配置模型
```python
# 文件: 代码实践/03_dataclass_practice.py

from dataclasses import dataclass, field
from pydantic import BaseModel, Field, SecretStr
from typing import Literal

# 使用 dataclass
@dataclass(slots=True)
class SessionInfo: # 会话信息类, 用于存储会话信息
    """会话信息"""
    id: str
    work_dir: str
    created_at: float
    history_file: str | None = None

    def is_active(self) -> bool:
        import time
        # 24小时内的会话认为是活跃的
        # 拓展 : 如何优化这个方法, 避免频繁调用 time.time()
        return time.time() - self.created_at < 86400
        
    
    
    
# 使用 Pydantic : Pydantic是指一个用于数据验证和设置的Python库, 用于定义数据模型和验证数据
ProviderType = Literal["kimi", "openai_legacy", "openai_responses", "anthropic"]

class ProviderConfig(BaseModel):
    """提供商配置"""
    type: ProviderType
    base_url: str = Field(..., min_length=1)
    api_key: SecretStr
    custom_headers: dict[str, str] = Field(default_factory=dict)

    class Config:
        # Pydantic 配置 : 定义 JSON 示例
        json_schema_extra = {
            "example": {
                "type": "kimi",
                "base_url": "https://api.moonshot.cn/v1",
                "api_key": "sk-xxx",
            }
        }

class ModelConfig(BaseModel):
    """模型配置"""
    provider: str
    model: str
    max_context_size: int = Field(default=100_000, gt=0)
    capabilities: set[str] = Field(default_factory=set)

# 测试
if __name__ == "__main__":
    # dataclass
    session = SessionInfo( # 会话信息对象, 用于存储会话信息
        id="abc123",
        work_dir="/home/user/project",
        created_at=1704844800.0,
    )
    print(f"Session active: {session.is_active()}")

    # Pydantic
    provider = ProviderConfig( # 提供商配置对象, 用于存储提供商的配置信息
        type="kimi",
        base_url="https://api.moonshot.cn/v1",
        api_key=SecretStr("sk-xxx"),
    )
    print(provider.model_dump())  # 序列化

    model = ModelConfig(
        provider="kimi",
        model="kimi-for-coding",
        max_context_size=128_000,
        capabilities={"thinking"},
    )
    print(model.model_dump_json(indent=2))  # JSON 输出 : 模型配置对象的 JSON 表示
```

#### 检查点
- [ ] 理解 dataclass 和 Pydantic 的区别
- [ ] 能选择合适的数据模型工具
- [ ] 掌握数据验证技巧
- [ ] 能定义复杂的数据结构

---

### 📝 03: 上下文管理器 (Day 5)

#### 学习内容

**with 语句基础**:
```python
# 文件操作
with open('file.txt') as f:
    content = f.read()
# 文件自动关闭

# 自定义上下文管理器
class ManagedResource:
    def __enter__(self): # 上下文管理器的进入方法, 用于获取资源
        print("Acquiring resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): # 上下文管理器的退出方法, 用于释放资源
        print("Releasing resource")
        return False  # False: 不抑制异常

with ManagedResource() as resource: # 上下文管理器的使用示例, 用于获取和释放资源
    print("Using resource")
    # 可能抛出异常
```
 
**contextlib 模块**:````
```python
from contextlib import contextmanager

@contextmanager
def file_lock(path: str):
    """文件锁上下文管理器"""
    lock = acquire_lock(path) # 上下文管理器的进入方法, 用于获取资源
    try:
        yield lock
    finally:
        release_lock(lock) # 上下文管理器的退出方法, 用于释放资源

# 使用
with file_lock("data.txt") as lock: # 上下文管理器的使用示例, 用于获取和释放资源
    # 持有锁
    process_file("data.txt")
# 自动释放锁
```````

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/app.py
@contextlib.contextmanager
def _app_env(self) -> Generator[None]: # 上下文管理器的进入方法, 用于获取应用环境
    """应用环境上下文管理器"""
    original_cwd = Path.cwd() # 上下文管理器的进入方法, 用于获取当前工作目录
    os.chdir(self._runtime.session.work_dir)  # 切换工作目录
    try:
        warnings.filterwarnings("ignore", category=DeprecationWarning) # 上下文管理器的进入方法, 用于忽略警告
        
        with contextlib.redirect_stderr(StreamToLogger()): # 上下文管理器的进入方法, 用于重定向标准错误输出到日志
            
            yield # 上下文管理器的退出方法, 用于恢复标准错误输出
    finally:
        os.chdir(original_cwd)  # 上下文管理器的退出方法, 用于恢复原目录
```

#### 实践练习

**练习4**: 实现实用的上下文管理器
```python
# 文件: 代码实践/04_context_manager_practice.py

import contextlib
import time
from pathlib import Path

# 1. 计时器
@contextlib.contextmanager
def timer(name: str):
    """计时上下文管理器"""
    start = time.time()
    print(f"[{name}] 开始...")
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"[{name}] 完成，耗时: {elapsed:.2f}秒")

# 2. 临时目录切换
@contextlib.contextmanager
def temporary_directory(path: Path):
    """临时切换工作目录"""
    original_dir = Path.cwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original_dir)

# 3. 环境变量设置
@contextlib.contextmanager
def env_vars(**kwargs):
    """临时设置环境变量"""
    original = {}
    for key, value in kwargs.items():
        original[key] = os.environ.get(key)
        os.environ[key] = value
    try:
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

# 测试
if __name__ == "__main__":
    # 计时器
    with timer("Data Processing"):
        time.sleep(1)
        # 处理数据

    # 临时目录
    with temporary_directory(Path("/tmp")):
        print(f"Current dir: {Path.cwd()}")

    # 环境变量
    with env_vars(API_KEY="test-key", DEBUG="true"):
        print(os.environ["API_KEY"])
```

#### 检查点
- [ ] 理解上下文管理器的作用
- [ ] 能使用 @contextmanager 装饰器
- [ ] 能处理上下文中的异常
- [ ] 理解 Kimi CLI 的环境管理

---

### 📝 04: 生成器与迭代器 (Day 6-7)

#### 学习内容

**Generator 和 Iterator**:
```python
# Iterator (迭代器)
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

# Generator (生成器)
def countdown(start):
    while start > 0:
        yield start
        start -= 1

# 使用
for i in countdown(5):
    print(i)  # 5, 4, 3, 2, 1
```

**yield 关键字**:
```python
def fibonacci(n):
    """斐波那契数列生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a # yield 语句会暂停函数的执行, 并返回当前值
        a, b = b, a + b # 更新状态, 准备下一次迭代

# 使用
for num in fibonacci(10):
    print(num, end=" ")  # 0 1 1 2 3 5 8 13 21 34
```

**生成器表达式**:
```python
# 列表推导式
squares = [x**2 for x in range(10)]  # 立即计算，占用内存

# 生成器表达式
squares_gen = (x**2 for x in range(10))  # 惰性求值，节省内存

# 使用
for square in squares_gen:
    print(square)
```

**itertools 实用工具**:
```python
import itertools

# chain: 连接多个迭代器
combined = itertools.chain([1, 2], [3, 4], [5, 6])
print(list(combined))  # [1, 2, 3, 4, 5, 6]

# islice: 切片迭代器
sliced = itertools.islice(range(100), 10, 20)
print(list(sliced))  # [10, 11, ..., 19]

# batched: 分批（Python 3.12+）
batches = itertools.batched(range(10), 3)
for batch in batches:
    print(batch)  # (0, 1, 2), (3, 4, 5), ...
```

#### 实践练习

**练习5**: 实用生成器
```python
# 文件: 代码实践/05_generator_practice.py

from typing import Generator, Iterator
import itertools

# 1. 分块读取大文件
def read_file_in_chunks(file_path: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """按块读取文件"""
    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

# 2. 分批处理数据
def batch_processor(items: list, batch_size: int) -> Generator[list, None, None]:
    """分批处理数据"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

# 3. 无限序列生成器
def counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """无限计数器"""
    current = start
    while True:
        yield current
        current += step

# 4. 流式数据处理管道
def process_pipeline(data: Iterator[str]) -> Generator[dict, None, None]:
    """数据处理管道"""
    # 第一步: 过滤空行
    filtered = (line.strip() for line in data if line.strip())

    # 第二步: 转换格式
    transformed = ({"line": i, "content": line} for i, line in enumerate(filtered))

    # 第三步: 处理
    for item in transformed:
        yield item

# 测试
if __name__ == "__main__":
    # 分块读取
    # for chunk in read_file_in_chunks("large_file.txt", 512):
    #     process(chunk)

    # 分批处理
    items = list(range(100))
    for batch in batch_processor(items, 10):
        print(f"Processing batch: {batch[0]}-{batch[-1]}")

    # 无限序列
    c = counter(10, 5)
    for _ in range(5):
        print(next(c))  # 10, 15, 20, 25, 30

    # 处理管道
    data = ["  line 1  ", "", "line 2", "  ", "line 3"]
    for item in process_pipeline(iter(data)):
        print(item)
```

#### 检查点
- [ ] 理解 Generator 和 Iterator 的区别
- [ ] 能用 yield 编写生成器
- [ ] 掌握生成器表达式
- [ ] 能用 itertools 优化代码

---

## 📊 模块总结

### 知识点检查
- [ ] Type Hints 和 Literal 类型
- [ ] dataclass 和 Pydantic
- [ ] 上下文管理器
- [ ] 生成器和迭代器

### 代码练习
- [ ] 练习1: 类型安全配置类
- [ ] 练习2: Kimi 类型实践
- [ ] 练习3: 数据模型
- [ ] 练习4: 上下文管理器
- [ ] 练习5: 生成器应用

### 输出成果
- [ ] 5个练习代码
- [ ] 学习笔记
- [ ] 代码提交到 Git

---

## 🔄 下一步

完成本模块后，进入 **模块02: 异步编程**。

---

*Created by 老王 | Last Updated: 2025-01-10*
