from flask import Blueprint, render_template

bp = Blueprint('hyl', __name__, url_prefix='/hyl')

@bp.route('/')
def index():
    return render_template('hyl/index.html')
