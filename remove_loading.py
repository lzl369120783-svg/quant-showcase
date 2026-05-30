#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除 loading screen，保留原文件编码"""

with open('index.html', 'rb') as f:
    data = f.read()

# 1. 删除 loading screen CSS
# 找到 /* 加载动画 */ 开始到 .loading-text 结束的整个 CSS 块
css_start = data.find(b'        /* \xe5\x8a\xa0\xe8\xbd\xbd\xe5\x8a\xa8\xe7\x94\xbb */')
if css_start >= 0:
    # 找到 .loading-text 块的结束 (下一个 */ 后的 })
    css_end = data.find(b'        }', css_start + 100) + len(b'        }')
    data = data[:css_start] + data[css_end:]
    print('✅ 删除 loading screen CSS')

# 2. 删除 loading screen HTML
html_start = data.find(b'    <!-- \xe5\x8a\xa0\xe8\xbd\xbd\xe5\x8a\xa8\xe7\x94\xbb -->')
if html_start >= 0:
    html_end = data.find(b'    </div>\n', html_start) + len(b'    </div>\n')
    data = data[:html_start] + data[html_end:]
    print('✅ 删除 loading screen HTML')

# 3. 删除 loading screen JS
js_start = data.find(b'        // \xe5\x8a\xa0\xe8\xbd\xbd\xe5\x8a\xa8\xe7\x94\xbb')
if js_start >= 0:
    # 找到 }; 后面的换行
    js_end = data.find(b'        }, 3000);\n', js_start) + len(b'        }, 3000);\n')
    data = data[:js_start] + data[js_end:]
    print('✅ 删除 loading screen JS')

with open('index.html', 'wb') as f:
    f.write(data)
print('✅ 文件已保存，大小:', len(data))
