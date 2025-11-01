# GloVe - 基于全局统计的词向量

**学习日期**: 2025-10-31
**课程来源**: 深度学习序列模型系列 - GloVe 算法
**重要程度**: 🟡推荐 ⭐⭐⭐
**前置知识**: Word2Vec、词嵌入、矩阵分解
**模块地位**: 词嵌入的另一种经典方法，与 Word2Vec 齐名
**论文**: "GloVe: Global Vectors for Word Representation" (Pennington et al., 2014)

---

## 📌 基本定义

**GloVe (Global Vectors for Word Representation)** 是斯坦福大学于 2014 年提出的词嵌入算法，通过对全局词-词共现统计进行矩阵分解来学习词向量。

### 核心特点

```
GloVe 的三大特点:
═══════════════════

1. 全局统计 🌐
   - 基于整个语料库的共现统计
   - 不是局部窗口的在线学习
   - 预先计算共现矩阵

2. 显式优化目标 📐
   - 明确的损失函数
   - 优化词向量使其点积 ≈ log(共现次数)
   - 可解释性强

3. 快速训练 ⚡
   - 批量优化（非在线）
   - 适合中等规模语料
   - 收敛快

与 Word2Vec 的关系:
✅ 互补而非竞争
✅ 性能相近 
✅ 各有优势
```

---

## 🎯 核心思想

### Word2Vec 的局限

```
Word2Vec 的问题:
═══════════════

1. 局部窗口
   Skip-gram: 只看中心词周围 ±m 个词

   "The cat sat on the mat"
         ↑
      中心词
     ←  m  →
   只利用局部信息

2. 在线学习
   每次只看一个训练样本
   没有利用全局统计信息

3. 隐式目标
   通过预测任务间接学习
   不直观

示例:
语料中 "cat" 和 "dog" 共现 100 次
Word2Vec:
  - 生成 100 个训练样本
  - 逐个训练
  - 间接学习关系

问题:
  为什么不直接利用"共现 100 次"这个统计信息？
```

---

### GloVe 的解决方案

```
GloVe 的核心思想:
═══════════════

词的意义由其共现模式决定
→ 直接对共现统计建模！

关键洞察:
────────

词向量的点积应该反映词的共现程度

数学表达:
  w_i · w_j ≈ log(共现次数)

为什么用 log？
  - 共现次数可能很大（如 "the" 和 "is"）
  - log 压缩数值范围
  - 符合 Zipf 定律

完整目标:
  w_i · w_j + b_i + b_j ≈ log(X_ij)

其中:
  w_i, w_j: 词向量
  b_i, b_j: 偏置项
  X_ij: 词 i 和 j 的共现次数
```

---

## 🧮 数学原理

### 共现矩阵

```
定义:
════

X_ij = 词 i 在词 j 的上下文中出现的次数

示例语料:
────────

"I like deep learning. I like NLP. I enjoy flying."

窗口大小 = 1 (只看相邻词)

共现矩阵 X:
          I   like  deep  learning  NLP  enjoy  flying
I         0    2     0      0       0     1      0
like      2    0     1      0       1     0      0
deep      0    1     0      1       0     0      0
learning  0    0     1      0       0     0      0
NLP       0    1     0      0       0     0      0
enjoy     1    0     0      0       0     0      1
flying    0    0     0      0       0     1      0

观察:
  X_ij = 词 i 和词 j 共现的次数
  X 是对称矩阵: X_ij = X_ji
  对角线为 0 (词不和自己共现)

扩展:
  可以用不同窗口大小
  可以用距离加权 (近的词权重大)
```

---

### 目标函数推导

