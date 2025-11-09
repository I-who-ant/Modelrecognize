# Day39: 模型参数调优

> **核心内容**: 掌握关键参数的含义和调优策略，优化模型输出质量

---

## 📝 核心参数详解

### 1. Temperature (温度)

**作用**: 控制输出的随机性和创造性

**取值范围**: 0.0 - 2.0

**效果**:
- **0.0-0.3**: 确定性强，输出稳定
  - 适合: 事实问答、代码生成、数据提取
  - 示例: "Python中列表和元组的区别是什么？"

- **0.4-0.7**: 平衡创造性和准确性
  - 适合: 一般对话、内容生成、翻译
  - 示例: "写一篇产品介绍"

- **0.8-1.5**: 高创造性，输出多样
  - 适合: 创意写作、头脑风暴、故事创作
  - 示例: "写一个科幻短篇故事"

- **1.6-2.0**: 极高随机性，可能不连贯
  - 适合: 实验性创作、艺术生成
  - ⚠️ 谨慎使用，可能产生无意义输出

**实例对比**:
```
提示词: "描述一个未来城市"

Temperature = 0.2:
"未来城市是一个高度智能化的都市，拥有自动驾驶交通系统、
垂直农场和清洁能源基础设施。建筑采用可持续材料建造。"
→ 准确、规范、稳定

Temperature = 0.7:
"未来城市如同水晶般闪耀在夜空中。飞行汽车穿梭于摩天大楼之间，
全息广告在空中翩翩起舞。地面的智能道路会根据交通流量自动调整..."
→ 有创意、具体、生动

Temperature = 1.5:
"城市漂浮在云端，由量子网络连接。居民通过意念控制一切，
建筑会根据心情变换颜色。时间在这里是非线性的..."
→ 非常有创意，但可能过于抽象
```

---

### 2. Top-p (Nucleus Sampling / 核采样)

**作用**: 控制候选词的范围，限制概率累积

**取值范围**: 0.0 - 1.0

**原理**:
- 模型按概率从高到低排序候选词
- Top-p=0.9 表示只考虑概率累积达到90%的词

**效果**:
- **0.1-0.5**: 保守，选择高概率词
  - 输出稳定、准确
  - 适合专业内容、技术文档

- **0.6-0.9**: 平衡，允许一定多样性
  - 输出自然、流畅
  - 适合大多数场景

- **0.95-1.0**: 开放，允许低概率词
  - 输出多样、有创意
  - 适合创作性任务

**Top-p vs Temperature**:
```
推荐组合:
- 稳定输出: Temperature=0.2, Top-p=0.5
- 平衡输出: Temperature=0.7, Top-p=0.9
- 创意输出: Temperature=1.0, Top-p=0.95

避免组合:
- Temperature=0.0, Top-p=1.0 (矛盾)
- Temperature=2.0, Top-p=0.1 (浪费高温度)
```

---

### 3. Max Tokens (最大令牌数)

**作用**: 限制输出的最大长度

**设置建议**:
```
简短回答: 50-200 tokens
  └─ 问答、摘要

中等长度: 500-1000 tokens
  └─ 解释、分析

长文本: 2000-4000 tokens
  └─ 文章、报告

代码生成: 1000-2000 tokens
  └─ 完整函数/类
```

**注意事项**:
- 设置过小 → 输出被截断
- 设置过大 → 浪费成本，可能产生冗余

---

### 4. Frequency Penalty (频率惩罚)

**作用**: 减少重复内容的出现

**取值范围**: -2.0 - 2.0

**效果**:
- **0.0**: 无惩罚，允许重复
- **0.1-0.5**: 轻度惩罚，减少明显重复
- **0.6-1.0**: 中度惩罚，避免重复词汇
- **1.0-2.0**: 强惩罚，强制多样性

**使用场景**:
```
需要重复 (0.0):
- 代码生成 (循环、模式)
- 格式化输出

避免重复 (0.5-1.0):
- 创意写作
- 文章生成
- 对话系统
```

---

### 5. Presence Penalty (存在惩罚)

**作用**: 鼓励谈论新话题

**取值范围**: -2.0 - 2.0

**效果**:
- **0.0**: 无惩罚
- **0.5-1.0**: 鼓励探索新主题
- **1.0-2.0**: 强制话题多样性

**Frequency vs Presence**:
```
Frequency Penalty: 词汇级别 (避免同一个词重复)
Presence Penalty: 主题级别 (鼓励新话题)

示例:
- 只用Frequency: 避免"很好很好很好"
- 加上Presence: 从产品特点 → 用户评价 → 使用场景
```

