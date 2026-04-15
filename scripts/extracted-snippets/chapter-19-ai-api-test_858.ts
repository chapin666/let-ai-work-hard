# Source: chapter-19-ai-api-test.md
# Lines: 858-883
# Language: typescript

// 1. 分页响应模式
const paginatedResponse = {
  data: eachLike(itemMatcher),
  total: integer(),
  page: integer(),
  pageSize: integer(),
  hasMore: boolean(),
};

// 2. 错误响应模式
const errorResponse = {
  error: {
    code: string(),
    message: string(),
    details: optional(array()),
  },
};

// 3. 乐观更新模式
const optimisticUpdate = {
  id: integer(),
  status: oneOf(['pending', 'processing', 'completed', 'failed']),
  updatedAt: datetime(),
};
