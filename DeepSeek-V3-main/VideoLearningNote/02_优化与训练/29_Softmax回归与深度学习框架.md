from torch.nn.functional import softmax

# Softmax回归与深度学习框架

**学习日期**: 2025-10-30
**课程来源**: 深度学习优化与训练系列
**重要程度**: 🔴必学 ⭐⭐⭐
**前置知识**: 逻辑回归、梯度下降、交叉熵损失
**关键地位**: 多分类任务的基础，深度学习框架的入门

---

## 📌 本节概述

本节包含三个紧密相关的主题：

```
1. Softmax回归 (Softmax Regression)
   └─ 多分类问题的数学基础

2. 训练Softmax分类器
   └─ 如何在实践中训练多分类模型

3. 深度学习框架
   └─ PyTorch、TensorFlow等工具的使用
```

---

# 第一部分：Softmax回归

## 📖 基本定义

**Softmax回归**（也称为多元逻辑回归）是逻辑回归在多分类问题上的推广。它将输入映射到多个类别的概率分布上。

### 核心思想

```
二分类 (Logistic Regression):
  输出: P(y=1|x)  单个概率
  激活: Sigmoid

多分类 (Softmax Regression):
  输出: [P(y=1|x), P(y=2|x), ..., P(y=K|x)]  概率分布
  激活: Softmax
```

---

## 🎯 为什么需要Softmax？

### 问题场景

```
手写数字识别 (MNIST):
  输入: 28×28 图像
  输出: 0, 1, 2, ..., 9  (10个类别)

图像分类 (ImageNet):
  输入: 224×224 彩色图像
  输出: 1000个类别

文本分类:
  输入: 文本
  输出: 新闻类别 (体育/财经/娱乐/...)
```

**问题**：如何输出多个类别的概率？

### Softmax的解决方案

```
原始输出 (logits):
  z₁ = 2.0
  z₂ = 1.0
  z₃ = 0.1

Softmax转换:
  p₁ = e^2.0 / (e^2.0 + e^1.0 + e^0.1) = 0.659
  p₂ = e^1.0 / (e^2.0 + e^1.0 + e^0.1) = 0.242
  p₃ = e^0.1 / (e^2.0 + e^1.0 + e^0.1) = 0.099

性质:
  ✓ 所有概率为正: pᵢ > 0
  ✓ 概率和为1: Σpᵢ = 1
  ✓ 保持大小关系: z₁ > z₂ > z₃ → p₁ > p₂ > p₃
```

---

## 🔧 Softmax数学原理

### 1️⃣ Softmax函数定义

**单个样本的Softmax**:

```python
# 输入: z = [z₁, z₂, ..., zₖ]  (K个类别的原始分数)
# 输出: p = [p₁, p₂, ..., pₖ]  (K个类别的概率)

对于第 i 类:
  pᵢ = exp(zᵢ) / Σⱼ₌₁ᴷ exp(zⱼ)

其中:
- zᵢ: 第i类的原始分数 (logits)
- pᵢ: 第i类的预测概率
- K: 类别总数
```

**数值稳定性问题**:

```python
问题: 当 zᵢ 很大时，exp(zᵢ) 会溢出

例子:
  z = [1000, 2000, 3000]
  exp(3000) ≈ ∞  (数值溢出!)

解决: 减去最大值
  z_stable = z - max(z)
  z_stable = [1000-3000, 2000-3000, 3000-3000]
            = [-2000, -1000, 0]

  exp(0) / (exp(-2000) + exp(-1000) + exp(0))
  ≈ 1 / (0 + 0 + 1) = 1

数学上等价:
  exp(zᵢ - max(z)) / Σⱼ exp(zⱼ - max(z))
  = exp(zᵢ) / Σⱼ exp(zⱼ)
```

### 2️⃣ Softmax回归模型

**完整的前向传播**:

```
输入: x ∈ ℝᵈ  (d维特征向量)

线性变换:
  z = W·x + b
  其中:
    W ∈ ℝᴷˣᵈ (权重矩阵)
    b ∈ ℝᴷ   (偏置向量)
    z ∈ ℝᴷ   (K个类别的logits)

Softmax激活:
  p = softmax(z)
  pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)

预测:
  ŷ = argmax(p)  (选择概率最大的类别)
```

