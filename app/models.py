from flask import Blueprint, render_template
from app import db  # SQLAlchemy 객체 가져오기

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('index.html')


