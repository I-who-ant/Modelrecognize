# 🚀 异步编程代码实践 - 学习指南

> **作者**：老王
> **目标**：通过实战代码搞懂 Python 异步编程的本质和应用

---

## 📚 学习路径

### 1️⃣ 必读文档
**[深度理解async异步编程.md](./深度理解async异步编程.md)**

这是老王我花了心思写的深度解析文档，涵盖了：

- ✅ **核心概念**：async ≠ 多线程！
- ✅ **本质理解**：同步阻塞 vs 多线程 vs 异步协程
- ✅ **事件循环原理**：协程如何在单线程中协作调度
- ✅ **常见陷阱**：忘记 await、阻塞操作、死锁等
- ✅ **实用技巧**：超时控制、并发限制、重试机制
- ✅ **最佳实践**：KISS、YAGNI、DRY原则在异步编程中的应用

**建议**：先通读这个文档，理解概念后再运行代码！

---

### 2️⃣ 代码实践（按顺序运行）

#### **01_同步vs异步对比.py** - 入门必看
**核心问题**：异步到底比同步快多少?

```bash
python 01_同步vs异步对比.py
```

**你将看到**：
- ⏱️ **测试1&2**：睡眠对比（同步6秒 vs 异步3秒）
- 🌐 **测试3&4**：HTTP请求对比（同步4秒 vs 异步2秒）
- 🎯 **测试5**：`create_task` 的正确用法（"启动后不管"）
- ❌ **测试6**：常见错误示范（忘记 await）

**关键结论**：
- 异步在IO等待场景下性能提升 **2-10倍**
- 并发数越多，提升越明显
- 单线程即可实现高并发

---

#### **02_事件循环原理.py** - 深入理解
**核心问题**：事件循环到底是怎么工作的？

```bash
python 02_事件循环原理.py
```

**你将学到**：
- 🔧 **手写简化版事件循环**：理解任务调度原理
- 🔍 **检查真实事件循环状态**：all_tasks、is_running 等
- 💡 **IO多路复用原理**：select/epoll 是什么
- 📊 **可视化展示**：观察任务交替执行的过程

**关键结论**：
- 事件循环维护任务队列，轮流执行
- 遇到 await 就让出控制权，切换到下一个任务
- IO就绪时恢复对应任务
- 底层依赖 select/epoll 实现高效IO监控

---

#### **03_实战技巧与陷阱.py** - 避坑指南
**核心问题**：生产环境中如何避开常见陷阱？

```bash
python 03_实战技巧与陷阱.py
```

**陷阱警示**：
- 💀 **陷阱1**：在 async 中用 `time.sleep` 阻塞事件循环
- 🤦 **陷阱2**：忘记 await 导致协程不执行
- 💥 **陷阱3**：异常处理不当导致全部失败
- ⏰ **陷阱4**：没有超时控制导致永久等待
- 🔥 **陷阱5**：并发数过高耗尽资源

**实战技巧**：
- ✅ **技巧1**：重试机制（指数退避）
- ✅ **技巧2**：进度追踪（实时反馈）
- ✅ **技巧3**：优雅关闭（CancelledError 处理）
- ✅ **技巧4**：`as_completed` 尽早处理结果

---

#### **04_终极对比.py** - 决策指南
**核心问题**：什么时候用异步？什么时候用多线程？

```bash
python 04_终极对比.py
```

**对比维度**：
- 🌐 **IO密集型**：网络请求（同步 vs 多线程 vs 异步）
- 💻 **CPU密集型**：计算质数（同步 vs 多线程 vs 异步 vs 多进程）
- 📊 **资源占用**：内存、CPU、并发数对比
- 🎯 **决策树**：如何选择合适的并发方式

**关键结论**：
- IO密集型 → **异步协程**（高并发、低资源）
- CPU密集型 → **多进程**（真正并行、避开GIL）
- 混合场景 → **异步 + run_in_executor(ProcessPoolExecutor)**
- 简单脚本 → **同步**（别过度设计）

---

## 🎯 快速答疑（你最关心的问题）

### Q1: async 函数会创建新线程吗？
**答**：❌ **不会！** async 函数只是标记这是一个**协程函数**，所有协程都在**同一个线程**中运行。

```python
# 证明代码
import asyncio
import threading

async def test():
    print(f"运行在线程：{threading.current_thread().name}")

asyncio.run(test())  # 输出：MainThread
```

---

### Q2: await 是等待吗？可以不管它继续执行吗？
**答**：是，也不是！

- `await` **会暂停当前协程**，等待被等待的协程完成
- **但不会阻塞整个线程**！事件循环可以调度其他协程
- **不能不管它继续执行**，如果想"启动后不管"，应该用 `asyncio.create_task()`

```python
# ❌ 错误：await 会等待
async def wrong():
    await slow_task()  # 这里会等3秒
    print("继续")       # 3秒后才执行

# ✅ 正确：create_task "启动后不管"
async def right():
    task = asyncio.create_task(slow_task())  # 立即返回
    print("继续")  # 立即执行
    # ... 做其他事情
    await task  # 需要的时候再等待结果
```

---

### Q3: 什么时候该用异步？什么时候该用多线程？

