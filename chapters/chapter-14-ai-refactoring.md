# 第14章：让遗留项目焕发新生的手术

> **AI辅助代码重构实战**

---

## 故事：小陈的重构挑战

### 周一：接手"古董"项目

"小陈，有个重要任务交给你。"技术总监王总把他叫进办公室。

"咱们公司的核心订单系统，你知道吧？"

"知道，那个用了5年的老系统？"小陈点点头。

"对，就是它。"王总叹了口气，"这个系统现在问题太多了：
- 代码耦合严重，改一个地方崩三个地方
- 技术栈老旧，jQuery + PHP，招不到人维护
- 性能极差，高峰期经常卡死
- 没有任何文档，只有几个老员工勉强能看懂

"公司决定重构这个系统，用现代化的技术栈重写。预估工期..."王总顿了顿，"至少半年。"

小陈心里一沉。半年？那可是180天的工作量。

"但我有个想法，"王总看着小陈，"听说你最近用AI辅助开发，效率很高。要不要试试用AI来辅助重构？"

小陈想了想："王总，我愿意试试。但我有个条件——给我两周时间做技术调研和方案设计，如果方案可行，再正式启动。"

"成交。"

---

### 周二：诊断病情

周二，小陈开始"诊断"这个遗留项目。

他先把项目结构克隆到本地，一打开就倒吸一口凉气：

```
order-system/
├── admin/              # 后台管理
│   ├── js/
│   │   ├── app.js      # 5000+行
│   │   ├── utils.js    # 3000+行
│   │   └── ...
│   ├── css/
│   └── index.html
├── api/                # 后端接口
│   ├── order.php       # 8000+行
│   ├── user.php
│   └── db.php
└── assets/
```

"这...这根本没有任何架构可言。"小陈感到头皮发麻。

他没有急着动手，而是打开AI助手，开始系统性地分析。

**第一步：代码分析**

```
请帮我分析这个遗留项目的代码结构和问题：

项目背景：
- 5年历史的老项目
- 前端：jQuery + 原生JS
- 后端：PHP
- 核心文件几千行，没有模块化

[粘贴关键代码片段]

请分析：
1. 代码的主要问题有哪些？（按严重程度排序）
2. 技术债务的分布情况
3. 重构的风险点
4. 建议的重构策略（渐进式 vs 大爆炸式）
```

AI给出了详细的分析报告：

> **代码问题分析**：
> 
> **严重问题（必须修复）**：
> 1. **全局变量污染** - 所有变量都在全局命名空间
> 2. **没有模块化** - 代码耦合严重，无法独立测试
> 3. **重复代码** - 同样的逻辑散落在各处
> 4. **没有错误处理** - 代码随时可能崩溃
> 
> **中等问题（建议修复）**：
> 1. **没有类型系统** - 容易出错，维护困难
> 2. **DOM操作混乱** - 直接操作DOM，性能差
> 3. **API设计不规范** - 接口混乱，没有统一规范
> 
> **重构策略建议**：
> 采用**渐进式重构**：
> 1. 第一阶段：模块化改造（不改动功能）
> 2. 第二阶段：技术栈升级（jQuery → React）
> 3. 第三阶段：架构优化（分层、解耦）
> 4. 第四阶段：性能优化和测试覆盖
> 
> **为什么不推荐大爆炸式重构**：
> - 项目复杂度高，重写风险大
> - 业务逻辑复杂，容易遗漏
> - 重构期间需要维护两个版本，成本高

**第二步：制定重构计划**

小陈根据AI的建议，制定了详细的重构计划：

```
请帮我制定一个渐进式重构方案：

项目概况：
- 前端：jQuery项目，约2万行JS代码
- 后端：PHP项目，约1.5万行代码
- 核心功能：订单管理、用户管理、报表统计

目标技术栈：
- 前端：React + TypeScript + Vite
- 后端：NestJS + Prisma + PostgreSQL

请制定：
1. 分阶段重构计划（每阶段1-2周）
2. 每个阶段的具体任务
3. 风险控制和回滚方案
4. 验收标准
```

