# Source: chapter-18-ai-automation-test.md
# Lines: 48-54
# Language: javascript

// 为了测试而测试
test('should work', () => {
  const result = someFunction();
  expect(result).toBeDefined(); // 测了个寂寞
});
