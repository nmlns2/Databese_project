from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import db, Memo
from dotenv import load_dotenv
import os
from uuid import UUID
# timedelta と timezone を追加して時差を調整します
from datetime import datetime, timedelta, timezone

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)
app.secret_key = 'dev-secret-key-for-kanban-app' 

# SQLAlchemy設定
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# --- 1. 一覧表示（時差を考慮した修正版） ---
@app.route('/')
def index():
    # 日本時間 (UTC+9) 設定
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    today = now.strftime('%Y-%m-%d')
    now_time = now.strftime('%H:%M')
    
    # --- 検索ワードの取得 ---
    search_query = request.args.get('search', '') # URLの ?search=... を取得
    
    # データベースへの問い合わせ
    query = Memo.query
    if search_query:
        # タイトルに検索ワードが含まれているものだけに絞る (ilikeは大小文字を区別しない)
        query = query.filter(Memo.title.ilike(f'%{search_query}%'))
    
    all_memos = query.order_by(Memo.created_at.desc()).all()
    
    tasks = {'未着手': [], '進行中': [], '完了': [], '保留': []}
    for memo in all_memos:
        if memo.status in tasks:
            tasks[memo.status].append(memo)
            
    # search_query も HTML に返して、検索窓に文字を残せるようにする
    return render_template('index.html', tasks=tasks, today=today, now_time=now_time, search_query=search_query)

# --- 2. 詳細表示 ---
@app.route('/memo/<uuid:memo_id>')
def view_memo(memo_id):
    memo = Memo.query.get_or_404(str(memo_id))
    return render_template('view_memo.html', memo=memo)

# --- 3. 新規作成フォーム表示 ---
@app.route('/create', methods=['GET'])
def show_create_memo():
    return render_template('create_memo.html')

# --- 4. 新規タスク作成 ---
@app.route('/create', methods=['POST'])
def create_memo():
    new_memo = Memo(
        title=request.form['title'],
        content=request.form.get('content'),
        start_date=request.form['start_date'],
        start_time=request.form.get('start_time'),
        end_date=request.form['end_date'],
        end_time=request.form.get('end_time'),
        priority=request.form['priority'],
        status='未着手'
    )
    db.session.add(new_memo)
    db.session.commit()
    flash('新しいタスクを保存しました！', 'success')
    return redirect(url_for('index'))

# --- 5. ステータス更新 ---
@app.route('/memo/<uuid:memo_id>/update_status', methods=['POST'])
def update_status(memo_id):
    memo = Memo.query.get_or_404(str(memo_id))
    memo.status = request.form.get('status')
    db.session.commit()
    flash(f'ステータスを「{memo.status}」に更新しました。', 'info')
    return redirect(url_for('index'))

# --- 6. タスク削除 ---
@app.route('/memo/<uuid:memo_id>/delete', methods=['POST'])
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(str(memo_id))
    db.session.delete(memo)
    db.session.commit()
    flash('タスクを削除しました。', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)