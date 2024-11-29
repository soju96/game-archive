# from flask import Blueprint, render_template

# bp = Blueprint('ssm', __name__, url_prefix='/ssm')

# @bp.route('/')
# def board():
#     return render_template('ssm/index.html')

# @bp.route('/detail')
# def question_detail(question_id):
#     return render_template('ssm/detail.html', question_id=question_id)

#공략 게시판 페이지
from flask import Blueprint, render_template, request, redirect, url_for, flash
bp = Blueprint('ssm', __name__, url_prefix='/ssm')

@bp.route('/')
def index():
     # 요청 파라미터로부터 현재 페이지 번호를 가져옴 (기본값은 1)
    current_page = request.args.get('page', 1, type=int)
    guides_per_page = 10  # 한 페이지당 10개의 게시글
    total_guides = 100  # 전체 게시글 수 (임시로 100개라고 가정)
    total_pages = (total_guides + guides_per_page - 1) // guides_per_page

    # 현재 페이지에 표시할 게시글의 범위 계산
    start_index = (current_page - 1) * guides_per_page + 1
    end_index = min(start_index + guides_per_page - 1, total_guides)
    # return render_template('ssm/index.html')
    return render_template(
        'ssm/index.html',
        current_page=current_page,
        total_pages=total_pages,
        start_index=start_index,
        end_index=end_index
    )
# 질문 등록 페이지 및 제출 처리
@bp.route('/submit_question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        # 입력받은 폼 데이터 처리
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        
        # 여기서 데이터베이스에 저장하는 로직을 추가하면 됨
        flash('질문이 성공적으로 등록되었습니다.')
        return redirect(url_for('ssm.index'))
    
    return render_template('ssm/submit_question.html')

# 질문 상세 페이지
@bp.route('ssm/guide_detail/<int:guide_id>')
def guide_detail(guide_id):
    # guide_id로 데이터 베이스 사용.
    return render_template('ssm/guide_detail.html', guide_id=guide_id)

# if __name__ == '__main__':
#     app.run(debug=True)