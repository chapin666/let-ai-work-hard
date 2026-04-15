#!/usr/bin/env python3
"""
增强版代码验证流水线
- 语法检查
- 可执行性验证（Python/JS/Bash）
- Prompt 模板验证
- 生成详细报告
"""
import os
import re
import json
import ast
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

WORK_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard")
CHAPTERS_DIR = WORK_DIR / "chapters"
REPORTS_DIR = WORK_DIR / "reports"
SNIPPETS_DIR = WORK_DIR / "scripts" / "extracted-snippets"

class CodeValidator:
    def __init__(self):
        self.issues = []
        self.fixed_issues = []
        self.code_stats = Counter()
        self.all_code_blocks = []
        self.executable_tests = []
        self.prompt_blocks = []
        
    def extract_code_blocks(self, text, filepath):
        """提取所有代码块"""
        pattern = r'^```(\S*)\s*\n(.*?)^```'
        for m in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
            lang = m.group(1).strip().lower()
            code = m.group(2)
            start_line = text[:m.start()].count('\n') + 1
            end_line = text[:m.end()].count('\n') + 1
            
            block = {
                'file': filepath,
                'lang': lang,
                'code': code,
                'start_line': start_line,
                'end_line': end_line,
                'id': f"{filepath.name}:{start_line}"
            }
            self.all_code_blocks.append(block)
            self.code_stats[lang if lang else 'none'] += 1
            
            # 分类存储
            if lang in ('python', 'javascript', 'js', 'typescript', 'ts', 'bash', 'shell'):
                self.executable_tests.append(block)
            if 'prompt' in code.lower() or lang in ('text', 'markdown'):
                if len(code) > 100 and ('角色' in code or '任务' in code or 'system' in code):
                    self.prompt_blocks.append(block)
    
    def validate_python(self, code, info):
        """Python 语法检查"""
        stripped = code.strip()
        if not stripped or stripped.startswith('#'):
            return True
        try:
            ast.parse(stripped)
            return True
        except SyntaxError as e:
            self.issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': 'python',
                'type': 'syntax',
                'problem': f"Python 语法错误: {e.msg} (line {e.lineno})",
                'suggestion': "检查代码块语法完整性",
                'severity': 'error'
            })
            return False
    
    def validate_json(self, code, info):
        """JSON 语法检查"""
        stripped = code.strip()
        if not stripped:
            return True
        # 移除注释
        lines = stripped.split('\n')
        cleaned = '\n'.join(l for l in lines if not l.strip().startswith('//'))
        try:
            json.loads(cleaned)
            return True
        except json.JSONDecodeError as e:
            self.issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': 'json',
                'type': 'syntax',
                'problem': f"JSON 解析错误: {e.msg}",
                'suggestion': "检查 JSON 语法，如缺少逗号、引号不匹配",
                'severity': 'error'
            })
            return False
    
    def validate_yaml(self, code, info):
        """YAML 语法检查"""
        try:
            import yaml
            stripped = code.strip()
            if not stripped:
                return True
            yaml.safe_load(stripped)
            return True
        except Exception as e:
            self.issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': 'yaml',
                'type': 'syntax',
                'problem': f"YAML 解析错误: {e}",
                'suggestion': "检查 YAML 缩进和语法",
                'severity': 'warning'
            })
            return False
    
    def validate_js_ts(self, code, info):
        """JS/TS 基础检查（括号匹配）"""
        stripped = code.strip()
        if not stripped:
            return True
            
        pairs = {'(': ')', '[': ']', '{': '}'}
        stack = []
        in_string = False
        string_char = None
        escaped = False
        
        for ch in stripped:
            if escaped:
                escaped = False
                continue
            if ch == '\\':
                escaped = True
                continue
            if ch in ('"', "'", '`'):
                if not in_string:
                    in_string = True
                    string_char = ch
                elif ch == string_char:
                    in_string = False
                    string_char = None
                continue
            if in_string:
                continue
            if ch in pairs:
                stack.append(ch)
            elif ch in pairs.values():
                if not stack:
                    self.issues.append({
                        'file': info['file'],
                        'lines': f"{info['start_line']}-{info['end_line']}",
                        'lang': info['lang'],
                        'type': 'syntax',
                        'problem': f"多余的闭合符号: {ch}",
                        'suggestion': "检查括号匹配",
                        'severity': 'error'
                    })
                    return False
                last = stack.pop()
                if pairs[last] != ch:
                    self.issues.append({
                        'file': info['file'],
                        'lines': f"{info['start_line']}-{info['end_line']}",
                        'lang': info['lang'],
                        'type': 'syntax',
                        'problem': f"括号不匹配: {last} 与 {ch}",
                        'suggestion': "检查括号匹配",
                        'severity': 'error'
                    })
                    return False
        
        if stack:
            self.issues.append({
                'file': info['file'],
                'lines': f"{info['start_line']}-{info['end_line']}",
                'lang': info['lang'],
                'type': 'syntax',
                'problem': f"未闭合的符号: {', '.join(stack)}",
                'suggestion': "检查括号匹配",
                'severity': 'error'
            })
            return False
        return True
    
    def test_executable(self, code, info):
        """测试代码是否可执行"""
        lang = info['lang']
        
        # 跳过明显不可执行的（如示例片段）
        if len(code.strip()) < 50:
            return {'status': 'skipped', 'reason': '代码太短，可能是示例片段'}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{lang}', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            if lang == 'python':
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return {'status': 'passed'}
                else:
                    return {'status': 'failed', 'error': result.stderr[:200]}
                    
            elif lang in ('javascript', 'js'):
                result = subprocess.run(
                    ['node', '--check', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return {'status': 'passed'}
                else:
                    return {'status': 'failed', 'error': result.stderr[:200]}
                    
            elif lang in ('bash', 'shell'):
                result = subprocess.run(
                    ['bash', '-n', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return {'status': 'passed'}
                else:
                    return {'status': 'failed', 'error': result.stderr[:200]}
            else:
                return {'status': 'skipped', 'reason': f'暂不支持 {lang} 的执行测试'}
                
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'reason': '执行超时'}
        except FileNotFoundError as e:
            return {'status': 'skipped', 'reason': f'缺少运行环境: {e}'}
        except Exception as e:
            return {'status': 'error', 'reason': str(e)[:200]}
        finally:
            os.unlink(temp_path)
    
    def extract_snippets(self):
        """提取所有可执行代码到独立文件"""
        SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
        
        # 清理旧文件
        for f in SNIPPETS_DIR.glob("*"):
            f.unlink()
        
        lang_ext = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'bash': 'sh',
            'shell': 'sh',
            'json': 'json',
            'yaml': 'yml',
            'sql': 'sql'
        }
        
        snippet_index = []
        for block in self.all_code_blocks:
            lang = block['lang']
            if lang not in lang_ext:
                continue
                
            ext = lang_ext[lang]
            filename = f"{block['file'].stem}_{block['start_line']}.{ext}"
            filepath = SNIPPETS_DIR / filename
            
            # 添加文件头注释
            header = f"""# Source: {block['file'].name}
# Lines: {block['start_line']}-{block['end_line']}
# Language: {lang}

"""
            filepath.write_text(header + block['code'], encoding='utf-8')
            
            snippet_index.append({
                'filename': filename,
                'source': str(block['file']),
                'lines': f"{block['start_line']}-{block['end_line']}",
                'lang': lang
            })
        
        # 保存索引
        index_path = SNIPPETS_DIR / 'index.json'
        index_path.write_text(json.dumps(snippet_index, indent=2, ensure_ascii=False), encoding='utf-8')
        
        return len(snippet_index)
    
    def run_all_checks(self):
        """运行所有检查"""
        print("🔍 开始代码验证流水线...")
        print(f"   扫描目录: {CHAPTERS_DIR}")
        
        # 1. 提取所有代码块
        print("\n📦 提取代码块...")
        for md_file in sorted(CHAPTERS_DIR.glob("*.md")):
            text = md_file.read_text(encoding='utf-8')
            self.extract_code_blocks(text, md_file)
        print(f"   共发现 {len(self.all_code_blocks)} 个代码块")
        
        # 2. 语法检查
        print("\n🔎 语法检查...")
        for block in self.all_code_blocks:
            lang = block['lang']
            if lang == 'python':
                self.validate_python(block['code'], block)
            elif lang in ('json',):
                self.validate_json(block['code'], block)
            elif lang in ('yaml', 'yml'):
                self.validate_yaml(block['code'], block)
            elif lang in ('javascript', 'typescript', 'js', 'ts'):
                self.validate_js_ts(block['code'], block)
        
        syntax_errors = len([i for i in self.issues if i['type'] == 'syntax'])
        print(f"   发现 {syntax_errors} 个语法问题")
        
        # 3. 可执行性测试
        print("\n⚙️ 可执行性测试...")
        executable_results = []
        for block in self.executable_tests[:50]:  # 限制数量避免太慢
            result = self.test_executable(block['code'], block)
            result['block'] = block
            executable_results.append(result)
        
        passed = len([r for r in executable_results if r['status'] == 'passed'])
        failed = len([r for r in executable_results if r['status'] == 'failed'])
        skipped = len([r for r in executable_results if r['status'] == 'skipped'])
        print(f"   通过: {passed}, 失败: {failed}, 跳过: {skipped}")
        
        # 4. 提取代码片段
        print("\n💾 提取代码片段...")
        snippet_count = self.extract_snippets()
        print(f"   已提取 {snippet_count} 个代码片段到 scripts/extracted-snippets/")
        
        # 5. 生成报告
        print("\n📝 生成报告...")
        self.generate_report(executable_results)
        print(f"   报告已保存到 reports/validation-report.md")
        
        return {
            'total_blocks': len(self.all_code_blocks),
            'issues': len(self.issues),
            'executable_passed': passed,
            'executable_failed': failed,
            'snippets': snippet_count
        }
    
    def generate_report(self, executable_results):
        """生成详细报告"""
        lines = []
        lines.append("# 代码验证报告")
        lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n**扫描范围**: {len(list(CHAPTERS_DIR.glob('*.md')))} 个章节文件")
        lines.append(f"\n**代码块总数**: {len(self.all_code_blocks)} 个")
        
        # 语言统计
        lines.append("\n## 语言统计\n")
        lines.append("| 语言 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        for lang, count in self.code_stats.most_common():
            pct = count / len(self.all_code_blocks) * 100
            lines.append(f"| {lang} | {count} | {pct:.1f}% |")
        
        # 语法问题
        lines.append("\n## 语法检查结果\n")
        if self.issues:
            lines.append(f"**发现 {len(self.issues)} 个问题**:\n")
            for idx, issue in enumerate(self.issues, 1):
                emoji = "🔴" if issue['severity'] == 'error' else "🟡"
                lines.append(f"### {idx}. {emoji} {issue['file'].name} (行 {issue['lines']})")
                lines.append(f"- **类型**: {issue['type']}")
                lines.append(f"- **语言**: {issue['lang']}")
                lines.append(f"- **问题**: {issue['problem']}")
                lines.append(f"- **建议**: {issue['suggestion']}")
                lines.append("")
        else:
            lines.append("✅ **未发现语法问题**")
        
        # 可执行性测试
        lines.append("\n## 可执行性测试\n")
        passed = len([r for r in executable_results if r['status'] == 'passed'])
        failed = len([r for r in executable_results if r['status'] == 'failed'])
        skipped = len([r for r in executable_results if r['status'] == 'skipped'])
        
        lines.append(f"- ✅ 通过: {passed}")
        lines.append(f"- ❌ 失败: {failed}")
        lines.append(f"- ⏭️ 跳过: {skipped}\n")
        
        if failed > 0:
            lines.append("### 执行失败的代码块\n")
            for r in executable_results:
                if r['status'] == 'failed':
                    block = r['block']
                    lines.append(f"- **{block['file'].name}:{block['start_line']}** ({block['lang']})")
                    lines.append(f"  - 错误: {r.get('error', '未知错误')[:100]}")
                    lines.append("")
        
        # Prompt 统计
        lines.append("\n## Prompt 模板统计\n")
        lines.append(f"共发现 **{len(self.prompt_blocks)}** 个疑似 Prompt 模板\n")
        lines.append("| 来源文件 | 行号 | 长度 |")
        lines.append("|----------|------|------|")
        for block in self.prompt_blocks[:20]:
            lines.append(f"| {block['file'].name} | {block['start_line']} | {len(block['code'])} 字符 |")
        if len(self.prompt_blocks) > 20:
            lines.append(f"| ... | ... | 还有 {len(self.prompt_blocks) - 20} 个 |")
        
        # 代码片段索引
        lines.append("\n## 提取的代码片段\n")
        lines.append(f"所有可执行代码片段已提取到 `scripts/extracted-snippets/`\n")
        lines.append(f"共 {len(list(SNIPPETS_DIR.glob('*'))) - 1} 个文件（不含 index.json）\n")
        
        # 保存报告
        REPORTS_DIR.mkdir(exist_ok=True)
        report_path = REPORTS_DIR / 'validation-report.md'
        report_path.write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    validator = CodeValidator()
    result = validator.run_all_checks()
    
    print("\n" + "="*50)
    print("📊 验证完成")
    print(f"   代码块: {result['total_blocks']}")
    print(f"   问题数: {result['issues']}")
    print(f"   可执行测试通过: {result['executable_passed']}")
    print(f"   代码片段: {result['snippets']}")
