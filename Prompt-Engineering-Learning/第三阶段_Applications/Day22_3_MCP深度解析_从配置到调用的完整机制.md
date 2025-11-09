# Day22_3 - MCP(Model Context Protocol)深度解析:从配置到调用的完整机制

**学习日期**: 2025-11-08
**阶段**: 第三阶段 - Applications (实际应用深度扩展)
**重要程度**: ⭐⭐⭐⭐⭐ **MCP核心机制!**

---

## 你的困惑

你对MCP(Model Context Protocol)的工作机制有疑问:

```
疑问1: MCP在应用层怎么配置的?
疑问2: 启用MCP后,模型怎么就能调用了?
疑问3: 是启用后就自动在提示词中加入,然后模型等待调用结果?
疑问4: MCP、应用层、模型之间的关系到底是什么?
```

**老王我告诉你**:MCP是一个**标准化的工具协议**,应用层通过它来管理各种外部工具,模型通过提示词(或Function Calling)来"知道"和"调用"这些工具!

---

## 核心概念:MCP的完整工作流程

```python
MCP工作流程 = """

用户问题: "读取/home/user/doc.txt文件内容"
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 1: 应用层(CherryStudio)准备提示词              │
│                                                     │
│ 检查已启用的MCP服务器:                              │
│ • Filesystem MCP ✓ (已启用)                        │
│ • Git MCP ✓ (已启用)                               │
│ • PostgreSQL MCP ✗ (未启用)                        │
│                                                     │
│ 从已启用的MCP收集工具列表:                          │
│ • filesystem_read (来自Filesystem MCP)             │
│ • filesystem_write (来自Filesystem MCP)            │
│ • git_status (来自Git MCP)                         │
│ • git_commit (来自Git MCP)                         │
│ • ...                                               │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: 应用层构造系统提示(自动生成!)               │
│                                                     │
│ 系统提示词:                                         │
│ "你是一个智能助手,可以使用以下工具:                 │
│                                                     │
│ 1. filesystem_read                                  │
│    描述: 读取文件内容                               │
│    参数: path (文件路径)                            │
│                                                     │
│ 2. filesystem_write                                 │
│    描述: 写入文件                                   │
│    参数: path (文件路径), content (内容)            │
│                                                     │
│ 3. git_status                                       │
│    描述: 查看Git状态                                │
│    参数: 无                                         │
│                                                     │
│ ...                                                 │
│                                                     │
│ 当需要使用工具时,请输出:                            │
│ <tool_use>                                          │
│ 工具名: filesystem_read                             │
│ 参数: path=/home/user/doc.txt                      │
│ </tool_use>                                         │
│ "                                                   │
│                                                     │
│ ⚠️ 关键: 这个系统提示是应用层自动生成的!            │
│          用户看不到,但模型会收到!                   │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: 发送给模型(LLM)                             │
│                                                     │
│ 消息:                                               │
│ [                                                   │
│   {                                                 │
│     "role": "system",                               │
│     "content": "你是助手,可以使用以下工具:..."      │
│   },                                                │
│   {                                                 │
│     "role": "user",                                 │
│     "content": "读取/home/user/doc.txt文件内容"     │
│   }                                                 │
│ ]                                                   │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: 模型分析并决定调用工具                      │
│                                                     │
│ 模型思考(内部):                                     │
│ "用户要读取文件,我看到有filesystem_read工具,       │
│  参数需要path,就是/home/user/doc.txt"              │
│                                                     │
│ 模型输出:                                           │
│ "好的,让我读取这个文件。                            │
│  <tool_use>                                         │
│  工具名: filesystem_read                            │
│  参数: path=/home/user/doc.txt                     │
│  </tool_use>"                                       │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: 应用层解析模型输出                          │
│                                                     │
│ • 检测到<tool_use>标签                              │
│ • 提取: 工具名 = filesystem_read                   │
│ • 提取: 参数 = {path: "/home/user/doc.txt"}       │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 6: 应用层通过MCP调用工具                       │
│                                                     │
│ 1. 找到对应的MCP服务器(Filesystem MCP)              │
│                                                     │
│ 2. 通过MCP协议发送请求:                             │
│    {                                                │
│      "method": "tools/call",                        │
│      "params": {                                    │
│        "name": "filesystem_read",                   │
│        "arguments": {                               │
│          "path": "/home/user/doc.txt"              │
│        }                                            │
│      }                                              │
│    }                                                │
│                                                     │
│ 3. Filesystem MCP服务器执行:                        │
│    • 实际读取文件/home/user/doc.txt                 │
│    • 返回文件内容                                   │
│                                                     │
│ 4. MCP返回结果:                                     │
│    {                                                │
│      "content": "文件内容: Hello World..."          │
│    }                                                │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 7: 应用层将结果返回给模型                      │
│                                                     │
│ 添加工具调用结果到对话:                             │
│ [                                                   │
│   ...(前面的消息),                                  │
│   {                                                 │
│     "role": "tool",                                 │
│     "content": "文件内容: Hello World..."           │
│   }                                                 │
│ ]                                                   │
│                                                     │
│ 再次调用模型,让它整合结果                           │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 8: 模型生成最终回答                            │
│                                                     │
│ 模型看到工具返回的内容,生成友好回答:                │
│ "文件内容如下:                                      │
│  Hello World..."                                    │
└─────────────────────────────────────────────────────┘

"""

print(MCP工作流程)
```

