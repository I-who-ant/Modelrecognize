"""
练习4: 上下文管理器实践

学习目标:
- 理解上下文管理器的作用
- 使用 @contextmanager 装饰器
- 实现实用的上下文管理器
"""

import contextlib
import time
import os
from pathlib import Path
import tempfile


# ========== 1. 计时器上下文管理器 ==========

@contextlib.contextmanager
def timer(name: str):
    """计时器上下文管理器

    用法:
        with timer("数据处理"):
            process_data()
    """
    start = time.time()
    print(f"[{name}] 开始...")
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"[{name}] 完成，耗时: {elapsed:.2f}秒")


# ========== 2. 临时目录切换 ==========

@contextlib.contextmanager
def temporary_directory(path: Path):
    """临时切换工作目录

    用法:
        with temporary_directory(Path("/tmp")):
            # 在 /tmp 目录下工作
            pass
    """
    original_dir = Path.cwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original_dir)


# ========== 3. 环境变量设置 ==========

@contextlib.contextmanager
def env_vars(**kwargs):
    """临时设置环境变量

    用法:
        with env_vars(API_KEY="test-key", DEBUG="true"):
            # 使用临时环境变量
            pass
    """
    original = {}
    for key, value in kwargs.items():
        original[key] = os.environ.get(key)
        os.environ[key] = str(value)

    try:
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


# ========== 4. 文件锁（模拟）==========

@contextlib.contextmanager
def file_lock(file_path: Path):
    """文件锁上下文管理器（简化版）

    用法:
        with file_lock(Path("data.txt")):
            # 处理文件
            pass
    """
    lock_file = file_path.with_suffix(file_path.suffix + ".lock")

    # 获取锁
    if lock_file.exists():
        raise RuntimeError(f"文件已被锁定: {file_path}")

    lock_file.touch()
    print(f"🔒 已锁定: {file_path}")

    try:
        yield file_path
    finally:
        # 释放锁
        lock_file.unlink(missing_ok=True)
        print(f"🔓 已解锁: {file_path}")


# ========== 5. 临时文件 ==========

@contextlib.contextmanager
def temporary_file(content: str = "", suffix: str = ".txt"):
    """创建临时文件

    用法:
        with temporary_file("测试内容") as temp_path:
            print(f"临时文件: {temp_path}")
    """
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix=suffix,
        delete=False
    ) as f:
        f.write(content)
        temp_path = Path(f.name)

    try:
        yield temp_path
    finally:
        temp_path.unlink(missing_ok=True)


# ========== 6. 类实现方式 ==========

class ManagedResource:
    """使用类实现上下文管理器"""

    def __init__(self, name: str):
        self.name = name
        self.resource = None

    def __enter__(self):
        print(f"获取资源: {self.name}")
        self.resource = f"Resource[{self.name}]"
        return self.resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"释放资源: {self.name}")
        self.resource = None
        # 返回 False 表示不抑制异常
        return False


# ========== 演示函数 ==========

def demo_timer():
    """演示计时器"""
    print("\n" + "=" * 60)
    print("1. 计时器演示")
    print("=" * 60)

    with timer("睡眠1秒"):
        time.sleep(1)

    with timer("睡眠0.5秒"):
        time.sleep(0.5)


def demo_directory_switch():
    """演示目录切换"""
    print("\n" + "=" * 60)
    print("2. 临时目录切换演示")
    print("=" * 60)

    print(f"当前目录: {Path.cwd()}")

    with temporary_directory(Path("/tmp")):
        print(f"切换到: {Path.cwd()}")

    print(f"恢复到: {Path.cwd()}")


def demo_env_vars():
    """演示环境变量"""
    print("\n" + "=" * 60)
    print("3. 环境变量演示")
    print("=" * 60)

    print(f"原始 API_KEY: {os.environ.get('API_KEY', '未设置')}")

    with env_vars(API_KEY="test-key-123", DEBUG="true"):
        print(f"临时 API_KEY: {os.environ.get('API_KEY')}")
        print(f"临时 DEBUG: {os.environ.get('DEBUG')}")

    print(f"恢复后 API_KEY: {os.environ.get('API_KEY', '未设置')}")


def demo_file_lock():
    """演示文件锁"""
    print("\n" + "=" * 60)
    print("4. 文件锁演示")
    print("=" * 60)

    test_file = Path("test_lock.txt")
    test_file.write_text("测试内容")

    try:
        with file_lock(test_file):
            print(f"正在处理文件: {test_file}")
            time.sleep(0.5)
    finally:
        test_file.unlink(missing_ok=True)


def demo_temporary_file():
    """演示临时文件"""
    print("\n" + "=" * 60)
    print("5. 临时文件演示")
    print("=" * 60)

    with temporary_file("这是临时内容", suffix=".txt") as temp_path:
        print(f"临时文件路径: {temp_path}")
        print(f"临时文件内容: {temp_path.read_text()}")
        print(f"文件存在: {temp_path.exists()}")

    print(f"退出后文件存在: {temp_path.exists()}")


def demo_class_context_manager():
    """演示类实现的上下文管理器"""
    print("\n" + "=" * 60)
    print("6. 类实现的上下文管理器")
    print("=" * 60)

    with ManagedResource("数据库连接") as resource:
        print(f"使用资源: {resource}")


def main():
    """主函数"""
    print("\n=== 练习4: 上下文管理器实践 ===")

    demo_timer()
    demo_directory_switch()
    demo_env_vars()
    demo_file_lock()
    demo_temporary_file()
    demo_class_context_manager()

    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 扩展练习:
# 1. 实现数据库连接的上下文管理器
# 2. 实现日志级别临时切换的上下文管理器
# 3. 实现异常捕获和日志记录的上下文管理器
# 4. 分析 Kimi CLI 的 _app_env 上下文管理器实现
