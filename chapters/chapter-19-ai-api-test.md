# 第19章：让前后端不再扯皮的契约测试

> **AI辅助API测试——用契约让前后端协作更顺畅**

---

## 故事：前后端的"罗生门"

### 周三下午：又双叒叕出问题了

"小王，用户列表接口返回的数据结构变了？"前端开发小林在群里@他。

小王心里一沉："不会吧，我没改过这个接口啊。"

他赶紧打开Postman测试，接口正常返回，数据结构也没变。

"没变啊，你那边看到什么问题？"

小林发来一张截图："你看，user对象里少了avatar字段，导致头像显示不了。"

小王瞪大眼睛："avatar字段？那个字段两个月前就标记为废弃了，我在文档里写了啊！"

"什么文档？"

"Swagger文档啊。"

"我没看Swagger，我直接看你的代码返回值写的..."小林无奈地说。

小王无语了。这已经是一个月内第三次因为接口"误会"导致的问题了：

- 第一次：小王加了新字段，前端没更新类型定义，导致TS报错
- 第二次：小林改了参数名（拼写错误修正），小王这边没同步，接口404
- 第三次：就是这次，字段被移除但前端不知道

**最可怕的是**，这些问题在本地开发时都不一定能发现——因为Mock数据和真实接口往往不同步。

只有到联调阶段，甚至上线后，问题才会暴露。

---


![API测试流程](../images/chapter-19-api-test-flow.svg)



### 周五复盘会：谁在甩锅？

周五的复盘会上，前后端各执一词。

**前端说**：
- "后端改接口不通知"
- "文档总是过期的"
- "Mock数据和真实接口对不上"

**后端说**：
- "加了字段是兼容的，前端应该能正常处理"
- "Swagger写了啊，谁让你们不看"
- "我本地测试是好的，肯定是前端调用方式不对"

产品经理听得头疼："那解决方案呢？"

大家沉默。

小王举手："我最近在研究契约测试（Contract Testing），可能能解决我们的问题。"

"什么测试？"大家问。

"就是让前后端先约定好接口契约，然后双方各自根据契约开发和测试。如果有一方违反了契约，测试就会失败，问题在开发阶段就能发现，而不是联调时。"

"听起来不错，"产品经理说，"需要多长时间实施？"

"给我一周时间做试点，如果效果好再推广。"

---

### 第一周：理解契约测试

小王没有急着动手，而是先深入理解契约测试的理念。

**什么是契约测试？**

```
传统流程：
后端开发 → 前端开发 → 联调 → 发现问题 → 互相甩锅 → 延期

契约测试流程：
约定契约 → 后端开发（按契约） → 前端开发（按契约）
   ↑                                        ↓
   └──────── 契约测试失败，早发现问题 ──────┘
```

**核心思想**：
- 消费者（前端）定义它需要什么数据
- 提供者（后端）保证它提供什么数据
- 契约就是双方的"合同"

**与传统API测试的区别**：

| 传统API测试 | 契约测试 |
|:---|:---|
| 测试整个API | 测试数据格式契约 |
| 需要真实服务 | 可以Mock |
| 在集成阶段发现问题 | 在开发阶段发现问题 |
| 测试所有端点 | 只测试双方约定的契约 |

小王决定使用**Pact**作为契约测试框架，这是业界最流行的选择。

---

### 第二周：AI辅助搭建契约测试

#### Day 1：用AI设计契约

小王先用AI帮团队设计第一个契约。

他描述了需求：

```
我们需要设计一个获取用户列表的API契约。

需求：
- 支持分页（page, pageSize）
- 支持搜索（keyword可选）
- 返回用户列表和总数
- 每个用户包含：id, name, email, avatar, role, createdAt

请用Pact DSL生成：
1. 消费者端（前端）的契约定义
2. 提供者端（后端）的契约验证
3. 契约文档（Markdown格式）

技术栈：前端React + TypeScript，后端Node.js + Express
```

AI生成了完整的契约定义：

