# Source: chapter-18-ai-automation-test.md
# Lines: 235-239
# Language: javascript

// 正确的写法
const successMessage = await screen.findByText('加载完成', {}, { timeout: 4000 });
expect(successMessage).toBeInTheDocument();
