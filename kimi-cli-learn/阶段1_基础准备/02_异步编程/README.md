# 模块02: 异步编程

**学习时长**: 7天

**学习目标**: 深入掌握 Python 异步编程，理解 Kimi CLI 的异步架构

---

## 📋 学习内容概览

1. **asyncio 基础** (Day 8-9)
2. **异步 I/O** (Day 10-11)
3. **并发控制** (Day 12-13)
4. **异步生成器** (Day 14)

---

## 🎯 学习目标

- ✅ 理解异步编程的核心概念（事件循环、协程）
- ✅ 掌握 async/await 语法
- ✅ 能使用 aiohttp、aiofiles 进行异步 I/O
- ✅ 掌握异步并发控制（gather, wait, Semaphore）
- ✅ 理解并能编写异步生成器
- ✅ 理解 Kimi CLI 的异步架构设计

---

## 📚 学习资源

### 官方文档
- [asyncio 官方文档](https://docs.python.org/3.13/library/asyncio.html)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [aiofiles 文档](https://github.com/Tinche/aiofiles)

### 推荐教程
- Real Python: Async IO in Python
- Real Python: Getting Started With Async Features
- FastAPI 异步教程

---

## 📖 详细学习内容

### 📝 01: asyncio 基础 (Day 8-9)

#### 学习内容

**async/await 语法基础**:
```python
import asyncio

# 定义异步函数
async def say_hello(name: str, delay: int):
    """异步打招呼"""
    print(f"Hello {name}!")
    await asyncio.sleep(delay)  # 异步等待
    print(f"Goodbye {name}!")

# 运行异步函数
asyncio.run(say_hello("Alice", 1)) # 运行异步函数, 输出: Hello Alice!, Goodbye Alice!
```

**事件循环 (Event Loop)**:
```python
import asyncio

# 方式1: asyncio.run() (推荐，Python 3.7+)
async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
#结果: Hello, World!
asyncio.run(main())

# 方式2: 手动管理事件循环（不推荐）
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

**Task 和 Future**:
```python
import asyncio

async def task_example():
    """Task 示例"""
    # 创建 Task
    task = asyncio.create_task(say_hello("Alice", 1))

    # 可以在这里做其他事情
    print("Task created, doing other work...")

    # 等待 Task 完成
    await task

# Task vs 直接 await
async def demo():
    # 直接 await（顺序执行）
    await asyncio.sleep(1)
    await asyncio.sleep(1)  # 总共 2 秒

    # 使用 Task（并发执行）
    task1 = asyncio.create_task(asyncio.sleep(1))
    task2 = asyncio.create_task(asyncio.sleep(1))
    await task1 # 等待 task1 完成
    await task2 # 等待 task2 完成, 总共 1 秒
    



```

**协程 (Coroutine)**:
```python
import asyncio

# 协程函数定义
async def coroutine_func():
    """这是一个协程函数"""
    await asyncio.sleep(0.1)
    return "Result"

# 调用协程函数返回协程对象
coro = coroutine_func()  # 这不会执行函数！

# 必须 await 或传给事件循环
result = asyncio.run(coroutine_func())  # 这才会执行
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/app.py
async def run_shell_mode(self, command: str | None = None) -> bool:
    """运行 Shell 模式（异步）"""
    from kimi_cli.ui.shell import ShellApp

    welcome_info = [...]  # 欢迎信息

    # 在异步上下文中运行
    with self._app_env():
        app = ShellApp(self._soul, welcome_info=welcome_info)
        return await app.run(command)  # await 异步运行

# src/kimi_cli/cli.py
async def _run() -> bool:
    """内部异步运行函数"""
    instance = await KimiCLI.create(...)  # await 创建实例

    match ui:
        case "shell":
            return await instance.run_shell_mode(command)  # await 运行
        case "print":
            return await instance.run_print_mode(...)
        # ...

# 入口：同步到异步的桥梁
while True:
    try:
        succeeded = asyncio.run(_run())  # 启动事件循环
        if not succeeded:
            sys.exit(1)
        break
    except Reload:
        continue
```

#### 实践练习

**练习6**: 异步计时器和并发执行
```python
# 文件: 代码实践/06_asyncio_basics.py

import asyncio
import time

async def async_timer(seconds: int, name: str) -> str:
    """异步计时器"""
    print(f"[{name}] 开始（{seconds}秒）")
    start = time.time()
    await asyncio.sleep(seconds)
    elapsed = time.time() - start
    print(f"[{name}] 完成（实际耗时: {elapsed:.2f}秒）")
    return f"{name} completed"


async def sequential_execution():
    """顺序执行（慢）"""
    print("\n=== 顺序执行 ===")
    start = time.time()

    await async_timer(1, "Task1")
    await async_timer(2, "Task2")
    await async_timer(3, "Task3")

    total = time.time() - start
    print(f"总耗时: {total:.2f}秒")  # 约 6 秒


async def concurrent_execution():
    """并发执行（快）"""
    print("\n=== 并发执行 ===")
    start = time.time()

    # 方式1: 使用 gather
    results = await asyncio.gather(
        async_timer(1, "Task1"),
        async_timer(2, "Task2"),
        async_timer(3, "Task3"),
    )
    print(f"结果: {results}")

    total = time.time() - start
    print(f"总耗时: {total:.2f}秒")  # 约 3 秒（最长的那个）


async def task_based_execution():
    """基于 Task 的执行"""
    print("\n=== 基于 Task 的执行 ===")
    start = time.time()

    # 创建 Task
    task1 = asyncio.create_task(async_timer(1, "Task1"))
    task2 = asyncio.create_task(async_timer(2, "Task2"))
    task3 = asyncio.create_task(async_timer(3, "Task3"))

    # 可以在这里做其他事情
    print("Tasks 已创建，等待完成...")

    # 等待所有 Task
    await task1
    await task2
    await task3

    total = time.time() - start
    print(f"总耗时: {total:.2f}秒")


async def main():
    """主函数"""
    await sequential_execution()
    await concurrent_execution()
    await task_based_execution()


if __name__ == "__main__":
    asyncio.run(main())


# 扩展练习:
# 1. 实现一个异步倒计时器
# 2. 实现异步任务取消（task.cancel()）
# 3. 实现异步超时控制（asyncio.wait_for()）
# 4. 处理异步异常
```

#### 检查点
- [ ] 理解 async/await 语法
- [ ] 理解事件循环的作用
- [ ] 掌握 Task 和 Future 的区别
- [ ] 能编写并发异步代码

---

### 📝 02: 异步 I/O (Day 10-11)

#### 学习内容

**aiohttp 异步 HTTP 客户端**:
```python
import aiohttp
import asyncio

async def fetch_url(url: str) -> str:
    """异步获取 URL 内容"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# 使用
async def main():
    html = await fetch_url("https://example.com")
    print(html[:100])

asyncio.run(main())
```

**并发获取多个 URL**:
```python
async def fetch_multiple_urls(urls: list[str]) -> list[str]:
    """并发获取多个 URL"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_one(session: aiohttp.ClientSession, url: str) -> str:
    """获取单个 URL"""
    async with session.get(url) as response:
        return await response.text()
```

**aiofiles 异步文件操作**:
```python
import aiofiles

async def read_file_async(file_path: str) -> str:
    """异步读取文件"""
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()
    return content

async def write_file_async(file_path: str, content: str):
    """异步写入文件"""
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(content)
```

**httpx 异步 HTTP 客户端**（Kimi CLI 使用）:
```python
import httpx

async def fetch_with_httpx(url: str) -> str:
    """使用 httpx 获取 URL"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# 支持 HTTP/2, 更好的性能
```

**Kimi CLI 中的应用**:
```python
# src/kimi_cli/llm.py (使用 kosong 库，底层用 httpx)
# src/kimi_cli/soul/kimisoul.py
async def chat(self, user_input: str) -> AsyncIterator[str]:
    """异步聊天（流式响应）"""
    # 调用 LLM API（异步 HTTP）
    async for chunk in self._llm.astream_chat(messages):
        yield chunk  # 异步生成器

# src/kimi_cli/tools/web/fetch.py
async def fetch_url(url: str) -> str:
    """异步获取网页内容"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

#### 实践练习

**练习7**: 异步爬虫
```python
# 文件: 代码实践/07_async_io_practice.py

import asyncio
import aiohttp
import aiofiles
import time
from pathlib import Path

async def fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    index: int
) -> tuple[int, str, str]:
    """获取单个 URL"""
    print(f"[{index}] 开始获取: {url}")
    start = time.time()

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            content = await response.text()
            elapsed = time.time() - start
            print(f"[{index}] 完成: {url} ({elapsed:.2f}秒)")
            return (index, url, content)
    except Exception as e:
        print(f"[{index}] 错误: {url} - {e}")
        return (index, url, "")


async def save_to_file(file_path: Path, content: str):
    """异步保存到文件"""
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(content)


async def async_crawler(urls: list[str], save_dir: Path):
    """异步爬虫"""
    print(f"\n=== 开始爬取 {len(urls)} 个网页 ===\n")
    start = time.time()

    # 创建保存目录
    save_dir.mkdir(parents=True, exist_ok=True)

    # 并发获取所有 URL
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, i) for i, url in enumerate(urls)]
        results = await asyncio.gather(*tasks)

    # 异步保存所有文件
    save_tasks = []
    for index, url, content in results:
        if content:
            file_name = f"page_{index}.html"
            file_path = save_dir / file_name
            save_tasks.append(save_to_file(file_path, content))

    await asyncio.gather(*save_tasks)

    total = time.time() - start
    print(f"\n=== 爬取完成，总耗时: {total:.2f}秒 ===")
    print(f"保存位置: {save_dir}")


async def main():
    """主函数"""
    # 测试 URL 列表
    urls = [
        "https://example.com",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3",
    ]

    save_dir = Path("./crawler_output")
    await async_crawler(urls, save_dir)


if __name__ == "__main__":
    asyncio.run(main())


# 扩展练习:
# 1. 添加重试机制（tenacity 库）
# 2. 添加进度条（Rich Progress）
# 3. 支持代理和自定义 Headers
# 4. 实现速率限制（避免被封）
```

#### 检查点
- [ ] 掌握 aiohttp 使用
- [ ] 掌握 aiofiles 文件操作
- [ ] 能编写异步爬虫
- [ ] 理解异步 I/O 的优势

---

### 📝 03: 并发控制 (Day 12-13)

#### 学习内容

**asyncio.gather() - 并发执行**:
```python
import asyncio

# gather: 等待所有任务完成
results = await asyncio.gather(
    task1(),
    task2(),
    task3(),
    return_exceptions=True  # 返回异常而非抛出
)
# results: [result1, result2, result3] 或包含异常
```

**asyncio.wait() - 更灵活的等待**:
```python
# wait: 更底层的控制
done, pending = await asyncio.wait(
    [task1(), task2(), task3()],
    timeout=5.0,  # 超时
    return_when=asyncio.FIRST_COMPLETED  # 返回条件
)
# return_when 选项:
# - FIRST_COMPLETED: 任意一个完成
# - FIRST_EXCEPTION: 第一个异常
# - ALL_COMPLETED: 全部完成（默认）
```

**asyncio.Semaphore - 限流**:
```python
import asyncio

async def download_with_limit(url: str, semaphore: asyncio.Semaphore):
    """限流下载"""
    async with semaphore:  # 获取信号量
        # 最多同时运行的数量受限
        return await download(url)

async def main():
    # 最多 5 个并发
    semaphore = asyncio.Semaphore(5)

    tasks = [
        download_with_limit(url, semaphore)
        for url in urls  # 100 个 URL
    ]
    await asyncio.gather(*tasks)
    # 虽然有 100 个任务，但最多只有 5 个同时运行
```

**asyncio.Queue - 异步队列**:
```python
import asyncio

async def producer(queue: asyncio.Queue):
    """生产者"""
    for i in range(10):
        await queue.put(i)
        print(f"生产: {i}")
        await asyncio.sleep(0.1)

async def consumer(queue: asyncio.Queue, name: str):
    """消费者"""
    while True:
        item = await queue.get()
        print(f"[{name}] 消费: {item}")
        await asyncio.sleep(0.5)
        queue.task_done()

async def main():
    queue = asyncio.Queue(maxsize=5)  # 队列最大 5 个元素

    # 启动生产者和消费者
    await asyncio.gather(
        producer(queue),
        consumer(queue, "Consumer1"),
        consumer(queue, "Consumer2"),
    )
```

**超时控制**:
```python
import asyncio

# asyncio.wait_for() - 超时控制
try:
    result = await asyncio.wait_for(
        slow_task(),
        timeout=5.0  # 5 秒超时
    )
except asyncio.TimeoutError:
    print("任务超时")
```

#### 实践练习

**练习8**: 限流异步下载器
```python
# 文件: 代码实践/08_concurrency_control.py

import asyncio
import aiohttp
import time
from typing import AsyncIterator

class AsyncDownloader:
    """异步下载器（带限流）"""

    def __init__(self, max_concurrency: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def download_one(self, url: str, index: int) -> tuple[int, bool, str]:
        """下载单个文件"""
        async with self.semaphore:  # 限流
            print(f"[{index}] 开始下载: {url}")
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    content = await response.text()
                    print(f"[{index}] 完成: {url[:50]}...")
                    return (index, True, content[:100])
            except Exception as e:
                print(f"[{index}] 失败: {url} - {e}")
                return (index, False, str(e))

    async def download_all(self, urls: list[str]) -> list[tuple[int, bool, str]]:
        """下载所有文件"""
        tasks = [self.download_one(url, i) for i, url in enumerate(urls)]
        return await asyncio.gather(*tasks)


async def demo_gather_vs_wait():
    """演示 gather 和 wait 的区别"""

    async def task(n: int, delay: float):
        await asyncio.sleep(delay)
        if n == 2:
            raise ValueError(f"Task {n} failed")
        return f"Result {n}"

    print("\n=== gather 示例 ===")
    try:
        results = await asyncio.gather(
            task(1, 0.5),
            task(2, 1.0),
            task(3, 0.3),
            return_exceptions=True  # 返回异常
        )
        print(f"结果: {results}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n=== wait 示例 ===")
    tasks_set = {
        asyncio.create_task(task(1, 0.5)),
        asyncio.create_task(task(2, 1.0)),
        asyncio.create_task(task(3, 0.3)),
    }
    done, pending = await asyncio.wait(
        tasks_set,
        return_when=asyncio.FIRST_COMPLETED  # 第一个完成就返回
    )
    print(f"完成任务数: {len(done)}")
    print(f"待处理任务数: {len(pending)}")

    # 取消待处理任务
    for task in pending:
        task.cancel()


async def main():
    """主函数"""
    # 测试限流下载
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/3",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/1",
    ]

    print(f"下载 {len(urls)} 个文件，最多 3 个并发")
    start = time.time()

    async with AsyncDownloader(max_concurrency=3) as downloader:
        results = await downloader.download_all(urls)

    elapsed = time.time() - start
    success_count = sum(1 for _, success, _ in results if success)
    print(f"\n总耗时: {elapsed:.2f}秒")
    print(f"成功: {success_count}/{len(urls)}")

    # 演示 gather vs wait
    await demo_gather_vs_wait()


if __name__ == "__main__":
    asyncio.run(main())


# 扩展练习:
# 1. 实现异步生产者-消费者模式
# 2. 添加重试机制（指数退避）
# 3. 实现动态并发控制（根据系统负载）
# 4. 添加进度追踪
```

#### 检查点
- [ ] 理解 gather 和 wait 的区别
- [ ] 掌握 Semaphore 限流
- [ ] 能使用 asyncio.Queue
- [ ] 掌握超时控制

---

### 📝 04: 异步生成器 (Day 14)

#### 学习内容

**async for - 异步迭代**:
```python
async def async_range(n: int):
    """异步生成器"""
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

# 使用
async for num in async_range(5):
    print(num)
```

**AsyncGenerator 类型**:
```python
from typing import AsyncGenerator

async def stream_data() -> AsyncGenerator[str, None]:
    """流式数据生成器"""
    for i in range(10):
        await asyncio.sleep(0.1)
        yield f"Chunk {i}"
```

**流式响应处理**（重要！）:
```python
import aiohttp

async def stream_response(url: str) -> AsyncGenerator[str, None]:
    """流式获取响应"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # 逐块读取
            async for chunk in response.content.iter_chunked(1024):
                yield chunk.decode()

# 使用
async for chunk in stream_response("https://api.example.com/stream"):
    print(chunk, end='')
```

**Kimi CLI 中的流式响应**:
```python
# src/kimi_cli/soul/kimisoul.py
async def chat(self, user_input: str) -> AsyncIterator[str]:
    """聊天（流式）"""
    messages = self._build_messages(user_input)

    # 调用 LLM，流式返回
    async for chunk in self._llm.chat_provider.astream_chat(messages):
        # 逐块处理
        if chunk.delta.content:
            yield chunk.delta.content  # 异步生成器

# src/kimi_cli/ui/shell/app.py
async def _display_response_stream(self, stream: AsyncIterator[str]):
    """显示流式响应"""
    async for chunk in stream:
        # 实时显示
        print(chunk, end='', flush=True)
```

#### 实践练习

**练习9**: 流式响应解析器
```python
# 文件: 代码实践/09_async_generator.py

import asyncio
import aiohttp
import json
from typing import AsyncGenerator

async def stream_sse_events(url: str) -> AsyncGenerator[dict, None]:
    """
    流式解析 SSE (Server-Sent Events)

    SSE 格式:
    data: {"content": "Hello"}
    data: {"content": " World"}
    data: [DONE]
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for line in response.content:
                line = line.decode().strip()

                # 跳过空行
                if not line:
                    continue

                # 解析 data: 行
                if line.startswith("data: "):
                    data = line[6:]  # 去掉 "data: "

                    # 结束标记
                    if data == "[DONE]":
                        break

                    # 解析 JSON
                    try:
                        event = json.loads(data)
                        yield event
                    except json.JSONDecodeError:
                        continue


async def stream_file_lines(file_path: str) -> AsyncGenerator[str, None]:
    """异步按行读取文件"""
    import aiofiles

    async with aiofiles.open(file_path, 'r') as f:
        async for line in f:
            yield line.strip()


async def batch_generator(
    items: list,
    batch_size: int
) -> AsyncGenerator[list, None]:
    """分批生成器"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        # 模拟异步处理
        await asyncio.sleep(0.1)
        yield batch


async def simulated_llm_stream(prompt: str) -> AsyncGenerator[str, None]:
    """模拟 LLM 流式响应"""
    response = f"Response to: {prompt}. This is a simulated streaming response."
    words = response.split()

    for word in words:
        await asyncio.sleep(0.05)  # 模拟网络延迟
        yield word + " "


async def demo_stream_processing():
    """演示流式处理"""
    print("\n=== 模拟 LLM 流式响应 ===")
    prompt = "What is Python?"

    full_response = ""
    async for chunk in simulated_llm_stream(prompt):
        print(chunk, end='', flush=True)  # 实时显示
        full_response += chunk

    print(f"\n\n完整响应: {full_response}")


async def demo_batch_processing():
    """演示分批处理"""
    print("\n=== 分批处理 ===")
    items = list(range(20))

    async for batch in batch_generator(items, batch_size=5):
        print(f"处理批次: {batch}")


async def demo_file_streaming():
    """演示文件流式读取"""
    print("\n=== 流式读取文件 ===")

    # 创建测试文件
    import aiofiles
    test_file = "test_stream.txt"
    async with aiofiles.open(test_file, 'w') as f:
        await f.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")

    # 流式读取
    line_count = 0
    async for line in stream_file_lines(test_file):
        print(f"读取: {line}")
        line_count += 1

    print(f"总共 {line_count} 行")


async def main():
    """主函数"""
    await demo_stream_processing()
    await demo_batch_processing()
    await demo_file_streaming()


if __name__ == "__main__":
    asyncio.run(main())


# 扩展练习:
# 1. 实现 SSE 完整解析器
# 2. 实现流式 JSON 解析
# 3. 实现异步管道（多个生成器串联）
# 4. 分析 Kimi CLI 的流式响应实现
```

#### 检查点
- [ ] 理解 async for 和异步生成器
- [ ] 能处理流式 HTTP 响应
- [ ] 理解 SSE 协议
- [ ] 理解 Kimi CLI 的流式架构

---

## 📊 模块总结

### 知识点检查
- [ ] async/await 语法
- [ ] 事件循环和 Task
- [ ] aiohttp 和 aiofiles
- [ ] 并发控制（gather, wait, Semaphore）
- [ ] 异步生成器和流式处理

### 代码练习
- [ ] 练习6: asyncio 基础
- [ ] 练习7: 异步爬虫
- [ ] 练习8: 并发控制
- [ ] 练习9: 异步生成器

### 综合项目
- [ ] **异步爬虫项目**（整合所有知识点）
  - 爬取多个网站
  - 限流控制
  - 异步保存文件
  - 进度显示
  - 错误处理和重试

### 输出成果
- [ ] 4个练习代码
- [ ] 1个综合项目
- [ ] 学习笔记
- [ ] 分析 Kimi CLI 异步架构

---

## 🔍 深入理解 Kimi CLI 异步架构

### Kimi CLI 异步流程分析

```python
# 1. 入口：cli.py
def kimi(...):
    async def _run() -> bool:
        # 异步创建实例
        instance = await KimiCLI.create(...)
        # 异步运行模式
        return await instance.run_shell_mode(command)

    # 启动事件循环
    asyncio.run(_run())

# 2. 应用层：app.py
class KimiCLI:
    async def run_shell_mode(self, command: str | None = None) -> bool:
        app = ShellApp(self._soul, ...)
        # 异步运行 Shell
        return await app.run(command)

# 3. Soul层：soul/kimisoul.py
class KimiSoul:
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        # 异步调用 LLM
        async for chunk in self._llm.astream_chat(messages):
            yield chunk  # 流式返回

# 4. UI层：ui/shell/app.py
class ShellApp:
    async def _display_response_stream(self, stream: AsyncIterator[str]):
        # 异步显示流式响应
        async for chunk in stream:
            print(chunk, end='', flush=True)
```

**关键点**:
- ✅ 全异步架构
- ✅ 流式响应（实时显示）
- ✅ 高效并发（工具调用）
- ✅ 非阻塞 I/O

---

## 🔄 下一步

完成本模块后，进入 **阶段2: CLI开发** → **模块03: Click框架**。

---

*Created by 老王 | Last Updated: 2025-01-10*
