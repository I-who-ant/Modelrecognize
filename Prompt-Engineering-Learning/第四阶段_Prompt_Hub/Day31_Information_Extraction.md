# Day31: Information Extraction - 信息抽取提示词模板库

> **应用场景**: 实体抽取、关系抽取、事件抽取、数据结构化、知识图谱构建等

---

## 📝 场景概述

### 核心挑战
- 准确识别和抽取目标信息
- 处理模糊和歧义的表达
- 保持信息的完整性和准确性
- 结构化输出格式的一致性

### 技术要求
- 理解复杂的自然语言表达
- 识别实体边界和类型
- 提取实体间的关系
- 输出标准化的结构数据

---

## 🎯 快速模板库

### 模板1: 基础实体抽取 (NER)

```
任务: 从文本中抽取{实体类型}

文本:
{输入文本}

实体类型:
- {类型1}: {定义和示例}
- {类型2}: {定义和示例}
- {类型3}: {定义和示例}

输出格式:
{
  "{类型1}": [实体列表],
  "{类型2}": [实体列表],
  ...
}
```

**示例 - 新闻实体抽取**:
```
任务: 从新闻文本中抽取实体

文本:
"特斯拉CEO埃隆·马斯克周三在推特上宣布,公司将于2025年在上海建立新的超级工厂,
预计投资50亿美元,创造5000个就业岗位。"

实体类型:
- 人名(PERSON): 人物姓名
- 组织(ORGANIZATION): 公司、机构名称
- 地点(LOCATION): 地理位置
- 时间(TIME): 时间表达
- 金额(MONEY): 货币金额
- 数量(NUMBER): 数值信息

→ 输出:
{
  "PERSON": ["埃隆·马斯克"],
  "ORGANIZATION": ["特斯拉", "推特"],
  "LOCATION": ["上海"],
  "TIME": ["周三", "2025年"],
  "MONEY": ["50亿美元"],
  "NUMBER": ["5000个就业岗位"]
}

附加信息:
- 置信度: 高 (所有实体边界清晰)
- 歧义: "推特"可能是平台而非公司主体,但上下文中作为发布平台使用
```

---

### 模板2: 关系抽取 (Relation Extraction)

```
任务: 抽取文本中实体之间的关系

文本:
{输入文本}

目标关系类型:
- {关系1}: {主体类型} - {关系描述} - {客体类型}
- {关系2}: {主体类型} - {关系描述} - {客体类型}

输出格式:
[
  {
    "relation": "{关系类型}",
    "subject": "{主体}",
    "object": "{客体}",
    "evidence": "{支持该关系的原文片段}"
  },
  ...
]
```

**示例 - 人物关系抽取**:
```
任务: 抽取文本中的人物关系

文本:
"苹果公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩于1976年创立。
乔布斯担任CEO直到2011年,随后由蒂姆·库克接任。库克在2011年8月成为CEO,
并一直领导公司至今。"

目标关系类型:
- 创立者(FOUNDER_OF): 人物 - 创立 - 公司
- 任职(WORK_FOR): 人物 - 任职于 - 公司
- 职位(POSITION): 人物 - 担任 - 职位
- 继任(SUCCEED): 人物 - 接替 - 人物

→ 输出:
[
  {
    "relation": "FOUNDER_OF",
    "subject": "史蒂夫·乔布斯",
    "object": "苹果公司",
    "evidence": "苹果公司由史蒂夫·乔布斯...于1976年创立"
  },
  {
    "relation": "FOUNDER_OF",
    "subject": "史蒂夫·沃兹尼亚克",
    "object": "苹果公司",
    "evidence": "苹果公司由...史蒂夫·沃兹尼亚克...于1976年创立"
  },
  {
    "relation": "FOUNDER_OF",
    "subject": "罗纳德·韦恩",
    "object": "苹果公司",
    "evidence": "苹果公司由...罗纳德·韦恩于1976年创立"
  },
  {
    "relation": "POSITION",
    "subject": "史蒂夫·乔布斯",
    "object": "CEO",
    "evidence": "乔布斯担任CEO直到2011年",
    "time": "?-2011"
  },
  {
    "relation": "POSITION",
    "subject": "蒂姆·库克",
    "object": "CEO",
    "evidence": "库克在2011年8月成为CEO",
    "time": "2011年8月-至今"
  },
  {
    "relation": "SUCCEED",
    "subject": "蒂姆·库克",
    "object": "史蒂夫·乔布斯",
    "evidence": "随后由蒂姆·库克接任",
    "context": "CEO职位"
  }
]

知识图谱三元组:
(史蒂夫·乔布斯, 创立, 苹果公司)
(史蒂夫·沃兹尼亚克, 创立, 苹果公司)
(罗纳德·韦恩, 创立, 苹果公司)
(史蒂夫·乔布斯, 担任, CEO)
(蒂姆·库克, 担任, CEO)
(蒂姆·库克, 接替, 史蒂夫·乔布斯)
```

