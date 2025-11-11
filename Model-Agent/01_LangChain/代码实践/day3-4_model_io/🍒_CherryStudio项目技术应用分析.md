# 🍒 Cherry Studio - Day3-4: 模型I/O封装技术应用

## 核心模块

**主要文件**: `src/renderer/src/utils/stream.ts` + `src/renderer/src/types/newMessage.ts`

---

## 1. Chat Messages 消息结构

### Message类型定义

**文件**: `src/renderer/src/types/newMessage.ts`

Cherry Studio的消息结构与LangChain的HumanMessage/AIMessage类似：

```typescript
export interface Message {
  id: string
  role: 'system' | 'user' | 'assistant'  // 对应LangChain角色
  content: string | MessageContent[]     // 支持文本+图像
  timestamp: number
  metadata?: MessageMetadata
}

export interface MessageMetadata {
  provider?: string      // openai, gemini, anthropic
  model?: string        // gpt-3.5-turbo, claude-3
  tokens?: TokenUsage   // Token统计
  cost?: number         // 成本
  latency?: number      // 响应时间
}

export interface TokenUsage {
  promptTokens: number
  completionTokens: number
  totalTokens: number
}
```

**对比LangChain**:

| Cherry Studio | LangChain | 说明 |
|--------------|-----------|------|
| `Message.role` | `HumanMessage/AIMessage/SystemMessage` | 角色定义 |
| `Message.content` | `message.content` | 消息内容 |
| `Message.metadata` | `message.additional_kwargs` | 元数据 |

---

## 2. 流式输出实现 (Streaming)

### 核心实现

**文件**: `src/renderer/src/utils/stream.ts`

```typescript
export async function* streamChatCompletion(
  provider: string,
  model: string,
  messages: Message[],
  options?: StreamOptions
): AsyncGenerator<string, void, unknown> {
  const endpoint = getProviderEndpoint(provider)
  const headers = getProviderHeaders(provider)

  // 发起流式请求
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      ...headers,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model,
      messages: messages.map(m => ({
        role: m.role,
        content: m.content
      })),
      stream: true,  // 关键：开启流式
      ...options
    })
  })

  // 处理SSE流
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    // 解码chunk
    const chunk = decoder.decode(value, { stream: true })
    const lines = chunk.split('\n').filter(Boolean)

    for (const line of lines) {
      // 解析SSE格式: data: {...}
      if (line.startsWith('data: ')) {
        const data = line.slice(6)

        if (data === '[DONE]') {
          return  // 流结束
        }

        try {
          const parsed = JSON.parse(data)
          const content = parsed.choices?.[0]?.delta?.content

          if (content) {
            yield content  // 逐块返回
          }
        } catch (e) {
          console.error('Parse error:', e)
        }
      }
    }
  }
}
```

**使用示例**:

```typescript
// 在UI中实时显示
async function chatWithStreaming(userInput: string) {
  const messages = [
    { role: 'user', content: userInput }
  ]

  let fullResponse = ''

  for await (const chunk of streamChatCompletion('openai', 'gpt-3.5-turbo', messages)) {
    fullResponse += chunk
    updateUIWithChunk(chunk)  // 实时更新界面
  }

  saveMessage(fullResponse)
}
```

**技术亮点**:

- ✅ 支持多提供商（OpenAI、Gemini、Anthropic等）
- ✅ 统一的Stream接口
- ✅ 实时UI更新
- ✅ 错误处理和重连

---

## 3. Token追踪与成本管理

### Token统计实现

**文件**: `src/renderer/src/services/TokenTrackingService.ts` (推测)

```typescript
export class TokenTrackingService {
  // 估算Token数（调用前）
  estimateTokens(messages: Message[]): number {
    // 简单估算：中文1.5字符≈1 token, 英文4字符≈1 token
    let total = 0

    for (const msg of messages) {
      const content = typeof msg.content === 'string'
        ? msg.content
        : msg.content.map(c => c.text || '').join('')

      // 粗略估算
      total += Math.ceil(content.length / 2)
    }

    return total
  }

  // 从响应提取Token统计
  extractTokenUsage(response: APIResponse): TokenUsage {
    // OpenAI格式
    if (response.usage) {
      return {
        promptTokens: response.usage.prompt_tokens,
        completionTokens: response.usage.completion_tokens,
        totalTokens: response.usage.total_tokens
      }
    }

    // 其他提供商格式转换
    return {
      promptTokens: 0,
      completionTokens: 0,
      totalTokens: 0
    }
  }

  // 成本计算
  calculateCost(usage: TokenUsage, model: string): number {
    const priceTable = {
      'gpt-4': {
        prompt: 0.03 / 1000,      // $0.03 per 1K tokens
        completion: 0.06 / 1000
      },
      'gpt-3.5-turbo': {
        prompt: 0.0005 / 1000,
        completion: 0.0015 / 1000
      },
      'claude-3-opus': {
        prompt: 0.015 / 1000,
        completion: 0.075 / 1000
      }
    }

    const price = priceTable[model] || priceTable['gpt-3.5-turbo']

    return (
      usage.promptTokens * price.prompt +
      usage.completionTokens * price.completion
    )
  }
}
```

