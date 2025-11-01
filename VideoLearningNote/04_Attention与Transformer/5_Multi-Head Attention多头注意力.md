# 5_Multi-Head Attention多头注意力

## 🎯 学习目标

- 理解Multi-Head Attention的核心思想和设计动机
- 掌握多头注意力的数学计算过程
- 明白不同头关注的不同类型信息
- 学会Multi-Head Attention的实现细节
- 理解多头注意力与单头注意力的区别

## 📚 问题引入

**为什么需要Multi-Head？**

虽然Self-Attention可以建立全局依赖关系，但存在以下问题：

1. **信息捕获单一**：单头注意力只能用一种方式关注其他位置
2. **语义表示有限**：无法同时捕获不同类型的依赖关系
3. **表示能力不足**：单个表示空间限制了模型的表达能力

**解决方案：并行计算多个注意力头！**

---

## 🎭 Multi-Head Attention的核心思想

### 💡 **什么是Multi-Head Attention？**

**多头注意力 = "从多个角度同时关注"**

```
文本: "I love Beijing"

单头注意力：只能理解一种关系
- 只能关注语法关系 OR 语义关系 OR 位置关系

多头注意力：可以从多个角度理解
- 头1：关注语法关系（主谓宾）
- 头2：关注语义关系（主题-属性）
- 头3：关注位置关系（远距离依赖）
- 头4：关注情感关系（积极/消极）
```

### 🔍 **直观理解**

#### **类比1：人类注意力**

```
阅读句子时，大脑会同时关注多个方面：

句子："The cat that I saw yesterday was sleeping"

头1（语法关注）：
- "cat" ← → "was" (主谓关系)
- "that" ← → "cat" (修饰关系)

头2（语义关注）：
- "cat" ← → "sleeping" (猫的状态)
- "yesterday" ← → "saw" (时间关系)

头3（位置关注）：
- "I" ← → "saw" (近邻关系)
- "cat" ← → "was" (远距离但相关)

头4（结构关注）：
- "The" ← → "cat" (定冠词修饰)
- "that I saw" ← → "cat" (从句关系)
```

#### **类比2：多角度分析**

```
分析同一个问题：为什么"猫"能理解主人？

角度1（生物角度）：猫的认知能力、记忆力
角度2（情感角度）：猫与主人的情感纽带
角度3（行为角度）：猫的行为模式、反应
角度4（认知角度）：动物的认知科学

综合所有角度 → 全面理解问题
```

---

## 🧮 Multi-Head Attention的数学原理

### **整体公式**

```
MultiHead(Q, K, V) = Concat(head_1, head_2, ..., head_h) W^O

其中 head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

而 Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

### **步骤分解**

给定输入 `X ∈ ℝ^{L×d_model}`：

#### **步骤1：线性投影为多个头**

```python
# 每个头都有独立的投影矩阵
for i in range(h):  # h是头的数量
    Q_i = X @ W_Q^i    # [L, d_model] @ [d_model, d_k] = [L, d_k]
    K_i = X @ W_K^i
    V_i = X @ W_V^i
```

#### **步骤2：并行计算每个头的注意力**

```python
# 对每个头独立计算注意力
for i in range(h):
    scores_i = Q_i @ K_i^T / √d_k
    weights_i = softmax(scores_i)
    head_i = weights_i @ V_i
```

#### **步骤3：拼接所有头的输出**

```python
# 将所有头的输出拼接
concat_output = Concat(head_1, head_2, ..., head_h)  # [L, h*d_k]
```

#### **步骤4：最终线性投影**

```python
# 投影回原始维度
output = concat_output @ W_O  # [L, h*d_k] @ [h*d_k, d_model] = [L, d_model]
```

---

## 📊 完整的Multi-Head Attention示例

### **示例：双头注意力**

#### **输入信息**
```python
输入序列: ["I", "love", "Beijing"]
序列长度: L = 3
模型维度: d_model = 8
头数量: h = 2
每个头的维度: d_k = d_model / h = 4

X = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],  # "I"
    [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],  # "love"
    [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]   # "Beijing"
]
```

#### **投影矩阵**
```python
# 头1的投影矩阵
W_Q1 = torch.randn(8, 4) * 0.1
W_K1 = torch.randn(8, 4) * 0.1
W_V1 = torch.randn(8, 4) * 0.1

# 头2的投影矩阵
W_Q2 = torch.randn(8, 4) * 0.1
W_K2 = torch.randn(8, 4) * 0.1
W_V2 = torch.randn(8, 4) * 0.1

# 输出投影矩阵
W_O = torch.randn(8, 8) * 0.1
```

#### **步骤1：计算每个头的Q、K、V**
```python
# 头1
Q1 = X @ W_Q1  # [3, 8] @ [8, 4] = [3, 4]
K1 = X @ W_K1
V1 = X @ W_V1

# 头2
Q2 = X @ W_Q2  # [3, 4]
K2 = X @ W_K2
V2 = X @ W_V2
```

#### **步骤2：计算每个头的注意力**
```python
# 头1的注意力
scores1 = Q1 @ K1.T / math.sqrt(4)  # [3, 3]
weights1 = F.softmax(scores1, dim=-1)
head1 = weights1 @ V1  # [3, 4]

# 头2的注意力
scores2 = Q2 @ K2.T / math.sqrt(4)  # [3, 3]
weights2 = F.softmax(scores2, dim=-1)
head2 = weights2 @ V2  # [3, 4]
```

#### **步骤3：拼接和投影**
```python
# 拼接两个头
concat = torch.cat([head1, head2], dim=-1)  # [3, 8]

# 最终投影
output = concat @ W_O  # [3, 8]
```

---

## 🎨 不同头关注的信息类型

### **示例：8头注意力分析**

```
输入句子: "The quick brown fox jumps over the lazy dog"

每个头关注的模式：

头1 (语法关注):
  "The"     → 关注 "fox" (限定词)
  "quick"   → 关注 "fox" (形容词)
  "brown"   → 关注 "fox" (形容词)
  "fox"     → 关注 "jumps" (动词)
  "jumps"   → 关注 "fox" (主语)
  "over"    → 关注 "dog" (介词宾语)
  "the"     → 关注 "dog" (限定词)
  "lazy"    → 关注 "dog" (形容词)

头2 (语义关注):
  "quick"   → 与 "fox" 的动态特性相关
  "brown"   → 与 "fox" 的外观特征相关
  "jumps"   → 与 "fox" 的行为特征相关
  "lazy"    → 与 "dog" 的状态特征相关

头3 (位置关注):
  相邻词汇之间有更强的注意力权重
  "quick" ↔ "brown", "brown" ↔ "fox"

头4 (句法关注):
  关注完整的主谓宾结构
  "fox" (主语) ↔ "jumps" (谓语)

头5 (依存语法关注):
  关注依赖关系
  "fox" ← 依赖 "The"
  "jumps" ← 依赖 "fox"

头6 (语义角色关注):
  关注语义角色
  "fox": 执行者 (Agent)
  "jumps": 动作 (Action)
  "over": 方向 (Direction)

头7 (长距离依赖关注):
  关注跨越多个词的依赖
  "The" → ... → "fox"
  "the" → ... → "dog"

头8 (修辞关注):
  关注修辞结构
  "quick" vs "lazy" (对比)
```

### **注意力权重可视化**

```
输入: "I love Beijing"

头1 (语法头):
          I    love  Beijing
    I    0.3   0.6   0.1    ← 主谓关系
    love 0.4   0.3   0.3
    Beijing 0.2  0.2  0.6

头2 (语义头):
          I    love  Beijing
    I    0.2   0.7   0.1    ← 情感关系
    love 0.3   0.2   0.5
    Beijing 0.1  0.4  0.5

