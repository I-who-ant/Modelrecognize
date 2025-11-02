# Day 19: 图提示（Graph Prompting）

## 理论学习

### 图提示的核心原理

图提示（Graph Prompting）是一种基于图结构的提示工程技术，将问题表示为图的形式，利用图神经网络和图遍历算法来指导大语言模型的推理过程。该技术通过将复杂问题分解为图节点和边的关系，实现结构化的推理和决策。

#### 技术机制与工作原理

**核心流程：**
1. **图构建阶段（Graph Construction）**
   - 识别问题中的实体和关系
   - 构建节点和边的表示
   - 形成完整的图结构

2. **图遍历阶段（Graph Traversal）**
   - 设计图遍历策略（DFS、BFS、最短路径等）
   - 按策略访问节点和边
   - 收集和更新节点信息

3. **图推理阶段（Graph Reasoning）**
   - 基于图结构进行逻辑推理
   - 利用节点间的关系传播信息
   - 得出图级别的结论

4. **答案生成阶段（Answer Generation）**
   - 基于图推理结果生成最终答案
   - 提供推理路径和依据
   - 输出结构化的解答

**技术创新点：**
- **结构化推理**：将抽象问题具象化为图结构
- **关系建模**：显式建模实体间的关系
- **路径追踪**：提供清晰的推理路径
- **可解释性**：增强推理过程的可解释性

#### 理论基础

**图提示架构模型**
```
Graph Prompting = Construct(Analyze) → Traverse(Navigate) → Reason(Infer) → Generate(Answer)

其中：
- Construct: 图构建函数，分析问题并生成图结构
- Traverse: 图遍历函数，按照策略访问节点和边
- Reason: 图推理函数，基于图结构进行推理
- Generate: 答案生成函数，输出最终结果
```

**分层系统架构**
```
第一层：问题分析层（Problem Analysis Layer）
输入：原始问题描述
输出：实体和关系列表

第二层：图构建层（Graph Construction Layer）
输入：实体关系列表
输出：结构化图表示

第三层：图遍历层（Graph Traversal Layer）
输入：图表示和遍历策略
输出：遍历路径和节点序列

第四层：图推理层（Graph Reasoning Layer）
输入：遍历路径和图结构
输出：推理结果和中间状态

第五层：答案生成层（Answer Generation Layer）
输入：推理结果
输出：最终答案和解释
```

**图提示设计框架**
```python
class GraphPromptingFramework:
    """图提示设计框架"""
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = GraphBuilder()
        self.graph_traverser = GraphTraverser()
        self.graph_reasoner = GraphReasoner()
        self.answer_generator = AnswerGenerator()

    def design_graph_prompt(self, question, context=None):
        """
        设计图提示

        Args:
            question: 问题描述
            context: 上下文信息

        Returns:
            dict: 图提示设计结果
        """
        print(f"\n设计图提示: {question}")

        # 1. 问题分析
        print("1. 分析问题...")
        entities, relations = self.analyze_question(question, context)
        print(f"   实体: {entities}")
        print(f"   关系: {relations}")

        # 2. 图构建
        print("2. 构建图结构...")
        graph = self.graph_builder.construct_graph(entities, relations)
        print(f"   图节点: {len(graph.nodes())}")
        print(f"   图边: {len(graph.edges())}")

        # 3. 遍历策略设计
        print("3. 设计遍历策略...")
        traversal_strategy = self.design_traversal_strategy(graph, question)

        # 4. 图遍历执行
        print("4. 执行图遍历...")
        traversal_path = self.graph_traverser.traverse(
            graph, traversal_strategy
        )

        # 5. 图推理
        print("5. 进行图推理...")
        reasoning_result = self.graph_reasoner.reason(
            graph, traversal_path, question
        )

        # 6. 答案生成
        print("6. 生成最终答案...")
        final_answer = self.answer_generator.generate(
            reasoning_result, traversal_path
        )

        return {
            'entities': entities,
            'relations': relations,
            'graph': graph,
            'traversal_strategy': traversal_strategy,
            'traversal_path': traversal_path,
            'reasoning_result': reasoning_result,
            'final_answer': final_answer
        }

    def analyze_question(self, question, context):
        """分析问题，提取实体和关系"""
        analysis_prompt = f"""
        分析以下问题，提取实体和关系：

        问题：{question}
        上下文：{context}

        请提取：
        1. 主要实体（人物、地点、物品、概念等）
        2. 实体间的关系（因果、包含、比较等）

        实体列表：
        关系列表：
        """
        analysis_result = self.llm.generate(analysis_prompt, max_tokens=400)

        # 解析分析结果
        entities = self.extract_entities(analysis_result)
        relations = self.extract_relations(analysis_result)

        return entities, relations

    def extract_entities(self, analysis_result):
        """提取实体"""
        # 简化的实体提取
        # 实际应用中需要更复杂的实体识别
        entities = []
        lines = analysis_result.split('\n')
        for line in lines:
            if '实体' in line or '实体' in line:
                # 提取实体名
                entity = line.split('：')[-1].strip()
                if entity:
                    entities.append(entity)
        return entities

    def extract_relations(self, analysis_result):
        """提取关系"""
        # 简化的关系提取
        relations = []
        lines = analysis_result.split('\n')
        for line in lines:
            if '关系' in line or '关系' in line:
                # 提取关系
                relation = line.split('：')[-1].strip()
                if relation:
                    relations.append(relation)
        return relations

    def design_traversal_strategy(self, graph, question):
        """设计遍历策略"""
        strategy_prompt = f"""
        基于以下图和问题，设计遍历策略：

        图结构：节点{len(graph.nodes())}个，边{len(graph.edges())}个
        问题：{question}

        可选策略：
        1. DFS（深度优先）：适合查找路径和连通性
        2. BFS（广度优先）：适合查找最短路径
        3. 启发式搜索：适合优化问题
        4. 关键路径分析：适合依赖关系

        请选择最适合的遍历策略并说明原因：
        """
        strategy_response = self.llm.generate(strategy_prompt, max_tokens=300)

        # 解析策略
        traversal_strategy = self.parse_traversal_strategy(strategy_response)

        return traversal_strategy

    def parse_traversal_strategy(self, strategy_response):
        """解析遍历策略"""
        # 简化的策略解析
        if 'DFS' in strategy_response or '深度优先' in strategy_response:
            return {'type': 'DFS', 'params': {'max_depth': 5}}
        elif 'BFS' in strategy_response or '广度优先' in strategy_response:
            return {'type': 'BFS', 'params': {'max_depth': 5}}
        elif '启发式' in strategy_response:
            return {'type': 'heuristic', 'params': {'heuristic': 'distance'}}
        else:
            return {'type': 'BFS', 'params': {'max_depth': 5}}  # 默认策略

class GraphBuilder:
    """图构建器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def construct_graph(self, entities, relations):
        """构建图"""
        graph = self.nx.DiGraph()  # 有向图

        # 添加节点
        for entity in entities:
            graph.add_node(entity, type='entity')

        # 添加边（简化处理）
        for relation in relations:
            if '->' in relation or '→' in relation:
                parts = relation.replace('→', '->').split('->')
                if len(parts) == 2:
                    source, target = parts[0].strip(), parts[1].strip()
                    if source in entities and target in entities:
                        graph.add_edge(source, target, relation=relation)

        return graph

class GraphTraverser:
    """图遍历器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def traverse(self, graph, strategy):
        """遍历图"""
        traversal_type = strategy['type']
        params = strategy['params']

        traversal_path = []

        if traversal_type == 'DFS':
            traversal_path = self.depth_first_search(graph, params)
        elif traversal_type == 'BFS':
            traversal_path = self.breadth_first_search(graph, params)
        elif traversal_type == 'heuristic':
            traversal_path = self.heuristic_search(graph, params)
        else:
            traversal_path = self.breadth_first_search(graph, params)

        return traversal_path

    def depth_first_search(self, graph, params):
        """深度优先搜索"""
        if not graph.nodes():
            return []

        start_node = list(graph.nodes())[0]
        max_depth = params.get('max_depth', 5)

        visited = set()
        path = []

        def dfs(node, depth):
            if depth > max_depth or node in visited:
                return

            visited.add(node)
            path.append(node)

            for neighbor in graph.successors(node):
                dfs(neighbor, depth + 1)

        dfs(start_node, 0)
        return path

    def breadth_first_search(self, graph, params):
        """广度优先搜索"""
        if not graph.nodes():
            return []

        start_node = list(graph.nodes())[0]
        max_depth = params.get('max_depth', 5)

        queue = [(start_node, 0)]
        visited = set()
        path = []

        while queue:
            node, depth = queue.pop(0)

            if depth > max_depth or node in visited:
                continue

            visited.add(node)
            path.append(node)

            for neighbor in graph.successors(node):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))

        return path

    def heuristic_search(self, graph, params):
        """启发式搜索"""
        # 简化的启发式搜索
        return self.breadth_first_search(graph, params)

class GraphReasoner:
    """图推理器"""
    def __init__(self, llm):
        self.llm = llm

    def reason(self, graph, traversal_path, question):
        """图推理"""
        if not traversal_path:
            return "无法推理：遍历路径为空"

        # 构建推理上下文
        reasoning_context = self.build_reasoning_context(graph, traversal_path)

        # 执行推理
        reasoning_prompt = f"""
        基于以下图遍历路径进行推理：

        问题：{question}
        遍历路径：{traversal_path}
        图上下文：{reasoning_context}

        请进行逻辑推理：
        """
        reasoning_result = self.llm.generate(reasoning_prompt, max_tokens=500)

        return reasoning_result

    def build_reasoning_context(self, graph, traversal_path):
        """构建推理上下文"""
        context_parts = []

        for node in traversal_path:
            node_info = f"节点: {node}"
            if graph.nodes[node]:
                node_info += f", 属性: {graph.nodes[node]}"
            context_parts.append(node_info)

            # 添加相邻边信息
            for edge in graph.edges(node):
                if edge[1] in traversal_path:
                    edge_data = graph.edges[edge]
                    context_parts.append(f"边: {edge[0]} -> {edge[1]}, 关系: {edge_data}")

        return "\n".join(context_parts)

class AnswerGenerator:
    """答案生成器"""
    def __init__(self, llm):
        self.llm = llm

    def generate(self, reasoning_result, traversal_path):
        """生成最终答案"""
        answer_prompt = f"""
        基于图推理结果，生成最终答案：

        推理结果：{reasoning_result}
        遍历路径：{traversal_path}

        请提供完整、准确的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=600)
```

