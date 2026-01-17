import uuid
from flask_sqlalchemy import SQLAlchemy
# ログイン管理とセキュリティのための部品を追加
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- 1. ユーザー情報のテーブル (新規追加) ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # パスワードはそのまま保存せず、暗号化（ハッシュ化）して保存します
    password_hash = db.Column(db.String(256), nullable=False)
    
    # このユーザーが持っている課題リスト（1対多のリレーションシップ）
    memos = db.relationship('Memo', backref='author', lazy=True)

    def set_password(self, password):
        """パスワードを暗号化して保存する"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """入力されたパスワードが正しいか確認する"""
        return check_password_hash(self.password_hash, password)

# --- 2. 課題データのテーブル (user_idを追加) ---
class Memo(db.Model):
    __tablename__ = 'memos'

    # IDは既存のUUID形式を維持
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 課題のタイトル
    title = db.Column(db.String(100), nullable=False)
    
    # 詳細コメント
    content = db.Column(db.Text, nullable=True)
    
    # 日付
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)

    # 時間
    start_time = db.Column(db.String(5), nullable=True)
    end_time = db.Column(db.String(5), nullable=True)
    
    # 優先度
    priority = db.Column(db.String(10), nullable=False)
    
    # ステータス
    status = db.Column(db.String(20), default='未着手', nullable=False)
    
    # 作成日時と更新日時
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 【重要】誰の課題かを示すユーザーIDを追加（外部キー）
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Memo {self.title}>'