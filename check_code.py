#!/usr/bin/env python3
"""
提取并验证 Markdown 文件中的代码块
"""
import os
import re
import json
import ast
from collections import Counter
from pathlib import Path

WORK_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard")
CHAPTERS_DIR = WORK_DIR / "chapters"
REPORTS_DIR = WORK_DIR / "reports"

issues = []
fixed_issues = []
code_stats = Counter()
all_code_blocks = []

def extract_code_blocks(text, filepath):
    for m in re.finditer(r'^```(\S*)\s*\n(.*?)^```', text, re.MULTILINE | re.DOTALL):
        lang = m.group(1).strip().lower()
        code = m.group(2)
        start_line = text[:m.start()].count('\n') + 1
        end_line = text[:m.end()].count('\n') + 1
        all_code_blocks.append({
            'file': filepath,
            'lang': lang,
            'code': code,
            'start_line': start_line,
            'end_line': end_line,
        })
        code_stats[lang if lang else 'none'] += 1

for md_file in sorted(CHAPTERS_DIR.glob("*.md")):
    text = md_file.read_text(encoding='utf-8')
    extract_code_blocks(text, md_file.name)

print(f"共发现 {len(all_code_blocks)} 个代码块")
print("语言统计:")
for lang, count in code_stats.most_common():
    print(f"  {lang}: {count}")

def validate_python(code, info):
    stripped = code.strip()
    if not stripped:
        return
    if stripped.startswith('#') and '\n' not in stripped:
        return
    try:
        ast.parse(stripped)
    except SyntaxError as e:
        # 检查是否是 Markdown 嵌套导致（代码块内包含 ```）
        if '```' in stripped:
            issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': 'python',
                'problem': f"Python 语法错误（可能是 Markdown 代码块嵌套截断导致）: {e.msg} (line {e.lineno})",
                'suggestion': "检查 Markdown 中是否嵌套了其他代码块，导致 Python 代码被提前截断"
            })
        else:
            issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': 'python',
                'problem': f"Python 语法错误: {e.msg} (line {e.lineno})",
                'suggestion': "检查代码块的语法完整性"
            })

def validate_json(code, info):
    stripped = code.strip()
    if not stripped:
        return
    cleaned = stripped
    if stripped.startswith('//') or stripped.startswith('/*'):
        lines = stripped.split('\n')
        cleaned_lines = [l for l in lines if not l.strip().startswith('//')]
        cleaned = '\n'.join(cleaned_lines).strip()
    try:
        json.loads(cleaned)
    except json.JSONDecodeError as e:
        issues.append({
            'file': info['file'],
            'lines': f"{info['start_line']}-{info['end_line']}",
            'lang': 'json',
            'problem': f"JSON 解析错误: {e.msg} (char {e.colno})",
            'suggestion': "检查 JSON 语法，如缺少逗号、引号不匹配等"
        })

def validate_yaml(code, info):
    import yaml
    stripped = code.strip()
    if not stripped:
        return
    try:
        yaml.safe_load(stripped)
    except Exception as e:
        issues.append({
            'file': info['file'],
            'lines': f"{info['start_line']}-{info['end_line']}",
            'lang': 'yaml',
            'problem': f"YAML 解析错误: {e}",
            'suggestion': "检查 YAML 缩进和语法"
        })

def validate_sql(code, info):
    stripped = code.strip()
    if not stripped:
        return
    problems = []
    open_parens = stripped.count('(')
    close_parens = stripped.count(')')
    if open_parens != close_parens:
        problems.append(f"括号不匹配: ({open_parens} vs ){close_parens}")
    in_single = False
    in_double = False
    escaped = False
    for ch in stripped:
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
    if in_single or in_double:
        problems.append("字符串引号未闭合")
    if problems:
        issues.append({
            'file': info['file'],
            'lines': f"{info['start_line']}-{info['end_line']}",
            'lang': 'sql',
            'problem': "; ".join(problems),
            'suggestion': "检查 SQL 语法完整性"
        })

def validate_js_ts(code, info):
    stripped = code.strip()
    if not stripped:
        return
    # JS/TS 中 > 操作符（>, >=, =>, >>, >>>）极易与尖括号混淆，
    # 且 JSX/TSX 大量使用 <>，因此完全不做尖括号检查
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = []
    in_single = False
    in_double = False
    in_backtick = False
    escaped = False
    prev_char = ''
    for ch in stripped:
        if escaped:
            escaped = False
            prev_char = ch
            continue
        if ch == '\\':
            escaped = True
            prev_char = ch
            continue
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
            prev_char = ch
            continue
        if ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
            prev_char = ch
            continue
        if ch == '`' and not in_single and not in_double:
            in_backtick = not in_backtick
            prev_char = ch
            continue
        if in_single or in_double or in_backtick:
            prev_char = ch
            continue
        if ch in pairs:
            stack.append(ch)
        elif ch in pairs.values():
            if not stack:
                issues.append({
                    'file': info['file'],
                    'lines': f"{info['start_line']}-{info['end_line']}",
                    'lang': info['lang'],
                    'problem': f"多余的闭合符号: {ch}",
                    'suggestion': "检查括号匹配"
                })
                return
            last = stack.pop()
            if pairs[last] != ch:
                issues.append({
                    'file': info['file'],
                    'lines': f"{info['start_line']}-{info['end_line']}",
                    'lang': info['lang'],
                    'problem': f"括号不匹配: {last} 与 {ch}",
                    'suggestion': "检查括号匹配"
                })
                return
        prev_char = ch
    if stack:
        issues.append({
            'file': info['file'],
            'lines': f"{info['start_line']}-{info['end_line']}",
            'lang': info['lang'],
            'problem': f"未闭合的符号: {', '.join(stack)}",
            'suggestion': "检查括号匹配"
        })

