# Source: chapter-25-ai-monitoring.md
# Lines: 193-202
# Language: python

# 基于依赖拓扑的根因分析
def find_root_cause(alerts, dependency_graph):
    """在告警组中找根因"""
    # 按依赖层级排序（基础设施优先）
    sorted_alerts = sorted(alerts, 
                          key=lambda a: get_layer(a.source))
    
    return sorted_alerts[0]
