# Source: chapter-38-ai-best-practices.md
# Lines: 254-274
# Language: typescript

// AI网关统一接口
interface AIGateway {
  // 代码生成
  generateCode(request: CodeGenRequest): Promise<CodeGenResponse>;
  
  // 代码评审
  reviewCode(request: ReviewRequest): Promise<ReviewResponse>;
  
  // 需求分析
  analyzeRequirement(request: RequirementRequest): Promise<AnalysisResponse>;
  
  // 知识问答
  answerQuestion(request: QnARequest): Promise<QnAResponse>;
  
  // 统一的能力
  logUsage(user: User, feature: string, tokens: number): void;
  checkQuota(user: User, feature: string): boolean;
  auditRequest(request: Request, response: Response): void;
}