---

## 第一部分:MCP是什么?

### 1.1 MCP的定义

```python
MCP定义 = {
    "全称": "Model Context Protocol (模型上下文协议)",

    "是什么": "一个标准化的协议,用于连接LLM应用和外部工具/服务",

    "由谁提出": "Anthropic (Claude的开发商)",

    "解决什么问题": {
        "问题": "每个工具都有自己的API和调用方式,很难统一管理",
        "解决": "统一的协议,让应用能用同样的方式调用不同工具"
    },

    "类比": "就像USB接口,不管什么设备,插上就能用"
}
```

### 1.2 MCP的架构

```python
MCP架构 = """

┌────────────────────────────────────────────────────┐
│ LLM应用层 (CherryStudio / Cursor / Claude Desktop) │
│                                                    │
│ • 用户界面                                         │
│ • 对话管理                                         │
│ • MCP客户端 ← 这是关键!                            │
└────────────────────────────────────────────────────┘
                    ↕ MCP协议 (标准化通信)
┌────────────────────────────────────────────────────┐
│ MCP服务器层 (各种工具的MCP实现)                    │
│                                                    │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ │
│ │Filesystem MCP│ │  Git MCP     │ │PostgreSQL   │ │
│ │              │ │              │ │    MCP      │ │
│ │• read_file   │ │• git_status  │ │• query_db   │ │
│ │• write_file  │ │• git_commit  │ │• insert     │ │
│ │• list_dir    │ │• git_log     │ │• update     │ │
│ └──────────────┘ └──────────────┘ └─────────────┘ │
└────────────────────────────────────────────────────┘
                    ↕
┌────────────────────────────────────────────────────┐
│ 实际工具/服务                                      │
│                                                    │
│ • 文件系统                                         │
│ • Git仓库                                          │
│ • PostgreSQL数据库                                 │
│ • 任何你想集成的工具...                            │
└────────────────────────────────────────────────────┘

⚠️ 关键:
• MCP客户端在应用层,负责管理所有MCP服务器
• MCP服务器是工具的"翻译器",把MCP协议翻译成工具的API
• 应用层通过统一的MCP协议调用所有工具
"""

print(MCP架构)
```

---

## 第二部分:应用层如何配置MCP?

### 2.1 CherryStudio的MCP配置界面

```python
CherryStudio配置界面 = """

┌──────────────────────────────────────────────────────┐
│ CherryStudio - MCP配置                               │
├──────────────────────────────────────────────────────┤
│                                                      │
│ 🔧 已安装的MCP服务器                                 │
│                                                      │
│ ☑ Filesystem MCP                                     │
│   路径: /usr/local/bin/mcp-filesystem               │
│   状态: ● 运行中                                     │
│   提供工具: filesystem_read, filesystem_write, ...   │
│   [配置] [停止] [卸载]                               │
│                                                      │
│ ☑ Git MCP                                            │
│   路径: /usr/local/bin/mcp-git                      │
│   状态: ● 运行中                                     │
│   提供工具: git_status, git_commit, git_log, ...     │
│   [配置] [停止] [卸载]                               │
│                                                      │
│ ☐ PostgreSQL MCP                                     │
│   路径: /usr/local/bin/mcp-postgres                 │
│   状态: ○ 已安装但未启用                             │
│   提供工具: query_db, insert_data, ...               │
│   [启用] [配置] [卸载]                               │
│                                                      │
│ ☐ Puppeteer MCP                                      │
│   状态: 未安装                                       │
│   [安装]                                             │
│                                                      │
│ [+ 添加自定义MCP服务器]                              │
│                                                      │
└──────────────────────────────────────────────────────┘

⚠️ 配置步骤:
1. 安装MCP服务器(npm install -g @modelcontextprotocol/server-filesystem)
2. 在CherryStudio中启用MCP服务器(勾选复选框)
3. 配置参数(如果需要,比如数据库连接字符串)
4. MCP服务器自动启动并连接
"""

print(CherryStudio配置界面)
```

