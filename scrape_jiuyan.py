#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
韭研公社内容抓取脚本（使用agent-browser）
"""
import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "reports"

POSTS = [
    {
        "name": "盘前纪要",
        "url": "https://www.jiuyangongshe.com/a/jrsst0j85y"
    },
    {
        "name": "开盘必读",
        "url": "https://www.jiuyangongshe.com/a/2z3nl4k8fgw"
    }
]


def fetch_post(url):
    """使用agent-browser抓取帖子内容"""
    try:
        # 打开页面
        subprocess.run(["npx", "agent-browser", "open", url], 
                      capture_output=True, text=True, timeout=30)
        
        # 获取内容
        result = subprocess.run(
            ["npx", "agent-browser", "eval", "document.querySelector('.text-box')?.innerText"],
            capture_output=True, text=True, timeout=30
        )
        
        # 解析输出（去掉Node.js警告）
        lines = result.stdout.strip().split('\n')
        content = '\n'.join(lines[2:])  # 跳过警告行
        
        # 去掉引号
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        
        # 处理转义字符
        content = content.replace('\\n', '\n').replace('\\t', '\t')
        
        return content
    except Exception as e:
        print(f"抓取失败: {e}")
        return None


def main():
    """主函数"""
    print("开始抓取韭研公社内容...")
    
    today = datetime.now().strftime("%Y%m%d")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    posts_content = []
    
    for post in POSTS:
        print(f"正在抓取: {post['name']}...")
        content = fetch_post(post['url'])
        
        if content:
            posts_content.append((post['name'], content))
            print(f"  ✓ {post['name']} 抓取成功")
        else:
            posts_content.append((post['name'], "抓取失败，请稍后重试"))
            print(f"  ✗ {post['name']} 抓取失败")
    
    # 保存为JSON
    json_file = OUTPUT_DIR / f"morning_brief_{today}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(posts_content, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存: {json_file}")
    
    # 生成HTML
    subprocess.run(["python", str(Path(__file__).parent / "fetch_morning_brief.py")], 
                  capture_output=False)


if __name__ == "__main__":
    main()
