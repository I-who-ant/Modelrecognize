# BLEU 评分 - 机器翻译质量评估

**学习日期**: 2025-10-31
**课程来源**: 深度学习序列模型系列 - BLEU 评分
**重要程度**: 🔴必学 ⭐⭐⭐⭐⭐
**前置知识**: 机器翻译、Seq2Seq
**模块地位**: 机器翻译和文本生成的标准评估指标
**论文**: "BLEU: a Method for Automatic Evaluation of Machine Translation" (Papineni et al., 2002)

---

## 📌 基本定义

**BLEU (Bilingual Evaluation Understudy)** 是一种自动评估机器翻译质量的指标，通过比较模型输出与人类参考翻译的 n-gram 重叠度来打分。

### 为什么需要 BLEU？

```
机器翻译评估的挑战:
═══════════════════

人工评估:
  ✅ 准确
  ❌ 慢 (每个样本需要 5-10 分钟)
  ❌ 贵 (专业翻译人员)
  ❌ 主观 (不同评审标准不一)
  ❌ 不可重复 (无法大规模使用)

需要自动评估:
  ✅ 快速 (毫秒级)
  ✅ 便宜 (计算成本)
  ✅ 客观 (相同输入相同输出)
  ✅ 可重复 (便于比较系统)

示例:
════

输入: "The cat is on the mat"

参考翻译1: "猫在垫子上"
参考翻译2: "那只猫在垫子上"

模型输出: "猫在垫子上面"

问题: 如何自动评分?

BLEU 的答案:
  计算 n-gram 匹配程度
```

---

## 🎯 核心思想

### N-gram 精度 (Precision)

```
基本想法:
════════

一个好的翻译应该包含:
  ✅ 参考翻译中的词
  ✅ 参考翻译中的短语

测量方法:
  计算模型输出中有多少 n-gram 出现在参考中

N-gram 定义:
═══════════

Unigram (1-gram): 单个词
  "猫", "在", "垫子", "上"

Bigram (2-gram): 两个连续词
  "猫 在", "在 垫子", "垫子 上"

Trigram (3-gram): 三个连续词
  "猫 在 垫子", "在 垫子 上"

4-gram: 四个连续词
  "猫 在 垫子 上"

示例:
════

候选翻译: "the the the the"
参考翻译: "the cat is on the mat"

Unigram 精度:
  候选中的 unigram: ["the", "the", "the", "the"]
  有多少在参考中? 全部!
  精度 = 4/4 = 100% ← 不合理!

问题:
  简单计数会被重复词"欺骗"

解决:
  限制每个 n-gram 的匹配次数
  最多不超过在参考中出现的次数
```

---

### 修正的 N-gram 精度

```
核心公式:
════════

Clipped Precision:
  p_n = Σ_{n-gram∈候选} Count_clip(n-gram) / Σ_{n-gram∈候选} Count(n-gram)w

其中:
  Count_clip(n-gram) = min(Count(n-gram), Max_Ref_Count(n-gram))

  Count(n-gram): n-gram 在候选中出现的次数
  Max_Ref_Count(n-gram): n-gram 在所有参考中的最大出现次数

详细示例:
════════

候选: "the the the the"
参考: "the cat is on the mat"

1-gram "the":
  候选中出现: 4 次
  参考中最多: 2 次 (一个在开头,一个在 "on the")
  Count_clip("the") = min(4, 2) = 2

总 1-gram 数: 4

Clipped 1-gram 精度:
  p_1 = 2 / 4 = 0.5 = 50% ✅ 合理!

更复杂的示例:
═══════════

候选: "猫 在 垫子 上面"
参考: "猫 在 垫子 上"

1-gram:
  "猫": Count_clip = min(1, 1) = 1
  "在": Count_clip = min(1, 1) = 1
  "垫子": Count_clip = min(1, 1) = 1
  "上面": Count_clip = min(1, 0) = 0  ← 不在参考中
  总 1-gram: 4
  p_1 = (1+1+1+0) / 4 = 3/4 = 0.75

2-gram:
  "猫 在": Count_clip = min(1, 1) = 1
  "在 垫子": Count_clip = min(1, 1) = 1
  "垫子 上面": Count_clip = min(1, 0) = 0  ← 不在参考中
  总 2-gram: 3
  p_2 = (1+1+0) / 3 = 2/3 ≈ 0.67

3-gram:
  "猫 在 垫子": Count_clip = min(1, 1) = 1
  "在 垫子 上面": Count_clip = min(1, 0) = 0
  总 3-gram: 2
  p_3 = 1/2 = 0.5

4-gram:
  "猫 在 垫子 上面": Count_clip = min(1, 0) = 0
  总 4-gram: 1
  p_4 = 0/1 = 0.0
```

