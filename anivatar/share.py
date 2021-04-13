from flask import Blueprint, current_app, render_template, send_from_directory, session, url_for

bp = Blueprint('share', __name__, url_prefix='/share')


@bp.route('/download')
def download():
    stem = session['session_id']

    shift_arg = session.get('shift_arg')
    if shift_arg is None:
        stem += '-0-0'
    else:
        stem += f'-{shift_arg[0]}-{shift_arg[1]}'
    filename = '{}.png'.format(stem)
    return send_from_directory(current_app.config['ROOT_PATH'] + 'static/portrait', filename, as_attachment=True)


@bp.route('/summary')
def summary():
    stem = session['session_id']

    shift_arg = session.get('shift_arg')
    if shift_arg is None:
        stem += '-0-0'
    else:
        stem += f'-{shift_arg[0]}-{shift_arg[1]}'

    rotate_arg = session.get('rotate_arg')
    if rotate_arg is None:
        stem += '-0'
    else:
        stem += f'-{rotate_arg}'

    avatar_path = url_for('static', filename='portrait/{}.png'.format(stem))
    return render_template('share.html', avatar_path=avatar_path)
