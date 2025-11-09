"""
文档加载器完整示例

学习目标:
1. 掌握多种文档加载器的使用
2. 理解Document对象结构
3. 学会处理不同格式的数据源
"""
from dotenv import load_dotenv
from pathlib import Path
import sys

load_dotenv()

# 创建示例数据目录
DATA_DIR = Path("sample_data")
DATA_DIR.mkdir(exist_ok=True)


def demo_text_loader():
    """文本文件加载器"""
    print("=" * 60)
    print("1. TextLoader - 文本文件加载")
    print("=" * 60)

    from langchain_community.document_loaders import TextLoader

    # 创建示例文本文件
    sample_file = DATA_DIR / "sample.txt"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("""LangChain是一个用于开发由大语言模型驱动的应用程序的框架。

核心功能:
1. 模型I/O封装
2. 数据连接
3. 链(Chains)
4. 代理(Agents)
5. 内存(Memory)

LangChain使开发者能够快速构建复杂的LLM应用。""")

    # 加载文本
    loader = TextLoader(str(sample_file), encoding='utf-8')
    docs = loader.load()

    print(f"\n加载文档数: {len(docs)}")
    print(f"\n第一个文档:")
    print(f"  内容长度: {len(docs[0].page_content)} 字符")
    print(f"  内容预览: {docs[0].page_content[:100]}...")
    print(f"  元数据: {docs[0].metadata}")


def demo_directory_loader():
    """目录批量加载"""
    print("\n" + "=" * 60)
    print("2. DirectoryLoader - 批量加载目录")
    print("=" * 60)

    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    # 创建多个示例文件
    for i in range(3):
        file_path = DATA_DIR / f"doc{i+1}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"这是第{i+1}个文档的内容。\n" * 5)

    # 批量加载
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="*.txt",           # 文件模式
        loader_cls=TextLoader,  # 使用的加载器类
        loader_kwargs={'encoding': 'utf-8'},
        show_progress=True      # 显示进度
    )

    docs = loader.load()

    print(f"\n加载文档数: {len(docs)}")
    for i, doc in enumerate(docs):
        print(f"\n文档{i+1}:")
        print(f"  来源: {doc.metadata['source']}")
        print(f"  内容长度: {len(doc.page_content)} 字符")


def demo_pdf_loader():
    """PDF加载器"""
    print("\n" + "=" * 60)
    print("3. PyPDFLoader - PDF文件加载")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import PyPDFLoader

        # 注意: 这里需要真实的PDF文件
        print("\nPyPDFLoader使用示例:")
        print("""
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader("document.pdf")
        pages = loader.load()

        # 每页作为单独的Document
        for i, page in enumerate(pages):
            print(f"Page {i+1}:")
            print(f"  Content length: {len(page.page_content)}")
            print(f"  Metadata: {page.metadata}")
        """)

        print("\n如果需要保留更多PDF结构信息,可以使用UnstructuredPDFLoader:")
        print("""
        from langchain_community.document_loaders import UnstructuredPDFLoader

        loader = UnstructuredPDFLoader("document.pdf")
        docs = loader.load()
        """)

    except ImportError:
        print("\n⚠️ pypdf未安装，请运行: pip install pypdf")


def demo_web_loader():
    """网页加载器"""
    print("\n" + "=" * 60)
    print("4. WebBaseLoader - 网页加载")
    print("=" * 60)

    try:
        from langchain_community.document_loaders import WebBaseLoader

        # 加载网页
        loader = WebBaseLoader("https://python.langchain.com/docs/get_started/introduction")

        print("\n正在加载网页...")
        docs = loader.load()

        print(f"\n加载成功!")
        print(f"  文档数: {len(docs)}")
        print(f"  内容长度: {len(docs[0].page_content)} 字符")
        print(f"  元数据: {docs[0].metadata}")
        print(f"  内容预览: {docs[0].page_content[:200]}...")

    except ImportError:
        print("\n⚠️ beautifulsoup4未安装，请运行: pip install beautifulsoup4")
    except Exception as e:
        print(f"\n网页加载失败(可能需要网络): {e}")
        print("\n示例代码:")
        print("""
        from langchain_community.document_loaders import WebBaseLoader

        loader = WebBaseLoader("https://example.com")
        docs = loader.load()

        # 加载多个网页
        urls = ["https://example.com/page1", "https://example.com/page2"]
        loader = WebBaseLoader(urls)
        docs = loader.load()
        """)


def demo_csv_loader():
    """CSV加载器"""
    print("\n" + "=" * 60)
    print("5. CSVLoader - CSV文件加载")
    print("=" * 60)

    from langchain_community.document_loaders import CSVLoader
    import csv

    # 创建示例CSV
    csv_file = DATA_DIR / "users.csv"
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['姓名', '年龄', '职业'])
        writer.writerow(['张三', '25', 'Python开发'])
        writer.writerow(['李四', '30', '数据分析师'])
        writer.writerow(['王五', '28', '前端工程师'])

    # 加载CSV
    loader = CSVLoader(
        file_path=str(csv_file),
        encoding='utf-8'
    )

    docs = loader.load()

    print(f"\n加载文档数: {len(docs)}")
    print("\n每行作为一个Document:")
    for i, doc in enumerate(docs):
        print(f"\n文档{i+1}:")
        print(f"  内容: {doc.page_content}")
        print(f"  元数据: {doc.metadata}")


