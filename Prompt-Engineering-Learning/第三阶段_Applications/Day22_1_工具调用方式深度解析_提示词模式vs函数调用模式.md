# Day22_2 - 工具调用方式深度解析:提示词模式 vs 函数调用模式

**学习日期**: 2025-11-08
**阶段**: 第三阶段 - Applications (实际应用深度扩展)
**重要程度**: ⭐⭐⭐⭐⭐ **关键配置理解!**

---

## 你的困惑(纠正老王我之前的误解)

你在CherryStudio等应用的**模型设置**中发现:

```
工具调用方式(Tool Call Mode):
├─ 提示词调用 (Prompt-based) ← 默认选项
└─ 函数调用 (Function Calling)
```

这个配置是什么意思?为什么有两种模式?和之前Day22_1说的不是一回事!

**老王我现在明白了**:这是**同一个工具,两种不同的调用实现方式**!

---

## 核心概念:一句话理解

```
工具调用方式 = 当LLM需要使用外部工具时,如何"告诉工具该做什么"

提示词模式(Prompt-based):
  LLM生成自然语言描述 → 应用解析 → 调用工具

函数调用模式(Function Calling):
  LLM生成JSON格式参数 → 应用解析 → 调用工具

目标相同: 都是调用外部工具
实现不同: 用自然语言 vs 用JSON格式
```

---

## 第一部分:问题重新理解

### 1.1 CherryStudio的完整架构

```python
CherryStudio完整架构 = """

┌──────────────────────────────────────────────────────────┐
│ CherryStudio 应用架构                                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ ┌──────────────────────────────────────────────────┐    │
│ │ 1. 模型配置 (Model Configuration)                │    │
│ │                                                  │    │
│ │ • API地址: https://api.openai.com/v1            │    │
│ │ • API密钥: sk-xxxxx                             │    │
│ │ • 模型名称: gpt-4                               │    │
│ │                                                  │    │
│ │ ⚙️ 工具调用方式(Tool Call Mode):                │    │
│ │   ├─ 📝 提示词调用 (Prompt-based) ← 默认        │    │
│ │   └─ 🔧 函数调用 (Function Calling)             │    │
│ └──────────────────────────────────────────────────┘    │
│                                                          │
│ ┌──────────────────────────────────────────────────┐    │
│ │ 2. 工具/增强能力 (Tools/Enhancements)            │    │
│ │                                                  │    │
│ │ • 知识库 (Knowledge Base)                       │    │
│ │ • MCP服务器 (MCP Servers)                       │    │
│ │ • 自定义工具 (Custom Tools)                     │    │
│ │ • 插件系统 (Plugins)                            │    │
│ └──────────────────────────────────────────────────┘    │
│                                                          │
│            当用户需要使用工具时                          │
│                     ↓                                    │
│         根据"工具调用方式"决定如何调用                   │
│                     ↓                                    │
│        ┌────────────┴────────────┐                      │
│        ↓                         ↓                       │
│   提示词模式              函数调用模式                   │
│   (默认)                  (可选)                         │
└──────────────────────────────────────────────────────────┘

"""

print(CherryStudio完整架构)
```

### 1.2 关键理解

```python
关键理解 = {
    "老王我之前的误解": {
        "Day22_1错误理解": "认为是'调用模板'和'调用工具'两种不同的东西",
        "实际情况": "都是在调用外部工具,只是实现方式不同!"
    },

    "正确理解": {
        "目标": "都是为了让LLM使用外部工具(知识库、MCP、计算器等)",
        "区别": "如何'描述工具调用'的格式不同",
        "类比": "就像寄快递,目的都是寄东西,但可以'口头告诉快递员'或'填写电子单据'"
    },

    "配置项的含义": {
        "提示词调用(默认)": "LLM用自然语言描述想调用什么工具,应用解析这段话",
        "函数调用": "LLM按JSON格式输出工具调用参数,应用直接解析JSON"
    }
}
```

---

## 第二部分:两种工具调用方式的详细对比

### 2.1 提示词调用模式(Prompt-based Tool Calling)

