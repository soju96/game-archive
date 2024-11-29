from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
import bcrypt

bp = Blueprint('hjw', __name__, url_prefix='/hjw')

# 로그인 페이지
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 데이터베이스에서 사용자 조회
        user = User.query.filter_by(username=username).first()

        # 로그인 검증
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            flash("로그인 성공!")  # Flash 메시지 전달
            return redirect(url_for('main.index'))  # 메인 화면으로 리다이렉트
        else:
            flash("아이디 또는 비밀번호가 잘못되었습니다.")
            return render_template('hjw/index.html')

    # GET 요청 처리
    return render_template('hjw/index.html')


# 회원가입 페이지
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
        elif User.query.filter_by(username=username).first():
            error_username = "이미 존재하는 아이디입니다."

        if password != confirm_password:
            error_password = "비밀번호와 비밀번호 확인이 일치하지 않습니다."

        # 오류가 없으면 사용자 등록
        if not error_username and not error_password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password=hashed_password.decode('utf-8'), email=email)
            db.session.add(new_user)
            db.session.commit()
            return render_template('hjw/signup.html', success=True)

        return render_template('hjw/signup.html', error_username=error_username, error_password=error_password)

    return render_template('hjw/signup.html')


# Access Token과 Refresh Token 발급 API
@bp.route('/tokens', methods=['POST'])
def tokens():
    data = request.get_json()  # 클라이언트로부터 JSON 데이터 받기
    username = data.get('username')
    password = data.get('password')

    # 데이터베이스에서 사용자 조회
    user = User.query.filter_by(username=username).first()

    # 로그인 검증
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))

        # 토큰 반환
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


# 보호된 리소스 접근 API
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"안녕하세요, 사용자 {current_user}님!"}), 200


# Refresh Token을 사용한 Access Token 갱신 API
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({
        "message": "새 Access Token이 발급되었습니다.",
        "access_token": new_access_token
    }), 200
