# Day 13: 主动提示（Active Prompt）

## 理论学习

### 主动提示的核心原理

主动提示（Active Prompt）是一种通过让模型主动提出问题、请求澄清和生成示例来改进提示质量的技术。该技术由Diao等人提出，旨在通过模型与人类之间的主动交互，自动发现和改进提示设计，无需人工干预。

#### 技术机制与工作原理

**核心流程：**
1. **主动询问阶段（Active Questioning）**
   - 模型主动分析提示的不确定部分
   - 提出具体的澄清问题
   - 请求提供补充信息或示例

2. **示例生成阶段（Example Generation）**
   - 基于当前理解生成高质量示例
   - 选择最具代表性和挑战性的案例
   - 确保示例覆盖不同难度和场景

3. **澄清交互阶段（Clarification Interaction）**
   - 针对模糊或不确定的指令进行澄清
   - 通过多轮对话完善理解
   - 逐步收敛到清晰的任务定义

4. **提示优化阶段（Prompt Optimization）**
   - 基于交互结果优化提示结构
   - 生成更加准确和有效的指令
   - 持续迭代改进提示质量

**技术创新点：**
- **主动学习**：模型主动识别并解决不确定性
- **自举优化**：通过自我提问改进提示质量
- **动态适应**：根据任务特点动态调整交互策略
- **知识挖掘**：通过提问挖掘任务隐含知识

#### 理论基础

**主动学习框架**
```
主动提示的优化过程可以表示为：
P* = Optimize(P₀, Questions, Examples)

其中：
- P₀: 初始提示
- Questions: 主动生成的问题
- Examples: 生成的示例
- P*: 优化后的提示

约束条件：
- 最大化任务性能
- 最小化交互成本
- 满足时间限制
```

**分层交互架构**
```
第一层：不确定性检测层（Uncertainty Detection Layer）
输入：当前提示和任务
输出：不确定区域和置信度

第二层：主动提问层（Active Questioning Layer）
输入：不确定区域
输出：澄清问题列表

第三层：示例生成层（Example Generation Layer）
输入：任务特征、澄清结果
输出：高质量示例

第四层：提示更新层（Prompt Update Layer）
输入：交互历史、示例集
输出：更新后的提示
```

**不确定性量化模型**
```python
class UncertaintyQuantifier:
    """不确定性量化器"""
    def __init__(self, llm):
        self.llm = llm

    def quantify_uncertainty(self, prompt, task_context):
        """
        量化提示的不确定性
        """
        uncertainty_indicators = {
            'ambiguity': self.assess_ambiguity(prompt),
            'incompleteness': self.assess_incompleteness(prompt, task_context),
            'vagueness': self.assess_vagueness(prompt),
            'complexity': self.assess_complexity(prompt)
        }

        # 综合不确定性评分
        overall_uncertainty = (
            0.3 * uncertainty_indicators['ambiguity'] +
            0.3 * uncertainty_indicators['incompleteness'] +
            0.2 * uncertainty_indicators['vagueness'] +
            0.2 * uncertainty_indicators['complexity']
        )

        return {
            'overall': overall_uncertainty,
            'detailed': uncertainty_indicators
        }

    def assess_ambiguity(self, prompt):
        """评估歧义性"""
        ambiguity_indicators = [
            '可能', '也许', '似乎', '大概',
            '或者', '也可以', '任选其一'
        ]

        # 计算歧义词汇密度
        ambiguity_count = sum(1 for indicator in ambiguity_indicators if indicator in prompt)
        prompt_length = len(prompt.split())

        return min(ambiguity_count / max(prompt_length / 10, 1), 1.0)

    def assess_incompleteness(self, prompt, task_context):
        """评估完整性"""
        required_elements = [
            '任务目标', '输入格式', '输出要求', '约束条件'
        ]

        missing_elements = 0
        for element in required_elements:
            if not self.element_present(prompt, element):
                missing_elements += 1

        return missing_elements / len(required_elements)

    def assess_vagueness(self, prompt):
        """评估模糊性"""
        vague_terms = ['一些', '适当', '合适', '足够', '较好']
        return min(sum(1 for term in vague_terms if term in prompt) / 5, 1.0)

    def assess_complexity(self, prompt):
        """评估复杂性"""
        complexity_markers = [
            '首先', '然后', '接着', '最后',
            '如果', '那么', '因为', '所以',
            '步骤一', '步骤二', '步骤三'
        ]

        marker_count = sum(1 for marker in complexity_markers if marker in prompt)
        return min(marker_count / 8, 1.0)
```

### 主动提示 vs 其他技术对比

**vs Standard Prompt Engineering**
| 维度 | 主动提示 | 标准提示工程 |
|------|----------|-------------|
| 设计方式 | 主动交互、自举优化 | 静态设计、人工干预 |
| 适应性 | 高（动态调整） | 中（需要人工修改） |
| 效率 | 中等（需要交互） | 高（一次性完成） |
| 质量保证 | 高（通过澄清保证） | 依赖经验 |
| 自动化程度 | 高（自主交互） | 低（人工主导） |

**vs Automatic Prompt Engineer**
| 维度 | 主动提示 | 自动提示工程师 |
|------|----------|---------------|
| 交互方式 | 模型-人类交互 | 模型自我优化 |
| 信息获取 | 通过提问获取 | 通过算法搜索 |
| 优化机制 | 问答驱动优化 | 搜索驱动优化 |
| 优势 | 理解更深入 | 速度更快 |
| 应用场景 | 复杂理解任务 | 标准化任务 |

### 主动提示的分类体系

**1. 澄清导向主动提示（Clarification-Oriented）**

主要通过提问澄清任务要求：

```python
class ClarificationOrientedActivePrompt:
    """澄清导向主动提示"""
    def __init__(self, llm):
        self.llm = llm
        self.clarification_strategies = {
            'requirement_clarification': self.clarify_requirements,
            'output_format_clarification': self.clarify_output_format,
            'constraint_clarification': self.clarify_constraints,
            'edge_case_clarification': self.clarify_edge_cases
        }

    def run_clarification_dialogue(self, initial_prompt, task):
        """
        运行澄清对话
        """
        current_prompt = initial_prompt
        dialogue_history = []

        # 识别需要澄清的点
        unclear_aspects = self.identify_unclear_aspects(current_prompt, task)

        for aspect in unclear_aspects:
            # 生成澄清问题
            question = self.generate_clarification_question(aspect, task)

            # 收集澄清信息
            clarification = self.collect_clarification(question)

            # 更新提示
            current_prompt = self.update_prompt_with_clarification(
                current_prompt, clarification
            )

            dialogue_history.append({
                'aspect': aspect,
                'question': question,
                'clarification': clarification
            })

        return {
            'optimized_prompt': current_prompt,
            'dialogue_history': dialogue_history
        }

    def identify_unclear_aspects(self, prompt, task):
        """识别不清晰的方面"""
        unclear_detection_prompt = f"""
        分析以下提示，识别可能需要澄清的不明确方面：

        提示：{prompt}
        任务：{task.description}

        请从以下维度分析：
        1. 任务要求是否明确
        2. 输出格式是否清晰
        3. 约束条件是否具体
        4. 特殊要求是否说明

        分析结果：
        """
        analysis = self.llm.generate(unclear_detection_prompt, max_tokens=400)

        # 解析不明确方面
        unclear_aspects = self.parse_unclear_aspects(analysis)

        return unclear_aspects

    def generate_clarification_question(self, aspect, task):
        """生成澄清问题"""
        question_templates = {
            'requirement_clarification': "请具体说明对{aspect}的要求是什么？",
            'output_format': "关于{aspect}，您希望输出什么样的格式？",
            'constraint': "{aspect}方面有什么特殊的限制条件吗？",
            'edge_case': "遇到{aspect}的边缘情况时，应该如何处理？"
        }

        template = question_templates.get(aspect['type'], "关于{aspect}，请提供更多信息。")
        return template.format(aspect=aspect['description'])

    def collect_clarification(self, question):
        """收集澄清信息（模拟）"""
        # 在实际应用中，这里会与用户交互
        clarification_prompt = f"""
        请回答以下澄清问题：

        问题：{question}

        回答：
        """
        return self.llm.generate(clarification_prompt, max_tokens=200)

    def update_prompt_with_clarification(self, prompt, clarification):
        """使用澄清信息更新提示"""
        update_prompt = f"""
        基于以下澄清信息，优化原始提示：

        原始提示：{prompt}

        澄清信息：{clarification}

        请生成优化后的提示，确保包含澄清的信息，表述清晰明确。

        优化后提示：
        """
        return self.llm.generate(update_prompt, max_tokens=500)
```

**2. 示例导向主动提示（Example-Oriented）**

