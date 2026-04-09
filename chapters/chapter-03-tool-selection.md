# 第3章：选对工具，事半功倍

> **AI工具选型——找到适合自己的**

---

## 故事：小张的"工具选择困难症"

### 周一：被选择淹没

周一早上，小张盯着浏览器里打开的十几个标签页，感觉脑袋嗡嗡作响。

左边是Cursor的下载页面，右边是GitHub Copilot的订阅页面，还有一个Windsurf的广告弹窗不知什么时候冒了出来。Slack里，前端组的同事说"Cursor最好用"，后端组的老王却说"Copilot最稳定"，产品经理阿强甚至安利起了"Claude代码神器"。

"到底该用哪个？"

小张抓了抓头发。他是全栈开发，既要写React前端，又要写Node.js后端，偶尔还要写点Python脚本。他想要的AI工具是能通吃所有场景的"瑞士军刀"，但看了一圈测评文章，每个工具都被吹得天花乱坠，又都被骂得体无完肤。

"先试试Cursor吧，好像挺火的。"

他下载安装，导入了自己的项目，兴冲冲地敲了一行注释：

```javascript
// 写一个用户登录表单，包含邮箱和密码验证
```

然后按下Tab键。

AI开始生成代码，一行行跳出来。但小张越看眉头皱得越紧——

"这用的是class组件？现在都2024年了，谁还用class写React啊？"

"而且这表单验证逻辑怎么写在组件里？不应该用react-hook-form吗？"

"还有这个样式...inline style？我的项目里明明配置好了Tailwind..."

他按了Esc取消生成，深吸一口气。

"可能是我没设置好。"

---

### 周二：配置地狱

周二一整天，小张都在研究Cursor的配置。

他发现Cursor有个".cursorrules"文件，可以自定义AI的行为。于是他照着文档开始写：

```
You are an expert React developer.
- Always use functional components with hooks
- Use TypeScript for type safety
- Style with Tailwind CSS
- Use react-hook-form for form handling
- Follow the project's existing code style
```

写完之后，他又试了一次同样的需求。这次生成的代码好多了——确实用了函数组件，也用了TypeScript。但当他仔细看表单验证逻辑时，发现问题：

```typescript
// AI生成的验证逻辑
const validateEmail = (email: string) => {
  return email.includes('@');
};
```

"这也太简单了吧？我的项目里明明有现成的email验证工具函数..."

小张突然意识到一个问题：**AI不知道他的项目里有什么**。它只能根据通用的最佳实践生成代码，但每个项目都有自己的规范、自己的工具库、自己的约定。

"也许我应该试试Copilot？它号称最懂上下文..."

---

### 周三：Copilot的惊喜与失望

周三，小张花了10美元订阅了GitHub Copilot。

打开VS Code，Copilot已经安装好了。他打开昨天那个表单文件，开始手动修改AI的验证逻辑。

```typescript
import { validateEmail } from '@/utils/validation';
```

他刚敲完这行import，Copilot就给出了建议：

```typescript
import { validateEmail, validatePassword } from '@/utils/validation';
```

"嗯？它怎么知道我还需要validatePassword？"

小张往下滚动，发现下面确实要用到密码验证。Copilot似乎"读懂"了他的意图。

他继续写：

```typescript
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
```

Copilot立刻补全了：

```typescript
  const [errors, setErrors] = useState<{email?: string; password?: string}>({});
  
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    // TODO: 验证并提交
  };
```

小张眼睛一亮。这种"读懂上下文"的能力确实很强。而且Copilot的代码补全很轻量，不会像Cursor那样一下子生成一大段，让人感到失控。

但当他想重构一个复杂函数时，Copilot就不够用了——它只能一行行补全，不能一次性理解"把这个回调地狱改成async/await"这样的高层指令。

"Cursor适合写新代码，Copilot适合改代码..."小张在笔记本上记下一行字。

---

### 周四：意外的发现

周四下午，小张偶然在公司技术群里看到一个链接：

"我们后端组整理的AI工具对比表，需要的自取~"

他点开一看，是一张详细的表格：

| 工具 | 代码生成 | 上下文理解 | 聊天功能 | 价格 | 适合场景 |
|:---:|:---:|:---:|:---:|:---:|:---|
| Cursor | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $20/月 | 快速原型、复杂逻辑生成 |
| Copilot | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | $10/月 | 日常编码、补全优化 |
| Windsurf | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $15/月 | Cascade模式适合探索性开发 |
| Cody | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 免费/$9 | 代码库搜索、大型项目 |
| Continue | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 免费开源 | 可定制、隐私优先 |