def demo_custom_loader():
    """自定义加载器"""
    print("\n" + "=" * 60)
    print("6. 自定义Document创建")
    print("=" * 60)

    from langchain_core.documents import Document

    # 手动创建Document
    docs = [
        Document(
            page_content="Python是一门简洁的编程语言。",
            metadata={
                "source": "manual",
                "topic": "编程语言",
                "language": "Python",
                "difficulty": "初级"
            }
        ),
        Document(
            page_content="JavaScript主要用于Web开发。",
            metadata={
                "source": "manual",
                "topic": "编程语言",
                "language": "JavaScript",
                "difficulty": "中级"
            }
        ),
        Document(
            page_content="Rust是一门注重安全的系统编程语言。",
            metadata={
                "source": "manual",
                "topic": "编程语言",
                "language": "Rust",
                "difficulty": "高级"
            }
        )
    ]

    print(f"\n创建了{len(docs)}个Document")

    print("\n可以基于元数据进行过滤:")
    beginner_docs = [doc for doc in docs if doc.metadata.get("difficulty") == "初级"]
    print(f"  初级难度文档数: {len(beginner_docs)}")
    print(f"  内容: {beginner_docs[0].page_content}")


def demo_markdown_loader():
    """Markdown加载器"""
    print("\n" + "=" * 60)
    print("7. UnstructuredMarkdownLoader - Markdown加载")
    print("=" * 60)

    # 创建示例Markdown
    md_file = DATA_DIR / "readme.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("""# LangChain教程

## 什么是LangChain?

LangChain是一个用于开发大语言模型应用的框架。

## 核心组件

### 1. 模型I/O

- Chat Models
- LLMs
- Prompts

### 2. 数据连接

- Document Loaders
- Text Splitters
- Vector Stores

## 示例代码

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
response = llm.invoke("Hello")
```

## 总结

LangChain简化了LLM应用开发。
""")

    try:
        from langchain_community.document_loaders import UnstructuredMarkdownLoader

        loader = UnstructuredMarkdownLoader(str(md_file))
        docs = loader.load()

        print(f"\n加载文档数: {len(docs)}")
        print(f"\n内容预览:")
        print(docs[0].page_content[:300])

    except ImportError:
        print("\n⚠️ unstructured未安装，请运行: pip install unstructured")
        print("\n可以使用TextLoader作为替代:")
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(str(md_file), encoding='utf-8')
        docs = loader.load()
        print(f"  加载成功: {len(docs)} 个文档")


def demo_document_structure():
    """深入理解Document结构"""
    print("\n" + "=" * 60)
    print("8. Document对象结构详解")
    print("=" * 60)

    from langchain_core.documents import Document

    doc = Document(
        page_content="这是文档的主要内容。可以是任意长度的文本。",
        metadata={
            "source": "example.txt",
            "page": 1,
            "author": "老王",
            "created_at": "2025-01-09",
            "tags": ["教程", "LangChain"],
            "word_count": 20
        }
    )

    print("\n✅ Document包含两个核心属性:")
    print("\n1. page_content (str):")
    print(f"   类型: {type(doc.page_content)}")
    print(f"   内容: {doc.page_content}")

    print("\n2. metadata (dict):")
    print(f"   类型: {type(doc.metadata)}")
    print(f"   内容: {doc.metadata}")

    print("\n✅ 元数据的重要性:")
    print("  - 来源追踪(source)")
    print("  - 过滤检索(基于metadata筛选)")
    print("  - 上下文信息(page, author等)")
    print("  - 自定义字段(任意键值对)")

    print("\n✅ 访问Document属性:")
    print(f"  内容: doc.page_content")
    print(f"  元数据: doc.metadata")
    print(f"  特定字段: doc.metadata['source']")


if __name__ == "__main__":
    print("📄 LangChain Document Loaders 完整示例\n")

    # 运行所有示例
    demo_text_loader()
    demo_directory_loader()
    demo_pdf_loader()
    demo_web_loader()
    demo_csv_loader()
    demo_markdown_loader()
    demo_custom_loader()
    demo_document_structure()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. Document对象:
   - page_content: 文本内容(必需)
   - metadata: 元数据字典(可选但重要)

2. 常用加载器:
   ✅ TextLoader: 纯文本(.txt)
   ✅ PyPDFLoader: PDF文件(.pdf)
   ✅ WebBaseLoader: 网页内容
   ✅ CSVLoader: CSV数据(.csv)
   ✅ DirectoryLoader: 批量加载
   ✅ UnstructuredMarkdownLoader: Markdown(.md)

3. 选择加载器:
   - 文件格式决定加载器类型
   - 考虑元数据需求
   - 批量加载用DirectoryLoader
   - 特殊格式考虑unstructured系列

4. 元数据最佳实践:
   - 始终包含source(来源)
   - 添加有助于检索的字段
   - 保持元数据结构一致
   - 可自定义任意字段

5. 依赖安装:
   PDF: pip install pypdf
   网页: pip install beautifulsoup4
   通用: pip install unstructured

6. 注意事项:
   ⚠️ 文件编码(默认utf-8)
   ⚠️ 大文件内存占用
   ⚠️ 网络加载可能失败
   ⚠️ 不同加载器返回格式可能不同

7. 下一步:
   加载后需要:
   → 文本切割(Text Splitting)
   → 向量化(Embedding)
   → 存入向量库(Vector Store)
    """)

    print(f"\n📁 示例数据目录: {DATA_DIR.absolute()}")