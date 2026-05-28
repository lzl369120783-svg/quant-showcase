#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
韭研公社盘前纪要抓取脚本
每天早上自动抓取两位博主的帖子，生成精简版HTML
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

# 配置
POSTS = [
    {
        "name": "盘前纪要",
        "url": "https://www.jiuyangongshe.com/a/jrsst0j85y",
        "id": "jrsst0j85y"
    },
    {
        "name": "开盘必读",
        "url": "https://www.jiuyangongshe.com/a/2z3nl4k8fgw",
        "id": "2z3nl4k8fgw"
    }
]

OUTPUT_DIR = Path(__file__).parent / "reports"


def extract_key_info(text, max_chars=3000):
    """从长文中提取关键信息，生成精简版"""
    lines = text.split('\n')
    key_sections = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 保留标题和关键内容
        if any(keyword in line for keyword in [
            'No.', '热点', '事件', '要闻', '公告', '连板', '涨停',
            '机构', '调研', '美股', '大宗', '新股', '人气',
            '一、', '二、', '三、', '四、', '五、',
            '1、', '2、', '3、', '4、', '5、',
            '电力', '算力', 'AI', '芯片', '存储', '消费', '机器人',
            '涨停', '跌停', '连板', '首板', '龙头'
        ]):
            if current_section:
                key_sections.append(current_section)
            current_section = line
        elif current_section:
            # 保留股票代码和关键信息
            if re.search(r'[（(]\d{6}[）)]', line) or '：' in line:
                current_section += " " + line
    
    if current_section:
        key_sections.append(current_section)
    
    # 截取指定长度
    result = '\n'.join(key_sections)
    if len(result) > max_chars:
        result = result[:max_chars] + "..."
    
    return result


def generate_html(posts_content):
    """生成盘前纪要HTML页面"""
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()]
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>盘前纪要 - {today} {weekday}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .back-btn {{
            display: inline-block;
            padding: 8px 16px;
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid rgba(255, 215, 0, 0.3);
            color: #FFD700;
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}
        .back-btn:hover {{
            background: rgba(255, 215, 0, 0.2);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255, 215, 0, 0.05);
            border: 1px solid rgba(255, 215, 0, 0.2);
            border-radius: 8px;
        }}
        .header h1 {{
            color: #FFD700;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .date {{
            color: #a0a0b0;
            font-size: 14px;
        }}
        .section {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .section-header {{
            background: rgba(255, 215, 0, 0.1);
            padding: 12px 20px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.2);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .section-header h2 {{
            color: #FFD700;
            font-size: 18px;
        }}
        .section-header .toggle {{
            color: #a0a0b0;
            transition: transform 0.3s;
        }}
        .section-header .toggle.collapsed {{
            transform: rotate(-90deg);
        }}
        .section-content {{
            padding: 15px 20px;
            max-height: 2000px;
            overflow: hidden;
            transition: max-height 0.3s ease-out, padding 0.3s;
        }}
        .section-content.collapsed {{
            max-height: 0;
            padding: 0 20px;
        }}
        .content-text {{
            white-space: pre-wrap;
            line-height: 1.8;
            font-size: 14px;
        }}
        .content-text .highlight {{
            color: #FFD700;
            font-weight: bold;
        }}
        .content-text .stock {{
            color: #ff4757;
        }}
        .content-text .index {{
            color: #00D4FF;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 22px; }}
            .section-header h2 {{ font-size: 16px; }}
        }}
    </style>
    <script src="back-button.js"></script>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-btn">← 返回首页</a>
        
        <div class="header">
            <h1>📊 盘前纪要</h1>
            <div class="date">{today} {weekday} · 来源：韭研公社</div>
        </div>
'''
    
    for i, (name, content) in enumerate(posts_content):
        # 高亮处理
        processed = content
        # 高亮标题
        processed = re.sub(r'(No\.\d+\s+[^\n]+)', r'<span class="highlight">\1</span>', processed)
        # 高亮股票代码
        processed = re.sub(r'([（(])(\d{6})([）)])', r'\1<span class="stock">\2</span>\3', processed)
        # 高亮关键指标
        processed = re.sub(r'(涨停|跌停|连板|首板|龙头|创新高)', r'<span class="highlight">\1</span>', processed)
        
        html += f'''
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2>{'📰' if i == 0 else '📋'} {name}</h2>
                <span class="toggle">▼</span>
            </div>
            <div class="section-content">
                <div class="content-text">{processed}</div>
            </div>
        </div>
'''
    
    html += f'''
        <div class="footer">
            数据来源：韭研公社 · 仅供参考，不构成投资建议
        </div>
    </div>
    
    <script>
        function toggleSection(header) {{
            const content = header.nextElementSibling;
            const toggle = header.querySelector('.toggle');
            content.classList.toggle('collapsed');
            toggle.classList.toggle('collapsed');
        }}
    </script>
</body>
</html>'''
    
    return html


def main():
    """主函数"""
    print("开始抓取韭研公社盘前纪要...")
    
    # 读取之前保存的内容（如果有）
    posts_content = []
    
    # 这里实际运行时需要使用浏览器抓取
    # 由于韭研公社是JS渲染的，需要用playwright或agent-browser
    # 这里先生成一个模板，实际内容由外部脚本填充
    
    today = datetime.now().strftime("%Y%m%d")
    output_file = OUTPUT_DIR / f"morning_brief_{today}.html"
    
    # 检查是否已有抓取的内容
    json_file = OUTPUT_DIR / f"morning_brief_{today}.json"
    if json_file.exists():
        with open(json_file, 'r', encoding='utf-8') as f:
            posts_content = json.load(f)
    else:
        print(f"未找到今日数据文件: {json_file}")
        print("请先运行抓取脚本获取数据")
        return
    
    # 生成HTML
    html = generate_html(posts_content)
    
    # 保存文件
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 盘前纪要已生成: {output_file}")
    return output_file


if __name__ == "__main__":
    main()
