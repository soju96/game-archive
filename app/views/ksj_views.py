from flask import Blueprint, render_template

bp = Blueprint('ksj', __name__, url_prefix='/ksj')

@bp.route('/')
def index():
    return render_template('ksj/index.html')
