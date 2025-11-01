# 4_Self-Attention自注意力机制

## 🎯 学习目标

- 理解Self-Attention的核心思想和工作原理
- 掌握Query、Key、Value在Self-Attention中的具体含义
- 明白Self-Attention与传统Attention的区别
- 学会Self-Attention的数学计算过程
- 理解Self-Attention的并行计算优势

## 📚 问题引入

**为什么要学习Self-Attention？**

传统的Seq2Seq+Attention存在以下问题：
1. **串行计算**：RNN必须逐步处理，无法并行
2. **长距离依赖**：即使有注意力，RNN仍有梯度消失问题
3. **计算效率低**：无法充分利用GPU并行计算能力

**解决方案：完全去除RNN，只用Attention！**

---

## 🔄 Self-Attention vs 传统Attention

### **传统Attention（Cross-Attention）**

```
编码器输出: [a₁, a₂, a₃, ..., aₙ]
解码器状态: s

Query (Q) ← 解码器状态
Keys (K)  ← 编码器隐藏状态
Values (V) ← 编码器隐藏状态

特点：Query来自解码器，Key/Value来自编码器
```

### **Self-Attention（自注意力）**

```
输入序列: [x₁, x₂, x₃, ..., xₙ]

Query (Q) ← 输入序列本身
Keys (K)  ← 输入序列本身
Values (V) ← 输入序列本身

特点：Query、Key、Value都来自同一个输入序列
```

---

## 🎯 Self-Attention的核心思想

### 💡 **什么是Self-Attention？**

**自注意力 = "每个词都看向句子中的其他所有词"**

```
句子: "I love Beijing"
       ↓ Self-Attention

"I"看向"love"和"Beijing" → "I"的新表示
"love"看向"I"和"Beijing" → "love"的新表示
"Beijing"看向"I"和"love" → "Beijing"的新表示

每个词都通过关注其他词来更新自己的表示！
```

### 🔍 **直觉理解**

**类比：人类阅读理解**

```
阅读句子："The cat that sat on the mat was black"

当理解"The cat"时：
- "cat"需要关注"sat"来理解动作
- "cat"需要关注"was black"来理解状态
- "The"需要关注"cat"来理解关系

Self-Attention就是让模型模拟这种"全方位关注"！
```

---

## 🧮 Self-Attention的数学原理

### **整体公式**

```
Self-Attention(X) = softmax(XW_Q(XW_K)^T / √d_k) XW_V 

多头 : Attention(Q, K, V) = softmax(QK^T / √d_k) V

其中:
X: 输入序列 [seq_len, d_model]
W_Q, W_K, W_V: 可学习的投影矩阵
```

### **步骤分解**

给定输入序列 `X ∈ ℝ^{L×d}`，其中L是序列长度，d是模型维度：

#### **步骤1：创建Query、Key、Value**

```python
Q = X @ W_Q  # [L, d]
K = X @ W_K  # [L, d]
V = X @ W_V  # [L, d]

# 其中 W_Q, W_K, W_V ∈ ℝ^{d×d_k}
# 通常 d_k = d_model / num_heads (如果使用多头注意力)
```

#### **步骤2：计算注意力分数**

```python
# 计算所有位置对之间的相似度
scores = Q @ K^T  # [L, L]

# 缩放（防止梯度消失/爆炸）
scores = scores / math.sqrt(d_k)

# 缩放的原因：
# Q和K的期望方差是d_k
# 除以√d_k后，方差变为1，数值更稳定
```

#### **步骤3：应用掩码（可选）**

```python
# 在解码器中，需要遮盖未来位置
if mask is not None:
    scores = scores.masked_fill(mask == 0, -1e9)
```

#### **步骤4：Softmax归一化**

```python
attention_weights = F.softmax(scores, dim=-1)  # [L, L]
# 每一行的权重和为1.0
```

#### **步骤5：加权求和得到输出**

```python
output = attention_weights @ V  # [L, L] @ [L, d] = [L, d]
```

---

## 📊 完整的Self-Attention示例

### **示例：计算"Self-Attention"的注意力权重**

#### **输入信息**
```python
输入序列: ["Self", "-", "Attention"]
序列长度: L = 3
模型维度: d = 4

X = [
    [0.1, 0.2, 0.3, 0.4],  # "Self"
    [0.5, 0.6, 0.7, 0.8],  # "-"
    [0.9, 1.0, 1.1, 1.2]   # "Attention"
]
```

#### **投影矩阵（简化示例）**
```python
# 假设我们学习到的投影矩阵
W_Q = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]
]

W_K = W_Q  # 简化：W_K = W_Q
W_V = W_Q  # 简化：W_V = W_Q

# 注意：实际中W_Q, W_K, W_V是不同的！
```

