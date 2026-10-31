from .home import home_bp
from .auth import auth_bp
from .auction import auction_bp
from .dashboard import dashboard_bp
from .profile import profile_bp


def register_blueprints(app):

    app.register_blueprint(home_bp)

    app.register_blueprint(auth_bp)

    app.register_blueprint(auction_bp)

    app.register_blueprint(dashboard_bp)

    app.register_blueprint(profile_bp)