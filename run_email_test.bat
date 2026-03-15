@echo off
chcp 65001 >nul
echo ========================================
echo 邮件读取工具测试
echo ========================================
echo.

echo 激活虚拟环境...
call D:\project\ShitBot_bata\shitbot_env\Scripts\activate.bat

echo.
echo 运行测试脚本...
python D:\project\ShitBot_bata\test_email_reader.py

echo.
echo 测试完成
pause
