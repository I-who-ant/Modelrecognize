# Word2Vec - 词嵌入的革命性突破

**学习日期**: 2025-10-31
**课程来源**: 深度学习序列模型系列 - Word2Vec 算法详解
**重要程度**: 🔴必学 ⭐⭐⭐⭐⭐
**前置知识**: 词嵌入基础、嵌入矩阵、神经网络、softmax
**模块地位**: NLP 历史上的里程碑，开启现代词嵌入时代
**论文**: "Efficient Estimation of Word Representations in Vector Space" (Mikolov et al., 2013)

---

## 📌 基本定义

**Word2Vec** 是 Google 于 2013 年提出的高效词嵌入学习算法，通过在大规模语料上训练浅层神经网络，将词映射为低维稠密向量，使得语义相近的词在向量空间中距离接近。

### 核心特点

```
Word2Vec 的三大突破:
═══════════════════════

1. 高效性 🚀
   - 训练速度快 (数十亿词 / 小时)
   - 负采样优化 (避免完整 softmax)
   - 可扩展到超大语料

2. 语义性 🧠
   - 捕捉语义关系
   - 支持向量运算 (king - man + woman ≈ queen)
   - 自动聚类相似词

3. 通用性 🌐
   - 无监督学习 (只需原始文本)
   - 可迁移到各种 NLP 任务
   - 多语言支持

历史意义:
✅ 重新点燃词嵌入研究
✅ 推动神经 NLP 爆发
✅ 奠定预训练范式基础
✅ 影响后续 BERT、GPT 等模型
```

---

## 🎯 问题背景

### 为什么 Word2Vec 是革命性的？

```
2013 年之前的困境:
─────────────────

方法 1: One-Hot 编码
问题:
❌ 维度爆炸 (词汇表 × 1)
❌ 稀疏表示 (99.99% 是 0)
❌ 无语义信息 (所有词等距)

示例:
"cat": [0,0,0,0,1,0,0,...,0]  (10000 维)
"dog": [0,0,1,0,0,0,0,...,0]
"apple": [0,1,0,0,0,0,0,...,0]

余弦相似度:
  cos(cat, dog) = 0  ← 完全不相关？
  cos(cat, apple) = 0  ← 等距？

方法 2: LSA/SVD (1990s)
特点:
✅ 降维
✅ 捕捉共现信息
❌ 计算复杂度高 O(n³)
❌ 难以增量训练
❌ 性能有限

方法 3: 神经语言模型 (2003)
特点:
✅ 学习稠密向量
❌ 训练极慢
❌ 难以扩展

Word2Vec 的突破:
───────────────

✅ 简化任务: 不求完美语言模型，只求词向量
✅ 负采样: 避免完整 softmax
✅ 浅层网络: 只用 2 层
✅ 高效实现: C 语言优化

结果:
速度提升 1000 倍！
质量超越前人！
```

---

## 🧮 核心算法

### 分布式假设 (Distributional Hypothesis)

```
Firth (1957): "You shall know a word by the company it keeps"

直觉:
───

语料: "The cat sits on the mat"

上下文 → 中心词:
["The", "sits", "on"] → "cat"

如果两个词的上下文分布相似 → 它们语义相似

示例:
"cat": [on, the, mat, sits, sleeps, ...]
"dog": [on, the, mat, runs, sleeps, ...]
        ↑   ↑   ↑
      上下文重叠 → 语义相似！

关键洞察:
✅ 语义 = 上下文模式
✅ 上下文预测 = 语义学习
```

---

## 🏗️ 两种架构

### 1. CBOW (Continuous Bag-of-Words)

```
CBOW: 用上下文预测中心词
─────────────────────

输入: 上下文词
输出: 中心词

示例:
语料: "The quick brown fox jumps"
窗口: m = 2

输入: ["The", "quick", "jumps", "over"]
输出: "fox"

网络结构:
──────────

      o_{c-2}   o_{c-1}   o_{c+1}   o_{c+2}
     (quick)   (brown)   (jumps)   (over)
         ↓         ↓         ↓         ↓
      [嵌入矩阵 E: V × d]
         ↓         ↓         ↓         ↓
       e_{c-2}   e_{c-1}   e_{c+1}   e_{c+2}
         └─────────┴─────────┴─────────┘
                        ↓
                  平均池化 → h
                        ↓
            [输出矩阵 W_out: V × d]
                        ↓
                    softmax
                        ↓
                 P(fox | context)

前向传播:
────────

1. 嵌入查找:
   e_i = E · o_i   (i ∈ context)

2. 平均池化:
   h = (1/(2m)) · Σ e_i

3. 预测:
   y = softmax(W_out · h)

4. 损失:
   L = -log P(w_c | context)
     = -log(exp(u_c^T · h) / Σ_w exp(u_w^T · h))

参数:
- 嵌入矩阵 E: [V, d]
- 输出矩阵 W_out: [V, d]
- 总参数: 2Vd

特点:
✅ 训练快 (一次前向传播)
✅ 适合频繁词
❌ 对低频词不敏感
```

---

### 2. Skip-gram (更常用)

```
Skip-gram: 用中心词预测上下文
───────────────────────────

输入: 中心词
输出: 上下文词 (多个)

示例:
语料: "The quick brown fox jumps"
窗口: m = 2

输入: "fox"
输出: ["quick", "brown", "jumps", "over"]

网络结构:
──────────

         w_c (fox)
            ↓
         [嵌入层 E]
            ↓
           e_c
            ↓
       [输出层 W_out]
            ↓
         softmax
            ↓
      ┌─────┼─────┬─────┐
      ↓     ↓     ↓     ↓
  P(quick) P(brown) P(jumps) P(over)

目标函数:
────────

最大化: P(context | w_c) = ∏_{j∈context} P(w_j | w_c)

对数似然:
  log P(context | w_c) = Σ_{j∈context} log P(w_j | w_c)

其中:
  P(w_o | w_c) = exp(u_o^T · v_c) / Σ_{w∈V} exp(u_w^T · v_c)

损失函数:
  L = -Σ_{j=-m}^{m, j≠0} log P(w_{c+j} | w_c)

前向传播:
────────

1. 查找中心词向量:
   v_c = E[word_c]

2. 对每个上下文位置 j:
   score_j = W_out · v_c
   P(w_{c+j} | w_c) = softmax(score_j)

3. 计算损失:
   L = -Σ_j log P(w_{c+j} | w_c)

特点:
✅ 对低频词效果好 (更多训练样本)
✅ 捕捉更多语义信息
❌ 训练稍慢 (多次预测)
```

---

### CBOW vs Skip-gram

```
对比分析:
════════

维度          CBOW                Skip-gram
────────────────────────────────────────────
训练速度      快 (1 次预测)       慢 (2m 次预测)
内存占用      低                  高
低频词        差                  好
语义质量      中等                优秀
适用场景      大语料/高频词       小语料/低频词

为什么 Skip-gram 对低频词好？
────────────────────────

CBOW:
  低频词作为目标 → 训练样本少

Skip-gram:
  低频词作为输入 → 产生多个训练样本 (2m 个)

示例:
低频词 "giraffe" 出现 10 次

CBOW: 10 个训练样本
  [context] → "giraffe"

Skip-gram: 10 × 2m = 40 个训练样本 (m=2)
  "giraffe" → "tall"
  "giraffe" → "animal"
  "giraffe" → "zoo"
  "giraffe" → "neck"
  ...

更多训练 → 更好的向量！

实践选择:
────────

小数据 (<10M 词) + 关注低频词 → Skip-gram
大数据 (>1B 词) + 关注速度 → CBOW
通用场景 → Skip-gram (更常用)
```

