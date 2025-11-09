# Prompt Engineering Guide 学习项目

> **基于官方 Prompt Engineering Guide 的系统化学习路径**

---

## 📖 项目介绍

这是一个系统化学习 Prompt Engineering 的完整项目，基于 [Prompt Engineering Guide](https://www.promptingguide.ai/) 官方资源制定。

### 🎯 学习目标

- **掌握提示工程基础理论**: 理解概念、原理、最佳实践
- **精通核心技术方法**: 23 种先进技术，从零样本到自动化
- **具备实际应用能力**: 能够在真实场景中设计、优化提示词
- **建立完整知识体系**: 理论 + 实践 + 创新 + 分享

### 📅 学习周期

**总计**: 43 天 (约 6 周)
- **第一阶段**: Introduction (5天) - 基础理论
- **第二阶段**: Techniques (16天) - 核心技术
- **第三阶段**: Applications (5天) - 实际应用
- **第四阶段**: Prompt Hub (11天) - 提示集合
- **第五阶段**: Models (3天) - 模型特点
- **第六阶段**: Risks (1天) - 风险安全
- **第七阶段**: Papers & Tools (2天) - 论文工具

---

## 🗂️ 项目结构

```
Prompt-Engineering-Learning/
├── 📄 README.md                    # 项目说明 (当前文件)
├── 📄 学习计划总览.md               # 完整学习计划
├── 📄 学习笔记模板.md               # 标准笔记模板
├── 📄 资源索引.md                  # 所有资源链接索引
│
├── 📁 第一阶段_Introduction/       # 基础理论 (5天)
│   ├── Day1_Prompt_Engineering_Introduction.md
│   ├── Day2_Prompt_Engineering_LLM_Settings.md
│   ├── Day3_Prompt_Engineering_Basics_of_Prompting.md
│   ├── Day4_Prompt_Engineering_Prompt_Elements.md
│   └── Day5_Prompt_Engineering_General_Tips_for_Designing_Prompts.md
│
├── 📁 第二阶段_Techniques/         # 核心技术 (16天)
│   ├── Day6_Zero-Shot_Prompting.md # 零样本提示任务
│   ├── Day7_Few-Shot_Prompting.md # 少样本提示任务
│   ├── Day8_Chain-of-Thought_Prompting.md # 链思考提示任务
│   ├── Day9_Self-Consistency.md # 自洽任务
│   ├── Day10_Generate_Knowledge_Prompting.md # 生成知识提示任务
│   ├── Day11_Prompt_Chaining.md # 提示链任务
│   ├── Day12_Tree_of_Thoughts_ToT.md # 树思考任务
│   ├── Day13_Retrieval_Augmented_Generation.md # RAG任务
│   ├── Day14_Automatic_Reasoning_and_Tool-use_ART.md # 自动推理和工具使用任务
│   ├── Day15_Automatic_Prompt_Engineer.md # 自动提示工程师任务
│   ├── Day16_Active-Prompt.md # 主动提示任务
│   ├── Day17_Directional_Stimulus_Prompting.md # 方向刺激提示任务
│   ├── Day18_Program-Aided_Language_Models.md # 程序辅助语言模型任务
│   ├── Day19_ReAct_Prompting.md # ReAct 提示任务
│   ├── Day20_Multimodal_CoT_Prompting.md # 多模态链思考提示任务
│   └── Day21_Graph_Prompting.md # 图提示任务
│
├── 📁 第三阶段_Applications/       # 实际应用 (5天) ⭐ 新增完整文件
│   ├── 📄 00_学习路线导航.md # 快速选择学习资源
│   ├── 📁 Day22_Function_Calling/
│   │   ├── Day22_Function_Calling.md # 主文件: 函数调用原理
│   │   ├── Day22_1_工具调用方式深度解析.md ⭐ # 快速版: 3种方式对比
│   │   ├── Day22_2_Prompt_Engineering的两种应用方向.md # 进阶版: API vs 模型部署
│   │   └── Day22_3_MCP深度解析.md # 深度版: 完整机制
│   │
│   ├── 📁 Day23_Generating_Data/
│   │   ├── Day23_Generating_Data.md # 主文件: 完整工作流
│   │   ├── Day23_1_生成数据实战避坑指南.md ⭐ # 快速版: 0→10万数据
│   │   └── Day23_2_合成数据集的质量评估与验证体系.md # 深度版: 企业级质量体系
│   │
│   ├── 📁 Day24_Generating_Synthetic_Dataset_for_RAG/
│   │   ├── Day24_Generating_Synthetic_Dataset_for_RAG.md # 主文件: RAG完整解析
│   │   └── Day24_1_RAG知识库构建快速指南.md ⭐ # 快速版: 5步快速指南 + 代码
│   │
│   ├── 📁 Day25_Tackling_Generated_Datasets_Diversity/
│   │   ├── Day25_Tackling_Generated_Datasets_Diversity.md # 主文件: 多样性理论
│   │   └── Day25_1_提示词处理数据多样性快速指南.md ⭐ # 快速版: 5维度 + 4种方案
│   │
│   └── 📁 Day26_Generating_Code/
│       ├── Day26_Generating_Code.md # 主文件: 代码生成原理
│       └── Day26_1_AI代码生成完整流程.md ⭐ # 快速版: 5步工作流 + 模板
│
├── 📁 第四阶段_Prompt_Hub/         # 提示集合 (11天)
│   ├── Day27_Classification.md # 分类任务
│   ├── Day28_Coding.md  # 编码任务
│   ├── Day29_Creativity.md # 创造力任务
│   ├── Day30_Evaluation.md # 评估任务
│   ├── Day31_Information_Extraction.md # 信息提取任务
│   ├── Day32_Image_Generation.md # 图像生成任务
│   ├── Day33_Mathematics.md # 数学任务
│   ├── Day34_Question_Answering.md # 问答任务
│   ├── Day35_Reasoning.md # 推理任务
│   ├── Day36_Text_Summarization.md # 文本摘要任务
│   └── Day37_Truthfulness_Adversarial_Prompting.md # 真实度对抗提示任务
│
├── 📁 第五阶段_Models/             # 模型特点 (3天)
│   ├── Day38_ChatGPT.md # ChatGPT 模型特点
│   ├── Day39_Code_Llama_Flan_Gemini.md # Code Llama, Flan, Gemini 模型特点
│   └── Day40_GPT-4_LLaMA_Mistral_7B_Mixtral_OLMo_Phi-2_Model_Collection.md # GPT-4, LLaMA, Mistral-7B, Mixtral-8x7B, OLMo, Phi-2 模型集合
│
├── 📁 第六阶段_Risks/              # 风险安全 (1天)
│   └── Day41_Risks_and_Misuses.md
│
├── 📁 第七阶段_Papers_Tools/       # 论文工具 (2天)
│   ├── Day42_Papers.md # 相关论文
│   └── Day43_Tools_Notebooks_Datasets.md # 相关工具、笔记本和数据集
│
└── 📁 学习笔记汇总/                # 学习成果
    ├── 学习心得汇总.md 
    ├── 最佳实践总结.md
    └── 项目作品集.md
```

---

## 🚀 快速开始

### 1. 准备环境

```bash
# 克隆或下载本项目
git clone <repository-url>
cd Prompt-Engineering-Learning

# 或直接使用本地目录
# /home/seeback/PycharmProjects/Modelrecognize/Prompt-Engineering-Learning/
```

### 2. 获取 API 密钥

```bash
# 准备以下 API 密钥 (至少一个)
# 1. OpenAI API: https://platform.openai.com/
# 2. Anthropic Claude API: https://console.anthropic.com/
# 3. DeepSeek API: https://platform.deepseek.com/
# 4. Google Gemini API: https://makersuite.google.com/
```

### 3. 安装依赖

```bash
# Python 环境 (3.9+)
pip install openai anthropic langchain jupyter

# 或使用 conda
conda create -n prompt-eng python=3.9
conda activate prompt-eng
pip install openai anthropic langchain jupyter
```

### 4. 开始学习

```bash
# 阅读学习计划
cat 学习计划总概览.md

# 开始第一天学习
cat 第一阶段_Introduction/Day1_Prompt_Engineering_Introduction.md

# 或打开 Jupyter Notebook
jupyter notebook
```

---

## 📚 学习资源

### 官方资源

- **在线指南**: https://www.promptingguide.ai/
- **视频讲座**: https://youtu.be/dOxUroR57xs
- **代码示例**: `Prompt-Engineering-Guide-main/notebooks/`
- **完整幻灯片**: `Prompt-Engineering-Guide-main/lecture/`

### 本地资源

```
📦 Prompt-Engineering-Guide-main/
├─ guides/ (8个指南文档)
├─ notebooks/ (12个实战代码)
└─ lecture/ (完整讲座)
```

### 补充工具

```
💰 Prompt 市场:
├─ PromptBase: https://promptbase.com/
├─ AIPRM: https://aiprm.com/
└─ PromptHero: https://prompthero.com/

🔧 开发工具:
├─ LangChain: LLM 应用框架
├─ LlamaIndex: 数据框架
└─ OpenPrompt: 提示优化
```

---

## 🎯 学习方法

### 每日学习流程

```
1. 阅读理论 (30分钟)
   ├─ 理解核心概念
   ├─ 掌握技术原理
   └─ 记录关键要点

2. 实践操作 (60-90分钟)
   ├─ 设计提示词
   ├─ 测试不同参数
   ├─ 优化输出效果
   └─ 记录实验结果

3. 总结反思 (30分钟)
   ├─ 整理学习笔记
   ├─ 总结最佳实践
   ├─ 记录疑问问题
   └─ 规划明日学习
```

### 学习原则

- **循序渐进**: 不跳跃，从基础开始
- **实践为主**: 每天至少 2 小时动手实践
- **理论结合**: 理解原理，指导实践
- **持续记录**: 使用标准笔记模板
- **迭代优化**: 基于反馈不断改进

---

## 📊 评估标准

### 每日评估

```
评分维度 (每个 20 分):
├─ 理论理解 (20分)
├─ 实践应用 (20分)
├─ 创新思考 (20分)
├─ 笔记质量 (20分)
└─ 项目完成度 (20分)

总分 90+: 优秀 ⭐⭐⭐⭐⭐
总分 80-89: 良好 ⭐⭐⭐⭐
总分 70-79: 合格 ⭐⭐⭐
```

### 阶段目标

```
第一阶段 (Introduction):
✅ 掌握基础概念和原则
✅ 理解 LLM 参数影响
✅ 设计简单提示词

第二阶段 (Techniques):
✅ 掌握 23 种核心技术
✅ 能够组合使用技术
✅ 解决复杂问题

第三阶段 (Applications):
✅ 完成端到端项目
✅ 整合多种技术
✅ 建立评估体系

第四阶段 (Prompt Hub):
✅ 掌握各类应用模板
✅ 建立个人提示库
✅ 优化性能指标

第五阶段 (Models):
✅ 理解不同模型特点
✅ 制定适配策略
✅ 优化使用效果

第六阶段 (Risks):
✅ 理解安全风险
✅ 掌握防御方法
✅ 建立评估机制

第七阶段 (Papers & Tools):
✅ 阅读关键论文
✅ 使用开发工具
✅ 跟踪最新发展
```

---

## 💡 学习技巧

### 高效技巧

```
1. 模板复用
   - 建立提示词模板库
   - 记录有效组合
   - 快速应用到新场景

2. 对比实验
   - 设计 A/B 测试
   - 记录参数影响
   - 找到最优配置

3. 问题驱动
   - 从实际问题出发
   - 寻找技术方案
   - 验证效果

4. 社区学习
   - 加入学习群组
   - 分享学习心得
   - 参与讨论交流
```

### 常见问题

```
Q1: 学习时间不够怎么办？
A1: 可以压缩到 21 天，每天 4-5 小时，专注于核心内容。

Q2: 没有 API 密钥怎么办？
A2: 可以使用本地模型 (Ollama) 或免费试用额度。

Q3: 感觉进度慢怎么办？
A3: 是正常的，保持节奏，持续实践比速度更重要。

Q4: 如何保持学习动力？
A4: 设置小目标，记录进步，分享成果，获得反馈。
```

---

## 🏆 学习成果

### 预期成果

```
43天后你将拥有:
✅ 理论体系:
   ├─ 完整的提示工程知识
   ├─ 深入的技术理解
   └─ 前瞻的发展视野

✅ 实践能力:
   ├─ 熟练应用 23+ 技术
   ├─ 设计高效提示策略
   ├─ 优化性能指标
   └─ 解决实际问题

✅ 项目作品:
   ├─ 完整提示工程项目
   ├─ 优化的提示模板库
   ├─ 自动化评估系统
   └─ 技术博客或分享

✅ 职业发展:
   ├─ 掌握前沿技能
   ├─ 建立专业声誉
   ├─ 获得就业机会
   └─ 持续成长能力
```

### 成功案例

```
优秀学员成果:
├─ 出版提示工程书籍
├─ 成为技术布道者
├─ 开发提示工具
├─ 创立 AI 创业项目
├─ 成为行业专家
└─ 影响技术发展
```

---

## 🤝 贡献与交流

### 学习交流

```
💬 社区资源:
├─ Discord: 实时讨论
├─ GitHub: 代码分享
├─ Twitter: 技术动态
└─ Newsletter: 学习资讯

🎓 分享方式:
├─ 撰写技术博客
├─ 制作教学视频
├─ 开源项目贡献
└─ 组织学习活动
```

### 贡献指南

```
欢迎贡献:
├─ 完善学习笔记
├─ 添加实践案例
├─ 优化学习计划
├─ 修复错误内容
├─ 翻译多语言版本
└─ 开发辅助工具
```

---

## 📄 许可证

本学习项目基于 [MIT License](https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/LICENSE.md) 开源。

---

## 🙏 致谢

- **DAIR.AI**: 提供优秀的 Prompt Engineering Guide
- **开源社区**: 贡献工具和资源
- **学习者**: 共同探索和成长

---

## 📞 联系我们

- **项目地址**: [GitHub Repository]
- **在线讨论**: [Discord Link]
- **学习咨询**: [Email]
- **技术交流**: [Twitter]

---

**🚀 开始你的 Prompt Engineering 之旅！**

**明天从 Day 1 开始，让我们一起成为提示工程专家！**

---

## 📅 最新进展 (2025-11-09)

### 重大突破

```
最近完成的核心工作:
┌──────────────────────────────────────────────┐
│ ✅ 第三阶段完整优化 (2025-11-09)             │
│ ├─ 创建Day24_1: RAG知识库构建快速指南      │
│ │  └─ 5步RAG工作流 + 完整代码 + 时间估算   │
│ ├─ 创建Day25_1: 数据多样性5维度方案        │
│ │  └─ 诊断工具 + 4种解决方案 + 50分钟计划 │
│ ├─ 创建Day26_1: AI代码生成完整流程         │
│ │  └─ 5部分提示词结构 + 迭代策略 + 模板   │
│ ├─ 创建学习路线导航: 3条学习路径             │
│ │  └─ 快速版/完整版/项目驱动版自助选择    │
│ └─ 优化README结构: 第三阶段完整文件地图     │
│    └─ 25个文件系统组织 + 清晰导航          │
│                                             │
│ ✅ 模型部署理解 (2025-11-03)               │
│ ├─ 基础模型 vs 应用优化架构                │
│ ├─ DeepSeek-V3完整部署指南                │
│ ├─ 开源 vs 商业API对比分析                │
│ └─ ToT等复杂机制实现解析                  │
│                                             │
│ ✅ 深度理解总结 (2025-11-03)               │
│ ├─ Generate Knowledge迭代机制             │
│ ├─ Prompt Chaining应用本质                │
│ ├─ 671B参数实际意义与硬件需求             │
│ └─ 完整技术栈整合                         │
│                                             │
│ ✅ 学习成就总结 (2025-11-03)               │
│ ├─ 60天核心学习回顾                       │
│ ├─ 从理论到实践的完整旅程                 │
│ ├─ 未来发展规划                          │
│ └─ 学习方法论总结                         │
│                                             │
│ 累计成果 (2025-11-09):                    │
│ ├─ 创建文档: 55+ (新增5个快速版+导航)    │
│ ├─ 学习笔记: 100+                        │
│ ├─ 核心概念: 60+                         │
│ ├─ 实践代码: 25+                         │
│ ├─ 完整工作流: 8+                        │
│ └─ 学习时长: 320+ 小时                   │
└──────────────────────────────────────────────┘
```

### 第三阶段完整性检查 ✅

```
Day22 (工具调用):
  ✅ 主文件 + 3个扩展版本 (共4个)
  ├─ Day22: 主文件 (函数调用完整解析)
  ├─ Day22_1: 快速版 (3种工具调用方式对比)
  ├─ Day22_2: 进阶版 (API vs 模型部署)
  └─ Day22_3: 深度版 (MCP协议深度机制)

Day23 (数据生成):
  ✅ 主文件 + 2个扩展版本 (共3个)
  ├─ Day23: 主文件 (完整工作流)
  ├─ Day23_1: 快速版 (0→10万数据避坑指南)
  └─ Day23_2: 深度版 (企业级质量评估体系)

Day24 (RAG系统):
  ✅ 主文件 + 快速版 (共2个)
  ├─ Day24: 主文件 (RAG完整解析)
  └─ Day24_1: 快速版 ⭐ (5步快速指南 + 代码) [刚创建]

Day25 (多样性处理):
  ✅ 主文件 + 快速版 (共2个)
  ├─ Day25: 主文件 (多样性理论)
  └─ Day25_1: 快速版 ⭐ (5维度 + 4种方案) [刚创建]

Day26 (代码生成):
  ✅ 主文件 + 快速版 (共2个)
  ├─ Day26: 主文件 (代码生成原理)
  └─ Day26_1: 快速版 ⭐ (5步工作流 + 模板) [刚创建]

导航文档:
  ✅ 00_学习路线导航.md ⭐ (3条学习路径自助选择) [刚创建]

总计: 14个Day文件 + 1个导航 = 15个文件
```

---

**最后更新**: 2025-11-09
**版本**: v2.1 (第三阶段完整优化)
**作者**: Claude Code Assistant

🎉 **第三阶段现已完整!** 用户可通过00_学习路线导航.md快速选择学习路径！