### 图提示 vs 其他技术对比

**vs Chain-of-Thought (CoT)**
| 维度 | 图提示 | CoT |
|------|--------|-----|
| 结构化程度 | 高（图结构） | 中（线性链） |
| 关系建模 | 强（显式关系） | 弱（隐式关系） |
| 可解释性 | 强（路径可视化） | 中（文本解释） |
| 复杂度处理 | 强（多分支推理） | 弱（单路径推理） |
| 实现难度 | 高（图构建） | 低（文本生成） |

**vs Tree of Thoughts (ToT)**
| 维度 | 图提示 | ToT |
|------|--------|-----|
| 结构复杂性 | 复杂（图） | 中等（树） |
| 关系表示 | 多样（有向边） | 单一（父子关系） |
| 遍历策略 | 灵活（多种算法） | 有限（树遍历） |
| 路径选择 | 智能（基于策略） | 启发式（评分） |
| 适用场景 | 广泛（关系密集） | 专门（层次结构） |

### 图提示的分类体系

**1. 实体关系图提示（Entity-Relationship Graph Prompting）**

基于实体关系图的问题解决：

```python
class EntityRelationshipGraphPrompting:
    """实体关系图提示"""
    def __init__(self, llm):
        self.llm = llm
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()
        self.graph_builder = EntityRelationshipGraphBuilder()

    def solve_with_er_graph(self, question, context=None):
        """使用实体关系图解决问题"""
        # 1. 提取实体
        entities = self.entity_extractor.extract_entities(question, context)
        print(f"提取实体: {entities}")

        # 2. 提取关系
        relations = self.relation_extractor.extract_relations(question, entities)
        print(f"提取关系: {relations}")

        # 3. 构建ER图
        er_graph = self.graph_builder.build_graph(entities, relations)
        print(f"ER图节点: {len(er_graph.nodes())}")

        # 4. 图推理
        reasoning_result = self.perform_graph_reasoning(er_graph, question)

        # 5. 生成答案
        answer = self.generate_answer(reasoning_result)

        return {
            'entities': entities,
            'relations': relations,
            'graph': er_graph,
            'reasoning': reasoning_result,
            'answer': answer
        }

    def perform_graph_reasoning(self, graph, question):
        """执行图推理"""
        reasoning_prompt = f"""
        基于以下实体关系图进行推理：

        问题：{question}
        实体：{list(graph.nodes())}
        关系：{list(graph.edges(data=True))}

        请进行逻辑推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=500)

    def generate_answer(self, reasoning_result):
        """生成答案"""
        answer_prompt = f"""
        基于推理结果生成最终答案：

        推理：{reasoning_result}

        答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=400)

class EntityExtractor:
    """实体提取器"""
    def extract_entities(self, question, context):
        """提取实体"""
        extraction_prompt = f"""
        从以下问题中提取实体（人物、地点、物品、概念等）：

        问题：{question}
        上下文：{context}

        请列出所有识别的实体：
        """
        result = self.llm.generate(extraction_prompt, max_tokens=300)
        return self.parse_entities(result)

    def parse_entities(self, result):
        """解析实体"""
        entities = []
        lines = result.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                entity = line.split('：')[-1].strip() if '：' in line else line.strip()
                if entity and len(entity) > 1:
                    entities.append(entity)
        return entities

class RelationExtractor:
    """关系提取器"""
    def extract_relations(self, question, entities):
        """提取关系"""
        relations = []

        # 简单的关系提取
        relation_patterns = [
            f"{entities[0]}是{entities[1]}的..." if len(entities) >= 2 else "",
            f"{entities[0]}与{entities[1]}相关" if len(entities) >= 2 else "",
            f"{entities[0]}导致{entities[1]}" if len(entities) >= 2 else ""
        ]

        return relation_patterns

class EntityRelationshipGraphBuilder:
    """实体关系图构建器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def build_graph(self, entities, relations):
        """构建图"""
        graph = self.nx.DiGraph()

        # 添加实体节点
        for entity in entities:
            graph.add_node(entity, type='entity')

        # 添加关系边
        for relation in relations:
            if '->' in relation:
                parts = relation.split('->')
                if len(parts) == 2:
                    source, target = parts[0].strip(), parts[1].strip()
                    if source in entities and target in entities:
                        graph.add_edge(source, target, type='relation')

        return graph
```

**2. 因果关系图提示（Causal Graph Prompting）**

基于因果关系图的推理：

```python
class CausalGraphPrompting:
    """因果关系图提示"""
    def __init__(self, llm):
        self.llm = llm
        self.causal_extractor = CausalRelationExtractor()
        self.causal_graph_builder = CausalGraphBuilder()

    def solve_with_causal_graph(self, question, context=None):
        """使用因果关系图解决问题"""
        # 1. 提取因果关系
        causes, effects = self.causal_extractor.extract_causal_relations(
            question, context
        )
        print(f"原因: {causes}")
        print(f"结果: {effects}")

        # 2. 构建因果图
        causal_graph = self.causal_graph_builder.build_causal_graph(causes, effects)
        print(f"因果图节点: {len(causal_graph.nodes())}")

        # 3. 因果推理
        causal_reasoning = self.perform_causal_reasoning(causal_graph, question)

        # 4. 生成答案
        answer = self.generate_causal_answer(causal_reasoning)

        return {
            'causes': causes,
            'effects': effects,
            'causal_graph': causal_graph,
            'reasoning': causal_reasoning,
            'answer': answer
        }

    def perform_causal_reasoning(self, graph, question):
        """执行因果推理"""
        reasoning_prompt = f"""
        基于以下因果关系图进行推理：

        问题：{question}
        因果节点：{list(graph.nodes())}
        因果边：{list(graph.edges(data=True))}

        请分析因果关系并推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=500)

    def generate_causal_answer(self, reasoning):
        """生成因果答案"""
        answer_prompt = f"""
        基于因果推理结果回答问题：

        推理：{reasoning}

        答案（包含因果解释）：
        """
        return self.llm.generate(answer_prompt, max_tokens=400)

class CausalRelationExtractor:
    """因果关系提取器"""
    def extract_causal_relations(self, question, context):
        """提取因果关系"""
        extraction_prompt = f"""
        从以下问题中提取因果关系：

        问题：{question}
        上下文：{context}

        请识别：
        1. 可能的原因
        2. 可能的结果

        原因列表：
        结果列表：
        """
        result = self.llm.generate(extraction_prompt, max_tokens=400)
        return self.parse_causal_relations(result)

    def parse_causal_relations(self, result):
        """解析因果关系"""
        lines = result.split('\n')
        causes = []
        effects = []

        for line in lines:
            if '原因' in line or 'cause' in line.lower():
                cause = line.split('：')[-1].strip() if '：' in line else line.strip()
                if cause:
                    causes.append(cause)
            elif '结果' in line or 'effect' in line.lower():
                effect = line.split('：')[-1].strip() if '：' in line else line.strip()
                if effect:
                    effects.append(effect)

        return causes, effects

class CausalGraphBuilder:
    """因果图构建器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def build_causal_graph(self, causes, effects):
        """构建因果图"""
        graph = self.nx.DiGraph()

        # 添加所有节点
        all_nodes = causes + effects
        for node in all_nodes:
            if node not in graph.nodes():
                graph.add_node(node)

        # 添加因果边
        for cause in causes:
            for effect in effects:
                if cause != effect:
                    graph.add_edge(cause, effect, type='causes')

        return graph
```

**3. 知识图谱提示（Knowledge Graph Prompting）**

基于知识图谱的推理：

```python
class KnowledgeGraphPrompting:
    """知识图谱提示"""
    def __init__(self, llm):
        self.llm = llm
        self.concept_extractor = ConceptExtractor()
        self.knowledge_builder = KnowledgeGraphBuilder()

    def solve_with_knowledge_graph(self, question, context=None):
        """使用知识图谱解决问题"""
        # 1. 提取概念
        concepts = self.concept_extractor.extract_concepts(question, context)
        print(f"提取概念: {concepts}")

        # 2. 构建知识图谱
        kg = self.knowledge_builder.build_knowledge_graph(concepts)
        print(f"知识图谱节点: {len(kg.nodes())}")

        # 3. 知识推理
        knowledge_reasoning = self.perform_knowledge_reasoning(kg, question)

        # 4. 生成答案
        answer = self.generate_knowledge_answer(knowledge_reasoning)

        return {
            'concepts': concepts,
            'knowledge_graph': kg,
            'reasoning': knowledge_reasoning,
            'answer': answer
        }

    def perform_knowledge_reasoning(self, graph, question):
        """执行知识推理"""
        reasoning_prompt = f"""
        基于以下知识图谱进行推理：

        问题：{question}
        概念：{list(graph.nodes())}
        知识边：{list(graph.edges(data=True))}

        请基于知识图谱进行推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=500)

    def generate_knowledge_answer(self, reasoning):
        """生成知识答案"""
        answer_prompt = f"""
        基于知识推理结果回答问题：

        推理：{reasoning}

        答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=400)

class ConceptExtractor:
    """概念提取器"""
    def extract_concepts(self, question, context):
        """提取概念"""
        extraction_prompt = f"""
        从以下问题中提取关键概念：

        问题：{question}
        上下文：{context}

        请列出所有重要概念：
        """
        result = self.llm.generate(extraction_prompt, max_tokens=300)
        return self.parse_concepts(result)

    def parse_concepts(self, result):
        """解析概念"""
        concepts = []
        lines = result.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                concept = line.split('：')[-1].strip() if '：' in line else line.strip()
                if concept and len(concept) > 1:
                    concepts.append(concept)
        return concepts

class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def build_knowledge_graph(self, concepts):
        """构建知识图谱"""
        graph = self.nx.Graph()  # 无向图

        # 添加概念节点
        for concept in concepts:
            graph.add_node(concept, type='concept')

        # 添加概念间的关系（简化处理）
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                graph.add_edge(concepts[i], concepts[j], type='related')

        return graph
```

