from flask import Blueprint, render_template
from .ksj_views import get_games  # 할인 관련 함수 가져오기

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # 할인 게임 데이터 가져오기
    games = get_games()

    # 최대 8개 게임만 메인 페이지에 표시
    highlighted_games = games[:12]

    return render_template(
        'common/main.html',
        highlighted_games=highlighted_games  # 메인에서 표시할 게임 데이터 전달
    )
