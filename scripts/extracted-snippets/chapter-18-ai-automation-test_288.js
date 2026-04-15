# Source: chapter-18-ai-automation-test.md
# Lines: 288-300
# Language: javascript

// 原来的测试 - 混乱不堪
test('user can login', async () => {
  // ... 50行准备代码
  await page.goto('/login');
  await sleep(1000); // 等页面加载
  await page.fill('input[type="email"]', 'test@test.com');
  await page.fill('input[type="password"]', 'password');
  await page.click('button'); // 没有选择器的按钮
  await sleep(2000); // 等跳转
  // ... 50行断言代码
});
