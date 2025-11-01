# 6_Transformer网络原理

## 🎯 学习目标

- 理解Transformer的整体架构和设计思想
- 掌握Encoder-Decoder结构的具体实现
- 理解前馈神经网络(FFN)的作用
- 掌握位置编码(Position Encoding)的原理
- 明白LayerNorm vs BatchNorm的区别
- 学会完整的Transformer计算流程

## 📚 问题引入

**为什么需要Transformer？**

虽然Self-Attention和Multi-Head Attention解决了RNN的问题，但仍需要：
1. **完整的架构**：如何将各种组件组合成网络
2. **位置信息**：Self-Attention没有位置概念
3. **非线性变换**：仅靠注意力无法建模复杂函数
4. **训练稳定性**：如何确保深层网络的稳定训练

**解决方案：完整的Transformer架构！**

---

## 🏗️ Transformer整体架构

### **完整结构图**

```
                    Transformer架构
                           ↓
    ┌─────────────────────────────────────────┐
    │                编码器 (Encoder)           │
    │  ┌─────────────────────────────────────┐ │
    │  │           层1 (Layer 1)              │ │
    │  │  ┌──────────────┐ ┌───────────────┐  │ │
    │  │  │ Multi-Head   │ │ Feed Forward  │  │ │
    │  │  │ Attention    │ │ Network       │  │ │
    │  │  │ + Residual   │ │ + Residual    │  │ │
    │  │  │ + LayerNorm  │ │ + LayerNorm   │  │ │
    │  │  └──────────────┘ └───────────────┘  │ │
    │  └─────────────────────────────────────┘ │
    │                  ↓                       │
    │  ┌─────────────────────────────────────┐ │
    │  │           层2 (Layer 2)              │ │
    │  │  ┌──────────────┐ ┌───────────────┐  │ │
    │  │  │ Multi-Head   │ │ Feed Forward  │  │ │
    │  │  │ Attention    │ │ Network       │  │ │
    │  │  │ + Residual   │ │ Residual      │  │ │
    │  │  │ + LayerNorm  │ │ + LayerNorm   │  │ │
    │  │  └──────────────┘ └───────────────┘  │ │
    │  └─────────────────────────────────────┘ │
    │                  ↓                       │
    │                ... N层                    │
    └─────────────────────────────────────────┘
                           ↓
    ┌─────────────────────────────────────────┐
    │                解码器 (Decoder)           │
    │  ┌─────────────────────────────────────┐ │
    │  │           层1 (Layer 1)              │ │
    │  │  ┌──────────────┐ ┌───────────────┐  │ │
    │  │  │ Masked       │ │ Multi-Head    │  │ │
    │  │  │ Multi-Head   │ │ Attention     │  │ │
    │  │  │ Attention    │ │ (Cross-Attn)  │  │ │
    │  │  │ + Residual   │ │ + Residual    │  │ │
    │  │  │ + LayerNorm  │ │ + LayerNorm   │  │ │
    │  │  └──────────────┘ └───────────────┘  │ │
    │  │              ┌───────────────┐       │ │
    │  │              │ Feed Forward  │       │ │
    │  │              │ Network       │       │ │
    │  │              │ + Residual    │       │ │
    │  │              │ + LayerNorm   │       │ │
    │  │              └───────────────┘       │ │
    │  └─────────────────────────────────────┘ │
    │                  ↓                       │
    │                ... N层                    │
    └─────────────────────────────────────────┘
                           ↓
    ┌─────────────────────────────────────────┐
    │              输出层                       │
    │         Linear + Softmax                 │
    └─────────────────────────────────────────┘
```

### **核心组件**

1. **编码器 (Encoder)**
   - Multi-Head Self-Attention
   - Feed-Forward Network (FFN)
   - 残差连接 + LayerNorm

2. **解码器 (Decoder)**
   - Masked Multi-Head Self-Attention
   - Multi-Head Cross-Attention
   - Feed-Forward Network (FFN)
   - 残差连接 + LayerNorm

3. **位置编码 (Position Encoding)**
   - 解决序列位置信息问题

---

## 🔄 编码器 (Encoder) 详解

### **编码器层结构**

```
编码器层输入: X ∈ ℝ^{L×d_model}
    ↓
第一步: Multi-Head Self-Attention
    ↓ 残差连接 + LayerNorm
    ↓
第二步: Feed-Forward Network
    ↓ 残差连接 + LayerNorm
    ↓
编码器层输出: X' ∈ ℝ^{L×d_model}
```

