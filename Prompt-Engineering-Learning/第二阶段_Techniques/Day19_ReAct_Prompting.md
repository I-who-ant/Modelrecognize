
# Day 17: ReAct（Reasoning and Acting）提示技术

## 理论学习

### ReAct的核心原理

ReAct（Reasoning and Acting）是一种将推理（Reasoning）和行动（Acting）结合起来的提示技术框架。
该技术由Google Research提出，通过让大语言模型在推理过程中显式地调用外部工具和采取行动，形成"思考-行动-观察"的循环机制，从而解决复杂的多步骤问题。

#### 技术机制与工作原理

**核心流程：**
1. **推理阶段（Reasoning）**
   - 分析当前问题和上下文
   - 生成推理步骤和行动计划
   - 确定下一步需要采取的行动

2. **行动阶段（Acting）**
   - 根据推理结果调用合适的工具
   - 执行具体的操作或查询
   - 获取行动结果和环境反馈

3. **观察阶段（Observation）**
   - 收集和分析行动结果
   - 更新对问题的理解和状态
   - 为下一轮推理提供新信息

4. **循环迭代**
   - 基于观察结果继续推理
   - 重复"推理-行动-观察"循环
   - 直到得出最终答案

**技术创新点：**
- **透明化推理**：显式展示模型的推理过程和逻辑
- **工具集成**：无缝集成外部工具和API调用
- **动态适应**：根据执行结果动态调整推理路径
- **可验证性**：每个推理步骤都有可观察的行动支撑

#### 理论基础

**ReAct架构模型**
```
ReAct = Repeat(Reason → Act → Observe) + Final_Answer

其中：
- Reason: 推理函数，分析当前状态和问题
- Act: 行动函数，调用工具或执行操作
- Observe: 观察函数，处理行动结果
- Final_Answer: 最终答案生成
```

**分层执行架构**
```
第一层：问题理解层（Problem Understanding Layer）
输入：用户问题
输出：问题理解和初始状态

第二层：推理计划层（Reasoning Planning Layer）
输入：当前状态
输出：推理步骤和行动计划

第三层：工具执行层（Tool Execution Layer）
输入：行动指令
输出：工具执行结果

第四层：结果观察层（Result Observation Layer）
输入：工具输出
输出：观察结果和状态更新

第五层：答案生成层（Answer Generation Layer）
输入：最终状态
输出：最终答案和推理总结
```

**推理-行动循环模型**
```python
class ReActCycle:
    """ReAct循环执行器"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.max_iterations = 10
        self.memory = []

    def reason_act_observe_loop(self, question, initial_context=None):
        """
        执行ReAct循环

        Args:
            question: 用户问题
            initial_context: 初始上下文

        Returns:
            dict: 包含推理过程和最终答案的结果
        """
        current_state = {
            'question': question,
            'context': initial_context or {},
            'reasoning_trace': [],
            'action_results': [],
            'observations': []
        }

        for iteration in range(self.max_iterations):
            # 1. 推理阶段
            reasoning = self.generate_reasoning(current_state)
            current_state['reasoning_trace'].append(reasoning)

            # 检查是否完成
            if self.is_task_complete(reasoning, current_state):
                break

            # 2. 行动阶段
            action = self.generate_action(reasoning, current_state)
            if action:
                action_result = self.execute_action(action)
                current_state['action_results'].append(action_result)

                # 3. 观察阶段
                observation = self.process_observation(action_result)
                current_state['observations'].append(observation)

                # 更新状态
                current_state['context'] = self.update_context(
                    current_state['context'], observation
                )
            else:
                # 如果没有可执行行动，结束循环
                break

        # 生成最终答案
        final_answer = self.generate_final_answer(current_state)

        return {
            'question': question,
            'reasoning_trace': current_state['reasoning_trace'],
            'action_results': current_state['action_results'],
            'observations': current_state['observations'],
            'final_answer': final_answer,
            'iterations': iteration + 1
        }

    def generate_reasoning(self, state):
        """生成推理步骤"""
        reasoning_prompt = f"""
        分析当前问题和上下文，生成推理步骤：

        问题：{state['question']}

        当前上下文：
        {self.format_context(state['context'])}

        已有推理：
        {self.format_reasoning_trace(state['reasoning_trace'])}

        已有观察：
        {self.format_observations(state['observations'])}

        请生成下一步的推理思考：
        """
        reasoning = self.llm.generate(reasoning_prompt, max_tokens=300)
        return reasoning.strip()

    def generate_action(self, reasoning, state):
        """基于推理生成行动"""
        action_prompt = f"""
        基于以下推理，生成具体的行动指令：

        推理：{reasoning}

        可用工具：
        {self.format_available_tools()}

        请选择合适的工具并生成行动指令，格式：
        行动: [工具名称] - [具体参数]
        """
        action_response = self.llm.generate(action_prompt, max_tokens=150)

        # 解析行动
        return self.parse_action(action_response)

    def execute_action(self, action):
        """执行行动"""
        if not action:
            return None

        tool_name = action['tool']
        parameters = action['parameters']

        if tool_name in self.tools:
            result = self.tools[tool_name].execute(**parameters)
            return {
                'tool': tool_name,
                'parameters': parameters,
                'result': result,
                'success': True
            }
        else:
            return {
                'tool': tool_name,
                'parameters': parameters,
                'error': f"工具 {tool_name} 不存在",
                'success': False
            }

    def process_observation(self, action_result):
        """处理观察结果"""
        if not action_result or not action_result.get('success'):
            return {
                'observation': "行动执行失败",
                'status': 'failure'
            }

        observation_prompt = f"""
        基于以下行动结果，生成观察总结：

        行动：{action_result['tool']}
        参数：{action_result['parameters']}
        结果：{action_result['result']}

        请简洁总结观察到的关键信息：
        """
        observation = self.llm.generate(observation_prompt, max_tokens=200)
        return {
            'observation': observation.strip(),
            'status': 'success',
            'raw_result': action_result['result']
        }

    def is_task_complete(self, reasoning, state):
        """判断任务是否完成"""
        completion_prompt = f"""
        基于以下推理，判断任务是否完成：

        问题：{state['question']}
        当前推理：{reasoning}

        已执行行动数量：{len(state['action_results'])}
        已观察结果：{len(state['observations'])}

        请回答：任务是否已经完成并可以给出最终答案？（是/否）
        """
        response = self.llm.generate(completion_prompt, max_tokens=50)
        return "是" in response

    def generate_final_answer(self, state):
        """生成最终答案"""
        answer_prompt = f"""
        基于完整的推理过程和观察结果，回答原始问题：

        问题：{state['question']}

        完整推理过程：
        {self.format_reasoning_trace(state['reasoning_trace'])}

        所有观察结果：
        {self.format_observations(state['observations'])}

        请提供完整的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=600)

    def format_context(self, context):
        """格式化上下文"""
        if not context:
            return "无"
        return str(context)

    def format_reasoning_trace(self, trace):
        """格式化推理轨迹"""
        return "\n".join([f"{i+1}. {r}" for i, r in enumerate(trace)])

    def format_observations(self, observations):
        """格式化观察结果"""
        return "\n".join([f"{i+1}. {o['observation']}" for i, o in enumerate(observations)])

    def format_available_tools(self):
        """格式化可用工具"""
        tool_list = []
        for name, tool in self.tools.items():
            tool_list.append(f"- {name}: {tool.description}")
        return "\n".join(tool_list)

    def parse_action(self, action_response):
        """解析行动响应"""
        # 简化的行动解析
        if "行动:" in action_response:
            lines = action_response.split("\n")
            for line in lines:
                if "行动:" in line:
                    # 解析工具名称和参数
                    # 这里需要更复杂的解析逻辑
                    return {
                        'tool': 'search',  # 默认工具
                        'parameters': {'query': 'default'}
                    }
        return None

    def update_context(self, current_context, observation):
        """更新上下文"""
        updated = current_context.copy()
        # 根据观察结果更新上下文
        # 这里需要根据具体应用场景实现
        return updated
```

### ReAct vs 其他技术对比

**vs Chain-of-Thought (CoT)**
| 维度 | ReAct | CoT |
|------|-------|-----|
| 推理透明度 | 高（显式推理+行动） | 中（纯推理） |
| 工具使用 | 强（集成外部工具） | 弱（仅内部推理） |
| 可验证性 | 高（行动可验证） | 低（推理难验证） |
| 适应性 | 强（基于反馈调整） | 中（固定路径） |
| 复杂性 | 高（循环执行） | 中（线性推理） |

**vs Program-Aided Language Model (PAL)**
| 维度 | ReAct | PAL |
|------|-------|-----|
| 执行模式 | 推理-行动循环 | 代码生成执行 |
| 工具集成 | 通用工具框架 | 程序执行环境 |
| 动态性 | 强（实时调整） | 中（预设程序） |
| 错误处理 | 自动重试 | 程序调试 |
| 适用场景 | 广泛（多工具） | 专门（计算为主） |

### ReAct的分类体系

**1. 同步ReAct（Synchronous ReAct）**

串行执行推理和行动：

```python
class SynchronousReAct:
    """同步ReAct执行器"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    def execute_synchronous(self, question):
        """同步执行ReAct"""
        state = self.initialize_state(question)
        iteration = 0

        while not self.is_complete(state) and iteration < self.max_iterations:
            # 推理
            reasoning = self.reason(state)

            # 行动
            action = self.plan_action(reasoning, state)
            if action:
                result = self.execute_action(action)

                # 观察
                observation = self.observe(result)

                # 更新状态
                state = self.update_state(state, observation)

            iteration += 1

        return self.finalize(state)

    def reason(self, state):
        """推理阶段"""
        prompt = self.build_reasoning_prompt(state)
        return self.llm.generate(prompt)

    def plan_action(self, reasoning, state):
        """计划行动"""
        prompt = self.build_action_prompt(reasoning, state)
        response = self.llm.generate(prompt)
        return self.parse_action(response)

    def execute_action(self, action):
        """执行行动"""
        tool = self.tools.get(action['tool'])
        if tool:
            return tool.execute(**action['parameters'])
        return None

    def observe(self, result):
        """观察结果"""
        if result:
            return {
                'type': 'success',
                'data': result,
                'summary': self.summarize_result(result)
            }
        return {
            'type': 'failure',
            'error': '行动执行失败'
        }

    def is_complete(self, state):
        """检查是否完成"""
        # 基于状态判断是否完成
        return state.get('completed', False)

    def build_reasoning_prompt(self, state):
        """构建推理提示"""
        return f"""
        问题: {state['question']}
        上下文: {state.get('context', {})}
        已完成步骤: {len(state.get('steps', []))}

        请分析当前状态，确定下一步应该做什么。
        """

    def build_action_prompt(self, reasoning, state):
        """构建行动提示"""
        available_tools = list(self.tools.keys())
        return f"""
        基于以下推理，选择合适的行动：

        推理: {reasoning}

        可用工具: {available_tools}

        请以JSON格式返回行动：
        {{"tool": "工具名", "parameters": {{}}}}
        """

    def parse_action(self, response):
        """解析行动"""
        try:
            import json
            return json.loads(response)
        except:
            return None

    def summarize_result(self, result):
        """总结结果"""
        return f"执行结果: {str(result)[:100]}"
```

