# Claude 自定义命令集合参考

> 这是一组高效的 Claude Code 自定义 slash 命令集合，可以作为学习和参考的范例。

## 📚 目录

1. [命令概览](#命令概览)
2. [命令详解](#命令详解)
3. [设计原则](#设计原则)
4. [如何应用到 Kimi CLI](#如何应用到-kimi-cli)

---

## 命令概览

### 核心命令分类

| 类别 | 命令 | 用途 | 核心特点 |
|------|------|------|---------|
| 🔍 分析类 | `/ask` | 只读分析 | 严格禁止修改 |
| 🎯 对齐类 | `/align` | 认知对齐 | 复述确认理解 |
| ⚡ 执行类 | `/act` | 严格执行 | 100%符合需求 |
| 🐛 调试类 | `/debug` | 诊断问题 | 找原因不修复 |
| 📝 文档类 | `/doc` | 文档管理 | 记录事实信息 |
| 🛠️ 工具类 | `/plan-command` | 命令规划 | 设计命令结构 |
| 🌍 学习类 | `/english` | 英语学习 | 双语输出 |
| 🧹 清理类 | `/rm-useless-try-catch` | 代码清理 | 删除无用代码 |
| 💾 记忆类 | `/mem` | 上下文管理 | 管理 CLAUDE.md |
| 🚀 后台类 | `/bg` | 后台任务 | 智能执行 |
| 🤖 咨询类 | `/codex` | 技术咨询 | 上下文感知 |

---

## 命令详解

### 1. `/ask` - 只读分析助手

**核心理念**：严格的只读分析，不做任何修改

**适用场景**：
- 查询项目信息
- 分析代码结构
- 了解系统状态
- 审查配置

**关键限制**：
```markdown
严格禁止：
- ❌ Write（写入文件）
- ❌ Edit（编辑文件）
- ❌ Bash（可能修改系统）

仅允许：
- ✅ Read（读取文件）
- ✅ Grep（搜索）
- ✅ Glob（查找文件）
- ✅ 分析和总结
```

**示例用法**：
```
/ask 这个项目的架构是什么样的？
/ask 分析 src/app.py 的功能
/ask 列出所有 API 端点
```

**设计亮点**：
- 🎯 单一职责：只分析，不修改
- 🔒 安全性：防止误操作
- 📊 清晰输出：结构化的分析结果

---

### 2. `/align` - 认知对齐助手

**核心理念**：理解用户意图并复述确认，避免误解

**工作流程**：
```
1. 接收用户需求
   ↓
2. 分析核心意图
   ↓
3. 识别可能的歧义
   ↓
4. 用自己的话复述
   ↓
5. 等待用户确认
```

**适用场景**：
- 需求不够明确时
- 复杂任务开始前
- 避免理解偏差
- 多步骤任务规划

**示例用法**：
```
/align 帮我优化这个函数的性能
/align 重构这个模块的代码结构
/align 实现用户登录功能
```

**输出格式**：
```markdown
## 我的理解

**核心需求**：[用自己的话复述]

**关键要点**：
1. [要点1]
2. [要点2]
3. [要点3]

**可能的歧义**：
- [歧义点1]：[说明]
- [歧义点2]：[说明]

**我的理解是否正确？如有偏差请指正。**
```

**设计亮点**：
- 🤝 减少误解：明确共识
- 📋 结构化输出：清晰易读
- 🔄 迭代改进：可反复确认

---

### 3. `/act` - 执行助手

**核心理念**：严格按需求执行，100%符合要求

**核心原则**：
```
1. ✅ 100% 符合需求，不简化方案
2. ✅ 不绕过已达成的共识
3. ✅ 遇到问题时保持原始意图
4. ✅ 完成后只报告未完成项
```

**适用场景**：
- 执行明确的需求
- 实施讨论好的方案
- 批量操作
- 重复性任务

**示例用法**：
```
/act 按照刚才的设计实现登录功能
/act 严格按照 API 文档添加所有端点
/act 完整实现测试用例，不要简化
```

**完成报告格式**：
```markdown
## 执行完成

**已完成**：
- ✅ [任务1]
- ✅ [任务2]

**未完成**：
- ⏸️ [任务3]：[原因]

**不符合要求的地方**：
- ⚠️ [问题]：[说明]
```

**设计亮点**：
- 🎯 严格执行：不打折扣
- 📝 清晰报告：透明度高
- 🔍 问题追踪：明确未完成项

---

### 4. `/debug` - 调试助手

**核心理念**：诊断而非治疗，找原因不修复

**工作流程**：
```
1. 理解问题
   ↓
2. 收集信息
   ↓
3. 形成假设
   ↓
4. 验证假设
   ↓
5. 假设错误 → 新假设
   ↓
6. 找到根本原因
```

**核心原则**：
```markdown
✅ 允许：
- 分析日志
- 检查配置
- 测试假设
- 追踪调用链

❌ 禁止：
- 修复代码
- 未经验证的猜测
- 直接给出解决方案
```

**示例用法**：
```
/debug 用户登录失败
/debug API 响应超时
/debug 数据库连接错误
```

**输出格式**：
```markdown
## 诊断报告

**问题现象**：
[描述问题]

**信息收集**：
- [收集的信息1]
- [收集的信息2]

**假设验证过程**：
1. 假设1：[假设] → [验证结果]
2. 假设2：[假设] → [验证结果]

**根本原因**：
[确定的根本原因]

**证据**：
- [证据1]
- [证据2]

**建议的调查方向**：
- [方向1]
- [方向2]
```

**设计亮点**：
- 🔬 科学方法：假设-验证循环
- 📊 过程透明：展示推理过程
- 🎯 聚焦诊断：不分散注意力

---

### 5. `/doc` - 文档管理助手

**核心理念**：记录事实信息，不记录猜想

**文件命名规则**：
```
新建文档：YYYYMMDD-主题.md
示例：20250110-API设计.md

修改文档：保持原有文件名
```

**内容原则**：
```markdown
✅ 记录：
- 确切的内容
- 事实信息
- 设计决策
- 配置参数

❌ 禁止：
- 安全讨论（属于 SECURITY.md）
- 性能讨论（属于性能分析）
- 未来展望（属于 TODO.md）
- 猜想和假设
```

**示例用法**：
```
/doc 记录今天的 API 设计决策
/doc 更新数据库 schema 文档
/doc 添加新的配置项说明
```

**文档结构模板**：
```markdown
# [主题]

**创建时间**：YYYY-MM-DD
**负责人**：[名字]

## 背景

[为什么要记录这个]

## 内容

[具体的事实信息]

## 相关链接

- [相关文档]
- [相关代码]
```

**设计亮点**：
- 📅 时间戳命名：易于追溯
- 📝 事实导向：可靠性高
- 🗂️ 统一格式：易于维护

---

### 6. `/plan-command` - 命令规划助手

**核心理念**：帮助设计 Claude Code 自定义命令

**功能清单**：
```
1. 分析用户需求
2. 提供命令名称建议
3. 设计 YAML frontmatter
4. 提供命令内容结构
5. 给出实现建议
```

**示例用法**：
```
/plan-command 我想要一个代码审查命令
/plan-command 设计一个自动化测试命令
```

**输出格式**：
```markdown
## 命令设计方案

### 命令名称建议
- `/review` （推荐）
- `/code-review`
- `/check`

### YAML Frontmatter
\`\`\`yaml
name: review
description: 代码审查助手
triggers:
  - review
  - code-review
\`\`\`

### 命令内容结构
\`\`\`markdown
# 代码审查助手

## 审查重点
- 代码质量
- 性能问题
- 安全隐患

## 审查流程
1. 读取代码
2. 分析问题
3. 给出建议
\`\`\`

### 实现建议
- 使用 Read 工具读取代码
- 使用 Grep 搜索反模式
- 结构化输出审查结果
```

**设计亮点**：
- 🎨 创意辅助：提供多种方案
- 📋 结构化输出：直接可用
- 💡 最佳实践：基于经验

---

### 7. `/english` - 英语学习助手

**核心理念**：解决问题的同时练习英语

**双语输出格式**：
```markdown
## 📝 表达优化建议（中文）

**原始表达的问题**：
- [语法问题]
- [词汇问题]

**意图理解**：
[我理解你想表达的是...]

**关键表达**：
- 原句：[你的表达]
- 改进：[地道表达]

**地道表达示例**：
- [示例1]
- [示例2]

---

## 💬 实际回答（英文）

[用英文回答用户的具体问题]
```

**示例用法**：
```
/english How can I fix this bug?
/english Please help me optimize this function
/english What is the best way to handle errors?
```

**支持的操作**：
- ✅ 回答技术问题
- ✅ 执行代码操作
- ✅ 分析和建议
- ✅ 所有常规功能

**设计亮点**：
- 🌍 双重价值：技术+英语
- 📚 学习导向：分析表达问题
- 💼 实战练习：真实场景

---

### 8. `/rm-useless-try-catch` - 清理无用异常处理

**核心理念**：删除无意义的异常处理代码

**识别模式**：
```javascript
// 模式1：仅记录日志
try {
  doSomething();
} catch (error) {
  console.error(error);  // ← 无意义
}

// 模式2：原地重抛
try {
  doSomething();
} catch (error) {
  throw error;  // ← 无意义
}

// 模式3：空 catch
try {
  doSomething();
} catch (error) {
  // ← 无意义
}

// 保留：有实际处理逻辑
try {
  doSomething();
} catch (error) {
  handleError(error);  // ← 有意义
  return fallbackValue;
}
```

**示例用法**：
```
/rm-useless-try-catch src/
/rm-useless-try-catch app.js
```

**清理报告**：
```markdown
## 清理报告

**已删除**：
- `src/app.js:42` - 仅记录日志的 try-catch
- `src/utils.js:78` - 空 catch 块

**保留**：
- `src/api.js:123` - 有错误恢复逻辑

**总计**：删除 2 个无用块，保留 1 个有效块
```

**设计亮点**：
- 🧹 自动化清理：提高效率
- 🔍 智能识别：准确判断
- 📊 清晰报告：可审查

---

### 9. `/mem` - CLAUDE.md 管理助手

**核心理念**：管理项目上下文记忆

**支持操作**：
```markdown
1. 新增信息
   /mem 添加规则：禁止使用 any 类型

2. 修改信息
   /mem 更新测试规则，改为必须写单元测试

3. 删除信息
   /mem 删除关于 console.log 的限制
```

**操作流程**：
```
1. 读取当前 CLAUDE.md
   ↓
2. 解析用户操作意图
   ↓
3. 执行新增/修改/删除
   ↓
4. 更新 CLAUDE.md
   ↓
5. 展示变更内容
```

**示例用法**：
```
/mem 添加编码规范：使用 TypeScript 严格模式
/mem 更新数据库配置为 PostgreSQL
/mem 删除旧的 API 版本说明
```

**变更报告**：
```markdown
## CLAUDE.md 变更

**操作类型**：新增

**变更内容**：
\`\`\`diff
+ ## 编码规范
+ - 使用 TypeScript 严格模式
+ - 所有函数必须有类型注解
\`\`\`

**生效位置**：[文件路径]
```

**设计亮点**：
- 💾 持久化记忆：累积项目知识
- 🔄 易于维护：结构化管理
- 📝 变更追踪：透明可审计

---

### 10. `/bg` - 智能后台任务助手

**核心理念**：根据自然语言执行后台任务

**智能需求理解**：
```
用户说：构建项目
AI 理解：需要运行构建命令
AI 判断：这是 Node.js 项目 → npm run build
```

**子命令**：
```bash
/bg 构建项目           # 执行后台任务
/bg list              # 列出所有后台任务
/bg kill <task_id>    # 终止任务
/bg output <task_id>  # 查看任务输出
```

**示例用法**：
```
/bg 运行测试
/bg 启动开发服务器
/bg 构建生产版本
/bg list
/bg output task_001
```

**任务列表格式**：
```markdown
## 后台任务列表

| ID | 命令 | 状态 | 启动时间 |
|----|------|------|----------|
| task_001 | npm test | 运行中 | 10:30:15 |
| task_002 | npm build | 完成 | 10:25:00 |
```

**设计亮点**：
- 🧠 智能推理：理解意图
- 🔄 上下文感知：基于项目类型
- 📊 任务管理：完整的生命周期

---

### 11. `/codex` - Codex 咨询助手

**核心理念**：带上下文的技术咨询

**工作流程**：
```
1. 分析问题类型
   ↓
2. 判断是否需要上下文
   ↓
3. 收集相关文件/配置
   ↓
4. 组织上下文信息
   ↓
5. 调用 codex 获取建议
```

**上下文收集策略**：
```markdown
**通用技术问题**：
- 无需上下文
- 示例："如何优化 React 性能？"

**项目特定问题**：
- 收集配置文件
- 示例："这个项目的构建配置有什么问题？"

**代码问题**：
- 读取相关代码
- 示例："这段代码怎么优化？"
```

**示例用法**：
```
/codex 如何优化 React 性能？
/codex 分析这个项目的依赖问题
/codex 这段代码有什么问题？
```

**输出格式**：
```markdown
## 上下文信息

**项目类型**：React + TypeScript
**相关配置**：
- package.json
- tsconfig.json

---

## Codex 建议

[技术建议内容]
```

**设计亮点**：
- 🎯 智能上下文：自动判断需求
- 📚 项目感知：基于实际情况
- 💡 专业建议：高质量输出

---

## 设计原则

### 1. 单一职责原则

每个命令只做一件事，做好一件事：

```
✅ 好的设计：
/ask   - 只读分析
/debug - 只诊断，不修复
/doc   - 只记录事实

❌ 不好的设计：
/analyze-and-fix  - 职责混乱
/do-everything    - 功能不明确
```

### 2. 明确的约束

通过约束提高可靠性：

```
/ask  → 严格禁止修改操作
/debug → 严格禁止给出解决方案
/doc  → 严格禁止记录猜想
```

### 3. 结构化输出

统一的输出格式，易于理解：

```markdown
## [标题]

**[关键信息1]**：
- 内容

**[关键信息2]**：
- 内容
```

### 4. 可组合性

命令可以组合使用：

```
/align 优化这个函数
→ 确认需求

/debug 这个函数为什么慢
→ 找到原因

/act 实施优化方案
→ 执行操作
```

---

## 如何应用到 Kimi CLI

### 1. 命令结构对比

**Claude 命令**：
```markdown
---
name: ask
description: 只读分析助手
---

严格禁止使用 Write、Edit 等工具...
```

**Kimi CLI 实现**：
```python
# src/kimi_cli/commands/ask.py
@click.command()
@click.argument('query')
def ask(query):
    """只读分析助手"""
    # 限制只能使用只读工具
    allowed_tools = ['read', 'grep', 'glob']
    # 执行分析...
```

---

### 2. 工具约束实现

**Claude 方式**（声明式）：
```markdown
严格禁止：Write、Edit、Bash
仅允许：Read、Grep、Glob
```

**Kimi CLI 实现**（代码控制）：
```python
class ReadOnlyToolManager:
    """只读工具管理器"""

    ALLOWED_TOOLS = ['read', 'grep', 'glob']

    def execute_tool(self, tool_name, **kwargs):
        if tool_name not in self.ALLOWED_TOOLS:
            raise ToolNotAllowedError(
                f"工具 {tool_name} 在只读模式下不可用"
            )

        return super().execute_tool(tool_name, **kwargs)
```

---

### 3. 结构化输出实现

**使用 Rich 实现结构化输出**：

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def output_debug_report(problem, hypotheses, root_cause):
    """输出调试报告"""
    console = Console()

    # 问题描述
    console.print(Panel(
        problem,
        title="🐛 问题现象",
        border_style="red"
    ))

    # 假设验证表格
    table = Table(title="假设验证过程")
    table.add_column("假设", style="cyan")
    table.add_column("验证结果", style="green")

    for h in hypotheses:
        table.add_row(h.hypothesis, h.result)

    console.print(table)

    # 根本原因
    console.print(Panel(
        root_cause,
        title="✅ 根本原因",
        border_style="green"
    ))
```

---

### 4. 命令组合实现

**实现命令流水线**：

```python
class CommandPipeline:
    """命令流水线"""

    def __init__(self):
        self.commands = []

    def add(self, command):
        """添加命令"""
        self.commands.append(command)
        return self

    async def execute(self):
        """执行流水线"""
        context = {}

        for cmd in self.commands:
            result = await cmd.execute(context)
            context.update(result)

        return context

# 使用示例
pipeline = CommandPipeline()
pipeline.add(AlignCommand("优化函数"))  # 对齐需求
pipeline.add(DebugCommand("分析性能"))  # 诊断问题
pipeline.add(ActCommand("实施优化"))    # 执行操作

await pipeline.execute()
```

---

## 学习要点

### 1. 命令设计的关键要素

```python
# 好的命令设计应该包含：

class GoodCommand:
    """优秀命令的要素"""

    # 1. 清晰的名称
    name = "ask"

    # 2. 明确的描述
    description = "只读分析助手"

    # 3. 明确的约束
    allowed_tools = ['read', 'grep']
    forbidden_tools = ['write', 'edit']

    # 4. 结构化输出
    def format_output(self, result):
        return {
            "summary": "...",
            "details": "...",
            "next_steps": "..."
        }
```

### 2. 约束的重要性

```
约束 = 可靠性

/ask  - 禁止修改 → 安全的分析
/debug - 禁止修复 → 聚焦诊断
/doc  - 禁止猜想 → 可信的文档
```

### 3. 输出格式的价值

```markdown
好的输出格式应该：
1. ✅ 结构清晰
2. ✅ 易于扫描
3. ✅ 信息完整
4. ✅ 可操作性强
```

---

## 总结

这组命令展示了优秀的命令设计原则：

1. **单一职责**：每个命令专注一件事
2. **明确约束**：通过限制提高可靠性
3. **结构化输出**：统一格式，易于理解
4. **可组合性**：命令可以配合使用
5. **上下文感知**：智能判断所需信息

**对 Kimi CLI 开发的启发**：

- 🎯 设计清晰的命令接口
- 🔒 实现工具级别的权限控制
- 📊 提供结构化的输出格式
- 🔄 支持命令组合和流水线
- 🧠 增强上下文感知能力

这些设计理念可以直接应用到 Kimi CLI 的开发中，提升工具的专业性和易用性！
