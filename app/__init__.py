from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@mysql/flask_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    with app.app_context():
        # 간단한 CRUD 테스트를 위한 엔드포인트 추가
        @app.route('/test-db')
        def test_db():
            try:
                # CREATE: 새로운 사용자 추가
                new_user = User(username='testuser', email='test@example.com', password='hashedpassword')
                db.session.add(new_user)
                db.session.commit()

                # READ: 사용자 조회
                user = User.query.filter_by(username='testuser').first()
                if not user:
                    return jsonify({"message": "User not found"}), 404

                # UPDATE: 사용자 이메일 업데이트
                user.email = 'newemail@example.com'
                db.session.commit()

                # DELETE: 사용자 삭제
                db.session.delete(user)
                db.session.commit()

                return jsonify({"message": "CRUD operations successful"}), 200

            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({"error": "Database error", "details": str(e)}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
    
        
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

    
    # 모델 임포트
    #from app.models.csm_models.models import News, Content, Comment
    #from app.models.hjw_models.models import User
    #from app.models.hyl_models.models import Question, Answer
    #from app.models.ssm_models.models import GameSolution
       
    return app

# News_table 모델 정의
class News(db.Model):
    __tablename__ = 'News_table'

    news_id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    auth = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
# Content_table 모델 정의
class Content(db.Model):
    __tablename__ = 'Content_table'

    content_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Comment_table 모델 정의
class Comment(db.Model):
    __tablename__ = 'Comment_table'

    comment_id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('Content_table.content_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User_table.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False) 

# User_table 모델 정의
class User(db.Model):
    __tablename__ = 'User_table'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
    last_login = db.Column(db.DateTime)

# Question_table 모델 정의
class Question(db.Model):
    __tablename__ = 'Question_table'

    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User_table.user_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

# Answer_table 모델 정의
class Answer(db.Model):
    __tablename__ = 'Answer_table'

    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question_table.question_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User_table.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    






    
