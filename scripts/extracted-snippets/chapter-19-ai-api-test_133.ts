# Source: chapter-19-ai-api-test.md
# Lines: 133-188
# Language: typescript

// contracts/userConsumer.pact.ts
import { Pact } from '@pact-foundation/pact';
import { like, eachLike, integer, string, boolean } from '@pact-foundation/pact/dsl/matchers';

const provider = new Pact({
  consumer: 'UserFrontend',
  provider: 'UserService',
  port: 1234,
});

describe('User API Contract', () => {
  beforeAll(() => provider.setup());
  afterEach(() => provider.verify());
  afterAll(() => provider.finalize());

  describe('GET /api/users', () => {
    it('returns paginated list of users', async () => {
      // 定义期望的交互
      await provider.addInteraction({
        state: 'users exist',
        uponReceiving: 'a request for user list with pagination',
        withRequest: {
          method: 'GET',
          path: '/api/users',
          query: { page: '1', pageSize: '10' },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: {
            data: eachLike({
              id: integer(1),
              name: string('张三'),
              email: string('zhangsan@example.com'),
              avatar: string('https://example.com/avatar.jpg'),
              role: string('admin'),
              createdAt: string('2024-01-01T00:00:00Z'),
            }),
            total: integer(100),
            page: integer(1),
            pageSize: integer(10),
          },
        },
      });

      // 调用实际API
      const response = await fetchUsers({ page: 1, pageSize: 10 });
      
      // 验证响应
      expect(response.data).toHaveLength(1);
      expect(response.data[0].name).toBe('张三');
    });
  });
});
