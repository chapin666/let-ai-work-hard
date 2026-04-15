# Source: chapter-06-ai-ide-basics.md
# Lines: 585-601
# Language: bash

# 安装
pip install openai-codex

# 1. 基本Agent任务
codex "给这个项目添加JWT认证"

# 2. 多模态任务：传设计稿生成代码
codex --image ./login-design.png "实现这个登录页面"

# 3. 自动化模式（适合CI/CD）
codex --approval-mode auto "运行所有测试并修复失败的用例"

# 4. 带上下文的复杂任务
codex "@src/services/user.js @src/models/user.js 重构这两个文件，
       将回调改为async/await，保持API兼容"
