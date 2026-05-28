// 通用返回按钮脚本
(function() {
    // 创建返回按钮
    const backBtn = document.createElement('a');
    backBtn.href = '../index.html';
    backBtn.innerHTML = '← 返回首页';
    backBtn.style.cssText = `
        position: fixed;
        top: 20px;
        left: 20px;
        background: rgba(0, 212, 255, 0.2);
        color: #00D4FF;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 14px;
        z-index: 9999;
        border: 1px solid rgba(0, 212, 255, 0.3);
        transition: all 0.3s;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `;
    backBtn.onmouseover = function() {
        this.style.background = 'rgba(0, 212, 255, 0.3)';
        this.style.transform = 'translateX(5px)';
    };
    backBtn.onmouseout = function() {
        this.style.background = 'rgba(0, 212, 255, 0.2)';
        this.style.transform = 'translateX(0)';
    };
    document.body.appendChild(backBtn);
})();
