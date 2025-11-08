# Day 18: 多模态提示（Multimodal Prompting）

## 理论学习

### 多模态提示的核心原理

多模态提示（Multimodal Prompting）是一种集成多种感知模态（文本、图像、音频、视频等）的提示工程技术。
该技术通过设计有效的跨模态提示策略，使大语言模型能够理解、处理和生成多种模态的信息，实现更自然、更强大的人机交互体验。

#### 技术机制与工作原理

**核心流程：**
1. **模态识别与理解**
   - 识别输入的多模态内容
   - 提取各模态的关键信息
   - 建立模态间的关联关系

2. **跨模态提示设计**
   - 设计模态间的提示格式
   - 建立模态对齐策略
   - 构造统一的多模态提示

3. **联合理解与推理**
   - 融合多模态信息
   - 执行跨模态推理
   - 生成模态一致的输出

4. **多模态输出生成**
   - 生成符合要求的多模态内容
   - 保证模态间的一致性
   - 优化输出质量

**技术创新点：**
- **模态融合**：有效整合不同模态的信息
- **跨模态对齐**：建立模态间的语义对齐
- **联合推理**：实现跨模态的逻辑推理
- **统一接口**：提供一致的多模态交互方式

#### 理论基础

**多模态架构模型**
```
Multimodal = Encode(Modalities) → Align(Prompts) → Fusion(Features) → Generate(Outputs)

其中：
- Encode: 模态编码函数，将各模态转换为特征
- Align: 模态对齐函数，建立跨模态对应关系
- Fusion: 特征融合函数，整合多模态信息
- Generate: 输出生成函数，产生多模态结果
```

**分层系统架构**
```
第一层：模态输入层（Modality Input Layer）
输入：多模态数据
输出：模态特征表示

第二层：模态对齐层（Modality Alignment Layer）
输入：各模态特征
输出：对齐后的跨模态特征

第三层：提示融合层（Prompt Fusion Layer）
输入：跨模态特征和文本提示
输出：融合的多模态提示

第四层：多模态推理层（Multimodal Reasoning Layer）
输入：多模态提示
输出：推理结果和特征

第五层：多模态生成层（Multimodal Generation Layer）
输入：推理结果
输出：多模态输出内容
```

**多模态提示设计框架**
```python
class MultimodalPromptingFramework:
    """多模态提示设计框架"""
    def __init__(self, multimodal_llm):
        self.llm = multimodal_llm
        self.modalities = ['text', 'image', 'audio', 'video']
        self.encoders = self.initialize_encoders()
        self.alignment_matrix = None

    def design_multimodal_prompt(self, inputs, task_description):
        """
        设计多模态提示

        Args:
            inputs: 多模态输入字典
            task_description: 任务描述

        Returns:
            dict: 设计的多模态提示
        """
        # 1. 模态识别
        available_modalities = self.identify_available_modalities(inputs)

        # 2. 编码各模态
        encoded_features = {}
        for modality in available_modalities:
            encoded_features[modality] = self.encode_modality(
                modality, inputs[modality]
            )

        # 3. 跨模态对齐
        aligned_features = self.align_modalities(
            encoded_features, task_description
        )

        # 4. 提示构造
        prompt = self.construct_multimodal_prompt(
            aligned_features, task_description
        )

        return {
            'available_modalities': available_modalities,
            'encoded_features': encoded_features,
            'aligned_features': aligned_features,
            'multimodal_prompt': prompt
        }

    def identify_available_modalities(self, inputs):
        """识别可用的模态"""
        available = []
        for modality in self.modalities:
            if modality in inputs and inputs[modality] is not None:
                available.append(modality)
        return available

    def encode_modality(self, modality, data):
        """编码特定模态"""
        encoder = self.encoders.get(modality)
        if encoder:
            return encoder.encode(data)
        else:
            # 默认文本编码
            return self.default_text_encoder(data)

    def align_modalities(self, features, task_description):
        """跨模态对齐"""
        # 1. 计算模态间相关性
        correlations = self.calculate_cross_modal_correlations(features)

        # 2. 构建对齐矩阵
        self.alignment_matrix = self.build_alignment_matrix(
            features, correlations
        )

        # 3. 应用对齐变换
        aligned_features = self.apply_alignment(features, self.alignment_matrix)

        return aligned_features

    def construct_multimodal_prompt(self, aligned_features, task_description):
        """构造多模态提示"""
        prompt_components = {
            'task': task_description,
            'modalities': {},
            'instructions': self.generate_modality_instructions(aligned_features)
        }

        # 为每个模态构造提示组件
        for modality, features in aligned_features.items():
            prompt_components['modalities'][modality] = self.encode_modality_prompt(
                modality, features
            )

        # 融合多模态提示
        final_prompt = self.fusion_multimodal_prompt(prompt_components)

        return final_prompt

    def calculate_cross_modal_correlations(self, features):
        """计算跨模态相关性"""
        modalities = list(features.keys())
        correlations = {}

        for i, mod1 in enumerate(modalities):
            for j, mod2 in enumerate(modalities[i+1:], i+1):
                # 计算模态间的相关性
                corr = self.compute_similarity(features[mod1], features[mod2])
                correlations[f"{mod1}-{mod2}"] = corr

        return correlations

    def build_alignment_matrix(self, features, correlations):
        """构建对齐矩阵"""
        # 简化的对齐矩阵构建
        n_modalities = len(features)
        alignment_matrix = [[1.0] * n_modalities for _ in range(n_modalities)]

        # 根据相关性调整对齐权重
        modalities = list(features.keys())
        for i, mod1 in enumerate(modalities):
            for j, mod2 in enumerate(modalities[i+1:], i+1):
                correlation = correlations.get(f"{mod1}-{mod2}", 0.5)
                alignment_matrix[i][j] = correlation
                alignment_matrix[j][i] = correlation

        return alignment_matrix

    def apply_alignment(self, features, alignment_matrix):
        """应用对齐变换"""
        aligned_features = {}
        modalities = list(features.keys())

        for i, modality in enumerate(modalities):
            # 应用对齐权重
            aligned_features[modality] = self.weight_features(
                features[modality], alignment_matrix[i]
            )

        return aligned_features

    def weight_features(self, features, weights):
        """对特征加权"""
        # 简化的特征加权
        return features * weights[0] if len(weights) > 0 else features

    def encode_modality_prompt(self, modality, features):
        """编码模态提示"""
        modality_prompts = {
            'text': self.encode_text_prompt,
            'image': self.encode_image_prompt,
            'audio': self.encode_audio_prompt,
            'video': self.encode_video_prompt
        }

        encoder = modality_prompts.get(modality, self.encode_text_prompt)
        return encoder(features)

    def encode_text_prompt(self, text_features):
        """编码文本提示"""
        return f"[TEXT] {text_features}"

    def encode_image_prompt(self, image_features):
        """编码图像提示"""
        return f"[IMAGE] <processed image features>"

    def encode_audio_prompt(self, audio_features):
        """编码音频提示"""
        return f"[AUDIO] <processed audio features>"

    def encode_video_prompt(self, video_features):
        """编码视频提示"""
        return f"[VIDEO] <processed video features>"

    def fusion_multimodal_prompt(self, components):
        """融合多模态提示"""
        fusion_prompt = f"""
        任务：{components['task']}

        多模态信息：
        {chr(10).join([
            f"{modality}: {prompt}"
            for modality, prompt in components['modalities'].items()
        ])}

        指示：{components['instructions']}

        请基于以上多模态信息完成指定任务。
        """
        return fusion_prompt

    def generate_modality_instructions(self, aligned_features):
        """生成模态指示"""
        instructions = []

        for modality, features in aligned_features.items():
            instruction = self.get_modality_instruction(modality)
            instructions.append(instruction)

        return " | ".join(instructions)

    def get_modality_instruction(self, modality):
        """获取模态指示"""
        instruction_mapping = {
            'text': "请仔细阅读文本内容，理解其含义和上下文",
            'image': "请观察图像内容，识别其中的对象、场景和关系",
            'audio': "请聆听音频内容，理解说话内容、情感和语调",
            'video': "请观看视频内容，理解动态场景、事件序列和内容"
        }

        return instruction_mapping.get(modality, f"请处理{modality}模态信息")

    def initialize_encoders(self):
        """初始化编码器"""
        return {
            'text': TextEncoder(),
            'image': ImageEncoder(),
            'audio': AudioEncoder(),
            'video': VideoEncoder()
        }

    def default_text_encoder(self, data):
        """默认文本编码器"""
        if isinstance(data, str):
            return data
        return str(data)

    def compute_similarity(self, features1, features2):
        """计算特征相似度"""
        # 简化的相似度计算
        return 0.8  # 模拟相似度分数
```

### 多模态提示 vs 单模态提示对比

**vs Text-Only Prompting**
| 维度 | 多模态提示 | 纯文本提示 |
|------|------------|------------|
| 信息丰富度 | 高（多模态融合） | 低（仅文本） |
| 理解深度 | 强（跨模态理解） | 中（语义理解） |
| 应用范围 | 广泛（多媒体） | 有限（文本为主） |
| 实现复杂度 | 高（模态对齐） | 低（简单文本） |
| 计算成本 | 高（多模态处理） | 低（文本处理） |

**vs Image Captioning**
| 维度 | 多模态提示 | 图像描述 |
|------|------------|----------|
| 交互性 | 强（双向交互） | 弱（单向生成） |
| 灵活性 | 高（可定制提示） | 中（固定模式） |
| 任务范围 | 广（多种任务） | 窄（描述为主） |
| 智能化 | 强（推理+生成） | 中（生成为主） |
| 适应性 | 高（动态调整） | 低（静态生成） |

### 多模态提示的分类体系

**1. 并行多模态提示（Parallel Multimodal Prompting）**

同时输入多个模态的信息：

```python
class ParallelMultimodalPrompting:
    """并行多模态提示"""
    def __init__(self, llm):
        self.llm = llm
        self.modalities = ['text', 'image', 'audio', 'video']

    def create_parallel_prompt(self, inputs):
        """创建并行提示"""
        # 1. 并行编码所有模态
        parallel_encodings = {}
        for modality in inputs:
            parallel_encodings[modality] = self.encode_modality_parallel(
                modality, inputs[modality]
            )

        # 2. 并行构造提示
        parallel_prompts = []
        for modality, encoding in parallel_encodings.items():
            prompt = self.construct_modality_prompt(modality, encoding)
            parallel_prompts.append(prompt)

        # 3. 并行融合提示
        fused_prompt = self.fuse_parallel_prompts(parallel_prompts)

        return fused_prompt

    def encode_modality_parallel(self, modality, data):
        """并行编码模态"""
        # 为每个模态创建独立的编码流程
        encoding_pipeline = self.create_encoding_pipeline(modality)
        return encoding_pipeline.process(data)

    def create_encoding_pipeline(self, modality):
        """创建编码管道"""
        pipelines = {
            'text': TextEncodingPipeline(),
            'image': ImageEncodingPipeline(),
            'audio': AudioEncodingPipeline(),
            'video': VideoEncodingPipeline()
        }

        return pipelines.get(modality, TextEncodingPipeline())

    def construct_modality_prompt(self, modality, encoding):
        """构造模态提示"""
        modality_templates = {
            'text': f"[文本信息]\n{encoding}",
            'image': f"[图像信息]\n{self.process_image_encoding(encoding)}",
            'audio': f"[音频信息]\n{self.process_audio_encoding(encoding)}",
            'video': f"[视频信息]\n{self.process_video_encoding(encoding)}"
        }

        return modality_templates.get(modality, f"[{modality}] {encoding}")

    def fuse_parallel_prompts(self, prompts):
        """融合并行提示"""
        fusion_instruction = f"""
        基于以下并行输入的多模态信息，完成相应任务：

        {chr(10).join(prompts)}

        任务要求：
        1. 整合所有模态信息
        2. 进行跨模态理解
        3. 生成综合答案

        请开始处理：
        """
        return self.llm.generate(fusion_instruction)

    def process_image_encoding(self, encoding):
        """处理图像编码"""
        return f"图像特征: {encoding[:100]}... (省略中间内容)"

    def process_audio_encoding(self, encoding):
        """处理音频编码"""
        return f"音频特征: {encoding[:100]}... (省略中间内容)"

    def process_video_encoding(self, encoding):
        """处理视频编码"""
        return f"视频特征: {encoding[:100]}... (省略中间内容)"
```

