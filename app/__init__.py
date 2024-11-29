from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # SQLAlchemy 객체 초기화


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 데이터베이스 초기화
    db.init_app(app)

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