### **第一步：Multi-Head Self-Attention + Residual + LayerNorm**

```python
class EncoderSelfAttentionLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        self.self_attention = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        # Feed-Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self, x, mask=None):
        # ======== 第一步: Self-Attention ========
        # 输入x经过self-attention
        attn_output, attn_weights = self.self_attention(x, mask)
        # 残差连接 + LayerNorm
        x = self.norm1(x + attn_output)

        # ======== 第二步: Feed-Forward ========
        # 输入x经过FFN
        ffn_output = self.ffn(x)
        # 残差连接 + LayerNorm
        x = self.norm2(x + ffn_output)

        return x, attn_weights

# 验证形状变化
x = torch.randn(2, 10, 512)  # [batch, seq_len, d_model]
encoder_layer = EncoderSelfAttentionLayer(d_model=512, n_heads=8, d_ff=2048)
output, weights = encoder_layer(x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
```

### **完整编码器**

```python
class Encoder(nn.Module):
    """完整的Transformer编码器"""

    def __init__(self, d_model, n_heads, d_ff, n_layers, max_seq_len):
        super().__init__()
        self.d_model = d_model
        self.n_layers = n_layers

        # 位置编码
        self.pos_encoding = PositionalEncoding(d_model, max_seq_len)

        # 多个编码器层
        self.layers = nn.ModuleList([
            EncoderSelfAttentionLayer(d_model, n_heads, d_ff)
            for _ in range(n_layers)
        ])

        # 输出层归一化
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        # 添加位置编码
        x = x + self.pos_encoding(x)

        # 逐层计算
        all_outputs = []
        all_attention_weights = []

        for layer in self.layers:
            x, attn_weights = layer(x, mask)
            all_outputs.append(x)
            all_attention_weights.append(attn_weights)

        # 最终层归一化
        x = self.norm(x)

        return x, all_outputs, all_attention_weights

# 使用示例
d_model = 512
n_heads = 8
d_ff = 2048
n_layers = 6
max_seq_len = 1000

encoder = Encoder(d_model, n_heads, d_ff, n_layers, max_seq_len)
encoder_output, encoder_states, all_attention = encoder(x)
print(f"Encoder output shape: {encoder_output.shape}")
print(f"Number of layers: {len(encoder_states)}")
```

---

## 🔄 解码器 (Decoder) 详解

### **解码器层结构**

```
解码器层输入: Y ∈ ℝ^{L×d_model}
    ↓
第一步: Masked Multi-Head Self-Attention
    ↓ 残差连接 + LayerNorm
    ↓
第二步: Multi-Head Cross-Attention (Query=解码器, Key/Value=编码器)
    ↓ 残差连接 + LayerNorm
    ↓
第三步: Feed-Forward Network
    ↓ 残差连接 + LayerNorm
    ↓
解码器层输出: Y' ∈ ℝ^{L×d_model}
```

### **Masked Multi-Head Self-Attention**

```python
def create_decoder_mask(seq_len):
    """创建解码器的掩码，防止看到未来信息"""
    # 上三角矩阵（不包括对角线）
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
    return mask  # [seq_len, seq_len]

# 掩码示例
seq_len = 5
mask = create_decoder_mask(seq_len)
print("Decoder mask:")
print(mask)

# 掩码的作用：
# 时间步1: 可以看位置1
# 时间步2: 可以看位置1, 2
# 时间步3: 可以看位置1, 2, 3
# ...
```

### **解码器层实现**

