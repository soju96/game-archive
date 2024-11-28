# from flask import Blueprint, render_template

# bp = Blueprint('ssm', __name__, url_prefix='/ssm')

# @bp.route('/')
# def board():
#     return render_template('ssm/index.html')

# @bp.route('/detail')
# def question_detail(question_id):
#     return render_template('ssm/detail.html', question_id=question_id)

from flask import Blueprint, render_template
bp = Blueprint('ssm', __name__, url_prefix='/ssm')
@bp.route('/')
def index():
    return render_template('ssm/index.html')