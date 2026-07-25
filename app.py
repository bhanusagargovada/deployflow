from flask import Flask
from config import DevelopmentConfig
from database import db, migrate, bcrypt, login_manager
from flask import after_this_request
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(config_class=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    if config_class is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    try:
        from routes.auth import auth_bp
        from routes.dashboard import dashboard_bp
        from routes.projects import projects_bp
        from routes.tasks import tasks_bp
        from routes.releases import releases_bp
        from routes.reports import reports_bp
        from routes.admin import admin_bp
        from routes.comments import comments_bp
        from routes.notifications import notifications_bp
        from routes.api import api_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(projects_bp)
        app.register_blueprint(tasks_bp)
        app.register_blueprint(releases_bp)
        app.register_blueprint(reports_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(comments_bp)
        app.register_blueprint(notifications_bp)
        app.register_blueprint(api_bp)
        from routes.profile import profile_bp
        from routes.settings import settings_bp
        app.register_blueprint(profile_bp)
        app.register_blueprint(settings_bp)
        from routes.exports import exports_bp
        app.register_blueprint(exports_bp)
    except Exception:
        # Blueprints may be added later during development
        pass

    # error handlers
    from flask import render_template

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    # If app is behind a proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app
