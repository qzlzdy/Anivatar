import json

from flask import Blueprint, current_app, render_template, send_from_directory, session, url_for

bp = Blueprint('share', __name__, url_prefix='/share')


@bp.route('/download')
def download():
    # session_id, zoom_factor, shift_x, shift_y, rotate_angle, filter
    output = [session['session_id'], 1, 0, 0, 0, '']
    filename = hash(json.dumps(output))
    g.original_path = url_for('static', filename='portrait/{}.png'.format(filename))

    zoom_arg = session.get('zoom_arg')
    if zoom_arg is not None:
        output[1] = zoom_arg

    shift_arg = session.get('shift_arg')
    if shift_arg is not None:
        output[2] = shift_arg[0]
        output[3] = shift_arg[1]

    rotate_arg = session.get('rotate_arg')
    if rotate_arg is not None:
        output[4] = rotate_arg

    filter_arg = session.get('filter')
    if filter_arg is None:
        pass
    elif filter_arg == 'null':
        pass
    elif filter_arg == 'sketch':
        output[5] = 's'
    elif filter_arg == 'nostalgia':
        output[5] = 'n'
    elif filter_arg == 'halo':
        output[5] = 'h'
    elif filter_arg == 'rising':
        output[5] = 'r'

    filename = '{}.png'.format(hash(json.dumps(output)))
    return send_from_directory(current_app.config['ROOT_PATH'] + 'static/portrait', filename, as_attachment=True)


@bp.route('/summary')
def summary():
    # session_id, zoom_factor, shift_x, shift_y, rotate_angle, filter
    output = [session['session_id'], 1, 0, 0, 0, '']

    zoom_arg = session.get('zoom_arg')
    if zoom_arg is not None:
        output[1] = zoom_arg

    shift_arg = session.get('shift_arg')
    if shift_arg is not None:
        output[2] = shift_arg[0]
        output[3] = shift_arg[1]

    rotate_arg = session.get('rotate_arg')
    if rotate_arg is not None:
        output[4] = rotate_arg

    filter_arg = session.get('filter')
    if filter_arg is None:
        pass
    elif filter_arg == 'null':
        pass
    elif filter_arg == 'sketch':
        output[5] = 's'
    elif filter_arg == 'nostalgia':
        output[5] = 'n'
    elif filter_arg == 'halo':
        output[5] = 'h'
    elif filter_arg == 'rising':
        output[5] = 'r'

    filename = hash(json.dumps(output))

    avatar_path = url_for('static', filename='portrait/{}.png'.format(filename))
    return render_template('share.html', avatar_path=avatar_path)