AI生成的重构计划：

> **重构路线图**：
> 
> **阶段1：模块化改造（第1-2周）**
> - 目标：将代码从面条式改造为模块化，不改动功能
> - 前端：使用Webpack打包，将代码拆分为模块
> - 后端：使用Composer管理依赖，拆分Service层
> - 风险：低（只是代码移动，逻辑不变）
> 
> **阶段2： strangler fig模式（第3-6周）**
> - 目标：逐步替换功能模块
> - 方法：新功能用新架构，旧功能逐步迁移
> - 使用proxy模式将请求路由到新旧系统
> 
> **阶段3：核心模块重构（第7-10周）**
> - 订单管理模块重构
> - 用户管理模块重构
> - 报表统计重构
> 
> **阶段4：收尾优化（第11-12周）**
> - 性能优化
> - 测试覆盖
> - 文档完善
> - 旧系统下线

---

### 周三：第一阶段——模块化改造

周三开始，小陈启动第一阶段重构。

**前端模块化**

```
请帮我将以下jQuery代码改造为模块化结构：

原始代码：
[粘贴app.js的部分代码]

目标：
- 使用ES6模块（import/export）
- 按功能拆分文件
- 保持现有功能不变
- 使用Webpack打包

请生成：
1. 新的目录结构
2. 拆分后的模块文件
3. Webpack配置
4. 迁移步骤
```

AI生成的方案：

> **新目录结构**：> ```> src/> ├── modules/> │   ├── order/        # 订单相关> │   │   ├── index.js  # 统一导出> │   │   ├── list.js   # 订单列表> │   │   ├── detail.js # 订单详情> │   │   └── utils.js  # 订单工具函数> │   ├── user/         # 用户相关> │   └── report/       # 报表相关> ├── utils/            # 通用工具> ├── components/       # 通用组件> └── app.js           # 入口文件> ```

AI还生成了具体的代码拆分示例：

```javascript
// src/modules/order/list.js
// 原app.js中订单列表相关代码提取

import { formatDate, formatMoney } from '../../utils/format';
import { showToast, showConfirm } from '../../components/dialog';

/**
 * 订单列表模块
 */
export class OrderList {
  constructor(container) {
    this.container = container;
    this.currentPage = 1;
    this.pageSize = 20;
    this.filters = {};
  }

  /**
   * 初始化列表
   */
  init() {
    this.bindEvents();
    this.loadData();
  }

  /**
   * 绑定事件
   */
  bindEvents() {
    // 搜索按钮
    this.container.on('click', '.js-search', () => {
      this.handleSearch();
    });

    // 分页按钮
    this.container.on('click', '.js-page', (e) => {
      const page = $(e.currentTarget).data('page');
      this.goToPage(page);
    });

    // ... 其他事件绑定
  }

  /**
   * 加载数据
   */
  async loadData() {
    try {
      showLoading();
      const response = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          page: this.currentPage,
          pageSize: this.pageSize,
          ...this.filters,
        }),
      });

      const data = await response.json();
      this.render(data);
    } catch (error) {
      showToast('加载失败：' + error.message);
    } finally {
      hideLoading();
    }
  }

  /**
   * 渲染列表
   */
  render(data) {
    const html = data.list.map(order => `
      <tr data-id="${order.id}">
        <td>${order.orderNo}</td>
        <td>${order.customerName}</td>
        <td>${formatMoney(order.amount)}</td>
        <td>${this.renderStatus(order.status)}</td>
        <td>${formatDate(order.createdAt)}</td>
        <td>
          <button class="btn-view" data-id="${order.id}">查看</button>
          <button class="btn-edit" data-id="${order.id}">编辑</button>
        </td>
      </tr>
    `).join('');

    this.container.find('.order-table tbody').html(html);
    this.renderPagination(data.total);
  }

  // ... 其他方法
}
```

