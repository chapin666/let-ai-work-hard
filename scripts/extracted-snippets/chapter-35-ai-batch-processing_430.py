# Source: chapter-35-ai-batch-processing.md
# Lines: 430-512
# Language: python

# batch_transform.py
import re
from pathlib import Path

class BatchTransformer:
    def __init__(self, rules_file):
        self.rules = self._load_rules(rules_file)
    
    def transform(self, file_path, output_path):
        """转换单个文件"""
        content = Path(file_path).read_text(encoding='utf-8')
        
        for rule in self.rules:
            if rule['type'] == 'regex':
                content = re.sub(rule['pattern'], rule['replacement'], content)
            elif rule['type'] == 'string':
                content = content.replace(rule['pattern'], rule['replacement'])
        
        Path(output_path).write_text(content, encoding='utf-8')
        return True
    
    def transform_batch(self, file_list, output_dir):
        """批量转换"""
        results = []
        for file_path in file_list:
            try:
                output_path = Path(output_dir) / Path(file_path).name
                self.transform(file_path, output_path)
                results.append({'file': file_path, 'status': 'success'})
            except Exception as e:
                results.append({'file': file_path, 'status': 'error', 'error': str(e)})
        
        return results

# 定义转换规则
rules = [
    # 生命周期钩子
    {
        'type': 'regex',
        'pattern': r'\bbeforeDestroy\s*\(',
        'replacement': 'beforeUnmount('
    },
    {
        'type': 'regex',
        'pattern': r'\bdestroyed\s*\(',
        'replacement': 'unmounted('
    },
    # Vue 3中已移除的语法
    {
        'type': 'regex',
        'pattern': r'Vue\.set\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)',
        'replacement': r'\1[\2] = \3'
    },
    {
        'type': 'regex',
        'pattern': r'Vue\.delete\s*\(\s*([^,]+),\s*([^)]+)\)',
        'replacement': r'delete \1[\2]'
    },
    # v-model语法（简单情况）
    {
        'type': 'regex',
        'pattern': r'v-model\.sync',
        'replacement': 'v-model'
    },
    # v-for key位置
    {
        'type': 'regex',
        'pattern': r'v-for="([^"]+)"\s+:key="([^"]+)"',
        'replacement': r'v-for="\1" :key="\2"'
    },
    # 事件修饰符
    {
        'type': 'regex',
        'pattern': r'@([^=]+)\.native',
        'replacement': r'@\1'
    },
]

# 批量转换
transformer = BatchTransformer(rules)
results = transformer.transform_batch(simple_files, './migrated/auto/')
