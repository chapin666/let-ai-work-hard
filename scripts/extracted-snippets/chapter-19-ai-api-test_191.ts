# Source: chapter-19-ai-api-test.md
# Lines: 191-210
# Language: typescript

// contracts/userProvider.pact.ts
import { Verifier } from '@pact-foundation/pact';

describe('Pact Verification', () => {
  it('validates the expectations of UserFrontend', async () => {
    await new Verifier({
      provider: 'UserService',
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: [path.resolve(process.cwd(), './pacts/UserFrontend-UserService.json')],
      stateHandlers: {
        'users exist': async () => {
          // 准备测试数据
          await seedUsers();
        },
      },
    }).verifyProvider();
  });
});
