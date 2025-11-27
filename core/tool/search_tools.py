"""
Search tools for mini-code-agent.
"""

import os
import re
from typing import List, Optional, Set


def search_in_files(
    root_path: str,
    pattern: str,
    encoding: str = "utf-8",
    exclude_dirs: Optional[Set[str]] = None,
) -> List[str]:
    """
    在指定文件夹下搜索包含指定正则内容的文件，返回文件绝对路径列表

    :param root_path: 搜索的根目录
    :param pattern: 正则表达式
    :param encoding: 文件编码（默认 utf-8）
    :param exclude_dirs: 要忽略的目录名集合（默认忽略 .idea 和 node_modules 提高检索速度）
    :return: 匹配到的文件路径列表
    """
    if exclude_dirs is None:
        exclude_dirs = {".idea", "node_modules"}

    if not os.path.exists(root_path):
        print(f"❌ 路径不存在: {root_path}")
        return []
    if not os.path.isdir(root_path):
        print(f"❌ 不是文件夹: {root_path}")
        return []

    regex = re.compile(pattern)
    result = []

    for dirpath, dirs, files in os.walk(root_path):
        # 排除指定目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for filename in files:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(
                    file_path, "r", encoding=encoding, errors="ignore"
                ) as f:
                    for line in f:
                        if regex.search(line):
                            result.append(os.path.abspath(file_path))
                            break
            except (OSError, UnicodeDecodeError):
                continue

    return result
