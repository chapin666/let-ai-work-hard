# Source: chapter-23-ai-docker.md
# Lines: 786-805
# Language: bash

#!/bin/bash
# 容器安全扫描脚本

IMAGE=$1

echo "🔍 扫描镜像: $IMAGE"

# 使用Trivy扫描
trivy image --severity HIGH,CRITICAL $IMAGE

# 检查是否有root用户运行
if docker run --rm --entrypoint sh $IMAGE -c "whoami" | grep -q "root"; then
  echo "⚠️ 警告：容器以root用户运行"
fi

# 检查镜像大小
SIZE=$(docker images --format "{{.Size}}" $IMAGE)
echo "📦 镜像大小: $SIZE"
