#!/usr/bin/env bash
set -eu

cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
  echo "[ERROR] .venv が見つかりません。"
  echo "先に README の手順どおりに仮想環境を作成してください。"
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "[ERROR] .env が見つかりません。"
  echo ".env.example をコピーして .env を作成し、DISCORD_BOT_TOKEN を設定してください。"
  exit 1
fi

echo "忖度ダイスボットを起動します..."
exec .venv/bin/python -m bot.main