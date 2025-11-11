"""
练习1: 类型安全的配置类

学习目标:
- 掌握 Literal 类型
- 使用 get_args() 验证参数
- 类型注解实践
"""

from typing import Literal, Union, Optional, get_args

# 定义配置类型
Environment = Literal["development", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Config:
    """类型安全的配置类

    示例:
        >>> config = Config("development", log_level="DEBUG", debug=True)
        >>> print(config.env)
        development
        >>> print(config.is_production())
        False
    """

    def __init__(
        self,
        env: Environment,
        log_level: LogLevel = "INFO",
        port: int = 8000,
        debug: bool = False,
    ):
        # 验证环境类型
        if env not in get_args(Environment):
            valid_envs = ", ".join(get_args(Environment))
            raise ValueError(
                f"Invalid environment: {env}. "
                f"Must be one of: {valid_envs}"
            )

        # 验证日志级别
        if log_level not in get_args(LogLevel):
            valid_levels = ", ".join(get_args(LogLevel))
            raise ValueError(
                f"Invalid log_level: {log_level}. "
                f"Must be one of: {valid_levels}"
            )

        self.env = env
        self.log_level = log_level
        self.port = port
        self.debug = debug

    def is_production(self) -> bool:
        """检查是否为生产环境"""
        return self.env == "production"

    def is_debug_mode(self) -> bool:
        """检查是否为调试模式"""
        return self.debug or self.log_level == "DEBUG"

    def get_config_dict(self) -> dict[str, Union[str, int, bool]]:
        """获取配置字典"""
        return {
            "env": self.env,
            "log_level": self.log_level,
            "port": self.port,
            "debug": self.debug,
        }

    def __repr__(self) -> str:
        return (
            f"Config(env='{self.env}', log_level='{self.log_level}', "
            f"port={self.port}, debug={self.debug})"
        )


def main():
    """测试代码"""
    print("=== 练习1: 类型安全的配置类 ===\n")

    # 测试1: 正确的配置
    print("测试1: 创建开发环境配置")
    config_dev = Config("development", log_level="DEBUG", debug=True)
    print(f"配置: {config_dev}")
    print(f"是否生产环境: {config_dev.is_production()}")
    print(f"是否调试模式: {config_dev.is_debug_mode()}")
    print(f"配置字典: {config_dev.get_config_dict()}")
    print()

    # 测试2: 生产环境配置
    print("测试2: 创建生产环境配置")
    config_prod = Config("production", log_level="ERROR", port=80)
    print(f"配置: {config_prod}")
    print(f"是否生产环境: {config_prod.is_production()}")
    print()

    # 测试3: 默认参数
    print("测试3: 使用默认参数")
    config_default = Config("staging")
    print(f"配置: {config_default}")
    print()

    # 测试4: 无效的环境（会抛出异常）
    print("测试4: 尝试使用无效环境")
    try:
        config_invalid = Config("invalid_env")  # 这会抛出 ValueError
    except ValueError as e:
        print(f"捕获到错误: {e}")
    print()

    # 测试5: 无效的日志级别
    print("测试5: 尝试使用无效日志级别")
    try:
        config_invalid_log = Config("development", log_level="TRACE")  # ValueError
    except ValueError as e:
        print(f"捕获到错误: {e}")
    print()

    # 测试6: 获取所有可能的环境值
    print("测试6: 获取所有可能的值")
    print(f"可用环境: {get_args(Environment)}")
    print(f"可用日志级别: {get_args(LogLevel)}")


if __name__ == "__main__":
    main()


# 扩展练习:
# 1. 添加更多配置选项（如数据库配置、API密钥等）
# 2. 实现配置的序列化和反序列化（JSON/YAML）
# 3. 添加配置验证逻辑（如端口号范围检查）
# 4. 实现配置的环境变量覆盖功能