---

## ⚡ 负采样 (Negative Sampling)

### 问题：Softmax 的计算瓶颈

```
标准 softmax:
═════════════

P(w_o | w_c) = exp(u_o^T · v_c) / Σ_{w∈V} exp(u_w^T · v_c)
                                    └──────┬──────┘
                                需要遍历整个词汇表!

计算复杂度:
──────────

每个样本: O(|V|)
词汇表大小: |V| = 100,000 ~ 1,000,000
语料大小: 1,000,000,000 词

总计算量: 10^6 × 10^9 = 10^15 次运算！

具体示例:
────────

假设:
- 词汇表: 100,000 词
- 嵌入维度: 300
- 语料: 1B 词
- 窗口: 5

每个训练样本:
1. 向量点积: 300 次乘法 × 100,000 词 = 30M 次
2. 指数运算: 100,000 次
3. 求和: 100,000 次
4. 除法: 1 次

单个样本 ≈ 30M 次运算
总计 = 1B × 10 × 30M = 3 × 10^17 次运算

在现代 GPU (10 TFLOPS) 上:
  3 × 10^17 / 10^13 = 30,000 秒 ≈ 8 小时

每轮训练 8 小时！不可接受！

瓶颈分析:
────────

✅ 前向传播 (嵌入查找): 快
✅ 隐藏层计算: 快
❌ Softmax 归一化: 极慢 ← 瓶颈！

为什么慢？
- 需要遍历整个词汇表
- 指数运算昂贵
- 无法并行化 (需要全局求和)
```

---

### 负采样的解决方案

```
核心思想:
════════

不计算完整 softmax
只区分正样本和少量负样本

正样本: 真实的上下文词对
  ("fox", "jumps") ← 出现在语料中

负样本: 随机采样的不相关词对
  ("fox", "banana") ← 不在上下文中
  ("fox", "computer")
  ("fox", "democracy")

目标:
✅ 正样本: 向量相似 → score 高
❌ 负样本: 向量不相似 → score 低

训练目标变化:
─────────────

原始目标 (Softmax):
  最大化 log P(w_o | w_c)
  = log(exp(u_o^T · v_c) / Σ_w exp(u_w^T · v_c))

负采样目标:
  最大化 log σ(u_o^T · v_c)  [正样本]
  + Σ_{i=1}^k log σ(-u_i^T · v_c)  [负样本]

其中:
- σ: sigmoid 函数
- k: 负样本数量 (5-20)
- u_i: 负样本的向量

直觉解释:
────────

正样本 ("fox", "jumps"):
  希望 u_jumps^T · v_fox → 大
  即 σ(u_jumps^T · v_fox) → 1

负样本 ("fox", "banana"):
  希望 u_banana^T · v_fox → 小
  即 σ(u_banana^T · v_fox) → 0
  等价于 σ(-u_banana^T · v_fox) → 1

优化目标:
  max Π_{正} σ(score)  ×  Π_{负} σ(-score)
  = max Σ_{正} log σ(score)  +  Σ_{负} log σ(-score)

计算复杂度:
──────────

原始: O(|V|) = 100,000
负采样: O(1 + k) = 1 + 5 = 6

速度提升: 100,000 / 6 ≈ 16,000 倍！🚀
```

---

### 负采样的数学推导

```
从概率角度理解:
═══════════════

给定中心词 w_c 和候选词 w:

D = 1: (w_c, w) 是真实词对 (正样本)
D = 0: (w_c, w) 是随机词对 (负样本)

建模:
  P(D=1 | w, w_c) = σ(u_w^T · v_{w_c})

目标: 最大化似然
  L = Π_{正样本} P(D=1 | w, w_c) × Π_{负样本} P(D=0 | w, w_c)

对数似然:
  log L = Σ_{正} log σ(u_w^T · v_{w_c})
        + Σ_{负} log(1 - σ(u_w^T · v_{w_c}))
        = Σ_{正} log σ(u_w^T · v_{w_c})
        + Σ_{负} log σ(-u_w^T · v_{w_c})

这就是负采样的目标函数！

为什么用 sigmoid 而不是 softmax？
─────────────────────────────

Softmax: 多分类
  P(w | context) = exp(score_w) / Σ_{w'} exp(score_{w'})
  需要遍历所有词

Sigmoid: 二分类 (正/负样本)
  P(D=1 | w, context) = σ(score_w)
  只需计算当前词

关键区别:
✅ Sigmoid: 独立的二分类问题
✅ 每个词单独判断 (正/负)
✅ 无需归一化约束

完整算法:
────────

输入: (w_c, w_o) 正样本词对

1. 采样 k 个负样本:
   w_neg_1, w_neg_2, ..., w_neg_k ~ P_n(w)

2. 计算损失:
   L = -log σ(u_o^T · v_c)  [正样本]
       -Σ_{i=1}^k log σ(-u_i^T · v_c)  [负样本]

3. 梯度下降:
   ∂L/∂v_c = -(1 - σ(u_o^T · v_c)) · u_o  [正样本]
            + Σ_i σ(u_i^T · v_c) · u_i  [负样本]

   ∂L/∂u_o = -(1 - σ(u_o^T · v_c)) · v_c
   ∂L/∂u_i = σ(u_i^T · v_c) · v_c

4. 参数更新:
   v_c ← v_c - α · ∂L/∂v_c
   u_o ← u_o - α · ∂L/∂u_o
   u_i ← u_i - α · ∂L/∂u_i

复杂度对比:
──────────

每个训练样本:

Softmax:
  前向: O(|V| × d) ← 瓶颈
  反向: O(|V| × d)
  总计: O(2|V|d) 

负采样:
  前向: O((1+k) × d)
  反向: O((1+k) × d)
  总计: O(2(1+k)d)

实际数字 (V=100K, d=300, k=5):
  Softmax: 2 × 100,000 × 300 = 60M
  负采样: 2 × 6 × 300 = 3,600

速度提升: 60M / 3.6K ≈ 16,000 倍！🚀🚀🚀
```

---

### 负样本分布的选择

