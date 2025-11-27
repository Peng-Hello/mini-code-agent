"""
File editing tools for mini-code-agent.
"""

import re


def replace_in_file(
    file_path: str, pattern: str, replacement: str, encoding: str = "utf-8"
) -> bool:
    """
    根据正则匹配替换指定文件的内容

    :param file_path: 文件路径
    :param pattern: 正则表达式
    :param replacement: 替换内容
    :param encoding: 文件编码（默认 utf-8）
    :return: 替换是否成功（True 成功，False 失败）
    """
    import os

    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    if not os.path.isfile(file_path):
        print(f"❌ 不是文件: {file_path}")
        return False

    try:
        with open(file_path, "r", encoding=encoding, errors="ignore") as f:
            content = f.read()

        new_content, count = re.subn(pattern, replacement, content)
        if count == 0:
            print(f"⚠️ 未匹配到任何内容: {pattern}")
            return False

        with open(file_path, "w", encoding=encoding) as f:
            f.write(new_content)

        print(f"✅ 替换完成: {file_path}，共替换 {count} 处")
        return True

    except Exception as e:
        print(f"❌ 替换失败: {e}")
        return False
