# Day22 - Function Calling(函数调用):让LLM调用外部工具

**学习日期**: 2025-11-08
**阶段**: 第三阶段 - Applications (实际应用)
**重要程度**: ⭐⭐⭐⭐⭐ **核心能力!**

---

## 你的困惑

你学完了Day6-Day22的所有**技术**(Techniques),现在进入**应用**(Applications)阶段。第一个应用就是**Function Calling(函数调用)**。你可能在想:这TM是什么?和前面学的ReAct、PAL有什么关系?

**老王我告诉你**:Function Calling就是让LLM能够**调用外部工具和API**的能力!它是构建实用AI应用的**核心基础**!

---

## 核心概念:一句话解释

**Function Calling(函数调用)**就是:
```
用户问题 → LLM理解并决定调用哪个函数 → 输出函数调用参数(JSON) → 执行函数 → LLM整合结果 → 最终答案
```

**本质**:LLM不直接执行函数,而是**理解意图**并**生成调用参数**,由外部系统执行!

---

## 第一部分:Function Calling是什么?

### 1.1 定义和核心能力

```python
Function_Calling定义 = {
    "是什么": "可靠地将LLM连接到外部工具的能力",

    "LLM的角色": {
        "不是": "直接执行函数/调用API",
        "而是": "理解用户意图 → 决定调用哪个函数 → 生成调用参数(JSON格式)"
    },

    "实际执行": "由外部系统/代码执行函数调用",

    "完整流程": [
        "1. 用户提问",
        "2. LLM分析问题,决定需要调用哪个函数",
        "3. LLM输出JSON格式的函数调用参数",
        "4. 外部系统执行函数调用",
        "5. 将结果返回给LLM",
        "6. LLM整合结果,生成最终答案"
    ]
}
```

### 1.2 为什么需要Function Calling?

**LLM的局限性**:
```python
LLM的限制 = {
    "训练数据截止": "只知道截止日期之前的信息,无法获取最新数据",
    "没有网络访问": "无法主动访问互联网、数据库、API",
    "无法执行动作": "无法发送邮件、订票、下单等实际操作",
    "计算不精确": "复杂数学计算可能出错"
}

# 示例:用户问题LLM无法直接回答
无法回答的问题 = [
    "伦敦现在的天气如何?",        # ✗ 需要实时天气API
    "我的账户余额是多少?",        # ✗ 需要数据库查询
    "帮我订一张明天去北京的机票",  # ✗ 需要调用订票API
    "计算35628 × 89453的精确值"  # ✗ 需要精确计算工具
]

# Function Calling的解决方案
Function_Calling解决方案 = {
    "实时数据": "调用天气API获取最新天气",
    "私有数据": "调用数据库查询接口获取用户数据",
    "执行动作": "调用订票系统API完成订票",
    "精确计算": "调用计算器工具进行精确计算"
}
```

### 1.3 Function Calling vs 之前学过的技术

```python
技术对比 = {
    "PAL (Day18)": {
        "相似点": "都需要外部执行器",
        "区别": {
            "PAL": "LLM生成代码(Python等) → 代码执行器执行",
            "Function Calling": "LLM生成函数调用参数(JSON) → 函数执行器执行"
        },
        "示例": {
            "PAL": "LLM生成'radius=5; area=math.pi*radius**2' → Python执行",
            "Function Calling": "LLM生成'{\"location\":\"London\"}' → 调用get_weather()函数"
        }
    },

    "ReAct (Day19)": {
        "相似点": "都是'推理+行动'模式",
        "区别": {
            "ReAct": "通用框架,Thought→Action→Observation循环",
            "Function Calling": "ReAct的Action层的具体实现方式"
        },
        "关系": "Function Calling是ReAct中'Action'的一种标准化实现"
    },

    "Retrieval Augmented Generation (Day13)": {
        "相似点": "都需要外部知识源",
        "区别": {
            "RAG": "主要是检索文档/知识库",
            "Function Calling": "更广泛,可调用任何外部工具/API/服务"
        }
    }
}
```

---

