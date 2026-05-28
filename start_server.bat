@echo off
chcp 65001 >nul
echo ========================================
echo   实时监控服务器启动脚本
echo ========================================
echo.
echo 正在启动服务器...
echo 请勿关闭此窗口
echo.
cd /d "C:\Users\Administrator\Desktop\quant-showcase"
python realtime_server.py 8088