### 2.2 配置文件示例

```json
// CherryStudio的MCP配置文件: ~/.cherry-studio/mcp-config.json
{
  "mcpServers": [
    {
      "name": "filesystem",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user"
      ],
      "enabled": true,
      "env": {}
    },
    {
      "name": "git",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git"
      ],
      "enabled": true,
      "env": {}
    },
    {
      "name": "postgres",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres"
      ],
      "enabled": false,
      "env": {
        "POSTGRES_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  ]
}
```

---

## 第三部分:启用MCP后发生了什么?

### 3.1 应用层的自动化工作

```python
启用MCP后应用层的工作 = {
    "Step 1: 启动MCP服务器": {
        "动作": "应用层启动MCP服务器进程",
        "示例": "执行: npx @modelcontextprotocol/server-filesystem /home/user",
        "结果": "MCP服务器在后台运行,监听MCP协议请求"
    },

    "Step 2: 发现工具": {
        "动作": "应用层通过MCP协议查询服务器提供的工具",
        "MCP请求": {
            "method": "tools/list",
            "params": {}
        },
        "MCP响应": {
            "tools": [
                {
                    "name": "filesystem_read",
                    "description": "读取文件内容",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "文件路径"}
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "filesystem_write",
                    "description": "写入文件",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["path", "content"]
                    }
                }
            ]
        }
    },

    "Step 3: 注册工具到应用": {
        "动作": "应用层将MCP工具注册到内部工具列表",
        "内部数据结构": {
            "available_tools": [
                {
                    "source": "filesystem_mcp",
                    "name": "filesystem_read",
                    "description": "读取文件内容",
                    "parameters": {...}
                },
                {
                    "source": "filesystem_mcp",
                    "name": "filesystem_write",
                    "description": "写入文件",
                    "parameters": {...}
                },
                {
                    "source": "git_mcp",
                    "name": "git_status",
                    "description": "查看Git状态",
                    "parameters": {...}
                }
            ]
        }
    },

    "Step 4: 构建系统提示": {
        "动作": "应用层自动生成包含工具列表的系统提示",
        "生成逻辑": """
        system_prompt = "你是助手,可以使用以下工具:\\n\\n"

        for tool in available_tools:
            system_prompt += f"{tool.name}\\n"
            system_prompt += f"  描述: {tool.description}\\n"
            system_prompt += f"  参数: {tool.parameters}\\n\\n"

        system_prompt += "当需要使用工具时,请输出<tool_use>...</tool_use>"
        """,
        "结果": "每次对话都自动包含这个系统提示(用户看不到)"
    }
}
```

### 3.2 完整代码示例:应用层实现