**2. 并行ReAct（Parallel ReAct）**

并行执行多个推理-行动路径：

```python
class ParallelReAct:
    """并行ReAct执行器"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.num_paths = 3

    def execute_parallel(self, question):
        """并行执行多个ReAct路径"""
        # 生成多个初始路径
        initial_prompts = self.generate_initial_prompts(question)

        # 并行执行每个路径
        paths = []
        for i, prompt in enumerate(initial_prompts):
            path = self.execute_single_path(question, prompt, path_id=i)
            paths.append(path)

        # 选择最佳路径
        best_path = self.select_best_path(paths)

        return best_path

    def execute_single_path(self, question, initial_prompt, path_id):
        """执行单条路径"""
        state = {
            'question': question,
            'path_id': path_id,
            'initial_prompt': initial_prompt,
            'steps': [],
            'observations': []
        }

        for iteration in range(self.max_iterations):
            # 基于路径特定的提示推理
            reasoning = self.path_specific_reasoning(state)

            # 生成行动
            action = self.generate_path_action(reasoning, state)

            if action:
                result = self.execute_action(action)

                # 观察和记录
                observation = self.record_observation(result, path_id)
                state['observations'].append(observation)

                # 更新状态
                state = self.update_path_state(state, observation)

            # 检查完成条件
            if self.is_path_complete(state):
                break

        return state

    def generate_initial_prompts(self, question):
        """生成初始推理路径提示"""
        base_prompt = f"问题: {question}\n请开始推理和行动："

        variants = [
            f"{base_prompt}\n方法1: 直接分析问题",
            f"{base_prompt}\n方法2: 分解问题为子问题",
            f"{base_prompt}\n方法3: 从已知信息开始"
        ]

        return variants

    def path_specific_reasoning(self, state):
        """路径特定的推理"""
        path_context = f"路径{state['path_id']}的推理历史:\n"
        path_context += "\n".join([step['reasoning'] for step in state['steps']])

        prompt = f"""
        {path_context}

        当前问题: {state['question']}
        当前观察: {state['observations'][-1] if state['observations'] else '无'}

        请继续推理：
        """
        return self.llm.generate(prompt)

    def select_best_path(self, paths):
        """选择最佳路径"""
        scores = []
        for path in paths:
            score = self.evaluate_path_quality(path)
            scores.append(score)

        best_idx = scores.index(max(scores))
        return paths[best_idx]

    def evaluate_path_quality(self, path):
        """评估路径质量"""
        factors = [
            len(path['observations']) * 0.3,  # 探索深度
            path.get('success_rate', 0.5) * 0.4,  # 成功率
            path.get('efficiency', 0.5) * 0.3  # 效率
        ]
        return sum(factors)
```

**3. 分层ReAct（Hierarchical ReAct）**

多层次的推理-行动结构：

```python
class HierarchicalReAct:
    """分层ReAct执行器"""
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.num_levels = 3

    def execute_hierarchical(self, question):
        """分层执行ReAct"""
        # 顶层规划
        top_level_plan = self.generate_top_level_plan(question)

        # 中层分解
        mid_level_tasks = self.decompose_to_mid_level(top_level_plan)

        # 底层执行
        final_results = []
        for task in mid_level_tasks:
            result = self.execute_low_level(task)
            final_results.append(result)

        # 整合结果
        integrated_answer = self.integrate_results(final_results, question)

        return {
            'question': question,
            'top_level_plan': top_level_plan,
            'mid_level_tasks': mid_level_tasks,
            'low_level_results': final_results,
            'final_answer': integrated_answer
        }

    def generate_top_level_plan(self, question):
        """生成顶层计划"""
        prompt = f"""
        针对问题制定高层执行计划：

        问题：{question}

        请制定3-5个主要步骤的计划：
        """
        plan = self.llm.generate(prompt, max_tokens=400)
        return self.parse_plan(plan)

    def decompose_to_mid_level(self, top_plan):
        """分解为中层任务"""
        mid_level_tasks = []
        for step in top_plan['steps']:
            task_prompt = f"""
            将以下高层步骤分解为具体的ReAct任务：

            高层步骤：{step['description']}

            请提供：
            1. 具体的推理步骤
            2. 需要的工具和行动
            3. 预期结果

            中层任务：
            """
            task = self.llm.generate(task_prompt, max_tokens=300)
            mid_level_tasks.append({
                'parent_step': step,
                'task_description': task
            })

        return mid_level_tasks

    def execute_low_level(self, task):
        """执行底层ReAct任务"""
        # 使用基本的ReAct循环执行
        react_executor = SynchronousReAct(self.llm, self.tools)
        result = react_executor.execute_synchronous(task['task_description'])
        return {
            'task': task,
            'react_result': result
        }

    def integrate_results(self, results, original_question):
        """整合结果"""
        integration_prompt = f"""
        整合以下任务结果，回答原始问题：

        原始问题：{original_question}

        任务结果：
        {chr(10).join([
            f"任务{i+1}: {result['react_result']['final_answer']}"
            for i, result in enumerate(results)
        ])}

        请提供完整的整合答案：
        """
        return self.llm.generate(integration_prompt, max_tokens=600)

    def parse_plan(self, plan_text):
        """解析计划文本"""
        # 简化的计划解析
        steps = []
        lines = plan_text.split('\n')
        for line in lines:
            if '步骤' in line or 'Step' in line:
                steps.append({
                    'description': line.strip(),
                    'id': len(steps) + 1
                })
        return {'steps': steps}
```

### ReAct系统的核心技术

**1. 推理链生成（Reasoning Chain Generation）**

```python
class ReasoningChainGenerator:
    """推理链生成器"""
    def __init__(self, llm):
        self.llm = llm

    def generate_reasoning_chain(self, question, context=None):
        """生成推理链"""
        chain = []
        current_question = question

        while True:
            # 生成下一步推理
            reasoning_step = self.generate_next_reasoning(
                current_question, context, chain
            )

            # 检查是否完成
            if self.is_reasoning_complete(reasoning_step):
                break

            chain.append(reasoning_step)

            # 更新问题
            current_question = self.extract_next_question(reasoning_step)

        return chain

    def generate_next_reasoning(self, question, context, previous_steps):
        """生成下一步推理"""
        context_text = self.format_context(context)
        previous_text = self.format_previous_steps(previous_steps)

        prompt = f"""
        基于以下信息，生成下一步推理：

        当前问题：{question}
        上下文：{context_text}
        已有推理步骤：
        {previous_text}

        请生成：
        1. 当前的分析和推理
        2. 需要采取的行动（如果需要）
        3. 下一步的问题（如果需要）

        推理步骤：
        """
        reasoning = self.llm.generate(prompt, max_tokens=400)
        return self.parse_reasoning_step(reasoning)

    def parse_reasoning_step(self, reasoning_text):
        """解析推理步骤"""
        # 简化的推理步骤解析
        return {
            'reasoning': reasoning_text,
            'actions': self.extract_actions(reasoning_text),
            'next_question': self.extract_next_question(reasoning_text)
        }

    def extract_actions(self, reasoning_text):
        """从推理中提取行动"""
        # 简单的关键词匹配
        action_keywords = ['查询', '搜索', '计算', '分析', '调用']
        actions = []
        for keyword in action_keywords:
            if keyword in reasoning_text:
                actions.append(keyword)
        return actions

    def extract_next_question(self, reasoning_text):
        """提取下一步问题"""
        # 简化的提取逻辑
        if '接下来' in reasoning_text or '下一步' in reasoning_text:
            return "继续推理"
        return None

    def is_reasoning_complete(self, reasoning_step):
        """判断推理是否完成"""
        completion_indicators = ['完成', '结束', '得出结论', '答案是']
        reasoning = reasoning_step['reasoning']
        return any(indicator in reasoning for indicator in completion_indicators)

    def format_context(self, context):
        """格式化上下文"""
        if not context:
            return "无"
        return str(context)

    def format_previous_steps(self, steps):
        """格式化已有步骤"""
        if not steps:
            return "无"
        return "\n".join([f"{i+1}. {step['reasoning'][:100]}" for i, step in enumerate(steps)])
```

**2. 行动选择与执行（Action Selection & Execution）**

