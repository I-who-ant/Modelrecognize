#!/usr/bin/env python3
"""
异步编程终极对比：同步 vs 多线程 vs 异步
作者：老王
目的：一次性搞清楚三者的区别和适用场景
"""

import asyncio
import aiohttp
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List


# ============================================================
# 场景：下载多个网页内容
# ============================================================

URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]


# ------------------------------------------------------------
# 方式1：同步串行（最慢）
# ------------------------------------------------------------

def sync_download(urls: List[str]):
    """同步串行下载"""
    print("\n" + "="*70)
    print("方式1：同步串行下载（最慢）")
    print("="*70 + "\n")

    results = []
    start = time.time()

    for i, url in enumerate(urls, 1):
        print(f"  [同步] 开始下载 {i}/{len(urls)}: {url}")
        try:
            response = requests.get(url, timeout=10)
            results.append(response.status_code)
            print(f"  [同步] 完成下载 {i}/{len(urls)} (状态: {response.status_code})")
        except Exception as e:
            print(f"  [同步] 下载失败 {i}: {e}")
            results.append(None)

    elapsed = time.time() - start

    print(f"\n结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"特点：")
    print(f"  ✅ 代码简单，易于理解")
    print(f"  ❌ 速度最慢，一个一个下载")
    print(f"  ❌ 线程被阻塞，无法做其他事")

    return results, elapsed


# ------------------------------------------------------------
# 方式2：多线程并发
# ------------------------------------------------------------

def threaded_download(urls: List[str]):
    """多线程并发下载"""
    print("\n" + "="*70)
    print("方式2：多线程并发下载")
    print("="*70 + "\n")

    results = []
    start = time.time()

    def download_one(url, index):
        """单个下载任务"""
        thread_name = threading.current_thread().name
        print(f"  [线程{thread_name}] 开始下载 {index}/{len(urls)}: {url}")
        try:
            response = requests.get(url, timeout=10)
            print(f"  [线程{thread_name}] 完成下载 {index} (状态: {response.status_code})")
            return response.status_code
        except Exception as e:
            print(f"  [线程{thread_name}] 下载失败 {index}: {e}")
            return None

    # 使用线程池
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(download_one, url, i)
            for i, url in enumerate(urls, 1)
        ]
        results = [future.result() for future in futures]

    elapsed = time.time() - start

    print(f"\n结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"特点：")
    print(f"  ✅ 速度快，真正的并行执行")
    print(f"  ✅ 适合CPU密集型任务")
    print(f"  ⚠️ 线程创建有开销（每个线程约1MB栈）")
    print(f"  ⚠️ 受GIL限制（Python特有问题）")
    print(f"  ⚠️ 线程安全问题需要加锁")

    return results, elapsed


# ------------------------------------------------------------
# 方式3：异步协程（推荐用于IO密集型）
# ------------------------------------------------------------

async def async_download(urls: List[str]):
    """异步协程下载"""
    print("\n" + "="*70)
    print("方式3：异步协程下载（IO密集型推荐）")
    print("="*70 + "\n")

    results = []
    start = time.time()

    async def download_one(session, url, index):
        """单个下载任务"""
        print(f"  [协程] 开始下载 {index}/{len(urls)}: {url}")
        try:
            async with session.get(url, timeout=10) as response:
                status = response.status
                print(f"  [协程] 完成下载 {index} (状态: {status})")
                return status
        except Exception as e:
            print(f"  [协程] 下载失败 {index}: {e}")
            return None

    # 使用单个会话并发下载
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_one(session, url, i)
            for i, url in enumerate(urls, 1)
        ]
        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"\n结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"特点：")
    print(f"  ✅ 速度快，接近多线程")
    print(f"  ✅ 资源占用少（单线程，协程只是函数）")
    print(f"  ✅ 没有GIL问题")
    print(f"  ✅ 没有线程安全问题")
    print(f"  ✅ 适合IO密集型（网络、文件、数据库）")
    print(f"  ⚠️ 需要异步库支持（aiohttp、aiofiles等）")
    print(f"  ⚠️ 代码稍复杂（需要理解async/await）")

    return results, elapsed


# ============================================================
# CPU密集型任务对比
# ============================================================

def cpu_bound_task(n):
    """CPU密集型任务：计算质数"""
    count = 0
    for i in range(2, n):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