**向量化形式**:

```python
# 批量处理 m 个样本
X: (m, d)  # m个样本，每个d维
W: (d, K)  # 权重矩阵
b: (K,)    # 偏置向量

Z = X @ W + b        # (m, K) logits
P = softmax(Z)       # (m, K) 概率分布
```

### 3️⃣ 损失函数：交叉熵

**单个样本的交叉熵损失**:

```python
L(y, p) = -Σᵢ₌₁ᴷ yᵢ · log(pᵢ)

其中:
- y = [0, 0, 1, 0, ..., 0]  (one-hot编码的真实标签)
- p = [p₁, p₂, p₃, p₄, ..., pₖ] (预测概率)

简化:
  如果真实类别是 c，则:
  L = -log(pᶜ)

  目标: 最大化正确类别的概率 pᶜ
       等价于最小化 -log(pᶜ)
```

**批量损失**:

```python
# m个样本的平均损失
J = (1/m) · Σⱼ₌₁ᵐ L⁽ʲ⁾
  = -(1/m) · Σⱼ₌₁ᵐ log(p⁽ʲ⁾_yⱼ)

其中:
- j: 样本索引
- yⱼ: 第j个样本的真实类别
- p⁽ʲ⁾_yⱼ: 第j个样本在真实类别上的预测概率
```

---

## 🧮 梯度推导

### Softmax-交叉熵的梯度

**关键结论**（非常优雅！）:

```python
∂L/∂zᵢ = pᵢ - yᵢ

其中:
- zᵢ: 第i类的logit
- pᵢ: 第i类的预测概率
- yᵢ: 第i类的真实标签 (one-hot中的值)

例子:
  真实类别: 2 (y = [0, 0, 1, 0])
  预测概率: p = [0.1, 0.2, 0.6, 0.1]

  梯度: ∂L/∂z = [0.1, 0.2, -0.4, 0.1]
                = p - y

意义:
  - 预测概率 > 真实标签 → 正梯度 → 减小 zᵢ
  - 预测概率 < 真实标签 → 负梯度 → 增大 zᵢ
```

**完整的反向传播**:

```python
# 1. 损失对logits的梯度
dZ = P - Y  # (m, K)

# 2. 损失对权重的梯度
dW = (1/m) · X.T @ dZ  # (d, K)

# 3. 损失对偏置的梯度
db = (1/m) · np.sum(dZ, axis=0)  # (K,)

# 4. 损失对输入的梯度（如果需要）
dX = dZ @ W.T  # (m, d)
```

---

## 💻 NumPy实现