**2. 序列多模态提示（Sequential Multimodal Prompting）**

按顺序处理多个模态：

```python
class SequentialMultimodalPrompting:
    """序列多模态提示"""
    def __init__(self, llm):
        self.llm = llm
        self.processing_order = None

    def create_sequential_prompt(self, inputs, order=None):
        """创建序列提示"""
        # 1. 确定处理顺序
        self.processing_order = order or self.determine_processing_order(inputs)

        # 2. 序列编码模态
        sequential_state = {}
        for modality in self.processing_order:
            if modality in inputs:
                # 使用前序状态编码当前模态
                sequential_state = self.encode_modality_sequential(
                    modality, inputs[modality], sequential_state
                )

        # 3. 序列构造最终提示
        final_prompt = self.construct_sequential_prompt(
            sequential_state
        )

        return final_prompt

    def determine_processing_order(self, inputs):
        """确定处理顺序"""
        # 默认顺序：文本 -> 图像 -> 音频 -> 视频
        default_order = ['text', 'image', 'audio', 'video']

        # 根据可用模态过滤
        available_order = [mod for mod in default_order if mod in inputs]

        # 基于任务优化顺序
        optimized_order = self.optimize_processing_order(available_order)

        return optimized_order

    def optimize_processing_order(self, available_modalities):
        """优化处理顺序"""
        # 简化的优化策略
        # 1. 文本优先（作为锚点）
        if 'text' in available_modalities:
            available_modalities.remove('text')
            available_modalities.insert(0, 'text')

        # 2. 其他模态按复杂度排序
        # 图像 < 音频 < 视频
        complexity_order = {'image': 1, 'audio': 2, 'video': 3}
        available_modalities.sort(
            key=lambda x: complexity_order.get(x, 99)
        )

        return available_modalities

    def encode_modality_sequential(self, modality, data, previous_state):
        """序列编码模态"""
        # 1. 获取模态编码器
        encoder = self.get_modality_encoder(modality)

        # 2. 融合前序状态
        contextualized_data = self融合_previous_context(data, previous_state)

        # 3. 编码当前模态
        encoded_features = encoder.encode(contextualized_data)

        # 4. 更新状态
        updated_state = self.update_sequential_state(
            previous_state, modality, encoded_features
        )

        return updated_state

    def get_modality_encoder(self, modality):
        """获取模态编码器"""
        encoders = {
            'text': TextEncoder(),
            'image': ImageEncoder(),
            'audio': AudioEncoder(),
            'video': VideoEncoder()
        }
        return encoders.get(modality)

    def merge_previous_context(self, data, previous_state):
        """融合前序上下文"""
        if not previous_state:
            return data

        # 将前序信息融入当前数据
        merged_data = {
            'current': data,
            'context': previous_state
        }

        return merged_data

    def update_sequential_state(self, previous_state, modality, features):
        """更新序列状态"""
        new_state = previous_state.copy()
        new_state[modality] = {
            'features': features,
            'timestamp': datetime.now().isoformat()
        }

        # 保持状态一致性
        new_state['processing_order'] = self.processing_order
        new_state['last_modality'] = modality

        return new_state

    def construct_sequential_prompt(self, sequential_state):
        """构造序列提示"""
        # 构建序列化的上下文
        contextual_layers = []

        for modality in self.processing_order:
            if modality in sequential_state:
                layer = self.construct_modality_layer(
                    modality, sequential_state[modality]
                )
                contextual_layers.append(layer)

        # 融合所有层级
        fusion_prompt = f"""
        基于序列化的多模态信息处理：

        {chr(10).join(contextual_layers)}

        请基于逐步累积的信息完成指定任务。

        任务处理：
        """
        return self.llm.generate(fusion_prompt)

    def construct_modality_layer(self, modality, state):
        """构造模态层级"""
        features = state['features']
        timestamp = state['timestamp']

        layer_templates = {
            'text': f"[步骤 {len(self.processing_order)} - 文本] 处理文本信息: {features}",
            'image': f"[步骤 {len(self.processing_order)} - 图像] 观察图像内容: {self.describe_image_features(features)}",
            'audio': f"[步骤 {len(self.processing_order)} - 音频] 聆听音频内容: {self.describe_audio_features(features)}",
            'video': f"[步骤 {len(self.processing_order)} - 视频] 观看视频内容: {self.describe_video_features(features)}"
        }

        return layer_templates.get(modality, f"[步骤] 处理{modality}信息: {features}")

    def describe_image_features(self, features):
        """描述图像特征"""
        return f"图像特征摘要: {features[:80]}..."

    def describe_audio_features(self, features):
        """描述音频特征"""
        return f"音频特征摘要: {features[:80]}..."

    def describe_video_features(self, features):
        """描述视频特征"""
        return f"视频特征摘要: {features[:80]}..."
```

**3. 层级多模态提示（Hierarchical Multimodal Prompting）**

分层次的模态处理：

```python
class HierarchicalMultimodalPrompting:
    """层级多模态提示"""
    def __init__(self, llm):
        self.llm = llm
        self.hierarchy_levels = {
            'low': ['texture', 'color', 'tone'],      # 底层：基础特征
            'mid': ['object', 'scene', 'content'],    # 中层：结构特征
            'high': ['concept', 'emotion', 'meaning']  # 高层：语义特征
        }

    def create_hierarchical_prompt(self, inputs):
        """创建层级提示"""
        # 1. 分层编码
        hierarchical_features = self.encode_hierarchical(inputs)

        # 2. 层级融合
        fused_features = self.fuse_hierarchical_features(
            hierarchical_features
        )

        # 3. 构造层级提示
        hierarchical_prompt = self.construct_hierarchical_prompt(
            fused_features
        )

        return hierarchical_prompt

    def encode_hierarchical(self, inputs):
        """分层编码"""
        hierarchical_encoding = {}

        # 为每个模态进行分层编码
        for modality, data in inputs.items():
            hierarchical_encoding[modality] = self.encode_modality_hierarchical(
                modality, data
            )

        return hierarchical_encoding

    def encode_modality_hierarchical(self, modality, data):
        """模态分层编码"""
        levels_encoding = {}

        for level in self.hierarchy_levels:
            level_features = self.extract_level_features(
                modality, data, level
            )
            levels_encoding[level] = level_features

        return levels_encoding

    def extract_level_features(self, modality, data, level):
        """提取层级特征"""
        level_prompts = {
            'low': f"提取{modality}的基础特征（低层）",
            'mid': f"分析{modality}的结构特征（中层）",
            'high': f"理解{modality}的语义特征（高层）"
        }

        prompt = level_prompts.get(level, "提取特征")
        processed = self.llm.generate(f"{prompt}: {data}", max_tokens=200)

        return processed

    def fuse_hierarchical_features(self, hierarchical_features):
        """融合层级特征"""
        fused_features = {}

        for level in self.hierarchy_levels:
            level_features = {}

            for modality, features in hierarchical_features.items():
                if level in features:
                    level_features[modality] = features[level]

            # 同层级跨模态融合
            if level_features:
                fused_features[level] = self.fuse_same_level_features(
                    level_features
                )

        return fused_features

    def fuse_same_level_features(self, level_features):
        """同层级特征融合"""
        modalities = list(level_features.keys())

        if len(modalities) == 1:
            return level_features[modalities[0]]

        # 跨模态特征融合
        fusion_prompt = f"""
        融合以下{len(modalities)}个模态的{list(level_features.values())[0]}层级信息：

        模态信息：
        {chr(10).join([f"{mod}: {feat}" for mod, feat in level_features.items()])}

        请提取共同的{list(level_features.values())[0]}层级特征：
        """

        fused = self.llm.generate(fusion_prompt, max_tokens=300)
        return fused

    def construct_hierarchical_prompt(self, fused_features):
        """构造层级提示"""
        # 从低层到高层构建提示
        hierarchical_sections = []

        for level in ['low', 'mid', 'high']:
            if level in fused_features:
                section = self.construct_level_section(
                    level, fused_features[level]
                )
                hierarchical_sections.append(section)

        # 整合所有层级
        final_prompt = f"""
        基于以下分层多模态信息进行分析：

        {chr(10).join(hierarchical_sections)}

        请综合所有层级的信息，完成指定任务。

        任务执行：
        """

        return self.llm.generate(final_prompt)

    def construct_level_section(self, level, features):
        """构造层级章节"""
        level_names = {
            'low': '基础特征层',
            'mid': '结构特征层',
            'high': '语义特征层'
        }

        level_prompts = {
            'low': '基于这些基础特征进行分析',
            'mid': '基于这些结构特征进行理解',
            'high': '基于这些语义特征进行推理'
        }

        section = f"""
        === {level_names.get(level, level)} ===
        {features}

        {level_prompts.get(level, '处理该层级信息')}
        """

        return section
```

### 多模态提示系统的核心技术

**1. 模态对齐（Modality Alignment）**

```python
class CrossModalityAlignment:
    """跨模态对齐"""
    def __init__(self):
        self.alignment_strategies = [
            'attention_based',
            'contrastive_learning',
            'fused_feature_matching'
        ]

    def align_modalities(self, source_modality, target_modality, features):
        """模态对齐"""
        # 1. 选择对齐策略
        strategy = self.select_alignment_strategy(
            source_modality, target_modality
        )

        # 2. 执行对齐
        aligned_features = self.execute_alignment(
            strategy, features
        )

        return aligned_features

    def select_alignment_strategy(self, source_modality, target_modality):
        """选择对齐策略"""
        # 基于模态组合选择策略
        modality_pairs = {
            ('text', 'image'): 'attention_based',
            ('image', 'audio'): 'contrastive_learning',
            ('text', 'audio'): 'fused_feature_matching',
            ('video', 'text'): 'attention_based'
        }

        pair = (min(source_modality, target_modality),
                max(source_modality, target_modality))

        return modality_pairs.get(pair, 'attention_based')

    def execute_alignment(self, strategy, features):
        """执行对齐"""
        alignment_methods = {
            'attention_based': self.attention_based_alignment,
            'contrastive_learning': self.contrastive_alignment,
            'fused_feature_matching': self.fused_feature_alignment
        }

        method = alignment_methods.get(strategy, self.attention_based_alignment)
        return method(features)

    def attention_based_alignment(self, features):
        """基于注意力的对齐"""
        # 模拟注意力对齐过程
        aligned = {}
        for modality, feature in features.items():
            # 应用自注意力机制
            attended_feature = self.apply_self_attention(feature)
            aligned[modality] = attended_feature

        return aligned

    def contrastive_alignment(self, features):
        """对比学习对齐"""
        # 模拟对比学习对齐过程
        aligned = {}
        modalities = list(features.keys())

        for i, mod1 in enumerate(modalities):
            for j, mod2 in enumerate(modalities[i+1:], i+1):
                # 计算对比损失并对齐
                aligned_pair = self.compute_contrastive_alignment(
                    features[mod1], features[mod2]
                )
                aligned[mod1] = aligned_pair[0]
                aligned[mod2] = aligned_pair[1]

        return aligned

    def fused_feature_alignment(self, features):
        """融合特征匹配对齐"""
        # 模拟融合特征匹配
        # 1. 提取共同特征空间
        common_space = self.extract_common_feature_space(features)

        # 2. 将各模态映射到共同空间
        aligned = {}
        for modality, feature in features.items():
            aligned[modality] = self.map_to_common_space(
                feature, common_space
            )

        return aligned

    def apply_self_attention(self, feature):
        """应用自注意力"""
        # 简化的自注意力实现
        return f"attended({feature[:50]}...)"

    def compute_contrastive_alignment(self, feature1, feature2):
        """计算对比对齐"""
        # 简化的对比对齐
        return (
            f"aligned({feature1[:40]}...)",
            f"aligned({feature2[:40]}...)"
        )

    def extract_common_feature_space(self, features):
        """提取共同特征空间"""
        return "common_feature_space"

    def map_to_common_space(self, feature, common_space):
        """映射到共同空间"""
        return f"mapped_to({common_space})"
```