def sync_cpu_bound():
    """同步执行CPU密集型任务"""
    print("\n" + "="*70)
    print("CPU密集型任务：同步执行")
    print("="*70 + "\n")

    numbers = [50000, 50000, 50000, 50000]
    start = time.time()

    results = [cpu_bound_task(n) for n in numbers]

    elapsed = time.time() - start
    print(f"结果：{results}")
    print(f"耗时：{elapsed:.2f}秒\n")
    return elapsed


def threaded_cpu_bound():
    """多线程执行CPU密集型任务"""
    print("\n" + "="*70)
    print("CPU密集型任务：多线程执行")
    print("="*70 + "\n")

    numbers = [50000, 50000, 50000, 50000]
    start = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, numbers))

    elapsed = time.time() - start
    print(f"结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"⚠️ 注意：由于GIL锁，多线程对CPU密集型任务帮助不大！\n")
    return elapsed


async def async_cpu_bound():
    """异步执行CPU密集型任务（错误示范）"""
    print("\n" + "="*70)
    print("CPU密集型任务：异步执行（错误示范）")
    print("="*70 + "\n")

    async def async_cpu_task(n):
        """这样做是错误的！"""
        return cpu_bound_task(n)  # ❌ 这会阻塞事件循环

    numbers = [50000, 50000, 50000, 50000]
    start = time.time()

    results = await asyncio.gather(*[async_cpu_task(n) for n in numbers])

    elapsed = time.time() - start
    print(f"结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"❌ 异步对CPU密集型任务无效，甚至更慢（开销）\n")
    return elapsed


async def async_cpu_bound_correct():
    """异步中正确处理CPU密集型任务"""
    print("\n" + "="*70)
    print("CPU密集型任务：在异步中正确处理（使用进程池）")
    print("="*70 + "\n")

    from concurrent.futures import ProcessPoolExecutor

    numbers = [50000, 50000, 50000, 50000]
    start = time.time()

    loop = asyncio.get_event_loop()

    # 在进程池中执行（避开GIL）
    with ProcessPoolExecutor() as executor:
        results = await asyncio.gather(*[
            loop.run_in_executor(executor, cpu_bound_task, n)
            for n in numbers
        ])

    elapsed = time.time() - start
    print(f"结果：{results}")
    print(f"耗时：{elapsed:.2f}秒")
    print(f"✅ 使用进程池可以真正并行执行CPU任务\n")
    return elapsed


# ============================================================
# 资源占用对比
# ============================================================

def compare_resource_usage():
    """对比资源占用"""
    print("\n" + "="*70)
    print("资源占用对比")
    print("="*70 + "\n")

    comparison = """
假设场景：同时处理1000个网络请求

1. 同步方式：
   - 线程数：1
   - 内存：最少（约几MB）
   - 耗时：最长（1000 × 平均延迟）
   - 适用：简单脚本、顺序处理

2. 多线程方式：
   - 线程数：1000（或线程池大小）
   - 内存：大（每线程约1MB栈 = 1GB！）
   - 耗时：快（并行执行）
   - 适用：CPU密集型、阻塞IO
   - 问题：GIL限制、上下文切换开销

3. 异步协程方式：
   - 线程数：1
   - 内存：小（协程只是函数，1000个约几十MB）
   - 耗时：快（并发执行）
   - 适用：IO密集型（网络、文件、数据库）
   - 优势：高并发、低资源

对比表格：
┌─────────────┬──────────┬──────────┬──────────┐
│   指标      │ 同步     │ 多线程   │ 异步     │
├─────────────┼──────────┼──────────┼──────────┤
│ 并发数      │ 1        │ 受限     │ 高       │
│ 内存占用    │ 最小     │ 大       │ 小       │
│ CPU占用     │ 低       │ 高       │ 低       │
│ IO效率      │ 差       │ 好       │ 最好     │
│ CPU效率     │ 差       │ 一般     │ 差       │
│ 代码复杂度  │ 简单     │ 中等     │ 中等     │
│ GIL影响     │ 无       │ 严重     │ 无       │
└─────────────┴──────────┴──────────┴──────────┘
    """
    print(comparison)


# ============================================================
# 决策树：如何选择？
# ============================================================

def decision_tree():
    """决策树：选择合适的并发方式"""
    print("\n" + "="*70)
    print("决策树：如何选择合适的并发方式？")
    print("="*70 + "\n")

    tree = """
                开始
                 │
        ┌────────┴────────┐
        │                 │
    需要并发吗?         不需要
        │                 │
       是              ┌──┘
        │              │
        │           使用同步
        │           方式即可
        │
    ┌───┴───┐
    │       │
 IO密集   CPU密集
    │       │
    │       └─────────────────┐
    │                         │
 使用异步协程              使用多进程
 (asyncio)               (multiprocessing)
    │                         │
    │                         │
 优点：                    优点：
 - 高并发                  - 真正并行
 - 低资源                  - 避开GIL
 - 无GIL                   - 高性能
    │                         │
 适用：                    适用：
 - 网络请求                - 数据计算
 - 文件IO                  - 图像处理
 - 数据库查询              - 加密解密
 - WebSocket               - 科学计算


特殊情况：

1. 混合场景（既有IO又有CPU）：
   → 异步 + run_in_executor(ProcessPoolExecutor)
   → IO用协程，CPU用进程池

2. 需要共享状态：
   → 避免多线程（锁的复杂性）
   → 优先异步协程（天然线程安全）

3. 第三方库限制：
   → 如果库不支持异步（如requests）
   → 用 run_in_executor 包装同步调用
   → 或寻找异步替代品（如aiohttp）

4. 简单脚本：
   → 同步就够了，别过度设计
    """
    print(tree)


# ============================================================
# 主函数
# ============================================================

async def main():
    """主函数"""
    print("🔥 同步 vs 多线程 vs 异步 终极对比")
    print("作者：老王\n")

    # IO密集型对比
    print("\n" + "🌐 IO密集型任务对比（网络请求）".center(70, "="))

    try:
        # 1. 同步
        sync_results, sync_time = sync_download(URLS)

        # 2. 多线程
        thread_results, thread_time = threaded_download(URLS)

        # 3. 异步
        async_results, async_time = await async_download(URLS)

        # 对比
        print("\n" + "="*70)
        print("IO密集型任务性能对比：")
        print("="*70)
        print(f"  同步耗时：   {sync_time:.2f}秒  （基准）")
        print(f"  多线程耗时： {thread_time:.2f}秒  （提升 {sync_time/thread_time:.1f}x）")
        print(f"  异步耗时：   {async_time:.2f}秒  （提升 {sync_time/async_time:.1f}x）")
        print("="*70 + "\n")

    except Exception as e:
        print(f"⚠️ IO测试跳过（网络问题）：{e}\n")

    # CPU密集型对比
    print("\n" + "💻 CPU密集型任务对比（计算质数）".center(70, "="))

    sync_cpu_time = sync_cpu_bound()
    thread_cpu_time = threaded_cpu_bound()
    async_cpu_time = await async_cpu_bound()
    process_cpu_time = await async_cpu_bound_correct()

    print("\n" + "="*70)
    print("CPU密集型任务性能对比：")
    print("="*70)
    print(f"  同步耗时：     {sync_cpu_time:.2f}秒  （基准）")
    print(f"  多线程耗时：   {thread_cpu_time:.2f}秒  （提升 {sync_cpu_time/thread_cpu_time:.1f}x，受GIL限制）")
    print(f"  异步耗时：     {async_cpu_time:.2f}秒  （❌ 无效果）")
    print(f"  进程池耗时：   {process_cpu_time:.2f}秒  （✅ 提升 {sync_cpu_time/process_cpu_time:.1f}x）")
    print("="*70 + "\n")

    # 资源占用对比
    compare_resource_usage()

    # 决策树
    decision_tree()

    # 总结
    print("\n" + "="*70)
    print("老王总结")
    print("="*70)
    summary = """
1. IO密集型任务（网络、文件、数据库）：
   → 首选：异步协程（asyncio + aiohttp/aiofiles）
   → 理由：高并发、低资源、无GIL问题

2. CPU密集型任务（计算、加密、图像）：
   → 首选：多进程（multiprocessing）
   → 理由：真正并行、避开GIL

3. 混合场景：
   → asyncio + run_in_executor(ProcessPoolExecutor)

4. 简单脚本/低并发：
   → 同步代码就够了，别过度设计

5. 记住：
   - 异步 ≠ 多线程！
   - 异步是单线程协作调度
   - await 必须等待，不是"启动后不管"
   - 想"启动后不管"用 create_task()
    """
    print(summary)
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())