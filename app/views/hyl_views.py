from flask import Blueprint, render_template

bp = Blueprint('hyl', __name__, url_prefix='/hyl')

@bp.route('/')
def index():
    return render_template('hyl/index.html')

# 질문 게시판
@bp.route('/qna')
def qna():
    return render_template('hyl/qna.html')