# from flask import Blueprint, render_template

# bp = Blueprint('ssm', __name__, url_prefix='/ssm')

# @bp.route('/')
# def board():
#     return render_template('ssm/index.html')

# @bp.route('/detail')
# def question_detail(question_id):
#     return render_template('ssm/detail.html', question_id=question_id)

#공략 게시판 페이지
from flask import Blueprint, render_template
bp = Blueprint('ssm', __name__, url_prefix='/ssm')
@bp.route('/')
def index():
    return render_template('ssm/index.html')

# 질문 상세 페이지
@bp.route('ssm/guide_detail/<int:guide_id>')
def guide_detail(guide_id):
    # guide_id로 데이터 베이스 사용.
    return render_template('ssm/guide_detail.html', guide_id=guide_id)

# if __name__ == '__main__':
#     app.run(debug=True)