```
动机:
════

我们希望词向量满足:
  w_i^T · w_j = log P(j|i)

但这不对称！P(j|i) ≠ P(i|j)

改进:
  w_i^T · w_j = log P(i,j)
             = log X_ij - log X

其中 X = Σ_{i,j} X_ij (总共现次数)

问题:
  log X 是常数，可以吸收到偏置中

最终:
  w_i^T · w_j + b_i + b_j = log X_ij

损失函数:
════════

朴素想法:
  L = Σ_{i,j} (w_i^T · w_j + b_i + b_j - log X_ij)²

问题:
  1. X_ij 可能为 0 (log 0 无定义)
  2. 所有共现对权重相同 (不合理)

解决方案 1: 只对 X_ij > 0 求和
  L = Σ_{X_ij > 0} (w_i^T · w_j + b_i + b_j - log X_ij)²

解决方案 2: 加权
  L = Σ_{i,j} f(X_ij) · (w_i^T · w_j + b_i + b_j - log X_ij)²

权重函数 f(X_ij):
─────────────

设计原则:
  1. f(0) = 0  (不计入损失)
  2. f(x) 单调递增 (共现多 → 权重大)
  3. f(x) 有上界 (避免高频词主导)

GloVe 的选择:
  f(x) = (x / x_max)^α    if x < x_max
         1                  otherwise

通常: x_max = 100, α = 0.75

可视化:
  f(x)
    ↑
  1.0│         ────────────  (饱和)
     │       ／
  0.5│     ／
     │   ／
  0.0│ ／
     └──────────────────→ x
        0   100

特点:
  ✅ 低频词: 权重小 (可能是噪声)
  ✅ 中频词: 权重中等
  ✅ 高频词: 权重饱和 (避免 "the", "a" 主导)

完整目标函数:
═══════════

J = Σ_{i,j} f(X_ij) · (w_i^T · w̃_j + b_i + b̃_j - log X_ij)²

其中:
  w_i: 词 i 的"中心词"向量
  w̃_j: 词 j 的"上下文"向量
  b_i, b̃_j: 偏置项

⚠️ 注意:
  GloVe 也用两个向量矩阵
  最终词向量 = (w_i + w̃_i) / 2
```

---

### 优化算法

```
梯度下降:
════════

参数: {w_i, w̃_j, b_i, b̃_j}

梯度:
  ∂J/∂w_i = Σ_j 2·f(X_ij)·(w_i^T·w̃_j + b_i + b̃_j - log X_ij)·w̃_j

  ∂J/∂w̃_j = Σ_i 2·f(X_ij)·(w_i^T·w̃_j + b_i + b̃_j - log X_ij)·w_i

  ∂J/∂b_i = Σ_j 2·f(X_ij)·(w_i^T·w̃_j + b_i + b̃_j - log X_ij)

  ∂J/∂b̃_j = Σ_i 2·f(X_ij)·(w_i^T·w̃_j + b_i + b̃_j - log X_ij)

更新:
  w_i ← w_i - η · ∂J/∂w_i
  w̃_j ← w̃_j - η · ∂J/∂w̃_j
  b_i ← b_i - η · ∂J/∂b_i
  b̃_j ← b̃_j - η · ∂J/∂b̃_j

优化技巧:
────────

1. AdaGrad 自适应学习率
   η_t = η_0 / sqrt(Σ g_t²)

2. 批量采样
   不需要遍历所有 (i,j) 对
   只采样 X_ij > 0 的对

3. 并行化
   可以并行计算不同词对的梯度

4. 初始化
   随机初始化: w ~ U(-0.5/d, 0.5/d)
   b = 0
```

---

## 💻 完整实现

### GloVe 训练 (Python)

