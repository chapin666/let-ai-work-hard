# Source: chapter-21-ai-sql-optimization.md
# Lines: 537-569
# Language: javascript

// scripts/slow-query-analyzer.js
const { analyzeSlowQuery } = require('./ai-helper');

async function analyzeSlowQueries() {
  // 从数据库获取慢查询日志
  const slowQueries = await db.query(`
    SELECT 
      sql_text,
      avg_timer_wait / 1000000000 as avg_time_ms,
      count_star
    FROM performance_schema.events_statements_summary_by_digest
    WHERE avg_timer_wait > 10000000000  -- > 10秒
    ORDER BY avg_timer_wait DESC
    LIMIT 10
  `);
  
  for (const query of slowQueries) {
    console.log(`\n分析慢查询: ${query.sql_text.substring(0, 100)}...`);
    
    const analysis = await analyzeSlowQuery(query.sql_text, {
      avgTime: query.avg_time_ms,
      executionCount: query.count_star,
    });
    
    // 生成优化建议报告
    await generateOptimizationReport(query, analysis);
  }
}

// 定时执行
setInterval(analyzeSlowQueries, 24 * 60 * 60 * 1000); // 每天一次
