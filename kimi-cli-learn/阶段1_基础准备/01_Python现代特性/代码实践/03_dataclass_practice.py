"""
练习3: Dataclass 和 Pydantic 实践

学习目标:
- 掌握 dataclass 的使用
- 掌握 Pydantic 数据验证
- 理解两者的区别和使用场景
"""

from dataclasses import dataclass, field
from pydantic import BaseModel, Field, SecretStr, field_validator
from typing import Literal
import time


# ========== 使用 dataclass ==========

@dataclass(slots=True)
class SessionInfo:
    """会话信息（使用 dataclass）

    slots=True: 优化内存使用
    """
    id: str
    work_dir: str
    created_at: float = field(default_factory=time.time)
    history_file: str | None = None
    _private_data: str = field(default="", repr=False)

    def is_active(self, timeout: float = 86400.0) -> bool:
        """检查会话是否活跃（24小时内）"""
        return time.time() - self.created_at < timeout

    def age_in_hours(self) -> float:
        """会话年龄（小时）"""
        return (time.time() - self.created_at) / 3600


# ========== 使用 Pydantic ==========

ProviderType = Literal["kimi", "openai_legacy", "openai_responses", "anthropic"]


class ProviderConfig(BaseModel):
    """LLM 提供商配置（使用 Pydantic）"""
    type: ProviderType
    base_url: str = Field(..., min_length=1, description="API base URL")
    api_key: SecretStr = Field(..., description="API key")
    custom_headers: dict[str, str] = Field(default_factory=dict)

    @field_validator('base_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """验证 URL 格式"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('base_url must start with http:// or https://')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "kimi",
                "base_url": "https://api.moonshot.cn/v1",
                "api_key": "sk-xxx",
            }
        }
    }


class ModelConfig(BaseModel):
    """模型配置"""
    provider: str
    model: str
    max_context_size: int = Field(default=100_000, gt=0, description="最大上下文大小")
    capabilities: set[str] = Field(default_factory=set, description="模型能力")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度参数")

    @field_validator('model')
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """验证模型名称"""
        if not v.strip():
            raise ValueError('model name cannot be empty')
        return v.strip()


def demo_dataclass():
    """演示 dataclass"""
    print("=" * 60)
    print("Dataclass 演示")
    print("=" * 60)

    # 创建会话
    session = SessionInfo(
        id="abc123",
        work_dir="/home/user/project",
        history_file=".kimi_history",
    )

    print(f"会话信息: {session}")
    print(f"是否活跃: {session.is_active()}")
    print(f"会话年龄: {session.age_in_hours():.2f} 小时")
    print()


def demo_pydantic():
    """演示 Pydantic"""
    print("=" * 60)
    print("Pydantic 演示")
    print("=" * 60)

    # 创建 Provider 配置
    print("1. 创建有效的 Provider 配置")
    provider = ProviderConfig(
        type="kimi",
        base_url="https://api.moonshot.cn/v1",
        api_key=SecretStr("sk-xxxxx"),
        custom_headers={"User-Agent": "KimiCLI/1.0"}
    )
    print(f"Provider: {provider.type}")
    print(f"Base URL: {provider.base_url}")
    print(f"API Key: {provider.api_key.get_secret_value()[:8]}...")
    print()

    # 创建 Model 配置
    print("2. 创建 Model 配置")
    model = ModelConfig(
        provider="kimi",
        model="kimi-for-coding",
        max_context_size=128_000,
        capabilities={"thinking", "image_in", "web_search"},
        temperature=0.7,
    )
    print(model.model_dump_json(indent=2))
    print()

    # 验证失败示例
    print("3. 测试参数验证")
    try:
        invalid_provider = ProviderConfig(
            type="kimi",
            base_url="invalid-url",  # 无效 URL
            api_key=SecretStr("sk-xxx"),
        )
    except Exception as e:
        print(f"验证失败: {e}")
    print()


def demo_comparison():
    """对比 dataclass 和 Pydantic"""
    print("=" * 60)
    print("Dataclass vs Pydantic 对比")
    print("=" * 60)

    comparison = """
    | 特性           | dataclass        | Pydantic         |
    |----------------|------------------|------------------|
    | 数据验证       | ❌ 不支持        | ✅ 自动验证      |
    | 序列化         | ❌ 需手动实现    | ✅ 内置支持      |
    | 类型转换       | ❌ 不转换        | ✅ 自动转换      |
    | 性能           | ✅ 更快          | ⚠️  稍慢         |
    | 内存占用       | ✅ 更少(slots)   | ⚠️  稍多         |
    | 使用场景       | 简单数据结构     | 需要验证的配置   |

    使用建议:
    - dataclass: 内部数据结构，性能敏感场景
    - Pydantic: 外部输入，配置文件，API 数据
    """
    print(comparison)


def main():
    """主函数"""
    print("\n=== 练习3: Dataclass 和 Pydantic 实践 ===\n")

    demo_dataclass()
    demo_pydantic()
    demo_comparison()


if __name__ == "__main__":
    main()


# 扩展练习:
# 1. 实现一个使用 dataclass 的配置类，手动添加验证
# 2. 实现 Pydantic 模型的嵌套验证
# 3. 对比两者在大量数据时的性能差异
# 4. 实现配置的环境变量覆盖功能
