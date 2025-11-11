"""练习41: Soul 层核心实现"""
from typing import AsyncIterator, Any
from dataclasses import dataclass
import asyncio


# ========== 1. 数据模型 ==========

@dataclass
class ChatChunk:
    """聊天响应块"""
    delta: dict[str, Any]
    finish_reason: str | None = None


@dataclass
class ToolCall:
    """工具调用"""
    id: str
    name: str
    arguments: dict[str, Any]


# ========== 2. LLM 抽象层 ==========

class LLMProvider:
    """LLM 提供商基类"""
    
    async def astream_chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ) -> AsyncIterator[ChatChunk]:
        """流式聊天"""
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """模拟 LLM（用于测试）"""
    
    async def astream_chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None
    ) -> AsyncIterator[ChatChunk]:
        """模拟流式响应"""
        
        # 获取用户最后一条消息
        user_msg = messages[-1]["content"]
        
        # 简单规则：如果提到"文件"，调用read_file工具
        if "文件" in user_msg and tools:
            # 返回工具调用
            yield ChatChunk(
                delta={
                    "tool_calls": [
                        ToolCall(
                            id="call_001",
                            name="read_file",
                            arguments={"file_path": "/tmp/test.txt"}
                        )
                    ]
                },
                finish_reason=None
            )
            yield ChatChunk(delta={}, finish_reason="tool_calls")
        
        else:
            # 返回文本内容
            response = f"收到您的消息: {user_msg}"
            for char in response:
                await asyncio.sleep(0.02)
                yield ChatChunk(
                    delta={"content": char},
                    finish_reason=None
                )
            
            yield ChatChunk(delta={}, finish_reason="stop")


# ========== 3. 工具管理器 ==========

class Tool:
    """工具基类"""
    
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def get_schema(self) -> dict:
        """获取工具 Schema"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }
    
    async def execute(self, arguments: dict) -> str:
        """执行工具"""
        raise NotImplementedError


class ReadFileTool(Tool):
    """读取文件工具"""
    
    def __init__(self):
        super().__init__(
            name="read_file",
            description="读取文件内容",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "文件路径"}
                },
                "required": ["file_path"]
            }
        )
    
    async def execute(self, arguments: dict) -> str:
        """执行读取"""
        file_path = arguments["file_path"]
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return f"文件内容:\n{content}"
        except FileNotFoundError:
            return f"错误: 文件不存在 {file_path}"


class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.tools: dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        """注册工具"""
        self.tools[tool.name] = tool
        print(f"✓ 注册工具: {tool.name}")
    
    def get_tool_schemas(self) -> list[dict]:
        """获取所有工具 Schema"""
        return [tool.get_schema() for tool in self.tools.values()]
    
    async def execute(self, tool_call: ToolCall) -> str:
        """执行工具调用"""
        if tool_call.name not in self.tools:
            return f"错误: 未知工具 {tool_call.name}"
        
        tool = self.tools[tool_call.name]
        return await tool.execute(tool_call.arguments)


# ========== 4. Soul 层核心 ==========

class Soul:
    """Soul 层 - Agent 执行引擎"""
    
    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.tool_manager = ToolManager()
        self.messages: list[dict] = []
        self.system_prompt = self._build_system_prompt()
        
        # 注册默认工具
        self._register_default_tools()
    
    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return """你是 Kimi，一个专业的 AI 编程助手。

你可以使用工具来帮助用户完成任务。必要时调用工具，但不要过度使用。"""
    
    def _register_default_tools(self):
        """注册默认工具"""
        self.tool_manager.register(ReadFileTool())
    
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """聊天接口"""
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # 执行 Agent 循环
        async for chunk in self._agent_loop(max_turns=3):
            yield chunk
    
    async def _agent_loop(self, max_turns: int = 5) -> AsyncIterator[str]:
        """Agent 循环"""
        
        for turn in range(max_turns):
            print(f"\n🔄 Agent 循环 - 轮次 {turn + 1}")
            
            # 1. 调用 LLM
            response_stream = self.llm.astream_chat(
                messages=self.messages,
                tools=self.tool_manager.get_tool_schemas()
            )
            
            # 2. 收集响应
            full_content = ""
            tool_calls = []
            
            async for chunk in response_stream:
                # 文本内容
                if content := chunk.delta.get("content"):
                    full_content += content
                    yield content  # 流式输出给用户
                
                # 工具调用
                if tc_list := chunk.delta.get("tool_calls"):
                    tool_calls.extend(tc_list)
                
                # 结束
                if chunk.finish_reason:
                    print(f"\n  finish_reason: {chunk.finish_reason}")
            
            # 3. 添加助手消息
            assistant_msg = {"role": "assistant", "content": full_content}
            if tool_calls:
                assistant_msg["tool_calls"] = tool_calls
            self.messages.append(assistant_msg)
            
            # 4. 如果没有工具调用，结束循环
            if not tool_calls:
                break
            
            # 5. 执行工具调用
            for tc in tool_calls:
                print(f"\n  🔧 执行工具: {tc.name}")
                result = await self.tool_manager.execute(tc)
                print(f"     结果: {result[:50]}...")
                
                # 添加工具结果
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.name,
                    "content": result
                })
            
            # 继续下一轮
        
        # 达到最大轮次
        else:
            yield "\n\n[达到最大思考轮次]"


# ========== 演示函数 ==========

async def demo_soul_basic():
    """演示 Soul 基础功能"""
    print("\n" + "=" * 60)
    print("1. Soul 基础功能演示")
    print("=" * 60)
    
    # 创建 LLM 和 Soul
    llm = MockLLMProvider()
    soul = Soul(llm)
    
    # 测试对话
    print("\n对话1: 简单文本回复")
    async for chunk in soul.chat("你好"):
        print(chunk, end='', flush=True)
    print()


async def demo_soul_with_tools():
    """演示 Soul 工具调用"""
    print("\n" + "=" * 60)
    print("2. Soul 工具调用演示")
    print("=" * 60)
    
    # 创建测试文件
    with open("/tmp/test.txt", "w") as f:
        f.write("这是测试文件的内容。\n包含多行。")
    
    llm = MockLLMProvider()
    soul = Soul(llm)
    
    # 测试工具调用
    print("\n对话2: 触发工具调用")
    async for chunk in soul.chat("帮我读取文件"):
        print(chunk, end='', flush=True)
    print()


async def demo_message_history():
    """演示消息历史"""
    print("\n" + "=" * 60)
    print("3. 消息历史查看")
    print("=" * 60)
    
    llm = MockLLMProvider()
    soul = Soul(llm)
    
    # 多轮对话
    await soul.chat("第一条消息").__anext__()  # 消耗生成器
    async for _ in soul.chat("第一条消息"):
        pass
    
    async for _ in soul.chat("第二条消息"):
        pass
    
    # 查看历史
    print("\n消息历史:")
    for i, msg in enumerate(soul.messages, 1):
        role = msg["role"]
        content = msg.get("content", "")
        print(f"{i}. [{role}] {content[:50]}...")


async def main():
    """主函数"""
    print("\n=== 练习41: Soul 层核心实现 ===")
    
    await demo_soul_basic()
    await demo_soul_with_tools()
    await demo_message_history()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. Soul 层实现了完整的 Agent 循环
# 2. LLM 抽象层支持不同的模型提供商
# 3. 工具管理器统一管理所有工具
# 4. 消息历史包含用户、助手、工具三种角色
# 5. 流式处理提供实时反馈
# 6. Agent 循环支持多轮工具调用