---

## 🧮 完整 BLEU 公式

### BLEU-N 分数

```
BLEU-N 定义:
═══════════

BLEU-N = BP × exp(Σ_{n=1}^N w_n · log p_n)

其中:
  N: 最大 n-gram 长度 (通常 N=4)
  p_n: n-gram 的 Clipped Precision
  w_n: 权重 (通常均等: w_n = 1/N)
  BP: Brevity Penalty (长度惩罚)

展开形式:
  BLEU-4 = BP × (p_1 · p_2 · p_3 · p_4)^(1/4)
         = BP × 4√(p_1 · p_2 · p_3 · p_4)

为什么用几何平均?
───────────────

算术平均 vs 几何平均:

算术平均:
  (p_1 + p_2 + p_3 + p_4) / 4

问题:
  如果 p_4 = 0 (没有 4-gram 匹配)
  算术平均仍然可能很高
  (0.8 + 0.7 + 0.6 + 0.0) / 4 = 0.525

几何平均:
  4√(p_1 · p_2 · p_3 · p_4)

优势:
  如果任何一个 p_n = 0
  整个 BLEU = 0
  4√(0.8 × 0.7 × 0.6 × 0.0) = 0

  更严格! 需要所有 n-gram 都匹配

示例对比:
────────

翻译A:
  p_1=0.9, p_2=0.8, p_3=0.7, p_4=0.6
  几何平均 = 4√(0.9×0.8×0.7×0.6) ≈ 0.74

翻译B:
  p_1=0.9, p_2=0.8, p_3=0.1, p_4=0.0
  几何平均 = 4√(0.9×0.8×0.1×0.0) = 0

翻译A 更好! ✅
```

---

### 长度惩罚 (Brevity Penalty)

```
问题:
════

短翻译容易获得高精度!

示例:
  候选: "猫"
  参考: "猫 在 垫子 上"

  1-gram 精度 = 1/1 = 100% ← 不合理!

短翻译会被错误地高估

解决:
════

Brevity Penalty (BP):
  如果候选比参考短,给予惩罚

公式:
  BP = 1                     if c > r
       exp(1 - r/c)          if c ≤ r

其中:
  c: 候选翻译的长度
  r: 最接近的参考翻译的长度

解释:
  c > r: 候选比参考长,不惩罚 (BP = 1)
  c = r: 长度相同,不惩罚 (BP = 1)
  c < r: 候选比参考短,惩罚 (BP < 1)

示例:
════

示例1: 候选过短
  候选长度 c = 1
  参考长度 r = 4
  BP = exp(1 - 4/1) = exp(-3) ≈ 0.05
  → 严重惩罚! ✅

示例2: 候选稍短
  候选长度 c = 3
  参考长度 r = 4
  BP = exp(1 - 4/3) = exp(-0.33) ≈ 0.72
  → 中等惩罚

示例3: 候选长度合适
  候选长度 c = 4
  参考长度 r = 4
  BP = 1 (因为 c = r)
  → 不惩罚 ✅

示例4: 候选过长
  候选长度 c = 6
  参考长度 r = 4
  BP = 1 (因为 c > r)
  → 不惩罚 (精度已经会自然降低)

多个参考翻译:
═══════════

选择长度最接近候选的参考:
  r = argmin_{ref} |length(候选) - length(ref)|

示例:
  候选长度: 5
  参考1长度: 4
  参考2长度: 7
  选择参考1 (因为 |5-4| < |5-7|)
  r = 4
```