```python
class DecoderSelfAttentionLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff):
        super().__init__()
        # 自注意力（带掩码）
        self.self_attention = MultiHeadAttention(d_model, n_heads)
        # 交叉注意力（编码器-解码器）
        self.cross_attention = MultiHeadAttention(d_model, n_heads)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)

        # Feed-Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

    def forward(self, x, encoder_output, self_mask=None, cross_mask=None):
        # ======== 第一步: Masked Self-Attention ========
        self_attn_output, self_attn_weights = self.self_attention(x, self_mask)
        x = self.norm1(x + self_attn_output)

        # ======== 第二步: Cross-Attention ========
        cross_attn_output, cross_attn_weights = self.cross_attention(
            query=x,  # 来自解码器
            key=encoder_output,  # 来自编码器
            value=encoder_output,  # 来自编码器
            mask=cross_mask
        )
        x = self.norm2(x + cross_attn_output)

        # ======== 第三步: Feed-Forward ========
        ffn_output = self.ffn(x)
        x = self.norm3(x + ffn_output)

        return x, self_attn_weights, cross_attn_weights

# 使用示例
decoder_layer = DecoderSelfAttentionLayer(d_model=512, n_heads=8, d_ff=2048)

# 模拟数据
decoder_input = torch.randn(2, 5, 512)  # 解码器输入
encoder_output = torch.randn(2, 10, 512)  # 编码器输出

# 创建掩码
decoder_mask = create_decoder_mask(5).unsqueeze(0).unsqueeze(1)  # [1, 1, 5, 5]

decoder_output, self_weights, cross_weights = decoder_layer(
    x=decoder_input,
    encoder_output=encoder_output,
    self_mask=decoder_mask
)

print(f"Decoder output shape: {decoder_output.shape}")
print(f"Self-attention weights shape: {self_weights.shape}")
print(f"Cross-attention weights shape: {cross_weights.shape}")
```

### **完整解码器**

```python
class Decoder(nn.Module):
    """完整的Transformer解码器"""

    def __init__(self, d_model, n_heads, d_ff, n_layers, max_seq_len):
        super().__init__()
        self.d_model = d_model
        self.n_layers = n_layers

        # 位置编码
        self.pos_encoding = PositionalEncoding(d_model, max_seq_len)

        # 多个解码器层
        self.layers = nn.ModuleList([
            DecoderSelfAttentionLayer(d_model, n_heads, d_ff)
            for _ in range(n_layers)
        ])

        # 输出层归一化
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, encoder_output, self_mask=None, cross_mask=None):
        # 添加位置编码
        x = x + self.pos_encoding(x)

        # 逐层计算
        all_self_attention = []
        all_cross_attention = []

        for layer in self.layers:
            x, self_attn, cross_attn = layer(
                x, encoder_output, self_mask, cross_mask
            )
            all_self_attention.append(self_attn)
            all_cross_attention.append(cross_attn)

        # 最终层归一化
        x = self.norm(x)

        return x, all_self_attention, all_cross_attention

# 使用示例
decoder = Decoder(d_model, n_heads, d_ff, n_layers, max_seq_len)
decoder_output, decoder_self_attn, decoder_cross_attn = decoder(
    x=decoder_input,
    encoder_output=encoder_output,
    self_mask=decoder_mask
)

print(f"Decoder output shape: {decoder_output.shape}")
```

---

## 📐 位置编码 (Position Encoding)

### **为什么需要位置编码？**

```
问题：Self-Attention是位置无关的

输入1: "I love Beijing"
输入2: "Beijing love I"

Q、K、V完全相同 → 注意力权重相同 → 输出相同！

但这两个句子的语义完全不同！

解决方案：添加位置信息！
```

### **正弦-余弦位置编码 (Sinusoidal PE)**

```python
import math

class PositionalEncoding(nn.Module):
    """正弦-余弦位置编码"""

    def __init__(self, d_model, max_seq_len=5000):
        super().__init__()
        self.d_model = d_model

        # 预计算位置编码
        pe = torch.zeros(max_seq_len, d_model)
        position = torch.arange(0, max_seq_len, dtype=torch.float).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() *
            (-math.log(10000.0) / d_model)
        )

        # 偶数维度用sin
        pe[:, 0::2] = torch.sin(position * div_term)
        # 奇数维度用cos
        pe[:, 1::2] = torch.cos(position * div_term)

        self.register_buffer('pe', pe.unsqueeze(0))  # [1, max_seq_len, d_model]

    def forward(self, x):
        """
        x: [batch, seq_len, d_model]
        """
        seq_len = x.size(1)
        x = x + self.pe[:, :seq_len, :]
        return x

# 使用示例
pos_encoding = PositionalEncoding(d_model=512, max_seq_len=1000)

# 模拟输入
x = torch.randn(2, 10, 512)
x_with_pe = pos_encoding(x)

print(f"Input shape: {x.shape}")
print(f"Output shape: {x_with_pe.shape}")
print(f"Position encoding shape: {pos_encoding.pe.shape}")

# 可视化位置编码
import matplotlib.pyplot as plt

pe = pos_encoding.pe.squeeze(0).numpy()  # [1000, 512]

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(pe.T, cmap='RdBu', aspect='auto')
plt.xlabel('Position')
plt.ylabel('Dimension')
plt.title('Position Encoding Heatmap')

plt.subplot(1, 2, 2)
plt.plot(pe[:, 0], label='dim 0 (sin)')
plt.plot(pe[:, 1], label='dim 1 (cos)')
plt.xlabel('Position')
plt.plot(pe[:, 2], label='dim 2 (sin)')
plt.plot(pe[:, 3], label='dim 3 (cos)')
plt.xlabel('Position')
plt.ylabel('Value')
plt.title('Position Encoding Curves')
plt.legend()
plt.tight_layout()
plt.show()
```