```
如何采样负样本？
═══════════════

方法 1: 均匀分布
───────────────

P(w) = 1 / |V|

问题:
❌ 高频词 ("the", "is") 被过度采样
❌ 模型学会区分 "the" 和其他词
❌ 对语义帮助不大

方法 2: 词频分布
───────────────

P(w) ∝ count(w)

问题:
❌ 过度惩罚高频词
❌ 低频词几乎不被采样
❌ 训练不平衡

方法 3: 平滑词频 (Word2Vec 采用)
──────────────────────────────

P(w) ∝ count(w)^{3/4}

原理:
✅ 提升低频词概率
✅ 降低高频词概率
✅ 保持分布的基本形状

数学解释:
────────

词频比:
  count(the) / count(giraffe) = 10,000 / 10 = 1000

均匀分布:
  1 / 1 = 1

原始词频:
  10,000 / 10 = 1000

3/4 次方:
  (10,000)^{3/4} / (10)^{3/4}
  = 1000^{3/4}
  ≈ 178

观察:
原始比例 1000 → 平滑后 178
显著降低了频率差距！

为什么是 3/4？
─────────────

幂次 α 的影响:
- α = 0: 均匀分布
- α = 1: 原始词频
- 0 < α < 1: 平滑效果

实验发现 α = 0.75 (3/4) 效果最好

直觉:
✅ 不太平滑 (α→0): 低频词仍被忽略
✅ 不太极端 (α→1): 高频词主导
✅ 适中 (α=3/4): 平衡两者

实际示例:
────────

     词       频率    均匀    原始    3/4次方
────────────────────────────────────────────
    the      50000   0.0001   0.50    0.178
    is       10000   0.0001   0.10    0.056
    cat       1000   0.0001   0.01    0.010
    giraffe    100   0.0001   0.001   0.003
    rare        10   0.0001   0.0001  0.001

观察:
✅ "the" 的概率从 50% 降到 18%
✅ "giraffe" 的概率从 0.1% 升到 0.3%
✅ 相对差距缩小: 500 倍 → 60 倍
✅ 低频词有了学习机会！

实现代码:
────────

```python
import numpy as np

def build_negative_sampling_table(word_counts, power=0.75, table_size=1e8):
    """
    构建负采样表

    参数:
        word_counts: {word_idx: count} 词频字典
        power: 平滑指数 (通常 0.75)
        table_size: 采样表大小

    返回:
        采样表 (整数数组)
    """
    # 计算平滑后的频率
    pow_freq = np.array([count**power for count in word_counts.values()])
    words_pow = pow_freq / pow_freq.sum()

    # 构建采样表
    # 每个词占用 words_pow[i] × table_size 个位置
    sampling_table = np.zeros(int(table_size), dtype=np.int32)
    word_idx = 0
    word_prob = words_pow[word_idx]

    for i in range(int(table_size)):
        sampling_table[i] = word_idx

        # 超过当前词的份额,切换到下一个词
        if i / table_size > sum(words_pow[:word_idx+1]):
            word_idx += 1

    return sampling_table

def sample_negatives(sampling_table, k):
    """快速采样 k 个负样本"""
    indices = np.random.randint(0, len(sampling_table), size=k)
    return sampling_table[indices]

# 示例使用
word_counts = {'the': 50000, 'is': 10000, 'cat': 1000, 'giraffe': 100}
table = build_negative_sampling_table(word_counts)
neg_samples = sample_negatives(table, k=5)
print(f"负样本: {neg_samples}")
```

效果对比:
────────

原始 softmax:
  每步训练: O(V) = 100,000 次计算
  训练速度: 1000 词/秒

负采样 (k=5):
  每步训练: O(k) = 5 次计算
  训练速度: 16,000,000 词/秒

质量:
  几乎无损失！
  在 word analogy 任务上性能相当

结论:
✅ 极大加速训练
✅ 保持向量质量
✅ 使大规模训练成为可能
```

---

## 🌲 层次 Softmax (Hierarchical Softmax)

### 另一种加速方案：二叉树结构

```
Word2Vec 的两种优化方法:
════════════════════════

方法 1: 层次 Softmax (Hierarchical Softmax)
  - Mikolov 2013 原始论文中的方法
  - 使用二叉树（Huffman 树）表示词汇表
  - 复杂度: O(log V)

方法 2: 负采样 (Negative Sampling)
  - 更简单、更常用
  - 采样少量负样本
  - 复杂度: O(k), k << V

本节重点: 层次 Softmax ← 你说的这个！
```

---

### 核心思想

```
原始 Softmax 问题:
═════════════════

P(w_o | w_c) = exp(u_o^T · v_c) / Σ_{w∈V} exp(u_w^T · v_c)
                                   └──────┬──────┘
                          需要遍历整个词汇表 V = 100,000

复杂度: O(V) - 太慢！

层次 Softmax 解决方案:
═══════════════════════

核心思想:
不直接预测词,而是预测一条从根到叶子的路径

1. 用二叉树表示词汇表
   - 每个词是一个叶子节点
   - V 个词 → V 个叶子

2. 预测变成路径选择
   - 从根节点开始
   - 每个节点做二分类: 左/右
   - log₂(V) 次二分类决策

3. 复杂度降低
   O(V) → O(log V)
   100,000 → 17 ✨

类比理解:
────────

猜词游戏:
  朴素方法: "是 cat 吗?", "是 dog 吗?", ... (10万次)
  二分搜索: "是动物吗?", "是哺乳动物吗?", "是猫科吗?" (17次)

层次 Softmax = 在词汇表上做二分搜索！
```

---

### 二叉树结构

```
Huffman 树构建:
═══════════════

为什么用 Huffman 树?
✅ 高频词路径短 → 训练快
✅ 低频词路径长 → 合理（反正少见）
✅ 平衡树深度和频率

示例词汇表 (词频):
──────────────

the:  50000  ← 高频
is:   10000
cat:  1000
dog:  1000
run:  500
jump: 500
rare: 10    ← 低频

构建步骤:
────────

1. 所有词作为叶子节点,权重=词频

      the(50000)  is(10000)  cat(1000)  dog(1000)  run(500)  jump(500)  rare(10)

2. 重复合并最小的两个节点:

   第一次合并: rare(10) + jump(500) = node1(510)

      the(50000)  is(10000)  cat(1000)  dog(1000)  run(500)  node1(510)
                                                            /    \
                                                         rare   jump

   第二次合并: run(500) + node1(510) = node2(1010)

      the(50000)  is(10000)  cat(1000)  dog(1000)  node2(1010)
                                                    /         \
                                                 run         node1
                                                           /     \
                                                        rare    jump

   ... 继续合并直到根节点

3. 最终的 Huffman 树:

                        root(63020)
                      /              \
                 the(50000)        node_a(13020)
                                  /              \
                             is(10000)         node_b(3020)
                                              /            \
                                        node_c(2000)     node2(1010)
                                        /         \       /         \
                                    cat(1000)  dog(1000) run(500)  node1(510)
                                                                    /     \
                                                                rare(10) jump(500)

路径编码 (左=0, 右=1):
────────────────────

词      路径                深度
─────────────────────────────────
the     [0]                  1    ← 最短
is      [1,0]                2
cat     [1,1,0,0]            4
dog     [1,1,0,1]            4
run     [1,1,1,0]            4
jump    [1,1,1,1,1]          5
rare    [1,1,1,1,0]          5    ← 最长

观察:
✅ 高频词 "the" 只需 1 步
✅ 低频词 "rare" 需要 5 步
✅ 平均深度 ≈ log₂(V)
```

---

### 数学建模