---

## 💻 完整实现

### Python 实现

```python
import numpy as np
from collections import Counter
from typing import List

def get_ngrams(tokens: List[str], n: int) -> Counter:
    """
    提取 n-gram

    参数:
        tokens: 词列表
        n: n-gram 的 n

    返回:
        Counter: n-gram 计数
    """
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i+n])
        ngrams.append(ngram)
    return Counter(ngrams)


def clipped_precision(candidate: List[str],
                     references: List[List[str]],
                     n: int) -> float:
    """
    计算 Clipped n-gram Precision

    参数:
        candidate: 候选翻译 (词列表)
        references: 参考翻译列表 (每个是词列表)
        n: n-gram 的 n

    返回:
        precision: Clipped Precision
    """
    # 提取候选的 n-gram
    candidate_ngrams = get_ngrams(candidate, n)

    if not candidate_ngrams:
        return 0.0

    # 对每个 n-gram,找到在所有参考中的最大出现次数
    max_ref_counts = Counter()
    for reference in references:
        ref_ngrams = get_ngrams(reference, n)
        for ngram in candidate_ngrams:
            max_ref_counts[ngram] = max(
                max_ref_counts[ngram],
                ref_ngrams[ngram]
            )

    # 计算 Clipped Count
    clipped_counts = {
        ngram: min(count, max_ref_counts[ngram])
        for ngram, count in candidate_ngrams.items()
    }

    # Clipped Precision
    numerator = sum(clipped_counts.values())
    denominator = sum(candidate_ngrams.values())

    if denominator == 0:
        return 0.0

    return numerator / denominator


def brevity_penalty(candidate_length: int,
                   reference_lengths: List[int]) -> float:
    """
    计算长度惩罚 (Brevity Penalty)

    参数:
        candidate_length: 候选翻译长度
        reference_lengths: 所有参考翻译的长度

    返回:
        BP: Brevity Penalty
    """
    # 选择最接近的参考长度
    closest_ref_length = min(
        reference_lengths,
        key=lambda ref_len: abs(ref_len - candidate_length)
    )

    # 计算 BP
    if candidate_length >= closest_ref_length:
        return 1.0
    else:
        return np.exp(1 - closest_ref_length / candidate_length)


def compute_bleu(candidate: List[str],
                references: List[List[str]],
                max_n: int = 4,
                weights: List[float] = None) -> float:
    """
    计算 BLEU 分数

    参数:
        candidate: 候选翻译 (词列表)
        references: 参考翻译列表 (每个是词列表)
        max_n: 最大 n-gram (通常是 4)
        weights: 各 n-gram 的权重 (默认均等)

    返回:
        bleu_score: BLEU 分数 (0-1 之间)
    """
    if weights is None:
        weights = [1.0 / max_n] * max_n

    # 计算各 n-gram 的 Clipped Precision
    precisions = []
    for n in range(1, max_n + 1):
        p_n = clipped_precision(candidate, references, n)
        precisions.append(p_n)

    # 如果有任何 precision 为 0,BLEU = 0
    if any(p == 0 for p in precisions):
        return 0.0

    # 计算几何平均 (对数域)
    log_precision_sum = sum(
        w * np.log(p) for w, p in zip(weights, precisions)
    )
    geometric_mean = np.exp(log_precision_sum)

    # 计算 Brevity Penalty
    candidate_length = len(candidate)
    reference_lengths = [len(ref) for ref in references]
    bp = brevity_penalty(candidate_length, reference_lengths)

    # BLEU 分数
    bleu_score = bp * geometric_mean

    return bleu_score


# ═══════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════

# 示例1: 完美匹配
candidate = "猫 在 垫子 上".split()
references = [
    "猫 在 垫子 上".split()
]
bleu = compute_bleu(candidate, references)
print(f"示例1 BLEU: {bleu:.4f}")  # 应该接近 1.0

# 示例2: 部分匹配
candidate = "猫 在 垫子 上面".split()
references = [
    "猫 在 垫子 上".split()
]
bleu = compute_bleu(candidate, references)
print(f"示例2 BLEU: {bleu:.4f}")

# 示例3: 多个参考翻译
candidate = "猫 在 垫子 上".split()
references = [
    "猫 在 垫子 上".split(),
    "那只 猫 在 垫子 上".split(),
    "猫 正在 垫子 上".split()
]
bleu = compute_bleu(candidate, references)
print(f"示例3 BLEU: {bleu:.4f}")

# 示例4: 完全不匹配
candidate = "狗 在 椅子 下".split()
references = [
    "猫 在 垫子 上".split()
]
bleu = compute_bleu(candidate, references)
print(f"示例4 BLEU: {bleu:.4f}")  # 应该接近 0.0

# 示例5: 过短的翻译
candidate = "猫".split()
references = [
    "猫 在 垫子 上".split()
]
bleu = compute_bleu(candidate, references)
print(f"示例5 BLEU: {bleu:.4f}")  # 受长度惩罚


# ═══════════════════════════════════════════════════════
# 语料库级 BLEU (Corpus-level BLEU)
# ═══════════════════════════════════════════════════════

def corpus_bleu(candidates: List[List[str]],
               references_list: List[List[List[str]]],
               max_n: int = 4) -> float:
    """
    计算语料库级 BLEU

    参数:
        candidates: 候选翻译列表
        references_list: 参考翻译列表的列表
        max_n: 最大 n-gram

    返回:
        corpus_bleu_score: 语料库级 BLEU
    """
    # 累积所有样本的统计量
    total_clipped_counts = [0] * max_n
    total_counts = [0] * max_n
    total_candidate_length = 0
    total_reference_length = 0

    for candidate, references in zip(candidates, references_list):
        candidate_length = len(candidate)
        reference_lengths = [len(ref) for ref in references]

        # 选择最接近的参考长度
        closest_ref_length = min(
            reference_lengths,
            key=lambda ref_len: abs(ref_len - candidate_length)
        )

        total_candidate_length += candidate_length
        total_reference_length += closest_ref_length

        # 累积 n-gram 统计
        for n in range(1, max_n + 1):
            candidate_ngrams = get_ngrams(candidate, n)

            # 找最大参考计数
            max_ref_counts = Counter()
            for reference in references:
                ref_ngrams = get_ngrams(reference, n)
                for ngram in candidate_ngrams:
                    max_ref_counts[ngram] = max(
                        max_ref_counts[ngram],
                        ref_ngrams[ngram]
                    )

            # Clipped Count
            clipped = sum(
                min(count, max_ref_counts[ngram])
                for ngram, count in candidate_ngrams.items()
            )

            total_clipped_counts[n-1] += clipped
            total_counts[n-1] += sum(candidate_ngrams.values())

    # 计算精度
    precisions = [
        clipped / count if count > 0 else 0
        for clipped, count in zip(total_clipped_counts, total_counts)
    ]

    # 如果有任何 precision 为 0
    if any(p == 0 for p in precisions):
        return 0.0

    # 几何平均
    log_precision_sum = sum(np.log(p) / max_n for p in precisions)
    geometric_mean = np.exp(log_precision_sum)

    # Brevity Penalty
    if total_candidate_length >= total_reference_length:
        bp = 1.0
    else:
        bp = np.exp(1 - total_reference_length / total_candidate_length)

    # Corpus BLEU
    corpus_bleu_score = bp * geometric_mean

    return corpus_bleu_score


# 使用
candidates = [
    "猫 在 垫子 上".split(),
    "狗 在 公园 里".split(),
    "鸟 在 天空 中".split()
]

references_list = [
    ["猫 在 垫子 上".split()],
    ["狗 在 公园 里 玩耍".split()],
    ["鸟 在 天空 中 飞翔".split()]
]

corpus_score = corpus_bleu(candidates, references_list)
print(f"\nCorpus BLEU: {corpus_score:.4f}")
```