---

### 模板3: 事件抽取 (Event Extraction)

```
任务: 抽取文本中的事件信息

文本:
{输入文本}

事件模板:
- 事件类型: {类型名称}
- 触发词: {标志性词汇}
- 事件要素:
  * {要素1}: {说明}
  * {要素2}: {说明}
  * ...

输出每个事件的:
- 事件类型
- 触发词
- 各要素的值
- 时间
- 地点
```

**示例 - 并购事件抽取**:
```
任务: 抽取企业并购事件

文本:
"2023年10月13日,微软公司宣布以687亿美元的价格收购动视暴雪,
交易预计将在2024年第二季度完成。这是微软历史上最大的一笔收购,
也是游戏行业最大的并购案。微软CEO萨提亚·纳德拉表示,
此次收购将加强微软在游戏领域的地位。"

事件模板:
- 事件类型: 企业并购(ACQUISITION)
- 触发词: "收购"、"并购"、"买下"
- 事件要素:
  * 收购方(Acquirer): 发起收购的公司
  * 被收购方(Target): 被收购的公司
  * 交易金额(Amount): 收购价格
  * 宣布时间(Announce_Time): 宣布日期
  * 完成时间(Complete_Time): 预计/实际完成时间
  * 发言人(Spokesperson): 相关发言人
  * 收购目的(Purpose): 收购原因/目标

→ 输出:
{
  "event_type": "ACQUISITION",
  "trigger": "收购",
  "arguments": {
    "Acquirer": "微软公司",
    "Target": "动视暴雪",
    "Amount": "687亿美元",
    "Announce_Time": "2023年10月13日",
    "Complete_Time": "2024年第二季度(预计)",
    "Spokesperson": "萨提亚·纳德拉(微软CEO)",
    "Purpose": "加强微软在游戏领域的地位"
  },
  "context": {
    "significance": [
      "微软历史上最大的一笔收购",
      "游戏行业最大的并购案"
    ]
  },
  "evidence": {
    "Acquirer": "微软公司宣布...",
    "Target": "...收购动视暴雪",
    "Amount": "以687亿美元的价格收购...",
    "Announce_Time": "2023年10月13日,微软公司宣布...",
    "Complete_Time": "交易预计将在2024年第二季度完成",
    "Spokesperson": "微软CEO萨提亚·纳德拉表示...",
    "Purpose": "此次收购将加强微软在游戏领域的地位"
  }
}

时间线:
- 2023-10-13: 宣布收购
- 2024-Q2: 预计完成

补充推理:
- 交易状态: 进行中(已宣布,未完成)
- 行业: 游戏/科技
- 影响: 行业格局重塑
```

---

### 模板4: 表格/列表抽取

```
任务: 将文本中的信息转换为结构化表格

文本:
{包含列表或表格信息的文本}

目标表格结构:
列名: [{列1}, {列2}, {列3}, ...]

请抽取数据并填充到表格中,如果某个字段缺失,标注为"N/A"。

输出格式: JSON或Markdown表格
```

