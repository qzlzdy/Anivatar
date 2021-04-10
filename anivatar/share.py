from flask import Blueprint

bp = Blueprint('share', __name__, '/share')


@bp.route('/download')
def download():
    return 'Download Image'