**消费者端（Frontend）**：
```typescript
// contracts/userConsumer.pact.ts
import { Pact } from '@pact-foundation/pact';
import { like, eachLike, integer, string, boolean } from '@pact-foundation/pact/dsl/matchers';

const provider = new Pact({
  consumer: 'UserFrontend',
  provider: 'UserService',
  port: 1234,
});

describe('User API Contract', () => {
  beforeAll(() => provider.setup());
  afterEach(() => provider.verify());
  afterAll(() => provider.finalize());

  describe('GET /api/users', () => {
    it('returns paginated list of users', async () => {
      // 定义期望的交互
      await provider.addInteraction({
        state: 'users exist',
        uponReceiving: 'a request for user list with pagination',
        withRequest: {
          method: 'GET',
          path: '/api/users',
          query: { page: '1', pageSize: '10' },
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: {
            data: eachLike({
              id: integer(1),
              name: string('张三'),
              email: string('zhangsan@example.com'),
              avatar: string('https://example.com/avatar.jpg'),
              role: string('admin'),
              createdAt: string('2024-01-01T00:00:00Z'),
            }),
            total: integer(100),
            page: integer(1),
            pageSize: integer(10),
          },
        },
      });

      // 调用实际API
      const response = await fetchUsers({ page: 1, pageSize: 10 });
      
      // 验证响应
      expect(response.data).toHaveLength(1);
      expect(response.data[0].name).toBe('张三');
    });
  });
});
```

**提供者端（Backend）**：
```typescript
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
```

