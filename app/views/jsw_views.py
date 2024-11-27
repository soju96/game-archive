from flask import Blueprint, render_template

bp = Blueprint('jsw', __name__, url_prefix='/jsw')

@bp.route('/')
def index():
    return render_template('jsw/index.html')
