# 第4章：一句话需求变完美代码的秘密

> **提示工程基础——RPCT框架**

---

## 故事：小李的"AI沟通困境"

### 周二上午：糟糕的第一次尝试

周二上午，小李遇到了一个棘手的问题。

产品经理丢过来一个需求："给后台管理系统加一个数据导出功能，要支持Excel和CSV两种格式。"

放在以前，小李需要先调研库、设计接口、写代码、测试，至少得一天。但现在他有AI了——"让AI写，我审核就行。"

他打开Cursor，信心满满地输入：

```
写一个数据导出功能
```

按下回车，AI开始生成代码。一分钟后，屏幕上出现了50多行代码：

```javascript
// AI生成的代码
function exportData(data) {
  const csv = convertToCSV(data);
  downloadFile(csv, 'export.csv');
}

function convertToCSV(data) {
  // ... CSV转换逻辑
}

function downloadFile(content, filename) {
  const blob = new Blob([content], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}
```

小李皱起眉头。这代码有问题：

1. 只实现了CSV，Excel呢？
2. 没有错误处理，数据格式不对怎么办？
3. 大数据量怎么办？会不会卡死浏览器？
4. 没有进度提示，用户怎么知道导出成功了？
5. 文件名是固定的，不能按日期命名吗？

他叹了口气，开始手动修改。改完之后发现，花的时间和自己写差不多。

"AI也不过如此..."他嘟囔着。

---

### 周三下午：意外的启发

周三下午，小李去茶水间倒水，碰到前端组的小王。

"哎，你用AI写那个导出功能了吗？"小王问。

"写了，但生成的代码很烂，改起来费劲。"

"你提示词怎么写的？"

"就写'写一个数据导出功能'啊，还能怎么写？"

小王笑了："怪不得。你这么写，AI只能猜你的需求。你得告诉它更多——用什么技术栈、要处理什么场景、有什么特殊要求。"

"那要写多长？写一大堆文字？"

"不用。有个框架叫**RPCT**，按照这个结构写，几句话就够了。"

小李来了兴趣："R-P-C-T？是什么？"

"Role（角色）、Profile（背景）、Constraint（约束）、Task（任务）。等会儿我发你一篇文章。"

---

### 周四：RPCT框架实战

周四早上，小李仔细研究了RPCT框架。

**R - Role（角色）**：给AI一个明确的身份
- ❌ 错误："帮我写代码"
- ✅ 正确："你是一个有5年经验的Node.js后端工程师"

**P - Profile（背景）**：说明项目背景和技术栈
- ❌ 错误：没说明
- ✅ 正确："我们的项目使用Express + TypeScript，数据库是PostgreSQL，使用Prisma作为ORM"

**C - Constraint（约束）**：列出限制条件和要求
- ❌ 错误：没说明
- ✅ 正确："数据量可能很大（10万行以上），需要考虑性能。需要支持Excel和CSV两种格式"

**T - Task（任务）**：具体要做什么
- ❌ 错误："写一个导出功能"
- ✅ 正确："实现一个API端点 /api/export，接收查询参数，返回可下载的文件"

小李决定用RPCT框架重新写那个导出需求：

```
Role: 你是一个有5年经验的Node.js后端工程师，擅长处理大数据导出。

Profile: 我们的项目使用Express + TypeScript，数据库是PostgreSQL，使用Prisma作为ORM。前端是React。

Constraint:
- 数据量可能很大（10万行以上），需要流式处理，不能一次性加载到内存
- 需要支持Excel(xlsx)和CSV两种格式，由请求参数决定
- 文件名需要包含日期和时间戳
- 需要进度反馈机制（通过WebSocket或SSE）
- 要有完善的错误处理和日志记录
- 代码需要包含单元测试

Task: 实现一个API端点 /api/export，接收以下参数：
- format: 'csv' | 'xlsx'
- table: 表名
- filters: 可选的筛选条件
- 返回一个下载链接，并通过WebSocket推送进度
```

