# 模块13: Soul 层 (Agent 核心)

**学习时长**: 5天

**学习目标**: 深入理解 Kimi CLI 的 Agent 执行引擎

---

## 📋 学习内容概览

1. **kimisoul.py 源码分析** (Day 68-69)
2. **agent.py 源码分析** (Day 70)
3. **context.py 源码分析** (Day 71)
4. **runtime.py 源码分析** (Day 72)

---

## 🎯 学习目标

- ✅ 理解 Soul 核心职责
- ✅ 掌握 Agent 执行流程
- ✅ 理解上下文管理
- ✅ 理解运行时环境

---

## 📚 必读源码

```
src/kimi_cli/soul/
├── kimisoul.py     # Agent 执行引擎
├── agent.py        # Agent 规范加载
├── context.py      # 上下文管理
├── runtime.py      # 运行时环境
└── tool_use.py     # 工具调用处理
```

---

## 📖 核心知识点

### KimiSoul (核心引擎)

**职责**:
- 管理对话循环
- 工具调用决策
- 流式响应处理
- 上下文更新

**关键代码**:
```python
class KimiSoul:
    async def chat(self, user_input: str) -> AsyncIterator[str]:
        """主对话循环"""
        # 1. 构建消息
        messages = self._build_messages(user_input)

        # 2. 调用 LLM（流式）
        async for chunk in self._llm.astream_chat(messages):
            # 3. 处理工具调用
            if chunk.tool_calls:
                await self._execute_tools(chunk.tool_calls)
                continue

            # 4. 输出内容
            if chunk.delta.content:
                yield chunk.delta.content
```

### Agent 规范

**规范文件** (`agents/` 目录):
```markdown
# Agent Specification

## Role
You are ...

## Capabilities
- Capability 1
- Capability 2

## Instructions
1. Step 1
2. Step 2

## Tools Available
- tool_name_1
- tool_name_2
```

### Context 管理

**职责**:
- 对话历史管理
- 上下文窗口控制
- 记忆持久化

**策略**:
- 滑动窗口
- 摘要压缩
- 重要性排序

### Runtime 环境

**职责**:
- 工作目录管理
- 会话状态
- 环境变量

---

## 📊 实践练习

**练习40**: Debug Agent 执行流程
- 单步调试完整对话
- 理解每个步骤的作用

**练习41**: 追踪工具调用
- 跟踪从决策到执行的完整流程
- 理解工具调用参数构建

**练习42**: 分析上下文管理
- 研究上下文窗口控制算法
- 理解摘要生成逻辑

**练习43**: 设计自定义 Agent
- 编写自定义 Agent 规范
- 测试执行效果

---

## 🔄 下一步

完成本模块后，进入 **模块14: Tools 工具系统**。

---

*Created by 老王 | Last Updated: 2025-01-10*