```python
提示词模式工作流程 = """

用户: "查询今天的天气"
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 1: CherryStudio准备系统提示                    │
│                                                     │
│ 系统提示:                                           │
│ "你可以使用以下工具:                                │
│  - get_weather: 查询天气,需要参数location          │
│  - search_web: 搜索网页,需要参数query              │
│  - query_kb: 查询知识库,需要参数question           │
│                                                     │
│  当你需要使用工具时,按以下格式输出:                 │
│  <tool_use>                                         │
│  工具名: get_weather                                │
│  参数: location=北京                                │
│  </tool_use>                                        │
│  或者用更自然的方式说明你要使用什么工具"            │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: LLM生成响应(自然语言描述)                   │
│                                                     │
│ LLM输出:                                            │
│ "我需要使用get_weather工具来查询天气。             │
│  <tool_use>                                         │
│  工具名: get_weather                                │
│  参数: location=北京                                │
│  </tool_use>"                                       │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: CherryStudio解析LLM输出                     │
│                                                     │
│ • 检测到<tool_use>标签                              │
│ • 提取工具名: get_weather                          │
│ • 提取参数: location=北京                          │
│ • (需要应用自己解析这段文本!)                       │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: 调用实际工具                                │
│                                                     │
│ result = get_weather(location="北京")               │
│ # 返回: {"temperature": 15, "condition": "晴"}     │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: 将结果返回给LLM,LLM生成最终答案             │
│                                                     │
│ "北京今天天气晴朗,温度15℃,适合出行。"               │
└─────────────────────────────────────────────────────┘

⚠️ 关键特点:
1. LLM输出自然语言 + 特殊标签(如<tool_use>)
2. 应用需要解析LLM输出的文本
3. 格式灵活,但解析复杂
4. 兼容性好(所有LLM都能输出文本)
"""

print(提示词模式工作流程)
```

### 2.2 函数调用模式(Function Calling Mode)

```python
函数调用模式工作流程 = """

用户: "查询今天的天气"
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 1: CherryStudio准备函数定义                    │
│                                                     │
│ tools = [                                           │
│     {                                               │
│         "type": "function",                         │
│         "function": {                               │
│             "name": "get_weather",                  │
│             "description": "查询天气",              │
│             "parameters": {                         │
│                 "type": "object",                   │
│                 "properties": {                     │
│                     "location": {"type": "string"}  │
│                 },                                  │
│                 "required": ["location"]            │
│             }                                       │
│         }                                           │
│     }                                               │
│ ]                                                   │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 2: 调用LLM(传入函数定义)                       │
│                                                     │
│ response = llm.chat.completions.create(             │
│     model="gpt-4",                                  │
│     messages=[{"role": "user", "content": "查询天气"}],│
│     tools=tools  # ← 传入函数定义                   │
│ )                                                   │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 3: LLM生成结构化JSON响应                       │
│                                                     │
│ {                                                   │
│     "tool_calls": [                                 │
│         {                                           │
│             "id": "call_123",                       │
│             "type": "function",                     │
│             "function": {                           │
│                 "name": "get_weather",              │
│                 "arguments": "{\"location\":\"北京\"}"│
│             }                                       │
│         }                                           │
│     ]                                               │
│ }                                                   │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 4: CherryStudio直接解析JSON                    │
│                                                     │
│ • 直接读取tool_calls数组                            │
│ • 提取function.name: "get_weather"                 │
│ • 解析function.arguments: {"location": "北京"}     │
│ • (JSON格式,无需复杂解析!)                          │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 5: 调用实际工具                                │
│                                                     │
│ result = get_weather(location="北京")               │
│ # 返回: {"temperature": 15, "condition": "晴"}     │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│ Step 6: 将结果返回给LLM,LLM生成最终答案             │
│                                                     │
│ "北京今天天气晴朗,温度15℃,适合出行。"               │
└─────────────────────────────────────────────────────┘

⚠️ 关键特点:
1. LLM输出标准JSON格式
2. 应用直接解析JSON(简单!)
3. 格式严格,但可靠
4. 需要LLM支持(如GPT-4、Claude等)
"""

print(函数调用模式工作流程)
```

### 2.3 核心区别对比表

```python
核心区别 = {
    "LLM输出格式": {
        "提示词模式": "自然语言 + 特殊标签(如<tool_use>工具名:xxx</tool_use>)",
        "函数调用模式": "标准JSON格式({\"tool_calls\": [{\"function\": {...}}]})"
    },

    "应用解析难度": {
        "提示词模式": "复杂(需要文本解析、正则匹配、标签提取)",
        "函数调用模式": "简单(直接JSON.parse())"
    },

    "可靠性": {
        "提示词模式": "较低(LLM可能不按格式输出、标签错误、参数格式不对)",
        "函数调用模式": "高(LLM经过专门训练,输出格式严格)"
    },

    "兼容性": {
        "提示词模式": "高(所有LLM都能用,包括本地小模型)",
        "函数调用模式": "中等(需要LLM支持Function Calling,如GPT-4、Claude、Gemini)"
    },

    "性能": {
        "提示词模式": "可能需要多次尝试才能正确解析",
        "函数调用模式": "一次调用通常就能成功"
    },

    "应用实现成本": {
        "提示词模式": "高(需要写复杂的文本解析逻辑)",
        "函数调用模式": "低(直接用API提供的结构化数据)"
    }
}
```

