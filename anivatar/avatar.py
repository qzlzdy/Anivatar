from flask import Blueprint, request, render_template

bp = Blueprint('avatar', __name__, url_prefix='/avatar')


@bp.route('/generate', methods=('POST',))
def generate():
    if 'labels' in request.form:
        labels = request.form.getlist('labels')
    else:
        labels = None
    truncation = float(request.form['truncation'])
    return render_template('avatar.html', latent='example')