### **相对位置编码 (Relative PE)**

```python
class RelativePositionalEncoding(nn.Module):
    """相对位置编码"""

    def __init__(self, d_model, max_rel_pos=512):
        super().__init__()
        self.d_model = d_model
        self.max_rel_pos = max_rel_pos

        # 可学习的相对位置嵌入
        self.rel_pos_embed = nn.Embedding(2 * max_rel_pos + 1, d_model)

    def forward(self, seq_len):
        """生成相对位置编码"""
        # 创建相对位置索引
        rel_pos = torch.arange(seq_len).unsqueeze(1) - torch.arange(seq_len).unsqueeze(0)
        # 限制在[-max_rel_pos, max_rel_pos]
        rel_pos = torch.clamp(rel_pos, -self.max_rel_pos, self.max_rel_pos)
        # 映射到[0, 2*max_rel_pos]
        rel_pos = rel_pos + self.max_rel_pos

        # 获取位置嵌入
        rel_pe = self.rel_pos_embed(rel_pos)
        return rel_pe

# 使用示例
rel_pe = RelativePositionalEncoding(d_model=512, max_rel_pos=128)
relative_encoding = rel_pe(seq_len=10)
print(f"Relative PE shape: {relative_encoding.shape}")
```

---

## 🔧 前馈神经网络 (Feed-Forward Network, FFN)

### **FFN的作用**

```
为什么需要FFN？
1. 增加非线性变换能力
2. 学习更复杂的函数映射
3. 增强模型的表示能力
4. 维度变换 (d_model → d_ff → d_model)
```

### **FFN结构**

```python
class FeedForward(nn.Module):
    """Transformer中的前馈神经网络"""

    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        """
        x: [batch, seq_len, d_model]
        """
        # 第一层：升维
        x = self.linear1(x)  # [batch, seq_len, d_ff]
        # 激活函数：ReLU
        x = F.relu(x)
        # Dropout正则化
        x = self.dropout(x)
        # 第二层：降维
        x = self.linear2(x)  # [batch, seq_len, d_model]

        return x

# 使用示例
ffn = FeedForward(d_model=512, d_ff=2048, dropout=0.1)
ffn_output = ffn(x)
print(f"FFN input shape: {x.shape}")
print(f"FFN output shape: {ffn_output.shape}")

# FFN的维度变化：
# d_model (512) → d_ff (2048) → d_model (512)
# 中间的d_ff通常设置为d_model的4倍
```

### **FFN vs Self-Attention**

| 组件 | Self-Attention | Feed-Forward Network |
|------|---------------|---------------------|
| **作用** | 建模序列内部关系 | 逐位置非线性变换 |
| **计算** | 跨位置计算 | 位置独立计算 |
| **参数共享** | 参数在序列位置间共享 | 无参数共享 |
| **复杂度** | O(L² × d) | O(L × d × d_ff) |
| **位置依赖** | 位置间有依赖 | 位置独立 |

---

## 🎨 LayerNorm vs BatchNorm

### **LayerNorm的特点**

```python
class LayerNorm(nn.Module):
    """层归一化 - Transformer中使用"""

    def __init__(self, normalized_shape, eps=1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(normalized_shape))
        self.bias = nn.Parameter(torch.zeros(normalized_shape))

    def forward(self, x):
        """
        x: [batch, seq_len, d_model]
        """
        mean = x.mean(-1, keepdim=True)  # 在最后一个维度上计算均值
        std = x.std(-1, keepdim=True)    # 在最后一个维度上计算标准差
        x_norm = (x - mean) / (std + self.eps)  # 归一化
        return x_norm * self.weight + self.bias  # 缩放和平移

# 使用示例
layer_norm = LayerNorm(normalized_shape=512)
ln_output = layer_norm(x)
print(f"LayerNorm input shape: {x.shape}")
print(f"LayerNorm output shape: {ln_output.shape}")
```