---

## 第三部分:为什么提示词模式是默认?

### 3.1 默认选择的原因

```python
为什么默认提示词模式 = {
    "原因1: 兼容性": {
        "说明": "不是所有模型都支持Function Calling",
        "示例": [
            "✓ GPT-4, GPT-3.5-turbo支持Function Calling",
            "✓ Claude 3支持Function Calling",
            "✓ Gemini Pro支持Function Calling",
            "✗ 本地小模型(Llama 7B等)通常不支持",
            "✗ 旧版模型不支持"
        ],
        "提示词模式优势": "所有模型都能用!只要能输出文本就行"
    },

    "原因2: 降低门槛": {
        "说明": "用户不需要了解Function Calling的复杂概念",
        "用户体验": "直接使用,无需学习JSON格式、参数定义等"
    },

    "原因3: 灵活性": {
        "说明": "提示词模式更灵活,可以自定义标签格式",
        "示例": "可以用<tool_use>、【工具调用】、或其他自定义标记"
    },

    "原因4: 成本考虑": {
        "说明": "支持Function Calling的API通常更贵",
        "对比": [
            "GPT-4(支持FC): $0.03/1K tokens",
            "GPT-3.5-turbo(支持FC): $0.002/1K tokens",
            "本地模型(提示词模式): 免费"
        ]
    }
}
```

### 3.2 什么时候应该切换到函数调用模式?

```python
切换到函数调用模式的场景 = {
    "场景1: 使用支持FC的高级模型": {
        "条件": "模型是GPT-4、Claude 3、Gemini Pro等",
        "原因": "这些模型经过Function Calling训练,输出更可靠",
        "建议": "强烈推荐切换!"
    },

    "场景2: 需要高可靠性": {
        "条件": "工具调用不能出错(如金融交易、医疗决策)",
        "原因": "函数调用模式格式严格,错误率低",
        "建议": "必须使用函数调用模式"
    },

    "场景3: 复杂参数结构": {
        "条件": "工具参数复杂(嵌套对象、数组等)",
        "示例": """
        {
            "user": {
                "name": "张三",
                "preferences": {
                    "tags": ["科技", "AI"],
                    "max_results": 10
                }
            }
        }
        """,
        "原因": "JSON格式天然支持复杂结构,提示词模式难以解析",
        "建议": "使用函数调用模式"
    },

    "场景4: 多工具调用": {
        "条件": "一次需要调用多个工具",
        "原因": "函数调用模式可以返回多个tool_calls,清晰明确",
        "建议": "使用函数调用模式"
    },

    "保持提示词模式的场景": {
        "场景1": "使用本地小模型(不支持FC)",
        "场景2": "对可靠性要求不高的简单任务",
        "场景3": "成本敏感,用便宜的模型",
        "场景4": "快速原型开发"
    }
}
```

---

## 第四部分:实际代码对比

### 4.1 提示词模式的应用实现