```python
class ActionSelector:
    """行动选择器"""
    def __init__(self, llm, tools, action_history):
        self.llm = llm
        self.tools = tools
        self.action_history = action_history

    def select_optimal_action(self, reasoning, current_state):
        """选择最优行动"""
        # 1. 识别潜在行动
        potential_actions = self.identify_potential_actions(reasoning)

        # 2. 评估行动可行性
        feasible_actions = self.evaluate_action_feasibility(
            potential_actions, current_state
        )

        # 3. 选择最佳行动
        if feasible_actions:
            best_action = self.select_best_action(
                feasible_actions, current_state
            )
            return best_action

        return None

    def identify_potential_actions(self, reasoning):
        """识别潜在行动"""
        action_prompt = f"""
        基于以下推理，识别需要采取的行动：

        推理内容：{reasoning}

        请列出所有可能需要的行动（使用工具名称）：
        1. 搜索类行动：search, query, lookup
        2. 计算类行动：calculate, compute, evaluate
        3. 分析类行动：analyze, compare, classify
        4. 获取类行动：fetch, get, retrieve
        5. 其他行动：请描述

        潜在行动：
        """
        response = self.llm.generate(action_prompt, max_tokens=300)
        return self.parse_actions(response)

    def evaluate_action_feasibility(self, actions, state):
        """评估行动可行性"""
        feasible = []
        for action in actions:
            # 检查工具是否存在
            if action['tool'] in self.tools:
                # 检查参数是否合理
                if self.validate_action_parameters(action, state):
                    feasible.append(action)

        return feasible

    def select_best_action(self, feasible_actions, state):
        """选择最佳行动"""
        if len(feasible_actions) == 1:
            return feasible_actions[0]

        # 多行动时基于启发式选择
        action_scores = []
        for action in feasible_actions:
            score = self.score_action(action, state)
            action_scores.append((action, score))

        # 选择得分最高的行动
        best_action = max(action_scores, key=lambda x: x[1])[0]
        return best_action

    def score_action(self, action, state):
        """为行动评分"""
        score = 0.0

        # 基于工具适用性评分
        tool = self.tools[action['tool']]
        if hasattr(tool, 'relevance_score'):
            score += tool.relevance_score * 0.4

        # 基于历史成功率评分
        history_score = self.get_action_history_score(action)
        score += history_score * 0.3

        # 基于效率评分
        efficiency_score = self.get_action_efficiency_score(action)
        score += efficiency_score * 0.3

        return score

    def get_action_history_score(self, action):
        """获取行动历史分数"""
        tool_name = action['tool']
        history = self.action_history.get(tool_name, [])

        if not history:
            return 0.5  # 默认分数

        successful = sum(1 for h in history if h.get('success', False))
        return successful / len(history)

    def get_action_efficiency_score(self, action):
        """获取行动效率分数"""
        # 简化的效率评分
        return 0.8  # 默认效率分数

    def validate_action_parameters(self, action, state):
        """验证行动参数"""
        # 简化的参数验证
        required_params = self.tools[action['tool']].required_params
        provided_params = action.get('parameters', {})

        return all(param in provided_params for param in required_params)

    def parse_actions(self, response_text):
        """解析行动列表"""
        actions = []
        lines = response_text.split('\n')

        for line in lines:
            if line.strip() and not line.startswith('#'):
                # 简单的行动解析
                action = {
                    'tool': self.extract_tool_name(line),
                    'parameters': {}
                }
                actions.append(action)

        return actions

    def extract_tool_name(self, line):
        """从行中提取工具名"""
        # 简化的工具名提取
        tools = ['search', 'calculate', 'analyze', 'fetch', 'get']
        for tool in tools:
            if tool in line.lower():
                return tool
        return 'search'  # 默认工具
```

**3. 观察结果处理（Observation Processing）**

```python
class ObservationProcessor:
    """观察结果处理器"""
    def __init__(self, llm):
        self.llm = llm

    def process_observation(self, action_result, action, context):
        """处理观察结果"""
        # 1. 提取关键信息
        key_info = self.extract_key_information(action_result)

        # 2. 更新上下文
        updated_context = self.update_context(context, key_info, action)

        # 3. 生成观察总结
        observation_summary = self.generate_observation_summary(
            action_result, key_info
        )

        return {
            'key_info': key_info,
            'updated_context': updated_context,
            'summary': observation_summary,
            'relevance_score': self.assess_relevance(key_info, context)
        }

    def extract_key_information(self, action_result):
        """提取关键信息"""
        if not action_result.get('success', False):
            return {
                'type': 'error',
                'content': action_result.get('error', '未知错误'),
                'importance': 'high'
            }

        result_data = action_result['result']

        # 使用LLM提取关键信息
        extraction_prompt = f"""
        从以下结果中提取关键信息：

        结果：{result_data}

        请提取：
        1. 主要发现
        2. 重要数据
        3. 相关结论
        4. 置信度

        格式：JSON
        """
        try:
            response = self.llm.generate(extraction_prompt, max_tokens=400)
            key_info = self.parse_extracted_info(response)
            key_info['type'] = 'success'
            return key_info
        except:
            return {
                'type': 'partial',
                'content': str(result_data)[:200],
                'importance': 'medium'
            }

    def update_context(self, current_context, key_info, action):
        """更新上下文"""
        updated = current_context.copy()

        # 添加新的观察信息
        observation_id = len(updated.get('observations', [])) + 1
        updated['observations'] = updated.get('observations', [])
        updated['observations'].append({
            'id': observation_id,
            'action': action,
            'key_info': key_info,
            'timestamp': datetime.now().isoformat()
        })

        # 更新相关状态
        updated['last_update'] = datetime.now().isoformat()

        return updated

    def generate_observation_summary(self, action_result, key_info):
        """生成观察总结"""
        summary_prompt = f"""
        为以下观察生成简洁总结：

        行动：{action_result['tool']}
        结果：{action_result['result']}
        关键信息：{key_info}

        总结：
        """
        summary = self.llm.generate(summary_prompt, max_tokens=200)
        return summary.strip()

    def assess_relevance(self, key_info, context):
        """评估观察相关性"""
        # 基于信息类型和上下文计算相关性
        relevance_factors = [
            self.calculate_type_relevance(key_info.get('type')),
            self.calculate_content_relevance(key_info, context),
            self.calculate_importance_relevance(key_info.get('importance'))
        ]

        return sum(relevance_factors) / len(relevance_factors)

    def calculate_type_relevance(self, info_type):
        """计算类型相关性"""
        type_scores = {
            'success': 0.9,
            'partial': 0.6,
            'error': 0.3,
            'warning': 0.5
        }
        return type_scores.get(info_type, 0.5)

    def calculate_content_relevance(self, key_info, context):
        """计算内容相关性"""
        # 简化的内容相关性计算
        return 0.7  # 默认相关性

    def calculate_importance_relevance(self, importance):
        """计算重要性相关性"""
        importance_scores = {
            'high': 0.9,
            'medium': 0.6,
            'low': 0.3
        }
        return importance_scores.get(importance, 0.5)

    def parse_extracted_info(self, response_text):
        """解析提取的信息"""
        try:
            import json
            return json.loads(response_text)
        except:
            # 备用解析方法
            return {
                'content': response_text,
                'importance': 'medium'
            }
```

## 实践任务

### 任务1：基础ReAct系统实现

**目标：**
实现一个基础的ReAct系统，能够进行"推理-行动-观察"的循环执行。

**步骤1：核心ReAct系统**
```python
class BasicReActSystem:
    """基础ReAct系统"""
    def __init__(self, llm):
        self.llm = llm
        self.tools = {}
        self.memory = ReActMemory()
        self.max_iterations = 10

    def register_tool(self, name, tool_instance):
        """注册工具"""
        self.tools[name] = tool_instance
        print(f"注册工具: {name}")

    def solve_question(self, question, context=None):
        """
        解决用户问题

        Args:
            question: 用户问题
            context: 初始上下文

        Returns:
            dict: 包含推理过程和答案的结果
        """
        print(f"\n开始解决: {question}")

        # 初始化状态
        state = {
            'question': question,
            'context': context or {},
            'iteration': 0,
            'reasoning_steps': [],
            'actions': [],
            'observations': []
        }

        # 执行ReAct循环
        for iteration in range(self.max_iterations):
            print(f"\n--- 迭代 {iteration + 1} ---")

            state['iteration'] = iteration + 1

            # 1. 推理阶段
            reasoning = self.reason(state)
            state['reasoning_steps'].append(reasoning)
            print(f"推理: {reasoning[:100]}...")

            # 2. 检查是否完成
            if self.is_task_complete(reasoning, state):
                print("任务完成，生成最终答案")
                break

            # 3. 行动阶段
            action = self.select_action(reasoning, state)
            if action:
                state['actions'].append(action)
                print(f"行动: {action['tool']} - {action['parameters']}")

                # 4. 执行行动
                action_result = self.execute_action(action)
                print(f"结果: {action_result.get('status', 'unknown')}")

                # 5. 观察阶段
                observation = self.process_observation(
                    action_result, action, state
                )
                state['observations'].append(observation)
                print(f"观察: {observation['summary'][:100]}...")

                # 6. 更新上下文
                state['context'] = observation['updated_context']
            else:
                print("无法确定下一步行动，结束循环")
                break

        # 生成最终答案
        final_answer = self.generate_final_answer(state)

        return {
            'question': question,
            'reasoning_steps': state['reasoning_steps'],
            'actions': state['actions'],
            'observations': state['observations'],
            'final_answer': final_answer,
            'iterations': state['iteration']
        }

    def reason(self, state):
        """推理阶段"""
        context_str = self.format_context(state['context'])
        reasoning_history = self.format_reasoning_history(
            state['reasoning_steps']
        )

        reasoning_prompt = f"""
        作为ReAct系统的推理组件，分析当前问题并确定下一步行动。

        问题：{state['question']}
        当前上下文：
        {context_str}

        已完成的推理步骤：
        {reasoning_history}

        当前迭代：{state['iteration']}

        请提供：
        1. 当前问题的分析
        2. 需要采取的行动（如果需要）
        3. 预期的观察结果（如果采取行动）

        推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=400)

    def select_action(self, reasoning, state):
        """选择行动"""
        # 检查推理中是否提到需要采取行动
        action_keywords = ['搜索', '查询', '计算', '分析', '获取', '调用']
        needs_action = any(keyword in reasoning for keyword in action_keywords)

        if not needs_action:
            return None

        # 选择合适的工具
        available_tools = list(self.tools.keys())
        tool_selection_prompt = f"""
        基于以下推理，选择合适的工具和参数：

        推理：{reasoning}
        问题：{state['question']}
        可用工具：{available_tools}

        请以JSON格式返回：
        {{
            "tool": "工具名称",
            "parameters": {{"param1": "value1", "param2": "value2"}}
        }}

        工具选择：
        """
        response = self.llm.generate(tool_selection_prompt, max_tokens=200)

        try:
            import json
            action = json.loads(response)
            # 验证工具是否存在
            if action['tool'] in self.tools:
                return action
        except:
            pass

        # 默认搜索工具
        return {
            'tool': 'search',
            'parameters': {'query': state['question']}
        }

    def execute_action(self, action):
        """执行行动"""
        tool_name = action['tool']
        parameters = action['parameters']

        if tool_name in self.tools:
            tool = self.tools[tool_name]
            try:
                result = tool.execute(**parameters)
                return {
                    'status': 'success',
                    'result': result,
                    'tool': tool_name,
                    'parameters': parameters
                }
            except Exception as e:
                return {
                    'status': 'error',
                    'error': str(e),
                    'tool': tool_name,
                    'parameters': parameters
                }
        else:
            return {
                'status': 'error',
                'error': f'工具 {tool_name} 不存在',
                'tool': tool_name,
                'parameters': parameters
            }

    def process_observation(self, action_result, action, state):
        """处理观察结果"""
        observation_processor = ObservationProcessor(self.llm)
        return observation_processor.process_observation(
            action_result, action, state['context']
        )

    def is_task_complete(self, reasoning, state):
        """判断任务是否完成"""
        completion_prompt = f"""
        基于以下信息，判断问题是否已经解决：

        问题：{state['question']}
        当前推理：{reasoning}

        已执行行动数：{len(state['actions'])}
        已收集观察数：{len(state['observations'])}

        回答：是 或 否
        """
        response = self.llm.generate(completion_prompt, max_tokens=50)
        return '是' in response

    def generate_final_answer(self, state):
        """生成最终答案"""
        answer_prompt = f"""
        基于完整的ReAct推理过程，回答原始问题：

        问题：{state['question']}

        推理步骤：
        {chr(10).join([
            f"{i+1}. {step[:200]}"
            for i, step in enumerate(state['reasoning_steps'])
        ])}

        观察结果：
        {chr(10).join([
            f"{i+1}. {obs['summary'][:200]}"
            for i, obs in enumerate(state['observations'])
        ])}

        请提供完整、准确的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=600)

    def format_context(self, context):
        """格式化上下文"""
        if not context:
            return "无"
        return str(context)

    def format_reasoning_history(self, steps):
        """格式化推理历史"""
        if not steps:
            return "无"
        return "\n".join([
            f"{i+1}. {step[:100]}..."
            for i, step in enumerate(steps)
        ])

class ReActMemory:
    """ReAct记忆组件"""
    def __init__(self):
        self.episodic_memory = []  # 情节记忆
        self.working_memory = {}   # 工作记忆

    def store_episode(self, episode):
        """存储情节"""
        self.episodic_memory.append({
            'timestamp': datetime.now().isoformat(),
            'episode': episode
        })

    def retrieve_relevant_episodes(self, query, k=3):
        """检索相关情节"""
        # 简化的相关情节检索
        return self.episodic_memory[-k:] if self.episodic_memory else []

    def update_working_memory(self, key, value):
        """更新工作记忆"""
        self.working_memory[key] = value

    def get_working_memory(self, key):
        """获取工作记忆"""
        return self.working_memory.get(key)
```

