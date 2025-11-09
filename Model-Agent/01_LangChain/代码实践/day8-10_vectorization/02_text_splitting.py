"""
文本切割策略完整示例

学习目标:
1. 掌握不同切割器的使用
2. 理解chunk_size和overlap的影响
3. 学会针对不同场景选择切割策略
"""
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def demo_basic_splitting():
    """基础文本切割"""
    print("=" * 60)
    print("1. CharacterTextSplitter - 基础字符切割")
    print("=" * 60)

    from langchain.text_splitter import CharacterTextSplitter

    text = """LangChain是一个用于开发大语言模型应用的框架。

它提供了多个核心组件:模型I/O、数据连接、链、代理和内存。

通过LangChain,开发者可以快速构建复杂的LLM应用,如问答系统、聊天机器人等。

框架支持多种大语言模型,包括OpenAI、Anthropic等。"""

    # 基础切割
    splitter = CharacterTextSplitter(
        separator="\n\n",      # 按段落分隔
        chunk_size=100,        # 每块最大100字符
        chunk_overlap=20,      # 重叠20字符
        length_function=len    # 使用len计算长度
    )

    chunks = splitter.split_text(text)

    print(f"\n原文长度: {len(text)} 字符")
    print(f"切割后块数: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n块 {i+1} (长度: {len(chunk)}):")
        print(f"{chunk}")


def demo_recursive_splitting():
    """递归字符切割(推荐)"""
    print("\n" + "=" * 60)
    print("2. RecursiveCharacterTextSplitter - 递归切割(推荐)")
    print("=" * 60)

    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text = """# LangChain教程

## 什么是LangChain?

LangChain是一个强大的框架。它有以下特点:
1. 模块化设计
2. 易于使用
3. 功能丰富

## 核心组件

LangChain包含多个核心组件,每个组件负责不同的功能。

### 模型I/O
负责与语言模型的交互。

### 数据连接
处理外部数据源。"""

    # 递归切割
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        # 分隔符优先级:从粗到细
        separators=[
            "\n\n",  # 段落
            "\n",    # 行
            "。",    # 中文句号
            "!",     # 感叹号
            "?",     # 问号
            "，",    # 中文逗号
            " ",     # 空格
            ""       # 字符
        ]
    )

    chunks = splitter.split_text(text)

    print(f"\n原文长度: {len(text)} 字符")
    print(f"切割后块数: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n块 {i+1} (长度: {len(chunk)}):")
        print(f"'{chunk}'")

    print("\n✅ RecursiveCharacterTextSplitter优势:")
    print("  - 优先使用大分隔符(保持语义完整)")
    print("  - 大分隔符不够用时,递归使用小分隔符")
    print("  - 适合绝大多数场景")


def demo_chunk_size_impact():
    """chunk_size和overlap的影响"""
    print("\n" + "=" * 60)
    print("3. chunk_size和overlap参数影响")
    print("=" * 60)

    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text = "Python是一门编程语言。" * 50  # 重复50次

    print("\n场景1: 小chunk_size,无overlap")
    splitter1 = RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=0
    )
    chunks1 = splitter1.split_text(text)
    print(f"  块数: {len(chunks1)}")
    print(f"  每块平均长度: {sum(len(c) for c in chunks1) / len(chunks1):.1f}")

    print("\n场景2: 小chunk_size,有overlap")
    splitter2 = RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=10
    )
    chunks2 = splitter2.split_text(text)
    print(f"  块数: {len(chunks2)}")
    print(f"  每块平均长度: {sum(len(c) for c in chunks2) / len(chunks2):.1f}")

    print("\n场景3: 大chunk_size,有overlap")
    splitter3 = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    chunks3 = splitter3.split_text(text)
    print(f"  块数: {len(chunks3)}")
    print(f"  每块平均长度: {sum(len(c) for c in chunks3) / len(chunks3):.1f}")

    print("\n✅ 参数选择建议:")
    print("  chunk_size:")
    print("    - 短问答: 200-500字符")
    print("    - 长文本理解: 500-1000字符")
    print("    - 代码文档: 1000-2000字符")
    print("  chunk_overlap:")
    print("    - 推荐10-20%的chunk_size")
    print("    - 保证上下文连贯性")
    print("    - 避免重要信息被切断")


