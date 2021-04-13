import json
import os
import random

from flask import Blueprint, session, render_template

bp = Blueprint('labels', __name__, url_prefix='/labels')


@bp.route('/show')
def show():
    session.clear()
    session['session_id'] = str(random.getrandbits(32))
    with open(os.path.dirname(__file__) + '/core/tags.json', 'r') as f:
        tags = json.load(f)
    return render_template('labels.html', tags=tags)
