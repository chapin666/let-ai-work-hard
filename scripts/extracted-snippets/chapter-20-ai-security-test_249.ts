# Source: chapter-20-ai-security-test.md
# Lines: 249-316
# Language: typescript

// tests/security/login.security.test.ts
import request from 'supertest';
import app from '../../app';

describe('Login API Security Tests', () => {
  describe('SQL Injection Prevention', () => {
    const sqlInjectionPayloads = [
      "' OR '1'='1",
      "' OR '1'='1' --",
      "admin'--",
      "1'; DROP TABLE users; --",
      "' UNION SELECT * FROM users --",
    ];

    sqlInjectionPayloads.forEach((payload) => {
      it(`should reject SQL injection attempt: ${payload.substring(0, 20)}...`, async () => {
        const response = await request(app)
          .post('/api/login')
          .send({ email: payload, password: 'password' });
        
        // 不应该返回成功登录
        expect(response.status).not.toBe(200);
        // 不应该包含数据库错误信息
        expect(response.body.error).not.toMatch(/sql|database|error/i);
      });
    });
  });

  describe('Brute Force Protection', () => {
    it('should block after 5 failed attempts', async () => {
      // 连续5次失败登录
      for (let i = 0; i < 5; i++) {
        await request(app)
          .post('/api/login')
          .send({ email: 'test@test.com', password: 'wrong' });
      }
      
      // 第6次应该被阻止
      const response = await request(app)
        .post('/api/login')
        .send({ email: 'test@test.com', password: 'wrong' });
      
      expect(response.status).toBe(429);
      expect(response.body.error).toContain('Too many attempts');
    });
  });

  describe('Information Leakage Prevention', () => {
    it('should not reveal if email exists', async () => {
      const validEmail = 'exists@test.com';
      const invalidEmail = 'notexists@test.com';
      
      const validResponse = await request(app)
        .post('/api/login')
        .send({ email: validEmail, password: 'wrong' });
      
      const invalidResponse = await request(app)
        .post('/api/login')
        .send({ email: invalidEmail, password: 'wrong' });
      
      // 两种情况的响应应该一致，不能让用户猜测哪些邮箱已注册
      expect(validResponse.status).toBe(invalidResponse.status);
      expect(validResponse.body.error).toBe(invalidResponse.body.error);
    });
  });
});
