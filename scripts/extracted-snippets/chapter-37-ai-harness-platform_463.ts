# Source: chapter-37-ai-harness-platform.md
# Lines: 463-474
# Language: typescript

interface ContextEngine {
  // 索引项目文档
  index(docs: Document[]): Promise<void>;
  
  // 根据查询检索相关上下文
  retrieve(query: string, options: RetrieveOptions): Context[];
  
  // 构建适合模型输入的上下文窗口
  buildWindow(contexts: Context[], maxTokens: number): string;
}
