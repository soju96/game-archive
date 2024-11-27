from flask import Blueprint, render_template

bp = Blueprint('csm', __name__, url_prefix='/csm')

@bp.route('/')
def index():
    return render_template('csm/index.html')