主要通过生成和优化示例改进提示：

```python
class ExampleOrientedActivePrompt:
    """示例导向主动提示"""
    def __init__(self, llm):
        self.llm = llm
        self.example_generation_strategies = {
            'representative_examples': self.generate_representative_examples,
            'edge_case_examples': self.generate_edge_case_examples,
            'difficulty_gradient': self.generate_difficulty_gradient,
            'domain_specific': self.generate_domain_specific
        }

    def run_example_optimization(self, initial_prompt, task):
        """
        运行示例优化
        """
        # 分析任务需求
        task_analysis = self.analyze_task_requirements(task)

        # 生成初始示例集
        initial_examples = self.generate_initial_examples(task)

        # 识别示例缺口
        example_gaps = self.identify_example_gaps(initial_examples, task_analysis)

        # 生成补充示例
        supplementary_examples = self.generate_supplementary_examples(
            example_gaps, task
        )

        # 整合示例到提示
        optimized_prompt = self.integrate_examples(
            initial_prompt, initial_examples + supplementary_examples
        )

        return {
            'optimized_prompt': optimized_prompt,
            'examples_used': initial_examples + supplementary_examples,
            'optimization_log': {
                'initial_count': len(initial_examples),
                'supplementary_count': len(supplementary_examples),
                'total_count': len(initial_examples) + len(supplementary_examples)
            }
        }

    def generate_initial_examples(self, task):
        """生成初始示例"""
        generation_prompt = f"""
        为以下任务生成3-5个高质量示例：

        任务：{task.description}
        任务类型：{task.type}
        输入格式：{task.input_format}
        输出格式：{task.output_format}

        要求：
        1. 示例应该覆盖不同难度级别
        2. 包含典型的正面和负面案例
        3. 示例应该清晰展示期望的输入和输出
        4. 确保示例的多样性和代表性

        示例格式：
        输入：[具体输入]
        输出：[期望输出]
        """
        examples_text = self.llm.generate(generation_prompt, max_tokens=600)
        return self.parse_examples(examples_text)

    def identify_example_gaps(self, examples, task_analysis):
        """识别示例缺口"""
        gap_analysis_prompt = f"""
        分析以下示例集，识别可能的缺口：

        已有示例：
        {self.format_examples(examples)}

        任务需求分析：
        {task_analysis}

        请识别：
        1. 缺失的示例类型
        2. 未覆盖的场景
        3. 难度层次缺口
        4. 特殊案例缺失

        分析结果：
        """
        gap_analysis = self.llm.generate(gap_analysis_prompt, max_tokens=400)
        return self.parse_gap_analysis(gap_analysis)

    def generate_supplementary_examples(self, gaps, task):
        """生成补充示例"""
        supplementary_examples = []

        for gap in gaps:
            generation_prompt = f"""
            针对以下缺口，生成一个具体示例：

            缺口类型：{gap['type']}
            缺口描述：{gap['description']}
            任务：{task.description}

            请生成一个具体的示例，包括输入和输出。

            示例：
            """
            example_text = self.llm.generate(generation_prompt, max_tokens=200)
            supplementary_examples.append(self.parse_single_example(example_text))

        return supplementary_examples

    def integrate_examples(self, prompt, examples):
        """将示例整合到提示中"""
        example_section = self.format_examples_for_prompt(examples)

        integration_prompt = f"""
        将以下示例整合到提示中：

        原始提示：{prompt}

        示例集合：{example_section}

        要求：
        1. 将示例自然地融入提示结构
        2. 保持提示的清晰性和完整性
        3. 确保示例能够有效指导模型行为
        4. 添加适当的说明和过渡

        整合后提示：
        """
        return self.llm.generate(integration_prompt, max_tokens=600)
```

**3. 迭代导向主动提示（Iterative-Oriented）**

通过多轮迭代改进提示：

```python
class IterativeOrientedActivePrompt:
    """迭代导向主动提示"""
    def __init__(self, llm, evaluator):
        self.llm = llm
        self.evaluator = evaluator
        self.max_iterations = 5

    def run_iterative_optimization(self, initial_prompt, task):
        """
        运行迭代优化
        """
        current_prompt = initial_prompt
        iteration_history = []

        for iteration in range(self.max_iterations):
            print(f"迭代 {iteration + 1}/{self.max_iterations}")

            # 评估当前提示
            current_score = self.evaluator.evaluate(current_prompt, task)

            # 识别改进点
            improvement_points = self.identify_improvement_points(
                current_prompt, task, current_score
            )

            if not improvement_points:
                print("未发现明显改进点，停止迭代")
                break

            # 生成改进建议
            improvement_suggestions = self.generate_improvement_suggestions(
                improvement_points, current_prompt
            )

            # 应用改进
            improved_prompt = self.apply_improvements(
                current_prompt, improvement_suggestions
            )

            # 验证改进效果
            improved_score = self.evaluator.evaluate(improved_prompt, task)

            iteration_history.append({
                'iteration': iteration + 1,
                'previous_score': current_score,
                'improved_score': improved_score,
                'improvement': improved_score - current_score,
                'improvement_points': improvement_points,
                'improved_prompt': improved_prompt
            })

            # 检查是否有实际改进
            if improved_score > current_score:
                current_prompt = improved_prompt
                print(f"  改进幅度: {improved_score - current_score:.4f}")
            else:
                print("  无显著改进，保持当前提示")

        return {
            'optimized_prompt': current_prompt,
            'iteration_history': iteration_history,
            'total_improvement': (
                iteration_history[-1]['improved_score'] if iteration_history
                else 0
            )
        }

    def identify_improvement_points(self, prompt, task, score):
        """识别改进点"""
        analysis_prompt = f"""
        分析以下提示，识别可以改进的方面：

        提示：{prompt}
        任务：{task.description}
        当前评分：{score:.4f}

        请从以下维度分析改进点：
        1. 指令清晰度 - 是否有模糊或不明确的表述
        2. 结构组织 - 是否需要重新组织信息
        3. 细节完整性 - 是否缺少必要的细节
        4. 示例质量 - 示例是否充分和恰当

        每个改进点应该具体说明：
        - 问题描述
        - 改进建议
        - 预期效果

        分析结果：
        """
        analysis = self.llm.generate(analysis_prompt, max_tokens=500)
        return self.parse_improvement_points(analysis)

    def generate_improvement_suggestions(self, improvement_points, current_prompt):
        """生成改进建议"""
        suggestions = []

        for point in improvement_points:
            suggestion_prompt = f"""
            针对以下改进点，生成具体建议：

            改进点：{point['description']}
            当前提示：{current_prompt}

            请生成：
            1. 具体的改进方案
            2. 需要添加或修改的内容
            3. 改进后的表述

            建议：
            """
            suggestion = self.llm.generate(suggestion_prompt, max_tokens=300)
            suggestions.append({
                'point': point,
                'suggestion': suggestion
            })

        return suggestions

    def apply_improvements(self, current_prompt, suggestions):
        """应用改进"""
        improvement_text = "\n\n".join(
            [f"改进建议: {s['suggestion']}" for s in suggestions]
        )

        application_prompt = f"""
        基于以下改进建议，优化原始提示：

        原始提示：{current_prompt}

        改进建议：
        {improvement_text}

        请应用这些建议，生成优化后的提示。确保：
        1. 整合所有改进建议
        2. 保持提示的完整性和连贯性
        3. 表述清晰准确

        优化后提示：
        """
        return self.llm.generate(application_prompt, max_tokens=600)
```

### 主动提示的核心算法

**1. 不确定性检测算法（Uncertainty Detection）**

```python
class ActiveUncertaintyDetector:
    """主动不确定性检测器"""
    def __init__(self, llm):
        self.llm = llm

    def detect_critical_uncertainties(self, prompt, task):
        """
        检测关键不确定性
        """
        uncertainty_analysis = {
            'task_ambiguity': self.analyze_task_ambiguity(prompt, task),
            'input_format_ambiguity': self.analyze_input_ambiguity(prompt, task),
            'output_format_ambiguity': self.analyze_output_ambiguity(prompt, task),
            'constraint_ambiguity': self.analyze_constraint_ambiguity(prompt, task)
        }

        # 计算关键性得分
        critical_uncertainties = []
        for aspect, uncertainty in uncertainty_analysis.items():
            if uncertainty['level'] > 0.6:  # 阈值
                critical_uncertainties.append({
                    'aspect': aspect,
                    'uncertainty_level': uncertainty['level'],
                    'questions': uncertainty['potential_questions']
                })

        return critical_uncertainties

    def analyze_task_ambiguity(self, prompt, task):
        """分析任务歧义性"""
        analysis_prompt = f"""
        评估以下提示在描述任务时的歧义性：

        提示：{prompt}
        任务描述：{task.description}

        请评估：
        1. 任务目标是否明确
        2. 期望的输出是否清晰
        3. 成功标准是否具体
        4. 是否有模糊或多义的表述

        歧义性评分（0-1）：[数值]
        潜在问题：[列出具体问题]
        澄清建议：[提出澄清问题]
        """
        analysis = self.llm.generate(analysis_prompt, max_tokens=400)

        # 提取关键信息
        uncertainty_level = self.extract_uncertainty_level(analysis)
        potential_questions = self.extract_potential_questions(analysis)

        return {
            'level': uncertainty_level,
            'potential_questions': potential_questions
        }
```

