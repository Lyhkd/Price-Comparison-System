
import os
project_root = os.path.abspath(os.path.dirname(__file__))
os.environ['PROJECT_ROOT'] = project_root

from app import create_app, celery

app = create_app(db_init=False, register_celery_blueprint=True)

if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(rule)
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run()

    