**步骤2：工具实现**
```python
class SearchTool:
    """搜索工具"""
    def __init__(self):
        self.name = "search"
        self.description = "搜索相关信息"
        self.required_params = ['query']

    def execute(self, query):
        """执行搜索"""
        print(f"  执行搜索: {query}")

        # 模拟搜索结果
        mock_results = {
            'python': 'Python是一种高级编程语言...',
            '人工智能': '人工智能是计算机科学的一个分支...',
            '机器学习': '机器学习是人工智能的核心技术...'
        }

        # 简单的关键词匹配
        for key, value in mock_results.items():
            if key in query.lower():
                return f"搜索结果: {value}"

        return f"搜索结果: 关于'{query}'的一般信息（模拟数据）"

class CalculatorTool:
    """计算工具"""
    def __init__(self):
        self.name = "calculate"
        self.description = "执行数学计算"
        self.required_params = ['expression']

    def execute(self, expression):
        """执行计算"""
        print(f"  执行计算: {expression}")

        try:
            # 安全的计算（实际应用中需要更安全的实现）
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"计算结果: {expression} = {result}"
            else:
                return "错误: 包含不允许的字符"
        except Exception as e:
            return f"计算错误: {str(e)}"

class AnalyzerTool:
    """分析工具"""
    def __init__(self):
        self.name = "analyze"
        self.description = "分析数据或文本"
        self.required_params = ['data']

    def execute(self, data):
        """执行分析"""
        print(f"  执行分析: {data[:50]}...")

        # 简化的文本分析
        analysis = {
            'length': len(data),
            'word_count': len(data.split()),
            'char_types': {
                'letters': sum(c.isalpha() for c in data),
                'digits': sum(c.isdigit() for c in data),
                'spaces': data.count(' ')
            }
        }

        return f"分析结果: {analysis}"
```

### 任务2：高级ReAct系统优化

**目标：**
实现高级ReAct系统优化，包括多路径推理、自适应停止条件、错误恢复等。

**步骤：高级ReAct系统**
```python
class AdvancedReActSystem:
    """高级ReAct系统"""
    def __init__(self, llm):
        self.llm = llm
        self.tools = {}
        self.reasoning_strategies = [
            'analytical', 'creative', 'systematic'
        ]
        self.max_iterations = 10
        self.num_parallel_paths = 3

    def solve_question_advanced(self, question, context=None):
        """高级问题解决"""
        print(f"\n开始高级解决: {question}")

        # 1. 多路径推理
        paths = self.parallel_reasoning(question, context)

        # 2. 自适应停止判断
        if self.should_stop_early(paths, question):
            return self.select_best_path(paths)

        # 3. 继续优化路径
        optimized_paths = self.optimize_reasoning_paths(paths, question)

        # 4. 选择最佳路径
        best_path = self.select_optimal_path(optimized_paths)

        return best_path

    def parallel_reasoning(self, question, context):
        """并行多路径推理"""
        paths = []

        for i, strategy in enumerate(self.reasoning_strategies):
            print(f"\n--- 路径 {i+1}: {strategy} 推理 ---")

            path = self.execute_reasoning_path(
                question, context, strategy
            )
            path['strategy'] = strategy
            path['path_id'] = i + 1
            paths.append(path)

        return paths

    def execute_reasoning_path(self, question, context, strategy):
        """执行单条推理路径"""
        state = {
            'question': question,
            'context': context or {},
            'strategy': strategy,
            'iterations': 0,
            'reasoning_steps': [],
            'actions': [],
            'observations': [],
            'path_quality': 0.0
        }

        for iteration in range(self.max_iterations):
            state['iterations'] = iteration + 1

            # 基于策略的推理
            reasoning = self.strategy_based_reasoning(state)

            # 检查完成条件
            if self.enhanced_completion_check(reasoning, state):
                break

            # 执行行动
            action = self.strategy_based_action(reasoning, state)
            if action:
                result = self.execute_action(action)
                observation = self.enhanced_observation_processing(
                    result, action, state
                )

                state['actions'].append(action)
                state['observations'].append(observation)
                state['context'] = observation['updated_context']

            # 更新路径质量
            state['path_quality'] = self.calculate_path_quality(state)

        # 生成路径答案
        path_answer = self.generate_path_answer(state)

        return {
            'state': state,
            'answer': path_answer,
            'quality_score': state['path_quality']
        }

    def strategy_based_reasoning(self, state):
        """基于策略的推理"""
        strategy = state['strategy']

        strategy_prompts = {
            'analytical': f"""
            以分析性思维进行推理：
            问题：{state['question']}
            上下文：{state['context']}

            请系统分析问题的各个组成部分，识别关键要素和逻辑关系。
            """,

            'creative': f"""
            以创造性思维进行推理：
            问题：{state['question']}
            上下文：{state['context']}

            请探索多种可能的解决方案，考虑创新性的方法。
            """,

            'systematic': f"""
            以系统性思维进行推理：
            问题：{state['question']}
            上下文：{state['context']}

            请按照结构化的步骤，逐步分解和解决问题。
            """
        }

        prompt = strategy_prompts.get(strategy, strategy_prompts['analytical'])
        return self.llm.generate(prompt, max_tokens=400)

    def enhanced_completion_check(self, reasoning, state):
        """增强的完成检查"""
        # 多维度完成评估
        completion_indicators = [
            '完成' in reasoning,
            '结束' in reasoning,
            '得出结论' in reasoning,
            len(state['observations']) >= 2
        ]

        # 基于质量的检查
        quality_threshold = 0.7
        if state['path_quality'] > quality_threshold:
            completion_indicators.append(True)

        return any(completion_indicators)

    def calculate_path_quality(self, state):
        """计算路径质量"""
        quality_factors = {
            'observation_count': min(len(state['observations']) / 5, 1.0),
            'action_success_rate': self.calculate_action_success_rate(state),
            'reasoning_coherence': self.assess_reasoning_coherence(state),
            'solution_completeness': self.assess_solution_completeness(state)
        }

        weights = {
            'observation_count': 0.2,
            'action_success_rate': 0.3,
            'reasoning_coherence': 0.3,
            'solution_completeness': 0.2
        }

        quality_score = sum(
            quality_factors[factor] * weights[factor]
            for factor in quality_factors
        )

        return quality_score

    def calculate_action_success_rate(self, state):
        """计算行动成功率"""
        if not state['actions']:
            return 0.5

        successful_actions = sum(
            1 for obs in state['observations']
            if obs.get('key_info', {}).get('type') == 'success'
        )

        return successful_actions / len(state['actions'])

    def assess_reasoning_coherence(self, state):
        """评估推理连贯性"""
        if len(state['reasoning_steps']) < 2:
            return 0.5

        # 简化的连贯性评估
        coherence_score = 0.8  # 模拟分数
        return coherence_score

    def assess_solution_completeness(self, state):
        """评估解决方案完整性"""
        # 基于观察的完整性评估
        completeness_indicators = [
            len(state['observations']) >= 2,
            state['path_quality'] > 0.6,
            '最终' in str(state.get('answer', ''))
        ]

        return sum(completeness_indicators) / len(completeness_indicators)

    def should_stop_early(self, paths, question):
        """判断是否应该提前停止"""
        # 如果某个路径质量显著高于其他路径
        quality_scores = [path['quality_score'] for path in paths]
        max_quality = max(quality_scores)
        avg_quality = sum(quality_scores) / len(quality_scores)

        # 如果最佳路径明显优于平均水平
        if max_quality - avg_quality > 0.3 and max_quality > 0.8:
            return True

        return False

    def optimize_reasoning_paths(self, paths, question):
        """优化推理路径"""
        optimized_paths = []

        for path in paths:
            # 基于路径质量决定是否优化
            if path['quality_score'] < 0.7:
                print(f"  优化路径 {path['path_id']}...")
                optimized_path = self.optimize_single_path(path, question)
                optimized_paths.append(optimized_path)
            else:
                optimized_paths.append(path)

        return optimized_paths

    def optimize_single_path(self, path, question):
        """优化单条路径"""
        original_state = path['state']

        # 生成优化建议
        optimization_prompt = f"""
        基于以下推理路径的不足，提出优化建议：

        原始问题：{question}
        当前路径质量：{original_state['path_quality']}
        推理步骤：{original_state['reasoning_steps'][-1] if original_state['reasoning_steps'] else '无'}

        请提供：
        1. 识别的问题和不足
        2. 改进的推理方向
        3. 建议的行动

        优化建议：
        """
        suggestions = self.llm.generate(optimization_prompt, max_tokens=300)

        # 应用优化
        optimized_state = original_state.copy()
        optimized_state['optimization_applied'] = True
        optimized_state['optimization_suggestions'] = suggestions

        return {
            'state': optimized_state,
            'answer': path['answer'],  # 保持原答案
            'quality_score': min(path['quality_score'] + 0.1, 1.0)
        }

    def select_optimal_path(self, paths):
        """选择最优路径"""
        if not paths:
            return None

        # 选择质量最高的路径
        best_path = max(paths, key=lambda x: x['quality_score'])

        print(f"\n选择最优路径: 路径 {best_path['path_id']} "
              f"(质量分数: {best_path['quality_score']:.3f})")

        return best_path

    def generate_path_answer(self, state):
        """生成路径答案"""
        answer_prompt = f"""
        基于以下ReAct推理路径，生成最终答案：

        问题：{state['question']}
        推理策略：{state['strategy']}

        推理步骤：
        {chr(10).join([
            f"{i+1}. {step[:150]}"
            for i, step in enumerate(state['reasoning_steps'])
        ])}

        观察结果：
        {chr(10).join([
            f"{i+1}. {obs['summary'][:150]}"
            for i, obs in enumerate(state['observations'])
        ])}

        请提供完整、准确的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=600)

    def strategy_based_action(self, reasoning, state):
        """基于策略的行动选择"""
        strategy = state['strategy']

        # 不同策略的行动偏好
        strategy_preferences = {
            'analytical': ['analyze', 'calculate'],
            'creative': ['search', 'explore'],
            'systematic': ['calculate', 'analyze', 'search']
        }

        preferred_tools = strategy_preferences.get(strategy, ['search'])

        # 选择首选工具
        for tool in preferred_tools:
            if tool in self.tools:
                return {
                    'tool': tool,
                    'parameters': self.generate_tool_parameters(tool, reasoning, state)
                }

        return None

    def generate_tool_parameters(self, tool_name, reasoning, state):
        """生成工具参数"""
        param_generation_prompt = f"""
        为工具 {tool_name} 生成合适的参数：

        推理：{reasoning}
        问题：{state['question']}

        请提供参数（JSON格式）：
        """
        response = self.llm.generate(param_generation_prompt, max_tokens=150)

        try:
            import json
            return json.loads(response)
        except:
            # 默认参数
            default_params = {
                'search': {'query': state['question']},
                'calculate': {'expression': '1+1'},
                'analyze': {'data': state['question']}
            }
            return default_params.get(tool_name, {})

    def enhanced_observation_processing(self, action_result, action, state):
        """增强的观察处理"""
        observation_processor = ObservationProcessor(self.llm)
        observation = observation_processor.process_observation(
            action_result, action, state['context']
        )

        # 添加路径特定信息
        observation['path_strategy'] = state['strategy']
        observation['iteration'] = state['iterations']

        return observation

    def register_tool(self, name, tool_instance):
        """注册工具"""
        self.tools[name] = tool_instance

    def execute_action(self, action):
        """执行行动"""
        tool_name = action['tool']
        parameters = action['parameters']

        if tool_name in self.tools:
            tool = self.tools[tool_name]
            try:
                result = tool.execute(**parameters)
                return {
                    'status': 'success',
                    'result': result,
                    'tool': tool_name,
                    'parameters': parameters
                }
            except Exception as e:
                return {
                    'status': 'error',
                    'error': str(e),
                    'tool': tool_name,
                    'parameters': parameters
                }
        else:
            return {
                'status': 'error',
                'error': f'工具 {tool_name} 不存在',
                'tool': tool_name,
                'parameters': parameters
            }
```