**2. 智能问题生成算法（Intelligent Question Generation）**

```python
class IntelligentQuestionGenerator:
    """智能问题生成器"""
    def __init__(self, llm):
        self.llm = llm

    def generate_strategic_questions(self, uncertainties, task):
        """
        生成战略性澄清问题
        """
        strategic_questions = []

        for uncertainty in uncertainties:
            # 根据不确定性类型选择生成策略
            if uncertainty['aspect'] == 'task_ambiguity':
                questions = self.generate_task_clarification_questions(uncertainty, task)
            elif uncertainty['aspect'] == 'input_format_ambiguity':
                questions = self.generate_input_format_questions(uncertainty, task)
            elif uncertainty['aspect'] == 'output_format_ambiguity':
                questions = self.generate_output_format_questions(uncertainty, task)
            elif uncertainty['aspect'] == 'constraint_ambiguity':
                questions = self.generate_constraint_questions(uncertainty, task)
            else:
                questions = self.generate_general_questions(uncertainty, task)

            strategic_questions.extend(questions)

        return strategic_questions

    def generate_task_clarification_questions(self, uncertainty, task):
        """生成任务澄清问题"""
        question_templates = [
            "您希望我完成的具体任务目标是什么？",
            "什么样的输出结果算是成功完成任务？",
            "完成任务的主要步骤是什么？",
            "是否有特定的成功标准或评估指标？"
        ]

        # 基于任务类型选择最相关的问题
        task_type = task.type
        relevant_templates = self.select_relevant_templates(question_templates, task_type)

        return relevant_templates[:2]  # 限制问题数量

    def generate_input_format_questions(self, uncertainty, task):
        """生成输入格式问题"""
        return [
            "请描述输入数据的格式和结构",
            "输入中哪些字段是必需的，哪些是可选的？",
            "输入数据是否有特定的格式要求（如JSON、CSV等）？"
        ]

    def generate_output_format_questions(self, uncertainty, task):
        """生成输出格式问题"""
        return [
            "您希望输出什么样的格式（如文本、列表、表格等）？",
            "输出中需要包含哪些关键信息？",
            "是否有特定的格式规范需要遵循？"
        ]

    def select_relevant_templates(self, templates, task_type):
        """选择相关模板"""
        type_relevance = {
            'classification': ["您希望我完成的具体任务目标是什么？", "什么样的输出结果算是成功完成任务？"],
            'generation': ["请描述输入数据的格式和结构", "输出中需要包含哪些关键信息？"],
            'reasoning': ["完成任务的主要步骤是什么？", "是否有特定的成功标准或评估指标？"]
        }

        return type_relevance.get(task_type, templates[:2])
```

**3. 示例智能生成算法（Intelligent Example Generation）**

```python
class IntelligentExampleGenerator:
    """智能示例生成器"""
    def __init__(self, llm):
        self.llm = llm

    def generate_informative_examples(self, prompt, task, num_examples=3):
        """
        生成信息丰富的示例
        """
        # 分析任务需求
        task_requirements = self.analyze_task_requirements(task)

        # 确定示例类型
        example_types = self.determine_example_types(task_requirements)

        generated_examples = []
        for example_type in example_types[:num_examples]:
            example = self.generate_specific_example(example_type, prompt, task)
            generated_examples.append(example)

        return generated_examples

    def analyze_task_requirements(self, task):
        """分析任务需求"""
        analysis_prompt = f"""
        分析以下任务的关键需求：

        任务：{task.description}
        任务类型：{task.type}

        请分析：
        1. 任务的核心要素
        2. 关键决策点
        3. 容易出错的环节
        4. 需要特殊处理的场景

        分析结果：
        """
        analysis = self.llm.generate(analysis_prompt, max_tokens=400)
        return self.parse_task_requirements(analysis)

    def determine_example_types(self, requirements):
        """确定示例类型"""
        example_types = []

        # 基本示例
        example_types.append({
            'type': 'basic',
            'description': '标准情况下的基本示例'
        })

        # 边界案例
        if requirements['has_edge_cases']:
            example_types.append({
                'type': 'edge_case',
                'description': '边界情况或特殊情况'
            })

        # 复杂案例
        if requirements['complexity'] == 'high':
            example_types.append({
                'type': 'complex',
                'description': '复杂的挑战性案例'
            })

        # 常见错误示例
        if requirements['common_mistakes']:
            example_types.append({
                'type': 'mistake_prevention',
                'description': '展示如何避免常见错误'
            })

        return example_types

    def generate_specific_example(self, example_type, prompt, task):
        """生成特定类型的示例"""
        generation_prompt = f"""
        生成一个{example_type['description']}：

        任务：{task.description}
        任务类型：{task.type}
        当前提示：{prompt}

        要求：
        1. 示例应该清晰展示任务要求
        2. 输入和输出要具体明确
        3. 体现{example_type['type']}的特点
        4. 有助于模型理解任务

        请生成：
        示例说明：[简要说明]
        输入：[具体输入]
        输出：[期望输出]
        """
        example_text = self.llm.generate(generation_prompt, max_tokens=400)
        return self.parse_example(example_text)
```

## 实践任务

### 任务1：基础主动提示系统

**目标：**
实现一个基础的主动提示系统，能够主动识别提示中的不确定部分并提出澄清问题。

**步骤1：核心主动提示系统**
```python
class BasicActivePromptSystem:
    """基础主动提示系统"""
    def __init__(self, llm, task_evaluator):
        self.llm = llm
        self.evaluator = task_evaluator
        self.uncertainty_detector = ActiveUncertaintyDetector(llm)
        self.question_generator = IntelligentQuestionGenerator(llm)
        self.example_generator = IntelligentExampleGenerator(llm)

    def主动_optimize_prompt(self, initial_prompt, task, max_iterations=3):
        """
        主动优化提示

        Args:
            initial_prompt: 初始提示
            task: 任务描述
            max_iterations: 最大迭代次数

        Returns:
            dict: 优化结果
        """
        current_prompt = initial_prompt
        optimization_log = []

        print("开始主动提示优化...")
        print(f"初始提示：{current_prompt[:100]}...")

        for iteration in range(max_iterations):
            print(f"\n=== 迭代 {iteration + 1} ===")

            # 1. 检测不确定性
            print("1. 检测不确定性...")
            critical_uncertainties = self.uncertainty_detector.detect_critical_uncertainties(
                current_prompt, task
            )

            if not critical_uncertainties:
                print("   未发现明显不确定性，优化完成")
                break

            print(f"   发现 {len(critical_uncertainties)} 个潜在问题")

            # 2. 生成澄清问题
            print("2. 生成澄清问题...")
            clarification_questions = self.question_generator.generate_strategic_questions(
                critical_uncertainties, task
            )

            print(f"   生成了 {len(clarification_questions)} 个澄清问题")
            for i, q in enumerate(clarification_questions, 1):
                print(f"   问题{i}: {q}")

            # 3. 收集澄清信息
            print("3. 收集澄清信息...")
            clarifications = self.collect_clarifications(clarification_questions)

            # 4. 生成补充示例
            print("4. 生成补充示例...")
            informative_examples = self.example_generator.generate_informative_examples(
                current_prompt, task, num_examples=2
            )

            # 5. 优化提示
            print("5. 优化提示...")
            optimized_prompt = self.optimize_prompt_with_feedback(
                current_prompt, clarifications, informative_examples
            )

            # 6. 评估改进效果
            previous_score = self.evaluator.evaluate(current_prompt, task)
            improved_score = self.evaluator.evaluate(optimized_prompt, task)

            improvement = improved_score - previous_score

            print(f"   优化前评分: {previous_score:.4f}")
            print(f"   优化后评分: {improved_score:.4f}")
            print(f"   改进幅度: {improvement:.4f}")

            # 记录优化历史
            optimization_log.append({
                'iteration': iteration + 1,
                'uncertainties': critical_uncertainties,
                'questions': clarification_questions,
                'clarifications': clarifications,
                'examples': informative_examples,
                'previous_score': previous_score,
                'improved_score': improved_score,
                'improvement': improvement,
                'optimized_prompt': optimized_prompt
            })

            # 如果有显著改进，更新当前提示
            if improvement > 0.01:
                current_prompt = optimized_prompt
                print(f"   ✓ 接受改进")
            else:
                print(f"   ✗ 改进不明显，保持当前提示")

        return {
            'optimized_prompt': current_prompt,
            'optimization_log': optimization_log,
            'total_improvement': (
                optimization_log[-1]['improved_score'] if optimization_log else 0
            )
        }

    def collect_clarifications(self, questions):
        """收集澄清信息（模拟实现）"""
        clarifications = []

        for question in questions:
            # 在实际应用中，这里会与用户交互
            # 这里使用模型模拟澄清回答
            clarification_prompt = f"""
            基于以下澄清问题，提供一个详细的回答：

            问题：{question}

            请提供：
            1. 直接回答问题
            2. 提供具体的细节和要求
            3. 说明需要注意的事项

            回答：
            """
            clarification = self.llm.generate(clarification_prompt, max_tokens=300)
            clarifications.append(clarification)

        return clarifications

    def optimize_prompt_with_feedback(self, current_prompt, clarifications, examples):
        """基于反馈优化提示"""
        feedback_text = "\n\n".join([
            f"澄清信息: {clarification}" for clarification in clarifications
        ])

        example_text = "\n\n".join([
            f"示例: {example}" for example in examples
        ])

        optimization_prompt = f"""
        基于以下澄清信息和示例，优化原始提示：

        原始提示：
        {current_prompt}

        澄清信息：
        {feedback_text}

        补充示例：
        {example_text}

        优化要求：
        1. 整合所有澄清信息，消除不确定性
        2. 合理安排示例，辅助理解
        3. 保持提示的清晰性和完整性
        4. 确保优化后的提示能有效指导任务执行

        优化后提示：
        """
        return self.llm.generate(optimization_prompt, max_tokens=700)
```

