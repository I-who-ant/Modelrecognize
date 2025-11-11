"""练习42: Agent 循环高级特性"""
from typing import AsyncIterator
from dataclasses import dataclass
import asyncio
import time


# ========== 1. 高级循环控制 ==========

@dataclass
class AgentLoopConfig:
    """Agent 循环配置"""
    max_turns: int = 5
    timeout_per_turn: float = 30.0
    max_tool_calls_per_turn: int = 3
    enable_parallel_tools: bool = True


class AgentLoopMetrics:
    """Agent 循环指标"""
    
    def __init__(self):
        self.total_turns = 0
        self.total_tool_calls = 0
        self.total_time = 0.0
        self.tool_execution_times: dict[str, list[float]] = {}
    
    def record_tool_execution(self, tool_name: str, duration: float):
        """记录工具执行时间"""
        if tool_name not in self.tool_execution_times:
            self.tool_execution_times[tool_name] = []
        self.tool_execution_times[tool_name].append(duration)
    
    def get_summary(self) -> dict:
        """获取摘要"""
        return {
            "total_turns": self.total_turns,
            "total_tool_calls": self.total_tool_calls,
            "total_time": self.total_time,
            "avg_tools_per_turn": (
                self.total_tool_calls / self.total_turns
                if self.total_turns > 0 else 0
            ),
            "tool_stats": {
                name: {
                    "count": len(times),
                    "avg_time": sum(times) / len(times) if times else 0,
                    "max_time": max(times) if times else 0
                }
                for name, times in self.tool_execution_times.items()
            }
        }


# ========== 2. 高级 Agent 循环 ==========

class AdvancedAgentLoop:
    """高级 Agent 循环"""
    
    def __init__(
        self,
        config: AgentLoopConfig,
        llm,
        tool_manager
    ):
        self.config = config
        self.llm = llm
        self.tool_manager = tool_manager
        self.metrics = AgentLoopMetrics()
        self.messages: list[dict] = []
    
    async def run(self, user_input: str) -> AsyncIterator[str]:
        """运行 Agent 循环"""
        start_time = time.time()
        
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            async for chunk in self._loop():
                yield chunk
        
        finally:
            self.metrics.total_time = time.time() - start_time
    
    async def _loop(self) -> AsyncIterator[str]:
        """内部循环逻辑"""
        
        for turn in range(self.config.max_turns):
            self.metrics.total_turns += 1
            
            print(f"\n{'='*60}")
            print(f"🔄 Agent 循环 - 轮次 {turn + 1}/{self.config.max_turns}")
            print(f"{'='*60}")
            
            # 设置单轮超时
            try:
                async with asyncio.timeout(self.config.timeout_per_turn):
                    result = await self._execute_turn()
                    
                    async for chunk in result:
                        yield chunk
                    
                    # 检查是否应该结束
                    if await self._should_stop():
                        break
            
            except asyncio.TimeoutError:
                yield "\n\n⏱️ 本轮超时，继续下一轮..."
                continue
        
        else:
            # 达到最大轮次
            yield "\n\n⚠️ 达到最大思考轮次"
    
    async def _execute_turn(self) -> AsyncIterator[str]:
        """执行单轮"""
        
        # 1. 调用 LLM
        print("📤 调用 LLM...")
        response_stream = self.llm.astream_chat(
            messages=self.messages,
            tools=self.tool_manager.get_tool_schemas()
        )
        
        # 2. 收集响应
        full_content = ""
        tool_calls = []
        
        async for chunk in response_stream:
            if content := chunk.delta.get("content"):
                full_content += content
                yield content
            
            if tc_list := chunk.delta.get("tool_calls"):
                tool_calls.extend(tc_list)
        
        # 3. 记录助手消息
        assistant_msg = {"role": "assistant", "content": full_content}
        if tool_calls:
            assistant_msg["tool_calls"] = tool_calls
        self.messages.append(assistant_msg)
        
        # 4. 执行工具调用
        if tool_calls:
            # 限制工具调用数量
            if len(tool_calls) > self.config.max_tool_calls_per_turn:
                print(f"\n⚠️ 工具调用过多 ({len(tool_calls)})，仅执行前 {self.config.max_tool_calls_per_turn} 个")
                tool_calls = tool_calls[:self.config.max_tool_calls_per_turn]
            
            await self._execute_tools(tool_calls)
    
    async def _execute_tools(self, tool_calls: list):
        """执行工具调用（支持并行）"""
        
        if self.config.enable_parallel_tools:
            # 并行执行
            print(f"\n🔧 并行执行 {len(tool_calls)} 个工具...")
            tasks = [self._execute_single_tool(tc) for tc in tool_calls]
            await asyncio.gather(*tasks)
        
        else:
            # 串行执行
            print(f"\n🔧 串行执行 {len(tool_calls)} 个工具...")
            for tc in tool_calls:
                await self._execute_single_tool(tc)
    
    async def _execute_single_tool(self, tool_call):
        """执行单个工具"""
        start = time.time()
        
        print(f"  ▶ {tool_call.name}({tool_call.arguments})")
        
        try:
            result = await self.tool_manager.execute(tool_call)
            duration = time.time() - start
            
            # 记录指标
            self.metrics.total_tool_calls += 1
            self.metrics.record_tool_execution(tool_call.name, duration)
            
            print(f"    ✓ 完成 ({duration:.2f}s): {str(result)[:50]}...")
            
            # 添加工具结果
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.name,
                "content": str(result)
            })
        
        except Exception as e:
            print(f"    ✗ 错误: {e}")
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.name,
                "content": f"错误: {e}"
            })
    
    async def _should_stop(self) -> bool:
        """判断是否应该停止循环"""
        # 检查最后一条助手消息
        if self.messages:
            last_msg = self.messages[-1]
            
            # 如果没有工具调用，停止
            if last_msg.get("role") == "assistant" and not last_msg.get("tool_calls"):
                return True
        
        return False
    
    def print_metrics(self):
        """打印指标"""
        print("\n" + "=" * 60)
        print("📊 Agent 循环指标")
        print("=" * 60)
        
        summary = self.metrics.get_summary()
        
        print(f"\n总轮次: {summary['total_turns']}")
        print(f"总工具调用: {summary['total_tool_calls']}")
        print(f"总耗时: {summary['total_time']:.2f}s")
        print(f"平均每轮工具调用: {summary['avg_tools_per_turn']:.1f}")
        
        if summary['tool_stats']:
            print("\n工具统计:")
            for name, stats in summary['tool_stats'].items():
                print(f"  {name}:")
                print(f"    调用次数: {stats['count']}")
                print(f"    平均耗时: {stats['avg_time']:.2f}s")
                print(f"    最大耗时: {stats['max_time']:.2f}s")