### 任务3：ReAct系统评估与优化

**目标：**
构建ReAct系统的全面评估框架，分析系统性能和推理质量。

**步骤：评估与优化系统**
```python
class ReActSystemEvaluator:
    """ReAct系统评估器"""
    def __init__(self, react_system):
        self.react_system = react_system
        self.evaluation_metrics = {
            'reasoning_quality': self.evaluate_reasoning_quality,
            'action_effectiveness': self.evaluate_action_effectiveness,
            'observation_relevance': self.evaluate_observation_relevance,
            'solution_completeness': self.evaluate_solution_completeness,
            'efficiency': self.evaluate_efficiency
        }

    def comprehensive_evaluation(self, test_questions):
        """
        综合评估ReAct系统

        Args:
            test_questions: 测试问题列表

        Returns:
            dict: 评估结果
        """
        print("开始ReAct系统综合评估...")
        print(f"测试问题数量: {len(test_questions)}")

        evaluation_results = []

        for i, question_data in enumerate(test_questions, 1):
            print(f"\n测试问题 {i}/{len(test_questions)}: "
                  f"{question_data['question'][:50]}...")

            try:
                # 执行ReAct系统
                result = self.react_system.solve_question_advanced(
                    question_data['question']
                )

                # 评估各项指标
                metric_scores = {}
                for metric_name, metric_func in self.evaluation_metrics.items():
                    try:
                        score = metric_func(result, question_data)
                        metric_scores[metric_name] = score
                        print(f"  {metric_name}: {score:.4f}")
                    except Exception as e:
                        print(f"  {metric_name}: 评估失败 - {e}")
                        metric_scores[metric_name] = 0.0

                evaluation_results.append({
                    'question_data': question_data,
                    'result': result,
                    'metric_scores': metric_scores,
                    'success': True
                })

                print(f"  ✓ 成功完成")

            except Exception as e:
                print(f"  ✗ 执行失败: {e}")
                evaluation_results.append({
                    'question_data': question_data,
                    'error': str(e),
                    'success': False
                })

        # 生成综合报告
        report = self.generate_comprehensive_report(evaluation_results)

        return report

    def evaluate_reasoning_quality(self, result, ground_truth):
        """评估推理质量"""
        reasoning_steps = result.get('reasoning_steps', [])
        if not reasoning_steps:
            return 0.0

        # 评估推理的逻辑性
        logical_coherence = self.assess_logical_coherence(reasoning_steps)

        # 评估推理的完整性
        completeness = self.assess_reasoning_completeness(
            reasoning_steps, result.get('question', '')
        )

        # 评估推理的深度
        depth_score = min(len(reasoning_steps) / 5, 1.0)

        # 综合评分
        quality_score = (
            0.4 * logical_coherence +
            0.3 * completeness +
            0.3 * depth_score
        )

        return quality_score

    def assess_logical_coherence(self, reasoning_steps):
        """评估逻辑连贯性"""
        if len(reasoning_steps) < 2:
            return 0.5

        # 简化的连贯性评估
        coherence_prompt = f"""
        评估以下推理步骤的逻辑连贯性：

        推理步骤：
        {chr(10).join([f"{i+1}. {step[:200]}" for i, step in enumerate(reasoning_steps)])}

        请评分（0-1）：
        """
        # 这里需要LLM评估
        return 0.8  # 模拟评分

    def assess_reasoning_completeness(self, reasoning_steps, question):
        """评估推理完整性"""
        # 检查是否覆盖了问题的关键方面
        completeness_prompt = f"""
        评估推理是否完整回答了问题：

        问题：{question}

        推理步骤：
        {chr(10).join([f"{i+1}. {step[:150]}" for i, step in enumerate(reasoning_steps)])}

        请评分（0-1）：
        """
        # 这里需要LLM评估
        return 0.75  # 模拟评分

    def evaluate_action_effectiveness(self, result, ground_truth):
        """评估行动有效性"""
        actions = result.get('actions', [])
        observations = result.get('observations', [])

        if not actions:
            return 0.0

        # 计算行动成功率
        successful_actions = sum(
            1 for obs in observations
            if obs.get('key_info', {}).get('type') == 'success'
        )
        success_rate = successful_actions / len(actions)

        # 计算行动相关性
        relevance_score = self.assess_action_relevance(actions, result)

        # 综合评分
        effectiveness_score = (
            0.6 * success_rate +
            0.4 * relevance_score
        )

        return effectiveness_score

    def assess_action_relevance(self, actions, result):
        """评估行动相关性"""
        # 简化的相关性评估
        question = result.get('question', '')
        relevant_actions = 0

        for action in actions:
            tool_name = action.get('tool', '')
            if any(keyword in question.lower() for keyword in ['计算', '数学']):
                if tool_name == 'calculate':
                    relevant_actions += 1
            elif any(keyword in question.lower() for keyword in ['搜索', '查找']):
                if tool_name == 'search':
                    relevant_actions += 1

        return relevant_actions / len(actions) if actions else 0

    def evaluate_observation_relevance(self, result, ground_truth):
        """评估观察相关性"""
        observations = result.get('observations', [])
        if not observations:
            return 0.0

        # 计算平均相关性分数
        relevance_scores = [
            obs.get('relevance_score', 0.5)
            for obs in observations
        ]

        return sum(relevance_scores) / len(relevance_scores)

    def evaluate_solution_completeness(self, result, ground_truth):
        """评估解决方案完整性"""
        answer = result.get('final_answer', '')
        question = result.get('question', '')

        if not answer:
            return 0.0

        # 使用LLM评估答案完整性
        completeness_prompt = f"""
        评估以下答案是否完整回答了问题：

        问题：{question}
        答案：{answer}

        请评分（0-1）：
        """
        # 这里需要LLM评估
        return 0.8  # 模拟评分

    def evaluate_efficiency(self, result, ground_truth):
        """评估效率"""
        iterations = result.get('iterations', 0)
        observations = result.get('observations', [])

        # 基于迭代次数和观察数量的效率评分
        if iterations == 0:
            return 0.0

        # 理想情况下，观察数量应与迭代次数成正比
        efficiency = len(observations) / iterations if iterations > 0 else 0

        # 归一化到0-1范围
        return min(efficiency, 1.0)

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
                'total_questions': len(evaluation_results),
                'successful_questions': len(successful_results),
                'failed_questions': len(failed_results),
                'success_rate': len(successful_results) / len(evaluation_results),
                'overall_metrics': overall_metrics
            },
            'detailed_results': evaluation_results,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

        # 打印总结
        print("\n" + "=" * 60)
        print("ReAct系统评估总结")
        print("=" * 60)
        print(f"测试问题总数: {len(evaluation_results)}")
        print(f"成功问题: {len(successful_results)}")
        print(f"失败问题: {len(failed_results)}")
        print(f"成功率: {report['summary']['success_rate']:.1%}")

        print("\n各项指标评分:")
        for metric, score in overall_metrics.items():
            print(f"  {metric}: {score:.4f}")

        return report

    def generate_improvement_recommendations(self, metrics):
        """生成改进建议"""
        recommendations = []

        if metrics.get('reasoning_quality', 0) < 0.7:
            recommendations.append(
                "提高推理质量：优化推理提示，增加推理步骤的逻辑连贯性"
            )

        if metrics.get('action_effectiveness', 0) < 0.6:
            recommendations.append(
                "改进行动有效性：优化工具选择算法，提高行动成功率"
            )

        if metrics.get('observation_relevance', 0) < 0.7:
            recommendations.append(
                "增强观察相关性：改进观察处理算法，提高信息提取质量"
            )

        if metrics.get('solution_completeness', 0) < 0.7:
            recommendations.append(
                "提高答案完整性：优化答案生成策略，确保覆盖所有问题要点"
            )

        if metrics.get('efficiency', 0) < 0.6:
            recommendations.append(
                "优化执行效率：减少不必要的迭代，提高ReAct循环效率"
            )

        if not recommendations:
            recommendations.append("系统性能良好，可考虑在更复杂的任务上进一步测试")

        return recommendations
```

