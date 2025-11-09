"""
LangChain环境验证脚本
检查开发环境是否配置正确

学习目标:
1. 验证LangChain安装
2. 检查环境变量配置
3. 测试基本功能
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def check_python_version():
    """检查Python版本"""
    print("\n--- 检查Python版本 ---")
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 警告: LangChain需要Python 3.8+")
        return False
    else:
        print("✅ Python版本符合要求")
        return True


def check_langchain():
    """检查LangChain安装"""
    print("\n--- 检查LangChain ---")

    try:
        import langchain
        print(f"✅ LangChain版本: {langchain.__version__}")

        # 检查核心包
        try:
            import langchain_core
            print(f"✅ langchain-core: {langchain_core.__version__}")
        except ImportError:
            print("⚠️  langchain-core未安装")

        # 检查OpenAI集成
        try:
            import langchain_openai
            print(f"✅ langchain-openai: {langchain_openai.__version__}")
        except ImportError:
            print("⚠️  langchain-openai未安装")

        # 检查社区包
        try:
            import langchain_community
            print(f"✅ langchain-community: {langchain_community.__version__}")
        except ImportError:
            print("⚠️  langchain-community未安装(可选)")

        return True

    except ImportError:
        print("❌ LangChain未安装!")
        print("   安装命令: pip install langchain")
        return False


def check_env_vars():
    """检查环境变量"""
    print("\n--- 检查环境变量 ---")

    env_vars = {
        "OPENAI_API_KEY": "OpenAI API密钥",
        "DEEPSEEK_API_KEY": "DeepSeek API密钥(可选)",
        "ZHIPU_API_KEY": "智谱GLM API密钥(可选)",
        "LANGSMITH_API_KEY": "LangSmith API密钥(可选)"
    }

    found_any = False
    for var, desc in env_vars.items():
        value = os.getenv(var)
        if value:
            # 只显示前8位,保护隐私
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var}: {masked}")
            found_any = True
        else:
            if "可选" not in desc:
                print(f"❌ {var}: 未设置 ({desc})")
            else:
                print(f"⚠️  {var}: 未设置 ({desc})")

    return found_any


def check_dependencies():
    """检查常用依赖"""
    print("\n--- 检查常用依赖 ---")

    dependencies = {
        "tiktoken": "Token计算",
        "chromadb": "向量数据库",
        "python-dotenv": "环境变量管理",
    }

    all_installed = True
    for package, desc in dependencies.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}: 已安装 ({desc})")
        except ImportError:
            print(f"⚠️  {package}: 未安装 ({desc})")
            all_installed = False

    return all_installed


def test_basic_functionality():
    """测试基本功能"""
    print("\n--- 测试基本功能 ---")

    try:
        from langchain_openai import ChatOpenAI

        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  跳过功能测试(未配置OPENAI_API_KEY)")
            return True

        print("正在测试LLM调用...")
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=50
        )

        response = llm.invoke("Say 'Hello'")
        print(f"✅ LLM调用成功: {response.content[:50]}...")
        return True

    except Exception as e:
        print(f"❌ LLM调用失败: {str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("LangChain 环境验证")
    print("=" * 60)

    results = {
        "Python版本": check_python_version(),
        "LangChain安装": check_langchain(),
        "环境变量": check_env_vars(),
        "依赖包": check_dependencies(),
        "基本功能": test_basic_functionality()
    }

    print("\n" + "=" * 60)
    print("检查结果汇总")
    print("=" * 60)

    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    # 总体评估
    if all(results.values()):
        print("\n🎉 恭喜!所有检查通过,环境配置正确!")
    else:
        print("\n⚠️  部分检查未通过,请根据上述提示进行修复")

    print("\n💡 提示:")
    print("1. 如果缺少包,使用 pip install <package> 安装")
    print("2. API Key请在.env文件中配置")
    print("3. 建议安装所有依赖以获得完整功能")


if __name__ == "__main__":
    main()