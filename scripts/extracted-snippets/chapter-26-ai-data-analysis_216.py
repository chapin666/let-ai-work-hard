# Source: chapter-26-ai-data-analysis.md
# Lines: 216-431
# Language: python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pymysql
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class UserRetentionAnalyzer:
    """用户留存分析器"""
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        
    def connect(self):
        """连接数据库"""
        self.conn = pymysql.connect(**self.db_config)
        print("✅ 数据库连接成功")
        
    def load_data(self):
        """加载数据"""
        # 加载留存数据
        retention_sql = """
        SELECT 
            cohort_date,
            device_type,
            channel,
            total_users,
            retention_d1,
            retention_d7,
            retention_d30
        FROM retention_summary
        WHERE cohort_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
        """
        self.retention_df = pd.read_sql(retention_sql, self.conn)
        
        # 加载用户特征数据
        features_sql = """
        SELECT 
            u.user_id,
            u.device_type,
            u.channel,
            DATEDIFF(NOW(), u.register_date) as user_age_days,
            COUNT(DISTINCT e.session_id) as total_sessions,
            COUNT(CASE WHEN e.event_type = 'purchase' THEN 1 END) as purchase_count,
            COALESCE(SUM(o.order_amount), 0) as total_spend,
            AVG(f.rating) as avg_rating,
            CASE WHEN u.last_login_date >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 0 ELSE 1 END as is_churned
        FROM users u
        LEFT JOIN events e ON u.user_id = e.user_id 
            AND e.event_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        LEFT JOIN orders o ON u.user_id = o.user_id 
            AND o.order_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        LEFT JOIN feedback f ON u.user_id = f.user_id
        WHERE u.register_date >= DATE_SUB(NOW(), INTERVAL 90 DAY)
        GROUP BY u.user_id, u.device_type, u.channel, u.register_date, u.last_login_date
        """
        self.features_df = pd.read_sql(features_sql, self.conn)
        print(f"📊 加载了 {len(self.retention_df)} 条留存数据, {len(self.features_df)} 个用户特征")
        
    def analyze_retention_trend(self):
        """分析留存趋势"""
        # 按时间聚合
        daily_retention = self.retention_df.groupby('cohort_date').agg({
            'total_users': 'sum',
            'retention_d1': 'mean',
            'retention_d7': 'mean',
            'retention_d30': 'mean'
        }).reset_index()
        
        # 绘制趋势图
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 留存率趋势
        axes[0, 0].plot(daily_retention['cohort_date'], daily_retention['retention_d1'], 
                        marker='o', label='次日留存', linewidth=2)
        axes[0, 0].plot(daily_retention['cohort_date'], daily_retention['retention_d7'], 
                        marker='s', label='7日留存', linewidth=2)
        axes[0, 0].plot(daily_retention['cohort_date'], daily_retention['retention_d30'], 
                        marker='^', label='30日留存', linewidth=2)
        axes[0, 0].set_title('留存率趋势变化', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('注册日期')
        axes[0, 0].set_ylabel('留存率 (%)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 分渠道留存对比
        channel_retention = self.retention_df.groupby('channel')['retention_d30'].mean().sort_values(ascending=False)
        channel_retention.plot(kind='bar', ax=axes[0, 1], color='steelblue')
        axes[0, 1].set_title('各渠道30日留存率对比', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('渠道')
        axes[0, 1].set_ylabel('30日留存率 (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 分设备留存对比
        device_retention = self.retention_df.groupby('device_type')['retention_d30'].mean().sort_values(ascending=False)
        device_retention.plot(kind='bar', ax=axes[1, 0], color='coral')
        axes[1, 0].set_title('各设备类型30日留存率对比', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('设备类型')
        axes[1, 0].set_ylabel('30日留存率 (%)')
        
        # 4.  cohort热力图
        cohort_pivot = self.retention_df.pivot_table(
            values='retention_d30', 
            index='channel', 
            columns='device_type', 
            aggfunc='mean'
        )
        sns.heatmap(cohort_pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1, 1])
        axes[1, 1].set_title('渠道×设备留存率热力图', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('retention_analysis.png', dpi=150, bbox_inches='tight')
        print("📈 留存分析图表已保存")
        return fig
    
    def identify_churn_factors(self):
        """识别流失因素（使用机器学习）"""
        # 准备特征
        feature_cols = ['user_age_days', 'total_sessions', 'purchase_count', 'total_spend']
        X = self.features_df[feature_cols].fillna(0)
        y = self.features_df['is_churned']
        
        # 训练随机森林模型
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        model.fit(X_train, y_train)
        
        # 特征重要性
        importance_df = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔍 流失影响因素排序：")
        for idx, row in importance_df.iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        # 可视化
        plt.figure(figsize=(10, 6))
        sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
        plt.title('用户流失影响因素重要性', fontsize=14, fontweight='bold')
        plt.xlabel('重要性')
        plt.tight_layout()
        plt.savefig('churn_factors.png', dpi=150)
        
        return importance_df
    
    def generate_insights(self):
        """生成业务洞察"""
        insights = []
        
        # 1. 留存率变化
        recent_retention = self.retention_df[self.retention_df['cohort_date'] >= 
                                              (datetime.now() - timedelta(days=30))]['retention_d30'].mean()
        older_retention = self.retention_df[(self.retention_df['cohort_date'] < 
                                              (datetime.now() - timedelta(days=30))) & 
                                             (self.retention_df['cohort_date'] >= 
                                              (datetime.now() - timedelta(days=60)))]['retention_d30'].mean()
        
        retention_change = recent_retention - older_retention
        insights.append(f"📊 近30日平均30日留存率为 {recent_retention:.1f}%，相比前30日 {'上升' if retention_change > 0 else '下降'}了 {abs(retention_change):.1f}个百分点")
        
        # 2. 最佳渠道
        best_channel = self.retention_df.groupby('channel')['retention_d30'].mean().idxmax()
        best_channel_rate = self.retention_df.groupby('channel')['retention_d30'].mean().max()
        insights.append(f"🏆 留存表现最佳的渠道是 {best_channel}，30日留存率达到 {best_channel_rate:.1f}%")
        
        # 3. 问题渠道
        worst_channel = self.retention_df.groupby('channel')['retention_d30'].mean().idxmin()
        worst_channel_rate = self.retention_df.groupby('channel')['retention_d30'].mean().min()
        if worst_channel_rate < best_channel_rate * 0.7:
            insights.append(f"⚠️ {worst_channel}渠道的留存率({worst_channel_rate:.1f}%)明显低于平均水平，建议重点优化")
        
        # 4. 设备差异
        mobile_retention = self.retention_df[self.retention_df['device_type'] == 'mobile']['retention_d30'].mean()
        desktop_retention = self.retention_df[self.retention_df['device_type'] == 'desktop']['retention_d30'].mean()
        if mobile_retention < desktop_retention * 0.8:
            insights.append(f"📱 移动端留存率({mobile_retention:.1f}%)显著低于桌面端({desktop_retention:.1f}%)，建议检查移动端体验")
        
        return insights

# 使用示例
if __name__ == '__main__':
    db_config = {
        'host': 'localhost',
        'user': 'analyst',
        'password': 'your_password',
        'database': 'analytics',
        'charset': 'utf8mb4'
    }
    
    analyzer = UserRetentionAnalyzer(db_config)
    analyzer.connect()
    analyzer.load_data()
    
    # 分析留存趋势
    analyzer.analyze_retention_trend()
    
    # 识别流失因素
    analyzer.identify_churn_factors()
    
    # 生成洞察
    print("\n💡 核心洞察：")
    for insight in analyzer.generate_insights():
        print(f"  • {insight}")