## 深度思考

### ReAct的认知科学基础

**双重过程理论模拟**

ReAct模拟了人类的双重过程认知模式：
- **系统1（快思考）**：快速的直觉性推理
- **系统2（慢思考）**：缓慢的逻辑性分析

```python
class DualProcessReAct:
    """双重过程ReAct模拟器"""
    def __init__(self, llm):
        self.llm = llm
        self.system1 = IntuitiveReasoner()  # 系统1：直觉推理
        self.system2 = AnalyticalReasoner()  # 系统2：分析推理

    def dual_process_reasoning(self, question, context=None):
        """双重过程推理"""
        # 1. 系统1快速直觉反应
        intuitive_response = self.system1.quick_response(
            question, context
        )

        # 2. 系统2深度分析
        analytical_response = self.system2.deep_analysis(
            question, context, intuitive_response
        )

        # 3. 整合两个系统的结果
        integrated_answer = self.integrate_responses(
            intuitive_response, analytical_response, question
        )

        return {
            'intuitive_response': intuitive_response,
            'analytical_response': analytical_response,
            'integrated_answer': integrated_answer
        }

    def integrate_responses(self, intuitive, analytical, question):
        """整合双重过程结果"""
        integration_prompt = f"""
        整合以下两种推理结果：

        问题：{question}

        直觉反应（系统1）：
        {intuitive}

        分析结果（系统2）：
        {analytical}

        请提供综合的最终答案：
        """
        return self.llm.generate(integration_prompt, max_tokens=600)

class IntuitiveReasoner:
    """直觉推理器（系统1）"""
    def quick_response(self, question, context):
        """快速直觉反应"""
        # 基于模式和经验的快速反应
        fast_prompt = f"""
        基于直觉和模式识别，快速回答问题：

        问题：{question}
        上下文：{context}

        请快速给出第一反应：
        """
        return self.llm.generate(fast_prompt, max_tokens=200)

class AnalyticalReasoner:
    """分析推理器（系统2）"""
    def deep_analysis(self, question, context, intuitive_response):
        """深度分析"""
        # 系统性的逻辑分析
        analytical_prompt = f"""
        进行深度逻辑分析：

        问题：{question}
        上下文：{context}
        直觉反应：{intuitive_response}

        请进行详细分析：
        1. 问题分解
        2. 逻辑推理
        3. 证据评估
        4. 结论验证

        分析：
        """
        return self.llm.generate(analytical_prompt, max_tokens=500)
```

**工作记忆与长期记忆**

ReAct中的记忆系统：
```python
class ReActMemorySystem:
    """ReAct记忆系统"""
    def __init__(self):
        self.working_memory = WorkingMemory()
        self.long_term_memory = LongTermMemory()
        self.episodic_memory = EpisodicMemory()

    def manage_memory(self, current_state):
        """管理记忆系统"""
        # 工作记忆更新
        self.working_memory.update_current_context(current_state)

        # 长期记忆检索
        relevant_long_term = self.long_term_memory.retrieve_relevant(
            current_state['question']
        )

        # 情节记忆激活
        relevant_episodes = self.episodic_memory.retrieve_similar(
            current_state, k=3
        )

        # 记忆整合
        integrated_memory = self.integrate_memory_sources(
            current_state, relevant_long_term, relevant_episodes
        )

        return integrated_memory

    def integrate_memory_sources(self, working, long_term, episodic):
        """整合多种记忆源"""
        integration_prompt = f"""
        整合以下记忆源：

        当前状态：{working}
        长期记忆：{long_term}
        情节记忆：{episodic}

        请生成综合的上下文：
        """
        # 这里需要LLM生成
        return f"整合记忆: {working} + {long_term} + {episodic}"

class WorkingMemory:
    """工作记忆"""
    def __init__(self):
        self.current_context = {}
        self.capacity = 7  # 米勒定律：7±2

    def update_current_context(self, state):
        """更新当前上下文"""
        self.current_context = state

class LongTermMemory:
    """长期记忆"""
    def __init__(self):
        self.knowledge_base = {}

    def retrieve_relevant(self, query):
        """检索相关知识"""
        # 简化的知识检索
        return f"长期记忆: {query}的相关知识"

class EpisodicMemory:
    """情节记忆"""
    def __init__(self):
        self.episodes = []

    def retrieve_similar(self, current_state, k=3):
        """检索相似情节"""
        return f"相似情节: {current_state}"
```

### ReAct的技术挑战与解决方案

**1. 推理复杂度控制**

挑战：如何控制推理的复杂度和深度

解决方案：
```python
class AdaptiveComplexityController:
    """自适应复杂度控制器"""
    def __init__(self, llm):
        self.llm = llm
        self.complexity_thresholds = {
            'simple': 3,      # 简单问题最多3步
            'medium': 5,      # 中等问题最多5步
            'complex': 8      # 复杂问题最多8步
        }

    def adapt_complexity(self, question, current_step):
        """自适应复杂度控制"""
        # 1. 评估问题复杂度
        complexity = self.assess_question_complexity(question)

        # 2. 获取阈值
        threshold = self.complexity_thresholds.get(complexity, 5)

        # 3. 检查是否需要简化
        if current_step >= threshold:
            return self.simplify_reasoning(question)

        return self.continue_reasoning(question, current_step)

    def assess_question_complexity(self, question):
        """评估问题复杂度"""
        complexity_prompt = f"""
        评估以下问题的复杂度：

        问题：{question}

        复杂度级别（简单/中等/复杂）：
        """
        response = self.llm.generate(complexity_prompt, max_tokens=50)

        if '简单' in response:
            return 'simple'
        elif '复杂' in response:
            return 'complex'
        else:
            return 'medium'

    def simplify_reasoning(self, question):
        """简化推理"""
        simplification_prompt = f"""
        简化以下问题的推理：

        问题：{question}

        请提供简化的推理步骤：
        """
        return self.llm.generate(simplification_prompt, max_tokens=300)

    def continue_reasoning(self, question, step):
        """继续推理"""
        continue_prompt = f"""
        继续推理步骤 {step}：

        问题：{question}

        请继续推理：
        """
        return self.llm.generate(continue_prompt, max_tokens=400)
```

**2. 错误恢复机制**

挑战：如何从推理和行动错误中恢复

解决方案：
```python
class ErrorRecoveryManager:
    """错误恢复管理器"""
    def __init__(self, llm):
        self.llm = llm
        self.recovery_strategies = [
            'retry_with_modification',
            'alternative_path',
            'simplified_approach',
            'backtrack'
        ]

    def recover_from_error(self, error_info, current_state):
        """从错误中恢复"""
        # 1. 分析错误类型
        error_type = self.classify_error(error_info)

        # 2. 选择恢复策略
        recovery_strategy = self.select_recovery_strategy(
            error_type, current_state
        )

        # 3. 执行恢复
        recovery_result = self.execute_recovery(
            recovery_strategy, error_info, current_state
        )

        return recovery_result

    def classify_error(self, error_info):
        """分类错误类型"""
        error_types = {
            'tool_error': '工具执行错误',
            'reasoning_error': '推理逻辑错误',
            'context_error': '上下文理解错误',
            'observation_error': '观察处理错误'
        }

        error_message = str(error_info)

        for error_type, description in error_types.items():
            if error_type in error_message.lower():
                return error_type

        return 'unknown_error'

    def select_recovery_strategy(self, error_type, current_state):
        """选择恢复策略"""
        strategy_mapping = {
            'tool_error': 'alternative_path',
            'reasoning_error': 'retry_with_modification',
            'context_error': 'backtrack',
            'observation_error': 'simplified_approach'
        }

        default_strategy = 'retry_with_modification'
        return strategy_mapping.get(error_type, default_strategy)

    def execute_recovery(self, strategy, error_info, current_state):
        """执行恢复"""
        if strategy == 'retry_with_modification':
            return self.retry_with_modification(error_info, current_state)
        elif strategy == 'alternative_path':
            return self.alternative_path(error_info, current_state)
        elif strategy == 'simplified_approach':
            return self.simplified_approach(error_info, current_state)
        elif strategy == 'backtrack':
            return self.backtrack(error_info, current_state)

    def retry_with_modification(self, error_info, state):
        """带修改的重试"""
        modification_prompt = f"""
        基于以下错误，调整推理方法：

        错误：{error_info}
        当前状态：{state}

        请提出修改后的方法：
        """
        modification = self.llm.generate(modification_prompt, max_tokens=300)
        return {
            'strategy': 'retry_with_modification',
            'modification': modification,
            'next_action': 'retry'
        }

    def alternative_path(self, error_info, state):
        """替代路径"""
        alternative_prompt = f"""
        由于当前方法出错，请提出替代方案：

        错误：{error_info}
        问题：{state.get('question', '')}

        请提供替代的解决路径：
        """
        alternative = self.llm.generate(alternative_prompt, max_tokens=400)
        return {
            'strategy': 'alternative_path',
            'alternative': alternative,
            'next_action': 'switch_path'
        }

    def simplified_approach(self, error_info, state):
        """简化方法"""
        simplified_prompt = f"""
        将问题简化为更容易处理的形式：

        问题：{state.get('question', '')}
        错误：{error_info}

        请提供简化后的方法：
        """
        simplified = self.llm.generate(simplified_prompt, max_tokens=300)
        return {
            'strategy': 'simplified_approach',
            'simplified': simplified,
            'next_action': 'simplify'
        }

    def backtrack(self, error_info, state):
        """回溯"""
        backtrack_prompt = f"""
        回退到之前的有效状态：

        错误：{error_info}
        当前推理步骤：{state.get('reasoning_steps', [])}

        请确定回溯点：
        """
        backtrack = self.llm.generate(backtrack_prompt, max_tokens=200)
        return {
            'strategy': 'backtrack',
            'backtrack_point': backtrack,
            'next_action': 'backtrack'
        }
```

