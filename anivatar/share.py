import json

from flask import Blueprint, current_app, g, render_template, send_from_directory, session, url_for

bp = Blueprint('share', __name__, url_prefix='/share')


@bp.before_request
def load_avatar_id():
    # session_id, shift_x, shift_y, rotate_angle, lightness, saturation, contrast, filter, vertical, horizontal
    output = [session['session_id'], 0, 0, 0, 0, 0, 10, '', False, False]

    shift_arg = session.get('shift_arg')
    if shift_arg is not None:
        output[1] = shift_arg[0]
        output[2] = shift_arg[1]

    rotate_arg = session.get('rotate_arg')
    if rotate_arg is not None:
        output[3] = rotate_arg

    lightness_arg = session.get('lightness_arg')
    if lightness_arg is not None:
        output[4] = lightness_arg

    saturation_arg = session.get('saturation_arg')
    if saturation_arg is not None:
        output[5] = saturation_arg

    contrast_arg = session.get('contrast_arg')
    if contrast_arg is not None:
        output[6] = contrast_arg

    filter_arg = session.get('filter')
    if filter_arg is None:
        pass
    elif filter_arg == 'null':
        pass
    elif filter_arg == 'sketch':
        output[7] = 's'
    elif filter_arg == 'nostalgia':
        output[7] = 'n'
    elif filter_arg == 'halo':
        output[7] = 'h'
    elif filter_arg == 'rising':
        output[7] = 'r'
    elif filter_arg == 'relief':
        output[7] = 'c'
    elif filter_arg == 'engraving':
        output[7] = 'e'
    elif filter_arg == 'glass':
        output[7] = 'g'

    vertical_flag = session.get('vertical_flag')
    if vertical_flag is not None:
        output[8] = vertical_flag

    horizontal_flag = session.get('horizontal_flag')
    if horizontal_flag is not None:
        output[9] = horizontal_flag

    g.avatar_id = hash(json.dumps(output))


@bp.route('/download')
def download():
    filename = '{}.png'.format(g.avatar_id)
    return send_from_directory(current_app.config['ROOT_PATH'] + 'static/portrait', filename, as_attachment=True)


@bp.route('/summary')
def summary():
    record_path = current_app.config['ROOT_PATH'] + url_for('static', filename='record.txt')
    with open(record_path, 'a') as f:
        f.write(str(g.avatar_id) + '\n')
    avatar_path = url_for('static', filename='portrait/{}.png'.format(g.avatar_id))
    return render_template('share.html', avatar_path=avatar_path)
