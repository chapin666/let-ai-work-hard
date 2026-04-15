# Source: chapter-14-ai-refactoring.md
# Lines: 581-630
# Language: typescript

// regression-test.ts
/**
 * 回归测试：对比新旧系统API响应
 */
import axios from 'axios';
import { deepStrictEqual } from 'assert';

const OLD_API = 'http://localhost:8080/api';
const NEW_API = 'http://localhost:3000/api/v2';

async function compareEndpoints(endpoint: string) {
  console.log(`测试接口: ${endpoint}`);

  const [oldResponse, newResponse] = await Promise.all([
    axios.get(`${OLD_API}${endpoint}`),
    axios.get(`${NEW_API}${endpoint}`),
  ]);

  try {
    // 对比响应结构
    deepStrictEqual(
      Object.keys(oldResponse.data).sort(),
      Object.keys(newResponse.data).sort(),
    );

    console.log('✓ 接口结构一致');
  } catch (error) {
    console.error('✗ 接口结构不一致:', error.message);
    process.exit(1);
  }
}

async function runRegressionTests() {
  const endpoints = [
    '/users',
    '/orders',
    '/orders/123',
    '/reports/sales',
  ];

  for (const endpoint of endpoints) {
    await compareEndpoints(endpoint);
  }

  console.log('\n所有回归测试通过！');
}

runRegressionTests();
