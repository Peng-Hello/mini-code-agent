# AI 核心功能实现

## 需求信息
| 项目 | 内容 |  
|------|------|  
| 版本号 | v1.0.0 |  

## 需求
这个是Agent 核心的代码实现。包括工具集成，实现Agent 配置，实现功能。
现成代码：D:\Project\Course\CodeAgent\index.py
现成代码的功能是验证过可行的，你要做的是把他主函数函数化，然后工具放在特定文件夹，AI 配置抽象成读用户目录的.mini-code-agent 文件夹里面的config配置文件。
配置文件路径有两种情况：
1. 用户目录下的.mini-code-agent 文件夹里面的config配置文件
2. 当前路径项目的.mini-code-agent 文件夹里面的config配置文件

## 上一步
后面会做一个CLI APP界面出来调用里面函数来激活AI agent。入参可能有用户输入的问题。

## 下一步
实时把运行日志显示到CLI APP UI界面。

## 工作目录
代码实现路径：mini-code-agent\core

工作目录结构：
```
mini-code-agent
├─ core // AI 核心实现
  └─ tool // 工具单独放在这
```

