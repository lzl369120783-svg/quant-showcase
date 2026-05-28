// 从本地服务器加载实时数据
const SERVER_URL = 'http://localhost:8088';

async function loadRealtimeData() {
    try {
        const response = await fetch(`${SERVER_URL}/api/monitor?t=${Date.now()}`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ 已连接本地服务器');
            return data;
        }
    } catch (e) {
        console.log('⚠️ 本地服务器未连接，使用静态数据');
    }
}

// 每60秒刷新数据
setInterval(loadRealtimeData, 60000);
loadRealtimeData();
