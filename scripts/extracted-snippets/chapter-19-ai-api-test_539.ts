# Source: chapter-19-ai-api-test.md
# Lines: 539-552
# Language: typescript

// 临时兼容处理
const normalizeVisibility = (visibility: string) => {
  // "team"在功能上等价于"internal"
  if (visibility === 'team') return 'internal';
  return visibility;
};

// 接口返回时转换
res.json({
  ...project,
  visibility: normalizeVisibility(project.visibility),
});