**2. 跨模态融合（Cross-Modal Fusion）**

```python
class CrossModalFusion:
    """跨模态融合"""
    def __init__(self, llm):
        self.llm = llm
        self.fusion_methods = {
            'early_fusion': self.early_fusion,
            'late_fusion': self.late_fusion,
            'hybrid_fusion': self.hybrid_fusion
        }

    def fuse_modalities(self, aligned_features, method='hybrid_fusion'):
        """融合模态"""
        fusion_func = self.fusion_methods.get(method, self.hybrid_fusion)
        return fusion_func(aligned_features)

    def early_fusion(self, features):
        """早期融合：在特征层面融合"""
        # 1. 特征拼接
        concatenated_features = self.concatenate_features(features)

        # 2. 特征变换
        transformed_features = self.transform_features(
            concatenated_features
        )

        return transformed_features

    def late_fusion(self, features):
        """晚期融合：在决策层面融合"""
        # 1. 各模态独立处理
        modality_outputs = {}
        for modality, feature in features.items():
            output = self.process_modality_independent(modality, feature)
            modality_outputs[modality] = output

        # 2. 融合决策
        fused_decision = self.fuse_decisions(modality_outputs)

        return fused_decision

    def hybrid_fusion(self, features):
        """混合融合：结合早期和晚期融合"""
        # 1. 分层融合
        intermediate_fusions = self.create_intermediate_fusions(features)

        # 2. 跨层融合
        cross_layer_fusion = self.fuse_cross_layers(intermediate_fusions)

        # 3. 最终融合
        final_fusion = self.final_fusion(cross_layer_fusion)

        return final_fusion

    def concatenate_features(self, features):
        """特征拼接"""
        concatenated = []
        for modality, feature in features.items():
            concatenated.append(f"[{modality}]{feature}")

        return " | ".join(concatenated)

    def transform_features(self, concatenated_features):
        """特征变换"""
        # 使用LLM进行特征变换和增强
        transformation_prompt = f"""
        增强和变换以下多模态特征：

        特征：{concatenated_features}

        请进行特征变换，提取关键信息：
        """
        return self.llm.generate(transformation_prompt, max_tokens=400)

    def process_modality_independent(self, modality, feature):
        """独立处理模态"""
        process_prompt = f"""
        处理以下{modality}模态信息：

        信息：{feature}

        请提取关键信息：
        """
        return self.llm.generate(process_prompt, max_tokens=300)

    def fuse_decisions(self, modality_outputs):
        """融合决策"""
        outputs_text = chr(10).join([
            f"{mod}: {output}"
            for mod, output in modality_outputs.items()
        ])

        fusion_prompt = f"""
        融合以下各模态的处理结果：

        {outputs_text}

        请生成综合决策：
        """
        return self.llm.generate(fusion_prompt, max_tokens=400)

    def create_intermediate_fusions(self, features):
        """创建中间层融合"""
        # 1. 成对融合
        pairs = self.generate_modality_pairs(features)
        pair_fusions = {}

        for pair in pairs:
            mod1, mod2 = pair
            fusion = self.fuse_pair(features[mod1], features[mod2], pair)
            pair_fusions[f"{mod1}+{mod2}"] = fusion

        # 2. 三元组融合
        triplets = self.generate_modality_triplets(features)
        triplet_fusions = {}

        for triplet in triplets:
            fusion = self.fuse_triplet(
                [features[mod] for mod in triplet], triplet
            )
            triplet_fusions["+".join(triplet)] = fusion

        return {
            'pairs': pair_fusions,
            'triplets': triplet_fusions
        }

    def generate_modality_pairs(self, features):
        """生成模态对"""
        modalities = list(features.keys())
        pairs = []

        for i in range(len(modalities)):
            for j in range(i + 1, len(modalities)):
                pairs.append((modalities[i], modalities[j]))

        return pairs

    def generate_modality_triplets(self, features):
        """生成模态三元组"""
        modalities = list(features.keys())
        triplets = []

        if len(modalities) >= 3:
            for i in range(len(modalities)):
                for j in range(i + 1, len(modalities)):
                    for k in range(j + 1, len(modalities)):
                        triplets.append((modalities[i], modalities[j], modalities[k]))

        return triplets

    def fuse_pair(self, feature1, feature2, pair):
        """融合模态对"""
        fusion_prompt = f"""
        融合以下模态对的信息：

        模态对：{pair[0]} + {pair[1]}
        特征1：{feature1}
        特征2：{feature2}

        请生成融合后的特征：
        """
        return self.llm.generate(fusion_prompt, max_tokens=350)

    def fuse_triplet(self, features, triplet):
        """融合模态三元组"""
        fusion_prompt = f"""
        融合以下三个模态的信息：

        模态：{triplet}
        特征：{features}

        请生成融合后的特征：
        """
        return self.llm.generate(fusion_prompt, max_tokens=400)

    def fuse_cross_layers(self, intermediate_fusions):
        """跨层融合"""
        all_fusions = []
        all_fusions.extend(intermediate_fusions['pairs'].values())
        all_fusions.extend(intermediate_fusions['triplets'].values())

        cross_fusion_prompt = f"""
        融合以下多层次的融合结果：

        融合结果：
        {chr(10).join(all_fusions)}

        请生成跨层融合结果：
        """
        return self.llm.generate(cross_fusion_prompt, max_tokens=450)

    def final_fusion(self, cross_layer_fusion):
        """最终融合"""
        final_prompt = f"""
        基于跨层融合结果，生成最终的多模态融合表示：

        跨层融合：{cross_layer_fusion}

        请生成最终的融合表示：
        """
        return self.llm.generate(final_prompt, max_tokens=500)
```

**3. 多模态提示优化（Multimodal Prompt Optimization）**

```python
class MultimodalPromptOptimizer:
    """多模态提示优化器"""
    def __init__(self, llm):
        self.llm = llm
        self.optimization_strategies = [
            'gradient_based',
            'evolutionary',
            'reinforcement_learning',
            'bayesian_optimization'
        ]

    def optimize_multimodal_prompt(self, initial_prompt, feedback):
        """优化多模态提示"""
        # 1. 分析当前性能
        performance_analysis = self.analyze_prompt_performance(
            initial_prompt, feedback
        )

        # 2. 选择优化策略
        optimization_strategy = self.select_optimization_strategy(
            performance_analysis
        )

        # 3. 执行优化
        optimized_prompt = self.execute_optimization(
            optimization_strategy, initial_prompt, performance_analysis
        )

        return optimized_prompt

    def analyze_prompt_performance(self, prompt, feedback):
        """分析提示性能"""
        analysis_prompt = f"""
        分析以下多模态提示的性能：

        提示：{prompt}

        反馈：{feedback}

        请分析：
        1. 性能问题所在
        2. 需要优化的方面
        3. 优化建议

        分析结果：
        """
        return self.llm.generate(analysis_prompt, max_tokens=400)

    def select_optimization_strategy(self, analysis):
        """选择优化策略"""
        # 基于分析结果选择策略
        strategy_mapping = {
            '模态对齐': 'gradient_based',
            '特征融合': 'evolutionary',
            '提示结构': 'reinforcement_learning',
            '参数调优': 'bayesian_optimization'
        }

        for key, strategy in strategy_mapping.items():
            if key in analysis:
                return strategy

        return 'evolutionary'  # 默认策略

    def execute_optimization(self, strategy, prompt, analysis):
        """执行优化"""
        optimization_methods = {
            'gradient_based': self.gradient_based_optimization,
            'evolutionary': self.evolutionary_optimization,
            'reinforcement_learning': self.rl_optimization,
            'bayesian_optimization': self.bayesian_optimization
        }

        method = optimization_methods.get(strategy, self.evolutionary_optimization)
        return method(prompt, analysis)

    def gradient_based_optimization(self, prompt, analysis):
        """基于梯度的优化"""
        # 模拟梯度下降优化
        optimization_prompt = f"""
        基于分析结果，优化以下多模态提示（梯度下降方向）：

        原提示：{prompt}

        分析：{analysis}

        请生成优化后的提示：
        """
        return self.llm.generate(optimization_prompt, max_tokens=500)

    def evolutionary_optimization(self, prompt, analysis):
        """进化优化"""
        # 模拟进化算法优化
        variants = self.generate_prompt_variants(prompt, analysis)

        # 评估变体
        evaluated_variants = self.evaluate_prompt_variants(variants)

        # 选择最优变体
        best_variant = self.select_best_variant(evaluated_variants)

        return best_variant

    def generate_prompt_variants(self, prompt, analysis):
        """生成提示变体"""
        variants = []

        # 生成多个变体
        for i in range(5):
            variant_prompt = f"""
            基于以下分析，生成多模态提示的第{i+1}个变体：

            原提示：{prompt}
            分析：{analysis}

            变体{i+1}：
            """
            variant = self.llm.generate(variant_prompt, max_tokens=450)
            variants.append(variant)

        return variants

    def evaluate_prompt_variants(self, variants):
        """评估提示变体"""
        evaluated = []

        for variant in variants:
            evaluation_prompt = f"""
            评估以下多模态提示变体的质量：

            变体：{variant}

            请评分（0-1）并简要说明：
            """
            evaluation = self.llm.generate(evaluation_prompt, max_tokens=200)
            evaluated.append((variant, evaluation))

        return evaluated

    def select_best_variant(self, evaluated_variants):
        """选择最优变体"""
        # 简化的选择逻辑
        # 实际应用中需要基于评估分数选择
        best_variant = evaluated_variants[0][0]
        return best_variant

    def rl_optimization(self, prompt, analysis):
        """强化学习优化"""
        # 模拟强化学习优化
        rl_prompt = f"""
        使用强化学习方法优化多模态提示：

        当前提示：{prompt}

        分析：{analysis}

        请生成强化学习优化后的提示：
        """
        return self.llm.generate(rl_prompt, max_tokens=500)

    def bayesian_optimization(self, prompt, analysis):
        """贝叶斯优化"""
        # 模拟贝叶斯优化
        bayesian_prompt = f"""
        使用贝叶斯方法优化多模态提示：

        当前提示：{prompt}

        分析：{analysis}

        请生成贝叶斯优化后的提示：
        """
        return self.llm.generate(bayesian_prompt, max_tokens=500)
```

## 实践任务

### 任务1：基础多模态提示系统实现

**目标：**
实现一个基础的多模态提示系统，能够处理文本、图像等多种模态的输入。

