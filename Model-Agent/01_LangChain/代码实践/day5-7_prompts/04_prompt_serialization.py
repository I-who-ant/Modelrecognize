"""
Prompt模板序列化示例

学习目标:
1. 掌握模板的序列化和反序列化
2. 学会组织Prompt库
3. 理解版本控制最佳实践
"""
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    load_prompt
)
from pathlib import Path
import json
import yaml
from dotenv import load_dotenv

load_dotenv()

# 创建prompts目录
PROMPTS_DIR = Path("prompts_library")
PROMPTS_DIR.mkdir(exist_ok=True)


def demo_save_json():
    """保存为JSON格式"""
    print("=" * 60)
    print("1. 保存为JSON格式")
    print("=" * 60)

    # 创建模板
    template = PromptTemplate(
        input_variables=["product", "language"],
        template="Translate the product name '{product}' to {language}"
    )

    # 保存为JSON
    json_path = PROMPTS_DIR / "translate.json"
    template.save(str(json_path))

    print(f"\n✅ 模板已保存到: {json_path}")

    # 查看文件内容
    with open(json_path, 'r') as f:
        content = json.load(f)
        print("\nJSON内容:")
        print(json.dumps(content, indent=2, ensure_ascii=False))


def demo_save_yaml():
    """保存为YAML格式(推荐)"""
    print("\n" + "=" * 60)
    print("2. 保存为YAML格式")
    print("=" * 60)

    # 创建模板
    template = PromptTemplate(
        input_variables=["topic", "length"],
        template="""请写一篇关于{topic}的文章。

要求:
- 字数: {length}字左右
- 语言: 简洁易懂
- 结构: 总-分-总"""
    )

    # 保存为YAML
    yaml_path = PROMPTS_DIR / "article.yaml"
    template.save(str(yaml_path))

    print(f"\n✅ 模板已保存到: {yaml_path}")

    # 查看文件内容
    with open(yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("\nYAML内容:")
        print(content)


def demo_load_prompt():
    """加载Prompt模板"""
    print("\n" + "=" * 60)
    print("3. 加载Prompt模板")
    print("=" * 60)

    # 从JSON加载
    json_path = PROMPTS_DIR / "translate.json"
    if json_path.exists():
        template = load_prompt(str(json_path))
        print("\n从JSON加载的模板:")
        print(template.format(product="iPhone", language="Chinese"))

    # 从YAML加载
    yaml_path = PROMPTS_DIR / "article.yaml"
    if yaml_path.exists():
        template = load_prompt(str(yaml_path))
        print("\n从YAML加载的模板:")
        print(template.format(topic="AI", length=500))


def demo_save_chat_template():
    """保存ChatPromptTemplate"""
    print("\n" + "=" * 60)
    print("4. 保存ChatPromptTemplate")
    print("=" * 60)

    # 创建Chat模板
    template = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，你的专长是{specialty}"),
        ("human", "{question}")
    ])

    # ChatPromptTemplate的序列化稍复杂，需要手动处理
    # 这里展示如何保存配置
    config = {
        "_type": "chat_prompt",
        "messages": [
            {"role": "system", "content": "你是一个{role}，你的专长是{specialty}"},
            {"role": "human", "content": "{question}"}
        ],
        "input_variables": ["role", "specialty", "question"]
    }

    chat_path = PROMPTS_DIR / "chat_expert.yaml"
    with open(chat_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True)

    print(f"\n✅ Chat模板配置已保存到: {chat_path}")


def demo_prompt_library():
    """创建Prompt库"""
    print("\n" + "=" * 60)
    print("5. 组织Prompt库")
    print("=" * 60)

    # 创建分类目录
    categories = ["translation", "summary", "analysis", "chat"]
    for cat in categories:
        (PROMPTS_DIR / cat).mkdir(exist_ok=True)

    # 翻译类模板
    translate_templates = {
        "simple": PromptTemplate(
            input_variables=["text", "target_lang"],
            template="Translate to {target_lang}: {text}"
        ),
        "formal": PromptTemplate(
            input_variables=["text", "target_lang"],
            template="Translate the following text to {target_lang} in a formal tone:\n\n{text}"
        ),
        "with_context": PromptTemplate(
            input_variables=["text", "target_lang", "context"],
            template="""Context: {context}

Translate to {target_lang}: {text}"""
        )
    }

    # 保存翻译模板
    for name, template in translate_templates.items():
        path = PROMPTS_DIR / "translation" / f"{name}.yaml"
        template.save(str(path))
        print(f"  ✅ 保存: {path.name}")

    # 总结类模板
    summary_templates = {
        "brief": PromptTemplate(
            input_variables=["text"],
            template="Summarize in one sentence: {text}"
        ),
        "detailed": PromptTemplate(
            input_variables=["text", "num_points"],
            template="Summarize the following in {num_points} key points:\n\n{text}"
        )
    }

    for name, template in summary_templates.items():
        path = PROMPTS_DIR / "summary" / f"{name}.yaml"
        template.save(str(path))
        print(f"  ✅ 保存: {path.name}")

    print(f"\n📚 Prompt库已创建: {PROMPTS_DIR}")