## 第二部分:Function Calling的完整工作流程

### 2.1 完整流程图

```python
Function_Calling完整流程 = """

┌──────────────────────────────────────────────────────────┐
│ Step 1: 用户提问                                         │
│ 用户: "伦敦现在的天气如何?"                              │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 2: 定义可用函数(开发者预先定义)                    │
│                                                          │
│ tools = [                                                │
│     {                                                    │
│         "type": "function",                              │
│         "function": {                                    │
│             "name": "get_current_weather",               │
│             "description": "获取指定地点的当前天气",      │
│             "parameters": {                              │
│                 "type": "object",                        │
│                 "properties": {                          │
│                     "location": {                        │
│                         "type": "string",                │
│                         "description": "城市名,如London"  │
│                     },                                   │
│                     "unit": {                            │
│                         "type": "string",                │
│                         "enum": ["celsius", "fahrenheit"]│
│                     }                                    │
│                 },                                       │
│                 "required": ["location"]                 │
│             }                                            │
│         }                                                │
│     }                                                    │
│ ]                                                        │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 3: LLM分析并决定调用函数                           │
│                                                          │
│ LLM内部推理过程(不可见):                                │
│ • 用户问的是"伦敦天气"                                   │
│ • 我有一个get_current_weather函数可用                   │
│ • 这个函数需要location参数                              │
│ • 从问题中提取location="London"                         │
│ • 单位默认用celsius(摄氏度)                             │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 4: LLM输出函数调用参数(JSON格式)                   │
│                                                          │
│ {                                                        │
│     "tool_calls": [                                      │
│         {                                                │
│             "id": "call_123",                            │
│             "type": "function",                          │
│             "function": {                                │
│                 "name": "get_current_weather",           │
│                 "arguments": "{                          │
│                     \"location\": \"London\",            │
│                     \"unit\": \"celsius\"                │
│                 }"                                       │
│             }                                            │
│         }                                                │
│     ]                                                    │
│ }                                                        │
│                                                          │
│ ⚠️ 关键: LLM只生成JSON,不执行函数!                       │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 5: 外部系统执行函数调用(开发者代码)                │
│                                                          │
│ # 解析LLM的输出                                          │
│ function_name = "get_current_weather"                    │
│ arguments = {"location": "London", "unit": "celsius"}   │
│                                                          │
│ # 调用实际的API或函数                                    │
│ if function_name == "get_current_weather":               │
│     weather = call_weather_api(arguments["location"])    │
│                                                          │
│ # 假设API返回:                                           │
│ weather_result = {                                       │
│     "location": "London",                                │
│     "temperature": 15,                                   │
│     "unit": "celsius",                                   │
│     "condition": "Cloudy",                               │
│     "humidity": 65                                       │
│ }                                                        │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 6: 将结果返回给LLM                                  │
│                                                          │
│ messages.append({                                        │
│     "role": "function",                                  │
│     "name": "get_current_weather",                       │
│     "content": json.dumps(weather_result)                │
│ })                                                       │
│                                                          │
│ # 再次调用LLM,让它整合结果                               │
│ final_response = openai.chat.completions.create(...)     │
└──────────────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────────────┐
│ Step 7: LLM生成最终用户友好的回答                       │
│                                                          │
│ "伦敦当前天气为多云,温度15摄氏度,湿度65%。建议出门携带外套!" │
└──────────────────────────────────────────────────────────┘

"""

print(Function_Calling完整流程)
```

### 2.2 核心要点

```python
关键理解 = {
    "LLM的职责": {
        "✓ 做的事": [
            "理解用户意图",
            "决定需要调用哪个函数",
            "从用户问题中提取参数",
            "生成符合格式的JSON调用参数",
            "整合函数返回结果,生成友好回答"
        ],
        "✗ 不做的事": [
            "不直接执行函数",
            "不访问API",
            "不连接数据库",
            "不做实际的网络请求"
        ]
    },

    "开发者的职责": {
        "做的事": [
            "定义可用函数列表及其参数规范",
            "解析LLM输出的JSON参数",
            "执行实际的函数调用",
            "处理API返回结果",
            "将结果返回给LLM"
        ]
    },

    "分工合作": "LLM负责'智能理解和决策',开发者负责'实际执行和集成'"
}
```

