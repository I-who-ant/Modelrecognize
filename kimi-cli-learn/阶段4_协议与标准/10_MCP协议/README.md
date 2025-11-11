# 模块10: MCP 协议 (Model Context Protocol)

**学习时长**: 5天

**学习目标**: 掌握 MCP 协议，能开发 MCP 服务器

---

## 📋 学习内容概览

1. **协议概述** (Day 54)
2. **工具定义** (Day 55)
3. **Resources 管理** (Day 56)
4. **Prompts 模板** (Day 57)
5. **开发 MCP 服务器** (Day 58)

---

## 🎯 学习目标

- ✅ 理解 MCP 协议规范
- ✅ 能定义 MCP 工具
- ✅ 能开发 MCP 服务器
- ✅ 理解 Kimi CLI 的 MCP 集成

---

## 📚 学习资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)

---

## 📖 核心知识点

### MCP 简介

Model Context Protocol (MCP) 是 Anthropic 推出的标准化协议，用于 LLM 与外部工具的集成。

### 工具定义

```python
from fastmcp import FastMCP

mcp = FastMCP("my-tools")

@mcp.tool()
def calculate(expression: str) -> float:
    """计算数学表达式"""
    return eval(expression)
```

### Resources

```python
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """读取文件"""
    with open(path) as f:
        return f.read()
```

### Kimi CLI 集成

```python
# src/kimi_cli/tools/mcp/
- client.py: MCP 客户端
- manager.py: MCP 服务器管理
```

---

## 📊 实践练习

**练习34**: 开发基础 MCP 服务器
**练习35**: 开发高级 MCP 服务器（数据库工具）
**练习36**: 集成到 Kimi CLI

---

## 🔄 下一步

完成本模块后，进入 **阶段5: Kimi CLI 核心架构**。

---

*Created by 老王 | Last Updated: 2025-01-10*