def demo_version_control():
    """演示版本控制"""
    print("\n" + "=" * 60)
    print("6. 版本控制")
    print("=" * 60)

    # 创建带版本信息的模板
    template_v1 = {
        "_type": "prompt",
        "_version": "1.0",
        "_author": "老王",
        "_created": "2025-01-09",
        "_description": "基础翻译模板",
        "input_variables": ["text", "target_lang"],
        "template": "Translate to {target_lang}: {text}"
    }

    template_v2 = {
        "_type": "prompt",
        "_version": "2.0",
        "_author": "老王",
        "_updated": "2025-01-10",
        "_changelog": "添加了质量要求",
        "input_variables": ["text", "target_lang"],
        "template": """Translate to {target_lang} with high quality:

{text}

Requirements:
- Maintain the original meaning
- Use natural expressions
- Keep the tone consistent"""
    }

    # 保存不同版本
    v1_path = PROMPTS_DIR / "translate_v1.yaml"
    v2_path = PROMPTS_DIR / "translate_v2.yaml"

    with open(v1_path, 'w', encoding='utf-8') as f:
        yaml.dump(template_v1, f, allow_unicode=True)

    with open(v2_path, 'w', encoding='utf-8') as f:
        yaml.dump(template_v2, f, allow_unicode=True)

    print(f"  ✅ v1.0 保存到: {v1_path}")
    print(f"  ✅ v2.0 保存到: {v2_path}")

    print("\n版本控制最佳实践:")
    print("  1. 在YAML中包含版本号、作者、日期")
    print("  2. 记录变更日志(changelog)")
    print("  3. 使用Git管理Prompt文件")
    print("  4. 为重大变更创建新文件")
    print("  5. 保留旧版本以便回滚")


def demo_template_manager():
    """简单的模板管理器"""
    print("\n" + "=" * 60)
    print("7. 模板管理器")
    print("=" * 60)

    class PromptManager:
        """Prompt模板管理器"""

        def __init__(self, base_dir: Path):
            self.base_dir = base_dir
            self.base_dir.mkdir(exist_ok=True)

        def save(self, name: str, template: PromptTemplate, category: str = "default"):
            """保存模板"""
            category_dir = self.base_dir / category
            category_dir.mkdir(exist_ok=True)
            path = category_dir / f"{name}.yaml"
            template.save(str(path))
            return path

        def load(self, name: str, category: str = "default") -> PromptTemplate:
            """加载模板"""
            path = self.base_dir / category / f"{name}.yaml"
            if not path.exists():
                raise FileNotFoundError(f"Template not found: {path}")
            return load_prompt(str(path))

        def list_templates(self, category: str = None):
            """列出所有模板"""
            if category:
                search_dir = self.base_dir / category
                pattern = "*.yaml"
            else:
                search_dir = self.base_dir
                pattern = "**/*.yaml"

            return list(search_dir.glob(pattern))

    # 使用管理器
    manager = PromptManager(PROMPTS_DIR)

    # 保存模板
    template = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms"
    )
    path = manager.save("explain", template, "education")
    print(f"\n✅ 保存模板: {path}")

    # 列出模板
    print("\n📂 所有模板:")
    for tmpl_path in manager.list_templates():
        print(f"  - {tmpl_path.relative_to(PROMPTS_DIR)}")

    # 加载模板
    loaded = manager.load("explain", "education")
    print(f"\n✅ 加载模板: {loaded.format(topic='LangChain')}")


if __name__ == "__main__":
    print("💾 Prompt模板序列化完整示例\n")

    # 运行所有示例
    demo_save_json()
    demo_save_yaml()
    demo_load_prompt()
    demo_save_chat_template()
    demo_prompt_library()
    demo_version_control()
    demo_template_manager()

    # 总结
    print("\n" + "=" * 60)
    print("关键点总结")
    print("=" * 60)
    print("""
1. 序列化格式:
   ✅ JSON: 机器友好
   ✅ YAML: 人类友好(推荐)

2. 为什么序列化:
   - 版本控制(Git)
   - 团队协作
   - 非技术人员可编辑
   - A/B测试
   - 多语言管理

3. 目录组织:
   prompts/
   ├── translation/
   ├── summary/
   ├── analysis/
   └── chat/

4. 版本控制:
   - 添加版本号、作者、日期
   - 记录变更日志
   - 使用Git管理
   - 保留历史版本

5. 最佳实践:
   - 使用YAML格式
   - 按功能分类存储
   - 添加元数据(版本、描述)
   - 建立命名规范
   - 定期review和优化

6. 进阶功能:
   - 实现模板管理器
   - 支持模板继承
   - 自动化测试
   - 性能监控

7. 注意事项:
   ⚠️ 敏感信息不要硬编码
   ⚠️ 定期备份
   ⚠️ 文档化使用方法
   ⚠️ 建立review流程
    """)

    print(f"\n📚 Prompt库位置: {PROMPTS_DIR.absolute()}")