### ReAct的创新应用场景

**1. 研究探索助手**
```python
class ResearchExplorationAssistant:
    """研究探索助手"""
    def __init__(self, react_system, knowledge_base):
        self.react_system = react_system
        self.knowledge_base = knowledge_base

    def explore_research_topic(self, topic):
        """探索研究主题"""
        exploration_prompt = f"""
        探索研究主题：{topic}

        请使用ReAct方法：
        1. 推理：分析当前研究现状
        2. 行动：搜索相关文献和数据
        3. 观察：整理发现的关键信息
        4. 重复直到得出结论

        开始探索：
        """
        result = self.react_system.solve_question_advanced(
            exploration_prompt
        )

        # 生成探索报告
        report = self.generate_exploration_report(result, topic)

        return report

    def generate_exploration_report(self, result, topic):
        """生成探索报告"""
        report_prompt = f"""
        基于ReAct探索结果，生成研究主题报告：

        主题：{topic}

        探索过程：
        推理步骤数：{len(result['reasoning_steps'])}
        行动数：{len(result['actions'])}
        观察数：{len(result['observations'])}

        最终答案：{result['answer']}

        请生成结构化报告：
        """
        return self.react_system.llm.generate(report_prompt, max_tokens=800)
```

**2. 故障诊断专家**
```python
class TroubleshootingExpert:
    """故障诊断专家"""
    def __init__(self, react_system):
        self.react_system = react_system
        self.diagnostic_database = DiagnosticDatabase()

    def diagnose_problem(self, problem_description):
        """诊断问题"""
        diagnosis_prompt = f"""
        诊断以下问题：

        问题描述：{problem_description}

        请使用ReAct方法：
        1. 推理：分析症状可能的原因
        2. 行动：查询诊断数据库
        3. 观察：记录匹配的故障模式
        4. 重复直到确定根因

        开始诊断：
        """
        result = self.react_system.solve_question_advanced(
            diagnosis_prompt
        )

        # 生成诊断报告
        diagnosis_report = self.generate_diagnosis_report(result)

        return diagnosis_report

    def generate_diagnosis_report(self, result):
        """生成诊断报告"""
        report = {
            'problem_analysis': result['reasoning_steps'],
            'diagnosis_steps': result['observations'],
            'root_cause': result['answer'],
            'confidence': self.calculate_confidence(result)
        }
        return report

    def calculate_confidence(self, result):
        """计算诊断置信度"""
        factors = [
            len(result['observations']) * 0.2,
            len(result['actions']) * 0.3,
            result.get('quality_score', 0.5) * 0.5
        ]
        return min(sum(factors), 1.0)

class DiagnosticDatabase:
    """诊断数据库"""
    def __init__(self):
        self.diagnostics = {
            '常见故障模式': [
                {'症状': '过热', '原因': '散热不良', '解决方案': '清洁散热器'},
                {'症状': '死机', '原因': '内存不足', '解决方案': '增加内存'},
                {'症状': '慢速', '原因': '磁盘满', '解决方案': '清理磁盘'}
            ]
        }

    def search(self, symptom):
        """搜索诊断信息"""
        matches = []
        for pattern in self.diagnostics['常见故障模式']:
            if symptom in pattern['症状']:
                matches.append(pattern)
        return matches
```

## 质量评估

### ReAct系统的质量评估框架

**1. 推理质量评估（Reasoning Quality）**

评估ReAct系统的推理能力：

```python
def evaluate_reasoning_quality(react_results, test_cases):
    """
    评估推理质量
    """
    quality_metrics = {
        'logical_coherence': evaluate_logical_coherence,
        'reasoning_depth': evaluate_reasoning_depth,
        'inference_accuracy': evaluate_inference_accuracy,
        'step_justification': evaluate_step_justification
    }

    evaluation_results = {}

    for metric_name, calculator in quality_metrics.items():
        scores = []
        for result in react_results:
            score = calculator(result, test_cases)
            scores.append(score)

        avg_score = sum(scores) / len(scores)
        evaluation_results[metric_name] = avg_score

    return evaluation_results

def evaluate_logical_coherence(result, test_cases):
    """评估逻辑连贯性"""
    reasoning_steps = result.get('reasoning_steps', [])
    if len(reasoning_steps) < 2:
        return 0.5

    # 检查推理步骤之间的逻辑关系
    coherence_score = 0.0
    for i in range(len(reasoning_steps) - 1):
        current_step = reasoning_steps[i]
        next_step = reasoning_steps[i + 1]

        # 简化的连贯性评估
        if has_logical_connection(current_step, next_step):
            coherence_score += 1.0

    return coherence_score / (len(reasoning_steps) - 1)

def has_logical_connection(step1, step2):
    """检查两个推理步骤之间是否有逻辑连接"""
    # 简化的连接检测
    connection_indicators = ['因此', '所以', '基于', '根据', '由于']
    return any(indicator in step2 for indicator in connection_indicators)

def evaluate_reasoning_depth(result, test_cases):
    """评估推理深度"""
    iterations = result.get('iterations', 0)
    observations = len(result.get('observations', []))

    # 深度评估：迭代次数和观察数量的综合
    depth_score = min((iterations + observations) / 10, 1.0)
    return depth_score

def evaluate_inference_accuracy(result, test_cases):
    """评估推理准确性"""
    final_answer = result.get('final_answer', '')
    expected_answer = test_cases.get('expected_answer', '')

    if not expected_answer:
        return 0.5

    # 使用语义相似度评估准确性
    similarity = calculate_semantic_similarity(final_answer, expected_answer)
    return similarity

def evaluate_step_justification(result, test_cases):
    """评估步骤合理性"""
    actions = result.get('actions', [])
    if not actions:
        return 0.5

    # 评估每个行动是否有充分的推理支撑
    justified_actions = 0
    reasoning_steps = result.get('reasoning_steps', [])

    for action in actions:
        if has_justification(action, reasoning_steps):
            justified_actions += 1

    return justified_actions / len(actions)

def has_justification(action, reasoning_steps):
    """检查行动是否有推理支撑"""
    action_keywords = action.get('tool', '').lower()
    # 简化的合理性检查
    return any(action_keywords in step.lower() for step in reasoning_steps)
```

**2. 行动效果评估（Action Effectiveness）**

评估ReAct系统的行动能力：

```python
def evaluate_action_effectiveness(react_results, test_cases):
    """
    评估行动有效性
    """
    effectiveness_metrics = {
        'action_relevance': evaluate_action_relevance,
        'tool_appropriateness': evaluate_tool_appropriateness,
        'execution_success_rate': evaluate_execution_success_rate,
        'information_gain': evaluate_information_gain
    }

    evaluation_results = {}

    for metric_name, calculator in effectiveness_metrics.items():
        scores = []
        for result in react_results:
            score = calculator(result, test_cases)
            scores.append(score)

        avg_score = sum(scores) / len(scores)
        evaluation_results[metric_name] = avg_score

    return evaluation_results

def evaluate_action_relevance(result, test_cases):
    """评估行动相关性"""
    actions = result.get('actions', [])
    if not actions:
        return 0.0

    question = result.get('question', '').lower()
    relevant_actions = 0

    for action in actions:
        action_description = f"{action.get('tool', '')} {str(action.get('parameters', ''))}"
        action_lower = action_description.lower()

        # 检查行动是否与问题相关
        question_keywords = extract_keywords(question)
        action_keywords = extract_keywords(action_lower)

        overlap = set(question_keywords) & set(action_keywords)
        if overlap:
            relevant_actions += 1

    return relevant_actions / len(actions)

def extract_keywords(text):
    """提取关键词"""
    # 简化的关键词提取
    stopwords = {'的', '了', '在', '是', '我', '你', '他', '这', '那', '和', '与'}
    words = text.split()
    return [word for word in words if word not in stopwords and len(word) > 1]

def evaluate_tool_appropriateness(result, test_cases):
    """评估工具适当性"""
    actions = result.get('actions', [])
    if not actions:
        return 0.5

    appropriate_actions = 0
    for action in actions:
        tool = action.get('tool', '')
        parameters = action.get('parameters', {})

        # 检查工具-参数匹配
        if is_tool_parameter_match(tool, parameters):
            appropriate_actions += 1

    return appropriate_actions / len(actions)

def is_tool_parameter_match(tool, parameters):
    """检查工具参数匹配"""
    # 简化的参数匹配检查
    tool_requirements = {
        'search': ['query'],
        'calculate': ['expression'],
        'analyze': ['data']
    }

    required_params = tool_requirements.get(tool, [])
    return all(param in parameters for param in required_params)

def evaluate_execution_success_rate(result, test_cases):
    """评估执行成功率"""
    observations = result.get('observations', [])
    if not observations:
        return 0.0

    successful_observations = sum(
        1 for obs in observations
        if obs.get('key_info', {}).get('type') == 'success'
    )

    return successful_observations / len(observations)

def evaluate_information_gain(result, test_cases):
    """评估信息增益"""
    observations = result.get('observations', [])
    if not observations:
        return 0.0

    total_information = 0
    for obs in observations:
        info = obs.get('key_info', {})
        if 'content' in info:
            # 基于内容长度和相关性计算信息量
            content_length = len(str(info['content']))
            relevance = obs.get('relevance_score', 0.5)
            total_information += content_length * relevance

    # 归一化信息增益
    max_possible_info = 1000  # 假设的最大信息量
    return min(total_information / max_possible_info, 1.0)
```