```python
class PromptBasedToolCaller:
    """提示词模式的工具调用实现"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.available_tools = {
            "get_weather": self.get_weather,
            "search_web": self.search_web,
            "query_kb": self.query_kb
        }

    def create_system_prompt(self):
        """创建系统提示,告诉LLM如何使用工具"""
        tools_description = """
你可以使用以下工具:

1. get_weather - 查询天气
   参数: location (城市名)

2. search_web - 搜索网页
   参数: query (搜索关键词)

3. query_kb - 查询知识库
   参数: question (问题)

当你需要使用工具时,请按以下格式输出:

<tool_use>
工具名: get_weather
参数: location=北京
</tool_use>

你可以先思考是否需要使用工具,再决定。
"""
        return tools_description

    def parse_tool_call(self, llm_response):
        """解析LLM输出,提取工具调用信息"""
        import re

        # 使用正则表达式提取<tool_use>标签内容
        pattern = r'<tool_use>(.*?)</tool_use>'
        matches = re.findall(pattern, llm_response, re.DOTALL)

        if not matches:
            return None  # 没有工具调用

        tool_calls = []
        for match in matches:
            # 提取工具名
            tool_name_match = re.search(r'工具名[:=]\s*(\w+)', match)
            if not tool_name_match:
                continue

            tool_name = tool_name_match.group(1)

            # 提取参数(简化版,实际需要更复杂的解析)
            params = {}
            param_matches = re.findall(r'(\w+)=([^\n]+)', match)
            for key, value in param_matches:
                params[key.strip()] = value.strip()

            tool_calls.append({
                "tool_name": tool_name,
                "parameters": params
            })

        return tool_calls

    def handle_query(self, user_query):
        """处理用户查询"""
        # 准备消息
        messages = [
            {"role": "system", "content": self.create_system_prompt()},
            {"role": "user", "content": user_query}
        ]

        # 调用LLM
        response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        llm_output = response.choices[0].message.content

        print(f"LLM输出:\n{llm_output}\n")

        # 解析工具调用
        tool_calls = self.parse_tool_call(llm_output)

        if not tool_calls:
            # 不需要工具,直接返回
            return llm_output

        # 执行工具调用
        tool_results = []
        for tool_call in tool_calls:
            tool_name = tool_call["tool_name"]
            params = tool_call["parameters"]

            print(f"📞 调用工具: {tool_name}")
            print(f"   参数: {params}")

            if tool_name in self.available_tools:
                result = self.available_tools[tool_name](**params)
                tool_results.append({
                    "tool": tool_name,
                    "result": result
                })
                print(f"   结果: {result}\n")

        # 将结果返回给LLM,生成最终答案
        messages.append({"role": "assistant", "content": llm_output})
        messages.append({
            "role": "user",
            "content": f"工具调用结果: {tool_results}\n请基于这些结果回答我的问题。"
        })

        final_response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        return final_response.choices[0].message.content

    # 工具实现(模拟)
    def get_weather(self, location):
        return f"{location}天气: 晴,15℃"

    def search_web(self, query):
        return f"搜索'{query}'的结果..."

    def query_kb(self, question):
        return f"知识库查询'{question}'的答案..."


# 使用
# caller = PromptBasedToolCaller(llm_client)
# result = caller.handle_query("北京今天天气怎么样?")
```

### 4.2 函数调用模式的应用实现

```python
class FunctionCallingToolCaller:
    """函数调用模式的工具调用实现"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.available_tools = {
            "get_weather": self.get_weather,
            "search_web": self.search_web,
            "query_kb": self.query_kb
        }

    def get_tools_definition(self):
        """获取工具的函数定义(OpenAI格式)"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "查询指定城市的天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市名,如:北京"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "搜索网页内容",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_kb",
                    "description": "查询知识库",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "要查询的问题"
                            }
                        },
                        "required": ["question"]
                    }
                }
            }
        ]

    def handle_query(self, user_query):
        """处理用户查询"""
        import json

        # 准备消息
        messages = [
            {"role": "user", "content": user_query}
        ]

        # 调用LLM(传入工具定义)
        response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=self.get_tools_definition()  # ← 传入函数定义
        )

        message = response.choices[0].message

        # 检查是否有工具调用
        if not message.tool_calls:
            # 不需要工具,直接返回
            return message.content

        print("✅ LLM决定调用工具(JSON格式):\n")

        # 执行工具调用
        for tool_call in message.tool_calls:
            # 直接从JSON中提取信息(无需复杂解析!)
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"📞 调用工具: {tool_name}")
            print(f"   参数(JSON): {tool_args}")

            if tool_name in self.available_tools:
                result = self.available_tools[tool_name](**tool_args)
                print(f"   结果: {result}\n")

                # 将结果添加到对话
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        # 再次调用LLM,整合结果
        final_response = self.llm_client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        return final_response.choices[0].message.content

    # 工具实现(与上面相同)
    def get_weather(self, location):
        return {"location": location, "condition": "晴", "temperature": "15℃"}

    def search_web(self, query):
        return {"query": query, "results": ["结果1", "结果2"]}

    def query_kb(self, question):
        return {"question": question, "answer": "答案..."}


# 使用
# caller = FunctionCallingToolCaller(llm_client)
# result = caller.handle_query("北京今天天气怎么样?")
```

### 4.3 代码对比总结