小陈按照AI的方案，逐步将代码模块化。虽然没有改动业务逻辑，但代码结构清晰多了。

**后端Service层拆分**

同样地，他用AI辅助拆分PHP代码：

```
请帮我将以下PHP代码拆分为Service层：

原始代码：
[粘贴order.php的代码]

目标：
- 分离Controller层（路由处理）
- 分离Service层（业务逻辑）
- 分离Repository层（数据访问）
- 保持API接口不变

请生成：
1. OrderController.php
2. OrderService.php
3. OrderRepository.php
4. 依赖注入配置
```

---

### 周四：第二阶段—— strangler fig模式

模块化改造完成后，小陈启动了第二阶段：用"绞杀者模式"逐步替换旧系统。

**什么是绞杀者模式？**

```
绞杀者模式（Strangler Fig Pattern）：

就像绞杀榕慢慢包裹并取代宿主树一样，
我们在旧系统外围构建新系统，
逐步将功能从旧系统迁移到新系统，
最终让新系统完全取代旧系统。

优点：
- 风险可控，逐步迁移
- 可以回滚
- 不影响业务运行
```

**实施步骤**

小陈搭建了一个API网关，将请求路由到新旧系统：

```javascript
// gateway.js - API网关
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// 新系统已完成的模块
const newSystemModules = [
  '/api/v2/orders',      // 新订单模块
  '/api/v2/users',       // 新用户模块
];

// 路由中间件
app.use((req, res, next) => {
  const isNewModule = newSystemModules.some(prefix =>
    req.path.startsWith(prefix)
  );

  if (isNewModule) {
    // 路由到新系统（NestJS）
    proxyToNewSystem(req, res, next);
  } else {
    // 路由到旧系统（PHP）
    proxyToOldSystem(req, res, next);
  }
});
```

然后，他开始逐个模块重构。第一个选择的是**用户管理模块**——相对独立，影响面小。

```
请帮我重构用户管理模块：

旧系统功能（PHP）：
- 用户列表查询
- 用户CRUD
- 用户权限检查
- 用户登录/登出

目标技术栈：
- NestJS + TypeScript
- Prisma + PostgreSQL
- JWT认证

请生成：
1. 数据库Schema（Prisma）
2. 完整的新系统代码（Controller/Service/DTO）
3. 数据迁移脚本（从旧数据库迁移到新数据库）
4. 功能对比测试用例
```

AI生成了完整的重构代码，小陈只需要做少量的调整就能运行。

**数据迁移**

最复杂的是数据迁移。小陈用AI生成了迁移脚本：

```typescript
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
```

---

### 周五：自动化测试保障

重构最怕什么？引入新bug。小陈决定用AI生成自动化测试来保障质量。

**生成测试用例**

```
请为以下代码生成完整的单元测试：

[粘贴OrderService代码]

要求：
- 使用Jest
- 覆盖所有方法
- 包含正常情况和异常情况
- Mock数据库依赖
- 测试覆盖率90%以上
```

AI生成的测试代码：

```typescript
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
```

**回归测试**

小陈还用AI生成了回归测试脚本，确保重构后的功能与旧系统一致：

```typescript
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
```

---

### 第二周：收获与成果

两周过去，小陈向王总汇报重构进展：

**已完成**：
1. ✓ 代码模块化改造（前端+后端）
2. ✓ 用户管理模块重构完成
3. ✓ 自动化测试覆盖80%+
4. ✓ 数据迁移脚本完成
5. ✓ 新旧系统并行运行稳定

**效果对比**：

| 指标 | 旧系统 | 新系统 | 提升 |
|:---|:---|:---|:---:|
| 代码行数 | 35,000行 | 8,000行 | 77%↓ |
| 平均响应时间 | 1.2s | 0.15s | 87%↓ |
| 测试覆盖率 | 0% | 85% | +85% |
| 构建时间 | 无构建 | 30s | 现代化 |
| 部署时间 | 手动FTP | 自动化CI/CD | 自动化 |

王总看完报告，非常满意：

