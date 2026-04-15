# Source: chapter-13-ai-backend.md
# Lines: 626-708
# Language: typescript

// guards/permissions.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PERMISSIONS_KEY } from '../decorators/permissions.decorator';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    private prisma: PrismaService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    // 获取需要的权限
    const requiredPermissions = this.reflector.getAllAndOverride<string[]>(
      PERMISSIONS_KEY,
      [context.getHandler(), context.getClass()],
    );

    // 如果没有标记权限，允许访问
    if (!requiredPermissions || requiredPermissions.length === 0) {
      return true;
    }

    // 获取当前用户
    const { user } = context.switchToHttp().getRequest();
    if (!user) {
      throw new ForbiddenException('未登录');
    }

    // 超级管理员直接通过
    if (user.isAdmin) {
      return true;
    }

    // 查询用户的所有权限
    const userWithRoles = await this.prisma.user.findUnique({
      where: { id: user.userId },
      include: {
        roles: {
          where: { role: { status: true } },
          include: {
            role: {
              include: {
                permissions: {
                  where: { permission: { status: true } },
                  include: { permission: true },
                },
              },
            },
          },
        },
      },
    });

    // 收集所有权限code
    const userPermissions = new Set<string>();
    userWithRoles?.roles.forEach((userRole) => {
      userRole.role.permissions.forEach((rolePermission) => {
        userPermissions.add(rolePermission.permission.code);
      });
    });

    // 检查是否拥有所有需要的权限
    const hasAllPermissions = requiredPermissions.every((permission) =>
      userPermissions.has(permission),
    );

    if (!hasAllPermissions) {
      throw new ForbiddenException('没有权限执行此操作');
    }

    return true;
  }
}