**步骤1：核心多模态提示系统**
```python
class BasicMultimodalPromptSystem:
    """基础多模态提示系统"""
    def __init__(self, llm):
        self.llm = llm
        self.modalities = {
            'text': TextProcessor(),
            'image': ImageProcessor(),
            'audio': AudioProcessor(),
            'video': VideoProcessor()
        }
        self.fusion_strategy = 'parallel'

    def create_multimodal_prompt(self, inputs, task_description):
        """
        创建多模态提示

        Args:
            inputs: 多模态输入字典
            task_description: 任务描述

        Returns:
            dict: 创建的多模态提示
        """
        print(f"\n创建多模态提示: {task_description}")

        # 1. 检查可用模态
        available_modalities = self.check_available_modalities(inputs)
        print(f"可用模态: {available_modalities}")

        # 2. 处理各模态
        processed_modalities = {}
        for modality in available_modalities:
            print(f"  处理{modality}模态...")
            processed_modalities[modality] = self.process_modality(
                modality, inputs[modality]
            )

        # 3. 融合模态信息
        print("融合模态信息...")
        fused_information = self.fuse_modalities(
            processed_modalities, self.fusion_strategy
        )

        # 4. 构造最终提示
        print("构造最终提示...")
        final_prompt = self.construct_final_prompt(
            fused_information, task_description
        )

        return {
            'available_modalities': available_modalities,
            'processed_modalities': processed_modalities,
            'fused_information': fused_information,
            'final_prompt': final_prompt
        }

    def check_available_modalities(self, inputs):
        """检查可用模态"""
        available = []
        for modality, data in inputs.items():
            if data is not None and modality in self.modalities:
                available.append(modality)
        return available

    def process_modality(self, modality, data):
        """处理单个模态"""
        processor = self.modalities.get(modality)
        if processor:
            return processor.process(data)
        else:
            return f"未处理的{modality}数据: {str(data)[:100]}"

    def fuse_modalities(self, modalities, strategy):
        """融合模态信息"""
        if strategy == 'parallel':
            return self.parallel_fusion(modalities)
        elif strategy == 'sequential':
            return self.sequential_fusion(modalities)
        elif strategy == 'hierarchical':
            return self.hierarchical_fusion(modalities)
        else:
            return self.parallel_fusion(modalities)

    def parallel_fusion(self, modalities):
        """并行融合"""
        fusion_prompt = f"""
        整合以下多模态信息：

        {chr(10).join([f"{mod}: {info}" for mod, info in modalities.items()])}

        请进行并行整合：
        """
        return self.llm.generate(fusion_prompt, max_tokens=400)

    def sequential_fusion(self, modalities):
        """序列融合"""
        sequence = []
        for modality, info in modalities.items():
            sequence.append(f"[{modality}] {info}")

        fusion_prompt = f"""
        按序列处理以下多模态信息：

        {chr(10).join(sequence)}

        请进行序列整合：
        """
        return self.llm.generate(fusion_prompt, max_tokens=400)

    def hierarchical_fusion(self, modalities):
        """分层融合"""
        # 简化的分层融合
        return self.parallel_fusion(modalities)

    def construct_final_prompt(self, fused_information, task_description):
        """构造最终提示"""
        final_prompt = f"""
        基于以下多模态信息完成指定任务：

        任务描述：{task_description}

        多模态信息：
        {fused_information}

        请基于以上多模态信息完成指定任务。

        任务执行：
        """
        return self.llm.generate(final_prompt, max_tokens=600)

    def generate_multimodal_output(self, prompt_result):
        """生成多模态输出"""
        print("\n生成多模态输出...")

        prompt = prompt_result['final_prompt']
        return self.llm.generate(prompt)

class TextProcessor:
    """文本处理器"""
    def process(self, text_data):
        """处理文本数据"""
        if isinstance(text_data, str):
            # 文本分析和预处理
            processed = f"[文本内容] {text_data[:200]}..."
            return processed
        else:
            return f"[文本数据] {str(text_data)}"

class ImageProcessor:
    """图像处理器"""
    def process(self, image_data):
        """处理图像数据"""
        # 模拟图像处理
        processed = f"[图像内容] 图像特征提取完成 (模拟数据)"
        return processed

class AudioProcessor:
    """音频处理器"""
    def process(self, audio_data):
        """处理音频数据"""
        # 模拟音频处理
        processed = f"[音频内容] 音频特征提取完成 (模拟数据)"
        return processed

class VideoProcessor:
    """视频处理器"""
    def process(self, video_data):
        """处理视频数据"""
        # 模拟视频处理
        processed = f"[视频内容] 视频特征提取完成 (模拟数据)"
        return processed
```

### 任务2：高级多模态提示优化

**目标：**
实现高级多模态提示系统，包括跨模态对齐、自适应融合、提示优化等功能。

**步骤：高级多模态提示系统**
```python
class AdvancedMultimodalPromptSystem:
    """高级多模态提示系统"""
    def __init__(self, llm):
        self.llm = llm
        self.modalities = {
            'text': AdvancedTextProcessor(),
            'image': AdvancedImageProcessor(),
            'audio': AdvancedAudioProcessor(),
            'video': AdvancedVideoProcessor()
        }
        self.cross_modal_aligner = CrossModalityAlignment()
        self.modal_fusion = CrossModalFusion(llm)
        self.prompt_optimizer = MultimodalPromptOptimizer(llm)
        self.adaptation_manager = AdaptivePromptManager(llm)

    def create_advanced_prompt(self, inputs, task_description, context=None):
        """创建高级多模态提示"""
        print(f"\n创建高级多模态提示: {task_description}")

        # 1. 模态识别和预处理
        available_modalities = self.identify_and_preprocess(inputs)
        print(f"可用模态: {available_modalities}")

        # 2. 模态特征提取
        extracted_features = self.extract_modality_features(
            available_modalities, inputs
        )
        print("提取模态特征完成")

        # 3. 跨模态对齐
        aligned_features = self.cross_modal_aligner.align_modalities(
            'text', 'image', extracted_features  # 简化示例
        )
        print("跨模态对齐完成")

        # 4. 自适应融合
        fused_representation = self.modal_fusion.fuse_modalities(
            aligned_features, method='hybrid_fusion'
        )
        print("自适应融合完成")

        # 5. 上下文感知提示构造
        contextualized_prompt = self.construct_contextualized_prompt(
            fused_representation, task_description, context
        )

        # 6. 提示优化
        optimized_prompt = self.prompt_optimizer.optimize_multimodal_prompt(
            contextualized_prompt, "initial version"
        )
        print("提示优化完成")

        return {
            'available_modalities': available_modalities,
            'extracted_features': extracted_features,
            'aligned_features': aligned_features,
            'fused_representation': fused_representation,
            'contextualized_prompt': contextualized_prompt,
            'optimized_prompt': optimized_prompt
        }

    def identify_and_preprocess(self, inputs):
        """识别和预处理模态"""
        preprocessed_inputs = {}

        for modality, data in inputs.items():
            if modality in self.modalities:
                print(f"  预处理{modality}模态...")
                preprocessed_inputs[modality] = self.modalities[modality].preprocess(
                    data
                )

        return list(preprocessed_inputs.keys())

    def extract_modality_features(self, modalities, inputs):
        """提取模态特征"""
        features = {}

        for modality in modalities:
            if modality in inputs:
                features[modality] = self.modalities[modality].extract_features(
                    inputs[modality]
                )

        return features

    def construct_contextualized_prompt(self, fused_representation, task_description, context):
        """构造上下文感知提示"""
        context_info = self.format_context(context)

        contextualized_prompt = f"""
        基于以下上下文和融合的多模态信息，执行任务：

        任务：{task_description}

        上下文信息：
        {context_info}

        融合的多模态信息：
        {fused_representation}

        请基于以上信息完成指定任务。

        任务执行：
        """

        return self.llm.generate(contextualized_prompt, max_tokens=600)

    def format_context(self, context):
        """格式化上下文"""
        if not context:
            return "无额外上下文"
        return str(context)

    def adapt_prompt_to_user(self, prompt, user_preferences):
        """根据用户偏好调整提示"""
        return self.adaptation_manager.adapt_to_user(
            prompt, user_preferences
        )

    def evaluate_multimodal_understanding(self, prompt_result):
        """评估多模态理解质量"""
        evaluation_prompt = f"""
        评估以下多模态提示的理解质量：

        可用模态：{prompt_result['available_modalities']}
        融合信息：{prompt_result['fused_representation']}

        请评估：
        1. 模态对齐质量
        2. 信息融合效果
        3. 提示完整性

        评估结果：
        """
        return self.llm.generate(evaluation_prompt, max_tokens=300)

class AdvancedTextProcessor:
    """高级文本处理器"""
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_extractor = EntityExtractor()

    def preprocess(self, text_data):
        """预处理文本"""
        if isinstance(text_data, str):
            # 清理和标准化
            cleaned = text_data.strip()
            return cleaned
        return str(text_data)

    def extract_features(self, text_data):
        """提取文本特征"""
        features = {}

        # 情感分析
        sentiment = self.sentiment_analyzer.analyze(text_data)
        features['sentiment'] = sentiment

        # 实体提取
        entities = self.entity_extractor.extract(text_data)
        features['entities'] = entities

        # 关键词提取
        keywords = self.extract_keywords(text_data)
        features['keywords'] = keywords

        # 语义特征
        semantic_features = self.extract_semantic_features(text_data)
        features['semantic'] = semantic_features

        return features

    def extract_keywords(self, text):
        """提取关键词"""
        # 简化的关键词提取
        words = text.lower().split()
        stopwords = {'的', '了', '在', '是', '我', '你', '他', '这', '那'}
        keywords = [word for word in words if word not in stopwords and len(word) > 2]
        return keywords[:10]  # 返回前10个关键词

    def extract_semantic_features(self, text):
        """提取语义特征"""
        # 模拟语义特征提取
        return f"语义特征: {text[:50]}..."

class AdvancedImageProcessor:
    """高级图像处理器"""
    def preprocess(self, image_data):
        """预处理图像"""
        # 模拟图像预处理
        return f"预处理后的图像 (模拟数据)"

    def extract_features(self, image_data):
        """提取图像特征"""
        features = {}

        # 对象检测
        objects = self.detect_objects(image_data)
        features['objects'] = objects

        # 场景识别
        scene = self.recognize_scene(image_data)
        features['scene'] = scene

        # 颜色特征
        colors = self.extract_color_features(image_data)
        features['colors'] = colors

        # 纹理特征
        textures = self.extract_texture_features(image_data)
        features['textures'] = textures

        return features

    def detect_objects(self, image_data):
        """检测对象"""
        return ["对象1", "对象2", "对象3"]  # 模拟检测结果

    def recognize_scene(self, image_data):
        """识别场景"""
        return "室内场景"  # 模拟场景识别

    def extract_color_features(self, image_data):
        """提取颜色特征"""
        return {"dominant_colors": ["红色", "蓝色", "绿色"]}

    def extract_texture_features(self, image_data):
        """提取纹理特征"""
        return {"texture_type": "平滑"}

class AdvancedAudioProcessor:
    """高级音频处理器"""
    def preprocess(self, audio_data):
        """预处理音频"""
        return f"预处理后的音频 (模拟数据)"

    def extract_features(self, audio_data):
        """提取音频特征"""
        features = {}

        # 语音识别
        speech = self.recognize_speech(audio_data)
        features['speech'] = speech

        # 情感识别
        emotion = self.recognize_emotion(audio_data)
        features['emotion'] = emotion

        # 音频特征
        audio_features = self.extract_audio_features(audio_data)
        features['audio'] = audio_features

        return features

    def recognize_speech(self, audio_data):
        """识别语音"""
        return "识别的语音内容 (模拟)"

    def recognize_emotion(self, audio_data):
        """识别情感"""
        return "中性情感"  # 模拟情感识别

    def extract_audio_features(self, audio_data):
        """提取音频特征"""
        return {
            "frequency": "中频",
            "volume": "中等",
            "tone": "平稳"
        }

class AdvancedVideoProcessor:
    """高级视频处理器"""
    def preprocess(self, video_data):
        """预处理视频"""
        return f"预处理后的视频 (模拟数据)"

    def extract_features(self, video_data):
        """提取视频特征"""
        features = {}

        # 帧特征
        frame_features = self.extract_frame_features(video_data)
        features['frames'] = frame_features

        # 运动特征
        motion_features = self.extract_motion_features(video_data)
        features['motion'] = motion_features

        # 时间特征
        temporal_features = self.extract_temporal_features(video_data)
        features['temporal'] = temporal_features

        return features

    def extract_frame_features(self, video_data):
        """提取帧特征"""
        return {"key_frames": ["帧1", "帧2", "帧3"]}

    def extract_motion_features(self, video_data):
        """提取运动特征"""
        return {"motion_type": "缓慢移动"}

    def extract_temporal_features(self, video_data):
        """提取时间特征"""
        return {"duration": "10秒", "fps": "30"}

class SentimentAnalyzer:
    """情感分析器"""
    def analyze(self, text):
        """分析情感"""
        # 简化的情感分析
        return "中性"

class EntityExtractor:
    """实体提取器"""
    def extract(self, text):
        """提取实体"""
        # 简化的实体提取
        return ["实体1", "实体2"]

class AdaptivePromptManager:
    """自适应提示管理器"""
    def __init__(self, llm):
        self.llm = llm

    def adapt_to_user(self, prompt, user_preferences):
        """根据用户偏好调整"""
        if not user_preferences:
            return prompt

        adaptation_prompt = f"""
        根据以下用户偏好调整提示：

        原始提示：{prompt}

        用户偏好：{user_preferences}

        调整后的提示：
        """
        return self.llm.generate(adaptation_prompt, max_tokens=500)
```

