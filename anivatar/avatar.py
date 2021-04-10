from flask import Blueprint

bp = Blueprint('avatar', __name__, url_prefix='/avatar')


@bp.route('/generate')
def generate():
    return 'Generated Portrait'
