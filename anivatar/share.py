from flask import Blueprint, render_template

bp = Blueprint('share', __name__, url_prefix='/share')


@bp.route('/download')
def download():
    return 'Download Image'


@bp.route('/summary')
def summary():
    return render_template('share.html')
