#!/usr/bin/env python3
"""
事件循环深度解析 - 手写简化版事件循环
作者：老王
目的：理解 asyncio 事件循环的工作原理
"""

import time
from collections import deque
from typing import Generator, Any


# ============================================================
# 手写简化版协程和事件循环
# ============================================================

class Task:
    """任务包装器（简化版）"""

    def __init__(self, coro, task_id):
        self.coro = coro  # 协程对象
        self.task_id = task_id
        self.done = False
        self.result = None

    def __repr__(self):
        status = "完成" if self.done else "运行中"
        return f"<Task {self.task_id} {status}>"


class SimpleEventLoop:
    """简化版事件循环 - 帮助理解原理"""

    def __init__(self):
        self.ready_queue = deque()  # 就绪队列
        self.sleeping_tasks = []    # 睡眠任务列表
        self.task_id_counter = 0

    def create_task(self, coro) -> Task:
        """创建任务并加入就绪队列"""
        self.task_id_counter += 1
        task = Task(coro, self.task_id_counter)
        self.ready_queue.append(task)
        print(f"  [事件循环] 创建任务 {task}")
        return task

    def sleep(self, delay: float) -> Generator[float, None, None]:
        """模拟 asyncio.sleep - 返回一个生成器"""
        # 生成器会被事件循环识别为"需要等待"
        yield delay  # 告诉事件循环："我要睡 delay 秒"

    def run_until_complete(self, main_coro):
        """运行主协程直到完成"""
        print(f"[事件循环] 启动，主协程：{main_coro}")

        # 创建主任务
        main_task = self.create_task(main_coro)

        # 主循环
        while self.ready_queue or self.sleeping_tasks:
            # 1. 检查睡眠任务是否到期
            self._wake_up_sleeping_tasks()

            # 2. 如果没有就绪任务，等待一小段时间
            if not self.ready_queue:
                time.sleep(0.01)  # 短暂休眠，避免忙等待
                continue

            # 3. 取出一个就绪任务
            task = self.ready_queue.popleft()

            print(f"  [事件循环] 调度任务 {task}")

            try:
                # 4. 执行任务到下一个 yield/await
                delay = task.coro.send(None)

                # 5. 如果任务返回了延迟，加入睡眠队列
                if isinstance(delay, (int, float)) and delay > 0:
                    wake_time = time.time() + delay
                    self.sleeping_tasks.append((wake_time, task))
                    print(f"    └─ 任务 {task.task_id} 睡眠 {delay}秒")
                else:
                    # 否则重新加入就绪队列
                    self.ready_queue.append(task)

            except StopIteration as e:
                # 任务完成
                task.done = True
                task.result = e.value
                print(f"    └─ 任务 {task.task_id} 完成，结果：{task.result}")

        print(f"[事件循环] 所有任务完成")
        return main_task.result

    def _wake_up_sleeping_tasks(self):
        """唤醒到期的睡眠任务"""
        current_time = time.time()
        still_sleeping = []

        for wake_time, task in self.sleeping_tasks:
            if current_time >= wake_time:
                # 时间到了，加入就绪队列
                self.ready_queue.append(task)
                print(f"  [事件循环] 唤醒任务 {task.task_id}")
            else:
                # 还没到时间，继续睡
                still_sleeping.append((wake_time, task))

        self.sleeping_tasks = still_sleeping


# ============================================================
# 使用简化版事件循环的示例
# ============================================================

def simple_coro(loop: SimpleEventLoop, name: str, delay: float):
    """简单协程 - 使用生成器实现"""
    print(f"    [{name}] 开始")

    print(f"    [{name}] 准备睡眠 {delay}秒")
    yield from loop.sleep(delay)  # 让出控制权

    print(f"    [{name}] 睡醒了")

    print(f"    [{name}] 再睡一会儿 0.5秒")
    yield from loop.sleep(0.5)

    print(f"    [{name}] 结束")
    return f"{name}的结果"


def test_simple_event_loop():
    """测试简化版事件循环"""
    print("\n" + "="*70)
    print("测试：手写简化版事件循环")
    print("="*70 + "\n")

    loop = SimpleEventLoop()

    # 创建主协程
    def main():
        # 创建3个子任务
        task1 = loop.create_task(simple_coro(loop, "任务A", 1.0))
        task2 = loop.create_task(simple_coro(loop, "任务B", 0.5))
        task3 = loop.create_task(simple_coro(loop, "任务C", 1.5))

        # 等待所有任务（简化版，只是 yield）
        yield from loop.sleep(0.1)

        print(f"\n  [主协程] 所有任务已创建")
        return "主任务完成"

    # 运行事件循环
    start_time = time.time()
    result = loop.run_until_complete(main())
    elapsed = time.time() - start_time

    print(f"\n结果：{result}")
    print(f"总耗时：{elapsed:.2f}秒")


