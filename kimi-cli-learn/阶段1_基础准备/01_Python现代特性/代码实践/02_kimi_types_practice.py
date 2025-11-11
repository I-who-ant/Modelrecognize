"""
练习2: Kimi CLI 参数类型实践

学习目标:
- 模拟 Kimi CLI 的参数设计
- 使用 Literal 和 Path 类型
- 理解类型安全的配置
"""

from typing import Literal, get_args
from pathlib import Path


# 定义 Kimi CLI 的类型
UIMode = Literal["shell", "print", "acp", "wire"]
InputFormat = Literal["text", "stream-json"]
OutputFormat = Literal["text", "stream-json"]


class KimiConfig:
    """Kimi CLI 配置类

    模拟 Kimi CLI 的参数设计模式
    """

    def __init__(
        self,
        work_dir: Path,
        ui: UIMode = "shell",
        input_format: InputFormat = "text",
        output_format: OutputFormat = "text",
        model_name: str | None = None,
        yolo: bool = False,
        debug: bool = False,
    ):
        # 验证 UI 模式
        if ui not in get_args(UIMode):
            valid_modes = ", ".join(get_args(UIMode))
            raise ValueError(f"Invalid UI mode: {ui}. Must be one of: {valid_modes}")

        # 验证工作目录
        self.work_dir = work_dir.absolute()
        if not self.work_dir.exists():
            raise ValueError(f"Work directory does not exist: {self.work_dir}")

        self.ui = ui
        self.input_format = input_format
        self.output_format = output_format
        self.model_name = model_name or "kimi-for-coding"
        self.yolo = yolo
        self.debug = debug

    def is_shell_mode(self) -> bool:
        """检查是否为 Shell 模式"""
        return self.ui == "shell"

    def is_interactive(self) -> bool:
        """检查是否为交互模式"""
        return self.ui in ["shell", "acp"]

    def __repr__(self) -> str:
        return (
            f"KimiConfig(\n"
            f"  work_dir={self.work_dir},\n"
            f"  ui={self.ui},\n"
            f"  model={self.model_name},\n"
            f"  yolo={self.yolo}\n"
            f")"
        )


def main():
    """测试代码"""
    print("=== 练习2: Kimi CLI 参数类型实践 ===\n")

    # 测试1: 创建有效配置
    print("测试1: 创建 Shell 模式配置")
    config1 = KimiConfig(
        work_dir=Path.cwd(),
        ui="shell",
        model_name="kimi-for-coding",
        yolo=True,
    )
    print(config1)
    print(f"是否 Shell 模式: {config1.is_shell_mode()}")
    print(f"是否交互模式: {config1.is_interactive()}\n")

    # 测试2: ACP 模式
    print("测试2: 创建 ACP 模式配置")
    config2 = KimiConfig(
        work_dir=Path.cwd(),
        ui="acp",
        input_format="stream-json",
        output_format="stream-json",
    )
    print(config2)
    print()

    # 测试3: 列出所有可用模式
    print("测试3: 所有可用的 UI 模式")
    print(f"UI 模式: {get_args(UIMode)}")
    print(f"输入格式: {get_args(InputFormat)}")
    print(f"输出格式: {get_args(OutputFormat)}")
    print()

    # 测试4: 无效模式（会抛出异常）
    print("测试4: 尝试使用无效 UI 模式")
    try:
        config_invalid = KimiConfig(
            work_dir=Path.cwd(),
            ui="invalid_mode"  # type: ignore
        )
    except ValueError as e:
        print(f"捕获到错误: {e}")


if __name__ == "__main__":
    main()


# 扩展练习:
# 1. 添加环境变量支持（如 KIMI_MODEL）
# 2. 实现配置文件加载（YAML/JSON）
# 3. 添加参数验证装饰器
# 4. 实现配置的序列化和反序列化
