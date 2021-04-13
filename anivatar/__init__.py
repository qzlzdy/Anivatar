import os

from flask import Flask, render_template


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        ROOT_PATH='/home/qzlzdy/Python/Anivatar/anivatar/'
        # ROOT_PATH='/home/tlyang/gokurakujyoudo/src/Anivatar/anivatar/'
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    from . import labels, avatar, edit, share
    app.register_blueprint(labels.bp)
    app.register_blueprint(avatar.bp)
    app.register_blueprint(edit.bp)
    app.register_blueprint(share.bp)

    return app
