# Day28: Coding - 代码生成提示词模板库

> **应用场景**: 代码生成、调试优化、文档编写、代码翻译、重构建议等

---

## 📝 场景概述

### 核心挑战
- 生成代码的正确性和可执行性
- 符合代码规范和最佳实践
- 处理复杂业务逻辑
- 多语言和框架适配

### 技术要求
- 准确理解需求和上下文
- 生成可运行的完整代码
- 提供必要的注释和文档
- 考虑边界情况和异常处理

---

## 🎯 快速模板库

### 模板1: 基础代码生成 (Zero-Shot)

```
任务: 用{编程语言}实现以下功能

功能描述: {具体需求}

要求:
- 代码应该{质量要求,如可读性好、有注释等}
- 包含必要的错误处理
- 遵循{语言}的最佳实践

请直接输出完整可运行的代码。
```

**示例 - Python函数生成**:
```
任务: 用Python实现以下功能

功能描述: 实现一个函数,检查给定的字符串是否是回文

要求:
- 代码应该简洁易读,有清晰的注释
- 包含必要的错误处理
- 遵循Python的最佳实践

→ 输出:
def is_palindrome(s: str) -> bool:
    """
    检查字符串是否是回文

    Args:
        s: 待检查的字符串

    Returns:
        True如果是回文,否则False

    Raises:
        TypeError: 如果输入不是字符串
    """
    if not isinstance(s, str):
        raise TypeError("输入必须是字符串")

    # 转换为小写并移除空格,仅保留字母数字
    cleaned = ''.join(c.lower() for c in s if c.isalnum())

    # 比较字符串和其反转
    return cleaned == cleaned[::-1]

# 测试用例
if __name__ == "__main__":
    test_cases = ["A man a plan a canal Panama", "race a car", ""]
    for test in test_cases:
        print(f"'{test}' is palindrome: {is_palindrome(test)}")
```

---

### 模板2: Few-Shot代码生成 (提升质量)

```
任务: 用{编程语言}实现{功能类型}

参考示例:

示例1 - {功能A}:
{代码示例1}

示例2 - {功能B}:
{代码示例2}

现在请实现: {目标功能描述}

要求:
- 保持与示例相似的代码风格
- {特定要求}
```

**示例 - API端点生成**:
```
任务: 用Express.js实现RESTful API端点

参考示例:

示例1 - 获取用户列表:
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json({ success: true, data: users });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});

示例2 - 创建用户:
app.post('/api/users', async (req, res) => {
  try {
    const { name, email } = req.body;
    const user = await User.create({ name, email });
    res.status(201).json({ success: true, data: user });
  } catch (error) {
    res.status(400).json({ success: false, message: error.message });
  }
});

现在请实现: 更新用户信息的API端点

要求:
- 保持与示例相似的错误处理风格
- 使用PUT方法
- 验证用户ID和请求体

→ 输出:
app.put('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { name, email } = req.body;

    // 验证用户ID
    if (!id || !mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: '无效的用户ID'
      });
    }

    // 验证请求体
    if (!name && !email) {
      return res.status(400).json({
        success: false,
        message: '至少需要提供name或email'
      });
    }

    // 更新用户
    const user = await User.findByIdAndUpdate(
      id,
      { name, email },
      { new: true, runValidators: true }
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        message: '用户不存在'
      });
    }

    res.json({ success: true, data: user });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
});
```

---

### 模板3: CoT代码生成 (复杂逻辑)

```
任务: 实现{复杂功能描述}

请按以下步骤思考并实现:

步骤1: 分析需求
- 核心功能:
- 输入输出:
- 边界情况:

步骤2: 设计方案
- 数据结构:
- 算法选择:
- 时间/空间复杂度:

步骤3: 实现代码
- 主要逻辑:
- 辅助函数:
- 错误处理:

步骤4: 测试验证
- 测试用例:
- 边界测试:

请输出完整的思考过程和最终代码。
```

