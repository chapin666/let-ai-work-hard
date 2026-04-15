# Source: chapter-35-ai-batch-processing.md
# Lines: 228-380
# Language: python

# analyze_codebase.py
import os
import re
import json
from pathlib import Path
from collections import defaultdict

class CodebaseAnalyzer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.stats = {
            'total_files': 0,
            'vue_files': 0,
            'js_files': 0,
            'patterns': defaultdict(int),
            'complexity_scores': {}
        }
    
    def analyze(self):
        """分析代码库"""
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                self._analyze_file(file_path)
        
        return self.stats
    
    def _analyze_file(self, file_path):
        """分析单个文件"""
        if file_path.suffix not in ['.vue', '.js']:
            return
        
        self.stats['total_files'] += 1
        if file_path.suffix == '.vue':
            self.stats['vue_files'] += 1
        else:
            self.stats['js_files'] += 1
        
        content = file_path.read_text(encoding='utf-8')
        
        # 检测各种模式
        patterns = {
            'options_api': r'export\s+default\s*\{',
            'data_function': r'data\s*\(\s*\)',
            'computed_props': r'computed:\s*\{',
            'watch_props': r'watch:\s*\{',
            'methods': r'methods:\s*\{',
            'lifecycle_beforeCreate': r'beforeCreate\s*\(',
            'lifecycle_created': r'created\s*\(',
            'lifecycle_beforeMount': r'beforeMount\s*\(',
            'lifecycle_mounted': r'mounted\s*\(',
            'lifecycle_beforeDestroy': r'beforeDestroy\s*\(',
            'lifecycle_destroyed': r'destroyed\s*\(',
            'filters': r'filters:\s*\{',
            'filters_usage': r'\|\s+\w+',
            'event_bus_emit': r'\$emit\s*\(',
            'event_bus_on': r'\$on\s*\(',
            'vue_set': r'Vue\.set\s*\(',
            'vue_delete': r'Vue\.delete\s*\(',
            'this_$refs': r'this\.\$refs',
            'mixins': r'mixins:\s*\[',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                self.stats['patterns'][pattern_name] += len(matches)
        
        # 计算复杂度分数（0-1）
        complexity = self._calculate_complexity(content)
        relative_path = str(file_path.relative_to(self.source_dir))
        self.stats['complexity_scores'][relative_path] = complexity
    
    def _calculate_complexity(self, content):
        """计算文件复杂度"""
        score = 0
        
        # 代码行数权重
        lines = content.split('\n')
        if len(lines) > 300:
            score += 0.3
        elif len(lines) > 100:
            score += 0.1
        
        # Options API复杂度
        if 'mixins' in content:
            score += 0.2
        if content.count('computed:') > 1:
            score += 0.1
        if content.count('watch:') > 2:
            score += 0.1
        
        # 特殊语法
        if 'provide' in content or 'inject' in content:
            score += 0.15
        if 'render' in content:
            score += 0.15
        
        return min(score, 1.0)
    
    def generate_migration_plan(self):
        """生成迁移计划"""
        plan = {
            'summary': {
                'total_files': self.stats['total_files'],
                'total_patterns': dict(self.stats['patterns']),
            },
            'batches': []
        }
        
        # 按复杂度排序
        sorted_files = sorted(
            self.stats['complexity_scores'].items(),
            key=lambda x: x[1]
        )
        
        # 分批处理
        # Batch 1: 简单文件（自动处理）
        simple_files = [f for f, s in sorted_files if s < 0.3]
        plan['batches'].append({
            'name': 'auto_batch',
            'strategy': 'automatic',
            'files': simple_files,
            'count': len(simple_files)
        })
        
        # Batch 2: 中等复杂度（AI辅助）
        medium_files = [f for f, s in sorted_files if 0.3 <= s < 0.7]
        plan['batches'].append({
            'name': 'ai_batch',
            'strategy': 'ai_assisted',
            'files': medium_files,
            'count': len(medium_files)
        })
        
        # Batch 3: 高复杂度（人工处理）
        complex_files = [f for f, s in sorted_files if s >= 0.7]
        plan['batches'].append({
            'name': 'manual_batch',
            'strategy': 'manual',
            'files': complex_files,
            'count': len(complex_files)
        })
        
        return plan

# 执行分析
analyzer = CodebaseAnalyzer('./src')
stats = analyzer.analyze()
plan = analyzer.generate_migration_plan()

print(json.dumps(plan, indent=2))
