import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Memo(db.Model):
    __tablename__ = 'memos'

    # IDは既存のUUID形式を維持
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # 課題のタイトル
    title = db.Column(db.String(100), nullable=False)
    
    # 詳細コメント（任意入力にするため nullable=True に変更）
    content = db.Column(db.Text, nullable=True)
    
    
    # 日付 (◯年◯月◯日〜◯年◯月◯日)
    start_date = db.Column(db.String(10), nullable=False) # 開始日 (例: 2026-01-15)
    end_date = db.Column(db.String(10), nullable=False)   # 終了日

    # --- 【追加】時間 ---
    start_time = db.Column(db.String(5), nullable=True) # HH:MM 形式
    end_time = db.Column(db.String(5), nullable=True)
    
    # 優先度 (高・中・低)
    priority = db.Column(db.String(10), nullable=False)
    
    # ステータス (未着手・進行中・完了・保留)
    # これが「どの列に表示するか」を決めます
    status = db.Column(db.String(20), default='未着手', nullable=False)
    
    # -----------------------------------------

    # 作成日時と更新日時（既存のものを維持）
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Memo {self.title}>'
