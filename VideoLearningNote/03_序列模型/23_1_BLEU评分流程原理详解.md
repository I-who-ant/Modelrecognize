# BLEU 评分流程原理详解 - 从编码到评分的完整路径

**学习日期**: 2025-11-01
**课程来源**: 深度学习序列模型系列 - BLEU评分流程
**重要程度**: 🔴必学 ⭐⭐⭐⭐⭐
**前置知识**: [23_BLEU评分](23_BLEU评分.md)
**模块地位**: 理解机器翻译系统的完整评估流程
**核心问题**: BLEU如何从输入文本生成候选翻译并评分？

---

## 📌 整体流程概览

```
BLEU评分完整流程 (端到端)
═══════════════════════

输入文本
   ↓
[编码器: Seq2Seq]
   ↓
上下文向量 c
   ↓
[解码器: RNN/LSTM]
   ↓
候选翻译 ŷ (序列生成)
   ↓
[BLEU评分器]
   ↓
BLEU分数 (0-100)

详细步骤:
═════════

1️⃣ 输入: 源语言句子 (英文)
2️⃣ 编码: 编码器将源序列转为上下文向量
3️⃣ 解码: 解码器基于上下文生成目标序列 (候选翻译)
4️⃣ 评分: BLEU将候选翻译与多个参考翻译对比
5️⃣ 输出: BLEU分数 (0-1 或 0-100)
```

---

## 🔄 详细流程步骤

### 步骤 1: 输入阶段 (Input)

```
源文本输入:
══════════

格式: 自然语言文本

示例:
  Input: "I love you"
  Type: 英文句子
  Length: 3个词

预处理:
  1. 分词 (Tokenization)
     "I love you" → ["I", "love", "you"]

  2. 添加特殊符号
     <SOS> I love you <EOS>
     ↓
     [1, 5, 23, 145, 2]  (词ID)

  3. 转为数值向量
     [1, 5, 23, 145, 2] (batch_size=1)

这就是编码器的输入!
```

---

### 步骤 2: 编码阶段 (Encoding)

```
Seq2Seq 编码器:
═════════════

结构: RNN/LSTM/GRU

输入:
  x = [x₁, x₂, ..., xₙ]  (源序列)
  = [<SOS>, "I", "love", "you", <EOS>]
  = [1, 5, 23, 145, 2]

编码过程:
═════════

时间步 t=1:
  x₁ = <SOS> (ID=1)
  h₁ = RNN(h₀, x₁)  (h₀是零向量)

时间步 t=2:
  x₂ = "I" (ID=5)
  h₂ = RNN(h₁, x₂)

时间步 t=3:
  x₃ = "love" (ID=23)
  h₃ = RNN(h₂, x₃)

时间步 t=4:
  x₄ = "you" (ID=145)
  h₄ = RNN(h₃, x₄)

时间步 t=5:
  x₅ = <EOS> (ID=2)
  h₅ = RNN(h₄, x₅)
  h₅ = c (上下文向量)

输出:
════

最终隐藏状态: c = h₅
  包含了整个源序列的语义信息
  这是解码器的输入!

图示:
════

  输入序列: <SOS> I love you <EOS>
              ↓  ↓  ↓    ↓   ↓
  隐藏状态:   h₁ h₂ h₃  h₄  h₅=c

编码器只负责"理解"源文本
接下来交给解码器"生成"翻译
```

---

### 步骤 3: 解码阶段 (Decoding)

```
Seq2Seq 解码器:
═════════════

结构: RNN/LSTM/GRU + Softmax分类器

输入:
  上下文向量 c = h₅

解码过程:
═════════

时间步 t=1 (第一个词):
  s₀ = 初始化状态 (通常 s₀ = tanh(W·c))
  输入: <SOS> (ID=1)

  解码:
    s₁ = RNN(s₀, <SOS>, c)
    P₁ = softmax(W·[s₁; c])  (词概率分布)
    y₁ = argmax(P₁) = "我"

  候选序列: [<SOS>, "我"]

时间步 t=2 (第二个词):
  输入: y₁ = "我"

  解码:
    s₂ = RNN(s₁, "我", c)
    P₂ = softmax(W·[s₂; c])
    y₂ = argmax(P₂) = "爱"

  候选序列: [<SOS>, "我", "爱"]

时间步 t=3 (第三个词):
  输入: y₂ = "爱"

  解码:
    s₃ = RNN(s₂, "爱", c)
    P₃ = softmax(W·[s₃; c])
    y₃ = argmax(P₃) = "你"

  候选序列: [<SOS>, "我", "爱", "你"]

时间步 t=4 (结束符):
  输入: y₃ = "你"

  解码:
    s₄ = RNN(s₃, "你", c)
    P₄ = softmax(W·[s₄; c])
    y₄ = argmax(P₄) = <EOS>

  候选序列: [<SOS>, "我", "爱", "你", <EOS>]

  到达 <EOS> → 停止生成!

输出:
════

候选翻译: ŷ = "我爱你"
数值表示: [1, 23, 56, 89, 2]

这是解码器"认为"最好的翻译!
接下来BLEU要评估它有多好
```