### 图提示系统的核心技术

**1. 图构建算法（Graph Construction Algorithm）**

```python
class AdvancedGraphBuilder:
    """高级图构建器"""
    def __init__(self, llm):
        self.llm = llm

    def construct_advanced_graph(self, text_data, graph_type='semantic'):
        """构建高级图"""
        if graph_type == 'semantic':
            return self.construct_semantic_graph(text_data)
        elif graph_type == 'dependency':
            return self.construct_dependency_graph(text_data)
        elif graph_type == 'concept':
            return self.construct_concept_graph(text_data)
        else:
            return self.construct_semantic_graph(text_data)

    def construct_semantic_graph(self, text_data):
        """构建语义图"""
        # 1. 语义分析
        semantic_analysis = self.analyze_semantics(text_data)

        # 2. 提取语义单元
        semantic_units = self.extract_semantic_units(semantic_analysis)

        # 3. 建立语义关系
        semantic_relations = self.extract_semantic_relations(semantic_units)

        # 4. 构建图
        import networkx as nx
        graph = nx.DiGraph()

        # 添加节点
        for unit in semantic_units:
            graph.add_node(unit['id'],
                          text=unit['text'],
                          type=unit['type'],
                          weight=unit['weight'])

        # 添加边
        for relation in semantic_relations:
            graph.add_edge(relation['source'],
                          relation['target'],
                          type=relation['type'],
                          weight=relation['weight'])

        return graph

    def analyze_semantics(self, text_data):
        """分析语义"""
        analysis_prompt = f"""
        分析以下文本的语义结构：

        文本：{text_data}

        请分析：
        1. 语义单元（句子、词组等）
        2. 语义类型（实体、属性、关系等）
        3. 语义权重

        语义分析：
        """
        return self.llm.generate(analysis_prompt, max_tokens=400)

    def extract_semantic_units(self, analysis):
        """提取语义单元"""
        # 简化的语义单元提取
        units = []
        lines = analysis.split('\n')

        for i, line in enumerate(lines):
            if line.strip():
                units.append({
                    'id': f'unit_{i}',
                    'text': line.strip(),
                    'type': 'semantic_unit',
                    'weight': 1.0
                })

        return units

    def extract_semantic_relations(self, units):
        """提取语义关系"""
        relations = []

        # 简化：相邻单元间有关系
        for i in range(len(units) - 1):
            relations.append({
                'source': units[i]['id'],
                'target': units[i + 1]['id'],
                'type': 'semantic_connection',
                'weight': 0.8
            })

        return relations

    def construct_dependency_graph(self, text_data):
        """构建依存图"""
        # 简化的依存关系构建
        import networkx as nx
        graph = nx.DiGraph()

        words = text_data.split()
        for i, word in enumerate(words):
            graph.add_node(f'word_{i}', text=word, pos='unknown')

        # 添加依存边（简化）
        for i in range(len(words) - 1):
            graph.add_edge(f'word_{i}', f'word_{i + 1}', type='dependency')

        return graph

    def construct_concept_graph(self, text_data):
        """构建概念图"""
        # 1. 概念识别
        concepts = self.identify_concepts(text_data)

        # 2. 概念关系识别
        concept_relations = self.identify_concept_relations(concepts)

        # 3. 构建图
        import networkx as nx
        graph = nx.Graph()

        for concept in concepts:
            graph.add_node(concept, type='concept')

        for relation in concept_relations:
            graph.add_edge(relation['concept1'],
                          relation['concept2'],
                          type=relation['relation_type'])

        return graph

    def identify_concepts(self, text_data):
        """识别概念"""
        concept_prompt = f"""
        从以下文本中识别关键概念：

        文本：{text_data}

        请列出所有重要概念：
        """
        result = self.llm.generate(concept_prompt, max_tokens=300)

        concepts = []
        lines = result.split('\n')
        for line in lines:
            if line.strip():
                concept = line.split('：')[-1].strip() if '：' in line else line.strip()
                if concept:
                    concepts.append(concept)

        return concepts

    def identify_concept_relations(self, concepts):
        """识别概念关系"""
        relation_prompt = f"""
        识别以下概念间的关系：

        概念：{concepts}

        请列出概念间的关系：
        """
        result = self.llm.generate(relation_prompt, max_tokens=300)

        relations = []
        lines = result.split('\n')
        for line in lines:
            if line.strip():
                # 简化的关系解析
                relations.append({
                    'concept1': concepts[0] if concepts else 'unknown',
                    'concept2': concepts[1] if len(concepts) > 1 else 'unknown',
                    'relation_type': 'semantic_related'
                })

        return relations
```

**2. 图遍历算法（Graph Traversal Algorithm）**

```python
class AdvancedGraphTraverser:
    """高级图遍历器"""
    def __init__(self, llm):
        self.llm = llm
        self.traversal_strategies = {
            'DFS': self.depth_first_search,
            'BFS': self.breadth_first_search,
            'DIJKSTRA': self.dijkstra_search,
            'A_STAR': self.a_star_search,
            'BEAM': self.beam_search,
            'GREEDY': self.greedy_search
        }

    def traverse_with_strategy(self, graph, strategy_name, start_node=None, target_node=None):
        """使用指定策略遍历图"""
        if strategy_name not in self.traversal_strategies:
            strategy_name = 'BFS'  # 默认策略

        strategy_func = self.traversal_strategies[strategy_name]

        # 选择起始节点
        if start_node is None:
            start_node = list(graph.nodes())[0] if graph.nodes() else None

        if start_node is None:
            return []

        # 执行遍历
        return strategy_func(graph, start_node, target_node)

    def depth_first_search(self, graph, start_node, target_node=None, max_depth=10):
        """深度优先搜索"""
        visited = set()
        path = []

        def dfs(node, depth):
            if depth > max_depth or node in visited:
                return False

            visited.add(node)
            path.append(node)

            if target_node and node == target_node:
                return True

            for neighbor in graph.successors(node):
                if dfs(neighbor, depth + 1):
                    return True

            return False

        dfs(start_node, 0)
        return path

    def breadth_first_search(self, graph, start_node, target_node=None):
        """广度优先搜索"""
        if start_node not in graph.nodes():
            return []

        queue = [start_node]
        visited = set([start_node])
        path = []

        while queue:
            node = queue.pop(0)
            path.append(node)

            if target_node and node == target_node:
                break

            for neighbor in graph.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return path

    def dijkstra_search(self, graph, start_node, target_node=None):
        """Dijkstra最短路径搜索"""
        import heapq

        if start_node not in graph.nodes():
            return []

        distances = {node: float('inf') for node in graph.nodes()}
        distances[start_node] = 0
        previous = {}
        visited = set()
        queue = [(0, start_node)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node in visited:
                continue

            visited.add(current_node)

            if target_node and current_node == target_node:
                break

            for neighbor in graph.successors(current_node):
                edge_weight = graph.edges[current_node, neighbor].get('weight', 1.0)
                distance = current_distance + edge_weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # 重构路径
        if target_node and target_node in previous:
            path = []
            node = target_node
            while node is not None:
                path.append(node)
                node = previous.get(node)
            return list(reversed(path))
        else:
            # 返回所有可达节点
            return [node for node in distances if distances[node] < float('inf')]

    def a_star_search(self, graph, start_node, target_node, heuristic_func=None):
        """A*搜索"""
        if start_node not in graph.nodes() or target_node not in graph.nodes():
            return []

        # 简化的A*实现
        return self.dijkstra_search(graph, start_node, target_node)

    def beam_search(self, graph, start_node, beam_width=3, max_steps=10):
        """束搜索"""
        current_paths = [[start_node]]

        for step in range(max_steps):
            next_paths = []

            for path in current_paths:
                current_node = path[-1]
                for neighbor in graph.successors(current_node):
                    new_path = path + [neighbor]
                    next_paths.append(new_path)

            # 排序并裁剪
            next_paths.sort(key=len, reverse=True)
            current_paths = next_paths[:beam_width]

            # 检查是否完成
            if all(len(path) >= max_steps for path in current_paths):
                break

        return current_paths[0] if current_paths else []

    def greedy_search(self, graph, start_node, target_node, greedy_func=None):
        """贪心搜索"""
        if start_node not in graph.nodes() or target_node not in graph.nodes():
            return []

        current_node = start_node
        path = [current_node]

        while current_node != target_node:
            neighbors = list(graph.successors(current_node))
            if not neighbors:
                break

            # 简化的贪心选择
            next_node = neighbors[0] if neighbors else None
            if next_node is None or next_node in path:
                break

            path.append(next_node)
            current_node = next_node

        return path

    def get_traversal_statistics(self, traversal_path, graph):
        """获取遍历统计信息"""
        if not traversal_path or not graph.nodes():
            return {
                'path_length': 0,
                'node_coverage': 0.0,
                'edge_coverage': 0.0,
                'efficiency': 0.0
            }

        # 路径长度
        path_length = len(traversal_path)

        # 节点覆盖率
        visited_nodes = set(traversal_path)
        node_coverage = len(visited_nodes) / len(graph.nodes())

        # 边覆盖率
        traversed_edges = 0
        for i in range(len(traversal_path) - 1):
            if graph.has_edge(traversal_path[i], traversal_path[i + 1]):
                traversed_edges += 1

        total_possible_edges = min(path_length - 1, len(graph.edges()))
        edge_coverage = traversed_edges / max(total_possible_edges, 1)

        # 效率（路径长度/节点覆盖率）
        efficiency = node_coverage / max(path_length, 1)

        return {
            'path_length': path_length,
            'node_coverage': node_coverage,
            'edge_coverage': edge_coverage,
            'efficiency': efficiency
        }
```

