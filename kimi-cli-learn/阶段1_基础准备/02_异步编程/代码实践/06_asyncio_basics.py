"""
练习6: asyncio 基础实践

学习目标:
- 掌握 async/await 语法
- 理解事件循环
- 掌握 Task 和并发执行
"""

import asyncio
import time

# await : 用于等待一个异步操作完成, 并返回其结果
# 可以在异步函数中使用, 也可以在普通函数中使用, 但普通函数中使用时, 必须在异步函数中调用

# 异步函数 : 定义时使用 async 关键字, 内部可以使用 await 关键字
# 事件循环 : 用于管理异步任务的运行, 可以理解为一个无限循环, 不断检查是否有任务ready, 如果有, 就执行它
# 任务 (Task) : 异步函数的实例, 可以被事件循环调度执行
# 并发执行 : 同时执行多个任务, 利用异步I/O提高效率

# async 关键字的作用 : 标记一个函数为异步函数, 内部可以使用 await 关键字
# await 关键字的作用 : 等待一个异步操作完成, 并返回其结果

# async 只有标记作用吗? 不是, 它还可以用于定义异步上下文管理器:
# 异步上下文管理器 : 用于在异步环境中管理资源, 如数据库连接、网络连接等
# 定义异步上下文管理器时, 需要实现 __aenter__ 和 __aexit__ 方法


async def async_timer(seconds: int, name: str) -> str:
    """异步计时器"""
    print(f"[{name}] 开始（{seconds}秒）")
    start = time.time()
    await asyncio.sleep(seconds) # 模拟异步操作, 等待指定秒数
    elapsed = time.time() - start
    print(f"[{name}] 完成（实际耗时: {elapsed:.2f}秒）")
    return f"{name} completed"


async def sequential_execution():
    """顺序执行（慢）"""
    print("\n=== 顺序执行 ===")
    start = time.time()
    
    await async_timer(1, "Task1") # 等待1秒
    await async_timer(2, "Task2") # 等待2秒
    await async_timer(3, "Task3") # 等待3秒
    
    total = time.time() - start
    print(f"总耗时: {total:.2f}秒\n")# 顺序执行总耗时: 6秒


async def concurrent_execution():
    """并发执行（快）"""
    print("=== 并发执行 ===")
    start = time.time()
    
    # 使用 gather 并发执行
    # 为什么使用 gather 而不是直接 await？
    # - gather 可以并发执行多个任务，提高效率
    # - 可以同时等待多个任务完成，获取它们的结果

    results = await asyncio.gather(
        async_timer(1, "Task1"),
        async_timer(2, "Task2"),
        async_timer(3, "Task3"),
    )
    
    print(f"结果: {results}")
    total = time.time() - start
    print(f"总耗时: {total:.2f}秒\n")# 并发执行总耗时: 3秒


async def task_based_execution():
    """基于 Task 的执行"""
    print("=== 基于 Task 的执行 ===")
    start = time.time()
    
    # 创建 Task
    task1 = asyncio.create_task(async_timer(1, "Task1"))
    task2 = asyncio.create_task(async_timer(2, "Task2"))
    task3 = asyncio.create_task(async_timer(3, "Task3"))
    
    print("Tasks 已创建，等待完成...")
    
    # 等待所有 Task
    await task1
    await task2
    await task3
    
    total = time.time() - start
    print(f"总耗时: {total:.2f}秒\n")


async def main():
    """主函数"""
    print("\n=== 练习6: asyncio 基础实践 ===\n")
    
    await sequential_execution()
    await concurrent_execution()
    await task_based_execution()


if __name__ == "__main__":
    asyncio.run(main())