---

## 📊 BLEU 分数解读

### 分数范围与含义

```
BLEU 分数范围:
═════════════

范围: 0.0 - 1.0 (通常表示为 0-100)

解读:
────

BLEU < 0.10 (10):
  ❌ 几乎不可用
  示例: 完全随机的翻译

BLEU 0.10-0.20 (10-20):
  ⚠️  质量很低
  示例: 单词级翻译,无语法

BLEU 0.20-0.30 (20-30):
  ⚠️  质量较低
  示例: 能理解大意,但有很多错误

BLEU 0.30-0.40 (30-40):
  ✅ 可接受
  示例: 大部分意思正确,有些语法错误

BLEU 0.40-0.50 (40-50):
  ✅ 良好
  示例: 意思准确,流畅度不错

BLEU 0.50-0.60 (50-60):
  ✅ 优秀
  示例: 接近人类翻译质量

BLEU > 0.60 (60):
  ✅✅ 非常优秀
  示例: 专业级翻译质量

参考数据:
════════

Google 翻译 (2016):
  英→中: BLEU ≈ 42
  中→英: BLEU ≈ 38

人类专业翻译:
  BLEU ≈ 60-70 (相对于其他人类翻译)

注意:
  人类翻译的 BLEU 也不是 100!
  因为翻译有多种正确方式
  不同人的翻译风格不同

现代 NMT 系统 (2024):
  英→中: BLEU ≈ 45-55
  中→英: BLEU ≈ 42-48
```