---

### 步骤 4: 评分阶段 (BLEU Scoring)

```
BLEU 评分器:
═══════════

输入:
  候选翻译: ŷ = "我爱你"
  参考翻译: y₁*, y₂*, y₃* (多个)

示例参考翻译:
  y₁* = "我爱你"
  y₂* = "那只猫在垫子上"
  y₃* = "我真的很爱你"

步骤 4.1: 提取 n-gram
════════════════════

候选: "我爱你" = ["我", "爱", "你"]

Unigram (1-gram):
  ["我", "爱", "你"]

Bigram (2-gram):
  ["我 爱", "爱 你"]

Trigram (3-gram):
  ["我 爱 你"]

4-gram:
  [] (序列长度不足)

步骤 4.2: 计算 Clipped Precision
═══════════════════════════════

对每个 n-gram:
  Count_clip(n-gram) = min(Count(n-gram), Max_Ref_Count(n-gram))

Unigram:
  "我": Count=1, Ref中最多出现: 1 → Clip=1
  "爱": Count=1, Ref中最多出现: 3 → Clip=1
  "你": Count=1, Ref中最多出现: 1 → Clip=1

  p₁ = (1+1+1) / 3 = 1.0 = 100%

Bigram:
  "我 爱": Count=1, Ref中最多出现: 1 → Clip=1
  "爱 你": Count=1, Ref中最多出现: 0 → Clip=0

  p₂ = (1+0) / 2 = 0.5 = 50%

Trigram:
  "我 爱 你": Count=1, Ref中最多出现: 1 → Clip=1

  p₃ = 1/1 = 1.0 = 100%

步骤 4.3: 长度惩罚 (Brevity Penalty)
══════════════════════════════════

候选长度: c = 3
参考长度: r = 选择最接近的 (假设r=3)

BP = 1 (因为 c >= r)

步骤 4.4: 计算几何平均
═══════════════════════

BLEU-3 = BP × (p₁ × p₂ × p₃)^(1/3)
       = 1 × (1.0 × 0.5 × 1.0)^(1/3)
       = 1 × (0.5)^(1/3)
       = 1 × 0.7937
       = 0.7937

BLEU 分数: 79.37 (或 79.37/100)

步骤 4.5: 如果使用 4-gram
═══════════════════════════

p₄ = 0 (没有4-gram)
→ BLEU-4 = 0 (任何 pₙ=0 → 整个分数为0)

实践中常用 BLEU-4 (N=4)
```

---

## 💻 完整流程代码示例

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter

# ═══════════════════════════════════════════════════════
# 步骤1: 输入预处理
# ═══════════════════════════════════════════════════════

def preprocess(text, tokenizer, vocab):
    """文本预处理"""
    # 分词
    tokens = tokenizer(text)
    # 转为词ID
    token_ids = [vocab['<SOS>']] + [vocab[tok] for tok in tokens] + [vocab['<EOS>']]
    return torch.LongTensor(token_ids).unsqueeze(0)

# 输入: "I love you"
src = preprocess("I love you", tokenizer, vocab)
# src: [[1, 5, 23, 145, 2]]

# ═══════════════════════════════════════════════════════
# 步骤2: 编码 (Encoder)
# ═══════════════════════════════════════════════════════

class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size, hidden_size, batch_first=True)

    def forward(self, x):
        # x: [batch_size, seq_len]
        embedded = self.embedding(x)
        # embedded: [batch_size, seq_len, embed_size]

        outputs, (hidden, cell) = self.rnn(embedded)
        # outputs: [batch_size, seq_len, hidden_size]
        # hidden: [1, batch_size, hidden_size]
        # cell: [1, batch_size, hidden_size]

        # 使用最后的隐藏状态作为上下文
        context = hidden[-1]  # [batch_size, hidden_size]

        return context, (hidden, cell)

encoder = Encoder(vocab_size=10000, embed_size=256, hidden_size=512)

# 编码
context, encoder_state = encoder(src)
# context: [1, 512]
# encoder_state: (hidden, cell)

# ═══════════════════════════════════════════════════════
# 步骤3: 解码 (Decoder + Beam Search)
# ═══════════════════════════════════════════════════════