```
二分类概率:
═══════════

在每个内部节点 n,选择方向的概率:

P(left | n) = σ(θ_n^T · v_c)
P(right | n) = 1 - σ(θ_n^T · v_c) = σ(-θ_n^T · v_c)

其中:
- v_c: 中心词的向量
- θ_n: 节点 n 的参数向量
- σ: sigmoid 函数

编码约定:
  左子树 = 0
  右子树 = 1

路径概率:
────────

词 w 的概率 = 沿着路径的所有决策概率之积

P(w | w_c) = ∏_{n ∈ path(w)} P(decision_n | n)

其中 decision_n ∈ {left, right}

数学表达:
────────

设 path(w) = [n₁, n₂, ..., n_L]
设 label_i ∈ {0, 1} 表示在节点 n_i 的方向

P(w | w_c) = ∏_{i=1}^L P(label_i | n_i)

           = ∏_{i=1}^L [P(left|n_i)]^{1-label_i} × [P(right|n_i)]^{label_i}

           = ∏_{i=1}^L [σ(θ_{n_i}^T · v_c)]^{1-label_i} × [σ(-θ_{n_i}^T · v_c)]^{label_i}

统一表达:
────────

定义 direction_i ∈ {-1, +1}:
  direction_i = +1  if label_i = 0 (左)
  direction_i = -1  if label_i = 1 (右)

则:
P(w | w_c) = ∏_{i=1}^L σ(direction_i · θ_{n_i}^T · v_c)

对数似然:
────────

log P(w | w_c) = Σ_{i=1}^L log σ(direction_i · θ_{n_i}^T · v_c)

这就是层次 Softmax 的目标函数！

具体示例:
────────

词 "cat" 的路径: root → 右 → 右 → 左 → 左
编码: [1, 1, 0, 0]
方向: [-1, -1, +1, +1]

P(cat | w_c) = σ(-θ₁^T · v_c)    ← 根节点向右
             × σ(-θ₂^T · v_c)    ← node_a 向右
             × σ(+θ₃^T · v_c)    ← node_b 向左
             × σ(+θ₄^T · v_c)    ← node_c 向左

只需要 4 次计算,而不是 100,000 次！
```

---

### 参数与梯度

```
模型参数:
════════

1. 输入嵌入矩阵 (中心词):
   V_in ∈ ℝ^{V × d}
   v_c = V_in[word_c]

2. 内部节点参数向量:
   θ_n ∈ ℝ^d  (每个内部节点一个)

   总共 V-1 个内部节点
   (二叉树有 V 个叶子 → V-1 个内部节点)

参数总量:
  输入: V × d
  输出: (V-1) × d
  总计: (2V-1) × d

对比:
  标准 Softmax: 2V × d
  层次 Softmax: (2V-1) × d
  参数量几乎相同,但计算快得多！

梯度推导:
════════

损失函数:
L = -log P(w_o | w_c) = -Σ_{n∈path} log σ(dir_n · θ_n^T · v_c)

对中心词向量 v_c 的梯度:
────────────────────

∂L/∂v_c = -Σ_{n∈path} dir_n · (1 - σ(dir_n · θ_n^T · v_c)) · θ_n

       = -Σ_{n∈path} [dir_n - σ(dir_n · θ_n^T · v_c) · dir_n] · θ_n

       = Σ_{n∈path} [σ(dir_n · θ_n^T · v_c) - 1_{dir_n=+1}] · θ_n

其中 1_{dir_n=+1} 是指示函数

对节点参数 θ_n 的梯度:
─────────────────────

∂L/∂θ_n = [σ(dir_n · θ_n^T · v_c) - 1] · dir_n · v_c

更新规则:
────────

v_c ← v_c - α · ∂L/∂v_c

θ_n ← θ_n - α · ∂L/∂θ_n  (对路径上的每个节点)

关键观察:
✅ 只更新路径上的节点 (log V 个)
✅ 其他节点不参与计算
✅ 梯度计算和更新都是 O(log V)
```

---

### 完整算法流程

```
训练一个样本 (w_c, w_o):
═══════════════════════

1. 前向传播
───────────

输入: 中心词 w_c

① 查找中心词向量:
   v_c = V_in[w_c]  ∈ ℝ^d

② 找到目标词 w_o 的路径:
   path(w_o) = [(n₁, dir₁), (n₂, dir₂), ..., (n_L, dir_L)]

   其中 n_i 是节点, dir_i ∈ {-1, +1} 是方向

③ 计算每个节点的输出:
   for (n, dir) in path(w_o):
       score = dir · θ_n^T · v_c
       prob = σ(score)

④ 计算总损失:
   L = -Σ log(prob)

2. 反向传播
───────────

① 初始化梯度:
   grad_v_c = 0

② 对路径上的每个节点:
   for (n, dir) in path(w_o):
       # 计算输出
       score = dir · θ_n^T · v_c
       output = σ(score)

       # 计算梯度
       grad_output = output - 1  # ∂L/∂score
       grad_θ_n = grad_output · dir · v_c
       grad_v_c += grad_output · dir · θ_n

       # 更新节点参数
       θ_n -= α · grad_θ_n

③ 更新中心词向量:
   v_c -= α · grad_v_c

3. 复杂度分析
────────────

每个样本:
- 前向: O(log V × d)
- 反向: O(log V × d)
- 总计: O(log V × d)

对比标准 Softmax:
- 前向: O(V × d)
- 反向: O(V × d)

加速比: V / log V
示例 (V=100,000): 100,000 / 17 ≈ 5,882 倍！
```

---

### Python 实现

