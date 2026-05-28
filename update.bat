@echo off
chcp 65001 >nul
echo ========================================
echo   量化交易网站自动更新脚本
echo ========================================
echo.

:: 设置路径
set SOURCE=C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer\output
set TARGET=C:\Users\Administrator\Desktop\quant-showcase
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%

echo [1/4] 复制最新报告文件...
if exist "%SOURCE%\account_snapshots\trade_analysis_%DATE%.html" (
    copy "%SOURCE%\account_snapshots\trade_analysis_%DATE%.html" "%TARGET%\reports\" >nul
    echo   ✓ 交易分析报告已更新
)

if exist "%SOURCE%\screen_%DATE%.html" (
    copy "%SOURCE%\screen_%DATE%.html" "%TARGET%\reports\" >nul
    echo   ✓ 选股报告已更新
)

if exist "%SOURCE%\review_%DATE%.html" (
    copy "%SOURCE%\review_%DATE%.html" "%TARGET%\reports\" >nul
    echo   ✓ 复盘报告已更新
)

if exist "%SOURCE%\monitor_%DATE%.html" (
    copy "%SOURCE%\monitor_%DATE%.html" "%TARGET%\reports\" >nul
    echo   ✓ 监控报告已更新
)

echo.
echo [2/5] 更新账户报告...
if exist "C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer\_pnl_report.html" (
    copy "C:\Users\Administrator\WorkBuddy\20260410111908\astock_analyzer\_pnl_report.html" "%TARGET%\pnl_report.html" >nul
    echo   ✓ 账户报告已更新
)

echo.
echo [3/5] 更新主页链接到今天的报告...
cd /d "%TARGET%"
powershell -Command "(Get-Content index.html) -replace 'trade_analysis_\d{8}', 'trade_analysis_%DATE%' -replace 'screen_\d{8}', 'screen_%DATE%' | Set-Content index.html"
powershell -Command "(Get-Content index.html) -replace 'review_\d{8}', 'review_%DATE%' -replace 'monitor_\d{8}', 'monitor_%DATE%' | Set-Content index.html"
echo   ✓ 主页链接已更新为 %DATE%

echo.
echo [4/5] 提交到Git...
cd /d "%TARGET%"
git add -A
git commit -m "Auto update: %DATE%" 2>nul
if %errorlevel%==0 (
    echo   ✓ Git提交成功
) else (
    echo   - 没有新的更改需要提交
)

echo.
echo [5/5] 推送到GitHub（Cloudflare Pages自动部署）...
git push origin main 2>nul
if %errorlevel%==0 (
    echo   ✓ GitHub推送成功
    echo   ✓ Cloudflare Pages会自动部署（1-2分钟）
) else (
    echo   ✗ GitHub推送失败
)

echo.
echo ========================================
echo   更新完成！
echo ========================================
echo.
echo 访问链接：
echo   Cloudflare: https://quant-showcase.pages.dev
echo   GitHub:     https://lzl369120783-svg.github.io/quant-showcase/
echo.
echo 注意：推送后Cloudflare Pages会自动部署，约1-2分钟生效
echo.
pause