class Decoder(nn.Module):
    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size + hidden_size, hidden_size, batch_first=True)
        self.output_proj = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_token, hidden, cell, context):
        # input_token: [batch_size, 1]
        embedded = self.embedding(input_token)
        # embedded: [batch_size, 1, embed_size]

        # 将上下文向量与嵌入拼接
        context_expanded = context.unsqueeze(1)  # [batch_size, 1, hidden_size]
        rnn_input = torch.cat([embedded, context_expanded], dim=-1)
        # rnn_input: [batch_size, 1, embed_size + hidden_size]

        # RNN 前向传播
        output, (hidden, cell) = self.rnn(rnn_input, (hidden, cell))
        # output: [batch_size, 1, hidden_size]

        # 输出概率
        logits = self.output_proj(output.squeeze(1))
        # logits: [batch_size, vocab_size]

        probs = F.softmax(logits, dim=-1)
        # probs: [batch_size, vocab_size]

        return probs, hidden, cell

decoder = Decoder(vocab_size=10000, embed_size=256, hidden_size=512)

def beam_search_decode(encoder, decoder, src, beam_size=5, max_len=50):
    """束搜索解码"""
    # 编码获取上下文
    context, _ = encoder(src)

    # 初始化候选
    candidates = [(['<SOS>'], 0.0, decoder_state)]

    for t in range(max_len):
        all_candidates = []

        for seq, score, decoder_state in candidates:
            last_word = seq[-1]

            # 如果已经结束,不再扩展
            if last_word == '<EOS>':
                all_candidates.append((seq, score, decoder_state))
                continue

            # 解码一步
            input_token = torch.LongTensor([[vocab[last_word]]])
            probs, new_hidden, new_cell = decoder(input_token, decoder_state[0], decoder_state[1], context)

            # 获取前 beam_size 个词
            top_probs, top_indices = torch.topk(probs, beam_size)

            for prob, word_idx in zip(top_probs[0], top_indices[0]):
                word = idx_to_vocab[word_idx.item()]
                new_seq = seq + [word]
                new_score = score + torch.log(prob)
                new_state = (new_hidden, new_cell)

                all_candidates.append((new_seq, new_score, new_state))

        # 选择前 beam_size 个候选
        all_candidates.sort(key=lambda x: x[1], reverse=True)
        candidates = all_candidates[:beam_size]

        # 早停: 如果所有候选都以 <EOS> 结束
        if all(seq[-1] == '<EOS>' for seq, _, _ in candidates):
            break

    # 返回最佳候选 (去掉 <SOS> 和 <EOS>)
    best_seq = candidates[0][0][1:-1]
    return best_seq

# 解码生成候选翻译
candidate = beam_search_decode(encoder, decoder, src, beam_size=5)
# candidate: ['我', '爱', '你']

# ═══════════════════════════════════════════════════════
# 步骤4: BLEU 评分
# ═══════════════════════════════════════════════════════

def compute_bleu(candidate, references, max_n=4):
    """
    计算BLEU分数

    参数:
        candidate: 候选翻译的词列表
        references: 参考翻译列表的列表 (每个参考是一个词列表)
        max_n: 最大n-gram (通常是4)

    返回:
        bleu_score: BLEU分数 (0-1)
    """
    # 计算各阶n-gram的clipped precision
    precisions = []

    for n in range(1, max_n + 1):
        # 提取候选的n-gram
        candidate_ngrams = get_ngrams(candidate, n)
        if not candidate_ngrams:
            return 0.0  # 如果没有n-gram,直接返回0

        # 对每个n-gram,找到在所有参考中的最大出现次数
        max_ref_counts = Counter()
        for reference in references:
            ref_ngrams = get_ngrams(reference, n)
            for ngram in candidate_ngrams:
                max_ref_counts[ngram] = max(
                    max_ref_counts[ngram],
                    ref_ngrams[ngram]
                )

        # 计算clipped count
        clipped_count = sum(
            min(count, max_ref_counts[ngram])
            for ngram, count in candidate_ngrams.items()
        )

        # 计算precision
        total_count = sum(candidate_ngrams.values())
        precision = clipped_count / total_count if total_count > 0 else 0
        precisions.append(precision)

    # 如果有任何precision为0,返回0
    if any(p == 0 for p in precisions):
        return 0.0

    # 计算几何平均
    log_precision_sum = sum(np.log(p) for p in precisions)
    geometric_mean = np.exp(log_precision_sum / len(precisions))

    # 计算长度惩罚
    candidate_length = len(candidate)
    reference_lengths = [len(ref) for ref in references]
    closest_ref_length = min(
        reference_lengths,
        key=lambda ref_len: abs(ref_len - candidate_length)
    )

    if candidate_length >= closest_ref_length:
        bp = 1.0
    else:
        bp = np.exp(1 - closest_ref_length / candidate_length)

    # BLEU分数
    bleu_score = bp * geometric_mean

    return bleu_score