**示例 - 产品信息表格化**:
```
任务: 将产品描述转换为对比表格

文本:
"我们有三款手机:
iPhone 15 Pro配备A17 Pro芯片,6.1英寸显示屏,售价7999元,提供128GB/256GB/512GB存储。
Galaxy S23搭载骁龙8 Gen 2,6.1英寸AMOLED屏幕,起售价5999元,有128GB和256GB版本。
小米14使用骁龙8 Gen 3处理器,6.36英寸屏幕,价格3999元起,提供8GB+256GB和12GB+512GB配置。"

目标表格结构:
列名: [产品名称, 处理器, 屏幕尺寸, 起售价, 存储选项]

→ 输出 (Markdown格式):

| 产品名称 | 处理器 | 屏幕尺寸 | 起售价 | 存储选项 |
|---------|--------|---------|--------|----------|
| iPhone 15 Pro | A17 Pro | 6.1英寸 | 7999元 | 128GB / 256GB / 512GB |
| Galaxy S23 | 骁龙8 Gen 2 | 6.1英寸 | 5999元 | 128GB / 256GB |
| 小米14 | 骁龙8 Gen 3 | 6.36英寸 | 3999元 | 8GB+256GB / 12GB+512GB |

→ 输出 (JSON格式):
```json
{
  "products": [
    {
      "name": "iPhone 15 Pro",
      "processor": "A17 Pro",
      "screen_size": "6.1英寸",
      "starting_price": 7999,
      "price_currency": "CNY",
      "storage_options": ["128GB", "256GB", "512GB"]
    },
    {
      "name": "Galaxy S23",
      "processor": "骁龙8 Gen 2",
      "screen_size": "6.1英寸",
      "starting_price": 5999,
      "price_currency": "CNY",
      "storage_options": ["128GB", "256GB"]
    },
    {
      "name": "小米14",
      "processor": "骁龙8 Gen 3",
      "screen_size": "6.36英寸",
      "starting_price": 3999,
      "price_currency": "CNY",
      "storage_options": ["8GB+256GB", "12GB+512GB"]
    }
  ]
}
```

数据归一化:
- 价格单位统一为人民币元(CNY)
- 屏幕尺寸统一为英寸
- 存储选项标准化为数组格式

数据质量:
- 完整性: 100% (所有字段都有值)
- 一致性: 高 (格式统一)
- 准确性: 高 (直接从原文抽取)
```

---

### 模板5: 属性抽取 (Attribute Extraction)

```
任务: 抽取实体的属性信息

实体: {实体名称}
文本: {包含该实体的文本}

目标属性:
- {属性1}: {定义}
- {属性2}: {定义}
- ...

输出格式:
{
  "entity": "{实体名}",
  "attributes": {
    "{属性1}": "{值}",
    "{属性2}": "{值}",
    ...
  },
  "confidence": "{高/中/低}"
}
```

**示例 - 电影属性抽取**:
```
任务: 抽取电影的属性信息

实体: 《肖申克的救赎》
文本:
"《肖申克的救赎》是由弗兰克·达拉邦特执导,蒂姆·罗宾斯和摩根·弗里曼主演的剧情片。
电影于1994年9月23日在美国上映,改编自斯蒂芬·金的小说《丽塔·海华丝和肖申克的救赎》。
影片时长142分钟,制作成本2500万美元,全球票房2870万美元。
尽管票房平平,但后来成为影史经典,在IMDb评分9.3分,位列第一。"

目标属性:
- 导演(Director)
- 主演(Cast)
- 类型(Genre)
- 上映日期(Release_Date)
- 片长(Runtime)
- 预算(Budget)
- 票房(Box_Office)
- 原著(Source)
- 评分(Rating)

→ 输出:
```json
{
  "entity": "肖申克的救赎",
  "entity_type": "MOVIE",
  "attributes": {
    "title": {
      "zh": "肖申克的救赎",
      "en": "The Shawshank Redemption"
    },
    "director": ["弗兰克·达拉邦特"],
    "cast": ["蒂姆·罗宾斯", "摩根·弗里曼"],
    "genre": ["剧情"],
    "release_date": "1994-09-23",
    "release_location": "美国",
    "runtime": "142分钟",
    "runtime_minutes": 142,
    "budget": {
      "amount": 25000000,
      "currency": "USD",
      "display": "2500万美元"
    },
    "box_office": {
      "amount": 28700000,
      "currency": "USD",
      "scope": "全球",
      "display": "2870万美元"
    },
    "source": {
      "type": "小说改编",
      "title": "丽塔·海华丝和肖申克的救赎",
      "author": "斯蒂芬·金"
    },
    "rating": {
      "platform": "IMDb",
      "score": 9.3,
      "rank": 1
    }
  },
  "extracted_facts": [
    "票房平平但后来成为影史经典",
    "IMDb排名第一"
  ],
  "confidence": "高",
  "data_quality": {
    "completeness": "95%",
    "notes": "未提及制片国家(可推断为美国)"
  }
}
```

属性来源映射:
- director ← "由弗兰克·达拉邦特执导"
- cast ← "蒂姆·罗宾斯和摩根·弗里曼主演"
- genre ← "剧情片"
- release_date ← "1994年9月23日在美国上映"
- runtime ← "影片时长142分钟"
- budget ← "制作成本2500万美元"
- box_office ← "全球票房2870万美元"
- source ← "改编自斯蒂芬·金的小说..."
- rating ← "在IMDb评分9.3分,位列第一"
```

