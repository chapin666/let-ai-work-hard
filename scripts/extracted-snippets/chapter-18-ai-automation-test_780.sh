# Source: chapter-18-ai-automation-test.md
# Lines: 780-787
# Language: bash

# 生成详细覆盖率报告
npm test -- --coverage --coverageReporters=text-summary

# 找出未测试的文件
npx jest --coverage --collectCoverageFrom='src/**/*.js' --coverageReporters=json | \
  jq '.coverageMap | to_entries[] | select(.value.statementCoverage.pct < 50) | .key'
