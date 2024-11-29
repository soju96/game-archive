from flask import Blueprint, render_template, jsonify

bp = Blueprint('hyl', __name__, url_prefix='/hyl')


# 더미 데이터
questions = [
    {"id": 1, "title": "질문 더미 테스트 1", "author": "유저1", "views": 188},
    {"id": 2, "title": "질문 더미 테스트 2", "author": "유저2", "views": 125},
    {"id": 3, "title": "질문 더미 테스트 3", "author": "유저3", "views": 341},
    {"id": 4, "title": "질문 더미 테스트 4", "author": "유저4", "views": 301},
    {"id": 5, "title": "질문 더미 테스트 5", "author": "유저5", "views": 142},
    {"id": 6, "title": "질문 더미 테스트 6", "author": "유저6", "views": 505},
    {"id": 7, "title": "질문 더미 테스트 7", "author": "유저7", "views": 344},
    {"id": 8, "title": "질문 더미 테스트 8", "author": "유저8", "views": 413},
    {"id": 9, "title": "질문 더미 테스트 9", "author": "유저9", "views": 393},
    {"id": 10, "title": "질문 더미 테스트 10", "author": "유저10", "views": 455},
]

@bp.route('/')
def index():
    return render_template('hyl/index.html')

# 질문 게시판
@bp.route('/qna')
def qna():
    return render_template('hyl/qna.html')

@bp.route('/api/qna')
def api_questions():
    return jsonify(questions)  # JSON 데이터 반환

@bp.route('/qna/create')
def qna_create():
    return render_template('hyl/qna-create.html')