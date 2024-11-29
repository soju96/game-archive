from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

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