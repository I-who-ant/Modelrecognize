"""
练习5: 生成器与迭代器实践

学习目标:
- 理解 Generator 和 Iterator 的区别
- 使用 yield 编写生成器
- 掌握生成器表达式
- 使用 itertools 优化代码
"""

from typing import Generator, Iterator
import itertools


# ========== 1. 基础生成器 ==========

def countdown(n: int) -> Generator[int, None, None]:
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1


def fibonacci(n: int) -> Generator[int, None, None]:
    """斐波那契数列生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# ========== 2. 文件处理生成器 ==========

def read_file_in_chunks(file_path: str, chunk_size: int = 1024) -> Generator[str, None, None]:
    """分块读取文件"""
    try:
        with open(file_path, 'r') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")


def read_lines(file_path: str) -> Generator[str, None, None]:
    """按行读取文件（过滤空行）"""
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")



# ========== 3. 数据处理生成器 ==========


def batch_processor(items: list, batch_size: int) -> Generator[list, None, None]:
    # 参数解析 :
    # items : 待处理的数据列表
    # batch_size : 每个批次的大小
    # 返回值解析 :
    # 生成器, 每个元素是一个数据批次, 批次大小为 batch_size


    """分批处理数据"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def filter_and_transform(
    data: Iterator[str]
) -> Generator[dict, None, None]:
    """过滤和转换数据管道"""
    # 第一步: 过滤空行
    filtered = (line.strip() for line in data if line.strip())

    # 第二步: 转换格式
    for i, line in enumerate(filtered):
        yield {
            "index": i,
            "content": line,
            "length": len(line)
        }


# ========== 4. 无限序列生成器 ==========

def counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """无限计数器"""
    current = start
    while True:
        yield current # 生成当前值 ,yield 语句会暂停函数的执行, 并返回当前值

        current += step


def repeat(value, times: int | None = None) -> Generator:
    """重复生成值"""
    if times is None:
        while True:
            yield value # yield相当于return, 但是yield会记住当前的状态, 下次调用时会从当前状态继续执行
    else:
        for _ in range(times):
            yield value


# ========== 5. Iterator 类实现 ==========

class RangeIterator:
    """自定义范围迭代器（模拟 range）"""

    def __init__(self, start: int, end: int, step: int = 1):
        self.current = start
        self.end = end
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration

        value = self.current
        self.current += self.step
        return value


# ========== 演示函数 ==========

def demo_basic_generators():
    """演示基础生成器"""
    print("\n" + "=" * 60)
    print("1. 基础生成器演示")
    print("=" * 60)

    print("\n倒计时:")
    for num in countdown(5):
        print(num, end=" ")
    print()

    print("\n斐波那契数列 (前10项):")
    for num in fibonacci(10):
        print(num, end=" ")
    print("\n")


def demo_batch_processing():
    """演示分批处理"""
    print("\n" + "=" * 60)
    print("2. 分批处理演示")
    print("=" * 60)

    items = list(range(20))
    print(f"原始数据: {items}\n")

    for batch_num, batch in enumerate(batch_processor(items, batch_size=5), 1):
        print(f"批次 {batch_num}: {batch}")


def demo_data_pipeline():
    """演示数据处理管道"""
    print("\n" + "=" * 60)
    print("3. 数据处理管道演示")
    print("=" * 60)

    data = ["  line 1  ", "", "line 2", "  ", "line 3", "line 4"]
    print(f"原始数据: {data}\n")

    print("处理后:")
    for item in filter_and_transform(iter(data)):
        print(f"  {item}")


def demo_infinite_generators():
    """演示无限生成器"""
    print("\n" + "=" * 60)
    print("4. 无限生成器演示")
    print("=" * 60)

    print("\n计数器 (前5个):")
    c = counter(10, 5)
    for _ in range(5):
        print(next(c), end=" ")
    print()

    print("\n重复值 (5次):")
    for val in repeat("Hello", 5):
        print(val, end=" ")
    print("\n")


def demo_generator_expressions():
    """演示生成器表达式"""
    print("\n" + "=" * 60)
    print("5. 生成器表达式演示")
    print("=" * 60)

    # 列表推导式 vs 生成器表达式
    numbers = range(10)

    # 列表推导式（立即计算，占用内存）
    squares_list = [x**2 for x in numbers]
    print(f"列表推导式结果: {squares_list}")

    # 生成器表达式（惰性求值，节省内存）
    squares_gen = (x**2 for x in numbers)
    print(f"生成器表达式: {squares_gen}")
    print(f"生成器结果: {list(squares_gen)}\n")


def demo_itertools():
    """演示 itertools 工具"""
    print("\n" + "=" * 60)
    print("6. itertools 工具演示")
    print("=" * 60)

    # chain: 连接多个迭代器
    print("\nchain - 连接迭代器:")
    combined = itertools.chain([1, 2], [3, 4], [5, 6])
    print(f"  {list(combined)}")

    # islice: 切片迭代器
    print("\nislice - 切片:")
    sliced = itertools.islice(range(100), 10, 20)
    print(f"  {list(sliced)}")

    # cycle: 循环迭代
    print("\ncycle - 循环 (前10个):")
    cycled = itertools.cycle(['A', 'B', 'C'])
    print(f"  {list(itertools.islice(cycled, 10))}")

    # groupby: 分组
    print("\ngroupby - 分组:")
    data = [1, 1, 2, 2, 2, 3, 3, 1, 1]
    for key, group in itertools.groupby(data):
        print(f"  {key}: {list(group)}")


def demo_iterator_class():
    """演示迭代器类"""
    print("\n" + "=" * 60)
    print("7. 迭代器类演示")
    print("=" * 60)

    print("\n自定义 RangeIterator:")
    for num in RangeIterator(0, 10, 2):
        print(num, end=" ")
    print("\n")


def main():
    """主函数"""
    print("\n=== 练习5: 生成器与迭代器实践 ===")

    demo_basic_generators()
    demo_batch_processing()
    demo_data_pipeline()
    demo_infinite_generators()
    demo_generator_expressions()
    demo_itertools()
    demo_iterator_class()

    print("\n" + "=" * 60)
    print("所有演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()


# 扩展练习:
# 1. 实现一个大文件处理器（使用生成器节省内存）
# 2. 实现数据流处理管道（过滤 → 转换 → 聚合）
# 3. 使用 itertools.batched (Python 3.12+) 优化分批处理
# 4. 实现一个支持回溯的迭代器