---

### 模板6: CoT信息抽取 (复杂推理)

```
任务: 通过推理抽取隐含信息

文本:
{包含隐含信息的文本}

请按以下步骤:

步骤1: 识别明确信息
- 直接陈述的事实

步骤2: 推理隐含信息
- 基于上下文的推断
- 领域知识的应用

步骤3: 验证推理
- 检查逻辑一致性
- 标注置信度

步骤4: 结构化输出
- 区分显式和隐式信息
```

**示例 - 招聘信息抽取**:
```
任务: 从职位描述中抽取详细信息

文本:
"我们是一家快速成长的AI初创公司,寻找资深后端工程师加入我们的核心团队。
你将负责设计和实现高并发微服务架构,与产品和算法团队紧密合作。
我们使用Go和Python,部署在AWS上,希望你有5年以上经验,
熟悉Kubernetes和分布式系统。我们提供有竞争力的薪资(可达年薪50-80万)、
股权期权,以及弹性工作制。办公地点在北京中关村。"

步骤1: 识别明确信息

显式信息:
- 职位: 资深后端工程师
- 公司类型: AI初创公司
- 公司状态: 快速成长
- 工作内容: 设计和实现高并发微服务架构,与产品和算法团队合作
- 技术栈: Go, Python, AWS, Kubernetes
- 经验要求: 5年以上
- 薪资范围: 50-80万年薪
- 福利: 股权期权、弹性工作制
- 工作地点: 北京中关村

步骤2: 推理隐含信息

隐含信息推理:
1. 团队规模: "核心团队" → 推测小团队(10-30人)
   置信度: 中
   依据: 初创公司 + "核心团队"表述

2. 技术栈深度: Go和Python并用 → Go做高性能服务,Python做算法接口
   置信度: 高
   依据: AI公司 + 高并发需求 + 算法团队

3. 云基础设施: AWS + Kubernetes → 容器化微服务架构,可能有DevOps职责
   置信度: 高
   依据: 现代技术栈标配

4. 融资阶段: 50-80万薪资 + 股权 → 可能B轮或C轮
   置信度: 中
   依据: 能给高薪+股权,说明有融资但还需用股权吸引人

5. 工作强度: "快速成长" + "弹性工作" → 工作强度大但有一定自由度
   置信度: 中
   依据: 初创公司特点

6. 级别: "资深" + 5年经验 + "核心团队" → 可能对应P6-P7级别(对标大厂)
   置信度: 高

7. 发展前景: "核心团队" → 有技术决策权,成长空间大
   置信度: 高

步骤3: 验证推理

一致性检查:
✅ 薪资与经验要求匹配(5年资深给50-80万合理)
✅ 技术栈与AI公司定位一致
✅ 地点(中关村)与AI公司聚集地吻合
✅ 股权+高薪组合符合初创公司竞争策略

步骤4: 结构化输出

```json
{
  "job_posting": {
    "explicit_info": {
      "position": {
        "title": "资深后端工程师",
        "level": "资深",
        "team": "核心团队"
      },
      "company": {
        "industry": "AI",
        "type": "初创公司",
        "stage": "快速成长"
      },
      "responsibilities": [
        "设计高并发微服务架构",
        "实现微服务架构",
        "与产品团队合作",
        "与算法团队合作"
      ],
      "requirements": {
        "experience": "5年以上",
        "tech_stack": ["Go", "Python", "AWS", "Kubernetes"],
        "skills": ["分布式系统", "微服务架构", "高并发"]
      },
      "compensation": {
        "salary": {
          "min": 500000,
          "max": 800000,
          "currency": "CNY",
          "period": "年"
        },
        "equity": true,
        "benefits": ["股权期权", "弹性工作制"]
      },
      "location": {
        "city": "北京",
        "district": "中关村"
      }
    },
    "inferred_info": {
      "team_size": {
        "estimate": "10-30人",
        "confidence": "中",
        "reasoning": "初创公司 + 核心团队表述"
      },
      "funding_stage": {
        "estimate": "B轮-C轮",
        "confidence": "中",
        "reasoning": "高薪资+股权组合,说明有融资但还需股权激励"
      },
      "work_intensity": {
        "estimate": "高强度但有弹性",
        "confidence": "中",
        "reasoning": "快速成长阶段 + 明确弹性工作制"
      },
      "career_growth": {
        "estimate": "高",
        "confidence": "高",
        "reasoning": "核心团队 + 技术决策权"
      },
      "level_mapping": {
        "estimate": "P6-P7 (对标阿里/字节)",
        "confidence": "高",
        "reasoning": "5年经验 + 资深 + 50-80万薪资"
      },
      "architecture_pattern": {
        "estimate": "云原生微服务",
        "confidence": "高",
        "reasoning": "AWS + Kubernetes + 微服务明确提及"
      }
    },
    "missing_info": [
      "具体业务方向(AI的哪个领域)",
      "团队总人数",
      "公司成立时间",
      "是否需要算法背景",
      "On-call要求",
      "远程办公政策"
    ],
    "red_flags": [],
    "green_flags": [
      "明确薪资范围(透明度高)",
      "核心团队(决策权)",
      "现代技术栈(不过时)",
      "弹性工作(work-life balance)"
    ]
  }
}
```

综合评估:
- 信息完整度: 75% (核心信息齐全,细节略有缺失)
- 吸引力: 高 (高薪+股权+核心团队+现代技术栈)
- 建议行动: 值得投递简历,面试时重点确认业务方向和团队氛围
```

