# Source: chapter-21-ai-sql-optimization.md
# Lines: 856-889
# Language: bash

# MySQL：查看表的索引使用情况
mysql -e "SELECT 
  TABLE_NAME, 
  INDEX_NAME, 
  CARDINALITY, 
  COLUMN_NAME 
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'your_db' 
AND TABLE_NAME = 'your_table';
"

# 查看索引使用效率（需要开启performance_schema）
mysql -e "SELECT 
  OBJECT_SCHEMA, 
  OBJECT_NAME, 
  INDEX_NAME, 
  COUNT_FETCH, 
  COUNT_INSERT 
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE OBJECT_SCHEMA = 'your_db';
"

# PostgreSQL：查看慢查询
psql -c "SELECT 
  query, 
  calls, 
  mean_time, 
  total_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"