```python
import numpy as np
from collections import Counter

class HuffmanNode:
    """Huffman 树节点"""
    def __init__(self, word=None, freq=0):
        self.word = word      # 叶子节点的词
        self.freq = freq      # 频率
        self.left = None
        self.right = None
        self.theta = None     # 内部节点的参数向量

def build_huffman_tree(word_counts):
    """
    构建 Huffman 树

    参数:
        word_counts: {word: count} 词频字典

    返回:
        root: 根节点
        paths: {word: [(node, direction), ...]} 路径字典
    """
    # 创建叶子节点
    nodes = [HuffmanNode(word=word, freq=count)
             for word, count in word_counts.items()]

    # 构建 Huffman 树
    while len(nodes) > 1:
        # 按频率排序
        nodes.sort(key=lambda x: x.freq)

        # 合并最小的两个节点
        left = nodes.pop(0)
        right = nodes.pop(0)

        parent = HuffmanNode(freq=left.freq + right.freq)
        parent.left = left
        parent.right = right

        nodes.append(parent)

    root = nodes[0]

    # 构建路径字典
    paths = {}

    def build_path(node, path, direction):
        """DFS 构建路径"""
        if node.word is not None:  # 叶子节点
            paths[node.word] = list(path)
        else:  # 内部节点
            if node.left:
                build_path(node.left, path + [(node, +1)], 'left')
            if node.right:
                build_path(node.right, path + [(node, -1)], 'right')

    build_path(root, [], 'root')

    return root, paths


def init_tree_params(root, embedding_dim):
    """初始化树的内部节点参数"""
    def init_node(node):
        if node.word is None:  # 内部节点
            node.theta = np.random.randn(embedding_dim) * 0.01
            if node.left:
                init_node(node.left)
            if node.right:
                init_node(node.right)

    init_node(root)


class Word2VecHierarchicalSoftmax:
    """
    Word2Vec with Hierarchical Softmax
    """
    def __init__(self, vocab, word_counts, embedding_dim, learning_rate=0.025):
        self.vocab = vocab  # {word: idx}
        self.idx2word = {idx: word for word, idx in vocab.items()}
        self.vocab_size = len(vocab)
        self.embedding_dim = embedding_dim
        self.lr = learning_rate

        # 初始化输入嵌入
        self.W_in = np.random.randn(self.vocab_size, embedding_dim) * 0.01

        # 构建 Huffman 树
        self.root, self.paths = build_huffman_tree(word_counts)
        init_tree_params(self.root, embedding_dim)

        print(f"Huffman 树构建完成")
        print(f"词汇表大小: {self.vocab_size}")

        # 统计平均路径长度
        avg_path_len = np.mean([len(path) for path in self.paths.values()])
        print(f"平均路径长度: {avg_path_len:.2f}")
        print(f"理论路径长度: {np.log2(self.vocab_size):.2f}")

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def train_pair(self, center_word, target_word):
        """
        训练单个词对

        参数:
            center_word: 中心词
            target_word: 目标词
        """
        if target_word not in self.paths:
            return

        # 中心词向量
        center_idx = self.vocab[center_word]
        v_c = self.W_in[center_idx]

        # 目标词的路径
        path = self.paths[target_word]

        # 前向传播 + 反向传播
        grad_v_c = np.zeros(self.embedding_dim)

        for node, direction in path:
            # 前向
            score = direction * np.dot(node.theta, v_c)
            output = self.sigmoid(score)

            # 梯度
            grad_output = output - 1  # ∂L/∂score

            # 更新节点参数
            node.theta -= self.lr * grad_output * direction * v_c

            # 累积中心词梯度
            grad_v_c += grad_output * direction * node.theta

        # 更新中心词向量
        self.W_in[center_idx] -= self.lr * grad_v_c

    def train(self, corpus, window_size=5, epochs=5):
        """训练模型"""
        print(f"开始训练 (Hierarchical Softmax)")
        print(f"窗口大小: {window_size}")
        print(f"训练轮数: {epochs}")

        for epoch in range(epochs):
            total_pairs = 0

            for i, center_word in enumerate(corpus):
                if center_word not in self.vocab:
                    continue

                # 上下文窗口
                start = max(0, i - window_size)
                end = min(len(corpus), i + window_size + 1)

                for j in range(start, end):
                    if j != i and corpus[j] in self.vocab:
                        self.train_pair(center_word, corpus[j])
                        total_pairs += 1

            print(f"Epoch {epoch+1}/{epochs} - 训练了 {total_pairs} 个词对")

        print("训练完成!")

    def most_similar(self, word, top_k=5):
        """查找最相似的词"""
        if word not in self.vocab:
            return []

        word_idx = self.vocab[word]
        query = self.W_in[word_idx]

        # 计算余弦相似度
        similarities = []
        for idx in range(self.vocab_size):
            if idx == word_idx:
                continue

            vec = self.W_in[idx]
            cos_sim = np.dot(query, vec) / (
                np.linalg.norm(query) * np.linalg.norm(vec) + 1e-10
            )
            similarities.append((self.idx2word[idx], cos_sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# 使用示例
if __name__ == "__main__":
    corpus = """
    the quick brown fox jumps over the lazy dog
    the dog runs fast in the park
    the cat sits on the mat
    """.lower().split()

    # 构建词汇表
    word_counts = Counter(corpus)
    vocab = {word: idx for idx, word in enumerate(word_counts.keys())}

    # 创建模型
    model = Word2VecHierarchicalSoftmax(
        vocab=vocab,
        word_counts=word_counts,
        embedding_dim=50,
        learning_rate=0.025
    )

    # 训练
    model.train(corpus, window_size=2, epochs=20)

    # 测试
    print("\n最相似的词:")
    for word in ['dog', 'cat']:
        print(f"\n'{word}':")
        similar = model.most_similar(word, top_k=3)
        for w, sim in similar:
            print(f"  {w}: {sim:.4f}")
```

---

### 层次 Softmax vs 负采样

```
对比总结:
════════

维度              层次 Softmax           负采样
──────────────────────────────────────────────────
复杂度            O(log V)               O(k)
参数量            (2V-1) × d             2V × d
训练速度          快                     更快
内存占用          中等                   低
实现难度          复杂（需要树）         简单
预训练            需要词频统计           不需要
增量训练          困难（树结构固定）     容易
低频词            效果好                 效果中等
高频词            路径短，训练快         可能过度采样

何时使用层次 Softmax:
───────────────────

✅ 词频分布不均匀（高频词很多）
✅ 追求极致训练速度
✅ 不想调负采样参数
✅ 理论上更严格（近似完整 softmax）

何时使用负采样:
─────────────

✅ 实现简单（更常用）⭐⭐⭐
✅ 更灵活（不依赖树结构）
✅ 支持在线学习
✅ 低频词效果更好
✅ 现代实践推荐

实验结果:
────────

在大多数任务上,两者性能相近
负采样更简单、更灵活 → 更受欢迎
现代 Word2Vec 实现多用负采样

原始论文 (Mikolov 2013):
  首先提出层次 Softmax
  后来引入负采样（更简单）

现代实践:
  gensim 默认: 负采样
  word2vec C 实现: 都支持
  大多数教程: 讲负采样
```

---

### 直观对比

```
三种方法的计算过程:
═══════════════════

任务: 预测词 "cat" 在中心词 "the" 的上下文中出现的概率

方法 1: 标准 Softmax
──────────────────

P(cat | the) = exp(u_cat^T · v_the) / Σ_{w∈V} exp(u_w^T · v_the)
               └────────┬────────┘   └──────────┬──────────┘
                  计算一次               遍历 100,000 词

计算量: 1 + 100,000 = 100,001 次向量点积


方法 2: 层次 Softmax
───────────────────

P(cat | the) = 沿着 Huffman 树的路径
             = σ(+θ₁^T·v) × σ(-θ₂^T·v) × σ(+θ₃^T·v) × ...
               └────┬────┘   └────┬────┘   └────┬────┘
                节点1向左      节点2向右      节点3向左

路径长度 ≈ log₂(100,000) ≈ 17

计算量: 17 次向量点积


方法 3: 负采样
─────────────

不计算 P(cat | the)
而是判断 ("cat", "the") 是否是真实词对

正样本: σ(u_cat^T · v_the)  ← 1 次
负样本: σ(-u_neg₁^T · v_the), ..., σ(-u_neg₅^T · v_the)  ← 5 次

计算量: 1 + 5 = 6 次向量点积


速度对比:
────────

标准 Softmax:  100,001 次  ← 基准
层次 Softmax:       17 次  ← 快 5882 倍
负采样:              6 次  ← 快 16667 倍 🚀

结论:
  负采样最快,但不是精确概率
  层次 Softmax 快且理论严格
  标准 Softmax 不可用（太慢）
```

---

### 关键要点总结

```
层次 Softmax 核心:
═════════════════

1. 二叉树表示词汇表
   ✅ 每个词是叶子
   ✅ Huffman 树优化频率

2. 预测变成路径选择
   ✅ 每个节点二分类
   ✅ log V 次决策

3. 高效训练
   ✅ 复杂度 O(log V)
   ✅ 只更新路径上的节点

4. 理论严格
   ✅ 近似完整 softmax
   ✅ 概率归一化

5. 实践考虑
   ⚠️ 实现复杂
   ⚠️ 树结构固定
   ⚠️ 现代较少使用

推荐:
  理解层次 Softmax 的思想 ✓
  实践中优先用负采样 ✓✓✓
```

---

## 💻 完整实现

### Skip-gram + 负采样 (PyTorch)