---

### 模板7: 多文档信息聚合

```
任务: 从多个文档中聚合信息

文档列表:
- 文档1: {内容}
- 文档2: {内容}
- 文档3: {内容}

聚合目标:
- 合并相同信息
- 解决冲突
- 补充缺失
- 交叉验证

输出:
- 聚合后的结构化信息
- 信息来源标注
- 冲突解决说明
```

**示例 - 人物信息聚合**:
```
任务: 聚合多个来源的人物信息

文档1 (维基百科):
"埃隆·马斯克(Elon Musk,1971年6月28日-),出生于南非比勒陀利亚,
企业家、工程师、慈善家。现任特斯拉CEO、SpaceX CEO兼CTO、推特CEO。"

文档2 (福布斯):
"埃隆·马斯克,2024年身家2500亿美元,全球首富。特斯拉和SpaceX创始人。
1971年生于南非,后移民加拿大再到美国。"

文档3 (公司官网):
"Elon Musk, CEO and Product Architect of Tesla.
Founded in 2003, Tesla's mission is to accelerate the world's
transition to sustainable energy."

聚合目标:
- 合并基本信息
- 解决职位冲突
- 补充缺失信息
- 验证准确性

→ 输出:
```json
{
  "person": {
    "name": {
      "en": "Elon Musk",
      "zh": "埃隆·马斯克",
      "sources": ["文档1", "文档2"]
    },
    "birth": {
      "date": "1971-06-28",
      "place": "南非比勒陀利亚",
      "sources": ["文档1", "文档2"],
      "confidence": "高",
      "note": "两个来源一致"
    },
    "nationality": {
      "birth": "南非",
      "current": "美国",
      "history": ["南非", "加拿大", "美国"],
      "sources": ["文档2"],
      "confidence": "高"
    },
    "occupation": {
      "primary": ["企业家", "工程师"],
      "sources": ["文档1"]
    },
    "positions": [
      {
        "company": "特斯拉(Tesla)",
        "titles": ["CEO", "Product Architect"],
        "sources": ["文档1", "文档3"],
        "confidence": "高",
        "note": "多来源确认"
      },
      {
        "company": "SpaceX",
        "titles": ["CEO", "CTO"],
        "sources": ["文档1", "文档2"],
        "confidence": "高"
      },
      {
        "company": "推特(Twitter)",
        "titles": ["CEO"],
        "sources": ["文档1"],
        "confidence": "中",
        "note": "仅一个来源,且推特被改名为X,信息可能过时"
      }
    },
    "founder_of": [
      {
        "company": "特斯拉",
        "year": 2003,
        "sources": ["文档3"],
        "note": "文档3说founded in 2003,但有争议(实际是2003年由他人创立,马斯克2004年投资加入)"
      },
      {
        "company": "SpaceX",
        "sources": ["文档2"],
        "confidence": "高"
      }
    ],
    "wealth": {
      "net_worth": 250000000000,
      "currency": "USD",
      "year": 2024,
      "rank": 1,
      "rank_scope": "全球",
      "sources": ["文档2"]
    }
  },
  "conflicts_resolved": [
    {
      "field": "特斯拉创始人身份",
      "conflict": "文档2说'创始人',但历史记录显示是早期投资人",
      "resolution": "标注为早期投资人和实际领导者,而非技术上的创始人",
      "confidence": "中"
    },
    {
      "field": "推特CEO职位",
      "conflict": "文档1提到推特CEO,但推特已改名为X,且马斯克职位可能有变化",
      "resolution": "保留信息但标注可能过时",
      "confidence": "中"
    }
  ],
  "missing_info": [
    "教育背景",
    "家庭信息",
    "其他投资和公司(如Neuralink, Boring Company)",
    "慈善活动(文档1提到但未详述)"
  ],
  "data_quality": {
    "completeness": "60%",
    "consistency": "80%",
    "timeliness": "部分信息可能过时(推特改名X)",
    "reliability": "高(多来源交叉验证)"
  },
  "update_needed": [
    "推特/X的最新职位",
    "2024最新身家数据",
    "补充其他公司信息"
  ]
}
```

聚合统计:
- 来源数量: 3个
- 信息字段: 15个
- 交叉验证字段: 5个(姓名、生日、特斯拉CEO、SpaceX CEO等)
- 冲突字段: 2个(特斯拉创始人、推特职位)
- 唯一来源字段: 8个(需进一步验证)

推荐下一步:
1. 查找更多权威来源补充教育和家庭信息
2. 确认推特/X的最新职位状态
3. 澄清特斯拉创始人vs早期投资人的表述
```

