# Source: chapter-21-ai-sql-optimization.md
# Lines: 194-206
# Language: sql

-- 优化1：orders表复合索引
CREATE INDEX idx_orders_created_status_user 
ON orders(created_at, status, user_id, amount);

-- 优化2：order_items表索引
CREATE INDEX idx_order_items_order_product 
ON order_items(order_id, product_id);

-- 优化3：products表索引
CREATE INDEX idx_products_id_category 
ON products(id, category);
