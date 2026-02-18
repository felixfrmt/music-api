import os

# Server socket
bind = "0.0.0.0:5000"
workers = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"


def on_starting(server):
    """Create DB tables before workers are forked."""
    from run import app
    from app.extensions import db
    with app.app_context():
        db.create_all()
        server.log.info("Database tables created (or already exist).")