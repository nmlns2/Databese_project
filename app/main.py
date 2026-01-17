from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, Memo, User 
from dotenv import load_dotenv
import os
from uuid import UUID
from datetime import datetime, timedelta, timezone
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-for-kanban-app') 

# --- SQLAlchemy設定 ---
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- ログイン管理の初期設定 ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

# --- ユーザー登録・ログイン・ログアウト（変更なし） ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('そのユーザー名は既に使用されています。', 'warning')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('登録完了！ログインしてください。', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('ユーザー名またはパスワードが違います。', 'warning')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- 1. 一覧表示（【修正】期限が近い順に並び替え） ---
@app.route('/')
@login_required
def index():
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    today = now.strftime('%Y-%m-%d')
    now_time = now.strftime('%H:%M')
    
    search_query = request.args.get('search', '')
    
    query = Memo.query.filter_by(user_id=current_user.id)
    if search_query:
        query = query.filter(Memo.title.ilike(f'%{search_query}%'))
    
    # 【変更箇所】期限(end_date)の昇順、その次に時間(end_time)の昇順で並べる
    all_memos = query.order_by(Memo.end_date.asc(), Memo.end_time.asc()).all()
    
    tasks = {'未着手': [], '進行中': [], '完了': [], '保留': []}
    for memo in all_memos:
        if memo.status in tasks:
            tasks[memo.status].append(memo)
            
    return render_template('index.html', tasks=tasks, today=today, now_time=now_time, search_query=search_query)

# --- 2. 詳細表示（変更なし） ---
@app.route('/memo/<uuid:memo_id>')
@login_required
def view_memo(memo_id):
    memo = Memo.query.filter_by(id=str(memo_id), user_id=current_user.id).first_or_404()
    return render_template('view_memo.html', memo=memo)

# --- 【新設】編集画面の表示 ---
@app.route('/memo/<uuid:memo_id>/edit', methods=['GET'])
@login_required
def edit_memo_form(memo_id):
    memo = Memo.query.filter_by(id=str(memo_id), user_id=current_user.id).first_or_404()
    return render_template('edit_memo.html', memo=memo)

# --- 【新設】編集内容の保存 ---
@app.route('/memo/<uuid:memo_id>/edit', methods=['POST'])
@login_required
def update_memo(memo_id):
    memo = Memo.query.filter_by(id=str(memo_id), user_id=current_user.id).first_or_404()
    
    memo.title = request.form['title']
    memo.content = request.form.get('content')
    memo.start_date = request.form['start_date']
    memo.start_time = request.form.get('start_time')
    memo.end_date = request.form['end_date']
    memo.end_time = request.form.get('end_time')
    memo.priority = request.form['priority']
    memo.status = request.form['status']
    
    db.session.commit()
    flash('タスクを更新しました！', 'success')
    return redirect(url_for('view_memo', memo_id=memo.id))

# --- 3. 新規作成フォーム表示（変更なし） ---
@app.route('/create', methods=['GET'])
@login_required
def show_create_memo():
    return render_template('create_memo.html')

# --- 4. 新規タスク作成（変更なし） ---
@app.route('/create', methods=['POST'])
@login_required
def create_memo():
    new_memo = Memo(
        title=request.form['title'],
        content=request.form.get('content'),
        start_date=request.form['start_date'],
        start_time=request.form.get('start_time'),
        end_date=request.form['end_date'],
        end_time=request.form.get('end_time'),
        priority=request.form['priority'],
        status='未着手',
        user_id=current_user.id
    )
    db.session.add(new_memo)
    db.session.commit()
    flash('新しいタスクを保存しました！', 'success')
    return redirect(url_for('index'))

# --- 5. ステータス更新（詳細画面用・変更なし） ---
@app.route('/memo/<uuid:memo_id>/update_status', methods=['POST'])
@login_required
def update_status(memo_id):
    memo = Memo.query.filter_by(id=str(memo_id), user_id=current_user.id).first_or_404()
    memo.status = request.form.get('status')
    db.session.commit()
    flash(f'ステータスを「{memo.status}」に更新しました。', 'info')
    return redirect(url_for('index'))

# --- 6. タスク削除（変更なし） ---
@app.route('/memo/<uuid:memo_id>/delete', methods=['POST'])
@login_required
def delete_memo(memo_id):
    memo = Memo.query.filter_by(id=str(memo_id), user_id=current_user.id).first_or_404()
    db.session.delete(memo)
    db.session.commit()
    flash('タスクを削除しました。', 'warning')
    return redirect(url_for('index'))

# --- 7. ドラッグ＆ドロップ用ステータス更新（変更なし） ---
@app.route('/update_status', methods=['POST'])
@login_required
def update_status_drag():
    data = request.get_json()
    memo = Memo.query.filter_by(id=data.get('id'), user_id=current_user.id).first()
    if memo:
        memo.status = data.get('status')
        db.session.commit()
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)