#!/usr/bin/env python3
"""
异步编程实战技巧与陷阱
作者：老王
目的：避开常见坑，掌握最佳实践
"""

import asyncio
import aiohttp
import time
from typing import List


# ============================================================
# 陷阱1：在 async 函数中使用同步阻塞操作
# ============================================================

async def trap_1_blocking_in_async():
    """陷阱1：阻塞事件循环"""
    print("\n" + "="*70)
    print("陷阱1：在 async 函数中使用同步阻塞操作")
    print("="*70 + "\n")

    # ❌ 错误示范
    async def bad_sleep():
        print("  [错误] 使用 time.sleep(2) - 这会阻塞整个事件循环！")
        time.sleep(2)  # 💀 整个事件循环被冻结2秒
        return "bad"

    # ✅ 正确方式
    async def good_sleep():
        print("  [正确] 使用 await asyncio.sleep(2) - 让出控制权")
        await asyncio.sleep(2)  # ✨ 只暂停当前协程，不阻塞事件循环
        return "good"

    print("并发执行错误和正确的方式...\n")

    start = time.time()

    # 同时执行多个任务
    task1 = asyncio.create_task(bad_sleep())
    task2 = asyncio.create_task(asyncio.sleep(1))  # 这个任务会被 bad_sleep 阻塞

    await task1
    await task2

    print(f"\n耗时：{time.time() - start:.2f}秒")
    print("⚠️ 注意：time.sleep(2) 阻塞了整个事件循环，导致第二个任务也被延迟\n")


# ============================================================
# 陷阱2：忘记 await
# ============================================================

async def trap_2_forget_await():
    """陷阱2：忘记 await"""
    print("\n" + "="*70)
    print("陷阱2：忘记 await")
    print("="*70 + "\n")

    async def fetch_data():
        await asyncio.sleep(1)
        return "数据"

    # ❌ 错误1：忘记 await
    print("❌ 错误示范1：忘记 await")
    result = fetch_data()  # 这只是创建了协程对象，没有执行！
    print(f"  结果类型：{type(result)}")
    print(f"  结果值：{result}")
    print("  ⚠️ 没有真正执行，拿不到数据！\n")

    # ❌ 错误2：忘记 await 导致警告
    print("❌ 错误示范2：协程未被等待会产生警告")
    fetch_data()  # RuntimeWarning: coroutine 'fetch_data' was never awaited
    await asyncio.sleep(0.1)  # 给警告时间显示
    print()

    # ✅ 正确方式
    print("✅ 正确方式：使用 await")
    result = await fetch_data()
    print(f"  结果类型：{type(result)}")
    print(f"  结果值：{result}\n")


# ============================================================
# 陷阱3：错误的异常处理
# ============================================================

async def trap_3_exception_handling():
    """陷阱3：异常处理"""
    print("\n" + "="*70)
    print("陷阱3：异常处理")
    print("="*70 + "\n")

    async def task_may_fail(task_id, will_fail=False):
        await asyncio.sleep(0.5)
        if will_fail:
            raise ValueError(f"任务{task_id}失败了！")
        return f"任务{task_id}成功"

    # ❌ 错误：gather 遇到异常会立即抛出
    print("❌ 方式1：gather 默认行为 - 一个失败全部终止")
    try:
        results = await asyncio.gather(
            task_may_fail(1, False),
            task_may_fail(2, True),   # 这个会失败
            task_may_fail(3, False),
        )
    except ValueError as e:
        print(f"  捕获异常：{e}")
        print("  ⚠️ 其他任务也被取消了！\n")

    # ✅ 正确：使用 return_exceptions=True
    print("✅ 方式2：gather 使用 return_exceptions=True")
    results = await asyncio.gather(
        task_may_fail(1, False),
        task_may_fail(2, True),
        task_may_fail(3, False),
        return_exceptions=True  # 不抛出异常，而是返回
    )
    print(f"  结果：{results}")
    print("  ✅ 所有任务都执行完毕，失败的任务返回异常对象\n")

    # ✅ 正确：单独处理每个任务
    print("✅ 方式3：单独捕获每个任务的异常")

    async def safe_task(task_id, will_fail):
        try:
            return await task_may_fail(task_id, will_fail)
        except ValueError as e:
            return f"任务{task_id}失败: {e}"

    results = await asyncio.gather(
        safe_task(1, False),
        safe_task(2, True),
        safe_task(3, False),
    )
    print(f"  结果：{results}\n")