### 任务2：多轮对话式主动提示

**目标：**
构建多轮对话式的主动提示系统，实现更深入的交互优化。

**步骤：多轮对话系统**
```python
class MultiTurnActivePromptSystem:
    """多轮对话主动提示系统"""
    def __init__(self, llm, task_evaluator):
        self.llm = llm
        self.evaluator = task_evaluator
        self.dialogue_manager = DialogueManager(llm)

    def interactive_optimization(self, initial_prompt, task, max_turns=5):
        """
        交互式提示优化
        """
        current_prompt = initial_prompt
        dialogue_history = []

        print("开始多轮对话优化...")
        print(f"初始提示: {current_prompt}")

        for turn in range(max_turns):
            print(f"\n--- 对话轮次 {turn + 1} ---")

            # 分析当前提示状态
            prompt_analysis = self.analyze_prompt_state(current_prompt, task)
            print(f"提示状态: {prompt_analysis['status']}")

            # 生成对话问题
            dialogue_question = self.dialogue_manager.generate_next_question(
                prompt_analysis, dialogue_history
            )

            print(f"系统提问: {dialogue_question}")

            # 模拟用户回答（实际应用中为真实交互）
            user_response = self.simulate_user_response(dialogue_question, task)

            print(f"用户回答: {user_response[:100]}...")

            # 更新提示
            updated_prompt = self.update_prompt_from_dialogue(
                current_prompt, dialogue_question, user_response
            )

            # 评估改进
            if updated_prompt != current_prompt:
                previous_score = self.evaluator.evaluate(current_prompt, task)
                improved_score = self.evaluator.evaluate(updated_prompt, task)

                print(f"评分变化: {previous_score:.4f} → {improved_score:.4f}")

                if improved_score >= previous_score:
                    current_prompt = updated_prompt
                    print("✓ 接受更新")
                else:
                    print("✗ 评分下降，保持原提示")
            else:
                print("- 提示无变化")

            # 记录对话历史
            dialogue_history.append({
                'turn': turn + 1,
                'question': dialogue_question,
                'response': user_response,
                'prompt_update': updated_prompt != current_prompt
            })

            # 检查是否达到收敛
            if self.check_convergence(dialogue_history, turn):
                print("\n达到收敛条件，结束对话")
                break

        return {
            'final_prompt': current_prompt,
            'dialogue_history': dialogue_history,
            'total_turns': len(dialogue_history)
        }

    def analyze_prompt_state(self, prompt, task):
        """分析提示状态"""
        analysis_prompt = f"""
        分析当前提示的状态：

        提示：{prompt}
        任务：{task.description}

        请从以下方面评估：
        1. 清晰度：指令是否明确易懂
        2. 完整性：是否包含所有必要信息
        3. 可操作性：是否易于模型理解和执行
        4. 潜在问题：可能存在的模糊或不足之处

        状态评估：
        """
        analysis = self.llm.generate(analysis_prompt, max_tokens=400)

        # 简单状态分类
        if "完全清晰" in analysis or "非常明确" in analysis:
            status = "清晰"
        elif "基本清晰" in analysis or "大部分明确" in analysis:
            status = "基本清晰"
        elif "有些模糊" in analysis or "部分不明确" in analysis:
            status = "需要改进"
        else:
            status = "需要澄清"

        return {
            'analysis': analysis,
            'status': status
        }

    def check_convergence(self, dialogue_history, current_turn):
        """检查收敛条件"""
        if current_turn < 2:
            return False

        # 检查最近两轮是否有实质改进
        recent_turns = dialogue_history[-3:]
        updates = [turn['prompt_update'] for turn in recent_turns]

        # 如果最近几轮都没有更新，认为收敛
        return sum(updates) == 0
```

### 任务3：主动示例生成系统

**目标：**
构建主动生成和优化示例的系统，通过智能示例提升提示质量。

