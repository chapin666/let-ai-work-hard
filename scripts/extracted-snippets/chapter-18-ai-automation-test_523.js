# Source: chapter-18-ai-automation-test.md
# Lines: 523-533
# Language: javascript

// 坏：测试依赖具体实现
test('opens modal', () => {
  fireEvent.click(screen.getByClass('btn-primary')); // class可能变
});

// 好：测试依赖行为
test('opens modal', () => {
  fireEvent.click(screen.getByRole('button', { name: /打开/i }));
});
