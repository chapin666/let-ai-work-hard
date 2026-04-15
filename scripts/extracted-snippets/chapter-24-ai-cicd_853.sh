# Source: chapter-24-ai-cicd.md
# Lines: 853-882
# Language: bash

#!/bin/bash
# rollback.sh - 一键回滚脚本

NAMESPACE=${1:-production}
DEPLOYMENT=${2:-myapp}
TO_REVISION=${3:-0}  # 0表示上一个版本

echo "🔄 开始回滚 $DEPLOYMENT (namespace: $NAMESPACE)..."

# 显示当前版本
kubectl rollout history deployment/$DEPLOYMENT -n $NAMESPACE

# 执行回滚
kubectl rollout undo deployment/$DEPLOYMENT -n $NAMESPACE --to-revision=$TO_REVISION

# 等待回滚完成
echo "⏳ 等待回滚完成..."
kubectl rollout status deployment/$DEPLOYMENT -n $NAMESPACE --timeout=300s

# 验证
if [ $? -eq 0 ]; then
    echo "✅ 回滚成功！"
    # 发送通知
    curl -X POST $WEBHOOK_URL -d "{"text": "✅ $DEPLOYMENT 已回滚到版本 $TO_REVISION"}"
else
    echo "❌ 回滚失败，请手动处理！"
    exit 1
fi