**示例 - 复杂算法实现**:
```
任务: 实现LRU缓存淘汰算法

步骤1: 分析需求
- 核心功能: 实现固定大小的缓存,淘汰最近最少使用的项
- 输入输出: get(key) 获取值, put(key, value) 设置值
- 边界情况: 缓存满时淘汰,访问不存在的key,容量为0

步骤2: 设计方案
- 数据结构: 哈希表(O(1)查找) + 双向链表(O(1)移动)
- 算法逻辑:
  * get: 查找并移动到链表头部
  * put: 添加到头部,满时删除尾部
- 时间复杂度: O(1) get和put操作
- 空间复杂度: O(capacity)

步骤3: 实现代码

class Node:
    """双向链表节点"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """LRU缓存实现"""

    def __init__(self, capacity: int):
        """
        初始化LRU缓存

        Args:
            capacity: 缓存容���
        """
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # 哨兵节点,简化边界处理
        self.head = Node()  # 最近使用
        self.tail = Node()  # 最久未使用
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: Node):
        """从链表移除节点"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node):
        """添加节点到链表头部(最近使用)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: Node):
        """移动节点到头部"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> Node:
        """移除尾部节点(最久未使用)"""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        """
        获取缓存值

        Args:
            key: 键

        Returns:
            存在返回值,不存在返回-1
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)  # 标记为最近使用
        return node.value

    def put(self, key: int, value: int):
        """
        设置缓存值

        Args:
            key: 键
            value: 值
        """
        if key in self.cache:
            # 更新已存在的key
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # 添加新key
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)

            # 检查容量
            if len(self.cache) > self.capacity:
                # 淘汰最久未使用的
                removed = self._remove_tail()
                del self.cache[removed.key]

步骤4: 测试验证

# 测试用例1: 基本功能
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1  # 返回1

cache.put(3, 3)  # 淘汰key 2
assert cache.get(2) == -1  # 不存在

# 测试用例2: 访问更新顺序
cache.put(4, 4)  # 淘汰key 1
assert cache.get(1) == -1
assert cache.get(3) == 3
assert cache.get(4) == 4

# 边界测试: 容量为1
cache = LRUCache(1)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == -1
assert cache.get(2) == 2
```

---

### 模板4: 代码调试优化

```
任务: 调试和优化以下代码

原始代码:
{有问题的代码}

问题描述: {具体问题,如报错、性能差、逻辑错误等}

请按以下格式输出:

1. 问题分析:
   - 根本原因:
   - 影响范围:

2. 修复方案:
   - 修复代码:
   - 修改说明:

3. 优化建议:
   - 性能优化:
   - 代码质量:

4. 测试验证:
   - 测试用例:
```

**示例 - 性能优化**:
```
任务: 调试和优化以下代码

原始代码:
def find_duplicates(nums):
    duplicates = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] == nums[j]:
                if nums[i] not in duplicates:
                    duplicates.append(nums[i])
    return duplicates

问题描述: 在处理大数组时性能很差,时间复杂度过高

1. 问题分析:
   - 根本原因: 使用了O(n²)的双重循环,且多次使用`in`操作(O(n))
   - 总体复杂度: O(n³)
   - 影响范围: 数组长度>1000时明显变慢

2. 修复方案:

修复代码:
def find_duplicates(nums):
    """
    查找数组中的重复元素

    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    seen = set()
    duplicates = set()

    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)

    return list(duplicates)

修改说明:
- 使用set代替list,in操作从O(n)降为O(1)
- 单次遍历代替双重循环,O(n²) → O(n)
- 总体复杂度从O(n³)降为O(n)

3. 优化建议:

性能优化:
- 如果需要保持原始顺序,可使用collections.Counter:
  from collections import Counter
  def find_duplicates_ordered(nums):
      counts = Counter(nums)
      return [num for num, count in counts.items() if count > 1]

- 内存受限场景,可使用原地算法(要求nums可修改且值范围是1到n):
  def find_duplicates_inplace(nums):
      result = []
      for num in nums:
          idx = abs(num) - 1
          if nums[idx] < 0:
              result.append(abs(num))
          else:
              nums[idx] = -nums[idx]
      return result

代码质量:
- 添加类型提示: def find_duplicates(nums: List[int]) -> List[int]
- 添加docstring说明函数用途
- 考虑边界情况: 空数组、单元素数组

4. 测试验证:

import time

# 性能对比测试
test_data = list(range(1000)) * 2  # 2000个元素,1000个重复

# 原始版本
start = time.time()
# result_old = find_duplicates_old(test_data)  # 会很慢
# print(f"原始版本耗时: {time.time() - start:.3f}s")

# 优化版本
start = time.time()
result_new = find_duplicates(test_data)
print(f"优化版本耗时: {time.time() - start:.4f}s")

# 正确性测试
assert set(find_duplicates([1,2,3,1,2])) == {1,2}
assert find_duplicates([1,2,3,4]) == []
assert find_duplicates([]) == []
```