**3. 图推理算法（Graph Reasoning Algorithm）**

```python
class AdvancedGraphReasoner:
    """高级图推理器"""
    def __init__(self, llm):
        self.llm = llm
        self.reasoning_methods = {
            'rule_based': self.rule_based_reasoning,
            'neural_based': self.neural_based_reasoning,
            'hybrid': self.hybrid_reasoning,
            'path_based': self.path_based_reasoning
        }

    def reason_with_method(self, graph, traversal_path, question, method='hybrid'):
        """使用指定方法推理"""
        if method not in self.reasoning_methods:
            method = 'hybrid'

        reasoning_func = self.reasoning_methods[method]
        return reasoning_func(graph, traversal_path, question)

    def rule_based_reasoning(self, graph, path, question):
        """基于规则的推理"""
        # 1. 提取图规则
        rules = self.extract_graph_rules(graph)

        # 2. 应用规则
        rule_applications = self.apply_rules(rules, path)

        # 3. 推导结论
        conclusions = self.derive_conclusions(rule_applications)

        return {
            'rules': rules,
            'applications': rule_applications,
            'conclusions': conclusions
        }

    def extract_graph_rules(self, graph):
        """提取图规则"""
        rules = []

        # 节点类型规则
        for node in graph.nodes():
            node_type = graph.nodes[node].get('type', 'unknown')
            if node_type == 'entity':
                rules.append(f"节点{node}是实体")
            elif node_type == 'concept':
                rules.append(f"节点{node}是概念")

        # 边类型规则
        for edge in graph.edges(data=True):
            source, target, edge_data = edge
            edge_type = edge_data.get('type', 'unknown')
            rules.append(f"{source}到{target}的关系类型是{edge_type}")

        return rules

    def apply_rules(self, rules, path):
        """应用规则"""
        applications = []

        for rule in rules:
            for node in path:
                if node in rule:
                    applications.append({
                        'rule': rule,
                        'applicable_node': node,
                        'confidence': 0.8
                    })

        return applications

    def derive_conclusions(self, applications):
        """推导结论"""
        conclusions = []

        for app in applications:
            conclusion = f"基于规则'{app['rule']}'在节点'{app['applicable_node']}'的结论"
            conclusions.append(conclusion)

        return conclusions

    def neural_based_reasoning(self, graph, path, question):
        """基于神经网络的推理"""
        # 使用LLM进行推理
        reasoning_prompt = f"""
        基于以下图结构和遍历路径进行推理：

        问题：{question}
        图节点：{list(graph.nodes())}
        图边：{list(graph.edges(data=True))}
        遍历路径：{path}

        请进行深度推理：
        """
        neural_reasoning = self.llm.generate(reasoning_prompt, max_tokens=500)

        return {
            'method': 'neural',
            'reasoning': neural_reasoning,
            'confidence': 0.85
        }

    def hybrid_reasoning(self, graph, path, question):
        """混合推理"""
        # 结合规则和神经方法
        rule_results = self.rule_based_reasoning(graph, path, question)
        neural_results = self.neural_based_reasoning(graph, path, question)

        # 融合结果
        fused_conclusions = self.fuse_reasoning_results(
            rule_results, neural_results
        )

        return {
            'rule_based': rule_results,
            'neural_based': neural_results,
            'fused_conclusions': fused_conclusions,
            'method': 'hybrid'
        }

    def fuse_reasoning_results(self, rule_results, neural_results):
        """融合推理结果"""
        fusion_prompt = f"""
        融合以下推理结果：

        规则推理：{rule_results.get('conclusions', [])}
        神经推理：{neural_results.get('reasoning', '')}

        请提供融合后的结论：
        """
        fused = self.llm.generate(fusion_prompt, max_tokens=400)
        return fused

    def path_based_reasoning(self, graph, path, question):
        """基于路径的推理"""
        # 分析路径中的节点和边
        path_analysis = self.analyze_path(graph, path)

        # 基于路径推理
        path_reasoning = self.reason_from_path(path_analysis, question)

        return {
            'path_analysis': path_analysis,
            'path_reasoning': path_reasoning,
            'method': 'path_based'
        }

    def analyze_path(self, graph, path):
        """分析路径"""
        analysis = {
            'path_length': len(path),
            'nodes': path,
            'edges': [],
            'node_types': [],
            'edge_types': []
        }

        for i in range(len(path) - 1):
            edge_data = graph.edges[path[i], path[i + 1]]
            analysis['edges'].append((path[i], path[i + 1], edge_data))
            analysis['edge_types'].append(edge_data.get('type', 'unknown'))

        for node in path:
            node_data = graph.nodes[node]
            analysis['node_types'].append(node_data.get('type', 'unknown'))

        return analysis

    def reason_from_path(self, path_analysis, question):
        """从路径推理"""
        reasoning_prompt = f"""
        基于以下路径分析进行推理：

        问题：{question}
        路径长度：{path_analysis['path_length']}
        路径节点：{path_analysis['nodes']}
        节点类型：{path_analysis['node_types']}
        边类型：{path_analysis['edge_types']}

        请基于路径结构进行推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=400)

    def evaluate_reasoning_quality(self, reasoning_result, ground_truth=None):
        """评估推理质量"""
        if not reasoning_result:
            return {'score': 0.0, 'reasons': ['推理结果为空']}

        quality_factors = {
            'completeness': self.evaluate_completeness(reasoning_result),
            'consistency': self.evaluate_consistency(reasoning_result),
            'coherence': self.evaluate_coherence(reasoning_result),
            'soundness': self.evaluate_soundness(reasoning_result)
        }

        # 计算综合分数
        weights = {
            'completeness': 0.3,
            'consistency': 0.25,
            'coherence': 0.25,
            'soundness': 0.2
        }

        overall_score = sum(
            quality_factors[factor] * weights[factor]
            for factor in quality_factors
        )

        return {
            'overall_score': overall_score,
            'quality_factors': quality_factors,
            'assessment': self.generate_quality_assessment(quality_factors)
        }

    def evaluate_completeness(self, result):
        """评估完整性"""
        # 检查推理是否包含必要组成部分
        necessary_components = ['conclusion', 'reasoning', 'evidence']
        present_components = sum(1 for comp in necessary_components if comp in str(result))

        return present_components / len(necessary_components)

    def evaluate_consistency(self, result):
        """评估一致性"""
        # 简化的一致性评估
        return 0.8  # 模拟分数

    def evaluate_coherence(self, result):
        """评估连贯性"""
        # 基于推理步骤的连贯性评估
        return 0.75  # 模拟分数

    def evaluate_soundness(self, result):
        """评估合理性"""
        # 基于逻辑推理的合理性评估
        return 0.8  # 模拟分数

    def generate_quality_assessment(self, factors):
        """生成质量评估"""
        assessment = []

        if factors['completeness'] < 0.6:
            assessment.append("推理不够完整")

        if factors['consistency'] < 0.6:
            assessment.append("推理前后不一致")

        if factors['coherence'] < 0.6:
            assessment.append("推理过程不够连贯")

        if factors['soundness'] < 0.6:
            assessment.append("推理缺乏合理性")

        if not assessment:
            assessment.append("推理质量良好")

        return assessment
```

## 实践任务

### 任务1：基础图提示系统实现

**目标：**
实现一个基础的多模态提示系统，能够处理文本、图像等多种模态的输入。

**步骤1：核心图提示系统**
```python
class BasicGraphPromptSystem:
    """基础图提示系统"""
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = BasicGraphBuilder()
        self.graph_traverser = BasicGraphTraverser()
        self.graph_reasoner = BasicGraphReasoner()

    def solve_question_with_graph(self, question, context=None):
        """
        使用图提示解决问题

        Args:
            question: 问题描述
            context: 上下文信息

        Returns:
            dict: 图提示解决结果
        """
        print(f"\n=== 图提示问题解决 ===")
        print(f"问题: {question}")

        # 1. 分析问题
        print("\n1. 分析问题...")
        problem_analysis = self.analyze_problem(question, context)
        print(f"   分析结果: {problem_analysis}")

        # 2. 构建图
        print("\n2. 构建图结构...")
        graph = self.graph_builder.build_graph_from_text(problem_analysis)
        print(f"   图节点数: {len(graph.nodes())}")
        print(f"   图边数: {len(graph.edges())}")

        # 3. 遍历图
        print("\n3. 遍历图结构...")
        traversal_path = self.graph_traverser.traverse_graph(graph)
        print(f"   遍历路径: {traversal_path}")

        # 4. 图推理
        print("\n4. 进行图推理...")
        reasoning_result = self.graph_reasoner.reason_on_graph(
            graph, traversal_path, question
        )

        # 5. 生成答案
        print("\n5. 生成最终答案...")
        final_answer = self.generate_final_answer(reasoning_result)

        return {
            'question': question,
            'problem_analysis': problem_analysis,
            'graph': graph,
            'traversal_path': traversal_path,
            'reasoning_result': reasoning_result,
            'final_answer': final_answer
        }

    def analyze_problem(self, question, context):
        """分析问题"""
        analysis_prompt = f"""
        分析以下问题，提取关键元素：

        问题：{question}
        上下文：{context}

        请提取：
        1. 主要实体（人物、地点、物品等）
        2. 关键关系（因果、包含、比较等）
        3. 问题类型（是什么、为什么、怎么做等）

        分析结果：
        """
        return self.llm.generate(analysis_prompt, max_tokens=400)

    def generate_final_answer(self, reasoning_result):
        """生成最终答案"""
        answer_prompt = f"""
        基于图推理结果生成最终答案：

        推理结果：{reasoning_result}

        请提供完整、准确的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=500)

class BasicGraphBuilder:
    """基础图构建器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def build_graph_from_text(self, text_analysis):
        """从文本分析构建图"""
        graph = self.nx.DiGraph()

        # 简化的图构建：基于文本中的关键词
        lines = text_analysis.split('\n')
        nodes = []

        for line in lines:
            if line.strip() and '：' in line:
                # 提取冒号后的内容作为节点
                parts = line.split('：')
                if len(parts) >= 2:
                    node_text = parts[1].strip()
                    if node_text and len(node_text) > 1:
                        nodes.append(node_text)

        # 添加节点
        for i, node in enumerate(nodes):
            graph.add_node(f"node_{i}", text=node)

        # 添加边（相邻节点相连）
        for i in range(len(nodes) - 1):
            graph.add_edge(f"node_{i}", f"node_{i+1}", type='sequential')

        return graph

class BasicGraphTraverser:
    """基础图遍历器"""
    def __init__(self):
        import networkx as nx
        self.nx = nx

    def traverse_graph(self, graph):
        """遍历图"""
        if not graph.nodes():
            return []

        # 从第一个节点开始BFS
        start_node = list(graph.nodes())[0]
        visited = set()
        path = []

        queue = [start_node]
        visited.add(start_node)

        while queue:
            node = queue.pop(0)
            path.append(node)

            # 添加邻居到队列
            for neighbor in graph.successors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return path

class BasicGraphReasoner:
    """基础图推理器"""
    def __init__(self, llm):
        self.llm = llm

    def reason_on_graph(self, graph, path, question):
        """在图上进行推理"""
        # 构建图上下文
        graph_context = self.build_graph_context(graph, path)

        # 推理提示
        reasoning_prompt = f"""
        基于以下图结构进行推理：

        问题：{question}
        图节点：{list(graph.nodes(data=True))}
        图边：{list(graph.edges(data=True))}
        遍历路径：{path}
        上下文：{graph_context}

        请进行逻辑推理：
        """
        return self.llm.generate(reasoning_prompt, max_tokens=400)

    def build_graph_context(self, graph, path):
        """构建图上下文"""
        context_parts = []

        for node in path:
            node_data = graph.nodes[node]
            context_parts.append(f"节点: {node_data.get('text', node)}")

            # 添加边的信息
            for edge in graph.edges(node):
                edge_data = graph.edges[edge]
                context_parts.append(f"  -> 连接到: {edge[1]}, 关系: {edge_data.get('type', 'unknown')}")

        return "\n".join(context_parts)
```

