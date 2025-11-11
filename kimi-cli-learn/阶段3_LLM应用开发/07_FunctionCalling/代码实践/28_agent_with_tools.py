"""练习28: Agent + Tools 完整示例"""
from typing import Any, AsyncIterator
from pydantic import BaseModel
import json


# ========== 1. 工具定义 ==========

class Tool(BaseModel):
    """工具定义"""
    name: str
    description: str
    parameters: dict[str, Any]


class ToolCall(BaseModel):
    """工具调用"""
    id: str
    name: str
    arguments: dict[str, Any]


# ========== 2. 模拟 LLM ==========

class MockLLM:
    """模拟的 LLM（简化版）"""
    
    def __init__(self, tools: list[Tool]):
        self.tools = tools
    
    def chat(self, messages: list[dict]) -> dict:
        """模拟聊天（会返回工具调用）"""
        user_msg = messages[-1]["content"]
        
        # 简单规则：根据关键词决定调用哪个工具
        if "天气" in user_msg:
            return {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_001",
                        "name": "get_weather",
                        "arguments": {"city": "北京"}
                    }
                ]
            }
        
        elif "计算" in user_msg or "+" in user_msg:
            return {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_002",
                        "name": "calculate",
                        "arguments": {"expression": "2+3"}
                    }
                ]
            }
        
        else:
            return {
                "role": "assistant",
                "content": "我可以帮你查天气或做计算",
                "tool_calls": None
            }


# ========== 3. Agent 实现 ==========

class ToolAgent:
    """带工具的 Agent"""
    
    def __init__(self):
        self.messages: list[dict] = []
        self.tools: dict[str, Any] = {}
        self.tool_schemas: list[Tool] = []
    
    def register_tool(self, name: str, description: str, parameters: dict, func):
        """注册工具"""
        self.tools[name] = func
        self.tool_schemas.append(Tool(
            name=name,
            description=description,
            parameters=parameters
        ))
        print(f"✓ 注册工具: {name}")
    
    def _execute_tool(self, tool_call: dict) -> Any:
        """执行工具"""
        name = tool_call["name"]
        args = tool_call["arguments"]
        
        print(f"\n🔧 执行工具: {name}")
        print(f"   参数: {json.dumps(args, ensure_ascii=False)}")
        
        if name not in self.tools:
            return f"错误: 未知工具 {name}"
        
        try:
            result = self.tools[name](**args)
            print(f"   结果: {result}")
            return result
        except Exception as e:
            return f"错误: {e}"
    
    def chat(self, user_input: str) -> str:
        """聊天（支持工具调用）"""
        print(f"\n👤 用户: {user_input}")
        
        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # 模拟 LLM
        llm = MockLLM(self.tool_schemas)
        
        # 最多尝试 3 轮（防止无限循环）
        for i in range(3):
            print(f"\n🤖 Agent 思考轮次 {i+1}...")
            
            # 调用 LLM
            response = llm.chat(self.messages)
            
            # 检查是否有工具调用
            if response.get("tool_calls"):
                # 执行所有工具
                tool_results = []
                for tc in response["tool_calls"]:
                    result = self._execute_tool(tc)
                    tool_results.append({
                        "tool_call_id": tc["id"],
                        "name": tc["name"],
                        "result": result
                    })
                
                # 添加助手消息（工具调用）
                self.messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": response["tool_calls"]
                })
                
                # 添加工具结果
                self.messages.append({
                    "role": "tool",
                    "content": json.dumps(tool_results, ensure_ascii=False)
                })
                
                # 继续下一轮（让 LLM 基于工具结果生成回复）
                # 这里简化：直接返回工具结果
                final_answer = f"根据工具执行结果: {json.dumps(tool_results, ensure_ascii=False, indent=2)}"
                print(f"\n💬 助手: {final_answer}")
                return final_answer
            
            else:
                # 没有工具调用，直接返回内容
                content = response["content"]
                self.messages.append(response)
                print(f"\n💬 助手: {content}")
                return content
        
        return "达到最大思考轮次"


# ========== 4. 示例工具函数 ==========

def get_weather(city: str, unit: str = "celsius") -> dict:
    """获取天气"""
    return {
        "city": city,
        "temperature": 15,
        "condition": "晴",
        "unit": unit
    }


def calculate(expression: str) -> float:
    """计算表达式"""
    return eval(expression, {"__builtins__": {}}, {})


def search_database(query: str) -> list[dict]:
    """搜索数据库"""
    return [
        {"id": 1, "title": f"结果1: {query}"},
        {"id": 2, "title": f"结果2: {query}"}
    ]


# ========== 演示函数 ==========

def demo_agent_with_tools():
    """演示 Agent + Tools"""
    print("\n" + "=" * 60)
    print("Agent + Tools 完整示例")
    print("=" * 60)
    
    # 创建 Agent
    agent = ToolAgent()
    
    # 注册工具
    agent.register_tool(
        name="get_weather",
        description="获取天气信息",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"}
            },
            "required": ["city"]
        },
        func=get_weather
    )
    
    agent.register_tool(
        name="calculate",
        description="计算数学表达式",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "数学表达式"}
            },
            "required": ["expression"]
        },
        func=calculate
    )
    
    # 测试对话
    print("\n" + "=" * 60)
    print("对话测试")
    print("=" * 60)
    
    agent.chat("北京今天天气怎么样？")
    
    print("\n" + "-" * 60)
    
    agent.chat("帮我计算 2+3")
    
    print("\n" + "-" * 60)
    
    agent.chat("你好")


def main():
    """主函数"""
    print("\n=== 练习28: Agent + Tools 完整示例 ===")
    
    demo_agent_with_tools()
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 学习要点:
# 1. Agent 需要管理对话历史和工具调用
# 2. LLM 决定何时调用工具、调用哪个工具
# 3. Agent 执行工具后，将结果返回给 LLM
# 4. 可能需要多轮交互才能完成任务
# 5. 这就是 ReAct (Reasoning + Acting) 模式
