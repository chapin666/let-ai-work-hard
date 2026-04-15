# Source: chapter-24-ai-cicd.md
# Lines: 441-503
# Language: bash

#!/bin/bash
# canary-analysis.sh - 金丝雀发布健康检查

set -e

NAMESPACE="myapp-prod"
CANARY_DEPLOYMENT="backend-canary"
ANALYSIS_DURATION=300  # 5分钟分析窗口
ERROR_THRESHOLD=5      # 错误率阈值5%
LATENCY_THRESHOLD=500  # P99延迟阈值500ms

echo "🔍 开始金丝雀分析 (${ANALYSIS_DURATION}秒)..."

# 获取Prometheus指标
get_error_rate() {
  curl -s "http://prometheus:9090/api/v1/query?query=\
    sum(rate(http_requests_total{status=~'5..',version='canary'}[1m])) \
    / \
    sum(rate(http_requests_total{version='canary'}[1m]))" \
    | jq -r '.data.result[0].value[1] // 0'
}

get_latency_p99() {
  curl -s "http://prometheus:9090/api/v1/query?query=\
    histogram_quantile(0.99, \
      sum(rate(http_request_duration_seconds_bucket{version='canary'}[1m])) by (le)\
    )" \
    | jq -r '.data.result[0].value[1] // 0'
}

# 分析循环
START_TIME=$(date +%s)
while true; do
  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))
  
  if [ $ELAPSED -ge $ANALYSIS_DURATION ]; then
    echo "✅ 金丝雀分析通过！可以进入下一阶段"
    exit 0
  fi
  
  ERROR_RATE=$(get_error_rate)
  LATENCY=$(get_latency_p99)
  
  echo "⏱️  已运行 ${ELAPSED}秒 - 错误率: ${ERROR_RATE}, P99延迟: ${LATENCY}ms"
  
  # 检查是否超过阈值
  if (( $(echo "$ERROR_RATE > $ERROR_THRESHOLD / 100" | bc -l) )); then
    echo "❌ 错误率超过阈值 ($ERROR_THRESHOLD%)，自动回滚"
    kubectl delete deployment/$CANARY_DEPLOYMENT -n $NAMESPACE
    exit 1
  fi
  
  if (( $(echo "$LATENCY > $LATENCY_THRESHOLD" | bc -l) )); then
    echo "❌ P99延迟超过阈值 (${LATENCY_THRESHOLD}ms)，自动回滚"
    kubectl delete deployment/$CANARY_DEPLOYMENT -n $NAMESPACE
    exit 1
  fi
  
  sleep 10
done
