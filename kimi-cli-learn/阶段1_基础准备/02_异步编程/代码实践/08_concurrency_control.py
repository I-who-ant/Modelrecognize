"""练习8: 并发控制实践 - 限流异步下载器"""
import asyncio
import aiohttp
import time



class AsyncDownloader:
    """异步下载器（带限流）"""
    def __init__(self, max_concurrency: int = 5): # 初始化信号量, 限制并发数
        self.semaphore = asyncio.Semaphore(max_concurrency)  # 初始化信号量, 限制并发数
        self.session: aiohttp.ClientSession | None = None   # 异步会话, 用于发送HTTP请求
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):  # 异步上下文退出方法, 用于关闭异步会话
        if self.session:
            await self.session.close()
    
    async def download_one(self, url: str, index: int):
        """下载单个文件"""
        async with self.semaphore:  # 异步上下文管理器, 用于控制并发数
            print(f"[{index}] 开始下载: {url}")
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    content = await response.text()
                    print(f"[{index}] 完成")
                    return (index, True, content[:100])
            except Exception as e:
                print(f"[{index}] 失败: {e}")
                return (index, False, str(e))
    
    async def download_all(self, urls: list[str]):
        """下载所有文件"""
        tasks = [self.download_one(url, i) for i, url in enumerate(urls)]
        return await asyncio.gather(*tasks)

async def main():
    urls = ["https://httpbin.org/delay/1"] * 8
    print(f"下载 {len(urls)} 个文件，最多 3 个并发")
    start = time.time()
    async with AsyncDownloader(max_concurrency=3) as downloader:
        results = await downloader.download_all(urls)
    elapsed = time.time() - start
    success = sum(1 for _, s, _ in results if s)
    print(f"\n总耗时: {elapsed:.2f}秒，成功: {success}/{len(urls)}")

if __name__ == "__main__":
    asyncio.run(main())