---

### 模板5: 代码文档生成

```
任务: 为以下代码生成完整文档

代码:
{待文档化的代码}

请生成:
1. 函数/类的docstring (Google风格或NumPy风格)
2. 参数说明
3. 返回值说明
4. 使用示例
5. 注意事项/边界情况
```

**示例 - API文档生成**:
```
任务: 为以下代码生成完整文档

代码:
def binary_search(arr, target, left=0, right=None):
    if right is None:
        right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

→ 输出完整文档:

def binary_search(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
    """
    在有序数组中使用二分查找搜索目标值

    使用经典的二分查找算法,在已排序的数组中高效查找目标值的索引位置。
    如果目标值不存在,返回-1。

    Args:
        arr (List[int]): 已排序的整数数组(升序)
        target (int): 要查找的目标值
        left (int, optional): 搜索范围的左边界索引,默认为0
        right (Optional[int], optional): 搜索范围的右边界索引,默认为数组最后一个索引

    Returns:
        int: 目标值在数组中的索引,如果不存在则返回-1

    Raises:
        TypeError: 如果arr不是列表或target不是整数
        ValueError: 如果left或right超出数组范围

    Examples:
        >>> arr = [1, 3, 5, 7, 9, 11]
        >>> binary_search(arr, 7)
        3

        >>> binary_search(arr, 6)
        -1

        >>> binary_search(arr, 5, left=2, right=4)
        2

    Note:
        - 数组必须是有序的(升序),否则结果不可预测
        - 时间复杂度: O(log n)
        - 空间复杂度: O(1)
        - 如果数组包含重复元素,返回的是任意一个匹配位置

    See Also:
        - bisect.bisect_left: 标准库中的二分查找实现
        - arr.index(): 线性查找,O(n)复杂度
    """
    # 参数验证
    if not isinstance(arr, list):
        raise TypeError("arr必须是列表类型")
    if not isinstance(target, int):
        raise TypeError("target必须是整数类型")

    if right is None:
        right = len(arr) - 1

    if left < 0 or right >= len(arr) or left > right:
        raise ValueError(f"无效的搜索范围: left={left}, right={right}")

    while left <= right:
        # 使用位运算避免整数溢出
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

---

### 模板6: 多语言代码翻译

```
任务: 将以下{源语言}代码翻译为{目标语言}

源代码({源语言}):
{代码}

要求:
- 保持相同的功能逻辑
- 遵循{目标语言}的习惯用法
- 保留注释并翻译
- 适配语言特性差异

请输出:
1. 翻译后的代码
2. 关键差异说明
3. 使用注意事项
```

**示例 - Python转JavaScript**:
```
任务: 将以下Python代码翻译为JavaScript

源代码(Python):
def fibonacci(n):
    """生成斐波那契数列的前n项"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]

    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])

    return fib

# 使用装饰器缓存
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_recursive(n):
    """递归���现(带缓存)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

→ 输出:

1. 翻译后的代码:

/**
 * 生成斐波那契数列的前n项
 * @param {number} n - 要生成的项数
 * @returns {number[]} 斐波那契数列数组
 */
function fibonacci(n) {
    if (n <= 0) {
        return [];
    } else if (n === 1) {
        return [0];
    }

    const fib = [0, 1];
    for (let i = 2; i < n; i++) {
        fib.push(fib[i-1] + fib[i-2]);
    }

    return fib;
}

