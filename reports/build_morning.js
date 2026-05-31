const fs = require('fs');
let content = fs.readFileSync('jiuyan_full.txt', 'utf8');
// Remove surrounding quotes
content = content.replace(/^"/, '').replace(/"$/, '');
// Replace literal \n with actual newlines
content = content.replace(/\\n/g, '\n');
// Split into lines
const lines = content.split('\n');

// Parse sections
let sections = [];
let current = { title: '', content: [] };

for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.match(/^(No\.|一、|二、|三、|四、|五、|六、|七、|八、|九、|十、)/)) {
        if (current.title) sections.push(current);
        current = { title: trimmed, content: [] };
    } else {
        current.content.push(line);
    }
}
if (current.title) sections.push(current);

console.log('Found sections:', sections.length);
sections.forEach((s, i) => console.log(i + ':', s.title));

// Build section HTML
let sectionsHtml = '';
for (const sec of sections) {
    let contentHtml = sec.content.join('\n')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/（([^）]+)）/g, '（<span class="stock">$1</span>）');
    
    sectionsHtml += `
        <div class="section">
            <div class="section-header" onclick="toggleSection(this)">
                <h2>${sec.title}</h2>
                <span class="toggle">▼</span>
            </div>
            <div class="section-content">
                <div class="content-text">${contentHtml}</div>
            </div>
        </div>`;
}

// Full HTML
let html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>盘前纪要 - 2026-05-29 周五</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .back-btn {
            display: inline-block; padding: 8px 16px;
            background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3);
            color: #FFD700; text-decoration: none; border-radius: 4px;
            margin-bottom: 20px; transition: all 0.3s;
        }
        .back-btn:hover { background: rgba(255, 215, 0, 0.2); }
        .header {
            text-align: center; margin-bottom: 30px; padding: 20px;
            background: rgba(255, 215, 0, 0.05); border: 1px solid rgba(255, 215, 0, 0.2); border-radius: 8px;
        }
        .header h1 { color: #FFD700; font-size: 28px; margin-bottom: 10px; }
        .header .date { color: #a0a0b0; font-size: 14px; }
        .section {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px; margin-bottom: 20px; overflow: hidden;
        }
        .section-header {
            background: rgba(255, 215, 0, 0.1); padding: 12px 20px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.2); cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
        }
        .section-header h2 { color: #FFD700; font-size: 18px; }
        .section-header .toggle { color: #a0a0b0; transition: transform 0.3s; }
        .section-header .toggle.collapsed { transform: rotate(-90deg); }
        .section-content {
            padding: 15px 20px; max-height: 5000px; overflow: hidden;
            transition: max-height 0.3s ease-out, padding 0.3s;
        }
        .section-content.collapsed { max-height: 0; padding: 0 20px; }
        .content-text {
            white-space: pre-wrap; line-height: 1.8; font-size: 14px;
        }
        .content-text .stock { color: #ff4757; font-weight: bold; }
        .footer {
            text-align: center; padding: 20px; color: #666; font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-btn">← 返回首页</a>
        <div class="header">
            <h1>📊 盘前纪要</h1>
            <div class="date">2026-05-29 周五</div>
        </div>
${sectionsHtml}
        <div class="footer">数据来源：韭研公社 · 仅供参考，不构成投资建议</div>
    </div>
    <script>
        function toggleSection(header) {
            const content = header.nextElementSibling;
            const toggle = header.querySelector('.toggle');
            content.classList.toggle('collapsed');
            toggle.classList.toggle('collapsed');
        }
    </script>
</body>
</html>`;

fs.writeFileSync('morning_brief_20260529.html', html, 'utf8');
console.log('Done! Written morning_brief_20260529.html');