---

### 模板8: Schema-Guided抽取

```
任务: 按照预定义Schema抽取信息

Schema定义:
{JSON Schema或数据模型定义}

文本:
{输入文本}

请严格按照Schema输出,必填字段不能为空,
选填字段如果没有信息则设为null。

验证:
- 字段类型正确
- 必填字段存在
- 枚举值合法
```

**示例 - 电商产品信息抽取**:
```
任务: 按照产品Schema抽取商品信息

Schema定义:
```json
{
  "type": "object",
  "required": ["name", "category", "price"],
  "properties": {
    "name": {"type": "string"},
    "brand": {"type": "string"},
    "category": {
      "type": "string",
      "enum": ["电子产品", "服装", "食品", "图书", "其他"]
    },
    "price": {
      "type": "object",
      "required": ["amount", "currency"],
      "properties": {
        "amount": {"type": "number", "minimum": 0},
        "currency": {"type": "string", "enum": ["CNY", "USD", "EUR"]}
      }
    },
    "specifications": {
      "type": "object",
      "additionalProperties": {"type": "string"}
    },
    "ratings": {
      "type": "object",
      "properties": {
        "average": {"type": "number", "minimum": 0, "maximum": 5},
        "count": {"type": "integer", "minimum": 0}
      }
    },
    "stock": {"type": "integer", "minimum": 0},
    "description": {"type": "string"}
  }
}
```

文本:
"苹果iPhone 15 Pro,搭载A17 Pro芯片,6.1英寸超视网膜XDR显示屏,
钛金属设计。售价7999元起,提供128GB/256GB/512GB/1TB存储选项。
用户评分4.8分(基于1523条评论),现货充足。"

→ 输出:
```json
{
  "name": "iPhone 15 Pro",
  "brand": "苹果",
  "category": "电子产品",
  "price": {
    "amount": 7999,
    "currency": "CNY",
    "note": "起售价,不同存储版本价格不同"
  },
  "specifications": {
    "处理器": "A17 Pro芯片",
    "屏幕": "6.1英寸超视网膜XDR显示屏",
    "材质": "钛金属",
    "存储选项": "128GB / 256GB / 512GB / 1TB"
  },
  "ratings": {
    "average": 4.8,
    "count": 1523
  },
  "stock": null,
  "stock_status": "现货充足",
  "description": "搭载A17 Pro芯片,6.1英寸超视网膜XDR显示屏,钛金属设计"
}
```

Schema验证:
✅ 必填字段完整 (name, category, price都有值)
✅ 字段类型正确 (price.amount是number, ratings.count是integer)
✅ 枚举值合法 (category="电子产品"在允许值中)
✅ 数值范围合法 (ratings.average=4.8在0-5之间)
⚠️ stock字段为null (文本只说"现货充足",无具体数量)

数据完整性: 90% (仅stock字段缺失具体数值)
```