/**
 * 递归实现斐波那契(带缓存)
 * JavaScript中使用闭包实现类似lru_cache的功能
 */
const fibonacciRecursive = (() => {
    const cache = new Map();

    return function fib(n) {
        if (n <= 1) {
            return n;
        }

        if (cache.has(n)) {
            return cache.get(n);
        }

        const result = fib(n - 1) + fib(n - 2);
        cache.set(n, result);
        return result;
    };
})();

// ES6+ 版本: 使用生成器
function* fibonacciGenerator(n) {
    let [a, b] = [0, 1];
    for (let i = 0; i < n; i++) {
        yield a;
        [a, b] = [b, a + b];
    }
}

// 使用示例
console.log(fibonacci(10));  // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
console.log(fibonacciRecursive(10));  // 55
console.log([...fibonacciGenerator(10)]);  // [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

2. 关��差异说明:

语法差异:
- Python的`elif` → JavaScript的`else if`
- Python的`append()` → JavaScript的`push()`
- Python的列表推导 → JavaScript的生成器或Array.from()

装饰器实现:
- Python的`@lru_cache`是内置装饰器语法
- JavaScript使用闭包+Map手动实现缓存
- 也可以使用Proxy或装饰器提案(需要Babel)

类型系统:
- Python有类型提示(可选)
- JavaScript可使用JSDoc或TypeScript
- 建议在TS中使用: `function fibonacci(n: number): number[]`

3. 使用注意事项:

性能对比:
- JavaScript的数组操作通常比Python快
- 但大数计算Python有优势(支持任意精度整数)
- JS中超过Number.MAX_SAFE_INTEGER需用BigInt

最佳实践:
- 生产环境建议使用TypeScript版本保证类型安全
- 可以使用lodash.memoize简化缓存实现
- 考虑使用尾递归优化(需要严格模式)
```

---

### 模板7: 代码重构建议

```
任务: 重构以下代码以提升质量

原始代码:
{待重构的代码}

重构目标: {如提升可读性、减少重复、改进架构等}

请按以下格式输出:

1. 代码问题识别:
   - 坏味道列表:
   - 违反的原则:

2. 重构方案:
   - 重构手法:
   - 重构后代码:

3. 改进效果:
   - 可读性提升:
   - 可维护性提升:
   - 性能影响:

4. 迁移建议:
   - 重构步骤:
   - 测试策略:
```

**示例 - 提取类重构**:
```
任务: 重构以下代码以提升质量

原始代码:
class User:
    def __init__(self, name, email, street, city, zipcode):
        self.name = name
        self.email = email
        self.street = street
        self.city = city
        self.zipcode = zipcode

    def get_full_address(self):
        return f"{self.street}, {self.city} {self.zipcode}"

    def send_email(self, subject, body):
        # 发送邮件逻辑
        print(f"Sending to {self.email}: {subject}")
        # SMTP代码...

    def validate_email(self):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

重构目标: 提升可维护性,遵循单一职责原则

1. 代码问题识别:

坏味道列表:
- 过大的类: User类承担了用户信息、地址、邮件三种职责
- 功能嫉妒: send_email和validate_email应该属于Email相关的类
- 数据泥团: street, city, zipcode应该封装为Address对象

违反的原则:
- 单一职责原则(SRP): 一个类应该只有一个改变的理由
- 开放封闭原则(OCP): 添加新功能需要修改User类

2. 重构方案:

重构手法:
- 提取类(Extract Class): 将Address和Email相关逻辑分离
- 搬移方法(Move Method): 将方法移到合适的类
- 引入值对象(Value Object): Address作为值对象

重构后代码:

from dataclasses import dataclass
from typing import Optional
import re

@dataclass(frozen=True)
class Address:
    """地址值对象"""
    street: str
    city: str
    zipcode: str

    def get_full_address(self) -> str:
        """获取完整地址字符串"""
        return f"{self.street}, {self.city} {self.zipcode}"

    def __str__(self) -> str:
        return self.get_full_address()

