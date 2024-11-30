from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify, current_app, session
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.utils.jwt_utils import JWTUtils
import bcrypt, json

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
            # JWT 생성 (중복 제거)
            access_token, refresh_token = JWTUtils.generate_tokens(user.user_id)

            # 세션에 사용자 정보 저장
            session['user_id'] = user.user_id
            session['username'] = user.username

            # JWT를 쿠키에 저장
            response = make_response(redirect(url_for('main.index')))
            response.set_cookie('access_token', access_token, httponly=True, secure=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)

            return response

        flash("아이디 또는 비밀번호가 잘못되었습니다.", category="error")
        return render_template('hjw/index.html')

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
            error_password = "비밀번호가 일치하지 않습니다."

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

    # 데이터 유효성 검증
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Invalid data"}), 400

    username = data['username']
    password = data['password']

    # 데이터베이스에서 사용자 조회
    user = User.query.filter_by(username=username).first()

    # 로그인 검증
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # JWT 토큰 생성
        access_token, refresh_token = JWTUtils.generate_tokens(user.user_id)

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
    response = {
        "message": f"안녕하세요, 사용자 {current_user}님!"
    }
    return current_app.response_class(  # current_app으로 Flask 애플리케이션 객체 사용
        response=json.dumps(response, ensure_ascii=False),  # ensure_ascii=False로 한글 처리
        status=200,
        mimetype='application/json'
    )


# Refresh Token을 사용한 Access Token 갱신 API
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)

    # 새로운 Access Token을 쿠키에 저장
    response = jsonify({"message": "새 Access Token이 발급되었습니다."})
    response.set_cookie('access_token', new_access_token, httponly=True, secure=True)
    return response


@bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('hjw.index')))
    
    # 세션 초기화
    session.clear()

    # JWT 쿠키 제거
    response.delete_cookie('access_token', samesite='Strict')
    response.delete_cookie('refresh_token', samesite='Strict')

    flash("로그아웃되었습니다.", category="info")
    return response