```python
# ========== CherryStudio内部的MCP客户端实现(简化版) ==========

import subprocess
import json

class MCPClient:
    """MCP客户端:管理MCP服务器和工具调用"""

    def __init__(self):
        self.mcp_servers = {}  # {name: process}
        self.available_tools = []  # 所有可用工具的列表

    def start_mcp_server(self, config):
        """启动MCP服务器"""
        name = config["name"]
        command = config["command"]
        args = config["args"]

        # 启动MCP服务器进程
        process = subprocess.Popen(
            [command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=config.get("env", {})
        )

        self.mcp_servers[name] = {
            "process": process,
            "config": config
        }

        # 发现工具
        tools = self.discover_tools(name)
        self.available_tools.extend(tools)

        print(f"✓ MCP服务器 {name} 已启动")
        print(f"  提供 {len(tools)} 个工具")

    def discover_tools(self, server_name):
        """通过MCP协议发现工具"""
        # 发送MCP请求: tools/list
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }

        response = self.send_mcp_request(server_name, request)

        # 解析工具列表
        tools = []
        for tool_info in response.get("result", {}).get("tools", []):
            tools.append({
                "source": server_name,
                "name": tool_info["name"],
                "description": tool_info["description"],
                "parameters": tool_info["inputSchema"]
            })

        return tools

    def send_mcp_request(self, server_name, request):
        """发送MCP请求"""
        server = self.mcp_servers[server_name]
        process = server["process"]

        # 通过stdin发送JSON请求
        request_json = json.dumps(request) + "\n"
        process.stdin.write(request_json.encode())
        process.stdin.flush()

        # 从stdout读取JSON响应
        response_json = process.stdout.readline().decode()
        response = json.loads(response_json)

        return response

    def build_system_prompt(self):
        """构建包含工具列表的系统提示"""
        prompt = "你是一个智能助手,可以使用以下工具:\n\n"

        for i, tool in enumerate(self.available_tools, 1):
            prompt += f"{i}. {tool['name']}\n"
            prompt += f"   描述: {tool['description']}\n"

            # 添加参数说明
            params = tool['parameters'].get('properties', {})
            if params:
                prompt += "   参数:\n"
                for param_name, param_info in params.items():
                    param_desc = param_info.get('description', '')
                    prompt += f"   - {param_name}: {param_desc}\n"

            prompt += "\n"

        # 添加调用格式说明
        prompt += """当需要使用工具时,请按以下格式输出:

<tool_use>
工具名: tool_name
参数: param1=value1, param2=value2
</tool_use>

现在请处理用户的问题。
"""

        return prompt

    def call_tool(self, tool_name, arguments):
        """调用MCP工具"""
        # 找到工具所属的MCP服务器
        tool = next((t for t in self.available_tools if t["name"] == tool_name), None)

        if not tool:
            return {"error": f"工具 {tool_name} 不存在"}

        server_name = tool["source"]

        # 发送MCP请求: tools/call
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        response = self.send_mcp_request(server_name, request)

        if "result" in response:
            return response["result"]
        else:
            return {"error": response.get("error", "未知错误")}


# ========== 使用示例:CherryStudio的完整流程 ==========

class CherryStudioApp:
    """CherryStudio应用(简化版)"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.mcp_client = MCPClient()

    def load_mcp_config(self):
        """加载并启动MCP服务器"""
        # 读取配置文件
        with open("~/.cherry-studio/mcp-config.json") as f:
            config = json.load(f)

        # 启动所有已启用的MCP服务器
        for server_config in config["mcpServers"]:
            if server_config.get("enabled", False):
                self.mcp_client.start_mcp_server(server_config)

    def handle_user_message(self, user_message):
        """处理用户消息"""
        # Step 1: 构建系统提示(自动包含MCP工具)
        system_prompt = self.mcp_client.build_system_prompt()

        # Step 2: 调用LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        llm_output = response.choices[0].message.content

        # Step 3: 检查是否需要调用工具
        if "<tool_use>" in llm_output:
            # 解析工具调用
            tool_call = self.parse_tool_call(llm_output)

            # 调用MCP工具
            print(f"📞 调用工具: {tool_call['tool_name']}")
            print(f"   参数: {tool_call['arguments']}")

            tool_result = self.mcp_client.call_tool(
                tool_call["tool_name"],
                tool_call["arguments"]
            )

            print(f"   结果: {tool_result}")

            # 将结果返回给LLM
            messages.append({"role": "assistant", "content": llm_output})
            messages.append({
                "role": "tool",
                "content": json.dumps(tool_result, ensure_ascii=False)
            })

            # 再次调用LLM生成最终答案
            final_response = self.llm_client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )

            return final_response.choices[0].message.content
        else:
            # 不需要工具,直接返回
            return llm_output

    def parse_tool_call(self, llm_output):
        """解析LLM输出的工具调用"""
        import re

        # 提取<tool_use>内容
        match = re.search(r'<tool_use>(.*?)</tool_use>', llm_output, re.DOTALL)
        if not match:
            return None

        content = match.group(1)

        # 提取工具名
        tool_match = re.search(r'工具名[:=]\s*(\w+)', content)
        tool_name = tool_match.group(1) if tool_match else None

        # 提取参数(简化版)
        arguments = {}
        param_matches = re.findall(r'(\w+)=([^\n,]+)', content)
        for key, value in param_matches:
            arguments[key.strip()] = value.strip()

        return {
            "tool_name": tool_name,
            "arguments": arguments
        }


# ========== 运行示例 ==========
if __name__ == "__main__":
    import openai

    # 初始化应用
    app = CherryStudioApp(llm_client=openai)

    # 加载MCP配置(启动MCP服务器)
    app.load_mcp_config()

    # 用户提问
    user_question = "读取/home/user/doc.txt文件内容"

    # 处理(自动调用MCP工具)
    result = app.handle_user_message(user_question)

    print(f"\n最终回答: {result}")
```