```python
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import Counter
from tqdm import tqdm

class Word2VecSkipGram(nn.Module):
    """
    Word2Vec Skip-gram with Negative Sampling
    """
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim

        # 中心词嵌入 (输入)
        self.in_embeddings = nn.Embedding(vocab_size, embedding_dim)
        # 上下文词嵌入 (输出)
        self.out_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # 初始化
        self.in_embeddings.weight.data.uniform_(-0.5/embedding_dim, 0.5/embedding_dim)
        self.out_embeddings.weight.data.zero_()

    def forward(self, center_words, context_words, negative_words):
        """
        前向传播

        参数:
            center_words: [batch_size] 中心词索引
            context_words: [batch_size] 上下文词索引 (正样本)
            negative_words: [batch_size, k] 负样本索引

        返回:
            loss: 标量损失
        """
        batch_size = center_words.size(0)
        k = negative_words.size(1)

        # 中心词向量 [batch_size, embed_dim]
        center_embeds = self.in_embeddings(center_words)

        # 正样本向量 [batch_size, embed_dim]
        pos_embeds = self.out_embeddings(context_words)

        # 负样本向量 [batch_size, k, embed_dim]
        neg_embeds = self.out_embeddings(negative_words)

        # 正样本得分 [batch_size]
        pos_score = (center_embeds * pos_embeds).sum(dim=1)
        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-10)

        # 负样本得分 [batch_size, k]
        neg_score = torch.bmm(neg_embeds, center_embeds.unsqueeze(2)).squeeze(2)
        neg_loss = -torch.log(torch.sigmoid(-neg_score) + 1e-10).sum(dim=1)

        # 总损失
        loss = (pos_loss + neg_loss).mean()

        return loss

    def get_embeddings(self):
        """获取最终的词嵌入"""
        return self.in_embeddings.weight.data.cpu().numpy()


class Word2VecTrainer:
    """Word2Vec 训练器"""

    def __init__(self, corpus, window_size=5, embedding_dim=100,
                 neg_samples=5, min_count=5, learning_rate=0.025):
        """
        参数:
            corpus: 文本列表 (分词后)
            window_size: 上下文窗口大小
            embedding_dim: 嵌入维度
            neg_samples: 负样本数量
            min_count: 最小词频阈值
            learning_rate: 学习率
        """
        self.window_size = window_size
        self.embedding_dim = embedding_dim
        self.neg_samples = neg_samples
        self.learning_rate = learning_rate

        # 构建词汇表
        self.build_vocab(corpus, min_count)

        # 构建负采样表
        self.build_sampling_table()

        # 创建模型
        self.model = Word2VecSkipGram(len(self.vocab), embedding_dim)
        self.optimizer = optim.SGD(self.model.parameters(), lr=learning_rate)

        # 准备训练数据
        self.train_data = self.prepare_training_data(corpus)

    def build_vocab(self, corpus, min_count):
        """构建词汇表"""
        # 统计词频
        word_counts = Counter(corpus)

        # 过滤低频词
        filtered_counts = {w: c for w, c in word_counts.items() if c >= min_count}

        # 按频率排序
        sorted_words = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)

        # 构建映射
        self.vocab = {word: idx for idx, (word, _) in enumerate(sorted_words)}
        self.idx2word = {idx: word for word, idx in self.vocab.items()}
        self.word_counts = {self.vocab[word]: count for word, count in sorted_words}

        print(f"词汇表大小: {len(self.vocab)}")
        print(f"总词数: {sum(self.word_counts.values())}")

    def build_sampling_table(self, power=0.75, table_size=int(1e8)):
        """构建负采样表"""
        # 计算平滑后的概率
        pow_freq = np.array([count**power for count in self.word_counts.values()])
        words_pow = pow_freq / pow_freq.sum()

        # 构建采样表
        self.sampling_table = np.zeros(table_size, dtype=np.int32)
        word_idx = 0
        cumsum = 0

        for i in range(table_size):
            self.sampling_table[i] = word_idx

            if (i + 1) / table_size > cumsum + words_pow[word_idx]:
                cumsum += words_pow[word_idx]
                word_idx = min(word_idx + 1, len(self.vocab) - 1)

    def prepare_training_data(self, corpus):
        """准备训练数据 (中心词-上下文词对)"""
        data = []
        corpus_indices = [self.vocab.get(w) for w in corpus if w in self.vocab]

        for i, center_idx in enumerate(corpus_indices):
            if center_idx is None:
                continue

            # 上下文窗口
            start = max(0, i - self.window_size)
            end = min(len(corpus_indices), i + self.window_size + 1)

            for j in range(start, end):
                if j != i and corpus_indices[j] is not None:
                    data.append((center_idx, corpus_indices[j]))

        print(f"训练样本数: {len(data)}")
        return data

    def sample_negatives(self, batch_size):
        """采样负样本"""
        indices = np.random.randint(0, len(self.sampling_table),
                                   size=(batch_size, self.neg_samples))
        return torch.LongTensor(self.sampling_table[indices])

    def train(self, epochs=5, batch_size=128):
        """训练模型"""
        self.model.train()
        num_batches = len(self.train_data) // batch_size

        for epoch in range(epochs):
            total_loss = 0

            # 打乱数据
            np.random.shuffle(self.train_data)

            # 批次训练
            progress_bar = tqdm(range(num_batches), desc=f"Epoch {epoch+1}/{epochs}")

            for batch_idx in progress_bar:
                # 获取批次数据
                batch_start = batch_idx * batch_size
                batch_end = batch_start + batch_size
                batch = self.train_data[batch_start:batch_end]

                center_words = torch.LongTensor([pair[0] for pair in batch])
                context_words = torch.LongTensor([pair[1] for pair in batch])
                negative_words = self.sample_negatives(len(batch))

                # 前向传播
                loss = self.model(center_words, context_words, negative_words)

                # 反向传播
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()
                progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})

            avg_loss = total_loss / num_batches
            print(f"Epoch {epoch+1} - Average Loss: {avg_loss:.4f}")

        print("训练完成!")

    def most_similar(self, word, top_k=5):
        """查找最相似的词"""
        if word not in self.vocab:
            print(f"词 '{word}' 不在词汇表中")
            return []

        word_idx = self.vocab[word]
        embeddings = self.model.get_embeddings()

        # 查询向量
        query = embeddings[word_idx]

        # 计算余弦相似度
        similarities = []
        for idx in range(len(self.vocab)):
            if idx == word_idx:
                continue

            vec = embeddings[idx]
            cos_sim = np.dot(query, vec) / (np.linalg.norm(query) * np.linalg.norm(vec) + 1e-10)
            similarities.append((self.idx2word[idx], cos_sim))

        # 排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def analogy(self, word_a, word_b, word_c, top_k=1):
        """
        词类比: word_a - word_b + word_c ≈ ?
        例如: king - man + woman ≈ queen
        """
        words = [word_a, word_b, word_c]
        for w in words:
            if w not in self.vocab:
                print(f"词 '{w}' 不在词汇表中")
                return []

        embeddings = self.model.get_embeddings()

        # 向量运算
        vec_a = embeddings[self.vocab[word_a]]
        vec_b = embeddings[self.vocab[word_b]]
        vec_c = embeddings[self.vocab[word_c]]

        target = vec_a - vec_b + vec_c

        # 查找最相似的词
        similarities = []
        exclude = {self.vocab[w] for w in words}

        for idx in range(len(self.vocab)):
            if idx in exclude:
                continue

            vec = embeddings[idx]
            cos_sim = np.dot(target, vec) / (np.linalg.norm(target) * np.linalg.norm(vec) + 1e-10)
            similarities.append((self.idx2word[idx], cos_sim))

        # 排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# ═══════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # 示例语料 (实际应用中应使用大规模语料)
    corpus = """
    the quick brown fox jumps over the lazy dog
    the dog runs fast in the park
    the cat sits on the mat
    the brown cat and the black dog play together
    neural networks learn from data
    deep learning is a subset of machine learning
    word embeddings capture semantic meaning
    context words predict center words in skip-gram
    """.lower().split()

    print("=" * 60)
    print("Word2Vec 训练示例")
    print("=" * 60)

    # 创建训练器
    trainer = Word2VecTrainer(
        corpus=corpus,
        window_size=2,
        embedding_dim=50,
        neg_samples=5,
        min_count=1,
        learning_rate=0.025
    )

    # 训练
    trainer.train(epochs=20, batch_size=32)

    # 测试相似词
    print("\n" + "=" * 60)
    print("词相似度测试")
    print("=" * 60)

    test_words = ['dog', 'cat', 'learning']
    for word in test_words:
        print(f"\n与 '{word}' 最相似的词:")
        similar = trainer.most_similar(word, top_k=3)
        for w, sim in similar:
            print(f"  {w:15s}: {sim:.4f}")

    # 测试词类比 (小语料可能效果不好)
    print("\n" + "=" * 60)
    print("词类比测试")
    print("=" * 60)
    print("\ndog - quick + fast ≈ ?")
    analogy_result = trainer.analogy('dog', 'quick', 'fast', top_k=3)
    for w, sim in analogy_result:
        print(f"  {w:15s}: {sim:.4f}")
```