**契约文档**：
```markdown
# 用户列表API契约

## 端点
`GET /api/users`

## 请求参数
| 参数 | 类型 | 必需 | 说明 |
|-----|------|-----|------|
| page | integer | 是 | 页码，从1开始 |
| pageSize | integer | 是 | 每页条数 |
| keyword | string | 否 | 搜索关键词 |

## 响应格式
```json
{
  "data": [
    {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com",
      "avatar": "https://example.com/avatar.jpg",
      "role": "admin",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "pageSize": 10
}
```
```

#### Day 2：AI辅助契约维护

契约建立后，最大的问题是**维护**。

当接口需要变更时，如何保证契约同步更新？小王用AI设计了一套工作流：

**Prompt - 契约变更影响分析**：
```
我计划对以下API进行变更，请分析对契约的影响：

当前契约：
[粘贴当前契约]

计划变更：
1. 移除avatar字段（改用单独的获取头像接口）
2. 添加status字段（active/inactive）
3. 修改createdAt格式（从ISO字符串改为时间戳）

请分析：
1. 哪些是破坏性变更（breaking change）？
2. 对前后端各有什么影响？
3. 推荐的迁移方案（如何平滑过渡）
4. 新版本的契约定义
```

AI给出了详细的分析报告：

```markdown
## 变更影响分析

### 破坏性变更
- **移除avatar字段**：前端如果使用该字段，会undefined
- **修改createdAt格式**：前端如果做日期解析，会失败

### 非破坏性变更
- **添加status字段**：新增字段是兼容的

### 迁移方案
建议采用渐进式迁移：

**阶段1（兼容期）**：
- avatar字段保留但标记为deprecated
- createdAt同时返回两种格式
- 添加status字段

**阶段2（切换期）**：
- 通知前端使用新字段
- 监控avatar字段的使用情况

**阶段3（清理期）**：
- 移除avatar字段
- 只保留时间戳格式的createdAt
```

#### Day 3-4：集成到CI/CD

契约测试必须集成到CI中才有价值。小王用AI生成了完整的CI配置：

```yaml
# .github/workflows/contract-test.yml
name: Contract Tests

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  # 消费者契约测试
  consumer-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run consumer contract tests
        run: |
          cd frontend
          npm ci
          npm run test:contract
          
      - name: Upload pact files
        uses: actions/upload-artifact@v3
        with:
          name: pacts
          path: frontend/pacts/

  # 提供者契约验证
  provider-verify:
    needs: consumer-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Download pact files
        uses: actions/download-artifact@v3
        with:
          name: pacts
          path: pacts/
          
      - name: Start provider service
        run: |
          cd backend
          npm ci
          npm run start:test &
          sleep 5
          
      - name: Verify provider
        run: |
          cd backend
          npm run test:contract:verify

  # 契约兼容性检查
  can-i-deploy:
    needs: [consumer-test, provider-verify]
    runs-on: ubuntu-latest
    steps:
      - name: Check if safe to deploy
        run: |
          docker run --rm \
            -e PACT_BROKER_BASE_URL=${{ secrets.PACT_BROKER_URL }} \
            -e PACT_BROKER_TOKEN=${{ secrets.PACT_BROKER_TOKEN }} \
            pactfoundation/pact-cli:latest \
            can-i-deploy \
            --pacticipant UserFrontend \
            --version ${{ github.sha }} \
            --to-environment production
```

#### Day 5：AI生成Mock服务

最让小王惊喜的是，AI还能基于契约自动生成Mock服务。

```
请基于以下Pact契约，生成一个Mock服务器：

契约文件：
[粘贴契约JSON]

要求：
1. 使用MSW（Mock Service Worker）
2. 支持动态数据生成（使用faker）
3. 支持延迟模拟
4. 包含错误场景（404, 500等）
```

AI生成的Mock服务代码：

```typescript
// mocks/handlers.ts
import { rest } from 'msw';
import { faker } from '@faker-js/faker';

const generateUser = (id: number) => ({
  id,
  name: faker.person.fullName(),
  email: faker.internet.email(),
  avatar: faker.image.avatar(),
  role: faker.helpers.arrayElement(['admin', 'user', 'guest']),
  createdAt: faker.date.past().toISOString(),
});

export const handlers = [
  // 用户列表
  rest.get('/api/users', (req, res, ctx) => {
    const page = parseInt(req.url.searchParams.get('page') || '1');
    const pageSize = parseInt(req.url.searchParams.get('pageSize') || '10');
    
    // 模拟延迟
    const delay = faker.number.int({ min: 100, max: 500 });
    
    const users = Array.from({ length: pageSize }, (_, i) => 
      generateUser((page - 1) * pageSize + i + 1)
    );
    
    return res(
      ctx.delay(delay),
      ctx.json({
        data: users,
        total: 100,
        page,
        pageSize,
      })
    );
  }),

  // 错误场景
  rest.get('/api/users/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ error: 'Internal Server Error' })
    );
  }),
];
```

---

### 第三周：实战验证

契约测试体系搭建完成，小王找了一个小功能来实战验证。

**场景**：新增"项目设置"页面，需要调用以下接口：
1. `GET /api/projects/:id` - 获取项目详情
2. `PUT /api/projects/:id` - 更新项目设置

#### Step 1：AI辅助定义契约

```
请为"项目设置"功能设计API契约：

功能需求：
1. 获取项目详情（项目名称、描述、可见性、成员数量）
2. 更新项目设置（名称、描述、可见性）

约束：
- 项目名称必填，2-50字符
- 描述可选，最多500字符
- 可见性只能是：public, private, internal

请生成：
1. Pact消费者测试（前端）
2. Pact提供者验证（后端）
3. TypeScript类型定义
```

#### Step 2：前后端并行开发

有了契约后，前后端可以并行开发：

**前端**：
```typescript
// 基于契约的类型定义
interface Project {
  id: number;
  name: string;
  description?: string;
  visibility: 'public' | 'private' | 'internal';
  memberCount: number;
}

// API调用
const getProject = async (id: number): Promise<Project> => {
  const response = await fetch(`/api/projects/${id}`);
  if (!response.ok) throw new Error('Failed to fetch project');
  return response.json();
};
```

**后端**：
```typescript
// 基于契约的接口实现
app.get('/api/projects/:id', async (req, res) => {
  const project = await db.project.findById(req.params.id);
  if (!project) return res.status(404).json({ error: 'Not found' });
  
  // 确保返回格式符合契约
  res.json({
    id: project.id,
    name: project.name,
    description: project.description,
    visibility: project.visibility,
    memberCount: project.members.length,
  });
});
```

#### Step 3：契约验证发现问题

在CI中，契约测试发现了一个问题：

```
[FAIL] Expected "visibility" to be one of ["public", "private", "internal"]
         Actual: "team"
```

原来后端数据库里有一个旧的"team"可见性选项，前端契约中没有定义。这个问题在开发阶段就被发现了，而不是联调时。

#### Step 4：平滑修复

```
请帮我设计一个平滑修复方案：

问题：
- 后端返回visibility: "team"，但契约只允许"public", "private", "internal"
- 数据库中有存量数据使用了"team"

要求：
1. 不能破坏现有功能
2. 逐步迁移到新值
3. 更新契约
```

AI给出的方案：
```typescript
// 临时兼容处理
const normalizeVisibility = (visibility: string) => {
  // "team"在功能上等价于"internal"
  if (visibility === 'team') return 'internal';
  return visibility;
};

// 接口返回时转换
res.json({
  ...project,
  visibility: normalizeVisibility(project.visibility),
});
```

---

### 周五：成果展示

三周后，小王向团队展示了契约测试的成果。

**对比数据**：

| 指标 | 实施前 | 实施后 | 改进 |
|:---|:---|:---|:---|
| 接口相关bug | 每周3-5个 | 每周0-1个 | 80%减少 |
| 联调时间 | 平均2天 | 平均0.5天 | 75%减少 |
| 接口文档准确率 | 约60% | 100%（契约即文档） | 质的提升 |
| 前后端扯皮次数 | 频繁 | 几乎为零 | 沟通成本大幅降低 |

**团队反馈**：

"以前改接口心惊胆战，现在契约测试会自动告诉我哪里破坏了兼容性。"——后端小李

"前端Mock数据一直是痛点，现在基于契约自动生成，和真实接口完全一致。"——前端小林

"终于不用在联调时才发现接口问题了，开发效率提升很多。"——产品经理

---

## 理论：契约测试深度解析

### 契约测试 vs 其他测试

```
测试金字塔：

       /\
      /  \     E2E测试（ expensive，少）
     /____\
    /      \   集成测试
   /________\
  /          \ 契约测试（ new layer ）
 /____________\
/              \单元测试（ cheap，多）
```

**契约测试的独特价值**：
- 比单元测试更高层，验证服务间交互
- 比集成测试更轻量，不需要同时启动所有服务
- 比E2E测试更快速，聚焦数据契约而非业务逻辑

### 消费者驱动 vs 提供者驱动

**消费者驱动契约（CDC）**：
```
消费者（前端）定义契约 → 提供者（后端）满足契约
```
- 优点：消费者需求优先，避免过度设计
- 缺点：多个消费者需求冲突时需要协调

**提供者驱动契约**：
```
提供者（后端）定义契约 → 消费者（前端）适配契约
```
- 优点：提供者控制API演进
- 缺点：可能忽视消费者真实需求

**推荐**：微服务场景下使用消费者驱动，内部API使用提供者驱动。

### 契约版本管理策略

**1. 乐观策略（推荐）**
- 允许消费者定义灵活的匹配规则
- 提供者可以添加新字段，只要不破坏已有契约
- 适合快速迭代的团队

**2. 严格策略**
- 要求完全匹配，不允许任何差异
- 更安全但灵活性差
- 适合对稳定性要求高的场景

### AI在契约测试中的角色

```
┌─────────────────────────────────────────────┐
│              AI辅助契约测试流程              │
├─────────────────────────────────────────────┤
│                                             │
│  1. 需求分析 → AI生成初始契约草案            │
│     ↓                                       │
│  2. 人工审查 → 调整契约细节                  │
│     ↓                                       │
│  3. AI生成 → 消费者测试代码                  │
│     ↓                                       │
│  4. AI生成 → 提供者验证代码                  │
│     ↓                                       │
│  5. AI生成 → Mock服务和类型定义              │
│     ↓                                       │
│  6. 变更影响分析 → AI评估breaking change     │
│     ↓                                       │
│  7. AI生成 → 迁移方案和兼容代码              │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 实践：AI辅助契约测试工作流

### Step 1：从零开始建立契约

**Prompt - 初始契约生成**：
```
请为以下业务功能设计完整的API契约：

业务场景：
[描述业务功能]

涉及接口：
1. [接口1描述]
2. [接口2描述]
...

技术要求：
- 使用[Pact/其他框架]
- 支持[具体技术需求]

输出：
1. OpenAPI/Swagger定义
2. Pact消费者测试代码
3. Pact提供者验证代码
4. TypeScript类型定义
5. Mock数据生成器
```

### Step 2：契约变更管理

**Prompt - 变更影响分析**：
```
请分析以下API变更对契约的影响：

当前契约：
[粘贴契约]

计划变更：
[描述变更内容]

请输出：
1. 变更类型（breaking/non-breaking）
2. 影响范围（哪些消费者受影响）
3. 迁移策略（如何平滑过渡）
4. 版本号建议
5. 更新后的契约
```

### Step 3：契约文档生成

**Prompt - 文档生成**：
```
请基于以下Pact契约生成API文档：

契约文件：
[粘贴契约JSON]

输出格式：
1. Markdown文档（适合GitHub/Confluence）
2. 包含请求/响应示例
3. 字段说明表格
4. 错误码说明
5. 变更历史
```

### Step 4：CI/CD集成

**完整CI工作流**：
```yaml
name: Contract-Driven Pipeline

on: [push, pull_request]

jobs:
  # 1. 消费者契约测试
  consumer-contract-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          cd consumer
          npm ci
          npm run test:contract
      - name: Upload to Pact Broker
        run: |
          docker run pactfoundation/pact-cli:latest \
            publish \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }} \
            ./pacts

  # 2. 提供者契约验证
  provider-contract-verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          cd provider
          npm ci
          npm run test:contract:verify

  # 3. 部署前检查
  can-i-deploy:
    needs: [consumer-contract-test, provider-contract-verify]
    runs-on: ubuntu-latest
    steps:
      - name: Check contract compatibility
        run: |
          docker run pactfoundation/pact-cli:latest \
            can-i-deploy \
            --pacticipant ${{ matrix.service }} \
            --version ${{ github.sha }} \
            --to-environment production