---

## 第三部分:完整代码实现

### 3.1 基础示例:天气查询

```python
import openai
import json

# ========== Step 1: 定义可用函数 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["location"],
            },
        },
    }
]

# ========== Step 2: 定义辅助函数 ==========
def get_completion(messages, model="gpt-3.5-turbo-1106", temperature=0, max_tokens=300, tools=None):
    """调用OpenAI API"""
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        tools=tools
    )
    return response.choices[0].message


def get_current_weather(location, unit="celsius"):
    """
    模拟天气API
    实际应用中,这里会调用真实的天气API
    """
    # 模拟API返回数据
    weather_data = {
        "London": {"temperature": 15, "condition": "Cloudy"},
        "San Francisco": {"temperature": 18, "condition": "Sunny"},
        "Beijing": {"temperature": 5, "condition": "Clear"},
    }

    weather = weather_data.get(location, {"temperature": 20, "condition": "Unknown"})

    return {
        "location": location,
        "temperature": weather["temperature"],
        "unit": unit,
        "condition": weather["condition"]
    }


# ========== Step 3: 处理用户问题 ==========
def handle_user_query(user_question):
    """完整的Function Calling流程"""

    print("="*60)
    print("🚀 Function Calling 演示")
    print("="*60)

    # 3.1 用户问题
    messages = [
        {
            "role": "user",
            "content": user_question
        }
    ]

    print(f"\n📝 用户问题: {user_question}")

    # 3.2 第一次调用LLM(让LLM决定是否需要调用函数)
    print("\n🤖 Step 1: LLM分析问题并决定函数调用...")
    response = get_completion(messages, tools=tools)

    # 3.3 检查LLM是否要调用函数
    if response.tool_calls:
        print("✅ LLM决定调用函数!")

        # 获取函数调用信息
        tool_call = response.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        print(f"\n📞 函数调用信息:")
        print(f"  函数名: {function_name}")
        print(f"  参数: {json.dumps(function_args, indent=2, ensure_ascii=False)}")

        # 3.4 执行实际的函数调用
        print("\n⚙️ Step 2: 执行函数调用...")
        if function_name == "get_current_weather":
            function_result = get_current_weather(
                location=function_args.get("location"),
                unit=function_args.get("unit", "celsius")
            )

        print(f"✓ 函数返回结果:")
        print(f"  {json.dumps(function_result, indent=2, ensure_ascii=False)}")

        # 3.5 将函数结果添加到对话历史
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": response.tool_calls
        })

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(function_result)
        })

        # 3.6 第二次调用LLM(让LLM整合结果生成最终答案)
        print("\n🤖 Step 3: LLM整合结果生成最终答案...")
        final_response = get_completion(messages)

        print(f"\n💬 最终回答:")
        print(f"  {final_response.content}")

    else:
        # LLM直接回答,不需要调用函数
        print("ℹ️ LLM直接回答,不需要调用函数")
        print(f"\n💬 回答:")
        print(f"  {response.content}")

    print("\n" + "="*60)
    return final_response if response.tool_calls else response


# ========== Step 4: 测试 ==========
if __name__ == "__main__":
    # 测试1: 需要调用函数的问题
    handle_user_query("伦敦现在的天气如何?")

    print("\n\n")

    # 测试2: 不需要调用函数的问题
    handle_user_query("什么是函数调用?")
```

### 3.2 预期输出

```
============================================================
🚀 Function Calling 演示
============================================================

📝 用户问题: 伦敦现在的天气如何?

🤖 Step 1: LLM分析问题并决定函数调用...
✅ LLM决定调用函数!

📞 函数调用信息:
  函数名: get_current_weather
  参数: {
  "location": "London",
  "unit": "celsius"
}

⚙️ Step 2: 执行函数调用...
✓ 函数返回结果:
  {
  "location": "London",
  "temperature": 15,
  "unit": "celsius",
  "condition": "Cloudy"
}

🤖 Step 3: LLM整合结果生成最终答案...

💬 最终回答:
  伦敦现在的天气是多云,温度为15摄氏度。

============================================================
```

