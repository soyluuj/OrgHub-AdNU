def register_blueprints(app):
    from .home import home_bp
    from .auth import auth_bp
    from .dashboard import dashboard_bp
    from .orders import orders_bp
    from .profile import profile_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(profile_bp)