import os

from flask import Blueprint, current_app, session, render_template, request, url_for

bp = Blueprint('avatar', __name__, url_prefix='/avatar')


@bp.route('/generate', methods=('POST',))
def generate():
    labels = request.form.getlist('labels')
    labels = ','.join(labels)
    truncation = float(request.form['truncation'])
    truncation_mean = int(request.form['truncation_mean'])
    cmd = 'python {}/fake_generate.py'.format(current_app.config['ROOT_PATH'] + 'core')
    if labels != '':
        cmd += f' --labels {labels}'
    if truncation < 1:
        cmd += f' --truncation {truncation}'
        cmd += f' --truncation_mean {truncation_mean}'
    cmd += f' --output {session["session_id"]}'
    os.system(cmd)
    avatar_path = url_for('static', filename='portrait/{}-0-0.png'.format(session['session_id']))
    return render_template('avatar.html', avatar_path=avatar_path)
