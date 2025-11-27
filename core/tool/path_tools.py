"""
Path management tools for mini-code-agent.
"""

import os
from typing import Optional


def create_path(
    base_path: str,
    name: str,
    is_file: bool = True,
    content: Optional[str] = None,
) -> str:
    """
    在指定文件夹下创建文件或文件夹，如果是文件还支持写入初始内容

    :param base_path: 基础路径（目录）
    :param name: 文件或文件夹名称
    :param is_file: 是否创建文件（True 创建文件，False 创建文件夹）
    :param content: 如果是文件，写入的内容（可选）
    :return: 创建的文件/文件夹绝对路径
    """
    try:
        # 确保 base_path 存在
        os.makedirs(base_path, exist_ok=True)

        target_path = os.path.join(base_path, name)

        if is_file:
            # 如果文件不存在则创建，并写入内容
            with open(target_path, "w", encoding="utf-8") as f:
                if content:
                    f.write(content)
            print(f"✅ 文件已创建: {os.path.abspath(target_path)}")
        else:
            # 创建文件夹
            os.makedirs(target_path, exist_ok=True)
            print(f"✅ 文件夹已创建: {os.path.abspath(target_path)}")

        return os.path.abspath(target_path)

    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return ""


def edit_path(
    path: str,
    new_name: Optional[str] = None,
    new_content: Optional[str] = None,
) -> Optional[str]:
    """
    编辑文件或文件夹

    :param path: 要编辑的文件或文件夹路径
    :param new_name: 新名称（可选）
    :param new_content: 新内容（仅文件有效，可选）
    :return: 编辑后的新路径，失败返回 None
    """
    if not os.path.exists(path):
        print(f"❌ 路径不存在: {path}")
        return None

    try:
        # 判断是文件还是文件夹
        if os.path.isfile(path):
            # 编辑文件内容
            if new_content is not None:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ 文件内容已更新: {path}")

            # 修改文件名称
            if new_name:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
                print(f"✅ 文件已重命名: {new_path}")
                return os.path.abspath(new_path)
            return os.path.abspath(path)

        elif os.path.isdir(path):
            # 修改文件夹名称
            if new_name:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
                print(f"✅ 文件夹已重命名: {new_path}")
                return os.path.abspath(new_path)
            return os.path.abspath(path)

    except Exception as e:
        print(f"❌ 编辑失败: {e}")
        return None