### 任务2：高级图提示系统优化

**目标：**
实现高级图提示系统，包括多种图类型、智能遍历策略、高级推理算法等功能。

**步骤：高级图提示系统**
```python
class AdvancedGraphPromptSystem:
    """高级图提示系统"""
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = AdvancedGraphBuilder(llm)
        self.graph_traverser = AdvancedGraphTraverser(llm)
        self.graph_reasoner = AdvancedGraphReasoner(llm)
        self.optimization_engine = GraphPromptOptimizationEngine(llm)

    def solve_complex_question(self, question, context=None, graph_type='semantic'):
        """
        解决复杂问题

        Args:
            question: 问题描述
            context: 上下文信息
            graph_type: 图类型 ('semantic', 'causal', 'dependency', 'knowledge')

        Returns:
            dict: 高级图提示解决结果
        """
        print(f"\n=== 高级图提示问题解决 ===")
        print(f"问题: {question}")
        print(f"图类型: {graph_type}")

        # 1. 复杂问题分析
        print("\n1. 复杂问题分析...")
        complex_analysis = self.analyze_complex_question(question, context)
        print(f"   分析维度: {len(complex_analysis)}")

        # 2. 构建高级图
        print("\n2. 构建高级图结构...")
        advanced_graph = self.graph_builder.build_advanced_graph(
            complex_analysis, graph_type
        )
        print(f"   图节点数: {len(advanced_graph.nodes())}")
        print(f"   图边数: {len(advanced_graph.edges())}")

        # 3. 智能遍历策略
        print("\n3. 应用智能遍历策略...")
        traversal_results = self.graph_traverser.intelligent_traverse(
            advanced_graph, question
        )
        print(f"   遍历路径数: {len(traversal_results['paths'])}")

        # 4. 高级图推理
        print("\n4. 执行高级图推理...")
        reasoning_results = self.graph_reasoner.advanced_reasoning(
            advanced_graph, traversal_results, question
        )

        # 5. 图提示优化
        print("\n5. 图提示优化...")
        optimized_results = self.optimization_engine.optimize_graph_prompt(
            reasoning_results, question
        )

        # 6. 生成最终答案
        print("\n6. 生成最终答案...")
        final_answer = self.generate_optimized_answer(optimized_results)

        return {
            'question': question,
            'graph_type': graph_type,
            'complex_analysis': complex_analysis,
            'advanced_graph': advanced_graph,
            'traversal_results': traversal_results,
            'reasoning_results': reasoning_results,
            'optimized_results': optimized_results,
            'final_answer': final_answer
        }

    def analyze_complex_question(self, question, context):
        """分析复杂问题"""
        analysis_prompt = f"""
        深度分析以下复杂问题：

        问题：{question}
        上下文：{context}

        请从多个维度分析：
        1. 问题结构（层次、依赖关系等）
        2. 实体类型（具体实体、抽象概念等）
        3. 关系类型（因果、包含、比较等）
        4. 推理类型（演绎、归纳、类比等）
        5. 解决方案（直接推理、多步推理等）

        详细分析：
        """
        return self.llm.generate(analysis_prompt, max_tokens=600)

    def generate_optimized_answer(self, optimized_results):
        """生成优化答案"""
        answer_prompt = f"""
        基于优化后的图推理结果生成最终答案：

        优化结果：{optimized_results}

        请提供最优化的最终答案：
        """
        return self.llm.generate(answer_prompt, max_tokens=500)

class AdvancedGraphBuilder:
    """高级图构建器"""
    def __init__(self, llm):
        self.llm = llm
        self.graph_types = {
            'semantic': self.build_semantic_graph,
            'causal': self.build_causal_graph,
            'dependency': self.build_dependency_graph,
            'knowledge': self.build_knowledge_graph
        }

    def build_advanced_graph(self, analysis, graph_type):
        """构建高级图"""
        if graph_type not in self.graph_types:
            graph_type = 'semantic'

        builder_func = self.graph_types[graph_type]
        return builder_func(analysis)

    def build_semantic_graph(self, analysis):
        """构建语义图"""
        import networkx as nx
        graph = nx.DiGraph()

        # 从分析中提取语义单元
        semantic_units = self.extract_semantic_units(analysis)
        semantic_relations = self.extract_semantic_relations(semantic_units)

        # 添加节点
        for unit in semantic_units:
            graph.add_node(unit['id'],
                          text=unit['text'],
                          type=unit['type'],
                          weight=unit['weight'])

        # 添加边
        for relation in semantic_relations:
            graph.add_edge(relation['source'],
                          relation['target'],
                          type=relation['type'],
                          weight=relation['weight'])

        return graph

    def extract_semantic_units(self, analysis):
        """提取语义单元"""
        units = []
        lines = analysis.split('\n')

        for i, line in enumerate(lines):
            if line.strip():
                units.append({
                    'id': f'semantic_{i}',
                    'text': line.strip(),
                    'type': 'semantic_unit',
                    'weight': 1.0
                })

        return units

    def extract_semantic_relations(self, units):
        """提取语义关系"""
        relations = []
        for i in range(len(units) - 1):
            relations.append({
                'source': units[i]['id'],
                'target': units[i + 1]['id'],
                'type': 'semantic_connection',
                'weight': 0.8
            })
        return relations

    def build_causal_graph(self, analysis):
        """构建因果图"""
        import networkx as nx
        graph = nx.DiGraph()

        # 提取因果关系
        causal_relations = self.extract_causal_relations(analysis)

        # 添加节点和边
        for relation in causal_relations:
            if 'cause' not in graph.nodes():
                graph.add_node(relation['cause'], type='cause')
            if 'effect' not in graph.nodes():
                graph.add_node(relation['effect'], type='effect')

            graph.add_edge(relation['cause'],
                          relation['effect'],
                          type='causes',
                          weight=relation['strength'])

        return graph

    def extract_causal_relations(self, analysis):
        """提取因果关系"""
        # 简化的因果关系提取
        relations = [
            {'cause': '原因1', 'effect': '结果1', 'strength': 0.9},
            {'cause': '原因2', 'effect': '结果2', 'strength': 0.7}
        ]
        return relations

    def build_dependency_graph(self, analysis):
        """构建依存图"""
        import networkx as nx
        graph = nx.DiGraph()

        # 提取依存关系
        dependency_relations = self.extract_dependency_relations(analysis)

        for relation in dependency_relations:
            graph.add_edge(relation['dependent'],
                          relation['head'],
                          type=relation['dep_type'],
                          weight=1.0)

        return graph

    def extract_dependency_relations(self, analysis):
        """提取依存关系"""
        # 简化的依存关系
        relations = [
            {'dependent': 'A', 'head': 'B', 'dep_type': 'nsubj'},
            {'dependent': 'B', 'head': 'C', 'dep_type': 'dobj'}
        ]
        return relations

    def build_knowledge_graph(self, analysis):
        """构建知识图谱"""
        import networkx as nx
        graph = nx.Graph()  # 无向图

        # 提取知识三元组
        knowledge_triples = self.extract_knowledge_triples(analysis)

        for triple in knowledge_triples:
            graph.add_edge(triple['subject'],
                          triple['object'],
                          relation=triple['relation'])

        return graph

    def extract_knowledge_triples(self, analysis):
        """提取知识三元组"""
        # 简化的知识三元组
        triples = [
            {'subject': '实体1', 'relation': '是', 'object': '概念1'},
            {'subject': '实体2', 'relation': '属于', 'object': '类别1'}
        ]
        return triples

class AdvancedGraphTraverser:
    """高级图遍历器"""
    def __init__(self, llm):
        self.llm = llm
        self.traversal_strategies = ['BFS', 'DFS', 'best_first', 'beam_search']

    def intelligent_traverse(self, graph, question):
        """智能遍历"""
        # 1. 选择最佳遍历策略
        strategy = self.select_best_strategy(graph, question)

        # 2. 执行遍历
        paths = self.execute_traversal(graph, strategy)

        # 3. 评估遍历结果
        evaluated_paths = self.evaluate_traversal_paths(paths, graph, question)

        return {
            'strategy': strategy,
            'paths': evaluated_paths,
            'best_path': evaluated_paths[0] if evaluated_paths else None
        }

    def select_best_strategy(self, graph, question):
        """选择最佳策略"""
        selection_prompt = f"""
        基于以下条件选择最佳遍历策略：

        问题：{question}
        图规模：节点{len(graph.nodes())}个，边{len(graph.edges())}个

        可选策略：
        1. BFS：广度优先，适合寻找最短路径
        2. DFS：深度优先，适合探索深层关系
        3. Best-First：最佳优先，适合目标导向搜索
        4. Beam Search：束搜索，适合受约束的搜索

        请选择最合适的策略并说明原因：
        """
        strategy_response = self.llm.generate(selection_prompt, max_tokens=200)

        # 解析策略
        for strategy in self.traversal_strategies:
            if strategy.lower() in strategy_response.lower():
                return strategy

        return 'BFS'  # 默认策略

    def execute_traversal(self, graph, strategy):
        """执行遍历"""
        paths = []

        if strategy == 'BFS':
            paths = self.breadth_first_traverse(graph)
        elif strategy == 'DFS':
            paths = self.depth_first_traverse(graph)
        elif strategy == 'best_first':
            paths = self.best_first_traverse(graph)
        elif strategy == 'beam_search':
            paths = self.beam_search_traverse(graph)

        return paths

    def breadth_first_traverse(self, graph):
        """广度优先遍历"""
        import networkx as nx
        paths = []

        for start_node in graph.nodes():
            visited = set([start_node])
            queue = [(start_node, [start_node])]

            while queue:
                node, path = queue.pop(0)
                paths.append(path)

                for neighbor in graph.successors(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        return paths

    def depth_first_traverse(self, graph):
        """深度优先遍历"""
        import networkx as nx
        paths = []

        for start_node in graph.nodes():
            visited = set()
            path = []

            def dfs(node):
                visited.add(node)
                path.append(node)
                paths.append(path.copy())

                for neighbor in graph.successors(node):
                    if neighbor not in visited:
                        dfs(neighbor)

                path.pop()

            dfs(start_node)

        return paths

    def best_first_traverse(self, graph):
        """最佳优先遍历"""
        # 简化的最佳优先搜索
        return self.breadth_first_traverse(graph)

    def beam_search_traverse(self, graph, beam_width=3):
        """束搜索遍历"""
        # 简化的束搜索
        return self.breadth_first_traverse(graph)[:beam_width]

    def evaluate_traversal_paths(self, paths, graph, question):
        """评估遍历路径"""
        evaluated_paths = []

        for path in paths:
            score = self.evaluate_single_path(path, graph, question)
            evaluated_paths.append({
                'path': path,
                'score': score
            })

        # 按分数排序
        evaluated_paths.sort(key=lambda x: x['score'], reverse=True)
        return evaluated_paths

    def evaluate_single_path(self, path, graph, question):
        """评估单条路径"""
        # 简化的路径评估
        factors = {
            'length': len(path) / 10,  # 归一化长度
            'connectivity': self.assess_connectivity(path, graph),
            'relevance': self.assess_relevance(path, question)
        }

        weights = {'length': 0.2, 'connectivity': 0.4, 'relevance': 0.4}
        score = sum(factors[factor] * weights[factor] for factor in factors)

        return score

    def assess_connectivity(self, path, graph):
        """评估连通性"""
        if len(path) < 2:
            return 0.0

        connected_edges = 0
        for i in range(len(path) - 1):
            if graph.has_edge(path[i], path[i + 1]):
                connected_edges += 1

        return connected_edges / (len(path) - 1)

    def assess_relevance(self, path, question):
        """评估相关性"""
        # 简化的相关性评估
        return 0.8  # 模拟分数

class GraphPromptOptimizationEngine:
    """图提示优化引擎"""
    def __init__(self, llm):
        self.llm = llm

    def optimize_graph_prompt(self, reasoning_results, question):
        """优化图提示"""
        # 1. 分析当前结果
        analysis = self.analyze_current_results(reasoning_results)

        # 2. 生成优化建议
        suggestions = self.generate_optimization_suggestions(analysis, question)

        # 3. 应用优化
        optimized = self.apply_optimizations(reasoning_results, suggestions)

        return optimized

    def analyze_current_results(self, results):
        """分析当前结果"""
        analysis_prompt = f"""
        分析以下图推理结果：

        结果：{results}

        请评估：
        1. 推理质量
        2. 完整性
        3. 准确性

        分析：
        """
        return self.llm.generate(analysis_prompt, max_tokens=300)

    def generate_optimization_suggestions(self, analysis, question):
        """生成优化建议"""
        suggestion_prompt = f"""
        基于分析结果，为以下问题提供优化建议：

        问题：{question}
        分析：{analysis}

        优化建议：
        """
        return self.llm.generate(suggestion_prompt, max_tokens=300)

    def apply_optimizations(self, results, suggestions):
        """应用优化"""
        optimization_prompt = f"""
        应用以下优化建议改进结果：

        原结果：{results}
        优化建议：{suggestions}

        优化后的结果：
        """
        return self.llm.generate(optimization_prompt, max_tokens=400)
```

