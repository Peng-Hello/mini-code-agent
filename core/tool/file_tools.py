"""
File operation tools for mini-code-agent.
"""

import os


def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    读取指定路径文件内容并返回字符串

    :param file_path: 文件路径 入参格式 r"path"
    :param encoding: 文件编码（默认 utf-8）
    :return: 文件内容字符串
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ 文件未找到: {file_path}")
    except PermissionError:
        print(f"❌ 没有权限读取文件: {file_path}")
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
    return ""


def list_file_tree(root_path: str, indent: str = "  ") -> str:
    """
    生成指定文件夹下的文件树

    :param root_path: 根目录路径
    :param indent: 缩进样式（默认两个空格）
    :return: 文件树字符串
    """
    if not os.path.exists(root_path):
        return f"❌ 路径不存在: {root_path}"
    if not os.path.isdir(root_path):
        return f"❌ 不是文件夹: {root_path}"

    tree_lines = []

    def _walk(dir_path: str, level: int = 0):
        try:
            items = sorted(os.listdir(dir_path))
        except PermissionError:
            tree_lines.append(f"{indent * level}❌ [无权限访问] {dir_path}")
            return

        for item in items:
            full_path = os.path.join(dir_path, item)
            prefix = indent * level + "├─ " if level > 0 else ""
            if os.path.isdir(full_path):
                tree_lines.append(f"{prefix}{item}/")
                _walk(full_path, level + 1)
            else:
                tree_lines.append(f"{prefix}{item}")

    _walk(root_path)
    return "\n".join(tree_lines)
