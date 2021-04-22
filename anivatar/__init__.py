import cv2 as cv
import os

from flask import Flask, render_template, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # ROOT_PATH='/home/qzlzdy/Python/Anivatar/anivatar/'
        ROOT_PATH='/home/tlyang/gokurakujyoudo/src/Anivatar/anivatar/'
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

    @app.route('/gallery')
    def gallery():
        images = []
        record_path = app.config['ROOT_PATH'] + url_for('static', filename='record.txt')
        with open(record_path, 'r') as f:
            for desc in f:
                link_path = url_for('static', filename='portrait/{}.png'.format(desc[:-1]))
                pre_path = url_for('static', filename='portrait/pre{}.png'.format(desc[:-1]))
                img = cv.imread(app.config['ROOT_PATH'] + link_path)
                img = cv.resize(img, (128, 128))
                cv.imwrite(app.config['ROOT_PATH'] + pre_path, img)
                images.append({
                    'pre': pre_path,
                    'link': link_path,
                    'desc': desc[:10] + '...' if len(desc) > 10 else desc
                })
        return render_template('gallery.html', images=images)

    @app.route('/details')
    def details():
        return render_template('details.html')

    from . import labels, avatar, edit, share
    app.register_blueprint(labels.bp)
    app.register_blueprint(avatar.bp)
    app.register_blueprint(edit.bp)
    app.register_blueprint(share.bp)

    return app