---

### 不同任务的 BLEU 标准

```
机器翻译:
════════

英→法 (相似语言):
  基线: BLEU 25-30
  良好: BLEU 35-40
  优秀: BLEU 45+

英→中 (差异大):
  基线: BLEU 20-25
  良好: BLEU 30-35
  优秀: BLEU 40+

文本摘要:
════════

抽取式摘要:
  基线: BLEU 30-35
  良好: BLEU 40-45
  优秀: BLEU 50+

生成式摘要:
  基线: BLEU 20-25
  良好: BLEU 30-35
  优秀: BLEU 40+

图像描述:
════════

简单场景:
  基线: BLEU 15-20
  良好: BLEU 25-30
  优秀: BLEU 35+

复杂场景:
  基线: BLEU 10-15
  良好: BLEU 20-25
  优秀: BLEU 30+

对话生成:
════════

(BLEU 不太适用,因为回复多样性)
  基线: BLEU 5-10
  良好: BLEU 15-20

⚠️ 对话更适合用人工评估或其他指标
```

---

## 💡 BLEU 的优势与局限

### 优势

```
1. 自动化 ✅
   不需要人工标注
   秒级计算

2. 客观 ✅
   相同输入,相同输出
   无主观偏见

3. 可重复 ✅
   便于比较不同系统
   标准化评估

4. 相关性好 ✅
   与人类判断高度相关
   (Pearson r ≈ 0.7-0.8)

5. 简单易懂 ✅
   基于 n-gram 匹配
   直观可解释

6. 广泛采用 ✅
   学术界标准
   工业界认可
```

---

### 局限性

