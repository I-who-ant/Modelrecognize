# CBOW vs Skip-gram 深度对比与词嵌入预测机制

**学习日期**: 2025-10-31
**重要程度**: 🔴必学 ⭐⭐⭐⭐⭐
**前置知识**: Word2Vec 基础、神经网络
**关键问题**:
1. CBOW 和 Skip-gram 的核心区别是什么？
2. 词嵌入如何从预测概率到选择词？

---
# 语料 意思 是: 一个句子中，每个位置的词都可以作为中心词，而上下文词是中心词周围的词。

## 🎯 核心问题 1：CBOW vs Skip-gram 的本质区别

### 最核心的三个区别

```
区别 1: 输入输出方向相反 ⭐⭐⭐⭐⭐
═════════════════════════════════

CBOW (Continuous Bag of Words):
  输入: 上下文词 (多个)
  输出: 中心词 (1个)

  示例: ["quick", "brown", "jumps", "over"] → "fox"
        ────────────────┬────────────────
                    多个输入
                        ↓
                    平均池化
                        ↓
                   预测中心词

Skip-gram:
  输入: 中心词 (1个)
  输出: 上下文词 (多个)

  示例: "fox" → ["quick", "brown", "jumps", "over"]
        ───
       单个
        ↓
      复制
        ↓
    预测多个上下文词

可视化:
──────

CBOW:
   [quick]  [brown]  [jumps]  [over]
      ↓        ↓        ↓        ↓
   e_quick e_brown e_jumps  e_over
      └────────┴────────┴────────┘
                  ↓
              平均池化 → h
                  ↓
             预测 "fox"

Skip-gram:
            [fox]
              ↓
            e_fox
              ↓
        ┌─────┼─────┬─────┐
        ↓     ↓     ↓     ↓
    predict predict predict predict
     "quick" "brown" "jumps" "over"

关键洞察:
✅ CBOW: 多对一 (Many → One)
✅ Skip-gram: 一对多 (One → Many)
```

---

### 区别 2: 训练样本数量差异 ⭐⭐⭐⭐⭐

```
训练样本生成:
═══════════

语料: "The quick brown fox jumps over the lazy dog"
窗口: m = 2
中心词: "fox"
上下文: ["quick", "brown", "jumps", "over"]

CBOW 生成样本:
─────────────

只生成 1 个训练样本:
  输入: ["quick", "brown", "jumps", "over"]
  输出: "fox"

每个位置生成 1 个样本
总样本数 = 语料长度

Skip-gram 生成样本:
──────────────────

生成 4 个训练样本:
  样本1: "fox" → "quick"
  样本2: "fox" → "brown"
  样本3: "fox" → "jumps"
  样本4: "fox" → "over"

每个位置生成 2×窗口大小 个样本
总样本数 = 语料长度 × 2m

数量对比:
────────

假设语料有 N 个词，窗口大小 m = 5

CBOW 训练样本:   N 个
Skip-gram 训练样本: N × 10 个

Skip-gram 的训练样本是 CBOW 的 10 倍！

为什么 Skip-gram 对低频词效果好？
─────────────────────────────

低频词 "giraffe" 在语料中出现 10 次:

CBOW:
  "giraffe" 作为目标出现 10 次
  → 10 个训练样本更新 "giraffe" 的向量

Skip-gram:
  "giraffe" 作为输入出现 10 次
  每次生成 10 个训练样本 (m=5)
  → 100 个训练样本更新 "giraffe" 的向量

更多训练样本 → 更好的向量！🎯
```

---

### 区别 3: 计算复杂度

```
单个位置的计算:
═══════════════

CBOW:
  前向传播:
    1. 查找上下文词向量: 2m 次查表
    2. 平均池化: 2m 次加法 + 1 次除法
    3. 预测中心词: 1 次 softmax/负采样

  复杂度: O(2m + V) 或 O(2m + k)

Skip-gram:
  前向传播:
    1. 查找中心词向量: 1 次查表
    2. 预测每个上下文词: 2m 次 softmax/负采样

  复杂度: O(1 + 2m×V) 或 O(1 + 2m×k)

使用负采样时:
  CBOW: O(k) - 更快 ✨
  Skip-gram: O(2m×k) - 慢 2m 倍

实际训练时间:
───────────

在 1B 词语料上 (m=5, k=5):

CBOW:
  样本数: 1B
  每样本: O(5) = 5 次计算
  总计: 5B 次计算

Skip-gram:
  样本数: 1B × 10 = 10B
  每样本: O(1 + 10×5) = 51 次计算
  总计: 510B 次计算

Skip-gram 慢约 100 倍！

但是：
✅ Skip-gram 质量更好（尤其低频词）
✅ 可以用更小的窗口加速
✅ 并行化更容易
```