### UI中的Token显示

```typescript
// 在对话界面显示Token和成本
export function MessageTokenInfo({ message }: { message: Message }) {
  const usage = message.metadata?.tokens
  const cost = message.metadata?.cost

  if (!usage) return null

  return (
    <div className="token-info">
      <span>
        {usage.totalTokens} tokens
      </span>
      {cost && (
        <span className="cost">
          ${cost.toFixed(6)}
        </span>
      )}
    </div>
  )
}
```

---

## 4. 结构化输出解析

### Pydantic风格的类型定义

**文件**: `src/renderer/src/types/structuredOutput.ts` (推测)

```typescript
// 定义结构化输出Schema
export interface PersonSchema {
  name: string
  age: number
  occupation: string
  skills: string[]
  education: {
    degree: string
    school: string
    year: number
  }
}

// JSON Schema定义
export const personJSONSchema = {
  type: 'object',
  properties: {
    name: { type: 'string', description: '姓名' },
    age: { type: 'number', description: '年龄' },
    occupation: { type: 'string', description: '职业' },
    skills: {
      type: 'array',
      items: { type: 'string' },
      description: '技能列表'
    },
    education: {
      type: 'object',
      properties: {
        degree: { type: 'string' },
        school: { type: 'string' },
        year: { type: 'number' }
      },
      required: ['degree', 'school', 'year']
    }
  },
  required: ['name', 'age', 'occupation', 'skills', 'education']
}
```

### 结构化输出调用

```typescript
// 使用Function Calling获取结构化输出
export async function extractStructuredData<T>(
  text: string,
  schema: object,
  schemaName: string
): Promise<T> {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'user',
          content: `从以下文本中提取信息:\n${text}`
        }
      ],
      functions: [{
        name: schemaName,
        description: '提取结构化信息',
        parameters: schema
      }],
      function_call: { name: schemaName }
    })
  })

  const data = await response.json()
  const functionCall = data.choices[0].message.function_call

  // 解析返回的JSON
  return JSON.parse(functionCall.arguments) as T
}

// 使用示例
const person = await extractStructuredData<PersonSchema>(
  "我叫张三，今年30岁，是一名软件工程师，擅长Python和TypeScript，毕业于清华大学计算机系...",
  personJSONSchema,
  'extract_person_info'
)

console.log(person.name)        // "张三"
console.log(person.age)         // 30
console.log(person.skills)      // ["Python", "TypeScript"]
```

---

## 5. 多模态输入支持

### 图像+文本消息

```typescript
export type MessageContent =
  | string
  | Array<TextContent | ImageContent>

export interface TextContent {
  type: 'text'
  text: string
}

export interface ImageContent {
  type: 'image_url'
  image_url: {
    url: string          // 图片URL或base64
    detail?: 'low' | 'high' | 'auto'
  }
}

// 发送图像+文本消息
const message: Message = {
  id: generateId(),
  role: 'user',
  content: [
    {
      type: 'text',
      text: '这张图片里有什么?'
    },
    {
      type: 'image_url',
      image_url: {
        url: 'data:image/png;base64,...',
        detail: 'high'
      }
    }
  ],
  timestamp: Date.now()
}
```

---

## 6. 与LangChain对比

| 功能 | Cherry Studio | LangChain (Day3-4) |
|-----|--------------|-------------------|
| **消息结构** | `Message` 接口 | `HumanMessage/AIMessage` |
| **流式输出** | `streamChatCompletion()` | `llm.stream()` |
| **Token追踪** | `TokenTrackingService` | `get_openai_callback()` |
| **成本计算** | 内置价格表 | 需手动计算 |
| **结构化输出** | Function Calling | `PydanticOutputParser` |
| **多模态** | 原生支持 | 需配置 |

---

## 实战应用场景

### 场景1: 实时翻译助手

```typescript
async function realtimeTranslation(sourceText: string) {
  const messages = [
    {
      role: 'system',
      content: '你是一个专业翻译，将用户输入翻译成英文'
    },
    {
      role: 'user',
      content: sourceText
    }
  ]

  let translation = ''

  for await (const chunk of streamChatCompletion('openai', 'gpt-3.5-turbo', messages)) {
    translation += chunk
    updateTranslationUI(translation)  // 实时更新
  }

  // 统计Token和成本
  const usage = await getTokenUsage(translation)
  displayCost(usage)
}
```

### 场景2: 简历信息提取

```typescript
async function extractResumeInfo(resumeText: string) {
  const schema = {
    type: 'object',
    properties: {
      name: { type: 'string' },
      phone: { type: 'string' },
      email: { type: 'string' },
      experience: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            company: { type: 'string' },
            position: { type: 'string' },
            duration: { type: 'string' }
          }
        }
      }
    }
  }

  const info = await extractStructuredData(resumeText, schema, 'resume_info')
  return info
}
```

---

*此文档分析了Cherry Studio项目中Day3-4对应的模型I/O封装技术应用。*
*最后更新: 2025-01-09*