---

## 💡 最佳实践

### 1. 选择合适的模板

```
简单实体识别:
└─ 使用模板1: 基础NER

关系图谱构建:
└─ 使用模板2: 关系抽取

复杂事件提取:
└─ 使用模板3: 事件抽取

非结构化转结构化:
└─ 使用模板4: 表格抽取

属性补全:
└─ 使用模板5: 属性抽取

需要推理:
└─ 使用模板6: CoT抽取

多源整合:
└─ 使用模板7: 信息聚合

标准化输出:
└─ 使用模板8: Schema-Guided
```

### 2. 提升抽取质量技巧

**明确定义**:
1. 给出实体类型的清晰定义和边界
2. 提供正例和反例
3. 说明模糊情况的处理规则

**结构化输出**:
1. 使用JSON等标准格式
2. 定义清晰的Schema
3. 包含置信度和来源信息

**质量控制**:
1. 交叉验证多个来源
2. 标注歧义和冲突
3. 提供证据支持

---

## 🔧 技术融合

### 结合前置技术

```
Day7: Few-Shot
└─ 提供抽取示例引导模型学习模式

Day8: CoT
└─ 复杂信息通过推理抽取

Day10: Generate Knowledge
└─ 先生成领域知识辅助抽取

Day13: RAG
└─ 检索相关文档辅助信息聚合
```

---

## ⚠️ 常见陷阱

### 陷阱1: 实体边界不清

```
❌ 错误:
文本:"苹果公司CEO"
抽取: ["苹果公司CEO"]

✅ 正确:
明确边界规则:
- 组织: "苹果公司"
- 职位: "CEO"
```

### 陷阱2: 忽略上下文

```
❌ 错误:
文本:"他去了银行"
抽取: 地点="银行"(金融机构)

✅ 正确:
考虑上下文:
"他去了银行存钱" → 金融机构
"他坐在河边的银行上" → 河岸
```

---

## 📚 参考资源

**官方资源**:
- Prompt Engineering Guide: Information Extraction
- OpenAI Cookbook: NER Examples

**扩展阅读**:
- 命名实体识别(NER)最佳实践
- 关系抽取和知识图谱构建
- Schema设计方法论

---

**下一步**: Day32 - Image Generation (图像生成提示词)
