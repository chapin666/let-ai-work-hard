# Source: chapter-14-ai-refactoring.md
# Lines: 469-575
# Language: typescript

// order.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { OrderService } from './order.service';
import { PrismaService } from '../prisma/prisma.service';

describe('OrderService', () => {
  let service: OrderService;
  let prisma: PrismaService;

  const mockPrisma = {
    order: {
      findMany: jest.fn(),
      findUnique: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      count: jest.fn(),
    },
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        OrderService,
        { provide: PrismaService, useValue: mockPrisma },
      ],
    }).compile();

    service = module.get<OrderService>(OrderService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  describe('findAll', () => {
    it('应该返回分页的订单列表', async () => {
      const mockOrders = [
        { id: 1, orderNo: 'ORD001', amount: 100 },
        { id: 2, orderNo: 'ORD002', amount: 200 },
      ];
      const mockTotal = 2;

      mockPrisma.order.findMany.mockResolvedValue(mockOrders);
      mockPrisma.order.count.mockResolvedValue(mockTotal);

      const result = await service.findAll({ page: 1, pageSize: 10 });

      expect(result.list).toEqual(mockOrders);
      expect(result.total).toBe(mockTotal);
      expect(result.page).toBe(1);
    });

    it('应该支持按状态筛选', async () => {
      const query = { page: 1, pageSize: 10, status: 'PENDING' };

      await service.findAll(query);

      expect(mockPrisma.order.findMany).toHaveBeenCalledWith(
        expect.objectContaining({
          where: { status: 'PENDING' },
        }),
      );
    });

    it('应该处理数据库错误', async () => {
      mockPrisma.order.findMany.mockRejectedValue(new Error('DB Error'));

      await expect(service.findAll({})).rejects.toThrow('查询订单失败');
    });
  });

  describe('create', () => {
    it('应该成功创建订单', async () => {
      const createData = {
        customerName: '张三',
        amount: 100,
        items: [{ productId: 1, quantity: 2 }],
      };

      const mockCreatedOrder = {
        id: 1,
        orderNo: 'ORD202401010001',
        ...createData,
      };

      mockPrisma.order.create.mockResolvedValue(mockCreatedOrder);

      const result = await service.create(createData);

      expect(result.orderNo).toMatch(/^ORD\d{14}\d{4}$/);
      expect(result.customerName).toBe(createData.customerName);
    });

    it('订单号应该唯一', async () => {
      mockPrisma.order.create
        .mockRejectedValueOnce({ code: 'P2002' })
        .mockResolvedValueOnce({ id: 1, orderNo: 'ORD001' });

      const result = await service.create({});

      expect(mockPrisma.order.create).toHaveBeenCalledTimes(2);
      expect(result).toBeDefined();
    });
  });

  // ... 更多测试用例
});
