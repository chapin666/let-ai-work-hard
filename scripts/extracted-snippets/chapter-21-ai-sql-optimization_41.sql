# Source: chapter-21-ai-sql-optimization.md
# Lines: 41-62
# Language: sql

SELECT 
  u.id,
  u.name,
  d.name as department,
  SUM(o.amount) as total_amount,
  COUNT(DISTINCT o.id) as order_count,
  AVG(o.amount) as avg_amount,
  MAX(o.created_at) as last_order_time
FROM users u
LEFT JOIN departments d ON u.department_id = d.id
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at >= '2024-01-01'
  AND o.created_at < '2024-02-01'
  AND o.status = 'completed'
  AND p.category IN ('A', 'B', 'C')
GROUP BY u.id, u.name, d.name
HAVING SUM(o.amount) > 10000
ORDER BY total_amount DESC;
