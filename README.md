# タスク管理ボード (Task Management Board)

このリポジトリは、FlaskとDocker、PostgreSQLを使用して作成された「タスク管理ボード」の完成版コードです。 以下の手順に従うだけで、すぐに自分のパソコンでタスク管理アプリを起動できます。

※ 予め Docker Desktop をインストールしておいてください。

## 🛠 使用技術
- Backend: Python 3.11, Flask, Flask-Login, Flask-SQLAlchemy
- Frontend: HTML5, CSS3 (Responsive Design), JavaScript, SortableJS, FontAwesome
- Database: PostgreSQL
- Infrastructure: Docker, Docker Compose

## 🚀 主な機能
- 個人アカウント機能: ユーザー登録とログインにより、自分専用のボードを保持できます。
- タスク追加・編集機能: 一度作成した課題の内容や期限、ステータスをいつでも修正可能です。
- 自動並び替え: 締切が近い順にタスクが自動で並ぶため、常に「今やるべきこと」が一番上に表示されます。
- スマホ完全対応（レスポンシブ）: 画面サイズに合わせてレイアウトが最適化。外出先でもスマホから快適に操作できます。
- パスワードセキュリティ: パスワードをハッシュ化してデータベースに保存する安全な設計です。
- ドラッグ&ドロップ: タスクを掴んで直感的に進捗（未着手〜完了）を更新。
- ダークモード対応: ワンクリックで目に優しいダークテーマに切り替え。
- 高機能検索: 課題名を入力するだけで、全ステータスから即座に絞り込み。
- 期限判定アラート:
  - 🔴 期限切れ！: 締切を過ぎた課題を赤字で警告。
  - 🟠 まもなく締切！: 当日が締切の課題をオレンジ色で強調。

 ## 📦 セットアップ方法
 
### 1. 設定ファイル（.env）の準備
アプリを動かすための「合言葉」を設定します。 プロジェクトのルートフォルダ（main.pyがある場所）に .env という名前のファイルを作成し、以下の内容を貼り付けてください。

API_PORT=3000

DB_PORT=5432

POSTGRES_USER=guest

POSTGRES_PASSWORD=password

POSTGRES_DB=guest

POSTGRES_HOST=db

### 2. アプリの起動
ターミナル（WindowsならPowerShell、Macならターミナル）を開き、以下のコマンドを打ち込みます。

docker-compose up --build

### 3.ブラウザでアクセス
起動完了後、ブラウザで以下の住所を入力してください。👉 http://localhost:3000 
※ 初回アクセス時は「新規登録」から自分のアカウントを作成してログインしてください。





