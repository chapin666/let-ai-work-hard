# Source: chapter-18-ai-automation-test.md
# Lines: 212-216
# Language: javascript

// 糟糕的写法
await sleep(2000); // 等2秒，希望页面加载完
expect(screen.getByText('加载完成')).toBeInTheDocument();
