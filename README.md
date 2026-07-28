# 忖度ダイスボット

Discord で使える、少し偏った 10d100 を振る Bot です。

## 機能

### `/sd10`
- 10d100 を振ります
- 各ダイスは **65以上が約20%** の確率で出ます

### `/scd10`
- 10d100 を振ります
- 各ダイスは **30%の確率で 1〜5** のどれかが出ます
- 残り 70% は `6〜100` の範囲から出ます

## 必要環境

- Python 3.11 以上推奨
- Discord Bot Token

## セットアップ

```bash
python -m venv .venv
```

### Windows (cmd)

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

## 設定

`.env.example` を参考に `.env` を作成してください。

```env
DISCORD_BOT_TOKEN=your_bot_token_here
# 任意: テスト用サーバーですぐ同期したい場合のみ設定
DISCORD_GUILD_ID=123456789012345678
```

## 起動

```bash
python -m bot.main
```

または Windows では、同梱の `run_bot.bat` をダブルクリックして起動できます。

Linux / Oracle Cloud Free では、`run_bot.sh` でも起動できます。

起動後、Bot がオンラインになり、スラッシュコマンドが同期されます。

- `DISCORD_GUILD_ID` を設定した場合: そのサーバーへすぐ同期
- 未設定の場合: グローバル同期（反映まで少し時間がかかることがあります）

## テスト

```bash
python -m unittest discover -s tests -v
```

## Discord Developer Portal 設定手順

1. https://discord.com/developers/applications を開く
2. `New Application` を作成
3. `Bot` タブで Bot を追加
4. `Reset Token` または `Copy` で Token を取得
5. `OAuth2 > URL Generator` を開く
6. Scopes で以下を選択
   - `bot`
   - `applications.commands`
7. Bot Permissions は最低限なら以下で十分です
   - `Send Messages`
   - `Use Slash Commands`
8. 生成された URL でサーバーに招待

## 招待するだけで使える状態にするには

ローカル実行だけではなく、Bot を常時動かす必要があります。

### 自宅PCをサーバーとして使う場合

この Bot は **自宅PCから Discord へ接続し続ける** 方式で動きます。  
そのため、普通は **ポート開放不要** です。

ただし、次の条件を満たす必要があります。

- PC の電源が入っている
- インターネット接続がある
- Windows がスリープしていない
- `run_bot.bat` または `python -m bot.main` で Bot が起動している

この条件を満たしていれば、**他の人は招待URLから Bot をサーバーに追加するだけで利用可能**です。

おすすめ:
- Render
- Railway
- VPS
- Oracle Cloud Free

このリポジトリを公開環境に配置し、環境変数 `DISCORD_BOT_TOKEN` を設定してください。

## デプロイの考え方

### Oracle Cloud Free を使う場合

Oracle Cloud Free の VM（通常は Ubuntu）でも、**Bot 本体の仕様変更は不要**です。  
必要なのは、Linux 環境向けのセットアップと常駐化です。

この Bot は Web サーバーではなく **Discord へ常時接続するクライアント** として動くため、通常は **HTTP公開やポート開放は不要** です。

#### Oracle Cloud Free での基本セットアップ例

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone <このリポジトリのURL>
cd sikenn
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

その後、`.env` に `DISCORD_BOT_TOKEN` を設定してください。

#### 手動起動

```bash
chmod +x run_bot.sh
./run_bot.sh
```

#### 常駐化（推奨）

本番運用では `systemd` を使うのがおすすめです。  
このリポジトリには `deploy/sondaku-dice-bot.service` のサンプルを同梱しています。

配置例:

```bash
sudo cp deploy/sondaku-dice-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sondaku-dice-bot
sudo systemctl start sondaku-dice-bot
sudo systemctl status sondaku-dice-bot
```

#### systemd サービスファイルの修正ポイント

サービスファイル内の以下は、実際のサーバー環境に合わせて変更してください。

