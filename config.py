from datetime import timedelta  # timedelta 모듈 임포트

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://game_user:secure_password@localhost/game_archive'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT 관련 설정
    JWT_SECRET_KEY = 'your-jwt-secret-key'  # JWT 서명에 사용할 비밀 키
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=15)  # Access Token 만료 시간
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=30)  # Refresh Token 만료 시간