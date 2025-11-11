"""练习32: ACP 协议基础"""
from typing import Any, Literal
from pydantic import BaseModel, Field
import json


# ========== 1. ACP 消息类型 ==========

class ACPRequest(BaseModel):
    """ACP 请求（基于 JSON-RPC 2.0）"""
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str | None = None
    method: str
    params: dict[str, Any] | list[Any] | None = None


class ACPResponse(BaseModel):
    """ACP 响应"""
    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str | None
    result: Any | None = None
    error: dict[str, Any] | None = None


class ACPError(BaseModel):
    """ACP 错误"""
    code: int
    message: str
    data: Any | None = None


# ========== 2. ACP 标准方法 ==========

class ACPMethods:
    """ACP 协议标准方法"""
    
    # 初始化
    INITIALIZE = "initialize"
    
    # 会话管理
    CREATE_SESSION = "session/create"
    LIST_SESSIONS = "session/list"
    DELETE_SESSION = "session/delete"
    
    # 消息发送
    SEND_MESSAGE = "message/send"
    
    # 工具相关
    LIST_TOOLS = "tools/list"
    EXECUTE_TOOL = "tools/execute"


# ========== 3. 初始化请求/响应 ==========

class InitializeParams(BaseModel):
    """初始化参数"""
    protocol_version: str = Field(default="0.1.0")
    client_info: dict[str, str] = Field(default_factory=dict)
    capabilities: dict[str, Any] = Field(default_factory=dict)


class InitializeResult(BaseModel):
    """初始化结果"""
    protocol_version: str
    server_info: dict[str, str]
    capabilities: dict[str, Any]


# ========== 4. 会话管理 ==========

class CreateSessionParams(BaseModel):
    """创建会话参数"""
    work_dir: str | None = None
    provider: str = "openai"
    model: str = "gpt-4"


class SessionInfo(BaseModel):
    """会话信息"""
    id: str
    work_dir: str
    provider: str
    model: str
    created_at: float


# ========== 5. 消息发送 ==========

class SendMessageParams(BaseModel):
    """发送消息参数"""
    session_id: str
    content: str
    stream: bool = False


class MessageChunk(BaseModel):
    """流式消息块"""
    type: Literal["content", "tool_call", "done"]
    content: str | None = None
    tool_calls: list[dict] | None = None


# ========== 6. ACP 客户端示例 ==========

class ACPClient:
    """ACP 客户端（简化版）"""
    
    def __init__(self):
        self.request_id = 0
    
    def _next_id(self) -> int:
        """生成下一个请求ID"""
        self.request_id += 1
        return self.request_id
    
    def create_request(self, method: str, params: dict | None = None) -> ACPRequest:
        """创建 ACP 请求"""
        return ACPRequest(
            id=self._next_id(),
            method=method,
            params=params
        )
    
    def initialize(self) -> ACPRequest:
        """创建初始化请求"""
        params = InitializeParams(
            client_info={
                "name": "my-client",
                "version": "1.0.0"
            },
            capabilities={
                "streaming": True,
                "tools": True
            }
        )
        
        return self.create_request(
            ACPMethods.INITIALIZE,
            params.model_dump()
        )
    
    def create_session(self, work_dir: str, provider: str = "openai") -> ACPRequest:
        """创建会话请求"""
        params = CreateSessionParams(
            work_dir=work_dir,
            provider=provider
        )
        
        return self.create_request(
            ACPMethods.CREATE_SESSION,
            params.model_dump()
        )
    
    def send_message(self, session_id: str, content: str, stream: bool = False) -> ACPRequest:
        """发送消息请求"""
        params = SendMessageParams(
            session_id=session_id,
            content=content,
            stream=stream
        )
        
        return self.create_request(
            ACPMethods.SEND_MESSAGE,
            params.model_dump()
        )


# ========== 演示函数 ==========

def demo_acp_request():
    """演示 ACP 请求格式"""
    print("\n" + "=" * 60)
    print("1. ACP 请求格式")
    print("=" * 60)
    
    # 创建请求
    request = ACPRequest(
        id=1,
        method="initialize",
        params={"protocol_version": "0.1.0"}
    )
    
    print("\nJSON-RPC 2.0 请求:")
    print(json.dumps(request.model_dump(), indent=2, ensure_ascii=False))


def demo_acp_response():
    """演示 ACP 响应格式"""
    print("\n" + "=" * 60)
    print("2. ACP 响应格式")
    print("=" * 60)
    
    # 成功响应
    success = ACPResponse(
        id=1,
        result={
            "protocol_version": "0.1.0",
            "server_info": {"name": "kimi-server", "version": "1.0.0"}
        }
    )
    
    print("\n成功响应:")
    print(json.dumps(success.model_dump(), indent=2, ensure_ascii=False))
    
    # 错误响应
    error = ACPResponse(
        id=2,
        error={
            "code": -32600,
            "message": "Invalid Request",
            "data": {"detail": "Missing required parameter"}
        }
    )
    
    print("\n错误响应:")
    print(json.dumps(error.model_dump(), indent=2, ensure_ascii=False))


def demo_acp_client():
    """演示 ACP 客户端使用"""
    print("\n" + "=" * 60)
    print("3. ACP 客户端使用")
    print("=" * 60)
    
    client = ACPClient()
    
    # 初始化
    init_req = client.initialize()
    print("\n初始化请求:")
    print(json.dumps(init_req.model_dump(), indent=2, ensure_ascii=False))
    
    # 创建会话
    session_req = client.create_session("/tmp/work")
    print("\n创建会话请求:")
    print(json.dumps(session_req.model_dump(), indent=2, ensure_ascii=False))
    
    # 发送消息
    msg_req = client.send_message("session_001", "你好", stream=True)
    print("\n发送消息请求:")
    print(json.dumps(msg_req.model_dump(), indent=2, ensure_ascii=False))


def main():
    """主函数"""
    print("\n=== 练习32: ACP 协议基础 ===")
    
    demo_acp_request()
    demo_acp_response()
    demo_acp_client()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 学习要点:
# 1. ACP 基于 JSON-RPC 2.0 协议
# 2. 请求必须包含: jsonrpc, id, method, params
# 3. 响应包含: jsonrpc, id, result/error
# 4. 支持会话管理、消息发送、工具调用等功能
# 5. Kimi CLI 使用 ACP 进行客户端-服务器通信