# ============================================================
# 陷阱4：超时处理不当
# ============================================================

async def trap_4_timeout():
    """陷阱4：超时处理"""
    print("\n" + "="*70)
    print("陷阱4：超时处理")
    print("="*70 + "\n")

    async def slow_operation():
        print("  慢操作开始...")
        await asyncio.sleep(5)
        print("  慢操作完成")
        return "结果"

    # ❌ 错误：没有超时控制
    print("❌ 错误方式：没有超时控制")
    print("  （如果不注释，这里会等5秒）")
    # await slow_operation()

    # ✅ 正确：使用 wait_for
    print("\n✅ 正确方式：使用 wait_for 设置超时")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(f"  结果：{result}")
    except asyncio.TimeoutError:
        print("  ⏰ 操作超时！")
        print("  ✅ 超时后任务会被自动取消\n")


# ============================================================
# 陷阱5：并发数过高
# ============================================================

async def trap_5_too_many_concurrency():
    """陷阱5：并发数过高"""
    print("\n" + "="*70)
    print("陷阱5：并发数过高")
    print("="*70 + "\n")

    async def fetch(url_id):
        await asyncio.sleep(0.1)  # 模拟网络请求
        return f"结果{url_id}"

    # ❌ 错误：无限制并发
    print("❌ 错误方式：同时发起1000个请求")
    print("  问题：可能耗尽文件描述符、内存、服务器拒绝连接")
    # urls = range(1000)
    # results = await asyncio.gather(*[fetch(i) for i in urls])

    # ✅ 正确：使用信号量限制并发
    print("\n✅ 正确方式：使用信号量限制最大并发数")

    async def fetch_with_semaphore(semaphore, url_id):
        async with semaphore:  # 获取信号量（最多N个同时执行)
            print(f"  开始请求 {url_id}")
            result = await fetch(url_id)
            print(f"  完成请求 {url_id}")
            return result

    # 限制最多同时执行5个
    semaphore = asyncio.Semaphore(5)
    urls = range(20)

    start = time.time()
    results = await asyncio.gather(*[
        fetch_with_semaphore(semaphore, i) for i in urls
    ])
    elapsed = time.time() - start

    print(f"\n  完成20个请求，耗时：{elapsed:.2f}秒")
    print(f"  理论耗时：20 / 5 * 0.1 = 0.4秒")
    print(f"  ✅ 通过信号量控制并发数，避免资源耗尽\n")


# ============================================================
# 技巧1：重试机制
# ============================================================

async def skill_1_retry():
    """技巧1：重试机制"""
    print("\n" + "="*70)
    print("技巧1：重试机制")
    print("="*70 + "\n")

    attempt_count = 0

    async def flaky_operation():
        """不稳定的操作（前2次失败）"""
        nonlocal attempt_count
        attempt_count += 1
        print(f"  尝试第 {attempt_count} 次...")

        if attempt_count < 3:
            raise ConnectionError("连接失败")

        return "成功！"

    # 重试装饰器
    async def retry(func, max_attempts=3, delay=1.0):
        """重试装饰器"""
        for attempt in range(1, max_attempts + 1):
            try:
                return await func()
            except Exception as e:
                if attempt == max_attempts:
                    print(f"  ❌ 重试{max_attempts}次后仍失败")
                    raise
                print(f"  ⚠️ 第{attempt}次失败：{e}")
                print(f"  等待 {delay}秒 后重试...")
                await asyncio.sleep(delay)

    result = await retry(flaky_operation, max_attempts=5, delay=0.5)
    print(f"  ✅ 最终结果：{result}\n")


# ============================================================
# 技巧2：进度追踪
# ============================================================

