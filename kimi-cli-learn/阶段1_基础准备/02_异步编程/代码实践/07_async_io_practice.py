"""练习7: 异步I/O实践 - 异步爬虫"""
import asyncio
import aiohttp
import aiofiles
import time
from pathlib import Path

async def fetch_url(session: aiohttp.ClientSession, url: str, index: int):
    """获取单个URL"""
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
    # aiofiles 是一个异步文件操作库, 用于在异步环境中读写文件
    # 它的使用方式与内置的 open 函数类似, 但需要在异步函数中使用 await 关键字

    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(content)

async def async_crawler(urls: list[str], save_dir: Path):
    """异步爬虫"""
    print(f"\n=== 开始爬取 {len(urls)} 个网页 ===\n")
    start = time.time()
    save_dir.mkdir(parents=True, exist_ok=True)

    # 创建异步会话
    # aiohttp.ClientSession 是一个异步会话类, 用于发送HTTP请求
    # 它的使用方式与 requests.Session 类似, 但需要在异步函数中使用 await 关键字

    # 异步会话可以在多个请求之间共享, 避免重复建立连接
    # 它的生命周期与异步函数相同, 即当异步函数执行完毕时, 会话也会被关闭

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, i) for i, url in enumerate(urls)]
        results = await asyncio.gather(*tasks)

    save_tasks = []
    for index, url, content in results:
        if content:
            file_path = save_dir / f"page_{index}.html"
            save_tasks.append(save_to_file(file_path, content))
    
    await asyncio.gather(*save_tasks)
    total = time.time() - start
    print(f"\n=== 爬取完成，总耗时: {total:.2f}秒 ===")

async def main():
    urls = ["https://example.com", "https://httpbin.org/delay/1"]
    await async_crawler(urls, Path("./crawler_output"))

if __name__ == "__main__":
    asyncio.run(main())
