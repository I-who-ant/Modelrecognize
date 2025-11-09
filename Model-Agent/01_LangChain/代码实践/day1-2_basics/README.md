# Day 1-2 基础示例

本目录包含LangChain入门的基础示例代码。

## 📁 文件说明

| 文件 | 说明 | 学习重点 |
|-----|------|---------|
| `01_hello_world.py` | 最基本的LLM调用 | 理解ChatModel初始化和invoke方法 |
| `02_chinese_llm.py` | 国产大模型测试 | 理解模型互换性 |
| `03_env_check.py` | 环境验证脚本 | 检查开发环境配置 |
| `.env.example` | 环境变量模板 | 配置API密钥 |

## 🚀 快速开始

### 1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件,填入你的API密钥
nano .env  # 或使用其他编辑器
```

### 2. 安装依赖

```bash
pip install langchain langchain-openai python-dotenv
```

### 3. 运行示例

```bash
# 环境检查
python 03_env_check.py

# Hello World
python 01_hello_world.py

# 多模型对比
python 02_chinese_llm.py
```

## 📚 学习顺序

建议按以下顺序学习:

1. **先运行**: `03_env_check.py` - 确保环境配置正确
2. **理解基础**: `01_hello_world.py` - 理解最基本的LLM调用
3. **扩展学习**: `02_chinese_llm.py` - 理解模型切换

## 💡 关键知识点

### 1. ChatModel初始化

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",     # 模型名称
    temperature=0.7,            # 随机性(0-1)
    max_tokens=500,             # 最大输出长度
    api_key="your-key"          # API密钥
)
```

### 2. 调用模型

```python
# 简单调用
response = llm.invoke("你的问题")

# 获取文本内容
text = response.content

# 获取元数据
metadata = response.response_metadata
```

### 3. 模型切换

LangChain的核心优势之一就是模型互换性:

```python
# OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

# DeepSeek(使用OpenAI兼容接口)
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1"
)
```

**只需修改初始化参数,业务代码完全不用改!**

## 🤔 常见问题

### Q1: ImportError: No module named 'langchain'

**解决**: 安装LangChain
```bash
pip install langchain langchain-openai
```

### Q2: API调用失败

**检查**:
1. API密钥是否正确
2. 网络连接是否正常
3. 是否需要代理

### Q3: 如何使用国产模型?

大多数国产模型都提供OpenAI兼容接口,可以使用`ChatOpenAI`类:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="模型名称",
    api_key="你的密钥",
    base_url="模型的API地址"
)
```

## 📖 扩展阅读

- [LangChain官方文档](https://docs.langchain.com/)
- [ChatOpenAI API文档](https://reference.langchain.com/python/langchain_openai/)
- [环境变量最佳实践](https://python.langchain.com/docs/guides/development/debugging)

## ✅ 学习检查清单

完成以下任务,确保你掌握了Day 1-2的内容:

- [ ] 成功运行环境检查脚本
- [ ] 理解ChatModel的初始化参数
- [ ] 成功调用至少1个LLM
- [ ] 理解响应对象的结构
- [ ] 尝试切换不同的模型
- [ ] 理解模型互换性的价值

---

**老王提示**: 这些示例都很简单,但是基础很重要!一定要亲自跑一遍,理解每一行代码的作用。别tm复制粘贴就完事了,要理解为什么这么写!💪