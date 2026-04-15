# Source: chapter-25-ai-monitoring.md
# Lines: 273-308
# Language: bash

#!/bin/bash
# 每日监控巡检脚本

echo "=== 监控巡检报告 ==="
echo "时间: $(date)"

# 检查磁盘
echo -e "\n📁 磁盘空间检查:"
df -h | grep -E '^/dev/' | awk '{print $5 " " $6}' | while read usage mount; do
  usage_num=${usage%%%}
  if [ $usage_num -gt 90 ]; then
    echo "❌ $mount: $usage (紧急)"
  elif [ $usage_num -gt 80 ]; then
    echo "⚠️  $mount: $usage (警告)"
  else
    echo "✅ $mount: $usage"
  fi
done

# 检查内存
echo -e "\n🧠 内存检查:"
mem_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
echo "内存使用率: ${mem_usage}%"

# 检查僵尸进程
echo -e "\n👻 僵尸进程检查:"
zombie_count=$(ps aux | grep -c '[Zz]ombie')
if [ $zombie_count -gt 0 ]; then
  echo "⚠️  发现 $zombie_count 个僵尸进程"
else
  echo "✅ 无僵尸进程"
fi

echo -e "\n=== 巡检完成 ==="
