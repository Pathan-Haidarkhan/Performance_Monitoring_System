from flask import Flask

from api import user_routes
from config import Config
from extensions import db, jwt, migrate
from utils.handlers import register_error_handlers, register_jwt_handlers
from utils.scheduler import start_scheduler
from api import *
from ui import ui_bp
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config.from_object(Config)


db.init_app(app)
jwt.init_app(app)
migrate.init_app(app,db)

register_error_handlers(app)
register_jwt_handlers(app)


app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(task_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(ui_bp)

with app.app_context():
    db.create_all()


# @app.route('/')
# def home():
#     return 'Performance Monitoring System!'


if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)