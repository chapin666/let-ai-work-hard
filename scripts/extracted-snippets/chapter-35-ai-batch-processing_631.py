# Source: chapter-35-ai-batch-processing.md
# Lines: 631-688
# Language: python

# validate_migration.py
import subprocess
from pathlib import Path

class MigrationValidator:
    def validate_syntax(self, file_path):
        """语法检查"""
        try:
            # Vue单文件语法检查
            result = subprocess.run(
                ['vue-tsc', '--noEmit', file_path],
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)
    
    def validate_lint(self, file_path):
        """代码规范检查"""
        try:
            result = subprocess.run(
                ['eslint', file_path],
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)
    
    def validate_all(self, migrated_dir):
        """验证所有迁移文件"""
        results = []
        
        for vue_file in Path(migrated_dir).rglob('*.vue'):
            file_result = {
                'file': str(vue_file),
                'syntax_valid': False,
                'lint_valid': False
            }
            
            # 语法检查
            syntax_ok, syntax_err = self.validate_syntax(vue_file)
            file_result['syntax_valid'] = syntax_ok
            if not syntax_ok:
                file_result['syntax_error'] = syntax_err
            
            # 规范检查
            lint_ok, lint_err = self.validate_lint(vue_file)
            file_result['lint_valid'] = lint_ok
            if not lint_ok:
                file_result['lint_error'] = lint_err
            
            results.append(file_result)
        
        return results