### **LayerNorm vs BatchNorm对比**

| 特性 | LayerNorm | BatchNorm |
|------|-----------|-----------|
| **归一化维度** | 每层的特征维度 | 批次维度 |
| **适用场景** | 序列数据、变长输入 | 图像数据、批量稳定 |
| **依赖性** | 不依赖批量大小 | 依赖批量大小 |
| **位置** | 残差连接内部 | 卷积层后 |
| **训练/推理** | 相同 | 不同（需要维护统计量） |

### **为什么Transformer使用LayerNorm？**

```
原因1：序列长度可变
- 不同的句子长度不同
- BatchNorm依赖固定的batch维度
- LayerNorm不依赖batch大小

原因2：位置独立计算
- 每个位置的归一化是独立的
- 符合Transformer的设计思想

原因3：训练稳定性
- LayerNorm让训练更稳定
- 减少梯度消失/爆炸
```

---

## 💻 完整Transformer实现

### **标准Transformer架构**

```python
class Transformer(nn.Module):
    """完整的Transformer模型"""

    def __init__(self, vocab_size, d_model=512, n_heads=8, d_ff=2048,
                 n_layers=6, max_seq_len=1000, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size

        # 词嵌入
        self.embedding = nn.Embedding(vocab_size, d_model)

        # 编码器
        self.encoder = Encoder(d_model, n_heads, d_ff, n_layers, max_seq_len)

        # 解码器
        self.decoder = Decoder(d_model, n_heads, d_ff, n_layers, max_seq_len)

        # 输出层
        self.output_projection = nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        """
        src: [batch, src_len] - 源序列
        tgt: [batch, tgt_len] - 目标序列
        src_mask: [batch, 1, src_len] - 源序列掩码
        tgt_mask: [batch, tgt_len, tgt_len] - 目标序列掩码
        """
        batch_size, src_len = src.size()
        batch_size, tgt_len = tgt.size()

        # ======== 编码器 ========
        # 词嵌入
        src_embedded = self.embedding(src) * math.sqrt(self.d_model)
        # 编码器前向传播
        encoder_output, encoder_states, encoder_attention = self.encoder(
            src_embedded, src_mask
        )

        # ======== 解码器 ========
        # 词嵌入
        tgt_embedded = self.embedding(tgt) * math.sqrt(self.d_model)
        # 解码器前向传播
        decoder_output, decoder_self_attention, decoder_cross_attention = self.decoder(
            tgt_embedded, encoder_output, tgt_mask, src_mask
        )

        # ======== 输出层 ========
        # 投影到词汇表大小
        output_logits = self.output_projection(decoder_output)

        return output_logits, {
            'encoder': encoder_attention,
            'decoder_self': decoder_self_attention,
            'decoder_cross': decoder_cross_attention
        }

# 使用示例
if __name__ == "__main__":
    # 模型参数
    vocab_size = 10000
    d_model = 512
    n_heads = 8
    d_ff = 2048
    n_layers = 6
    max_seq_len = 1000

    # 创建模型
    transformer = Transformer(vocab_size, d_model, n_heads, d_ff, n_layers, max_seq_len)

    # 模拟数据
    batch_size = 2
    src_len = 10
    tgt_len = 12

    src = torch.randint(0, vocab_size, (batch_size, src_len))
    tgt = torch.randint(0, vocab_size, (batch_size, tgt_len))

    # 创建掩码
    src_mask = (src != 0).unsqueeze(1).unsqueeze(2)  # [batch, 1, 1, src_len]
    tgt_mask = create_decoder_mask(tgt_len).unsqueeze(0).unsqueeze(1)  # [batch, 1, tgt_len, tgt_len]

    # 前向传播
    output, attention_dict = transformer(src, tgt, src_mask, tgt_mask)

    print(f"Input src shape: {src.shape}")
    print(f"Input tgt shape: {tgt.shape}")
    print(f"Output shape: {output.shape}")
    print(f"\nAttention keys: {attention_dict.keys()}")
```

### **编码器专用Transformer**