---

## 💡 核心问题 2：词嵌入如何从预测到选择？

### 关键误解澄清 ⚠️

```
常见误解:
════════

❌ 误解: Word2Vec 根据预测概率从词嵌入表中"选择"一个词

✅ 真相: Word2Vec 的目的不是预测词，而是学习词向量！

预测任务只是一个"代理任务"(Proxy Task)
用来驱动词向量的学习

类比理解:
────────

健身房的哑铃:
  哑铃本身不是目的
  目的是通过举哑铃锻炼肌肉

Word2Vec 的预测任务:
  预测本身不是目的
  目的是通过预测任务学习词向量

一旦训练完成，我们：
✅ 保留: 词向量（嵌入矩阵）
❌ 丢弃: 预测网络（输出层）

Word2Vec 的"产品"是词向量，不是预测模型！
```

---

### 训练阶段 vs 使用阶段

```
阶段对比:
════════

┌─────────────────────────────────────────────────────────┐
│ 训练阶段 (Training)                                      │
├─────────────────────────────────────────────────────────┤
│ 目的: 学习词向量                                         │
│                                                         │
│ 过程:                                                   │
│   1. 输入: 上下文/中心词                                │
│      ↓                                                  │
│   2. 查找词向量 (从嵌入矩阵 E)                          │
│      ↓                                                  │
│   3. 计算得分 (向量点积)                                │
│      ↓                                                  │
│   4. 计算概率 (softmax/负采样)  ← 这里有"预测"          │
│      ↓                                                  │
│   5. 计算损失 (交叉熵/二分类)                           │
│      ↓                                                  │
│   6. 反向传播，更新词向量                               │
│      ↓                                                  │
│   重复...直到收敛                                       │
│                                                         │
│ 输出: 学习好的嵌入矩阵 E                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 使用阶段 (Inference/Application)                        │
├─────────────────────────────────────────────────────────┤
│ 目的: 使用词向量做下游任务                              │
│                                                         │
│ 过程:                                                   │
│   1. 加载预训练的嵌入矩阵 E                             │
│      ↓                                                  │
│   2. 查表: e_word = E[word_idx]                         │
│      ↓                                                  │
│   3. 使用词向量:                                        │
│      - 计算相似度                                       │
│      - 词类比                                           │
│      - 作为特征输入分类器                               │
│      - ...                                              │
│                                                         │
│ ⚠️ 注意: 不需要"预测"，不需要"选择"！                   │
│          直接使用向量即可！                              │
└─────────────────────────────────────────────────────────┘

关键区别:
✅ 训练时: 需要预测（计算损失，更新参数）
✅ 使用时: 不需要预测（直接用向量）
```

---

### 详细的训练过程（以 Skip-gram 为例）

