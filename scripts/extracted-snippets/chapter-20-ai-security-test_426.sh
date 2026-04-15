# Source: chapter-20-ai-security-test.md
# Lines: 426-440
# Language: bash

#!/bin/sh
# .husky/pre-commit

echo "Running security checks..."

# 1. 检查密钥泄露
gitleaks protect --staged --verbose

# 2. 静态代码扫描
semgrep --config=auto --error

# 3. AI辅助安全检查
node scripts/ai-security-check.js --diff
