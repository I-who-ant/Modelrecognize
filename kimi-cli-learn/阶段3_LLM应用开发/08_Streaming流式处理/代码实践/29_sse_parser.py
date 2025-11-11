"""练习29: SSE 解析器实践"""
import asyncio
import json

async def parse_sse_stream(lines):
    """解析SSE流"""
    for line in lines:
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                break
            yield json.loads(data)

async def demo_sse():
    lines = [
        'data: {"content":"Hello"}',
        'data: {"content":" World"}',
        'data: [DONE]'
    ]
    async for chunk in parse_sse_stream(lines):
        print(chunk)

if __name__ == '__main__':
    asyncio.run(demo_sse())