按下回车，小李满怀期待地等待。

这次AI生成的代码完全不同了——

```typescript
// AI生成的代码（节选）
import { Response } from 'express';
import { PrismaClient } from '@prisma/client';
import * as XLSX from 'xlsx';
import { createObjectCsvStringifier } from 'csv-writer';
import WebSocket from 'ws';

const prisma = new PrismaClient();

interface ExportParams {
  format: 'csv' | 'xlsx';
  table: string;
  filters?: Record<string, any>;
}

export async function exportData(
  params: ExportParams, 
  ws: WebSocket,
  res: Response
) {
  const startTime = Date.now();
  const filename = `${params.table}_${formatDate(new Date())}.${params.format}`;
  
  try {
    // 获取总记录数
    const totalCount = await prisma[params.table].count({
      where: params.filters
    });
    
    ws.send(JSON.stringify({
      type: 'start',
      total: totalCount,
      message: `开始导出${totalCount}条记录`
    }));

    // 流式处理，每次1000条
    const batchSize = 1000;
    let processedCount = 0;
    const chunks: any[] = [];

    for (let skip = 0; skip < totalCount; skip += batchSize) {
      const records = await prisma[params.table].findMany({
        where: params.filters,
        skip,
        take: batchSize
      });

      chunks.push(...records);
      processedCount += records.length;

      // 发送进度
      ws.send(JSON.stringify({
        type: 'progress',
        processed: processedCount,
        total: totalCount,
        percentage: Math.round((processedCount / totalCount) * 100)
      }));
    }

    // 根据格式生成文件
    if (params.format === 'csv') {
      await generateCSV(chunks, filename, res);
    } else {
      await generateExcel(chunks, filename, res);
    }

    ws.send(JSON.stringify({
      type: 'complete',
      filename,
      duration: Date.now() - startTime
    }));

  } catch (error) {
    ws.send(JSON.stringify({
      type: 'error',
      message: error.message
    }));
    res.status(500).json({ error: 'Export failed' });
  }
}

// 生成CSV（流式写入）
async function generateCSV(data: any[], filename: string, res: Response) {
  // ... 实现细节
}

// 生成Excel（分sheet处理大文件）
async function generateExcel(data: any[], filename: string, res: Response) {
  // ... 实现细节
}
```

小李惊呆了。

这次生成的代码不仅包含了他要求的所有功能，还额外考虑了：
- 批量查询避免内存溢出
- WebSocket进度推送的格式设计
- 文件名格式化
- 完整的错误处理

"这就是RPCT的威力吗..."他喃喃自语。

---

### 周五：效果验证

周五，小李把这个导出功能集成到项目中，运行测试。

导出10万条记录：
- 内存占用稳定在200MB以内
- 导出耗时45秒
- WebSocket进度推送正常
- Excel和CSV格式都正确

更让人惊喜的是，当他把提示词模板分享给团队后，其他人使用AI的效率也明显提升。

"原来和AI沟通也是需要学习的..."小李在周报里写道。

---

## 理论知识：RPCT框架详解

### 为什么需要结构化提示？

小李的经历说明了一个核心问题：**AI不是你肚子里的蛔虫**。

当你说"写一个导出功能"时，AI不知道：
- 你的技术栈是什么
- 数据量有多大
- 需要支持什么格式
- 有没有特殊性能要求

它只能基于"最常见的情况"生成代码。这就是为什么第一次生成的代码不符合需求。

**结构化提示的价值**：
1. **减少猜测**：提供足够的上下文，让AI不需要猜
2. **提高一致性**：同样的结构，输出质量更稳定
3. **便于迭代**：可以清晰地看到哪个部分需要调整
4. **团队协作**：团队成员可以复用有效的提示模板

### RPCT框架的四个维度

