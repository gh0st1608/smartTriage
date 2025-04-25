from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    return app