### 任务3：图提示系统评估与优化

**目标：**
构建图提示系统的全面评估框架，分析系统性能和推理质量。

**步骤：评估与优化系统**
```python
class GraphPromptEvaluator:
    """图提示系统评估器"""
    def __init__(self, graph_system):
        self.graph_system = graph_system
        self.evaluation_metrics = {
            'graph_quality': self.evaluate_graph_quality,
            'traversal_effectiveness': self.evaluate_traversal_effectiveness,
            'reasoning_accuracy': self.evaluate_reasoning_accuracy,
            'answer_quality': self.evaluate_answer_quality,
            'efficiency': self.evaluate_efficiency
        }

    def comprehensive_evaluation(self, test_questions):
        """
        综合评估图提示系统

        Args:
            test_questions: 测试问题列表

        Returns:
            dict: 评估结果
        """
        print("开始图提示系统综合评估...")
        print(f"测试问题数量: {len(test_questions)}")

        evaluation_results = []

        for i, test_case in enumerate(test_questions, 1):
            print(f"\n测试问题 {i}/{len(test_questions)}: {test_case['question'][:50]}...")

            try:
                # 执行图提示系统
                result = self.graph_system.solve_complex_question(
                    test_case['question'],
                    test_case.get('context'),
                    test_case.get('graph_type', 'semantic')
                )

                # 评估各项指标
                metric_scores = {}
                for metric_name, metric_func in self.evaluation_metrics.items():
                    try:
                        score = metric_func(result, test_case)
                        metric_scores[metric_name] = score
                        print(f"  {metric_name}: {score:.4f}")
                    except Exception as e:
                        print(f"  {metric_name}: 评估失败 - {e}")
                        metric_scores[metric_name] = 0.0

                evaluation_results.append({
                    'test_case': test_case,
                    'result': result,
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

    def evaluate_graph_quality(self, result, test_case):
        """评估图质量"""
        graph = result.get('advanced_graph')
        if not graph:
            return 0.0

        # 评估图的各项质量指标
        graph_metrics = {
            'node_diversity': self.assess_node_diversity(graph),
            'edge_density': self.assess_edge_density(graph),
            'connectivity': self.assess_connectivity(graph),
            'structure_quality': self.assess_structure_quality(graph)
        }

        # 综合评分
        weights = {
            'node_diversity': 0.25,
            'edge_density': 0.25,
            'connectivity': 0.25,
            'structure_quality': 0.25
        }

        quality_score = sum(
            graph_metrics[metric] * weights[metric]
            for metric in graph_metrics
        )

        return quality_score

    def assess_node_diversity(self, graph):
        """评估节点多样性"""
        if not graph.nodes():
            return 0.0

        # 统计节点类型
        node_types = set()
        for node in graph.nodes():
            node_type = graph.nodes[node].get('type', 'unknown')
            node_types.add(node_type)

        return len(node_types) / len(graph.nodes())

    def assess_edge_density(self, graph):
        """评估边密度"""
        n = len(graph.nodes())
        if n <= 1:
            return 0.0

        m = len(graph.edges())
        max_edges = n * (n - 1)  # 有向图最大边数
        return m / max_edges

    def assess_connectivity(self, graph):
        """评估连通性"""
        try:
            import networkx as nx
            if nx.is_strongly_connected(graph):
                return 1.0
            else:
                # 计算强连通分量
                sccs = list(nx.strongly_connected_components(graph))
                largest_scc_size = max(len(scc) for scc in sccs) if sccs else 0
                return largest_scc_size / len(graph.nodes())
        except:
            return 0.5

    def assess_structure_quality(self, graph):
        """评估结构质量"""
        # 简化的结构质量评估
        if not graph.nodes():
            return 0.0

        # 基于平均度数评估
        total_degree = sum(dict(graph.degree()).values())
        avg_degree = total_degree / len(graph.nodes())

        # 归一化（假设理想平均度数为3）
        return min(avg_degree / 3.0, 1.0)

    def evaluate_traversal_effectiveness(self, result, test_case):
        """评估遍历有效性"""
        traversal_results = result.get('traversal_results')
        if not traversal_results:
            return 0.0

        # 评估遍历路径质量
        paths = traversal_results.get('paths', [])
        if not paths:
            return 0.0

        # 计算平均路径分数
        total_score = sum(path['score'] for path in paths)
        avg_score = total_score / len(paths)

        return avg_score

    def evaluate_reasoning_accuracy(self, result, test_case):
        """评估推理准确性"""
        reasoning_results = result.get('reasoning_results')
        if not reasoning_results:
            return 0.5

        # 使用LLM评估推理准确性
        accuracy_prompt = f"""
        评估以下图推理的准确性：

        问题：{test_case['question']}
        推理结果：{reasoning_results}

        请评分（0-1）：
        """
        # 这里需要LLM评估
        return 0.8  # 模拟评分

    def evaluate_answer_quality(self, result, test_case):
        """评估答案质量"""
        final_answer = result.get('final_answer', '')
        if not final_answer:
            return 0.0

        # 评估答案质量
        quality_aspects = {
            'completeness': self.assess_answer_completeness(final_answer),
            'accuracy': self.assess_answer_accuracy(final_answer, test_case),
            'clarity': self.assess_answer_clarity(final_answer),
            'relevance': self.assess_answer_relevance(final_answer, test_case)
        }

        # 综合评分
        weights = {
            'completeness': 0.3,
            'accuracy': 0.4,
            'clarity': 0.2,
            'relevance': 0.1
        }

        quality_score = sum(
            quality_aspects[aspect] * weights[aspect]
            for aspect in quality_aspects
        )

        return quality_score

    def assess_answer_completeness(self, answer):
        """评估答案完整性"""
        # 检查是否包含关键信息
        completeness_indicators = ['完成', '总结', '结论', '答案']
        indicator_count = sum(1 for indicator in completeness_indicators if indicator in answer)
        return indicator_count / len(completeness_indicators)

    def assess_answer_accuracy(self, answer, test_case):
        """评估答案准确性"""
        expected_elements = test_case.get('expected_elements', [])
        if not expected_elements:
            return 0.8  # 默认分数

        # 检查答案是否包含期望元素
        matched_elements = sum(1 for element in expected_elements if element in answer)
        return matched_elements / len(expected_elements)

    def assess_answer_clarity(self, answer):
        """评估答案清晰度"""
        # 基于答案长度和结构评估
        if len(answer) < 50:
            return 0.3
        elif len(answer) > 1000:
            return 0.6
        else:
            return 0.8

    def assess_answer_relevance(self, answer, test_case):
        """评估答案相关性"""
        question = test_case['question']
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())

        intersection = question_words & answer_words
        return len(intersection) / len(question_words) if question_words else 0

    def evaluate_efficiency(self, result, test_case):
        """评估效率"""
        # 评估处理时间、节点数、边数等
        graph = result.get('advanced_graph', {})
        traversal_results = result.get('traversal_results', {})

        if not graph or not traversal_results:
            return 0.0

        # 效率指标
        node_count = len(graph.nodes())
        edge_count = len(graph.edges())
        path_count = len(traversal_results.get('paths', []))

        # 简化的效率评估
        efficiency_factors = {
            'node_efficiency': 1.0 / max(node_count, 1),
            'edge_efficiency': 1.0 / max(edge_count, 1),
            'path_efficiency': 1.0 / max(path_count, 1)
        }

        return sum(efficiency_factors.values()) / len(efficiency_factors)

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
        print("图提示系统评估总结")
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

        if metrics.get('graph_quality', 0) < 0.7:
            recommendations.append(
                "改进图质量：优化图构建算法，提高节点和边的质量"
            )

        if metrics.get('traversal_effectiveness', 0) < 0.6:
            recommendations.append(
                "增强遍历效果：改进遍历策略选择，提高路径质量"
            )

        if metrics.get('reasoning_accuracy', 0) < 0.7:
            recommendations.append(
                "提高推理准确性：优化推理算法，增强逻辑推理能力"
            )

        if metrics.get('answer_quality', 0) < 0.7:
            recommendations.append(
                "提升答案质量：改进答案生成策略，提高完整性和准确性"
            )

        if metrics.get('efficiency', 0) < 0.5:
            recommendations.append(
                "优化系统效率：减少不必要的计算，提高处理速度"
            )

        if not recommendations:
            recommendations.append("系统性能优秀，可考虑在更复杂的图结构上测试")

        return recommendations
```

