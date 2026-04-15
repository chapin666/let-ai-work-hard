# Source: chapter-18-ai-automation-test.md
# Lines: 545-553
# Language: javascript

// 坏：测试间共享数据
test('test1', () => { createUser('john'); });
test('test2', () => { expect(countUsers()).toBe(0); }); // 可能失败

// 好：测试数据隔离
test('test1', () => { createUser('john'); });
test('test2', () => { createUser('jane'); expect(countUsers()).toBe(1); });
