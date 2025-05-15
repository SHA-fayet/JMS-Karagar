# app/__init__.py
from flask import Flask
from flask_mysqldb import MySQL
from .config import Config
from app.routes.alerts import start_scheduler  # Import only the scheduler start function

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)

    # Register blueprints AFTER initializing MySQL to prevent import issues
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.inmates import inmates_bp
    from .routes.visitors import visitors_bp
    from .routes.punishments import punishments_bp
    from .routes.transfers import transfers_bp
    from .routes.notifications import notifications_bp
    from .routes.cells import cells_bp
    from .routes.search import search_bp
    from .routes.visit_request import visit_request_bp
    from .routes.alerts import alerts_bp
    from .routes.work_assignments import work_assignments_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(inmates_bp)
    app.register_blueprint(visitors_bp)
    app.register_blueprint(punishments_bp)
    app.register_blueprint(transfers_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(cells_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(visit_request_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(work_assignments_bp)


    # ✅ Only start scheduler once
    start_scheduler()

    return app
