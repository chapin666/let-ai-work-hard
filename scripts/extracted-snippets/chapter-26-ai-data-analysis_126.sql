# Source: chapter-26-ai-data-analysis.md
# Lines: 126-208
# Language: sql

-- 1. 留存率计算（Cohort分析）
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE(register_date) as cohort_date,
        device_type,
        channel
    FROM users
    WHERE register_date >= DATE_SUB('2024-01-01', INTERVAL 90 DAY)
),
user_activity AS (
    SELECT 
        user_id,
        DATE(event_time) as active_date
    FROM events
    WHERE event_time >= DATE_SUB('2024-01-01', INTERVAL 90 DAY)
    GROUP BY user_id, DATE(event_time)
),
retention AS (
    SELECT 
        uc.cohort_date,
        uc.device_type,
        uc.channel,
        COUNT(DISTINCT uc.user_id) as total_users,
        COUNT(DISTINCT CASE WHEN ua.active_date = uc.cohort_date THEN uc.user_id END) as d0,
        COUNT(DISTINCT CASE WHEN ua.active_date = DATE_ADD(uc.cohort_date, INTERVAL 1 DAY) THEN uc.user_id END) as d1,
        COUNT(DISTINCT CASE WHEN ua.active_date = DATE_ADD(uc.cohort_date, INTERVAL 7 DAY) THEN uc.user_id END) as d7,
        COUNT(DISTINCT CASE WHEN ua.active_date = DATE_ADD(uc.cohort_date, INTERVAL 30 DAY) THEN uc.user_id END) as d30
    FROM user_cohorts uc
    LEFT JOIN user_activity ua ON uc.user_id = ua.user_id
    GROUP BY uc.cohort_date, uc.device_type, uc.channel
)
SELECT 
    cohort_date,
    device_type,
    channel,
    total_users,
    ROUND(d1 * 100.0 / total_users, 2) as retention_d1,
    ROUND(d7 * 100.0 / total_users, 2) as retention_d7,
    ROUND(d30 * 100.0 / total_users, 2) as retention_d30
FROM retention
ORDER BY cohort_date DESC, retention_d30 ASC;

-- 2. 用户行为路径分析（找出流失前的最后行为）
WITH user_last_session AS (
    SELECT 
        user_id,
        MAX(event_time) as last_active_time,
        COUNT(DISTINCT session_id) as total_sessions,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) as purchase_count,
        COUNT(CASE WHEN page_url LIKE '%checkout%' THEN 1 END) as checkout_visits,
        SUM(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) as page_views
    FROM events
    WHERE event_time >= DATE_SUB(NOW(), INTERVAL 60 DAY)
    GROUP BY user_id
),
churned_users AS (
    SELECT user_id
    FROM users
    WHERE last_login_date <= DATE_SUB(NOW(), INTERVAL 7 DAY)
      AND register_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
)
SELECT 
    '流失用户' as user_group,
    AVG(total_sessions) as avg_sessions,
    AVG(purchase_count) as avg_purchases,
    AVG(checkout_visits) as avg_checkout_visits,
    AVG(page_views) as avg_page_views
FROM user_last_session uls
JOIN churned_users cu ON uls.user_id = cu.user_id

UNION ALL

SELECT 
    '留存用户' as user_group,
    AVG(total_sessions) as avg_sessions,
    AVG(purchase_count) as avg_purchases,
    AVG(checkout_visits) as avg_checkout_visits,
    AVG(page_views) as avg_page_views
FROM user_last_session uls
WHERE uls.user_id NOT IN (SELECT user_id FROM churned_users);
