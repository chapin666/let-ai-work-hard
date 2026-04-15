# Source: chapter-22-ai-scripting.md
# Lines: 77-259
# Language: python

#!/usr/bin/env python3
"""
SSL证书批量更新脚本
并发执行，支持自动回滚
"""

import paramiko
import concurrent.futures
from pathlib import Path
import logging
from datetime import datetime
import subprocess
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'ssl_update_{datetime.now():%Y%m%d_%H%M%S}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SSLUpdater:
    def __init__(self, key_path, max_workers=5):
        self.key_path = key_path
        self.max_workers = max_workers
        self.results = {'success': [], 'failed': []}
    
    def update_server(self, ip):
        """更新单台服务器的SSL证书"""
        logger.info(f"开始处理服务器: {ip}")
        
        try:
            # 建立SSH连接
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username='root', key_filename=self.key_path, timeout=30)
            
            # 1. 备份现有证书
            backup_cmd = f"""
                backup_dir=/etc/ssl/backup_{datetime.now():%Y%m%d_%H%M%S}
                mkdir -p $backup_dir
                cp /etc/ssl/cert.pem $backup_dir/ 2>/dev/null || true
                cp /etc/ssl/key.pem $backup_dir/ 2>/dev/null || true
                echo $backup_dir
            """
            stdin, stdout, stderr = client.exec_command(backup_cmd)
            backup_dir = stdout.read().decode().strip()
            logger.info(f"[{ip}] 证书已备份到: {backup_dir}")
            
            # 2. 上传新证书（使用SFTP）
            sftp = client.open_sftp()
            sftp.put('new_cert.pem', '/tmp/cert.pem')
            sftp.put('new_key.pem', '/tmp/key.pem')
            sftp.close()
            logger.info(f"[{ip}] 新证书已上传到/tmp/")
            
            # 3. 替换证书文件
            replace_cmd = """
                sudo cp /tmp/cert.pem /etc/ssl/cert.pem && \
                sudo cp /tmp/key.pem /etc/ssl/key.pem && \
                sudo chmod 600 /etc/ssl/key.pem && \
                sudo chown root:root /etc/ssl/*.pem
            """
            stdin, stdout, stderr = client.exec_command(replace_cmd)
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status != 0:
                error = stderr.read().decode()
                raise Exception(f"替换证书失败: {error}")
            logger.info(f"[{ip}] 证书替换成功")
            
            # 4. 重启nginx
            stdin, stdout, stderr = client.exec_command('sudo systemctl restart nginx')
            exit_status = stdout.channel.recv_exit_status()
            
            if exit_status != 0:
                raise Exception(f"重启nginx失败: {stderr.read().decode()}")
            logger.info(f"[{ip}] nginx重启成功")
            
            # 5. 验证HTTPS
            verify_cmd = 'sleep 2 && curl -s -o /dev/null -w "%{http_code}" https://localhost'
            stdin, stdout, stderr = client.exec_command(verify_cmd)
            http_code = stdout.read().decode().strip()
            
            if http_code != '200':
                raise Exception(f"HTTPS验证失败，状态码: {http_code}")
            logger.info(f"[{ip}] HTTPS验证成功 (状态码: {http_code})")
            
            client.close()
            self.results['success'].append(ip)
            logger.info(f"✅ [{ip}] 更新成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ [{ip}] 更新失败: {str(e)}")
            self.results['failed'].append({'ip': ip, 'error': str(e)})
            
            # 尝试回滚
            try:
                if 'backup_dir' in dir():
                    rollback_cmd = f"""
                        sudo cp {backup_dir}/cert.pem /etc/ssl/cert.pem 2>/dev/null || true
                        sudo cp {backup_dir}/key.pem /etc/ssl/key.pem 2>/dev/null || true
                        sudo systemctl restart nginx
                    """
                    client.exec_command(rollback_cmd)
                    logger.info(f"[{ip}] 已自动回滚到备份版本")
            except:
                pass
            
            return False
    
    def run(self, ip_list_file):
        """主执行函数"""
        # 读取IP列表
        with open(ip_list_file, 'r') as f:
            ips = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        logger.info(f"开始批量更新SSL证书，共{len(ips)}台服务器，并发数: {self.max_workers}")
        
        # 并发执行
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.update_server, ip): ip for ip in ips}
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"[{ip}] 执行异常: {str(e)}")
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成执行报告"""
        report = f"""
========================================
SSL证书批量更新报告
生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}
========================================

总计: {len(self.results['success']) + len(self.results['failed'])}台
成功: {len(self.results['success'])}台
失败: {len(self.results['failed'])}台
成功率: {len(self.results['success'])/(len(self.results['success']) + len(self.results['failed']))*100:.1f}%

【成功列表】
"""
        for ip in self.results['success']:
            report += f"  ✅ {ip}\n"
        
        if self.results['failed']:
            report += "\n【失败列表】\n"
            for item in self.results['failed']:
                report += f"  ❌ {item['ip']} - {item['error']}\n"
        
        report += "\n========================================\n"
        
        # 保存报告
        report_file = f'ssl_report_{datetime.now():%Y%m%d_%H%M%S}.txt'
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(report)
        logger.info(f"详细报告已保存到: {report_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python ssl_updater.py <ip_list_file> [ssh_key_path]")
        print("示例: python ssl_updater.py ips.txt ~/.ssh/id_rsa")
        sys.exit(1)
    
    ip_file = sys.argv[1]
    key_path = sys.argv[2] if len(sys.argv) > 2 else '~/.ssh/id_rsa'
    
    updater = SSLUpdater(key_path)
    updater.run(ip_file)