```python
代码对比 = {
    "提示词模式": {
        "复杂度": "高",
        "代码行数": "~150行(包含复杂的文本解析逻辑)",
        "关键难点": [
            "需要写正则表达式解析<tool_use>标签",
            "需要手动解析参数字符串",
            "需要处理各种格式错误",
            "需要考虑LLM可能不按格式输出的情况"
        ],
        "维护成本": "高(格式变化需要修改解析逻辑)"
    },

    "函数调用模式": {
        "复杂度": "低",
        "代码行数": "~80行(直接用JSON)",
        "关键优势": [
            "直接用json.loads()解析",
            "参数自动提取,格式标准",
            "LLM输出可靠,错误率低",
            "API提供了tool_calls结构,直接使用"
        ],
        "维护成本": "低(API保证格式稳定)"
    }
}
```

---

## 第五部分:CherryStudio中的实际配置和使用

### 5.1 配置界面说明

```python
CherryStudio配置界面 = """

┌──────────────────────────────────────────────────────┐
│ 模型配置 (Model Settings)                           │
├──────────────────────────────────────────────────────┤
│                                                      │
│ 📡 API配置                                           │
│   • API地址: [https://api.openai.com/v1        ]   │
│   • API密钥: [sk-xxxxxxxxxxxxxxxxxxxxxxxx      ]   │
│   • 模型名称: [gpt-4                            ]   │
│                                                      │
│ ⚙️ 工具调用方式 (Tool Call Mode)                    │
│   ● 提示词调用 (Prompt-based) ← 默认                │
│   ○ 函数调用 (Function Calling)                     │
│                                                      │
│   说明:                                              │
│   • 提示词调用: 兼容所有模型,包括本地模型           │
│   • 函数调用: 需要模型支持(GPT-4/Claude 3等)        │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│ 🔧 可用工具/增强 (Available Tools)                   │
│                                                      │
│ ☑ 知识库 (Knowledge Base)                           │
│   • MyDocs库 (1000个文档)                           │
│   • TechNotes库 (500个笔记)                         │
│                                                      │
│ ☑ MCP服务器 (MCP Servers)                           │
│   • Filesystem MCP (文件操作)                       │
│   • Git MCP (Git操作)                               │
│   • PostgreSQL MCP (数据库查询)                     │
│                                                      │
│ ☑ 自定义工具 (Custom Tools)                         │
│   • Weather API (天气查询)                          │
│   • Calculator (计算器)                             │
│                                                      │
└──────────────────────────────────────────────────────┘

⚠️ 关键:
无论选择哪种"工具调用方式",都是在调用下面的"可用工具"!
区别只是"如何告诉这些工具该做什么"的格式不同!

"""

print(CherryStudio配置界面)
```

### 5.2 实际使用场景演示

```python
实际使用场景 = """

场景: 用户查询天气并搜索相关信息

用户输入: "查询北京天气,并搜索一下今天有什么重要新闻"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【提示词调用模式】的处理流程:

Step 1: CherryStudio发送给LLM
  系统提示: "你有get_weather和search_web两个工具..."
  用户消息: "查询北京天气,并搜索今天新闻"

Step 2: LLM返回
  "我需要先查天气,再搜索新闻。
   <tool_use>
   工具名: get_weather
   参数: location=北京
   </tool_use>
   <tool_use>
   工具名: search_web
   参数: query=今天重要新闻
   </tool_use>"

Step 3: CherryStudio解析
  • 正则匹配<tool_use>标签
  • 提取两个工具调用
  • 手动解析参数字符串
  • (代码复杂,可能出错)

Step 4: 执行工具
  • 调用get_weather(location="北京")
  • 调用search_web(query="今天重要新闻")

Step 5: 返回结果给LLM,生成最终答案

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【函数调用模式】的处理流程:

Step 1: CherryStudio发送给LLM
  工具定义(JSON格式): [
    {"function": {"name": "get_weather", ...}},
    {"function": {"name": "search_web", ...}}
  ]
  用户消息: "查询北京天气,并搜索今天新闻"

Step 2: LLM返回(标准JSON)
  {
    "tool_calls": [
      {
        "id": "call_1",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\":\"北京\"}"
        }
      },
      {
        "id": "call_2",
        "function": {
          "name": "search_web",
          "arguments": "{\"query\":\"今天重要新闻\"}"
        }
      }
    ]
  }

Step 3: CherryStudio解析
  • 直接JSON.parse()
  • 遍历tool_calls数组
  • 提取name和arguments
  • (代码简单,可靠!)

Step 4: 执行工具(与上面相同)

Step 5: 返回结果给LLM,生成最终答案

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

对比:
• 目标相同: 都调用get_weather和search_web
• LLM输出: 文本 vs JSON
• 解析复杂度: 高 vs 低
• 可靠性: 中 vs 高

"""

print(实际使用场景)
```