async def skill_2_progress_tracking():
    """技巧2：进度追踪"""
    print("\n" + "="*70)
    print("技巧2：进度追踪")
    print("="*70 + "\n")

    async def download_file(file_id, total_chunks=5):
        """模拟文件下载"""
        for chunk in range(total_chunks):
            await asyncio.sleep(0.2)
            progress = (chunk + 1) / total_chunks * 100
            yield file_id, chunk + 1, total_chunks, progress

    async def download_with_progress(file_ids):
        """带进度的批量下载"""
        print("开始下载...\n")

        async def download_one(file_id):
            async for fid, current, total, progress in download_file(file_id):
                print(f"  [文件{fid}] {current}/{total} ({progress:.0f}%)")

        await asyncio.gather(*[download_one(fid) for fid in file_ids])
        print("\n所有文件下载完成！")

    await download_with_progress([1, 2, 3])


# ============================================================
# 技巧3：优雅关闭
# ============================================================

async def skill_3_graceful_shutdown():
    """技巧3：优雅关闭"""
    print("\n" + "="*70)
    print("技巧3：优雅关闭")
    print("="*70 + "\n")

    async def background_task(name):
        """后台任务"""
        try:
            while True:
                print(f"  [{name}] 运行中...")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print(f"  [{name}] 收到取消信号，正在清理...")
            await asyncio.sleep(0.5)  # 模拟清理工作
            print(f"  [{name}] 已优雅退出")
            raise  # 重新抛出，让调用者知道任务已取消

    # 启动后台任务
    task1 = asyncio.create_task(background_task("任务A"))
    task2 = asyncio.create_task(background_task("任务B"))

    # 运行2秒
    await asyncio.sleep(2)

    print("\n主程序准备退出，取消后台任务...\n")

    # 取消任务
    task1.cancel()
    task2.cancel()

    # 等待任务完成清理
    try:
        await asyncio.gather(task1, task2)
    except asyncio.CancelledError:
        print("\n✅ 所有任务已优雅关闭\n")


# ============================================================
# 技巧4：使用 asyncio.as_completed 优化
# ============================================================

async def skill_4_as_completed():
    """技巧4：使用 as_completed 尽早处理结果"""
    print("\n" + "="*70)
    print("技巧4：使用 as_completed 尽早处理结果")
    print("="*70 + "\n")

    async def fetch(url_id, delay):
        await asyncio.sleep(delay)
        return f"URL{url_id}"

    urls = [(1, 2), (2, 1), (3, 3), (4, 0.5)]

    # ❌ gather：等所有完成才返回
    print("❌ 使用 gather（等所有任务完成）：")
    start = time.time()
    results = await asyncio.gather(*[fetch(uid, delay) for uid, delay in urls])
    print(f"  所有结果：{results}")
    print(f"  耗时：{time.time() - start:.2f}秒\n")

    # ✅ as_completed：谁先完成先处理谁
    print("✅ 使用 as_completed（先完成先处理）：")
    start = time.time()
    tasks = [fetch(uid, delay) for uid, delay in urls]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        elapsed = time.time() - start
        print(f"  [{elapsed:.1f}秒] 完成：{result}")

    print(f"\n  ✅ 可以边下载边处理，提升用户体验\n")


# ============================================================
# 主函数
# ============================================================

async def main():
    """主函数"""
    print("🔥 异步编程实战技巧与陷阱")
    print("作者：老王\n")

    # 陷阱
    await trap_1_blocking_in_async()
    await trap_2_forget_await()
    await trap_3_exception_handling()
    await trap_4_timeout()
    await trap_5_too_many_concurrency()

    # 技巧
    await skill_1_retry()
    await skill_2_progress_tracking()
    await skill_3_graceful_shutdown()
    await skill_4_as_completed()

    print("="*70)
    print("✅ 所有示例完成！")
    print("\n老王总结：")
    print("  1. 永远不要在 async 函数中用 time.sleep")
    print("  2. 别忘了 await，否则协程不会执行")
    print("  3. 用 return_exceptions=True 避免一个失败全军覆没")
    print("  4. 用 wait_for 设置超时，避免永久等待")
    print("  5. 用 Semaphore 限制并发数，避免资源耗尽")
    print("  6. 重试、进度追踪、优雅关闭都是生产环境必备")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())