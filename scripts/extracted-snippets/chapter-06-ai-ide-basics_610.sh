# Source: chapter-06-ai-ide-basics.md
# Lines: 610-622
# Language: bash

# 查看费用消耗
codex --cost

# 使用特定模型
codex --model gpt-4o "任务描述"

# 限制执行范围（安全）
codex --sandbox "执行可能危险的命令"

# 批量处理多个文件
codex "给src/components/下的所有组件添加PropTypes"
