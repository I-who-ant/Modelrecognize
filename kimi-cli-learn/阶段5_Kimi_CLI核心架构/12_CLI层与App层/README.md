# 模块12: CLI 层与 App 层

**学习时长**: 4天

**学习目标**: 深入理解 Kimi CLI 的入口和应用层

---

## 📋 学习内容概览

1. **cli.py 源码分析** (Day 64)
2. **app.py 源码分析** (Day 65)
3. **Session 管理** (Day 66)
4. **Config 配置** (Day 67)

---

## 🎯 学习目标

- ✅ 理解 CLI 层职责
- ✅ 理解 App 层架构
- ✅ 掌握 Session 生命周期
- ✅ 理解配置加载机制

---

## 📚 必读源码

```
src/kimi_cli/
├── cli.py          # 入口，参数解析
├── app.py          # KimiCLI 主类
├── session/        # 会话管理
└── config/         # 配置管理
```

---

## 📖 核心知识点

### CLI 层 (cli.py)

**职责**:
- 命令行参数解析
- 模式路由（shell/print/acp/wire）
- 异步入口封装

**关键代码**:
```python
@click.command()
@click.option("--ui", type=click.Choice(get_args(UIMode)))
def kimi(ui: UIMode, ...):
    async def _run() -> bool:
        instance = await KimiCLI.create(...)
        return await instance.run_shell_mode(...)

    asyncio.run(_run())
```

### App 层 (app.py)

**职责**:
- 实例化核心组件（Soul、LLM、Tools）
- 管理应用生命周期
- 提供不同 UI 模式入口

**关键代码**:
```python
class KimiCLI:
    @staticmethod
    async def create(...) -> "KimiCLI":
        """工厂方法创建实例"""
        # 1. 加载配置
        # 2. 初始化 Session
        # 3. 创建 LLM
        # 4. 初始化 Soul
        # 5. 注册 Tools
        pass

    async def run_shell_mode(self, ...):
        """Shell 模式"""
        from kimi_cli.ui.shell import ShellApp
        app = ShellApp(self._soul, ...)
        return await app.run(...)
```

### Session 管理

**生命周期**:
```
创建 → 加载历史 → 运行 → 保存状态 → 清理
```

**持久化**:
- 工作目录
- 对话历史
- 上下文信息

---

## 📊 实践练习

**练习37**: Debug 启动流程
- 设置断点跟踪完整启动过程
- 画出调用链路图

**练习38**: 添加自定义参数
- 添加一个新的 CLI 参数
- 在 App 层处理该参数

**练习39**: 分析配置加载
- 阅读配置加载代码
- 理解配置优先级

---

## 🔄 下一步

完成本模块后，进入 **模块13: Soul 层**。

---

*Created by 老王 | Last Updated: 2025-01-10*
