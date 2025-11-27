## Why
需要将现有的Agent代码实现从单一文件(index.py)重构为模块化的核心功能，为后续的CLI界面集成做好准备。当前代码将工具函数、AI配置、主逻辑混合在一起，难以维护和扩展。

## What Changes
- **BREAKING**: 将现有index.py中的工具函数重构为独立模块
- 在`core/tool/`目录下创建9个独立的工具模块
- 在`core/`目录下创建Agent核心逻辑模块
- 实现配置管理系统，支持双路径配置加载（优先级：项目路径 > 用户路径）
- 创建可调用的Agent主函数替代现有的`if __name__ == "__main__"`块
- 清理重复的`edit_path`函数定义

### 新增文件结构
```
core/
├── __init__.py
├── agent.py              # Agent主类和相关逻辑
├── config.py             # 配置管理
└── tool/
    ├── __init__.py       # 统一导出所有工具，单一import入口
    ├── file_tools.py     # read_file, list_file_tree
    ├── search_tools.py   # search_in_files
    ├── path_tools.py     # create_path, edit_path
    ├── edit_tools.py     # replace_in_file
    ├── web_tools.py      # fetch_website_html, use_search_engine
    └── io_tools.py       # tell_human_something
```

### 工具导入设计
- **使用方式**：通过`from core.tool import 工具名`统一导入
- **核心原则**：9个工具模块，但只有一个import语句
- **实现方式**：在`core/tool/__init__.py`中导入并重新导出所有工具
- **示例**：
  ```python
  from core.tool import read_file, list_file_tree, create_path
  # 只需要一个import语句即可使用所有工具
  ```

### 配置系统设计
支持两种配置路径，按优先级顺序：
1. **项目路径**（最高优先级）：`<当前工作目录>/.mini-code-agent/config.yaml`
2. **用户路径**（备用）：`<用户主目录>/.mini-code-agent/config.yaml`

优先级策略：
- 先检查项目路径的配置文件，如果存在则加载
- 如果项目路径不存在，则使用用户路径的配置文件
- 如果都无配置，使用默认配置或提示用户创建

配置格式：
- 使用`YAML`格式作为配置文件
- 文件名固定为`config.yaml`

### 修改文件
- 创建`config.yaml`格式说明文档和示例模板

## Impact
- 受影响的能力: agent-core
- 受影响的代码: 整个core/目录结构重构
- 为下一步CLI界面集成提供可调用的API
- 为实时日志显示功能奠定基础

## Next Steps
- CLI应用界面调用Agent函数
- 实时日志显示到CLI UI界面