```python
import numpy as np
from scipy.sparse import lil_matrix
from collections import Counter, defaultdict
from tqdm import tqdm

class GloVe:
    """
    GloVe: Global Vectors for Word Representation
    """
    def __init__(self, vocab_size, embedding_dim, x_max=100, alpha=0.75,
                 learning_rate=0.05, max_iter=100):
        """
        参数:
            vocab_size: 词汇表大小
            embedding_dim: 嵌入维度
            x_max: 权重函数的截断值
            alpha: 权重函数的指数
            learning_rate: 学习率
            max_iter: 最大迭代次数
        """
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.x_max = x_max
        self.alpha = alpha
        self.lr = learning_rate
        self.max_iter = max_iter

        # 初始化参数
        # 中心词向量
        self.W = np.random.uniform(
            -0.5/embedding_dim, 0.5/embedding_dim,
            (vocab_size, embedding_dim)
        )
        # 上下文词向量
        self.W_tilde = np.random.uniform(
            -0.5/embedding_dim, 0.5/embedding_dim,
            (vocab_size, embedding_dim)
        )
        # 偏置
        self.b = np.zeros(vocab_size)
        self.b_tilde = np.zeros(vocab_size)

        # AdaGrad 累积梯度
        self.gradsq_W = np.ones((vocab_size, embedding_dim))
        self.gradsq_W_tilde = np.ones((vocab_size, embedding_dim))
        self.gradsq_b = np.ones(vocab_size)
        self.gradsq_b_tilde = np.ones(vocab_size)

    def weight_func(self, x):
        """权重函数 f(x)"""
        if x < self.x_max:
            return (x / self.x_max) ** self.alpha
        else:
            return 1.0

    def build_cooccurrence_matrix(self, corpus, window_size=5):
        """
        构建共现矩阵

        参数:
            corpus: 词索引列表
            window_size: 窗口大小

        返回:
            cooccur: 稀疏共现矩阵
        """
        print("构建共现矩阵...")
        cooccur = defaultdict(float)

        for i, center_word in enumerate(tqdm(corpus)):
            # 上下文窗口
            start = max(0, i - window_size)
            end = min(len(corpus), i + window_size + 1)

            for j in range(start, end):
                if j != i:
                    context_word = corpus[j]
                    distance = abs(i - j)
                    # 距离加权 (可选)
                    weight = 1.0 / distance
                    cooccur[(center_word, context_word)] += weight

        # 转为稀疏矩阵格式
        print(f"共现对数量: {len(cooccur)}")
        return cooccur

    def train(self, cooccur_matrix):
        """
        训练 GloVe

        参数:
            cooccur_matrix: 共现矩阵 {(i,j): X_ij}
        """
        # 提取非零项
        data = [(i, j, x) for (i, j), x in cooccur_matrix.items() if x > 0]
        num_pairs = len(data)
        print(f"训练 GloVe on {num_pairs} 共现对")

        for iteration in range(self.max_iter):
            total_cost = 0.0

            # 随机打乱
            np.random.shuffle(data)

            for i, j, x_ij in tqdm(data, desc=f"Iter {iteration+1}"):
                # 权重
                weight = self.weight_func(x_ij)

                # 预测
                diff = (np.dot(self.W[i], self.W_tilde[j]) +
                       self.b[i] + self.b_tilde[j] - np.log(x_ij))

                # 损失
                cost = weight * diff ** 2
                total_cost += cost

                # 梯度
                grad_factor = 2 * weight * diff

                # 更新 W[i] (AdaGrad)
                grad_W = grad_factor * self.W_tilde[j]
                self.gradsq_W[i] += grad_W ** 2
                self.W[i] -= (self.lr / np.sqrt(self.gradsq_W[i])) * grad_W

                # 更新 W_tilde[j]
                grad_W_tilde = grad_factor * self.W[i]
                self.gradsq_W_tilde[j] += grad_W_tilde ** 2
                self.W_tilde[j] -= (self.lr / np.sqrt(self.gradsq_W_tilde[j])) * grad_W_tilde

                # 更新 b[i]
                grad_b = grad_factor
                self.gradsq_b[i] += grad_b ** 2
                self.b[i] -= (self.lr / np.sqrt(self.gradsq_b[i])) * grad_b

                # 更新 b_tilde[j]
                grad_b_tilde = grad_factor
                self.gradsq_b_tilde[j] += grad_b_tilde ** 2
                self.b_tilde[j] -= (self.lr / np.sqrt(self.gradsq_b_tilde[j])) * grad_b_tilde

            avg_cost = total_cost / num_pairs
            print(f"Iteration {iteration+1}/{self.max_iter}, Cost: {avg_cost:.4f}")

        print("训练完成!")

    def get_embeddings(self):
        """获取最终词向量 (平均两个矩阵)"""
        return (self.W + self.W_tilde) / 2

    def most_similar(self, word_idx, embeddings, top_k=5):
        """查找最相似的词"""
        query = embeddings[word_idx]

        # 计算余弦相似度
        similarities = []
        for idx in range(self.vocab_size):
            if idx == word_idx:
                continue

            vec = embeddings[idx]
            cos_sim = np.dot(query, vec) / (
                np.linalg.norm(query) * np.linalg.norm(vec) + 1e-10
            )
            similarities.append((idx, cos_sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# ═══════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    from collections import Counter

    # 示例语料
    corpus_text = """
    the quick brown fox jumps over the lazy dog
    the dog runs fast in the park
    the cat sits on the mat
    the brown cat and the black dog play together
    neural networks learn from data
    deep learning is a subset of machine learning
    word embeddings capture semantic meaning
    """.lower().split()

    # 构建词汇表
    word_counts = Counter(corpus_text)
    vocab = {word: idx for idx, word in enumerate(word_counts.keys())}
    idx2word = {idx: word for word, idx in vocab.items()}
    vocab_size = len(vocab)

    # 转换为索引
    corpus_indices = [vocab[word] for word in corpus_text]

    print("=" * 60)
    print("GloVe 训练示例")
    print("=" * 60)
    print(f"词汇表大小: {vocab_size}")
    print(f"语料长度: {len(corpus_indices)}")
    print()

    # 创建模型
    model = GloVe(
        vocab_size=vocab_size,
        embedding_dim=50,
        x_max=100,
        alpha=0.75,
        learning_rate=0.05,
        max_iter=50
    )

    # 构建共现矩阵
    cooccur = model.build_cooccurrence_matrix(corpus_indices, window_size=5)

    # 训练
    model.train(cooccur)

    # 获取词向量
    embeddings = model.get_embeddings()

    # 测试
    print("\n" + "=" * 60)
    print("词相似度测试")
    print("=" * 60)

    test_words = ['dog', 'cat', 'learning']
    for word in test_words:
        if word in vocab:
            word_idx = vocab[word]
            print(f"\n与 '{word}' 最相似的词:")
            similar = model.most_similar(word_idx, embeddings, top_k=3)
            for idx, sim in similar:
                print(f"  {idx2word[idx]:15s}: {sim:.4f}")
```