---

## 第四部分:进阶应用 - 多函数调用

### 4.1 定义多个函数

```python
# 定义多个工具函数
advanced_tools = [
    # 函数1: 天气查询
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取指定地点的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "城市名"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    },
    # 函数2: 数据库查询
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "查询数据库中的用户信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "用户ID"},
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "需要查询的字段,如['name','email','balance']"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    # 函数3: 发送邮件
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送电子邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "收件人邮箱"},
                    "subject": {"type": "string", "description": "邮件主题"},
                    "body": {"type": "string", "description": "邮件正文"}
                },
                "required": ["to", "subject", "body"]
            }
        }
    },
    # 函数4: 计算器
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式,如'35628 * 89453'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# 实现各个函数
def query_database(user_id, fields=None):
    """模拟数据库查询"""
    # 模拟数据库数据
    users_db = {
        "user_001": {
            "name": "张三",
            "email": "zhangsan@example.com",
            "balance": 1500.50,
            "vip_level": "Gold"
        },
        "user_002": {
            "name": "李四",
            "email": "lisi@example.com",
            "balance": 3200.00,
            "vip_level": "Platinum"
        }
    }

    user_data = users_db.get(user_id, {})

    if fields:
        return {field: user_data.get(field) for field in fields}
    else:
        return user_data


def send_email(to, subject, body):
    """模拟发送邮件"""
    # 实际应用中,这里会调用SMTP服务或邮件API
    return {
        "status": "success",
        "message": f"邮件已发送到 {to}",
        "subject": subject
    }


def calculator(expression):
    """安全计算器"""
    try:
        # 安全评估数学表达式
        result = eval(expression, {"__builtins__": {}}, {})
        return {
            "expression": expression,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e),
            "status": "failed"
        }


# 多函数调用处理器
def handle_advanced_query(user_question):
    """处理可能涉及多个函数的复杂查询"""
    messages = [{"role": "user", "content": user_question}]

    print(f"\n📝 用户问题: {user_question}")

    response = get_completion(messages, tools=advanced_tools)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"\n📞 调用函数: {function_name}")
            print(f"   参数: {json.dumps(function_args, ensure_ascii=False)}")

            # 根据函数名调用对应的函数
            if function_name == "get_current_weather":
                result = get_current_weather(**function_args)
            elif function_name == "query_database":
                result = query_database(**function_args)
            elif function_name == "send_email":
                result = send_email(**function_args)
            elif function_name == "calculator":
                result = calculator(**function_args)

            print(f"   结果: {json.dumps(result, ensure_ascii=False)}")

            # 添加函数调用结果到对话
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(result)
            })

    # 获取最终回答
    final_response = get_completion(messages)
    print(f"\n💬 最终回答: {final_response.content}")

    return final_response


# 测试复杂查询
if __name__ == "__main__":
    # 测试1: 数据库查询
    handle_advanced_query("查询用户user_001的姓名和余额")

    # 测试2: 精确计算
    handle_advanced_query("计算35628乘以89453的精确值")

    # 测试3: 组合任务
    handle_advanced_query("查询用户user_002的邮箱,然后给他发一封邮件,主题是'VIP特权通知',内容是感谢使用我们的服务")
```

---

## 第五部分:Function Calling的应用场景

### 5.1 核心应用场景

