# Source: chapter-13-ai-backend.md
# Lines: 226-396
# Language: typescript

// user.service.ts
import {
  Injectable,
  NotFoundException,
  ConflictException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { QueryUserDto } from './dto/query-user.dto';
import * as bcrypt from 'bcrypt';

@Injectable()
export class UserService {
  constructor(private prisma: PrismaService) {}

  async findAll(query: QueryUserDto) {
    const { page = 1, pageSize = 10, keyword, status } = query;
    const skip = (page - 1) * pageSize;

    const where: any = {};
    if (keyword) {
      where.OR = [
        { username: { contains: keyword } },
        { email: { contains: keyword } },
      ];
    }
    if (status !== undefined) {
      where.status = status;
    }

    const [list, total] = await Promise.all([
      this.prisma.user.findMany({
        where,
        skip,
        take: pageSize,
        orderBy: { createdAt: 'desc' },
        select: {
          id: true,
          username: true,
          email: true,
          status: true,
          createdAt: true,
          roles: {
            select: {
              role: {
                select: { id: true, name: true },
              },
            },
          },
        },
      }),
      this.prisma.user.count({ where }),
    ]);

    return {
      list,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
    };
  }

  async findOne(id: number) {
    const user = await this.prisma.user.findUnique({
      where: { id },
      include: {
        roles: {
          include: {
            role: true,
          },
        },
      },
    });

    if (!user) {
      throw new NotFoundException(`用户 #${id} 不存在`);
    }

    return user;
  }

  async create(createUserDto: CreateUserDto) {
    const { username, email, password, roleIds } = createUserDto;

    // 检查用户名和邮箱是否已存在
    const existing = await this.prisma.user.findFirst({
      where: {
        OR: [{ username }, { email }],
      },
    });

    if (existing) {
      throw new ConflictException('用户名或邮箱已存在');
    }

    // 加密密码
    const hashedPassword = await bcrypt.hash(password, 10);

    // 创建用户
    const user = await this.prisma.user.create({
      data: {
        username,
        email,
        password: hashedPassword,
        roles: {
          create: roleIds?.map((roleId) => ({
            role: { connect: { id: roleId } },
          })),
        },
      },
      include: {
        roles: {
          include: { role: true },
        },
      },
    });

    // 不返回密码
    const { password: _, ...result } = user;
    return result;
  }

  async update(id: number, updateUserDto: UpdateUserDto) {
    await this.findOne(id); // 确保用户存在

    const { roleIds, password, ...data } = updateUserDto;

    // 如果更新密码，需要加密
    if (password) {
      data.password = await bcrypt.hash(password, 10);
    }

    // 更新角色关联
    let roleUpdate: any = {};
    if (roleIds) {
      roleUpdate = {
        roles: {
          deleteMany: {},
          create: roleIds.map((roleId) => ({
            role: { connect: { id: roleId } },
          })),
        },
      };
    }

    const user = await this.prisma.user.update({
      where: { id },
      data: {
        ...data,
        ...roleUpdate,
      },
      include: {
        roles: {
          include: { role: true },
        },
      },
    });

    const { password: _, ...result } = user;
    return result;
  }

  async remove(id: number) {
    await this.findOne(id);
    await this.prisma.user.delete({ where: { id } });
  }
}
