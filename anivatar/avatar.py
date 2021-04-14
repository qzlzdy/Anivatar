import json
import subprocess

from flask import Blueprint, current_app, flash, session, redirect, render_template, request, url_for

bp = Blueprint('avatar', __name__, url_prefix='/avatar')


@bp.route('/generate', methods=('POST',))
def generate():
    labels = session.get('labels')
    if labels is None:
        labels = request.form.getlist('labels')
        labels = ','.join(labels)
        session['labels'] = labels

    truncation = session.get('truncation')
    if truncation is None:
        truncation = float(request.form['truncation'])
        session['truncation'] = truncation

    truncation_mean = session.get('truncation_mean')
    if truncation_mean is None:
        truncation_mean = int(request.form['truncation_mean'])
        session['truncation_mean'] = truncation_mean

    args = ['python', '{}/fake_generate.py'.format(current_app.config['ROOT_PATH'] + 'core')]
    if labels != '':
        args.append('--labels')
        args.append(labels)
    if truncation < 1:
        args.append('--truncation')
        args.append(str(truncation))
        args.append('--truncation_mean')
        args.append(str(truncation_mean))
    args.append('--output')
    # session_id, shift_x, shift_y, rotate_angle, filter
    output = [session['session_id'], 0, 0, 0, '']
    output = hash(json.dumps(output))
    args.append(str(output))
    subprocess.run(args)
    avatar_path = url_for('static', filename='portrait/{}.png'.format(output))
    return render_template('avatar.html', avatar_path=avatar_path)
