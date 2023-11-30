from flask import Flask
from controllers.MascotasController import mascotas_bp
from controllers.DuenoController import duenos_bp
from config.config import DevelpmentConfig, ProductionConfig
from flask_migrate import Migrate
from db import db, ma
from flask_cors import CORS


ACTIVE_ENDPOINTS = [('/mascotas',mascotas_bp),('/dueno',duenos_bp)]

def create_app(config=DevelpmentConfig):
    app = Flask(__name__)
    CORS(app)
    migrate = Migrate(app, db)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)    

    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    
    # Agregar los blueprints
    for url, blueprint in ACTIVE_ENDPOINTS:
        CORS(blueprint)
        app.register_blueprint(blueprint, url_prefix=url)

    return app


if __name__ == "__main__":
    app_flask = create_app()
    
    app_flask.run(host='0.0.0.0')
