#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
实时监控服务器
提供实时数据API，支持前端自动刷新
"""
import json
import os
import sys
import time
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# 添加astock_analyzer路径
sys.path.insert(0, r"C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer")

# 数据目录
OUTPUT_DIR = r"C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer\output"

class MonitorHandler(SimpleHTTPRequestHandler):
    """处理HTTP请求"""
    
    def do_GET(self):
        """处理GET请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # API: 获取实时监控数据
        if path == '/api/monitor':
            self.send_json(self.get_monitor_data())
            return
        
        # API: 获取账户数据
        if path == '/api/account':
            self.send_json(self.get_account_data())
            return
        
        # API: 获取市场数据
        if path == '/api/market':
            self.send_json(self.get_market_data())
            return
        
        # 默认：返回静态文件
        super().do_GET()
    
    def send_json(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def get_monitor_data(self):
        """获取实时监控数据"""
        today = datetime.now().strftime("%Y%m%d")
        
        # 读取各种数据文件
        daily_file = os.path.join(OUTPUT_DIR, "account_snapshots", f"daily_summary_{today}.json")
        screen_file = os.path.join(OUTPUT_DIR, f"screen_{today}.json")
        monitor_file = os.path.join(OUTPUT_DIR, f"monitor_{today}.json")
        pnl_file = os.path.join(OUTPUT_DIR, "..", "_pnl_report.json")
        
        data = {
            "update_time": datetime.now().strftime("%H:%M:%S"),
            "date": today,
            "market": self.load_json(daily_file).get("market_overview", {}),
            "sentiment": self.load_json(daily_file).get("sentiment", {}),
            "indices": self.load_json(daily_file).get("indices", {}),
            "sectors": self.load_json(daily_file).get("top_sectors", []),
            "positions": self.load_json(pnl_file).get("positions", []) if os.path.exists(pnl_file) else [],
            "trades": self.load_json(daily_file).get("today_trades", []),
        }
        
        return data
    
    def get_account_data(self):
        """获取账户数据"""
        pnl_file = os.path.join(OUTPUT_DIR, "..", "_pnl_report.json")
        if os.path.exists(pnl_file):
            return self.load_json(pnl_file)
        return {}
    
    def get_market_data(self):
        """获取市场数据"""
        today = datetime.now().strftime("%Y%m%d")
        daily_file = os.path.join(OUTPUT_DIR, "account_snapshots", f"daily_summary_{today}.json")
        return self.load_json(daily_file).get("market_overview", {})
    
    def load_json(self, filepath):
        """安全加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {args[0]}" if args else "")

def run_server(port=8088):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MonitorHandler)
    
    print("=" * 50)
    print("  实时监控服务器已启动")
    print("=" * 50)
    print(f"  访问地址: http://localhost:{port}")
    print(f"  API地址:  http://localhost:{port}/api/monitor")
    print("=" * 50)
    print("  按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8088
    run_server(port)
