# Source: chapter-18-ai-automation-test.md
# Lines: 266-280
# Language: javascript

// factories/user.factory.js
const { factory } = require('factory-bot');
const User = require('../models/User');

factory.define('user', User, {
  email: factory.sequence('email', (n) => `user${n}@test.com`),
  name: factory.chance('name'),
  role: 'developer',
  createdAt: new Date(),
});

// 使用示例
const user = await factory.create('user', { role: 'admin' });