#### **步骤1：计算Q、K、V**
```python
# Q = X @ W_Q
Q = [
    [0.1, 0.2, 0.3, 0.4],  # "Self"
    [0.5, 0.6, 0.7, 0.8],  # "-"
    [0.9, 1.0, 1.1, 1.2]   # "Attention"
]

K = Q  # 简化：K = Q
V = Q  # 简化：V = Q
```

#### **步骤2：计算注意力分数**
```python
# scores = Q @ K^T
# 注意：这里用的是实际值，不是简化的Q=K=V

import numpy as np

X = np.array([
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
    [0.9, 1.0, 1.1, 1.2]
])

# 随机投影矩阵（实际中从训练得到）
W_Q = np.random.randn(4, 4) * 0.1
W_K = np.random.randn(4, 4) * 0.1
W_V = np.random.randn(4, 4) * 0.1

Q = X @ W_Q
K = X @ W_K
V = X @ W_V

# 计算分数矩阵
scores = Q @ K.T  # [3, 3]
scores_scaled = scores / math.sqrt(4)  # 除以√d_k

print("Q:")
print(Q)
print("\nK:")
print(K)
print("\nScores:")
print(scores_scaled)
```

#### **步骤3：Softmax归一化**
```python
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

attention_weights = softmax(scores_scaled)
print("\nAttention Weights:")
print(attention_weights)

# 验证：每行和为1
print("\nRow sums (should be 1.0):")
print(np.sum(attention_weights, axis=1))
```

#### **步骤4：计算输出**
```python
output = attention_weights @ V
print("\nOutput:")
print(output)

# 验证：输出维度与输入相同
print(f"\nInput shape: {X.shape}")
print(f"Output shape: {output.shape}")
```

---

## 🎨 Self-Attention的可视化

### **注意力权重热力图**

```
输入序列: "The cat sat on the mat"
注意力权重矩阵 (5×5):

            The   cat   sat   on   mat
    The     0.30  0.25  0.10  0.15  0.20
    cat     0.20  0.35  0.25  0.10  0.10
    sat     0.15  0.30  0.35  0.15  0.05
    on      0.10  0.15  0.20  0.40  0.15
    mat     0.25  0.20  0.10  0.25  0.20

解读：
- "The"关注自己(0.30)和"cat"(0.25)最多
- "cat"关注自己(0.35)和"sat"(0.25)，因为动作与猫相关
- "sat"关注自己(0.35)和"cat"(0.30)，因为主谓关系
- "on"关注自己(0.40)和"mat"(0.25)，因为介词关系
- "mat"关注"on"(0.25)和"The"(0.25)，因为修饰关系
```

### **不同类型的Self-Attention**

#### **1. 句子级别的Self-Attention**
```
"I love Beijing" → 每个词都关注其他所有词
```

#### **2. 图像块的Self-Attention**
```
图像分割为 patches → 每个patch都关注其他所有patches
```

#### **3. 音频片段的Self-Attention**
```
音频分割为 frames → 每个frame都关注其他所有frames
```

---

## 🔍 Self-Attention的关键特性

### **1. 全局感受野**

```
RNN的感受野：
位置1: ← 只看位置1
位置2: ← 看位置1,2
位置3: ← 看位置1,2,3
...
位置N: ← 看位置1,2,3,...,N-1,N

Self-Attention的感受野：
位置1: ← 看位置1,2,3,...,N (所有位置!)
位置2: ← 看位置1,2,3,...,N (所有位置!)
位置3: ← 看位置1,2,3,...,N (所有位置!)
...
位置N: ← 看位置1,2,3,...,N (所有位置!)

优势：每个位置都可以直接看到所有其他位置！
```

### **2. 并行计算**

```
RNN的序列依赖：
t=1 → t=2 → t=3 → ... → t=N (必须串行)

Self-Attention的并行性：
所有位置同时计算注意力权重！
时间复杂度：O(N²)，但可以完全并行

优势：充分利用GPU并行计算能力！
```

### **3. 位置无关性**

```
问题：Self-Attention没有内置的位置信息
输入："I love Beijing" 和 "Beijing love I"
Q、K、V相同 → 注意力权重相同 → 输出相同！

解决：需要额外添加位置编码 (Position Encoding)
```

### **4. 线性复杂度（某些变体）**

```
标准Self-Attention：O(N²)
线性注意力 (Linear Attention)：O(N)
稀疏注意力 (Sparse Attention)：O(N√N)
```

---

## 💻 Self-Attention的完整实现