def demo_split_documents():
    """切割Document对象"""
    print("\n" + "=" * 60)
    print("4. 切割Document对象")
    print("=" * 60)

    from langchain_core.documents import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # 创建Document
    docs = [
        Document(
            page_content="Python是一门简洁优雅的编程语言。" * 20,
            metadata={"source": "doc1.txt", "page": 1}
        ),
        Document(
            page_content="JavaScript主要用于Web开发。" * 15,
            metadata={"source": "doc2.txt", "page": 2}
        )
    ]

    # 切割Document
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    split_docs = splitter.split_documents(docs)

    print(f"\n原始文档数: {len(docs)}")
    print(f"切割后文档数: {len(split_docs)}")

    print("\n切割后的Document:")
    for i, doc in enumerate(split_docs[:3]):  # 只显示前3个
        print(f"\n文档 {i+1}:")
        print(f"  内容: {doc.page_content[:50]}...")
        print(f"  元数据: {doc.metadata}")

    print("\n✅ 关键点:")
    print("  - 元数据会被保留")
    print("  - 每个块都是独立的Document")
    print("  - 适合后续向量化处理")


def demo_token_splitter():
    """按Token切割"""
    print("\n" + "=" * 60)
    print("5. TokenTextSplitter - 按Token切割")
    print("=" * 60)

    try:
        import tiktoken
        from langchain.text_splitter import TokenTextSplitter

        text = "LangChain是一个用于开发大语言模型应用的框架。" * 30

        # 按Token切割
        splitter = TokenTextSplitter(
            encoding_name="cl100k_base",  # GPT-3.5/4的编码
            chunk_size=100,               # 100个token
            chunk_overlap=20              # 重叠20个token
        )

        chunks = splitter.split_text(text)

        print(f"\n原文长度: {len(text)} 字符")
        print(f"切割后块数: {len(chunks)}")

        # 验证Token数
        enc = tiktoken.get_encoding("cl100k_base")
        for i, chunk in enumerate(chunks[:3]):
            token_count = len(enc.encode(chunk))
            print(f"\n块 {i+1}:")
            print(f"  字符数: {len(chunk)}")
            print(f"  Token数: {token_count}")

        print("\n✅ 使用场景:")
        print("  - 需要精确控制Token数")
        print("  - 计算LLM成本")
        print("  - 避免超过模型限制")

    except ImportError:
        print("\n⚠️ tiktoken未安装，请运行: pip install tiktoken")


def demo_markdown_splitter():
    """Markdown文档切割"""
    print("\n" + "=" * 60)
    print("6. MarkdownTextSplitter - 保留Markdown结构")
    print("=" * 60)

    from langchain.text_splitter import MarkdownTextSplitter

    markdown_text = """# LangChain框架

## 核心概念

LangChain是一个强大的框架。

### 模型I/O

负责与语言模型交互。

### 数据连接

处理外部数据源:
- 文档加载
- 文本切割
- 向量存储

## 使用示例

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
response = llm.invoke("Hello")
```

## 总结

LangChain简化了LLM应用开发。"""

    splitter = MarkdownTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    chunks = splitter.split_text(markdown_text)

    print(f"\n切割后块数: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n块 {i+1}:")
        print(f"{chunk}")
        print("-" * 40)

    print("\n✅ Markdown切割优势:")
    print("  - 保留标题层级结构")
    print("  - 保留代码块完整性")
    print("  - 保留列表结构")