**步骤：示例生成系统**
```python
class ActiveExampleGenerationSystem:
    """主动示例生成系统"""
    def __init__(self, llm, task_evaluator):
        self.llm = llm
        self.evaluator = task_evaluator
        self.example_analyzer = ExampleAnalyzer(llm)

    def主动_generate_examples(self, prompt, task, target_coverage=0.9):
        """
        主动生成示例
        """
        print("开始主动示例生成...")

        # 1. 分析任务空间
        print("1. 分析任务空间...")
        task_space = self.analyze_task_space(task)

        print(f"   识别任务要素: {task_space['key_elements']}")
        print(f"   识别难度层次: {task_space['difficulty_levels']}")

        # 2. 生成初始示例集
        print("\n2. 生成初始示例集...")
        initial_examples = self.generate_initial_example_set(task_space, task)

        # 3. 评估示例覆盖
        print("\n3. 评估示例覆盖...")
        coverage_analysis = self.evaluate_example_coverage(initial_examples, task_space)

        print(f"   当前覆盖度: {coverage_analysis['coverage_rate']:.2%}")
        print(f"   缺失要素: {coverage_analysis['missing_elements']}")

        # 4. 生成补充示例
        if coverage_analysis['coverage_rate'] < target_coverage:
            print("\n4. 生成补充示例...")
            missing_elements = coverage_analysis['missing_elements']
            supplementary_examples = self.generate_targeted_examples(
                missing_elements, task_space, task
            )
            final_examples = initial_examples + supplementary_examples
        else:
            print("\n4. 覆盖度已达标，无需补充示例")
            final_examples = initial_examples

        # 5. 优化示例组织
        print("\n5. 优化示例组织...")
        optimized_prompt = self.organize_examples_in_prompt(prompt, final_examples)

        # 6. 验证示例有效性
        print("\n6. 验证示例有效性...")
        validation_score = self.validate_examples_effectiveness(
            optimized_prompt, final_examples, task
        )

        print(f"   示例有效性评分: {validation_score:.4f}")

        return {
            'optimized_prompt': optimized_prompt,
            'examples': final_examples,
            'coverage_analysis': coverage_analysis,
            'validation_score': validation_score
        }

    def analyze_task_space(self, task):
        """分析任务空间"""
        analysis_prompt = f"""
        全面分析以下任务的空间结构：

        任务：{task.description}
        任务类型：{task.type}

        请分析：
        1. 关键要素：完成任务需要考虑的主要因素
        2. 难度层次：不同复杂度的案例
        3. 边界情况：特殊或极端的案例
        4. 决策点：需要特别关注的判断点
        5. 常见错误：容易出错的地方

        分析结果：
        """
        analysis = self.llm.generate(analysis_prompt, max_tokens=500)

        # 解析分析结果
        return self.parse_task_space_analysis(analysis)

    def parse_task_space_analysis(self, analysis):
        """解析任务空间分析"""
        # 简化的解析逻辑
        return {
            'key_elements': ['element1', 'element2', 'element3'],  # 模拟结果
            'difficulty_levels': ['simple', 'medium', 'complex'],
            'edge_cases': ['edge_case1', 'edge_case2'],
            'decision_points': ['decision1', 'decision2'],
            'common_mistakes': ['mistake1', 'mistake2']
        }

    def generate_initial_example_set(self, task_space, task):
        """生成初始示例集"""
        example_prompt = f"""
        基于任务空间分析，生成示例集：

        任务：{task.description}
        任务类型：{task.type}

        任务空间：
        关键要素：{task_space['key_elements']}
        难度层次：{task_space['difficulty_levels']}
        边界情况：{task_space['edge_cases']}
        决策点：{task_space['decision_points']}

        要求生成：
        1. 简单示例：展示基本功能和流程
        2. 中等示例：包含更多要素和细节
        3. 复杂示例：挑战性的综合案例
        4. 边界示例：特殊或极端情况

        每个示例包含：
        - 示例描述
        - 输入数据
        - 预期输出
        - 关键要点

        示例集：
        """
        examples_text = self.llm.generate(example_prompt, max_tokens=800)
        return self.parse_examples(examples_text)

    def evaluate_example_coverage(self, examples, task_space):
        """评估示例覆盖度"""
        coverage_prompt = f"""
        评估示例集对任务空间的覆盖情况：

        示例集：
        {self.format_examples(examples)}

        任务空间要素：
        关键要素：{task_space['key_elements']}
        难度层次：{task_space['difficulty_levels']}

        分析：
        1. 每个要素是否被充分示例化
        2. 难度层次是否完整覆盖
        3. 是否遗漏重要的要素或场景

        返回：
        - 覆盖度评估（0-1）
        - 缺失的要素列表
        - 改进建议
        """
        coverage_analysis = self.llm.generate(coverage_prompt, max_tokens=400)

        return self.parse_coverage_analysis(coverage_analysis)

    def parse_coverage_analysis(self, analysis):
        """解析覆盖分析"""
        # 简化的解析
        return {
            'coverage_rate': 0.75,  # 模拟值
            'missing_elements': ['element3', 'complex_case'],
            'improvement_suggestions': ['增加复杂案例', '补充边界情况']
        }

    def generate_targeted_examples(self, missing_elements, task_space, task):
        """生成针对性示例"""
        targeted_examples = []

        for element in missing_elements:
            example_prompt = f"""
            针对缺失要素"{element}"，生成一个示例：

            任务：{task.description}
            该要素的特点：{element}

            要求：
            1. 突出该要素的重要性
            2. 清晰展示处理方式
            3. 提供具体的输入输出

            示例：
            """
            example_text = self.llm.generate(example_prompt, max_tokens=300)
            targeted_examples.append(self.parse_single_example(example_text))

        return targeted_examples

    def organize_examples_in_prompt(self, prompt, examples):
        """将示例组织到提示中"""
        organization_prompt = f"""
        将示例集整合到提示中：

        原始提示：
        {prompt}

        示例集：
        {self.format_examples(examples)}

        整合要求：
        1. 在适当位置插入示例
        2. 保持提示的逻辑结构
        3. 添加示例说明和引导
        4. 确保整体连贯性

        整合后提示：
        """
        return self.llm.generate(organization_prompt, max_tokens=800)
```

### 任务4：主动提示质量评估

**目标：**
构建主动提示的质量评估系统，多维度评估主动优化的效果。

**步骤：质量评估系统**
```python
class ActivePromptQualityEvaluator:
    """主动提示质量评估器"""
    def __init__(self, llm, task_evaluator):
        self.llm = llm
        self.task_evaluator = task_evaluator
        self.evaluation_dimensions = {
            'clarity_improvement': self.evaluate_clarity_improvement,
            'completeness_enhancement': self.evaluate_completeness_enhancement,
            'effectiveness_gain': self.evaluate_effectiveness_gain,
            'interaction_efficiency': self.evaluate_interaction_efficiency
        }

    def comprehensive_evaluation(self, initial_prompt, optimized_prompt, task, optimization_log):
        """
        综合评估主动提示优化效果
        """
        evaluation_results = {}

        print("开始主动提示质量评估...")

        # 1. 评估清晰度改进
        print("\n1. 评估清晰度改进...")
        clarity_score = self.evaluation_dimensions['clarity_improvement'](
            initial_prompt, optimized_prompt, task
        )
        evaluation_results['clarity_improvement'] = clarity_score

        # 2. 评估完整性增强
        print("2. 评估完整性增强...")
        completeness_score = self.evaluation_dimensions['completeness_enhancement'](
            initial_prompt, optimized_prompt, task
        )
        evaluation_results['completeness_enhancement'] = completeness_score

        # 3. 评估有效性提升
        print("3. 评估有效性提升...")
        effectiveness_score = self.evaluation_dimensions['effectiveness_gain'](
            initial_prompt, optimized_prompt, task
        )
        evaluation_results['effectiveness_gain'] = effectiveness_score

        # 4. 评估交互效率
        print("4. 评估交互效率...")
        efficiency_score = self.evaluation_dimensions['interaction_efficiency'](
            optimization_log
        )
        evaluation_results['interaction_efficiency'] = efficiency_score

        # 5. 计算综合评分
        overall_score = self.calculate_overall_score(evaluation_results)

        # 6. 生成评估报告
        report = self.generate_evaluation_report(
            initial_prompt, optimized_prompt, evaluation_results, overall_score
        )

        print(f"\n综合评分: {overall_score:.4f}")

        return {
            'overall_score': overall_score,
            'dimension_scores': evaluation_results,
            'detailed_report': report
        }

    def evaluate_clarity_improvement(self, initial_prompt, optimized_prompt, task):
        """评估清晰度改进"""
        clarity_evaluation_prompt = f"""
        比较两个版本的提示在清晰度方面的改进：

        初始提示：
        {initial_prompt}

        优化后提示：
        {optimized_prompt}

        任务：{task.description}

        请从以下维度评估：
        1. 指令明确性 - 表述是否清晰无歧义
        2. 结构组织 - 信息组织是否有条理
        3. 逻辑连贯 - 整体逻辑是否流畅
        4. 可读性 - 是否易于理解和执行

        初始提示评分 (1-10)：
        优化后提示评分 (1-10)：
        改进程度：
        """
        evaluation = self.llm.generate(clarity_evaluation_prompt, max_tokens=400)

        # 提取评分（简化实现）
        return self.extract_score(evaluation)

    def evaluate_completeness_enhancement(self, initial_prompt, optimized_prompt, task):
        """评估完整性增强"""
        completeness_evaluation_prompt = f"""
        比较两个版本提示在完整性方面的提升：

        初始提示：
        {initial_prompt}

        优化后提示：
        {optimized_prompt}

        任务：{task.description}

        评估要点：
        1. 任务要求是否完整
        2. 输入输出格式是否明确
        3. 约束条件是否充分
        4. 边界情况是否考虑

        初始提示完整性评分 (1-10)：
        优化后完整性评分 (1-10)：
        """
        evaluation = self.llm.generate(completeness_evaluation_prompt, max_tokens=400)
        return self.extract_score(evaluation)

    def evaluate_effectiveness_gain(self, initial_prompt, optimized_prompt, task):
        """评估有效性提升"""
        # 使用实际性能测试
        initial_score = self.task_evaluator.evaluate(initial_prompt, task)
        optimized_score = self.task_evaluator.evaluate(optimized_prompt, task)

        # 计算有效性提升
        effectiveness_gain = (optimized_score - initial_score) / max(initial_score, 0.001)

        return min(effectiveness_gain, 1.0)  # 限制在0-1范围

    def evaluate_interaction_efficiency(self, optimization_log):
        """评估交互效率"""
        if not optimization_log:
            return 0.0

        efficiency_factors = {
            'turns_count': len(optimization_log),
            'improvement_per_turn': 0.0,
            'early_convergence': 0.0,
            'question_relevance': 0.0
        }

        # 计算每轮改进
        improvements = [entry['improvement'] for entry in optimization_log]
        if improvements:
            efficiency_factors['improvement_per_turn'] = sum(improvements) / len(improvements)

        # 检查早期收敛
        if len(optimization_log) <= 3:
            efficiency_factors['early_convergence'] = 1.0
        else:
            efficiency_factors['early_convergence'] = max(0, 1.0 - (len(optimization_log) - 3) / 10)

        # 评估问题相关性（简化实现）
        efficiency_factors['question_relevance'] = 0.8  # 模拟评分

        # 计算综合效率评分
        efficiency_score = (
            0.3 * efficiency_factors['early_convergence'] +
            0.3 * efficiency_factors['improvement_per_turn'] +
            0.2 * (1.0 / max(efficiency_factors['turns_count'], 1)) +
            0.2 * efficiency_factors['question_relevance']
        )

        return min(efficiency_score, 1.0)

    def calculate_overall_score(self, evaluation_results):
        """计算综合评分"""
        weights = {
            'clarity_improvement': 0.25,
            'completeness_enhancement': 0.25,
            'effectiveness_gain': 0.35,
            'interaction_efficiency': 0.15
        }

        overall_score = sum(
            evaluation_results[dimension] * weights[dimension]
            for dimension in weights.keys()
        )

        return overall_score

    def generate_evaluation_report(self, initial_prompt, optimized_prompt, scores, overall):
        """生成评估报告"""
        report = f"""
# 主动提示优化评估报告

## 总体评价
- **综合评分**: {overall:.4f}/1.000
- **优化状态**: {"优秀" if overall > 0.8 else "良好" if overall > 0.6 else "一般"}

## 分项评分

### 1. 清晰度改进 ({scores['clarity_improvement']:.4f})
- 指令明确性提升
- 结构组织优化
- 逻辑连贯性增强
- 可读性改善

### 2. 完整性增强 ({scores['completeness_enhancement']:.4f})
- 任务要求完整性
- 输入输出格式明确性
- 约束条件充分性
- 边界情况考虑

### 3. 有效性提升 ({scores['effectiveness_gain']:.4f})
- 任务性能改进
- 输出质量提升
- 预测准确性增强

### 4. 交互效率 ({scores['interaction_efficiency']:.4f})
- 优化轮次控制
- 改进幅度效率
- 早期收敛情况
- 问题相关性

## 原始提示
```
{initial_prompt}
```

## 优化后提示
```
{optimized_prompt}
```

## 改进要点
1. 通过主动澄清消除了歧义
2. 补充了缺失的关键信息
3. 优化了提示结构组织
4. 提升了整体有效性

## 建议
{self.generate_recommendations(scores)}
"""
        return report

    def generate_recommendations(self, scores):
        """生成改进建议"""
        recommendations = []

        if scores['clarity_improvement'] < 0.6:
            recommendations.append("进一步明确指令表述，简化复杂句式")

        if scores['completeness_enhancement'] < 0.6:
            recommendations.append("补充完整的输入输出格式和约束条件")

        if scores['effectiveness_gain'] < 0.5:
            recommendations.append("重点关注任务核心要素，增强示例针对性")

        if scores['interaction_efficiency'] < 0.5:
            recommendations.append("优化交互策略，减少不必要的澄清轮次")

        if not recommendations:
            recommendations.append("主动提示优化效果良好，可进一步应用于类似任务")

        return "\n".join([f"- {rec}" for rec in recommendations])

    def extract_score(self, evaluation_text):
        """从评估文本中提取评分（简化实现）"""
        # 简化的评分提取逻辑
        try:
            # 查找数字评分
            import re
            numbers = re.findall(r'(\d+(?:\.\d+)?)', evaluation_text)
            if numbers:
                # 返回第二个数字（优化后提示的评分）
                return min(float(numbers[1]) / 10, 1.0) if len(numbers) > 1 else float(numbers[0]) / 10
        except:
            pass

        return 0.7  # 默认评分
```

