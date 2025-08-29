# ChatLLM Pro v2 - 优化版本

## 🚀 快速开始

### 方法一：使用智能启动脚本（推荐）
```bash
# 在项目根目录下运行，自动处理端口冲突
python web/v2/start_app.py
```

### 方法二：使用基础启动脚本
```bash
# 在项目根目录下运行
python web/v2/run_app.py
```

### 方法二：作为模块运行
```bash
# 在项目根目录下运行
python -m web.v2.chat_server
```

### 方法三：直接运行（需要设置 PYTHONPATH）
```bash
# 设置 PYTHONPATH
export PYTHONPATH=/path/to/chat-llm-pro:$PYTHONPATH

# 运行应用
python web/v2/chat_server.py
```

## 🏗️ 架构说明

### 目录结构
```
web/v2/
├── chat_server.py              # 主应用文件
├── run_app.py                  # 启动脚本
├── components/                 # UI 组件
│   ├── chat_interface.py       # 聊天界面组件
│   └── knowledge_tab.py        # 知识管理组件
├── services/                   # 业务服务
│   ├── chat_service.py         # 聊天服务
│   ├── file_service.py         # 文件服务
│   └── model_manager.py        # 模型管理
├── utils/                      # 工具函数
│   └── error_handler.py        # 错误处理
└── test_optimization.py        # 测试脚本
```

### 主要改进

1. **模块化架构**: 将 321 行单体文件拆分为 8 个专注模块
2. **消除全局变量**: 使用依赖注入模式
3. **Markdown 支持**: 全面支持 Markdown 渲染
4. **错误处理**: 统一的错误处理机制
5. **现代化 UI**: 使用 Gradio 最新特性
6. **业务类型集成**: 完整支持原有的 10 种业务类型

## 🧪 测试

运行测试脚本验证优化效果：
```bash
# 基础功能测试
python web/v2/test_optimization.py

# 业务类型集成测试
python web/v2/test_business_types.py
```

## 🔧 故障排除

### 导入错误
如果遇到 `ImportError: attempted relative import with no known parent package` 错误：

1. 使用启动脚本：`python web/v2/run_app.py`
2. 或设置 PYTHONPATH：`export PYTHONPATH=/path/to/chat-llm-pro:$PYTHONPATH`

### 模块找不到
确保在项目根目录下运行，而不是在 `web/v2/` 目录下。

## 📊 优化效果

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| 主文件行数 | 321 行 | 120 行 | ✅ 减少 62% |
| 全局变量 | 3 个 | 0 个 | ✅ 完全消除 |
| 文件数量 | 1 个 | 8 个 | ✅ 模块化 |
| Markdown 支持 | 部分 | 全面 | ✅ 完整支持 |

## 🎯 使用说明

### 支持的业务类型

1. **摘要生成**: 总结关键词并生成摘要信息
2. **事件抽取**: 抽取文本中的事件，JSON 格式输出
3. **实体抽取**: 抽取文本中的实体信息，JSON 格式输出
4. **智能写作**: 辅助写作功能
5. **情感分类**: 判断文本情感分类，JSON 格式输出
6. **公告分类**: 判断公告类型，JSON 格式输出
7. **行业数据分析**: 分析行业数据关联性
8. **财报数据分析**: 分析财务报表数据
9. **问答**: 通用问答功能
10. **答题**: 答题辅助功能

### 功能模块

1. **场景问答**: 直接向大模型提问，支持所有业务类型
2. **文档问答**: 上传文档后进行问答，支持所有业务类型
3. **知识管理**: 添加和删除模型示例

所有功能都支持 Markdown 格式输出，界面更加美观易用。