```
具体示例:
════════

语料: "The quick brown fox jumps"
训练样本: ("fox", "brown")  ← 中心词, 上下文词

Step 1: 前向传播
───────────────

① 查找中心词向量:
   word_idx = vocab["fox"] = 3
   v_fox = E[3]  # E 是嵌入矩阵 [vocab_size × d]

   例如: v_fox = [0.2, -0.1, 0.5, ..., 0.3]  (300维)

② 计算得分:

   a) 使用完整 Softmax:
      对词汇表中的每个词 w:
        score_w = v_fox · u_w  (点积)

      score_brown = v_fox · u_brown = 0.8
      score_cat = v_fox · u_cat = 0.3
      score_the = v_fox · u_the = -0.2
      ...
      (10万个词都要计算)

   b) 使用负采样:
      正样本: score_brown = v_fox · u_brown = 0.8
      负样本: score_neg1 = v_fox · u_neg1 = 0.1
             score_neg2 = v_fox · u_neg2 = -0.3
             ...
      (只计算 1 + k 个词)

③ 计算概率:

   a) Softmax:
      P(brown | fox) = exp(0.8) / Σ exp(score_w)
                     = 2.23 / (2.23 + 1.35 + 0.82 + ...)
                     ≈ 0.0003  ← 很小！因为分母很大

   b) 负采样 (Sigmoid):
      P(brown | fox) = σ(0.8) = 0.69  ← 正样本概率
      P(neg1 | fox) = σ(0.1) = 0.53
      P(neg2 | fox) = σ(-0.3) = 0.43

④ 计算损失:

   a) Softmax:
      L = -log P(brown | fox) = -log(0.0003) = 8.1

   b) 负采样:
      L = -log σ(score_brown) - Σ log σ(-score_neg_i)
        = -log(0.69) - log(1-0.53) - log(1-0.43)
        ≈ 0.37 + 0.76 + 0.56 = 1.69

Step 2: 反向传播
───────────────

① 计算梯度:

   ∂L/∂v_fox = ... (根据链式法则)
   ∂L/∂u_brown = ...
   ∂L/∂u_neg_i = ...

② 更新参数:

   v_fox ← v_fox - α · ∂L/∂v_fox
   u_brown ← u_brown - α · ∂L/∂u_brown
   u_neg_i ← u_neg_i - α · ∂L/∂u_neg_i

   例如:
   v_fox = [0.2, -0.1, 0.5, ..., 0.3]
         - 0.01 × [0.05, -0.02, 0.1, ..., 0.04]
         = [0.1995, -0.0998, 0.499, ..., 0.2996]

Step 3: 重复
───────────

对语料中的每个训练样本重复上述过程
经过数百万次迭代，词向量逐渐收敛

最终结果:
────────

嵌入矩阵 E:
  E[0] = [0.12, -0.34, 0.56, ...]  ← "the"
  E[1] = [0.23, 0.11, -0.45, ...]  ← "quick"
  E[2] = [0.19, -0.08, 0.33, ...]  ← "brown"
  E[3] = [0.21, -0.09, 0.35, ...]  ← "fox"
  ...

观察:
✅ "brown" 和 "fox" 的向量接近（经常共现）
✅ "the" 的向量与它们不同（语义不同）

⚠️ 重点:
   训练过程中有"预测概率"
   但最终产品只是词向量 E
   使用时不需要"选择"或"预测"
```

---

### 使用阶段：不需要预测！

```
常见应用场景:
═══════════

场景 1: 计算词相似度
────────────────────

任务: 找到与 "dog" 最相似的词

步骤:
  ① 查找 "dog" 的向量:
     v_dog = E[vocab["dog"]]

  ② 计算与所有词的余弦相似度:
     for word in vocabulary:
         v_word = E[vocab[word]]
         similarity = cosine(v_dog, v_word)

  ③ 排序，输出 top-k

⚠️ 注意: 全程没有"预测概率"，只有向量运算！

场景 2: 词类比
─────────────

任务: king - man + woman ≈ ?

步骤:
  ① 查找向量:
     v_king = E[vocab["king"]]
     v_man = E[vocab["man"]]
     v_woman = E[vocab["woman"]]

  ② 向量运算:
     v_target = v_king - v_man + v_woman

  ③ 找最接近的词:
     for word in vocabulary:
         v_word = E[vocab[word]]
         similarity = cosine(v_target, v_word)

     最接近的是 "queen"

⚠️ 注意: 全程只有向量加减和相似度计算！

场景 3: 文本分类
───────────────

任务: 情感分类 (正面/负面)

步骤:
  ① 将句子中的每个词转为向量:
     sentence = ["I", "love", "this", "movie"]
     vectors = [E[vocab[w]] for w in sentence]

  ② 平均池化:
     sentence_vec = mean(vectors)

  ③ 输入分类器:
     logits = W_classifier · sentence_vec + b
     prediction = softmax(logits)

⚠️ 注意:
   这里的 softmax 是分类器的输出
   不是 Word2Vec 的预测！
   Word2Vec 只提供词向量！

场景 4: 作为神经网络的输入层
────────────────────────────

任务: 命名实体识别 (NER)

网络结构:
  输入词序列 → [嵌入层] → LSTM → 分类层 → 输出标签

嵌入层的实现:
  class EmbeddingLayer(nn.Module):
      def __init__(self, pretrained_embeddings):
          super().__init__()
          # 加载预训练的 Word2Vec
          self.embedding = nn.Embedding.from_pretrained(
              pretrained_embeddings,
              freeze=False  # 可微调
          )

      def forward(self, word_indices):
          # 直接查表，返回向量
          return self.embedding(word_indices)

  输入: [2, 5, 8, 12, ...]  (词索引)
  输出: [[0.2, -0.1, ...], [0.3, 0.1, ...], ...]  (词向量)

⚠️ 注意:
   嵌入层只是查表操作
   没有"预测"或"选择"
```

