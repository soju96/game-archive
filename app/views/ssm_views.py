from flask import Blueprint, render_template

bp = Blueprint('ssm', __name__, url_prefix='/ssm')

@bp.route('/')
def index():
    return render_template('ssm/index.html')