```

---

## 本章交付物

完成本章后，你应该拥有：

1. **契约测试基础设施**
   - Pact配置（消费者和提供者）
   - CI/CD集成脚本
   - Pact Broker配置

2. **契约文档库**
   - 所有API的契约定义
   - 变更历史记录
   - 迁移指南

3. **AI辅助Prompt库**
   - 契约生成Prompt
   - 变更分析Prompt
   - 文档生成Prompt

4. **团队工作流**
   - 契约驱动开发流程
   - 变更管理规范
   - 问题响应机制

---

## 行动清单

- [ ] 选择1-2个核心API作为试点
- [ ] 使用AI生成初始契约定义
- [ ] 配置Pact消费者测试（前端）
- [ ] 配置Pact提供者验证（后端）
- [ ] 搭建Pact Broker用于契约管理
- [ ] 集成契约测试到CI/CD
- [ ] 建立契约变更流程
- [ ] 培训团队契约驱动开发方法

---

## 本章彩蛋

### 彩蛋1：AI生成契约的"黄金Prompt"

```
你是一位资深API架构师，擅长设计RESTful API和契约测试。

请为以下业务需求设计API契约，遵循以下原则：

1. RESTful设计：
   - 使用正确的HTTP方法（GET/POST/PUT/DELETE）
   - 使用语义化的URL路径
   - 正确使用HTTP状态码

