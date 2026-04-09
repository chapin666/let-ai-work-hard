# 第6章：按Tab键比敲字母还多的日子

> **AI IDE入门——Cursor/Copilot深度使用**

---

## 故事：小张的IDE革命

### 周一：从怀疑到真香

小张是全栈工程师，平时用VS Code写代码。他一直听说AI IDE很强，但总觉得——"不就是智能补全吗，能有多厉害？"

周一早上，产品经理催得急，要他在下午前完成一个用户管理后台的列表页面。按以往经验，这种页面至少需要半天：

- 表格展示（分页、排序、筛选）
- 新增/编辑弹窗
- 删除确认
- 加载状态、空状态
- API对接

"要不试试Cursor？"旁边的同事说，"这种CRUD页面，它特别擅长。"

小张半信半疑地下载了Cursor，导入项目。

他打开一个新文件，敲下一行注释：

```typescript
// UserList页面：展示用户列表，支持分页、搜索、编辑、删除
```

然后按下Tab键。

光标停顿了一秒，然后代码像瀑布一样涌出来——

```typescript
import React, { useState, useEffect } from 'react';
import { Table, Button, Input, Modal, Form, message, Popconfirm } from 'antd';
import { SearchOutlined, PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { userApi } from '@/api/user';
import type { User } from '@/types/user';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 });
  const [searchKeyword, setSearchKeyword] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [form] = Form.useForm();

  // 获取用户列表
  const fetchUsers = async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const res = await userApi.getList({
        page,
        pageSize,
        keyword: searchKeyword,
      });
      setUsers(res.data.list);
      setPagination({
        current: page,
        pageSize,
        total: res.data.total,
      });
    } catch (error) {
      message.error('获取用户列表失败');
    } finally {
      setLoading(false);
    }
  };

  // ... 还有编辑、删除、搜索等方法
```

小张瞪大了眼睛。

这代码不仅结构完整，还：
- 正确引入了项目中使用的antd组件
- 使用了TypeScript类型
- 引用了项目的API模块和类型定义
- 包含了错误处理和加载状态

他继续按Tab键，AI继续生成——编辑弹窗、删除确认、搜索逻辑...整个页面就这样"按"出来了。

"这...这不对啊..."小张喃喃自语，"我这才按了几下Tab..."

他看了一眼时间，从打开Cursor到现在，才过了15分钟。而页面已经完成了80%。

"真香。"

---

### 周三：深度功能的探索

周一开始用Cursor，到周三小张已经渐入佳境。但他发现Cursor不只是"按Tab生成代码"那么简单。

#### 发现1：Chat模式

按`Ctrl+L`打开Chat面板，可以直接和AI对话。

小张试着问：

```
这个UserList组件有点复杂，能帮我把它拆分成小组件吗？
```

AI立刻给出了拆分方案：

```
建议拆分为：
1. UserTable - 纯展示表格
2. UserSearch - 搜索表单
3. UserModal - 编辑弹窗
4. useUserList - 自定义hook，管理数据逻辑
```

更厉害的是，点击"Apply"按钮，AI直接帮他重构了代码，创建了新的文件。

#### 发现2：代码解释

小张接手了一个遗留项目，有一段代码看不懂：

```typescript
const result = await Promise.all(
  ids.map(async (id) => {
    const item = await cache.get(id);
    if (item) return item;
    const fresh = await fetch(id);
    await cache.set(id, fresh, 3600);
    return fresh;
  })
);
```

他选中这段代码，右键"Explain Code"，AI给出了解释：

```
这段代码实现了带缓存的批量数据获取：
1. 对ids数组中的每个id并发执行
2. 先尝试从缓存获取
3. 缓存未命中则发起请求
4. 将结果写入缓存（TTL=3600秒）
5. 返回所有结果

注意：这里的Promise.all可能会导致缓存雪崩，如果大量id同时未命中。
```

"原来如此..."小张恍然大悟，"而且还指出了潜在问题！"

#### 发现3：Bug修复

小张写了个函数，但测试一直通不过。他把错误信息和代码贴到Chat里：

```
测试报错：TypeError: Cannot read property 'name' of undefined

代码：
function greet(user) {
  return `Hello, ${user.profile.name}!`;
}
```

AI立刻识别出问题：