## 深度思考

### 主动提示的认知科学基础

**元认知能力模拟**

人类在学习和问题解决中展现出强大的元认知能力：
- **自我监控**：意识到自己的知识状态和不足
- **主动求助**：主动寻求外部信息或帮助
- **策略调整**：根据反馈调整方法和策略
- **深度思考**：通过提问深化理解

主动提示模拟这一过程：
```python
class MetacognitiveActivePrompt:
    """元认知主动提示"""
    def __init__(self):
        self.meta_knowledge = MetaKnowledgeBase()
        self.self_monitor = SelfMonitor()
        self.strategy_planner = StrategyPlanner()

    def metacognitive_optimization(self, task):
        """元认知优化流程"""
        # 1. 自我监控：评估当前理解状态
        current_state = self.self_monitor.assess_current_understanding(task)

        # 2. 识别知识缺口
        knowledge_gaps = self.identify_knowledge_gaps(current_state, task)

        # 3. 制定主动学习策略
        learning_strategy = self.strategy_planner.plan_active_learning(
            knowledge_gaps, current_state
        )

        # 4. 执行主动交互
        interaction_results = self.execute_active_interaction(learning_strategy, task)

        # 5. 整合新知识
        updated_prompt = self.integrate_new_knowledge(
            current_state, interaction_results
        )

        # 6. 更新元知识库
        self.meta_knowledge.update(
            task, updated_prompt, knowledge_gaps, learning_strategy
        )

        return updated_prompt

    def identify_knowledge_gaps(self, current_state, task):
        """识别知识缺口"""
        gap_analysis = {
            'task_requirements_gaps': self.analyze_requirement_gaps(current_state, task),
            'example_gaps': self.analyze_example_gaps(current_state, task),
            'constraint_gaps': self.analyze_constraint_gaps(current_state, task),
            'procedure_gaps': self.analyze_procedure_gaps(current_state, task)
        }
        return gap_analysis
```

**社会学习理论应用**

主动提示体现了社会学习理论的核心思想：
- **观察学习**：通过观察示例学习
- **交互学习**：通过问答互动学习
- **反馈修正**：根据反馈调整行为
- **协作学习**：人机协作解决问题

```python
class SocialLearningActivePrompt:
    """社会学习主动提示"""
    def __init__(self, llm):
        self.llm = llm
        self.learning_history = []

    def social_interaction_optimization(self, prompt, task):
        """社会交互式优化"""
        interaction_phases = {
            'observation': self.observation_phase(prompt, task),
            'imitation': self.imitation_phase(prompt, task),
            'practice': self.practice_phase(prompt, task),
            'feedback': self.feedback_phase(prompt, task),
            'refinement': self.refinement_phase(prompt, task)
        }

        # 整合各阶段结果
        optimized_prompt = self.integrate_interaction_phases(
            prompt, interaction_phases
        )

        return optimized_prompt

    def observation_phase(self, prompt, task):
        """观察阶段"""
        # 分析提示的结构和内容
        observation_result = self.analyze_prompt_structure(prompt, task)
        return {
            'phase': 'observation',
            'findings': observation_result,
            'questions': self.generate_observation_questions(observation_result)
        }

    def imitation_phase(self, prompt, task):
        """模仿阶段"""
        # 基于观察生成改进建议
        return {
            'phase': 'imitation',
            'improvements': self.generate_improvement_suggestions(prompt, task)
        }
```

### 主动提示的创新应用场景

**1. 教育辅助系统**
```python
class EducationalActivePrompt:
    """教育辅助主动提示系统"""
    def __init__(self, llm, student_profile):
        self.llm = llm
        self.student_profile = student_profile
        self.learning_objectives = self.extract_learning_objectives()

    def personalize_active_prompt(self, learning_content):
        """个性化主动提示"""
        # 分析学习内容
        content_analysis = self.analyze_learning_content(learning_content)

        # 评估学生当前理解水平
        student_understanding = self.assess_student_understanding(
            content_analysis, self.student_profile
        )

        # 识别学习难点
        learning_difficulties = self.identify_learning_difficulties(
            content_analysis, student_understanding
        )

        # 生成个性化澄清问题
        personalized_questions = self.generate_personalized_questions(
            learning_difficulties, self.student_profile
        )

        # 构建适应性示例
        adaptive_examples = self.generate_adaptive_examples(
            content_analysis, self.student_profile
        )

        # 生成个性化提示
        personalized_prompt = self.construct_personalized_prompt(
            learning_content, personalized_questions, adaptive_examples
        )

        return personalized_prompt

    def generate_personalized_questions(self, difficulties, profile):
        """生成个性化问题"""
        question_strategies = {
            'visual_learner': self.generate_visual_questions,
            'auditory_learner': self.generate_auditory_questions,
            'kinesthetic_learner': self.generate_kinesthetic_questions
        }

        strategy = question_strategies.get(profile['learning_style'], self.generate_general_questions)
        return strategy(difficulties)
```

**2. 医疗咨询助手**
```python
class MedicalConsultationActivePrompt:
    """医疗咨询主动提示"""
    def __init__(self, llm, medical_knowledge_base):
        self.llm = llm
        self.kb = medical_knowledge_base

    def active_diagnosis_prompt(self, initial_symptoms):
        """主动诊断提示"""
        # 1. 分析初始症状
        symptom_analysis = self.analyze_symptoms(initial_symptoms)

        # 2. 识别潜在疾病
        potential_conditions = self.identify_potential_conditions(symptom_analysis)

        # 3. 生成澄清问题
        clarification_questions = self.generate_diagnostic_questions(
            potential_conditions, symptom_analysis
        )

        # 4. 构建诊断示例
        diagnostic_examples = self.generate_diagnostic_examples(
            potential_conditions
        )

        # 5. 整合成诊断提示
        diagnosis_prompt = self.construct_diagnosis_prompt(
            initial_symptoms, clarification_questions, diagnostic_examples
        )

        return diagnosis_prompt

    def generate_diagnostic_questions(self, conditions, analysis):
        """生成诊断性澄清问题"""
        diagnostic_questions = []

        for condition in conditions:
            # 生成针对特定疾病的问题
            condition_questions = self.kb.get_diagnostic_questions(condition)
            diagnostic_questions.extend(condition_questions)

        # 优先级排序
        prioritized_questions = self.prioritize_questions(diagnostic_questions)

        return prioritized_questions[:5]  # 返回前5个最重要的问题
```

