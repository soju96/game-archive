import requests
from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
import random
import string
import time
import threading
import logging

bp = Blueprint('ksj', __name__, url_prefix='/ksj')

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# 캐싱을 위한 전역 변수
cached_games = []
cache_expiry = 0
cache_lock = threading.Lock()

# Steam 게임 가져오기 (여러 카테고리 포함)
def get_games():
    global cached_games, cache_expiry
    with cache_lock:
        current_time = time.time()
        if current_time < cache_expiry:
            logging.info("캐시된 게임 데이터를 사용합니다.")
            return cached_games

        url = "https://store.steampowered.com/api/featuredcategories"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"API 호출 에러: {e}")
            return cached_games  # 이전 캐시 데이터를 반환하거나 빈 리스트 반환

        data = response.json()
        categories = ['specials', 'coming_soon', 'top_sellers', 'new_releases']
        games = []
        seen_game_ids = set()  # 중복 방지를 위한 집합

        for category in categories:
            items = data.get(category, {}).get("items", [])
            logging.info(f"카테고리 '{category}'의 게임 수: {len(items)}")
            for game in items:
                game_id = game.get("id")
                if not game_id:
                    continue  # ID가 없는 게임은 건너뜀
                if game_id in seen_game_ids:
                    continue  # 이미 추가된 게임은 건너뜀
                seen_game_ids.add(game_id)

                # 필수 필드 존재 여부 확인
                name = game.get("name", "Unknown")
                discount_percent = game.get("discount_percent", 0)
                original_price = game.get("original_price")
                final_price = game.get("final_price")
                image_url = game.get("large_capsule_image", "")
                category_name = category.replace('_', ' ').title()  # 카테고리 이름 추가

                # 가격 정보가 없는 경우 처리
                if original_price is None or final_price is None:
                    original_price_display = "무료"  # 또는 다른 기본값
                    final_price_display = "무료"
                else:
                    original_price_display = f"{int(original_price / 100):,}".replace(",", ".")  # 예: "1.500.000"
                    final_price_display = f"{int(final_price / 100):,}".replace(",", ".")  # 예: "1.350.000"

                games.append({
                    "id": game_id,
                    "name": name,
                    "discount_percent": discount_percent,
                    "original_price": original_price_display,
                    "final_price": final_price_display,
                    "image_url": image_url,
                    "category": category_name  # 카테고리 이름 추가
                })

        # 캐시 갱신 (예: 1시간 후 만료)
        cached_games = games
        cache_expiry = current_time + 3600  # 1시간
        logging.info(f"캐시된 게임 수: {len(games)}")
        return games

# 메인 페이지 라우트
@bp.route('/')
def index():
    # Steam 게임 리스트 가져오기
    games = get_games()

    # 필터 처리
    filter_type = request.args.get('filter', 'high')
    category_filter = request.args.get('category')  # 카테고리 필터 추가

    if filter_type == 'high':
        games = sorted(games, key=lambda x: x['discount_percent'], reverse=True)
    elif filter_type == 'low':
        games = sorted(games, key=lambda x: x['discount_percent'])

    if category_filter:
        games = [game for game in games if game['category'] == category_filter]

    # 페이지네이션 처리
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    paginated_games = games[start:end]
    total_pages = (len(games) + per_page - 1) // per_page

    return render_template(
        'ksj/index.html',
        games=paginated_games,
        filter_type=filter_type,
        category_filter=category_filter,
        current_page=page,
        total_pages=total_pages
    )

# 쿠폰 데이터 저장 (임시 저장소)
coupons = {
    "remaining": 100,  # 남은 쿠폰 수
    "generated_coupons": [],  # 발급된 쿠폰 리스트
    "reset_time": None  # 다음 리셋 시간
}

def reset_coupons():
    """매일 쿠폰 리셋 (100개 제한)"""
    coupons["remaining"] = 100
    coupons["generated_coupons"] = []
    coupons["reset_time"] = datetime.now() + timedelta(days=1)
    logging.info("쿠폰이 리셋되었습니다.")

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
        return {"error": "더 이상 쿠폰을 발급할 수 없습니다!"}, 400

    # 랜덤 쿠폰 생성
    coupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    coupons["generated_coupons"].append(coupon)
    coupons["remaining"] -= 1

    logging.info(f"쿠폰 발급: {coupon}")
    return {"coupon": coupon}
