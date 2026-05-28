# 设置Windows定时任务 - 每天15:30自动更新
$taskName = "QuantWebsiteAutoUpdate"
$scriptPath = "C:\Users\Administrator\Desktop\quant-showcase\update.bat"

# 删除旧任务（如果存在）
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# 创建新任务
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At "15:30"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "每日自动更新量化交易网站"

Write-Host "✅ 定时任务已创建！"
Write-Host "任务名称: $taskName"
Write-Host "执行时间: 每天 15:30"
Write-Host "脚本路径: $scriptPath"