**3. 法律咨询系统**
```python
class LegalConsultationActivePrompt:
    """法律咨询主动提示"""
    def __init__(self, llm, legal_database):
        self.llm = llm
        self.db = legal_database

    def active_legal_analysis_prompt(self, legal_issue):
        """主动法律分析提示"""
        # 1. 识别法律问题类型
        issue_classification = self.classify_legal_issue(legal_issue)

        # 2. 检索相关法律条文
        relevant_laws = self.db.search_relevant_laws(issue_classification)

        # 3. 生成澄清问题
        clarification_questions = self.generate_legal_clarification_questions(
            legal_issue, issue_classification
        )

        # 4. 构建法律分析示例
        legal_precedents = self.db.search_precedents(issue_classification)

        # 5. 整合成法律分析提示
        legal_analysis_prompt = self.construct_legal_prompt(
            legal_issue, relevant_laws, clarification_questions, legal_precedents
        )

        return legal_analysis_prompt
```

### 主动提示的技术挑战与解决方案

**1. 交互成本控制**

挑战：多轮交互可能导致成本过高和用户疲劳

解决方案：
```python
class InteractionCostOptimizer:
    """交互成本优化器"""
    def __init__(self):
        self.cost_model = InteractionCostModel()
        self.efficiency_optimizer = EfficiencyOptimizer()

    def optimize_interaction_cost(self, initial_prompt, task, max_cost=100):
        """优化交互成本"""
        # 1. 评估问题的信息价值
        question_value_scores = self.assess_question_value(initial_prompt, task)

        # 2. 选择高价值低成本的交互策略
        optimal_strategy = self.select_optimal_strategy(
            question_value_scores, max_cost
        )

        # 3. 动态调整交互深度
        adaptive_interaction = self.adaptive_interaction_depth(
            initial_prompt, task, optimal_strategy
        )

        return adaptive_interaction

    def assess_question_value(self, prompt, task):
        """评估问题的信息价值"""
        value_dimensions = {
            'uncertainty_reduction': self.assess_uncertainty_reduction(prompt, task),
            'example_effectiveness': self.assess_example_effectiveness(prompt, task),
            'user_engagement': self.assess_user_engagement(prompt, task)
        }

        return value_dimensions
```

**2. 交互质量保证**

挑战：如何确保生成的澄清问题真正有助于优化

解决方案：
```python
class InteractionQualityAssurance:
    """交互质量保证"""
    def __init__(self, llm):
        self.llm = llm
        self.quality_criteria = QualityCriteria()

    def validate_interaction_quality(self, question, context):
        """验证交互质量"""
        quality_checks = {
            'relevance': self.check_question_relevance(question, context),
            'specificity': self.check_question_specificity(question),
            'actionability': self.check_question_actionability(question),
            'conciseness': self.check_question_conciseness(question)
        }

        # 计算质量评分
        quality_score = sum(quality_checks.values()) / len(quality_checks)

        # 生成改进建议
        if quality_score < 0.7:
            suggestions = self.generate_improvement_suggestions(question, quality_checks)
            return {
                'quality_score': quality_score,
                'quality_checks': quality_checks,
                'improvements': suggestions,
                'approved': False
            }

        return {
            'quality_score': quality_score,
            'quality_checks': quality_checks,
            'approved': True
        }
```

**3. 个性化适应**

挑战：如何适应不同用户的交互偏好和能力

解决方案：
```python
class PersonalizationEngine:
    """个性化引擎"""
    def __init__(self, llm):
        self.llm = llm
        self.user_model = UserModel()

    def personalize_interaction_style(self, user_profile, task):
        """个性化交互风格"""
        # 分析用户特征
        user_features = self.analyze_user_features(user_profile)

        # 确定交互风格
        interaction_style = self.determine_interaction_style(user_features)

        # 生成个性化问题
        personalized_questions = self.generate_personalized_questions(
            task, interaction_style
        )

        # 调整问题复杂度
        adapted_questions = self.adapt_question_complexity(
            personalized_questions, user_features
        )

        return adapted_questions

    def analyze_user_features(self, profile):
        """分析用户特征"""
        return {
            'expertise_level': profile.get('domain_expertise', 'intermediate'),
            'communication_style': profile.get('communication_style', 'direct'),
            'learning_preference': profile.get('learning_preference', 'balanced'),
            'attention_span': profile.get('attention_span', 'medium')
        }
```

## 质量评估

### 主动提示的质量评估框架

**1. 交互质量评估（Interaction Quality）**

评估主动提示系统的交互质量：

```python
def evaluate_interaction_quality(active_prompt_system, test_cases):
    """
    评估交互质量
    """
    quality_metrics = {
        'question_relevance': 0.0,
        'question_clarity': 0.0,
        'interaction_efficiency': 0.0,
        'user_satisfaction': 0.0,
        'task_improvement': 0.0
    }

    total_cases = len(test_cases)

    for case in test_cases:
        # 运行主动提示系统
        result = active_prompt_system.主动_optimize_prompt(
            case['initial_prompt'], case['task']
        )

        # 评估各项指标
        for metric in quality_metrics.keys():
            metric_value = evaluate_single_metric(metric, result, case)
            quality_metrics[metric] += metric_value

    # 计算平均值
    for metric in quality_metrics.keys():
        quality_metrics[metric] /= total_cases

    return quality_metrics

def evaluate_single_metric(metric_name, result, case):
    """评估单个指标"""
    if metric_name == 'question_relevance':
        # 评估问题的相关性
        questions = result['optimization_log'][0]['questions'] if result['optimization_log'] else []
        return assess_question_relevance(questions, case['task'])

    elif metric_name == 'interaction_efficiency':
        # 评估交互效率
        turns = len(result['optimization_log'])
        improvement = result['total_improvement']
        return improvement / max(turns, 1)

    # 其他指标评估...
    return 0.8  # 默认评分
```

**2. 优化效果评估（Optimization Effectiveness）**

评估主动提示的优化效果：

```python
def evaluate_optimization_effectiveness(baseline_prompt, optimized_prompt, task):
    """
    评估优化效果
    """
    effectiveness_dimensions = {
        'clarity_improvement': compare_clarity(baseline_prompt, optimized_prompt),
        'completeness_improvement': compare_completeness(baseline_prompt, optimized_prompt),
        'task_performance_gain': evaluate_task_performance(optimized_prompt, task),
        'consistency_improvement': compare_consistency(baseline_prompt, optimized_prompt)
    }

    # 计算综合效果评分
    overall_effectiveness = sum(effectiveness_dimensions.values()) / len(effectiveness_dimensions)

    return {
        'overall_effectiveness': overall_effectiveness,
        'detailed_metrics': effectiveness_dimensions
    }

def compare_clarity(prompt1, prompt2):
    """比较清晰度"""
    clarity_indicators = [
        '具体', '明确', '详细', '清晰',
        '模糊', '不明确', '模糊不清'
    ]

    def count_clarity_indicators(prompt):
        positive = sum(1 for indicator in clarity_indicators[:4] if indicator in prompt)
        negative = sum(1 for indicator in clarity_indicators[4:] if indicator in prompt)
        return positive - negative

    score1 = count_clarity_indicators(prompt1)
    score2 = count_clarity_indicators(prompt2)

    improvement = score2 - score1
    return max(0, min(improvement / 5, 1.0))
```

**3. 用户体验评估（User Experience）**

评估使用主动提示系统的用户体验：

```python
def evaluate_user_experience(active_prompt_interactions):
    """
    评估用户体验
    """
    experience_metrics = {
        'ease_of_use': assess_ease_of_use(active_prompt_interactions),
        'time_efficiency': assess_time_efficiency(active_prompt_interactions),
        'satisfaction': assess_user_satisfaction(active_prompt_interactions),
        'learning_value': assess_learning_value(active_prompt_interactions)
    }

    # 计算综合体验评分
    overall_experience = sum(experience_metrics.values()) / len(experience_metrics)

    return {
        'overall_experience': overall_experience,
        'experience_breakdown': experience_metrics
    }

def assess_ease_of_use(interactions):
    """评估易用性"""
    ease_indicators = {
        'natural_conversation': check_natural_conversation(interactions),
        'clear_questions': check_question_clarity(interactions),
        'relevant_suggestions': check_suggestion_relevance(interactions)
    }

    return sum(ease_indicators.values()) / len(ease_indicators)

def check_natural_conversation(interactions):
    """检查对话自然性"""
    # 分析对话流程的自然度
    natural_patterns = ['问题-回答-澄清', '逐步深入', '逻辑连贯']
    return 0.8  # 模拟评分
```