```
局限1: 只看 n-gram,不看语义
═══════════════════════════

示例:
  参考: "猫 在 垫子 上"
  候选A: "猫 在 垫子 上"     → BLEU 1.0
  候选B: "猫咪 在 垫子 上"   → BLEU 0.8

  但 "猫" ≈ "猫咪" (语义相同)
  BLEU 无法捕捉!

局限2: 多样性问题
═══════════════

示例:
  输入: "How are you?"
  参考: "你好吗?"

  候选A: "你好吗?"    → BLEU 1.0
  候选B: "你怎么样?"  → BLEU 0.0

  但两者都是正确翻译!
  BLEU 只看 n-gram 重叠

局限3: 对长度敏感
═══════════════

过短的翻译:
  受长度惩罚,BLEU 低

过长的翻译:
  精度自然降低

但有时长度变化是合理的!

局限4: 无法处理句法
═══════════════════

示例:
  参考: "The cat sat on the mat"
  候选: "on the mat the cat sat"

  BLEU 可能相当高
  但语法完全错误!

局限5: 对参考翻译依赖
═══════════════════════

如果参考翻译质量差:
  BLEU 不准确

如果参考翻译只有一个:
  忽略了翻译的多样性

理想: 多个参考翻译 (3-5个)
现实: 通常只有 1 个 (成本高)

局限6: 无法评估流畅度
═══════════════════════

示例:
  候选: "猫 在 的 上 垫子"
  可能有较高的 unigram 匹配
  但完全不流畅!

BLEU 无法明确评估流畅度
```

---

## 🔧 改进与变体

### 改进方法

```
方法1: 使用多个参考翻译
════════════════════════

BLEU 随参考数量提升:
  1 个参考: 基线
  2 个参考: +5-10% BLEU
  4 个参考: +10-15% BLEU

建议: 至少 3-4 个参考

方法2: Smooth BLEU
═══════════════════

问题:
  短句子的高阶 n-gram 可能为 0
  导致 BLEU = 0

解决:
  添加平滑项,避免 0

方法3: BLEU+1 (Lin & Och, 2004)
═══════════════════════════════

为每个 n-gram 计数加 1:
  Count(n-gram) + 1

避免极端的 0 值

方法4: 句子级 BLEU (Sentence BLEU)
═══════════════════════════════════

标准 BLEU 是语料库级
句子级 BLEU 给单个句子打分

用途: 实时反馈,在线评估
```

---

### BLEU 变体与其他指标

```
BLEU 变体:
═════════

NIST:
  加权 n-gram (罕见 n-gram 权重大)
  对信息量的 n-gram 更敏感

METEOR:
  考虑同义词、词干
  使用 WordNet 等资源
  更好的语义匹配

ROUGE:
  常用于摘要评估
  基于 Recall (而非 Precision)

CIDEr:
  图像描述评估
  考虑 TF-IDF 加权

其他现代指标:
═══════════

BERTScore:
  基于 BERT 嵌入的相似度
  捕捉语义
  相关性更高

BLEURT:
  BERT 训练的评估模型
  学习人类评分

COMET:
  神经网络评估模型
  在人工评分数据上训练

对比:
════

┌──────────┬────────┬────────┬────────┬──────────┐
│  指标    │  速度  │ 相关性 │ 语义   │ 资源需求 │
├──────────┼────────┼────────┼────────┼──────────┤
│ BLEU     │ 快     │ 中     │ ❌     │ 低       │
│ METEOR   │ 中     │ 高     │ ✅     │ 中       │
│ BERTScore│ 慢     │ 很高   │ ✅✅   │ 高       │
│ BLEURT   │ 慢     │ 很高   │ ✅✅   │ 很高     │
└──────────┴────────┴────────┴────────┴──────────┘

建议:
  快速评估: BLEU
  研究: BLEU + METEOR
  最终评估: BERTScore / BLEURT + 人工
```

---

## 🎯 实践建议

### 何时使用 BLEU

