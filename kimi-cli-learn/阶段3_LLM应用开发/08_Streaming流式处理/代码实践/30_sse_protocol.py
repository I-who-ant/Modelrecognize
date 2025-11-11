"""练习30: SSE 协议实现"""
from typing import AsyncIterator
import asyncio
import json


# ========== 1. SSE 事件格式 ==========

class SSEEvent:
    """SSE 事件"""
    
    def __init__(
        self,
        data: str,
        event: str | None = None,
        id: str | None = None,
        retry: int | None = None
    ):
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry
    
    def format(self) -> str:
        """格式化为 SSE 协议字符串"""
        lines = []
        
        if self.event:
            lines.append(f"event: {self.event}")
        
        if self.id:
            lines.append(f"id: {self.id}")
        
        if self.retry:
            lines.append(f"retry: {self.retry}")
        
        # data 可以多行
        for line in self.data.split('\n'):
            lines.append(f"data: {line}")
        
        # SSE 事件以两个换行符结束
        return '\n'.join(lines) + '\n\n'


# ========== 2. SSE 流生成器 ==========

async def sse_stream(messages: AsyncIterator[str]) -> AsyncIterator[str]:
    """将消息流转换为 SSE 格式"""
    event_id = 0
    
    async for msg in messages:
        event_id += 1
        event = SSEEvent(
            data=msg,
            event="message",
            id=str(event_id)
        )
        yield event.format()


async def sse_json_stream(data_stream: AsyncIterator[dict]) -> AsyncIterator[str]:
    """将 JSON 数据流转换为 SSE 格式"""
    event_id = 0
    
    async for data in data_stream:
        event_id += 1
        event = SSEEvent(
            data=json.dumps(data, ensure_ascii=False),
            event="data",
            id=str(event_id)
        )
        yield event.format()


# ========== 3. 模拟 LLM SSE 流 ==========

async def mock_llm_stream() -> AsyncIterator[dict]:
    """模拟 LLM 流式返回"""
    chunks = [
        {"delta": {"role": "assistant", "content": ""}, "finish_reason": None},
        {"delta": {"content": "你好"}, "finish_reason": None},
        {"delta": {"content": "！"}, "finish_reason": None},
        {"delta": {"content": "我是"}, "finish_reason": None},
        {"delta": {"content": "AI"}, "finish_reason": None},
        {"delta": {"content": "助手"}, "finish_reason": None},
        {"delta": {"content": "。"}, "finish_reason": None},
        {"delta": {}, "finish_reason": "stop"}
    ]
    
    for chunk in chunks:
        await asyncio.sleep(0.1)  # 模拟网络延迟
        yield chunk


# ========== 4. SSE 客户端（解析器） ==========

class SSEParser:
    """SSE 事件解析器"""
    
    def __init__(self):
        self.event = None
        self.data = []
        self.id = None
        self.retry = None
    
    def feed_line(self, line: str) -> SSEEvent | None:
        """解析一行，返回完整事件（如果有）"""
        line = line.rstrip('\n\r')
        
        # 空行表示事件结束
        if not line:
            if self.data:
                event = SSEEvent(
                    data='\n'.join(self.data),
                    event=self.event,
                    id=self.id,
                    retry=self.retry
                )
                # 重置状态
                self.event = None
                self.data = []
                self.id = None
                self.retry = None
                return event
            return None
        
        # 注释行（以冒号开头）
        if line.startswith(':'):
            return None
        
        # 解析字段
        if ':' in line:
            field, _, value = line.partition(':')
            value = value.lstrip(' ')
            
            if field == 'event':
                self.event = value
            elif field == 'data':
                self.data.append(value)
            elif field == 'id':
                self.id = value
            elif field == 'retry':
                try:
                    self.retry = int(value)
                except ValueError:
                    pass
        
        return None


async def parse_sse_stream(sse_text: str) -> AsyncIterator[SSEEvent]:
    """解析 SSE 流"""
    parser = SSEParser()
    
    for line in sse_text.split('\n'):
        event = parser.feed_line(line + '\n')
        if event:
            yield event


# ========== 演示函数 ==========

async def demo_basic_sse():
    """演示基础 SSE 格式"""
    print("\n" + "=" * 60)
    print("1. 基础 SSE 事件格式")
    print("=" * 60)
    
    # 单个事件
    event = SSEEvent(
        data="Hello, World!",
        event="greeting",
        id="1"
    )
    
    print("单个事件:")
    print(event.format())
    
    # 多行数据
    event2 = SSEEvent(
        data="第一行\n第二行\n第三行",
        event="multiline",
        id="2"
    )
    
    print("多行事件:")
    print(event2.format())


async def demo_sse_stream():
    """演示 SSE 流"""
    print("\n" + "=" * 60)
    print("2. SSE 流式输出")
    print("=" * 60)
    
    async def message_generator():
        messages = ["你好", "世界", "！"]
        for msg in messages:
            await asyncio.sleep(0.1)
            yield msg
    
    print("生成 SSE 流:")
    async for sse in sse_stream(message_generator()):
        print(sse, end='')


async def demo_llm_sse():
    """演示 LLM SSE 流"""
    print("\n" + "=" * 60)
    print("3. LLM SSE 流式返回")
    print("=" * 60)
    
    print("模拟 LLM 流式输出:\n")
    
    full_text = ""
    async for sse in sse_json_stream(mock_llm_stream()):
        print(sse, end='')
        
        # 提取文本内容
        for line in sse.split('\n'):
            if line.startswith('data: '):
                try:
                    data = json.loads(line[6:])
                    if content := data.get("delta", {}).get("content"):
                        full_text += content
                        print(f"\r当前文本: {full_text}", end='', flush=True)
                except:
                    pass
    
    print(f"\n\n完整文本: {full_text}")


async def demo_sse_parser():
    """演示 SSE 解析"""
    print("\n" + "=" * 60)
    print("4. SSE 解析器")
    print("=" * 60)
    
    # 模拟 SSE 响应
    sse_text = """event: start
data: {"type": "start"}

event: message
id: 1
data: 你好

event: message
id: 2
data: 世界

event: end
data: {"type": "end"}

"""
    
    print("解析 SSE 文本:")
    async for event in parse_sse_stream(sse_text):
        print(f"事件类型: {event.event}")
        print(f"事件ID: {event.id}")
        print(f"数据: {event.data}")
        print("-" * 40)


async def main():
    """主函数"""
    print("\n=== 练习30: SSE 协议实现 ===")
    
    await demo_basic_sse()
    await demo_sse_stream()
    await demo_llm_sse()
    await demo_sse_parser()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. SSE 是基于 HTTP 的单向流式协议
# 2. 格式：event/data/id/retry 字段，以双换行符分隔事件
# 3. data 字段可以多行，每行以 "data: " 开头
# 4. LLM 流式返回通常使用 SSE + JSON 格式
# 5. 需要正确处理解析和错误恢复
