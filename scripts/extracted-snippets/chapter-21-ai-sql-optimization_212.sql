# Source: chapter-21-ai-sql-optimization.md
# Lines: 212-264
# Language: sql

-- 优化后的查询
WITH valid_products AS (
  -- 先过滤出符合条件的商品（数量很少）
  SELECT id FROM products WHERE category IN ('A', 'B', 'C')
),
valid_order_items AS (
  -- 再找出包含这些商品的订单项
  SELECT DISTINCT oi.order_id
  FROM order_items oi
  WHERE EXISTS (SELECT 1 FROM valid_products vp WHERE vp.id = oi.product_id)
),
valid_orders AS (
  -- 最后找出符合条件的订单（最关键的一步，大幅减少数据量）
  SELECT 
    o.id,
    o.user_id,
    o.amount,
    o.created_at
  FROM orders o
  WHERE o.created_at >= '2024-01-01'
    AND o.created_at < '2024-02-01'
    AND o.status = 'completed'
    AND EXISTS (
      SELECT 1 FROM valid_order_items voi WHERE voi.order_id = o.id
    )
),
user_stats AS (
  -- 聚合统计
  SELECT 
    vo.user_id,
    SUM(vo.amount) as total_amount,
    COUNT(DISTINCT vo.id) as order_count,
    AVG(vo.amount) as avg_amount,
    MAX(vo.created_at) as last_order_time
  FROM valid_orders vo
  GROUP BY vo.user_id
  HAVING SUM(vo.amount) > 10000
)
-- 最终JOIN用户信息
SELECT 
  u.id,
  u.name,
  d.name as department,
  us.total_amount,
  us.order_count,
  us.avg_amount,
  us.last_order_time
FROM user_stats us
JOIN users u ON us.user_id = u.id
LEFT JOIN departments d ON u.department_id = d.id
ORDER BY us.total_amount DESC;