```
问题：没有处理user或user.profile为undefined的情况。

修复方案：
function greet(user) {
  const name = user?.profile?.name ?? 'Guest';
  return `Hello, ${name}!`;
}
```

---

### 周五：Copilot的另一种体验

周五，小张切换到另一个项目——那个项目还在用VS Code，他装了GitHub Copilot。

和Cursor的"瀑布式生成"不同，Copilot更像一个"默契的搭档"。

#### 体验1：上下文感知

小张在写一个工具函数：

```typescript
import { validateEmail } from '@/utils/validation';
```

刚敲完这一行，Copilot就建议：

```typescript
import { validateEmail, validatePhone } from '@/utils/validation';
```

小张往下一看，原来下面确实要用到validatePhone。Copilot仿佛"读懂"了他的意图。

#### 体验2：渐进式补全

写React组件时：

```typescript
const [count, setCount] = useState(0);
```

Copilot建议接下来的代码：

```typescript
const increment = () => setCount(c => c + 1);
const decrement = () => setCount(c => c - 1);
```

这种渐进式的补全让小张感觉掌控感更强——AI是在"配合"他，而不是"代替"他。

#### 体验3：学习代码库

小张在项目里看到一行：

```typescript
const data = useSWR('/api/users', fetcher);
```

他不熟悉useSWR，刚想搜索，Copilot已经根据项目中的其他用法给出了补全建议。通过观察Copilot的建议，他很快理解了useSWR的用法。

---

## 理论知识：AI IDE深度解析

### Cursor vs Copilot：核心差异

| 维度 | Cursor | GitHub Copilot |
|:---|:---|:---|
| **交互模式** | Tab生成 + Chat对话 | 实时补全 |
| **生成粒度** | 大块代码、整个函数 | 行级、片段级 |
| **上下文范围** | 整个项目（通过@codebase） | 当前文件 + 相关文件 |
| **对话能力** | 强（内置Chat） | 弱（需配合Copilot Chat） |
| **代码修改** | 支持多文件编辑 | 单文件补全 |
| **价格** | $20/月 | $10/月 |
| **上手难度** | 需要学习Chat模式 | 开箱即用 |

### Cursor核心功能详解

#### 1. Tab生成（Cmd/Ctrl+K）

**适用场景**：快速生成代码块

**使用技巧**：
- 先用注释描述需求，再按Tab
- 生成过程中可以按Esc取消
- 生成后按Cmd+Z可以撤销

**最佳实践**：
```typescript
// ❌ 不好的提示
function processData

// ✅ 好的提示
// 处理订单数据：过滤已取消订单，按金额排序，返回前10条
function processData
```

#### 2. Chat模式（Cmd/Ctrl+L）

**适用场景**：复杂任务、代码解释、重构

**常用指令**：
```
@file 文件名 - 引用特定文件
@codebase - 引用整个代码库
@web - 搜索网络信息
@lint - 检查代码规范
```

**高效对话技巧**：
1. **先给上下文**："这个函数在项目中被多处调用..."
2. **明确输出格式**："请以表格形式列出..."
3. **要求解释**："请解释为什么要这样实现"

#### 3. Composer模式

**适用场景**：多文件编辑、大型重构

**使用方法**：
1. 打开Composer（Cmd/Ctrl+I）
2. 描述需求："给所有API添加错误重试逻辑"
3. AI会分析影响范围，列出要修改的文件
4. 确认后批量应用

### Copilot核心功能详解

#### 1. 实时代码补全

**触发方式**：开始输入，自动建议

**接受建议**：
- Tab：接受全部
- Ctrl+→：接受下一个词
- Ctrl+↓：查看下一个建议

**高效使用技巧**：
1. **写好函数签名**：Copilot会根据签名推断实现
2. **添加类型注释**：TypeScript类型能帮助Copilot理解意图
3. **保持编码风格**：Copilot会学习你的风格

#### 2. Copilot Chat（VS Code插件）

**适用场景**：代码解释、Bug修复、测试生成

**使用方法**：
1. 选中代码
2. 右键"Copilot" → "Explain This"
3. 或在侧边栏打开Copilot Chat

### 提示词在IDE中的应用

即使是AI IDE，好的提示词依然重要。

#### Cursor中的提示词技巧

**1. 使用@引用**

