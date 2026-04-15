#!/usr/bin/env python3
"""
Prompt 索引生成器
- 提取全书所有 Prompt 模板
- 按类型分类
- 生成可检索的索引
"""
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

WORK_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard")
CHAPTERS_DIR = WORK_DIR / "chapters"
OUTPUT_DIR = WORK_DIR

class PromptExtractor:
    """Prompt 提取器"""
    
    # Prompt 类型识别模式
    PATTERNS = {
        'system': [
            r'role\s*[=:]\s*["\']system["\']',
            r'system[_-]?prompt',
            r'【角色】|【任务】|【输出格式】',
            r'^你是.*专家',
        ],
        'code_generation': [
            r'生成.*代码',
            r'编写.*(函数|类|组件)',
            r'实现.*功能',
            r'convert|refactor|rewrite',
            r'优化.*代码',
        ],
        'review': [
            r'审查|review|检查.*代码',
            r'找出.*问题',
            r'bug|issue|problem',
        ],
        'explanation': [
            r'解释|explain|说明',
            r'什么是|how does',
            r'为什么|why',
        ],
        'testing': [
            r'测试|test',
            r'单元测试|unittest',
            r'测试用例',
        ],
        'documentation': [
            r'文档|doc',
            r'注释|comment',
            r'README',
        ],
        'chat': [
            r'对话|chat',
            r'conversation',
        ],
    }
    
    def __init__(self):
        self.prompts = []
        self.stats = defaultdict(int)
        
    def classify_prompt(self, text):
        """对 Prompt 进行分类"""
        text_lower = text.lower()
        scores = {}
        
        for category, patterns in self.PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'general'
    
    def extract_prompts_from_file(self, filepath):
        """从单个文件提取 Prompt"""
        text = filepath.read_text(encoding='utf-8')
        prompts = []
        
        # 模式1: 代码块中的 Prompt (XML/结构化格式)
        # 匹配 system prompt 或角色定义
        system_blocks = re.finditer(
            r'^```(?:text|markdown|xml)?\s*\n(.*?)```',
            text,
            re.MULTILINE | re.DOTALL
        )
        for m in system_blocks:
            content = m.group(1)
            if self._is_prompt(content):
                start_line = text[:m.start()].count('\n') + 1
                prompts.append({
                    'type': 'code_block',
                    'content': content.strip(),
                    'line': start_line,
                    'category': self.classify_prompt(content),
                    'length': len(content),
                })
        
        # 模式2: 行内 Prompt (用引号标注)
        inline_prompts = re.finditer(
            r'[Pp]rompt[:：]\s*["\'](.+?)["\']',
            text
        )
        for m in inline_prompts:
            content = m.group(1)
            if len(content) > 30:
                start_line = text[:m.start()].count('\n') + 1
                prompts.append({
                    'type': 'inline',
                    'content': content.strip(),
                    'line': start_line,
                    'category': self.classify_prompt(content),
                    'length': len(content),
                })
        
        # 模式3: JSON 格式的 messages
        json_prompts = re.finditer(
            r'```json\s*\n(\[.*?\{.*?role.*?content.*?\}.*?\])\s*```',
            text,
            re.DOTALL
        )
        for m in json_prompts:
            content = m.group(1)
            if '"system"' in content or '"user"' in content:
                start_line = text[:m.start()].count('\n') + 1
                prompts.append({
                    'type': 'json_format',
                    'content': content.strip(),
                    'line': start_line,
                    'category': self.classify_prompt(content),
                    'length': len(content),
                })
        
        return prompts
    
    def _is_prompt(self, text):
        """判断文本是否是 Prompt"""
        if len(text) < 50:
            return False
        
        # 特征检测
        indicators = [
            'role', 'system', 'user', 'assistant',
            '【角色】', '【任务】', '【要求】', '【输出】',
            'prompt', 'instruction',
            '你是', '请', '需要',
        ]
        
        return any(ind in text.lower() for ind in indicators)
    
    def extract_all(self):
        """提取全书所有 Prompt"""
        print("📚 扫描章节文件...")
        
        for md_file in sorted(CHAPTERS_DIR.glob("chapter-*.md")):
            chapter_prompts = self.extract_prompts_from_file(md_file)
            
            # 提取章节信息
            chapter_match = re.match(r'chapter-(\d+)', md_file.stem)
            chapter_num = int(chapter_match.group(1)) if chapter_match else 0
            
            # 读取章节标题
            first_lines = md_file.read_text(encoding='utf-8').split('\n')[:5]
            title = ""
            for line in first_lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            
            for p in chapter_prompts:
                p['chapter'] = chapter_num
                p['chapter_title'] = title
                p['file'] = md_file.name
                self.stats[p['category']] += 1
            
            self.prompts.extend(chapter_prompts)
        
        print(f"   共发现 {len(self.prompts)} 个 Prompt")
        return self.prompts
    
    def generate_markdown_index(self):
        """生成 Markdown 格式的索引"""
        lines = []
        lines.append("# Prompt 索引")
        lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n**Prompt 总数**: {len(self.prompts)} 个\n")
        
        # 统计概览
        lines.append("## 分类统计\n")
        lines.append("| 类型 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        for cat, count in sorted(self.stats.items(), key=lambda x: -x[1]):
            pct = count / len(self.prompts) * 100 if self.prompts else 0
            cat_name = {
                'system': '系统/角色定义',
                'code_generation': '代码生成',
                'review': '代码审查',
                'explanation': '解释说明',
                'testing': '测试相关',
                'documentation': '文档生成',
                'chat': '对话',
                'general': '通用/其他',
            }.get(cat, cat)
            lines.append(f"| {cat_name} | {count} | {pct:.1f}% |")
        
        # 按章节组织
        lines.append("\n## 按章节索引\n")
        
        by_chapter = defaultdict(list)
        for p in self.prompts:
            by_chapter[p['chapter']].append(p)
        
        for ch_num in sorted(by_chapter.keys()):
            prompts = by_chapter[ch_num]
            if not prompts:
                continue
            
            title = prompts[0]['chapter_title']
            file = prompts[0]['file']
            
            lines.append(f"### 第{ch_num}章: {title}\n")
            lines.append(f"📄 [{file}](./chapters/{file})\n")
            
            for idx, p in enumerate(prompts, 1):
                cat_name = {
                    'system': '系统',
                    'code_generation': '生成',
                    'review': '审查',
                    'explanation': '解释',
                    'testing': '测试',
                    'documentation': '文档',
                    'chat': '对话',
                    'general': '通用',
                }.get(p['category'], p['category'])
                
                # 提取前 60 字符作为摘要
                preview = p['content'].replace('\n', ' ')[:60] + '...'
                lines.append(f"{idx}. **{cat_name}** (行{p['line']}) - {preview}")
            lines.append("")
        
        # 热门 Prompt 列表
        lines.append("\n## 精选 Prompt 模板\n")
        lines.append("按使用场景分类的完整 Prompt:\n")
        
        by_category = defaultdict(list)
        for p in self.prompts:
            by_category[p['category']].append(p)
        
        for cat in ['system', 'code_generation', 'review', 'testing', 'documentation']:
            if cat not in by_category:
                continue
            
            cat_name = {
                'system': '系统/角色定义',
                'code_generation': '代码生成',
                'review': '代码审查',
                'testing': '测试',
                'documentation': '文档',
            }.get(cat, cat)
            
            lines.append(f"### {cat_name}\n")
            
            # 取每个分类最长的几个作为示例
            examples = sorted(by_category[cat], key=lambda x: -x['length'])[:3]
            for ex in examples:
                lines.append(f"**来源**: 第{ex['chapter']}章 {ex['chapter_title']} (行{ex['line']})\n")
                lines.append("```")
                # 截取前 500 字符
                content = ex['content'][:500]
                if len(ex['content']) > 500:
                    content += "\n... (截断)"
                lines.append(content)
                lines.append("```\n")
        
        return '\n'.join(lines)
    
    def generate_json_index(self):
        """生成 JSON 格式的索引"""
        return {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'total_prompts': len(self.prompts),
                'categories': dict(self.stats),
            },
            'prompts': [
                {
                    'chapter': p['chapter'],
                    'chapter_title': p['chapter_title'],
                    'file': p['file'],
                    'line': p['line'],
                    'type': p['type'],
                    'category': p['category'],
                    'length': p['length'],
                    'preview': p['content'][:100] + '...',
                }
                for p in self.prompts
            ]
        }
    
    def run(self):
        """运行提取流程"""
        print("🚀 开始生成 Prompt 索引...\n")
        
        # 提取
        self.extract_all()
        
        # 生成 Markdown 索引
        print("\n📝 生成 Markdown 索引...")
        md_content = self.generate_markdown_index()
        md_path = OUTPUT_DIR / 'PROMPTS.md'
        md_path.write_text(md_content, encoding='utf-8')
        print(f"   已保存: {md_path}")
        
        # 生成 JSON 索引
        print("\n📊 生成 JSON 索引...")
        json_data = self.generate_json_index()
        json_path = OUTPUT_DIR / 'prompts-index.json'
        json_path.write_text(
            json.dumps(json_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        print(f"   已保存: {json_path}")
        
        # 生成使用指南
        print("\n📖 生成使用指南...")
        guide_content = self._generate_usage_guide()
        guide_path = OUTPUT_DIR / 'PROMPTS-GUIDE.md'
        guide_path.write_text(guide_content, encoding='utf-8')
        print(f"   已保存: {guide_path}")
        
        print("\n" + "="*50)
        print("✅ Prompt 索引生成完成!")
        print(f"   发现 {len(self.prompts)} 个 Prompt")
        print(f"   分类: {list(self.stats.keys())}")
        print("\n生成的文件:")
        print(f"   - PROMPTS.md (完整索引)")
        print(f"   - prompts-index.json (机器可读)")
        print(f"   - PROMPTS-GUIDE.md (使用指南)")
    
    def _generate_usage_guide(self):
        """生成 Prompt 使用指南"""
        return """# Prompt 使用指南

本文档说明如何使用本书中的 Prompt 模板。

## 快速开始

1. **查找 Prompt**: 打开 [PROMPTS.md](./PROMPTS.md) 浏览所有模板
2. **按场景筛选**: 根据分类(代码生成/审查/测试等)找到需要的模板
3. **复制使用**: 复制模板内容到 ChatGPT/Claude/Cursor 中使用

## Prompt 类型说明

### 系统/角色定义
设定 AI 的角色和专业领域，通常放在对话开头。

```
你是资深前端工程师，擅长 React 和 TypeScript...
```

### 代码生成
用于让 AI 生成代码的模板，通常包含:
- 功能描述
- 技术栈要求
- 输入/输出格式

### 代码审查
让 AI 检查代码问题的模板，可以指定:
- 检查维度(性能/安全/可读性)
- 输出格式
- 严重程度分级

### 测试相关
生成测试用例或测试代码的模板。

## 使用技巧

1. **变量替换**: 模板中的 `{variable}` 需要替换为实际值
2. **上下文补充**: 根据具体情况添加必要的背景信息
3. **迭代优化**: 根据第一次输出调整 Prompt 以获得更好结果

## 自定义 Prompt

参考本书模板结构，构建自己的 Prompt:

```
【角色】
你是...

【任务】
请...

【要求】
1. ...
2. ...

【输入】
```
...
```

【输出格式】
...
```

---

更多示例请参考各章节内容。
"""


if __name__ == '__main__':
    extractor = PromptExtractor()
    extractor.run()
