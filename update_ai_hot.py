#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI热点自动更新脚本
从 aihot.virxact.com API 获取数据，更新 ai-hot.html
"""

import urllib.request
import json
from datetime import datetime

def escape(t):
    """HTML转义"""
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def fetch_aihot_data():
    """获取AIHOT日报数据"""
    req = urllib.request.Request(
        'https://aihot.virxact.com/api/public/daily',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))

def generate_html(data):
    """生成HTML页面"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    date = data['date']
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI热点 - {date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: linear-gradient(135deg, #0a0a1a, #1a1a2e); color: #e0e0e0; font-family: -apple-system, BlinkMacSystemFont, 'Microsoft YaHei', sans-serif; min-height: 100vh; padding: 20px; }}
        .c {{ max-width: 1000px; margin: 0 auto; }}
        .b {{ display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; background: rgba(255,215,0,.1); border: 1px solid rgba(255,215,0,.3); color: #FFD700; text-decoration: none; border-radius: 6px; margin-bottom: 20px; font-size: 14px; }}
        .b:hover {{ background: rgba(255,215,0,.2); }}
        .h {{ text-align: center; margin-bottom: 30px; padding: 30px; background: linear-gradient(135deg, rgba(255,215,0,.08), rgba(0,212,255,.05)); border: 1px solid rgba(255,215,0,.2); border-radius: 12px; }}
        .h h1 {{ color: #FFD700; font-size: 28px; margin-bottom: 10px; }}
        .h .s {{ color: #888; font-size: 14px; }}
        .u {{ text-align: center; color: #555; font-size: 12px; margin-bottom: 20px; }}
        .section {{ margin-bottom: 30px; }}
        .section-title {{ color: #00D4FF; font-size: 20px; font-weight: 600; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid rgba(0,212,255,.3); }}
        .n {{ display: flex; flex-direction: column; gap: 12px; }}
        .nc {{ background: rgba(18,18,42,.9); border: 1px solid rgba(255,215,0,.15); border-radius: 10px; padding: 16px; transition: all .3s; }}
        .nc:hover {{ border-color: rgba(255,215,0,.4); transform: translateY(-2px); }}
        .nt {{ color: #FFD700; font-size: 16px; font-weight: 600; margin-bottom: 6px; }}
        .nt a {{ color: #FFD700; text-decoration: none; }}
        .nt a:hover {{ text-decoration: underline; }}
        .nm {{ color: #888; font-size: 12px; margin-bottom: 8px; }}
        .nsm {{ color: #ccc; font-size: 14px; line-height: 1.6; }}
        .f {{ text-align: center; padding: 20px; color: #555; font-size: 12px; border-top: 1px solid rgba(255,255,255,.05); margin-top: 30px; }}
        @media (max-width: 768px) {{ .h h1 {{ font-size: 22px; }} .section-title {{ font-size: 18px; }} }}
    </style>
</head>
<body>
    <div class="c">
        <a href="index.html" class="b">← 返回首页</a>
        <div class="h">
            <h1>🔥 AI热点</h1>
            <div class="s">AI日报 · {date}</div>
        </div>
        <div class="u">数据来源：AIHOT · 更新时间: {now}</div>
'''
    
    for section in data['sections']:
        html += f'        <div class="section">\n'
        html += f'            <div class="section-title">{escape(section["label"])}</div>\n'
        html += f'            <div class="n">\n'
        
        for item in section['items']:
            title = escape(item.get('title', ''))
            summary = escape(item.get('summary', '')[:200])
            source = escape(item.get('sourceName', ''))
            url = item.get('sourceUrl', '#')
            
            html += f'''                <div class="nc">
                    <div class="nt"><a href="{url}" target="_blank">{title}</a></div>
                    <div class="nm">{source}</div>
                    <div class="nsm">{summary}</div>
                </div>
'''
        
        html += '            </div>\n'
        html += '        </div>\n'
    
    html += f'''        <div class="f">数据来源：aihot.virxact.com · 仅供参考</div>
    </div>
</body>
</html>'''
    
    return html

def main():
    print("开始更新AI热点...")
    
    try:
        data = fetch_aihot_data()
        print(f"获取数据成功: {data['date']}, {len(data['sections'])}个分类")
        
        html = generate_html(data)
        
        with open('ai-hot.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("✅ ai-hot.html 已更新")
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
