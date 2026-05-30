#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 index.html：添加 global-risk-monitor 链接卡片（保持UTF-8编码）"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 在"系统说明"卡片前插入"全球风险监控"卡片
# 先找到卡片区域的特征字符串
old = '''<a href="about.html" class="module-card">'''

new = '''<a href="global-risk-monitor/" class="module-card">
                    <div class="module-icon">🌍</div>
                    <div class="module-title">全球风险监控</div>
                </a>
                <a href="about.html" class="module-card">'''

if old in content:
    content = content.replace(old, new, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ 已添加全球风险监控卡片链接')
else:
    # 如果找不到 about.html，尝试找其他插入点
    print('⚠️ 未找到 about.html 链接，尝试其他方式...')
    # 查找卡片区域的结尾（通常在 </div> 之前）
    # 备用方案：在 </div> 前（容器结尾）添加
    if 'module-card' in content:
        print('📋 当前卡片列表：')
        import re
        cards = re.findall(r'<a [^>]*class="module-card"[^>]*>.*?</a>', content, re.DOTALL)
        for i, card in enumerate(cards[:5]):
            print(f'  {i}: {card[:80]}...')
    else:
        print('❌ 未找到 module-card，文件结构可能不同')