```python
import numpy as np

class SoftmaxRegression:
    """Softmax回归分类器"""

    def __init__(self, input_dim, num_classes):
        """
        参数:
            input_dim: 输入特征维度
            num_classes: 类别数量
        """
        self.input_dim = input_dim
        self.num_classes = num_classes

        # 初始化权重（Xavier初始化）
        self.W = np.random.randn(input_dim, num_classes) * np.sqrt(2.0 / input_dim)
        self.b = np.zeros(num_classes)

    def softmax(self, z):
        """
        Softmax激活函数（数值稳定版本）

        参数:
            z: (m, K) logits矩阵
        返回:
            p: (m, K) 概率矩阵
        """
        # 数值稳定技巧：减去最大值
        z_stable = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z_stable)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X):
        """
        前向传播

        参数:
            X: (m, d) 输入特征矩阵
        返回:
            p: (m, K) 预测概率矩阵
        """
        # 线性变换
        z = X @ self.W + self.b  # (m, K)

        # Softmax激活
        p = self.softmax(z)

        return p

    def compute_loss(self, X, y):
        """
        计算交叉熵损失

        参数:
            X: (m, d) 输入特征矩阵
            y: (m,) 真实标签向量（类别索引）
        返回:
            loss: 标量损失值
        """
        m = X.shape[0]

        # 前向传播
        p = self.forward(X)

        # 计算交叉熵损失
        # p[range(m), y] 获取每个样本在真实类别上的预测概率
        log_probs = -np.log(p[range(m), y] + 1e-8)  # 加小值避免log(0)
        loss = np.mean(log_probs)

        return loss

    def predict(self, X):
        """
        预测类别

        参数:
            X: (m, d) 输入特征矩阵
        返回:
            predictions: (m,) 预测类别向量
        """
        p = self.forward(X)
        return np.argmax(p, axis=1)

    def train(self, X, y, learning_rate=0.01, epochs=100, batch_size=32, verbose=True):
        """
        训练模型

        参数:
            X: (m, d) 训练数据
            y: (m,) 训练标签
            learning_rate: 学习率
            epochs: 训练轮数
            batch_size: 批量大小
            verbose: 是否打印训练信息
        """
        m = X.shape[0]
        num_batches = m // batch_size

        for epoch in range(epochs):
            # 随机打乱数据
            indices = np.random.permutation(m)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            epoch_loss = 0

            for i in range(num_batches):
                # 获取当前批次
                start = i * batch_size
                end = start + batch_size
                X_batch = X_shuffled[start:end]
                y_batch = y_shuffled[start:end]

                # 前向传播
                p = self.forward(X_batch)

                # 计算损失
                batch_loss = -np.mean(np.log(p[range(batch_size), y_batch] + 1e-8))
                epoch_loss += batch_loss

                # 反向传播
                # 1. 梯度：dL/dz = p - y_one_hot
                y_one_hot = np.zeros_like(p)
                y_one_hot[range(batch_size), y_batch] = 1
                dz = p - y_one_hot  # (batch_size, K)

                # 2. 权重梯度
                dW = (1/batch_size) * (X_batch.T @ dz)  # (d, K)
                db = (1/batch_size) * np.sum(dz, axis=0)  # (K,)

                # 3. 更新参数
                self.W -= learning_rate * dW
                self.b -= learning_rate * db

            # 打印训练信息
            if verbose and (epoch + 1) % 10 == 0:
                avg_loss = epoch_loss / num_batches
                train_acc = self.evaluate(X, y)
                print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}, Accuracy: {train_acc:.4f}")

    def evaluate(self, X, y):
        """
        评估模型准确率

        参数:
            X: (m, d) 测试数据
            y: (m,) 测试标签
        返回:
            accuracy: 准确率
        """
        predictions = self.predict(X)
        accuracy = np.mean(predictions == y)
        return accuracy


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 1. 生成模拟数据
    np.random.seed(42)

    # 3个类别，每类100个样本
    num_samples = 300
    num_features = 2
    num_classes = 3
    
    
    # 生成聚类数据
    X = np.random.randn(num_samples, num_features) # 生成标准正态分布的随机数 ,作用 :
    y = np.zeros(num_samples, dtype=int)

    # 类别0: 中心在(-2, -2)
    X[0:100] += np.array([-2, -2])
    y[0:100] = 0

    # 类别1: 中心在(2, -2)
    X[100:200] += np.array([2, -2])
    y[100:200] = 1

    # 类别2: 中心在(0, 2)
    X[200:300] += np.array([0, 2])
    y[200:300] = 2

    # 2. 划分训练集和测试集
    train_size = int(0.8 * num_samples)
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    # 3. 创建和训练模型
    print("训练Softmax回归模型...")
    model = SoftmaxRegression(input_dim=num_features, num_classes=num_classes)

    model.train(
        X_train, y_train,
        learning_rate=0.1,
        epochs=100,
        batch_size=32,
        verbose=True
    )

    # 4. 评估模型
    train_acc = model.evaluate(X_train, y_train)
    test_acc = model.evaluate(X_test, y_test)

    print(f"\n最终结果:")
    print(f"训练集准确率: {train_acc:.4f}")
    print(f"测试集准确率: {test_acc:.4f}")

    # 5. 预测示例
    sample = np.array([[0, 0]])  # 原点附近
    probs = model.forward(sample)
    prediction = model.predict(sample)

    print(f"\n预测示例:")
    print(f"输入: {sample[0]}")
    print(f"预测概率: {probs[0]}")
    print(f"预测类别: {prediction[0]}")
```

---

# 第二部分：训练Softmax分类器

## 🎯 训练流程

### 完整的训练循环