@dataclass
class Email:
    """邮箱值对象"""
    address: str

    def __post_init__(self):
        if not self.is_valid():
            raise ValueError(f"无效的邮箱地址: {self.address}")

    def is_valid(self) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.address) is not None

    def __str__(self) -> str:
        return self.address

class EmailService:
    """邮件服务"""

    @staticmethod
    def send(to: Email, subject: str, body: str) -> bool:
        """
        发送邮件

        Args:
            to: 收件人邮箱
            subject: 邮件主题
            body: 邮件正文

        Returns:
            发送成功返回True
        """
        try:
            print(f"Sending to {to}: {subject}")
            # SMTP实现...
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False

class User:
    """用户实体"""

    def __init__(self, name: str, email: Email, address: Address):
        self.name = name
        self.email = email
        self.address = address

    def send_notification(self, subject: str, body: str) -> bool:
        """发送通知邮件"""
        return EmailService.send(self.email, subject, body)

    def __repr__(self) -> str:
        return f"User(name={self.name}, email={self.email})"

# 使用示例
address = Address(
    street="123 Main St",
    city="Springfield",
    zipcode="12345"
)

email = Email("john@example.com")

user = User(
    name="John Doe",
    email=email,
    address=address
)

print(f"用户地址: {user.address}")
user.send_notification("Welcome", "欢迎使用我们的服务")

3. 改进效果:

可读性提升:
- ✅ 每个类职责清晰明���
- ✅ 使用dataclass减少样板代码
- ✅ 类型提示提升代码可读性

可维护性提升:
- ✅ Address和Email可独立测试
- ✅ 修改邮件逻辑只需改EmailService
- ✅ 添加新地址格式只需修改Address
- ✅ User类简化,更易维护

性能影响:
- ⚠️ 创建了更多对象,轻微内存开销
- ✅ frozen=True的Address可以安全缓存
- ✅ EmailService可以方便添加连接池等优化

4. 迁移建议:

重构步骤:
Step 1: 创建Address类,测试通过
Step 2: 创建Email类,测试通过
Step 3: 创建EmailService类,测试通过
Step 4: 修改User类使用新类,逐步迁移
Step 5: 删除User类中的旧方法
Step 6: 更新所有调用代码

测试策略:
- 为每个新类编写单元测试
- 保持User类的集成测试不变
- 使用适配器模式兼容旧接口(过渡期)
- 逐个模块迁移,降低风险

迁移代码示例(兼容旧接口):
class UserLegacy(User):
    """向后兼容的User类"""

    def __init__(self, name, email_str, street, city, zipcode):
        email = Email(email_str)
        address = Address(street, city, zipcode)
        super().__init__(name, email, address)

    @property
    def email(self):
        return self._email.address  # 返回字符串兼容旧代码

    def get_full_address(self):
        return self.address.get_full_address()
```

---

### 模板8: PAL代码执行 (Program-Aided Language)

```
任务: 解决以下问题,生成并执行Python代码

问题: {数学/逻辑问题描述}

解决步骤:
1. 分析问题,识别需要计算的部分
2. 编写Python代码实现计算逻辑
3. 执行代码获得结果
4. 验证结果合理性

请输出:
- 分析过程
- 完整可执行代码
- 执行结果
- 结果解释
```

**示例 - 数学问题求解**:
```
任务: 解决以下问题,生成并执行Python代码

问题: 一个公司有23名员工。每个员工每周工作5天,每天8小时。
如果公司支付每小时15美元,并且提供20%的福利成本,
那么公司每月(按4周计算)的总人力成本是多少?

解决步骤:

步骤1: 分析问题
- 员工数量: 23人
- 工作时间: 5天/周 × 8小时/天 = 40小时/周
- 时薪: $15/小时
- 福利成本: 工资的20%
- 计算周期: 4周/月

步骤2: 编写计算代码