# ============================================================
# 真实 asyncio 事件循环的内部机制
# ============================================================

import asyncio


async def real_coro(name: str, delay: float):
    """使用真实 asyncio 的协程"""
    print(f"    [{name}] 开始")
    await asyncio.sleep(delay)
    print(f"    [{name}] 完成")
    return f"{name}的结果"


async def inspect_event_loop():
    """检查真实事件循环的状态"""
    print("\n" + "="*70)
    print("测试：真实 asyncio 事件循环内部机制")
    print("="*70 + "\n")

    loop = asyncio.get_event_loop()

    print(f"当前事件循环：{loop}")
    print(f"是否正在运行：{loop.is_running()}")
    print(f"是否已关闭：{loop.is_closed()}")

    # 创建任务
    print("\n创建3个任务...")
    task1 = asyncio.create_task(real_coro("任务A", 1.0))
    task2 = asyncio.create_task(real_coro("任务B", 0.5))
    task3 = asyncio.create_task(real_coro("任务C", 1.5))

    print(f"任务1状态：{task1}")
    print(f"任务1是否完成：{task1.done()}")

    # 获取所有任务
    all_tasks = asyncio.all_tasks(loop)
    print(f"\n当前事件循环中的任务数量：{len(all_tasks)}")

    # 等待所有任务
    print("\n等待所有任务完成...")
    await asyncio.gather(task1, task2, task3)

    print(f"\n任务1状态：{task1}")
    print(f"任务1是否完成：{task1.done()}")
    print(f"任务1结果：{task1.result()}")


# ============================================================
# 事件循环的底层：select/epoll
# ============================================================

async def explain_io_multiplexing():
    """解释IO多路复用"""
    print("\n" + "="*70)
    print("概念：事件循环的底层 - IO多路复用")
    print("="*70 + "\n")

    explanation = """
事件循环的底层原理：IO多路复用

1. select/poll/epoll（Linux）或 kqueue（BSD/macOS）
   - 操作系统提供的系统调用
   - 可以同时监控多个文件描述符（socket、文件等）
   - 当某个IO就绪时，通知事件循环

2. asyncio 的工作流程：

   a) 注册IO事件：
      socket.connect()  →  注册"连接就绪"事件到 epoll

   b) 事件循环等待：
      epoll.poll(timeout)  →  阻塞等待，直到有事件就绪

   c) 处理就绪事件：
      for event in ready_events:
          callback = event.callback
          callback()  →  恢复对应的协程

   d) 继续循环

3. 为什么高效？

   单线程 + IO多路复用 = 高并发
   - 不需要为每个连接创建线程
   - 操作系统帮我们监控所有IO
   - 只在IO就绪时才执行，不浪费CPU

4. 真实例子：

   1000个HTTP请求（每个5秒）：
   - 多线程方案：1000个线程 × 每个1MB栈 = 1GB内存！
   - 异步方案：1个线程 + 1000个协程 ≈ 几MB内存
                 ↓
              性能提升100倍！
    """

    print(explanation)


# ============================================================
# 可视化事件循环
# ============================================================

async def visualize_event_loop():
    """可视化展示事件循环的工作过程"""
    print("\n" + "="*70)
    print("可视化：事件循环的工作流程")
    print("="*70 + "\n")

    async def task(name, steps):
        for step in range(steps):
            print(f"  [{name}] 步骤 {step + 1}/{steps}")
            await asyncio.sleep(0.3)
        return f"{name}完成"

    print("开始执行3个任务...")
    print("注意观察任务交替执行的过程：\n")

    start = time.time()
    results = await asyncio.gather(
        task("任务A", 3),
        task("任务B", 2),
        task("任务C", 4)
    )
    elapsed = time.time() - start

    print(f"\n所有任务完成！")
    print(f"结果：{results}")
    print(f"总耗时：{elapsed:.2f}秒")
    print(f"\n如果是串行执行，需要：(3+2+4) × 0.3 = 2.7秒")
    print(f"但异步执行只需要：max(3,2,4) × 0.3 = 1.2秒")


# ============================================================
# 主函数
# ============================================================

async def main():
    """主函数"""
    print("🔥 事件循环深度解析")
    print("作者：老王\n")

    # 测试1：简化版事件循环
    test_simple_event_loop()

    # 测试2：真实事件循环
    await inspect_event_loop()

    # 测试3：IO多路复用原理
    await explain_io_multiplexing()

    # 测试4：可视化
    await visualize_event_loop()

    print("\n" + "="*70)
    print("✅ 所有测试完成！")
    print("\n核心要点：")
    print("  1. 事件循环维护任务队列")
    print("  2. 任务遇到 await 就让出控制权")
    print("  3. IO就绪时恢复对应任务")
    print("  4. 单线程 + IO多路复用 = 高并发")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())