# Source: chapter-17-ai-test-design.md
# Lines: 40-50
# Language: javascript

// 这样的代码，一行就能"覆盖"，但毫无意义
test('calculateTotal should return number', () => {
  expect(typeof calculateTotal(10, 2)).toBe('number');
});

// 真正的问题场景根本没测到
test('calculateTotal with edge cases', () => {
  // undefined? null? 负数? 超大数? 小数精度?
});
