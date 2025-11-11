"""练习38: App 层设计"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal
import asyncio


# ========== 1. App 配置 ==========

@dataclass
class AppConfig:
    """App 层配置"""
    ui_mode: Literal["shell", "print", "acp", "wire"]
    work_dir: Path
    model: str
    provider: str
    temperature: float = 0.7
    max_tokens: int = 4000
    tools_enabled: bool = True


# ========== 2. Session 管理 ==========

@dataclass
class Session:
    """会话"""
    id: str
    work_dir: Path
    messages: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({"role": role, "content": content})
    
    def get_history(self) -> list[dict]:
        """获取历史消息"""
        return self.messages.copy()


class SessionManager:
    """会话管理器"""
    
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.sessions: dict[str, Session] = {}
        self.current_session: Session | None = None
    
    def create_session(self) -> Session:
        """创建新会话"""
        import time
        session_id = f"session_{int(time.time())}"
        
        session = Session(
            id=session_id,
            work_dir=self.work_dir
        )
        
        self.sessions[session_id] = session
        self.current_session = session
        
        print(f"✓ 创建会话: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Session | None:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def switch_session(self, session_id: str) -> bool:
        """切换会话"""
        if session := self.get_session(session_id):
            self.current_session = session
            print(f"✓ 切换到会话: {session_id}")
            return True
        return False


# ========== 3. UI 适配器 ==========

class UIAdapter:
    """UI 适配器基类"""
    
    async def display(self, content: str):
        """显示内容"""
        raise NotImplementedError
    
    async def display_stream(self, content_stream):
        """流式显示"""
        raise NotImplementedError
    
    async def get_input(self) -> str:
        """获取用户输入"""
        raise NotImplementedError


class ShellUI(UIAdapter):
    """Shell 交互式 UI"""
    
    async def display(self, content: str):
        print(f"\n🤖 AI: {content}")
    
    async def display_stream(self, content_stream):
        print("\n🤖 AI: ", end='', flush=True)
        async for chunk in content_stream:
            print(chunk, end='', flush=True)
        print()
    
    async def get_input(self) -> str:
        return input("\n👤 You: ")


class PrintUI(UIAdapter):
    """简单打印 UI"""
    
    async def display(self, content: str):
        print(content)
    
    async def display_stream(self, content_stream):
        async for chunk in content_stream:
            print(chunk, end='', flush=True)
        print()
    
    async def get_input(self) -> str:
        return input(">>> ")


# ========== 4. App 层 ==========

class App:
    """App 层 - 应用程序核心逻辑"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.session_manager = SessionManager(config.work_dir)
        self.ui = self._create_ui(config.ui_mode)
        self.soul = None  # 后续会连接 Soul 层
    
    def _create_ui(self, ui_mode: str) -> UIAdapter:
        """创建 UI 适配器"""
        if ui_mode == "shell":
            return ShellUI()
        elif ui_mode == "print":
            return PrintUI()
        else:
            raise ValueError(f"不支持的 UI 模式: {ui_mode}")
    
    async def initialize(self):
        """初始化 App"""
        print("🚀 初始化 Kimi App")
        
        # 创建会话
        self.session_manager.create_session()
        
        # 初始化 Soul 层（省略）
        # self.soul = Soul(config)
        # await self.soul.initialize()
        
        print("✓ 初始化完成")
    
    async def chat(self, user_input: str) -> str:
        """处理聊天"""
        session = self.session_manager.current_session
        
        if not session:
            raise RuntimeError("没有活动会话")
        
        # 添加用户消息
        session.add_message("user", user_input)
        
        # 调用 Soul 层处理（这里模拟）
        # response = await self.soul.chat(user_input)
        
        # 模拟 AI 回复
        response = f"收到: {user_input}"
        
        # 添加助手消息
        session.add_message("assistant", response)
        
        return response
    
    async def run(self):
        """运行 App（主循环）"""
        await self.initialize()
        
        await self.ui.display("欢迎使用 Kimi CLI！输入 'exit' 退出。")
        
        while True:
            try:
                # 获取用户输入
                user_input = await self.ui.get_input()
                
                # 退出命令
                if user_input.lower() in ["exit", "quit"]:
                    await self.ui.display("再见！")
                    break
                
                # 空输入
                if not user_input.strip():
                    continue
                
                # 处理聊天
                response = await self.chat(user_input)
                
                # 显示回复
                await self.ui.display(response)
            
            except KeyboardInterrupt:
                await self.ui.display("\n中断，正在退出...")
                break
            
            except Exception as e:
                await self.ui.display(f"错误: {e}")


# ========== 演示函数 ==========

async def demo_app():
    """演示 App 层"""
    print("\n" + "=" * 60)
    print("App 层演示")
    print("=" * 60)
    
    # 创建配置
    config = AppConfig(
        ui_mode="print",
        work_dir=Path("/tmp/kimi"),
        model="gpt-4",
        provider="openai"
    )
    
    # 创建 App
    app = App(config)
    
    # 初始化
    await app.initialize()
    
    # 模拟对话
    print("\n模拟对话:")
    response1 = await app.chat("你好")
    print(f"回复: {response1}")
    
    response2 = await app.chat("帮我写个函数")
    print(f"回复: {response2}")
    
    # 查看会话历史
    session = app.session_manager.current_session
    print(f"\n会话历史 ({len(session.messages)} 条消息):")
    for msg in session.messages:
        print(f"  {msg['role']:10} {msg['content']}")


async def main():
    """主函数"""
    print("\n=== 练习38: App 层设计 ===")
    
    await demo_app()
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. App 层是 CLI 和 Soul 层之间的桥梁
# 2. 负责会话管理、UI 适配、业务逻辑
# 3. UI 适配器模式支持多种 UI 模式
# 4. 会话管理器维护多个会话
# 5. App 层不处理 LLM 调用，而是委托给 Soul 层