---

## 🎨 直观理解

### 为什么 Word2Vec 有效？

```
信息论视角:
═══════════

互信息 (Mutual Information):
  I(w_c; w_o) = log P(w_o | w_c) / P(w_o)

Skip-gram 目标:
  max Σ log P(w_o | w_c)
  ≈ max Σ I(w_c; w_o)

含义:
最大化中心词和上下文词的互信息
→ 学习到的向量编码了词之间的关联

矩阵分解视角:
═══════════

Skip-gram with Negative Sampling ≈ 分解 PMI 矩阵

PMI (Pointwise Mutual Information):
  PMI(w, c) = log P(w, c) / (P(w) · P(c))

定理 (Levy & Goldberg, 2014):
  Word2Vec 隐式地在分解 PMI 矩阵的平移版本

数学:
  E[word] · E[context]^T ≈ PMI - log(k)

其中 k 是负样本数

直觉:
✅ Word2Vec 在学习词-上下文的 PMI
✅ 高 PMI → 词和上下文强关联
✅ 向量点积 ≈ PMI

分布式表示视角:
═══════════

传统: 符号表示 (离散)
  "cat" = 符号 #1234

Word2Vec: 分布式表示 (连续)
  "cat" = [0.3, -0.1, 0.8, ..., 0.2]

优势:
✅ 相似词 → 相似向量
✅ 可以插值
✅ 支持向量运算

类比:
符号表示 = 电话号码 (完全独立)
分布式表示 = GPS 坐标 (反映位置关系)
```

---

### 为什么向量运算有效？

```
经典例子:
════════

king - man + woman ≈ queen

为什么？
────────

假设向量空间中存在"性别"维度和"地位"维度:

king = [+王室, +男性]
man = [-王室, +男性]
queen = [+王室, -男性]
woman = [-王室, -男性]

向量运算:
king - man + woman
= [+王室, +男性] - [-王室, +男性] + [-王室, -男性]
= [+王室, 0] + [-王室, -男性]
= [+王室, -男性]
≈ queen ✓

数学解释:
─────────

词向量捕捉语义维度
向量运算 = 语义维度的线性组合

king ≈ man + royalty + male
queen ≈ woman + royalty + female

所以:
king - man + woman
= (man + royalty + male) - man + woman
= royalty + male + woman
≈ royalty + female
≈ queen

实际例子:
────────

国家-首都关系:
  Paris - France + Italy ≈ Rome
  Tokyo - Japan + China ≈ Beijing

时态关系:
  walking - walk + run ≈ running
  swam - swim + run ≈ ran

性别关系:
  uncle - man + woman ≈ aunt
  brother - boy + girl ≈ sister

为什么有时不准确？
───────────────

❌ 多义词: "bank" 可能混合 "河岸" 和 "银行"
❌ 低频词: 训练不充分
❌ 文化偏见: 语料中的偏见被编码
❌ 线性假设: 并非所有语义关系都是线性的

改进方向:
────────

✅ 更大的语料
✅ 上下文相关嵌入 (BERT)
✅ 去偏技术
✅ 非线性建模
```

---

## 📊 评估指标

### 1. 词相似度任务

```
测试集:
─────

WordSim-353: 353 个词对,人工标注相似度 (0-10)
SimLex-999: 999 个词对,区分相似度和关联度

示例:
词对              人工评分   Word2Vec 余弦相似度
────────────────────────────────────────────
(car, automobile)   8.9         0.87
(cat, dog)          7.5         0.76
(money, bank)       8.1         0.43  ← 多义词问题

评估:
计算人工评分和模型相似度的 Spearman 相关系数

Word2Vec 表现:
WordSim-353: ρ ≈ 0.65
SimLex-999: ρ ≈ 0.45
```

---

### 2. 词类比任务

```
Google Analogy Dataset:
───────────────────────

19,544 个类比问题,分为两类:

语义类比 (8,869 个):
- 国家-首都: Athens - Greece + Norway = Oslo
- 城市-州: Chicago - Illinois + California = Los Angeles

句法类比 (10,675 个):
- 时态: run - runs + walk = walks
- 比较级: good - better + bad = worse

评估:
准确率 = 预测正确的类比数 / 总数

Word2Vec 表现:
语义类比: 60-70%
句法类比: 50-65%
总体: 55-68%

影响因素:
✅ 语料大小 (越大越好)
✅ 窗口大小 (大窗口 → 好语义)
✅ 向量维度 (300 维左右最佳)
```

---

### 3. 下游任务性能

```
文本分类:
────────

任务: 情感分类、主题分类
方法: 用 Word2Vec 初始化嵌入层

提升:
平均提升 2-5% 准确率
特别是在小数据集上效果显著

命名实体识别 (NER):
──────────────────

任务: 识别人名、地名、组织名
方法: Word2Vec 作为特征

提升:
F1 分数提升 1-3%

机器翻译:
────────

任务: 源语言 → 目标语言
方法: 用 Word2Vec 初始化编码器/解码器

提升:
BLEU 分数提升 0.5-1.5

结论:
✅ Word2Vec 是通用的特征提取器
✅ 在多个 NLP 任务上有效
✅ 特别适合低资源场景
```

---

## 💡 核心要点总结

### Word2Vec 的五大关键

```
1. 分布式假设
   "You shall know a word by the company it keeps"
   上下文相似 → 语义相似

2. Skip-gram 架构
   中心词 → 预测上下文词
   对低频词效果好

3. 负采样优化
   避免完整 softmax
   速度提升 10,000 倍

4. 语义编码
   向量空间中的语义关系
   支持向量运算 (king - man + woman ≈ queen)

5. 迁移学习
   预训练词向量
   适用于各种下游任务
```

