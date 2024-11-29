class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://game_user:secure_password@localhost/game_archive'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