---

## 第四部分:提示词是怎么加入的?

### 4.1 系统提示的自动注入

```python
提示词注入机制 = {
    "用户看到的": {
        "输入框": "读取/home/user/doc.txt文件内容",
        "看起来": "只是一个简单的问题"
    },

    "实际发送给模型的": {
        "消息数组": [
            {
                "role": "system",
                "content": """你是智能助手,可以使用以下工具:

1. filesystem_read
   描述: 读取文件内容
   参数: path (文件路径)

2. filesystem_write
   描述: 写入文件
   参数: path (文件路径), content (文件内容)

3. git_status
   描述: 查看Git状态
   参数: 无

...

当需要使用工具时,请输出:
<tool_use>
工具名: tool_name
参数: param=value
</tool_use>
"""
            },
            {
                "role": "user",
                "content": "读取/home/user/doc.txt文件内容"
            }
        ]
    },

    "关键点": [
        "系统提示是应用层自动添加的",
        "用户看不到,但模型会收到",
        "每次对话都会自动包含(如果MCP启用)",
        "系统提示告诉模型有哪些工具可用",
        "系统提示告诉模型如何调用工具"
    ]
}
```

### 4.2 完整的消息流

```python
完整消息流示例 = """

用户输入: "读取/home/user/doc.txt文件内容"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第一次调用LLM】

发送给模型的消息:
[
  {
    "role": "system",
    "content": "你是助手,可以使用以下工具:\\n1. filesystem_read\\n描述: 读取文件内容\\n参数: path\\n\\n当需要时输出<tool_use>...</tool_use>"
  },
  {
    "role": "user",
    "content": "读取/home/user/doc.txt文件内容"
  }
]

模型返回:
"好的,让我读取这个文件。
<tool_use>
工具名: filesystem_read
参数: path=/home/user/doc.txt
</tool_use>"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【应用层执行工具调用】

1. 解析模型输出,提取工具调用信息
2. 通过MCP调用filesystem_read
3. 获得结果: {"content": "Hello World!"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【第二次调用LLM】

发送给模型的消息:
[
  {
    "role": "system",
    "content": "你是助手,可以使用以下工具:..."
  },
  {
    "role": "user",
    "content": "读取/home/user/doc.txt文件内容"
  },
  {
    "role": "assistant",
    "content": "好的,让我读取这个文件。<tool_use>...</tool_use>"
  },
  {
    "role": "tool",
    "content": "{\\"content\\": \\"Hello World!\\"}"  ← 工具返回结果
  }
]

模型返回:
"文件内容如下:
Hello World!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

最终展示给用户:
"文件内容如下:
Hello World!"

"""

print(完整消息流示例)
```

---

## 第五部分:MCP vs 普通函数调用

### 5.1 核心区别

```python
MCP_vs_普通函数调用 = {
    "普通函数调用": {
        "定义方式": "在应用代码中硬编码",
        "示例": """
        def get_weather(location):
            # 调用天气API
            return weather_data

        # 在代码中定义工具
        tools = [{
            "name": "get_weather",
            "function": get_weather,
            "parameters": {...}
        }]
        """,
        "优点": "简单,直接",
        "缺点": [
            "每个工具需要单独实现",
            "没有统一标准",
            "难以管理大量工具",
            "不能动态添加/移除工具"
        ]
    },

    "MCP方式": {
        "定义方式": "MCP服务器(独立进程)",
        "示例": """
        # MCP服务器已经实现好,只需启动
        npx @modelcontextprotocol/server-filesystem /home/user

        # 应用层自动发现工具
        # 无需写任何代码!
        """,
        "优点": [
            "标准化协议",
            "工具即插即用",
            "社区共享MCP服务器",
            "可以动态启用/禁用",
            "应用层代码简洁"
        ],
        "缺点": "需要额外的MCP服务器进程"
    }
}
```