```
┌─────────────────────────────────────────────────────┐
│                    RPCT 框架                         │
├─────────────┬───────────────────────────────────────┤
│     R       │  Role（角色）                          │
│             │  你是谁？你有什么经验？                  │
├─────────────┼───────────────────────────────────────┤
│     P       │  Profile（背景）                       │
│             │  项目背景、技术栈、业务场景              │
├─────────────┼───────────────────────────────────────┤
│     C       │  Constraint（约束）                    │
│             │  限制条件、质量要求、边界情况            │
├─────────────┼───────────────────────────────────────┤
│     T       │  Task（任务）                          │
│             │  具体要做什么，输出格式要求              │
└─────────────┴───────────────────────────────────────┘
```

#### R - Role（角色）

给AI设定一个具体的身份，让它以相应的 expertise 来回答。

**示例**：

| 场景 | 不明确的角色 | 明确的角色 |
|:---|:---|:---|
| 写代码 | "帮我写代码" | "你是一位有5年经验的Node.js后端工程师，熟悉微服务架构" |
| 写测试 | "写测试用例" | "你是一位资深的QA工程师，擅长边界值分析和异常场景设计" |
| 写文档 | "写API文档" | "你是一位技术写作者，擅长编写清晰、可执行的API文档" |

**技巧**：
- 经验年限要合理（3-10年比较适合大多数场景）
- 提及具体的专业领域
- 可以指定性格特点（"注重细节"、"喜欢简洁"）

#### P - Profile（背景）

说明项目的技术栈和业务背景，让AI理解代码的上下文。

**需要包含的信息**：
- 编程语言和框架
- 数据库和中间件
- 项目架构（单体/微服务）
- 团队规模（影响代码复杂度设计）

**示例**：
```
项目背景：
- 后端：Node.js + Express + TypeScript
- 数据库：PostgreSQL，使用Prisma作为ORM
- 前端：React 18 + Tailwind CSS
- 部署：Docker + Kubernetes
- 团队：10人，使用Git Flow工作流
```

#### C - Constraint（约束）

列出所有的限制条件和质量要求，这是生成高质量代码的关键。

**常见的约束类型**：

| 类别 | 示例 |
|:---|:---|
| 性能约束 | "查询响应时间<100ms"、"支持10万并发" |
| 安全约束 | "防止SQL注入"、"敏感数据需要加密" |
| 可用性约束 | "99.9%可用性"、"需要熔断降级机制" |
| 代码约束 | "需要单元测试覆盖"、"遵循SOLID原则" |
| 业务约束 | "符合GDPR规范"、"支持多语言" |

#### T - Task（任务）

清晰描述需要完成的具体任务，包括输入、输出和处理逻辑。

**好的任务描述包含**：
1. **功能描述**：这个任务要实现什么
2. **输入参数**：需要什么输入，格式是什么
3. **输出要求**：输出什么，格式是什么
4. **处理步骤**：逻辑流程（可选）

**示例**：
```
Task: 实现用户注册API

功能：接收用户信息，验证后创建账号

输入参数：
- email: string, 邮箱格式
- password: string, 8-20位，包含大小写字母和数字
- name: string, 2-20个字符

输出：
- 成功：{ success: true, userId: string, token: string }
- 失败：{ success: false, error: string, field?: string }

处理步骤：
1. 验证输入参数格式
2. 检查邮箱是否已注册
3. 密码bcrypt加密
4. 创建用户记录
5. 生成JWT token
6. 返回结果
```

### RPCT进阶技巧

#### 1. 分层细化法

对于复杂任务，可以分多层RPCT逐步细化：

```
第一层：整体架构（高level）
Role: 架构师
Profile: 电商平台，日均百万PV
Constraint: 高可用、可扩展
Task: 设计订单系统的整体架构

第二层：具体模块（中level）
Role: 高级工程师
Profile: 基于上层的架构，使用Node.js
Constraint: 响应时间<100ms，需要缓存
Task: 设计订单查询模块的实现

第三层：具体函数（低level）
Role: 开发工程师
Profile: 使用Redis做缓存
Constraint: 需要考虑缓存穿透、击穿
Task: 实现getOrderById函数
```

