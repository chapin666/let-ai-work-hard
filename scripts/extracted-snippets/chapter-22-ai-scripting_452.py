# Source: chapter-22-ai-scripting.md
# Lines: 452-561
# Language: python

#!/usr/bin/env python3
"""
服务器每日巡检脚本
"""
import paramiko
import concurrent.futures
import sqlite3
from datetime import datetime
import json
import requests
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CheckResult:
    host: str
    disk_usage: float
    memory_usage: float
    cpu_load: float
    zombie_processes: int
    warnings: List[str]
    checked_at: datetime

def check_server(ip: str) -> CheckResult:
    """检查单台服务器"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ip, username='monitor', key_filename='~/.ssh/monitor_key', timeout=30)
        
        # 获取磁盘使用率（最大分区）
        stdin, stdout, stderr = client.exec_command(
            "df -h | awk 'NR>1 && $1 ~ /^\/dev/ {print $5}' | sed 's/%//' | sort -nr | head -1"
        )
        disk_usage = float(stdout.read().decode().strip() or 0)
        
        # 获取内存使用率
        stdin, stdout, stderr = client.exec_command(
            "free | grep Mem | awk '{printf \"%.2f\", $3/$2 * 100.0}'"
        )
        memory_usage = float(stdout.read().decode().strip() or 0)
        
        # 获取CPU负载（5分钟平均）
        stdin, stdout, stderr = client.exec_command("uptime | awk -F'load average:' '{print $2}' | awk '{print $2}' | sed 's/,//'")
        cpu_load = float(stdout.read().decode().strip() or 0)
        
        # 获取僵尸进程数
        stdin, stdout, stderr = client.exec_command("ps aux | grep -c '[Zz]ombie'")
        zombie_processes = int(stdout.read().decode().strip() or 0)
        
        client.close()
        
        # 检查告警
        warnings = []
        if disk_usage > 85:
            warnings.append(f"磁盘使用率过高: {disk_usage}%")
        if memory_usage > 90:
            warnings.append(f"内存使用率过高: {memory_usage:.1f}%")
        if cpu_load > 10:
            warnings.append(f"CPU负载过高: {cpu_load}")
        if zombie_processes > 0:
            warnings.append(f"存在{zombie_processes}个僵尸进程")
        
        return CheckResult(
            host=ip,
            disk_usage=disk_usage,
            memory_usage=memory_usage,
            cpu_load=cpu_load,
            zombie_processes=zombie_processes,
            warnings=warnings,
            checked_at=datetime.now()
        )
        
    except Exception as e:
        return CheckResult(
            host=ip,
            disk_usage=0,
            memory_usage=0,
            cpu_load=0,
            zombie_processes=0,
            warnings=[f"连接失败: {str(e)}"],
            checked_at=datetime.now()
        )

def send_dingtalk_alert(webhook: str, results: List[CheckResult]):
    """发送钉钉告警"""
    alert_results = [r for r in results if r.warnings]
    
    if not alert_results:
        return
    
    content = "### 🚨 服务器巡检告警\n\n"
    for r in alert_results:
        content += f"**{r.host}**\n"
        for w in r.warnings:
            content += f"- ❌ {w}\n"
        content += "\n"
    
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "服务器巡检告警",
            "text": content
        }
    }
    
    requests.post(webhook, json=message, timeout=10)
