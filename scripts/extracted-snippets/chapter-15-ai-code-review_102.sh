# Source: chapter-15-ai-code-review.md
# Lines: 102-122
# Language: bash

#!/bin/sh
# .husky/pre-commit

echo "🤖 正在运行AI代码检查..."

# 获取暂存区的文件
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|jsx|ts|tsx)$')

if [ -n "$STAGED_FILES" ]; then
  # 调用AI检查API
  npx ai-code-review --files "$STAGED_FILES" --level=error
  
  if [ $? -ne 0 ]; then
    echo "❌ AI检查发现严重问题，请修复后重新提交"
    exit 1
  fi
fi

echo "✅ AI检查通过"