---

## 🎨 关键概念对比

### 传统神经网络 vs 词嵌入

```
传统神经网络 (如分类器):
═══════════════════════

任务: 图像分类
输入: 图像像素 [H × W × 3]
输出: 类别概率 [num_classes]

训练:
  ① 前向传播 → 预测概率
  ② 计算损失 (交叉熵)
  ③ 反向传播 → 更新权重

使用:
  ① 前向传播 → 预测概率
  ② 选择概率最大的类别

关键:
✅ 训练和使用都需要"预测"
✅ 最终产品是整个网络
✅ 输出是类别预测

词嵌入 (Word2Vec):
═════════════════

任务: 学习词表示
输入: 词索引
输出: 词向量 [embedding_dim]

训练:
  ① 查表 → 词向量
  ② 计算得分 → 预测概率 (代理任务)
  ③ 计算损失
  ④ 反向传播 → 更新词向量

使用:
  ① 查表 → 词向量
  ② 直接使用向量

关键:
✅ 训练时需要"预测"（驱动学习）
✅ 使用时不需要"预测"（只用向量）
✅ 最终产品是嵌入矩阵
✅ 输出是词向量

对比:
────

         训练        使用        最终产品
分类器    预测        预测        整个网络
词嵌入    预测        查表        嵌入矩阵

分类器: 预测是目的
词嵌入: 预测是手段，向量是目的
```

---

### 为什么 Word2Vec 不是"选择"词？

```
从信息流角度理解:
═══════════════

训练时的信息流:
──────────────

   词索引 (离散)
      ↓
   [嵌入层 E] ← 可学习参数
      ↓
   词向量 (连续)
      ↓
   [计算得分] ← 向量点积
      ↓
   得分 (连续)
      ↓
   [Softmax/Sigmoid]
      ↓
   概率 (连续, 0-1)
      ↓
   [损失函数] ← 与真实标签比较
      ↓
   损失 (标量)
      ↓
   [反向传播]
      ↓
   梯度 → 更新嵌入层 E ← 关键！

观察:
✅ 概率只是中间产物
✅ 真正被更新的是嵌入层 E
✅ 我们不关心预测准确率
✅ 我们只关心学到的向量质量

使用时的信息流:
──────────────

   词索引 (离散)
      ↓
   [嵌入层 E] ← 固定参数
      ↓
   词向量 (连续)
      ↓
   [下游任务]
      ↓
   结果

观察:
✅ 直接跳到词向量
✅ 没有"预测"环节
✅ 没有"选择"操作
✅ 只是查表 (table lookup)

类比理解:
────────

训练 Word2Vec = 学习一本词典
  词典: {"cat" → [0.2, -0.1, 0.5, ...],
         "dog" → [0.3, 0.1, 0.4, ...],
         ...}

使用 Word2Vec = 查词典
  输入: "cat"
  输出: [0.2, -0.1, 0.5, ...]

  不需要"选择"，直接查表！

传统分类器 = 学习判断规则
  训练: 学习规则
  使用: 应用规则预测

这是本质区别！
```

---

## 💡 核心要点总结

### CBOW vs Skip-gram

```
核心区别:
════════

1. 输入输出方向相反
   CBOW: 上下文 → 中心词 (多对一)
   Skip-gram: 中心词 → 上下文 (一对多)

2. 训练样本数量
   CBOW: N 个样本
   Skip-gram: N × 2m 个样本 (多 2m 倍)

3. 计算复杂度
   CBOW: 更快 (单次预测)
   Skip-gram: 更慢 (多次预测)

4. 低频词效果
   CBOW: 一般
   Skip-gram: 更好 (样本多)

5. 适用场景
   CBOW: 大语料 + 追求速度
   Skip-gram: 小语料 + 追求质量 ⭐

实践推荐: Skip-gram 更常用
```

---

### 词嵌入的"预测"本质

