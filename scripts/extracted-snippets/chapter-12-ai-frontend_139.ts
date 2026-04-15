# Source: chapter-12-ai-frontend.md
# Lines: 139-179
# Language: typescript

// 生成的代码结构
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button, Table, Modal, Form, Input, Select, message } from '@/components';
import { userApi } from '@/api/user';
import type { User, UserQuery, CreateUserDto } from './types';

// 表单验证schema
const userSchema = z.object({
  username: z.string().min(2, '用户名至少2个字符'),
  phone: z.string().regex(/^1[3-9]\d{9}$/, '手机号格式不正确'),
  role: z.enum(['admin', 'user', 'guest']),
  status: z.enum(['active', 'inactive']),
});

export default function UserList() {
  // 搜索状态
  const [query, setQuery] = useState<UserQuery>({
    page: 1,
    pageSize: 10,
    keyword: '',
    status: undefined,
  });
  
  // 弹窗状态
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  
  // 数据请求
  const { data, isLoading } = useQuery({
    queryKey: ['users', query],
    queryFn: () => userApi.getList(query),
  });
  
  // ... 更多代码
}
