## ADDED Requirements
### Requirement: Agent Configuration System
系统 SHALL 提供从两种路径读取AI配置的功能，按优先级顺序：
1. 项目路径的`.mini-code-agent/config.yaml`配置文件（最高优先级）
2. 用户目录的`.mini-code-agent/config.yaml`配置文件（备用路径）
支持`YAML`格式。

#### Scenario: Load configuration from project path
- **GIVEN** 项目路径存在`.mini-code-agent/config.yaml`文件
- **WHEN** Agent初始化时
- **THEN** 系统优先从项目路径加载配置并应用到DSPy LM

#### Scenario: Fallback to user home path
- **GIVEN** 项目路径无配置文件，但用户目录有`.mini-code-agent/config.yaml`
- **WHEN** Agent初始化时
- **THEN** 系统从用户目录加载配置并应用到DSPy LM

#### Scenario: No configuration found
- **GIVEN** 两种路径都无配置文件
- **WHEN** Agent初始化时
- **THEN** 系统使用默认配置或提示用户创建配置文件

### Requirement: Modular Tool System
系统 SHALL 提供模块化的工具系统，工具按功能分类存储在`core/tool/`目录下，并通过`core/tool/__init__.py`统一导出，使用户只需一个import语句即可访问所有工具。

#### Scenario: Single import access point
- **GIVEN** 工具按功能分类存储在独立模块中
- **WHEN** 用户需要使用多个工具
- **THEN** 只需一个import语句：`from core.tool import 工具1, 工具2, ...`

#### Scenario: Tool modules are organized by category
- **GIVEN** 工具按功能分类存储
- **WHEN** Agent需要使用工具
- **THEN** Agent可以正确导入和使用对应工具

#### Scenario: Tools provide consistent interface
- **GIVEN** 每个工具模块都有标准接口
- **WHEN** Agent调用工具时
- **THEN** 返回结果格式统一，错误处理一致

### Requirement: File Operations Tools
系统 SHALL 提供文件操作工具集合，包括文件读取、文件树生成、文件搜索功能。

#### Scenario: Read file content
- **GIVEN** 存在可读的文件路径
- **WHEN** 调用read_file工具
- **THEN** 返回文件内容，失败时返回错误信息

#### Scenario: Generate file tree
- **GIVEN** 存在目录路径
- **WHEN** 调用list_file_tree工具
- **THEN** 返回格式化的目录树字符串

#### Scenario: Search in files
- **GIVEN** 搜索根目录和正则模式
- **WHEN** 调用search_in_files工具
- **THEN** 返回匹配的文件路径列表

### Requirement: Path Management Tools
系统 SHALL 提供路径管理工具，包括创建、编辑、重命名文件和目录功能。

#### Scenario: Create file or directory
- **GIVEN** 基础路径和名称
- **WHEN** 调用create_path工具
- **THEN** 创建文件或目录并返回绝对路径

#### Scenario: Edit file or directory
- **GIVEN** 现有路径和新的内容或名称
- **WHEN** 调用edit_path工具
- **THEN** 更新内容或重命名并返回新路径

#### Scenario: Replace content in file
- **GIVEN** 文件路径、正则模式和替换内容
- **WHEN** 调用replace_in_file工具
- **THEN** 替换匹配内容并返回操作是否成功

### Requirement: Web Interaction Tools
系统 SHALL 提供网页交互工具，包括HTML获取和搜索引擎查询功能。

#### Scenario: Fetch website HTML
- **GIVEN** URL和等待时间
- **WHEN** 调用fetch_website_html工具
- **THEN** 返回动态渲染后的HTML内容

#### Scenario: Use search engine
- **GIVEN** 搜索关键词和搜索引擎
- **WHEN** 调用use_search_engine工具
- **THEN** 返回搜索结果列表[{title, url, desc}, ...]

### Requirement: Agent Core Engine
系统 SHALL 提供基于DSPy的Agent核心引擎，支持ReAct模式推理和工具调用。

#### Scenario: Initialize Agent with DSPy
- **GIVEN** 已配置的DSPy LM和工具列表
- **WHEN** 初始化Agent时
- **THEN** 创建可用的ReAct Agent实例

#### Scenario: Process user requirement
- **GIVEN** 用户需求字符串
- **WHEN** 调用Agent(requirement=...)时
- **THEN** Agent根据需求执行相应的工具调用并返回解决方案

#### Scenario: Agent provides status updates
- **GIVEN** Agent正在执行任务
- **WHEN** 每一步操作时
- **THEN** 通过tell_human_something工具输出当前操作状态

## MODIFIED Requirements
### Requirement: Agent Main Function
原有的`if __name__ == "__main__"`块 SHALL 被重构为可调用的函数接口。

#### Scenario: Call agent programmatically
- **GIVEN** 已配置的环境和工具
- **WHEN** 调用Agent(requirement=...)时
- **THEN** 返回解决方案，替代原有的main块执行
