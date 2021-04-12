import json
import random

from flask import Blueprint, session, render_template

bp = Blueprint('labels', __name__, url_prefix='/labels')


@bp.route('/show')
def show():
    with open('core/tags.json', 'r') as f:
        tags = json.load(f)
    return render_template('labels.html', tags=tags)


@bp.before_app_first_request
def generate_user_id():
    session['user_id'] = random.getrandbits(32)
