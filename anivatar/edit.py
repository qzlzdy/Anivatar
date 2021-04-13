import cv2 as cv
import numpy as np

from flask import Blueprint, current_app, g, redirect, render_template, request, session, url_for

bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_avatar_path():
    stem = session['session_id']
    g.original_path = url_for('static', filename='portrait/{}-0-0.png'.format(stem))

    shift_arg = session.get('shift_arg')
    if shift_arg is None:
        stem += '-0-0'
    else:
        stem += f'-{shift_arg[0]}-{shift_arg[1]}'

    avatar_path = url_for('static', filename='portrait/{}.png'.format(stem))
    g.avatar_path = avatar_path


@bp.route('/shift', methods=('POST',))
def shift():
    shift_x = int(request.form['shift_x'])
    shift_y = int(request.form['shift_y'])

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    rows, cols = img.shape[:-1]
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    dst = cv.warpAffine(img, M, (cols, rows))

    curr_pos = session.get('shift_arg')
    if curr_pos is None:
        curr_x, curr_y = 0, 0
    else:
        curr_x, curr_y = curr_pos
    session['shift_arg'] = (curr_x + shift_x, curr_y + shift_y)

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, dst)

    return redirect(url_for('.show'))


@bp.route('/shift-to', methods=('POST',))
def shift_to():
    shift_x = int(request.form['shift_x'])
    shift_y = int(request.form['shift_y'])

    img_path = current_app.config['ROOT_PATH'] + g.original_path
    img = cv.imread(img_path)
    rows, cols = img.shape[:-1]
    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    dst = cv.warpAffine(img, M, (cols, rows))

    session['shift_arg'] = (shift_x, shift_y)

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, dst)

    return redirect(url_for('.show'))


@bp.route('/rotate', methods=('POST',))
def rotate():
    angle = int(request.form['angle'])
    return redirect(url_for('.show'))


@bp.route('/show')
def show():
    return render_template('edit.html', avatar_path=g.avatar_path)
