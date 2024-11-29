from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User  # User 모델 가져오기
from app import db  # 데이터베이스 객체 가져오기
import bcrypt

bp = Blueprint('hjw', __name__, url_prefix='/hjw')


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 데이터베이스에서 사용자 조회
        user = User.query.filter_by(username=username).first()

        # 로그인 검증 (bcrypt로 비밀번호 비교)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return redirect(url_for('main.index'))  # 성공 시 대시보드로 리다이렉트
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.")  # 오류 메시지 표시
            return render_template('hjw/index.html')

    # GET 요청 처리 (로그인 화면 렌더링)
    return render_template('hjw/index.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        # 유효성 검사
        error_username = None
        error_password = None

        if len(username) < 3:
            error_username = "아이디는 최소 3글자 이상이어야 합니다."
        elif User.query.filter_by(username=username).first():  # 데이터베이스에서 사용자 중복 확인
            error_username = "이미 존재하는 아이디입니다."

        if password != confirm_password:
            error_password = "비밀번호와 비밀번호 확인이 일치하지 않습니다."

        # 오류가 없으면 사용자 등록
        if not error_username and not error_password:
            # bcrypt로 비밀번호 해시화
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password=hashed_password.decode('utf-8'), email=email)
            db.session.add(new_user)  # 새로운 사용자 데이터 추가
            db.session.commit()  # 변경 사항 저장
            return render_template('hjw/signup.html', success=True)  # 성공 플래그 전달

        # 오류가 있으면 다시 회원가입 페이지 렌더링
        return render_template('hjw/signup.html', error_username=error_username, error_password=error_password)

    # GET 요청: 회원가입 페이지 렌더링
    return render_template('hjw/signup.html')