"小陈，你这两周的成果，比预期好太多了。特别是用AI辅助生成测试用例，这个想法很棒。"

"王总，其实这还只是开始。"小陈说，"按照这个节奏，我估计整个重构可以在2个月内完成，而不是原计划的半年。"

"2个月？"王总眼睛一亮，"那就太好了。"他顿了顿，"对了，你愿意给全公司做个分享吗？讲讲你是怎么用AI辅助重构的。"

"当然愿意！"

---

## 理论：AI辅助代码重构的系统方法

### 遗留项目的典型症状

| 症状 | 表现 | 重构优先级 |
|:---|:---|:---:|
| 意大利面条代码 | 没有模块，几千行一个文件 | 🔴 高 |
| 技术栈过时 | jQuery/PHP等老旧技术 | 🔴 高 |
| 全局变量污染 | 命名冲突，难以追踪 | 🔴 高 |
| 无测试覆盖 | 改代码必出bug | 🔴 高 |
| 无文档 | 只有当事人能维护 | 🟡 中 |
| 性能低下 | 卡顿、崩溃 | 🟡 中 |
| 重复代码 | 多处实现同样逻辑 | 🟡 中 |

### 重构策略选择

```
┌─────────────────────────────────────────────────────────┐
│                    重构策略选择矩阵                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   系统复杂度                                            │
│       高 │                                              │
│          │   绞杀者模式（Strangler Fig）                │
│          │   ─────────────────────────────              │
│          │   逐步替换，风险可控                         │
│          │                                              │
│          │                    大爆炸重构（Big Bang）    │
│       低 │ ─────────────────────────────────────────────│
│          │ 重写成本 < 改造成本时采用                    │
│          │                                              │
│          └──────────────────────────────────────────────┤
│                     业务关键性                          │
│                     低 ────────────> 高                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 渐进式重构的5个阶段

```
阶段1：准备工作（1周）
├── 代码分析（用AI识别问题）
├── 制定重构计划
├── 搭建新基础设施
└── 建立测试基线

阶段2：模块化改造（2周）
├── 前端模块化（Webpack + ES6）
├── 后端分层（Controller/Service/Repository）
├── 提取公共代码
└── 添加基础测试

阶段3：绞杀者模式（4-6周）
├── 搭建API网关
├── 逐个模块重构
├── 数据迁移
└── 回归测试

阶段4：技术栈升级（2-3周）
├── jQuery → React/Vue
├── 后端框架升级
├── 数据库迁移
└── 性能优化

阶段5：收尾优化（1-2周）
├── 完善测试覆盖
├── 文档更新
├── 团队培训
└── 旧系统下线
```

### AI在重构中的角色

| 重构任务 | AI辅助方式 | 价值 |
|:---|:---|:---:|
| 代码分析 | 识别代码异味、技术债务 | ⭐⭐⭐ |
| 方案设计 | 生成重构计划 | ⭐⭐⭐ |
| 代码拆分 | 模块化改造 | ⭐⭐⭐ |
| 新代码生成 | 用新框架重写 | ⭐⭐⭐ |
| 测试生成 | 单元测试、集成测试 | ⭐⭐⭐ |
| 数据迁移 | 生成迁移脚本 | ⭐⭐⭐ |
| 文档生成 | API文档、架构图 | ⭐⭐ |

---

## 实践：建立你的AI辅助重构工作流

### Step 1：代码诊断

```
请帮我分析这个项目的代码质量：

[粘贴代码]

请分析：
1. 代码异味（Code Smells）
2. 设计问题
3. 安全风险
4. 性能瓶颈
5. 重构优先级建议
```

### Step 2：制定重构计划

```
请帮我制定重构计划：

项目现状：
[描述]

目标状态：
[描述]

请生成：
1. 分阶段重构路线图
2. 每个阶段的任务清单
3. 风险评估
4. 回滚方案
5. 验收标准
```

### Step 3：模块化改造

```
请帮我把这段代码模块化：