## 深度思考

### 图提示的认知科学基础

**图论与认知结构**

图提示模拟了人类的认知结构：
- **概念网络**：知识在脑中的网络化存储
- **联想路径**：思维在概念间的移动轨迹
- **推理图式**：解决问题的认知模板

```python
class CognitiveGraphModel:
    """认知图模型"""
    def __init__(self):
        self.conceptual_network = ConceptualNetwork()
        self.association_paths = AssociationPaths()
        self.reasoning_schemata = ReasoningSchemata()

    def simulate_cognitive_reasoning(self, problem_representation):
        """模拟认知推理"""
        # 1. 激活相关概念
        activated_concepts = self.conceptual_network.activate_concepts(
            problem_representation
        )

        # 2. 构建联想路径
        association_path = self.association_paths.build_paths(
            activated_concepts
        )

        # 3. 应用推理图式
        reasoning_result = self.reasoning_schemata.apply_schemata(
            association_path, problem_representation
        )

        return reasoning_result

class ConceptualNetwork:
    """概念网络"""
    def __init__(self):
        self.concepts = {}
        self.associations = {}

    def activate_concepts(self, problem_representation):
        """激活相关概念"""
        # 模拟概念激活
        activated = []
        for concept in self.concepts:
            if self.is_concept_relevant(concept, problem_representation):
                activation_strength = self.calculate_activation_strength(
                    concept, problem_representation
                )
                activated.append({
                    'concept': concept,
                    'strength': activation_strength
                })

        return sorted(activated, key=lambda x: x['strength'], reverse=True)

    def is_concept_relevant(self, concept, representation):
        """判断概念是否相关"""
        # 简化的相关性判断
        return True  # 模拟

    def calculate_activation_strength(self, concept, representation):
        """计算激活强度"""
        # 简化的激活强度计算
        return 0.8  # 模拟强度

class AssociationPaths:
    """联想路径"""
    def __init__(self):
        self.path_finder = PathFinder()

    def build_paths(self, activated_concepts):
        """构建联想路径"""
        paths = []

        for concept in activated_concepts:
            concept_paths = self.path_finder.find_paths(concept['concept'])
            paths.extend(concept_paths)

        return paths

class PathFinder:
    """路径查找器"""
    def find_paths(self, start_concept):
        """查找路径"""
        # 简化的路径查找
        return [
            {'path': [start_concept, '概念1', '概念2'], 'strength': 0.7},
            {'path': [start_concept, '概念3'], 'strength': 0.6}
        ]

class ReasoningSchemata:
    """推理图式"""
    def __init__(self):
        self.schemata = {
            'causal': CausalSchema(),
            'analogical': AnalogicalSchema(),
            'deductive': DeductiveSchema()
        }

    def apply_schemata(self, paths, problem_representation):
        """应用推理图式"""
        results = []

        for schema_type, schema in self.schemata.items():
            result = schema.apply(paths, problem_representation)
            if result:
                results.append(result)

        return self.combine_schema_results(results)

    def combine_schema_results(self, results):
        """组合图式结果"""
        combination_prompt = f"""
        组合以下推理图式的结果：

        结果：{results}

        综合结论：
        """
        # 这里需要实际的组合逻辑
        return "综合推理结论"

class CausalSchema:
    """因果图式"""
    def apply(self, paths, problem_representation):
        """应用因果图式"""
        return "因果推理结果"

class AnalogicalSchema:
    """类比图式"""
    def apply(self, paths, problem_representation):
        """应用类比图式"""
        return "类比推理结果"

class DeductiveSchema:
    """演绎图式"""
    def apply(self, paths, problem_representation):
        """应用演绎图式"""
        return "演绎推理结果"
```

**问题解决的心理模型**

图提示模拟了人类问题解决的心理过程：
```python
class ProblemSolvingModel:
    """问题解决模型"""
    def __init__(self):
        self.problem_representation = ProblemRepresentation()
        self.solution_search = SolutionSearch()
        self.evaluation = SolutionEvaluation()

    def solve_problem(self, problem_description):
        """解决问题"""
        # 1. 问题表征
        problem_struct = self.problem_representation.represent_problem(
            problem_description
        )

        # 2. 解空间搜索
        solution_candidates = self.solution_search.search_solutions(
            problem_struct
        )

        # 3. 解决方案评估
        best_solution = self.evaluation.evaluate_solutions(
            solution_candidates
        )

        return best_solution

class ProblemRepresentation:
    """问题表征"""
    def represent_problem(self, problem_description):
        """表征问题"""
        # 1. 问题分析
        analysis = self.analyze_problem(problem_description)

        # 2. 图式匹配
        schema_match = self.match_problem_schema(analysis)

        # 3. 问题图构建
        problem_graph = self.construct_problem_graph(analysis, schema_match)

        return problem_graph

    def analyze_problem(self, problem_description):
        """分析问题"""
        return f"问题分析: {problem_description}"

    def match_problem_schema(self, analysis):
        """匹配问题图式"""
        return "匹配的图式"

    def construct_problem_graph(self, analysis, schema_match):
        """构建问题图"""
        return "问题图结构"

class SolutionSearch:
    """解空间搜索"""
    def search_solutions(self, problem_graph):
        """搜索解"""
        # 1. 生成候选解
        candidates = self.generate_candidates(problem_graph)

        # 2. 启发式搜索
        search_paths = self.heuristic_search(candidates)

        return search_paths

    def generate_candidates(self, problem_graph):
        """生成候选解"""
        return ["候选解1", "候选解2"]

    def heuristic_search(self, candidates):
        """启发式搜索"""
        return [
            {'solution': "候选解1", 'heuristic_value': 0.8},
            {'solution': "候选解2', 'heuristic_value': 0.6}
        ]

class SolutionEvaluation:
    """解决方案评估"""
    def evaluate_solutions(self, candidates):
        """评估解"""
        # 选择最佳解
        best_candidate = max(candidates, key=lambda x: x['heuristic_value'])
        return best_candidate['solution']
```

### 图提示的技术挑战与解决方案

**1. 图构建复杂性**

