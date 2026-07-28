@echo off
cd /d %~dp0

if not exist .venv\Scripts\python.exe (
    echo [ERROR] .venv が見つかりません。
    echo 先に README の手順どおりに仮想環境を作成してください。
    pause
    exit /b 1
)

if not exist .env (
    echo [ERROR] .env が見つかりません。
    echo .env.example をコピーして .env を作成し、DISCORD_BOT_TOKEN を設定してください。
    pause
    exit /b 1
)

echo 忖度ダイスボットを起動します...
.venv\Scripts\python.exe -m bot.main

if errorlevel 1 (
    echo.
    echo [ERROR] Bot が異常終了しました。
    pause
)