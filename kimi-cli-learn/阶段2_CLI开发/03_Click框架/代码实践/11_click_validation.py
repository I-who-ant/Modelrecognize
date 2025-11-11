"""
练习11: Click 参数验证实践

学习目标:
- 掌握 Click 内置参数类型
- 创建自定义参数类型
- 使用 callback 验证参数
- 理解环境变量支持
"""

import click # 导入 click 模块，用于创建命令行接口
from pathlib import Path # 导入 Path 类，用于处理文件路径
import re # 导入 re 模块，用于正则表达式匹配


# ========== 自定义参数类型 ==========

class URLParamType(click.ParamType):
    """URL 参数类型"""
    name = "url"

    def convert(self, value, param, ctx):
        url_pattern = re.compile( # 编译 URL 正则表达式
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(value): # 如果 URL 不匹配正则表达式
            self.fail(f'{value} 不是有效的 URL', param, ctx)
        return value


URL = URLParamType() # 创建 URL 参数类型实例


# ========== 验证回调函数 ==========

def validate_positive(ctx, param, value):
    """验证正数"""
    if value <= 0:
        raise click.BadParameter('必须是正数')
    return value # 返回验证通过的值


def validate_file_extension(ctx, param, value):
    """验证文件扩展名"""
    if value is None:
        return value

    allowed = ['.txt', '.md', '.json', '.yaml']
    path = Path(value)

    if path.suffix not in allowed:
        raise click.BadParameter(
            f'不支持 {path.suffix}，仅支持: {", ".join(allowed)}'
        )
    return value # 返回验证通过的值


@click.command() # 定义命令行命令为 fetch
@click.option('--url', type=URL, required=True, help='目标 URL')
@click.option( #
    '--timeout',
    type=int,
    default=30,
    callback=validate_positive,
    help='超时时间（秒）'
)
@click.option(
    '--output',
    type=click.Path(dir_okay=False, path_type=Path),
    callback=validate_file_extension,
    help='输出文件'
)
@click.option( # 定义选项参数 --api-key, -k
    '--api-key',
    envvar='MY_API_KEY',
    required=True,
    hide_input=True,
    help='API 密钥'
)
def fetch(url, timeout, output, api_key): #
    """从 URL 获取数据"""
    click.echo(f"✅ URL: {url}")
    click.echo(f"✅ 超时: {timeout} 秒")
    click.echo(f"✅ 输出: {output}")
    click.echo(f"✅ API Key: {api_key[:5]}...")


if __name__ == '__main__':
    fetch()
