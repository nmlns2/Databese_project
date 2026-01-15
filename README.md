このリポジトリは、FlaskとDocker、PostgreSQLを使用して作成された「タスク管理ボード」の完成版コードです。 以下の手順に従うだけで、すぐに自分のパソコンでタスク管理アプリを起動できます。

※ 予め Docker Desktop をインストールしておいてください。

🛠 使用技術
Backend: Python 3.9+, Flask

Database: PostgreSQL

Infrastructure: Docker, Docker Compose

Frontend: HTML5, CSS3, FontAwesome (CDN)

🚀 アプリの主な機能
Jooto風カンバンボード: 4つの列で課題の進捗を整理。

高機能検索: 課題名を入力するだけで即座に絞り込み。

期限判定アラート:

🔴 期限切れ！: 締切を1分でも過ぎると赤字で警告。

🟠 まもなく締切！: 今日が締切の課題をオレンジ色で強調。

通知機能: 保存・更新・削除時に画面上部へメッセージを表示。

📦 ステップ1：設定ファイル（.env）の準備
アプリを動かすための「合言葉」を設定します。 プロジェクトのルートフォルダ（main.pyがある場所）に .env という名前のファイルを作成し、以下の内容を貼り付けてください。

コード スニペット

# Database Settings
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=kanban_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
🏃‍♂️ ステップ2：アプリの起動方法
準備ができたら、ターミナル（WindowsならPowerShell、Macならターミナル）を開き、以下のコマンドを打ち込みます。

Bash

docker-compose up --build
「Successfully started」などの表示が出れば準備完了です！

🌐 ステップ3：ブラウザで開く
起動が終わったら、ブラウザ（Chromeなど）で以下の住所を入力してください。

👉 http://localhost:5000

これで、あなた専用の課題管理ボードが使い始められます！

💡 使い方のヒント
検索: 画面中央の検索窓に文字を入れると、全ての列から一致する課題を探します。

期限: 終了日付と時間を入力すると、システムが自動で今の時刻と比較して色を変えてくれます。

終了: ターミナルで Ctrl + C を押すとアプリを停止できます。





