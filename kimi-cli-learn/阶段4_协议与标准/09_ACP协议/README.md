# 模块09: ACP 协议 (Agent Client Protocol)

**学习时长**: 4天

**学习目标**: 深入理解 ACP 协议，掌握 IDE 集成标准

---

## 📋 学习内容概览

1. **协议概述** (Day 50)
2. **消息格式** (Day 51)
3. **生命周期管理** (Day 52)
4. **IDE 集成** (Day 53)

---

## 🎯 学习目标

- ✅ 理解 ACP 协议规范
- ✅ 掌握 JSON-RPC 2.0 格式
- ✅ 理解工具调用机制
- ✅ 了解 IDE 集成方式（Zed、Cursor）

---

## 📚 学习资源

- [ACP 官方规范](https://agentclientprotocol.github.io/)
- Kimi CLI ACP 实现源码

---

## 📖 核心知识点

### ACP 协议简介

Agent Client Protocol (ACP) 是一个标准化的协议，用于 IDE 与 AI Agent 之间的通信。

### 消息格式 (JSON-RPC 2.0)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### 生命周期

```
initialize → capabilities → tools/list → tools/call → shutdown
```

### Kimi CLI 中的实现

```python
# src/kimi_cli/ui/acp/server.py
class ACPServer:
    async def handle_request(self, request):
        """处理 ACP 请求"""
        method = request["method"]

        if method == "initialize":
            return self.initialize()
        elif method == "tools/list":
            return self.list_tools()
        elif method == "tools/call":
            return await self.call_tool(request["params"])
```

---

## 📊 实践练习

**练习32**: 实现简单的 ACP 服务器
**练习33**: 分析 Kimi CLI ACP 实现

---

## 🔄 下一步

完成本模块后，进入 **模块10: MCP 协议**。

---

*Created by 老王 | Last Updated: 2025-01-10*