- `User=`
- `WorkingDirectory=`
- `ExecStart=`

たとえば Ubuntu ユーザー名が `ubuntu` なら、そのように書き換えます。

### 自宅PC常駐運用のおすすめ構成

- Start Command: `python -m bot.main`
- または `run_bot.bat`
- `.env` に `DISCORD_BOT_TOKEN` を設定
- 必要なら `.env` に `DISCORD_GUILD_ID` を設定

### Windows で常時使うための設定

#### 1. スリープを無効化
Bot はスリープ中に停止します。  
Windows の電源設定で、少なくとも Bot を動かすPCはスリープしないようにしてください。

#### 2. 起動時に自動で立ち上げる
おすすめは以下のどちらかです。

- **スタートアップフォルダ** に `run_bot.bat` のショートカットを入れる
- **タスクスケジューラ** でログオン時に `run_bot.bat` を実行する

#### 3. タスクスケジューラ例

- トリガー: `ログオン時`
- 操作: `プログラムの開始`
- プログラム/スクリプト: `cmd.exe`
- 引数の追加: `/c "C:\Users\セラク研修\Documents\sikenn\run_bot.bat"`

※ パスは実際の保存場所に合わせて変更してください。

#### 4. Bot を使う流れ

1. 自宅PCで Bot を起動しておく
2. Discord Developer Portal で OAuth2 招待URLを作る
3. その URL を開く
4. 追加したいサーバーを選ぶ
5. 招待完了後、`/sd10` と `/scd10` を使う

### 招待URLの作り方

Developer Portal の `OAuth2 > URL Generator` で次を選択してください。

- Scopes
  - `bot`
  - `applications.commands`
- Bot Permissions
  - `Send Messages`
  - `Use Slash Commands`

生成された URL を使えば、**サーバー管理権限を持つ人が招待するだけ**で導入できます。

### Render で動かす場合

Render では、この Bot のような **常時接続型アプリ** は Web API ではなく、
**Background Worker** または常時起動できる構成で動かすのが向いています。

#### 1. Render にリポジトリを接続
1. Render ダッシュボードで `New +` を開く
2. `Background Worker` を選ぶ
   - もし `Background Worker` が使えないプランの場合は、常時稼働できないため、
     Discord Bot にはあまり向きません
3. GitHub リポジトリを接続する

#### 2. Build / Start 設定
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m bot.main`

#### 3. 環境変数を設定
- `DISCORD_BOT_TOKEN` = Discord Bot Token
- 必要なら `DISCORD_GUILD_ID` = テスト用サーバー ID

#### 4. デプロイ後の確認
- Render のログで `Logged in as ...` が出ることを確認
- Discord サーバーで `/sd10` と `/scd10` を試す

#### 無料枠について
Render の Free 系は、プランやサービス種別によっては **スリープや再起動** が発生します。
Discord Bot は常時接続が必要なので、

- **まず試す**: Free 系で様子を見る
- **安定運用**: Hobby / 有料プランを推奨

#### Railway でもほぼ同様
- Start Command: `python -m bot.main`
- Environment Variable: `DISCORD_BOT_TOKEN`
- 任意で `DISCORD_GUILD_ID`

## ファイル構成

```text
.
├─ bot/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ dice.py
│  └─ main.py
├─ tests/
│  └─ test_dice.py
├─ deploy/
│  └─ sondaku-dice-bot.service
├─ .env.example
├─ requirements.txt
├─ run_bot.sh
└─ README.md
```

## 注意

- `/sd10` の「65以上が20%」は **確率的に約20%** です
- `/scd10` の「30%で1〜5」も **試行回数を重ねたときに概ね30%** になります
- 少ない回数では偏りが見た目どおりにならないことがあります
- 自宅PCの電源が落ちている間は Bot を使えません
- `.env` の Token は他人に共有しないでください
- Oracle Cloud Free では、VM 停止中は Bot も停止します