### **基础Self-Attention实现**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class SelfAttention(nn.Module):
    """基础的Self-Attention实现"""

    def __init__(self, d_model, n_heads=1):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        assert d_model % n_heads == 0, "d_model必须能被n_heads整除"

        # Query, Key, Value投影矩阵
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)

        # 输出投影矩阵
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.size()

        # 步骤1: 计算Q, K, V
        Q = self.W_q(x)  # [batch, seq_len, d_model]
        K = self.W_k(x)
        V = self.W_v(x)

        # 步骤2: 重排为多头形式
        Q = Q.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)

        # 步骤3: 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        # scores: [batch, n_heads, seq_len, seq_len]

        # 步骤4: 应用掩码
        if mask is not None:
            # mask: [batch, seq_len] 或 [batch, 1, seq_len]
            mask = mask.unsqueeze(1).unsqueeze(1)  # [batch, 1, 1, seq_len]
            scores = scores.masked_fill(mask == 0, -1e9)

        # 步骤5: Softmax归一化
        attention_weights = F.softmax(scores, dim=-1)  # [batch, n_heads, seq_len, seq_len]

        # 步骤6: 加权求和
        context = torch.matmul(attention_weights, V)  # [batch, n_heads, seq_len, d_k]

        # 步骤7: 合并多头
        context = context.transpose(1, 2).contiguous().view(
            batch_size, seq_len, d_model
        )  # [batch, seq_len, d_model]

        # 步骤8: 输出投影
        output = self.W_o(context)

        return output, attention_weights

# 使用示例
if __name__ == "__main__":
    # 模拟输入
    batch_size = 2
    seq_len = 5
    d_model = 8

    x = torch.randn(batch_size, seq_len, d_model)
    print(f"Input shape: {x.shape}")

    # 创建模型
    self_attn = SelfAttention(d_model=8, n_heads=2)

    # 前向传播
    output, attn_weights = self_attn(x)
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attn_weights.shape}")

    # 验证：注意力权重的性质
    print(f"\nAttention weights sum (should be 1.0):")
    print(f"Head 0: {attn_weights[0, 0].sum(dim=-1)}")
    print(f"Head 1: {attn_weights[0, 1].sum(dim=-1)}")
```

### **简化的单头Self-Attention**

```python
class SimpleSelfAttention(nn.Module):
    """简化的单头Self-Attention，便于理解"""

    def __init__(self, d_model):
        super().__init__()
        self.d_model = d_model

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.size()

        # 计算Q, K, V
        Q = self.W_q(x)  # [batch, seq_len, d_model]
        K = self.W_k(x)
        V = self.W_v(x)

        # 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_model)

        # Softmax
        attention_weights = F.softmax(scores, dim=-1)

        # 加权求和
        output = torch.matmul(attention_weights, V)

        return output, attention_weights

# 使用示例
simple_attn = SimpleSelfAttention(d_model=8)
output, weights = simple_attn(x)
print(f"Simplified output shape: {output.shape}")
```

---

## 🔄 Self-Attention vs RNN/LSTM

### **计算复杂度对比**

| 架构 | 时间复杂度 | 空间复杂度 | 并行性 | 长距离依赖 |
|------|-----------|-----------|--------|-----------|
| **RNN** | O(L) | O(1) | 差 | 差（梯度消失） |
| **LSTM/GRU** | O(L) | O(1) | 差 | 一般（改善但有限） |
| **Self-Attention** | O(L²) | O(L²) | 优秀 | 优秀（直接连接） |

### **信息流动对比**

#### **RNN的信息流动**
```
位置1 → 位置2 → 位置3 → 位置4 → 位置5
  ↑       ↑       ↑       ↑       ↑
  ──→ 传递信息（可能丢失） ←──
```

#### **Self-Attention的信息流动**
```
位置1 ↔ 位置2 ↔ 位置3 ↔ 位置4 ↔ 位置5
  ↑     ↑     ↑     ↑     ↑
  全连接：每个位置都可以直接与其他所有位置通信！
```

### **性能对比（以机器翻译为例）**

```
BLEU分数对比：

RNN:     24.5
LSTM:    28.3
Seq2Seq+Attention:  29.8
Transformer (Self-Attention):  32.4

训练速度对比：

RNN:     100小时
LSTM:    120小时
Seq2Seq+Attention:  150小时
Transformer (Self-Attention):  20小时  ← 并行化带来巨大提升！
```

---

## 🎯 Self-Attention的实际应用

### **1. 机器翻译**

```python
# Transformer在翻译中的应用
input_sentence = "I love natural language processing"
output_sentence = "我喜欢自然语言处理"