```python
class EncoderTransformer(nn.Module):
    """仅用于编码的Transformer (如BERT)"""

    def __init__(self, vocab_size, d_model=768, n_heads=12, d_ff=3072,
                 n_layers=12, max_seq_len=512, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size

        # 词嵌入和位置嵌入
        self.embedding = nn.Embedding(vocab_size, d_model)

        # 编码器
        self.encoder = Encoder(d_model, n_heads, d_ff, n_layers, max_seq_len)

        # 输出层 (用于分类)
        self.pooler = nn.Linear(d_model, d_model)
        self.activation = nn.Tanh()
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(d_model, 1)  # 二分类

    def forward(self, input_ids, attention_mask=None):
        # 词嵌入
        x = self.embedding(input_ids) * math.sqrt(self.d_model)

        # 编码器
        x, _, encoder_attention = self.encoder(x, attention_mask)

        # 池化 [CLS] token
        pooled_output = self.pooler(x[:, 0])  # 第一个token
        pooled_output = self.activation(pooled_output)
        pooled_output = self.dropout(pooled_output)

        # 分类
        logits = self.classifier(pooled_output)

        return logits, encoder_attention

# 使用示例
bert_encoder = EncoderTransformer(vocab_size=30000, d_model=768, n_heads=12)
input_ids = torch.randint(0, 30000, (2, 128))  # [batch, seq_len]
logits, attention = bert_encoder(input_ids)
print(f"Input shape: {input_ids.shape}")
print(f"Output shape: {logits.shape}")
```

### **解码器专用Transformer (GPT)**

```python
class DecoderTransformer(nn.Module):
    """仅用于解码的Transformer (如GPT)"""

    def __init__(self, vocab_size, d_model=768, n_heads=12, d_ff=3072,
                 n_layers=12, max_seq_len=1024, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size

        # 词嵌入和位置嵌入
        self.embedding = nn.Embedding(vocab_size, d_model)

        # 解码器
        self.decoder = Decoder(d_model, n_heads, d_ff, n_layers, max_seq_len)

        # 输出层
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, input_ids, attention_mask=None):
        batch_size, seq_len = input_ids.size()

        # 词嵌入
        x = self.embedding(input_ids) * math.sqrt(self.d_model)

        # 创建因果掩码
        causal_mask = create_decoder_mask(seq_len)
        if attention_mask is not None:
            causal_mask = causal_mask & attention_mask.unsqueeze(0).unsqueeze(1)

        # 解码器
        x, _, decoder_attention = self.decoder(x, None, causal_mask, None)

        # 输出投影
        logits = self.lm_head(x)

        return logits, decoder_attention

# 使用示例
gpt_decoder = DecoderTransformer(vocab_size=50000, d_model=768, n_heads=12)
input_ids = torch.randint(0, 50000, (2, 128))  # [batch, seq_len]
logits, attention = gpt_decoder(input_ids)
print(f"Input shape: {input_ids.shape}")
print(f"Output shape: {logits.shape}")
```

---

## 🔄 训练和推理流程

### **训练流程**

```python
def train_transformer(model, dataloader, optimizer, criterion, epoch):
    model.train()
    total_loss = 0

    for batch_idx, (src, tgt) in enumerate(dataloader):
        # 准备数据
        src = src.to(device)
        tgt = tgt.to(device)

        # 创建掩码
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        tgt_mask = create_decoder_mask(tgt.size(1)).unsqueeze(0).unsqueeze(1)

        # 前向传播
        optimizer.zero_grad()
        output, _ = model(src, tgt, src_mask, tgt_mask)

        # 计算损失
        tgt_input = tgt[:, :-1]  # 去掉最后一个token
        tgt_output = tgt[:, 1:]  # 去掉第一个token
        loss = criterion(output.reshape(-1, output.size(-1)), tgt_output.reshape(-1))

        # 反向传播
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if batch_idx % 100 == 0:
            print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}')

    return total_loss / len(dataloader)
```

### **推理流程 (贪婪解码)**

