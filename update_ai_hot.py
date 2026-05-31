#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI热点自动更新脚本
从 aihot.virxact.com API + 国内RSS源 获取数据，更新 ai-hot.html
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# 国内RSS源
RSS_SOURCES = [
    {'name': '机器之心', 'url': 'https://www.jiqizhixin.com/rss', 'category': 'AI媒体'},
    {'name': '量子位', 'url': 'https://www.qbitai.com/feed', 'category': 'AI媒体'},
    {'name': 'InfoQ中文', 'url': 'https://www.infoq.cn/feed', 'category': '技术'},
    {'name': '少数派', 'url': 'https://sspai.com/feed', 'category': '科技'},
]

def escape(t):
    """HTML转义"""
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def fetch_aihot_data():
    """获取AIHOT日报数据"""
    try:
        req = urllib.request.Request(
            'https://aihot.virxact.com/api/public/daily',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"AIHOT API获取失败: {e}")
        return None

def fetch_rss_news():
    """获取RSS新闻"""
    news_items = []
    
    for source in RSS_SOURCES:
        try:
            req = urllib.request.Request(source['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                root = ET.fromstring(content)
                
                count = 0
                for item in root.findall('.//item')[:5]:
                    if count >= 3:  # 每个源最多3条
                        break
                    
                    title = item.find('title')
                    link = item.find('link')
                    desc = item.find('description')
                    
                    if title is not None and title.text:
                        # 筛选AI相关
                        t = title.text
                        ai_keywords = ['AI', '人工智能', '大模型', 'GPT', '机器人', '芯片', '算力', '智能', '算法']
                        if any(kw in t for kw in ai_keywords) or source['category'] == 'AI媒体':
                            news_items.append({
                                'source': source['name'],
                                'category': source['category'],
                                'title': t,
                                'url': link.text if link is not None else '#',
                                'summary': (desc.text[:100] + '...') if desc is not None and desc.text else '',
                            })
                            count += 1
        except Exception as e:
            print(f"RSS {source['name']} 获取失败: {e}")
    
    return news_items

def generate_html(aihot_data, rss_items):
    """生成HTML页面"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    date = aihot_data['date'] if aihot_data else datetime.now().strftime('%Y-%m-%d')
    
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
        <div class="u">数据来源：AIHOT + 国内RSS · 更新时间: {now}</div>
'''
    
    # AIHOT数据
    if aihot_data and 'sections' in aihot_data:
        for section in aihot_data['sections']:
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
    
    # RSS数据
    if rss_items:
        html += '        <div class="section">\n'
        html += '            <div class="section-title">国内AI媒体</div>\n'
        html += '            <div class="n">\n'
        
        for item in rss_items:
            html += f'''                <div class="nc">
                    <div class="nt"><a href="{escape(item['url'])}" target="_blank">{escape(item['title'])}</a></div>
                    <div class="nm">{escape(item['source'])}</div>
                    <div class="nsm">{escape(item['summary'])}</div>
                </div>
'''
        
        html += '            </div>\n'
        html += '        </div>\n'
    
    html += f'''        <div class="f">数据来源：aihot.virxact.com + 国内RSS · 仅供参考</div>
    </div>
</body>
</html>'''
    
    return html

def main():
    print("开始更新AI热点...")
    
    # 获取AIHOT数据
    aihot_data = fetch_aihot_data()
    if aihot_data:
        print(f"AIHOT数据: {aihot_data['date']}, {len(aihot_data['sections'])}个分类")
    
    # 获取RSS数据
    rss_items = fetch_rss_news()
    print(f"RSS数据: {len(rss_items)}条")
    
    # 生成HTML
    html = generate_html(aihot_data, rss_items)
    
    with open('ai-hot.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ ai-hot.html 已更新")
    return 0

if __name__ == "__main__":
    exit(main())
