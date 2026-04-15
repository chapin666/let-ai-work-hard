# Source: chapter-19-ai-api-test.md
# Lines: 393-439
# Language: typescript

// mocks/handlers.ts
import { rest } from 'msw';
import { faker } from '@faker-js/faker';

const generateUser = (id: number) => ({
  id,
  name: faker.person.fullName(),
  email: faker.internet.email(),
  avatar: faker.image.avatar(),
  role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
  createdAt: faker.date.past().toISOString(),
});

export const handlers = [
  // 用户列表
  rest.get('/api/users', (req, res, ctx) => {
    const page = parseInt(req.url.searchParams.get('page') || '1');
    const pageSize = parseInt(req.url.searchParams.get('pageSize') || '10');
    
    // 模拟延迟
    const delay = faker.number.int({ min: 100, max: 500 });
    
    const users = Array.from({ length: pageSize }, (_, i) => 
      generateUser((page - 1) * pageSize + i + 1)
    );
    
    return res(
      ctx.delay(delay),
      ctx.json({
        data: users,
        total: 100,
        page,
        pageSize,
      })
    );
  }),

  // 错误场景
  rest.get('/api/users/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ error: 'Internal Server Error' })
    );
  }),
];
