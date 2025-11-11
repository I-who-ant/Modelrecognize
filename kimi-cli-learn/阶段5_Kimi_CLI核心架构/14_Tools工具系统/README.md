# 模块14: Tools 工具系统

**学习时长**: 5天

**学习目标**: 深入理解 Kimi CLI 的工具系统，能开发自定义工具

---

## 📋 学习内容概览

1. **文件工具** (Day 73)
2. **Bash 工具** (Day 74)
3. **Task 工具** (Day 75)
4. **Web 工具** (Day 76)
5. **开发自定义工具** (Day 77)

---

## 🎯 学习目标

- ✅ 理解所有内置工具
- ✅ 掌握工具开发规范
- ✅ 能开发自定义工具
- ✅ 理解工具注册机制

---

## 📚 必读源码

```
src/kimi_cli/tools/
├── base.py         # 工具基类
├── registry.py     # 工具注册
├── file/           # 文件工具（Read, Write, Edit, Grep, Glob）
├── bash.py         # Bash 命令执行
├── task.py         # 子 Agent
├── web/            # 网络工具（Search, Fetch）
└── mcp/            # MCP 工具集成
```

---

## 📖 核心知识点

### 工具基类

```python
class Tool(ABC):
    """工具基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """工具描述"""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict:
        """输入 JSON Schema"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
```

### 文件工具系列

1. **Read**: 读取文件
2. **Write**: 写入文件
3. **Edit**: 编辑文件（字符串替换）
4. **Grep**: 搜索文件内容
5. **Glob**: 查找文件

### Bash 工具

**功能**:
- 执行 Shell 命令
- 支持超时控制
- 支持后台运行

**安全性**:
- 命令白名单
- 路径验证
- 权限检查

### Task 工具

**功能**:
- 启动子 Agent
- 分解复杂任务
- 并行执行

**用途**:
- 代码搜索
- 多文件分析
- 复杂任务分解

### 自定义工具开发

**步骤**:

1. 继承 `Tool` 基类
2. 实现必需方法
3. 注册工具
4. 测试验证

**示例**:
```python
class MyCustomTool(Tool):
    @property
    def name(self) -> str:
        return "my_custom_tool"

    @property
    def description(self) -> str:
        return "My custom tool description"

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            },
            "required": ["param1"]
        }

    async def execute(self, param1: str) -> ToolResult:
        # 实现逻辑
        result = do_something(param1)

        return ToolResult(
            success=True,
            message="成功",
            data=result
        )
```

---

## 📊 实践练习

**练习44**: 阅读所有工具源码
- 理解每个工具的实现
- 总结设计模式

**练习45**: 开发自定义工具
- 需求：代码静态分析工具
- 功能：检测代码质量问题
- 集成到 Kimi CLI

**练习46**: 工具集成测试
- 测试工具调用流程
- 验证错误处理

---

## 🔄 下一步

完成本模块后，进入 **阶段6: 实战与扩展**。

---

*Created by 老王 | Last Updated: 2025-01-10*
