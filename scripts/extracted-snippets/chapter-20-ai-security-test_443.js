# Source: chapter-20-ai-security-test.md
# Lines: 443-474
# Language: javascript

// scripts/ai-security-check.js
const { execSync } = require('child_process');
const { analyzeSecurity } = require('./ai-helper');

async function main() {
  // 获取变更的文件
  const diff = execSync('git diff --cached --name-only').toString();
  const files = diff.split('\n').filter(f => f.endsWith('.js') || f.endsWith('.ts'));
  
  console.log(`Checking ${files.length} files for security issues...`);
  
  for (const file of files) {
    const content = execSync(`git show :${file}`).toString();
    
    // 只检查变更的代码块
    const analysis = await analyzeSecurity(content, {
      focus: ['authentication', 'authorization', 'injection', 'xss'],
    });
    
    if (analysis.riskScore > 7) {
      console.error(`❌ High risk detected in ${file}:`);
      console.error(analysis.issues.map(i => `  - ${i.description}`).join('\n'));
      process.exit(1);
    }
  }
  
  console.log('✅ Security check passed');
}

main();