```python
训练Softmax分类器的标准流程:

1. 数据准备
   ├─ 加载数据
   ├─ 归一化/标准化
   └─ 划分训练集/验证集/测试集

2. 模型初始化
   ├─ 初始化权重（Xavier/He）
   └─ 设置超参数

3. 训练循环
   for epoch in range(num_epochs):
       for batch in train_loader:
           # 前向传播
           logits = model(X_batch)
           probs = softmax(logits)

           # 计算损失
           loss = cross_entropy(probs, y_batch)

           # 反向传播
           gradients = backward(loss)

           # 更新参数
           optimizer.step(gradients)

       # 验证
       val_accuracy = evaluate(val_data)

4. 评估
   └─ 在测试集上评估最终性能
```

---

## 💡 训练技巧与最佳实践

### 1️⃣ 数据预处理

```python
# 特征归一化
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # 使用训练集的统计量

# 标签转换（如果需要）
# 确保标签是从0开始的整数: 0, 1, 2, ..., K-1
```

### 2️⃣ 权重初始化

```python
# Xavier初始化（适合Softmax）
W = np.random.randn(d, K) * np.sqrt(2.0 / (d + K))

# 或者更简单的版本
W = np.random.randn(d, K) * 0.01
b = np.zeros(K)
```

### 3️⃣ 学习率调整

```python
# 学习率衰减
learning_rate = initial_lr * (decay_rate ** (epoch / decay_steps))

# 或使用自适应优化器（Adam）
optimizer = Adam(learning_rate=0.001)
```

### 4️⃣ 正则化

```python
# L2正则化
loss = cross_entropy_loss + λ * ||W||²

# 实现
regularization_loss = 0.5 * lambda_reg * np.sum(W ** 2)
total_loss = cross_entropy_loss + regularization_loss
```

### 5️⃣ Early Stopping

```python
best_val_acc = 0
patience = 10
patience_counter = 0

for epoch in range(max_epochs):
    train(...)
    val_acc = evaluate(val_data)

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        save_model()
        patience_counter = 0
    else:
        patience_counter += 1

    if patience_counter >= patience:
        print("Early stopping!")
        break
```

---

## 🐛 常见问题与调试

### 问题1: 损失不下降

```python
可能原因:
1. 学习率太大 → 减小学习率（试试0.01、0.001）
2. 学习率太小 → 增大学习率
3. 数据未归一化 → 使用StandardScaler
4. 梯度计算错误 → 使用梯度检验

调试:
- 打印梯度范数: print(np.linalg.norm(dW))
- 检查损失曲线是否稳定下降
- 尝试更简单的数据集验证实现
```

### 问题2: 训练准确率高但测试准确率低

```python
过拟合!

解决方案:
1. 增加正则化强度
2. 使用Dropout
3. 增加训练数据
4. 减小模型容量
5. Early Stopping
```

### 问题3: 数值不稳定

```python
症状:
- 出现NaN或Inf
- 损失突然爆炸

解决:
1. 使用数值稳定的Softmax实现（减去max）
2. 梯度裁剪: grad = np.clip(grad, -5, 5)
3. 减小学习率
4. 检查输入数据是否有异常值
```

---

# 第三部分：深度学习框架

## 🚀 为什么使用深度学习框架？

### 手动实现 vs 深度学习框架

| 特性 | 手动实现 | 深度学习框架 |
|------|---------|-------------|
| **梯度计算** | 手动推导反向传播 | 自动微分 ✅ |
| **GPU加速** | 需要CUDA编程 | 内置支持 ✅ |
| **模型保存** | 自己序列化 | 一行代码 ✅ |
| **预训练模型** | 无 | 丰富的模型库 ✅ |
| **调试** | 困难 | 工具完善 ✅ |
| **社区支持** | 无 | 活跃社区 ✅ |

---

## 🔥 主流深度学习框架

### 1️⃣ PyTorch (⭐⭐⭐ 推荐！)

**优势**:
- ✅ 动态计算图（易于调试）
- ✅ Pythonic API（易于学习）
- ✅ 强大的社区支持
- ✅ DeepSeek-V3 使用的框架！

**安装**:
```bash
pip install torch torchvision
```

### 2️⃣ TensorFlow / Keras

**优势**:
- ✅ 成熟稳定
- ✅ 部署工具丰富
- ✅ Keras高层API简单

**安装**:
```bash
pip install tensorflow
```

### 3️⃣ JAX

