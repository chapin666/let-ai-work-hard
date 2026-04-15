# Source: chapter-35-ai-batch-processing.md
# Lines: 79-99
# Language: bash

# 统计需要改造的文件
find src -name "*.vue" | wc -l
# 输出: 352

find src -name "*.js" | xargs grep -l "Vue\." | wc -l
# 输出: 128

# 统计各种语法的使用频率
# Options API组件数量
grep -r "export default {" src --include="*.vue" | wc -l
# 输出: 340

# 使用filters的数量
grep -r "| format" src --include="*.vue" | wc -l
# 输出: 156

# 使用EventBus的数量
grep -r "\$emit" src --include="*.vue" | wc -l
# 输出: 423