# 参考翻译 (通常有3-5个)
references = [
    ['我', '爱', '你'],
    ['我', '很', '爱', '你'],
    ['我', '真的', '爱', '你']
]

# 计算BLEU
score = compute_bleu(candidate, references)
print(f"BLEU Score: {score:.4f}")  # 例如: 0.8234

# ═══════════════════════════════════════════════════════
# 完整流程总结
# ═══════════════════════════════════════════════════════

"""
BLEU评分完整流程:

1. 输入预处理
   输入: "I love you"
   → [1, 5, 23, 145, 2]

2. 编码
   → 上下文向量 c = [0.1, -0.2, ..., 0.5] (512维)

3. 解码 (束搜索)
   → 候选翻译: "我爱你" = ['我', '爱', '你']

4. BLEU评分
   → 对比候选与参考
   → 计算 n-gram 匹配
   → 应用长度惩罚
   → 输出: BLEU = 0.8234 (82.34%)

整个过程就是:
  输入文本 → 编码 → 上下文 → 解码 → 候选 → 评分 → BLEU分数
"""
```

---

## 📊 可视化流程图

```
完整BLEU评分流程图
═════════════════

                   ┌──────────────────────┐
                   │   输入源语言文本      │
                   │  "I love you"        │
                   └──────────┬───────────┘
                              ↓
                   ┌──────────────────────┐
                   │   1. 预处理           │
                   │  分词 → 词ID         │
                   │ [1,5,23,145,2]      │
                   └──────────┬───────────┘
                              ↓
                   ┌──────────────────────┐
                   │   2. 编码器 (Encoder) │
                   │      RNN/LSTM         │
                   │   输出上下文向量      │
                   │   c = h₅             │
                   └──────────┬───────────┘
                              ↓
                   ┌──────────────────────┐
                   │   3. 解码器 (Decoder) │
                   │      RNN/LSTM         │
                   │   + 束搜索            │
                   │   生成候选翻译         │
                   │   ŷ = "我爱你"        │
                   └──────────┬───────────┘
                              ↓
                   ┌──────────────────────┐
                   │   4. BLEU 评分器     │
                   │                      │
                   │  a. 提取n-gram       │
                   │  b. Clipped Precision│
                   │  c. 几何平均          │
                   │  d. 长度惩罚          │
                   │  e. 计算分数          │
                   │                      │
                   │   BLEU = 82.34%      │
                   └──────────────────────┘

                   ┌──────────────────────┐
                   │      最终输出         │
                   │   BLEU Score: 82.34  │
                   └──────────────────────┘
```

---

## 🔍 关键概念解释

### 1. 编码-解码如何产生候选翻译

```
编码器的作用:
═════════════

目标: 将源序列的语义信息压缩到向量中

机制:
  1. 逐步读取源序列的每个词
  2. 更新隐藏状态 (保留历史信息)
  3. 最终隐藏状态 = 整个序列的压缩表示

数学表达:
  hₜ = f(hₜ₋₁, xₜ)
  c = hₙ  (n是源序列长度)

结果:
  c 包含了 "I love you" 的完整语义
  解码器利用这个语义生成翻译

解码器的作用:
═════════════

目标: 基于上下文向量生成目标序列

机制:
  1. 初始化隐藏状态 (基于c)
  2. 每步预测最可能的下一个词
  3. 使用束搜索探索多条路径

数学表达:
  s₀ = g(c)
  P(yₜ | y₁,...,yₜ₋₁, c) = softmax(W·sₜ)
  yₜ = argmax P(yₜ | ...)

结果:
  ŷ = "我爱你" (模型认为的最佳翻译)
```

### 2. BLEU如何对候选翻译评分

```
BLEU评分原理:
════════════

核心思想: "好的翻译应该在n-gram层面与参考翻译相似"

评分步骤:
  1. 提取候选的n-gram
  2. 计算每个n-gram在参考中的匹配程度
  3. 对所有n-gram取几何平均
  4. 应用长度惩罚避免偏向短序列

为什么这样做:
  ✅ n-gram匹配能捕捉词汇和短语层面的相似性
  ✅ 多阶n-gram能捕捉不同粒度的信息
  ✅ 几何平均确保所有阶数都需要匹配
  ✅ 长度惩罚避免系统偏向简单翻译