---

## 🎯 场景化参数配置

### 场景1: 事实问答

```json
{
  "temperature": 0.2,
  "top_p": 0.5,
  "max_tokens": 200,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0
}
```
**理由**: 需要准确、稳定、简洁的答案

---

### 场景2: 代码生成

```json
{
  "temperature": 0.3,
  "top_p": 0.7,
  "max_tokens": 1500,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0
}
```
**理由**: 需要准确但允许一定灵活性，不惩罚重复(代码中的循环、模式)

---

### 场景3: 创意写作

```json
{
  "temperature": 0.9,
  "top_p": 0.95,
  "max_tokens": 2000,
  "frequency_penalty": 0.7,
  "presence_penalty": 0.6
}
```
**理由**: 高创造性，避免重复，鼓励多样化表达

---

### 场景4: 客服对话

```json
{
  "temperature": 0.5,
  "top_p": 0.8,
  "max_tokens": 300,
  "frequency_penalty": 0.3,
  "presence_penalty": 0.2
}
```
**理由**: 自然流畅，轻度避免重复，长度适中

---

### 场景5: 头脑风暴

```json
{
  "temperature": 1.2,
  "top_p": 0.95,
  "max_tokens": 1000,
  "frequency_penalty": 1.0,
  "presence_penalty": 1.5
}
```
**理由**: 高度创新，强制话题多样性，产生不同角度的想法

---

## 🧪 参数调优实验

### 实验框架

```python
def experiment_parameters(prompt, configs):
    """测试不同参数配置"""
    results = []

    for config in configs:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=config["temperature"],
            top_p=config["top_p"],
            max_tokens=config["max_tokens"],
            frequency_penalty=config.get("frequency_penalty", 0),
            presence_penalty=config.get("presence_penalty", 0)
        )

        results.append({
            "config": config,
            "output": response.choices[0].message.content
        })

    return results

# 实验配置
configs = [
    {"temperature": 0.2, "top_p": 0.5, "max_tokens": 200},  # 保守
    {"temperature": 0.7, "top_p": 0.9, "max_tokens": 200},  # 平衡
    {"temperature": 1.2, "top_p": 0.95, "max_tokens": 200}, # 创意
]

# 运行实验
results = experiment_parameters("描述AI的未来", configs)

# 对比输出
for i, result in enumerate(results):
    print(f"\n配置{i+1}: {result['config']}")
    print(f"输出: {result['output']}")
```

---

## 💡 调优最佳实践

### 1. 调优流程

```
步骤1: 确定任务类型
  └─ 事实性 vs 创造性

步骤2: 选择基础配置
  └─ 从推荐配置开始

步骤3: 小步调整
  └─ 每次只改一个参数

步骤4: A/B测试
  └─ 对比不同配置的输出

步骤5: 记录最佳实践
  └─ 建立参数配置库
```

### 2. 常见问题与解决

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 输出不稳定 | Temperature过高 | 降低到0.3-0.5 |
| 内容重复 | Frequency Penalty太低 | 提高到0.5-0.8 |
| 输出被截断 | Max Tokens太小 | 增加到合适长度 |
| 创意不足 | Temperature太低 | 提高到0.8-1.2 |
| 话题单一 | Presence Penalty太低 | 提高到0.5-1.0 |

---

## 📊 参数速查表

| 场景 | Temperature | Top-p | Max Tokens | Freq Penalty | Pres Penalty |
|------|-------------|-------|------------|--------------|--------------|
| **事实问答** | 0.2 | 0.5 | 200 | 0.0 | 0.0 |
| **代码生成** | 0.3 | 0.7 | 1500 | 0.0 | 0.0 |
| **技术写作** | 0.4 | 0.8 | 2000 | 0.2 | 0.2 |
| **客服对话** | 0.5 | 0.8 | 300 | 0.3 | 0.2 |
| **内容生成** | 0.7 | 0.9 | 1000 | 0.5 | 0.3 |
| **创意写作** | 0.9 | 0.95 | 2000 | 0.7 | 0.6 |
| **头脑风暴** | 1.2 | 0.95 | 1000 | 1.0 | 1.5 |

---

**关键要点**:
- Temperature控制创造性
- Top-p控制候选范围
- Frequency/Presence控制多样性
- 参数组合大于单一参数

**下一步**: Day40 - 针对性提示词适配