# ========== 演示函数 ==========

async def demo_advanced_loop():
    """演示高级 Agent 循环"""
    print("\n" + "=" * 60)
    print("高级 Agent 循环演示")
    print("=" * 60)
    
    # 模拟组件（从练习41导入）
    from dataclasses import dataclass as dc
    
    @dc
    class ChatChunk:
        delta: dict
        finish_reason: str | None = None
    
    @dc
    class ToolCall:
        id: str
        name: str
        arguments: dict
    
    class MockLLM:
        async def astream_chat(self, messages, tools):
            # 模拟工具调用
            yield ChatChunk(
                delta={"tool_calls": [
                    ToolCall(id="1", name="read_file", arguments={"path": "/tmp/test"})
                ]},
                finish_reason="tool_calls"
            )
    
    class MockToolManager:
        def get_tool_schemas(self):
            return []
        
        async def execute(self, tool_call):
            await asyncio.sleep(0.1)  # 模拟耗时
            return "工具执行结果"
    
    # 创建配置
    config = AgentLoopConfig(
        max_turns=3,
        timeout_per_turn=5.0,
        max_tool_calls_per_turn=2,
        enable_parallel_tools=True
    )
    
    # 创建循环
    loop = AdvancedAgentLoop(
        config=config,
        llm=MockLLM(),
        tool_manager=MockToolManager()
    )
    
    # 运行
    async for chunk in loop.run("测试输入"):
        print(chunk, end='', flush=True)
    
    # 打印指标
    loop.print_metrics()


async def main():
    """主函数"""
    print("\n=== 练习42: Agent 循环高级特性 ===")
    
    await demo_advanced_loop()
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. 循环控制：最大轮次、超时、工具数量限制
# 2. 性能监控：记录循环指标和工具执行时间
# 3. 并行执行：支持并发调用多个工具
# 4. 错误处理：优雅处理超时和工具执行失败
# 5. 终止条件：智能判断何时结束循环
