from flask import Blueprint

bp = Blueprint('labels', __name__, '/labels')


@bp.route('/submit')
def submit():
    return 'Submit Labels'