---

## 🆚 GloVe vs Word2Vec

### 核心区别

```
对比总结:
════════

┌──────────────────┬──────────────────┬──────────────────┐
│      维度        │    Word2Vec      │      GloVe       │
├──────────────────┼──────────────────┼──────────────────┤
│ 学习方式         │ 在线 (SGD)       │ 批量 (全局优化)  │
│ 统计信息         │ 局部窗口         │ 全局共现矩阵     │
│ 目标函数         │ 隐式 (预测任务)  │ 显式 (矩阵分解)  │
│ 训练流程         │ 逐个样本         │ 预计算 + 批量    │
│ 语料需求         │ >1B 词 (大)      │ 10M-1B (中)      │
│ 训练速度         │ 快 (单步)        │ 中等 (需预计算)  │
│ 内存占用         │ 低               │ 高 (共现矩阵)    │
│ 增量训练         │ 容易             │ 困难             │
│ 可解释性         │ 中等             │ 高 (直接优化)    │
│ 低频词           │ 好 (Skip-gram)   │ 中等             │
│ 高频词           │ 需要子采样       │ 权重饱和         │
└──────────────────┴──────────────────┴──────────────────┘

性能对比:
────────

词相似度 (WordSim-353):
  Word2Vec: 0.65
  GloVe: 0.66
  → 相近

词类比 (Google Analogy):
  Word2Vec: 68%
  GloVe: 70%
  → GloVe 略好

下游任务:
  整体相近，差距 < 2%

结论:
  性能相近，各有优势
```

---

### 何时用哪个？

