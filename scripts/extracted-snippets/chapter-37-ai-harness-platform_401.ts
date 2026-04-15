# Source: chapter-37-ai-harness-platform.md
# Lines: 401-412
# Language: typescript

interface ModelRouter {
  // 根据任务类型和成本选择最优模型
  selectModel(task: Task, constraints: Constraints): Model;
  
  // 支持模型降级（当主模型不可用时）
  fallback(primary: Model): Model;
  
  // 支持模型组合（复杂任务用多模型协作）
  ensemble(models: Model[], strategy: Strategy): Model;
}
