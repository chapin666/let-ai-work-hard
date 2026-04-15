# Source: chapter-18-ai-automation-test.md
# Lines: 536-542
# Language: javascript

// 坏：依赖固定时间
await sleep(1000);

// 好：等待条件
await waitFor(() => expect(element).toBeVisible());