### 任务3：多模态提示评估与优化

**目标：**
构建多模态提示系统的全面评估框架，分析系统性能和跨模态理解质量。

**步骤：评估与优化系统**
```python
class MultimodalPromptEvaluator:
    """多模态提示评估器"""
    def __init__(self, prompt_system):
        self.prompt_system = prompt_system
        self.evaluation_metrics = {
            'cross_modal_alignment': self.evaluate_cross_modal_alignment,
            'fusion_effectiveness': self.evaluate_fusion_effectiveness,
            'prompt_quality': self.evaluate_prompt_quality,
            'task_completion': self.evaluate_task_completion,
            'user_satisfaction': self.evaluate_user_satisfaction
        }

    def comprehensive_evaluation(self, test_cases):
        """
        综合评估多模态提示系统

        Args:
            test_cases: 测试用例列表

        Returns:
            dict: 评估结果
        """
        print("开始多模态提示系统综合评估...")
        print(f"测试用例数量: {len(test_cases)}")

        evaluation_results = []

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n测试用例 {i}/{len(test_cases)}: {test_case['name']}")

            try:
                # 创建多模态提示
                prompt_result = self.prompt_system.create_advanced_prompt(
                    test_case['inputs'],
                    test_case['task_description'],
                    test_case.get('context')
                )

                # 生成输出
                output = self.prompt_system.generate_multimodal_output(prompt_result)

                # 评估各项指标
                metric_scores = {}
                for metric_name, metric_func in self.evaluation_metrics.items():
                    try:
                        score = metric_func(prompt_result, output, test_case)
                        metric_scores[metric_name] = score
                        print(f"  {metric_name}: {score:.4f}")
                    except Exception as e:
                        print(f"  {metric_name}: 评估失败 - {e}")
                        metric_scores[metric_name] = 0.0

                evaluation_results.append({
                    'test_case': test_case,
                    'prompt_result': prompt_result,
                    'output': output,
                    'metric_scores': metric_scores,
                    'success': True
                })

                print(f"  ✓ 成功完成")

            except Exception as e:
                print(f"  ✗ 执行失败: {e}")
                evaluation_results.append({
                    'test_case': test_case,
                    'error': str(e),
                    'success': False
                })

        # 生成综合报告
        report = self.generate_comprehensive_report(evaluation_results)

        return report

    def evaluate_cross_modal_alignment(self, prompt_result, output, test_case):
        """评估跨模态对齐"""
        aligned_features = prompt_result.get('aligned_features', {})
        if not aligned_features:
            return 0.0

        # 评估对齐质量
        modalities = list(aligned_features.keys())
        if len(modalities) < 2:
            return 0.5  # 单模态无法评估对齐

        # 检查模态间的一致性
        consistency_score = self.assess_alignment_consistency(aligned_features)
        return consistency_score

    def assess_alignment_consistency(self, aligned_features):
        """评估对齐一致性"""
        # 简化的对齐一致性评估
        # 实际应用中需要更复杂的对齐质量评估
        return 0.8  # 模拟分数

    def evaluate_fusion_effectiveness(self, prompt_result, output, test_case):
        """评估融合有效性"""
        fused_representation = prompt_result.get('fused_representation', '')
        if not fused_representation:
            return 0.0

        # 使用LLM评估融合质量
        quality_prompt = f"""
        评估以下多模态融合信息的有效性：

        融合信息：{fused_representation}

        任务：{test_case['task_description']}

        请评分（0-1）：
        """
        # 这里需要LLM评估
        return 0.75  # 模拟评分

    def evaluate_prompt_quality(self, prompt_result, output, test_case):
        """评估提示质量"""
        optimized_prompt = prompt_result.get('optimized_prompt', '')
        if not optimized_prompt:
            return 0.5

        # 评估提示的完整性和清晰度
        quality_aspects = {
            'completeness': self.assess_prompt_completeness(optimized_prompt),
            'clarity': self.assess_prompt_clarity(optimized_prompt),
            'consistency': self.assess_prompt_consistency(optimized_prompt),
            'effectiveness': self.assess_prompt_effectiveness(optimized_prompt, test_case)
        }

        # 综合评分
        weights = {
            'completeness': 0.25,
            'clarity': 0.25,
            'consistency': 0.25,
            'effectiveness': 0.25
        }

        quality_score = sum(
            quality_aspects[aspect] * weights[aspect]
            for aspect in quality_aspects
        )

        return quality_score

    def assess_prompt_completeness(self, prompt):
        """评估提示完整性"""
        # 检查提示是否包含所有必要元素
        necessary_elements = ['任务', '多模态', '指示']
        return sum(1 for element in necessary_elements if element in prompt) / len(necessary_elements)

    def assess_prompt_clarity(self, prompt):
        """评估提示清晰度"""
        # 基于文本长度和结构评估
        if len(prompt) < 100:
            return 0.3
        elif len(prompt) > 1000:
            return 0.6
        else:
            return 0.8

    def assess_prompt_consistency(self, prompt):
        """评估提示一致性"""
        # 检查提示内部的一致性
        return 0.8  # 模拟分数

    def assess_prompt_effectiveness(self, prompt, test_case):
        """评估提示有效性"""
        # 基于任务完成度评估
        return 0.7  # 模拟分数

    def evaluate_task_completion(self, prompt_result, output, test_case):
        """评估任务完成度"""
        expected_output = test_case.get('expected_output', '')

        if not expected_output:
            # 基于任务类型评估完成度
            task_type = test_case.get('task_type', 'general')
            return self.assess_task_completion_by_type(output, task_type)

        # 实际输出与期望输出的比较
        return self.compare_output_with_expected(output, expected_output)

    def assess_task_completion_by_type(self, output, task_type):
        """基于任务类型评估完成度"""
        completion_indicators = {
            'classification': self.check_classification_completion,
            'generation': self.check_generation_completion,
            'analysis': self.check_analysis_completion,
            'qa': self.check_qa_completion
        }

        checker = completion_indicators.get(task_type, self.check_general_completion)
        return checker(output)

    def check_classification_completion(self, output):
        """检查分类任务完成"""
        return 0.8  # 模拟分数

    def check_generation_completion(self, output):
        """检查生成任务完成"""
        return len(output) / 500 if output else 0  # 基于输出长度

    def check_analysis_completion(self, output):
        """检查分析任务完成"""
        analysis_keywords = ['分析', '结果', '结论']
        return sum(1 for keyword in analysis_keywords if keyword in output) / len(analysis_keywords)

    def check_qa_completion(self, output):
        """检查问答任务完成"""
        return 0.8 if output else 0.0

    def check_general_completion(self, output):
        """检查一般任务完成"""
        return 0.7 if output else 0.0

    def compare_output_with_expected(self, output, expected):
        """比较实际输出与期望输出"""
        # 使用语义相似度比较
        similarity = self.calculate_semantic_similarity(output, expected)
        return similarity

    def calculate_semantic_similarity(self, text1, text2):
        """计算语义相似度"""
        # 简化的相似度计算
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0

    def evaluate_user_satisfaction(self, prompt_result, output, test_case):
        """评估用户满意度"""
        # 基于多个因素评估满意度
        satisfaction_factors = {
            'usefulness': self.assess_usefulness(output, test_case),
            'ease_of_understanding': self.assess_ease_of_understanding(output),
            'relevance': self.assess_relevance(output, test_case),
            'completeness': self.assess_satisfaction_completeness(output)
        }

        # 综合满意度评分
        weights = {
            'usefulness': 0.4,
            'ease_of_understanding': 0.2,
            'relevance': 0.3,
            'completeness': 0.1
        }

        satisfaction_score = sum(
            satisfaction_factors[factor] * weights[factor]
            for factor in satisfaction_factors
        )

        return satisfaction_score

    def assess_usefulness(self, output, test_case):
        """评估有用性"""
        # 简化的有用性评估
        return 0.8  # 模拟分数

    def assess_ease_of_understanding(self, output):
        """评估易理解性"""
        # 基于文本复杂性评估
        return 0.7 if output else 0.0

    def assess_relevance(self, output, test_case):
        """评估相关性"""
        task_keywords = test_case['task_description'].lower().split()
        output_lower = output.lower()

        relevance = sum(1 for keyword in task_keywords if keyword in output_lower)
        return relevance / len(task_keywords) if task_keywords else 0

    def assess_satisfaction_completeness(self, output):
        """评估完整性"""
        # 基于输出长度和结构评估完整性
        if not output:
            return 0.0

        completion_indicators = ['完成', '总结', '结论']
        return sum(1 for indicator in completion_indicators if indicator in output) / len(completion_indicators)

    def generate_comprehensive_report(self, evaluation_results):
        """生成综合评估报告"""
        successful_results = [r for r in evaluation_results if r['success']]
        failed_results = [r for r in evaluation_results if not r['success']]

        # 计算总体指标
        overall_metrics = {}
        for metric_name in self.evaluation_metrics.keys():
            scores = [
                r['metric_scores'][metric_name]
                for r in successful_results
                if 'metric_scores' in r
            ]
            overall_metrics[metric_name] = sum(scores) / len(scores) if scores else 0.0

        # 生成建议
        recommendations = self.generate_improvement_recommendations(overall_metrics)

        report = {
            'summary': {
                'total_test_cases': len(evaluation_results),
                'successful_cases': len(successful_results),
                'failed_cases': len(failed_results),
                'success_rate': len(successful_results) / len(evaluation_results),
                'overall_metrics': overall_metrics
            },
            'detailed_results': evaluation_results,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

        # 打印总结
        print("\n" + "=" * 60)
        print("多模态提示系统评估总结")
        print("=" * 60)
        print(f"测试用例总数: {len(evaluation_results)}")
        print(f"成功用例: {len(successful_results)}")
        print(f"失败用例: {len(failed_results)}")
        print(f"成功率: {report['summary']['success_rate']:.1%}")

        print("\n各项指标评分:")
        for metric, score in overall_metrics.items():
            print(f"  {metric}: {score:.4f}")

        return report

    def generate_improvement_recommendations(self, metrics):
        """生成改进建议"""
        recommendations = []

        if metrics.get('cross_modal_alignment', 0) < 0.7:
            recommendations.append(
                "改进跨模态对齐：优化模态对齐算法，提高不同模态间的语义一致性"
            )

        if metrics.get('fusion_effectiveness', 0) < 0.6:
            recommendations.append(
                "增强融合有效性：改进多模态融合策略，提高信息整合质量"
            )

        if metrics.get('prompt_quality', 0) < 0.7:
            recommendations.append(
                "提升提示质量：优化提示设计模板，提高提示的完整性和清晰度"
            )

        if metrics.get('task_completion', 0) < 0.7:
            recommendations.append(
                "提高任务完成度：改进提示执行策略，确保任务要求的充分满足"
            )

        if metrics.get('user_satisfaction', 0) < 0.7:
            recommendations.append(
                "增强用户满意度：根据用户反馈优化系统响应质量和用户体验"
            )

        if not recommendations:
            recommendations.append("系统性能优秀，可考虑在更复杂的多模态任务上进一步测试")

        return recommendations
```