```python
Function_Calling应用场景 = {
    "1. 对话代理(Chatbot)": {
        "场景": "智能客服、AI助手",
        "示例": [
            "查询订单状态 → query_order(order_id)",
            "修改配送地址 → update_address(order_id, new_address)",
            "办理退款 → process_refund(order_id, reason)"
        ],
        "技术融合": "结合ReAct框架,实现Thought→Action(Function Call)→Observation循环"
    },

    "2. 数据提取和标注": {
        "场景": "从文本中提取结构化数据",
        "示例": [
            "从文章中提取人名 → extract_entities(text, entity_type='PERSON')",
            "提取日期和金额 → extract_datetime_and_amounts(text)",
            "情感分析 → analyze_sentiment(text)"
        ],
        "优势": "LLM理解上下文 + 函数规范输出格式 = 结构化数据"
    },

    "3. 自然语言转API调用": {
        "场景": "将自然语言转换为API调用或数据库查询",
        "示例": [
            "用户: '给我看上个月销售额超过10万的产品'",
            "→ query_products(time_range='last_month', sales_min=100000)"
        ],
        "技术": "自然语言 → Function Parameters → SQL/API调用"
    },

    "4. 数学问题求解": {
        "场景": "复杂数学计算",
        "示例": [
            "用户: '计算复利: 本金10000,年利率5%,10年后本息合计'",
            "→ calculate_compound_interest(principal=10000, rate=0.05, years=10)"
        ],
        "优势": "避免LLM计算错误,确保精确结果"
    },

    "5. 知识库检索": {
        "场景": "RAG系统中的向量搜索",
        "示例": [
            "用户: 'Transformer的注意力机制是什么?'",
            "→ search_knowledge_base(query='Transformer attention mechanism', top_k=3)"
        ],
        "技术融合": "Function Calling + RAG"
    },

    "6. 工作流自动化": {
        "场景": "多步骤任务自动化",
        "示例": [
            "用户: '汇总本周会议纪要并发给团队'",
            "→ Step1: list_meetings(week='current')",
            "→ Step2: summarize_meetings(meeting_ids)",
            "→ Step3: send_email(to='team@example.com', content=summary)"
        ],
        "技术融合": "Function Calling + Prompt Chaining"
    }
}
```

### 5.2 实战案例:智能客服系统

```python
# 完整的客服系统示例
customer_service_tools = [
    {
        "type": "function",
        "function": {
            "name": "query_order",
            "description": "查询订单状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "取消订单",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "reason": {"type": "string", "description": "取消原因"}
                },
                "required": ["order_id", "reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_refund_policy",
            "description": "查询退款政策",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_category": {"type": "string", "description": "商品类别"}
                },
                "required": []
            }
        }
    }
]


class CustomerServiceBot:
    """智能客服机器人"""

    def __init__(self):
        self.conversation_history = []

    def query_order(self, order_id):
        """模拟订单查询"""
        orders = {
            "ORD001": {
                "status": "已发货",
                "tracking_number": "SF1234567890",
                "estimated_delivery": "2025-11-10"
            },
            "ORD002": {
                "status": "处理中",
                "estimated_delivery": "2025-11-12"
            }
        }
        return orders.get(order_id, {"status": "未找到订单"})

    def cancel_order(self, order_id, reason):
        """模拟取消订单"""
        # 实际应用中会调用订单系统API
        return {
            "order_id": order_id,
            "status": "已取消",
            "refund_status": "退款将在3-5个工作日到账",
            "cancel_reason": reason
        }

    def check_refund_policy(self, product_category=None):
        """查询退款政策"""
        policies = {
            "default": "7天无理由退货,15天质量问题退换",
            "electronics": "未拆封7天内可退,拆封后质量问题15天内可换",
            "food": "不支持退货,质量问题24小时内可换货"
        }
        return policies.get(product_category or "default")

    def handle_customer_request(self, user_message):
        """处理客户请求"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        print(f"\n👤 客户: {user_message}")

        # 调用LLM分析并决定函数调用
        response = get_completion(
            self.conversation_history,
            tools=customer_service_tools
        )

        # 处理函数调用
        if response.tool_calls:
            for tool_call in response.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"   🔧 系统调用: {func_name}({func_args})")

                # 执行函数
                if func_name == "query_order":
                    result = self.query_order(**func_args)
                elif func_name == "cancel_order":
                    result = self.cancel_order(**func_args)
                elif func_name == "check_refund_policy":
                    result = self.check_refund_policy(**func_args)

                # 添加函数调用和结果到历史
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })

                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        # 获取最终回复
        final_response = get_completion(self.conversation_history)
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response.content
        })

        print(f"🤖 客服: {final_response.content}\n")
        return final_response.content


# 使用示例
if __name__ == "__main__":
    bot = CustomerServiceBot()

    # 多轮对话
    bot.handle_customer_request("我想查询订单ORD001的状态")
    bot.handle_customer_request("这个订单我不想要了,帮我取消吧,因为买错了尺寸")
    bot.handle_customer_request("取消后多久能退款?")
```