def demo_code_splitter():
    """代码文档切割"""
    print("\n" + "=" * 60)
    print("7. PythonCodeTextSplitter - Python代码切割")
    print("=" * 60)

    from langchain.text_splitter import PythonCodeTextSplitter

    python_code = """
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

    def is_adult(self):
        return self.age >= 18


def create_user(name, age):
    user = User(name, age)
    return user


def main():
    user = create_user("Alice", 25)
    print(user.greet())
    print(f"Is adult: {user.is_adult()}")


if __name__ == "__main__":
    main()
"""

    splitter = PythonCodeTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    chunks = splitter.split_text(python_code)

    print(f"\n切割后块数: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        print(f"\n块 {i+1}:")
        print(f"{chunk}")
        print("-" * 40)

    print("\n✅ 代码切割特点:")
    print("  - 保留函数/类的完整性")
    print("  - 按代码逻辑切割")
    print("  - 支持多种语言(Python/JS/Java等)")


def demo_best_practices():
    """切割最佳实践"""
    print("\n" + "=" * 60)
    print("8. 切割策略最佳实践")
    print("=" * 60)

    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document

    print("\n场景1: 技术文档切割")
    print("-" * 40)
    tech_doc = """# API文档

## 用户认证

POST /api/auth/login

请求参数:
- username: 用户名
- password: 密码

返回结果:
- token: 访问令牌
- expires: 过期时间"""

    tech_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
    )

    chunks = tech_splitter.split_text(tech_doc)
    print(f"  技术文档切割为 {len(chunks)} 块")

    print("\n场景2: 问答数据切割")
    print("-" * 40)
    qa_text = """问:什么是LangChain?
答:LangChain是一个用于开发大语言模型应用的框架。

问:如何安装LangChain?
答:使用pip install langchain即可安装。

问:LangChain有哪些核心组件?
答:包括模型I/O、数据连接、链、代理和内存。"""

    qa_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=0,  # QA不需要overlap
        separators=["\n\n", "\n", ""]
    )

    chunks = qa_splitter.split_text(qa_text)
    print(f"  问答数据切割为 {len(chunks)} 块")

    print("\n场景3: 长文章切割")
    print("-" * 40)
    article = "这是一篇长文章。" * 100

    article_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,  # 10%的overlap
        separators=["。\n", "。", "!", "?", "，", " ", ""]
    )

    chunks = article_splitter.split_text(article)
    print(f"  长文章切割为 {len(chunks)} 块")

    print("\n✅ 最佳实践总结:")
    print("""
1. 通用场景:
   - 使用RecursiveCharacterTextSplitter
   - chunk_size: 500
   - chunk_overlap: 50

2. 技术文档:
   - 保留标题结构
   - chunk_size: 300-500
   - 自定义separators优先标题

3. 问答数据:
   - chunk_size: 200-300
   - chunk_overlap: 0(每个QA独立)
   - 按问答对切割

4. 代码文档:
   - 使用PythonCodeTextSplitter
   - chunk_size: 1000-2000
   - 保留函数完整性

5. Markdown:
   - 使用MarkdownTextSplitter
   - 保留标题层级
   - chunk_size: 500

6. 实验调优:
   - 没有万能参数
   - 根据检索效果调整
   - 监控Token消耗
   - 平衡精度和成本
    """)


if __name__ == "__main__":
    print("✂️ LangChain Text Splitters 完整示例\n")

    # 运行所有示例
    demo_basic_splitting()
    demo_recursive_splitting()
    demo_chunk_size_impact()
    demo_split_documents()
    demo_token_splitter()
    demo_markdown_splitter()
    demo_code_splitter()
    demo_best_practices()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 为什么切割:
   - Embedding模型有长度限制
   - 提高检索精度
   - 控制成本

2. 切割器选择:
   ✅ RecursiveCharacterTextSplitter (推荐,通用)
   ✅ TokenTextSplitter (精确控制Token)
   ✅ MarkdownTextSplitter (Markdown文档)
   ✅ PythonCodeTextSplitter (代码文档)

3. 关键参数:
   - chunk_size: 块大小(200-1000字符)
   - chunk_overlap: 重叠(10-20%的chunk_size)
   - separators: 分隔符优先级(粗→细)

4. 参数影响:
   - chunk_size过小: 块数多,检索慢,丢失上下文
   - chunk_size过大: 精度低,Token浪费
   - chunk_overlap: 保证上下文连贯,避免信息被切断

5. 最佳实践:
   - 通用: RecursiveCharacterTextSplitter
   - chunk_size: 500, overlap: 50
   - 自定义separators适配内容
   - 保留元数据
   - 实验调优

6. 注意事项:
   ⚠️ 切割后块数会显著增加
   ⚠️ overlap会增加存储和计算成本
   ⚠️ 不同内容类型需要不同策略
   ⚠️ 监控检索效果持续优化

7. 下一步:
   切割后需要:
   → 向量化(Embedding)
   → 存入向量库(Vector Store)
   → 检索(Retrieval)
    """)