```
适用场景:
════════

✅ 机器翻译系统比较
✅ 模型开发过程中的快速评估
✅ 超参数调优
✅ 论文中的标准化评估
✅ 大规模自动评估

不适用场景:
═══════════

❌ 对话生成 (回复多样性大)
❌ 创意写作 (无标准答案)
❌ 风格迁移 (保留语义但改变形式)
❌ 只有单个句子的评估 (不稳定)

最佳实践:
════════

1. 使用多个参考翻译
   至少 2-3 个,理想 4 个

2. 语料库级评估
   不要只看单个句子
   至少 100+ 样本

3. 结合人工评估
   定期人工检查
   建立信心区间

4. 多指标组合
   BLEU + METEOR + 人工
   全面评估质量

5. 注意统计显著性
   BLEU 提升 1-2 分可能无实际意义
   需要统计检验
```

---

### 常见陷阱

```
陷阱1: 过度优化 BLEU
═══════════════════

问题:
  直接优化 BLEU 作为损失函数
  可能导致不自然的翻译

示例:
  模型学会复制参考翻译
  但无法泛化

建议:
  用 BLEU 评估,不用 BLEU 训练
  (除非有特殊理由)

陷阱2: 单一参考
═════════════

问题:
  只有一个参考翻译
  低估了模型性能

示例:
  输入: "Thanks"
  参考: "谢谢"
  候选: "感谢" (也正确!)
  BLEU: 0.0 ❌

建议:
  至少 2-3 个参考

陷阱3: 忽略统计显著性
═══════════════════════

问题:
  BLEU 32.5 vs 32.8
  差异可能只是噪声

建议:
  使用 Bootstrap 重采样
  计算置信区间
  检验显著性

陷阱4: 跨语言比较
═════════════════

问题:
  英→中 BLEU 30
  vs
  英→法 BLEU 35

  无法直接比较!
  (语言对难度不同)

建议:
  只比较同一语言对的系统

陷阱5: 版本不一致
═══════════════════

问题:
  不同 BLEU 实现可能有细微差异
  (tokenization, 平滑等)

建议:
  使用标准实现 (SacreBLEU)
  论文中说明实现细节
```

---

## 💻 工具与库

### SacreBLEU (推荐)

```python
# 安装
# pip install sacrebleu

from sacrebleu import corpus_bleu

# 使用
hypotheses = [
    "猫 在 垫子 上",
    "狗 在 公园 里"
]

references = [[
    "猫 在 垫子 上",
    "狗 在 公园 里 玩耍"
]]

bleu = corpus_bleu(hypotheses, references)
print(f"BLEU: {bleu.score:.2f}")
print(f"详细: {bleu}")

# 输出:
# BLEU: 41.36
# 详细: BLEU = 41.36 58.3/44.4/33.3/25.0 (BP=0.969 ratio=0.970 hyp_len=9 ref_len=10)
#        └─────┘ └──────────────────────┘
#         总分    各 n-gram 精度

# 优势:
# ✅ 标准化实现
# ✅ 可重现
# ✅ 自动处理 tokenization
# ✅ 详细输出
```

---

### NLTK 实现

```python
from nltk.translate.bleu_score import corpus_bleu, sentence_bleu

# 语料库级
hypotheses = [
    ['猫', '在', '垫子', '上'],
    ['狗', '在', '公园', '里']
]

references = [
    [['猫', '在', '垫子', '上']],
    [['狗', '在', '公园', '里', '玩耍']]
]

score = corpus_bleu(references, hypotheses)
print(f"Corpus BLEU: {score:.4f}")

# 句子级
reference = [['猫', '在', '垫子', '上']]
hypothesis = ['猫', '在', '垫子', '上']

score = sentence_bleu(reference, hypothesis)
print(f"Sentence BLEU: {score:.4f}")
```

---

## 🔗 与其他概念的关系