头3 (位置头):
          I    love  Beijing
    I    0.5   0.3   0.2    ← 近邻关系
    love 0.3   0.4   0.3
    Beijing 0.2  0.3  0.5

组合结果：
每个位置的综合表示 = 0.33×head1 + 0.33×head2 + 0.33×head3
```

---

## 💻 Multi-Head Attention的完整实现

### **标准Multi-Head Attention实现**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    """标准Multi-Head Attention实现"""

    def __init__(self, d_model, n_heads=8):
        super().__init__()
        assert d_model % n_heads == 0, "d_model必须能被n_heads整除"

        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # 投影矩阵：每个头都有独立的参数
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.size()

        # ======== 步骤1: 线性投影 ========
        Q = self.W_q(x)  # [batch, seq_len, d_model]
        K = self.W_k(x)
        V = self.W_v(x)

        # ======== 步骤2: 重排为多头形式 ========
        Q = Q.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)

        # Q, K, V形状: [batch, n_heads, seq_len, d_k]

        # ======== 步骤3: 应用遮蔽（解码器用） ========
        if mask is not None:
            # mask: [batch, seq_len] 或 [batch, 1, seq_len]
            mask = mask.unsqueeze(1).unsqueeze(1)  # [batch, 1, 1, seq_len]
            Q = Q.masked_fill(mask == 0, 0)
            K = K.masked_fill(mask == 0, 0)
            V = V.masked_fill(mask == 0, 0)

        # ======== 步骤4: 计算注意力分数 ========
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        # scores: [batch, n_heads, seq_len, seq_len]

        # ======== 步骤5: Softmax归一化 ========
        attention_weights = F.softmax(scores, dim=-1)  # [batch, n_heads, seq_len, seq_len]

        # ======== 步骤6: 加权求和得到上下文 ========
        context = torch.matmul(attention_weights, V)  # [batch, n_heads, seq_len, d_k]

        # ======== 步骤7: 合并多头 ========
        context = context.transpose(1, 2).contiguous().view(
            batch_size, seq_len, d_model
        )  # [batch, seq_len, d_model]

        # ======== 步骤8: 输出投影 ========
        output = self.W_o(context)

        return output, attention_weights

# ======== 使用示例 ========
if __name__ == "__main__":
    # 模拟输入
    batch_size = 2
    seq_len = 10
    d_model = 512
    n_heads = 8

    x = torch.randn(batch_size, seq_len, d_model)
    print(f"Input shape: {x.shape}")

    # 创建模型
    mha = MultiHeadAttention(d_model=512, n_heads=8)

    # 前向传播
    output, attn_weights = mha(x)
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attn_weights.shape}")

    # 验证多头的作用
    print(f"\n多头的意义:")
    print(f"头数量: {mha.n_heads}")
    print(f"每个头的维度: {mha.d_k}")
    print(f"总维度保持不变: {d_model}")
```

### **可视化不同头的注意力**

```python
def visualize_multi_head_attention(attn_weights, words, n_heads=8):
    """
    可视化多头注意力的注意力权重

    参数:
        attn_weights: [batch, n_heads, seq_len, seq_len]
        words: 词汇列表
        n_heads: 头的数量
    """
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()

    batch_idx = 0  # 取第一个样本

    for head in range(n_heads):
        ax = axes[head]
        attention_matrix = attn_weights[batch_idx, head].cpu().numpy()

        # 绘制热力图
        im = ax.imshow(attention_matrix, cmap='Blues', aspect='auto')

        # 设置标签
        ax.set_xticks(range(len(words)))
        ax.set_yticks(range(len(words)))
        ax.set_xticklabels(words)
        ax.set_yticklabels(words)

        # 设置标题
        ax.set_title(f'Head {head+1}', fontsize=12)

        # 添加数值标签
        for i in range(len(words)):
            for j in range(len(words)):
                text = ax.text(j, i, f'{attention_matrix[i, j]:.2f}',
                             ha="center", va="center", color="black", fontsize=8)

    plt.tight_layout()
    plt.suptitle('Multi-Head Attention Visualization', fontsize=16)
    plt.show()

# 使用示例
words = ["I", "love", "Beijing"]
output, attn_weights = mha(x)
# visualize_multi_head_attention(attn_weights, words)
```

