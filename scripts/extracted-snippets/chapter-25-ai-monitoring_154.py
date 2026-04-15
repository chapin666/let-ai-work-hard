# Source: chapter-25-ai-monitoring.md
# Lines: 154-167
# Language: python

# 基于统计学的异常检测
def detect_anomaly(values, threshold=3):
    """使用3-sigma原则检测异常"""
    mean = np.mean(values)
    std = np.std(values)
    
    anomalies = []
    for i, v in enumerate(values):
        if abs(v - mean) > threshold * std:
            anomalies.append((i, v))
    
    return anomalies