---

### 实践建议

```
数据准备:
────────

✅ 语料大小: 至少 1M 词,最好 100M-1B
✅ 预处理: 小写化、去标点、分词
✅ 低频词: 过滤 count < 5
✅ 领域相关: 语料应匹配应用场景

超参数选择:
──────────

嵌入维度:
- 小数据 (<10M): 50-100
- 中等数据 (10M-100M): 100-300
- 大数据 (>100M): 300-500

窗口大小:
- 句法: 2-5
- 语义: 5-10
- 通用: 5

负样本数:
- 小数据: 5-10
- 大数据: 2-5
- 通用: 5

训练技巧:
────────

1. 学习率:
   初始 0.025,线性衰减到 0.0001

2. 训练轮数:
   小数据: 10-20 epochs
   大数据: 5-10 epochs

3. 子采样:
   对高频词进行子采样 (threshold ≈ 1e-5)

4. 动态窗口:
   随机选择窗口大小 [1, window_size]

5. 监控:
   定期在验证集评估相似度任务

使用建议:
────────

何时使用 Word2Vec:
✅ 静态词向量足够 (词义单一)
✅ 计算资源有限
✅ 需要快速训练
✅ 低资源场景

何时不用 Word2Vec:
❌ 需要上下文相关表示 (多义词)
❌ 有预训练的 BERT 等模型
❌ 子词信息重要 (用 FastText)
```

---

## 🔗 与其他概念的关系

```
词嵌入演进史:
═══════════

2003: Neural Language Model (Bengio et al.)
      └─ 首次提出神经词嵌入

2013: Word2Vec (Mikolov et al.) ← 你在这里
      ├─ Skip-gram
      ├─ CBOW
      └─ 负采样

2014: GloVe (Pennington et al.)
      └─ 全局共现统计

2016: FastText (Bojanowski et al.)
      └─ 子词信息

2018: ELMo (Peters et al.)
      └─ 上下文相关嵌入

2018: BERT (Devlin et al.)
      └─ 双向 Transformer 编码

2019: GPT-2/3 (OpenAI)
      └─ 大规模生成式预训练

知识图谱:
════════

词嵌入学习 (03/16) ✅
       ↓
Word2Vec (03/17) ← 你在这里
   ├─ CBOW
   ├─ Skip-gram
   ├─ 负采样
   └─ 层次 Softmax (可选)
       ↓
GloVe / FastText (03/19)
       ↓
Seq2Seq (03/22)
       ↓
Attention 机制 (03/28) ⭐⭐⭐⭐⭐
       ↓
Transformer (04/)
       ↓
BERT / GPT
       ↓
DeepSeek-V3
```

---

## 🎓 学习建议

### 1. 深入理解原理

```
关键问题:
✅ 为什么预测上下文能学到语义？
✅ 负采样如何近似 softmax？
✅ 为什么向量运算能做类比？
✅ Word2Vec 和矩阵分解的关系？

推荐阅读:
- 原始论文 (Mikolov et al., 2013)
- word2vec Explained (Rong, 2014)
- Neural Word Embedding as Implicit Matrix Factorization (Levy & Goldberg, 2014)
```

---

### 2. 动手实践

```
练习 1: 从头实现
────────────────

1. 实现 Skip-gram 前向传播
2. 实现负采样损失函数
3. 实现梯度计算
4. 在小语料上训练

练习 2: 超参数调优
───────────────────

1. 尝试不同嵌入维度
2. 尝试不同窗口大小
3. 尝试不同负样本数
4. 观察训练曲线

练习 3: 应用实验
───────────────

1. 加载预训练 Word2Vec (Google News)
2. 测试词相似度
3. 测试词类比
4. 可视化词向量 (t-SNE)

练习 4: 下游任务
───────────────

1. 用 Word2Vec 做文本分类
2. 对比 One-Hot vs Word2Vec
3. 对比预训练 vs 随机初始化
```

---

### 3. 工具使用

```
Python 库:
─────────

gensim:
```python
from gensim.models import Word2Vec

# 训练
model = Word2Vec(sentences, vector_size=100, window=5, min_count=5, workers=4)

# 使用
model.wv.most_similar('king', topn=10)
model.wv.similarity('cat', 'dog')
```

PyTorch:
```python
import torch.nn as nn

# 嵌入层
embed = nn.Embedding(vocab_size, embed_dim)
```

预训练模型:
──────────

Google Word2Vec:
- 3M 词汇表
- 300 维
- 1000B 词训练
- 下载: https://code.google.com/archive/p/word2vec/

GloVe:
- 多个版本 (50d, 100d, 200d, 300d)
- Wikipedia + Gigaword
- 下载: https://nlp.stanford.edu/projects/glove/

FastText:
- 294 种语言
- 子词信息
- 下载: https://fasttext.cc/docs/en/crawl-vectors.html
```

---

## ❓ 思考题

1. [ ] 为什么 Skip-gram 比 CBOW 对低频词效果更好？从训练样本数量角度解释。

2. [ ] 负采样的目标函数和标准 softmax 的关系是什么？为什么能近似？

3. [ ] 如果词汇表有 100 万词，窗口大小为 5，负样本数为 10，每个训练样本需要多少次运算？

4. [ ] Word2Vec 能否处理多义词（如 "bank"）？为什么？如何改进？

5. [ ] 词向量的维度越高越好吗？为什么？

6. [ ] 如何评估词嵌入的质量？哪些任务最能反映嵌入的好坏？

7. [ ] Word2Vec 和 PCA 降维有什么本质区别？

8. [ ] 为什么需要两个嵌入矩阵（输入和输出）？能否只用一个？

9. [ ] 如何用 Word2Vec 做情感分析？仅仅用词向量平均够吗？

10. [ ] Word2Vec 的向量运算为什么不是完全准确？哪些因素影响类比的准确性？

---

## 🚀 下一步

```
当前: 17_Word2Vec ✅
       ↓
建议路径 1 (深化词嵌入):
       ├─ 18_负采样详解
       ├─ 19_GloVe 与 FastText
       └─ 20_词嵌入应用实践

建议路径 2 (进入序列模型):
       ├─ 21_Seq2Seq 架构
       ├─ 22_编码器-解码器
       └─ 28_Attention 机制 ⭐⭐⭐⭐⭐

最终目标:
       └─ Transformer
       └─ BERT / GPT
       └─ DeepSeek-V3 🎯
```

---

**记住 Word2Vec 的核心**:
- 通过预测上下文学习语义 🧠
- 负采样实现高效训练 ⚡
- 向量运算捕捉语义关系 🎨
- 开启现代 NLP 的大门 🚪

**恭喜你掌握了 NLP 的基石！准备好探索更多了吗？** 🚀

---

**更新日期**: 2025-10-31
**重要性**: NLP 历史里程碑，必须深入理解 ⭐⭐⭐⭐⭐
**与 DeepSeek-V3**: Word2Vec → BERT → Transformer → 大模型
**核心价值**: 理解词嵌入的本质，为后续学习打下坚实基础
**下一步**: 深化词嵌入理解 或 进入 Seq2Seq 与 Attention
