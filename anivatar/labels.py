import json

from flask import Blueprint, current_app, render_template

bp = Blueprint('labels', __name__, url_prefix='/labels')


@bp.route('/show')
def show():
    with open('core/tags.json', 'r') as f:
        tags = json.load(f)
    return render_template('labels.html', tags=tags)
