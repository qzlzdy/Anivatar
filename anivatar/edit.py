from flask import Blueprint, render_template

bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.route('/crop', methods=('POST',))
def crop(start_x=0, start_y=0, end_x=512, end_y=512):
    image = (start_x, start_y, end_x, end_y)
    return 'Crop Image' + str(image)


@bp.route('/show')
def show():
    return render_template('edit.html', latent='example')