### 5.2 MCP的核心价值

```python
MCP核心价值 = {
    "1. 标准化": {
        "问题": "以前每个工具都有自己的API,应用层需要分别适配",
        "MCP解决": "统一的协议,应用层只需实现一次MCP客户端"
    },

    "2. 可复用": {
        "问题": "每个应用都要实现自己的文件操作、Git操作等",
        "MCP解决": "社区提供标准MCP服务器,所有应用共享"
    },

    "3. 可扩展": {
        "问题": "添加新工具需要修改应用代码",
        "MCP解决": "只需启用相应的MCP服务器,无需改代码"
    },

    "4. 隔离性": {
        "问题": "工具代码和应用代码混在一起",
        "MCP解决": "MCP服务器独立进程,崩溃不影响应用"
    }
}
```

---

## 第六部分:常见MCP服务器示例

### 6.1 官方MCP服务器

```python
官方MCP服务器 = {
    "Filesystem MCP": {
        "提供工具": [
            "read_file - 读取文件",
            "write_file - 写入文件",
            "list_directory - 列出目录",
            "search_files - 搜索文件",
            "get_file_info - 获取文件信息"
        ],
        "安装": "npm install -g @modelcontextprotocol/server-filesystem",
        "启动": "npx @modelcontextprotocol/server-filesystem /home/user",
        "用途": "让LLM能读写文件系统"
    },

    "Git MCP": {
        "提供工具": [
            "git_status - 查看状态",
            "git_diff - 查看差异",
            "git_log - 查看历史",
            "git_commit - 提交更改",
            "git_branch - 分支操作"
        ],
        "安装": "npm install -g @modelcontextprotocol/server-git",
        "启动": "npx @modelcontextprotocol/server-git",
        "用途": "让LLM能操作Git仓库"
    },

    "PostgreSQL MCP": {
        "提供工具": [
            "query - 执行SQL查询",
            "list_tables - 列出表",
            "describe_table - 查看表结构",
            "insert - 插入数据",
            "update - 更新数据"
        ],
        "安装": "npm install -g @modelcontextprotocol/server-postgres",
        "启动": "npx @modelcontextprotocol/server-postgres",
        "环境变量": "POSTGRES_URL=postgresql://...",
        "用途": "让LLM能查询数据库"
    },

    "Puppeteer MCP": {
        "提供工具": [
            "navigate - 打开网页",
            "screenshot - 截图",
            "click - 点击元素",
            "fill - 填写表单",
            "extract - 提取数据"
        ],
        "安装": "npm install -g @modelcontextprotocol/server-puppeteer",
        "用途": "让LLM能控制浏览器"
    }
}
```

---

## 总结:一句话理解

**MCP是标准化的工具协议,应用层启用MCP服务器后,自动发现工具并注入到系统提示中,模型通过提示词"知道"这些工具,应用层解析模型输出并通过MCP调用实际工具!**

### 完整流程口诀

```
MCP工作流程五步走:

1. 配置启用: 在应用中启用MCP服务器
2. 自动发现: 应用通过MCP协议获取工具列表
3. 注入提示: 应用自动生成系统提示(包含工具列表)
4. 模型决策: 模型看到提示,决定调用哪个工具
5. MCP执行: 应用解析输出,通过MCP调用实际工具

关键: 用户看不到系统提示,但模型能看到!
```

### 核心理解

```
MCP = 统一的工具协议 + 即插即用 + 标准化

应用层的自动化:
├─ 启动MCP服务器
├─ 发现工具列表
├─ 构建系统提示
├─ 注入到对话
└─ 解析和调用

模型的视角:
├─ 看到系统提示(自动添加的)
├─ 知道有哪些工具可用
├─ 决定调用哪个工具
└─ 输出工具调用指令

用户的视角:
├─ 只看到自己的输入和最终回答
├─ 不知道系统提示的存在
└─ 不知道中间的工具调用过程
```

---

**现在你应该完全明白MCP在整个系统中的应用机制了!** 🎯
