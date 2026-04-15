# Source: chapter-01-first-ai-experience.md
# Lines: 743-757
# Language: bash

# 安装
pip install openai-codex

# 基本使用
codex "给所有API添加统一错误处理"

# 多模态：传设计稿生成代码
codex --image ./design.png "根据设计稿生成React组件"

# CI/CD集成
# .github/workflows/auto-fix.yml
- name: Auto Fix Code
  run: codex --approval-mode auto "修复TypeScript错误"
