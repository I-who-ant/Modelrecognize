"""
结构化输出示例

学习目标:
1. 掌握Pydantic模型定义结构化数据
2. 理解多种OutputParser的使用
3. 学会从自然语言中提取结构化信息
"""
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import (
    PydanticOutputParser,
    JsonOutputParser,
    StrOutputParser
)
from langchain.output_parsers import (
    StructuredOutputParser,
    ResponseSchema,
    OutputFixingParser
)
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


# ===== Pydantic 模型定义 =====

class Person(BaseModel):
    """人物信息模型"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")
    city: str = Field(description="居住城市")

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0 or v > 150:
            raise ValueError('年龄必须在0-150之间')
        return v


class Article(BaseModel):
    """文章信息模型"""
    title: str = Field(description="文章标题")
    author: str = Field(description="作者姓名")
    summary: str = Field(description="文章摘要,50字以内")
    tags: List[str] = Field(description="文章标签列表")
    category: str = Field(description="文章分类")
    publish_date: Optional[str] = Field(description="发布日期,格式YYYY-MM-DD", default=None)


class ProductReview(BaseModel):
    """产品评价模型"""
    product_name: str = Field(description="产品名称")
    rating: int = Field(description="评分,1-5分", ge=1, le=5)
    pros: List[str] = Field(description="优点列表")
    cons: List[str] = Field(description="缺点列表")
    sentiment: str = Field(description="总体情感: positive/negative/neutral")
    recommended: bool = Field(description="是否推荐购买")


# ===== 示例函数 =====

def demo_pydantic_parser():
    """演示Pydantic解析器"""
    print("=" * 60)
    print("方法1: Pydantic Output Parser")
    print("=" * 60)

    # 1. 创建解析器
    parser = PydanticOutputParser(pydantic_object=Person)

    # 2. 获取格式说明
    format_instructions = parser.get_format_instructions()

    # 3. 构建Prompt
    text = "张三是一位25岁的软件工程师，目前居住在北京"

    prompt = f"""
从以下文本中提取人物信息:
{text}

{format_instructions}
"""

    # 4. 调用LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(prompt)

    print(f"\n原始文本: {text}")
    print(f"\nLLM响应:\n{response.content}\n")

    # 5. 解析为Pydantic对象
    try:
        person = parser.parse(response.content)
        print("解析结果:")
        print(f"  类型: {type(person)}")
        print(f"  姓名: {person.name}")
        print(f"  年龄: {person.age}")
        print(f"  职业: {person.occupation}")
        print(f"  城市: {person.city}")
    except Exception as e:
        print(f"解析失败: {e}")


def demo_json_parser():
    """演示JSON解析器"""
    print("\n" + "=" * 60)
    print("方法2: JSON Output Parser")
    print("=" * 60)

    parser = JsonOutputParser()

    prompt = f"""
提取以下信息并以JSON格式返回:
- 产品名称
- 价格
- 库存数量
- 是否有货

文本: "iPhone 15 Pro，售价7999元，库存20台，现货供应"

{parser.get_format_instructions()}
"""

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(prompt)

    print(f"\nLLM响应:\n{response.content}\n")

    # 解析为Python字典
    data = parser.parse(response.content)
    print("解析结果:")
    print(f"  类型: {type(data)}")
    print(f"  内容: {data}")


def demo_structured_parser():
    """演示结构化解析器"""
    print("\n" + "=" * 60)
    print("方法3: Structured Output Parser")
    print("=" * 60)

    # 定义响应结构
    response_schemas = [
        ResponseSchema(name="product", description="产品名称"),
        ResponseSchema(name="brand", description="品牌"),
        ResponseSchema(name="price", description="价格,只返回数字"),
        ResponseSchema(name="features", description="主要特点,用逗号分隔"),
        ResponseSchema(name="recommend", description="是否推荐: yes/no")
    ]

    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    prompt = f"""
分析以下产品评价:
"小米14 Pro手机真不错！性能强劲，拍照清晰，续航给力，价格4999元很值，强烈推荐！"

{parser.get_format_instructions()}
"""

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(prompt)

    print(f"\nLLM响应:\n{response.content}\n")

    result = parser.parse(response.content)
    print("解析结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")


def demo_complex_model():
    """演示复杂模型解析"""
    print("\n" + "=" * 60)
    print("复杂Pydantic模型示例")
    print("=" * 60)

    parser = PydanticOutputParser(pydantic_object=ProductReview)

    text = """
MacBook Pro 16寸 M3 Max版使用体验：