### 实际评估案例

**案例1：复杂问题ReAct评估**

```python
def evaluate_complex_problem_react(react_system, complex_problems):
    """
    评估ReAct系统在复杂问题上的表现
    """
    evaluation_results = []

    for problem in complex_problems:
        print(f"\n评估复杂问题: {problem['description']}")

        # 执行ReAct
        result = react_system.solve_question_advanced(problem['description'])

        # 评估维度
        complexity_score = evaluate_complexity_handling(result, problem)
        adaptability_score = evaluate_adaptability(result, problem)
        robustness_score = evaluate_robustness(result, problem)
        efficiency_score = evaluate_efficiency(result, problem)

        evaluation_results.append({
            'problem': problem,
            'result': result,
            'complexity_score': complexity_score,
            'adaptability_score': adaptability_score,
            'robustness_score': robustness_score,
            'efficiency_score': efficiency_score
        })

    # 计算总体表现
    overall_performance = {
        'average_complexity_handling': sum(r['complexity_score'] for r in evaluation_results) / len(evaluation_results),
        'average_adaptability': sum(r['adaptability_score'] for r in evaluation_results) / len(evaluation_results),
        'average_robustness': sum(r['robustness_score'] for r in evaluation_results) / len(evaluation_results),
        'average_efficiency': sum(r['efficiency_score'] for r in evaluation_results) / len(evaluation_results)
    }

    return {
        'detailed_results': evaluation_results,
        'overall_performance': overall_performance
    }

def evaluate_complexity_handling(result, problem):
    """评估复杂度处理能力"""
    iterations = result.get('iterations', 0)
    reasoning_steps = len(result.get('reasoning_steps', []))
    actions = len(result.get('actions', []))

    # 复杂度处理得分
    complexity_factors = {
        'depth': min(reasoning_steps / 5, 1.0),
        'breadth': min(actions / 3, 1.0),
        'persistence': min(iterations / 8, 1.0)
    }

    return sum(complexity_factors.values()) / len(complexity_factors)

def evaluate_adaptability(result, problem):
    """评估适应性"""
    observations = result.get('observations', [])
    if len(observations) < 2:
        return 0.5

    # 适应性：观察结果的多样性和相关性
    diversity_score = calculate_observation_diversity(observations)
    relevance_score = sum(
        obs.get('relevance_score', 0.5) for obs in observations
    ) / len(observations)

    return (diversity_score + relevance_score) / 2

def calculate_observation_diversity(observations):
    """计算观察多样性"""
    if len(observations) < 2:
        return 0.5

    # 简化的多样性计算
    unique_types = set(
        obs.get('key_info', {}).get('type', 'unknown')
        for obs in observations
    )

    return min(len(unique_types) / len(observations), 1.0)

def evaluate_robustness(result, problem):
    """评估鲁棒性"""
    observations = result.get('observations', [])
    if not observations:
        return 0.0

    # 鲁棒性：错误恢复能力
    error_recovery = sum(
        1 for obs in observations
        if obs.get('key_info', {}).get('type') == 'success' and
           obs.get('iteration', 1) > 1
    )

    return error_recovery / len(observations)

def evaluate_efficiency(result, problem):
    """评估效率"""
    iterations = result.get('iterations', 0)
    successful_actions = sum(
        1 for obs in result.get('observations', [])
        if obs.get('key_info', {}).get('type') == 'success'
    )

    if iterations == 0:
        return 0.0

    # 效率：成功行动数 / 总迭代数
    return successful_actions / iterations
```

## 完整学习框架

### 学习路径规划

**阶段1：基础理解（1周）**
- 理解ReAct的基本概念和推理-行动循环
- 学习"思考-行动-观察"模式
- 实现简单的ReAct系统

**阶段2：系统实现（1-2周）**
- 构建完整的ReAct执行流水线
- 实现工具管理和观察处理
- 开发多路径推理能力

**阶段3：优化提升（1周）**
- 实现高级优化算法
- 构建性能评估框架
- 增强错误恢复能力

**阶段4：应用实践（1周）**
- 在特定领域部署ReAct系统
- 测试和调优系统性能
- 总结最佳实践

### 项目实践体系

**项目1：智能研究助手**
```python
class IntelligentResearchAssistant:
    """智能研究助手"""
    def __init__(self, react_system):
        self.react_system = react_system
        self.research_tools = {
            'literature_search': LiteratureSearchTool(),
            'data_analysis': DataAnalysisTool(),
            'paper_summarizer': PaperSummarizerTool()
        }

        # 注册工具
        for name, tool in self.research_tools.items():
            self.react_system.register_tool(name, tool)

    def assist_research(self, research_question):
        """协助研究"""
        research_prompt = f"""
        研究问题：{research_question}

        使用ReAct方法进行研究：
        1. 推理：分析研究现状和缺口
        2. 行动：搜索相关文献和数据
        3. 观察：整理发现和洞见
        4. 重复直到得出研究结论

        开始研究：
        """
        return self.react_system.solve_question_advanced(research_prompt)
```

**项目2：自适应问答系统**
```python
class AdaptiveQASystem:
    """自适应问答系统"""
    def __init__(self, react_system):
        self.react_system = react_system
        self.knowledge_sources = {
            'web_search': WebSearchTool(),
            'database_query': DatabaseQueryTool(),
            'calculation': CalculationTool()
        }

        # 注册工具
        for name, tool in self.knowledge_sources.items():
            self.react_system.register_tool(name, tool)

    def answer_question(self, question, domain=None):
        """回答问题"""
        if domain:
            question = f"[{domain}领域] {question}"

        return self.react_system.solve_question_advanced(question)
```

### 评估认证体系

**技能认证标准**

```python
class ReActCertificationFramework:
    """ReAct技能认证框架"""
    def __init__(self):
        self.certification_levels = {
            'beginner': {
                'knowledge': ['basic_concepts', 'reasoning_acting_cycle', 'simple_tools'],
                'skills': ['basic_react_implementation', 'tool_usage', 'observation_processing'],
                'projects': ['simple_qa_system', 'basic_problem_solver']
            },
            'intermediate': {
                'knowledge': ['advanced_reasoning', 'multi_path_execution', 'error_recovery'],
                'skills': ['complex_react_systems', 'optimization_techniques', 'performance_tuning'],
                'projects': ['research_assistant', 'diagnostic_expert']
            },
            'advanced': {
                'knowledge': ['cognitive_modeling', 'adaptive_systems', 'scalable_architectures'],
                'skills': ['innovative_applications', 'large_scale_systems', 'research_contributions'],
                'projects': ['autonomous_researcher', 'enterprise_intelligence_platform']
            }
        }
```

### 未来发展方向

**技术演进方向**

1. **认知架构增强**
   - 更接近人类认知的推理模式
   - 元认知能力提升
   - 创造性问题解决

2. **多模态ReAct**
   - 支持视觉、听觉输入
   - 跨模态推理和行动
   - 多媒体信息处理

3. **分布式ReAct**
   - 多智能体协同推理
   - 分布式工具共享
   - 集体智能涌现

4. **个性化ReAct**
   - 用户思维模式适应
   - 个性化推理风格
   - 自适应交互界面

**应用拓展方向**

1. **科学研究**
   - 自动假设生成
   - 实验设计优化
   - 科学发现辅助

2. **教育培训**
   - 个性化学习助手
   - 苏格拉底式对话
   - 认知技能培养

3. **商业智能**
   - 决策支持系统
   - 策略规划助手
   - 风险管理工具

### 总结与反思

**ReAct的核心价值**

ReAct代表了AI系统发展的重要方向：
- **透明化推理**：显式展示推理过程，增强可解释性
- **工具集成**：无缝集成外部工具，扩展系统能力
- **动态适应**：基于反馈动态调整，提升灵活性
- **可验证性**：每个推理步骤都有可观察的行动支撑

**关键技术要素**

1. **推理生成**：高质量的逻辑推理链
2. **行动选择**：智能的工具选择和参数配置
3. **观察处理**：有效的状态更新和知识整合
4. **循环控制**：自适应的停止条件和路径选择

**学习建议**

1. **理论与实践结合**：深入理解认知科学基础，多动手实现
2. **关注认知模拟**：研究人类推理和决策过程
3. **重视工具生态**：构建丰富的工具库和接口
4. **持续评估优化**：建立完善的性能评估体系

**挑战与机遇**

ReAct面临的挑战：
- **推理复杂度**：如何控制推理的深度和范围
- **工具依赖**：如何处理工具失效和错误
- **效率优化**：如何在保证质量的前提下提高效率

同时带来的机遇：
- **认知增强**：提升人类的问题解决能力
- **自动化升级**：实现更智能的自动化系统
- **创新应用**：催生新的AI应用模式

通过系统学习ReAct技术，您将掌握一种强大的AI增强技术，为构建更智能、更透明、更可靠的AI系统提供重要支撑。

---

## 本章小结

ReAct（Reasoning and Acting）是一种将推理和行动结合起来的技术框架，通过"思考-行动-观察"的循环机制，解决复杂的多步骤问题。

### 核心要点
- **技术原理**：通过显式的推理-行动-观察循环，实现透明化的推理过程
- **实现方法**：包括同步、并行、分层等多种执行策略
- **应用领域**：研究探索、故障诊断、决策支持等多个需要推理和行动结合的场景
- **创新价值**：提供可验证、可解释的推理过程，实现认知透明化

### 实践价值
掌握ReAct技术能够：
- 构建透明化的AI推理系统
- 提升复杂问题解决的效率和准确性
- 实现可验证的认知过程
- 增强AI系统的可解释性和可信度

### 技能认证
通过本章学习，您应该能够：
1. 理解ReAct的基本原理和认知基础
2. 实现完整的ReAct系统流水线
3. 构建多路径推理和优化机制
4. 在实际应用中部署ReAct系统

ReAct代表了AI系统从黑盒向白盒转变的重要技术，通过显式化的推理和行动，为构建更智能、更可解释的AI系统奠定了技术基础。

---