原始代码：
[粘贴代码]

请：
1. 识别可以提取的模块
2. 生成模块化的代码结构
3. 保持功能不变
4. 添加模块间接口
```

### Step 4：代码重写

```
请用[新框架/技术]重写这段代码：

原始代码：
[粘贴代码]

目标技术栈：
[描述]

要求：
- 功能完全一致
- 使用新技术的最佳实践
- 添加类型定义
- 包含错误处理
```

### Step 5：生成测试

```
请为这段代码生成单元测试：

[粘贴代码]

要求：
- 使用[Jest/Vitest]
- 覆盖所有分支
- 包含Mock
- 测试覆盖率90%+
```

---

## 本章交付物

完成本章后，你应该拥有：

1. **重构分析模板**
   - 代码质量检查清单
   - 技术债务评估表
   - 重构计划模板

2. **AI辅助重构Prompt库**
   - 代码分析Prompt
   - 模块化Prompt
   - 代码重写Prompt
   - 测试生成Prompt

3. **一次实际重构经验**
   - 完成至少一个模块的重构
   - 建立重构工作流

---

## 行动清单

- [ ] 分析你手头的遗留项目，识别技术债务
- [ ] 使用AI生成代码质量报告
- [ ] 制定重构计划（渐进式或绞杀者模式）
- [ ] 选择一个低风险模块进行试点重构
- [ ] 用AI辅助生成单元测试
- [ ] 建立自动化回归测试
- [ ] 记录重构过程，形成团队知识

---

## 本章彩蛋

### 彩蛋1：代码异味检测Prompt

```
请检查这段代码中的"代码异味"：

[粘贴代码]

请识别以下问题：
1. 过长函数（>50行）
2. 过多参数（>4个）
3. 重复代码
4. 魔法数字
5. 深层嵌套（>3层）
6. 命名不规范
7. 注释过多或过少

对于每个问题，给出：
- 位置
- 问题描述
- 重构建议
```

### 彩蛋2：技术债务量化

```
请帮我量化这个项目的"技术债务"：

项目信息：
[描述]

请从以下维度评估：
1. 可维护性（1-10分）
2. 可测试性（1-10分）
3. 可扩展性（1-10分）
4. 安全性（1-10分）
5. 性能（1-10分）

给出：
- 每个维度的得分和理由
- 整体技术债务等级（低/中/高/极高）
- 优先修复建议
```

### 彩蛋3：自动生成迁移脚本

```
请帮我生成从[旧技术]到[新技术]的迁移脚本：

示例：
- jQuery选择器 → 原生querySelector
- 回调函数 → async/await
- var → let/const
- function → arrow function

[粘贴代码]

请生成完整的迁移脚本或代码转换方案。
```

---

> **小陈的重构心得**：> 
> "接手这个遗留项目的时候，我觉得这是个'不可能完成的任务'。
> 35,000行烂代码，5年技术债务，预计半年工期。
> 
> 但用AI辅助重构后，我发现：
> 1. AI可以快速识别代码问题，比人工审查快10倍
> 2. AI可以生成高质量的新代码，遵循最佳实践
> 3. AI可以自动生成测试，保障重构质量
> 4. AI可以生成迁移脚本，自动化重复工作
> 
> 重构不再是'体力活'，而是'指挥活'。
> 我负责制定策略、把控质量、处理复杂逻辑，
> AI负责执行具体任务、生成代码、验证结果。
> 
> 两周时间，我完成了原计划的两个月工作量。
> 更重要的是，我建立了一套可复制的AI辅助重构方法论。
> 
> 遗留项目不是噩梦，
> 没有AI的重构才是噩梦。
> 
> **让AI卷，我躺平。**"

---

**下一章预告**：第15章《让代码审查不再痛苦》——小陈将学习如何用AI辅助代码审查，从"怕别人看自己的代码"到"主动邀请别人 review"。通过AI预检、自动化工具、最佳实践，他把代码审查从"折磨"变成了"学习机会"。