优点：
1. 性能超强，运行大型项目毫无压力
2. 屏幕显示效果惊艳
3. 续航能力出色

缺点：
1. 价格略贵
2. 比较重，携带不太方便

总体来说非常推荐给专业用户，物有所值！评分5分。
"""

    prompt = f"""
从以下产品评价中提取结构化信息:
{text}

{parser.get_format_instructions()}
"""

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    response = llm.invoke(prompt)

    print(f"原始评价:\n{text}")
    print(f"\nLLM响应:\n{response.content}\n")

    try:
        review = parser.parse(response.content)
        print("解析结果:")
        print(f"  产品: {review.product_name}")
        print(f"  评分: {review.rating}/5")
        print(f"  优点: {', '.join(review.pros)}")
        print(f"  缺点: {', '.join(review.cons)}")
        print(f"  情感: {review.sentiment}")
        print(f"  推荐: {'是' if review.recommended else '否'}")
    except Exception as e:
        print(f"解析失败: {e}")


def demo_batch_extraction():
    """演示批量提取"""
    print("\n" + "=" * 60)
    print("批量结构化提取")
    print("=" * 60)

    parser = PydanticOutputParser(pydantic_object=Article)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    texts = [
        "《LangChain实战》由张三撰写，详细介绍了LangChain框架的使用方法和最佳实践。发布于2024-01-15。标签：AI, Python, LLM。分类：技术教程",
        "《深入理解Agent》作者李四，探讨了AI Agent的设计原理和实现细节。2024-02-20发布。标签：Agent, AI, 架构设计。分类：技术深度"
    ]

    articles = []
    for i, text in enumerate(texts, 1):
        prompt = f"""
从以下文本中提取文章信息:
{text}

{parser.get_format_instructions()}
"""
        response = llm.invoke(prompt)

        try:
            article = parser.parse(response.content)
            articles.append(article)
            print(f"\n文章 {i}:")
            print(f"  标题: {article.title}")
            print(f"  作者: {article.author}")
            print(f"  标签: {', '.join(article.tags)}")
            print(f"  分类: {article.category}")
        except Exception as e:
            print(f"\n文章 {i} 解析失败: {e}")


def demo_error_fixing():
    """演示自动修复解析错误"""
    print("\n" + "=" * 60)
    print("自动修复解析错误")
    print("=" * 60)

    # 原始解析器
    pydantic_parser = PydanticOutputParser(pydantic_object=Person)

    # 包装为自动修复解析器
    fixing_parser = OutputFixingParser.from_llm(
        parser=pydantic_parser,
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    )

    # 故意构造一个格式不完全正确的JSON
    bad_json = """
{
    "name": "王五",
    "age": "30岁",  # 这里应该是数字，不是字符串
    "occupation": "设计师",
    "city": "深圳"
}
"""

    print("错误的JSON:")
    print(bad_json)

    try:
        # 普通解析器会失败
        print("\n尝试普通解析...")
        pydantic_parser.parse(bad_json)
    except Exception as e:
        print(f"❌ 普通解析失败: {str(e)[:100]}...")

    try:
        # 自动修复解析器会尝试修复
        print("\n尝试自动修复解析...")
        person = fixing_parser.parse(bad_json)
        print("✅ 自动修复成功!")
        print(f"  姓名: {person.name}")
        print(f"  年龄: {person.age} (类型: {type(person.age)})")
    except Exception as e:
        print(f"修复也失败了: {e}")


if __name__ == "__main__":
    print("📦 LangChain 结构化输出完整示例\n")

    # 运行所有示例
    demo_pydantic_parser()
    demo_json_parser()
    demo_structured_parser()
    demo_complex_model()
    demo_batch_extraction()
    demo_error_fixing()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 三种主要解析器:
   ✅ PydanticOutputParser - 类型安全，自动验证
   ✅ JsonOutputParser - 简单灵活，返回字典
   ✅ StructuredOutputParser - 配置简单，固定字段

2. Pydantic的优势:
   - 类型检查和验证
   - IDE自动补全
   - 清晰的数据模型
   - 可复用的模型定义

3. 使用场景:
   - 信息提取
   - 数据标注
   - 表单填写
   - API响应生成

4. 最佳实践:
   - 复杂场景用Pydantic
   - 简单场景用Json
   - 使用OutputFixingParser自动修复错误
   - temperature=0提高一致性

5. 注意事项:
   - 需要清晰的format_instructions
   - LLM可能不完全遵守格式
   - 需要异常处理
   - 成本会略高(格式说明占Token)
    """)