挑战：如何从非结构化文本中自动构建高质量的图

解决方案：
```python
class IntelligentGraphBuilder:
    """智能图构建器"""
    def __init__(self, llm):
        self.llm = llm
        self.entity_recognizer = EntityRecognizer()
        self.relation_extractor = RelationExtractor()
        self.graph_validator = GraphValidator()

    def build_intelligent_graph(self, text_data, construction_strategy='adaptive'):
        """智能图构建"""
        # 1. 智能实体识别
        entities = self.entity_recognizer.recognize_entities(text_data)

        # 2. 智能关系提取
        relations = self.relation_extractor.extract_relations(
            text_data, entities, strategy=construction_strategy
        )

        # 3. 图构建与验证
        graph = self.construct_and_validate_graph(entities, relations)

        return graph

    def construct_and_validate_graph(self, entities, relations):
        """构建并验证图"""
        import networkx as nx
        graph = nx.DiGraph()

        # 添加节点
        for entity in entities:
            graph.add_node(entity['id'],
                          text=entity['text'],
                          type=entity['type'],
                          confidence=entity['confidence'])

        # 添加边
        for relation in relations:
            if relation['source'] in graph.nodes() and relation['target'] in graph.nodes():
                graph.add_edge(relation['source'],
                              relation['target'],
                              type=relation['type'],
                              confidence=relation['confidence'])

        # 验证图质量
        validation_result = self.graph_validator.validate_graph(graph)

        # 如果质量不佳，进行优化
        if not validation_result['is_valid']:
            graph = self.optimize_graph(graph, validation_result)

        return graph

    def optimize_graph(self, graph, validation_result):
        """优化图"""
        optimization_prompt = f"""
        基于验证结果优化以下图：

        验证结果：{validation_result}
        图结构：{list(graph.nodes())}, {list(graph.edges())}

        优化建议：
        """
        # 这里需要实际的图优化逻辑
        return graph

class EntityRecognizer:
    """实体识别器"""
    def recognize_entities(self, text_data):
        """识别实体"""
        # 简化的实体识别
        entities = [
            {'id': 'entity_1', 'text': '实体1', 'type': 'object', 'confidence': 0.9},
            {'id': 'entity_2', 'text': '实体2', 'type': 'concept', 'confidence': 0.8}
        ]
        return entities

class RelationExtractor:
    """关系提取器"""
    def extract_relations(self, text_data, entities, strategy='default'):
        """提取关系"""
        relations = [
            {'source': 'entity_1', 'target': 'entity_2', 'type': 'relates_to', 'confidence': 0.7}
        ]
        return relations

class GraphValidator:
    """图验证器"""
    def validate_graph(self, graph):
        """验证图"""
        # 简化的图验证
        validation_checks = {
            'has_nodes': len(graph.nodes()) > 0,
            'has_edges': len(graph.edges()) >= 0,
            'no_self_loops': not any(edge[0] == edge[1] for edge in graph.edges())
        }

        is_valid = all(validation_checks.values())
        return {
            'is_valid': is_valid,
            'checks': validation_checks
        }
```

**2. 遍历策略优化**

挑战：如何为特定问题选择最优的遍历策略

解决方案：
```python
class AdaptiveTraversalStrategy:
    """自适应遍历策略"""
    def __init__(self, llm):
        self.llm = llm
        self.strategy_optimizer = StrategyOptimizer()

    def select_optimal_strategy(self, graph, question, constraints=None):
        """选择最优策略"""
        # 1. 分析图特征
        graph_features = self.analyze_graph_features(graph)

        # 2. 分析问题特征
        problem_features = self.analyze_problem_features(question)

        # 3. 考虑约束条件
        constraint_features = self.analyze_constraints(constraints)

        # 4. 策略推荐
        strategy_recommendation = self.recommend_strategy(
            graph_features, problem_features, constraint_features
        )

        return strategy_recommendation

    def analyze_graph_features(self, graph):
        """分析图特征"""
        features = {
            'size': len(graph.nodes()),
            'density': len(graph.edges()) / max(len(graph.nodes()), 1),
            'max_depth': self.calculate_max_depth(graph),
            'branching_factor': self.calculate_avg_branching_factor(graph)
        }
        return features

    def calculate_max_depth(self, graph):
        """计算最大深度"""
        if not graph.nodes():
            return 0

        max_depth = 0
        for start_node in graph.nodes():
            visited = set()
            depth = self.calculate_depth_from_node(graph, start_node, visited, 0)
            max_depth = max(max_depth, depth)

        return max_depth

    def calculate_depth_from_node(self, graph, node, visited, depth):
        """从节点计算深度"""
        if node in visited or depth > 100:  # 防止无限递归
            return depth

        visited.add(node)
        max_child_depth = depth

        for successor in graph.successors(node):
            child_depth = self.calculate_depth_from_node(
                graph, successor, visited.copy(), depth + 1
            )
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def calculate_avg_branching_factor(self, graph):
        """计算平均分支因子"""
        if not graph.nodes():
            return 0

        branching_factors = [len(list(graph.successors(node))) for node in graph.nodes()]
        return sum(branching_factors) / len(branching_factors)

    def analyze_problem_features(self, question):
        """分析问题特征"""
        features = {
            'type': self.classify_question_type(question),
            'complexity': self.estimate_complexity(question),
            'goal_oriented': self.is_goal_oriented(question)
        }
        return features

    def classify_question_type(self, question):
        """分类问题类型"""
        if any(word in question for word in ['什么', 'what', '谁', 'who']):
            return 'factual'
        elif any(word in question for word in ['为什么', 'why', '原因']):
            return 'causal'
        elif any(word in question for word in ['怎么做', 'how', '方法']):
            return 'procedural'
        else:
            return 'analytical'

    def estimate_complexity(self, question):
        """估计复杂度"""
        # 基于问题长度和结构估计复杂度
        return len(question.split()) / 10  # 简化的复杂度估计

    def is_goal_oriented(self, question):
        """判断是否目标导向"""
        goal_indicators = ['目标', '目的', 'goal', 'aim', '找到', 'find']
        return any(indicator in question for indicator in goal_indicators)

    def analyze_constraints(self, constraints):
        """分析约束条件"""
        if not constraints:
            return {'time_limit': False, 'depth_limit': False, 'memory_limit': False}

        return {
            'time_limit': constraints.get('time_limit') is not None,
            'depth_limit': constraints.get('depth_limit') is not None,
            'memory_limit': constraints.get('memory_limit') is not None
        }

    def recommend_strategy(self, graph_features, problem_features, constraint_features):
        """推荐策略"""
        # 基于特征推荐策略
        if graph_features['size'] > 1000:
            return 'beam_search'
        elif problem_features['goal_oriented']:
            return 'best_first'
        elif graph_features['density'] > 0.5:
            return 'DFS'
        else:
            return 'BFS'

class StrategyOptimizer:
    """策略优化器"""
    def optimize_strategy(self, strategy, context):
        """优化策略"""
        # 简化的策略优化
        optimized_strategy = {
            'type': strategy,
            'parameters': self.get_optimized_parameters(strategy, context)
        }
        return optimized_strategy

    def get_optimized_parameters(self, strategy, context):
        """获取优化参数"""
        parameter_sets = {
            'BFS': {'max_depth': 10, 'visited_limit': 1000},
            'DFS': {'max_depth': 15, 'stack_limit': 500},
            'beam_search': {'beam_width': 5, 'max_depth': 8},
            'best_first': {'max_iterations': 100, 'heuristic_weight': 1.0}
        }
        return parameter_sets.get(strategy, {})
```

### 图提示的创新应用场景

**1. 智能问答系统**
```python
class IntelligentQAWithGraphPrompting:
    """基于图提示的智能问答系统"""
    def __init__(self, graph_system, knowledge_base):
        self.graph_system = graph_system
        self.knowledge_base = knowledge_base

    def answer_question(self, question, context=None):
        """回答问题"""
        # 1. 从知识库检索相关信息
        relevant_info = self.knowledge_base.retrieve_relevant_info(question)

        # 2. 构建知识图
        knowledge_graph = self.graph_system.graph_builder.build_advanced_graph(
            relevant_info, graph_type='knowledge'
        )

        # 3. 使用图提示推理
        result = self.graph_system.solve_complex_question(
            question, context, graph_type='knowledge'
        )

        return result['final_answer']

    def answer_complex_question(self, question_list):
        """回答复杂问题列表"""
        answers = []

        for question in question_list:
            answer = self.answer_question(question)
            answers.append({
                'question': question,
                'answer': answer
            })

        return answers
```

**2. 决策支持系统**
```python
class DecisionSupportWithGraphPrompting:
    """基于图提示的决策支持系统"""
    def __init__(self, graph_system):
        self.graph_system = graph_system
        self.decision_maker = DecisionMaker()

    def support_decision(self, decision_problem, options, criteria):
        """支持决策"""
        # 1. 构建决策图
        decision_graph = self.construct_decision_graph(
            decision_problem, options, criteria
        )

        # 2. 图推理分析
        analysis_result = self.graph_system.solve_complex_question(
            f"分析决策问题：{decision_problem}",
            graph_type='causal'
        )

        # 3. 生成决策建议
        decision_suggestion = self.decision_maker.make_decision(
            analysis_result, options, criteria
        )

        return decision_suggestion

    def construct_decision_graph(self, problem, options, criteria):
        """构建决策图"""
        import networkx as nx
        graph = nx.DiGraph()

        # 添加决策节点
        graph.add_node('decision_problem', text=problem, type='problem')
        for i, option in enumerate(options):
            graph.add_node(f'option_{i}', text=option, type='option')

        # 添加评估边
        for i, option in enumerate(options):
            for j, criterion in enumerate(criteria):
                graph.add_edge(f'option_{i}', f'criterion_{j}', type='evaluated_by')

        return graph

class DecisionMaker:
    """决策者"""
    def make_decision(self, analysis, options, criteria):
        """制定决策"""
        decision_prompt = f"""
        基于