表格下面还有一段备注：

> **选型建议**：
> - 追求效率最大化？**Cursor + Copilot组合**
> - 预算有限？**Continue + 本地模型**
> - 大型项目/企业级？**Cody + Copilot**
> - 探索性开发/学习？**Windsurf**

"原来不是选一个，而是组合使用？"

小张恍然大悟。他一直陷入"二选一"的思维误区，却没想到这些工具可以互补。

---

### 周五：找到适合自己的组合

周五，小张根据自己的工作流设计了一套工具组合：

**日常开发**：Copilot
- 写代码时的智能补全
- 根据上下文推荐代码
- 价格合适，反应迅速

**复杂任务**：Cursor
- 生成组件或页面
- 重构复杂逻辑
- 询问技术方案

**快速搜索**：公司内部的Cody
- 搜索项目代码库
- 理解遗留代码
- 查找相关实现

他打开Notion，把这个组合方案记录下来：

```
# 我的AI工具组合

## 1. GitHub Copilot（主力）
- 用途：日常编码补全
- 触发方式：自动补全
- 使用场景：
  * 写函数时自动补全参数处理
  * 写测试时生成测试用例
  * 重构时提供修改建议

## 2. Cursor（复杂任务）
- 用途：生成代码、技术咨询
- 触发方式：Tab生成 / Chat询问
- 使用场景：
  * 新功能模块开发
  * 技术方案设计
  * 代码审查和学习

## 3. Cody（代码搜索）
- 用途：项目代码库搜索
- 触发方式：快捷键 / 自然语言查询
- 使用场景：
  * 查找类似实现
  * 理解模块依赖
  * 新成员熟悉代码库
```

---

## 理论知识：AI工具选型方法论

### 为什么工具选型很重要？

小张的经历揭示了一个普遍问题：**没有最好的工具，只有最适合的工具**。

每个AI编程工具都有自己的特点和适用场景：

| 维度 | 说明 | 代表工具 |
|:---|:---|:---|
| **生成能力** | 从零生成完整代码块的能力 | Cursor, Windsurf |
| **理解能力** | 理解项目上下文和代码意图的能力 | Copilot, Cody |
| **交互方式** | 对话式 vs 补全式 | Cursor(对话), Copilot(补全) |
| **上下文范围** | 能看到的代码范围 | Cody(全仓库), Copilot(当前文件) |
| **定制化** | 可配置程度 | Continue(开源可定制) |

### 主流AI编程工具对比

#### 1. Cursor

**定位**：AI原生的代码编辑器

**核心特点**：
- 基于VS Code，完全兼容插件生态
- Tab键生成代码，Ctrl+L打开AI对话框
- 支持Composer模式（多文件编辑）
- 可自定义.cursorrules规则文件

**适合场景**：
- 快速原型开发
- 复杂逻辑生成
- 技术方案咨询

**不足之处**：
- 生成代码有时过于"通用"
- 需要配置才能适配项目规范
- 价格相对较高($20/月)

#### 2. GitHub Copilot

**定位**：代码补全助手

**核心特点**：
- 集成在VS Code、JetBrains等主流IDE
- 基于上下文实时补全
- 学习你的编码风格
- 与GitHub深度集成

**适合场景**：
- 日常编码工作
- 已有代码的补全优化
- 快速完成重复性代码

**不足之处**：
- 缺乏对话能力
- 无法一次性生成大段代码
- 有时过于"保守"

#### 3. Windsurf

**定位**：Cascade驱动的智能IDE

**核心特点**：
- Cascade模式：AI理解意图后自动执行
- 支持多步骤任务自动化
- 智能代码搜索和修改

**适合场景**：
- 探索性开发
- 学习和研究
- 复杂任务自动化

**不足之处**：
- 响应速度有时较慢
- 企业用户较少

#### 4. Cody (Sourcegraph)

**定位**：企业级代码智能助手

**核心特点**：
- 强大的代码库搜索能力
- 理解整个项目的上下文
- 支持代码解释、文档生成

**适合场景**：
- 大型项目开发
- 遗留代码理解
- 团队协作

**不足之处**：
- 个人版功能有限
- 需要配置代码库索引

#### 5. Continue

**定位**：开源的AI代码助手

**核心特点**：
- 完全开源，可自托管
- 支持多种模型(OpenAI、Anthropic、本地模型)
- 透明度高，可定制

**适合场景**：
- 隐私敏感的项目
- 预算有限的开发者
- 喜欢DIY的极客

**不足之处**：
- 功能相对简单
- 需要自己配置模型

### 选型决策框架

