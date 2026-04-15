# Source: chapter-21-ai-sql-optimization.md
# Lines: 503-533
# Language: javascript

// scripts/ai-sql-review.js
const fs = require('fs');
const { analyzeSQL } = require('./ai-helper');

async function reviewSQL(filePath) {
  const sql = fs.readFileSync(filePath, 'utf-8');
  
  const analysis = await analyzeSQL(sql, {
    dbType: 'mysql',
    tableStats: loadTableStats(),
  });
  
  // 如果有严重问题，退出非零
  if (analysis.criticalIssues.length > 0) {
    console.error('❌ Critical SQL issues found:');
    analysis.criticalIssues.forEach(issue => {
      console.error(`  - ${issue.description}`);
    });
    process.exit(1);
  }
  
  // 输出建议
  if (analysis.suggestions.length > 0) {
    console.log('💡 Suggestions:');
    analysis.suggestions.forEach(s => console.log(`  - ${s}`));
  }
}

reviewSQL(process.argv[2]);