```
@file UserList.tsx 这个文件的第45行为什么要用useCallback？
```

**2. 提供上下文**

```
我们的项目使用React Query做数据获取。请帮我把这个组件改为使用React Query。
```

**3. 明确输出要求**

```
请优化这个函数的性能。要求：
1. 时间复杂度从O(n²)降到O(n)
2. 保持原有功能不变
3. 添加注释说明优化思路
```

#### Copilot中的提示词技巧

**1. 用注释引导**

```typescript
// 使用二分查找找到目标值的索引
// 如果找不到返回-1
function binarySearch(arr: number[], target: number): number
```

**2. 提供示例**

```typescript
// 示例：formatCurrency(1234.5) => "¥1,234.50"
function formatCurrency(amount: number): string
```

**3. 指定算法/模式**

```typescript
// 使用发布-订阅模式实现事件总线
class EventBus
```

---

## 实践案例：高效工作流

### 工作流1：从零开始新功能

**场景**：开发一个新页面/模块

**Cursor工作流**：

1. **生成骨架**：
   ```
   // 用户管理页面，包含列表、搜索、新增、编辑、删除
   ```
   按Tab生成基础结构

2. **完善细节**：
   打开Chat，问：
   ```
   请为这个页面添加表单验证逻辑，使用react-hook-form和zod
   ```

3. **对接API**：
   ```
   项目中已有的userApi在@file api/user.ts，请对接真实的API
   ```

4. **代码审查**：
   ```
   请审查这个组件，检查是否有性能问题或不良实践
   ```

### 工作流2：Bug修复

**场景**：修复线上Bug

**Copilot工作流**：

1. **理解代码**：
   选中相关代码，Copilot Explain

2. **添加日志**：
   在关键位置开始输入`console.log`，让Copilot补全要打印的变量

3. **修复代码**：
   根据日志定位问题后，用注释引导修复：
   ```typescript
   // 如果user为null返回默认值
   const name = user
   ```
   Copilot会建议：`?.name ?? 'Anonymous'`

### 工作流3：代码重构

**场景**：重构遗留代码

**Cursor Composer工作流**：

1. **打开Composer**（Cmd/Ctrl+I）

2. **描述重构目标**：
   ```
   将项目中所有的class组件重构为functional组件，使用hooks替代生命周期方法。
   保持原有功能不变，添加必要的类型定义。
   ```

3. **审查修改计划**：
   AI会列出要修改的文件，逐一确认

4. **批量应用**：
   确认后一键重构

---

## 本章交付物

完成本章后，你应该拥有：

1. **个人AI IDE配置**
   - 安装并配置好Cursor或Copilot
   - 自定义规则和快捷键

2. **常用代码片段库**
   - 项目中常用的AI生成代码模式
   - 保存为模板或代码片段

3. **IDE使用手册**
   - 记录你的高效工作流
   - 常用提示词汇总

---

## 行动清单

- [ ] 安装Cursor或Copilot（建议两个都试用）
- [ ] 导入你的项目，体验Tab生成
- [ ] 用Chat模式解决一个实际问题
- [ ] 尝试Composer多文件编辑
- [ ] 记录3个最常用的提示词模式
- [ ] 对比Cursor和Copilot在你的项目中的表现

---

## 本章彩蛋

### Cursor隐藏技巧

**1. 快速修复**：
选中代码按`Cmd+K`，直接输入修复指令，不需要打开Chat

**2. 代码对比**：
AI修改代码后会显示diff，点击"Accept"或"Reject"

**3. 终端集成**：
在终端选中错误信息，右键"Add to Chat"，AI会帮你分析

### Copilot隐藏技巧

**1. 多行建议**：
输入`{`后，Copilot可能建议整个代码块，按Tab接受

**2. 测试生成**：
在测试文件中输入`describe('UserList',`，Copilot会建议测试用例

**3. 文档生成**：
输入`/**`，Copilot会自动生成JSDoc注释

---

> **小张的效率报告**：>
> "用AI IDE一周后的数据：> - 编写CRUD页面的时间：从4小时降到30分钟�
> - 接手遗留代码的理解速度：提升3倍
> - Bug修复平均时间：从2小时降到40分钟�
> 
> 最重要的是，我现在写代码更有'掌控感'了。AI是副驾驶，我才是主驾驶。"
