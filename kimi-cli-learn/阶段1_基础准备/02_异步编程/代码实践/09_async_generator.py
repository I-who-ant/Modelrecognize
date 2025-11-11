"""练习9: 异步生成器实践 - 流式响应解析器"""
import asyncio
import aiohttp
import json
from typing import AsyncGenerator

async def simulated_llm_stream(prompt: str) -> AsyncGenerator[str, None]:
    """模拟 LLM 流式响应"""
    response = f"Response to: {prompt}. This is a simulated streaming response."
    words = response.split()
    for word in words:
        await asyncio.sleep(0.05)
        yield word + " "

async def batch_generator(items: list, batch_size: int) -> AsyncGenerator[list, None]:
    """分批生成器"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size] # 生成当前批次
        await asyncio.sleep(0.1) # 模拟异步操作
        yield batch

async def demo_stream_processing():
    """演示流式处理"""
    print("\n=== 模拟 LLM 流式响应 ===")
    prompt = "What is Python?"
    full_response = ""
    async for chunk in simulated_llm_stream(prompt):
        print(chunk, end='', flush=True)
        full_response += chunk
    print(f"\n\n完整响应: {full_response}")

async def demo_batch_processing():
    """演示分批处理"""
    print("\n=== 分批处理 ===")
    items = list(range(20))
    async for batch in batch_generator(items, batch_size=5):
        print(f"处理批次: {batch}")

async def main():
    await demo_stream_processing()
    await demo_batch_processing()

if __name__ == "__main__":
    asyncio.run(main())
