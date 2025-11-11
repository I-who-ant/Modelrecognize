"""练习26: Function Schema 设计"""
from typing import Literal, Any
from pydantic import BaseModel, Field
import json


# ========== 1. 基础 Function Schema ==========

def create_basic_function_schema() -> dict:
    """创建基础的函数Schema"""
    return {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，例如：北京、上海"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位"
                }
            },
            "required": ["city"]
        }
    }


# ========== 2. 使用 Pydantic 定义 Schema ==========

class WeatherParams(BaseModel):
    """天气查询参数"""
    city: str = Field(description="城市名称")
    unit: Literal["celsius", "fahrenheit"] = Field(default="celsius", description="温度单位")


class FileOperation(BaseModel):
    """文件操作参数"""
    operation: Literal["read", "write", "delete"] = Field(description="操作类型")
    file_path: str = Field(description="文件路径")
    content: str | None = Field(default=None, description="写入内容（仅写操作需要）")


def pydantic_to_function_schema(model: type[BaseModel], name: str, description: str) -> dict:
    """将 Pydantic Model 转换为 Function Schema"""
    schema = model.model_json_schema()
    
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": schema.get("properties", {}),
            "required": schema.get("required", [])
        }
    }


# ========== 3. 复杂参数类型 ==========

class SearchParams(BaseModel):
    """搜索参数（支持多种复杂类型）"""
    query: str = Field(description="搜索关键词")
    filters: dict[str, Any] | None = Field(default=None, description="过滤条件（键值对）")
    max_results: int = Field(default=10, ge=1, le=100, description="最大结果数")
    sort_by: Literal["relevance", "date", "popularity"] = Field(default="relevance")
    include_fields: list[str] | None = Field(default=None, description="包含的字段列表")


# ========== 4. 多个函数的 Schema 集合 ==========

class FunctionRegistry:
    """函数注册表"""
    
    def __init__(self):
        self.functions: dict[str, dict] = {}
    
    def register(self, name: str, description: str, params_model: type[BaseModel]):
        """注册函数"""
        schema = pydantic_to_function_schema(params_model, name, description)
        self.functions[name] = schema
    
    def get_all_schemas(self) -> list[dict]:
        """获取所有函数Schema"""
        return list(self.functions.values())
    
    def get_schema(self, name: str) -> dict | None:
        """获取指定函数Schema"""
        return self.functions.get(name)


# ========== 演示函数 ==========

def demo_basic_schema():
    """演示基础Schema"""
    print("\n" + "=" * 60)
    print("1. 基础 Function Schema")
    print("=" * 60)
    
    schema = create_basic_function_schema()
    print(json.dumps(schema, indent=2, ensure_ascii=False))


def demo_pydantic_schema():
    """演示 Pydantic Schema"""
    print("\n" + "=" * 60)
    print("2. Pydantic Model 转 Function Schema")
    print("=" * 60)
    
    schema = pydantic_to_function_schema(
        WeatherParams,
        "get_weather",
        "获取天气信息"
    )
    print(json.dumps(schema, indent=2, ensure_ascii=False))


def demo_complex_schema():
    """演示复杂Schema"""
    print("\n" + "=" * 60)
    print("3. 复杂参数类型 Schema")
    print("=" * 60)
    
    schema = pydantic_to_function_schema(
        SearchParams,
        "search",
        "执行高级搜索"
    )
    print(json.dumps(schema, indent=2, ensure_ascii=False))


def demo_function_registry():
    """演示函数注册表"""
    print("\n" + "=" * 60)
    print("4. 函数注册表")
    print("=" * 60)
    
    registry = FunctionRegistry()
    
    # 注册多个函数
    registry.register("get_weather", "获取天气", WeatherParams)
    registry.register("file_operation", "文件操作", FileOperation)
    registry.register("search", "搜索", SearchParams)
    
    print(f"\n已注册 {len(registry.functions)} 个函数:")
    for name in registry.functions:
        print(f"  - {name}")
    
    print("\n所有 Schema:")
    print(json.dumps(registry.get_all_schemas(), indent=2, ensure_ascii=False))


def main():
    """主函数"""
    print("\n=== 练习26: Function Schema 设计 ===")
    
    demo_basic_schema()
    demo_pydantic_schema()
    demo_complex_schema()
    demo_function_registry()
    
    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 学习要点:
# 1. Function Schema 是 OpenAI Function Calling 的核心
# 2. 使用 Pydantic 可以更方便地定义和验证参数
# 3. Schema 必须精确描述参数类型、约束和说明
# 4. 支持复杂类型：dict、list、union、literal 等