# Self-Attention让模型能够：
# - "I"关注"love"和"processing"
# - "love"关注"I"和"processing"
# - 每个词都能根据需要关注句子中的任意位置
```

### **2. 文本摘要**

```python
# 长文档摘要
input_text = "一篇关于深度学习的10000字论文"
output_summary = "深度学习是机器学习的一个分支..."

# Self-Attention让模型能够：
# - 关注文档中的关键信息
# - 建立跨段落的依赖关系
# - 生成连贯的摘要
```

### **3. 问答系统**

```python
# 问答
context = "北京是中国的首都"
question = "中国的首都是什么？"

# Self-Attention让模型能够：
# - 问题中的"首都"关注上下文中的"北京"
# - 问题中的"中国"关注上下文中的"中国"
# - 建立问题和上下文之间的精确对齐
```

---

## 🚀 Self-Attention的改进和变体

### **1. 稀疏注意力 (Sparse Attention)**

```python
# 标准注意力：每个位置关注所有位置
attention_mask = torch.ones(L, L)

# 局部注意力：每个位置只关注局部窗口
window_size = 5
attention_mask = torch.zeros(L, L)
for i in range(L):
    start = max(0, i - window_size//2)
    end = min(L, i + window_size//2 + 1)
    attention_mask[i, start:end] = 1

# 稀疏注意力：基于内容的稀疏连接
def sparse_attention(Q, K, V, k=20):
    # 只保留每个query的top-k个最相似的key
    scores = Q @ K.transpose(-2, -1)
    top_k_scores, top_k_indices = torch.topk(scores, k, dim=-1)

    # 创建稀疏掩码
    sparse_mask = torch.zeros_like(scores)
    sparse_mask.scatter_(-1, top_k_indices, 1)

    # 应用掩码
    scores = scores.masked_fill(sparse_mask == 0, -1e9)

    # Softmax和加权求和
    weights = F.softmax(scores, dim=-1)
    output = weights @ V

    return output
```

### **2. 线性注意力 (Linear Attention)**

```python
# 核技巧避免O(N²)计算
def linear_attention(Q, K, V):
    """
    利用核技巧：exp(QK^T) ≈ φ(Q)φ(K)^T
    将O(N²)转换为O(N)
    """
    # 简单的线性注意力（实际中需要更复杂的核函数）
    phi_Q = F.relu(Q)
    phi_K = F.relu(K)

    # 计算
    KV = torch.sum(phi_K.unsqueeze(0) * V.unsqueeze(1), dim=-2)
    QK = torch.sum(phi_Q, dim=-1, keepdim=True)

    output = KV / QK
    return output
```

### **3. 可学习注意力 (Learnable Attention)**

```python
class LearnableAttention(nn.Module):
    """注意力权重可以通过学习得到"""

    def __init__(self, d_model, n_heads=1):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)

        # 可学习的注意力图
        self.attention_map = nn.Parameter(torch.randn(n_heads, seq_len, seq_len))

    def forward(self, x):
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        # 计算分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # 结合可学习注意力图
        scores = scores + self.attention_map.unsqueeze(0)

        # Softmax
        weights = F.softmax(scores, dim=-1)

        # 加权求和
        output = torch.matmul(weights, V)

        return output
```

---

## 💡 关键要点总结

### **Self-Attention的本质**

1. **Query、Key、Value来自同一个输入**
   - Q = XW_Q
   - K = XW_K
   - V = XW_V

2. **注意力分数 = Query与所有Key的相似度**
   - scores = QK^T / √d_k

3. **注意力权重 = 归一化的分数**
   - α = softmax(scores)

4. **输出 = 注意力权重的加权组合**
   - output = αV

### **核心优势**

1. ✅ **全局感受野**：每个位置都能看到所有位置
2. ✅ **并行计算**：充分利用GPU并行能力
3. ✅ **长距离依赖**：直接连接，无梯度消失
4. ✅ **灵活性**：可以学习不同类型的注意力模式

### **需要解决**

1. ⚠️ **位置信息**：需要额外添加位置编码
2. ⚠️ **计算复杂度**：O(N²)，对长序列是挑战
3. ⚠️ **内存消耗**：需要存储N×N的注意力矩阵

---

## 🎓 下一步学习

**现在您完全理解了Self-Attention，接下来可以学习：**

1. **Multi-Head Attention** - 并行计算多个注意力
2. **Transformer架构** - 完整的编码器-解码器结构
3. **位置编码 (Position Encoding)** - 解决位置信息问题
4. **在DeepSeek-V3中的应用** - Multi-Head Latent Attention

**选择您想继续学习的主题！** 🤔
