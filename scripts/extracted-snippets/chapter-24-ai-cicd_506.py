# Source: chapter-24-ai-cicd.md
# Lines: 506-613
# Language: python

#!/usr/bin/env python3
"""
generate_changelog.py - 自动生成发布变更日志
"""

import subprocess
import re
import sys
from datetime import datetime

def get_commits_between(from_tag, to_ref="HEAD"):
    """获取两个版本之间的所有提交"""
    cmd = f"git log {from_tag}..{to_ref} --pretty=format:'%h|%s|%an|%ad' --date=short --no-merges"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            hash_, message, author, date = line.split('|', 3)
            commits.append({
                'hash': hash_,
                'message': message,
                'author': author,
                'date': date
            })
    return commits

def categorize_commit(message):
    """根据提交信息分类"""
    patterns = {
        'feature': r'^(feat|feature)\s*:?\s*',
        'bugfix': r'^(fix|bugfix)\s*:?\s*',
        'docs': r'^(docs|doc)\s*:?\s*',
        'refactor': r'^refactor\s*:?\s*',
        'performance': r'^(perf|performance)\s*:?\s*',
        'security': r'^security\s*:?\s*',
    }
    
    for category, pattern in patterns.items():
        if re.match(pattern, message, re.IGNORECASE):
            return category
    return 'other'

def generate_changelog(commits):
    """生成格式化的变更日志"""
    categories = {
        'feature': [],
        'bugfix': [],
        'performance': [],
        'security': [],
        'refactor': [],
        'docs': [],
        'other': []
    }
    
    for commit in commits:
        category = categorize_commit(commit['message'])
        categories[category].append(commit)
    
    changelog = f"""# 发布变更日志
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 概览
- 提交总数: {len(commits)}
- 新功能: {len(categories['feature'])}
- Bug修复: {len(categories['bugfix'])}
- 性能优化: {len(categories['performance'])}
- 安全更新: {len(categories['security'])}

"""
    
    category_names = {
        'feature': '🚀 新功能',
        'bugfix': '🐛 Bug修复',
        'performance': '⚡ 性能优化',
        'security': '🔒 安全更新',
        'refactor': '🔧 代码重构',
        'docs': '📚 文档更新',
        'other': '📝 其他变更'
    }
    
    for category, items in categories.items():
        if items:
            changelog += f"## {category_names[category]}\n\n"
            for item in items:
                changelog += f"- **{item['hash']}** {item['message']} ({item['author']})\n"
            changelog += "\n"
    
    return changelog

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python generate_changelog.py <from_tag> [to_ref]")
        sys.exit(1)
    
    from_tag = sys.argv[1]
    to_ref = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    
    commits = get_commits_between(from_tag, to_ref)
    changelog = generate_changelog(commits)
    
    print(changelog)
    
    # 保存到文件
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)
