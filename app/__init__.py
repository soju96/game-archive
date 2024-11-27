from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        # Register blueprints
        from .views import main_views
        app.register_blueprint(main_views.bp)

    return app