#### 2. 正反例法

提供"好的示例"和"不好的示例"，让AI理解你的期望：

```
Constraint:
- 错误处理要具体，不能只是try-catch然后console.log

❌ 不好的示例：
try {
  const result = await db.query(sql);
  return result;
} catch (e) {
  console.log(e);
  return null;
}

✅ 好的示例：
try {
  const result = await db.query(sql);
  return { success: true, data: result };
} catch (error) {
  logger.error('Database query failed', { sql, error: error.message });
  return { 
    success: false, 
    error: '查询失败，请稍后重试',
    errorCode: 'DB_QUERY_ERROR'
  };
}
```

#### 3. 输出格式指定

明确告诉AI你希望代码/文档的格式：

```
Task: 实现用户认证中间件

输出要求：
1. TypeScript代码，包含类型定义
2. 每个函数前添加JSDoc注释
3. 包含单元测试（使用Jest）
4. 代码结构：
   - src/middleware/auth.ts (主实现)
   - src/middleware/auth.test.ts (测试)
   - src/types/auth.ts (类型定义)
```

---

## 实践案例：不同场景的RPCT模板

### 模板1：API开发

```
Role: 你是一个有5年经验的Node.js后端工程师，擅长RESTful API设计和性能优化。

Profile: 
- 技术栈：Node.js + Express + TypeScript + PostgreSQL(Prisma)
- 项目：电商平台后端API
- 已有模块：用户认证、商品管理

Constraint:
- 所有API需要统一返回格式 { success: boolean, data?: any, error?: string }
- 数据库查询需要记录慢查询日志（>100ms）
- 需要处理常见的异常：数据库连接失败、参数验证失败、权限不足
- 代码需要包含单元测试（Jest），覆盖率>80%
- 遵循RESTful设计规范

Task: 实现购物车相关API
- POST /api/cart/items - 添加商品到购物车
- GET /api/cart - 获取购物车内容
- PUT /api/cart/items/:id - 修改商品数量
- DELETE /api/cart/items/:id - 删除商品

需要实现：
1. 完整的控制器代码
2. 请求参数验证（使用zod或class-validator）
3. 数据库模型设计（Prisma schema）
4. 单元测试用例
```

### 模板2：前端组件开发

```
Role: 你是一个高级前端工程师，精通React和TypeScript，注重用户体验和代码可维护性。

Profile:
- 技术栈：React 18 + TypeScript + Tailwind CSS + React Query
- UI组件库：使用Headless UI + 自定义样式
- 项目：企业级后台管理系统

Constraint:
- 组件需要支持深色/浅色模式
- 需要处理加载状态、空状态、错误状态
- 表单组件需要使用react-hook-form
- 需要键盘可访问性（ARIA属性）
- 代码需要包含Storybook stories

Task: 实现一个用户选择器组件UserSelector

功能：
- 支持搜索用户（通过API）
- 支持单选和多选模式
- 显示用户头像和名称
- 已选用户以tag形式展示，可删除

Props接口：
interface UserSelectorProps {
  mode: 'single' | 'multiple';
  value?: string | string[];
  onChange: (value: string | string[]) => void;
  disabled?: boolean;
  placeholder?: string;
}

输出：
1. 完整的组件代码（TypeScript）
2. 类型定义
3. 使用示例
4. Storybook story
```

### 模板3：代码重构