### **简化版多头注意力**

```python
class SimpleMultiHeadAttention(nn.Module):
    """简化的多头注意力，便于理解"""

    def __init__(self, d_model, n_heads=4):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        # 所有头的投影矩阵堆叠在一起
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.size()

        # 投影
        Q = self.W_q(x)  # [batch, seq_len, d_model]
        K = self.W_k(x)
        V = self.W_v(x)

        # 重排为多头
        Q = Q.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)

        # 计算注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        weights = F.softmax(scores, dim=-1)
        context = torch.matmul(weights, V)

        # 合并多头
        context = context.transpose(1, 2).contiguous().view(
            batch_size, seq_len, d_model
        )

        # 输出投影
        output = self.W_o(context)

        return output, weights

# 测试简化版
simple_mha = SimpleMultiHeadAttention(d_model=64, n_heads=4)
simple_output, simple_weights = simple_mha(x)
print(f"Simplified Multi-Head Attention output shape: {simple_output.shape}")
```

---

## 🔍 Multi-Head vs Single-Head

### **表达能力对比**

| 特性 | 单头注意力 | 多头注意力 |
|------|-----------|-----------|
| **捕获关系类型** | 一种固定模式 | 多种并行模式 |
| **表示空间** | 单一空间 | 多个子空间组合 |
| **计算复杂度** | O(d) | O(h×d) |
| **并行性** | 一般 | 优秀（h个独立计算） |
| **学习能力** | 有限 | 强大（多角度学习） |

### **性能对比**

```
BLEU分数对比：
单头注意力:  28.5
双头注意力:  29.8
4头注意力:  31.2
8头注意力:  32.4
16头注意力: 32.1  ← 边际递减

最优配置：
大多数任务：8头注意力
大模型：16-64头注意力
```

### **注意力质量分析**

#### **单头注意力的局限**
```python
# 假设我们有句子："The cat sat on the mat"

单头注意力只能学到一种模式：
可能是语法模式 or 语义模式 or 位置模式
但无法同时学到多种模式！
```

#### **多头注意力的优势**
```python
# 同一句话："The cat sat on the mat"

头1：语法关系 (主谓宾)
- "cat" ↔ "sat" (主谓关系)
- "The" ↔ "cat" (修饰关系)

头2：语义关系 (属性-主体)
- "cat" ↔ "sat" (主体-动作)
- "mat" ↔ "on" (介词关系)

头3：位置关系 (远近距离)
- "The" ↔ "cat" (近邻)
- "sat" ↔ "mat" (近邻)
- "The" ↔ "mat" (远距离)

头4：句法结构 (短语组合)
- "The cat" ↔ "sat on the mat"
- "on the mat" ↔ "sat"
```

---

## 🎯 Multi-Head的优化技巧

### **1. 头的数量选择**

```python
# 经验法则
def get_num_heads(d_model):
    if d_model <= 256:
        return 4
    elif d_model <= 512:
        return 8
    elif d_model <= 1024:
        return 16
    else:
        return 32

# 例如：
# BERT Base: d_model=768, n_heads=12
# BERT Large: d_model=1024, n_heads=16
# GPT-3: d_model=12288, n_heads=96
```

### **2. 头的维度设计**

```python
# 标准设计
d_model = 512
n_heads = 8
d_k = d_v = d_model // n_heads = 64

# 这样设计的好处：
# 1. 总计算量与单头类似
# 2. 每个头有足够的维度表示信息
# 3. 内存使用合理
```

### **3. 残差连接**

