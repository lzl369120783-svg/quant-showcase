#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成监控数据JSON文件
每次运行A股分析V3.0.bat时自动执行
"""
import json
import os
from datetime import datetime

# 数据文件路径
OUTPUT_DIR = r"C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer\output"
WEB_DIR = r"C:\Users\Administrator\Desktop\quant-showcase"

def load_json(filepath):
    """安全加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def generate_monitor_data():
    """生成监控数据"""
    today = datetime.now().strftime("%Y%m%d")
    
    # 读取各种数据文件
    daily_file = os.path.join(OUTPUT_DIR, "account_snapshots", f"daily_summary_{today}.json")
    screen_file = os.path.join(OUTPUT_DIR, f"screen_{today}.json")
    monitor_file = os.path.join(OUTPUT_DIR, f"monitor_{today}.json")
    
    daily_data = load_json(daily_file)
    screen_data = load_json(screen_file)
    monitor_data = load_json(monitor_file)
    
    # 构建监控数据
    monitor_json = {
        "update_time": datetime.now().strftime("%H:%M:%S"),
        "date": today,
        # 市场概况
        "market": {
            "up_count": daily_data.get("up_count", 0),
            "down_count": daily_data.get("down_count", 0),
            "limit_up": daily_data.get("limit_up", 0),
            "limit_down": daily_data.get("limit_down", 0),
            "broken_limit": daily_data.get("broken_limit", 0),
            "abnormal": daily_data.get("abnormal_count", 0),
        },
        # 情绪指标
        "sentiment": {
            "level": daily_data.get("sentiment_level", "L3"),
            "score": daily_data.get("sentiment_score", 50),
            "description": daily_data.get("sentiment_desc", "中性"),
        },
        # 指数涨跌
        "indices": {
            "shanghai": daily_data.get("shanghai_change", 0),
            "shenzhen": daily_data.get("shenzhen_change", 0),
            "chinext": daily_data.get("chinext_change", 0),
        },
        # 题材排名
        "sectors": daily_data.get("top_sectors", []),
        # 持仓信息
        "positions": daily_data.get("positions", []),
        # 今日交易
        "trades": daily_data.get("today_trades", []),
    }
    
    # 保存到网站目录
    output_file = os.path.join(WEB_DIR, "monitor_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(monitor_json, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 监控数据已生成: {output_file}")
    return monitor_json

if __name__ == "__main__":
    generate_monitor_data()
