#!/usr/bin/env python3
"""
同步 vs 异步 性能对比实战
作者：老王
目的：直观感受异步编程的威力
"""

import time
import asyncio
import aiohttp
import requests


# ============================================================
# 场景1：模拟IO操作（睡眠）
# ============================================================

def sync_sleep_task(task_id, duration):
    """同步睡眠任务"""
    print(f"[同步] 任务{task_id} 开始，需要{duration}秒")
    time.sleep(duration)  # 阻塞当前线程
    print(f"[同步] 任务{task_id} 完成")
    return f"任务{task_id}的结果"


async def async_sleep_task(task_id, duration):
    """异步睡眠任务"""
    print(f"[异步] 任务{task_id} 开始,需要{duration}秒")
    await asyncio.sleep(duration)  # 不阻塞线程,让出控制权
    print(f"[异步] 任务{task_id} 完成")
    return f"任务{task_id}的结果"


def test_sync_sleep():
    """测试同步执行"""
    print("\n" + "="*60)
    print("测试1：同步执行3个任务")
    print("="*60)

    start = time.time()

    # 串行执行
    sync_sleep_task(1, 2)
    sync_sleep_task(2, 3)
    sync_sleep_task(3, 1)

    elapsed = time.time() - start
    print(f"\n同步总耗时：{elapsed:.2f}秒")


async def test_async_sleep():
    """测试异步执行"""
    print("\n" + "="*60)
    print("测试2：异步执行3个任务")
    print("="*60)

    start = time.time()

    # 并发执行
    await asyncio.gather(
        async_sleep_task(1, 2),
        async_sleep_task(2, 3),
        async_sleep_task(3, 1)
    )

    elapsed = time.time() - start
    print(f"\n异步总耗时：{elapsed:.2f}秒")


# ============================================================
# 场景2：HTTP请求（真实网络IO）
# ============================================================

URLS = [
    "https://httpbin.org/delay/1",  # 延迟1秒响应
    "https://httpbin.org/delay/2",  # 延迟2秒响应
    "https://httpbin.org/delay/1",  # 延迟1秒响应
]


def sync_fetch(url):
    """同步HTTP请求"""
    print(f"[同步] 开始请求：{url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"[同步] 完成请求：{url} (状态码：{response.status_code})")
        return response.status_code
    except Exception as e:
        print(f"[同步] 请求失败：{url} (错误：{e})")
        return None


async def async_fetch(session, url):
    """异步HTTP请求"""
    print(f"[异步] 开始请求：{url}")
    try:
        async with session.get(url, timeout=10) as response:
            status = response.status
            print(f"[异步] 完成请求：{url} (状态码：{status})")
            return status
    except Exception as e:
        print(f"[异步] 请求失败：{url} (错误：{e})")
        return None


def test_sync_http():
    """测试同步HTTP请求"""
    print("\n" + "="*60)
    print("测试3：同步HTTP请求")
    print("="*60)

    start = time.time()

    for url in URLS:
        sync_fetch(url)

    elapsed = time.time() - start
    print(f"\n同步HTTP总耗时：{elapsed:.2f}秒")


async def test_async_http():
    """测试异步HTTP请求"""
    print("\n" + "="*60)
    print("测试4：异步HTTP请求")
    print("="*60)

    start = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [async_fetch(session, url) for url in URLS]
        await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"\n异步HTTP总耗时：{elapsed:.2f}秒")


# ============================================================
# 场景3：混合场景 - 展示 create_task 的用法
# ============================================================

async def background_task(name, duration):
    """后台任务"""
    print(f"[后台任务] {name} 开始运行...")
    await asyncio.sleep(duration)
    print(f"[后台任务] {name} 完成")
    return f"{name}的结果"


async def test_create_task():
    """测试 create_task - "启动后不等待"的用法"""
    print("\n" + "="*60)
    print("测试5：create_task 的用法")
    print("="*60)

    print("\n方式1：直接 await（会等待完成）")
    start = time.time()
    result1 = await background_task("任务A", 2)  # 等待2秒
    print(f"任务A结果：{result1}")
    print(f"耗时：{time.time() - start:.2f}秒\n")

    print("方式2：使用 create_task（立即返回）")
    start = time.time()
    task = asyncio.create_task(background_task("任务B", 2))  # 立即返回
    print("任务B已启动，继续执行其他代码...")
    print("做一些其他事情...")
    await asyncio.sleep(0.5)  # 模拟其他操作
    print("现在需要任务B的结果了，等待中...")
    result2 = await task  # 等待任务完成
    print(f"任务B结果：{result2}")
    print(f"耗时：{time.time() - start:.2f}秒\n")

    print("方式3：并发多个任务")
    start = time.time()
    task1 = asyncio.create_task(background_task("任务C", 2))
    task2 = asyncio.create_task(background_task("任务D", 3))
    task3 = asyncio.create_task(background_task("任务E", 1))
    print("所有任务已启动，一起等待...")
    results = await asyncio.gather(task1, task2, task3)
    print(f"所有结果：{results}")
    print(f"耗时：{time.time() - start:.2f}秒（而不是2+3+1=6秒）")


# ============================================================
# 场景4：错误示范 - 忘记 await
# ============================================================

async def test_common_mistake():
    """常见错误示范"""
    print("\n" + "="*60)
    print("测试6：常见错误示范")
    print("="*60)

    print("\n❌ 错误1：忘记 await")
    result = async_sleep_task(99, 1)  # 这只是创建了协程对象，没有执行！
    print(f"返回值类型：{type(result)}")  # <class 'coroutine'>
    print(f"返回值：{result}")  # <coroutine object async_sleep_task at 0x...>

    print("\n✅ 正确方式：使用 await")
    result = await async_sleep_task(100, 1)  # 真正执行
    print(f"返回值类型：{type(result)}")  # <class 'str'>
    print(f"返回值：{result}")  # "任务100的结果"


# ============================================================
# 主函数
# ============================================================

async def main():
    """主函数"""
    print("🔥 异步编程性能对比实战")
    print("作者：老王")

    # 测试1&2：睡眠对比
    test_sync_sleep()
    await test_async_sleep()

    # 测试3&4：HTTP请求对比（需要网络）
    try:
        test_sync_http()
        await test_async_http()
    except Exception as e:
        print(f"\n⚠️ HTTP测试跳过（可能没网络）：{e}")

    # 测试5：create_task 用法
    await test_create_task()

    # 测试6：常见错误
    await test_common_mistake()

    print("\n" + "="*60)
    print("✅ 所有测试完成！")
    print("="*60)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

    """
    预期输出分析：

    测试1（同步睡眠）：2 + 3 + 1 = 6秒
    测试2（异步睡眠）：max(2, 3, 1) = 3秒  👈 快了一倍！

    测试3（同步HTTP）：1 + 2 + 1 = 4秒
    测试4（异步HTTP）：max(1, 2, 1) = 2秒  👈 快了一倍！

    测试5（create_task）：
      - 方式1：2秒（串行）
      - 方式2：2秒（但可以边等待边做其他事）
      - 方式3：3秒（而不是6秒）

    关键结论：
    1. 异步在IO等待场景下性能提升显著
    2. 并发数越多，提升越明显
    3. 单线程即可实现高并发
    """