2. 契约健壮性：
   - 消费者字段使用宽松匹配（like）
   - 提供者可以安全地添加新字段
   - 枚举值考虑扩展性

3. 版本管理：
   - 破坏性变更必须升级版本
   - 非破坏性变更保持兼容

业务需求：
[详细描述]

请输出：
1. OpenAPI 3.0定义
2. Pact消费者测试代码
3. Pact提供者验证代码
4. 字段变更兼容性说明
```

### 彩蛋2：契约测试检查清单

发布API前，检查这5个问题：

1. **契约是否已定义？** 消费者和提供者都认可
2. **契约测试是否通过？** CI中绿灯
3. **变更是否向后兼容？** 如果是breaking change，是否已通知所有消费者
4. **文档是否已更新？** 契约即文档，确保最新
5. **Mock是否已同步？** 前端Mock基于最新契约

### 彩蛋3：常见契约模式

```typescript
// 1. 分页响应模式
const paginatedResponse = {
  data: eachLike(itemMatcher),
  total: integer(),
  page: integer(),
  pageSize: integer(),
  hasMore: boolean(),
};

// 2. 错误响应模式
const errorResponse = {
  error: {
    code: string(),
    message: string(),
    details: optional(array()),
  },
};

// 3. 乐观更新模式
const optimisticUpdate = {
  id: integer(),
  status: oneOf(['pending', 'processing', 'completed', 'failed']),
  updatedAt: datetime(),
};
```

---

> **小王的契约测试感悟**：
> 
> "契约测试最大的价值不是技术，而是协作。
> 
> 以前前后端之间像是'黑盒'——我不知道你承诺了什么，你不知道我期望了什么。
> 有了契约，就像签了一份合同，双方都清楚边界和责任。
> 
> AI帮我们解决了契约测试的技术门槛，让我们可以专注于业务本身。
> 现在前后端很少因为接口问题扯皮了，团队氛围都变好了。"

---

**下一章预告**：第20章《在被黑客攻击之前发现问题》——小王将面对更严峻的挑战：安全测试。如何用AI辅助发现潜在的安全漏洞，在黑客之前堵住防线？