示例解释:
  候选: "我爱你"
  参考: "我爱你"

  匹配分析:
    Unigram: 3/3 = 100% ✓ (所有词都对)
    Bigram: 2/2 = 100% ✓ (短语都对)
    Trigram: 1/1 = 100% ✓ (整个序列都对)

  BLEU: 高分 (因为完全匹配)

  vs

  候选: "我爱你"
  参考: "那只猫在垫子上"

  匹配分析:
    Unigram: 0/3 = 0% ✗ (没有共同词)
    Bigram: 0/2 = 0% ✗
    Trigram: 0/1 = 0% ✗

  BLEU: 0分 (因为完全不匹配)
```

---

## 🎯 实际案例演示

### 案例1: 完美匹配

```
输入: "Thank you"
编码: [1, 34, 78, 2]
上下文: c = [0.2, -0.1, 0.8, ...]
解码: ŷ = "谢谢"
参考: ["谢谢", "感谢", "多谢"]
BLEU: 95.2%
解释: 候选与参考高度相似,n-gram匹配度高
```

### 案例2: 部分匹配

```
输入: "I love you"
编码: [1, 5, 23, 145, 2]
上下文: c = [0.1, -0.2, 0.5, ...]
解码: ŷ = "我喜欢你"
参考: ["我爱你", "我很爱你"]
BLEU: 67.4%
解释: 候选与参考部分匹配 (有共同词,也有差异)
```

### 案例3: 不匹配

```
输入: "Good morning"
编码: [1, 12, 45, 89, 2]
上下文: c = [0.3, -0.4, 0.2, ...]
解码: ŷ = "我爱你"
参考: ["早上好", "早安", "早安好"]
BLEU: 0.0%
解释: 候选与参考完全不匹配,n-gram无重合
```

---

## 💡 核心要点总结

```
1. BLEU评分流程
   输入文本 → 编码 → 上下文 → 解码 → 候选 → BLEU评分

2. 编码器作用
   压缩源序列的语义到上下文向量
   hₜ = f(hₜ₋₁, xₜ)

3. 解码器作用
   基于上下文生成目标序列
   使用束搜索找到最优路径

4. BLEU评分原理
   比较候选与参考的n-gram匹配度
   应用几何平均和长度惩罚

5. 关键优势
   ✅ 自动化评估
   ✅ 与人类判断相关
   ✅ 标准化的机器翻译评估

6. 关键局限
   ❌ 只看n-gram,不看语义
   ❌ 无法处理翻译多样性
   ❌ 依赖参考翻译质量
```

---

## 🤔 常见问题

```
Q1: 为什么要用编码-解码架构？
A1: 能够处理不同长度的输入和输出序列
    编码器"理解"输入,解码器"生成"输出

Q2: 束搜索的作用是什么？
A2: 在巨大的搜索空间中找到概率最大的序列
    避免贪心搜索的局部最优问题

Q3: BLEU分数多少算好？
A3: 因语言对而异
    英→中: 30+可接受, 40+良好, 50+优秀
    英→法: 35+可接受, 45+良好, 55+优秀

Q4: 为什么参考翻译越多越好？
A4: 翻译有多种正确方式
    更多参考能捕捉翻译的多样性
    避免因为参考不全面而低估模型

Q5: BLEU能用于其他任务吗？
A5: 主要用于机器翻译
    也可用于文本摘要、图像描述等生成任务
    但需要调整评估标准
```

---

## 🚀 下一步

```
当前: 23_1_BLEU评分流程原理详解 ✅

你现在已经理解:
  ✅ 从输入到输出的完整流程
  ✅ 编码-解码如何生成候选翻译
  ✅ BLEU如何对候选翻译评分

建议:
  - 查看 23_BLEU评分.md 获取更多实现细节
  - 进入 28_注意力机制原理 学习核心概念 ⭐⭐⭐⭐⭐
  - 理解为什么Attention能替代Seq2Seq
```

---

**记住BLEU流程的核心**:
- 输入 → 编码 → 上下文 → 解码 → 候选 → 评分 📊
- BLEU是端到端翻译系统的质量评估器 🎯
- 连接模型输出与最终性能指标 🔗

**恭喜你掌握了BLEU评分的完整流程！** 🎉

---

**更新日期**: 2025-11-01
**重要性**: 理解机器翻译系统的端到端评估流程
**与DeepSeek-V3**: 评分机制 → 模型性能评估 → 持续改进
**核心价值**: 从技术细节到系统性能的完整视角
**下一步**: 注意力机制 - 现代LLM的核心突破 ⭐⭐⭐⭐⭐
