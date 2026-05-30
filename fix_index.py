#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 index.html：添加 global-risk-monitor 链接卡片（保持UTF-8编码）"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 在 cards 结束 </div> 前插入新卡片
# 目标：在 "        </div>\n\n        <div style="text-align: center;">" 前插入
old = '        </div>\n\n        <div style="text-align: center;">'

new = '''            <div class="card">
                <div class="card-icon">🌍</div>
                <h3>全球风险监控</h3>
                <p><a href="global-risk-monitor/" style="color:#00d4ff;text-decoration:none;">查看全球市场风险监控 →</a></p>
            </div>
        </div>

        <div style="text-align: center;">'''

if old in content:
    content = content.replace(old, new, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('✅ 已添加全球风险监控卡片')
else:
    print('❌ 未找到插入位置')
    # 调试：找 </div> 的位置
    idx = content.rfind('        </div>')
    print(f'最后一个 </div> 位置: {idx}')
    print('附近内容:')
    print(repr(content[max(0,idx-50):idx+100]))