## 深度思考

### 多模态提示的认知科学基础

**多感官整合理论**

多模态提示模拟了人类的多感官整合机制：
- **视觉皮层**：处理图像信息
- **听觉皮层**：处理音频信息
- **语言皮层**：处理文本信息
- **联合皮层**：整合多模态信息

```python
class SensoryIntegrationModel:
    """感官整合模型"""
    def __init__(self):
        self.sensory_cortices = {
            'visual': VisualCortex(),
            'auditory': AuditoryCortex(),
            'language': LanguageCortex(),
            'integration': IntegrationCortex()
        }

    def integrate_multimodal_sensory(self, sensory_inputs):
        """整合多感官输入"""
        # 1. 各感官独立处理
        processed_senses = {}
        for sense, input_data in sensory_inputs.items():
            if sense in self.sensory_cortices:
                processed_senses[sense] = self.sensory_cortices[sense].process(
                    input_data
                )

        # 2. 联合皮层整合
        integrated_representation = self.sensory_cortices['integration'].integrate(
            processed_senses
        )

        return integrated_representation

    def attention_based_integration(self, sensory_inputs, attention_weights):
        """基于注意力的整合"""
        # 应用注意力权重
        weighted_inputs = {}
        for sense, input_data in sensory_inputs.items():
            weight = attention_weights.get(sense, 1.0)
            weighted_inputs[sense] = input_data * weight

        # 整合加权后的输入
        return self.integrate_multimodal_sensory(weighted_inputs)

class VisualCortex:
    """视觉皮层"""
    def process(self, image_data):
        """处理视觉信息"""
        # 模拟视觉处理层次
        return {
            'low_level': self.extract_low_level_features(image_data),
            'mid_level': self.extract_mid_level_features(image_data),
            'high_level': self.extract_high_level_features(image_data)
        }

    def extract_low_level_features(self, image_data):
        """提取低级特征（边缘、纹理、颜色）"""
        return "低级视觉特征"

    def extract_mid_level_features(self, image_data):
        """提取中级特征（形状、物体）"""
        return "中级视觉特征"

    def extract_high_level_features(self, image_data):
        """提取高级特征（场景、语义）"""
        return "高级视觉特征"

class AuditoryCortex:
    """听觉皮层"""
    def process(self, audio_data):
        """处理听觉信息"""
        return {
            'spectral': self.extract_spectral_features(audio_data),
            'temporal': self.extract_temporal_features(audio_data),
            'phonetic': self.extract_phonetic_features(audio_data),
            'semantic': self.extract_semantic_features(audio_data)
        }

    def extract_spectral_features(self, audio_data):
        """提取频谱特征"""
        return "频谱特征"

    def extract_temporal_features(self, audio_data):
        """提取时间特征"""
        return "时间特征"

    def extract_phonetic_features(self, audio_data):
        """提取语音特征"""
        return "语音特征"

    def extract_semantic_features(self, audio_data):
        """提取语义特征"""
        return "语义特征"

class LanguageCortex:
    """语言皮层"""
    def process(self, text_data):
        """处理语言信息"""
        return {
            'phonological': self.extract_phonological_features(text_data),
            'syntactic': self.extract_syntactic_features(text_data),
            'semantic': self.extract_semantic_features(text_data),
            'pragmatic': self.extract_pragmatic_features(text_data)
        }

    def extract_phonological_features(self, text_data):
        """提取语音学特征"""
        return "语音学特征"

    def extract_syntactic_features(self, text_data):
        """提取句法特征"""
        return "句法特征"

    def extract_semantic_features(self, text_data):
        """提取语义特征"""
        return "语义特征"

    def extract_pragmatic_features(self, text_data):
        """提取语用特征"""
        return "语用特征"

class IntegrationCortex:
    """联合皮层"""
    def integrate(self, processed_senses):
        """整合多感官信息"""
        # 模拟跨模态整合过程
        integration_prompt = f"""
        整合以下多感官处理结果：

        {processed_senses}

        请生成统一的多感官表示：
        """
        # 这里需要实际的整合逻辑
        return f"整合的多感官表示: {processed_senses}"
```

**跨模态同步机制**

多模态提示需要实现跨模态的同步：
```python
class CrossModalSynchronization:
    """跨模态同步机制"""
    def __init__(self):
        self.synchronization_strategies = [
            'temporal',
            'semantic',
            'structural',
            'attentional'
        ]

    def synchronize_modalities(self, modality_features, sync_strategy='temporal'):
        """同步模态"""
        if sync_strategy == 'temporal':
            return self.temporal_synchronization(modality_features)
        elif sync_strategy == 'semantic':
            return self.semantic_synchronization(modality_features)
        elif sync_strategy == 'structural':
            return self.structural_synchronization(modality_features)
        elif sync_strategy == 'attentional':
            return self.attentional_synchronization(modality_features)
        else:
            return self.temporal_synchronization(modality_features)

    def temporal_synchronization(self, features):
        """时间同步"""
        # 基于时间戳同步
        synchronized = {}
        timestamps = set()

        for modality, feature in features.items():
            if 'timestamp' in feature:
                timestamps.add(feature['timestamp'])

        for timestamp in sorted(timestamps):
            synchronized[timestamp] = {}
            for modality, feature in features.items():
                if feature.get('timestamp') == timestamp:
                    synchronized[timestamp][modality] = feature

        return synchronized

    def semantic_synchronization(self, features):
        """语义同步"""
        # 基于语义相似度同步
        semantic_groups = self.group_by_semantic_similarity(features)
        return semantic_groups

    def group_by_semantic_similarity(self, features):
        """按语义相似度分组"""
        # 简化的语义分组
        groups = {'high_similarity': [], 'medium_similarity': [], 'low_similarity': []}

        modalities = list(features.keys())
        for i, mod1 in enumerate(modalities):
            for mod2 in modalities[i+1:]:
                similarity = self.calculate_semantic_similarity(
                    features[mod1], features[mod2]
                )

                if similarity > 0.7:
                    groups['high_similarity'].append((mod1, mod2, similarity))
                elif similarity > 0.4:
                    groups['medium_similarity'].append((mod1, mod2, similarity))
                else:
                    groups['low_similarity'].append((mod1, mod2, similarity))

        return groups

    def calculate_semantic_similarity(self, feature1, feature2):
        """计算语义相似度"""
        # 简化的相似度计算
        return 0.8  # 模拟相似度

    def structural_synchronization(self, features):
        """结构同步"""
        # 基于结构对齐同步
        return self.align_structural_patterns(features)

    def align_structural_patterns(self, features):
        """对齐结构模式"""
        return f"结构对齐后的特征: {features}"

    def attentional_synchronization(self, features):
        """注意力同步"""
        # 基于注意力机制同步
        attention_weights = self.compute_attention_weights(features)
        return self.apply_attention_synchronization(features, attention_weights)

    def compute_attention_weights(self, features):
        """计算注意力权重"""
        return {modality: 1.0 / len(features) for modality in features}

    def apply_attention_synchronization(self, features, weights):
        """应用注意力同步"""
        synchronized = {}
        for modality, feature in features.items():
            weight = weights.get(modality, 1.0)
            synchronized[modality] = {
                'feature': feature,
                'weight': weight,
                'synchronized': f"注意力同步({weight:.2f}): {feature}"
            }
        return synchronized
```

### 多模态提示的技术挑战与解决方案

**1. 模态异构性挑战**

挑战：不同模态的数据结构和表示方式差异巨大

解决方案：
```python
class HeterogeneityHandler:
    """异构性处理器"""
    def __init__(self):
        self.modality_encoders = {
            'text': TextEncoder(),
            'image': ImageEncoder(),
            'audio': AudioEncoder(),
            'video': VideoEncoder()
        }
        self.unified_space_projector = UnifiedSpaceProjector()

    def handle_modality_heterogeneity(self, heterogeneous_inputs):
        """处理模态异构性"""
        # 1. 模态特定编码
        modality_specific_codes = {}
        for modality, data in heterogeneous_inputs.items():
            if modality in self.modality_encoders:
                modality_specific_codes[modality] = self.modality_encoders[modality].encode(
                    data
                )

        # 2. 投影到统一空间
        unified_representations = self.unified_space_projector.project_to_unified_space(
            modality_specific_codes
        )

        # 3. 异构性补偿
        compensated_representations = self.compensate_heterogeneity(
            unified_representations
        )

        return compensated_representations

    def compensate_heterogeneity(self, unified_representations):
        """异构性补偿"""
        compensation_prompt = f"""
        补偿以下统一空间表示中的异构性：

        表示：{unified_representations}

        请进行异构性补偿：
        """
        # 这里需要实际的补偿逻辑
        return f"补偿后的表示: {unified_representations}"

class TextEncoder:
    """文本编码器"""
    def encode(self, text_data):
        return f"文本编码: {text_data[:50]}..."

class ImageEncoder:
    """图像编码器"""
    def encode(self, image_data):
        return f"图像编码: <图像特征向量>"

class AudioEncoder:
    """音频编码器"""
    def encode(self, audio_data):
        return f"音频编码: <音频特征向量>"

class VideoEncoder:
    """视频编码器"""
    def encode(self, video_data):
        return f"视频编码: <视频特征向量>"

class UnifiedSpaceProjector:
    """统一空间投影器"""
    def project_to_unified_space(self, modality_codes):
        """投影到统一空间"""
        projection_prompt = f"""
        将以下模态特定编码投影到统一语义空间：

        编码：{modality_codes}

        请生成统一空间表示：
        """
        # 这里需要实际的投影逻辑
        return f"统一空间表示: {modality_codes}"
```

**2. 模态缺失处理**

挑战：某些模态可能缺失或不可用

