"""练习33: ACP 服务器实现"""
from typing import Any, Callable
from pydantic import BaseModel
import json
import asyncio
from dataclasses import dataclass, field
import time


# ========== 1. 导入 ACP 基础类型 ==========

from typing import Literal

class ACPRequest(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str | None = None
    method: str
    params: dict[str, Any] | list[Any] | None = None


class ACPResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str | None
    result: Any | None = None
    error: dict[str, Any] | None = None


# ========== 2. 会话管理 ==========

@dataclass
class Session:
    """会话"""
    id: str
    work_dir: str
    provider: str
    model: str
    created_at: float = field(default_factory=time.time)
    messages: list[dict] = field(default_factory=list)


class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self.sessions: dict[str, Session] = {}
        self.session_counter = 0
    
    def create(self, work_dir: str, provider: str, model: str) -> Session:
        """创建会话"""
        self.session_counter += 1
        session_id = f"session_{self.session_counter:03d}"
        
        session = Session(
            id=session_id,
            work_dir=work_dir,
            provider=provider,
            model=model
        )
        
        self.sessions[session_id] = session
        return session
    
    def get(self, session_id: str) -> Session | None:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def list_all(self) -> list[Session]:
        """列出所有会话"""
        return list(self.sessions.values())
    
    def delete(self, session_id: str) -> bool:
        """删除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# ========== 3. 方法处理器 ==========

class ACPMethodHandler:
    """ACP 方法处理器基类"""
    
    async def handle(self, params: dict | None) -> Any:
        """处理请求"""
        raise NotImplementedError


class InitializeHandler(ACPMethodHandler):
    """初始化处理器"""
    
    async def handle(self, params: dict | None) -> dict:
        return {
            "protocol_version": "0.1.0",
            "server_info": {
                "name": "kimi-acp-server",
                "version": "1.0.0"
            },
            "capabilities": {
                "streaming": True,
                "tools": True,
                "sessions": True
            }
        }


class CreateSessionHandler(ACPMethodHandler):
    """创建会话处理器"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
    
    async def handle(self, params: dict | None) -> dict:
        if not params:
            raise ValueError("Missing parameters")
        
        session = self.session_manager.create(
            work_dir=params.get("work_dir", "/tmp"),
            provider=params.get("provider", "openai"),
            model=params.get("model", "gpt-4")
        )
        
        return {
            "id": session.id,
            "work_dir": session.work_dir,
            "provider": session.provider,
            "model": session.model,
            "created_at": session.created_at
        }


class ListSessionsHandler(ACPMethodHandler):
    """列出会话处理器"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
    
    async def handle(self, params: dict | None) -> list[dict]:
        sessions = self.session_manager.list_all()
        return [
            {
                "id": s.id,
                "work_dir": s.work_dir,
                "provider": s.provider,
                "model": s.model,
                "created_at": s.created_at
            }
            for s in sessions
        ]


class SendMessageHandler(ACPMethodHandler):
    """发送消息处理器"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
    
    async def handle(self, params: dict | None) -> dict:
        if not params:
            raise ValueError("Missing parameters")
        
        session_id = params["session_id"]
        content = params["content"]
        
        session = self.session_manager.get(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # 添加用户消息
        session.messages.append({"role": "user", "content": content})
        
        # 模拟 AI 回复
        ai_response = f"收到消息: {content}"
        session.messages.append({"role": "assistant", "content": ai_response})
        
        return {
            "content": ai_response,
            "finish_reason": "stop"
        }


# ========== 4. ACP 服务器 ==========

class ACPServer:
    """ACP 服务器"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.handlers: dict[str, ACPMethodHandler] = {}
        
        # 注册默认处理器
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认处理器"""
        self.register_handler("initialize", InitializeHandler())
        self.register_handler("session/create", CreateSessionHandler(self.session_manager))
        self.register_handler("session/list", ListSessionsHandler(self.session_manager))
        self.register_handler("message/send", SendMessageHandler(self.session_manager))
    
    def register_handler(self, method: str, handler: ACPMethodHandler):
        """注册方法处理器"""
        self.handlers[method] = handler
        print(f"✓ 注册处理器: {method}")
    
    async def handle_request(self, request: ACPRequest) -> ACPResponse:
        """处理请求"""
        try:
            # 查找处理器
            if request.method not in self.handlers:
                return ACPResponse(
                    id=request.id,
                    error={
                        "code": -32601,
                        "message": f"Method not found: {request.method}"
                    }
                )
            
            handler = self.handlers[request.method]
            
            # 执行处理器
            result = await handler.handle(request.params)
            
            return ACPResponse(
                id=request.id,
                result=result
            )
        
        except Exception as e:
            return ACPResponse(
                id=request.id,
                error={
                    "code": -32603,
                    "message": str(e)
                }
            )
    
    async def handle_json(self, json_str: str) -> str:
        """处理 JSON 请求字符串"""
        try:
            request = ACPRequest.model_validate_json(json_str)
            response = await self.handle_request(request)
            return response.model_dump_json()
        
        except Exception as e:
            error_response = ACPResponse(
                id=None,
                error={
                    "code": -32700,
                    "message": f"Parse error: {e}"
                }
            )
            return error_response.model_dump_json()


# ========== 演示函数 ==========

async def demo_acp_server():
    """演示 ACP 服务器"""
    print("\n" + "=" * 60)
    print("ACP 服务器演示")
    print("=" * 60)
    
    server = ACPServer()
    
    # 测试初始化
    print("\n1. 测试初始化:")
    init_req = '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}'
    response = await server.handle_json(init_req)
    print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))
    
    # 测试创建会话
    print("\n2. 测试创建会话:")
    create_req = '''
    {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "session/create",
        "params": {
            "work_dir": "/tmp/test",
            "provider": "openai",
            "model": "gpt-4"
        }
    }
    '''
    response = await server.handle_json(create_req)
    print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))
    
    # 测试发送消息
    print("\n3. 测试发送消息:")
    msg_req = '''
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "message/send",
        "params": {
            "session_id": "session_001",
            "content": "你好！"
        }
    }
    '''
    response = await server.handle_json(msg_req)
    print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))
    
    # 测试列出会话
    print("\n4. 测试列出会话:")
    list_req = '{"jsonrpc": "2.0", "id": 4, "method": "session/list", "params": {}}'
    response = await server.handle_json(list_req)
    print(json.dumps(json.loads(response), indent=2, ensure_ascii=False))


async def main():
    """主函数"""
    print("\n=== 练习33: ACP 服务器实现 ===")
    
    await demo_acp_server()
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


# 学习要点:
# 1. ACP 服务器基于方法处理器模式
# 2. 每个方法对应一个处理器类
# 3. 服务器负责路由请求到对应处理器
# 4. 需要处理各种错误情况（解析错误、方法不存在、执行错误等）
# 5. 会话管理是 ACP 服务器的核心功能
