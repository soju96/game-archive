from flask import Blueprint, render_template

bp = Blueprint('hjw', __name__, url_prefix='/hjw')

@bp.route('/')
def index():
    return render_template('hjw/index.html')