```python
class MultiHeadAttentionWithResidual(nn.Module):
    """带残差连接的多头注意力"""

    def __init__(self, d_model, n_heads):
        super().__init__()
        self.mha = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        # 残差连接
        attn_output, attn_weights = self.mha(x)
        x = self.norm1(x + attn_output)
        return x, attn_weights

# 残差连接的作用：
# 1. 缓解梯度消失
# 2. 保持原始信息
# 3. 加速收敛
```

### **4. Dropout正则化**

```python
class MultiHeadAttentionWithDropout(nn.Module):
    """带Dropout的多头注意力"""

    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        self.mha = MultiHeadAttention(d_model, n_heads)
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        attn_output, attn_weights = self.mha(x, mask)

        # 应用Dropout
        attn_output = self.dropout(attn_output)

        # 残差连接和LayerNorm
        x = self.norm(x + attn_output)

        return x, attn_weights

# Dropout的作用：
# 1. 防止过拟合
# 2. 增强泛化能力
# 3. 提高模型鲁棒性
```

---

## 🔄 多头注意力的实际应用

### **1. 机器翻译**

```python
# 翻译任务中的多头注意力
input_en = ["I", "love", "natural", "language", "processing"]
output_zh = ["我", "喜欢", "自然语言", "处理"]

头1：语法关注
- "I" ↔ "love" (主谓关系)
- "language" ↔ "processing" (名词修饰)

头2：语义关注
- "natural" ↔ "language" (形容词-名词)
- "love" ↔ "我" (情感对应)

头3：位置关注
- 相邻词汇有更强的连接

头4：结构关注
- 完整短语 "natural language" ↔ "自然语言"
- "processing" ↔ "处理"
```

### **2. 文本摘要**

```python
# 长文档摘要
document = "一篇关于深度学习的论文..."
summary = "深度学习是机器学习的重要分支..."

头1：关键词提取
头2：主题识别
头3：逻辑关系
头4：摘要结构
```

### **3. 问答系统**

```python
# 问答任务
context = "北京是中国的首都"
question = "中国的首都是哪里？"

头1：实体识别
- "北京" ← → "首都"
- "中国" ← → "首都"

头2：关系识别
- "中国" ↔ "北京" (首都关系)

头3：问题意图
- "哪里" ← → "首都"
```

---

## 💡 关键要点总结

### **Multi-Head Attention的本质**

1. **并行学习多个视角**
   - 每个头负责学习不同类型的依赖关系
   - 多个头可以同时关注不同的信息

2. **线性变换+拼接**
   - 每个头有独立的投影矩阵
   - 最终输出是所有头的拼接

3. **保持维度不变**
   - 输入维度 = 输出维度 = d_model
   - 虽然计算了h个注意力，但维度保持一致

### **核心优势**

1. ✅ **多角度捕获信息**
   - 语法、语义、位置、结构等多种关系
   - 更全面的表示能力

2. ✅ **并行计算高效**
   - 多个头可以并行计算
   - 充分利用GPU资源

3. ✅ **增强表示能力**
   - 多个子空间的组合
   - 更丰富的特征表达

4. ✅ **训练稳定性更好**
   - 多头提供冗余表示
   - 单头失效不影响整体

### **设计原则**

1. **头的数量与维度平衡**
   - 通常 d_k = d_model / n_heads
   - 确保计算资源合理分配

2. **残差连接的重要性**
   - 保持梯度流动
   - 加速模型收敛

3. **Dropout正则化**
   - 防止过拟合
   - 提高泛化能力

---

## 🎓 下一步学习

**现在您完全理解了Multi-Head Attention，接下来可以学习：**

1. **Transformer整体架构** - 编码器-解码器结构
2. **位置编码** - 解决位置信息问题
3. **前馈神经网络** - Transformer中的Feed-Forward层
4. **在DeepSeek-V3中的应用** - Multi-Head Latent Attention

**选择您想继续学习的主题！** 🤔