解决方案：
```python
class MissingModalityHandler:
    """缺失模态处理器"""
    def __init__(self, llm):
        self.llm = llm
        self.imputation_strategies = {
            'prediction': self.predict_missing_modality,
            'generation': self.generate_missing_modality,
            'compensation': self.compensate_missing_modality,
            'adaptation': self.adapt_to_missing_modality
        }

    def handle_missing_modalities(self, available_modalities, task_description):
        """处理缺失模态"""
        # 1. 识别缺失模态
        all_expected_modalities = ['text', 'image', 'audio', 'video']
        missing_modalities = [
            mod for mod in all_expected_modalities
            if mod not in available_modalities
        ]

        if not missing_modalities:
            return {'status': 'complete', 'available': available_modalities}

        # 2. 选择处理策略
        handling_strategy = self.select_handling_strategy(
            missing_modalities, task_description
        )

        # 3. 执行处理
        result = self.execute_handling_strategy(
            handling_strategy, missing_modalities, available_modalities
        )

        return result

    def select_handling_strategy(self, missing_modalities, task_description):
        """选择处理策略"""
        if len(missing_modalities) == 1:
            return 'prediction'  # 单模态缺失用预测
        elif len(missing_modalities) >= 2:
            return 'adaptation'  # 多模态缺失用适应
        else:
            return 'compensation'  # 部分缺失用补偿

    def execute_handling_strategy(self, strategy, missing, available):
        """执行处理策略"""
        handler = self.imputation_strategies.get(strategy, self.compensate_missing_modality)

        if strategy == 'prediction':
            return handler(missing[0], available)
        elif strategy == 'generation':
            return handler(missing, available)
        elif strategy == 'compensation':
            return handler(available)
        elif strategy == 'adaptation':
            return handler(missing, available)

    def predict_missing_modality(self, missing_modality, available):
        """预测缺失模态"""
        prediction_prompt = f"""
        基于可用的模态信息，预测缺失的{missing_modality}模态：

        可用模态：{available}
        缺失模态：{missing_modality}

        请预测缺失模态的内容：
        """
        predicted = self.llm.generate(prediction_prompt, max_tokens=300)
        return {
            'strategy': 'prediction',
            'predicted_modality': missing_modality,
            'prediction': predicted
        }

    def generate_missing_modality(self, missing_modalities, available):
        """生成缺失模态"""
        generation_prompt = f"""
        生成以下缺失模态的内容：

        可用模态：{available}
        缺失模态：{missing_modalities}

        请生成缺失模态的内容：
        """
        generated = self.llm.generate(generation_prompt, max_tokens=400)
        return {
            'strategy': 'generation',
            'generated_modalities': missing_modalities,
            'generation': generated
        }

    def compensate_missing_modality(self, available):
        """补偿缺失模态"""
        compensation_prompt = f"""
        在没有某些模态的情况下，优化基于可用模态的处理：

        可用模态：{available}

        请提供补偿策略：
        """
        compensation = self.llm.generate(compensation_prompt, max_tokens=300)
        return {
            'strategy': 'compensation',
            'available_modalities': available,
            'compensation_strategy': compensation
        }

    def adapt_to_missing_modality(self, missing, available):
        """适应缺失模态"""
        adaptation_prompt = f"""
        调整任务处理方式以适应缺失的模态：

        可用模态：{available}
        缺失模态：{missing}

        请提出适应策略：
        """
        adaptation = self.llm.generate(adaptation_prompt, max_tokens=350)
        return {
            'strategy': 'adaptation',
            'missing_modalities': missing,
            'available_modalities': available,
            'adaptation': adaptation
        }
```

### 多模态提示的创新应用场景

**1. 智能教育助手**
```python
class IntelligentEducationAssistant:
    """智能教育助手"""
    def __init__(self, multimodal_system):
        self.multimodal_system = multimodal_system
        self.educational_tools = {
            'textbook_analyzer': TextbookAnalyzer(),
            'video_lecturer': VideoLecturer(),
            'audio_tutor': AudioTutor(),
            'interactive_demo': InteractiveDemo()
        }

    def assist_learning(self, learning_materials, student_preferences):
        """协助学习"""
        # 1. 分析学习材料（多模态）
        materials_analysis = self.analyze_learning_materials(learning_materials)

        # 2. 根据学生偏好调整
        adapted_materials = self.adapt_to_student_preferences(
            materials_analysis, student_preferences
        )

        # 3. 生成多模态学习提示
        learning_prompts = self.generate_multimodal_learning_prompts(
            adapted_materials
        )

        return learning_prompts

    def analyze_learning_materials(self, materials):
        """分析学习材料"""
        # 使用多模态系统分析不同类型的学习材料
        analysis_prompt = f"""
        分析以下多模态学习材料：

        材料类型：{list(materials.keys())}
        具体内容：{materials}

        请提供学习要点分析：
        """
        return self.multimodal_system.llm.generate(analysis_prompt, max_tokens=500)

    def adapt_to_student_preferences(self, analysis, preferences):
        """适应学生偏好"""
        adaptation_prompt = f"""
        根据学生偏好调整学习材料分析：

        原始分析：{analysis}
        学生偏好：{preferences}

        请提供适应性分析：
        """
        return self.multimodal_system.llm.generate(adaptation_prompt, max_tokens=400)

    def generate_multimodal_learning_prompts(self, adapted_materials):
        """生成多模态学习提示"""
        prompt_templates = {
            'visual': "请观察并理解以下视觉内容：{content}",
            'auditory': "请聆听并理解以下音频内容：{content}",
            'textual': "请阅读并理解以下文本内容：{content}",
            'interactive': "请参与以下互动学习：{content}"
        }

        return prompt_templates

class TextbookAnalyzer:
    """教科书分析器"""
    def analyze(self, textbook_content):
        return "教科书分析结果"

class VideoLecturer:
    """视频讲师"""
    def present(self, video_content):
        return "视频讲解"

class AudioTutor:
    """音频导师"""
    def tutor(self, audio_content):
        return "音频辅导"

class InteractiveDemo:
    """互动演示"""
    def demonstrate(self, demo_content):
        return "互动演示"
```

**2. 医疗诊断辅助系统**
```python
class MedicalDiagnosisAssistant:
    """医疗诊断辅助系统"""
    def __init__(self, multimodal_system):
        self.multimodal_system = multimodal_system
        self.medical_tools = {
            'image_analyzer': MedicalImageAnalyzer(),
            'symptom_extractor': SymptomExtractor(),
            'lab_result_reader': LabResultReader(),
            'history_analyzer': MedicalHistoryAnalyzer()
        }

    def assist_diagnosis(self, patient_data):
        """协助诊断"""
        # 1. 分析多模态患者数据
        multimodal_analysis = self.analyze_patient_data_multimodal(patient_data)

        # 2. 生成诊断提示
        diagnostic_prompts = self.generate_diagnostic_prompts(
            multimodal_analysis
        )

        # 3. 提供诊断建议
        diagnostic_suggestions = self.provide_diagnostic_suggestions(
            diagnostic_prompts
        )

        return diagnostic_suggestions

    def analyze_patient_data_multimodal(self, patient_data):
        """多模态分析患者数据"""
        analysis_prompt = f"""
        基于以下多模态患者数据进行分析：

        患者数据：{patient_data}

        请提供综合分析：
        """
        return self.multimodal_system.llm.generate(analysis_prompt, max_tokens=500)

    def generate_diagnostic_prompts(self, analysis):
        """生成诊断提示"""
        prompt = f"""
        基于患者数据分析，生成诊断相关提示：

        分析：{analysis}

        请生成诊断提示：
        """
        return self.multimodal_system.llm.generate(prompt, max_tokens=400)

    def provide_diagnostic_suggestions(self, prompts):
        """提供诊断建议"""
        suggestion_prompt = f"""
        基于诊断提示，提供专业的诊断建议：

        提示：{prompts}

        请提供建议（注意：仅供参考，非最终诊断）：
        """
        return self.multimodal_system.llm.generate(suggestion_prompt, max_tokens=400)

class MedicalImageAnalyzer:
    """医疗图像分析器"""
    def analyze(self, medical_image):
        return "医疗图像分析结果"

class SymptomExtractor:
    """症状提取器"""
    def extract(self, patient_description):
        return "症状提取结果"

class LabResultReader:
    """实验室结果读取器"""
    def read(self, lab_results):
        return "实验室结果分析"

class MedicalHistoryAnalyzer:
    """病史分析器"""
    def analyze(self, medical_history):
        return "病史分析结果"
```

## 质量评估

### 多模态提示系统的质量评估框架

**1. 跨模态理解质量评估（Cross-Modal Understanding Quality）**

评估多模态提示系统的跨模态理解能力：

```python
def evaluate_cross_modal_understanding(multimodal_results, test_cases):
    """
    评估跨模态理解质量
    """
    quality_metrics = {
        'modality_alignment_accuracy': evaluate_modality_alignment_accuracy,
        'cross_modal_reasoning': evaluate_cross_modal_reasoning,
        'information_integration': evaluate_information_integration,
        'semantic_consistency': evaluate_semantic_consistency
    }

    evaluation_results = {}

    for metric_name, calculator in quality_metrics.items():
        scores = []
        for result in multimodal_results:
            score = calculator(result, test_cases)
            scores.append(score)

        avg_score = sum(scores) / len(scores)
        evaluation_results[metric_name] = avg_score

    return evaluation_results

def evaluate_modality_alignment_accuracy(result, test_cases):
    """评估模态对齐准确性"""
    aligned_features = result.get('aligned_features', {})
    if not aligned_features:
        return 0.0

    # 评估不同模态间的对齐质量
    modalities = list(aligned_features.keys())
    if len(modalities) < 2:
        return 1.0  # 单模态无需对齐

    alignment_scores = []
    for i in range(len(modalities)):
        for j in range(i + 1, len(modalities)):
            mod1, mod2 = modalities[i], modalities[j]
            alignment_score = assess_pair_alignment(
                aligned_features[mod1], aligned_features[mod2]
            )
            alignment_scores.append(alignment_score)

    return sum(alignment_scores) / len(alignment_scores)

def assess_pair_alignment(feature1, feature2):
    """评估模态对的对齐质量"""
    # 简化的对齐质量评估
    return 0.8  # 模拟分数

def evaluate_cross_modal_reasoning(result, test_cases):
    """评估跨模态推理能力"""
    fused_representation = result.get('fused_representation', '')
    if not fused_representation:
        return 0.0

    # 评估融合表示的推理质量
    reasoning_quality = assess_reasoning_quality(fused_representation)
    return reasoning_quality

def assess_reasoning_quality(fused_representation):
    """评估推理质量"""
    # 基于推理指示词评估
    reasoning_indicators = ['因此', '所以', '基于', '根据', '由于', '推理', '分析']
    indicator_count = sum(1 for indicator in reasoning_indicators if indicator in fused_representation)

    return min(indicator_count / len(reasoning_indicators), 1.0)

def evaluate_information_integration(result, test_cases):
    """评估信息整合效果"""
    fused_representation = result.get('fused_representation', '')
    available_modalities = result.get('available_modalities', [])

    if not fused_representation or not available_modalities:
        return 0.0

    # 评估整合信息的完整性
    integration_completeness = assess_integration_completeness(
        fused_representation, available_modalities
    )

    return integration_completeness

def assess_integration_completeness(representation, modalities):
    """评估整合完整性"""
    # 检查是否包含所有模态的信息
    modality_mentions = sum(1 for mod in modalities if mod in representation)
    return modality_mentions / len(modalities)

def evaluate_semantic_consistency(result, test_cases):
    """评估语义一致性"""
    output = result.get('output', '')
    if not output:
        return 0.0

    # 评估输出内容的语义一致性
    consistency_score = assess_output_consistency(output)
    return consistency_score

def assess_output_consistency(output):
    """评估输出一致性"""
    # 简化的语义一致性评估
    # 实际应用中需要更复杂的语义分析
    return 0.8  # 模拟分数
```

**2. 多模态提示有效性评估（Multimodal Prompt Effectiveness）**

评估多模态提示的有效性：

```python
def evaluate_multimodal_prompt_effectiveness(multimodal_results, test_cases):
    """
    评估多模态提示有效性
    """
    effectiveness_metrics = {
        'prompt_completeness': evaluate_prompt_completeness,
        'modal_coverage': evaluate_modal_coverage,
        'fusion_effectiveness': evaluate_fusion_effectiveness,
        'task_adaptation': evaluate_task_adaptation
    }

    evaluation_results = {}

    for metric_name, calculator in effectiveness_metrics.items():
        scores = []
        for result in multimodal_results:
            score = calculator(result, test_cases)
            scores.append(score)

        avg_score = sum(scores) / len(scores)
        evaluation_results[metric_name] = avg_score

    return evaluation_results

def evaluate_prompt_completeness(result, test_cases):
    """评估提示完整性"""
    optimized_prompt = result.get('optimized_prompt', '')
    if not optimized_prompt:
        return 0.0

    # 检查提示是否包含所有必要元素
    necessary_elements = [
        '任务', '多模态', '指示', '信息', '完成'
    ]

    element_scores = []
    for element in necessary_elements:
        if element in optimized_prompt:
            element_scores.append(1.0)
        else:
            element_scores.append(0.0)

    return sum(element_scores) / len(element_scores)

def evaluate_modal_coverage(result, test_cases):
    """评估模态覆盖率"""
    available_modalities = result.get('available_modalities', [])
    expected_modalities = test_cases.get('expected_modalities', [])

    if not expected_modalities:
        return 1.0

    covered_modalities = set(available_modalities) & set(expected_modalities)
    return len(covered_modalities) / len(expected_modalities)

def evaluate_fusion_effectiveness(result, test_cases):
    """评估融合有效性"""
    fused_representation = result.get('fused_representation', '')
    if not fused_representation:
        return 0.0

    # 评估融合表示的质量
    fusion_quality = assess_fusion_quality(fused_representation)
    return fusion_quality

def assess_fusion_quality(fused_representation):
    """评估融合质量"""
    # 基于融合指示词评估
    fusion_indicators = ['整合', '融合', '结合', '综合', '统一']
    indicator_count = sum(1 for indicator in fusion_indicators if indicator in fused_representation)

    return min(indicator_count / len(fusion_indicators), 1.0)

def evaluate_task_adaptation(result, test_cases):
    """评估任务适应性"""
    task_description = test_cases.get('task_description', '')
    adapted_prompt = result.get('optimized_prompt', '')

    if not task_description or not adapted_prompt:
        return 0.5

    # 评估提示是否适应任务需求
    adaptation_quality = assess_task_adaptation_quality(
        task_description, adapted_prompt
    )

    return adaptation_quality

def assess_task_adaptation_quality(task, prompt):
    """评估任务适应性质量"""
    # 检查提示是否响应任务需求
    task_keywords = task.lower().split()
    prompt_lower = prompt.lower()

    keyword_matches = sum(1 for keyword in task_keywords if keyword in prompt_lower)
    return keyword_matches / len(task_keywords)
```