```
Role: 你是一个代码重构专家，擅长在不改变外部行为的前提下改进代码质量。

Profile:
- 语言：JavaScript/TypeScript
- 重构目标：提高可读性、可维护性、性能

Constraint:
- 不能改变函数的输入输出行为
- 需要保持原有的错误处理逻辑
- 重构后代码需要更易读、更易测试
- 复杂逻辑需要添加注释说明

Task: 重构以下代码

原始代码：
[粘贴你的代码]

重构目标：
1. 消除嵌套层级（目前太深）
2. 提取重复逻辑为独立函数
3. 使用早返回（early return）简化条件判断
4. 添加适当的错误处理

输出要求：
1. 重构后的完整代码
2. 说明每处重构的理由
3. 如果适用，提供单元测试验证重构前后行为一致
```

### 模板4：Bug修复

```
Role: 你是一个资深调试工程师，擅长快速定位并修复代码问题。

Profile:
- 技术栈：[填写你的技术栈]
- 问题环境：[开发/测试/生产]

Constraint:
- 修复需要针对问题根因，不是掩盖症状
- 修复不能引入新的问题
- 需要考虑边界情况
- 复杂修复需要添加注释说明原因

Task: 修复以下Bug

问题描述：
[描述Bug的现象]

复现步骤：
1. [步骤1]
2. [步骤2]
3. [预期结果] vs [实际结果]

相关代码：
[粘贴相关代码]

错误日志（如果有）：
[粘贴错误日志]

输出要求：
1. Bug根因分析
2. 修复后的代码
3. 说明为什么这样修复
4. 建议的预防措施（如何避免类似问题）
```

---

## 本章交付物

完成本章后，你应该拥有：

1. **个人RPCT模板库**
   - API开发模板
   - 前端组件模板
   - 重构任务模板
   - Bug修复模板

2. **5个有效的RPCT提示词**
   - 记录你实际使用过的有效提示词
   - 标注使用场景和效果

3. **提示词优化记录**
   - 记录同一任务的提示词迭代过程
   - 对比不同提示词的输出质量

---

## 行动清单

- [ ] 回顾最近3个你用AI完成但不满意的任务
- [ ] 用RPCT框架重写这3个任务的提示词
- [ ] 对比新旧提示词的输出质量差异
- [ ] 创建你的个人RPCT模板库（至少5个模板）
- [ ] 与团队分享你的模板，收集反馈

---

## 本章彩蛋

### RPCT的变体框架

**RTF框架**（适合简单任务）：
- Role（角色）
- Task（任务）
- Format（输出格式）

示例：
```
Role: 技术文档写作者
Task: 解释什么是JWT
Format: Markdown，包含定义、原理、优缺点三个部分，每部分不超过100字
```

**APE框架**（适合创意任务）：
- Action（行动）
- Purpose（目的）
- Expectation（期望）

示例：
```
Action: 设计一个用户登录页
Purpose: 让新用户快速注册，老用户快速登录
Expectation: 简洁美观，移动端优先，加载速度<1秒
```

**COSTAR框架**（适合复杂商业任务）：
- Context（上下文）
- Objective（目标）
- Style（风格）
- Tone（语气）
- Audience（受众）
- Response（响应格式）

### 提示词的"魔法词"

有些词能明显提升AI输出质量：

| 魔法词 | 效果 |
|:---|:---|
| "step by step" | 让AI分步骤思考 |
| "think carefully" | 让AI更谨慎 |
| "explain your reasoning" | 要求解释推理过程 |
| "provide examples" | 要求提供示例 |
| "consider edge cases" | 要求考虑边界情况 |
| "best practices" | 要求遵循最佳实践 |

---

> **小李的总结**：>
> "以前我以为AI不够聪明，现在发现是我不会问。RPCT框架教会我的不只是写提示词，更是如何清晰地表达需求——这对和人沟通也同样有用。"

---

## 下一章预告

**第5章：《让AI一步步思考复杂问题》**

小陈将学习如何用CoT（思维链）和结构化输出让AI处理复杂任务。通过拆解问题、分步推理、格式化输出，他把AI从"快但容易错"的工具变成了"慢但准确"的助手，成功解决了前端状态管理的难题。
