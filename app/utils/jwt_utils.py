from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta

class JWTUtils:
    @staticmethod
    def generate_tokens(identity):
        """Access Token과 Refresh Token 생성"""
        access_token = create_access_token(identity=str(identity))
        refresh_token = create_refresh_token(identity=str(identity))
        return access_token, refresh_token

    @staticmethod
    def get_identity_from_token():
        """JWT 토큰에서 사용자 ID 추출"""
        return get_jwt_identity()