**优势**:
- ✅ 函数式编程
- ✅ 高性能
- ✅ 灵活的自动微分

---

## 💻 PyTorch实现Softmax回归

### 完整代码示例

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# ==================== 定义模型 ====================

class SoftmaxClassifier(nn.Module):
    """PyTorch版Softmax分类器"""

    def __init__(self, input_dim, num_classes):
        super(SoftmaxClassifier, self).__init__()

        # 定义线性层
        self.linear = nn.Linear(input_dim, num_classes)

        # Softmax会在损失函数中计算，这里不需要显式定义

    def forward(self, x):
        """
        前向传播

        参数:
            x: (batch_size, input_dim)
        返回:
            logits: (batch_size, num_classes)
        """
        logits = self.linear(x)
        return logits


# ==================== 训练函数 ====================

def train_model(model, train_loader, val_loader, num_epochs=100, learning_rate=0.01):
    """
    训练模型

    参数:
        model: PyTorch模型
        train_loader: 训练数据加载器
        val_loader: 验证数据加载器
        num_epochs: 训练轮数
        learning_rate: 学习率
    """
    # 定义损失函数（包含Softmax）
    criterion = nn.CrossEntropyLoss()

    # 定义优化器
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # 训练循环
    for epoch in range(num_epochs):
        # ===== 训练阶段 =====
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0

        for X_batch, y_batch in train_loader:
            # 前向传播
            logits = model(X_batch)
            loss = criterion(logits, y_batch)

            # 反向传播
            optimizer.zero_grad()  # 清空梯度
            loss.backward()        # 计算梯度
            optimizer.step()       # 更新参数

            # 统计
            train_loss += loss.item()
            _, predicted = torch.max(logits, 1)
            train_total += y_batch.size(0)
            train_correct += (predicted == y_batch).sum().item()

        # ===== 验证阶段 =====
        model.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0

        with torch.no_grad():  # 不计算梯度
            for X_batch, y_batch in val_loader:
                logits = model(X_batch)
                loss = criterion(logits, y_batch)

                val_loss += loss.item()
                _, predicted = torch.max(logits, 1)
                val_total += y_batch.size(0)
                val_correct += (predicted == y_batch).sum().item()

        # 打印结果
        if (epoch + 1) % 10 == 0:
            train_acc = 100 * train_correct / train_total
            val_acc = 100 * val_correct / val_total
            print(f"Epoch [{epoch+1}/{num_epochs}]")
            print(f"  Train Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
            print(f"  Val Loss: {val_loss/len(val_loader):.4f}, Acc: {val_acc:.2f}%")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 1. 生成模拟数据
    np.random.seed(42)
    torch.manual_seed(42)

    num_samples = 1000
    input_dim = 20
    num_classes = 10

    # 生成随机数据
    X = np.random.randn(num_samples, input_dim).astype(np.float32)
    y = np.random.randint(0, num_classes, num_samples)

    # 2. 转换为PyTorch张量
    X_tensor = torch.from_numpy(X)
    y_tensor = torch.from_numpy(y).long()

    # 3. 创建数据加载器
    dataset = TensorDataset(X_tensor, y_tensor)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    # 4. 创建模型
    model = SoftmaxClassifier(input_dim=input_dim, num_classes=num_classes)
    print(model)
    print(f"模型参数数量: {sum(p.numel() for p in model.parameters())}")

    # 5. 训练模型
    print("\n开始训练...")
    train_model(
        model,
        train_loader,
        val_loader,
        num_epochs=100,
        learning_rate=0.01
    )

    # 6. 保存模型
    torch.save(model.state_dict(), 'softmax_classifier.pth')
    print("\n模型已保存到 softmax_classifier.pth")

    # 7. 加载模型（演示）
    loaded_model = SoftmaxClassifier(input_dim=input_dim, num_classes=num_classes)
    loaded_model.load_state_dict(torch.load('softmax_classifier.pth'))
    loaded_model.eval()
    print("模型加载成功!")
```

---

## 🎨 更高级的PyTorch示例：MNIST分类

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ==================== 定义模型 ====================

class MNISTClassifier(nn.Module):
    """MNIST手写数字分类器"""

    def __init__(self):
        super(MNISTClassifier, self).__init__()

        self.network = nn.Sequential(
            nn.Flatten(),                    # 28×28 → 784
            nn.Linear(784, 128),             # 隐藏层1
            nn.ReLU(),
            nn.Dropout(0.2),                 # Dropout正则化
            nn.Linear(128, 64),              # 隐藏层2
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 10)                # 输出层：10个类别
        )

    def forward(self, x):
        return self.network(x)


# ==================== 训练和评估 ====================

def train_mnist():
    # 1. 数据准备
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST的均值和标准差
    ])

    train_dataset = datasets.MNIST(
        root='./data',
        train=True,
        transform=transform,
        download=True
    )

    test_dataset = datasets.MNIST(
        root='./data',
        train=False,
        transform=transform,
        download=True
    )

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    # 2. 创建模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = MNISTClassifier().to(device)

    print(f"使用设备: {device}")
    print(f"训练集大小: {len(train_dataset)}")
    print(f"测试集大小: {len(test_dataset)}")

    # 3. 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 4. 训练循环
    num_epochs = 10

    for epoch in range(num_epochs):
        # 训练阶段
        model.train()
        train_loss = 0
        train_correct = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)

            # 前向传播
            output = model(data)
            loss = criterion(output, target)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 统计
            train_loss += loss.item()
            pred = output.argmax(dim=1)
            train_correct += pred.eq(target).sum().item()

        # 测试阶段
        model.eval()
        test_loss = 0
        test_correct = 0

        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                test_loss += criterion(output, target).item()
                pred = output.argmax(dim=1)
                test_correct += pred.eq(target).sum().item()

        # 打印结果
        train_acc = 100. * train_correct / len(train_dataset)
        test_acc = 100. * test_correct / len(test_dataset)

        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"  Train Loss: {train_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%")
        print(f"  Test Loss: {test_loss/len(test_loader):.4f}, Acc: {test_acc:.2f}%")

    return model


# 运行训练
if __name__ == "__main__":
    model = train_mnist()

    # 保存模型
    torch.save(model.state_dict(), 'mnist_classifier.pth')
    print("\nMNIST分类器训练完成!")
```

---

## 📊 深度学习框架对比

### PyTorch vs TensorFlow

```python
# ==================== PyTorch风格 ====================

# 定义模型
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

# 前向传播
output = model(input)

# 计算损失
loss = criterion(output, target)

# 反向传播
optimizer.zero_grad()
loss.backward()
optimizer.step()


# ==================== TensorFlow/Keras风格 ====================

# 定义模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10)
])

# 编译模型
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 训练模型
model.fit(X_train, y_train, epochs=10, batch_size=32)
```

---

## 🎯 深度学习框架的核心概念

### 1️⃣ 自动微分（Autograd）

```python
# PyTorch的自动微分
import torch

# 创建张量并启用梯度跟踪
x = torch.tensor([2.0], requires_grad=True)
w = torch.tensor([3.0], requires_grad=True)
b = torch.tensor([1.0], requires_grad=True)

# 前向传播
y = w * x + b
loss = y ** 2

# 反向传播（自动计算梯度）
loss.backward()

# 查看梯度
print(f"dL/dx = {x.grad}")  # 2 * (w*x + b) * w
print(f"dL/dw = {w.grad}")  # 2 * (w*x + b) * x
print(f"dL/db = {b.grad}")  # 2 * (w*x + b)
```

### 2️⃣ 计算图

```python
静态计算图 (TensorFlow 1.x):
  1. 定义图
  2. 编译图
  3. 运行图

动态计算图 (PyTorch, TensorFlow 2.x):
  1. 边执行边构建图
  2. 易于调试
  3. 支持动态控制流
```

### 3️⃣ GPU加速

```python
# 检查CUDA是否可用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"使用设备: {device}")

# 将模型和数据移到GPU
model = model.to(device)
X = X.to(device)
y = y.to(device)

# 训练（自动在GPU上运行）
output = model(X)
loss = criterion(output, y)
loss.backward()
optimizer.step()
```

---

## 🔧 常用深度学习工具

### 模型保存与加载

```python
# ==================== PyTorch ====================

# 保存模型参数（推荐）
torch.save(model.state_dict(), 'model.pth')

# 加载模型参数
model = MyModel()
model.load_state_dict(torch.load('model.pth'))
model.eval()

# 保存完整模型（不推荐，可移植性差）
torch.save(model, 'model_full.pth')
loaded_model = torch.load('model_full.pth')


# ==================== TensorFlow/Keras ====================

# 保存模型
model.save('model.h5')

# 加载模型
model = tf.keras.models.load_model('model.h5')
```

### TensorBoard可视化

```python
from torch.utils.tensorboard import SummaryWriter

# 创建writer
writer = SummaryWriter('runs/experiment_1')

# 记录损失
for epoch in range(num_epochs):
    # 训练...
    writer.add_scalar('Loss/train', train_loss, epoch)
    writer.add_scalar('Loss/val', val_loss, epoch)
    writer.add_scalar('Accuracy/train', train_acc, epoch)
    writer.add_scalar('Accuracy/val', val_acc, epoch)

writer.close()

# 启动TensorBoard
# tensorboard --logdir=runs
```

---

## 🎓 核心要点总结

### Softmax回归

```python
核心公式:
  pᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)

损失函数:
  L = -log(p_true_class)

梯度:
  ∂L/∂z = p - y  (非常优雅!)

应用:
  - 多分类任务
  - 神经网络的输出层
```

### 训练技巧

```
✓ 数据归一化
✓ Xavier初始化
✓ 使用Adam优化器
✓ 学习率衰减
✓ Early Stopping
✓ 正则化（L2、Dropout）
```

### 深度学习框架

```
PyTorch (推荐):
  ✓ 动态计算图
  ✓ Pythonic
  ✓ DeepSeek-V3使用

核心优势:
  ✓ 自动微分
  ✓ GPU加速
  ✓ 丰富的预训练模型
```

---

## 🔗 与DeepSeek-V3的关联

### DeepSeek-V3中的Softmax应用

```python
1. 输出层（Token预测）:
   logits = model(input_ids)  # (batch, seq_len, vocab_size)
   probs = softmax(logits)    # 每个位置的token概率分布
   next_token = argmax(probs[:, -1, :])

2. Attention权重:
   attention_scores = Q @ K.T / √d_k
   attention_weights = softmax(attention_scores)  # 注意力分布
   output = attention_weights @ V

3. 混合专家（MoE）:
   router_logits = router(x)
   expert_probs = softmax(router_logits)  # 专家选择概率
   selected_experts = topk(expert_probs, k=2)
```

### PyTorch在DeepSeek-V3中的角色

```python
DeepSeek-V3完全基于PyTorch构建:
  ├─ 模型定义: nn.Module
  ├─ 训练循环: 自定义优化器
  ├─ 分布式训练: torch.distributed
  ├─ 混合精度: torch.cuda.amp
  └─ 模型并行: torch.nn.parallel
```

---

## 📚 进阶资源

### 论文

1. **Softmax回归基础**
   - Pattern Recognition and Machine Learning (Bishop, 2006)
   - 第4.3节：多分类逻辑回归

2. **深度学习框架**
   - "Automatic differentiation in PyTorch" (Paszke et al., 2017)
   - PyTorch官方文档: https://pytorch.org/docs/

### 实践项目

```python
1. MNIST手写数字识别 ✅
   └─ 10分类问题，经典入门

2. CIFAR-10图像分类
   └─ 10类彩色图像，稍有挑战

3. 文本分类
   └─ 新闻分类、情感分析

4. 多标签分类
   └─ 使用Sigmoid而非Softmax
```

---

## 🚀 下一步学习

```
当前位置: Softmax回归与深度学习框架 ✅

已掌握:
  ✓ 多分类问题的数学基础
  ✓ Softmax回归的完整实现
  ✓ PyTorch深度学习框架
  ✓ 实际项目训练流程

下一步:
  → 卷积神经网络（CNN）
  → 或 Attention机制 ⭐⭐⭐（最重要！）
  → 或 序列模型（RNN/LSTM）
```

---

**更新日期**: 2025-10-30
**重要性**: 多分类任务的基础，深度学习实践的起点
**实践建议**: 先用NumPy实现理解原理，再用PyTorch实现实际项目
**关键技能**: Softmax数学、交叉熵损失、PyTorch使用

**记住**: Softmax回归是神经网络输出层的标准选择，理解它是深度学习的基础！🎯
