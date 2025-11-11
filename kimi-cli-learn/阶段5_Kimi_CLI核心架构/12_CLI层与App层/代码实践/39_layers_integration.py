"""练习39: 三层架构集成"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, AsyncIterator
import asyncio
import click


# ========== 1. 配置定义 ==========

@dataclass
class KimiConfig:
    """Kimi 全局配置"""
    # CLI 配置
    ui_mode: Literal["shell", "print"]
    verbose: bool
    
    # App 配置
    work_dir: Path
    
    # Soul 配置
    model: str
    provider: str
    temperature: float = 0.7
    tools_enabled: bool = True


# ========== 2. Soul 层（简化版） ==========

class MockLLM:
    """模拟 LLM"""
    
    async def astream_chat(self, messages: list[dict]) -> AsyncIterator[str]:
        """流式聊天"""
        response = "这是一个模拟的 AI 回复。"
        for char in response:
            await asyncio.sleep(0.05)
            yield char


class Soul:
    """Soul 层 - Agent 执行引擎"""
    
    def __init__(self, config: KimiConfig):
        self.config = config
        self.llm = MockLLM()
        self.messages: list[dict] = []
    
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """聊天（流式）"""
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_input})
        
        # 调用 LLM
        async for chunk in self.llm.astream_chat(self.messages):
            yield chunk
        
        # 收集完整回复
        # full_response = "..."
        # self.messages.append({"role": "assistant", "content": full_response})


# ========== 3. App 层 ==========

class UIAdapter:
    """UI 适配器"""
    
    async def display_stream(self, content_stream: AsyncIterator[str]):
        """流式显示"""
        print("\n🤖 AI: ", end='', flush=True)
        async for chunk in content_stream:
            print(chunk, end='', flush=True)
        print()
    
    async def get_input(self) -> str:
        """获取输入"""
        return input("\n👤 You: ")


class App:
    """App 层"""
    
    def __init__(self, config: KimiConfig):
        self.config = config
        self.ui = UIAdapter()
        self.soul = Soul(config)
    
    async def run_interactive(self):
        """运行交互式会话"""
        print("🚀 Kimi CLI 启动（交互模式）")
        print("   输入 'exit' 退出")
        
        while True:
            try:
                # 获取用户输入
                user_input = await self.ui.get_input()
                
                if user_input.lower() in ["exit", "quit"]:
                    print("\n再见！")
                    break
                
                if not user_input.strip():
                    continue
                
                # 调用 Soul 层处理
                response_stream = self.soul.chat(user_input)
                
                # 流式显示
                await self.ui.display_stream(response_stream)
            
            except KeyboardInterrupt:
                print("\n\n中断，正在退出...")
                break
    
    async def run_once(self, user_input: str):
        """运行单次对话（非交互模式）"""
        print(f"👤 用户: {user_input}")
        
        response_stream = self.soul.chat(user_input)
        await self.ui.display_stream(response_stream)


# ========== 4. CLI 层 ==========

@click.command()
@click.argument("prompt", required=False)
@click.option("--ui", type=click.Choice(["shell", "print"]), default="shell")
@click.option("--model", "-m", default="gpt-4")
@click.option("--work-dir", "-w", type=click.Path(path_type=Path), default=Path.cwd())
@click.option("--verbose", "-v", is_flag=True)
def kimi(
    prompt: str | None,
    ui: str,
    model: str,
    work_dir: Path,
    verbose: bool
):
    """Kimi CLI - AI 编程助手"""
    
    # 创建配置
    config = KimiConfig(
        ui_mode=ui,
        verbose=verbose,
        work_dir=work_dir,
        model=model,
        provider="openai"
    )
    
    # 创建 App
    app = App(config)
    
    # 运行
    if prompt:
        # 单次对话模式
        asyncio.run(app.run_once(prompt))
    else:
        # 交互模式
        asyncio.run(app.run_interactive())


# ========== 演示函数 ==========

async def demo_three_layers():
    """演示三层架构"""
    print("\n" + "=" * 60)
    print("三层架构集成演示")
    print("=" * 60)
    
    # 创建配置
    config = KimiConfig(
        ui_mode="print",
        verbose=True,
        work_dir=Path("/tmp/kimi"),
        model="gpt-4",
        provider="openai"
    )
    
    # 创建 App（包含 Soul）
    app = App(config)
    
    # 模拟对话
    print("\n模拟单次对话:")
    await app.run_once("你好！")
    
    print("\n" + "=" * 60)
    print("\n数据流向:")
    print("  CLI 层 (Click)")
    print("    ↓ 解析参数，创建配置")
    print("  App 层 (应用逻辑)")
    print("    ↓ 管理会话，适配 UI")
    print("  Soul 层 (Agent 引擎)")
    print("    ↓ 调用 LLM，执行工具")
    print("  返回结果")
    print("    ↑")
    print("  App 层处理")
    print("    ↑")
    print("  CLI 层显示")


def main_demo():
    """演示主函数"""
    print("\n=== 练习39: 三层架构集成 ===")
    
    asyncio.run(demo_three_layers())
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    # 可以运行演示
    # main_demo()
    
    # 或运行实际 CLI
    kimi()


# 学习要点:
# 1. 三层架构清晰分离关注点
# 2. CLI 层：参数解析、命令路由
# 3. App 层：业务逻辑、会话管理、UI 适配
# 4. Soul 层：Agent 引擎、LLM 调用、工具执行
# 5. 配置对象在层间传递
# 6. 异步流式处理贯穿整个架构
# 7. 每层职责单一，便于测试和维护

# 架构优势:
# - 职责清晰：每层专注自己的功能
# - 易于测试：可以独立测试每一层
# - 灵活扩展：可以替换任意层的实现
# - 维护性好：修改一层不影响其他层