def calculate_monthly_labor_cost():
    """
    计算公司月度总人力成本

    Returns:
        tuple: (基本工资, 福利成本, 总成本)
    """
    # 基础参数
    num_employees = 23
    hours_per_day = 8
    days_per_week = 5
    hourly_rate = 15
    benefit_rate = 0.20
    weeks_per_month = 4

    # 计算每周工作小时数
    hours_per_week = hours_per_day * days_per_week
    print(f"每周工作小时: {hours_per_week}")

    # 计算每月工作小时数
    hours_per_month = hours_per_week * weeks_per_month
    print(f"每月工作小时: {hours_per_month}")

    # 计算单个员工月工资
    salary_per_employee = hours_per_month * hourly_rate
    print(f"单个员工月工资: ${salary_per_employee:,.2f}")

    # 计算所有员工基本工资
    total_salary = num_employees * salary_per_employee
    print(f"总基本工资: ${total_salary:,.2f}")

    # 计算福利成本
    benefit_cost = total_salary * benefit_rate
    print(f"福利成本 (20%): ${benefit_cost:,.2f}")

    # 计算总人力成本
    total_cost = total_salary + benefit_cost
    print(f"月度总人力成本: ${total_cost:,.2f}")

    return total_salary, benefit_cost, total_cost

# 执行计算
salary, benefits, total = calculate_monthly_labor_cost()

步骤3: 执行结果

每周工作小时: 40
每月工作小时: 160
单个员工月工资: $2,400.00
总基本工资: $55,200.00
福利成本 (20%): $11,040.00
月度总人力成本: $66,240.00

步骤4: 结果验证

# 验证计算逻辑
assert 8 * 5 == 40, "每周工作小时计算错误"
assert 40 * 4 == 160, "每月工作小时计算错误"
assert 160 * 15 == 2400, "单人月工资计算错误"
assert 2400 * 23 == 55200, "总工资计算错误"
assert 55200 * 1.20 == 66240, "总成本计算错误"

print("✅ 所有验证通过")

# 敏感性分析: 如果员工数量增加10%会怎样?
new_employees = 23 * 1.1
new_cost = new_employees * 2400 * 1.20
increase = new_cost - total
print(f"\n📊 敏感性��析:")
print(f"员工数增加10% ({23} → {new_employees:.1f}人)")
print(f"成本增加: ${increase:,.2f} ({increase/total*100:.1f}%)")

最终答案:
公司每月的总人力成本是 $66,240.00
其中基本工资 $55,200.00,福利成本 $11,040.00
```

---

## 💡 最佳实践

### 1. 选择合适的模板

```
简单功能实现 (单个函数/方法):
└─ 使用模板1: 基础Zero-Shot生成

复杂逻辑 (算法/架构):
└─ 使用模板3: CoT逐步推理生成

需要特定风格:
└─ 使用模板2: Few-Shot示例引导

性能问题/Bug修复:
└─ 使用模板4: 调试优化

缺少文档:
└─ 使用模板5: 文档���成

跨语言迁移:
└─ 使用模板6: 代码翻译

代码质量差:
└─ 使用模板7: 重构建议

数学/逻辑计算:
└─ 使用模板8: PAL代码执行
```

### 2. 提升代码质量技巧

**明确需求**:
1. 详细描述功能需求和边界条件
2. 指定编程语言和版本
3. 说明代码规范和风格要求
4. 提供输入输出示例

**提供上下文**:
1. 给出项目结构和技术栈
2. 说明相关依赖和框架
3. 提供已有代码片段作为参考
4. 说明性能和安全要求

**迭代改进**:
1. 先生成基础版本验证逻辑
2. 逐步添加错误处理和边界情况
3. 优化性能和代码质量
4. 补充文档和测试用例

---

## 🔧 技术融合

### 结合前置技术

```
Day6: Zero-Shot
└─ 基础代码生成,适合简单功能

Day7: Few-Shot
└─ 通过示例学习代码风格和模式

Day8: Chain-of-Thought
└─ 复杂算法的逐步实现

Day18: PAL
└─ 数学逻辑问题的代码求解

Day13: RAG
└─ 检索API文档辅助代码生成

