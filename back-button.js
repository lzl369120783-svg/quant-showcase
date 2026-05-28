// 通用返回按钮脚本
(function() {
    // 等待页面加载完成
    window.addEventListener('load', function() {
        // 检查是否有toolbar，如果有则把返回按钮放到toolbar旁边
        const toolbar = document.querySelector('.toolbar');
        let topPos = '20px';

        if (toolbar) {
            // 如果有toolbar，返回按钮放在toolbar上方
            topPos = '10px';
        }

        // 创建返回按钮
        const backBtn = document.createElement('a');
        backBtn.href = '../index.html';
        backBtn.innerHTML = '← 返回首页';
        backBtn.style.cssText = `
            position: fixed;
            top: ${topPos};
            right: 20px;
            background: rgba(0, 212, 255, 0.2);
            color: #00D4FF;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            z-index: 10000;
            border: 1px solid rgba(0, 212, 255, 0.3);
            transition: all 0.3s;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        `;
        backBtn.onmouseover = function() {
            this.style.background = 'rgba(0, 212, 255, 0.3)';
            this.style.transform = 'translateX(-3px)';
        };
        backBtn.onmouseout = function() {
            this.style.background = 'rgba(0, 212, 255, 0.2)';
            this.style.transform = 'translateX(0)';
        };
        document.body.appendChild(backBtn);
    });
})();
