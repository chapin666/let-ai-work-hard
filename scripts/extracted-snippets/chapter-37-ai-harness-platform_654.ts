# Source: chapter-37-ai-harness-platform.md
# Lines: 654-665
# Language: typescript

// 简单任务用便宜模型，复杂任务用强模型
function routeModel(task: Task): Model {
  if (task.complexity < 0.3) {
    return 'gpt-3.5-turbo';  // 便宜
  } else if (task.complexity < 0.7) {
    return 'claude-3-haiku'; // 性价比
  } else {
    return 'gpt-4';          // 最强
  }
}