def check_prompt_integrity(text, filepath):
    prompts = re.finditer(r'^```(?:text|markdown)?\s*\n(.*?)```', text, re.MULTILINE | re.DOTALL)
    for m in prompts:
        content = m.group(1)
        start_line = text[:m.start()].count('\n') + 1
        markers = [
            ('{{', '}}'),
            ('{%', '%}'),
        ]
        for open_m, close_m in markers:
            open_count = content.count(open_m)
            close_count = content.count(close_m)
            if open_count != close_count:
                issues.append({
                    'file': filepath,
                    'lines': f"{start_line}",
                    'lang': 'prompt',
                    'problem': f"Prompt 模板中 '{open_m}' 和 '{close_m}' 数量不匹配 ({open_count} vs {close_count})",
                    'suggestion': "检查模板变量的闭合"
                })
        # 检查 XML 风格标签是否成对
        tags = re.findall(r'<(/?)([a-zA-Z_][a-zA-Z0-9_-]*)[^>]*>', content)
        tag_stack = []
        for slash, tag_name in tags:
            if slash:
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
                else:
                    issues.append({
                        'file': filepath,
                        'lines': f"{start_line}",
                        'lang': 'prompt',
                        'problem': f"XML 标签不匹配: </{tag_name}>",
                        'suggestion': f"检查 <{tag_name}> 标签是否正确闭合"
                    })
                    break
            else:
                tag_stack.append(tag_name)
        if tag_stack:
            issues.append({
                'file': filepath,
                'lines': f"{start_line}",
                'lang': 'prompt',
                'problem': f"XML 标签未闭合: {', '.join(tag_stack)}",
                'suggestion': "检查 XML 风格标签是否正确闭合"
            })

for block in all_code_blocks:
    lang = block['lang']
    code = block['code']
    if lang in ('python',):
        validate_python(code, block)
    elif lang in ('json',):
        validate_json(code, block)
    elif lang in ('yaml', 'yml'):
        validate_yaml(code, block)
    elif lang in ('sql',):
        validate_sql(code, block)
    elif lang in ('javascript', 'typescript', 'js', 'ts', 'jsx', 'tsx'):
        validate_js_ts(code, block)

for md_file in sorted(CHAPTERS_DIR.glob("*.md")):
    text = md_file.read_text(encoding='utf-8')
    check_prompt_integrity(text, md_file.name)

# 记录已修复的问题
fixed_issues.append(r"chapter-35-ai-batch-processing.md: 将 YAML 中的非法转义序列 `\"this.\$refs\"` 修复为单引号包裹 `'this.$refs'`")

print(f"\n发现问题: {len(issues)} 个")
for i in issues[:20]:
    print(i)

report_lines = []
report_lines.append("# 代码检查报告")
report_lines.append("")
report_lines.append("## 检查范围")
report_lines.append("")
report_lines.append(f"- 工作目录: `{WORK_DIR}`")
report_lines.append(f"- 扫描文件: `chapters/*.md` (共 {len(list(CHAPTERS_DIR.glob('*.md')))} 个文件)")
report_lines.append(f"- 提取代码块: {len(all_code_blocks)} 个")
report_lines.append("")
report_lines.append("## 代码块统计（按语言）")
report_lines.append("")
report_lines.append("| 语言 | 数量 |")
report_lines.append("|------|------|")
for lang, count in code_stats.most_common():
    report_lines.append(f"| {lang} | {count} |")
report_lines.append("")

report_lines.append("## 发现的问题")
report_lines.append("")
if issues:
    report_lines.append(f"共发现 **{len(issues)}** 个问题：")
    report_lines.append("")
    for idx, issue in enumerate(issues, 1):
        report_lines.append(f"### {idx}. {issue['file']} (行 {issue['lines']})")
        report_lines.append("")
        report_lines.append(f"- **问题类型**: {issue['lang']}")
        report_lines.append(f"- **问题描述**: {issue['problem']}")
        report_lines.append(f"- **建议修复**: {issue['suggestion']}")
        report_lines.append("")
else:
    report_lines.append("未发现明显问题。")
    report_lines.append("")

if fixed_issues:
    report_lines.append("## 自动修复")
    report_lines.append("")
    for fix in fixed_issues:
        report_lines.append(f"- {fix}")
    report_lines.append("")

report_lines.append("## 检查结论")
report_lines.append("")
if issues:
    report_lines.append(f"本次检查共扫描 {len(all_code_blocks)} 个代码块，发现 {len(issues)} 个问题。")
    report_lines.append("建议逐一核对上述问题，尤其是 Markdown 嵌套代码块截断、JSON 注释和 SQL 语句的语法完整性。")
else:
    report_lines.append(f"本次检查共扫描 {len(all_code_blocks)} 个代码块，所有检查的代码块语法均正常。")
report_lines.append("")

REPORTS_DIR.mkdir(exist_ok=True)
report_path = REPORTS_DIR / "batch3-code-report.md"
report_path.write_text("\n".join(report_lines), encoding='utf-8')
print(f"\n报告已保存到: {report_path}")