```python
def greedy_decode(model, src, src_mask, max_length=100, start_token=1, end_token=2):
    model.eval()
    batch_size = src.size(0)

    # 编码器编码
    with torch.no_grad():
        src_embedded = model.embedding(src) * math.sqrt(model.d_model)
        encoder_output, _, _ = model.encoder(src_embedded, src_mask)

    # 解码器初始化
    tgt = torch.ones(batch_size, 1).long().to(src.device) * start_token

    for i in range(max_length):
        # 创建目标掩码
        tgt_mask = create_decoder_mask(tgt.size(1)).to(src.device)

        # 解码器前向传播
        with torch.no_grad():
            tgt_embedded = model.embedding(tgt) * math.sqrt(model.d_model)
            decoder_output, _, _ = model.decoder(
                tgt_embedded, encoder_output, tgt_mask, src_mask
            )
            output = model.output_projection(decoder_output)

        # 选择下一个token
        next_token = output[:, -1].argmax(dim=-1, keepdim=True)
        tgt = torch.cat([tgt, next_token], dim=1)

        # 检查是否到达结束符
        if (next_token == end_token).all():
            break

    return tgt

# 使用示例
# src = torch.randint(0, 10000, (1, 20))
# src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
# result = greedy_decode(transformer, src, src_mask)
# print(f"Generated sequence: {result}")
```

### **推理流程 (束搜索)**

```python
def beam_search_decode(model, src, src_mask, beam_width=5, max_length=100,
                       start_token=1, end_token=2):
    model.eval()

    # 编码
    with torch.no_grad():
        src_embedded = model.embedding(src) * math.sqrt(model.d_model)
        encoder_output, _, _ = model.encoder(src_embedded, src_mask)

    # 初始化束搜索
    beams = [(torch.ones(1, 1).long().to(src.device) * start_token, 0.0)]

    for _ in range(max_length):
        new_beams = []

        for beam_seq, beam_score in beams:
            # 解码器前向传播
            with torch.no_grad():
                tgt_embedded = model.embedding(beam_seq) * math.sqrt(model.d_model)
                tgt_mask = create_decoder_mask(beam_seq.size(1)).to(src.device)
                decoder_output, _, _ = model.decoder(
                    tgt_embedded, encoder_output, tgt_mask, src_mask
                )
                output = model.output_projection(decoder_output)

            # 获取下一个token的概率分布
            next_token_probs = F.softmax(output[:, -1], dim=-1)

            # 获取top-k个候选
            top_k_probs, top_k_tokens = torch.topk(next_token_probs, beam_width)

            for i in range(beam_width):
                new_seq = torch.cat([beam_seq, top_k_tokens[:, i:i+1]], dim=1)
                new_score = beam_score + torch.log(top_k_probs[:, i])

                new_beams.append((new_seq, new_score))

        # 选择top-k个束
        beams = sorted(new_beams, key=lambda x: x[1], reverse=True)[:beam_width]

        # 检查是否有束到达结束符
        if all(beam_seq[0, -1] == end_token for beam_seq, _ in beams):
            break

    return beams[0][0]

# 使用示例
# result = beam_search_decode(transformer, src, src_mask, beam_width=3)
# print(f"Beam search result: {result}")
```

---

## 💡 关键要点总结

### **Transformer的核心组件**

1. **编码器 (Encoder)**
   - Multi-Head Self-Attention
   - Feed-Forward Network
   - 残差连接 + LayerNorm

2. **解码器 (Decoder)**
   - Masked Multi-Head Self-Attention
   - Multi-Head Cross-Attention
   - Feed-Forward Network
   - 残差连接 + LayerNorm

3. **位置编码 (Position Encoding)**
   - 正弦-余弦编码 (Sinusoidal)
   - 相对位置编码 (Relative)

### **关键特性**

1. ✅ **并行计算**：充分利用GPU
2. ✅ **长距离依赖**：直接连接任意位置
3. ✅ **灵活性**：可用于编码、解码、分类等多种任务
4. ✅ **可扩展性**：易于构建大型模型

### **设计原则**

1. **残差连接**：保持梯度流动
2. **LayerNorm**：稳定训练过程
3. **位置编码**：注入序列信息
4. **掩码机制**：控制信息流动

---

## 🎓 下一步学习

**现在您完全理解了Transformer的整体架构，接下来可以学习：**

1. **训练技巧** - 学习率调度、warm-up、label smoothing
2. **优化实现** - Flash Attention、梯度检查点
3. **变体模型** - BERT、GPT、T5等
4. **在DeepSeek-V3中的应用** - Multi-Head Latent Attention、MoE

**选择您想继续学习的主题！** 🤔