```
关键理解:
════════

❌ 误解: Word2Vec 根据概率"选择"词
✅ 真相: Word2Vec 学习词向量

1. 预测是手段，不是目的
   目的: 学习词向量
   手段: 通过预测任务驱动学习

2. 训练 ≠ 使用
   训练: 需要预测（计算损失）
   使用: 不需要预测（直接查表）

3. 最终产品是嵌入矩阵
   保留: 嵌入矩阵 E
   丢弃: 输出层、预测网络

4. 使用时是查表操作
   输入: 词索引
   输出: 词向量
   过程: table lookup (O(1))

类比:
  健身房的哑铃 (工具)
  → 锻炼肌肉 (目的)

  预测任务 (工具)
  → 学习词向量 (目的)
```

---

## 🤔 思考题

1. [ ] 为什么 Skip-gram 生成的训练样本是 CBOW 的 2m 倍？从数学角度推导。

2. [ ] 如果一个词在语料中出现 1 次，CBOW 和 Skip-gram 各生成多少训练样本？

3. [ ] 为什么说"预测只是代理任务"？能否设计其他代理任务来学习词向量？

4. [ ] 使用预训练词向量时，为什么不需要保留输出层（W_out）？

5. [ ] Word2Vec 的"查表"操作和神经网络的"前向传播"有什么区别？

6. [ ] 如果我们想用 Word2Vec 做"真正的词预测"（输入上下文，预测下一个词），应该怎么做？

---

## 🔗 相关概念

```
知识图谱:

传统神经网络
   ├─ 前馈网络
   ├─ 卷积网络
   └─ 预测是核心

Word2Vec ← 你在这里
   ├─ CBOW (多对一)
   ├─ Skip-gram (一对多) ⭐
   ├─ 预测是手段
   └─ 向量是目的

语言模型
   ├─ RNN/LSTM
   ├─ Transformer
   └─ 预测是核心（生成式）

区别:
✅ Word2Vec: 学习表示
✅ 语言模型: 学习分布
```

---

## 🚀 实践建议

### 理解 CBOW vs Skip-gram

```python
# CBOW: 多个输入 → 单个输出
def cbow_forward(context_words, center_word):
    """
    context_words: ["quick", "brown", "jumps", "over"]
    center_word: "fox"
    """
    # 查找上下文向量
    context_vecs = [embedding[w] for w in context_words]

    # 平均池化
    h = np.mean(context_vecs, axis=0)

    # 预测中心词（计算损失）
    score = np.dot(h, output_embedding[center_word])
    loss = -np.log(sigmoid(score))

    return loss  # 用于反向传播

# Skip-gram: 单个输入 → 多个输出
def skipgram_forward(center_word, context_words):
    """
    center_word: "fox"
    context_words: ["quick", "brown", "jumps", "over"]
    """
    # 查找中心词向量
    v_c = embedding[center_word]

    # 对每个上下文词预测
    total_loss = 0
    for context_word in context_words:
        score = np.dot(v_c, output_embedding[context_word])
        loss = -np.log(sigmoid(score))
        total_loss += loss

    return total_loss  # 用于反向传播
```

### 理解使用阶段

```python
# 训练完成后，只保留输入嵌入
pretrained_embedding = model.input_embedding  # [vocab_size, embed_dim]

# 使用阶段：直接查表
def get_word_vector(word):
    """不需要预测，直接查表"""
    word_idx = vocab[word]
    return pretrained_embedding[word_idx]

# 计算相似度
v_cat = get_word_vector("cat")
v_dog = get_word_vector("dog")
similarity = cosine_similarity(v_cat, v_dog)

# 词类比
v_king = get_word_vector("king")
v_man = get_word_vector("man")
v_woman = get_word_vector("woman")
v_target = v_king - v_man + v_woman

# 找最接近的词
similarities = [(word, cosine_similarity(v_target, get_word_vector(word)))
                for word in vocabulary]
best_match = max(similarities, key=lambda x: x[1])
print(f"king - man + woman ≈ {best_match[0]}")  # "queen"

# 注意：全程没有"预测"或"选择"，只有向量运算！
```

---

**更新日期**: 2025-10-31
**核心理解**:
1. Skip-gram 训练样本多，对低频词好
2. 预测只是训练手段，向量才是目的
3. 使用时不需要预测，只需查表

**下一步**: 深入理解负采样和层次 Softmax 的训练细节