### 实际评估案例

**案例1：多任务类型评估**

```python
def evaluate_multitask_active_prompt(system, task_categories):
    """
    多任务类型主动提示评估
    """
    category_results = {}

    for category_name, tasks in task_categories.items():
        print(f"\n评估类别: {category_name}")

        category_scores = []
        for task in tasks:
            result = system.主动_optimize_prompt(task['initial_prompt'], task)

            # 计算该任务的综合评分
            task_score = calculate_comprehensive_score(result)
            category_scores.append(task_score)

        avg_score = sum(category_scores) / len(category_scores)
        category_results[category_name] = {
            'average_score': avg_score,
            'task_count': len(tasks),
            'improvement_rate': calculate_improvement_rate(category_scores)
        }

        print(f"  平均评分: {avg_score:.4f}")
        print(f"  改进率: {category_results[category_name]['improvement_rate']:.4f}")

    return category_results

def calculate_comprehensive_score(result):
    """计算综合评分"""
    if not result['optimization_log']:
        return 0.5

    scores = []
    for entry in result['optimization_log']:
        # 综合考虑改进幅度、问题质量、示例有效性
        improvement_score = min(entry['improvement'], 1.0)
        question_score = assess_question_quality(entry['questions'])
        example_score = assess_example_quality(entry['examples'])

        combined_score = (0.5 * improvement_score +
                         0.3 * question_score +
                         0.2 * example_score)

        scores.append(combined_score)

    return sum(scores) / len(scores)
```

## 完整学习框架

### 学习路径规划

**阶段1：基础理解（1-2周）**
- 学习主动提示的基本概念和原理
- 理解不确定性检测和交互机制
- 实现基础的问题生成和澄清系统

**阶段2：算法实现（2-3周）**
- 实现多轮对话式主动提示
- 构建智能示例生成系统
- 开发质量评估和优化机制

**阶段3：系统集成（2-3周）**
- 整合多个主动提示模块
- 构建完整的优化流程
- 实现个性化适应功能

**阶段4：应用实践（1-2周）**
- 在实际任务中应用系统
- 评估不同场景下的效果
- 总结最佳实践和经验

### 项目实践体系

**项目1：智能对话助手**
```python
class IntelligentConversationAssistant:
    """智能对话助手"""
    def __init__(self, llm):
        self.llm = llm
        self.active_prompt = BasicActivePromptSystem(llm, None)
        self.conversation_manager = ConversationManager(llm)

    def assist_conversation(self, user_input):
        """协助对话"""
        # 分析用户输入
        user_intent = self.analyze_user_intent(user_input)

        # 应用主动提示优化
        optimized_response = self.active_prompt.主动_optimize_prompt(
            user_intent['initial_prompt'], user_intent['task']
        )

        # 生成最终回复
        final_response = self.generate_final_response(
            optimized_response, user_intent
        )

        return final_response
```

**项目2：学习辅助系统**
```python
class LearningAssistanceSystem:
    """学习辅助系统"""
    def __init__(self, llm, student_model):
        self.llm = llm
        self.student = student_model
        self.active_educator = EducationalActivePrompt(llm, student_model)

    def personalize_learning_assistance(self, learning_material):
        """个性化学习辅助"""
        # 分析学习材料
        material_analysis = self.analyze_learning_material(learning_material)

        # 评估学生状态
        student_state = self.assess_student_state(self.student, material_analysis)

        # 生成个性化主动提示
        personalized_prompt = self.active_educator.personalize_active_prompt(
            learning_material
        )

        return personalized_prompt
```

### 评估认证体系

**技能认证标准**

```python
class ActivePromptCertification:
    """主动提示技能认证"""
    def __init__(self):
        self.certification_levels = {
            'beginner': {
                'knowledge': ['basic_concepts', 'uncertainty_detection', 'question_generation'],
                'skills': ['simple_interaction', 'basic_optimization', 'clarity_improvement'],
                'projects': ['basic_active_system', 'single_task_optimization']
            },
            'intermediate': {
                'knowledge': ['multi_turn_dialogue', 'example_generation', 'quality_assessment'],
                'skills': ['complex_optimization', 'interaction_design', 'personalization'],
                'projects': ['multitask_system', 'educational_assistant']
            },
            'advanced': {
                'knowledge': ['metacognitive_optimization', 'adaptive_learning', 'social_interaction'],
                'skills': ['innovative_application', 'system_architecture', 'performance_optimization'],
                'projects': ['research_platform', 'enterprise_solution']
            }
        }

    def evaluate_certification(self, candidate_portfolio):
        """评估认证级别"""
        for level, requirements in self.certification_levels.items():
            if self.meets_requirements(candidate_portfolio, requirements):
                return level

        return 'entry'
```

### 未来发展方向

**技术演进路径**

1. **更智能的交互策略**
   - 基于上下文的动态问题选择
   - 预测性澄清和问题预防
   - 多模态交互支持

2. **更强的个性化能力**
   - 用户建模和偏好学习
   - 自适应交互风格
   - 长期记忆和连续学习

3. **更高效的成本控制**
   - 智能交互预算管理
   - 价值导向的问题选择
   - 批量优化策略

4. **更广泛的应用领域**
   - 专业领域定制化
   - 跨语言交互支持
   - 群体智能和协作

**应用拓展方向**

1. **企业应用**
   - 智能客服和咨询系统
   - 员工培训和知识传递
   - 决策支持和分析

2. **教育领域**
   - 个性化学习助手
   - 智能答疑系统
   - 学习路径规划

3. **创意产业**
   - 内容创作辅助
   - 设计和创新支持
   - 艺术创作伙伴

### 总结与反思

**主动提示的核心价值**

主动提示代表了人机交互的新范式：
- **主动性**：系统不再被动响应，而是主动寻求信息
- **智能性**：通过智能交互提升理解和执行质量
- **适应性**：动态适应不同任务和用户需求
- **协作性**：实现真正的人机协作

**关键技术要素**

1. **不确定性检测**：准确识别提示中的模糊和不完整之处
2. **智能问题生成**：提出有价值的澄清问题
3. **多轮对话管理**：维持连贯和有效的对话流程
4. **质量评估与优化**：确保交互的质量和效果

**学习建议**

1. **理解人性**：深入理解人类的思维和交互模式
2. **注重体验**：始终以用户体验为中心设计交互
3. **平衡效率**：在优化效果和交互成本之间找到平衡
4. **持续迭代**：基于反馈持续改进交互策略

**挑战与机遇**

主动提示面临的挑战：
- **交互成本**：多轮交互可能增加时间和资源消耗
- **用户疲劳**：过度交互可能导致用户不满
- **质量保证**：确保每次交互都真正有价值

同时带来的机遇：
- **深度理解**：通过主动交互实现更深入的理解
- **个性化服务**：为不同用户提供定制化体验
- **智能化提升**：推动AI系统向更高智能化水平发展

通过系统学习主动提示技术，您将掌握构建智能交互系统的核心能力，为创建真正智能、友好、高效的AI应用奠定坚实基础。

---

## 本章小结

主动提示是一种通过模型主动提出问题、请求澄清和生成示例来改进提示质量的技术，代表了人机交互向更高智能化水平发展的重要方向。

### 核心要点
- **技术原理**：通过不确定性检测、主动提问、示例生成等多轮交互，自动发现并改进提示中的问题
- **分类体系**：包括澄清导向、示例导向、迭代导向等多种优化策略
- **应用领域**：教育辅助、医疗咨询、法律服务等多个需要深度理解的场景
- **创新价值**：实现真正的人机协作，提升AI系统的智能化和用户体验

### 实践价值
掌握主动提示技术能够：
- 构建智能交互式AI系统
- 提升用户与AI的协作效率
- 实现个性化和定制化服务
- 推动AI向更高智能化水平发展

### 技能认证
通过本章学习，您应该能够：
1. 理解主动提示的基本原理和交互机制
2. 实现多轮对话式的主动提示系统
3. 构建智能示例生成和优化系统
4. 开发主动提示的质量评估和优化平台

主动提示代表了AI系统从被动响应向主动协作的重要转变，通过智能交互为构建更人性化、更高效的AI系统提供了新的技术路径。