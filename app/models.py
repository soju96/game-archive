from flask import Blueprint, render_template
from app import db  # SQLAlchemy 객체 가져오기

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('index.html')


# SQLAlchemy 데이터베이스 모델 (User_table 구조 기반)
class User(db.Model):
    __tablename__ = 'user_table'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    last_login = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User {self.username}>"