---

## 第六部分:MCP和知识库如何融入?

### 6.1 MCP(Model Context Protocol)的角色

```python
MCP在工具调用中的角色 = {
    "MCP是什么": "统一的工具/服务接口协议,让LLM能调用各种外部服务",

    "MCP提供的工具": [
        "Filesystem MCP - 文件系统操作(读写文件、列目录)",
        "Git MCP - Git操作(查看历史、创建分支、提交代码)",
        "PostgreSQL MCP - 数据库查询",
        "Puppeteer MCP - 网页自动化",
        "...其他MCP服务器"
    ],

    "MCP如何被调用": {
        "提示词模式": """
        LLM输出:
        <tool_use>
        工具名: filesystem_read
        参数: path=/home/user/doc.txt
        </tool_use>

        → CherryStudio解析 → 调用Filesystem MCP → 返回文件内容
        """,

        "函数调用模式": """
        LLM输出(JSON):
        {
          "tool_calls": [{
            "function": {
              "name": "filesystem_read",
              "arguments": "{\"path\":\"/home/user/doc.txt\"}"
            }
          }]
        }

        → CherryStudio解析 → 调用Filesystem MCP → 返回文件内容
        """
    },

    "关键理解": "MCP只是提供工具,'工具调用方式'决定如何让LLM使用这些MCP工具!"
}
```

### 6.2 知识库的角色

```python
知识库在工具调用中的角色 = {
    "知识库是什么": "向量数据库,存储文档/笔记,支持语义搜索",

    "知识库作为工具": {
        "工具名": "query_knowledge_base 或 search_docs",
        "功能": "根据用户问题,搜索最相关的文档片段",
        "实现": "向量化查询 → 余弦相似度 → 返回Top-K文档"
    },

    "如何被调用": {
        "提示词模式": """
        用户: "Transformer的注意力机制是什么?"

        LLM输出:
        <tool_use>
        工具名: query_kb
        参数: question=Transformer注意力机制
        </tool_use>

        → CherryStudio调用知识库 → 返回相关文档 → LLM生成答案
        """,

        "函数调用模式": """
        用户: "Transformer的注意力机制是什么?"

        LLM输出(JSON):
        {
          "tool_calls": [{
            "function": {
              "name": "query_kb",
              "arguments": "{\"question\":\"Transformer注意力机制\"}"
            }
          }]
        }

        → CherryStudio调用知识库 → 返回相关文档 → LLM生成答案
        """
    },

    "关键理解": "知识库也是一种工具,'工具调用方式'决定LLM如何描述查询需求!"
}
```

---

## 总结:一句话理解

**工具调用方式(Tool Call Mode)是指:当LLM需要使用外部工具(知识库、MCP、API等)时,用哪种格式告诉应用"我要调用什么工具,参数是什么"!**

### 核心对比

```
提示词调用(默认):
  LLM用自然语言+特殊标签描述 → 应用解析文本 → 调用工具
  优点: 兼容所有模型
  缺点: 解析复杂,可靠性较低

函数调用:
  LLM用标准JSON格式输出 → 应用解析JSON → 调用工具
  优点: 简单可靠,格式严格
  缺点: 需要模型支持Function Calling
```

### 记忆口诀

```
工具调用方式 = LLM怎么告诉应用"调用什么工具"

提示词模式: 说自然语言,应用自己理解
函数调用模式: 说标准JSON,应用直接读取

目标相同: 都是调用工具(MCP、知识库、API)
格式不同: 文本 vs JSON
```

### 配置建议

```
使用GPT-4/Claude 3等高级模型?
  → 切换到"函数调用模式" (可靠性高!)

使用本地模型或旧版模型?
  → 保持"提示词调用模式" (兼容性好!)

不确定?
  → 保持默认"提示词调用模式" (保险!)
```

---

**现在你应该完全明白CherryStudio中"工具调用方式"这个配置的含义了!**

这不是"调用模板"和"调用工具"两种东西,而是**同一个目标(调用工具),两种不同的实现方式(文本描述 vs JSON格式)**!🎯