```
使用 Word2Vec (Skip-gram + 负采样):
═══════════════════════════════════

✅ 大规模语料 (>1B 词)
✅ 追求训练速度
✅ 需要增量训练
✅ 低频词重要
✅ 内存受限

推荐场景:
  - 实时系统
  - 超大语料库
  - 流式数据

使用 GloVe:
═══════════

✅ 中等语料 (10M-1B)
✅ 有预计算资源
✅ 追求可解释性
✅ 词类比任务
✅ 研究分析

推荐场景:
  - 学术研究
  - 可解释性重要
  - 固定语料库

实践建议:
────────

1. 先试 GloVe 预训练模型 (Stanford 提供)
2. 如果不满意，再自己训练 Word2Vec
3. 两者都试试，选效果好的

现成资源:
  GloVe: 多个版本 (50d, 100d, 200d, 300d)
  下载: https://nlp.stanford.edu/projects/glove/
```

---

## 💡 核心要点总结

### GloVe 的五大特点

```
1. 全局统计
   直接建模整个语料的共现信息
   而非局部窗口

2. 显式目标
   w_i · w_j ≈ log X_ij
   可解释性强

3. 加权优化
   f(X_ij) 权重函数
   平衡高频词和低频词

4. 批量训练
   预先计算共现矩阵
   然后批量优化

5. 两个向量
   中心词向量 + 上下文向量
   最终平均
```

---

### 关键公式

```
共现矩阵:
  X_ij = 词 i 和 j 的共现次数

目标函数:
  J = Σ_{i,j} f(X_ij) · (w_i^T·w̃_j + b_i + b̃_j - log X_ij)²

权重函数:
  f(x) = (x/x_max)^α  if x < x_max
         1             otherwise

最终词向量:
  v_i = (w_i + w̃_i) / 2
```

---

## 🔗 与其他概念的关系

```
词嵌入演进:
═══════════

LSA/SVD (1990s)
  └─ 矩阵分解 (SVD)
     └─ 全局统计

Word2Vec (2013)
  └─ 神经网络
     └─ 局部窗口，在线学习

GloVe (2014) ← 你在这里
  └─ 结合两者优势
     ├─ 全局统计 (like LSA)
     └─ 神经优化 (like Word2Vec)

FastText (2016)
  └─ Word2Vec + 子词信息

BERT (2018)
  └─ 上下文相关嵌入

知识图谱:
════════

Word2Vec (03/17) ✅
       ↓
GloVe (03/18) ← 你在这里
   ├─ 全局共现统计
   ├─ 显式目标函数
   └─ 矩阵分解视角
       ↓
FastText (03/19)
       ↓
词嵌入应用 (03/20)
```

---

## 🤔 思考题

1. [ ] 为什么 GloVe 要用 log(X_ij) 而不是直接用 X_ij？

2. [ ] 权重函数 f(x) 为什么要设置上界 x_max？

3. [ ] 为什么 GloVe 需要两个词向量矩阵 (W 和 W̃)？

4. [ ] GloVe 和 PMI (Pointwise Mutual Information) 有什么关系？

5. [ ] 如果词汇表很大（1M 词），共现矩阵的存储和计算会有什么问题？

6. [ ] 为什么 Word2Vec 适合大语料，GloVe 适合中等语料？

7. [ ] 能否结合 Word2Vec 和 GloVe 的优点？

---

## 🚀 下一步

```
当前: 18_GloVe ✅
       ↓
建议路径:
       ├─ 19_FastText (子词信息)
       ├─ 20_情感分类 (词嵌入应用)
       └─ 21_词嵌入去偏 (公平性)

或者:
       └─ 跳到 Seq2Seq 与 Attention ⭐⭐⭐⭐⭐
```

---

**记住 GloVe 的核心**:
- 全局统计 vs 局部窗口 🌐
- 显式优化 vs 隐式学习 📐
- 批量训练 vs 在线学习 📊
- 与 Word2Vec 互补，非竞争 🤝

**实践建议**:
- 先用预训练的 GloVe (斯坦福提供)
- 如需自训练，中等语料用 GloVe
- 大语料用 Word2Vec

**恭喜你掌握了词嵌入的另一种经典方法！** 🚀

---

**更新日期**: 2025-10-31
**重要性**: 词嵌入的经典方法，与 Word2Vec 齐名
**与 DeepSeek-V3**: GloVe → BERT → Transformer → 大模型
**核心价值**: 理解全局统计的力量，对比在线学习
**下一步**: 词嵌入应用（情感分类）或 Seq2Seq
