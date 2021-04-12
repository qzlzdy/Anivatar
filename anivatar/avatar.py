from flask import Blueprint, session, render_template

bp = Blueprint('avatar', __name__, url_prefix='/avatar')


@bp.route('/generate', methods=('POST',))
def generate():

    return render_template('avatar.html', user_id=session['user_id'])