```
序列生成完整流程:
═══════════════

训练模型 (Seq2Seq + Attention)
   ↓
束搜索解码
   ↓
生成翻译
   ↓
BLEU 评分 ← 你在这里
   ↓
   ├─ 分数低 → 误差分析
   │            ├─ 搜索错误 → 优化束搜索
   │            └─ 模型错误 → 改进模型
   │
   └─ 分数高 → 人工验证
                └─ 确认质量

评估指标体系:
═══════════

自动指标:
  ├─ BLEU (n-gram 匹配)
  ├─ METEOR (同义词)
  ├─ ROUGE (召回率)
  ├─ CIDEr (图像描述)
  └─ BERTScore (语义)

人工评估:
  ├─ Adequacy (充分性)
  ├─ Fluency (流畅度)
  └─ Overall Quality (总体质量)

综合使用:
  自动指标 (快速筛选)
     ↓
  人工评估 (最终确认)
```

---

## 💡 核心要点总结

```
1. BLEU 核心思想
   基于 n-gram 匹配
   测量翻译与参考的相似度

2. 关键组件
   ✅ Clipped n-gram Precision
   ✅ 几何平均 (所有 n-gram)
   ✅ Brevity Penalty (长度惩罚)

3. 公式
   BLEU = BP × (p₁ × p₂ × p₃ × p₄)^(1/4)

4. 分数范围
   0.0-1.0 (通常表示为 0-100)
   40+ 良好, 50+ 优秀

5. 优势
   ✅ 快速自动
   ✅ 客观可重复
   ✅ 与人类判断相关

6. 局限
   ❌ 只看 n-gram,不看语义
   ❌ 无法捕捉多样性
   ❌ 依赖参考质量

7. 实践建议
   ✅ 多个参考翻译
   ✅ 语料库级评估
   ✅ 结合人工评估
   ✅ 使用标准工具 (SacreBLEU)
```

---

## 🤔 常见问题

```
Q1: BLEU 40 好还是 50 好？
A1: 50 更好 (分数越高越好)
    差距 10 分是显著提升

Q2: BLEU 能达到 100 吗？
A2: 理论上可以 (完全匹配参考)
    但实践中很少 (翻译有多样性)
    人类翻译通常 60-70

Q3: 为什么我的 BLEU 是负数？
A3: 不可能! BLEU ∈ [0, 1]
    检查实现是否有误

Q4: 句子级 BLEU 可靠吗？
A4: 不太可靠 (方差大)
    建议语料库级 (100+ 样本)

Q5: BLEU 提升多少算显著？
A5: 通常 1-2 分有实际意义
    需要统计检验确认

Q6: 可以用 BLEU 作为损失函数吗？
A6: 不推荐
    BLEU 不可微
    直接优化可能过拟合
```

---

## 🚀 下一步

```
当前: 23_BLEU评分 ✅

你已完成序列生成基础:
  ✅ Seq2Seq 模型
  ✅ 束搜索解码
  ✅ 束搜索误差分析
  ✅ BLEU 评分

下一步关键: Attention 机制 ⭐⭐⭐⭐⭐
       ↓
28_注意力机制原理
   └─ Seq2Seq 的革命性改进
   └─ 通往 Transformer 的关键桥梁
```

---

**记住 BLEU 的核心**:
- N-gram 匹配的几何平均 📊
- 长度惩罚避免短翻译 📏
- 快速但有局限 ⚡
- 结合人工评估最佳 ✅

**实践建议**:
- 使用 SacreBLEU (标准化)
- 多个参考翻译 (3-5 个)
- 语料库级评估 (>100 样本)
- 定期人工验证

**恭喜你掌握了机器翻译的标准评估指标！** 🎉

---

**更新日期**: 2025-10-31
**重要性**: 机器翻译评估的黄金标准
**与 DeepSeek-V3**: BLEU → 自动评估 → 大模型质量保证
**核心价值**: 快速客观评估翻译质量
**下一步**: 注意力机制 - Seq2Seq 的革命性改进 ⭐⭐⭐⭐⭐
