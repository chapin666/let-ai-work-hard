# Source: chapter-25-ai-monitoring.md
# Lines: 171-189
# Language: python

# 基于时间和拓扑的告警关联
def correlate_alerts(alerts, time_window=300):
    """将相关告警聚类"""
    groups = []
    
    for alert in alerts:
        found = False
        for group in groups:
            if is_related(alert, group[0], time_window):
                group.append(alert)
                found = True
                break
        
        if not found:
            groups.append([alert])
    
    return groups
