from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()  # SQLAlchemy 객체 초기화
jwt = JWTManager()  # JWTManager 초기화


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    response = jsonify({"message": "Access Token이 만료되었습니다. 다시 로그인해주세요."})
    response.status_code = 401
    response.headers["Location"] = "/hjw"
    return response

@jwt.unauthorized_loader
def handle_unauthorized(error):
    response = jsonify({"message": "로그인하셔야 접근할 수 있습니다."})
    response.status_code = 401
    response.headers["Location"] = "/hjw"
    return response


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 데이터베이스 초기화
    db.init_app(app)


    jwt.init_app(app)  # JWT 초기화
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # JWT를 쿠키에서 찾도록 설정
    app.config['JWT_COOKIE_SECURE'] = False         # HTTPS가 아닌 환경에서도 쿠키 사용 가능 (개발용)
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'  # Access Token 쿠키 이름
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'  # Refresh Token 쿠키 이름
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # CSRF 보호 비활성화 (필요시 활성화)

    # 모델 불러오기 (명시적으로 추가)
    with app.app_context():
        from app import models  # 모델 가져오기



    # Import and register Blueprints
    from app.views.main_views import bp as main_bp
    from app.views.csm_views import bp as csm_bp
    from app.views.hjw_views import bp as hjw_bp
    from app.views.hyl_views import bp as hyl_bp
    from app.views.jsw_views import bp as jsw_bp
    from app.views.ksj_views import bp as ksj_bp
    from app.views.ssm_views import bp as ssm_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(csm_bp)
    app.register_blueprint(hjw_bp)
    app.register_blueprint(hyl_bp)
    app.register_blueprint(jsw_bp)
    app.register_blueprint(ksj_bp)
    app.register_blueprint(ssm_bp)

    return app