---

## 第六部分:与前面技术的融合

### 6.1 Function Calling在技术体系中的位置

```python
技术融合视图 = """

第二阶段学习的技术(Techniques) → 第三阶段应用(Applications)

┌────────────────────────────────────────────────────────┐
│ Day19: ReAct (Reasoning + Acting)                      │
│ ├─ Thought: 推理思考                                   │
│ ├─ Action: 执行动作 ← ⚡ Function Calling在这里! ⚡    │
│ └─ Observation: 观察结果                               │
│                                                        │
│ Function Calling是ReAct中"Action"的标准化实现:       │
│ • ReAct定义了框架(Thought→Action→Observation)        │
│ • Function Calling提供了Action的具体机制              │
│   (定义函数 → LLM生成调用参数 → 执行 → 返回结果)     │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Day18: PAL (Program-Aided Language Models)             │
│ ├─ 核心: LLM生成代码 → 外部执行器执行                 │
│                                                        │
│ Function Calling vs PAL:                               │
│ ├─ 相似: 都需要"LLM生成 + 外部执行"                    │
│ ├─ 区别: PAL生成代码,Function Calling生成函数调用参数 │
│ └─ 关系: 两种不同的"外部工具调用"实现方式              │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Day13: RAG (Retrieval Augmented Generation)            │
│ ├─ 核心: 检索外部知识 → 增强生成                      │
│                                                        │
│ Function Calling + RAG:                                │
│ • RAG中的"检索"步骤可以用Function Calling实现:        │
│   search_knowledge_base(query, top_k) → 向量搜索     │
│ • Function Calling扩展了RAG的能力:                    │
│   不仅检索知识,还能调用任何外部工具/API                │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Day11: Prompt Chaining (提示链)                        │
│ ├─ 核心: 将复杂任务分解为多个步骤链式执行             │
│                                                        │
│ Function Calling + Prompt Chaining:                    │
│ • 每个步骤可以调用不同的函数                          │
│ • 后续步骤使用前面函数的返回结果                      │
│ • 实现复杂工作流自动化                                │
│                                                        │
│ 示例: 数据分析工作流                                  │
│ Step1: load_data() → Step2: clean_data() →            │
│ Step3: analyze_data() → Step4: generate_report()      │
└────────────────────────────────────────────────────────┘

"""

print(技术融合视图)
```

---

## 总结:一句话理解

**Function Calling就是让LLM理解用户意图并生成函数调用参数(JSON),由外部系统执行实际函数,实现LLM与外部工具的可靠连接!**

### 核心公式

```
Function Calling = LLM理解意图 + 生成调用参数(JSON) + 外部执行 + 结果整合
```

### 技术定位

```
在技术体系中:
├─ ReAct的Action层 → Function Calling是标准实现
├─ PAL的兄弟技术 → 都是"LLM生成 + 外部执行",但输出格式不同
├─ RAG的扩展应用 → 不仅检索知识,还能调用任何工具
└─ Prompt Chaining的执行引擎 → 每个链条步骤可调用函数
```

### 理解口诀

```
Function Calling核心三步:
1. 定义函数(开发者预先定义可用工具)
2. LLM决策(理解意图,生成JSON参数)
3. 外部执行(开发者代码执行实际函数)

记住: LLM只负责"智能理解和决策",不负责"实际执行"!
```

---

**现在你明白了吗?** Function Calling是实际应用的核心基础,让LLM从"只会聊天"进化到"能调用工具完成实际任务"!🚀

**接下来老王我会继续帮你学习Day23-Day26的内容!**
