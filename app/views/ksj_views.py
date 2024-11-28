import requests
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
import random
import string

bp = Blueprint('ksj', __name__, url_prefix='/ksj')

# Steam 할인 게임 가져오기
def get_discounted_games():
    url = "https://store.steampowered.com/api/featuredcategories"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        specials = data.get("specials", {}).get("items", [])
        games = []

        for game in specials:
            games.append({
                "id": game["id"],
                "name": game["name"],
                "discount_percent": game["discount_percent"],
                "original_price": int(game["original_price"] / 100),  # 가격은 센트 단위
                "final_price": int(game["final_price"] / 100),
                "image_url": game["large_capsule_image"]
            })

        return games
    else:
        return []

# 메인 페이지 라우트
@bp.route('/')
def index():
    # Steam 할인 게임 리스트 가져오기
    games = get_discounted_games()

    # 필터 처리
    filter_type = request.args.get('filter', 'high')
    if filter_type == 'high':
        games = sorted(games, key=lambda x: x['discount_percent'], reverse=True)
    elif filter_type == 'low':
        games = sorted(games, key=lambda x: x['discount_percent'])

    # 페이지네이션 처리
    page = int(request.args.get('page', 1))
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    paginated_games = games[start:end]
    total_pages = (len(games) + per_page - 1) // per_page

    return render_template(
        'ksj/index.html',
        games=paginated_games,
        filter_type=filter_type,
        current_page=page,
        total_pages=total_pages
    )


# 쿠폰 데이터 저장 (임시 저장소)
coupons = {
    "remaining": 10,  # 남은 쿠폰 수
    "generated_coupons": [],  # 발급된 쿠폰 리스트
    "reset_time": None  # 다음 리셋 시간
}

def reset_coupons():
    """매일 쿠폰 리셋 (100개 제한)"""
    coupons["remaining"] = 10
    coupons["generated_coupons"] = []
    coupons["reset_time"] = datetime.now() + timedelta(days=1)

@bp.route('/timedeal')
def timedeal():
    """타임딜 페이지"""
    now = datetime.now()

    # 리셋 시간 체크
    if not coupons["reset_time"] or now >= coupons["reset_time"]:
        reset_coupons()

    return render_template(
        'ksj/timedeal.html',
        remaining_coupons=coupons["remaining"],
        reset_time=coupons["reset_time"].strftime("%Y-%m-%d %H:%M:%S")
    )

@bp.route('/timedeal/coupon', methods=['POST'])
def generate_coupon():
    """쿠폰 발급"""
    if coupons["remaining"] <= 0:
        return {"error": "No more coupons available!"}, 400

    # 랜덤 쿠폰 생성
    coupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    coupons["generated_coupons"].append(coupon)
    coupons["remaining"] -= 1

    return {"coupon": coupon}

