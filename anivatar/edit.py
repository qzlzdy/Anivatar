import cv2 as cv
import numpy as np

from flask import Blueprint, current_app, g, redirect, render_template, request, session, url_for

bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_avatar_path():
    stem = session['session_id']
    g.original_path = url_for('static', filename='portrait/{}-0-0-0.png'.format(stem))

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

    filter_arg = session.get('filter')
    if filter_arg is None:
        pass
    elif filter_arg == 'null':
        pass
    elif filter_arg == 'sketch':
        stem += '-s'
    elif filter_arg == 'nostalgia':
        stem += '-n'
    elif filter_arg == 'halo':
        stem += '-h'
    elif filter_arg == 'rising':
        stem += '-r'

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

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    rows, cols = img.shape[:-1]
    M = cv.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), angle, 1)
    dst = cv.warpAffine(img, M, (cols, rows))

    rotate_arg = session.get('rotate_arg')
    if rotate_arg is None:
        curr_angle = 0
    else:
        curr_angle = rotate_arg
    session['rotate_arg'] = curr_angle + angle

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, dst)

    return redirect(url_for('.show'))


@bp.route('/rotate-to', methods=('POST',))
def rotate_to():
    angle = int(request.form['angle'])

    img_path = current_app.config['ROOT_PATH'] + g.original_path
    img = cv.imread(img_path)
    rows, cols = img.shape[:-1]
    M = cv.getRotationMatrix2D(((rows - 1) / 2.0, (cols - 1) / 2.0), angle, 1)
    dst = cv.warpAffine(img, M, (cols, rows))

    session['rotate_arg'] = angle

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, dst)

    return redirect(url_for('.show'))


def sketch_filter(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (5, 5), 0)
    img = cv.Canny(img, 50, 150)
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    return img


def nostalgia_filter(img_path):
    img = cv.imread(img_path)
    dst = np.zeros(img.shape, dtype='uint8')
    rows, cols = img.shape[:-1]
    for i in range(rows):
        for j in range(cols):
            B = 0.272 * img[i, j][2] + 0.534 * img[i, j][1] + 0.131 * img[i, j][0]
            G = 0.349 * img[i, j][2] + 0.686 * img[i, j][1] + 0.168 * img[i, j][0]
            R = 0.393 * img[i, j][2] + 0.769 * img[i, j][1] + 0.189 * img[i, j][0]
            B = min(255, B)
            G = min(255, G)
            R = min(255, R)
            dst[i, j] = np.uint8((B, G, R))
    return dst


def halo_filter(img_path):
    img = cv.imread(img_path)
    rows, cols = img.shape[:-1]
    center_x = rows / 2
    center_y = cols / 2
    radius = min(center_x, center_y)
    dst = np.zeros(img.shape, dtype='uint8')
    for i in range(rows):
        for j in range(cols):
            distance = (center_x - i) ** 2 + (center_y - j) ** 2
            B = img[i, j][0]
            G = img[i, j][1]
            R = img[i, j][2]
            if distance < radius ** 2:
                result = int(100 * (1 - distance ** 0.5 / radius))
                B += result
                G += result
                R += result
                B = min(255, max(0, B))
                G = min(255, max(0, G))
                R = min(255, max(0, R))
            dst[i, j] = np.uint8((B, G, R))

    return dst


def rising_filter(img_path):
    img = cv.imread(img_path)
    dst = np.zeros(img.shape, dtype='uint8')
    rows, cols = img.shape[:-1]
    for i in range(rows):
        for j in range(cols):
            B = img[i, j][0] ** 0.5 * 12
            G = img[i, j][1]
            R = img[i, j][2]
            B = min(255, B)
            dst[i, j] = np.uint8((B, G, R))
    return dst


@bp.route('/filters', methods=('POST',))
def filters():
    avatar_filter = request.form['filter']

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    if avatar_filter == 'sketch':
        img = sketch_filter(img_path)
    elif avatar_filter == 'nostalgia':
        img = nostalgia_filter(img_path)
    elif avatar_filter == 'halo':
        img = halo_filter(img_path)
    elif avatar_filter == 'rising':
        img = rising_filter(img_path)
    else:
        img = cv.imread(img_path)

    session['filter'] = avatar_filter

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/show')
def show():
    return render_template('edit.html', avatar_path=g.avatar_path)
