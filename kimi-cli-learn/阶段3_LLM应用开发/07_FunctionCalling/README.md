# 模块07: Function Calling 工具调用

**学习时长**: 5天

**学习目标**: 掌握 Function Calling，理解 Kimi CLI 的工具系统

---

## 📋 学习内容概览

1. **Function Calling 基础** (Day 36-37)
2. **工具定义与 JSON Schema** (Day 38)
3. **工具调用流程** (Day 39)
4. **错误处理与重试** (Day 40)

---

## 🎯 学习目标

- ✅ 理解 Function Calling 原理
- ✅ 能定义工具 JSON Schema
- ✅ 掌握工具调用流程
- ✅ 能实现错误处理和重试
- ✅ 理解 Kimi CLI 的工具架构

---

## 📚 学习资源

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Kimi API Function Calling](https://platform.moonshot.cn/docs)

---

## 📖 详细学习内容

### 📝 01: Function Calling 基础 (Day 36-37)

#### 工具定义格式

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
]
```

#### 练习25

实现基础的工具调用系统，支持：
- 工具注册
- 工具调用
- 结果返回

---

### 📝 02: 工具定义与 JSON Schema (Day 38)

#### JSON Schema 详解

```python
{
    "type": "object",
    "properties": {
        "param1": {"type": "string"},
        "param2": {"type": "integer", "minimum": 0},
        "param3": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["param1"]
}
```

#### 练习26

为常用操作定义工具 Schema：
- 文件操作
- 网络请求
- 数据处理

---

### 📝 03: 工具调用流程 (Day 39)

#### 完整流程

```
1. User Request
   ↓
2. LLM 决定调用工具
   ↓
3. 解析工具调用参数
   ↓
4. 执行工具
   ↓
5. 返回结果给 LLM
   ↓
6. LLM 生成最终响应
```

#### Kimi CLI 中的实现

```python
# src/kimi_cli/tools/
- base.py: 工具基类
- registry.py: 工具注册
- executor.py: 工具执行
```

#### 练习27

实现完整的工具调用流程。

---

### 📝 04: 错误处理与重试 (Day 40)

#### 错误类型

1. **参数错误**: 参数验证失败
2. **执行错误**: 工具执行异常
3. **超时错误**: 执行超时
4. **权限错误**: 无权限执行

#### 重试策略

```python
async def execute_with_retry(
    tool: Tool,
    max_retries: int = 3,
    backoff: float = 1.0
):
    for attempt in range(max_retries):
        try:
            return await tool.execute()
        except RetryableError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(backoff * (2 ** attempt))
```

#### 练习28

实现错误处理和重试机制。

---

## 📊 模块总结

### 知识点检查
- [ ] Function Calling 原理
- [ ] JSON Schema 定义
- [ ] 工具调用流程
- [ ] 错误处理策略

### 代码练习
- [ ] 练习25-28

### 输出成果
- [ ] 工具调用系统
- [ ] Kimi CLI 工具分析
- [ ] 学习笔记

---

## 🔄 下一步

完成本模块后，进入 **模块08: Streaming 流式处理**。

---

*Created by 老王 | Last Updated: 2025-01-10*
