from flask import Blueprint

bp = Blueprint('edit', __name__, '/edit')


@bp.route('/crop', methods=('POST',))
def crop(start_x, start_y, end_x, end_y):
    image = (start_x, start_y, end_x, end_y)
    return 'Crop Image' + str(image)