### 实际评估案例

**案例1：复杂多模态任务评估**

```python
def evaluate_complex_multimodal_task(multimodal_system, complex_tasks):
    """
    评估多模态系统在复杂任务上的表现
    """
    evaluation_results = []

    for task in complex_tasks:
        print(f"\n评估复杂多模态任务: {task['name']}")

        # 执行多模态提示系统
        result = multimodal_system.create_advanced_prompt(
            task['inputs'], task['task_description']
        )

        # 评估维度
        complexity_score = evaluate_complexity_handling(result, task)
        integration_score = evaluate_multimodal_integration(result, task)
        efficiency_score = evaluate_processing_efficiency(result, task)
        robustness_score = evaluate_robustness(result, task)

        evaluation_results.append({
            'task': task,
            'result': result,
            'complexity_score': complexity_score,
            'integration_score': integration_score,
            'efficiency_score': efficiency_score,
            'robustness_score': robustness_score
        })

    # 计算总体表现
    overall_performance = {
        'average_complexity_handling': sum(r['complexity_score'] for r in evaluation_results) / len(evaluation_results),
        'average_integration': sum(r['integration_score'] for r in evaluation_results) / len(evaluation_results),
        'average_efficiency': sum(r['efficiency_score'] for r in evaluation_results) / len(evaluation_results),
        'average_robustness': sum(r['robustness_score'] for r in evaluation_results) / len(evaluation_results)
    }

    return {
        'detailed_results': evaluation_results,
        'overall_performance': overall_performance
    }

def evaluate_complexity_handling(result, task):
    """评估复杂度处理能力"""
    available_modalities = len(result.get('available_modalities', []))
    processing_steps = len(result.get('extracted_features', []))

    # 复杂度处理得分
    complexity_score = min((available_modalities + processing_steps) / 10, 1.0)
    return complexity_score

def evaluate_multimodal_integration(result, task):
    """评估多模态整合效果"""
    aligned_features = result.get('aligned_features', {})
    fused_representation = result.get('fused_representation', '')

    # 整合质量评估
    if not aligned_features or not fused_representation:
        return 0.0

    # 基于对齐和融合质量评估
    alignment_quality = len(aligned_features) / 4.0  # 假设最多4个模态
    fusion_quality = 0.8 if fused_representation else 0.0

    return (alignment_quality + fusion_quality) / 2

def evaluate_processing_efficiency(result, task):
    """评估处理效率"""
    processing_time = result.get('processing_time', 0)
    num_modalities = len(result.get('available_modalities', []))

    if num_modalities == 0:
        return 0.0

    # 效率评估：模态数/处理时间
    efficiency = num_modalities / max(processing_time, 0.1)
    return min(efficiency / 10, 1.0)  # 归一化到0-1

def evaluate_robustness(result, task):
    """评估鲁棒性"""
    # 鲁棒性：成功处理的模态比例
    available = len(result.get('available_modalities', []))
    expected = len(task.get('expected_modalities', []))

    if expected == 0:
        return 1.0

    return available / expected
```

## 完整学习框架

### 学习路径规划

**阶段1：基础理解（1周）**
- 理解多模态提示的基本概念和原理
- 学习不同模态的特征和表示方法
- 实现简单的多模态提示系统

**阶段2：系统实现（1-2周）**
- 构建完整的多模态提示流水线
- 实现模态对齐和特征融合
- 开发跨模态推理能力

**阶段3：优化提升（1周）**
- 实现高级融合和对齐算法
- 构建性能评估框架
- 增强系统的鲁棒性和适应性

**阶段4：应用实践（1周）**
- 在特定领域部署多模态系统
- 测试和调优系统性能
- 总结最佳实践

### 项目实践体系

**项目1：多媒体内容理解系统**
```python
class MultimediaContentUnderstandingSystem:
    """多媒体内容理解系统"""
    def __init__(self, multimodal_system):
        self.multimodal_system = multimodal_system
        self.content_analyzers = {
            'video': VideoContentAnalyzer(),
            'image': ImageContentAnalyzer(),
            'audio': AudioContentAnalyzer(),
            'text': TextContentAnalyzer()
        }

    def understand_content(self, multimedia_content):
        """理解多媒体内容"""
        # 1. 分析各类型内容
        analysis_results = {}
        for content_type, content_data in multimedia_content.items():
            if content_type in self.content_analyzers:
                analysis_results[content_type] = self.content_analyzers[content_type].analyze(
                    content_data
                )

        # 2. 使用多模态系统整合理解
        multimodal_understanding = self.multimodal_system.create_advanced_prompt(
            analysis_results, "理解多媒体内容"
        )

        return multimodal_understanding
```

**项目2：多模态情感分析系统**
```python
class MultimodalSentimentAnalysisSystem:
    """多模态情感分析系统"""
    def __init__(self, multimodal_system):
        self.multimodal_system = multimodal_system
        self.sentiment_analyzers = {
            'text': TextSentimentAnalyzer(),
            'image': ImageSentimentAnalyzer(),
            'audio': AudioSentimentAnalyzer(),
            'video': VideoSentimentAnalyzer()
        }

    def analyze_sentiment(self, multimodal_input):
        """分析多模态情感"""
        # 1. 各模态情感分析
        sentiment_results = {}
        for modality, data in multimodal_input.items():
            if modality in self.sentiment_analyzers:
                sentiment_results[modality] = self.sentiment_analyzers[modality].analyze_sentiment(
                    data
                )

        # 2. 多模态情感融合
        fusion_prompt = f"""
        融合以下多模态情感分析结果：

        {sentiment_results}

        请提供综合情感分析：
        """
        return self.multimodal_system.llm.generate(fusion_prompt, max_tokens=400)
```

### 评估认证体系

**技能认证标准**

```python
class MultimodalPromptingCertificationFramework:
    """多模态提示技能认证框架"""
    def __init__(self):
        self.certification_levels = {
            'beginner': {
                'knowledge': ['basic_modalities', 'simple_fusion', 'multimodal_io'],
                'skills': ['basic_multimodal_prompt', 'modality_processing', 'simple_integration'],
                'projects': ['simple_multimodal_qa', 'basic_content_analysis']
            },
            'intermediate': {
                'knowledge': ['cross_modal_alignment', 'advanced_fusion', 'multimodal_reasoning'],
                'skills': ['complex_multimodal_system', 'optimization_techniques', 'performance_tuning'],
                'projects': ['multimodal_assistant', 'cross_modal_reasoning_system']
            },
            'advanced': {
                'knowledge': ['cognitive_modeling', 'adaptive_multimodal', 'scalable_architectures'],
                'skills': ['innovative_applications', 'large_scale_systems', 'research_contributions'],
                'projects': ['multimodal_ai_platform', 'adaptive_learning_system']
            }
        }
```

### 未来发展方向

**技术演进方向**

1. **统一多模态架构**
   - 单一模型处理所有模态
   - 端到端的多模态学习
   - 模态间的深度融合

2. **自适应多模态系统**
   - 根据任务动态选择模态
   - 自适应模态权重调整
   - 个性化多模态交互

3. **高效多模态计算**
   - 模态间的高效信息传递
   - 计算资源的智能分配
   - 实时多模态处理

4. **可解释多模态AI**
   - 多模态决策的可解释性
   - 模态贡献度分析
   - 跨模态因果推理

**应用拓展方向**

1. **虚拟现实/增强现实**
   - 沉浸式多模态交互
   - 实时环境理解
   - 空间多模态导航

2. **智能机器人**
   - 跨模态感知融合
   - 多模态动作规划
   - 自然交互界面

3. **创意内容生成**
   - 多模态创意辅助
   - 跨模态内容转换
   - 智能创作工具

### 总结与反思

**多模态提示的核心价值**

多模态提示代表了AI系统发展的重要方向：
- **信息丰富**：整合多种感官信息，提供更全面的理解
- **认知模拟**：模拟人类的跨模态认知机制
- **交互增强**：提供更自然、更直观的人机交互方式
- **能力扩展**：突破单一模态的限制

**关键技术要素**

1. **模态表示**：有效的多模态特征提取和表示
2. **模态对齐**：不同模态间的语义对齐和映射
3. **跨模态融合**：多模态信息的有效整合策略
4. **联合推理**：基于多模态信息的推理和决策

**学习建议**

1. **理论基础**：深入理解多模态认知科学和机器学习基础
2. **实践动手**：多动手实现不同类型的多模态系统
3. **跨学科学习**：结合计算机视觉、语音处理、自然语言处理等领域知识
4. **前沿追踪**：关注多模态AI的最新研究进展

**挑战与机遇**

多模态提示面临的挑战：
- **模态异构性**：不同模态的数据结构和语义差异
- **计算复杂度**：多模态处理的计算开销
- **数据对齐**：不同模态数据的精确对齐问题
- **评估困难**：多模态系统性能的客观评估

同时带来的机遇：
- **认知增强**：提升AI系统的认知能力
- **应用拓展**：开辟新的AI应用领域
- **人机交互**：实现更自然的人机交互体验
- **创新突破**：推动AI技术的整体进步

通过系统学习多模态提示技术，您将掌握一种强大的AI增强技术，为构建更智能、更自然、更全面的AI系统提供重要支撑。

---

## 本章小结

多模态提示（Multimodal Prompting）是一种集成多种感知模态的提示工程技术，通过有效的跨模态提示策略，使大语言模型能够理解、处理和生成多种模态的信息。

### 核心要点
- **技术原理**：通过模态识别、跨模态对齐、信息融合和联合推理，实现多模态信息处理
- **实现方法**：包括并行、序列、分层等多种多模态提示策略
- **应用领域**：智能教育、医疗诊断、内容理解、情感分析等多个需要多模态信息处理的场景
- **创新价值**：突破单模态限制，实现更自然、更全面的AI交互

### 实践价值
掌握多模态提示技术能够：
- 构建跨模态的智能理解和生成系统
- 提升AI系统的信息处理能力
- 实现更自然、更直观的人机交互
- 开拓新的AI应用领域和场景

### 技能认证
通过本章学习，您应该能够：
1. 理解多模态提示的基本原理和认知基础
2. 实现完整的多模态提示系统流水线
3. 构建跨模态对齐和融合机制
4. 在实际应用中部署多模态系统

多模态提示代表了AI系统向更全面、更自然、更智能方向发展的重要技术，为构建真正理解和生成多模态内容的AI系统奠定了技术基础。

---