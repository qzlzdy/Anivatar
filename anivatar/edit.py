import cv2 as cv
import json
import numpy as np

from flask import Blueprint, current_app, g, redirect, render_template, request, session, url_for

bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_avatar_path():
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

    filename = hash(json.dumps(output))
    avatar_path = url_for('static', filename='portrait/{}.png'.format(filename))
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
        rotate_arg = 0
    session['rotate_arg'] = rotate_arg + angle

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, dst)

    return redirect(url_for('.show'))


@bp.route('/lightness', methods=('POST',))
def lightness():
    lightness_value = int(request.form['lightness'])

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    img = img.astype('float32')
    img /= 255.0
    img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    img[:, :, 1] = (1.0 + lightness_value / 100.0) * img[:, :, 1]
    img[:, :, 1][img[:, :, 1] > 1] = 1
    img = cv.cvtColor(img, cv.COLOR_HLS2BGR)
    img *= 255

    lightness_arg = session.get('lightness_arg')
    if lightness_arg is None:
        lightness_arg = 0
    session['lightness_arg'] = lightness_arg + lightness_value

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/saturation', methods=('POST',))
def saturation():
    saturation_value = int(request.form['saturation'])

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    img = img.astype('float32')
    img /= 255.0
    img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    img[:, :, 2] = (1.0 + saturation_value / 100.0) * img[:, :, 2]
    img[:, :, 2][img[:, :, 2] > 1] = 1
    img = cv.cvtColor(img, cv.COLOR_HLS2BGR)
    img *= 255

    saturation_arg = session.get('saturation_arg')
    if saturation_arg is None:
        saturation_arg = 0
    session['saturation_arg'] = saturation_arg + saturation_value

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/contrast', methods=('POST',))
def contrast():
    contrast_value = int(request.form['contrast'])

    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    dst = np.zeros(img.shape, dtype='uint8')
    rows, cols = img.shape[:-1]
    for i in range(rows):
        for j in range(cols):
            lst = 0.1 * contrast_value * img[i, j]
            dst[i, j] = [int(ele) if ele < 255 else 255 for ele in lst]

    contrast_arg = session.get('contrast_arg')
    if contrast_arg is None:
        contrast_arg = 0
    session['contrast_arg'] = contrast_arg + contrast_value

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


def relief_filter(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    kernel = [[-1, 0], [0, 1]]
    rows, cols = img.shape
    dst = np.zeros(img.shape, dtype='uint8')
    for i in range(rows - 1):
        for j in range(cols - 1):
            V = np.sum(img[i:i + 2, j:j + 2] * kernel) + 128
            V = max(0, min(256, V))
            dst[i, j] = V
    return dst


def engraving_filter(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    kernel = [[1, 0], [0, -1]]
    rows, cols = img.shape
    dst = np.zeros(img.shape, dtype='uint8')
    for i in range(rows - 1):
        for j in range(cols - 1):
            V = np.sum(img[i:i + 2, j:j + 2] * kernel) + 128
            V = max(0, min(256, V))
            dst[i, j] = V
    return dst


def glass_filter(img_path):
    img = cv.imread(img_path)
    dst = np.zeros_like(img)
    rows, cols = img.shape[:-1]
    for i in range(rows - 5):
        for j in range(cols - 5):
            random_num = np.random.randint(0, 5)
            dst[i, j] = img[i + random_num, j + random_num]
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
    elif avatar_filter == 'relief':
        img = relief_filter(img_path)
    elif avatar_filter == 'engraving':
        img = engraving_filter(img_path)
    elif avatar_filter == 'glass':
        img = glass_filter(img_path)
    else:
        img = cv.imread(img_path)

    session['filter'] = avatar_filter

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/vertical', methods=('POST',))
def vertical():
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    img = cv.flip(img, 0)

    vertical_flag = session.get('vertical_flag')
    if vertical_flag is None:
        vertical_flag = False
    session['vertical_flag'] = not vertical_flag

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/horizontal', methods=('POST',))
def horizontal():
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    img = cv.imread(img_path)
    img = cv.flip(img, 1)

    horizontal_flag = session.get('horizontal_flag')
    if horizontal_flag is None:
        horizontal_flag = False
    session['horizontal_flag'] = not horizontal_flag

    load_avatar_path()
    img_path = current_app.config['ROOT_PATH'] + g.avatar_path
    cv.imwrite(img_path, img)

    return redirect(url_for('.show'))


@bp.route('/show')
def show():
    return render_template('edit.html', avatar_path=g.avatar_path)