Day22: Function Calling
└─ 代码生成 + 工具调用 = 智能开发助手
```

### 实战案例

**案例1: API开发助手**

```python
# 结合RAG + Few-Shot的API生成

prompt = """
任务: 生成RESTful API端点

参考文档(从RAG检索):
{api_framework_docs}

代码风格参考(Few-Shot):
{existing_api_examples}

需求:
- 资源: {resource_name}
- 操作: {operations}
- 认证: {auth_type}
- 数据验证: {validation_rules}

请生成完整的API实现,包括:
1. 路由定义
2. 请求处理
3. 数据验证
4. 错误处理
5. API文档注释
"""
```

**案例2: 代码审查助手**

```python
# 结合CoT + 重构建议

prompt = """
任务: 审查以下Pull Request代码

代码变更:
{code_diff}

审查维度:
1. 功能正确性 (逻辑是否正确)
2. 代码质量 (可读性、可维护性)
3. 性能影响 (是否引入性能问题)
4. 安全性 (是否有安全隐患)
5. 测试覆盖 (是否需要补充测试)

请按CoT方式逐步分析:
- 步骤1: 理解代码变更的目的
- 步骤2: 识别潜在问题
- 步骤3: 提出改进建议
- 步骤4: 给出修改后的代码(如有必要)
"""
```

---

## 📊 效果评估

### 评估维度

```
功能正确性:
- 代码是否满足需求
- 是否处理边界情况
- 目标: 100%符合需求

代码质量:
- 可读性、可维护性
- 遵循最佳实践
- 目标: 符合团队规范

性能:
- 时间/空间复杂度
- 是否有明显瓶颈
- 目标: 符合性能要求

安全性:
- 是否有安全漏洞
- 输入验证是否充分
- 目标: 通过安全审查
```

---

## ⚠️ 常见陷阱

### 陷阱1: 需求描述不清

```
❌ 错误:
"写一个排序函数"

✅ 正确:
"用Python实现快速排序算法,要求:
- 输入: 整数列表
- 输出: 升序排序后的新列表(不修改原列表)
- 时间复杂度: O(n log n)平均情况
- 包含类型提示和docstring"
```

### 陷阱2: 忽略边界情况

```
❌ 错误: 只考虑正常情况

✅ 正确: 明确说明需要处理的边界情况
- 空输入
- None值
- 极大/极小值
- 异常情况
```

### 陷阱3: 缺少测试验证

```
❌ 错误: 生成代码后直接使用

✅ 正确: 要求生成测试用例
- 正常情况测试
- 边界情况测试
- 异常情况测试
- 性能测试(如需要)
```

---

## 🎯 实战练习

### 练习1: 数据结构实现

```
任务: 实现一个线程安全的LRU Cache

要求:
- 使用Python实现
- 支持get和put操作,都是O(1)复杂度
- 线程安全(使用锁)
- 包含完整的类型提示和文档
- 提供使用示例和测试用例

提示: 使用CoT模板,逐步分析并实现
```

### 练习2: API重构

```
任务: 重构以下Flask API代码

原始代码:
@app.route('/users/<id>')
def get_user(id):
    user = db.query(f"SELECT * FROM users WHERE id={id}")
    return jsonify(user)

问题:
- SQL注入风险
- 缺少错误处理
- 没有输入验证
- 缺少API文档

要求: 使用重构模板完整重构
```

### 练习3: 算法优化

```
任务: 优化以下斐波那契数列生成代码

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

问题: 时间复杂度O(2^n),n>30时极慢

要求:
- 提供3种优化方案(记忆化、动态规划、矩阵快速幂)
- 对比各方案的时间/空间复杂度
- 提供性能测试代码
```

---

## 📚 参考资源

**官方资源**:
- Prompt Engineering Guide: https://www.promptingguide.ai/prompts/coding
- OpenAI Cookbook: Code Generation Examples

**扩展阅读**:
- PAL: Program-Aided Language Models
- CodeGen最佳实践
- AI辅助编程工具对比

---

**下一步**: Day29 - Creativity (创意写作提示词)
