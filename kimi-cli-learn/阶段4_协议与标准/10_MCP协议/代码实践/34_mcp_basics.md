# 练习34: MCP 协议基础

## 什么是 MCP？

MCP (Model Context Protocol) 是 Anthropic 提出的一个开放协议，用于**标准化 AI 模型与外部工具/数据源的集成**。

## MCP 核心概念

### 1. 协议架构

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   AI Model  │ ◀─────▶ │ MCP Server  │ ◀─────▶ │   Tool/API  │
│  (Client)   │         │  (Bridge)   │         │   (Source)  │
└─────────────┘         └─────────────┘         └─────────────┘
```

- **AI Model (Client)**: Claude、GPT 等大模型
- **MCP Server**: 工具集成服务器，提供标准化接口
- **Tool/API**: 文件系统、数据库、API 等外部资源

### 2. MCP 消息类型

#### 工具定义 (Tool Definition)

```json
{
  "name": "read_file",
  "description": "读取文件内容",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "文件路径"
      }
    },
    "required": ["file_path"]
  }
}
```

#### 工具调用 (Tool Call)

```json
{
  "name": "read_file",
  "arguments": {
    "file_path": "/home/user/document.txt"
  }
}
```

#### 工具结果 (Tool Result)

```json
{
  "content": "文件内容...",
  "is_error": false
}
```

## MCP vs Function Calling

| 特性 | OpenAI Function Calling | MCP |
|------|-------------------------|-----|
| 提出者 | OpenAI | Anthropic |
| 标准化 | API 级别 | 协议级别 |
| 工具定义 | JSON Schema | JSON Schema |
| 服务器 | 无 | MCP Server |
| 跨模型 | 仅 OpenAI | 支持多种模型 |
| 生态系统 | 闭源 | 开放协议 |

## MCP 服务器示例

### Python MCP Server

```python
from mcp import MCPServer, Tool

# 创建 MCP 服务器
server = MCPServer(name="file-tools")

# 定义工具
@server.tool()
async def read_file(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, 'r') as f:
        return f.read()

@server.tool()
async def write_file(file_path: str, content: str) -> str:
    """写入文件"""
    with open(file_path, 'w') as f:
        f.write(content)
    return f"已写入 {len(content)} 字符"

# 启动服务器
server.run()
```

### TypeScript MCP Server

```typescript
import { MCPServer } from '@anthropic-ai/mcp';

const server = new MCPServer({
  name: 'web-tools',
  tools: [
    {
      name: 'fetch_url',
      description: '获取网页内容',
      inputSchema: {
        type: 'object',
        properties: {
          url: { type: 'string', description: 'URL地址' }
        },
        required: ['url']
      },
      handler: async ({ url }) => {
        const response = await fetch(url);
        return await response.text();
      }
    }
  ]
});

server.start();
```

## MCP 在 Kimi CLI 中的应用

### 1. MCP 工具集成

Kimi CLI 通过 MCP 协议集成了多种工具：

- **文件工具**: 读取、写入、搜索文件
- **Bash 工具**: 执行命令
- **Web 工具**: 搜索、抓取网页
- **自定义工具**: 用户自定义 MCP Server

### 2. 工具配置

```toml
# kimi.toml
[tools]
enabled = true

[[tools.mcp_servers]]
name = "file-tools"
command = "python"
args = ["file_mcp_server.py"]

[[tools.mcp_servers]]
name = "web-tools"
command = "node"
args = ["web_mcp_server.js"]
```

### 3. 工具调用流程

```
用户输入 → Agent 分析 → 选择工具 → 调用 MCP Server → 执行工具 → 返回结果 → 继续对话
```

## 实践要点

1. **工具设计原则**:
   - 功能单一：每个工具只做一件事
   - 描述清晰：让 AI 能准确理解工具用途
   - 参数明确：定义清晰的输入输出

2. **错误处理**:
   - 返回清晰的错误信息
   - 区分用户错误和系统错误
   - 提供修复建议

3. **安全性**:
   - 输入验证：检查参数合法性
   - 权限控制：限制工具访问范围
   - 审计日志：记录工具调用历史

## 扩展阅读

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Anthropic MCP 介绍](https://www.anthropic.com/news/model-context-protocol)
- [MCP GitHub](https://github.com/anthropics/mcp)

## 下一步

- 练习35: 实现简单的 MCP Server
- 练习36: MCP 工具测试与调试