根据小张的经验，我们可以总结出一个选型决策框架：

```
选择AI工具的决策树：

1. 你的主要需求是什么？
   ├── 日常编码补全 → Copilot
   ├── 生成新代码/模块 → Cursor
   ├── 理解大型代码库 → Cody
   ├── 隐私优先/预算有限 → Continue
   └── 探索学习 → Windsurf

2. 你的预算？
   ├── 充足($20+/月) → Cursor + Copilot组合
   ├── 中等($10/月) → Copilot单兵作战
   └── 有限(免费) → Continue + 免费额度

3. 你的项目规模？
   ├── 个人/小项目 → 任意工具
   ├── 中型团队 → 统一Copilot或Cursor
   └── 大型企业 → Cody + 合规审查
```

---

## 实践案例：配置你的AI工具

### 案例1：配置Cursor的.cursorrules

为了让Cursor更好地适配你的项目，创建一个`.cursorrules`文件：

```
# 项目技术栈
- React 18 + TypeScript
- Tailwind CSS for styling
- react-hook-form for forms
- React Query for data fetching
- Jest + React Testing Library for tests

# 代码规范
- Use functional components with hooks
- Prefer const over let
- Use async/await over promises
- Write unit tests for utilities
- Add PropTypes/interfaces for component props

# 项目约定
- Import aliases: @/components, @/utils, @/hooks
- API calls go through src/api/
- Utilities go in src/utils/
- Custom hooks go in src/hooks/

# 输出要求
- Always provide complete, runnable code
- Include necessary imports
- Add brief comments for complex logic
- Follow existing file structure
```

### 案例2：配置Copilot的提示词

Copilot虽然没有显式的规则文件，但你可以通过注释引导它：

```typescript
// 在文件顶部添加项目上下文注释
/**
 * Project: MyApp
 * Stack: React + TypeScript + Tailwind
 * Form library: react-hook-form
 * Data fetching: React Query
 * 
 * Code conventions:
 * - Use const/let, no var
 * - Prefer destructuring
 * - Use optional chaining
 * - Handle errors with try/catch
 */
```

### 案例3：多工具协作工作流

```
场景：开发一个新功能"用户个人资料页"

步骤1：用Cursor生成页面框架
- 打开Cursor Chat
- 描述需求："创建一个用户资料页，包含头像、昵称、简介编辑..."
- 选择生成文件，保存到项目

步骤2：用Copilot完善细节
- 打开生成的文件
- 手动编写核心逻辑，让Copilot补全周边代码
- 利用Copilot的上下文理解，自动使用项目中已有的工具函数

步骤3：用Cody检查依赖
- 询问Cody："这个页面使用了哪些API？"
- 确保所有API调用都符合项目规范
- 检查是否有类似实现可以复用
```

---

## 本章交付物

完成本章后，你应该拥有：

1. **一份工具选型清单**
   - 列出你选择的AI工具及理由
   - 明确每个工具的使用场景

2. **项目配置文件**
   - `.cursorrules`（如果使用Cursor）
   - 或类似的Copilot引导注释

3. **个人工作流文档**
   - 什么时候用什么工具
   - 工具之间的切换方式

---

## 行动清单

- [ ] 列出你常用的编程语言和框架
- [ ] 评估你当前的项目规模（个人/团队/企业）
- [ ] 试用至少两种AI工具（建议Cursor和Copilot）
- [ ] 创建你的.cursorrules或等效配置
- [ ] 记录一周的使用体验，优化你的工具组合

---

## 本章彩蛋

### AI工具的"隐藏技能"

**Cursor的隐藏功能**：
- `Ctrl+Shift+L`：选中所有相同文本（像VS Code的Ctrl+D，但AI增强）
- `@codebase`：让AI理解整个代码库的上下文
- `@web`：让AI搜索网络获取最新信息

**Copilot的隐藏功能**：
- `Ctrl+Enter`：查看多个补全建议
- `Alt+]`：切换到下一个补全建议
- 在注释中写"TODO:"或"FIXME:"，Copilot会给出实现建议

**Windsurf的Cascade模式指令**：
- "Implement"：实现某个功能
- "Find"：查找代码
- "Explain"：解释代码
- "Refactor"：重构代码

---

> **小张的一周总结**：
>
> "没有完美的工具，只有适合的工具。与其纠结选哪个，不如先选一个用起来，在实践中找到最适合自己的组合。
>
> 现在我用Copilot写日常代码，用Cursor做复杂任务，效率比以前高了一倍。最重要的是，我不再焦虑了——因为我知道每个工具都有自己的位置。"