**老王的经验法则**：

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 🌐 网络请求（爬虫、API调用） | **异步协程** | 高并发、低资源、无GIL |
| 📁 文件读写（大文件、批量IO） | **异步协程** | IO等待时可处理其他任务 |
| 🗄️ 数据库查询（高并发访问） | **异步协程** | 单线程轻松支持数千连接 |
| 💻 数据计算（加密、哈希） | **多进程** | 真正并行、避开GIL |
| 🖼️ 图像处理（批量转换） | **多进程** | CPU密集型，需要真正并行 |
| 🔢 科学计算（NumPy、机器学习） | **多进程** | 利用多核CPU |
| 📝 简单脚本（低并发） | **同步代码** | 简单就是美，别过度设计 |

---

## 💡 老王的金玉良言

1. **异步不是多线程**：协程在单线程中协作调度，不创建新线程
2. **await 必须等待**：不能跳过 await 继续执行，除非用 `create_task()`
3. **适用于 IO 密集型**：网络、文件、数据库等有大量等待的场景
4. **避免阻塞操作**：async 函数中不能使用同步阻塞调用（如 `time.sleep`、`requests.get`）
5. **理解事件循环**：所有协程在一个事件循环中轮流执行
6. **性能提升显著**：IO密集型任务可提升 **10-100倍** 效率
7. **工具选择**：优先使用异步库（`aiohttp` > `requests`，`aiofiles` > `open`）
8. **并发控制**：用 `Semaphore` 限制并发数，避免资源耗尽
9. **异常处理**：用 `return_exceptions=True` 避免一个失败全军覆没
10. **超时保护**：用 `asyncio.wait_for()` 设置超时，避免永久等待

---

## 📖 推荐学习资源

### 官方文档
- [Python asyncio 官方文档](https://docs.python.org/zh-cn/3/library/asyncio.html)
- [aiohttp 文档](https://docs.aiohttp.org/)
- [aiofiles 文档](https://github.com/Tinche/aiofiles)

### 进阶阅读
- [Trio：更友好的异步框架](https://trio.readthedocs.io/)
- [uvloop：更快的事件循环](https://github.com/MagicStack/uvloop)
- [FastAPI：基于异步的Web框架](https://fastapi.tiangolo.com/)

---

## 🎓 学习建议

### 阶段1：理解概念（1天）
1. 通读 `深度理解async异步编程.md`
2. 理解核心概念：协程、事件循环、await
3. 明确异步 ≠ 多线程

### 阶段2：运行示例（1天）
1. 按顺序运行 4 个代码文件
2. 观察输出，理解执行流程
3. 修改参数，观察行为变化

### 阶段3：实战练习（3-5天）
1. 写一个异步爬虫（10个网页）
2. 实现带进度条的批量下载
3. 尝试异步数据库查询（用 `aiosqlite`）
4. 对比同步和异步的性能差异

### 阶段4：进阶应用（持续）
1. 学习 FastAPI 构建异步Web API
2. 研究 WebSocket 长连接
3. 了解异步上下文管理器（`async with`）
4. 探索异步生成器（`async for`）

---

## ⚡ 快速参考

### 常用API

```python
# 运行异步主函数
asyncio.run(main())

# 创建任务（启动后不等待）
task = asyncio.create_task(coro())

# 并发执行多个协程
results = await asyncio.gather(coro1(), coro2(), coro3())

# 超时控制
result = await asyncio.wait_for(coro(), timeout=5.0)

# 休眠（不阻塞事件循环）
await asyncio.sleep(1.0)

# 并发限制
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await do_something()

# 在线程池中运行同步函数
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(None, sync_func, arg)
```

---

## 🔧 常见问题排查

### 问题1：RuntimeWarning: coroutine was never awaited
**原因**：创建了协程对象但没有 await

```python
# ❌ 错误
async_func()  # 只是创建了协程对象

# ✅ 正确
await async_func()  # 真正执行
```

---

### 问题2：asyncio.run() cannot be called from a running event loop
**原因**：在已运行的事件循环中调用 `asyncio.run()`

```python
# ❌ 错误（在 async 函数中）
async def wrong():
    asyncio.run(other_coro())  # 已经在事件循环中了

# ✅ 正确
async def right():
    await other_coro()  # 直接 await
```

---

### 问题3：程序卡住不动
**可能原因**：
1. 使用了同步阻塞调用（如 `time.sleep`、`requests.get`）
2. 忘记 await
3. 死锁（循环依赖）

**排查方法**：
1. 检查是否使用了同步库
2. 确保所有协程都被 await
3. 检查任务依赖关系

---

## 🎉 完成学习后你将掌握

- ✅ 理解异步编程的本质和原理
- ✅ 知道何时使用异步、何时使用多线程
- ✅ 能够编写高性能的异步代码
- ✅ 避开常见陷阱，遵循最佳实践
- ✅ 独立完成异步项目开发

---

**老王寄语**：

异步编程一开始确实烧脑，但理解本质后你会发现这是处理并发的利器！

记住：**异步不是魔法，它只是在单线程中更聪明地利用等待时间**。

多写多练，很快就能得心应手！💪

有问题随时来找老王，咱们一起把这玩意儿搞透！🔥

---

**最后更新**：2025-01-10
**作者**：老王（暴躁技术流）