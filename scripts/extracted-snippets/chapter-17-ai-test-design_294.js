# Source: chapter-17-ai-test-design.md
# Lines: 294-459
# Language: javascript

// tests/auth/register.test.js
const request = require('supertest');
const app = require('../../app');
const { User } = require('../../models');
const { sendEmail } = require('../../services/email');

// Mock邮件服务
jest.mock('../../services/email');

describe('POST /api/auth/register', () => {
  // 每个测试前清理数据
  beforeEach(async () => {
    await User.deleteMany({});
    sendEmail.mockClear();
  });
  
  describe('正常注册流程', () => {
    test('使用有效邮箱和密码注册成功', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'SecurePass123'
        });
      
      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('message', '注册成功，请查收验证邮件');
      expect(response.body).toHaveProperty('userId');
      
      // 验证用户已创建但未激活
      const user = await User.findOne({ email: 'test@example.com' });
      expect(user).toBeTruthy();
      expect(user.isActive).toBe(false);
      expect(user.verificationToken).toBeTruthy();
      
      // 验证邮件已发送
      expect(sendEmail).toHaveBeenCalledWith({
        to: 'test@example.com',
        subject: '请验证您的邮箱',
        // ...
      });
    });
    
    test('验证邮件发送成功后可以激活账户', async () => {
      // 先注册
      const registerRes = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'SecurePass123'
        });
      
      const user = await User.findOne({ email: 'test@example.com' });
      const token = user.verificationToken;
      
      // 验证邮箱
      const verifyRes = await request(app)
        .get(`/api/auth/verify?token=${token}`);
      
      expect(verifyRes.status).toBe(200);
      
      // 验证用户已激活
      const updatedUser = await User.findOne({ email: 'test@example.com' });
      expect(updatedUser.isActive).toBe(true);
      expect(updatedUser.verificationToken).toBeNull();
    });
  });
  
  describe('邮箱验证', () => {
    test('使用无效邮箱格式应返回错误', async () => {
      const invalidEmails = [
        'notanemail',
        '@example.com',
        'test@',
        'test@.com',
        'test@example',
        ''
      ];
      
      for (const email of invalidEmails) {
        const response = await request(app)
          .post('/api/auth/register')
          .send({ email, password: 'SecurePass123' });
        
        expect(response.status).toBe(400);
        expect(response.body.errors).toContainEqual(
          expect.objectContaining({ field: 'email' })
        );
      }
    });
    
    test('使用已注册邮箱应返回错误', async () => {
      // 先注册一个用户
      await User.create({
        email: 'exists@example.com',
        password: 'hashedpassword',
        isActive: true
      });
      
      // 尝试用相同邮箱注册
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'exists@example.com',
          password: 'SecurePass123'
        });
      
      expect(response.status).toBe(409);
      expect(response.body.message).toContain('邮箱已被注册');
    });
  });
  
  describe('密码验证', () => {
    test('密码少于8位应返回错误', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'Short1'
        });
      
      expect(response.status).toBe(400);
      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'password', code: 'TOO_SHORT' })
      );
    });
    
    test('密码缺少大写字母应返回错误', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'lowercase123'
        });
      
      expect(response.status).toBe(400);
    });
    
    // ... 更多密码测试
  });
  
  describe('并发场景', () => {
    test('同时用相同邮箱注册应只有一个成功', async () => {
      const promises = Array(5).fill().map(() =>
        request(app)
          .post('/api/auth/register')
          .send({
            email: 'race@example.com',
            password: 'SecurePass123'
          })
      );
      
      const responses = await Promise.all(promises);
      
      const successCount = responses.filter(r => r.status === 201).length;
      const conflictCount = responses.filter(r => r.status === 409).length;
      
      expect(successCount).toBe(1);
      expect(conflictCount).toBe(4);
    });
  });
  
  // ... 更多测试
});
