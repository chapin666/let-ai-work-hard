# Source: chapter-14-ai-refactoring.md
# Lines: 394-444
# Language: typescript

// migrate-users.ts
import { PrismaClient } from '@prisma/client';
import { createConnection } from 'mysql2/promise';

const prisma = new PrismaClient();

async function migrateUsers() {
  // 连接旧数据库
  const oldDb = await createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'old_system',
  });

  // 读取旧数据
  const [oldUsers] = await oldDb.execute('SELECT * FROM users');

  console.log(`找到 ${oldUsers.length} 个用户需要迁移`);

  // 迁移数据
  for (const oldUser of oldUsers) {
    try {
      // 数据转换
      const newUser = {
        id: oldUser.id,
        username: oldUser.username,
        email: oldUser.email,
        // 密码需要重新加密
        password: await hashPassword(oldUser.password),
        status: mapStatus(oldUser.status),
        createdAt: new Date(oldUser.created_at),
        updatedAt: new Date(oldUser.updated_at),
      };

      // 写入新数据库
      await prisma.user.create({ data: newUser });

      console.log(`✓ 用户 ${oldUser.username} 迁移成功`);
    } catch (error) {
      console.error(`✗ 用户 ${oldUser.username} 迁移失败:`, error.message);
    }
  }

  console.log('迁移完成');
  process.exit(0);
}

migrateUsers().catch(console.error);
