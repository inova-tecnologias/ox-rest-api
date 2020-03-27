from flask import Flask
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
from .config import app_config

jwt = JWTManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(
        app,
        supports_credentials=True,
        expose_headers=['X-Auth-Token',
                          'X-Refresh-Token',
                          'X-Total-Count',
                          'Content-Range']
    )
    
    from .beta import blueprint as beta
    app.register_blueprint(beta, url_prefix='/api')
    
    return app